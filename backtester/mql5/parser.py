"""Recursive-descent parser for MQL5 (after preprocessing) → :mod:`.nodes` AST."""

from __future__ import annotations

from .lexer import MqlSyntaxError, Token
from .nodes import (
    Assign, Binary, Block, Break, Call, Cast, Char, ClassDecl, Comma, Continue, DeclStmt,
    Delete, DoWhile, Empty, EnumDecl, ExprStmt, For, FuncDecl, If, Index, InitList, Member,
    Name, New, Num, Param, Postfix, Program, Return, Scope, Sizeof, Str, Switch, Ternary,
    This, Typedef, TypeSpec, Unary, VarDecl, While,
)

BUILTIN_TYPES = {
    "void", "bool", "char", "uchar", "short", "ushort", "int", "uint", "long", "ulong",
    "float", "double", "string", "datetime", "color", "matrix", "vector", "matrixf", "vectorf",
    "complex", "vectorc", "matrixc",
}
BUILTIN_STRUCTS = {
    "MqlRates", "MqlDateTime", "MqlTick", "MqlParam", "MqlBookInfo", "MqlTradeRequest",
    "MqlTradeResult", "MqlTradeCheckResult", "MqlTradeTransaction", "MqlCalendarValue",
    "MqlCalendarEvent", "MqlCalendarCountry",
}
MODIFIERS = {"const", "static", "input", "sinput", "extern", "virtual", "public", "private",
             "protected", "register", "volatile", "inline", "override", "final"}

ASSIGN_OPS = {"=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>="}
BIN_PREC = [
    ("||",), ("&&",), ("|",), ("^",), ("&",), ("==", "!="), ("<", ">", "<=", ">="),
    ("<<", ">>"), ("+", "-"), ("*", "/", "%"),
]


class Parser:
    def __init__(self, tokens: list[Token], comments=None):
        self.t = tokens
        self.i = 0
        self.comments = comments or {}
        self.types: set[str] = set(BUILTIN_TYPES) | set(BUILTIN_STRUCTS)
        self.enum_names: set[str] = set()
        self.template_types: set[str] = set()
        self._prescan()

    # ----------------------------------------------------------------- utils

    def _prescan(self):
        t = self.t
        for k in range(len(t) - 1):
            a = t[k]
            if a.kind == "ID" and a.value in ("class", "struct", "enum", "interface", "union") and t[k + 1].kind == "ID":
                self.types.add(t[k + 1].value)
                if a.value == "enum":
                    self.enum_names.add(t[k + 1].value)
                # template class?
                j = k - 1
                if j >= 0 and t[j].is_op(">"):
                    # walk back to 'template'
                    depth = 0
                    while j >= 0:
                        if t[j].is_op(">"):
                            depth += 1
                        elif t[j].is_op("<"):
                            depth -= 1
                            if depth == 0:
                                break
                        j -= 1
                    if j >= 1 and t[j - 1].is_id("template"):
                        self.template_types.add(t[k + 1].value)
            if a.kind == "ID" and a.value == "typedef":
                # typedef <type> NAME;   or  typedef ret (*NAME)(...);
                j = k + 1
                depth = 0
                last_id = None
                while j < len(t) and not (t[j].is_op(";") and depth == 0):
                    if t[j].is_op("("):
                        depth += 1
                        if t[j + 1].is_op("*") and t[j + 2].kind == "ID":
                            last_id = t[j + 2].value
                            break
                    elif t[j].is_op(")"):
                        depth -= 1
                    elif t[j].kind == "ID" and depth == 0:
                        last_id = t[j].value
                    j += 1
                if last_id:
                    self.types.add(last_id)

    def peek(self, k=0) -> Token:
        j = self.i + k
        return self.t[j] if j < len(self.t) else self.t[-1]

    def next(self) -> Token:
        tok = self.t[self.i]
        self.i += 1
        return tok

    def error(self, msg, tok=None):
        tok = tok or self.peek()
        raise MqlSyntaxError(f"{msg} (got {tok.kind} {tok.value!r})", tok.file, tok.line)

    def expect_op(self, v) -> Token:
        tok = self.peek()
        if not tok.is_op(v):
            self.error(f"expected '{v}'")
        return self.next()

    def accept_op(self, v) -> bool:
        if self.peek().is_op(v):
            self.i += 1
            return True
        return False

    def accept_id(self, v) -> bool:
        if self.peek().is_id(v):
            self.i += 1
            return True
        return False

    def expect_id(self) -> str:
        tok = self.peek()
        if tok.kind != "ID":
            self.error("expected identifier")
        self.i += 1
        return tok.value

    def _node(self, node, tok):
        node.line = tok.line
        node.file = tok.file
        return node

    def is_type_name(self, name: str) -> bool:
        return name in self.types or name in self.template_types or name.startswith("ENUM_") \
            or name in self._tparams_scope()

    _tp_stack: list

    def _tparams_scope(self):
        return getattr(self, "_tp", set())

    def comment_at(self, tok):
        return self.comments.get((tok.file, tok.line), "")

    # ----------------------------------------------------------------- program

    def parse_program(self) -> Program:
        decls = []
        self._tp = set()
        while self.peek().kind != "EOF":
            if self.accept_op(";"):
                continue
            decls.extend(self.parse_external())
        return Program(decls)

    def parse_external(self):
        tok = self.peek()
        if tok.is_id("__IMPORT_BEGIN__"):
            self.next()
            lib = self.next().value
            out = []
            while not self.peek().is_id("__IMPORT_END__") and self.peek().kind != "EOF":
                if self.accept_op(";"):
                    continue
                for d in self.parse_external():
                    if isinstance(d, FuncDecl):
                        d.imported = lib
                    out.append(d)
            self.accept_id("__IMPORT_END__")
            return out
        if tok.is_id("template"):
            return [self.parse_template()]
        if tok.is_id("enum"):
            e = self.parse_enum()
            self.accept_op(";")
            return [e]
        if tok.kind == "ID" and tok.value in ("class", "struct", "interface", "union"):
            c = self.parse_class()
            out = [c]
            # struct Foo {...} var;
            if self.peek().kind == "ID" or self.peek().is_op("*"):
                ts = TypeSpec(c.name)
                out.extend(self.parse_declarators(ts, set(), self.peek()))
            self.accept_op(";")
            return out
        if tok.is_id("typedef"):
            return [self.parse_typedef()]
        if tok.is_id("input") and self.peek(1).is_id("group"):
            self.i += 2
            if self.peek().kind == "STR":
                self.next()
            self.accept_op(";")
            return []
        if tok.kind == "ID" and self.is_type_name(tok.value) and self.peek(1).is_op(";"):
            self.i += 2
            return []
        return self.parse_decl_or_func(top=True)

    def parse_template(self):
        tok = self.next()  # template
        self.expect_op("<")
        tps = []
        while not self.peek().is_op(">"):
            if self.peek().kind == "ID" and self.peek().value in ("typename", "class"):
                self.next()
            tps.append(self.expect_id())
            self.accept_op(",")
        self.expect_op(">")
        saved = self._tp
        self._tp = set(saved) | set(tps)
        try:
            if self.peek().kind == "ID" and self.peek().value in ("class", "struct"):
                c = self.parse_class()
                c.tparams = tps
                self.accept_op(";")
                return c
            ds = self.parse_decl_or_func(top=True)
            for d in ds:
                if isinstance(d, FuncDecl):
                    d.tparams = tps
            return ds[0] if ds else Program([])
        finally:
            self._tp = saved

    def parse_typedef(self):
        tok = self.next()
        ts = self.parse_type()
        if self.peek().is_op("(") and self.peek(1).is_op("*"):
            self.next()
            self.next()
            name = self.expect_id()
            self.expect_op(")")
            params = self.parse_params()
            self.expect_op(";")
            self.types.add(name)
            return self._node(Typedef(name, ts, params), tok)
        name = self.expect_id()
        self.expect_op(";")
        self.types.add(name)
        return self._node(Typedef(name, ts), tok)

    def parse_enum(self):
        tok = self.next()  # enum
        name = ""
        if self.peek().kind == "ID":
            name = self.next().value
            self.types.add(name)
        if self.accept_op(":"):
            self.parse_type()
        items = []
        if not self.accept_op("{"):
            return self._node(EnumDecl(name, []), tok)
        while not self.peek().is_op("}"):
            it = self.peek()
            iname = self.expect_id()
            val = None
            if self.accept_op("="):
                val = self.parse_assign_expr()
            items.append([iname, val, self.comment_at(it)])
            if not self.accept_op(","):
                break
        # comment after the last item (same line) — label
        self.expect_op("}")
        return self._node(EnumDecl(name, items), tok)

    def parse_class(self):
        tok = self.next()
        kind = tok.value
        name = self.expect_id() if self.peek().kind == "ID" else f"_anon{tok.line}"
        self.types.add(name)
        if self.peek().is_op("<"):        # specialization: skip
            self._skip_angles()
        base = None
        if self.accept_op(":"):
            while self.peek().kind == "ID" and self.peek().value in ("public", "private", "protected", "virtual"):
                self.next()
            base = self.parse_type()
            while self.accept_op(","):   # multiple inheritance (interfaces)
                while self.peek().kind == "ID" and self.peek().value in ("public", "private", "protected"):
                    self.next()
                self.parse_type()
        c = self._node(ClassDecl(kind, name, base), tok)
        if not self.peek().is_op("{"):
            c.forward = True
            return c
        self.expect_op("{")
        access = "private" if kind == "class" else "public"
        while not self.peek().is_op("}"):
            t = self.peek()
            if self.accept_op(";"):
                continue
            if t.kind == "ID" and t.value in ("public", "private", "protected") and self.peek(1).is_op(":"):
                access = t.value
                self.i += 2
                continue
            if t.is_id("enum"):
                c.members.append(self.parse_enum())
                self.accept_op(";")
                continue
            if t.kind == "ID" and t.value in ("class", "struct") and self.peek(2).is_op("{") or \
                    (t.kind == "ID" and t.value in ("class", "struct") and self.peek(2).is_op(":")):
                inner = self.parse_class()
                c.members.append(inner)
                if self.peek().kind == "ID":
                    c.members.extend(self.parse_declarators(TypeSpec(inner.name), set(), self.peek()))
                self.accept_op(";")
                continue
            if t.is_id("template"):
                d = self.parse_template()
                if isinstance(d, FuncDecl):
                    d.access = access
                c.members.append(d)
                continue
            if t.is_id("typedef"):
                c.members.append(self.parse_typedef())
                continue
            ms = self.parse_member(name)
            for m in ms:
                m.access = access
            c.members.extend(ms)
        self.expect_op("}")
        return c

    def parse_member(self, cls):
        start = self.peek()
        mods = set()
        while self.peek().kind == "ID" and self.peek().value in MODIFIERS:
            mods.add(self.next().value)
        # constructor / destructor
        if self.peek().is_op("~") and self.peek(1).is_id(cls):
            self.i += 2
            params = self.parse_params()
            f = self._node(FuncDecl(TypeSpec("void"), "~" + cls, params), start)
            f.kind = "dtor"
            f.virtual = "virtual" in mods
            self._func_tail(f)
            return [f]
        if self.peek().is_id(cls) and self.peek(1).is_op("("):
            self.next()
            params = self.parse_params()
            f = self._node(FuncDecl(TypeSpec("void"), cls, params), start)
            f.kind = "ctor"
            self._func_tail(f)
            return [f]
        ts = self.parse_type(mods)
        return self._after_type(ts, mods, start, member_of=cls)

    def _func_tail(self, f):
        while self.peek().kind == "ID" and self.peek().value in ("const", "override", "final"):
            if self.next().value == "const":
                f.const = True
        if self.accept_op(":"):
            # initializer list
            while True:
                nm = self.expect_id()
                if self.peek().is_op("<"):
                    self._skip_angles()
                self.expect_op("(")
                args = self.parse_args_until(")")
                f.inits.append((nm, args))
                if not self.accept_op(","):
                    break
        if self.accept_op("="):
            self.next()   # 0 / delete / default
            f.pure = True
            self.accept_op(";")
            return
        if self.peek().is_op("{"):
            f.body = self.parse_block()
        else:
            self.accept_op(";")

    def _skip_angles(self):
        depth = 0
        while True:
            t = self.next()
            if t.is_op("<"):
                depth += 1
            elif t.is_op(">"):
                depth -= 1
                if depth == 0:
                    return
            elif t.is_op(">>"):
                depth -= 2
                if depth <= 0:
                    return

    # ----------------------------------------------------------------- types

    def parse_type(self, mods=None) -> TypeSpec:
        mods = mods if mods is not None else set()
        while self.peek().kind == "ID" and self.peek().value in MODIFIERS \
                and self.peek().value not in ("unsigned", "signed"):
            mods.add(self.next().value)
        tok = self.peek()
        if tok.kind != "ID":
            self.error("expected type")
        name = self.next().value
        if name in ("unsigned", "signed"):
            # 'unsigned int' etc.
            if self.peek().kind == "ID" and self.peek().value in ("int", "char", "short", "long"):
                inner = self.next().value
                name = ("u" + inner) if name == "unsigned" else inner
            else:
                name = "uint" if name == "unsigned" else "int"
        if name in ("class", "struct", "enum"):   # elaborated type specifier
            name = self.expect_id()
        targs = []
        if self.peek().is_op("<") and (name in self.template_types or name in self.types):
            targs = self._parse_targs()
        while self.peek().is_op("::") and self.peek(1).kind == "ID" and self.is_type_name(self.peek(1).value) \
                and not self.peek(2).is_op("("):   # Outer::Inner
            self.next()
            name = self.next().value
        while self.peek().kind == "ID" and self.peek().value in ("const",):
            self.next()
            mods.add("const")
        ts = self._node(TypeSpec(name, targs, const="const" in mods), tok)
        if self.accept_op("*"):
            ts.pointer = True
            while self.accept_op("*"):
                pass
        if self.peek().is_id("const"):
            self.next()
        if self.accept_op("&"):
            ts.ref = True
        return ts

    def _parse_targs(self):
        self.expect_op("<")
        out = []
        while True:
            if self.peek().is_op(">"):
                self.next()
                break
            if self.peek().is_op(">>"):
                # close two levels: replace token
                tok = self.t[self.i]
                self.t[self.i] = Token("OP", ">", tok.file, tok.line)
                break
            if self.peek().kind == "NUM":
                self.next()
                out.append(TypeSpec("int"))
            else:
                out.append(self.parse_type())
            self.accept_op(",")
        return out

    def starts_type(self, k=0) -> bool:
        tok = self.peek(k)
        if tok.kind != "ID":
            return False
        if tok.value in MODIFIERS and tok.value not in ("public", "private", "protected"):
            return True
        return self.is_type_name(tok.value) or tok.value in ("unsigned", "signed")

    # ------------------------------------------------------------- declarations

    def parse_decl_or_func(self, top=False):
        start = self.peek()
        mods = set()
        while self.peek().kind == "ID" and self.peek().value in MODIFIERS:
            mods.add(self.next().value)
        if self.peek().is_id("enum"):
            e = self.parse_enum()
            out = [e]
            if self.peek().kind == "ID":
                out.extend(self.parse_declarators(TypeSpec(e.name or "int"), mods, start))
            self.accept_op(";")
            return out
        if self.peek().kind == "ID" and self.peek(1).is_op("::") and (
                self.peek(2).is_op("~") or (self.peek(2).is_id(self.peek().value) and self.peek(3).is_op("("))):
            cls = self.next().value
            self.next()
            dtor = self.accept_op("~")
            nm = self.expect_id()
            params = self.parse_params()
            f = self._node(FuncDecl(TypeSpec("void"), ("~" if dtor else "") + nm, params), start)
            f.kind = "dtor" if dtor else "ctor"
            f.cls = cls
            self._func_tail(f)
            return [f]
        if self.peek().kind == "ID" and self.peek().value in ("struct", "class") and self.peek(2).is_op("{"):
            c = self.parse_class()
            out = [c]
            if self.peek().kind == "ID":
                out.extend(self.parse_declarators(TypeSpec(c.name), mods, start))
            self.accept_op(";")
            return out
        ts = self.parse_type(mods)
        return self._after_type(ts, mods, start)

    def _after_type(self, ts, mods, start, member_of=None):
        # out-of-class method:  Type Class::name(  /  Class::Class( / Class::~Class(
        if self.peek().kind == "ID" and self.peek(1).is_op("::"):
            cls = self.next().value
            self.next()
            if self.accept_op("~"):
                nm = self.expect_id()
                params = self.parse_params()
                f = self._node(FuncDecl(TypeSpec("void"), "~" + nm, params), start)
                f.kind = "dtor"
                f.cls = cls
                self._func_tail(f)
                return [f]
            if self.peek().is_id("operator"):
                self.next()
                op = self._operator_symbol()
                params = self.parse_params()
                f = self._node(FuncDecl(ts, "operator" + op, params), start)
                f.kind = "operator"
                f.cls = cls
                self._func_tail(f)
                return [f]
            nm = self.expect_id()
            if self.peek().is_op("<"):
                self._skip_angles()
            if self.peek().is_op("("):
                params = self.parse_params()
                f = self._node(FuncDecl(ts, nm, params), start)
                f.cls = cls
                if nm == cls:
                    f.kind = "ctor"
                self._func_tail(f)
                return [f]
            # static member definition: int CFoo::count = 0;
            d = self._node(VarDecl(ts, nm, storage=mods | {"static_def"}), start)
            d.storage.add("cls:" + cls)
            dims = []
            while self.accept_op("["):
                dims.append(None if self.peek().is_op("]") else self.parse_expr())
                self.expect_op("]")
            d.dims = dims
            if self.accept_op("="):
                d.init = self.parse_initializer()
            self.expect_op(";")
            return [d]
        # constructor declared as ClassName(...) when type parsed as the name (out-of-class handled above)
        if member_of is None and ts.name in self.types and self.peek().is_op("(") and False:
            pass
        if self.peek().is_id("operator"):
            self.next()
            op = self._operator_symbol()
            params = self.parse_params()
            f = self._node(FuncDecl(ts, "operator" + op, params), start)
            f.kind = "operator"
            f.virtual = "virtual" in mods
            f.static = "static" in mods
            self._func_tail(f)
            return [f]
        # function?
        if self.peek().kind == "ID" and self.peek(1).is_op("("):
            name_tok = self.next()
            # distinguish CFoo obj(args); (object with ctor args) from a function
            if self._looks_like_params():
                params = self.parse_params()
                f = self._node(FuncDecl(ts, name_tok.value, params), start)
                f.virtual = "virtual" in mods
                f.static = "static" in mods
                self._func_tail(f)
                return [f]
            self.i -= 1
        return self.parse_declarators(ts, mods, start)

    def _looks_like_params(self) -> bool:
        # at '(' : params if empty, 'void)', or starts with a type/modifier followed by declarator
        j = self.i + 1
        t = self.t
        if t[j].is_op(")"):
            # `CFoo obj();` is a function declaration in C++ too
            return True
        if t[j].kind == "ID" and t[j].value in ("const", "void", "unsigned", "signed"):
            return True
        if t[j].kind == "ID" and self.is_type_name(t[j].value):
            # type followed by name or & or * or [
            k = j + 1
            if t[k].is_op("<"):
                return True
            if t[k].is_op("::"):
                return True
            return t[k].kind == "ID" or t[k].is_op("&") or t[k].is_op("*") or t[k].is_op(",") \
                or t[k].is_op(")") or t[k].is_op("[")
        return False

    def _operator_symbol(self) -> str:
        t = self.next()
        if t.is_op("(") and self.peek().is_op(")"):
            self.next()
            return "()"
        if t.is_op("[") and self.peek().is_op("]"):
            self.next()
            return "[]"
        if t.kind == "ID":   # conversion operator
            return " " + t.value
        return t.value

    def parse_params(self) -> list[Param]:
        self.expect_op("(")
        params = []
        while not self.peek().is_op(")"):
            if self.peek().is_op("..."):
                self.next()
                params.append(Param(TypeSpec("..."), "__varargs"))
                continue
            if self.peek().is_id("void") and self.peek(1).is_op(")"):
                self.next()
                break
            tok = self.peek()
            ts = self.parse_type()
            name = ""
            if self.peek().kind == "ID":
                name = self.next().value
            dims = []
            while self.accept_op("["):
                dims.append(None if self.peek().is_op("]") else self.parse_expr())
                self.expect_op("]")
            default = None
            if self.accept_op("="):
                default = self.parse_assign_expr()
            p = self._node(Param(ts, name or f"_p{len(params)}", default, dims), tok)
            params.append(p)
            if not self.accept_op(","):
                break
        self.expect_op(")")
        return params

    def parse_declarators(self, ts, mods, start) -> list[VarDecl]:
        out = []
        while True:
            dts = TypeSpec(ts.name, ts.targs, ts.const, ts.pointer, ts.ref)
            dts.line, dts.file = ts.line, ts.file
            while self.accept_op("*"):
                dts.pointer = True
            if self.accept_op("&"):
                dts.ref = True
            ntok = self.peek()
            name = self.expect_id()
            dims = []
            while self.accept_op("["):
                dims.append(None if self.peek().is_op("]") else self.parse_expr())
                self.expect_op("]")
            d = self._node(VarDecl(dts, name, dims, storage=mods), ntok)
            if self.accept_op("="):
                d.init = self.parse_initializer()
            elif self.peek().is_op("("):
                self.next()
                d.ctor_args = self.parse_args_until(")")
            d.comment = self.comment_at(ntok) or self.comment_at(self.peek())
            out.append(d)
            if self.accept_op(","):
                continue
            break
        tail = self.peek()
        if not self.accept_op(";"):
            self.error("expected ';' after declaration")
        if out and not out[-1].comment:
            out[-1].comment = self.comment_at(tail)
        return out

    def parse_initializer(self):
        if self.peek().is_op("{"):
            tok = self.next()
            items = []
            while not self.peek().is_op("}"):
                items.append(self.parse_initializer())
                if not self.accept_op(","):
                    break
            self.expect_op("}")
            return self._node(InitList(items), tok)
        return self.parse_assign_expr()

    # ------------------------------------------------------------- statements

    def parse_block(self) -> Block:
        tok = self.expect_op("{")
        body = []
        while not self.peek().is_op("}"):
            if self.peek().kind == "EOF":
                self.error("unexpected end of file in block")
            body.append(self.parse_stmt())
        self.expect_op("}")
        return self._node(Block(body), tok)

    def parse_stmt(self):
        tok = self.peek()
        if tok.kind == "OP":
            if tok.value == "{":
                return self.parse_block()
            if tok.value == ";":
                self.next()
                return self._node(Empty(), tok)
        if tok.kind == "ID":
            v = tok.value
            if v == "if":
                self.next()
                self.expect_op("(")
                cond = self.parse_expr()
                self.expect_op(")")
                then = self.parse_stmt()
                els = None
                if self.accept_id("else"):
                    els = self.parse_stmt()
                return self._node(If(cond, then, els), tok)
            if v == "for":
                self.next()
                self.expect_op("(")
                init = None
                if not self.peek().is_op(";"):
                    if self._is_decl_start():
                        init = self._node(DeclStmt(self._local_decls(semicolon=False)), tok)
                    else:
                        init = self._node(ExprStmt(self.parse_expr()), tok)
                self.expect_op(";")
                cond = None if self.peek().is_op(";") else self.parse_expr()
                self.expect_op(";")
                step = None if self.peek().is_op(")") else self.parse_expr()
                self.expect_op(")")
                body = self.parse_stmt()
                return self._node(For(init, cond, step, body), tok)
            if v == "while":
                self.next()
                self.expect_op("(")
                cond = self.parse_expr()
                self.expect_op(")")
                body = self.parse_stmt()
                return self._node(While(cond, body), tok)
            if v == "do":
                self.next()
                body = self.parse_stmt()
                if not self.accept_id("while"):
                    self.error("expected 'while'")
                self.expect_op("(")
                cond = self.parse_expr()
                self.expect_op(")")
                self.accept_op(";")
                return self._node(DoWhile(body, cond), tok)
            if v == "switch":
                return self.parse_switch()
            if v == "break":
                self.next()
                self.accept_op(";")
                return self._node(Break(), tok)
            if v == "continue":
                self.next()
                self.accept_op(";")
                return self._node(Continue(), tok)
            if v == "return":
                self.next()
                e = None
                if not self.peek().is_op(";"):
                    e = self.parse_expr()
                self.accept_op(";")
                return self._node(Return(e), tok)
            if v == "delete":
                self.next()
                if self.accept_op("["):
                    self.expect_op("]")
                e = self.parse_expr()
                self.accept_op(";")
                return self._node(Delete(e), tok)
            if v == "enum":
                e = self.parse_enum()
                self.accept_op(";")
                return self._node(DeclStmt([e]), tok)
            if v in ("struct", "class") and self.peek(2).is_op("{"):
                c = self.parse_class()
                decls = [c]
                if self.peek().kind == "ID":
                    decls.extend(self.parse_declarators(TypeSpec(c.name), set(), tok))
                else:
                    self.accept_op(";")
                return self._node(DeclStmt(decls), tok)
            if v == "typedef":
                return self._node(DeclStmt([self.parse_typedef()]), tok)
            if self.is_type_name(v) and self.peek(1).is_op(";"):
                self.i += 2
                return self._node(Empty(), tok)
            if self._is_decl_start():
                return self._node(DeclStmt(self._local_decls()), tok)
        e = self.parse_expr()
        if not self.accept_op(";"):
            self.error("expected ';'")
        return self._node(ExprStmt(e), tok)

    def _is_decl_start(self) -> bool:
        tok = self.peek()
        if tok.kind != "ID":
            return False
        if tok.value in ("const", "static", "input", "sinput", "extern", "unsigned", "signed"):
            return True
        if not self.is_type_name(tok.value):
            return False
        # Type followed by declarator: ID, *ID, &ID, <targs>, ::
        nxt = self.peek(1)
        if nxt.kind == "ID":
            return True
        if nxt.is_op("*") or nxt.is_op("&"):
            return self.peek(2).kind == "ID" and not self.peek(3).is_op("(") or self.peek(2).kind == "ID"
        if nxt.is_op("<") and tok.value in self.template_types:
            return True
        if nxt.is_op("::") and self.peek(2).kind == "ID" and self.peek(3).kind == "ID":
            return True
        return False

    def _local_decls(self, semicolon=True):
        start = self.peek()
        mods = set()
        while self.peek().kind == "ID" and self.peek().value in MODIFIERS:
            mods.add(self.next().value)
        ts = self.parse_type(mods)
        out = []
        while True:
            dts = TypeSpec(ts.name, ts.targs, ts.const, ts.pointer, ts.ref)
            dts.line, dts.file = ts.line, ts.file
            while self.accept_op("*"):
                dts.pointer = True
            if self.accept_op("&"):
                dts.ref = True
            ntok = self.peek()
            name = self.expect_id()
            dims = []
            while self.accept_op("["):
                dims.append(None if self.peek().is_op("]") else self.parse_expr())
                self.expect_op("]")
            d = self._node(VarDecl(dts, name, dims, storage=mods), ntok)
            if self.accept_op("="):
                d.init = self.parse_initializer()
            elif self.peek().is_op("("):
                self.next()
                d.ctor_args = self.parse_args_until(")")
            out.append(d)
            if self.accept_op(","):
                continue
            break
        if semicolon:
            if not self.accept_op(";"):
                self.error("expected ';' after declaration")
        return out

    def parse_switch(self):
        tok = self.next()
        self.expect_op("(")
        e = self.parse_expr()
        self.expect_op(")")
        self.expect_op("{")
        cases = []
        cur = None
        while not self.peek().is_op("}"):
            t = self.peek()
            if t.is_id("case"):
                self.next()
                lab = self.parse_ternary()
                if self.accept_op("..."):   # gcc range extension (rare)
                    self.parse_ternary()
                self.expect_op(":")
                if cur is not None and not cur[1]:
                    cur[0].append(lab)
                else:
                    cur = [[lab], []]
                    cases.append(cur)
                continue
            if t.is_id("default"):
                self.next()
                self.expect_op(":")
                if cur is not None and not cur[1]:
                    cur[0].append(None)
                else:
                    cur = [[None], []]
                    cases.append(cur)
                continue
            st = self.parse_stmt()
            if cur is None:
                cur = [[], []]
                cases.append(cur)
            cur[1].append(st)
        self.expect_op("}")
        return self._node(Switch(e, [(c[0], c[1]) for c in cases]), tok)

    # ------------------------------------------------------------- expressions

    def parse_args_until(self, close):
        args = []
        while not self.peek().is_op(close):
            args.append(self.parse_assign_expr())
            if not self.accept_op(","):
                break
        self.expect_op(close)
        return args

    def parse_expr(self):
        tok = self.peek()
        e = self.parse_assign_expr()
        if self.peek().is_op(","):
            items = [e]
            while self.accept_op(","):
                items.append(self.parse_assign_expr())
            return self._node(Comma(items), tok)
        return e

    def parse_assign_expr(self):
        tok = self.peek()
        left = self.parse_ternary()
        t = self.peek()
        if t.kind == "OP" and t.value in ASSIGN_OPS:
            self.next()
            right = self.parse_assign_expr()
            return self._node(Assign(t.value, left, right), tok)
        return left

    def parse_ternary(self):
        tok = self.peek()
        cond = self.parse_binary(0)
        if self.accept_op("?"):
            a = self.parse_assign_expr()
            self.expect_op(":")
            b = self.parse_assign_expr()
            return self._node(Ternary(cond, a, b), tok)
        return cond

    def parse_binary(self, level):
        if level >= len(BIN_PREC):
            return self.parse_unary()
        tok = self.peek()
        left = self.parse_binary(level + 1)
        ops = BIN_PREC[level]
        while True:
            t = self.peek()
            if t.kind == "OP" and t.value in ops:
                self.next()
                right = self.parse_binary(level + 1)
                left = self._node(Binary(t.value, left, right), tok)
            else:
                return left

    def parse_unary(self):
        tok = self.peek()
        if tok.kind == "OP":
            v = tok.value
            if v in ("-", "+", "!", "~", "++", "--", "*", "&"):
                self.next()
                e = self.parse_unary()
                return self._node(Unary(v, e), tok)
            if v == "(" and self._is_cast():
                self.next()
                ts = self.parse_type()
                self.expect_op(")")
                e = self.parse_unary()
                return self._node(Cast(ts, e), tok)
        if tok.is_id("new"):
            self.next()
            ts = self.parse_type()
            args = []
            size = None
            if self.accept_op("("):
                args = self.parse_args_until(")")
            elif self.accept_op("["):
                size = self.parse_expr()
                self.expect_op("]")
            return self._node(New(ts, args, size), tok)
        if tok.kind == "ID" and tok.value in ("dynamic_cast", "static_cast", "reinterpret_cast", "const_cast") \
                and self.peek(1).is_op("<"):
            self.next()
            self.expect_op("<")
            ts = self.parse_type()
            if self.peek().is_op(">>"):
                tk = self.t[self.i]
                self.t[self.i] = Token("OP", ">", tk.file, tk.line)
            else:
                self.expect_op(">")
            self.expect_op("(")
            e = self.parse_expr()
            self.expect_op(")")
            return self._node(Cast(ts, e), tok)
        if tok.is_id("sizeof"):
            self.next()
            self.expect_op("(")
            if self.starts_type() and (self.peek(1).is_op(")") or self.peek(1).is_op("*")):
                arg = self.parse_type()
            else:
                arg = self.parse_expr()
            self.expect_op(")")
            return self._node(Sizeof(arg), tok)
        return self.parse_postfix()

    def _is_cast(self) -> bool:
        t1 = self.peek(1)
        if t1.kind != "ID":
            return False
        name = t1.value
        if name in ("const", "unsigned", "signed"):
            return True
        if not self.is_type_name(name):
            return False
        k = 2
        if self.peek(k).is_op("<"):
            return True
        while self.peek(k).is_op("*") or self.peek(k).is_op("&"):
            k += 1
        if not self.peek(k).is_op(")"):
            return False
        nxt = self.peek(k + 1)
        # (Type) followed by an operand start → cast; '(Type)' alone in expr w/o operand is grouping
        if nxt.kind in ("ID", "NUM", "STR", "CHAR"):
            return True
        if nxt.kind == "OP" and nxt.value in ("(", "!", "~", "-", "+", "&", "*", "++", "--", "::"):
            # (int)-x is a cast; (x)-y for type-named variable is unlikely
            return True
        return False

    def parse_postfix(self):
        tok = self.peek()
        e = self.parse_primary()
        while True:
            t = self.peek()
            if t.kind != "OP":
                break
            v = t.value
            if v == "(":
                self.next()
                args = self.parse_args_until(")")
                e = self._node(Call(e, args), tok)
            elif v == "[":
                self.next()
                idx = self.parse_expr()
                self.expect_op("]")
                e = self._node(Index(e, idx), tok)
            elif v in (".", "->"):
                self.next()
                if self.peek().is_op("~"):
                    self.next()
                    name = "~" + self.expect_id()
                else:
                    name = self.expect_id()
                e = self._node(Member(e, name, v == "->"), tok)
            elif v in ("++", "--"):
                self.next()
                e = self._node(Postfix(v, e), tok)
            else:
                break
        return e

    def parse_primary(self):
        tok = self.next()
        k = tok.kind
        if k == "NUM":
            return self._node(Num(tok.value, tok.num_kind or ("float" if isinstance(tok.value, float) else "int"), tok.text), tok)
        if k == "STR":
            return self._node(Str(tok.value), tok)
        if k == "CHAR":
            return self._node(Char(tok.value), tok)
        if k == "ID":
            v = tok.value
            if v == "this":
                return self._node(This(), tok)
            if v in ("true", "false"):
                return self._node(Num(v == "true", "bool", v), tok)
            if v in ("NULL",):
                return self._node(Name("NULL"), tok)
            if (v in BUILTIN_TYPES or v in self.enum_names or v.startswith("ENUM_")) and self.peek().is_op("("):
                # functional cast double(x)
                self.next()
                args = self.parse_args_until(")")
                e = args[0] if args else Num(0)
                return self._node(Cast(TypeSpec(v), e), tok)
            if self.peek().is_op("::"):
                self.next()
                if self.peek().is_op("~"):
                    self.next()
                    return self._node(Scope(v, "~" + self.expect_id()), tok)
                nm = self.expect_id()
                return self._node(Scope(v, nm), tok)
            # template function call: Func<T>(...)
            if self.peek().is_op("<") and v in self.template_types:
                save = self.i
                try:
                    targs = self._parse_targs()
                    if self.peek().is_op("("):
                        return self._node(Name(v), tok)
                except MqlSyntaxError:
                    pass
                self.i = save
            return self._node(Name(v), tok)
        if k == "OP":
            if tok.value == "(":
                e = self.parse_expr()
                self.expect_op(")")
                return e
            if tok.value == "::":
                nm = self.expect_id()
                return self._node(Scope("", nm), tok)
            if tok.value == "{":
                self.i -= 1
                return self.parse_initializer()
        self.error("unexpected token in expression", tok)


def parse(tokens, comments=None) -> tuple[Program, Parser]:
    p = Parser(tokens, comments)
    return p.parse_program(), p
