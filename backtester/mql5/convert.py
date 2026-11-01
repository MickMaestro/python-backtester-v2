"""Convert one ``.mq5`` indicator into a plugin module (Python source text).

    from backtester.mql5.convert import Converter
    conv = Converter(include_roots=[...])
    result = conv.convert(path, source_label="MQL5 Indicators/Foo/foo.mq5")
    result.code      # the plugin module
    result.report    # warnings, unsupported features
"""

from __future__ import annotations

import datetime as _dt
import os
import re
from dataclasses import dataclass, field

from . import nodes as N
from . import rt_consts
from .lexer import MqlSyntaxError
from .parser import parse
from .preprocess import IncludeResolver, Preprocessor
from .translator import Translator, pyname
from .mqltypes import is_float, is_int

VERSION = "1.0"

MQL4_COLORS = {k[3:]: v for k, v in rt_consts.CONSTS.items() if k.startswith("clr")}


@dataclass
class ConvResult:
    ok: bool
    code: str = ""
    error: str = ""
    report: object = None
    meta: dict = field(default_factory=dict)
    class_name: str = ""
    notes: list = field(default_factory=list)


def _runtime_names() -> set:
    from . import runtime
    return set(runtime.__all__)


_RT_NAMES: set | None = None


def runtime_names():
    global _RT_NAMES
    if _RT_NAMES is None:
        _RT_NAMES = _runtime_names()
    return _RT_NAMES


def _color_value(tok: str):
    tok = tok.strip()
    if not tok:
        return None
    if tok in rt_consts.CONSTS:
        return int(rt_consts.CONSTS[tok])
    if tok in MQL4_COLORS:
        return int(MQL4_COLORS[tok])
    m = re.match(r"C'([^']*)'", tok)
    if m:
        parts = m.group(1).split(",")
        if len(parts) == 3:
            try:
                r, g, b = (int(p.strip(), 0) for p in parts)
                return (b << 16) | (g << 8) | r
            except ValueError:
                return None
    try:
        return int(tok, 0)
    except ValueError:
        return None


def _split_colors(txt: str) -> list:
    out = []
    depth = 0
    cur = ""
    for ch in txt:
        if ch == "'":
            depth ^= 1
        if ch == "," and not depth:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


def _unquote(v: str) -> str:
    v = v.strip()
    if v.startswith('"'):
        m = re.match(r'"((?:[^"\\]|\\.)*)"', v)
        return m.group(1) if m else v.strip('"')
    return v


def class_name_for(stem: str) -> str:
    parts = re.split(r"[^0-9A-Za-z\u0080-￿]+", stem)
    name = "".join(p[:1].upper() + p[1:] for p in parts if p)
    if not name or not (name[0].isalpha() or name[0] == "_"):
        name = "Ind" + name
    if not name.isidentifier():
        name = "Ind" + re.sub(r"\W", "_", name)
    return name


@dataclass
class LibInfo:
    path: str
    ok: bool
    module: str = ""
    reason: str = ""
    funcs: dict = field(default_factory=dict)     # function name -> overload count
    files: set = field(default_factory=set)       # this file + its (library) dependencies


LIB_PACKAGE = "backtester.mql5.lib"


def lib_module_name(path: str, roots: list[str]) -> str:
    rel = os.path.basename(path)
    for r in roots:
        try:
            rr = os.path.relpath(path, r)
        except ValueError:
            continue
        if not rr.startswith(".."):
            rel = rr
            break
    stem = os.path.splitext(rel)[0].replace(os.sep, "_").replace("/", "_")
    s = re.sub(r"[^0-9A-Za-z_]+", "_", stem).strip("_").lower()
    if not s or s[0].isdigit():
        s = "m_" + s
    return s


def _toplevel_names(code: str) -> list[str]:
    import ast
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    names = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.append(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.append(t.id)
    seen = set()
    return [n for n in names if not (n in seen or seen.add(n))]


class Converter:
    def __init__(self, include_roots: list[str], lib_dir: str | None = None):
        self.resolver = IncludeResolver(include_roots)
        self.roots = include_roots
        self.lib_dir = lib_dir
        self._libs: dict[str, LibInfo] = {}
        if lib_dir:
            os.makedirs(lib_dir, exist_ok=True)
            init = os.path.join(lib_dir, "__init__.py")
            if not os.path.exists(init):
                with open(init, "w", encoding="utf-8") as fh:
                    fh.write('"""Shared modules translated from MQL5 include files (generated)."""\n')

    # ------------------------------------------------------------ shared include modules

    def lib(self, path: str, _stack=()) -> LibInfo:
        info = self._libs.get(path)
        if info is not None:
            return info
        mod = lib_module_name(path, self.roots)
        if path in _stack:
            return LibInfo(path, False, mod, "include cycle")
        try:
            pp = Preprocessor(self.resolver).run(path)
            prog, _parser = parse(pp.tokens, pp.comments)
        except (MqlSyntaxError, RecursionError) as e:
            info = LibInfo(path, False, mod, f"parse error: {e}")
            self._libs[path] = info
            return info
        deps = [p for p in dict.fromkeys(pp.includes) if p != path]
        dep_infos = [self.lib(d, _stack + (path,)) for d in deps]
        bad = [d for d in dep_infos if not d.ok]
        if bad:
            info = LibInfo(path, False, mod, "depends on " + os.path.basename(bad[0].path))
            self._libs[path] = info
            return info
        tr = Translator(prog, runtime_names(), pp)
        tr.only_files = {path}
        tr.skip_files = set(deps)
        try:
            code = tr.translate()
        except Exception as e:
            info = LibInfo(path, False, mod, f"translation error: {type(e).__name__}: {e}")
            self._libs[path] = info
            return info
        issues = tr.state_issues({path})
        if tr.rep.unknown_names or tr.rep.unknown_funcs:
            issues.append("unresolved names " + ", ".join(sorted(tr.rep.unknown_names | tr.rep.unknown_funcs))[:200])
        if any(rt_consts_name in code for rt_consts_name in ("_s_",)) and tr.static_locals:
            issues.append("static locals")
        if re.search(r"(?m)^\s*(?:if|while|for)\b.*\b(?:#ifdef|#ifndef)\b", ""):
            pass
        own_funcs = {n: len(lst) for n, lst in tr.funcs.items()
                     if any(getattr(f, "file", None) == path for f in lst)}
        if issues:
            info = LibInfo(path, False, mod, "; ".join(issues[:5]))
            self._libs[path] = info
            return info
        files = {path}
        for d in dep_infos:
            files |= d.files
        info = LibInfo(path, True, mod, "", own_funcs, files)
        if self.lib_dir:
            imports = [f"from {LIB_PACKAGE}.{d.module} import *  # {os.path.basename(d.path)}"
                       for d in dep_infos]
            names = _toplevel_names(code)
            rel = os.path.basename(path)
            text = (f'"""{rel} — MQL5 include file, translated by backtester.mql5 (translator {VERSION}).\n\n'
                    f'Shared by the converted indicators that #include it. Generated: do not edit.\n"""\n'
                    "# flake8: noqa\n"
                    "from backtester.mql5.runtime import *\n"
                    + "\n".join(imports) + ("\n" if imports else "")
                    + "\n" + code + "\n\n__all__ = " + repr(names) + "\n")
            target = os.path.join(self.lib_dir, mod + ".py")
            old = open(target, encoding="utf-8").read() if os.path.exists(target) else None
            if old != text:
                with open(target, "w", encoding="utf-8") as fh:
                    fh.write(text)
        self._libs[path] = info
        return info

    def usable_libs(self, pp, tr) -> list[LibInfo]:
        if not self.lib_dir:
            return []
        cands: dict[str, LibInfo] = {}
        for inc in dict.fromkeys(pp.includes):
            info = self.lib(inc)
            if not info.ok:
                continue
            # the program must not add overloads to a library's functions
            if any(len(tr.funcs.get(n, [])) != c for n, c in info.funcs.items()):
                continue
            cands[inc] = info
        changed = True
        while changed:
            changed = False
            for p, info in list(cands.items()):
                if any(f not in cands for f in info.files):
                    del cands[p]
                    changed = True
        return list(cands.values())

    # ------------------------------------------------------------ metadata

    def properties(self, pp) -> dict:
        props: dict = {}
        types, colors, widths, styles, labels = {}, {}, {}, {}, {}
        levels = []
        desc = []
        main = pp.properties
        for key, val, file, line in main:
            k = key.lower()
            m = re.match(r"indicator_(type|color|width|style|label)(\d+)$", k)
            if m:
                what, idx = m.group(1), int(m.group(2))
                if what == "type":
                    types[idx] = int(rt_consts.CONSTS.get(val.strip(), 1)) if not val.strip().isdigit() else int(val)
                elif what == "color":
                    cols = [_color_value(c) for c in _split_colors(val)]
                    colors[idx] = [c for c in cols if c is not None]
                elif what == "width":
                    try:
                        widths[idx] = int(val)
                    except ValueError:
                        widths[idx] = 1
                elif what == "style":
                    styles[idx] = int(rt_consts.CONSTS.get(val.strip(), 0)) if not val.strip().isdigit() else int(val)
                elif what == "label":
                    labels[idx] = _unquote(val)
                continue
            m = re.match(r"indicator_level(\d+)$", k)
            if m:
                try:
                    levels.append(float(val.split()[0]))
                except (ValueError, IndexError):
                    v = rt_consts.CONSTS.get(val.strip())
                    if isinstance(v, (int, float)):
                        levels.append(float(v))
                continue
            if k in ("indicator_buffers", "indicator_plots"):
                try:
                    props[k] = int(val.split()[0])
                except (ValueError, IndexError):
                    props[k] = 0
                continue
            if k in ("indicator_separate_window", "indicator_chart_window"):
                props["window"] = "separate" if "separate" in k else "chart"
                continue
            if k in ("indicator_minimum", "indicator_maximum"):
                try:
                    props[k] = float(val)
                except ValueError:
                    pass
                continue
            if k == "description":
                desc.append(_unquote(val))
                continue
            if k in ("copyright", "link", "version"):
                props[k] = _unquote(val)
        return {"props": props, "types": types, "colors": colors, "widths": widths, "styles": styles,
                "labels": labels, "levels": levels, "description": desc}

    # ------------------------------------------------------------ inputs

    def input_specs(self, tr: Translator, pp) -> list[dict]:
        specs = []
        for d in tr.inputs:
            v = tr.globals[d.name]
            t = v.type
            label = d.comment or ""
            default = None
            if d.init is not None:
                default = tr.const_eval(d.init)
                if default is None and isinstance(d.init, N.Str):
                    default = d.init.value
                if default is None and isinstance(d.init, N.Name) and d.init.id in ("true", "false"):
                    default = d.init.id == "true"
            if default is None:
                default = "" if t == "string" else (0.0 if is_float(t) else 0)
            choice = None
            if t.startswith("enum:"):
                en = t[5:]
                tbl = None
                if en in tr.enums:
                    tbl = {}
                    for item in next((e.items for e in tr.enum_decls if e.name == en), []):
                        nm, _expr, cm = item[0], item[1], item[2] if len(item) > 2 else ""
                        val = tr.enums[en].get(nm)
                        if val is not None and val not in tbl:
                            tbl[val] = cm or nm
                elif en in rt_consts.ENUMS:
                    tbl = {k: _nice(v) for k, v in rt_consts.ENUMS[en].items()}
                if tbl:
                    if default not in tbl:
                        default = next(iter(tbl))
                    choice = tbl
            param = v.py
            if t in ("string", "color", "datetime") or t.startswith("C:") or t.endswith("[]"):
                param = None
            if t == "bool":
                default = bool(default)
            elif is_float(t):
                try:
                    default = float(default)
                except (TypeError, ValueError):
                    default = 0.0
            elif is_int(t) and not isinstance(default, bool):
                try:
                    default = int(default)
                except (TypeError, ValueError):
                    default = 0
            specs.append({"mql": d.name, "py": v.py, "param": param, "type": t if not t.startswith("enum:") else "int",
                          "default": default, "label": label, "choice": choice,
                          "sinput": "sinput" in d.storage})
        return specs

    # ------------------------------------------------------------ convert

    def convert(self, path: str, source_label: str = "", folder: str = "") -> ConvResult:
        try:
            pp = Preprocessor(self.resolver).run(path)
            prog, parser = parse(pp.tokens, pp.comments)
        except MqlSyntaxError as e:
            return ConvResult(False, error=f"parse error: {e}")
        except RecursionError:
            return ConvResult(False, error="parse error: expression nesting too deep")
        tr = Translator(prog, runtime_names(), pp)
        libs = []
        hoisted_maps = tr.local_type_maps     # collect() renames hoisted local classes in the AST
        try:
            tr.collect()
            libs = self.usable_libs(pp, tr)
        except Exception:
            libs = []
        tr = Translator(prog, runtime_names(), pp)
        tr.local_type_maps = hoisted_maps
        for info in libs:
            tr.skip_files |= info.files
        try:
            body = tr.translate()
        except RecursionError:
            return ConvResult(False, error="translation error: nesting too deep", report=tr.rep)
        except Exception as e:      # translator bug: report, don't crash the batch
            import traceback
            tb = traceback.format_exc().strip().splitlines()[-3:]
            return ConvResult(False, error=f"translation error: {type(e).__name__}: {e} | {' / '.join(tb)}",
                              report=tr.rep)
        meta = self.properties(pp)
        inputs = self.input_specs(tr, pp)
        oncalc = tr.funcs.get("OnCalculate", [])
        short = bool(oncalc) and len(oncalc[0].params) == 4
        stem = os.path.splitext(os.path.basename(path))[0]
        meta.update({
            "name": stem, "source": source_label or path, "folder": folder,
            "inputs": [{k: v for k, v in i.items() if k != "choice"} for i in inputs],
            "short_form": short, "has_oncalculate": bool(oncalc),
            "missing_includes": sorted(set(pp.missing_includes)),
            "imports": pp.imports,
        })
        cls = class_name_for(stem)
        taken = tr.module_names | set(tr.classes) | runtime_names() | {g.py for g in tr.globals.values()}
        if cls in taken or pyname(cls) in taken:
            cls = cls + "Indicator"
        extra = self.unknown_constants(tr, meta)
        if extra:
            body = "\n".join(extra) + "\n\n" + body
        notes = self._notes(tr, pp, prog, meta)
        meta["libraries"] = [os.path.basename(i.path) for i in libs]
        code = self.render(meta, inputs, body, cls, tr, notes, short, libs)
        return ConvResult(True, code=code, report=tr.rep, meta=meta, class_name=cls, notes=notes)

    def unknown_constants(self, tr, meta) -> list[str]:
        """Definitions for names the program uses but neither it nor the runtime
        defines: MQL4 colour names, #property values, unknown constants."""
        out = []
        for name in sorted(tr.rep.unknown_names):
            py = pyname(name)
            if name in MQL4_COLORS:
                out.append(f"{py} = 0x{MQL4_COLORS[name]:06X}  # MQL4 colour name")
            elif re.match(r"indicator_(color|width|style)(\d+)$", name):
                what, k = re.match(r"indicator_(color|width|style)(\d+)$", name).groups()
                k = int(k)
                if what == "color":
                    v = (meta["colors"].get(k) or [0])[0]
                elif what == "width":
                    v = meta["widths"].get(k, 1)
                else:
                    v = meta["styles"].get(k, 0)
                out.append(f"{py} = {v}  # #property {name}")
            elif re.match(r"indicator_(buffers|plots)$", name):
                out.append(f"{py} = {meta['props'].get(name, 0)}  # #property {name}")
            elif re.match(r"^[A-Z][A-Z0-9_]*$", name) and "_" in name:
                out.append(f"{py} = 0  # MQL5 constant unknown to the converter")
            else:
                continue
            tr.rep.unknown_names.discard(name)
        return out

    def _notes(self, tr, pp, prog, meta):
        notes = []
        names = set(tr.funcs)
        if "OnTimer" in names:
            notes.append("OnTimer is not called (no timer events in a backtest chart).")
        if "OnChartEvent" in names:
            notes.append("OnChartEvent is not called (no chart events).")
        if not meta["has_oncalculate"]:
            notes.append("The program has no OnCalculate: it draws only chart objects or reacts to events.")
        if pp.imports:
            notes.append("Imports DLL/library functions: " + ", ".join(pp.imports) + " (not available).")
        if meta["missing_includes"]:
            notes.append("Missing include files: " + ", ".join(meta["missing_includes"]))
        if tr.rep.unknown_funcs:
            notes.append("Functions not available here: " + ", ".join(sorted(tr.rep.unknown_funcs)))
        if tr.rep.unknown_names:
            notes.append("Unresolved names: " + ", ".join(sorted(tr.rep.unknown_names))[:300])
        uses_obj = any(f in tr.rt and f.startswith("Object") for f in self._called_names(prog))
        if uses_obj:
            notes.append("Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but "
                         "not drawn; only indicator buffers are plotted.")
        return notes

    def _called_names(self, prog):
        out = set()

        def visit(n):
            if isinstance(n, N.Call) and isinstance(n.func, N.Name):
                out.add(n.func.id)
            if isinstance(n, N.Node):
                for k in n.__slots__:
                    if k not in ("line", "file"):
                        visit(getattr(n, k, None))
            elif isinstance(n, (list, tuple)):
                for x in n:
                    visit(x)
        visit(prog.decls)
        return out

    def render(self, meta, inputs, body, cls, tr, notes, short, libs=()) -> str:
        props = meta["props"]
        lines = []
        title = meta["name"]
        src = meta["source"]
        doc = [f"{title} — converted from MQL5: {src}", ""]
        for d in meta.get("description") or []:
            if d:
                doc.append(d)
        info = []
        if props.get("copyright"):
            info.append(f"Copyright: {props['copyright']}")
        if props.get("link"):
            info.append(f"Link: {props['link']}")
        if props.get("version"):
            info.append(f"Version: {props['version']}")
        if info:
            doc.append("; ".join(info))
        doc.append("")
        doc.append(f"Translated automatically by backtester.mql5 (translator {VERSION}) on "
                   f"{_dt.date.today().isoformat()}. The code below follows the MQL5 source statement by statement;")
        doc.append("see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).")
        if notes:
            doc.append("")
            doc.append("Notes:")
            for n in notes:
                doc.append(f"- {n}")
        docstr = "\n".join(doc).replace("\\", "\\\\").replace('"""', "'''")
        lines.append(f'"""{docstr}\n"""')
        lines.append("# flake8: noqa")
        lines.append("from backtester.mql5.runtime import *  # MQL5 standard library")
        for info in libs:
            lines.append(f"from {LIB_PACKAGE}.{info.module} import *  # #include {os.path.basename(info.path)}")
        lines.append("")
        lines.append(f"MQL5_META = {_pyrepr(meta)}")
        lines.append("")
        lines.append(body)
        lines.append("")
        lines.append("")
        lines.append("# " + "-" * 70 + " plugin")
        lines.append("from backtester.indicators.base import Choice as _Choice, Pane as _Pane")
        lines.append("from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator")
        lines.append("")
        lines.append("")
        lines.append(f"class {cls}(_MQL5Indicator):")
        lines.append(f"    name = {title!r}")
        sep = props.get("window") == "separate"
        lines.append(f"    pane = _Pane.{'SEPARATE' if sep else 'PRICE'}")
        lines.append("    program_file = __file__")
        lines.append("    meta = MQL5_META")
        lines.append("    params = {")
        for i in inputs:
            if not i["param"]:
                continue
            dv = i["default"]
            lab = f"  # {i['label']}" if i["label"] else ""
            if i["choice"]:
                lines.append(f"        {i['param']!r}: _Choice({_pyrepr(i['choice'])}, default={dv!r}),{lab}")
            else:
                lines.append(f"        {i['param']!r}: {dv!r},{lab}")
        if short:
            lines.append("        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', "
                         "5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),")
        lines.append("    }")
        if "indicator_minimum" in props and "indicator_maximum" in props:
            lines.append(f"    y_range = ({props['indicator_minimum']!r}, {props['indicator_maximum']!r})")
        lines.append("")
        return "\n".join(lines) + "\n"


def _nice(name: str) -> str:
    for pre in ("PRICE_", "MODE_", "PERIOD_", "VOLUME_", "STO_", "STYLE_", "DRAW_"):
        if name.startswith(pre):
            return name[len(pre):].replace("_", " ").title() if pre != "PERIOD_" else name[len(pre):]
    return name


def _pyrepr(v) -> str:
    """repr() that stays readable for nested dicts/lists."""
    if isinstance(v, dict):
        return "{" + ", ".join(f"{_pyrepr(k)}: {_pyrepr(x)}" for k, x in v.items()) + "}"
    if isinstance(v, (list, tuple)):
        inner = ", ".join(_pyrepr(x) for x in v)
        return f"[{inner}]" if isinstance(v, list) else f"({inner}{',' if len(v) == 1 else ''})"
    return repr(v)
