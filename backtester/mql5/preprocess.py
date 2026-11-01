"""MQL5 preprocessor: ``#include``, ``#define`` (object- and function-like,
``#`` stringify and ``##`` paste), ``#ifdef/#ifndef/#else/#endif``, and
collection of ``#property`` / ``#import`` / ``#resource`` directives.

Each file is included once per translation unit, as the MetaEditor compiler
does. Include lookup: the including file's folder first (for ``"..."``), then
the configured include roots (the codebase ``MQL5 Include`` folder and the
terminal's standard ``MQL5/Include``). Matching is case-insensitive, as on
Windows.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from .lexer import Lexer, MqlSyntaxError, Token, tokenize_line


def read_source(path: str) -> str:
    b = open(path, "rb").read()
    if b[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return b.decode("utf-16")
    if b[:3] == b"\xef\xbb\xbf":
        return b[3:].decode("utf-8", "replace")
    if len(b) > 8 and b[1:16:2].count(0) >= 6 and b[0:16:2].count(0) == 0:
        return b.decode("utf-16-le", "replace")
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("cp1251", "replace")


class IncludeResolver:
    """Case-insensitive file lookup in a list of root folders."""

    def __init__(self, roots: list[str]):
        self.roots = [r for r in roots if r and os.path.isdir(r)]
        self._index: list[dict[str, str]] = []
        for r in self.roots:
            idx = {}
            for dp, _dn, fs in os.walk(r):
                for f in fs:
                    full = os.path.join(dp, f)
                    rel = os.path.relpath(full, r).replace("\\", "/").lower()
                    idx[rel] = full
            self._index.append(idx)
        self._dir_cache: dict[str, dict[str, str]] = {}

    def _in_dir(self, base: str, rel: str) -> str | None:
        path = os.path.normpath(os.path.join(base, rel.replace("\\", "/")))
        if os.path.isfile(path):
            return path
        # case-insensitive walk of each component
        parts = os.path.normpath(rel.replace("\\", "/")).split(os.sep)
        cur = base
        for p in parts:
            if p == "..":
                cur = os.path.dirname(cur)
                continue
            if p in (".", ""):
                continue
            try:
                entries = os.listdir(cur)
            except OSError:
                return None
            low = {e.lower(): e for e in entries}
            if p.lower() not in low:
                return None
            cur = os.path.join(cur, low[p.lower()])
        return cur if os.path.isfile(cur) else None

    def resolve(self, name: str, current_file: str, angle: bool) -> str | None:
        rel = name.replace("\\", "/").lstrip("/")
        if not angle and current_file:
            p = self._in_dir(os.path.dirname(current_file), rel)
            if p:
                return p
        key = os.path.normpath(rel).replace("\\", "/").lower()
        while key.startswith("../"):
            key = key[3:]
        for idx in self._index:
            if key in idx:
                return idx[key]
        # "Include/Foo.mqh" or "MQL5/Include/Foo.mqh" spelled from a project root
        for prefix in ("mql5/include/", "include/"):
            if key.startswith(prefix):
                for idx in self._index:
                    if key[len(prefix):] in idx:
                        return idx[key[len(prefix):]]
        # last resort: unique basename match
        base = key.rsplit("/", 1)[-1]
        hits = [v for idx in self._index for k, v in idx.items() if k.rsplit("/", 1)[-1] == base]
        if len(hits) >= 1:
            return hits[0]
        if current_file:
            p = self._in_dir(os.path.dirname(current_file), base)
            if p:
                return p
        return None


@dataclass
class Macro:
    name: str
    params: list[str] | None   # None = object-like
    body: list[Token]
    variadic: bool = False


@dataclass
class PPResult:
    tokens: list[Token]
    properties: list[tuple[str, str, str, int]] = field(default_factory=list)
    includes: list[str] = field(default_factory=list)
    missing_includes: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)
    comments: dict[tuple[str, int], str] = field(default_factory=dict)
    macros: dict[str, Macro] = field(default_factory=dict)
    file_tokens: dict[str, int] = field(default_factory=dict)


BUILTIN_DEFINES = {"__MQL5__": "1", "__MQL__": "1", "__MQLBUILD__": "4620",
                   "__MQL5BUILD__": "4620", "_RELEASE": "1"}


def _tok_text(t: Token) -> str:
    if t.kind == "STR":
        return '"' + str(t.value).replace("\\", "\\\\").replace('"', '\\"') + '"'
    if t.kind == "CHAR":
        return repr(chr(t.value))
    if t.kind == "NUM":
        return t.text or str(t.value)
    return str(t.value)


class Preprocessor:
    def __init__(self, resolver: IncludeResolver, max_depth: int = 40):
        self.resolver = resolver
        self.max_depth = max_depth

    def run(self, path: str, extra_defines: dict[str, str] | None = None) -> PPResult:
        self.macros: dict[str, Macro] = {}
        for k, v in {**BUILTIN_DEFINES, **(extra_defines or {})}.items():
            self.macros[k] = Macro(k, None, tokenize_line(v, "<builtin>", 0))
        self.res = PPResult(tokens=[])
        self.included: set[str] = set()
        out: list[Token] = []
        self._file(path, out, 0)
        out.append(Token("EOF", None, path, 0))
        self.res.tokens = self._merge_strings(out)
        self.res.macros = self.macros
        return self.res

    # ---------------------------------------------------------------- files

    def _file(self, path: str, out: list[Token], depth: int) -> None:
        key = os.path.normcase(os.path.abspath(path))
        if key in self.included:
            return
        self.included.add(key)
        if depth > self.max_depth:
            raise MqlSyntaxError("include nesting too deep", path, 0)
        text = read_source(path)
        lx = Lexer(text, path)
        toks = lx.tokenize()[:-1]
        for ln, c in lx.comments.items():
            self.res.comments[(path, ln)] = c
        self.res.file_tokens[path] = len(toks)
        cond: list[list[bool]] = []   # stack of [active, taken]
        active = True
        in_import = False
        pending: list[Token] = []

        def flush():
            if pending:
                out.extend(self._expand_all_noconcat(pending))
                pending.clear()
        for t in toks:
            if t.kind != "PP":
                if active:
                    pending.append(t)
                continue
            flush()
            d = t.value
            m = re.match(r"(\w+)\s*(.*)$", d, re.S)
            if not m:
                continue
            kw, rest = m.group(1), m.group(2).strip()
            if kw in ("ifdef", "ifndef"):
                name = rest.split()[0] if rest.split() else ""
                val = (name in self.macros) == (kw == "ifdef")
                cond.append([active, val])
                active = active and val
                continue
            if kw == "if":
                val = self._eval_if(rest)
                cond.append([active, val])
                active = active and val
                continue
            if kw == "elif":
                if cond:
                    outer, taken = cond[-1]
                    val = (not taken) and self._eval_if(rest)
                    cond[-1][1] = taken or val
                    active = outer and val
                continue
            if kw == "else":
                if cond:
                    outer, taken = cond[-1]
                    active = outer and not taken
                    cond[-1][1] = True
                continue
            if kw == "endif":
                if cond:
                    active = cond.pop()[0]
                continue
            if not active:
                continue
            if kw == "define":
                self._define(rest, t)
            elif kw == "undef":
                self.macros.pop(rest.split()[0] if rest.split() else "", None)
            elif kw == "include":
                mm = re.match(r'[<"]([^>"]+)[>"]', rest)
                if not mm:
                    continue
                name = mm.group(1)
                angle = rest.startswith("<")
                target = self.resolver.resolve(name, path, angle)
                if target is None:
                    self.res.missing_includes.append(name)
                    continue
                self.res.includes.append(target)
                self._file(target, out, depth + 1)
            elif kw == "property":
                mm = re.match(r"(\w+)\s*(.*)$", rest, re.S)
                if mm:
                    self.res.properties.append((mm.group(1), mm.group(2).strip(), path, t.line))
            elif kw == "import":
                if rest:
                    mm = re.match(r'"([^"]*)"', rest)
                    name = mm.group(1) if mm else rest
                    self.res.imports.append(name)
                    out.append(Token("ID", "__IMPORT_BEGIN__", path, t.line))
                    out.append(Token("STR", name, path, t.line))
                    in_import = True
                else:
                    if in_import:
                        out.append(Token("ID", "__IMPORT_END__", path, t.line))
                    in_import = False
            elif kw == "resource":
                self.res.resources.append(rest.strip('"'))
            # pragma, etc.: ignored
        flush()
        if in_import:
            out.append(Token("ID", "__IMPORT_END__", path, 0))

    def _eval_if(self, expr: str) -> bool:
        expr = re.sub(r"defined\s*\(\s*(\w+)\s*\)", lambda m: "1" if m.group(1) in self.macros else "0", expr)
        expr = re.sub(r"defined\s+(\w+)", lambda m: "1" if m.group(1) in self.macros else "0", expr)

        def name_val(m):
            n = m.group(0)
            mac = self.macros.get(n)
            if mac and mac.params is None and len(mac.body) == 1 and mac.body[0].kind == "NUM":
                return str(mac.body[0].value)
            return "0"
        expr = re.sub(r"[A-Za-z_]\w*", name_val, expr)
        expr = expr.replace("&&", " and ").replace("||", " or ").replace("!", " not ").replace(" not =", "!=")
        try:
            return bool(eval(expr, {"__builtins__": {}}, {}))
        except Exception:
            return False

    def _define(self, rest: str, t: Token) -> None:
        m = re.match(r"([A-Za-z_\u0080-\uffff][\w\u0080-\uffff]*)", rest)
        if not m:
            return
        name = m.group(1)
        after = rest[m.end():]
        if after.startswith("("):
            close = after.find(")")
            params_txt = after[1:close]
            params = [p.strip() for p in params_txt.split(",") if p.strip()]
            variadic = bool(params) and params[-1] == "..."
            if variadic:
                params[-1] = "__VA_ARGS__"
            body = tokenize_line(after[close + 1:], t.file, t.line)
            self.macros[name] = Macro(name, params, body, variadic)
        else:
            body = tokenize_line(after, t.file, t.line)
            self.macros[name] = Macro(name, None, body)

    # ------------------------------------------------------------ expansion

    @staticmethod
    def _merge_strings(out: list[Token]) -> list[Token]:
        merged: list[Token] = []
        for t in out:
            if t.kind == "STR" and merged and merged[-1].kind == "STR":
                merged[-1] = Token("STR", merged[-1].value + t.value, merged[-1].file, merged[-1].line)
            else:
                merged.append(t)
        return merged

    @staticmethod
    def _clone(b: Token, origin: Token, hide) -> Token:
        return Token(b.kind, b.value, origin.file, origin.line, b.num_kind, b.text,
                     b.space_before, frozenset(hide | b.hide))

    def _expand_arg(self, arg: list[Token]) -> list[Token]:
        saved = arg + [Token("EOF", None)]
        res = self._expand_all_noconcat(saved)
        return [x for x in res if x.kind != "EOF"]

    def _expand_all_noconcat(self, toks):
        out = []
        stack = list(reversed(toks))
        while stack:
            t = stack.pop()
            if t.kind == "ID" and t.value in self.macros and t.value not in t.hide:
                mac = self.macros[t.value]
                if mac.params is None:
                    body = [self._clone(b, t, t.hide | {mac.name}) for b in mac.body]
                    stack.extend(reversed(self._paste(body)))
                    continue
                if not stack or not stack[-1].is_op("("):
                    out.append(t)
                    continue
                stack.pop()
                args = [[]]
                depth = 0
                while stack:
                    a = stack.pop()
                    if a.kind == "EOF":
                        stack.append(a)
                        break
                    if a.kind == "OP" and a.value in "([{":
                        depth += 1
                    elif a.kind == "OP" and a.value in ")]}":
                        if depth == 0 and a.value == ")":
                            break
                        depth -= 1
                    if a.is_op(",") and depth == 0:
                        args.append([])
                        continue
                    args[-1].append(a)
                if args == [[]]:
                    args = []
                stack.extend(reversed(self._substitute(mac, args, t)))
                continue
            if t.kind == "ID" and t.value == "__LINE__":
                t = Token("NUM", t.line, t.file, t.line, "int", str(t.line))
            elif t.kind == "ID" and t.value in ("__FILE__", "__PATH__"):
                t = Token("STR", os.path.basename(t.file), t.file, t.line)
            elif t.kind == "ID" and t.value in ("__DATE__", "__DATETIME__"):
                t = Token("NUM", 1_700_000_000, t.file, t.line, "datetime", "0")
            out.append(t)
        return out

    def _substitute(self, mac: Macro, args: list[list[Token]], origin: Token) -> list[Token]:
        params = mac.params or []
        amap: dict[str, list[Token]] = {}
        for i, p in enumerate(params):
            if p == "__VA_ARGS__":
                rest = []
                for j, a in enumerate(args[i:]):
                    if j:
                        rest.append(Token("OP", ",", origin.file, origin.line))
                    rest.extend(a)
                amap[p] = rest
                break
            amap[p] = args[i] if i < len(args) else []
        hide = origin.hide | {mac.name}
        body = mac.body
        res: list[Token] = []
        i = 0
        while i < len(body):
            b = body[i]
            # stringify
            if b.is_op("#") and i + 1 < len(body) and body[i + 1].kind == "ID" and body[i + 1].value in amap:
                txt = " ".join(_tok_text(x) for x in amap[body[i + 1].value])
                res.append(Token("STR", txt, origin.file, origin.line))
                i += 2
                continue
            if b.kind == "ID" and b.value in amap:
                pasted = (i + 1 < len(body) and body[i + 1].is_op("##")) or (res and res[-1].is_op("##"))
                rep = amap[b.value] if pasted else self._expand_arg(amap[b.value])
                res.extend(self._clone(x, origin, hide) for x in rep)
                i += 1
                continue
            res.append(self._clone(b, origin, hide))
            i += 1
        return self._paste(res)

    def _paste(self, toks: list[Token]) -> list[Token]:
        if not any(t.is_op("##") for t in toks):
            return toks
        out: list[Token] = []
        i = 0
        while i < len(toks):
            t = toks[i]
            if t.is_op("##") and out and i + 1 < len(toks):
                left = out.pop()
                right = toks[i + 1]
                txt = _tok_text(left) + _tok_text(right)
                new = tokenize_line(txt, left.file, left.line)
                for x in new:
                    x.hide = left.hide
                out.extend(new)
                i += 2
                continue
            out.append(t)
            i += 1
        return out
