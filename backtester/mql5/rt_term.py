"""MQL5 runtime — the terminal: bar series by symbol/timeframe, symbol and
account info, indicator buffers and plot properties, indicator handles
(``iMA``…, ``iCustom``) with ``CopyBuffer``, chart objects, global variables.

A :class:`Context` describes one running program (one indicator on one
chart). Contexts nest: an ``iCustom`` handle runs another converted indicator
in its own context, on the same bars or on bars aggregated to a higher
timeframe.
"""

from __future__ import annotations

import math
import threading

import numpy as np

from .rt_core import (
    DBL_MAX, EMPTY_VALUE, INVALID_HANDLE, Arr, MqlDateTime, MqlObject, MqlRuntimeError,
    TimeToStruct, _print,
)

# ------------------------------------------------------------------ timeframes

PERIOD_CURRENT = 0
PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6 = 1, 2, 3, 4, 5, 6
PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30 = 10, 12, 15, 20, 30
PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4 = 16385, 16386, 16387, 16388
PERIOD_H6, PERIOD_H8, PERIOD_H12 = 16390, 16392, 16396
PERIOD_D1, PERIOD_W1, PERIOD_MN1 = 16408, 32769, 49153

TF_NAMES = {
    0: "PERIOD_CURRENT", 1: "PERIOD_M1", 2: "PERIOD_M2", 3: "PERIOD_M3", 4: "PERIOD_M4",
    5: "PERIOD_M5", 6: "PERIOD_M6", 10: "PERIOD_M10", 12: "PERIOD_M12", 15: "PERIOD_M15",
    20: "PERIOD_M20", 30: "PERIOD_M30", 16385: "PERIOD_H1", 16386: "PERIOD_H2",
    16387: "PERIOD_H3", 16388: "PERIOD_H4", 16390: "PERIOD_H6", 16392: "PERIOD_H8",
    16396: "PERIOD_H12", 16408: "PERIOD_D1", 32769: "PERIOD_W1", 49153: "PERIOD_MN1",
}


def tf_seconds(tf: int) -> int:
    if tf < 16385:
        return tf * 60
    if tf < 32769:
        return (tf - 16384) * 3600
    if tf == PERIOD_W1:
        return 7 * 86400
    if tf == PERIOD_MN1:
        return 30 * 86400
    return 86400


def seconds_to_tf(sec: float) -> int:
    best = PERIOD_H1
    for tf in TF_NAMES:
        if tf == 0:
            continue
        if abs(tf_seconds(tf) - sec) < abs(tf_seconds(best) - sec):
            best = tf
    return best


# ------------------------------------------------------------------ series

class Series:
    """Bars of one symbol/timeframe, oldest first, as Python lists."""

    def __init__(self, time, open_, high, low, close, tick_volume, volume, spread):
        self.time = [int(x) for x in time]
        self.open = [float(x) for x in open_]
        self.high = [float(x) for x in high]
        self.low = [float(x) for x in low]
        self.close = [float(x) for x in close]
        self.tick_volume = [int(x) for x in tick_volume]
        self.volume = [int(x) for x in volume]
        self.spread = [int(x) for x in spread]
        self.n = len(self.time)
        self._np = {}

    def np(self, name):
        a = self._np.get(name)
        if a is None:
            a = np.asarray(getattr(self, name), dtype=float)
            self._np[name] = a
        return a

    @classmethod
    def from_df(cls, df):
        n = len(df)
        t = df["time"]
        if np.issubdtype(t.dtype, np.datetime64):
            times = (t.to_numpy().astype("datetime64[s]").astype(np.int64)).tolist()
        else:
            times = [int(x) for x in t]
        col = (lambda k, d=0: df[k].to_numpy() if k in df.columns else np.full(n, d))
        return cls(times, col("open"), col("high"), col("low"), col("close"),
                   col("tick_volume"), col("real_volume"), col("spread"))

    def bar_index_at(self, t: int) -> int:
        """Forward index of the bar containing time ``t`` (-1 if before first)."""
        import bisect
        return bisect.bisect_right(self.time, int(t)) - 1


def _bucket(t: int, tf: int) -> int:
    if tf == PERIOD_W1:
        # MT5 weeks start on Sunday 00:00
        days = t // 86400
        dow = (days + 4) % 7          # 1970-01-01 was a Thursday -> 4
        return (days - dow) * 86400
    if tf == PERIOD_MN1:
        import time as _t
        tm = _t.gmtime(t)
        import calendar
        return calendar.timegm((tm.tm_year, tm.tm_mon, 1, 0, 0, 0))
    sec = tf_seconds(tf)
    return t - t % sec


def aggregate(base: Series, tf: int) -> Series:
    keys = [_bucket(t, tf) for t in base.time]
    T, O, H, L, C, TV, V, S = [], [], [], [], [], [], [], []
    last = None
    for i, k in enumerate(keys):
        if k != last:
            T.append(k)
            O.append(base.open[i])
            H.append(base.high[i])
            L.append(base.low[i])
            C.append(base.close[i])
            TV.append(base.tick_volume[i])
            V.append(base.volume[i])
            S.append(base.spread[i])
            last = k
        else:
            if base.high[i] > H[-1]:
                H[-1] = base.high[i]
            if base.low[i] < L[-1]:
                L[-1] = base.low[i]
            C[-1] = base.close[i]
            TV[-1] += base.tick_volume[i]
            V[-1] += base.volume[i]
            S[-1] = base.spread[i]
    return Series(T, O, H, L, C, TV, V, S)


class Market:
    """The data the 'terminal' has: per symbol, the base series and its period."""

    def __init__(self):
        self.symbols: dict[str, tuple[Series, int, dict]] = {}
        self._cache: dict[tuple[str, int], Series] = {}

    def add(self, symbol: str, series: Series, period: int, spec: dict):
        self.symbols[symbol] = (series, period, spec)
        self._cache = {k: v for k, v in self._cache.items() if k[0] != symbol}

    def series(self, symbol: str, tf: int) -> Series | None:
        ent = self.symbols.get(symbol)
        if ent is None:
            return None
        base, bper, _spec = ent
        if tf == 0 or tf == bper:
            return base
        key = (symbol, tf)
        s = self._cache.get(key)
        if s is not None:
            return s
        if tf_seconds(tf) < tf_seconds(bper) or tf_seconds(tf) % tf_seconds(bper) and tf not in (PERIOD_W1, PERIOD_MN1):
            return None    # lower timeframe than the data: no history
        s = aggregate(base, tf)
        self._cache[key] = s
        return s


# ------------------------------------------------------------------ context

class PlotProps:
    __slots__ = ("props",)

    def __init__(self):
        self.props: dict = {}


class Context:
    def __init__(self, market: Market, symbol: str, period: int, name: str = "", program=None):
        self.market = market
        self.symbol = symbol
        self.period = period
        self.name = name
        self.program = program
        self.buffers: dict[int, tuple[Arr, int]] = {}
        self.plot_props: dict[int, dict] = {}
        self.ind_props: dict = {"levels": {}, "levelcolor": {}, "leveltext": {}}
        self.handles: list = []
        self.last_error = 0
        self.objects: dict[str, dict] = {}
        self.object_order: list[str] = []
        self.events: list[str] = []
        self.rates_total = 0
        self.calc_depth = 0
        ent = market.symbols.get(symbol)
        self.spec = ent[2] if ent else {}

    @property
    def series(self) -> Series:
        return self.market.series(self.symbol, self.period)


_tls = threading.local()


_DEFAULT_CTX = []


def ctx() -> Context:
    c = getattr(_tls, "ctx", None)
    if c is None:
        if not _DEFAULT_CTX:
            m = Market()
            m.add("EURUSD", Series([], [], [], [], [], [], [], []), PERIOD_H1, {"point": 0.00001, "digits": 5})
            _DEFAULT_CTX.append(Context(m, "EURUSD", PERIOD_H1, "default"))
        return _DEFAULT_CTX[0]
    return c


def push_ctx(c: Context):
    stack = getattr(_tls, "stack", None)
    if stack is None:
        stack = _tls.stack = []
    stack.append(getattr(_tls, "ctx", None))
    _tls.ctx = c


def pop_ctx():
    _tls.ctx = _tls.stack.pop()


def _sym(symbol):
    c = ctx()
    if symbol is None or symbol == "" or symbol == 0:
        return c.symbol
    return str(symbol)


def _tf(tf):
    c = ctx()
    tf = int(tf) if tf is not None else 0
    return c.period if tf == 0 else tf


def _series(symbol, tf) -> Series | None:
    c = ctx()
    return c.market.series(_sym(symbol), _tf(tf))


# ------------------------------------------------------------------ program info

def Symbol():
    return ctx().symbol


def Period():
    return ctx().period


def Point():
    return float(ctx().spec.get("point", 0.00001))


def Digits():
    return int(ctx().spec.get("digits", 5))


def ChartSymbol(chart_id=0):
    return ctx().symbol


def ChartPeriod(chart_id=0):
    return ctx().period


def PeriodSeconds(tf=PERIOD_CURRENT):
    return tf_seconds(_tf(tf))


def IsStopped():
    return False


def GetLastError():
    return ctx().last_error


def ResetLastError():
    ctx().last_error = 0


def SetUserError(code):
    ctx().last_error = 65536 + int(code)


def _set_error(code):
    try:
        ctx().last_error = code
    except MqlRuntimeError:
        pass


def UninitializeReason():
    return 0


def TerminalClose(code):
    return True


def ExpertRemove():
    pass


def TesterStatistics(stat):
    return 0.0


def TesterStop():
    pass


# ------------------------------------------------------------------ time

def TimeCurrent(st=None):
    s = ctx().series
    t = s.time[-1] if s and s.n else 0
    if st is not None:
        TimeToStruct(t, st)
    return t


def TimeTradeServer(st=None):
    return TimeCurrent(st)


def TimeLocal(st=None):
    return TimeCurrent(st)


def TimeGMT(st=None):
    return TimeCurrent(st)


def TimeDaylightSavings():
    return 0


def TimeGMTOffset():
    return 0


# ------------------------------------------------------------------ series access

def Bars(symbol=None, tf=0, start=None, stop=None):
    s = _series(symbol, tf)
    if s is None:
        _set_error(4401)
        return 0
    if start is None:
        return s.n
    a, b = sorted((int(start), int(stop)))
    return sum(1 for t in s.time if a <= t <= b)


def iBars(symbol=None, tf=0):
    return Bars(symbol, tf)


def _field(symbol, tf, shift, name):
    s = _series(symbol, tf)
    if s is None:
        return 0
    shift = int(shift)
    if shift < 0 or shift >= s.n:
        return 0
    return getattr(s, name)[s.n - 1 - shift]


def iTime(symbol=None, tf=0, shift=0):
    return _field(symbol, tf, shift, "time")


def iOpen(symbol=None, tf=0, shift=0):
    return _field(symbol, tf, shift, "open")


def iHigh(symbol=None, tf=0, shift=0):
    return _field(symbol, tf, shift, "high")


def iLow(symbol=None, tf=0, shift=0):
    return _field(symbol, tf, shift, "low")


def iClose(symbol=None, tf=0, shift=0):
    return _field(symbol, tf, shift, "close")


def iVolume(symbol=None, tf=0, shift=0):
    return _field(symbol, tf, shift, "tick_volume")


def iTickVolume(symbol=None, tf=0, shift=0):
    return _field(symbol, tf, shift, "tick_volume")


def iRealVolume(symbol=None, tf=0, shift=0):
    return _field(symbol, tf, shift, "volume")


def iSpread(symbol=None, tf=0, shift=0):
    return _field(symbol, tf, shift, "spread")


def iBarShift(symbol=None, tf=0, time=0, exact=False):
    s = _series(symbol, tf)
    if s is None or s.n == 0:
        return -1
    t = int(time)
    k = s.bar_index_at(t)
    if k < 0:
        return -1 if exact else s.n - 1
    if exact and s.time[k] != t:
        # exact: the time must fall inside the bar
        if t >= s.time[k] + tf_seconds(_tf(tf)):
            return -1
    return s.n - 1 - k


MODE_OPEN, MODE_LOW, MODE_HIGH, MODE_CLOSE, MODE_VOLUME, MODE_REAL_VOLUME, MODE_SPREAD, MODE_TIME = 0, 1, 2, 3, 4, 5, 6, 7
_SERIES_MODE = {0: "open", 1: "low", 2: "high", 3: "close", 4: "tick_volume", 5: "volume", 6: "spread", 7: "time"}


def iHighest(symbol=None, tf=0, type=MODE_HIGH, count=-1, start=0):
    s = _series(symbol, tf)
    if s is None:
        return -1
    arr = getattr(s, _SERIES_MODE.get(int(type), "high"))
    n = s.n
    if count is None or count < 0 or count == -1:
        count = n - start
    best, bv = -1, None
    for sh in range(int(start), min(n, int(start) + int(count))):
        v = arr[n - 1 - sh]
        if bv is None or v > bv:
            bv, best = v, sh
    return best


def iLowest(symbol=None, tf=0, type=MODE_LOW, count=-1, start=0):
    s = _series(symbol, tf)
    if s is None:
        return -1
    arr = getattr(s, _SERIES_MODE.get(int(type), "low"))
    n = s.n
    if count is None or count < 0:
        count = n - start
    best, bv = -1, None
    for sh in range(int(start), min(n, int(start) + int(count))):
        v = arr[n - 1 - sh]
        if bv is None or v < bv:
            bv, best = v, sh
    return best


class _DT(int):
    """A datetime argument: selects the time-based overload of CopyXxx even for 0."""
    __slots__ = ()


def _copy_range(s: Series, a, b):
    """Resolve the three CopyXxx call forms to a forward index range [lo, hi)."""
    n = s.n
    a_dt, b_dt = isinstance(a, _DT), isinstance(b, _DT)
    a = int(a)
    b = int(b)
    if a_dt or a > 100_000_000:              # start_time
        if b_dt or b > 100_000_000:          # (start_time, stop_time)
            t0, t1 = sorted((a, b))
            lo = next((i for i, t in enumerate(s.time) if t >= t0), n)
            hi = s.bar_index_at(t1) + 1
            return lo, max(lo, hi)
        hi = s.bar_index_at(a) + 1           # (start_time, count): bars up to start_time
        lo = max(0, hi - b)
        return lo, hi
    start, count = a, b
    if start < 0 or start >= n or count <= 0:
        return 0, 0
    hi = n - start
    lo = max(0, hi - count)
    return lo, hi


def _copy_into(dst: Arr, values: list, bound_n=None):
    """Copy chronologically ordered values into an MQL array the way
    CopyBuffer/CopyRates do: dynamic arrays are resized to the count; indicator
    buffers keep their size and are filled time-aligned from the newest end."""
    cnt = len(values)
    if dst.buffer:
        n = len(dst.a)
        k = min(cnt, n)
        dst.a[n - k:] = values[cnt - k:]
        return k
    if dst.dyn:
        dst.a = list(values)
        return cnt
    k = min(cnt, len(dst.a))
    dst.a[:k] = values[:k]
    return k


def _copy_series(symbol, tf, a, b, dst, name):
    s = _series(symbol, tf)
    if s is None:
        _set_error(4401)
        return -1
    lo, hi = _copy_range(s, a, b)
    if hi <= lo:
        return -1 if s.n == 0 else 0 if hi == lo else -1
    vals = getattr(s, name)[lo:hi]
    return _copy_into(dst, vals)


def CopyTime(symbol, tf, a, b, dst):
    return _copy_series(symbol, tf, a, b, dst, "time")


def CopyOpen(symbol, tf, a, b, dst):
    return _copy_series(symbol, tf, a, b, dst, "open")


def CopyHigh(symbol, tf, a, b, dst):
    return _copy_series(symbol, tf, a, b, dst, "high")


def CopyLow(symbol, tf, a, b, dst):
    return _copy_series(symbol, tf, a, b, dst, "low")


def CopyClose(symbol, tf, a, b, dst):
    return _copy_series(symbol, tf, a, b, dst, "close")


def CopyTickVolume(symbol, tf, a, b, dst):
    return _copy_series(symbol, tf, a, b, dst, "tick_volume")


def CopyRealVolume(symbol, tf, a, b, dst):
    return _copy_series(symbol, tf, a, b, dst, "volume")


def CopySpread(symbol, tf, a, b, dst):
    return _copy_series(symbol, tf, a, b, dst, "spread")


class MqlRates(MqlObject):
    def __init__(self):
        self.time = 0
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0
        self.tick_volume = 0
        self.spread = 0
        self.real_volume = 0


class MqlTick(MqlObject):
    def __init__(self):
        self.time = 0
        self.bid = 0.0
        self.ask = 0.0
        self.last = 0.0
        self.volume = 0
        self.time_msc = 0
        self.flags = 0
        self.volume_real = 0.0


class MqlParam(MqlObject):
    def __init__(self):
        self.type = 0
        self.integer_value = 0
        self.double_value = 0.0
        self.string_value = ""


class MqlBookInfo(MqlObject):
    def __init__(self):
        self.type = 0
        self.price = 0.0
        self.volume = 0
        self.volume_real = 0.0


def CopyRates(symbol, tf, a, b, dst):
    s = _series(symbol, tf)
    if s is None:
        return -1
    lo, hi = _copy_range(s, a, b)
    vals = []
    for i in range(lo, hi):
        r = MqlRates()
        r.time, r.open, r.high, r.low, r.close = s.time[i], s.open[i], s.high[i], s.low[i], s.close[i]
        r.tick_volume, r.spread, r.real_volume = s.tick_volume[i], s.spread[i], s.volume[i]
        vals.append(r)
    if hi <= lo:
        return -1
    return _copy_into(dst, vals)


def CopyTicks(*args):
    return -1


def CopyTicksRange(*args):
    return -1


def SymbolInfoTick(symbol, tick):
    s = _series(symbol, 0)
    if s is None or s.n == 0:
        return False
    tick.time = s.time[-1]
    tick.bid = s.close[-1]
    tick.ask = s.close[-1] + s.spread[-1] * Point()
    tick.last = s.close[-1]
    tick.volume = s.tick_volume[-1]
    tick.time_msc = tick.time * 1000
    return True


SERIES_BARS_COUNT, SERIES_FIRSTDATE, SERIES_LASTBAR_DATE = 0, 1, 5
SERIES_SERVER_FIRSTDATE, SERIES_TERMINAL_FIRSTDATE, SERIES_SYNCHRONIZED = 2, 3, 4


def SeriesInfoInteger(symbol, tf, prop, ref=None):
    s = _series(symbol, tf)
    if s is None:
        v = 0
    elif prop == SERIES_BARS_COUNT:
        v = s.n
    elif prop in (SERIES_FIRSTDATE, SERIES_SERVER_FIRSTDATE, SERIES_TERMINAL_FIRSTDATE):
        v = s.time[0] if s.n else 0
    elif prop == SERIES_LASTBAR_DATE:
        v = s.time[-1] if s.n else 0
    elif prop == SERIES_SYNCHRONIZED:
        v = True
    else:
        v = 0
    if ref is not None:
        ref.v = v
        return s is not None
    return v


# ------------------------------------------------------------------ symbol / account

SYMBOL_BID, SYMBOL_ASK, SYMBOL_POINT, SYMBOL_DIGITS, SYMBOL_SPREAD = 1, 4, 16, 17, 18
SYMBOL_LAST, SYMBOL_BIDHIGH, SYMBOL_BIDLOW, SYMBOL_ASKHIGH, SYMBOL_ASKLOW = 7, 2, 3, 5, 6
SYMBOL_TRADE_TICK_VALUE, SYMBOL_TRADE_TICK_SIZE, SYMBOL_TRADE_CONTRACT_SIZE = 26, 27, 28
SYMBOL_VOLUME_MIN, SYMBOL_VOLUME_MAX, SYMBOL_VOLUME_STEP = 34, 35, 36
SYMBOL_TRADE_TICK_VALUE_PROFIT, SYMBOL_TRADE_TICK_VALUE_LOSS = 53, 54
SYMBOL_TRADE_STOPS_LEVEL, SYMBOL_TRADE_FREEZE_LEVEL, SYMBOL_SPREAD_FLOAT = 31, 32, 41
SYMBOL_DESCRIPTION, SYMBOL_CURRENCY_BASE, SYMBOL_CURRENCY_PROFIT, SYMBOL_CURRENCY_MARGIN = 20, 22, 23, 24
SYMBOL_PATH, SYMBOL_TIME, SYMBOL_SELECT, SYMBOL_VISIBLE, SYMBOL_VOLUME = 21, 15, 0, 76, 10
SYMBOL_TRADE_MODE, SYMBOL_TRADE_CALC_MODE, SYMBOL_MARGIN_INITIAL = 33, 29, 42
SYMBOL_SWAP_LONG, SYMBOL_SWAP_SHORT, SYMBOL_SESSION_VOLUME = 38, 39, 71
SYMBOL_LASTHIGH, SYMBOL_LASTLOW, SYMBOL_VOLUMEHIGH, SYMBOL_VOLUMELOW = 8, 9, 11, 12
SYMBOL_EXPIRATION_MODE, SYMBOL_FILLING_MODE, SYMBOL_ORDER_MODE, SYMBOL_TRADE_EXEMODE = 49, 50, 51, 52
SYMBOL_BASIS, SYMBOL_BANK, SYMBOL_NAME, SYMBOL_EXCHANGE, SYMBOL_ISIN = 25, 30, 99, 98, 97
SYMBOL_SECTOR, SYMBOL_INDUSTRY, SYMBOL_COUNTRY = 96, 95, 94
SYMBOL_POINT_VALUE = 0


def _spec(symbol=None):
    c = ctx()
    ent = c.market.symbols.get(_sym(symbol))
    return ent[2] if ent else {}


def SymbolInfoDouble(symbol, prop, ref=None):
    s = _series(symbol, 0)
    spec = _spec(symbol)
    point = float(spec.get("point", 0.00001))
    last = s.close[-1] if s is not None and s.n else 0.0
    spread = s.spread[-1] if s is not None and s.n else 0
    vals = {
        SYMBOL_BID: last, SYMBOL_ASK: last + spread * point, SYMBOL_LAST: last,
        SYMBOL_POINT: point, SYMBOL_TRADE_TICK_SIZE: float(spec.get("tick_size", point)),
        SYMBOL_TRADE_TICK_VALUE: float(spec.get("tick_value", 1.0)),
        SYMBOL_TRADE_TICK_VALUE_PROFIT: float(spec.get("tick_value", 1.0)),
        SYMBOL_TRADE_TICK_VALUE_LOSS: float(spec.get("tick_value", 1.0)),
        SYMBOL_TRADE_CONTRACT_SIZE: float(spec.get("contract_size", 100000.0)),
        SYMBOL_VOLUME_MIN: float(spec.get("volume_min", 0.01)),
        SYMBOL_VOLUME_MAX: float(spec.get("volume_max", 100.0)),
        SYMBOL_VOLUME_STEP: float(spec.get("volume_step", 0.01)),
        SYMBOL_BIDHIGH: max(s.high[-1440:]) if s is not None and s.n else 0.0,
        SYMBOL_BIDLOW: min(s.low[-1440:]) if s is not None and s.n else 0.0,
    }
    v = float(vals.get(int(prop), 0.0))
    if ref is not None:
        ref.v = v
        return s is not None
    return v


def SymbolInfoInteger(symbol, prop, ref=None):
    s = _series(symbol, 0)
    spec = _spec(symbol)
    vals = {
        SYMBOL_DIGITS: int(spec.get("digits", 5)),
        SYMBOL_SPREAD: s.spread[-1] if s is not None and s.n else 0,
        SYMBOL_TIME: s.time[-1] if s is not None and s.n else 0,
        SYMBOL_SELECT: 1, SYMBOL_VISIBLE: 1, SYMBOL_SPREAD_FLOAT: 1,
        SYMBOL_TRADE_STOPS_LEVEL: int(spec.get("stops_level", 0)),
        SYMBOL_TRADE_CALC_MODE: int(spec.get("calc_mode", 0)),
        SYMBOL_TRADE_MODE: 4,
        SYMBOL_VOLUME: s.tick_volume[-1] if s is not None and s.n else 0,
    }
    v = int(vals.get(int(prop), 0))
    if ref is not None:
        ref.v = v
        return s is not None
    return v


def SymbolInfoString(symbol, prop, ref=None):
    name = _sym(symbol)
    spec = _spec(symbol)
    base = spec.get("currency_base", name[:3])
    profit = spec.get("currency_profit", name[3:6] if len(name) >= 6 else "USD")
    vals = {SYMBOL_DESCRIPTION: spec.get("description", name), SYMBOL_CURRENCY_BASE: base,
            SYMBOL_CURRENCY_PROFIT: profit, SYMBOL_CURRENCY_MARGIN: base, SYMBOL_PATH: name,
            SYMBOL_NAME: name}
    v = str(vals.get(int(prop), ""))
    if ref is not None:
        ref.v = v
        return True
    return v


def SymbolSelect(name, select=True):
    return _sym(name) in ctx().market.symbols


def SymbolExist(name, ref=None):
    ok = _sym(name) in ctx().market.symbols
    if ref is not None:
        ref.v = False
    return ok


def SymbolsTotal(selected=True):
    return len(ctx().market.symbols)


def SymbolName(pos, selected=True):
    names = list(ctx().market.symbols)
    return names[pos] if 0 <= pos < len(names) else ""


def SymbolIsSynchronized(name=None):
    return True


def SymbolInfoSessionQuote(*args):
    return False


def SymbolInfoSessionTrade(*args):
    return False


def MarketBookAdd(symbol):
    return False


def MarketBookRelease(symbol):
    return True


def MarketBookGet(symbol, book):
    return False


ACCOUNT_BALANCE, ACCOUNT_EQUITY, ACCOUNT_MARGIN, ACCOUNT_MARGIN_FREE, ACCOUNT_PROFIT = 37, 40, 41, 42, 39
ACCOUNT_CREDIT, ACCOUNT_MARGIN_LEVEL, ACCOUNT_LEVERAGE, ACCOUNT_LOGIN = 38, 43, 35, 0
ACCOUNT_CURRENCY, ACCOUNT_NAME, ACCOUNT_SERVER, ACCOUNT_COMPANY = 36, 1, 3, 2
ACCOUNT_TRADE_MODE, ACCOUNT_LIMIT_ORDERS, ACCOUNT_MARGIN_SO_MODE = 32, 47, 44
ACCOUNT_TRADE_ALLOWED, ACCOUNT_TRADE_EXPERT, ACCOUNT_MARGIN_SO_CALL, ACCOUNT_MARGIN_SO_SO = 33, 34, 45, 46
ACCOUNT_MARGIN_MODE, ACCOUNT_CURRENCY_DIGITS = 48, 49
ACCOUNT_MARGIN_INITIAL, ACCOUNT_MARGIN_MAINTENANCE, ACCOUNT_ASSETS, ACCOUNT_LIABILITIES = 50, 51, 52, 53
ACCOUNT_COMMISSION_BLOCKED = 54


def AccountInfoDouble(prop):
    return {ACCOUNT_BALANCE: 10000.0, ACCOUNT_EQUITY: 10000.0, ACCOUNT_MARGIN_FREE: 10000.0,
            ACCOUNT_MARGIN_LEVEL: 0.0}.get(int(prop), 0.0)


def AccountInfoInteger(prop):
    return {ACCOUNT_LEVERAGE: 100, ACCOUNT_LOGIN: 0, ACCOUNT_TRADE_ALLOWED: 1,
            ACCOUNT_TRADE_EXPERT: 1, ACCOUNT_CURRENCY_DIGITS: 2}.get(int(prop), 0)


def AccountInfoString(prop):
    return {ACCOUNT_CURRENCY: "USD", ACCOUNT_NAME: "Backtester", ACCOUNT_SERVER: "Backtester",
            ACCOUNT_COMPANY: "Backtester"}.get(int(prop), "")


def AccountBalance():
    return 10000.0


def AccountEquity():
    return 10000.0


def AccountFreeMargin():
    return 10000.0


# trading: indicators cannot trade
def PositionsTotal():
    return 0


def OrdersTotal():
    return 0


def HistoryDealsTotal():
    return 0


def HistoryOrdersTotal():
    return 0


def HistorySelect(*a):
    return True


def HistorySelectByPosition(*a):
    return True


def PositionSelect(*a):
    return False


def PositionSelectByTicket(*a):
    return False


def PositionGetSymbol(i):
    return ""


def PositionGetTicket(i):
    return 0


def PositionGetDouble(prop, ref=None):
    if ref is not None:
        ref.v = 0.0
        return False
    return 0.0


def PositionGetInteger(prop, ref=None):
    if ref is not None:
        ref.v = 0
        return False
    return 0


def PositionGetString(prop, ref=None):
    if ref is not None:
        ref.v = ""
        return False
    return ""


def OrderGetTicket(i):
    return 0


def OrderSelect(*a):
    return False


def OrderGetDouble(prop, ref=None):
    return 0.0


def OrderGetInteger(prop, ref=None):
    return 0


def OrderGetString(prop, ref=None):
    return ""


def HistoryDealGetTicket(i):
    return 0


def HistoryDealGetDouble(t, prop, ref=None):
    return 0.0


def HistoryDealGetInteger(t, prop, ref=None):
    return 0


def HistoryDealGetString(t, prop, ref=None):
    return ""


def HistoryOrderGetTicket(i):
    return 0


def HistoryOrderGetDouble(t, prop, ref=None):
    return 0.0


def HistoryOrderGetInteger(t, prop, ref=None):
    return 0


def HistoryOrderGetString(t, prop, ref=None):
    return ""


def OrderSend(request, result):
    _set_error(4756)
    return False


def OrderCheck(request, result):
    return False


def OrderCalcMargin(*a):
    return False


def OrderCalcProfit(*a):
    return False


# ------------------------------------------------------------------ terminal / program info

MQL_PROGRAM_TYPE, MQL_DLLS_ALLOWED, MQL_TRADE_ALLOWED, MQL_DEBUG, MQL_PROFILER = 2, 3, 4, 5, 10
MQL_TESTER, MQL_OPTIMIZATION, MQL_VISUAL_MODE, MQL_FRAME_MODE, MQL_LICENSE_TYPE = 6, 7, 8, 12, 9
MQL_PROGRAM_NAME, MQL_PROGRAM_PATH, MQL_MEMORY_LIMIT, MQL_MEMORY_USED, MQL_SIGNALS_ALLOWED = 0, 1, 23, 24, 14
MQL_FORWARD, MQL_HANDLES_USED = 16, 17
PROGRAM_SCRIPT, PROGRAM_EXPERT, PROGRAM_INDICATOR, PROGRAM_SERVICE = 1, 2, 3, 5


def MQLInfoInteger(prop):
    return {MQL_PROGRAM_TYPE: PROGRAM_INDICATOR, MQL_DLLS_ALLOWED: 0, MQL_TRADE_ALLOWED: 0,
            MQL_MEMORY_LIMIT: 4096}.get(int(prop), 0)


def MQLInfoString(prop):
    c = ctx()
    if int(prop) == MQL_PROGRAM_NAME:
        return c.name
    if int(prop) == MQL_PROGRAM_PATH:
        return "MQL5\\Indicators\\" + c.name + ".ex5"
    return ""


MQL5InfoInteger = MQLInfoInteger
MQL5InfoString = MQLInfoString

TERMINAL_BUILD, TERMINAL_CONNECTED, TERMINAL_DLLS_ALLOWED, TERMINAL_TRADE_ALLOWED = 5, 6, 7, 8
TERMINAL_EMAIL_ENABLED, TERMINAL_FTP_ENABLED, TERMINAL_MAXBARS, TERMINAL_CODEPAGE = 9, 10, 11, 12
TERMINAL_CPU_CORES, TERMINAL_MEMORY_PHYSICAL, TERMINAL_MEMORY_TOTAL, TERMINAL_MEMORY_AVAILABLE = 21, 14, 15, 16
TERMINAL_MEMORY_USED, TERMINAL_DISK_SPACE, TERMINAL_SCREEN_DPI, TERMINAL_PING_LAST = 17, 20, 27, 28
TERMINAL_COMMUNITY_ACCOUNT, TERMINAL_COMMUNITY_CONNECTION, TERMINAL_NOTIFICATIONS_ENABLED = 23, 24, 26
TERMINAL_MQID, TERMINAL_SCREEN_WIDTH, TERMINAL_SCREEN_HEIGHT, TERMINAL_X64 = 22, 30, 31, 32
TERMINAL_LANGUAGE, TERMINAL_COMPANY, TERMINAL_NAME, TERMINAL_PATH = 13, 0, 1, 2
TERMINAL_DATA_PATH, TERMINAL_COMMONDATA_PATH = 3, 4
TERMINAL_KEYSTATE_LEFT, TERMINAL_KEYSTATE_UP, TERMINAL_KEYSTATE_RIGHT, TERMINAL_KEYSTATE_DOWN = 1000, 1001, 1002, 1003
TERMINAL_KEYSTATE_SHIFT, TERMINAL_KEYSTATE_CONTROL, TERMINAL_KEYSTATE_MENU = 1004, 1005, 1006
TERMINAL_KEYSTATE_CAPSLOCK, TERMINAL_KEYSTATE_NUMLOCK, TERMINAL_KEYSTATE_SCRLOCK = 1007, 1008, 1009
TERMINAL_KEYSTATE_ENTER, TERMINAL_KEYSTATE_INSERT, TERMINAL_KEYSTATE_DELETE = 1010, 1011, 1012
TERMINAL_KEYSTATE_HOME, TERMINAL_KEYSTATE_END, TERMINAL_KEYSTATE_TAB = 1013, 1014, 1015
TERMINAL_KEYSTATE_PAGEUP, TERMINAL_KEYSTATE_PAGEDOWN, TERMINAL_KEYSTATE_ESCAPE = 1016, 1017, 1018


def TerminalInfoInteger(prop):
    return {TERMINAL_BUILD: 4620, TERMINAL_CONNECTED: 1, TERMINAL_MAXBARS: 100000,
            TERMINAL_CODEPAGE: 0, TERMINAL_CPU_CORES: 4, TERMINAL_SCREEN_DPI: 96,
            TERMINAL_SCREEN_WIDTH: 1920, TERMINAL_SCREEN_HEIGHT: 1080, TERMINAL_X64: 1}.get(int(prop), 0)


def TerminalInfoString(prop):
    return {TERMINAL_LANGUAGE: "English", TERMINAL_COMPANY: "MetaQuotes Ltd.",
            TERMINAL_NAME: "MetaTrader 5", TERMINAL_PATH: "C:\\MT5",
            TERMINAL_DATA_PATH: "C:\\MT5", TERMINAL_COMMONDATA_PATH: "C:\\MT5\\Common"}.get(int(prop), "")


def TerminalInfoDouble(prop):
    return 0.0


# ------------------------------------------------------------------ indicator properties

INDICATOR_DATA, INDICATOR_COLOR_INDEX, INDICATOR_CALCULATIONS = 0, 1, 2
INDICATOR_DIGITS, INDICATOR_HEIGHT, INDICATOR_LEVELS, INDICATOR_LEVELCOLOR = 0, 1, 2, 3
INDICATOR_LEVELSTYLE, INDICATOR_LEVELWIDTH, INDICATOR_FIXED_MINIMUM, INDICATOR_FIXED_MAXIMUM = 4, 5, 6, 7
INDICATOR_MINIMUM, INDICATOR_MAXIMUM, INDICATOR_LEVELVALUE = 0, 1, 2
INDICATOR_SHORTNAME, INDICATOR_LEVELTEXT = 0, 1
PLOT_ARROW, PLOT_ARROW_SHIFT, PLOT_DRAW_BEGIN, PLOT_DRAW_TYPE, PLOT_SHOW_DATA = 0, 1, 2, 3, 4
PLOT_SHIFT, PLOT_LINE_STYLE, PLOT_LINE_WIDTH, PLOT_COLOR_INDEXES, PLOT_LINE_COLOR = 5, 6, 7, 8, 9
PLOT_EMPTY_VALUE = 0
PLOT_LABEL = 0

DRAW_NONE, DRAW_LINE, DRAW_SECTION, DRAW_HISTOGRAM, DRAW_HISTOGRAM2, DRAW_ARROW = 0, 1, 2, 3, 4, 5
DRAW_ZIGZAG, DRAW_FILLING, DRAW_COLOR_LINE, DRAW_COLOR_SECTION, DRAW_COLOR_HISTOGRAM = 6, 7, 8, 9, 10
DRAW_COLOR_HISTOGRAM2, DRAW_COLOR_ARROW, DRAW_COLOR_ZIGZAG, DRAW_BARS, DRAW_CANDLES = 11, 12, 13, 14, 15
DRAW_COLOR_BARS, DRAW_COLOR_CANDLES = 16, 17

STYLE_SOLID, STYLE_DASH, STYLE_DOT, STYLE_DASHDOT, STYLE_DASHDOTDOT = 0, 1, 2, 3, 4


def SetIndexBuffer(index, arr, data_type=INDICATOR_DATA):
    c = ctx()
    if not isinstance(arr, Arr):
        return False
    arr.buffer = True
    arr.dyn = True
    c.buffers[int(index)] = (arr, int(data_type))
    if c.rates_total and len(arr.a) != c.rates_total:
        arr.a = [0.0] * c.rates_total
    return True


def _pp(plot):
    c = ctx()
    return c.plot_props.setdefault(int(plot), {})


def PlotIndexSetInteger(plot, prop, a, b=None):
    d = _pp(plot)
    if b is None:
        d[("i", int(prop))] = a
    else:
        d[("i", int(prop), int(a))] = b
    return True


def PlotIndexSetDouble(plot, prop, value):
    _pp(plot)[("d", int(prop))] = value
    return True


def PlotIndexSetString(plot, prop, value):
    _pp(plot)[("s", int(prop))] = value
    return True


def PlotIndexGetInteger(plot, prop, modifier=None):
    d = _pp(plot)
    if modifier is not None and ("i", int(prop), int(modifier)) in d:
        return d[("i", int(prop), int(modifier))]
    v = d.get(("i", int(prop)))
    if v is None:
        v = ctx().ind_props.get(("plot_default", int(plot), int(prop)), 0)
    return v


def IndicatorSetInteger(prop, a, b=None):
    c = ctx()
    if b is None:
        c.ind_props[("i", int(prop))] = a
    else:
        c.ind_props[("i", int(prop), int(a))] = b
    return True


def IndicatorSetDouble(prop, a, b=None):
    c = ctx()
    if b is None:
        c.ind_props[("d", int(prop))] = a
    else:
        c.ind_props[("d", int(prop), int(a))] = b
    return True


def IndicatorSetString(prop, a, b=None):
    c = ctx()
    if b is None:
        c.ind_props[("s", int(prop))] = a
    else:
        c.ind_props[("s", int(prop), int(a))] = b
    return True


def IndicatorDigits(d):
    return IndicatorSetInteger(INDICATOR_DIGITS, d)


def IndicatorShortName(name):
    return IndicatorSetString(INDICATOR_SHORTNAME, name)


# ------------------------------------------------------------------ handles

class Handle:
    def __init__(self, kind, symbol, tf, args, runner):
        self.kind = kind
        self.symbol = symbol
        self.tf = tf
        self.args = args
        self.runner = runner      # callable(handle) -> (dict buffer->list, nbars)
        self._data = None
        self.error = None

    def data(self):
        if self._data is None:
            try:
                self._data = self.runner(self)
            except MqlRuntimeError as e:
                self.error = str(e)
                self._data = ({}, 0)
        return self._data


def _register(h: Handle) -> int:
    c = ctx()
    c.handles.append(h)
    return 10 + len(c.handles) - 1


def _handle(hid) -> Handle | None:
    try:
        hid = int(hid)
    except (TypeError, ValueError):
        return None
    c = ctx()
    k = hid - 10
    if 0 <= k < len(c.handles):
        return c.handles[k]
    return None


def IndicatorRelease(hid):
    return _handle(hid) is not None


def BarsCalculated(hid):
    h = _handle(hid)
    if h is None:
        return -1
    bufs, n = h.data()
    return n if bufs or n else -1


def CopyBuffer(hid, buffer_num, a, b, dst):
    h = _handle(hid)
    if h is None:
        _set_error(4807)
        return -1
    bufs, n = h.data()
    vals = bufs.get(int(buffer_num))
    if vals is None:
        return -1
    s = ctx().market.series(h.symbol, h.tf)
    if s is None:
        return -1
    lo, hi = _copy_range(s, a, b)
    hi = min(hi, len(vals))
    if hi <= lo:
        return -1
    return _copy_into(dst, list(vals[lo:hi]))


def IndicatorParameters(hid, type_ref, params):
    return 0


def ChartIndicatorAdd(chart, sub, hid):
    return True


def ChartIndicatorDelete(chart, sub, name):
    return True


def ChartIndicatorGet(chart, sub, name):
    return INVALID_HANDLE


def ChartIndicatorName(chart, sub, index):
    return ""


def ChartIndicatorsTotal(chart, sub):
    return 0


# ------------------------------------------------------------------ objects / chart

def _obj_store():
    return ctx().objects


OBJPROP_TIME, OBJPROP_PRICE = 0, 1


def ObjectCreate(chart_id, name, type, sub_window=0, *coords):
    c = ctx()
    if name in c.objects:
        return False
    times, prices = {}, {}
    for k in range(0, len(coords) - 1, 2):
        times[k // 2] = coords[k]
        prices[k // 2] = coords[k + 1]
    c.objects[name] = {"type": type, "sub": sub_window, "i": {}, "d": {}, "s": {},
                       "time": times, "price": prices}
    c.object_order.append(name)
    return True


def ObjectDelete(chart_id, name):
    c = ctx()
    if name in c.objects:
        del c.objects[name]
        c.object_order.remove(name)
        return True
    return False


def ObjectsDeleteAll(chart_id=0, a=None, b=-1, c_=-1):
    c = ctx()
    if isinstance(a, str):
        names = [n for n in c.object_order if n.startswith(a)]
    else:
        names = list(c.object_order)
    for n in names:
        ObjectDelete(chart_id, n)
    return len(names)


def ObjectFind(chart_id, name):
    o = ctx().objects.get(name)
    return o["sub"] if o is not None else -1


def ObjectsTotal(chart_id=0, sub=-1, type=-1):
    return len(ctx().objects)


def ObjectName(chart_id, pos, sub=-1, type=-1):
    names = ctx().object_order
    return names[pos] if 0 <= pos < len(names) else ""


def ObjectMove(chart_id, name, point, time, price):
    o = ctx().objects.get(name)
    if o is None:
        return False
    o["time"][int(point)] = time
    o["price"][int(point)] = price
    return True


def _obj_set(kind, chart_id, name, prop, a, b=None):
    o = ctx().objects.get(name)
    if o is None:
        return False
    mod, val = (0, a) if b is None else (a, b)
    if kind == "d" and int(prop) == OBJPROP_PRICE:
        o["price"][int(mod)] = val
    elif kind == "i" and int(prop) == OBJPROP_TIME:
        o["time"][int(mod)] = val
    else:
        o[kind][(int(prop), int(mod))] = val
    return True


def ObjectSetInteger(chart_id, name, prop, a, b=None):
    return _obj_set("i", chart_id, name, prop, a, b)


def ObjectSetDouble(chart_id, name, prop, a, b=None):
    return _obj_set("d", chart_id, name, prop, a, b)


def ObjectSetString(chart_id, name, prop, a, b=None):
    return _obj_set("s", chart_id, name, prop, a, b)


def _obj_get(kind, chart_id, name, prop, mod=0, ref=None, default=0):
    o = ctx().objects.get(name)
    if o is None:
        val = default
        ok = False
    else:
        ok = True
        if kind == "d" and int(prop) == OBJPROP_PRICE:
            val = o["price"].get(int(mod), default)
        elif kind == "i" and int(prop) == OBJPROP_TIME:
            val = o["time"].get(int(mod), default)
        elif kind == "i" and int(prop) == 27:   # OBJPROP_TYPE
            val = o["type"]
        else:
            val = o[kind].get((int(prop), int(mod)), default)
    if ref is not None:
        ref.v = val
        return ok
    return val


def ObjectGetInteger(chart_id, name, prop, mod=0, ref=None):
    return _obj_get("i", chart_id, name, prop, mod, ref, 0)


def ObjectGetDouble(chart_id, name, prop, mod=0, ref=None):
    return _obj_get("d", chart_id, name, prop, mod, ref, 0.0)


def ObjectGetString(chart_id, name, prop, mod=0, ref=None):
    return _obj_get("s", chart_id, name, prop, mod, ref, "")


def ObjectGetValueByTime(chart_id, name, time, line_id=0):
    o = ctx().objects.get(name)
    if o is None:
        return 0.0
    t0, t1 = o["time"].get(0, 0), o["time"].get(1, 0)
    p0, p1 = o["price"].get(0, 0.0), o["price"].get(1, 0.0)
    if t1 == t0:
        return p0
    return p0 + (p1 - p0) * (time - t0) / (t1 - t0)


def ObjectGetTimeByValue(chart_id, name, value, line_id=0):
    o = ctx().objects.get(name)
    if o is None:
        return 0
    t0, t1 = o["time"].get(0, 0), o["time"].get(1, 0)
    p0, p1 = o["price"].get(0, 0.0), o["price"].get(1, 0.0)
    if p1 == p0:
        return t0
    return int(t0 + (t1 - t0) * (value - p0) / (p1 - p0))


def ObjectSetText(name, text, *a):
    return ObjectSetString(0, name, 999, text)


def ObjectDescription(name):
    return ObjectGetString(0, name, 999)


CHART_VISIBLE_BARS, CHART_FIRST_VISIBLE_BAR, CHART_WIDTH_IN_BARS, CHART_WIDTH_IN_PIXELS = 100, 104, 105, 106
CHART_HEIGHT_IN_PIXELS, CHART_PRICE_MIN, CHART_PRICE_MAX, CHART_SCALE, CHART_WINDOWS_TOTAL = 107, 108, 109, 5, 103


def ChartID():
    return 0


def ChartGetInteger(chart_id, prop, sub=0, ref=None):
    s = ctx().series
    n = s.n if s else 0
    vals = {CHART_VISIBLE_BARS: min(n, 100), CHART_FIRST_VISIBLE_BAR: min(n, 100) - 1,
            CHART_WIDTH_IN_BARS: 100, CHART_WIDTH_IN_PIXELS: 1200, CHART_HEIGHT_IN_PIXELS: 500,
            CHART_SCALE: 2, CHART_WINDOWS_TOTAL: 2}
    v = vals.get(int(prop), 0)
    if ref is not None:
        ref.v = v
        return True
    return v


def ChartGetDouble(chart_id, prop, sub=0, ref=None):
    s = ctx().series
    v = 0.0
    if s is not None and s.n:
        if int(prop) == CHART_PRICE_MAX:
            v = max(s.high[-100:])
        elif int(prop) == CHART_PRICE_MIN:
            v = min(s.low[-100:])
    if ref is not None:
        ref.v = v
        return True
    return v


def ChartGetString(chart_id, prop, ref=None):
    if ref is not None:
        ref.v = ""
        return True
    return ""


def ChartSetInteger(*a):
    return True


def ChartSetDouble(*a):
    return True


def ChartSetString(*a):
    return True


def ChartRedraw(chart_id=0):
    pass


def ChartWindowFind(*a):
    return 0


def ChartNavigate(*a):
    return True


def ChartFirst():
    return 0


def ChartNext(chart_id):
    return -1


def ChartOpen(*a):
    return 0


def ChartClose(*a):
    return True


def ChartSetSymbolPeriod(*a):
    return True


def ChartApplyTemplate(*a):
    return False


def ChartSaveTemplate(*a):
    return False


def ChartScreenShot(*a):
    return False


def ChartTimePriceToXY(chart_id, sub, time, price, x, y):
    x.v = 0
    y.v = 0
    return True


def ChartXYToTimePrice(chart_id, x, y, sub, time, price):
    sub.v = 0
    time.v = TimeCurrent()
    price.v = 0.0
    return True


def WindowRedraw():
    pass


def WindowFind(name):
    return 0


def EventSetTimer(sec):
    return True


def EventSetMillisecondTimer(ms):
    return True


def EventKillTimer():
    pass


def EventChartCustom(*a):
    return True


def PlaySound(*a):
    return True


def SendMail(*a):
    return True


def SendNotification(*a):
    return True


def SendFTP(*a):
    return True


def MessageBox(*a):
    return 1


def ResourceCreate(*a):
    return False


def ResourceFree(*a):
    return True


def ResourceReadImage(*a):
    return False


def ResourceSave(*a):
    return False


def TextSetFont(*a):
    return True


def TextOut(*a):
    return True


def TextGetSize(text, w, h):
    w.v = 7 * len(text)
    h.v = 12
    return True


# ------------------------------------------------------------------ global variables

_GLOBALS: dict[str, tuple[float, int]] = {}


def GlobalVariableSet(name, value):
    _GLOBALS[name] = (float(value), TimeCurrent())
    return TimeCurrent()


def GlobalVariableGet(name, ref=None):
    v = _GLOBALS.get(name, (0.0, 0))[0]
    if ref is not None:
        ref.v = v
        return name in _GLOBALS
    return v


def GlobalVariableCheck(name):
    return name in _GLOBALS


def GlobalVariableDel(name):
    return _GLOBALS.pop(name, None) is not None


def GlobalVariableTime(name):
    return _GLOBALS.get(name, (0.0, 0))[1]


def GlobalVariablesTotal():
    return len(_GLOBALS)


def GlobalVariableName(i):
    names = list(_GLOBALS)
    return names[i] if 0 <= i < len(names) else ""


def GlobalVariablesDeleteAll(prefix="", limit=0):
    names = [n for n in _GLOBALS if n.startswith(prefix or "")]
    for n in names:
        del _GLOBALS[n]
    return len(names)


def GlobalVariableTemp(name):
    return True


def GlobalVariableSetOnCondition(name, value, check):
    if _GLOBALS.get(name, (None,))[0] == check:
        GlobalVariableSet(name, value)
        return True
    return False


def GlobalVariablesFlush():
    pass


# ------------------------------------------------------------------ files (no file system for indicators)

def FileOpen(*a):
    return INVALID_HANDLE


def FileClose(h):
    pass


def FileIsExist(*a):
    return False


def FileDelete(*a):
    return False


def FileWrite(*a):
    return 0


def FileWriteString(*a):
    return 0


def FileWriteDouble(*a):
    return 0


def FileWriteInteger(*a):
    return 0


def FileWriteArray(*a):
    return 0


def FileReadString(*a):
    return ""


def FileReadNumber(*a):
    return 0.0


def FileReadDouble(*a):
    return 0.0


def FileReadInteger(*a):
    return 0


def FileReadArray(*a):
    return 0


def FileReadBool(*a):
    return False


def FileReadDatetime(*a):
    return 0


def FileIsEnding(*a):
    return True


def FileIsLineEnding(*a):
    return True


def FileSize(*a):
    return 0


def FileSeek(*a):
    return False


def FileTell(*a):
    return 0


def FileFlush(*a):
    pass


def FileFindFirst(*a):
    return INVALID_HANDLE


def FileFindNext(*a):
    return False


def FileFindClose(*a):
    pass


def FolderCreate(*a):
    return False


def FileCopy(*a):
    return False


def FileMove(*a):
    return False


def FileLoad(*a):
    return -1


def FileSave(*a):
    return False


def WebRequest(*a):
    return -1
