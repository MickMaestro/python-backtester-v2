"""``AlexSTAL_OutsideBar.mqh`` (AlexSTAL, 2011) — line-by-line port.

Decides which extreme of a bar formed first (high then low, or low then
high). With ``UseSmallerTFforEB`` it looks inside the bar on successively
smaller timeframes; otherwise (or when no smaller-timeframe data answers) it
falls back to the candle's direction.

The smaller-timeframe search reads bars through :mod:`.terminal`. This app
loads one timeframe per chart, so unless the terminal has been given the
smaller timeframes too (``Terminal.add(Rates(df_m1, symbol, PERIOD_M1))``)
those lookups fail exactly as ``CopyRates`` does without history — and the
function returns the simple-logic answer, as it would in MT5.
"""

from __future__ import annotations

from . import terminal as T

# enum OrderFormationBarHighLow
OFBError, OFBLowEqualHigh, OFBHighLow, OFBLowHigh, OFBErrorFindSmallTF = 0, 1, 2, 3, 4


def _rates_at(symbol, timeframe, shift):
    r = T.rates_for(symbol, timeframe)
    if r is None:
        return None
    i = len(r) - 1 - int(shift)
    if not 0 <= i < len(r):
        return None
    return r, i


def NumberDaysMonth(Date: int) -> int:
    s = T.TimeToStruct(Date)
    if s.mon == 2:
        return 29 if s.year % 4 == 0 else 28
    return {1: 31, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31,
            11: 30, 12: 31}.get(s.mon, 0)


def NumberOfPassesSearch(timeframe: int) -> int:
    tf = int(timeframe)
    if tf in (T.PERIOD_M2, T.PERIOD_M3, T.PERIOD_M4, T.PERIOD_M5, T.PERIOD_M6,
              T.PERIOD_M10, T.PERIOD_M12, T.PERIOD_M15):
        return 1
    if tf in (T.PERIOD_M20, T.PERIOD_M30, T.PERIOD_H1, T.PERIOD_H2, T.PERIOD_H3,
              T.PERIOD_H4, T.PERIOD_H6):
        return 2
    if tf in (T.PERIOD_H8, T.PERIOD_H12, T.PERIOD_D1):
        return 3
    if tf in (T.PERIOD_W1, T.PERIOD_MN1):
        return 4
    return 0


def SmallTFforNumberOfPassesSearch(timeframe: int, Passes: int) -> int:
    tf = int(timeframe)
    table = None
    if tf in (T.PERIOD_M2, T.PERIOD_M3, T.PERIOD_M4, T.PERIOD_M5, T.PERIOD_M6,
              T.PERIOD_M10, T.PERIOD_M12, T.PERIOD_M15):
        table = {1: T.PERIOD_M1}
    elif tf == T.PERIOD_M20:
        table = {1: T.PERIOD_M2, 2: T.PERIOD_M1}
    elif tf in (T.PERIOD_M30, T.PERIOD_H1):
        table = {1: T.PERIOD_M5, 2: T.PERIOD_M1}
    elif tf in (T.PERIOD_H2, T.PERIOD_H3):
        table = {1: T.PERIOD_M15, 2: T.PERIOD_M1}
    elif tf in (T.PERIOD_H4, T.PERIOD_H6):
        table = {1: T.PERIOD_M30, 2: T.PERIOD_M1}
    elif tf in (T.PERIOD_H8, T.PERIOD_H12):
        table = {1: T.PERIOD_H1, 2: T.PERIOD_M5, 3: T.PERIOD_M1}
    elif tf in (T.PERIOD_D1,):
        table = {1: T.PERIOD_H4, 2: T.PERIOD_M30, 3: T.PERIOD_M1}
    elif tf in (T.PERIOD_W1, T.PERIOD_MN1):
        table = {1: T.PERIOD_D1, 2: T.PERIOD_H4, 3: T.PERIOD_M30, 4: T.PERIOD_M1}
    return 0 if table is None else table.get(int(Passes), 0)


def SimpleLogicBarHighLow(symbol, timeframe, shift) -> int:
    got = _rates_at(symbol, timeframe, shift)
    if got is None:
        return OFBError
    r, i = got
    o, h, l, c = r.open[i], r.high[i], r.low[i], r.close[i]
    res = OFBError
    if h == l:
        return OFBLowEqualHigh
    if c > o:
        res = OFBLowHigh
    if c < o:
        res = OFBHighLow
    if res == OFBError:
        a1 = h - c
        a2 = c - l
        if a1 > a2:
            res = OFBLowHigh
        if a1 < a2:
            res = OFBHighLow
        if res == OFBError:
            res = OFBHighLow
    return res


def SmallTFLogicBarHighLow(symbol, timeframe, shift, TFsmall) -> int:
    got = _rates_at(symbol, timeframe, shift)
    if got is None:
        return OFBError
    r, i = got
    BarH, BarL = r.high[i], r.low[i]
    if BarH == BarL:
        return OFBLowEqualHigh
    BarDTs = int(r.time[i])
    if int(timeframe) != T.PERIOD_MN1:
        BarDTe = BarDTs + T.PeriodSeconds(timeframe) - 1
    else:
        BarDTe = BarDTs + 1440 * NumberDaysMonth(BarDTs) * 60 - 1
    small = T.rates_for(symbol, TFsmall)
    if small is None:
        return OFBError
    mask = (small.time >= BarDTs) & (small.time <= BarDTe)
    idx = mask.nonzero()[0]
    if len(idx) == 0:
        return OFBError
    tmpI = 0
    for k in idx:
        if small.high[k] >= BarH:
            tmpI += 1
        if small.low[k] <= BarL:
            tmpI += 2
        if tmpI != 0:
            break
    return {1: OFBHighLow, 2: OFBLowHigh, 3: OFBErrorFindSmallTF}.get(tmpI, OFBError)


def GetOrderFormationBarHighLow(symbol, timeframe, shift, UseSmallerTFforEB: bool) -> int:
    tmp = OFBError
    if UseSmallerTFforEB:
        for i in range(1, NumberOfPassesSearch(timeframe) + 1):
            tmp = SmallTFLogicBarHighLow(symbol, timeframe, shift,
                                         SmallTFforNumberOfPassesSearch(timeframe, i))
            if tmp in (OFBHighLow, OFBLowHigh):
                break
        if tmp not in (OFBHighLow, OFBLowHigh):
            tmp = SimpleLogicBarHighLow(symbol, timeframe, shift)
    else:
        tmp = SimpleLogicBarHighLow(symbol, timeframe, shift)
    return tmp
