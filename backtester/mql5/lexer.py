"""MQL5 tokenizer.

Produces a flat list of :class:`Token`. Preprocessor directives come out as a
single ``PP`` token holding the whole (continuation-joined) directive line, so
the preprocessor can work on tokens and directives in one stream.

Trailing ``//`` comments are not tokens, but their text is kept per source line
(``Lexer.comments``): MetaTrader uses the comment after an ``input`` or an
enum member as its display label, and the converter does the same.
"""

from __future__ import annotations

import calendar
import re
from dataclasses import dataclass, field


class MqlSyntaxError(Exception):
    def __init__(self, msg, file="", line=0):
        super().__init__(f"{file}:{line}: {msg}" if file else msg)
        self.file = file
        self.line = line


@dataclass(slots=True)
class Token:
    kind: str          # ID NUM STR CHAR OP PP EOF
    value: object      # text for ID/OP/PP, python value for NUM/STR/CHAR
    file: str = ""
    line: int = 0
    num_kind: str = ""  # NUM: 'int', 'float', 'color', 'datetime'
    text: str = ""      # NUM: original spelling
    space_before: bool = False  # PP: whether whitespace preceded (for '#' stringify)
    hide: frozenset = field(default_factory=frozenset)  # macro names not to re-expand

    def __repr__(self):
        return f"Token({self.kind},{self.value!r},{self.line})"

    def is_op(self, v):
        return self.kind == "OP" and self.value == v

    def is_id(self, v=None):
        return self.kind == "ID" and (v is None or self.value == v)


OPS = sorted("""
>>= <<= ... -> ++ -- && || == != <= >= += -= *= /= %= &= |= ^= << >> ::
+ - * / % = < > ! ~ & | ^ ? : ; , . ( ) [ ] { } # @ \\ $
""".split(), key=len, reverse=True)

_ID_RE = re.compile(r"[A-Za-z_\u0080-￿][A-Za-z0-9_\u0080-￿]*")
_NUM_RE = re.compile(
    r"0[xX][0-9a-fA-F]+[uUlL]*"
    r"|(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?[fFlLuU]*"
)
_ESC = {"n": "\n", "t": "\t", "r": "\r", "0": "\0", "\\": "\\", "'": "'", '"': '"',
        "a": "\a", "b": "\b", "f": "\f", "v": "\v", "?": "?"}

NAMED_COLORS: dict[str, int] = {}
_COND_RE = re.compile(r"#[ \t]*(ifdef|ifndef)[ \t]+([\w\u0080-\uffff]+)|#[ \t]*(else|endif)\b")   # filled by runtime constants (clrRed -> 0x0000FF ...)


def _parse_color(body: str) -> int:
    parts = [p.strip() for p in body.split(",")]
    if len(parts) == 3:
        vals = []
        for p in parts:
            p = p or "0"
            vals.append(int(p, 0) if p.lower().startswith("0x") else int(float(p)))
        r, g, b = (v & 0xFF for v in vals)
        return (b << 16) | (g << 8) | r
    name = body.strip()
    if name in NAMED_COLORS:
        return NAMED_COLORS[name]
    if name.lower().startswith("0x"):
        return int(name, 16)
    return 0


def _parse_datetime(body: str) -> int:
    s = body.strip()
    m = re.match(r"(\d{4})\.(\d{1,2})\.(\d{1,2})(?:\s+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?)?", s)
    if m:
        y, mo, d = int(m[1]), int(m[2]), int(m[3])
        hh, mm, ss = int(m[4] or 0), int(m[5] or 0), int(m[6] or 0)
        try:
            return calendar.timegm((y, mo, d, hh, mm, ss))
        except (ValueError, OverflowError):
            return 0
    m = re.match(r"(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?", s)
    if m:   # time of the compile date: use 1970.01.01 (deterministic)
        return int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3] or 0)
    m = re.match(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", s)
    if m:
        try:
            return calendar.timegm((int(m[3]), int(m[2]), int(m[1]), 0, 0, 0))
        except (ValueError, OverflowError):
            return 0
    return 0


def _unescape(body: str, file: str, line: int) -> str:
    out = []
    i = 0
    n = len(body)
    while i < n:
        c = body[i]
        if c == "\\" and i + 1 < n:
            e = body[i + 1]
            if e in "xX":
                j = i + 2
                while j < n and j < i + 6 and body[j] in "0123456789abcdefABCDEF":
                    j += 1
                out.append(chr(int(body[i + 2:j] or "0", 16)))
                i = j
                continue
            if e.isdigit():
                j = i + 1
                while j < n and j < i + 4 and body[j] in "01234567":
                    j += 1
                out.append(chr(int(body[i + 1:j], 8)))
                i = j
                continue
            out.append(_ESC.get(e, e))
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


class Lexer:
    def __init__(self, text: str, file: str = ""):
        self.text = text.replace("\r\n", "\n").replace("\r", "\n")
        self.file = file
        self.comments: dict[int, str] = {}
        self.tokens: list[Token] = []

    def tokenize(self) -> list[Token]:
        s = self.text
        n = len(s)
        i = 0
        line = 1
        at_line_start = True
        toks = self.tokens
        f = self.file
        while i < n:
            c = s[i]
            if c == "\n":
                line += 1
                i += 1
                at_line_start = True
                continue
            if c in " \t\f\v﻿":
                i += 1
                continue
            if c == "\\" and i + 1 < n and s[i + 1] == "\n":   # stray continuation
                i += 2
                line += 1
                continue
            if c == "/" and i + 1 < n:
                if s[i + 1] == "/":
                    j = s.find("\n", i)
                    if j < 0:
                        j = n
                    txt = s[i + 2:j].strip()
                    if txt:
                        self.comments.setdefault(line, txt)
                    i = j
                    continue
                if s[i + 1] == "*":
                    j = s.find("*/", i + 2)
                    if j < 0:
                        j = n - 2
                    txt = s[i + 2:j]
                    if "\n" not in txt and txt.strip():
                        self.comments.setdefault(line, txt.strip())
                    line += txt.count("\n")
                    i = j + 2
                    continue
            if c == "#" and at_line_start:
                m = _COND_RE.match(s, i)
                if m:
                    # conditional directives take one word; the rest of the line is code
                    toks.append(Token("PP", (m.group(1) + " " + m.group(2)) if m.group(1) else m.group(3), f, line))
                    i = m.end()
                    continue
                # directive: up to end of line, honouring backslash continuations
                start_line = line
                j = i + 1
                buf = []
                while j < n:
                    ch = s[j]
                    if ch == "\\" and j + 1 < n and s[j + 1] == "\n":
                        j += 2
                        line += 1
                        buf.append(" ")
                        continue
                    if ch == "\\" and j + 2 < n and s[j + 1] == "\r" and s[j + 2] == "\n":
                        j += 3
                        line += 1
                        continue
                    if ch == "\n":
                        break
                    if ch == "/" and j + 1 < n and s[j + 1] == "/":
                        # comment ends the directive (but keep strings intact)
                        if buf.count('"') % 2 == 0:
                            k = s.find("\n", j)
                            k = n if k < 0 else k
                            txt = s[j + 2:k].strip()
                            if txt:
                                self.comments.setdefault(line, txt)
                            j = k
                            break
                    if ch == "/" and j + 1 < n and s[j + 1] == "*" and buf.count('"') % 2 == 0:
                        k = s.find("*/", j + 2)
                        k = n - 2 if k < 0 else k
                        line += s[j:k].count("\n")
                        j = k + 2
                        buf.append(" ")
                        continue
                    buf.append(ch)
                    j += 1
                toks.append(Token("PP", "".join(buf).strip(), f, start_line))
                i = j
                continue
            if c == "#":
                m = re.compile(r"#\s*(ifdef|ifndef)\s+(\w+)|#\s*(else|endif)\b").match(s, i)
                if m:
                    toks.append(Token("PP", (m.group(1) + " " + m.group(2)) if m.group(1) else m.group(3), f, line))
                    i = m.end()
                    continue
            at_line_start = False
            if c == '"':
                j = i + 1
                while j < n and s[j] != '"':
                    if s[j] == "\\":
                        j += 1
                    if j < n and s[j] == "\n":
                        line += 1
                    j += 1
                body = s[i + 1:j]
                toks.append(Token("STR", _unescape(body, f, line), f, line))
                i = j + 1
                continue
            if c == "'":
                j = i + 1
                while j < n and s[j] != "'":
                    if s[j] == "\\":
                        j += 1
                    j += 1
                body = _unescape(s[i + 1:j], f, line)
                toks.append(Token("CHAR", ord(body[0]) if body else 0, f, line))
                i = j + 1
                continue
            if c in "0123456789" or (c == "." and i + 1 < n and s[i + 1] in "0123456789"):
                m = _NUM_RE.match(s, i)
                txt = m.group(0)
                i = m.end()
                core = txt.rstrip("uUlLfF") if not txt.lower().startswith("0x") else txt.rstrip("uUlL")
                if core.lower().startswith("0x"):
                    toks.append(Token("NUM", int(core, 16), f, line, "int", txt))
                elif any(ch in core for ch in ".eE"):
                    toks.append(Token("NUM", float(core), f, line, "float", txt))
                else:
                    v = int(core)
                    toks.append(Token("NUM", v, f, line, "int", txt))
                continue
            m = _ID_RE.match(s, i)
            if m:
                word = m.group(0)
                j = m.end()
                if word in ("C", "D") and j < n and s[j] == "'" and 0 < s.find("'", j + 1) <= j + 40 \
                        and "\n" not in s[j:s.find("'", j + 1)]:
                    k = s.find("'", j + 1)
                    body = s[j + 1:k]
                    if word == "C":
                        toks.append(Token("NUM", _parse_color(body), f, line, "color", f"C'{body}'"))
                    else:
                        toks.append(Token("NUM", _parse_datetime(body), f, line, "datetime", f"D'{body}'"))
                    i = k + 1
                    continue
                toks.append(Token("ID", word, f, line))
                i = j
                continue
            for op in OPS:
                if s.startswith(op, i):
                    toks.append(Token("OP", op, f, line))
                    i += len(op)
                    break
            else:
                # unknown char: skip it (e.g. stray unicode punctuation)
                i += 1
        toks.append(Token("EOF", None, f, line))
        return toks


def tokenize_line(text: str, file: str = "", line: int = 0) -> list[Token]:
    """Tokenize a directive's body (no PP handling)."""
    lx = Lexer(text, file)
    toks = lx.tokenize()[:-1]
    for t in toks:
        t.line = line
    return toks
