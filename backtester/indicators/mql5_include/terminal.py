"""A small stand-in for the MetaTrader terminal's data functions, for the
include libraries (and converted indicators) that read bars by symbol and
timeframe instead of through ``OnCalculate``'s arrays.

MQL5 code calls ``CopyClose(symbol, timeframe, start_pos, count, arr)``,
``iClose(symbol, timeframe, shift)``, ``SymbolInfoDouble(symbol, SYMBOL_POINT)``
and so on. Here a :class:`Rates` object wraps one bar DataFrame (this app's
``time, open, high, low, close, tick_volume, spread, real_volume`` frame) and
answers those calls for *its* symbol/timeframe. A :class:`Terminal` holds
several of them so multi-symbol / multi-timeframe code can be ported; asking
for a symbol or timeframe it does not have fails the way MQL5 does (the
``Copy*`` functions return -1) rather than inventing data.

Indexing follows MQL5: ``shift``/``start_pos`` count back from the newest
bar (0 = newest).
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass

import numpy as np
import pandas as pd

# ENUM_TIMEFRAMES
PERIOD_CURRENT = 0
PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6 = 1, 2, 3, 4, 5, 6
PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30 = 10, 12, 15, 20, 30
PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4 = 16385, 16386, 16387, 16388
PERIOD_H6, PERIOD_H8, PERIOD_H12 = 16390, 16392, 16396
PERIOD_D1, PERIOD_W1, PERIOD_MN1 = 16408, 32769, 49153

PERIOD_SECONDS = {
    PERIOD_M1: 60, PERIOD_M2: 120, PERIOD_M3: 180, PERIOD_M4: 240, PERIOD_M5: 300,
    PERIOD_M6: 360, PERIOD_M10: 600, PERIOD_M12: 720, PERIOD_M15: 900, PERIOD_M20: 1200,
    PERIOD_M30: 1800, PERIOD_H1: 3600, PERIOD_H2: 7200, PERIOD_H3: 10800, PERIOD_H4: 14400,
    PERIOD_H6: 21600, PERIOD_H8: 28800, PERIOD_H12: 43200, PERIOD_D1: 86400,
    PERIOD_W1: 604800, PERIOD_MN1: 2592000,
}
PERIOD_NAMES = {
    PERIOD_M1: "M1", PERIOD_M2: "M2", PERIOD_M3: "M3", PERIOD_M4: "M4", PERIOD_M5: "M5",
    PERIOD_M6: "M6", PERIOD_M10: "M10", PERIOD_M12: "M12", PERIOD_M15: "M15",
    PERIOD_M20: "M20", PERIOD_M30: "M30", PERIOD_H1: "H1", PERIOD_H2: "H2", PERIOD_H3: "H3",
    PERIOD_H4: "H4", PERIOD_H6: "H6", PERIOD_H8: "H8", PERIOD_H12: "H12", PERIOD_D1: "D1",
    PERIOD_W1: "W1", PERIOD_MN1: "MN1",
}
PERIOD_BY_NAME = {v: k for k, v in PERIOD_NAMES.items()}

# ENUM_SYMBOL_INFO_* subset that has meaning offline
SYMBOL_POINT = "point"
SYMBOL_DIGITS = "digits"
SYMBOL_TRADE_CONTRACT_SIZE = "contract_size"
SYMBOL_TRADE_TICK_SIZE = "tick_size"
SYMBOL_SPREAD = "spread"
SYMBOL_BID = "bid"
SYMBOL_ASK = "ask"
SYMBOL_LASTHIGH = "last_high"
SYMBOL_LASTLOW = "last_low"
SYMBOL_TIME = "time"


def PeriodSeconds(period: int) -> int:
    return PERIOD_SECONDS.get(int(period), 0)


def PeriodInStr(period: int) -> str:
    """``mymql_v201.mqh``'s period name (``"NOPERIOD"`` when unknown)."""
    return PERIOD_NAMES.get(int(period), "NOPERIOD")


def to_datetime_int(value) -> int:
    """A timestamp (``numpy.datetime64``/``pd.Timestamp``) → MQL5 ``datetime``
    (whole seconds since 1970-01-01, server time, no time zone)."""
    return int(pd.Timestamp(value).value // 1_000_000_000)


@dataclass
class MqlDateTime:
    year: int
    mon: int
    day: int
    hour: int
    min: int
    sec: int
    day_of_week: int      # 0 = Sunday
    day_of_year: int      # 0 = 1 January


def TimeToStruct(t: int) -> MqlDateTime:
    d = _dt.datetime(1970, 1, 1) + _dt.timedelta(seconds=int(t))
    return MqlDateTime(d.year, d.month, d.day, d.hour, d.minute, d.second,
                       (d.weekday() + 1) % 7, d.timetuple().tm_yday - 1)


def StructToTime(s: MqlDateTime) -> int:
    d = _dt.datetime(s.year, s.mon, s.day, s.hour, s.min, s.sec)
    return int((d - _dt.datetime(1970, 1, 1)).total_seconds())


class Rates:
    """One symbol/timeframe of bars, queried MQL5-style (0 = newest)."""

    def __init__(self, df: pd.DataFrame, symbol: str = "", period: int = PERIOD_CURRENT,
                 **spec):
        self.df = df
        self.symbol = symbol
        self.period = period
        self.time = np.array([to_datetime_int(t) for t in df["time"]], dtype=np.int64) \
            if "time" in df.columns else np.arange(len(df), dtype=np.int64)
        self.open = df["open"].to_numpy(dtype=float)
        self.high = df["high"].to_numpy(dtype=float)
        self.low = df["low"].to_numpy(dtype=float)
        self.close = df["close"].to_numpy(dtype=float)
        n = len(df)
        self.tick_volume = (df["tick_volume"].to_numpy(dtype=np.int64)
                            if "tick_volume" in df.columns else np.zeros(n, dtype=np.int64))
        self.real_volume = (df["real_volume"].to_numpy(dtype=np.int64)
                            if "real_volume" in df.columns else np.zeros(n, dtype=np.int64))
        self.spread = (df["spread"].to_numpy(dtype=np.int64)
                       if "spread" in df.columns else np.zeros(n, dtype=np.int64))
        self.spec = dict(spec)
        if "point" not in self.spec and df.attrs.get("point"):
            self.spec["point"] = float(df.attrs["point"])
        if "digits" not in self.spec and df.attrs.get("digits") is not None:
            self.spec["digits"] = int(df.attrs["digits"])

    def __len__(self) -> int:
        return len(self.close)

    # ------------------------------------------------------------ Copy*

    def _copy(self, arr: np.ndarray, start_pos: int, count: int) -> np.ndarray | None:
        """``CopyXxx(symbol, tf, start_pos, count, out)`` → the slice in
        *forward* (oldest-first) order, as MQL5 fills a non-series array;
        ``None`` where MQL5 returns -1."""
        n = len(arr)
        start_pos, count = int(start_pos), int(count)
        if start_pos < 0 or count <= 0 or start_pos >= n:
            return None
        hi = n - start_pos
        lo = max(0, hi - count)
        return arr[lo:hi].copy()

    def CopyOpen(self, start_pos, count):
        return self._copy(self.open, start_pos, count)

    def CopyHigh(self, start_pos, count):
        return self._copy(self.high, start_pos, count)

    def CopyLow(self, start_pos, count):
        return self._copy(self.low, start_pos, count)

    def CopyClose(self, start_pos, count):
        return self._copy(self.close, start_pos, count)

    def CopyTime(self, start_pos, count):
        return self._copy(self.time, start_pos, count)

    def CopyTickVolume(self, start_pos, count):
        return self._copy(self.tick_volume, start_pos, count)

    def CopyRealVolume(self, start_pos, count):
        return self._copy(self.real_volume, start_pos, count)

    def CopySpread(self, start_pos, count):
        return self._copy(self.spread, start_pos, count)

    # ----------------------------------------------------------- iXxx

    def _at(self, arr, shift):
        i = len(arr) - 1 - int(shift)
        return arr[i] if 0 <= i < len(arr) else None

    def iOpen(self, shift):
        v = self._at(self.open, shift)
        return 0.0 if v is None else float(v)

    def iHigh(self, shift):
        v = self._at(self.high, shift)
        return 0.0 if v is None else float(v)

    def iLow(self, shift):
        v = self._at(self.low, shift)
        return 0.0 if v is None else float(v)

    def iClose(self, shift):
        v = self._at(self.close, shift)
        return 0.0 if v is None else float(v)

    def iTime(self, shift):
        v = self._at(self.time, shift)
        return 0 if v is None else int(v)

    def iVolume(self, shift):
        v = self._at(self.tick_volume, shift)
        return 0 if v is None else int(v)

    def Bars(self, start_time=None, stop_time=None) -> int:
        if start_time is None:
            return len(self)
        lo, hi = sorted((int(start_time), int(stop_time)))
        return int(np.count_nonzero((self.time >= lo) & (self.time <= hi)))

    def iBarShift(self, time, exact: bool = False) -> int:
        """Shift of the bar containing ``time`` (MQL5: the last bar opened at
        or before it); -1 when ``exact`` and no bar opens exactly then."""
        t = int(time)
        i = int(np.searchsorted(self.time, t, side="right")) - 1
        if i < 0:
            return -1
        if exact and self.time[i] != t:
            return -1
        return len(self) - 1 - i

    def iHighest(self, series: str = "high", count: int = -1, start: int = 0) -> int:
        """MQL5 ``iHighest``: shift of the highest value in ``count`` bars from
        ``start`` (first found from ``start`` going back)."""
        arr = getattr(self, series)
        n = len(arr)
        if count <= 0:
            count = n - start
        best = -1
        for shift in range(start, min(start + count, n)):
            if best < 0 or arr[n - 1 - shift] > arr[n - 1 - best]:
                best = shift
        return best

    def iLowest(self, series: str = "low", count: int = -1, start: int = 0) -> int:
        arr = getattr(self, series)
        n = len(arr)
        if count <= 0:
            count = n - start
        best = -1
        for shift in range(start, min(start + count, n)):
            if best < 0 or arr[n - 1 - shift] < arr[n - 1 - best]:
                best = shift
        return best

    # ------------------------------------------------------- symbol info

    def SymbolInfoDouble(self, prop) -> float:
        if prop == SYMBOL_POINT:
            if "point" in self.spec:
                return float(self.spec["point"])
            return 10.0 ** -self.SymbolInfoInteger(SYMBOL_DIGITS)
        if prop == SYMBOL_TRADE_TICK_SIZE:
            return float(self.spec.get("tick_size", self.SymbolInfoDouble(SYMBOL_POINT)))
        if prop == SYMBOL_TRADE_CONTRACT_SIZE:
            return float(self.spec.get("contract_size", 0.0))
        if prop in (SYMBOL_BID, SYMBOL_ASK):
            # Offline, the latest bar's close stands in for the current quote.
            return float(self.close[-1]) if len(self) else 0.0
        if prop == SYMBOL_LASTHIGH:
            return float(self.high[-1]) if len(self) else 0.0
        if prop == SYMBOL_LASTLOW:
            return float(self.low[-1]) if len(self) else 0.0
        return float(self.spec.get(prop, 0.0))

    def SymbolInfoInteger(self, prop) -> int:
        if prop == SYMBOL_DIGITS:
            if "digits" in self.spec:
                return int(self.spec["digits"])
            from backtester.indicators import mql5
            return mql5.digits(self.df)
        if prop == SYMBOL_SPREAD:
            return int(self.spread[-1]) if len(self) else 0
        if prop == SYMBOL_TIME:
            return int(self.time[-1]) if len(self) else 0
        return int(self.spec.get(prop, 0))


class Terminal:
    """Several :class:`Rates`, looked up by (symbol, period) the way MQL5
    code asks for them. ``symbol=None``/``""`` and ``PERIOD_CURRENT`` resolve
    to the chart's own series (the first one added)."""

    def __init__(self, chart: Rates | None = None):
        self._rates: dict[tuple[str, int], Rates] = {}
        self.chart = chart
        if chart is not None:
            self.add(chart)

    def add(self, rates: Rates) -> None:
        self._rates[(rates.symbol, int(rates.period))] = rates
        if self.chart is None:
            self.chart = rates

    def get(self, symbol=None, period=PERIOD_CURRENT) -> Rates | None:
        if self.chart is None:
            return None
        sym = self.chart.symbol if not symbol else symbol
        per = self.chart.period if int(period) == PERIOD_CURRENT else int(period)
        return self._rates.get((sym, per))


# -------------------------------------------------------- the "current" one
#
# MQL5 code reaches the terminal through free functions (``iClose(symbol, tf,
# shift)``), so ports that keep those signatures need an ambient terminal.
# A converted indicator sets it at the top of ``calculate``:
#
#     terminal.set_current(Terminal(Rates(df, symbol, PERIOD_H1)))

_CURRENT: Terminal | None = None


def set_current(term: Terminal | None) -> None:
    global _CURRENT
    _CURRENT = term


def current() -> Terminal:
    if _CURRENT is None:
        raise RuntimeError("No terminal data set: call terminal.set_current(Terminal(Rates(df)))")
    return _CURRENT


def rates_for(symbol=None, period=PERIOD_CURRENT) -> Rates | None:
    return current().get(symbol, period)
