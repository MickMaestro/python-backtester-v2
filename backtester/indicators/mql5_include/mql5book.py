"""MQL5 Book includes (MetaQuotes' *MQL5 Programming for Traders*) — ports of
the parts that compute something:

- ``MQL5Book/TimeServerDST.mqh`` — works out the broker server's UTC offset
  and daylight-saving state from when its weeks open in the H1 history
  (:func:`TimeServerZone` and friends, :func:`WeekIndex`, :func:`WeekStart`).
- ``MQL5Book/StringUtils.mqh``, ``MapArray.mqh``, ``QuickSortStructTRef.mqh``,
  ``AutoPtr.mqh``, ``PRTF.mqh``, ``IS.mqh``, ``Defines.mqh``.
- ``MQL5Book/DateTime.mqh`` is :class:`.mql4_compat.DateTime`;
  ``MQL5Book/MqlError.mqh`` is :mod:`.mql_error`.

``TimeServerDST`` notes: it reads ``PERIOD_H1`` bars of ``symbol`` from
:mod:`.terminal` (the chart's own series when the chart is H1, else whatever
H1 series was added). Offline there is no live server clock, so the final
"online time zone change" correction (``TimeGMT() - TimeTradeServer()``,
only applied when connected and not in the tester) never runs — as in the
MT5 strategy tester. Whether the symbol is a precious metal (whose week opens
an hour later) comes from the series spec: ``Rates(..., industry="metal")``
or a description starting with "Gold"; otherwise it is treated as Forex.
The function-level ``static`` cache is kept (module state), including its
invalidation rules.
"""

from __future__ import annotations

from . import terminal as T
from .mql4_compat import DateTime  # noqa: F401 — MQL5Book/DateTime.mqh
from .mql_error import E2S, MQL_ERROR  # noqa: F401 — MQL5Book/MqlError.mqh
from .mql_runtime import INT_MIN, idiv, imod

# ============================================================ TimeServerDST

TZDST_NOW_SCAN = -1
TZDST_THRESHOLD = idiv(52, 4)
LONG_MAX = 9223372036854775807


class ServerTimeZone:
    def __init__(self, offsetGMT=0, offsetDST=0, supportDST=False):
        self.offsetGMT = offsetGMT
        self.offsetDST = offsetDST
        self.supportDST = supportDST

    def copy(self):
        return ServerTimeZone(self.offsetGMT, self.offsetDST, self.supportDST)

    def __repr__(self):
        return f"ServerTimeZone(offsetGMT={self.offsetGMT}, offsetDST={self.offsetDST}, supportDST={self.supportDST})"


class TimeZoneChange:
    def __init__(self, weekstart, before, DSTb, after, DSTa):
        self.weekstart, self.before, self.DSTb, self.after, self.DSTa = weekstart, before, DSTb, after, DSTa


def HourToUTC(current: int, dst: bool = False) -> int:
    if current == INT_MIN:
        return INT_MIN
    result = current + 2 + int(dst)
    result = imod(result, 24)
    if result > 12:
        result = result - 24
    return result


def UTCToHour(current: int, dst: bool = False) -> int:
    if current == INT_MIN:
        return INT_MIN
    return imod(current + 24 - 2 - int(dst), 24)


def WeekIndex(t: int) -> int:
    return idiv(int(t) + 345600, 604800)


def WeekStart(t: int) -> int:
    return int(t) - imod(int(t) + 345600, 604800)


def _wrap24(v: int) -> int:
    return imod(v + 24, 24)


class _Cache:
    st = ServerTimeZone()
    changes: list = []
    hours = [0] * 24
    cacheTime = 0
    cacheSymbol = None
    cacheThreshold = 0
    lastindex = -1
    lastrequest = LONG_MAX


def _empty():
    return ServerTimeZone(INT_MIN, INT_MIN, False)


def TimeServerZone(srvtime: int = 0, threshold: int = TZDST_THRESHOLD,
                   lookupYears: float = 0.0, symbol: str | None = None) -> ServerTimeZone:
    """Server time zone as ``ServerTimeZone(offsetGMT, offsetDST, supportDST)``
    (offsets in seconds, negated as MQL5's ``TimeGMTOffset`` is); offsets are
    ``INT_MIN`` when the history cannot tell."""
    year = 365 * 24 * 60 * 60
    hour = 3600
    C = _Cache
    utc = INT_MIN
    DST = False
    rates = T.rates_for(symbol, T.PERIOD_H1)
    sym = symbol if symbol else (T.current().chart.symbol if T.current().chart else "")
    now = int(rates.time[-1]) if rates is not None and len(rates) else 0
    curtime = int(srvtime)
    if curtime <= 0 or curtime > now:
        curtime = now
    if (srvtime < 0 or WeekIndex(curtime) > WeekIndex(C.cacheTime)
            or C.cacheSymbol != sym or C.cacheThreshold != threshold):
        C.cacheTime = 0
        C.changes = []
        C.hours = [0] * 24
        C.st = _empty()
        C.lastindex = -1
        C.lastrequest = LONG_MAX

    if C.cacheTime and C.changes:
        if curtime <= C.changes[0].weekstart:
            return _empty()
        i = C.lastindex if curtime >= C.lastrequest else 0
        while i < len(C.changes):
            ch = C.changes[i]
            if ch.weekstart > curtime and C.hours[UTCToHour(ch.before)] > threshold:
                utc = ch.before
                DST = ch.DSTb
                break
            i += 1
        if i == len(C.changes):
            i = len(C.changes) - 1
            utc = C.changes[i].after
            DST = C.changes[i].DSTa
        C.lastrequest = curtime
        C.lastindex = i
    else:
        spec = rates.spec if rates is not None else {}
        metal = (spec.get("industry") == "metal"
                 or str(spec.get("description", "")).startswith("Gold"))
        array = None
        if rates is not None and len(rates):
            times = [int(t) for t in rates.time]
            if lookupYears:
                lo = curtime - int(lookupYears * year)
                hi = curtime + int(metal) * hour
                sub = [t for t in times if lo <= t <= hi]
                array = sub if sub else times
            else:
                array = times
        if not array:
            return _empty()
        n = len(array)
        dst = [False] * 24
        current = previous = last = prevlast = INT_MIN
        i = 1
        while i < n:
            if array[i] - array[i - 1] <= 24 * hour:
                i += 1
                continue
            s = T.TimeToStruct(array[i])
            if s.day_of_week > 1:                       # weekday > MONDAY
                i += 1
                continue
            previous = current
            current = s.hour
            if 3 <= s.mon <= 11:
                iYear = s.year
                d1 = 14 - imod(1 + idiv(5 * iYear, 4), 7)
                d2 = 7 - imod(1 + idiv(5 * iYear, 4), 7)
                dst_begin = T.StructToTime(T.MqlDateTime(iYear, 3, d1, 0, 0, 0, 0, 0))
                dst_end = T.StructToTime(T.MqlDateTime(iYear, 11, d2, 0, 0, 0, 0, 0))
                if dst_begin <= array[i] < dst_end:
                    current = _wrap24(current + 1)
            if metal:
                current = _wrap24(current - 1)
            if previous != current:
                C.changes.append(TimeZoneChange(
                    WeekStart(array[i]), HourToUTC(previous),
                    previous != INT_MIN and _wrap24(previous - 1) == current,
                    HourToUTC(current),
                    previous == _wrap24(current - 1)))
            C.hours[current] += 1
            if array[i] <= curtime + int(metal) * hour:
                prevlast = last
                last = current
            i += 48
            i += 1
        if last == INT_MIN:
            return _empty()
        if C.hours[last] < threshold + 1:
            if prevlast != INT_MIN and prevlast != current:
                if not C.hours[prevlast] < threshold + 1:
                    last = prevlast
        for h in range(24):
            if C.hours[h] > threshold:
                if C.hours[_wrap24(h - 1)] > threshold:
                    dst[h] = True
                    C.st.supportDST = True
        DST = dst[last]
        utc = HourToUTC(last)
        C.cacheTime = array[n - 1]
        C.cacheSymbol = sym
        C.cacheThreshold = threshold
    # (online correction against TimeGMT() skipped: never connected offline)
    C.st.offsetGMT = -utc * hour
    C.st.offsetDST = -int(DST) * hour
    return C.st.copy()


def TimeServerDaylightSavings(srvtime=0, threshold=TZDST_THRESHOLD, lookupYears=0.0, symbol=None) -> int:
    return TimeServerZone(srvtime, threshold, lookupYears, symbol).offsetDST


def TimeServerGMTOffsetHistory(srvtime=0, threshold=TZDST_THRESHOLD, lookupYears=0.0, symbol=None) -> int:
    return TimeServerZone(srvtime, threshold, lookupYears, symbol).offsetGMT


def TimeServerDaylightSavingsSupported(srvtime=0, threshold=TZDST_THRESHOLD, lookupYears=0.0,
                                       symbol=None) -> bool:
    return TimeServerZone(srvtime, threshold, lookupYears, symbol).supportDST


# ============================================================ StringUtils


def StringCombine(array, glue) -> str:
    glue = glue if isinstance(glue, str) else chr(glue)
    return glue.join(array) if array else ""


def SubArrayCombine(array, glue: str = "", start: int = 0, count: int = -1) -> str:
    n = len(array)
    if start >= n:
        return ""
    if count == -1:
        count = n - start
    return glue.join(array[start: start + count])


def StringReverse(source: str) -> str:
    return source[::-1]


# ============================================================ MapArray


class MapArray:
    """An insertion-ordered key → value list with linear lookup."""

    def __init__(self):
        self.array: list[list] = []

    def getSize(self) -> int:
        return len(self.array)

    def getKey(self, i: int):
        return self.array[i][0]

    def getValue(self, i: int):
        return self.array[i][1]

    def find(self, k) -> int:
        for i, (key, _) in enumerate(self.array):
            if key == k:
                return i
        return -1

    def put(self, k, v) -> int:
        i = self.find(k)
        if i != -1:
            self.array[i][1] = v
            return i
        self.array.append([k, v])
        return len(self.array) - 1

    def inc(self, k, plus=1) -> int:
        i = self.find(k)
        if i != -1:
            self.array[i][1] += plus
            return i
        self.array.append([k, plus])
        return len(self.array) - 1

    def remove(self, k) -> None:
        i = self.find(k)
        if i != -1:
            del self.array[i]

    def __getitem__(self, key):
        if isinstance(key, int) and not (self.array and isinstance(self.array[0][0], int)):
            return self.array[key][1]
        i = self.find(key)
        return self.array[i][1] if i != -1 else None

    def reset(self) -> None:
        self.array = []

    def print(self) -> None:
        for k, v in self.array:
            print(k, v)


# ===================================================== QuickSortStructTRef


class QuickSortStructTRef:
    """Quicksort with a user ``Compare(a, b)`` (true = a goes after b),
    recursive (:meth:`QuickSort`) and explicit-stack (:meth:`QuickSortLoop`)
    versions, as in the source (same pivot choice, so equal elements end up
    in the same order)."""

    def Compare(self, a, b) -> bool:
        raise NotImplementedError

    @staticmethod
    def Swap(array, i, j):
        if i != j:
            array[i], array[j] = array[j], array[i]

    def QuickSort(self, array, start: int = 0, end: int | None = None) -> None:
        if end is None:
            end = start + len(array) - 1
        if start < end:
            pivot = start
            self.Swap(array, idiv(start + end, 2) + 1, end)
            for i in range(start, end + 1):
                if not self.Compare(array[i], array[end]):
                    self.Swap(array, i, pivot)
                    pivot += 1
            pivot -= 1
            self.QuickSort(array, start, pivot - 1)
            self.QuickSort(array, pivot + 1, end)

    def QuickSortLoop(self, array, start: int = 0, end: int | None = None) -> None:
        if end is None:
            end = start + len(array) - 1
        stack = [(start, end)]
        while stack:
            s, e = stack.pop()
            if s < e:
                pivot = s
                self.Swap(array, idiv(s + e, 2) + 1, e)
                for i in range(s, e + 1):
                    if not self.Compare(array[i], array[e]):
                        self.Swap(array, i, pivot)
                        pivot += 1
                pivot -= 1
                if e > pivot + 1:
                    stack.append((pivot + 1, e))
                if s < pivot - 1:
                    stack.append((s, pivot - 1))


def SORT_STRUCT(array, field: str) -> None:
    """``SORT_STRUCT(T, A, F)``: ascending by ``F`` (``Compare`` is ``a.F > b.F``)."""
    class _Sort(QuickSortStructTRef):
        def Compare(self, a, b):
            return getattr(a, field) > getattr(b, field)
    _Sort().QuickSort(array)


def SORT_STRUCT_REF(array, field: str) -> None:
    class _Sort(QuickSortStructTRef):
        def Compare(self, a, b):
            return getattr(a, field) > getattr(b, field)
    _Sort().QuickSortLoop(array)


def SORT_STRUCT_REF_2(array, f1: str, f2: str) -> None:
    class _Sort(QuickSortStructTRef):
        def Compare(self, a, b):
            return (getattr(a, f1) > getattr(b, f1)
                    or (getattr(a, f1) == getattr(b, f1) and getattr(a, f2) > getattr(b, f2)))
    _Sort().QuickSortLoop(array)


# ============================================================ small ones


class AutoPtr:
    """Owns an object pointer; Python's garbage collector does the freeing."""

    def __init__(self, p=None):
        self.ptr = p

    def __getitem__(self, x=0):
        return self.ptr

    def set(self, p):
        self.ptr = p
        return p


def ResultPrint(s: str, retval=None, last_error: int = 0):
    """``PRTF`` helper: prints ``expr=value / ok`` (or the error name)."""
    err = f"{E2S(last_error)}({last_error})"
    print(f"{s}={retval} / {'ok' if last_error == 0 else err}")
    return retval


def ErrorPrint(s: str, retval=None, last_error: int = 0):
    if last_error:
        return ResultPrint(s, retval, last_error)
    return retval


# enum IS
EQUAL, GREATER, NOT_EQUAL, LESS, OR_EQUAL, OR_BITWISE, EQUAL_OR_ZERO = range(7)


def PUSH(array: list, value):
    """``PUSH(A, V)`` from Defines.mqh."""
    array.append(value)
    return value


def EXPAND(array: list) -> int:
    """``EXPAND(A)``: grow by one, return the new last index."""
    array.append(None)
    return len(array) - 1


def STR_TIME_MSC(t_msc: int) -> str:
    import datetime as _dt
    d = _dt.datetime(1970, 1, 1) + _dt.timedelta(seconds=int(t_msc) // 1000)
    return d.strftime("%Y.%m.%d %H:%M:%S") + "'%03d" % (int(t_msc) % 1000)
