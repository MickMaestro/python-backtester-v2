"""MQL4-compatibility includes — ports of:

- ``Define.mqh`` (MQL4 constants), ``Enum.mqh`` (``TFMigrate``),
- ``functions.mqh`` and the identical ``FxWeirdos/functionsMQL4.mqh``
  (MetaQuotes' "MQL4 functions in MQL5" migration helpers),
- ``MT4Bridge/MT4Mode.mqh``, ``MT4Bridge/MT4MarketInfo.mqh``,
  ``MT4Bridge/MT4Time.mqh``,
- ``DateTime.mqh`` and the identical ``MQL5Book/DateTime.mqh``
  (``TimeYear(T)``-style accessors),
- the data/array helpers of ``mymql_v201.mqh`` (``iTime/iOpen/…``,
  ``PeriodInStr``, ``iMAOnArray``).

Bar data comes from the ambient :mod:`.terminal` (``terminal.set_current``),
standing in for the symbol/timeframe the MQL code names. Functions that only
create, find or style chart objects or plot properties (``ObjectCreateMQL4``,
``SetIndexStyleMQL4``, …) are kept as no-ops so a line-by-line port still
runs; the app draws an indicator from its returned series, not from chart
objects.

Faithfully reproduced source bugs:

- ``iHighestMQL4``/``iLowestMQL4`` with ``type == MODE_LOW`` both use
  ``ArrayMaximum``/``ArrayMinimum`` on the *lows* the same way as the other
  types — i.e. ``iHighestMQL4(MODE_LOW)`` returns the highest low.
- ``SetIndexStyleMQL4``'s ``switch`` statements have no ``break``s (they fall
  through to the default) — harmless here since it is a no-op.
"""

from __future__ import annotations

import math

import numpy as np

from . import terminal as T
from .mql_runtime import EMPTY_VALUE, MODE_EMA, MODE_LWMA, MODE_SMA, MODE_SMMA, \
    PRICE_CLOSE, PRICE_HIGH, PRICE_LOW, PRICE_MEDIAN, PRICE_OPEN, PRICE_TYPICAL, PRICE_WEIGHTED

# ================================================================= Define.mqh
OP_BUY, OP_SELL, OP_BUYLIMIT, OP_SELLLIMIT, OP_BUYSTOP, OP_SELLSTOP = 0, 1, 2, 3, 4, 5
MODE_OPEN, MODE_LOW, MODE_HIGH, MODE_CLOSE, MODE_VOLUME, MODE_REAL_VOLUME = 0, 1, 2, 3, 4, 5
MODE_TIME = 5
MODE_TRADES, MODE_HISTORY = 0, 1
SELECT_BY_POS, SELECT_BY_TICKET = 0, 1
DOUBLE_VALUE, FLOAT_VALUE = 0, 1
CHART_BAR, CHART_CANDLE = 0, 1
MODE_ASCEND, MODE_DESCEND = 0, 1
MODE_BID, MODE_ASK, MODE_POINT, MODE_DIGITS, MODE_SPREAD = 9, 10, 11, 12, 13
MODE_STOPLEVEL, MODE_LOTSIZE, MODE_TICKVALUE, MODE_TICKSIZE = 14, 15, 16, 17
MODE_SWAPLONG, MODE_SWAPSHORT, MODE_STARTING, MODE_EXPIRATION = 18, 19, 20, 21
MODE_TRADEALLOWED, MODE_MINLOT, MODE_LOTSTEP, MODE_MAXLOT = 22, 23, 24, 25
MODE_SWAPTYPE, MODE_PROFITCALCMODE, MODE_MARGINCALCMODE = 26, 27, 28
MODE_MARGININIT, MODE_MARGINMAINTENANCE, MODE_MARGINHEDGED = 29, 30, 31
MODE_MARGINREQUIRED, MODE_FREEZELEVEL = 32, 33
EMPTY = -1

# functions.mqh enums
MODE_GATORJAW, MODE_GATORTEETH, MODE_GATORLIPS = 1, 2, 3
MODE_MAIN, MODE_PLUSDI, MODE_MINUSDI = 0, 1, 2
MODE_BASE, MODE_UPPER, MODE_LOWER = 0, 1, 2
MODE_TENKANSEN, MODE_KIJUNSEN, MODE_SENKOUSPANA, MODE_SENKOUSPANB, MODE_CHINKOUSPAN = 1, 2, 3, 4, 5
STO_LOWHIGH, STO_CLOSECLOSE = 0, 1


# =================================================================== Enum.mqh

def TFMigrate(tf: int) -> int:
    return {
        0: T.PERIOD_CURRENT, 1: T.PERIOD_M1, 5: T.PERIOD_M5, 15: T.PERIOD_M15,
        30: T.PERIOD_M30, 60: T.PERIOD_H1, 240: T.PERIOD_H4, 1440: T.PERIOD_D1,
        10080: T.PERIOD_W1, 43200: T.PERIOD_MN1, 2: T.PERIOD_M2, 3: T.PERIOD_M3,
        4: T.PERIOD_M4, 6: T.PERIOD_M6, 10: T.PERIOD_M10, 12: T.PERIOD_M12,
        16385: T.PERIOD_H1, 16386: T.PERIOD_H2, 16387: T.PERIOD_H3, 16388: T.PERIOD_H4,
        16390: T.PERIOD_H6, 16392: T.PERIOD_H8, 16396: T.PERIOD_H12, 16408: T.PERIOD_D1,
        32769: T.PERIOD_W1, 49153: T.PERIOD_MN1,
    }.get(int(tf), T.PERIOD_CURRENT)


def MethodMigrate(method: int) -> int:
    return {0: MODE_SMA, 1: MODE_EMA, 2: MODE_SMMA, 3: MODE_LWMA}.get(int(method), MODE_SMA)


def PriceMigrate(price: int) -> int:
    return {1: PRICE_CLOSE, 2: PRICE_OPEN, 3: PRICE_HIGH, 4: PRICE_LOW, 5: PRICE_MEDIAN,
            6: PRICE_TYPICAL, 7: PRICE_WEIGHTED}.get(int(price), PRICE_CLOSE)


def StoFieldMigrate(field: int) -> int:
    return STO_CLOSECLOSE if int(field) == 1 else STO_LOWHIGH


# ============================================================ data accessors


def _rates(symbol, tf, migrate=True):
    return T.rates_for(symbol, TFMigrate(tf) if migrate else tf)


def _one(series: str, symbol, tf, index, migrate=True):
    if index < 0:
        return -1
    r = _rates(symbol, tf, migrate)
    if r is None:
        return -1
    arr = getattr(r, series)
    i = len(arr) - 1 - int(index)
    if not 0 <= i < len(arr):
        return -1
    return arr[i].item() if hasattr(arr[i], "item") else arr[i]


def iLowMQL4(symbol, tf, index):
    return _one("low", symbol, tf, index)


def iHighMQL4(symbol, tf, index):
    return _one("high", symbol, tf, index)


def iOpenMQL4(symbol, tf, index):
    return _one("open", symbol, tf, index)


def iCloseMQL4(symbol, tf, index):
    return _one("close", symbol, tf, index)


def iTimeMQL4(symbol, tf, index):
    return _one("time", symbol, tf, index)


def iBarsMQL4(symbol, tf):
    r = _rates(symbol, tf)
    return 0 if r is None else len(r)


# mymql_v201.mqh: same, with an MQL5 ENUM_TIMEFRAMES argument (no migration)
def iTime(symbol, tf, index):
    return _one("time", symbol, tf, index, migrate=False)


def iClose(symbol, tf, index):
    return _one("close", symbol, tf, index, migrate=False)


def iOpen(symbol, tf, index):
    return _one("open", symbol, tf, index, migrate=False)


def iHigh(symbol, tf, index):
    return _one("high", symbol, tf, index, migrate=False)


def iLow(symbol, tf, index):
    return _one("low", symbol, tf, index, migrate=False)


PeriodInStr = T.PeriodInStr


def _extreme_mql4(symbol, tf, type_, count, start, pick):
    if start < 0:
        return -1
    r = _rates(symbol, tf)
    if r is None:
        return 0
    if count <= 0:
        count = len(r)
    if type_ <= MODE_OPEN:
        arr = r.open
    elif type_ == MODE_LOW:
        arr = r.low
    elif type_ == MODE_HIGH:
        arr = r.high
    elif type_ == MODE_CLOSE:
        arr = r.close
    elif type_ == MODE_VOLUME:
        arr = r.tick_volume
    else:                                    # type >= MODE_TIME
        arr = r.time
    n = len(arr)
    # CopyXxx(start, count) into a series array, then ArrayMaximum(arr, 0, count)
    window = [arr[n - 1 - s] for s in range(start, min(start + count, n))]
    if not window:
        return start
    best = 0
    for i in range(1, len(window)):
        if pick(window[i], window[best]):
            best = i
    return best + start


def iHighestMQL4(symbol, tf, type_, count=-1, start=0):
    return _extreme_mql4(symbol, tf, type_, count, start, lambda a, b: a > b)


def iLowestMQL4(symbol, tf, type_, count=-1, start=0):
    return _extreme_mql4(symbol, tf, type_, count, start, lambda a, b: a < b)


def iATRMQL4(symbol, tf, period, shift):
    """``iATR`` + ``CopyBuffer`` on the requested series (terminal ATR)."""
    r = _rates(symbol, tf)
    if r is None:
        return -1
    from backtester.indicators import mql5
    atr = mql5.atr(r.high, r.low, r.close, int(period))
    i = len(atr) - 1 - int(shift)
    if not 0 <= i < len(atr) or not np.isfinite(atr[i]):
        return EMPTY_VALUE
    return float(atr[i])


def iMAMQL4(symbol, tf, period, ma_shift, method, price, shift):
    """``iMA`` + ``CopyBuffer`` on the requested series (terminal MA)."""
    r = _rates(symbol, tf)
    if r is None:
        return -1
    from backtester.indicators import mql5
    names = {MODE_SMA: "sma", MODE_EMA: "ema", MODE_SMMA: "smma", MODE_LWMA: "lwma"}
    src = mql5.applied_price(r.df, mql5.MT5_PRICE_BY_INDEX[PriceMigrate(price)])
    line = mql5.shift_forward(mql5.ma(src, int(period), names[MethodMigrate(method)]), int(ma_shift))
    i = len(line) - 1 - int(shift)
    if not 0 <= i < len(line) or not np.isfinite(line[i]):
        return EMPTY_VALUE
    return float(line[i])


def CopyBufferMQL4(values, index, shift):
    """``CopyBuffer(handle, index, shift, 1)`` on an already-computed list
    of buffers (``values[index]`` forward-indexed)."""
    if index not in (0, 1, 2, 3, 4) or index >= len(values):
        return EMPTY_VALUE
    buf = values[index]
    i = len(buf) - 1 - int(shift)
    if not 0 <= i < len(buf) or not np.isfinite(buf[i]):
        return EMPTY_VALUE
    return float(buf[i])


# ================================================================ time


def TimeHourMQL4(date):
    return T.TimeToStruct(date).hour


def TimeMinuteMQL4(date):
    return T.TimeToStruct(date).min


def TimeSecondsMQL4(date):
    return T.TimeToStruct(date).sec


def TimeDayOfWeekMQL4(date):
    return T.TimeToStruct(date).day_of_week


def TimeDayMQL4(date):
    return T.TimeToStruct(date).day


def _now():
    """``TimeCurrent()`` offline: the newest bar's time of the chart series."""
    r = T.current().chart
    return int(r.time[-1]) if r is not None and len(r) else 0


def HourMQL4():
    return T.TimeToStruct(_now()).hour


def DayOfWeekMQL4():
    return T.TimeToStruct(_now()).day_of_week


def MonthMQL4():
    return T.TimeToStruct(_now()).mon


class DateTime:
    """``DateTime.mqh`` / ``MQL5Book/DateTime.mqh`` / ``MT4Time.mqh``: cached
    ``TimeToStruct`` behind ``TimeYear(T)``-style accessors."""

    _DateTime: "DateTime"

    def __init__(self):
        self.origin = 0
        self.mdtstruct = T.TimeToStruct(0)

    def convert(self, dt):
        if self.origin != dt:
            self.origin = dt
            self.mdtstruct = T.TimeToStruct(dt)

    @staticmethod
    def assign(dt) -> "DateTime":
        DateTime._DateTime.convert(int(dt))
        return DateTime._DateTime

    def timeDayOfWeek(self):
        return self.mdtstruct.day_of_week

    def timeDayOfYear(self):
        return self.mdtstruct.day_of_year

    def timeYear(self):
        return self.mdtstruct.year

    def timeMonth(self):
        return self.mdtstruct.mon

    def timeDay(self):
        return self.mdtstruct.day

    def timeHour(self):
        return self.mdtstruct.hour

    def timeMinute(self):
        return self.mdtstruct.min

    def timeSeconds(self):
        return self.mdtstruct.sec


DateTime._DateTime = DateTime()


def TimeDayOfWeek(t):
    return DateTime.assign(t).timeDayOfWeek()


def TimeDayOfYear(t):
    return DateTime.assign(t).timeDayOfYear()


def TimeYear(t):
    return DateTime.assign(t).timeYear()


def TimeMonth(t):
    return DateTime.assign(t).timeMonth()


def TimeDay(t):
    return DateTime.assign(t).timeDay()


def TimeHour(t):
    return DateTime.assign(t).timeHour()


def TimeMinute(t):
    return DateTime.assign(t).timeMinute()


def TimeSeconds(t):
    return DateTime.assign(t).timeSeconds()


# MT4Time.mqh's argument-less forms read TimeCurrent()
def Year():
    return TimeYear(_now())


def Month():
    return TimeMonth(_now())


def Day():
    return TimeDay(_now())


def Hour():
    return TimeHour(_now())


def Minute():
    return TimeMinute(_now())


def Seconds():
    return TimeSeconds(_now())


# ============================================================ market info


def MarketInfo(symbol, type_):
    """``MT4MarketInfo.mqh`` / ``MarketInfoMQL4``. Offline, only what the
    dataset knows is real: point, digits, spread, last high/low/time and the
    latest close as bid/ask. Trading properties (lots, swaps, margins) are
    not stored with the bars and return 0, as an unset property does."""
    r = T.rates_for(symbol)
    if r is None:
        return 0.0
    if type_ == MODE_LOW:
        return r.SymbolInfoDouble(T.SYMBOL_LASTLOW)
    if type_ == MODE_HIGH:
        return r.SymbolInfoDouble(T.SYMBOL_LASTHIGH)
    if type_ == MODE_TIME:
        return float(r.SymbolInfoInteger(T.SYMBOL_TIME))
    if type_ == MODE_BID:
        return r.SymbolInfoDouble(T.SYMBOL_BID)
    if type_ == MODE_ASK:
        return r.SymbolInfoDouble(T.SYMBOL_ASK)
    if type_ == MODE_POINT:
        return r.SymbolInfoDouble(T.SYMBOL_POINT)
    if type_ == MODE_DIGITS:
        return float(r.SymbolInfoInteger(T.SYMBOL_DIGITS))
    if type_ == MODE_SPREAD:
        return float(r.SymbolInfoInteger(T.SYMBOL_SPREAD))
    if type_ == MODE_LOTSIZE:
        return r.SymbolInfoDouble(T.SYMBOL_TRADE_CONTRACT_SIZE)
    if type_ == MODE_TICKSIZE:
        return r.SymbolInfoDouble(T.SYMBOL_TRADE_TICK_SIZE)
    # Contract values a dataset can carry in its Rates spec when known.
    spec_keys = {MODE_TICKVALUE: "tick_value", MODE_MINLOT: "volume_min",
                 MODE_LOTSTEP: "volume_step", MODE_MAXLOT: "volume_max",
                 MODE_PROFITCALCMODE: "calc_mode", MODE_STOPLEVEL: "stops_level"}
    if type_ in spec_keys:
        return float(r.spec.get(spec_keys[type_], 0.0))
    return 0.0


MarketInfoMQL4 = MarketInfo


# ============================================================ arrays


def iMAOnArray(array, total, period, ma_shift, ma_method, shift) -> float:
    """``iMAOnArray`` (functions.mqh's ``iMAOnArrayMQL4``, mymql_v201's
    ``iMAOnArray``): an MA of a **series-ordered** array (index 0 = newest)
    evaluated at ``shift``. Returns 0 when there is not enough data."""
    if total == 0:
        total = len(array)
    if 0 < total <= period:
        return 0
    if shift > total - period - ma_shift:
        return 0
    if ma_method == MODE_SMA:
        arr = list(array[shift + ma_shift: shift + ma_shift + period])
        total = len(arr)
        buf = [0.0] * total
        s = 0.0
        pos = total - 1
        for _ in range(1, period):
            s += arr[pos]
            pos -= 1
        while pos >= 0:
            s += arr[pos]
            buf[pos] = s / period
            s -= arr[pos + period - 1]
            pos -= 1
        return buf[0]
    if ma_method == MODE_EMA:
        buf = [0.0] * total
        pr = 2.0 / (period + 1)
        pos = total - 2
        while pos >= 0:
            if pos == total - 2:
                buf[pos + 1] = array[pos + 1]
            buf[pos] = array[pos] * pr + buf[pos + 1] * (1 - pr)
            pos -= 1
        return buf[shift + ma_shift]
    if ma_method == MODE_SMMA:
        buf = [0.0] * total
        s = 0.0
        pos = total - period
        while pos >= 0:
            if pos == total - period:
                k = pos
                for _ in range(period):
                    s += array[k]
                    buf[k] = 0
                    k += 1
            else:
                s = buf[pos + 1] * (period - 1) + array[pos]
            buf[pos] = s / period
            pos -= 1
        return buf[shift + ma_shift]
    if ma_method == MODE_LWMA:
        buf = [0.0] * total
        s = lsum = 0.0
        weight = 0
        pos = total - 1
        for i in range(1, period + 1):
            price = array[pos]
            s += price * i
            lsum += price
            weight += i
            pos -= 1
        pos += 1
        i = pos + period
        while pos >= 0:
            buf[pos] = s / weight
            if pos == 0:
                break
            pos -= 1
            i -= 1
            price = array[pos]
            s = s - lsum + price * period
            lsum -= array[i]
            lsum += price
        return buf[shift + ma_shift]
    return 0


iMAOnArrayMQL4 = iMAOnArray


# ============================================ chart objects / plot styling
#
# No-ops: the app draws an indicator from the series it returns. They return
# what MQL5 returns for a successful call so ported control flow is unchanged.


def ObjectsDeleteAllMQL4(window=EMPTY, type_=EMPTY):
    return 0


def ObjectFindMQL4(name):
    return -1


def ObjectsTotalMQL4(type_=EMPTY, window=-1):
    return 0


def ObjectNameMQL4(index):
    return ""


def ObjectDeleteMQL4(name):
    return True


def ObjectCreateMQL4(name, type_, window, time1, price1, time2=0, price2=0, time3=0, price3=0):
    return True


def ObjectSetTextMQL4(name, text, font_size, font="", text_color=None):
    return True


def ObjectSetMQL4(name, index, value):
    return True


def SetIndexStyleMQL4(index, type_, style=EMPTY, width=EMPTY, clr=None):
    return None
