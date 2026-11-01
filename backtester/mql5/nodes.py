"""AST node classes for the MQL5 front end (plain classes with __slots__)."""

from __future__ import annotations


class Node:
    __slots__ = ("line", "file")

    def __repr__(self):
        fields = ", ".join(f"{k}={getattr(self, k, None)!r}" for k in self.__slots__ if k not in ("line", "file"))
        return f"{type(self).__name__}({fields})"


# ------------------------------------------------------------------ types

class TypeSpec(Node):
    __slots__ = ("name", "targs", "const", "pointer", "ref", "unsigned")

    def __init__(self, name, targs=None, const=False, pointer=False, ref=False):
        self.line = 0
        self.file = ""
        self.name = name          # 'int', 'double', 'CFoo', ...
        self.targs = targs or []  # template arguments (TypeSpec list)
        self.const = const
        self.pointer = pointer
        self.ref = ref

    def __repr__(self):
        t = self.name
        if self.targs:
            t += "<" + ",".join(map(repr, self.targs)) + ">"
        return t + ("*" if self.pointer else "") + ("&" if self.ref else "")


# ------------------------------------------------------------------ expressions

class Expr(Node):
    __slots__ = ()


class Num(Expr):
    __slots__ = ("value", "kind", "text")

    def __init__(self, value, kind="int", text=""):
        self.value, self.kind, self.text = value, kind, text


class Str(Expr):
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value


class Char(Expr):
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value


class Name(Expr):
    __slots__ = ("id",)

    def __init__(self, id):
        self.id = id


class Scope(Expr):          # Class::name  or ::name (cls='')
    __slots__ = ("cls", "id")

    def __init__(self, cls, id):
        self.cls, self.id = cls, id


class This(Expr):
    __slots__ = ()


class Member(Expr):
    __slots__ = ("obj", "name", "arrow")

    def __init__(self, obj, name, arrow=False):
        self.obj, self.name, self.arrow = obj, name, arrow


class Index(Expr):
    __slots__ = ("obj", "idx")

    def __init__(self, obj, idx):
        self.obj, self.idx = obj, idx


class Call(Expr):
    __slots__ = ("func", "args", "targs")

    def __init__(self, func, args, targs=None):
        self.func, self.args, self.targs = func, args, targs or []


class Unary(Expr):          # - + ! ~ ++pre --pre * &
    __slots__ = ("op", "e")

    def __init__(self, op, e):
        self.op, self.e = op, e


class Postfix(Expr):        # x++ x--
    __slots__ = ("op", "e")

    def __init__(self, op, e):
        self.op, self.e = op, e


class Binary(Expr):
    __slots__ = ("op", "l", "r")

    def __init__(self, op, l, r):
        self.op, self.l, self.r = op, l, r


class Assign(Expr):
    __slots__ = ("op", "target", "value")

    def __init__(self, op, target, value):
        self.op, self.target, self.value = op, target, value


class Ternary(Expr):
    __slots__ = ("cond", "a", "b")

    def __init__(self, cond, a, b):
        self.cond, self.a, self.b = cond, a, b


class Cast(Expr):
    __slots__ = ("type", "e")

    def __init__(self, type, e):
        self.type, self.e = type, e


class New(Expr):
    __slots__ = ("type", "args", "size")

    def __init__(self, type, args, size=None):
        self.type, self.args, self.size = type, args, size


class Comma(Expr):
    __slots__ = ("items",)

    def __init__(self, items):
        self.items = items


class InitList(Expr):
    __slots__ = ("items",)

    def __init__(self, items):
        self.items = items


class Sizeof(Expr):
    __slots__ = ("arg",)

    def __init__(self, arg):
        self.arg = arg


# ------------------------------------------------------------------ statements

class Stmt(Node):
    __slots__ = ()


class Block(Stmt):
    __slots__ = ("body",)

    def __init__(self, body):
        self.body = body


class ExprStmt(Stmt):
    __slots__ = ("e",)

    def __init__(self, e):
        self.e = e


class DeclStmt(Stmt):
    __slots__ = ("decls",)

    def __init__(self, decls):
        self.decls = decls


class If(Stmt):
    __slots__ = ("cond", "then", "els")

    def __init__(self, cond, then, els):
        self.cond, self.then, self.els = cond, then, els


class For(Stmt):
    __slots__ = ("init", "cond", "step", "body")

    def __init__(self, init, cond, step, body):
        self.init, self.cond, self.step, self.body = init, cond, step, body


class While(Stmt):
    __slots__ = ("cond", "body")

    def __init__(self, cond, body):
        self.cond, self.body = cond, body


class DoWhile(Stmt):
    __slots__ = ("body", "cond")

    def __init__(self, body, cond):
        self.body, self.cond = body, cond


class Switch(Stmt):
    __slots__ = ("e", "cases")   # cases: list of (labels:list[Expr|None], stmts)

    def __init__(self, e, cases):
        self.e, self.cases = e, cases


class Break(Stmt):
    __slots__ = ()


class Continue(Stmt):
    __slots__ = ()


class Return(Stmt):
    __slots__ = ("e",)

    def __init__(self, e):
        self.e = e


class Delete(Stmt):
    __slots__ = ("e",)

    def __init__(self, e):
        self.e = e


class Empty(Stmt):
    __slots__ = ()


# ------------------------------------------------------------------ declarations

class VarDecl(Node):
    __slots__ = ("type", "name", "dims", "init", "ctor_args", "storage", "comment", "is_member", "access")

    def __init__(self, type, name, dims=None, init=None, ctor_args=None, storage=(), comment=""):
        self.type = type
        self.name = name
        self.dims = dims or []         # list of Expr|None  (None = dynamic)
        self.init = init
        self.ctor_args = ctor_args     # CFoo obj(1,2)
        self.storage = set(storage)    # {'input','sinput','static','const','extern'}
        self.comment = comment
        self.is_member = False
        self.access = "public"


class Param(Node):
    __slots__ = ("type", "name", "default", "dims")

    def __init__(self, type, name, default=None, dims=None):
        self.type, self.name, self.default, self.dims = type, name, default, dims or []


class FuncDecl(Node):
    __slots__ = ("ret", "name", "params", "body", "cls", "kind", "const", "virtual", "static",
                 "tparams", "inits", "pure", "imported", "access", "variadic")

    def __init__(self, ret, name, params, body=None):
        self.ret = ret
        self.name = name
        self.params = params
        self.body = body
        self.cls = None          # 'CFoo' for out-of-class definitions
        self.kind = "func"       # func | ctor | dtor | operator
        self.const = False
        self.virtual = False
        self.static = False
        self.tparams = []
        self.inits = []          # ctor initializer list: (name, [args])
        self.pure = False
        self.imported = ""
        self.access = "public"
        self.variadic = False


class ClassDecl(Node):
    __slots__ = ("kind", "name", "base", "members", "tparams", "forward")

    def __init__(self, kind, name, base=None):
        self.kind = kind      # class | struct | interface
        self.name = name
        self.base = base      # TypeSpec | None
        self.members = []
        self.tparams = []
        self.forward = False


class EnumDecl(Node):
    __slots__ = ("name", "items")

    def __init__(self, name, items):
        self.name = name
        self.items = items    # list of (name, Expr|None, comment)


class Typedef(Node):
    __slots__ = ("name", "type", "func_params")

    def __init__(self, name, type, func_params=None):
        self.name, self.type, self.func_params = name, type, func_params


class Program(Node):
    __slots__ = ("decls",)

    def __init__(self, decls):
        self.decls = decls
