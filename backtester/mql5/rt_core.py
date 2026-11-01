"""MQL5 runtime — language core: arrays, references, numeric conversions,
math, strings, time. Imported by generated code via :mod:`.runtime`.

Semantics follow MetaTrader 5:

* arrays are :class:`Arr`; ``ArraySetAsSeries`` flips logical indexing
  (0 = newest) without moving data; out-of-range access raises
  :class:`MqlRuntimeError` ("array out of range"), which stops the indicator
  as it does in the terminal;
* integer division / modulo truncate toward zero (``_idiv``/``_imod``);
* double division by zero gives ±inf / nan (``_fdiv``);
* double → int conversion truncates; NaN or out-of-range gives INT_MIN.
"""

from __future__ import annotations

import calendar
import math
import random as _random
import time as _time

DBL_MAX = 1.7976931348623157e308
DBL_MIN = 2.2250738585072014e-308
DBL_EPSILON = 2.220446049250313e-16
DBL_DIG = 15
DBL_MANT_DIG = 53
FLT_MAX = 3.402823466e38
FLT_MIN = 1.175494351e-38
FLT_EPSILON = 1.192092896e-07
EMPTY_VALUE = DBL_MAX
INT_MAX = 2147483647
INT_MIN = -2147483648
UINT_MAX = 4294967295
LONG_MAX = 9223372036854775807
LONG_MIN = -9223372036854775808
ULONG_MAX = 18446744073709551615
SHORT_MAX = 32767
SHORT_MIN = -32768
USHORT_MAX = 65535
CHAR_MAX = 127
CHAR_MIN = -128
UCHAR_MAX = 255
WRONG_VALUE = -1
EMPTY = -1
INVALID_HANDLE = -1
NULL = None
M_PI = math.pi
M_PI_2 = math.pi / 2
M_PI_4 = math.pi / 4
M_1_PI = 1 / math.pi
M_2_PI = 2 / math.pi
M_2_SQRTPI = 2 / math.sqrt(math.pi)
M_E = math.e
M_LOG2E = math.log2(math.e)
M_LOG10E = math.log10(math.e)
M_LN2 = math.log(2)
M_LN10 = math.log(10)
M_SQRT2 = math.sqrt(2)
M_SQRT1_2 = math.sqrt(0.5)


class MqlRuntimeError(Exception):
    """A critical runtime error that stops an MQL5 program (array out of range,
    zero divide, invalid pointer ...)."""


class MqlStop(Exception):
    """ExpertRemove / program asked to stop."""


# ------------------------------------------------------------------ numerics

def _idiv(a, b):
    a = int(a)
    b = int(b)
    if b == 0:
        raise MqlRuntimeError("zero divide")
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def _imod(a, b):
    a = int(a)
    b = int(b)
    if b == 0:
        raise MqlRuntimeError("zero divide")
    r = abs(a) % abs(b)
    return r if a >= 0 else -r


def _fdiv(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        a = float(a)
        if a != a or a == 0.0:
            return math.nan
        return math.inf if (a > 0) == (math.copysign(1.0, float(b)) > 0) else -math.inf
    except TypeError:
        if a is None or b is None:
            raise MqlRuntimeError("invalid pointer access")
        raise


def _fmod_c(a, b):
    try:
        return math.fmod(a, b)
    except (ValueError, ZeroDivisionError):
        return math.nan


def _toint(x, bits=32, signed=True):
    """C conversion of a double to an integer type (truncation)."""
    if isinstance(x, int):
        v = x
    else:
        if isinstance(x, str):
            return StringToInteger(x)
        if x is None:
            return 0
        try:
            v = int(x)
        except (ValueError, OverflowError):
            return -(1 << (bits - 1)) if signed else 0
        lim = 1 << (bits - 1)
        if signed and not (-lim <= v < lim):
            return -lim
    return _wrap(v, bits, signed)


def _wrap(v, bits=32, signed=True):
    v = int(v)
    m = (1 << bits) - 1
    v &= m
    if signed and v >> (bits - 1):
        v -= 1 << bits
    return v


def _int(x):        # int / datetime-free (32-bit)
    return _toint(x, 32, True)


def _long(x):
    return _toint(x, 64, True)


def _uint(x):
    return _toint(x, 32, False)


def _ulong(x):
    return _toint(x, 64, False)


def _short(x):
    return _toint(x, 16, True)


def _ushort(x):
    return _toint(x, 16, False)


def _char(x):
    return _toint(x, 8, True)


def _uchar(x):
    return _toint(x, 8, False)


def _double(x):
    if isinstance(x, str):
        return StringToDouble(x)
    if x is None:
        return 0.0
    return float(x)


def _float32(x):
    import struct
    try:
        return struct.unpack("f", struct.pack("f", float(x)))[0]
    except OverflowError:
        return math.copysign(math.inf, x)


def _bool(x):
    if isinstance(x, str):
        return x != ""
    return bool(x)


def _num(x):
    """Value of a bool/None in arithmetic."""
    if x is None:
        return 0
    return x


# ------------------------------------------------------------------ strings

def _fmt_double(v: float) -> str:
    """MQL5's default double → string conversion (up to 16 significant digits)."""
    if v != v:
        return "nan"
    if v in (math.inf, -math.inf):
        return "inf" if v > 0 else "-inf"
    if v == DBL_MAX:
        return "1.797693134862316e+308"
    s = f"{v:.16g}"
    if "e" in s:
        mant, exp = s.split("e")
        e = int(exp)
        s = f"{mant}e{'+' if e >= 0 else '-'}{abs(e):02d}"
    return s


def _str(x) -> str:
    if isinstance(x, str):
        return x
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, float):
        return _fmt_double(x)
    if x is None:
        return ""
    return str(x)


def _concat(*parts) -> str:
    return "".join(_str(p) for p in parts)


# ------------------------------------------------------------------ references

class Box:
    """A scalar passed by reference (``double &x``)."""
    __slots__ = ("v",)

    def __init__(self, v=0):
        self.v = v

    def __repr__(self):
        return f"Box({self.v!r})"


class _ElemRef:
    __slots__ = ("a", "i")

    def __init__(self, a, i):
        self.a, self.i = a, i

    @property
    def v(self):
        return self.a[self.i]

    @v.setter
    def v(self, val):
        self.a[self.i] = val


class _AttrRef:
    __slots__ = ("o", "n")

    def __init__(self, o, n):
        self.o, self.n = o, n

    @property
    def v(self):
        return getattr(self.o, self.n)

    @v.setter
    def v(self, val):
        setattr(self.o, self.n, val)


class _GlobRef:
    __slots__ = ("g", "n")

    def __init__(self, g, n):
        self.g, self.n = g, n

    @property
    def v(self):
        return self.g[self.n]

    @v.setter
    def v(self, val):
        self.g[self.n] = val


class _ValRef:
    """An rvalue passed where a reference is expected (writes are dropped)."""
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v


def _box_set(b, v):
    b.v = v
    return v


def _setitem(a, i, v):
    a[i] = v
    return v


def _setattr(o, n, v):
    setattr(o, n, v)
    return v


def _incitem(a, i, d, post):
    old = a[i]
    a[i] = old + d
    return old if post else old + d


def _incattr(o, n, d, post):
    old = getattr(o, n)
    setattr(o, n, old + d)
    return old if post else old + d


def _incbox(b, d, post):
    old = b.v
    b.v = old + d
    return old if post else old + d


# ------------------------------------------------------------------ objects

class MqlObject:
    """Base of translated classes/structs: value-semantics copy support."""

    def _q_assign(self, other):
        if other is None:
            return self
        for k, v in other.__dict__.items():
            cur = self.__dict__.get(k)
            if isinstance(v, Arr):
                if isinstance(cur, Arr) and not cur.dyn:
                    cur._copy_from(v)
                else:
                    self.__dict__[k] = v._clone()
            elif isinstance(v, MqlObject) and not getattr(v, "_q_ptr", False) and isinstance(cur, MqlObject) \
                    and k not in self._q_pointer_fields():
                cur._q_assign(v)
            else:
                self.__dict__[k] = v
        return self

    @classmethod
    def _q_pointer_fields(cls):
        return getattr(cls, "_q_ptrs", ())

    def _q_copy(self):
        new = object.__new__(type(self))
        new.__dict__ = {}
        for k, v in self.__dict__.items():
            if isinstance(v, Arr):
                new.__dict__[k] = v._clone()
            elif isinstance(v, MqlObject) and k not in self._q_pointer_fields():
                new.__dict__[k] = v._q_copy()
            else:
                new.__dict__[k] = v
        return new

    def __bool__(self):
        return True


def _copy(v):
    """Value copy for struct/class assignment and by-value passing."""
    if isinstance(v, MqlObject):
        return v._q_copy()
    if isinstance(v, Arr):
        return v._clone()
    return v


def _assign(target, src):
    """``a = b`` for struct/class values: copy into the existing object."""
    if isinstance(target, MqlObject):
        target._q_assign(src)
        return target
    return _copy(src)


def CheckPointer(p):
    if p is None:
        return POINTER_INVALID
    return POINTER_DYNAMIC if getattr(p, "_q_dyn", False) else POINTER_AUTOMATIC


def GetPointer(p):
    return p


def _new(obj):
    try:
        obj._q_dyn = True
    except AttributeError:
        pass
    return obj


POINTER_INVALID = 0
POINTER_DYNAMIC = 1
POINTER_AUTOMATIC = 2


def _delete(p):
    if p is None:
        return
    try:
        p._q_dtor()
    except AttributeError:
        pass


# ------------------------------------------------------------------ arrays

class Arr:
    """An MQL5 array. Data is stored oldest-first ("physical" order);
    ``series`` flips logical indexing so that index 0 is the last element.

    ``dyn``: dynamic (resizable). ``fill``: value for new elements, or
    ``factory`` (callable) for arrays of structs/objects. ``dims``: fixed sizes
    of the inner dimensions for multi-dimensional arrays (rows are Arr)."""

    __slots__ = ("a", "series", "dyn", "fill", "factory", "dims", "buffer", "reserve", "__weakref__")

    def __init__(self, size=0, fill=0.0, dyn=True, factory=None, dims=(), series=False):
        self.fill = fill
        self.factory = factory
        self.dims = tuple(dims)
        self.dyn = dyn
        self.series = series
        self.buffer = False
        self.reserve = 0
        self.a = []
        if size:
            self.a = [self._make() for _ in range(size)] if (factory or dims) else [fill] * size

    def _make(self):
        if self.dims:
            return Arr(self.dims[0], self.fill, False, self.factory, self.dims[1:])
        if self.factory is not None:
            return self.factory()
        return self.fill

    @classmethod
    def of(cls, values, fill=0.0, dyn=True, factory=None, size=None, dims=()):
        arr = cls(0, fill, dyn, factory, dims)
        vals = list(values)
        if dims:
            rows = []
            for v in vals:
                r = Arr(dims[0], fill, False, factory, dims[1:])
                sub = list(v) if isinstance(v, (list, tuple)) else [v]
                for j, x in enumerate(sub[:dims[0]]):
                    if isinstance(x, (list, tuple)):
                        r.a[j] = Arr.of(x, fill, False, factory, None, dims[2:]) if len(dims) > 1 else x
                    else:
                        r.a[j] = x
                rows.append(r)
            vals = rows
        if size is not None and size > len(vals):
            arr.a = vals + [arr._make() for _ in range(size - len(vals))]
        else:
            arr.a = vals
        return arr

    def __len__(self):
        return len(self.a)

    def __getitem__(self, i):
        try:
            if i < 0:
                raise IndexError
            return self.a[~i] if self.series else self.a[i]
        except IndexError:
            raise MqlRuntimeError(f"array out of range (index {i}, size {len(self.a)})") from None
        except TypeError:
            return self[int(i)]

    def __setitem__(self, i, v):
        try:
            if i < 0:
                raise IndexError
            if self.series:
                self.a[~i] = v
            else:
                self.a[i] = v
        except IndexError:
            raise MqlRuntimeError(f"array out of range (index {i}, size {len(self.a)})") from None
        except TypeError:
            self[int(i)] = v

    def __iter__(self):
        return iter(self.a[::-1] if self.series else self.a)

    def __repr__(self):
        return f"Arr({len(self.a)}{', series' if self.series else ''})"

    def _clone(self):
        new = Arr(0, self.fill, self.dyn, self.factory, self.dims, self.series)
        new.a = [_copy(x) for x in self.a] if (self.factory or self.dims) else list(self.a)
        return new

    def _copy_from(self, other):
        n = min(len(self.a), len(other.a)) if not self.dyn else len(other.a)
        if self.dyn:
            self.a = [_copy(x) for x in other.a]
        else:
            for i in range(n):
                self.a[i] = _copy(other.a[i])

    def resize(self, n, reserve=0):
        n = int(n)
        if n < 0:
            return -1
        cur = len(self.a)
        if n > cur:
            if self.factory or self.dims:
                self.a.extend(self._make() for _ in range(n - cur))
            else:
                self.a.extend([self.fill] * (n - cur))
        elif n < cur:
            del self.a[n:]
        return n

    def total(self):
        if self.dims:
            return sum(r.total() if isinstance(r, Arr) else 1 for r in self.a)
        return len(self.a)

    def flat(self):
        if self.dims:
            out = []
            for r in self.a:
                out.extend(r.flat() if isinstance(r, Arr) else [r])
            return out
        return self.a


def _arr_init(arr, value):
    if arr.dims:
        for r in arr.a:
            _arr_init(r, value)
        return
    if arr.factory is None:
        n = len(arr.a)
        arr.a[:] = [value] * n


# --- array functions -------------------------------------------------------

def ArrayResize(arr, new_size, reserve_size=0):
    if not isinstance(arr, Arr):
        return -1
    if not arr.dyn and not arr.buffer:
        return len(arr.a) if new_size == len(arr.a) else -1
    if arr.buffer:
        return len(arr.a)
    return arr.resize(new_size, reserve_size)


def ArraySize(arr):
    if isinstance(arr, Arr):
        return arr.total()
    if isinstance(arr, (list, tuple, str)):
        return len(arr)
    return 0


def ArrayRange(arr, rank):
    if rank == 0:
        return len(arr.a)
    d = arr.dims
    if rank - 1 < len(d):
        return d[rank - 1]
    return 0


def ArrayInitialize(arr, value):
    if not isinstance(arr, Arr):
        return 0
    if value is None:
        value = "" if isinstance(arr.fill, str) else 0
    _arr_init(arr, value)
    return arr.total()


def ArrayFill(arr, start, count, value):
    if value is None:
        value = 0
    if arr.series:
        n = len(arr.a)
        for i in range(start, min(start + count, n)):
            arr.a[n - 1 - i] = value
    else:
        if start + count > len(arr.a) and arr.dyn:
            arr.resize(start + count)
        for i in range(start, min(start + count, len(arr.a))):
            arr.a[i] = value


def ArraySetAsSeries(arr, flag):
    if not isinstance(arr, Arr) or arr.dims:
        return False
    arr.series = bool(flag)
    return True


def ArrayGetAsSeries(arr):
    return bool(arr.series) if isinstance(arr, Arr) else False


def ArrayIsSeries(arr):
    return bool(getattr(arr, "_timeseries", False))


def ArrayIsDynamic(arr):
    return bool(arr.dyn) and not arr.buffer


def ArrayFree(arr):
    if isinstance(arr, Arr) and arr.dyn and not arr.buffer:
        arr.a = []


def ArrayCopy(dst, src, dst_start=0, src_start=0, count=WHOLE_ARRAY if False else -1):
    """Copies logically (respecting the series flags of both arrays)."""
    dst_start = max(int(dst_start), 0)
    src_start = max(int(src_start), 0)
    if count is None or count < 0 or count == WHOLE_ARRAY:
        count = len(src.a) - src_start
    count = max(0, min(count, len(src.a) - src_start))
    if count <= 0:
        return 0
    need = dst_start + count
    if len(dst.a) < need:
        if dst.dyn and not dst.buffer:
            dst.resize(need)
        else:
            count = max(0, len(dst.a) - dst_start)
    if src.dims or dst.dims:
        sf, df_ = src.flat(), None
        # copy as flat sequences into rows
        flat_dst = []
        for r in dst.a:
            flat_dst.extend(r.a if isinstance(r, Arr) else [r])
        for k in range(count):
            flat_dst[dst_start + k] = sf[src_start + k]
        pos = 0
        for r in dst.a:
            if isinstance(r, Arr):
                for j in range(len(r.a)):
                    r.a[j] = flat_dst[pos]
                    pos += 1
        return count
    vals = [src[src_start + k] for k in range(count)]
    for k in range(count):
        dst[dst_start + k] = _copy(vals[k])
    return count


WHOLE_ARRAY = -1


def ArrayMaximum(arr, start=0, count=WHOLE_ARRAY):
    n = len(arr.a)
    if count == WHOLE_ARRAY or count is None or count < 0:
        count = n - start
    count = min(count, n - start)
    if count <= 0 or start < 0:
        return -1
    best = start
    bv = arr[start]
    for i in range(start + 1, start + count):
        v = arr[i]
        if v > bv:
            bv = v
            best = i
    return best


def ArrayMinimum(arr, start=0, count=WHOLE_ARRAY):
    n = len(arr.a)
    if count == WHOLE_ARRAY or count is None or count < 0:
        count = n - start
    count = min(count, n - start)
    if count <= 0 or start < 0:
        return -1
    best = start
    bv = arr[start]
    for i in range(start + 1, start + count):
        v = arr[i]
        if v < bv:
            bv = v
            best = i
    return best


def ArraySort(arr, count=WHOLE_ARRAY, start=0, direction=0):
    if arr.dims:
        # sort rows by first column
        rows = arr.a
        rows.sort(key=lambda r: r.a[0])
        return True
    vals = sorted(arr.a)
    arr.a[:] = vals
    return True


def ArrayBsearch(arr, value):
    vals = list(arr)
    if not vals:
        return -1
    lo, hi = 0, len(vals) - 1
    asc = vals[0] <= vals[-1]
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if vals[mid] == value:
            return mid
        if (vals[mid] < value) == asc:
            lo = mid + 1
        else:
            hi = mid - 1
        best = mid
    # nearest
    cand = min(range(len(vals)), key=lambda k: abs(vals[k] - value))
    return cand


def ArrayReverse(arr, start=0, count=WHOLE_ARRAY):
    vals = list(arr)
    if count == WHOLE_ARRAY or count < 0:
        count = len(vals) - start
    seg = vals[start:start + count][::-1]
    for k, v in enumerate(seg):
        arr[start + k] = v
    return True


def ArrayInsert(dst, src, dst_start, src_start=0, count=WHOLE_ARRAY):
    vals = list(src)[src_start:] if count == WHOLE_ARRAY or count < 0 else list(src)[src_start:src_start + count]
    cur = list(dst)
    cur[dst_start:dst_start] = [_copy(v) for v in vals]
    dst.a = cur[::-1] if dst.series else cur
    return True


def ArrayRemove(arr, start, count=WHOLE_ARRAY):
    cur = list(arr)
    if count == WHOLE_ARRAY or count < 0:
        count = len(cur) - start
    del cur[start:start + count]
    arr.a = cur[::-1] if arr.series else cur
    return True


def ArrayCompare(a, b, a_start=0, b_start=0, count=WHOLE_ARRAY):
    x = list(a)[a_start:]
    y = list(b)[b_start:]
    if count != WHOLE_ARRAY and count >= 0:
        x, y = x[:count], y[:count]
    for p, q in zip(x, y):
        if p < q:
            return -1
        if p > q:
            return 1
    return (len(x) > len(y)) - (len(x) < len(y))


def ArraySwap(a, b):
    if not (isinstance(a, Arr) and isinstance(b, Arr)):
        return False
    a.a, b.a = b.a, a.a
    return True


def ArrayPrint(arr, digits=None, separator=" ", start=0, count=WHOLE_ARRAY, flags=0):
    _print(" ".join(_str(v) for v in list(arr)[start:]))


def ArrayDimension(arr):
    return 1 + len(arr.dims)


def ZeroMemory(x):
    if isinstance(x, Arr):
        _arr_init(x, "" if isinstance(x.fill, str) else 0)
    elif isinstance(x, MqlObject):
        for k, v in list(x.__dict__.items()):
            if isinstance(v, bool):
                x.__dict__[k] = False
            elif isinstance(v, int):
                x.__dict__[k] = 0
            elif isinstance(v, float):
                x.__dict__[k] = 0.0
            elif isinstance(v, str):
                x.__dict__[k] = ""
            elif isinstance(v, (Arr, MqlObject)):
                ZeroMemory(v)
    elif isinstance(x, (Box, _ElemRef, _AttrRef, _GlobRef)):
        v = x.v
        x.v = "" if isinstance(v, str) else (0.0 if isinstance(v, float) else 0)


# ------------------------------------------------------------------ math

def MathAbs(x):
    return abs(x)


def MathMax(a, b):
    return a if a > b else b


def MathMin(a, b):
    return a if a < b else b


def MathSqrt(x):
    try:
        return math.sqrt(x)
    except ValueError:
        return math.nan
    except TypeError:
        return math.sqrt(float(x))


def MathPow(b, e):
    try:
        r = math.pow(b, e)
        return r
    except (ValueError, OverflowError):
        try:
            return float(b) ** float(e) if b >= 0 else math.nan
        except (OverflowError, ZeroDivisionError):
            return math.inf
    except ZeroDivisionError:
        return math.inf


def MathLog(x):
    try:
        return math.log(x)
    except ValueError:
        return -math.inf if x == 0 else math.nan


def MathLog10(x):
    try:
        return math.log10(x)
    except ValueError:
        return -math.inf if x == 0 else math.nan


def MathLog2(x):
    try:
        return math.log2(x)
    except ValueError:
        return -math.inf if x == 0 else math.nan


def MathLog1p(x):
    try:
        return math.log1p(x)
    except ValueError:
        return -math.inf if x == -1 else math.nan


def MathExp(x):
    try:
        return math.exp(x)
    except OverflowError:
        return math.inf


def MathExpm1(x):
    try:
        return math.expm1(x)
    except OverflowError:
        return math.inf


def MathFloor(x):
    try:
        return float(math.floor(x))
    except (ValueError, OverflowError):
        return float(x)


def MathCeil(x):
    try:
        return float(math.ceil(x))
    except (ValueError, OverflowError):
        return float(x)


def MathRound(x):
    try:
        return float(math.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)
    except (ValueError, OverflowError):
        return float(x)


def MathMod(a, b):
    return _fmod_c(a, b)


def MathSin(x):
    try:
        return math.sin(x)
    except ValueError:
        return math.nan


def MathCos(x):
    try:
        return math.cos(x)
    except ValueError:
        return math.nan


def MathTan(x):
    try:
        return math.tan(x)
    except ValueError:
        return math.nan


def MathArcsin(x):
    try:
        return math.asin(x)
    except ValueError:
        return math.nan


def MathArccos(x):
    try:
        return math.acos(x)
    except ValueError:
        return math.nan


def MathArctan(x):
    return math.atan(x)


def MathArctan2(y, x):
    return math.atan2(y, x)


def MathSinh(x):
    try:
        return math.sinh(x)
    except OverflowError:
        return math.copysign(math.inf, x)


def MathCosh(x):
    try:
        return math.cosh(x)
    except OverflowError:
        return math.inf


def MathTanh(x):
    return math.tanh(x)


def MathArcsinh(x):
    return math.asinh(x)


def MathArccosh(x):
    try:
        return math.acosh(x)
    except ValueError:
        return math.nan


def MathArctanh(x):
    try:
        return math.atanh(x)
    except ValueError:
        return math.nan if abs(x) > 1 else math.copysign(math.inf, x)


def MathIsValidNumber(x):
    try:
        return math.isfinite(x) and abs(x) < DBL_MAX
    except TypeError:
        return False


_rand_state = [1]


def MathSrand(seed):
    _rand_state[0] = int(seed) & 0xFFFFFFFF


def MathRand():
    # MSVC rand(): deterministic like the terminal for a given seed
    _rand_state[0] = (_rand_state[0] * 214013 + 2531011) & 0xFFFFFFFF
    return (_rand_state[0] >> 16) & 0x7FFF


def MathSwap(a, b):
    if isinstance(a, (Box, _ElemRef, _AttrRef, _GlobRef)):
        a.v, b.v = b.v, a.v


def MathClassify(x):
    if x != x:
        return 4
    if math.isinf(x):
        return 3
    return 2 if x == 0 else 1


fabs = MathAbs
fmax = MathMax
fmin = MathMin
sqrt = MathSqrt
pow = MathPow
log = MathLog
log10 = MathLog10
exp = MathExp
floor = MathFloor
ceil = MathCeil
fmod = MathMod
sin = MathSin
cos = MathCos
tan = MathTan
asin = MathArcsin
acos = MathArccos
atan = MathArctan
atan2 = MathArctan2


def round(x):     # noqa: A001  (MQL round)
    return MathRound(x)


def rand():
    return MathRand()


def srand(seed):
    MathSrand(seed)


def NormalizeDouble(value, digits):
    try:
        digits = int(digits)
        if digits < 0:
            digits = 0
        if digits > 8:
            digits = 8
        if not math.isfinite(value):
            return value
        p = 10.0 ** digits
        return math.floor(abs(value) * p + 0.5) / p * (1 if value >= 0 else -1)
    except (TypeError, OverflowError):
        return value


# ------------------------------------------------------------------ conversions / strings

def DoubleToString(value, digits=8):
    try:
        digits = int(digits)
    except (TypeError, ValueError):
        digits = 8
    if value != value:
        return "nan"
    if value in (math.inf, -math.inf):
        return "inf" if value > 0 else "-inf"
    if digits < 0:
        return f"{value:.{min(-digits, 16)}e}"
    digits = min(digits, 16)
    return f"{value:.{digits}f}"


def IntegerToString(number, str_len=0, fill_symbol=" "):
    s = str(int(number))
    if len(s) < str_len:
        ch = chr(fill_symbol) if isinstance(fill_symbol, int) else str(fill_symbol)
        s = ch * (str_len - len(s)) + s
    return s


def StringToDouble(s):
    s = str(s).strip()
    import re
    m = re.match(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?", s)
    return float(m.group(0)) if m else 0.0


def StringToInteger(s):
    s = str(s).strip()
    import re
    m = re.match(r"[+-]?\d+", s)
    return int(m.group(0)) if m else 0


def CharToString(c):
    return chr(int(c) & 0xFF) if int(c) >= 0 else ""


def ShortToString(c):
    try:
        return chr(int(c) & 0xFFFF)
    except ValueError:
        return ""


def StringLen(s):
    return len(s) if s is not None else 0


def StringFind(s, sub, start=0):
    if s is None or sub is None:
        return -1
    return s.find(sub, int(start))


def StringSubstr(s, start, length=-1):
    if s is None:
        return ""
    start = int(start)
    if start < 0 or start >= len(s):
        return ""
    if length is None or length < 0:
        return s[start:]
    return s[start:start + int(length)]


def StringGetCharacter(s, pos):
    try:
        return ord(s[pos]) if 0 <= pos < len(s) else 0
    except (TypeError, IndexError):
        return 0


def StringGetChar(s, pos):
    return StringGetCharacter(s, pos)


def StringSetCharacter(ref, pos, ch):
    s = ref.v
    ch = chr(int(ch)) if int(ch) else ""
    if pos == len(s):
        ref.v = s + ch
    elif 0 <= pos < len(s):
        ref.v = s[:pos] + ch + s[pos + 1:]
    else:
        return False
    return True


def StringToUpper(ref):
    if isinstance(ref, str):
        return ref.upper()
    ref.v = ref.v.upper()
    return True


def StringToLower(ref):
    if isinstance(ref, str):
        return ref.lower()
    ref.v = ref.v.lower()
    return True


def StringTrimLeft(ref):
    if isinstance(ref, str):
        return ref.lstrip()
    old = ref.v
    ref.v = old.lstrip(" \t\r\n")
    return len(old) - len(ref.v)


def StringTrimRight(ref):
    if isinstance(ref, str):
        return ref.rstrip()
    old = ref.v
    ref.v = old.rstrip(" \t\r\n")
    return len(old) - len(ref.v)


def StringReplace(ref, find, replacement):
    s = ref.v
    if not find:
        return -1
    cnt = s.count(find)
    ref.v = s.replace(find, replacement)
    return cnt


def StringConcatenate(ref, *args):
    s = _concat(*args)
    if isinstance(ref, (Box, _ElemRef, _AttrRef, _GlobRef)):
        ref.v = s
        return len(s)
    return s


def StringAdd(ref, sub):
    ref.v = ref.v + _str(sub)
    return True


def StringInit(ref, new_len=0, char=0):
    ref.v = (chr(char) if char else "") * int(new_len) if char else ""
    return True


def StringFill(ref, char):
    ref.v = chr(char) * len(ref.v)
    return True


def StringBufferLen(s):
    return len(s)


def StringCompare(a, b, case_sensitive=True):
    if not case_sensitive:
        a, b = a.lower(), b.lower()
    return (a > b) - (a < b)


def StringSplit(s, sep, result):
    sep = chr(sep) if isinstance(sep, int) else sep
    parts = s.split(sep) if s else []
    if s == "":
        parts = []
    result.a = list(parts)
    if result.series:
        result.a.reverse()
    return len(parts)


def StringToCharArray(s, arr, start=0, count=-1, codepage=0):
    data = s.encode("cp1252", "replace") + b"\0"
    if count >= 0:
        data = data[:count]
    need = start + len(data)
    if len(arr.a) < need and arr.dyn:
        arr.resize(need)
    for k, b in enumerate(data):
        if start + k < len(arr.a):
            arr[start + k] = b
    return len(data)


def CharArrayToString(arr, start=0, count=-1, codepage=0):
    vals = list(arr)[start:] if count < 0 else list(arr)[start:start + count]
    out = []
    for v in vals:
        if v == 0:
            break
        out.append(chr(v & 0xFF))
    return "".join(out)


def StringToShortArray(s, arr, start=0, count=-1):
    data = [ord(c) for c in s] + [0]
    if count >= 0:
        data = data[:count]
    need = start + len(data)
    if len(arr.a) < need and arr.dyn:
        arr.resize(need)
    for k, b in enumerate(data):
        arr[start + k] = b
    return len(data)


def ShortArrayToString(arr, start=0, count=-1):
    vals = list(arr)[start:] if count < 0 else list(arr)[start:start + count]
    out = []
    for v in vals:
        if v == 0:
            break
        out.append(chr(v))
    return "".join(out)


def ColorToString(c, color_name=False):
    c = int(c) & 0xFFFFFFFF
    if color_name:
        for k, v in _COLOR_NAMES.items():
            if v == c:
                return k
    if c == 0xFFFFFFFF:
        return "clrNONE"
    r, g, b = c & 0xFF, (c >> 8) & 0xFF, (c >> 16) & 0xFF
    return f"{r},{g},{b}"


def StringToColor(s):
    s = s.strip()
    if s in _COLOR_NAMES:
        return _COLOR_NAMES[s]
    parts = s.split(",")
    if len(parts) == 3:
        r, g, b = (int(p) for p in parts)
        return (b << 16) | (g << 8) | r
    return 0


def ColorToARGB(c, alpha=255):
    c = int(c)
    r, g, b = c & 0xFF, (c >> 8) & 0xFF, (c >> 16) & 0xFF
    return (int(alpha) << 24) | (r << 16) | (g << 8) | b


def StringFormat(fmt, *args):
    return _cformat(fmt, args)


def _cformat(fmt, args):
    import re
    out = []
    ai = 0
    i = 0
    pat = re.compile(r"%([-+ #0]*)(\*|\d+)?(?:\.(\*|\d+))?(hh|h|ll|l|I64|I32|L)?([diouxXeEfgGcsSp%])")
    for m in pat.finditer(fmt):
        out.append(fmt[i:m.start()])
        i = m.end()
        flags, width, prec, _len, conv = m.groups()
        if conv == "%":
            out.append("%")
            continue
        if width == "*":
            width = str(args[ai] if ai < len(args) else 0)
            ai += 1
        if prec == "*":
            prec = str(args[ai] if ai < len(args) else 0)
            ai += 1
        val = args[ai] if ai < len(args) else 0
        ai += 1
        spec = "%" + (flags or "") + (width or "") + (("." + prec) if prec is not None else "")
        try:
            if conv in "di":
                out.append((spec + "d") % int(_num(val) if not isinstance(val, str) else StringToInteger(val)))
            elif conv in "ouxX":
                out.append((spec + conv) % (int(val) & 0xFFFFFFFFFFFFFFFF if int(val) < 0 else int(val)))
            elif conv in "eEfgG":
                v = float(val) if not isinstance(val, str) else StringToDouble(val)
                out.append((spec + conv) % v)
            elif conv == "c":
                out.append(chr(int(val)))
            elif conv in "sS":
                out.append((spec + "s") % _str(val))
            elif conv == "p":
                out.append(hex(id(val)))
        except (TypeError, ValueError, OverflowError):
            out.append(_str(val))
    out.append(fmt[i:])
    return "".join(out)


_PRINT_LOG: list[str] = []
_PRINT_ENABLED = [False]


def _print(s):
    _PRINT_LOG.append(s)
    if len(_PRINT_LOG) > 500:
        del _PRINT_LOG[:250]
    if _PRINT_ENABLED[0]:
        print(s)


def Print(*args):
    _print(_concat(*args))


def Alert(*args):
    _print("Alert: " + _concat(*args))


def Comment(*args):
    pass


def PrintFormat(fmt, *args):
    _print(_cformat(fmt, args))


def printf(fmt, *args):
    _print(_cformat(fmt, args))


def DebugBreak():
    pass


# ------------------------------------------------------------------ time

class MqlDateTime(MqlObject):
    def __init__(self):
        self.year = 0
        self.mon = 0
        self.day = 0
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.day_of_week = 0
        self.day_of_year = 0


def TimeToStruct(t, st):
    t = int(t)
    tm = _time.gmtime(t if t >= 0 else 0)
    st.year, st.mon, st.day = tm.tm_year, tm.tm_mon, tm.tm_mday
    st.hour, st.min, st.sec = tm.tm_hour, tm.tm_min, tm.tm_sec
    st.day_of_week = (tm.tm_wday + 1) % 7
    st.day_of_year = tm.tm_yday - 1
    return True


def StructToTime(st):
    try:
        y, mo, d = int(st.year), int(st.mon), int(st.day)
        if y < 1970:
            y = 1970
        mo = min(max(mo, 1), 12)
        d = min(max(d, 1), 31)
        return calendar.timegm((y, mo, 1, int(st.hour), int(st.min), int(st.sec))) + (d - 1) * 86400
    except (ValueError, OverflowError):
        return 0


TIME_DATE = 1
TIME_MINUTES = 2
TIME_SECONDS = 4


def TimeToString(t, mode=TIME_DATE | TIME_MINUTES):
    t = int(t)
    tm = _time.gmtime(t if t >= 0 else 0)
    parts = []
    if mode & TIME_DATE:
        parts.append(f"{tm.tm_year:04d}.{tm.tm_mon:02d}.{tm.tm_mday:02d}")
    if mode & TIME_SECONDS:
        parts.append(f"{tm.tm_hour:02d}:{tm.tm_min:02d}:{tm.tm_sec:02d}")
    elif mode & TIME_MINUTES:
        parts.append(f"{tm.tm_hour:02d}:{tm.tm_min:02d}")
    return " ".join(parts)


def StringToTime(s):
    import re
    s = str(s).strip()
    m = re.match(r"(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})(?:[ T]+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?)?", s)
    if m:
        try:
            return calendar.timegm((int(m[1]), int(m[2]), int(m[3]), int(m[4] or 0), int(m[5] or 0), int(m[6] or 0)))
        except (ValueError, OverflowError):
            return 0
    m = re.match(r"(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?", s)
    if m:
        base = _current_day_start()
        return base + int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3] or 0)
    return 0


def _current_day_start():
    from . import rt_term
    t = rt_term.TimeCurrent()
    return t - t % 86400


def TimeYear(t):
    return _time.gmtime(int(t)).tm_year


def TimeMonth(t):
    return _time.gmtime(int(t)).tm_mon


def TimeDay(t):
    return _time.gmtime(int(t)).tm_mday


def TimeHour(t):
    return _time.gmtime(int(t)).tm_hour


def TimeMinute(t):
    return _time.gmtime(int(t)).tm_min


def TimeSeconds(t):
    return _time.gmtime(int(t)).tm_sec


def TimeDayOfWeek(t):
    return (_time.gmtime(int(t)).tm_wday + 1) % 7


def TimeDayOfYear(t):
    return _time.gmtime(int(t)).tm_yday - 1


def GetTickCount():
    return int(_time.monotonic() * 1000) & 0xFFFFFFFF


def GetTickCount64():
    return int(_time.monotonic() * 1000)


def GetMicrosecondCount():
    return int(_time.monotonic() * 1_000_000)


def Sleep(ms):
    pass


# ------------------------------------------------------------------ colours

_COLOR_NAMES: dict[str, int] = {}

_WEB_COLORS = """AliceBlue F0F8FF AntiqueWhite FAEBD7 Aqua 00FFFF Aquamarine 7FFFD4 Azure F0FFFF Beige F5F5DC
Bisque FFE4C4 Black 000000 BlanchedAlmond FFEBCD Blue 0000FF BlueViolet 8A2BE2 Brown A52A2A BurlyWood DEB887
CadetBlue 5F9EA0 Chartreuse 7FFF00 Chocolate D2691E Coral FF7F50 CornflowerBlue 6495ED Cornsilk FFF8DC
Crimson DC143C Cyan 00FFFF DarkBlue 00008B DarkCyan 008B8B DarkGoldenrod B8860B DarkGray A9A9A9 DarkGreen 006400
DarkKhaki BDB76B DarkMagenta 8B008B DarkOliveGreen 556B2F DarkOrange FF8C00 DarkOrchid 9932CC DarkRed 8B0000
DarkSalmon E9967A DarkSeaGreen 8FBC8F DarkSlateBlue 483D8B DarkSlateGray 2F4F4F DarkTurquoise 00CED1
DarkViolet 9400D3 DeepPink FF1493 DeepSkyBlue 00BFFF DimGray 696969 DodgerBlue 1E90FF FireBrick B22222
FloralWhite FFFAF0 ForestGreen 228B22 Fuchsia FF00FF Gainsboro DCDCDC GhostWhite F8F8FF Gold FFD700
Goldenrod DAA520 Gray 808080 Green 008000 GreenYellow ADFF2F Honeydew F0FFF0 HotPink FF69B4 IndianRed CD5C5C
Indigo 4B0082 Ivory FFFFF0 Khaki F0E68C Lavender E6E6FA LavenderBlush FFF0F5 LawnGreen 7CFC00
LemonChiffon FFFACD LightBlue ADD8E6 LightCoral F08080 LightCyan E0FFFF LightGoldenrod FAFAD2 LightGray D3D3D3
LightGreen 90EE90 LightPink FFB6C1 LightSalmon FFA07A LightSeaGreen 20B2AA LightSkyBlue 87CEFA
LightSlateGray 778899 LightSteelBlue B0C4DE LightYellow FFFFE0 Lime 00FF00 LimeGreen 32CD32 Linen FAF0E6
Magenta FF00FF Maroon 800000 MediumAquamarine 66CDAA MediumBlue 0000CD MediumOrchid BA55D3 MediumPurple 9370DB
MediumSeaGreen 3CB371 MediumSlateBlue 7B68EE MediumSpringGreen 00FA9A MediumTurquoise 48D1CC
MediumVioletRed C71585 MidnightBlue 191970 MintCream F5FFFA MistyRose FFE4E1 Moccasin FFE4B5 NavajoWhite FFDEAD
Navy 000080 OldLace FDF5E6 Olive 808000 OliveDrab 6B8E23 Orange FFA500 OrangeRed FF4500 Orchid DA70D6
PaleGoldenrod EEE8AA PaleGreen 98FB98 PaleTurquoise AFEEEE PaleVioletRed DB7093 PapayaWhip FFEFD5
PeachPuff FFDAB9 Peru CD853F Pink FFC0CB Plum DDA0DD PowderBlue B0E0E6 Purple 800080 Red FF0000
RosyBrown BC8F8F RoyalBlue 4169E1 SaddleBrown 8B4513 Salmon FA8072 SandyBrown F4A460 SeaGreen 2E8B57
Seashell FFF5EE Sienna A0522D Silver C0C0C0 SkyBlue 87CEEB SlateBlue 6A5ACD SlateGray 708090 Snow FFFAFA
SpringGreen 00FF7F SteelBlue 4682B4 Tan D2B48C Teal 008080 Thistle D8BFD8 Tomato FF6347 Turquoise 40E0D0
Violet EE82EE Wheat F5DEB3 White FFFFFF WhiteSmoke F5F5F5 Yellow FFFF00 YellowGreen 9ACD32"""

for _name, _hex in zip(_WEB_COLORS.split()[0::2], _WEB_COLORS.split()[1::2]):
    _rgb = int(_hex, 16)
    _bgr = ((_rgb & 0xFF) << 16) | (_rgb & 0xFF00) | ((_rgb >> 16) & 0xFF)
    _COLOR_NAMES["clr" + _name] = _bgr
_COLOR_NAMES["clrNONE"] = 0xFFFFFFFF
CLR_NONE = 0xFFFFFFFF
clrNONE = 0xFFFFFFFF
CLR_DEFAULT = 0xFF000000
clrDefault = 0xFF000000
for _k, _v in _COLOR_NAMES.items():
    globals()[_k] = _v


def color_to_hex(c) -> str:
    """MQL colour (BGR int) → '#rrggbb' (None for clrNONE)."""
    try:
        c = int(c)
    except (TypeError, ValueError):
        return None
    if c < 0 or c >= 0xFF000000:
        return None
    r, g, b = c & 0xFF, (c >> 8) & 0xFF, (c >> 16) & 0xFF
    return f"#{r:02x}{g:02x}{b:02x}"


def RGB(r, g, b):
    return (int(b) << 16) | (int(g) << 8) | int(r)
