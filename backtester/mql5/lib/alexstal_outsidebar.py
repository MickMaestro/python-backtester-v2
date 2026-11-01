"""AlexSTAL_OutsideBar.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *

# enum OrderFormationBarHighLow
OFBError = 0
OFBLowEqualHigh = 1
OFBHighLow = 2
OFBLowHigh = 3
OFBErrorFindSmallTF = 4
_enum('OrderFormationBarHighLow', {0: 'OFBError', 1: 'OFBLowEqualHigh', 2: 'OFBHighLow', 3: 'OFBLowHigh', 4: 'OFBErrorFindSmallTF'})


def GetOrderFormationBarHighLow(symbol, timeframe, shift, UseSmallerTFforEB):
    tmp = OFBError
    if UseSmallerTFforEB:
        i = 1
        while i <= NumberOfPassesSearch(timeframe):
            tmp = SmallTFLogicBarHighLow(symbol, timeframe, shift, SmallTFforNumberOfPassesSearch(timeframe, i))
            if tmp == OFBHighLow or tmp == OFBLowHigh:
                break
            i += 1
        if tmp != OFBHighLow and tmp != OFBLowHigh:
            tmp = SimpleLogicBarHighLow(symbol, timeframe, shift)
    else:
        tmp = SimpleLogicBarHighLow(symbol, timeframe, shift)
    return tmp

def SmallTFLogicBarHighLow(symbol, timeframe, shift, TFsmall):
    tmp = Arr(1, 0, dyn=False, factory=MqlRates)
    copied = CopyRates(symbol, timeframe, shift, 1, tmp)
    if copied <= 0:
        return OFBError
    BarH = tmp[0].high
    BarL = tmp[0].low
    if BarH == BarL:
        return OFBLowEqualHigh
    BarDTs = tmp[0].time
    BarDTe = 0
    if timeframe != PERIOD_MN1:
        BarDTe = BarDTs + PeriodSeconds(timeframe) - 1
    else:
        BarDTe = BarDTs + (1440 * NumberDaysMonth(BarDTs) * 60) - 1
    tmpSmall = Arr(0, 0, factory=MqlRates)
    copied = CopyRates(symbol, TFsmall, _DT(BarDTs), _DT(BarDTe), tmpSmall)
    if copied <= 0:
        return OFBError
    tmpI = 0
    for i in range(0, ArraySize(tmpSmall)):
        if tmpSmall[i].high >= BarH:
            tmpI = tmpI + 1
        if tmpSmall[i].low <= BarL:
            tmpI = tmpI + 2
        if tmpI != 0:
            break
    _sw1 = tmpI
    if _sw1 == 0:
        return OFBError
    elif _sw1 == 1:
        return OFBHighLow
    elif _sw1 == 2:
        return OFBLowHigh
    elif _sw1 == 3:
        return OFBErrorFindSmallTF
    else:
        return OFBError

def SimpleLogicBarHighLow(symbol, timeframe, shift):
    tmp = Arr(1, 0, dyn=False, factory=MqlRates)
    copied = CopyRates(symbol, timeframe, shift, 1, tmp)
    if copied <= 0:
        return OFBError
    res = OFBError
    if tmp[0].high == tmp[0].low:
        return OFBLowEqualHigh
    if tmp[0].close > tmp[0].open:
        res = OFBLowHigh
    if tmp[0].close < tmp[0].open:
        res = OFBHighLow
    if res == OFBError:
        a1 = tmp[0].high - tmp[0].close
        a2 = tmp[0].close - tmp[0].low
        if a1 > a2:
            res = OFBLowHigh
        if a1 < a2:
            res = OFBHighLow
        if res == OFBError:
            res = OFBHighLow
    return res

def NumberOfPassesSearch(timeframe):
    _sw2 = timeframe
    if _sw2 == PERIOD_M1:
        return 0
    elif _sw2 in (PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15):
        return 1
    elif _sw2 in (PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6):
        return 2
    elif _sw2 in (PERIOD_H8, PERIOD_H12, PERIOD_D1):
        return 3
    elif _sw2 in (PERIOD_W1, PERIOD_MN1):
        return 4
    else:
        return 0

def SmallTFforNumberOfPassesSearch(timeframe, Passes):
    _sw3 = timeframe
    if _sw3 in (PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15):
        _sw4 = Passes
        if _sw4 == 1:
            return PERIOD_M1
        else:
            return 0
    elif _sw3 == PERIOD_M20:
        _sw5 = Passes
        if _sw5 == 1:
            return PERIOD_M2
        elif _sw5 == 2:
            return PERIOD_M1
        else:
            return 0
    elif _sw3 in (PERIOD_M30, PERIOD_H1):
        _sw6 = Passes
        if _sw6 == 1:
            return PERIOD_M5
        elif _sw6 == 2:
            return PERIOD_M1
        else:
            return 0
    elif _sw3 in (PERIOD_H2, PERIOD_H3):
        _sw7 = Passes
        if _sw7 == 1:
            return PERIOD_M15
        elif _sw7 == 2:
            return PERIOD_M1
        else:
            return 0
    elif _sw3 in (PERIOD_H4, PERIOD_H6):
        _sw8 = Passes
        if _sw8 == 1:
            return PERIOD_M30
        elif _sw8 == 2:
            return PERIOD_M1
        else:
            return 0
    elif _sw3 in (PERIOD_H8, PERIOD_H12):
        _sw9 = Passes
        if _sw9 == 1:
            return PERIOD_H1
        elif _sw9 == 2:
            return PERIOD_M5
        elif _sw9 == 3:
            return PERIOD_M1
        else:
            return 0
    elif _sw3 == PERIOD_D1:
        _sw10 = Passes
        if _sw10 == 1:
            return PERIOD_H4
        elif _sw10 == 2:
            return PERIOD_M30
        elif _sw10 == 3:
            return PERIOD_M1
        else:
            return 0
    elif _sw3 == PERIOD_W1:
        _sw11 = Passes
        if _sw11 == 1:
            return PERIOD_D1
        elif _sw11 == 2:
            return PERIOD_H4
        elif _sw11 == 3:
            return PERIOD_M30
        elif _sw11 == 4:
            return PERIOD_M1
        else:
            return 0
    elif _sw3 == PERIOD_MN1:
        _sw12 = Passes
        if _sw12 == 1:
            return PERIOD_D1
        elif _sw12 == 2:
            return PERIOD_H4
        elif _sw12 == 3:
            return PERIOD_M30
        elif _sw12 == 4:
            return PERIOD_M1
        else:
            return 0
    else:
        return 0

def NumberDaysMonth(Date):
    tmpDT = MqlDateTime()
    TimeToStruct(Date, tmpDT)
    _sw13 = tmpDT.mon
    if _sw13 == 1:
        return 31
    elif _sw13 == 2:
        if _imod(tmpDT.year, 4) == 0:
            return 29
        else:
            return 28
    elif _sw13 == 3:
        return 31
    elif _sw13 == 4:
        return 30
    elif _sw13 == 5:
        return 31
    elif _sw13 == 6:
        return 30
    elif _sw13 == 7:
        return 31
    elif _sw13 == 8:
        return 31
    elif _sw13 == 9:
        return 30
    elif _sw13 == 10:
        return 31
    elif _sw13 == 11:
        return 30
    elif _sw13 == 12:
        return 31
    else:
        return 0

__all__ = ['OFBError', 'OFBLowEqualHigh', 'OFBHighLow', 'OFBLowHigh', 'OFBErrorFindSmallTF', 'GetOrderFormationBarHighLow', 'SmallTFLogicBarHighLow', 'SimpleLogicBarHighLow', 'NumberOfPassesSearch', 'SmallTFforNumberOfPassesSearch', 'NumberDaysMonth']
