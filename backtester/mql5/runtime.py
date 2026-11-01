"""The MQL5 standard library for converted programs.

Generated modules do ``from backtester.mql5.runtime import *``; everything an
MQL5 program can name (functions, constants, structs) plus the translator's
helpers (``_idiv``, ``Box``, ``Arr`` ...) is exported from here.
"""

from __future__ import annotations

from . import rt_consts as _consts
from .rt_core import *            # noqa: F401,F403
from .rt_core import (            # noqa: F401  (underscore helpers are not star-exported)
    _AttrRef, _ElemRef, _GlobRef, _ValRef, _assign, _bool, _box_set, _char, _concat, _copy, _delete,
    _double, _fdiv, _float32, _fmod_c, _idiv, _imod, _incattr, _incbox, _incitem, _int, _long, _new, _num,
    _print, _setattr, _setitem, _short, _str, _toint, _uchar, _uint, _ulong, _ushort, _wrap, _cformat,
    _COLOR_NAMES, _PRINT_LOG,
)
from .rt_ind import *             # noqa: F401,F403
from .rt_term import *            # noqa: F401,F403
from .rt_term import _DT, _set_error   # noqa: F401

globals().update({k: v for k, v in _consts.CONSTS.items() if k not in globals()})

_USER_ENUMS: dict[str, dict] = {}


def _enum(name, table):
    _USER_ENUMS[name] = table


def EnumToString(value, enum_name=""):
    try:
        v = int(value)
    except (TypeError, ValueError):
        return str(value)
    for tbl in (_USER_ENUMS.get(enum_name), _consts.ENUMS.get(enum_name)):
        if tbl and v in tbl:
            return tbl[v]
    if enum_name:
        return f"{enum_name}::{v}"
    return str(v)


_UNSET = object()


def _alloc(cls):
    return cls.__new__(cls)


class _SwitchBreak(Exception):
    pass


def _range_end(v, bound, delta):
    """Value of a C for-loop variable after the loop ran to completion."""
    if delta > 0:
        return v if v >= bound else v + delta
    return v if v <= bound else v + delta


def _struct_init(obj, values):
    fields = getattr(type(obj), "_q_fields", ())
    for name, v in zip(fields, values):
        cur = getattr(obj, name, None)
        if isinstance(cur, Arr) and isinstance(v, list):
            for i, x in enumerate(v[: len(cur.a)]):
                cur.a[i] = x
        else:
            setattr(obj, name, v)
    return obj


import threading as _threading

_INPUTS = _threading.local()


def _input(name, default):
    """Value of an input variable: the plugin parameter if one was given."""
    ov = getattr(_INPUTS, "values", None)
    if ov and name in ov:
        return ov[name]
    return default


def _set_inputs(values):
    _INPUTS.values = dict(values or {})


def _missing(name):
    def f(*args):
        raise MqlRuntimeError(f"function {name} is not available in the converted program")
    return f


def StringTrim(s):
    return s.strip()


def DoubleToStr(v, digits=8):
    return DoubleToString(v, digits)


def iMAOnArray(arr, total, period, ma_shift, method, shift):
    vals = list(arr)
    if arr.series:
        vals = vals[::-1]
    ma = ma_on(vals, period, method)
    n = len(ma)
    k = n - 1 - int(shift) - int(ma_shift)
    return ma[k] if 0 <= k < n else 0.0


__all__ = [k for k in globals() if not k.startswith("__") and k not in ("annotations",)]
