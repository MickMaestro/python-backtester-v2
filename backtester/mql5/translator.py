"""Translate a parsed MQL5 program (:mod:`.nodes`) into Python source that
runs on :mod:`.runtime`.

The output mirrors the MQL5 source: the same globals, functions, classes and
statements, with MQL5 semantics made explicit where Python differs —
``_idiv`` for integer division, ``_int`` for double→int truncation, ``Box``
for scalars passed by reference, ``Arr`` for arrays (series indexing),
value-copy for structs, ``global`` declarations for module-level state.
"""

from __future__ import annotations

import keyword
import math
import re
from dataclasses import dataclass, field

from . import nodes as N
from .mqltypes import (
    BUILTIN_REFS, BUILTIN_RET, BUILTIN_STRUCT_FIELDS, CONVERTER, SIZEOF, SPECIAL_NAMES, SPECIAL_TYPES,
    elem, is_array, is_float, is_int, is_num, is_obj, is_ptr, obj_class,
)

PY_RESERVED = set(keyword.kwlist) | {
    "range", "float", "int", "str", "len", "list", "dict", "tuple", "min", "max", "abs", "isinstance",
    "object", "super", "type", "print", "sorted", "sum", "any", "all", "enumerate", "zip", "map",
    "filter", "iter", "next", "getattr", "setattr", "globals", "self", "bool", "id", "hash", "repr",
    "Exception", "NotImplementedError", "staticmethod", "classmethod", "property", "slice", "set",
    "math", "Box", "Arr",
}


class TranslateError(Exception):
    pass


def _sanitize(name: str) -> str:
    if name.isidentifier():
        return name
    out = []
    for i, ch in enumerate(name):
        ok = (ch + "a").isidentifier() if i == 0 else ("a" + ch).isidentifier()
        out.append(ch if ok else f"_u{ord(ch):x}_")
    s = "".join(out)
    return s if s.isidentifier() else "_" + s


def pyname(name: str) -> str:
    name = _sanitize(name)
    if name in PY_RESERVED or keyword.iskeyword(name):
        return name + "_"
    return name


def pyattr(name: str) -> str:
    name = _sanitize(name)
    if keyword.iskeyword(name) or name in ("self",):
        return name + "_"
    return name


@dataclass
class Var:
    name: str            # MQL name
    py: str              # python expression to reach it (name, self.x, Cls.x)
    type: str
    kind: str            # local | param | global | field | static_field | static_local | input
    boxed: bool = False  # access through .v
    ref: bool = False    # scalar reference parameter (access .v)
    cls: str = ""


@dataclass
class ClassInfo:
    name: str
    kind: str
    base: str | None
    decl: object
    fields: dict = field(default_factory=dict)        # name -> type
    field_decls: list = field(default_factory=list)
    static_fields: dict = field(default_factory=dict)  # name -> (type, VarDecl)
    methods: dict = field(default_factory=dict)       # name -> [FuncDecl]
    ctors: list = field(default_factory=list)
    dtor: object = None
    tparams: list = field(default_factory=list)
    nested_enums: list = field(default_factory=list)


@dataclass
class Report:
    warnings: list = field(default_factory=list)
    unsupported: list = field(default_factory=list)
    unknown_names: set = field(default_factory=set)
    unknown_funcs: set = field(default_factory=set)

    def warn(self, node, msg):
        self.warnings.append((getattr(node, "line", 0), msg))


class _Loop:
    __slots__ = ("kind", "step", "label")

    def __init__(self, kind, step=None):
        self.kind = kind          # loop | switch_simple | switch_exc
        self.step = step          # list of step lines to emit before 'continue'


class Translator:
    def __init__(self, program: N.Program, runtime_names: set[str], pp=None, enum_tables=None):
        self.prog = program
        self.rt = runtime_names
        self.pp = pp
        self.rep = Report()
        self.enum_tables = enum_tables or {}     # runtime enums: name -> {value: label}
        self.classes: dict[str, ClassInfo] = {}
        self.funcs: dict[str, list] = {}         # name -> [FuncDecl]
        self.func_py: dict[int, str] = {}        # id(FuncDecl) -> python name
        self.globals: dict[str, Var] = {}
        self.global_decls: list = []
        self.enums: dict[str, dict] = {}         # enum type -> {item: value}
        self.enum_items: dict[str, tuple] = {}   # item -> (enum, value)
        self.enum_decls: list = []
        self.typedefs: dict[str, object] = {}
        self.inputs: list = []
        self.static_locals: list = []            # (pyname, init_code)
        self._tmp = 0
        self.out: list[str] = []
        # function context
        self.scopes: list[dict] = []
        self.cur_cls: ClassInfo | None = None
        self.cur_func = None
        self.cur_ret = "void"
        self.cur_static = False
        self.func_globals: set[str] = set()
        self.loops: list[_Loop] = []
        self.boxed_locals: set[str] = set()
        self.local_names_used: set[str] = set()
        self.module_names: set[str] = set()
        self.local_type_maps: dict = {}
        self.skip_files: set = set()        # declarations from these files are imported, not emitted
        self.only_files: set | None = None  # library mode: emit only declarations from these files
        self.type_alias: dict = {}
        self.hoisted: set = set()

    # ================================================================ symbols

    def _local_classes(self, f):
        found = []

        def visit(n):
            if isinstance(n, N.DeclStmt):
                for d in n.decls:
                    if isinstance(d, N.ClassDecl) and not d.forward:
                        found.append(d)
            if isinstance(n, N.Node):
                for k in n.__slots__:
                    if k not in ("line", "file"):
                        visit(getattr(n, k, None))
            elif isinstance(n, (list, tuple)):
                for x in n:
                    visit(x)
        visit(f.body)
        return found

    def _hoist_local_classes(self):
        funcs = []
        for d in self.prog.decls:
            if isinstance(d, N.FuncDecl):
                funcs.append(d)
            elif isinstance(d, N.ClassDecl):
                funcs.extend(m for m in d.members if isinstance(m, N.FuncDecl))
        for f in funcs:
            if f.body is None:
                continue
            for c in self._local_classes(f):
                name = c.name
                if name in self.classes:
                    old = self.classes[name].decl
                    same = [(m.name, repr(m.type)) for m in old.members if isinstance(m, N.VarDecl)] == \
                        [(m.name, repr(m.type)) for m in c.members if isinstance(m, N.VarDecl)]
                    if same:
                        continue
                    new = f"{name}_{pyname(f.name)}"
                    self.local_type_maps.setdefault(id(f), {})[name] = new
                    c.name = new
                self._collect_decl(c)
                c.forward = False
                self.hoisted.add(id(c))

    def collect(self):
        for d in self.prog.decls:
            self._collect_decl(d)
        self._hoist_local_classes()
        # attach out-of-class method bodies
        for d in self.prog.decls:
            if isinstance(d, N.FuncDecl) and d.cls:
                ci = self.classes.get(d.cls)
                if ci is None:
                    self.rep.warn(d, f"method of unknown class {d.cls}")
                    continue
                if d.kind == "ctor":
                    self._attach(ci.ctors, d)
                elif d.kind == "dtor":
                    ci.dtor = d
                else:
                    self._attach(ci.methods.setdefault(d.name, []), d)
        for ci in self.classes.values():
            for k, lst in ci.methods.items():
                ci.methods[k] = [f for f in lst if not (f.body is None and any(
                    g is not f and len(g.params) == len(f.params) and g.body is not None for g in lst))]
        # functions: drop prototypes that have definitions
        for k, lst in self.funcs.items():
            self.funcs[k] = [f for f in lst if not (f.body is None and any(
                g is not f and self._same_sig(f, g) and g.body is not None for g in lst))]
        # python names for functions
        for k, lst in self.funcs.items():
            base = pyname(k)
            if k in self.rt or base in self.rt:
                base = base + "_u"
            if k in self.globals or k in self.classes:
                base = base + "_f"
            if len(lst) == 1:
                self.func_py[id(lst[0])] = base
            else:
                for i, f in enumerate(lst):
                    self.func_py[id(f)] = f"{base}_{i + 1}"
        self.module_names = set(self.globals) | set(self.funcs) | set(self.classes) | set(self.enum_items)

    def _same_sig(self, a, b):
        if len(a.params) != len(b.params):
            return False
        return all(self.tstr(p.type, p.dims) == self.tstr(q.type, q.dims) for p, q in zip(a.params, b.params))

    def _attach(self, lst, d):
        for i, f in enumerate(lst):
            if f.body is None and len(f.params) == len(d.params) and all(
                    self.tstr(p.type, p.dims) == self.tstr(q.type, q.dims) for p, q in zip(f.params, d.params)):
                d.static = d.static or f.static
                d.virtual = d.virtual or f.virtual
                # keep default values from the declaration
                for p, q in zip(f.params, d.params):
                    if q.default is None and p.default is not None:
                        q.default = p.default
                lst[i] = d
                return
        lst.append(d)

    def _collect_decl(self, d, cls: ClassInfo | None = None):
        if isinstance(d, N.EnumDecl):
            self._collect_enum(d)
        elif isinstance(d, N.ClassDecl):
            if d.forward:
                if d.name not in self.classes:
                    self.classes[d.name] = ClassInfo(d.name, d.kind, None, d)
                return
            base = d.base.name if d.base else None
            ci = ClassInfo(d.name, d.kind, base, d, tparams=d.tparams)
            old = self.classes.get(d.name)
            self.classes[d.name] = ci
            for m in d.members:
                if isinstance(m, N.VarDecl):
                    if "static" in m.storage:
                        ci.static_fields[m.name] = (self.tstr(m.type, m.dims), m)
                    else:
                        ci.fields[m.name] = self.tstr(m.type, m.dims)
                        ci.field_decls.append(m)
                elif isinstance(m, N.FuncDecl):
                    if m.kind == "ctor":
                        self._attach(ci.ctors, m)
                    elif m.kind == "dtor":
                        ci.dtor = m
                    else:
                        self._attach(ci.methods.setdefault(m.name, []), m)
                elif isinstance(m, N.EnumDecl):
                    self._collect_enum(m)
                    ci.nested_enums.append(m)
                elif isinstance(m, N.ClassDecl):
                    self._collect_decl(m)
                elif isinstance(m, N.Typedef):
                    self.typedefs[m.name] = m
        elif isinstance(d, N.FuncDecl):
            if d.cls:
                return
            self.funcs.setdefault(d.name, [])
            self._attach(self.funcs[d.name], d)
        elif isinstance(d, N.VarDecl):
            if "static_def" in d.storage:
                cls_name = next((s[4:] for s in d.storage if s.startswith("cls:")), None)
                ci = self.classes.get(cls_name)
                if ci is not None:
                    t = ci.static_fields.get(d.name, (self.tstr(d.type, d.dims), d))[0]
                    ci.static_fields[d.name] = (t, d)
                return
            t = self.tstr(d.type, d.dims)
            kind = "input" if ("input" in d.storage or "sinput" in d.storage) else "global"
            pn = pyname(d.name)
            if d.name in self.rt or pn in self.rt:
                pn = pn + "_v"
            v = Var(d.name, pn, t, kind)
            self.globals[d.name] = v
            self.global_decls.append(d)
            if kind == "input":
                self.inputs.append(d)
        elif isinstance(d, N.Typedef):
            self.typedefs[d.name] = d
        elif isinstance(d, N.Program):
            pass

    def _collect_enum(self, d):
        vals = {}
        cur = -1
        for item in d.items:
            name, expr = item[0], item[1]
            if expr is not None:
                v = self.const_eval(expr)
                if v is None:
                    v = cur + 1
                    self.rep.warn(d, f"enum value of {name} not constant")
                cur = int(v)
            else:
                cur += 1
            vals[name] = cur
            self.enum_items[name] = (d.name, cur)
        if d.name:
            self.enums[d.name] = vals
        self.enum_decls.append(d)

    def const_eval(self, e):
        """Evaluate a constant integer/float expression (enum values, array sizes)."""
        try:
            return self._ce(e)
        except Exception:
            return None

    def _ce(self, e):
        if isinstance(e, N.Num):
            return e.value
        if isinstance(e, N.Char):
            return e.value
        if isinstance(e, N.Name):
            if e.id in self.enum_items:
                return self.enum_items[e.id][1]
            g = self.globals.get(e.id)
            if g is not None:
                for d in self.global_decls:
                    if d.name == e.id and d.init is not None and ("const" in d.storage or "input" in d.storage
                                                                     or "sinput" in d.storage):
                        return self._ce(d.init)
            from . import rt_consts
            if e.id in rt_consts.CONSTS:
                return rt_consts.CONSTS[e.id]
            raise ValueError(e.id)
        if isinstance(e, N.Unary):
            v = self._ce(e.e)
            return {"-": -v, "+": v, "~": ~int(v), "!": int(not v)}[e.op]
        if isinstance(e, N.Binary):
            a, b = self._ce(e.l), self._ce(e.r)
            op = e.op
            if op == "/":
                return int(a / b) if isinstance(a, int) and isinstance(b, int) else a / b
            if op == "%":
                return int(math.fmod(a, b))
            return {"+": a + b, "-": a - b, "*": a * b, "<<": a << b, ">>": a >> b, "|": a | b,
                    "&": a & b, "^": a ^ b, "==": int(a == b), "!=": int(a != b), "<": int(a < b),
                    ">": int(a > b), "<=": int(a <= b), ">=": int(a >= b), "&&": int(a and b),
                    "||": int(a or b)}[op]
        if isinstance(e, N.Cast):
            v = self._ce(e.e)
            return int(v) if e.type.name not in ("double", "float") else float(v)
        if isinstance(e, N.Ternary):
            return self._ce(e.a) if self._ce(e.cond) else self._ce(e.b)
        if isinstance(e, N.Sizeof):
            return 8
        raise ValueError("non-const")

    # ================================================================ types

    def tstr(self, ts: N.TypeSpec, dims=None) -> str:
        """Static type string of a declaration."""
        if ts is None:
            return "?"
        n = self.type_alias.get(ts.name, ts.name)
        if n in self.typedefs and isinstance(self.typedefs[n], N.Typedef) and self.typedefs[n].func_params is None:
            td = self.typedefs[n]
            base = self.tstr(td.type)
        elif n in ("double", "float", "int", "uint", "long", "ulong", "short", "ushort", "char", "uchar",
                   "bool", "datetime", "color", "string", "void"):
            base = n
        elif n in self.enums or n.startswith("ENUM_"):
            base = "enum:" + n
        elif n in self.classes or n in BUILTIN_STRUCT_FIELDS:
            base = ("P:" if ts.pointer else "C:") + n
        elif n in self.typedefs:
            base = "fn:" + n
        elif self.cur_cls is not None and n in self.cur_cls.tparams:
            base = "T"
        else:
            base = ("P:" if ts.pointer else "C:") + n if n[:1].isupper() and n not in ("T",) else "T"
        if base == "T":
            base = "?"
        return base + "[]" * len(dims or [])

    def default_value(self, t: str) -> str:
        if t == "string":
            return '""'
        if t == "bool":
            return "False"
        if is_float(t):
            return "0.0"
        if is_int(t):
            return "0"
        if is_ptr(t) or t.startswith("fn:"):
            return "None"
        if is_obj(t):
            c = obj_class(t)
            return f"{self.cls_py(c)}()"
        return "0"

    def cls_py(self, c: str) -> str:
        return pyname(c) if c not in ("MqlRates", "MqlDateTime", "MqlTick", "MqlParam", "MqlBookInfo") else c

    def fill_of(self, t: str) -> str:
        return {"string": '""', "bool": "False"}.get(t, "0.0" if is_float(t) else ("None" if (is_ptr(t) or t == "?" or t.startswith("fn:")) else "0"))

    def new_array_code(self, t: str, dims: list, init=None) -> str:
        """Arr(...) for a declaration with type `t` (element type) and dims."""
        et = t
        while et.endswith("[]"):
            et = et[:-2]
        fill = self.fill_of(et)
        factory = None
        if is_obj(et) and not is_ptr(et):
            factory = self.cls_py(obj_class(et))
            if obj_class(et) not in self.classes and obj_class(et) not in BUILTIN_STRUCT_FIELDS:
                factory = None
        first = dims[0] if dims else None
        inner = []
        for d in dims[1:]:
            v = self.const_eval(d) if d is not None else 0
            inner.append(str(v) if v is not None else self.ex(d)[0])
        args = []
        if init is not None and isinstance(init, N.InitList):
            items = self.initlist_code(init, et)
            size = None
            if first is not None:
                v = self.const_eval(first)
                size = str(v) if v is not None else self.ex(first)[0]
            parts = [items, f"fill={fill}"]
            if first is not None:
                parts.append("dyn=False")
            if factory:
                parts.append(f"factory={factory}")
            if size:
                parts.append(f"size={size}")
            if inner:
                parts.append(f"dims=({', '.join(inner)},)")
            return f"Arr.of({', '.join(parts)})"
        if first is None:
            args.append("0")
        else:
            v = self.const_eval(first)
            args.append(str(int(v)) if v is not None else self.ex(first)[0])
        args.append(fill)
        if first is not None:
            args.append("dyn=False")
        if factory:
            args.append(f"factory={factory}")
        if inner:
            args.append(f"dims=({', '.join(inner)},)")
        return f"Arr({', '.join(args)})"

    def initlist_code(self, il, et):
        parts = []
        for it in il.items:
            if isinstance(it, N.InitList):
                parts.append(self.initlist_code(it, et))
            else:
                c, t = self.ex(it)[:2]
                parts.append(self.conv(c, t, et))
        return "[" + ", ".join(parts) + "]"

    # ================================================================ output

    def emit(self, line: str, ind: int):
        self.out.append("    " * ind + line)

    def tmp(self, prefix="_t"):
        self._tmp += 1
        return f"{prefix}{self._tmp}"

    # ================================================================ program

    def emits(self, node) -> bool:
        f = getattr(node, "file", None)
        if f in self.skip_files:
            return False
        if self.only_files is not None and f not in self.only_files:
            return False
        return True

    def state_issues(self, files: set) -> list[str]:
        """Why declarations from `files` could not live in a shared module."""
        issues = []
        for d in self.global_decls:
            if d.file in files and "const" not in d.storage and "input" not in d.storage:
                issues.append(f"global variable {d.name}")
        for ci in self.classes.values():
            if getattr(ci.decl, "file", None) in files:
                for nm, (t, d) in ci.static_fields.items():
                    if "const" not in d.storage:
                        issues.append(f"static member {ci.name}::{nm}")

        def has_static(n):
            if isinstance(n, N.DeclStmt):
                if any(isinstance(d, N.VarDecl) and "static" in d.storage for d in n.decls):
                    return True
            if isinstance(n, N.Node):
                return any(has_static(getattr(n, k, None)) for k in n.__slots__ if k not in ("line", "file"))
            if isinstance(n, (list, tuple)):
                return any(has_static(x) for x in n)
            return False
        funcs = [f for lst in self.funcs.values() for f in lst]
        for ci in self.classes.values():
            funcs.extend(f for lst in ci.methods.values() for f in lst)
            funcs.extend(ci.ctors)
        for f in funcs:
            if getattr(f, "file", None) in files and f.body is not None and has_static(f.body):
                issues.append(f"static local in {f.name}")
        return issues

    def translate(self) -> str:
        self.collect()
        out = self.out
        # enums
        for d in self.enum_decls:
            if not d.items or not self.emits(d):
                continue
            label = f"enum {d.name}" if d.name else "enum"
            out.append(f"# {label}")
            names = []
            for item in d.items:
                nm = item[0]
                val = self.enum_items[nm][1] if self.enum_items.get(nm, (None,))[0] == d.name else None
                if val is None:
                    continue
                out.append(f"{pyname(nm)} = {val}")
                names.append((nm, val, item[2] if len(item) > 2 else ""))
            if d.name:
                tbl = ", ".join(f"{v}: {n!r}" for n, v, _c in names)
                out.append(f"_enum({d.name!r}, {{{tbl}}})")
            out.append("")
        # simple globals first (inputs, consts, literals)
        simple, complex_ = [], []
        for d in self.global_decls:
            if self.emits(d):
                (simple if self._is_simple_global(d) else complex_).append(d)
        if simple:
            out.append("# ---- inputs and global variables")
        for d in simple:
            self.global_var(d)
        # classes in dependency order
        for ci in self._class_order():
            if not self.emits(ci.decl):
                continue
            out.append("")
            self.translate_class(ci)
        # functions
        for name, lst in self.funcs.items():
            for f in lst:
                if not self.emits(f):
                    continue
                if f.imported:
                    out.append("")
                    out.append(f"def {self.func_py[id(f)]}(*args):")
                    out.append(f"    raise NotImplementedError({('DLL/library function ' + name + ' from ' + f.imported)!r})")
                    self.rep.unsupported.append(f"imported function {name} ({f.imported})")
                    continue
                if f.body is None:
                    self.rep.warn(f, f"function {name} declared but not defined")
                    out.append("")
                    out.append(f"def {self.func_py[id(f)]}(*args):")
                    out.append(f"    raise NotImplementedError({('function ' + name + ' has no body')!r})")
                    continue
                out.append("")
                self.translate_function(f, None)
        if complex_:
            out.append("")
            out.append("# ---- global variables initialised from expressions")
            for d in complex_:
                self.global_var(d)
        if self.static_locals:
            out.append("")
            out.append("# ---- static local variables")
            for name, code in self.static_locals:
                out.append(f"{name} = {code}")
        return "\n".join(out)

    def _is_simple_global(self, d):
        t = self.tstr(d.type, d.dims)
        et = t.rstrip("[]")
        if is_obj(et) and not is_ptr(et):
            return False
        if d.init is None and d.ctor_args is None:
            return True
        if isinstance(d.init, N.InitList):
            return all(self.const_eval(x) is not None or isinstance(x, (N.Str, N.InitList)) for x in d.init.items)
        if isinstance(d.init, (N.Num, N.Str, N.Char)):
            return True
        return self.const_eval(d.init) is not None

    def _class_order(self):
        done, order = set(), []

        def visit(ci, stack=()):
            if ci.name in done or ci.name in stack:
                return
            if ci.base and ci.base in self.classes:
                visit(self.classes[ci.base], stack + (ci.name,))
            # value members of class type must exist when __init__ runs (not at def time) -> no dep
            done.add(ci.name)
            order.append(ci)
        for ci in self.classes.values():
            visit(ci)
        return order

    def global_var(self, d):
        v = self.globals[d.name]
        t = v.type
        comment = f"  # {d.comment}" if d.comment and len(d.comment) < 120 else ""
        if is_obj(t) and not is_ptr(t) and not d.dims and d.init is None and obj_class(t) in self.classes:
            # allocate first, then construct: a constructor may refer to the object itself
            cls = self.cls_py(obj_class(t))
            args = self.call_args_for_ctor(obj_class(t), d.ctor_args) if d.ctor_args else ""
            self.out.append(f"{v.py} = _alloc({cls}){comment}")
            self.out.append(f"{v.py}.__init__({args})")
            return
        code = self.init_code(d, t)
        if v.kind == "input":
            code = f"_input({v.py!r}, {code})"
        self.out.append(f"{v.py} = {code}{comment}")

    def init_code(self, d, t) -> str:
        """Initial value for a variable declaration of type t."""
        if d.dims:
            return self.new_array_code(t, d.dims, d.init)
        if d.ctor_args is not None and is_obj(t):
            args = self.call_args_for_ctor(obj_class(t), d.ctor_args)
            return f"{self.cls_py(obj_class(t))}({args})"
        if d.init is None:
            return self.default_value(t)
        if isinstance(d.init, N.InitList):
            if is_obj(t) and not is_ptr(t):
                c = obj_class(t)
                vals = [self.ex(x)[0] if not isinstance(x, N.InitList) else self.initlist_code(x, "?")
                        for x in d.init.items]
                return f"_struct_init({self.cls_py(c)}(), [{', '.join(vals)}])"
            if d.init.items:
                c, et = self.ex(d.init.items[0])[:2]
                return self.conv(c, et, t)
            return self.default_value(t)
        c, et = self.ex(d.init)[:2]
        if is_obj(t) and not is_ptr(t):
            return f"_copy({c})" if self._is_lvalue(d.init) else c
        return self.conv(c, et, t)

    def _is_lvalue(self, e):
        return isinstance(e, (N.Name, N.Index, N.Member, N.Scope, N.This))

    # ================================================================ classes

    def all_fields(self, ci: ClassInfo) -> dict:
        res = {}
        chain = []
        c = ci
        seen = set()
        while c is not None and c.name not in seen:
            seen.add(c.name)
            chain.append(c)
            c = self.classes.get(c.base) if c.base else None
        for c in reversed(chain):
            res.update(c.fields)
        return res

    def find_field(self, cname: str, fname: str):
        """(type, static, owner_class) of a field of class `cname`, searching bases."""
        if cname in BUILTIN_STRUCT_FIELDS:
            t = BUILTIN_STRUCT_FIELDS[cname].get(fname)
            return (t, False, cname) if t else None
        c = self.classes.get(cname)
        seen = set()
        while c is not None and c.name not in seen:
            seen.add(c.name)
            if fname in c.fields:
                return c.fields[fname], False, c.name
            if fname in c.static_fields:
                return c.static_fields[fname][0], True, c.name
            c = self.classes.get(c.base) if c.base else None
        return None

    def find_methods(self, cname: str, mname: str):
        c = self.classes.get(cname)
        seen = set()
        while c is not None and c.name not in seen:
            seen.add(c.name)
            if mname in c.methods:
                return c.methods[mname], c.name
            c = self.classes.get(c.base) if c.base else None
        return None, None

    def method_py(self, cname, f, overloads=None):
        """Python name of a method, mangled when overloaded in its class."""
        ci = self.classes.get(cname)
        lst = overloads
        if lst is None and ci is not None:
            lst = ci.methods.get(f.name, [f])
        name = f.name
        if name.startswith("operator"):
            return OPERATOR_METHODS.get(name[8:].strip(), "_q_op")
        base = pyattr(name)
        if lst and len(lst) > 1:
            # mangle by arity when unique, else by position
            ar = [len(g.params) for g in lst]
            if ar.count(len(f.params)) == 1:
                return f"{base}_{len(f.params)}"
            return f"{base}_{lst.index(f) + 1}" if f in lst else base
        return base

    def translate_class(self, ci: ClassInfo):
        out = self.out
        base = self.cls_py(ci.base) if ci.base and (ci.base in self.classes) else "MqlObject"
        if ci.base and ci.base not in self.classes:
            self.rep.warn(ci.decl, f"base class {ci.base} unknown")
        out.append(f"class {self.cls_py(ci.name)}({base}):")
        prev_cls = self.cur_cls
        self.cur_cls = ci
        try:
            fields = [d.name for d in ci.field_decls]
            out.append(f"    _q_fields = ({', '.join(repr(pyattr(f)) for f in fields)}{',' if len(fields) == 1 else ''})")
            ptrs = [d.name for d in ci.field_decls if self.tstr(d.type, d.dims).startswith("P:")]
            if ptrs:
                out.append(f"    _q_ptrs = ({', '.join(repr(pyattr(p)) for p in ptrs)},)")
            for e in ci.nested_enums:
                for item in e.items:
                    nm = item[0]
                    if nm in self.enum_items:
                        out.append(f"    {pyattr(nm)} = {self.enum_items[nm][1]}")
            post = []
            for nm, (t, d) in ci.static_fields.items():
                if d.init is not None or d.dims:
                    code = self.init_code(d, t)
                else:
                    code = self.default_value(t)
                if is_obj(t) or "(" in code:
                    out.append(f"    {pyattr(nm)} = None")
                    post.append(f"{self.cls_py(ci.name)}.{pyattr(nm)} = {code}")
                else:
                    out.append(f"    {pyattr(nm)} = {code}")
            # constructors
            self.translate_ctors(ci)
            if ci.dtor is not None and ci.dtor.body is not None:
                f = ci.dtor
                self.translate_function(f, ci, py_name="_q_dtor")
            for name, lst in ci.methods.items():
                for f in lst:
                    self.translate_function(f, ci, py_name=self.method_py(ci.name, f, lst))
                    if name == "operator==":
                        out.append("    __hash__ = MqlObject.__hash__")
            out.extend(post)
        finally:
            self.cur_cls = prev_cls

    def field_init_lines(self, ci: ClassInfo, ind: int):
        for d in ci.field_decls:
            t = self.tstr(d.type, d.dims)
            if d.dims:
                code = self.new_array_code(t, d.dims, None)
            else:
                code = self.default_value(t)
            self.emit(f"self.{pyattr(d.name)} = {code}", ind)

    def translate_ctors(self, ci: ClassInfo):
        ctors = [c for c in ci.ctors if c.body is not None or not c.params]
        base_call = None
        if ci.base and ci.base in self.classes:
            base_call = f"{self.cls_py(ci.base)}.__init__(self)"
        if not ctors:
            self.emit("def __init__(self, *args):", 1)
            if base_call:
                self.emit(base_call, 2)
            self.field_init_lines(ci, 2)
            if not ci.field_decls and not base_call:
                self.emit("pass", 2)
            return
        if len(ctors) == 1:
            self.translate_function(ctors[0], ci, py_name="__init__", ctor=True)
            return
        # several constructors: dispatch on argument count / types
        names = []
        for i, c in enumerate(ctors):
            nm = f"_q_ctor{i + 1}"
            names.append((nm, c))
            self.translate_function(c, ci, py_name=nm, ctor=True)
        self.emit("def __init__(self, *args):", 1)
        for nm, c in names:
            req = sum(1 for p in c.params if p.default is None)
            mx = len(c.params)
            conds = [f"{req} <= len(args) <= {mx}"]
            # discriminate by first argument type when arities overlap
            if c.params:
                pt = self.tstr(c.params[0].type, c.params[0].dims)
                chk = self._type_check_code("args[0]", pt)
                if chk:
                    conds.append(f"(len(args) == 0 or {chk})")
            self.emit(f"if {' and '.join(conds)}:", 2)
            self.emit(f"self.{nm}(*args)", 3)
            self.emit("return", 3)
        self.emit(f"self.{names[0][0]}(*args)", 2)

    def _type_check_code(self, v, t):
        if t == "string":
            return f"isinstance({v}, str)"
        if is_obj(t):
            return f"isinstance({v}, MqlObject)"
        if is_array(t):
            return f"isinstance({v}, Arr)"
        if is_float(t):
            return f"isinstance({v}, float)"
        if is_int(t):
            return f"(isinstance({v}, int) and not isinstance({v}, bool))" if t != "bool" else f"isinstance({v}, bool)"
        return ""

    # ================================================================ functions

    def translate_function(self, f: N.FuncDecl, ci: ClassInfo | None, py_name: str | None = None, ctor=False):
        ind0 = 1 if ci is not None else 0
        saved = (self.scopes, self.cur_func, self.cur_ret, self.cur_static, self.func_globals, self.loops,
                 self.boxed_locals, self.local_names_used, self.out, self.type_alias)
        self.type_alias = self.local_type_maps.get(id(f), {})
        self.scopes = [{}]
        self.cur_func = f
        self.cur_ret = self.tstr(f.ret) if f.kind not in ("ctor", "dtor") else "void"
        self.cur_static = bool(f.static) and ci is not None
        self.func_globals = set()
        self.loops = []
        self.local_names_used = set()
        body_out: list[str] = []
        self.out = body_out
        try:
            self.boxed_locals = self.find_boxed_locals(f)
            params_code = []
            pre = []
            for p in f.params:
                if p.type.name == "...":
                    params_code.append("*__varargs")
                    continue
                pt = self.tstr(p.type, p.dims)
                ref = bool(p.type.ref) and not p.dims and not is_array(pt) and not (is_obj(pt) and not is_ptr(pt)) \
                    and not p.type.const
                pn = self.local_py(p.name)
                v = Var(p.name, pn, pt, "param", ref=ref)
                if not ref and p.name in self.boxed_locals:
                    v.boxed = True
                    pre.append(f"{pn} = Box({pn})")
                self.scopes[-1][p.name] = v
                if p.default is not None:
                    dc, dt = self.ex(p.default)[:2]
                    if self.const_eval(p.default) is None and not isinstance(p.default, (N.Num, N.Str, N.Char)):
                        if not (isinstance(p.default, N.Name) and (p.default.id in self.enum_items or p.default.id == "NULL"
                                                                    or p.default.id in self.rt)):
                            dc = self.conv(dc, dt, pt)
                    else:
                        dc = self.conv(dc, dt, pt)
                    params_code.append(f"{pn}={dc}")
                else:
                    params_code.append(pn)
            if ci is not None and not self.cur_static:
                params_code.insert(0, "self")
            ind = ind0 + 1
            for line in pre:
                self.emit(line, ind)
            if ctor:
                if ci.base and ci.base in self.classes:
                    binit = next((a for n, a in f.inits if n == ci.base), None)
                    if binit is not None:
                        bctor = self._pick_ctor(ci.base, binit)
                        self.emit(f"{self.cls_py(ci.base)}.__init__(self{', ' if binit else ''}{self.call_args(bctor, binit) if bctor else ', '.join(self.ex(a)[0] for a in binit)})", ind)
                    else:
                        self.emit(f"{self.cls_py(ci.base)}.__init__(self)", ind)
                self.field_init_lines(ci, ind)
                for nm, args in f.inits:
                    if nm == ci.base:
                        continue
                    ft = ci.fields.get(nm)
                    if ft is None:
                        self.rep.warn(f, f"initializer for unknown member {nm}")
                        continue
                    if is_obj(ft) and not is_ptr(ft) and not is_array(ft):
                        self.emit(f"self.{pyattr(nm)} = {self.cls_py(obj_class(ft))}({self.call_args_for_ctor(obj_class(ft), args)})", ind)
                    elif args:
                        c, t = self.ex(args[0])[:2]
                        self.emit(f"self.{pyattr(nm)} = {self.conv(c, t, ft)}", ind)
            n_before = len(body_out)
            if f.body is not None:
                self.block(f.body.body, ind)
            if f.kind == "func" and f.name == "OnInit" and ci is None and self.cur_ret != "void":
                pass
            if len(body_out) == n_before and not pre and not ctor:
                self.emit("pass", ind)
            elif len(body_out) == 0:
                self.emit("pass", ind)
        finally:
            gl = sorted(self.func_globals)
            (self.scopes, self.cur_func, self.cur_ret, self.cur_static, self.func_globals, self.loops,
             self.boxed_locals, self.local_names_used, self.out, self.type_alias) = saved
        name = py_name or self.func_py.get(id(f), pyname(f.name))
        if self.cur_static_decorator(f, ci):
            self.emit("@staticmethod", ind0)
        self.emit(f"def {name}({', '.join(params_code)}):", ind0)
        if gl:
            self.emit(f"global {', '.join(gl)}", ind0 + 1)
        self.out.extend(body_out)

    def cur_static_decorator(self, f, ci):
        return ci is not None and f.static and f.kind == "func"

    def _pick_ctor(self, cname, args):
        ci = self.classes.get(cname)
        if ci is None:
            return None
        cands = [c for c in ci.ctors if sum(1 for p in c.params if p.default is None) <= len(args) <= len(c.params)]
        return cands[0] if cands else None

    def call_args_for_ctor(self, cname, args):
        c = self._pick_ctor(cname, args)
        if c is not None:
            return self.call_args(c, args)
        return ", ".join(self.ex(a)[0] for a in args)

    def local_py(self, name: str) -> str:
        """Python name for a new local, avoiding collisions with module-level names
        and with a same-named variable of an enclosing block (C shadowing)."""
        base = pyname(name)
        if name in self.module_names or base in self.rt or name in SPECIAL_TYPES:
            base = base + "_"
        visible = any(name in s for s in self.scopes)
        if not visible:
            return base
        existing = {v.py for s in self.scopes for v in s.values()}
        k = 2
        nm = f"{base}_{k}"
        while nm in existing:
            k += 1
            nm = f"{base}_{k}"
        return nm

    def find_boxed_locals(self, f) -> set:
        """Locals/params passed to scalar reference parameters anywhere in f."""
        boxed = set()

        def visit(n):
            if isinstance(n, N.Call):
                refs = self.ref_positions_for_call(n)
                for i, a in enumerate(n.args):
                    if i in refs and isinstance(a, N.Name):
                        boxed.add(a.id)
            if isinstance(n, N.Node):
                for k in getattr(n, "__slots__", ()):
                    if k in ("line", "file"):
                        continue
                    visit(getattr(n, k, None))
            elif isinstance(n, (list, tuple)):
                for x in n:
                    visit(x)
        visit(f.body)
        return boxed

    def ref_positions_for_call(self, call: N.Call) -> set:
        fn = call.func
        nargs = len(call.args)
        if isinstance(fn, N.Name):
            name = fn.id
            # user function?
            if self.cur_cls is not None:
                ms, owner = self.find_methods(self.cur_cls.name, name)
                if ms:
                    f = self.pick_overload(ms, call.args, quiet=True)
                    return self.ref_params(f) if f else set()
            if name in self.funcs:
                f = self.pick_overload(self.funcs[name], call.args, quiet=True)
                if f is not None:
                    return self.ref_params(f)
            spec = BUILTIN_REFS.get(name)
            if spec:
                return set(spec.get(nargs, spec.get(None, ())))
            return set()
        if isinstance(fn, N.Member):
            t = self.quick_type(fn.obj)
            if is_obj(t):
                ms, owner = self.find_methods(obj_class(t), fn.name)
                if ms:
                    f = self.pick_overload(ms, call.args, quiet=True)
                    return self.ref_params(f) if f else set()
        if isinstance(fn, N.Scope):
            if fn.cls and fn.cls in self.classes:
                ms, owner = self.find_methods(fn.cls, fn.id)
                if ms:
                    f = self.pick_overload(ms, call.args, quiet=True)
                    return self.ref_params(f) if f else set()
            if not fn.cls and fn.id in self.funcs:
                f = self.pick_overload(self.funcs[fn.id], call.args, quiet=True)
                return self.ref_params(f) if f else set()
        return set()

    def ref_params(self, f) -> set:
        out = set()
        for i, p in enumerate(f.params):
            if p.type.ref and not p.dims and not p.type.const:
                pt = self.tstr(p.type)
                if not is_array(pt) and not (is_obj(pt) and not is_ptr(pt)):
                    out.add(i)
        return out

    def quick_type(self, e) -> str:
        """Type of an expression without emitting code (best effort)."""
        saved_out, saved_glob = self.out, set(self.func_globals)
        saved_un = (set(self.rep.unknown_names), set(self.rep.unknown_funcs), len(self.rep.warnings))
        self.out = []
        try:
            return self.ex(e)[1]
        except Exception:
            return "?"
        finally:
            self.out = saved_out
            self.func_globals = saved_glob
            self.rep.unknown_names, self.rep.unknown_funcs = saved_un[0], saved_un[1]
            del self.rep.warnings[saved_un[2]:]

    def pick_overload(self, cands, args, quiet=False):
        n = len(args)
        ok = [f for f in cands if sum(1 for p in f.params if p.default is None and p.type.name != "...") <= n
              and (n <= len(f.params) or any(p.type.name == "..." for p in f.params))]
        if not ok:
            return cands[0] if cands else None
        if len(ok) == 1:
            return ok[0]
        # score by argument types
        types = [self.quick_type(a) for a in args]
        best, bscore = ok[0], -1e9
        for f in ok:
            s = 0
            for t, p in zip(types, f.params):
                pt = self.tstr(p.type, p.dims)
                if t == pt:
                    s += 3
                elif is_int(t) and is_int(pt):
                    s += 2
                elif is_num(t) and is_num(pt):
                    s += 1
                elif (t == "string") != (pt == "string"):
                    s -= 5
                elif is_array(t) != is_array(pt):
                    s -= 5
                elif is_obj(t) and is_obj(pt):
                    s += 2 if self.is_subclass(obj_class(t), obj_class(pt)) else -2
            s -= 0.1 * abs(len(f.params) - n)
            if s > bscore:
                best, bscore = f, s
        return best

    def is_subclass(self, a, b):
        seen = set()
        while a and a not in seen:
            if a == b:
                return True
            seen.add(a)
            ci = self.classes.get(a)
            a = ci.base if ci else None
        return False

    # ================================================================ statements

    def block(self, stmts, ind):
        for s in stmts:
            self.stmt(s, ind)

    def stmt(self, s, ind):
        m = getattr(self, "st_" + type(s).__name__, None)
        if m is None:
            self.rep.warn(s, f"unsupported statement {type(s).__name__}")
            self.emit(f"pass  # unsupported {type(s).__name__}", ind)
            return
        m(s, ind)

    def body_block(self, s, ind):
        """Emit a nested statement as an indented block (never empty)."""
        n = len(self.out)
        self.scopes.append({})
        try:
            if isinstance(s, N.Block):
                self.block(s.body, ind)
            elif s is not None:
                self.stmt(s, ind)
        finally:
            self.scopes.pop()
        if len(self.out) == n:
            self.emit("pass", ind)

    def st_Block(self, s, ind):
        self.scopes.append({})
        try:
            self.block(s.body, ind)
        finally:
            self.scopes.pop()

    def st_Empty(self, s, ind):
        pass

    def st_DeclStmt(self, s, ind):
        for d in s.decls:
            if isinstance(d, N.VarDecl):
                self.local_decl(d, ind)
            elif isinstance(d, N.EnumDecl):
                self._collect_enum(d)
                for item in d.items:
                    nm = item[0]
                    self.emit(f"{pyname(nm)} = {self.enum_items[nm][1]}", ind)
                    self.scopes[-1][nm] = Var(nm, pyname(nm), "enum:" + (d.name or "int"), "local")
            elif isinstance(d, N.ClassDecl):
                pass    # hoisted to module level
            elif isinstance(d, N.Typedef):
                self.typedefs[d.name] = d

    def local_decl(self, d: N.VarDecl, ind):
        t = self.tstr(d.type, d.dims)
        if "static" in d.storage:
            fname = self.cur_func.name if self.cur_func is not None else "f"
            owner = (self.cur_cls.name + "_") if self.cur_cls is not None else ""
            gname = f"_s_{pyname(owner + fname).replace('~', 'd')}_{pyname(d.name)}"
            while any(gname == g for g, _ in self.static_locals):
                gname += "_"
            lazy = d.init is not None and not d.dims and not isinstance(d.init, (N.Num, N.Str, N.Char, N.InitList)) \
                and self.const_eval(d.init) is None \
                and not (isinstance(d.init, N.Name) and (d.init.id in self.enum_items or d.init.id in self.rt))
            if lazy:
                # C++: initialised the first time the declaration executes
                self.static_locals.append((gname, "_UNSET"))
                self.scopes[-1][d.name] = Var(d.name, gname, t, "static_local")
                code = self.init_code(d, t)
                self.func_globals.add(gname)
                self.emit(f"if {gname} is _UNSET:", ind)
                self.emit(f"{gname} = {code}", ind + 1)
                return
            saved_scopes = self.scopes
            self.scopes = [{}]
            try:
                code = self.init_code(d, t)
            finally:
                self.scopes = saved_scopes
            self.static_locals.append((gname, code))
            self.scopes[-1][d.name] = Var(d.name, gname, t, "static_local")
            return
        pn = self.local_py(d.name)
        boxed = d.name in self.boxed_locals and not d.dims and not is_array(t) and not (is_obj(t) and not is_ptr(t))
        code = self.init_code(d, t)
        v = Var(d.name, pn, t, "local", boxed=boxed)
        self.scopes[-1][d.name] = v
        if boxed:
            code = f"Box({code})"
        comment = ""
        self.emit(f"{pn} = {code}{comment}", ind)

    def st_ExprStmt(self, s, ind):
        e = s.e
        if isinstance(e, N.Comma):
            for x in e.items:
                self.st_ExprStmt(N.ExprStmt(x), ind)
            return
        if isinstance(e, N.Assign):
            self.assign_stmt(e, ind)
            return
        if isinstance(e, (N.Postfix, N.Unary)) and e.op in ("++", "--"):
            self.incdec_stmt(e.e, 1 if e.op == "++" else -1, ind)
            return
        code = self.ex(e)[0]
        self.emit(code, ind)

    def st_If(self, s, ind):
        cond = self.cond(s.cond)
        self.emit(f"if {cond}:", ind)
        self.body_block(s.then, ind + 1)
        els = s.els
        while els is not None:
            if isinstance(els, N.If):
                self.emit(f"elif {self.cond(els.cond)}:", ind)
                self.body_block(els.then, ind + 1)
                els = els.els
            else:
                self.emit("else:", ind)
                self.body_block(els, ind + 1)
                break

    def st_While(self, s, ind):
        cond = self.cond(s.cond)
        self.emit(f"while {cond}:", ind)
        self.loops.append(_Loop("loop"))
        try:
            self.body_block(s.body, ind + 1)
        finally:
            self.loops.pop()

    def st_DoWhile(self, s, ind):
        self.emit("while True:", ind)
        cond_code = None
        # 'continue' must test the condition first
        lp = _Loop("loop")
        cond_code = self.cond(N.Unary("!", s.cond))
        lp.step = [f"if {cond_code}:", "    break"]
        self.loops.append(lp)
        try:
            self.body_block(s.body, ind + 1)
        finally:
            self.loops.pop()
        self.emit(f"if {cond_code}:", ind + 1)
        self.emit("break", ind + 2)

    def st_For(self, s, ind):
        self.scopes.append({})
        try:
            if self.try_range_for(s, ind):
                return
            if s.init is not None:
                self.stmt(s.init, ind)
            cond = self.cond(s.cond) if s.cond is not None else "True"
            step_lines = []
            if s.step is not None:
                saved = self.out
                self.out = []
                self.st_ExprStmt(N.ExprStmt(s.step), 0)
                step_lines = self.out
                self.out = saved
            self.emit(f"while {cond}:", ind)
            self.loops.append(_Loop("loop", step_lines))
            try:
                n = len(self.out)
                self.body_block(s.body, ind + 1)
                if step_lines:
                    for ln in step_lines:
                        self.emit(ln, ind + 1)
            finally:
                self.loops.pop()
        finally:
            self.scopes.pop()

    # --- for -> range ------------------------------------------------------

    def try_range_for(self, s: N.For, ind) -> bool:
        init, cond, step = s.init, s.cond, s.step
        if init is None or cond is None or step is None:
            return False
        # loop variable and start
        declared = False
        if isinstance(init, N.DeclStmt) and len(init.decls) == 1 and isinstance(init.decls[0], N.VarDecl):
            d = init.decls[0]
            if d.init is None or d.dims or isinstance(d.init, N.InitList):
                return False
            var, start = d.name, d.init
            vt = self.tstr(d.type)
            declared = True
        elif isinstance(init, N.ExprStmt) and isinstance(init.e, N.Assign) and init.e.op == "=" \
                and isinstance(init.e.target, N.Name):
            var, start = init.e.target.id, init.e.value
            v = self.lookup(var)
            if v is None or v.kind not in ("local", "param") or v.boxed or v.ref:
                return False
            vt = v.type
        else:
            return False
        if vt not in ("int", "long", "uint", "short", "ushort", "char", "uchar", "ulong") and not vt.startswith("enum:"):
            return False
        # step
        delta = None
        if isinstance(step, (N.Postfix, N.Unary)) and step.op in ("++", "--") and isinstance(step.e, N.Name) \
                and step.e.id == var:
            delta = 1 if step.op == "++" else -1
        elif isinstance(step, N.Assign) and step.op in ("+=", "-=") and isinstance(step.target, N.Name) \
                and step.target.id == var:
            c = self.const_eval(step.value)
            if isinstance(c, int) and c > 0:
                delta = c if step.op == "+=" else -c
        if delta is None:
            return False
        # condition: strip '&& !IsStopped()'
        cond = self._strip_stop(cond)
        if not (isinstance(cond, N.Binary) and cond.op in ("<", "<=", ">", ">=") and isinstance(cond.l, N.Name)
                and cond.l.id == var):
            return False
        bound = cond.r
        if delta > 0 and cond.op not in ("<", "<="):
            return False
        if delta < 0 and cond.op not in (">", ">="):
            return False
        assigned = self.assigned_names(s.body)
        if var in assigned:
            return False
        if not self.invariant(bound, assigned, s.body):
            return False
        bt = self.quick_type(bound)
        if not is_int(bt):
            return False
        if self.uses_ref_or_addr(s.body, var):
            return False
        # emit
        if declared:
            pn = self.local_py(var)
            self.scopes[-1][var] = Var(var, pn, vt, "local")
        else:
            pn = self.lookup(var).py
        sc = self.conv(*self.ex(start)[:2], vt)
        bc = self.ex(bound)[0]
        if cond.op == "<=":
            bc = f"{bc} + 1" if delta > 0 else bc
        if cond.op == ">=":
            bc = f"{bc} - 1"
        rng = f"range({sc}, {bc})" if delta == 1 else f"range({sc}, {bc}, {delta})"
        post_value = not declared
        if post_value:
            self.emit(f"{pn} = {sc}", ind)
            rng = rng.replace(f"range({sc}, ", f"range({pn}, ", 1)
        self.emit(f"for {pn} in {rng}:", ind)
        self.loops.append(_Loop("loop"))
        try:
            self.body_block(s.body, ind + 1)
        finally:
            self.loops.pop()
        if post_value:
            # C leaves the variable at the first value failing the condition
            if delta == 1:
                fin = f"max({pn}, {bc})" if False else None
            self.emit("else:", ind)
            if delta > 0:
                self.emit(f"{pn} = _range_end({pn}, {bc}, {delta})", ind + 1)
            else:
                self.emit(f"{pn} = _range_end({pn}, {bc}, {delta})", ind + 1)
        return True

    def _strip_stop(self, cond):
        if isinstance(cond, N.Binary) and cond.op == "&&":
            r = cond.r
            if isinstance(r, N.Unary) and r.op == "!" and (
                    (isinstance(r.e, N.Call) and isinstance(r.e.func, N.Name) and r.e.func.id == "IsStopped")
                    or (isinstance(r.e, N.Name) and r.e.id == "_StopFlag")):
                return cond.l
        return cond

    def assigned_names(self, node) -> set:
        res = set()

        def visit(n):
            if isinstance(n, N.Assign):
                if isinstance(n.target, N.Name):
                    res.add(n.target.id)
                visit(n.value)
                visit(n.target)
                return
            if isinstance(n, (N.Postfix, N.Unary)) and n.op in ("++", "--"):
                if isinstance(n.e, N.Name):
                    res.add(n.e.id)
            if isinstance(n, N.Call):
                refs = self.ref_positions_for_call(n)
                for i, a in enumerate(n.args):
                    if i in refs and isinstance(a, N.Name):
                        res.add(a.id)
                # calls to user functions/methods may change globals/members
                fn = n.func
                if isinstance(fn, N.Name) and (fn.id in self.funcs or (self.cur_cls and self.find_methods(self.cur_cls.name, fn.id)[0])):
                    res.add("<call>")
                elif isinstance(fn, N.Member):
                    res.add("<call>")
                    if isinstance(fn.obj, N.Name):
                        res.add(fn.obj.id)
                elif isinstance(fn, N.Name) and fn.id in ("ArrayResize", "ArrayFree", "ArrayCopy", "CopyBuffer",
                                                          "CopyTime", "CopyClose", "CopyOpen", "CopyHigh",
                                                          "CopyLow", "CopyRates", "StringSplit", "ArrayInsert",
                                                          "ArrayRemove", "CopyTickVolume", "CopyRealVolume",
                                                          "CopySpread", "ArraySwap", "StringToCharArray"):
                    if n.args and isinstance(n.args[0], N.Name):
                        res.add("<resize:" + n.args[0].id + ">")
                    for a in n.args:
                        if isinstance(a, N.Name):
                            res.add("<resize:" + a.id + ">")
            if isinstance(n, N.DeclStmt):
                for d in n.decls:
                    if isinstance(d, N.VarDecl):
                        res.add(d.name)
            if isinstance(n, N.Node):
                for k in n.__slots__:
                    if k in ("line", "file"):
                        continue
                    visit(getattr(n, k, None))
            elif isinstance(n, (list, tuple)):
                for x in n:
                    visit(x)
        visit(node)
        return res

    def uses_ref_or_addr(self, node, var) -> bool:
        return False

    PURE_FUNCS = {"MathMin", "MathMax", "MathAbs", "fmin", "fmax", "MathFloor", "MathCeil", "MathRound",
                  "MathSqrt", "MathPow", "ArraySize", "ArrayRange", "StringLen", "Bars", "MathLog",
                  "PeriodSeconds", "MathMod"}

    def invariant(self, e, assigned, body) -> bool:
        if isinstance(e, (N.Num, N.Char)):
            return True
        if isinstance(e, N.Name):
            if e.id in assigned:
                return False
            v = self.lookup(e.id)
            if v is not None and v.kind in ("field", "static_field", "global", "static_local") and "<call>" in assigned:
                return False
            return True
        if isinstance(e, N.Binary):
            return self.invariant(e.l, assigned, body) and self.invariant(e.r, assigned, body)
        if isinstance(e, N.Unary) and e.op in ("-", "+", "~"):
            return self.invariant(e.e, assigned, body)
        if isinstance(e, N.Cast):
            return self.invariant(e.e, assigned, body)
        if isinstance(e, N.Ternary):
            return all(self.invariant(x, assigned, body) for x in (e.cond, e.a, e.b))
        if isinstance(e, N.Call) and isinstance(e.func, N.Name) and e.func.id in self.PURE_FUNCS:
            if e.func.id in ("ArraySize", "ArrayRange", "StringLen") and e.args and isinstance(e.args[0], N.Name):
                if "<resize:" + e.args[0].id + ">" in assigned or e.args[0].id in assigned or "<call>" in assigned:
                    return False
            return all(self.invariant(a, assigned, body) for a in e.args)
        if isinstance(e, N.Member) and isinstance(e.obj, N.Name):
            return "<call>" not in assigned and e.obj.id not in assigned
        return False

    # --- switch ------------------------------------------------------------

    def st_Switch(self, s, ind):
        sv = self.tmp("_sw")
        self.emit(f"{sv} = {self.ex(s.e)[0]}", ind)
        cases = s.cases
        simple = True
        for k, (labels, body) in enumerate(cases):
            last = k == len(cases) - 1
            if self._has_switch_break(body, top=False) and not self._ends_with_jump(body):
                simple = False
            if not last and not self._ends_with_jump(body):
                if body:   # fallthrough into the next case
                    simple = False
        if simple:
            first = True
            default_body = None
            for labels, body in cases:
                body2 = self._strip_final_break(body)
                if None in labels:
                    if len(labels) > 1:
                        pass
                    default_body = body2
                    continue
                vals = [self.ex(l)[0] for l in labels]
                test = f"{sv} == {vals[0]}" if len(vals) == 1 else f"{sv} in ({', '.join(vals)})"
                self.emit(f"{'if' if first else 'elif'} {test}:", ind)
                first = False
                self.loops.append(_Loop("switch_simple"))
                try:
                    self.body_block(N.Block(body2), ind + 1)
                finally:
                    self.loops.pop()
            if default_body is not None:
                if first:
                    self.loops.append(_Loop("switch_simple"))
                    try:
                        self.scopes.append({})
                        n = len(self.out)
                        self.block(default_body, ind)
                        self.scopes.pop()
                    finally:
                        self.loops.pop()
                else:
                    self.emit("else:", ind)
                    self.loops.append(_Loop("switch_simple"))
                    try:
                        self.body_block(N.Block(default_body), ind + 1)
                    finally:
                        self.loops.pop()
            return
        # general switch with fallthrough: index of the entry case, then run all following
        kv = self.tmp("_k")
        parts = []
        default_idx = None
        for k, (labels, body) in enumerate(cases):
            for l in labels:
                if l is None:
                    default_idx = k
                else:
                    parts.append((self.ex(l)[0], k))
        expr = str(default_idx if default_idx is not None else len(cases))
        for val, k in reversed(parts):
            expr = f"{k} if {sv} == {val} else {expr}"
        self.emit(f"{kv} = {expr}", ind)
        self.emit("try:", ind)
        self.loops.append(_Loop("switch_exc"))
        try:
            for k, (labels, body) in enumerate(cases):
                self.emit(f"if {kv} <= {k}:", ind + 1)
                self.body_block(N.Block(body), ind + 2)
        finally:
            self.loops.pop()
        self.emit("except _SwitchBreak:", ind)
        self.emit("pass", ind + 1)

    def _ends_with_jump(self, body):
        if not body:
            return False
        last = body[-1]
        if isinstance(last, N.Block):
            return self._ends_with_jump(last.body)
        if isinstance(last, (N.Break, N.Return, N.Continue)):
            return True
        if isinstance(last, N.If) and last.els is not None:
            a = self._ends_with_jump([last.then]) if not isinstance(last.then, N.Block) else self._ends_with_jump(last.then.body)
            b = self._ends_with_jump([last.els]) if not isinstance(last.els, N.Block) else self._ends_with_jump(last.els.body)
            return a and b and not self._has_switch_break([last], top=False)
        return False

    def _has_switch_break(self, stmts, top=True):
        """Is there a 'break' (belonging to this switch) anywhere except as the last statement?"""
        def visit(n, depth):
            if isinstance(n, N.Break):
                return depth > 0
            if isinstance(n, (N.For, N.While, N.DoWhile, N.Switch)):
                return False
            if isinstance(n, N.Block):
                return any(visit(x, depth + 1) for x in n.body)
            if isinstance(n, N.If):
                return visit(n.then, depth + 1) or (n.els is not None and visit(n.els, depth + 1))
            return False
        body = stmts[:-1] if stmts and isinstance(stmts[-1], N.Break) else stmts
        return any(visit(x, 1 if True else 0) for x in body)

    def _strip_final_break(self, body):
        if body and isinstance(body[-1], N.Break):
            return body[:-1]
        if body and isinstance(body[-1], N.Block):
            inner = self._strip_final_break(body[-1].body)
            return body[:-1] + [N.Block(inner)]
        return body

    def st_Break(self, s, ind):
        lp = self.loops[-1] if self.loops else None
        if lp is not None and lp.kind == "switch_exc":
            self.emit("raise _SwitchBreak", ind)
        elif lp is not None and lp.kind == "switch_simple":
            # break inside a nested if of a simple switch case: cannot happen (simple check)
            self.emit("pass  # break", ind)
        else:
            self.emit("break", ind)

    def st_Continue(self, s, ind):
        # find enclosing loop (skipping switches)
        for lp in reversed(self.loops):
            if lp.kind == "loop":
                if lp.step:
                    for ln in lp.step:
                        self.emit(ln, ind)
                break
        self.emit("continue", ind)

    def st_Return(self, s, ind):
        if s.e is None:
            self.emit("return", ind)
            return
        c, t = self.ex(s.e)[:2]
        rt = self.cur_ret
        if is_obj(rt) and not is_ptr(rt) and self._is_lvalue(s.e):
            c = f"_copy({c})"
        else:
            c = self.conv(c, t, rt)
        self.emit(f"return {c}", ind)

    def st_Delete(self, s, ind):
        self.emit(f"_delete({self.ex(s.e)[0]})", ind)

    # ================================================================ assignments

    def assign_stmt(self, e: N.Assign, ind):
        if isinstance(e.value, N.Assign) and e.op == "=":
            # a = b = c  -> b = c; a = b
            self.assign_stmt(e.value, ind)
            self.assign_stmt(N.Assign("=", e.target, e.value.target), ind)
            return
        tgt, tt, kind = self.lvalue(e.target)
        vc, vt = self.ex(e.value)[:2]
        op = e.op
        if op == "=":
            if is_obj(tt) and not is_ptr(tt) and not is_array(tt):
                if kind == "name" and isinstance(e.value, (N.Call, N.New)) and not self._is_lvalue(e.value):
                    self.emit(f"_assign({tgt}, {vc})", ind)
                else:
                    self.emit(f"_assign({tgt}, {vc})", ind)
                return
            self.emit(f"{tgt} = {self.conv(vc, vt, tt)}", ind)
            return
        bop = op[:-1]
        if tt == "string" and bop == "+":
            self.emit(f"{tgt} += {self.to_str(vc, vt)}", ind)
            return
        res_type = self.arith_type(bop, tt, vt)
        if bop == "/" and is_int(tt) and is_int(vt):
            self.emit(f"{tgt} = _idiv({tgt}, {vc})", ind)
            return
        if bop == "/":
            rhs = f"_fdiv({tgt}, {vc})" if not self.nonzero_const(e.value) else f"{tgt} / {self.par(vc)}"
            self.emit(f"{tgt} = {self.conv(rhs, 'double', tt)}", ind)
            return
        if bop == "%":
            self.emit(f"{tgt} = _imod({tgt}, {vc})", ind)
            return
        pyop = {"+": "+", "-": "-", "*": "*", "&": "&", "|": "|", "^": "^", "<<": "<<", ">>": ">>"}[bop]
        if is_int(tt) and is_float(vt):
            self.emit(f"{tgt} = {CONVERTER.get(tt, '_int') if tt != 'bool' else '_bool'}({tgt} {pyop} {self.par(vc)})", ind)
            return
        if bop == "<<" and tt in ("int", "uint", "long", "ulong"):
            self.emit(f"{tgt} = {CONVERTER[tt]}({tgt} << {self.par(vc)})", ind)
            return
        self.emit(f"{tgt} {pyop}= {vc}", ind)

    def incdec_stmt(self, target, d, ind):
        tgt, tt, kind = self.lvalue(target)
        self.emit(f"{tgt} {'+' if d > 0 else '-'}= 1", ind)

    def lvalue(self, e):
        """(python lvalue code, type, kind) for an assignment target."""
        if isinstance(e, N.Name):
            v = self.lookup(e.id)
            if v is None:
                self.rep.unknown_names.add(e.id)
                return pyname(e.id), "?", "name"
            self.note_global_assign(v)
            if v.boxed or v.ref:
                return f"{v.py}.v", v.type, "box"
            return v.py, v.type, "name"
        if isinstance(e, N.Index):
            oc, ot = self.ex(e.obj)[:2]
            ic, it = self.ex(e.idx)[:2]
            if is_float(it):
                ic = f"_int({ic})"
            return f"{oc}[{ic}]", elem(ot) if is_array(ot) else "?", "index"
        if isinstance(e, N.Member):
            oc, ot = self.ex(e.obj)[:2]
            ft = "?"
            static = False
            if is_obj(ot):
                fi = self.find_field(obj_class(ot), e.name)
                if fi:
                    ft, static, owner = fi
                    if static:
                        return f"{self.cls_py(owner)}.{pyattr(e.name)}", ft, "attr"
            return f"{self.par(oc)}.{pyattr(e.name)}", ft, "attr"
        if isinstance(e, N.Scope):
            if e.cls and e.cls in self.classes:
                fi = self.find_field(e.cls, e.id)
                return f"{self.cls_py(e.cls)}.{pyattr(e.id)}", fi[0] if fi else "?", "attr"
            v = self.globals.get(e.id)
            if v is not None:
                self.func_globals.add(v.py)
                return v.py, v.type, "name"
            return pyname(e.id), "?", "name"
        if isinstance(e, N.Unary) and e.op == "*":
            return self.lvalue(e.e)
        c, t = self.ex(e)[:2]
        self.rep.warn(e, "unsupported assignment target")
        return c, t, "expr"

    def note_global_assign(self, v: Var):
        if v.kind in ("global", "static_local", "input") and not v.boxed:
            self.func_globals.add(v.py)

    # ================================================================ expressions

    def cond(self, e) -> str:
        e = self._strip_stop(e) if isinstance(e, N.Binary) else e
        if isinstance(e, N.Unary) and e.op == "!" and isinstance(e.e, N.Call) and isinstance(e.e.func, N.Name) \
                and e.e.func.id == "IsStopped":
            return "True"
        c, t, _a = self.ex(e, cond=True)
        return c

    @staticmethod
    def par(code: str) -> str:
        if _is_atomic(code):
            return code
        return f"({code})"

    def nonzero_const(self, e):
        v = self.const_eval(e)
        return v is not None and v != 0

    def arith_type(self, op, a, b):
        if op in ("+",) and ("string" in (a, b)):
            return "string"
        if is_float(a) or is_float(b):
            return "double"
        if a == "?" or b == "?":
            return "double" if (a == "?" and not is_int(b)) or (b == "?" and not is_int(a)) else "?"
        if is_int(a) and is_int(b):
            if "ulong" in (a, b):
                return "ulong"
            if "long" in (a, b) or "datetime" in (a, b):
                return "long"
            if "uint" in (a, b) or "color" in (a, b):
                return "uint"
            return "int"
        return "?"

    def conv(self, code: str, src: str, dst: str) -> str:
        """Implicit conversion of a value of type src to type dst."""
        if dst in ("?", "void", "") or src == dst:
            return code
        if src == "null":
            if dst == "string":
                return '""'
            if dst == "bool":
                return "False"
            if is_float(dst):
                return "0.0"
            if is_int(dst):
                return "0"
            return code
        if dst == "string":
            if src == "string":
                return code
            return self.to_str(code, src)
        if dst == "bool":
            if src == "bool":
                return code
            if src == "string":
                return f"_bool({code})"
            if is_num(src):
                return f"({code} != 0)" if not _is_atomic(code) or True else code
            return f"_bool({code})"
        if is_int(dst):
            if src == "string":
                return f"StringToInteger({code})"
            if is_float(src) or src == "?":
                if src == "?" and _looks_int(code):
                    return code
                cv = CONVERTER.get(dst, "_int")
                if dst.startswith("enum:"):
                    cv = "_int"
                return f"{cv}({code})"
            return code
        if is_float(dst):
            if src == "string":
                return f"StringToDouble({code})"
            if is_int(src) and _is_int_literal(code):
                return code + ".0" if not code.startswith("0x") else f"float({code})"
            return code
        return code

    def to_str(self, code, t):
        if t == "string":
            return code
        if t == "bool":
            return f"_str({code})"
        return f"_str({code})"

    def ex(self, e, cond=False):
        """Translate an expression: (code, type, atomic)."""
        m = getattr(self, "ex_" + type(e).__name__, None)
        if m is None:
            self.rep.warn(e, f"unsupported expression {type(e).__name__}")
            return "None", "?", True
        r = m(e) if not cond else (m(e, cond=True) if type(e).__name__ in ("Binary", "Unary") else m(e))
        return r

    def ex_Num(self, e):
        v = e.value
        if e.kind == "bool":
            return ("True" if v else "False"), "bool", True
        if e.kind == "float" or isinstance(v, float):
            txt = repr(float(v))
            return txt, "double", True
        if e.kind == "color":
            return (f"0x{v:06X}" if v >= 0 else str(v)), "color", True
        if e.kind == "datetime":
            return str(v), "datetime", True
        t = "int"
        txt = e.text or str(v)
        if txt.lower().startswith("0x"):
            code = txt.rstrip("uUlL")
            if v > 0x7FFFFFFF:
                t = "uint" if v <= 0xFFFFFFFF else "long"
        else:
            code = str(v)
            if v > 2147483647:
                t = "long"
        return code, t, True

    def ex_Str(self, e):
        return _pystr(e.value), "string", True

    def ex_Char(self, e):
        return str(e.value), "ushort", True

    def ex_This(self, e):
        return "self", ("P:" + self.cur_cls.name) if self.cur_cls else "?", True

    def lookup(self, name) -> Var | None:
        for s in reversed(self.scopes):
            if name in s:
                return s[name]
        if self.cur_cls is not None:
            fi = self.find_field(self.cur_cls.name, name)
            if fi is not None:
                t, static, owner = fi
                if static or self.cur_static:
                    return Var(name, f"{self.cls_py(owner)}.{pyattr(name)}", t, "static_field", cls=owner)
                return Var(name, f"self.{pyattr(name)}", t, "field", cls=owner)
        v = self.globals.get(name)
        if v is not None:
            return v
        return None

    def ex_Name(self, e):
        name = e.id
        if name == "NULL":
            return "None", "null", True
        if name in ("__FUNCTION__", "__FUNCSIG__"):
            fn = self.cur_func.name if self.cur_func is not None else ""
            if self.cur_cls is not None and fn:
                fn = f"{self.cur_cls.name}::{fn}"
            return repr(fn), "string", True
        v = self.lookup(name)
        if v is not None:
            if v.boxed or v.ref:
                return f"{v.py}.v", v.type, True
            return v.py, v.type, True
        if name in SPECIAL_TYPES:
            return SPECIAL_NAMES[name], SPECIAL_TYPES[name], True
        if name in self.enum_items:
            en, val = self.enum_items[name]
            return pyname(name), "enum:" + (en or "int"), True
        if name in self.funcs:
            f = self.funcs[name][0]
            return self.func_py[id(f)], "fn:" + name, True
        if self.cur_cls is not None:
            ms, owner = self.find_methods(self.cur_cls.name, name)
            if ms:
                return f"self.{self.method_py(owner, ms[0])}", "fn:" + name, True
        if name in self.classes:
            return self.cls_py(name), "class", True
        if name in self.rt:
            from . import rt_consts
            t = rt_consts.CONST_TYPES.get(name, "?")
            return name, t, True
        if name in ("true", "false"):
            return ("True" if name == "true" else "False"), "bool", True
        self.rep.unknown_names.add(name)
        return pyname(name), "?", True

    def ex_Scope(self, e):
        if e.cls == "":
            v = self.globals.get(e.id)
            if v is not None:
                return v.py, v.type, True
            if e.id in self.funcs:
                f = self.funcs[e.id][0]
                return self.func_py[id(f)], "fn:" + e.id, True
            return pyname(e.id), BUILTIN_RET.get(e.id, "?"), True
        if e.cls in self.classes:
            fi = self.find_field(e.cls, e.id)
            if fi:
                return f"{self.cls_py(fi[2])}.{pyattr(e.id)}", fi[0], True
            ms, owner = self.find_methods(e.cls, e.id)
            if ms:
                return f"{self.cls_py(owner)}.{self.method_py(owner, ms[0])}", "fn:" + e.id, True
            if e.id in self.enum_items:
                return pyname(e.id), "enum:" + (self.enum_items[e.id][0] or "int"), True
        if e.cls in self.enums and e.id in self.enum_items:
            return pyname(e.id), "enum:" + e.cls, True
        if e.id in self.enum_items:
            return pyname(e.id), "enum:" + (self.enum_items[e.id][0] or "int"), True
        if e.cls.startswith("ENUM_") and e.cls not in self.classes and e.id in self.rt:
            return e.id, "enum:" + e.cls, True          # ENUM_MA_METHOD::MODE_SMA
        return f"{pyname(e.cls)}.{pyattr(e.id)}", "?", True

    def ex_Member(self, e):
        oc, ot, _a = self.ex(e.obj)
        if is_obj(ot):
            cname = obj_class(ot)
            fi = self.find_field(cname, e.name)
            if fi:
                t, static, owner = fi
                if static:
                    return f"{self.cls_py(owner)}.{pyattr(e.name)}", t, True
                return f"{self.par(oc)}.{pyattr(e.name)}", t, True
            ms, owner = self.find_methods(cname, e.name)
            if ms:
                return f"{self.par(oc)}.{self.method_py(owner, ms[0])}", "fn:" + e.name, True
        return f"{self.par(oc)}.{pyattr(e.name)}", "?", True

    def ex_Index(self, e):
        oc, ot, _a = self.ex(e.obj)
        ic, it, _b = self.ex(e.idx)
        if is_float(it):
            ic = f"_int({ic})"
        if ot == "string":
            return f"StringGetCharacter({oc}, {ic})", "ushort", True
        return f"{self.par(oc)}[{ic}]", elem(ot) if is_array(ot) else "?", True

    def ex_Cast(self, e):
        c, t, a = self.ex(e.e)
        tn = e.type.name
        if e.type.pointer or tn in self.classes:
            return c, ("P:" + tn) if e.type.pointer else "C:" + tn, a
        dt = self.tstr(e.type)
        if dt == "double" or dt == "float":
            if is_float(t):
                return c, dt, a
            if t == "string":
                return f"StringToDouble({c})", dt, True
            if _is_int_literal(c):
                return c + ".0", dt, True
            return f"float({c})", dt, True
        if dt == "string":
            return self.to_str(c, t), "string", True
        if dt == "bool":
            if t == "bool":
                return c, "bool", a
            return f"_bool({c})", "bool", True
        if is_int(dt):
            if t == "string":
                return f"StringToInteger({c})", dt, True
            if dt.startswith("enum:"):
                if is_float(t):
                    return f"_int({c})", dt, True
                return c, dt, a
            cv = CONVERTER.get(dt, "_int")
            if is_int(t) and t != "?":
                same = {"int": ("int", "short", "char", "uchar", "ushort", "bool"),
                        "long": ("int", "long", "short", "char", "uchar", "ushort", "uint", "bool", "datetime"),
                        "datetime": ("int", "long", "datetime", "uint"), "uint": ("uint", "uchar", "ushort", "color"),
                        "ulong": ("uint", "uchar", "ushort", "ulong")}.get(dt, ())
                if t in same or t.startswith("enum:"):
                    return c, dt, a
            return f"{cv}({c})", dt, True
        return c, dt, a

    def ex_Unary(self, e, cond=False):
        op = e.op
        if op in ("++", "--"):
            return self.incdec_expr(e.e, 1 if op == "++" else -1, post=False)
        if op == "&":
            return self.ex(e.e)
        if op == "*":
            return self.ex(e.e)
        c, t, a = self.ex(e.e, cond=cond) if op == "!" else self.ex(e.e)
        if op == "!":
            if isinstance(e.e, N.Call) and isinstance(e.e.func, N.Name) and e.e.func.id == "IsStopped":
                return "True", "bool", True
            return f"not {self.par(c)}", "bool", False
        if op == "-":
            return f"-{self.par(c)}", (t if is_num(t) else "?"), False
        if op == "+":
            return c, t, a
        if op == "~":
            if t in ("uint", "color"):
                return f"_uint(~{self.par(c)})", t, True
            if t == "ulong":
                return f"_ulong(~{self.par(c)})", t, True
            if t in ("uchar", "ushort"):
                return f"{CONVERTER[t]}(~{self.par(c)})", t, True
            return f"~{self.par(c)}", t, False
        return c, t, a

    def ex_Postfix(self, e):
        return self.incdec_expr(e.e, 1 if e.op == "++" else -1, post=True)

    def incdec_expr(self, target, d, post):
        if isinstance(target, N.Name):
            v = self.lookup(target.id)
            if v is not None and not v.boxed and not v.ref and v.kind in ("local", "param", "global", "static_local", "input"):
                self.note_global_assign(v)
                op = "+" if d > 0 else "-"
                if post:
                    inv = "-" if d > 0 else "+"
                    return f"(({v.py} := {v.py} {op} 1) {inv} 1)", v.type, True
                return f"({v.py} := {v.py} {op} 1)", v.type, True
            if v is not None and (v.boxed or v.ref):
                return f"_incbox({v.py}, {d}, {post})", v.type, True
            if v is not None and v.kind in ("field", "static_field"):
                obj, attr = v.py.rsplit(".", 1)
                return f"_incattr({obj}, {attr!r}, {d}, {post})", v.type, True
        if isinstance(target, N.Index):
            oc, ot = self.ex(target.obj)[:2]
            ic, it = self.ex(target.idx)[:2]
            if is_float(it):
                ic = f"_int({ic})"
            return f"_incitem({oc}, {ic}, {d}, {post})", elem(ot) if is_array(ot) else "?", True
        if isinstance(target, N.Member):
            oc, ot = self.ex(target.obj)[:2]
            ft = "?"
            if is_obj(ot):
                fi = self.find_field(obj_class(ot), target.name)
                if fi:
                    ft = fi[0]
                    if fi[1]:
                        oc = self.cls_py(fi[2])
            return f"_incattr({oc}, {pyattr(target.name)!r}, {d}, {post})", ft, True
        self.rep.warn(target, "unsupported increment target")
        c, t = self.ex(target)[:2]
        return c, t, True

    BIN_PY = {"+": "+", "-": "-", "*": "*", "<": "<", ">": ">", "<=": "<=", ">=": ">=", "==": "==",
              "!=": "!=", "&": "&", "|": "|", "^": "^", "<<": "<<", ">>": ">>"}

    def ex_Binary(self, e, cond=False):
        op = e.op
        if op in ("&&", "||"):
            lc = self.ex(e.l, cond=True)
            rc = self.ex(e.r, cond=True)
            pyop = "and" if op == "&&" else "or"
            l_code = self._logic_operand(lc, op, cond)
            r_code = self._logic_operand(rc, op, cond)
            return f"{l_code} {pyop} {r_code}", "bool", False
        lc, lt, la = self.ex(e.l)
        rc, rt, ra = self.ex(e.r)
        if op in ("==", "!="):
            if lt == "null" or rt == "null":
                other_t = rt if lt == "null" else lt
                other = rc if lt == "null" else lc
                if other_t == "string":
                    return f"{self.par(other)} {'==' if op == '==' else '!='} \"\"", "bool", False
                if is_num(other_t):
                    return f"{self.par(other)} {op} 0", "bool", False
                return f"{self.par(other)} is {'not ' if op == '!=' else ''}None", "bool", False
            if (lt == "string") != (rt == "string") and "?" not in (lt, rt):
                # numeric vs string comparison: MQL converts the string
                if lt == "string":
                    lc = f"StringToDouble({lc})"
                else:
                    rc = f"StringToDouble({rc})"
        if op == "+" and (lt == "string" or rt == "string"):
            left = self.par(self.to_str(lc, lt))
            if isinstance(e.l, N.Binary) and e.l.op == "+" and lt == "string":
                left = lc
            return f"{left} + {self.par(self.to_str(rc, rt))}", "string", False
        if op == "/":
            if is_int(lt) and is_int(rt):
                return f"_idiv({lc}, {rc})", self.arith_type("/", lt, rt), True
            if self.nonzero_const(e.r):
                return f"{self.par(lc)} / {self.par(rc)}", "double", False
            return f"_fdiv({lc}, {rc})", "double", True
        if op == "%":
            if is_float(lt) or is_float(rt):
                return f"MathMod({lc}, {rc})", "double", True
            return f"_imod({lc}, {rc})", self.arith_type("%", lt, rt), True
        pyop = self.BIN_PY[op]
        if op in ("<", ">", "<=", ">=", "==", "!="):
            return f"{self.par(lc)} {pyop} {self.par(rc)}", "bool", False
        if op in ("&", "|", "^"):
            if lt == "bool" and rt == "bool":
                return f"{self.par(lc)} {pyop} {self.par(rc)}", "bool", False
            return f"{self.par(lc)} {pyop} {self.par(rc)}", self.arith_type(op, lt, rt) if is_int(lt) or is_int(rt) else "int", False
        if op == "<<":
            t = lt if is_int(lt) else "int"
            if t in ("int", "uint", "long", "ulong"):
                return f"{CONVERTER[t]}({self.par(lc)} << {self.par(rc)})", t, True
            return f"{self.par(lc)} << {self.par(rc)}", t, False
        if op == ">>":
            return f"{self.par(lc)} >> {self.par(rc)}", lt if is_int(lt) else "int", False
        t = self.arith_type(op, lt, rt)
        if lt == "datetime" and rt == "datetime" and op == "-":
            t = "long"
        left = self.par(lc)
        if isinstance(e.l, N.Binary) and ((op in "+-" and e.l.op in "+-") or (op == "*" and e.l.op == "*")) \
                and not _is_atomic(lc):
            left = lc       # left-associative chain: a + b + c, no nested parentheses
        return f"{left} {pyop} {self.par(rc)}", t, False

    def _logic_operand(self, r, op, cond):
        code, t, atom = r
        if not cond and t != "bool":
            code = f"_bool({code})"
        elif not atom and (" and " in code or " or " in code or code.startswith("not ")):
            code = f"({code})"
        elif not atom and op == "&&" and " or " in code:
            code = f"({code})"
        return code

    def ex_Ternary(self, e):
        cc = self.cond(e.cond)
        ac, at = self.ex(e.a)[:2]
        bc, bt = self.ex(e.b)[:2]
        t = at
        if at != bt:
            if is_num(at) and is_num(bt):
                t = "double" if (is_float(at) or is_float(bt)) else at
            elif at == "null":
                t = bt
            elif at == "?":
                t = bt
        if isinstance(e.b, N.Ternary) and bc.startswith("(") and bc.endswith(")") and " if " in bc:
            inner = bc[1:-1]
            return f"({self.par(ac)} if {self.par(cc)} else {inner})", t, True
        return f"({self.par(ac)} if {self.par(cc)} else {self.par(bc)})", t, True

    def ex_Assign(self, e):
        """Assignment used as an expression value."""
        tgt = e.target
        vc, vt = self.ex(e.value)[:2]
        if e.op != "=":
            bop = e.op[:-1]
            cur_c, cur_t = self.ex(tgt)[:2]
            if bop == "/" and is_int(cur_t) and is_int(vt):
                vc = f"_idiv({cur_c}, {vc})"
            elif bop == "/":
                vc = f"_fdiv({cur_c}, {vc})"
            elif bop == "%":
                vc = f"_imod({cur_c}, {vc})"
            elif bop == "+" and cur_t == "string":
                vc = f"{cur_c} + {self.to_str(vc, vt)}"
            else:
                vc = f"{self.par(cur_c)} {bop} {self.par(vc)}"
            vt = self.arith_type(bop, cur_t, vt) if cur_t != "string" else "string"
        if isinstance(tgt, N.Name):
            v = self.lookup(tgt.id)
            if v is not None:
                vc2 = self.conv(vc, vt, v.type)
                if v.boxed or v.ref:
                    return f"_box_set({v.py}, {vc2})", v.type, True
                if v.kind in ("field", "static_field"):
                    obj, attr = v.py.rsplit(".", 1)
                    return f"_setattr({obj}, {attr!r}, {vc2})", v.type, True
                self.note_global_assign(v)
                return f"({v.py} := {vc2})", v.type, True
        if isinstance(tgt, N.Index):
            oc, ot = self.ex(tgt.obj)[:2]
            ic, it = self.ex(tgt.idx)[:2]
            if is_float(it):
                ic = f"_int({ic})"
            et = elem(ot) if is_array(ot) else "?"
            return f"_setitem({oc}, {ic}, {self.conv(vc, vt, et)})", et, True
        if isinstance(tgt, N.Member):
            oc, ot = self.ex(tgt.obj)[:2]
            ft = "?"
            if is_obj(ot):
                fi = self.find_field(obj_class(ot), tgt.name)
                if fi:
                    ft = fi[0]
                    if fi[1]:
                        oc = self.cls_py(fi[2])
            return f"_setattr({oc}, {pyattr(tgt.name)!r}, {self.conv(vc, vt, ft)})", ft, True
        self.rep.warn(e, "unsupported assignment expression")
        return vc, vt, True

    def ex_Comma(self, e):
        parts = [self.ex(x)[0] for x in e.items]
        t = self.ex(e.items[-1])[1]
        return f"({', '.join(parts)})[-1]", t, True

    def ex_InitList(self, e):
        return "[" + ", ".join(self.ex(x)[0] for x in e.items) + "]", "?", True

    def ex_Sizeof(self, e):
        a = e.arg
        if isinstance(a, N.TypeSpec):
            return str(SIZEOF.get(a.name, 8)), "int", True
        t = self.quick_type(a)
        return str(SIZEOF.get(t, 8)), "int", True

    def ex_New(self, e):
        cname = self.type_alias.get(e.type.name, e.type.name)
        if e.size is not None:
            return f"Arr({self.ex(e.size)[0]}, factory={self.cls_py(cname)})", "P:" + cname + "[]", True
        args = self.call_args_for_ctor(cname, e.args) if cname in self.classes else ", ".join(self.ex(a)[0] for a in e.args)
        return f"{self.cls_py(cname)}({args})", "P:" + cname, True

    # ================================================================ calls

    def ex_Call(self, e):
        fn = e.func
        if isinstance(fn, N.Name):
            return self.call_name(fn.id, e)
        if isinstance(fn, N.Member):
            oc, ot, _a = self.ex(fn.obj)
            if is_obj(ot):
                cname = obj_class(ot)
                ms, owner = self.find_methods(cname, fn.name)
                if ms:
                    f = self.pick_overload(ms, e.args)
                    rt = self.tstr(f.ret)
                    return f"{self.par(oc)}.{self.method_py(owner, f)}({self.call_args(f, e.args)})", rt, True
                fi = self.find_field(cname, fn.name)
                if fi is not None:     # function pointer member
                    return f"{self.par(oc)}.{pyattr(fn.name)}({self.plain_args(e.args)})", "?", True
            return f"{self.par(oc)}.{pyattr(fn.name)}({self.plain_args(e.args)})", "?", True
        if isinstance(fn, N.Scope):
            if fn.cls == "":
                return self.call_name(fn.id, e, global_only=True)
            if fn.cls in self.classes:
                ms, owner = self.find_methods(fn.cls, fn.id)
                if ms:
                    f = self.pick_overload(ms, e.args)
                    rt = self.tstr(f.ret)
                    if f.static:
                        return f"{self.cls_py(owner)}.{self.method_py(owner, f)}({self.call_args(f, e.args)})", rt, True
                    args = self.call_args(f, e.args)
                    return f"{self.cls_py(owner)}.{self.method_py(owner, f)}(self{', ' if args else ''}{args})", rt, True
            return f"{pyname(fn.cls)}.{pyattr(fn.id)}({self.plain_args(e.args)})", "?", True
        c, t = self.ex(fn)[:2]
        return f"{self.par(c)}({self.plain_args(e.args)})", "?", True

    def plain_args(self, args):
        return ", ".join(self.ex(a)[0] for a in args)

    def call_args(self, f: N.FuncDecl, args) -> str:
        out = []
        params = f.params
        for i, a in enumerate(args):
            if i < len(params) and params[i].type.name != "...":
                p = params[i]
                pt = self.tstr(p.type, p.dims)
                if p.type.ref and not p.dims and not is_array(pt) and not (is_obj(pt) and not is_ptr(pt)) \
                        and not p.type.const:
                    out.append(self.ref_arg(a))
                    continue
                c, t = self.ex(a)[:2]
                if is_obj(pt) and not is_ptr(pt) and not p.type.ref and self._is_lvalue(a) and not is_array(pt):
                    out.append(f"_copy({c})")
                else:
                    out.append(self.conv(c, t, pt))
            else:
                out.append(self.ex(a)[0])
        return ", ".join(out)

    def ref_arg(self, a) -> str:
        """Reference to an lvalue for a scalar reference parameter."""
        if isinstance(a, N.Name):
            v = self.lookup(a.id)
            if v is not None:
                if v.boxed or v.ref:
                    return v.py
                if v.kind in ("global", "input", "static_local"):
                    return f"_GlobRef(globals(), {v.py!r})"
                if v.kind in ("field", "static_field"):
                    obj, attr = v.py.rsplit(".", 1)
                    return f"_AttrRef({obj}, {attr!r})"
                self.rep.warn(a, f"local {a.id} passed by reference but not boxed")
                return f"_ValRef({v.py})"
        if isinstance(a, N.Index):
            oc = self.ex(a.obj)[0]
            ic, it = self.ex(a.idx)[:2]
            if is_float(it):
                ic = f"_int({ic})"
            return f"_ElemRef({oc}, {ic})"
        if isinstance(a, N.Member):
            oc, ot = self.ex(a.obj)[:2]
            if is_obj(ot):
                fi = self.find_field(obj_class(ot), a.name)
                if fi and fi[1]:
                    return f"_AttrRef({self.cls_py(fi[2])}, {pyattr(a.name)!r})"
            return f"_AttrRef({oc}, {pyattr(a.name)!r})"
        if isinstance(a, N.Scope):
            if a.cls in self.classes:
                return f"_AttrRef({self.cls_py(a.cls)}, {pyattr(a.id)!r})"
            v = self.globals.get(a.id)
            if v is not None:
                return f"_GlobRef(globals(), {v.py!r})"
        c = self.ex(a)[0]
        return f"_ValRef({c})"

    def call_name(self, name, e: N.Call, global_only=False):
        args = e.args
        # function-pointer variable
        if not global_only:
            v = self.lookup(name)
            if v is not None and (v.type.startswith("fn:") or v.type == "?") and name not in self.funcs:
                return f"{v.py}({self.plain_args(args)})", "?", True
            if self.cur_cls is not None:
                ms, owner = self.find_methods(self.cur_cls.name, name)
                if ms:
                    f = self.pick_overload(ms, args)
                    rt = self.tstr(f.ret)
                    if f.static or self.cur_static:
                        return f"{self.cls_py(owner)}.{self.method_py(owner, f)}({self.call_args(f, args)})", rt, True
                    return f"self.{self.method_py(owner, f)}({self.call_args(f, args)})", rt, True
        if name in self.funcs:
            cands = self.funcs[name]
            f = self.pick_overload(cands, args)
            fits = sum(1 for p in f.params if p.default is None and p.type.name != "...") <= len(args) <= len(f.params) \
                or any(p.type.name == "..." for p in f.params)
            if fits or name not in self.rt:
                rt = self.tstr(f.ret)
                return f"{self.func_py[id(f)]}({self.call_args(f, args)})", rt, True
        if name in self.classes:
            return f"{self.cls_py(name)}({self.call_args_for_ctor(name, args)})", "C:" + name, True
        return self.call_builtin(name, args, e)

    def call_builtin(self, name, args, e):
        if name == "IsStopped":
            return "False", "bool", True
        if name in ("GetPointer",):
            return self.ex(args[0])[0], self.ex(args[0])[1], True
        if name == "EnumToString" and args:
            c, t = self.ex(args[0])[:2]
            en = t[5:] if t.startswith("enum:") else ""
            return f"EnumToString({c}, {en!r})", "string", True
        if name == "typename" and args:
            t = self.quick_type(args[0])
            return _pystr(t.replace("C:", "").replace("P:", "").replace("enum:", "")), "string", True
        if name in ("ArraySize",) and args:
            pass
        refs = set()
        spec = BUILTIN_REFS.get(name)
        if spec:
            refs = set(spec.get(len(args), spec.get(None, ())))
        out = []
        dt_args = ()
        if name in _COPY_FUNCS:
            dt_args = (1, 2) if name == "CopyTicksRange" else (2, 3)
        for i, a in enumerate(args):
            if i in dt_args and self.quick_type(a) == "datetime" and i not in refs:
                out.append(f"_DT({self.ex(a)[0]})")
                continue
            if i in refs:
                t = self.quick_type(a)
                if name == "ZeroMemory" and (is_array(t) or (is_obj(t))):
                    out.append(self.ex(a)[0])
                    continue
                if name in ("TimeToStruct", "SymbolInfoTick"):
                    out.append(self.ex(a)[0])
                    continue
                out.append(self.ref_arg(a))
            else:
                out.append(self.ex(a)[0])
        rt = BUILTIN_RET.get(name)
        if name not in self.rt:
            self.rep.unknown_funcs.add(name)
            return f"_missing({name!r})({', '.join(out)})", rt or "?", True
        if rt is None:
            from . import rt_consts
            rt = rt_consts.FUNC_TYPES.get(name, "?")
        if name in ("MathMax", "MathMin", "fmax", "fmin", "MathAbs", "fabs") and args:
            ts = [self.quick_type(a) for a in args]
            if all(is_int(t) for t in ts):
                rt = "int" if all(t in ("int", "short", "char", "uchar", "ushort", "bool") or t.startswith("enum:") for t in ts) else "long"
        return f"{name}({', '.join(out)})", rt, True


_COPY_FUNCS = {"CopyTime", "CopyOpen", "CopyHigh", "CopyLow", "CopyClose", "CopyTickVolume", "CopyRealVolume",
               "CopySpread", "CopyRates", "CopyBuffer"}

OPERATOR_METHODS = {
    "[]": "__getitem__", "=": "_q_assign", "==": "__eq__", "!=": "__ne__", "<": "__lt__", ">": "__gt__",
    "<=": "__le__", ">=": "__ge__", "+": "__add__", "-": "__sub__", "*": "__mul__", "/": "__truediv__",
    "+=": "__iadd__", "-=": "__isub__", "*=": "__imul__", "/=": "__itruediv__", "()": "__call__",
    "!": "_q_not", "%": "__mod__", "&": "__and__", "|": "__or__", "^": "__xor__", "<<": "__lshift__",
    ">>": "__rshift__", "&&": "_q_and", "||": "_q_or", "~": "__invert__", "++": "_q_inc", "--": "_q_dec",
}


def _pystr(s: str) -> str:
    r = repr(s)
    return r


_ATOM_RE = re.compile(r"^[\w.]+$|^-?\d+(\.\d*)?([eE][-+]?\d+)?$")


def _is_atomic(code: str) -> bool:
    if _ATOM_RE.match(code):
        return True
    # a single call / index / parenthesised expression
    if code and code[0] in "([" and _matching(code, 0) == len(code) - 1:
        return True
    depth = 0
    in_str = None
    i = 0
    n = len(code)
    # name followed by balanced (...)/[...] groups only
    m = re.match(r"^[\w.]+", code)
    if not m:
        if code.startswith(("'", '"')):
            j = _str_end(code, 0)
            return j == n - 1
        return False
    i = m.end()
    while i < n:
        if code[i] in "([":
            j = _matching(code, i)
            if j < 0:
                return False
            i = j + 1
            if i < n and code[i] == ".":
                m2 = re.match(r"\.[\w]+", code[i:])
                if not m2:
                    return False
                i += m2.end()
            continue
        return False
    return True


def _str_end(code, i):
    q = code[i]
    j = i + 1
    while j < len(code):
        if code[j] == "\\":
            j += 2
            continue
        if code[j] == q:
            return j
        j += 1
    return -1


def _matching(code: str, i: int) -> int:
    pairs = {"(": ")", "[": "]", "{": "}"}
    stack = []
    j = i
    n = len(code)
    while j < n:
        ch = code[j]
        if ch in "'\"":
            j = _str_end(code, j)
            if j < 0:
                return -1
        elif ch in pairs:
            stack.append(pairs[ch])
        elif ch in ")]}":
            if not stack or stack.pop() != ch:
                return -1
            if not stack:
                return j
        j += 1
    return -1


def _is_int_literal(code: str) -> bool:
    return bool(re.fullmatch(r"-?\d+", code))


def _looks_int(code: str) -> bool:
    return _is_int_literal(code)
