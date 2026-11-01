"""MQL5 language semantics that line-by-line ports of ``.mqh`` code rely on.

Python and MQL5 disagree in a handful of places that silently change results
when code is transliterated, so the converted include libraries route those
operations through the helpers here instead of using the Python operator:

- **Integer division** truncates toward zero in MQL5 (``-7/2 == -3``);
  Python's ``//`` floors (``-7//2 == -4``). Use :func:`idiv` / :func:`imod`.
- **Floating-point division by zero** yields ``inf``/``nan`` in MQL5; Python
  raises ``ZeroDivisionError``. Use :func:`fdiv`.
- **MathPow / MathSqrt / MathLog** return ``inf``/``nan`` on overflow or a bad
  domain in MQL5; :mod:`math` raises. Use :func:`MathPow` etc.
- **EMPTY_VALUE** is ``DBL_MAX`` in MQL5. The faithful ports keep returning it
  exactly where the original does (so code that tests ``== EMPTY_VALUE``
  behaves the same); :func:`to_nan` converts a finished buffer to this app's
  NaN convention.
- **Unsigned wrap-around**: ``uint`` arithmetic such as ``prev_calculated-1``
  with ``prev_calculated == 0`` wraps to ``4294967295``. :func:`as_uint`
  reproduces it where the original depends on it.
"""

from __future__ import annotations

import math

import numpy as np

#: MQL5 ``EMPTY_VALUE`` / ``DBL_MAX``.
EMPTY_VALUE = 1.7976931348623157e308
DBL_MAX = EMPTY_VALUE
DBL_MIN = 2.2250738585072014e-308
DBL_EPSILON = 2.220446049250313e-16
INT_MAX = 2147483647
INT_MIN = -2147483648
UINT_MAX = 4294967295
UCHAR_MAX = 255
WHOLE_ARRAY = -1

# ENUM_MA_METHOD
MODE_SMA, MODE_EMA, MODE_SMMA, MODE_LWMA = 0, 1, 2, 3

# ENUM_APPLIED_PRICE (MQL5 numbering)
PRICE_CLOSE, PRICE_OPEN, PRICE_HIGH, PRICE_LOW = 1, 2, 3, 4
PRICE_MEDIAN, PRICE_TYPICAL, PRICE_WEIGHTED = 5, 6, 7


# ------------------------------------------------------------------ integers


def idiv(a: int, b: int) -> int:
    """C/MQL5 integer division: truncates toward zero."""
    a, b = int(a), int(b)
    if b == 0:
        raise ZeroDivisionError("integer division by zero (MQL5: critical error)")
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def imod(a: int, b: int) -> int:
    """C/MQL5 ``%``: the remainder takes the sign of the dividend."""
    return int(a) - idiv(a, b) * int(b)


def as_int32(value: int) -> int:
    """Wrap to a signed 32-bit ``int`` as MQL5 arithmetic does on overflow."""
    value = int(value) & 0xFFFFFFFF
    return value - 0x100000000 if value & 0x80000000 else value


def as_uint(value: int) -> int:
    """Wrap to an unsigned 32-bit ``uint``."""
    return int(value) & 0xFFFFFFFF


def as_uchar(value: int) -> int:
    return int(value) & 0xFF


# -------------------------------------------------------------------- floats


def fdiv(a: float, b: float) -> float:
    """``double`` division with IEEE semantics instead of an exception."""
    a, b = float(a), float(b)
    try:
        return a / b
    except ZeroDivisionError:
        if a == 0 or a != a:
            return math.nan
        return math.copysign(math.inf, a) * math.copysign(1.0, b)


def MathPow(base: float, exponent: float) -> float:
    try:
        return math.pow(base, exponent)
    except OverflowError:
        return math.inf
    except ValueError:            # negative base, fractional exponent
        return math.nan
    except ZeroDivisionError:     # 0 ** negative
        return math.inf


def MathSqrt(x: float) -> float:
    return math.sqrt(x) if x >= 0 else math.nan


def MathLog(x: float) -> float:
    if x > 0:
        return math.log(x)
    return -math.inf if x == 0 else math.nan


def MathLog10(x: float) -> float:
    if x > 0:
        return math.log10(x)
    return -math.inf if x == 0 else math.nan


def MathExp(x: float) -> float:
    try:
        return math.exp(x)
    except OverflowError:
        return math.inf


MathAbs = abs
MathSin = math.sin
MathCos = math.cos
MathTan = math.tan
MathArctan = math.atan
MathFloor = math.floor
MathCeil = math.ceil


def MathMax(a, b):
    return a if a > b else b


def MathMin(a, b):
    return a if a < b else b


def MathRound(x: float) -> float:
    """Round half away from zero (MQL5), not Python's banker's rounding."""
    return math.floor(x + 0.5) if x >= 0 else -math.floor(-x + 0.5)


def NormalizeDouble(value: float, digits: int) -> float:
    if value != value or abs(value) == math.inf:
        return value
    factor = 10.0 ** int(digits)
    return MathRound(value * factor) / factor


# ------------------------------------------------------------------- buffers


def to_nan(values) -> np.ndarray:
    """Convert an MQL5 buffer to this app's convention: EMPTY_VALUE → NaN."""
    out = np.asarray(values, dtype=float).copy()
    out[out == EMPTY_VALUE] = np.nan
    out[~np.isfinite(out) & ~np.isnan(out)] = np.nan
    return out


def from_nan(values) -> np.ndarray:
    """The reverse of :func:`to_nan`, for feeding NaN-convention arrays to
    code that tests for EMPTY_VALUE."""
    out = np.asarray(values, dtype=float).copy()
    out[np.isnan(out)] = EMPTY_VALUE
    return out


def price_arrays(df):
    """``open, high, low, close`` as float arrays from a bar frame."""
    return tuple(df[c].to_numpy(dtype=float) for c in ("open", "high", "low", "close"))
