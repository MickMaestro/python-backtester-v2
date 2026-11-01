"""PPMCC — converted from MQL5: MQL5 Indicators/PPMCC/PPMCC.mq5

Pearson product-moment correlation coefficient
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 1, 'indicator_maximum': 1.0, 'indicator_minimum': -1.0}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'PPMCC'}, 'levels': [], 'description': ['Pearson product-moment correlation coefficient'], 'name': 'PPMCC', 'source': 'MQL5 Indicators/PPMCC/PPMCC.mq5', 'folder': 'PPMCC', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'InpSymbolX', 'py': 'InpSymbolX', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'First symbol name', 'sinput': False}, {'mql': 'InpAppliedPriceX', 'py': 'InpAppliedPriceX', 'param': 'InpAppliedPriceX', 'type': 'int', 'default': 1, 'label': 'First symbol applied price', 'sinput': False}, {'mql': 'InpSymbolY', 'py': 'InpSymbolY', 'param': None, 'type': 'string', 'default': 'USDJPY', 'label': 'Second symbol name', 'sinput': False}, {'mql': 'InpAppliedPriceY', 'py': 'InpAppliedPriceY', 'param': 'InpAppliedPriceY', 'type': 'int', 'default': 1, 'label': 'Second symbol applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 50)  # Period
InpSymbolX = _input('InpSymbolX', 'EURUSD')  # First symbol name
InpAppliedPriceX = _input('InpAppliedPriceX', PRICE_CLOSE)  # First symbol applied price
InpSymbolY = _input('InpSymbolY', 'USDJPY')  # Second symbol name
InpAppliedPriceY = _input('InpAppliedPriceY', PRICE_CLOSE)  # Second symbol applied price
BufferPPMCC = Arr(0, 0.0)
BufferAB = Arr(0, 0.0)
BufferC = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
BufferMAX = Arr(0, 0.0)
BufferMAY = Arr(0, 0.0)
BufferMAA = Arr(0, 0.0)
BufferMAB = Arr(0, 0.0)
period_ma = 0
handle_maX = 0
handle_maY = 0
handle_maA = 0
handle_maB = 0

def OnInit():
    global handle_maA, handle_maB, handle_maX, handle_maY, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferPPMCC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferAB, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAX, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMAY, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMAA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferMAB, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PPMCC' + '(' + _str(period_ma) + ')' + InpSymbolX + '/' + InpSymbolY)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPPMCC, True)
    ArraySetAsSeries(BufferAB, True)
    ArraySetAsSeries(BufferC, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferMAX, True)
    ArraySetAsSeries(BufferMAY, True)
    ArraySetAsSeries(BufferMAA, True)
    ArraySetAsSeries(BufferMAB, True)
    if not SymbolCheck(InpSymbolX):
        return INIT_FAILED
    if not SymbolCheck(InpSymbolY):
        return INIT_FAILED
    ResetLastError()
    handle_maX = iMA(InpSymbolX, PERIOD_CURRENT, period_ma, 0, MODE_SMA, InpAppliedPriceX)
    if handle_maX == INVALID_HANDLE:
        Print('The ', InpSymbolX, ' iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maA = iMA(InpSymbolX, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPriceX)
    if handle_maA == INVALID_HANDLE:
        Print('The ', InpSymbolX, ' iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maY = iMA(InpSymbolY, PERIOD_CURRENT, period_ma, 0, MODE_SMA, InpAppliedPriceY)
    if handle_maY == INVALID_HANDLE:
        Print('The ', InpSymbolY, ' iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maB = iMA(InpSymbolY, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPriceY)
    if handle_maB == INVALID_HANDLE:
        Print('The ', InpSymbolY, ' iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    barsX = Bars(InpSymbolX, PERIOD_CURRENT)
    barsY = Bars(InpSymbolY, PERIOD_CURRENT)
    if (rates_total < 4 or barsX < 4) or barsY < 4:
        return 0
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferPPMCC, EMPTY_VALUE)
        ArrayInitialize(BufferAB, 0)
        ArrayInitialize(BufferC, 0)
        ArrayInitialize(BufferMAX, 0)
        ArrayInitialize(BufferMAY, 0)
        ArrayInitialize(BufferMAA, 0)
        ArrayInitialize(BufferMAB, 0)
    limit_min = fmin(rates_total, fmin(barsX, barsY)) - 1
    copied = 0
    count = (1 if (limit == 0) else limit_min)
    copied = CopyBuffer(handle_maX, 0, 0, count, BufferMAX)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maA, 0, 0, count, BufferMAA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maY, 0, 0, count, BufferMAY)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maB, 0, 0, count, BufferMAB)
    if copied != count:
        return 0
    count = (limit if (limit == 0) else limit_min)
    for i in range(count, 0 - 1, -1):
        index1 = BarShift(InpSymbolX, PERIOD_CURRENT, time[i])
        index2 = BarShift(InpSymbolY, PERIOD_CURRENT, time[i])
        if index1 > count or index2 > count:
            continue
        if index1 != WRONG_VALUE and index2 != WRONG_VALUE:
            avg1 = BufferMAX[index1]
            avg2 = BufferMAY[index2]
            a = BufferMAA[index1] - avg1
            b = BufferMAB[index1] - avg2
            BufferAB[i] = a * b
            BufferC[i] = a * a
            BufferD[i] = b * b
    for i in range(limit, 0 - 1, -1):
        Numerator = MAOnArray(BufferAB, 0, period_ma, 0, MODE_SMA, i)
        DenominatorC = MAOnArray(BufferC, 0, period_ma, 0, MODE_SMA, i)
        DenominatorD = MAOnArray(BufferD, 0, period_ma, 0, MODE_SMA, i)
        Denominator = sqrt(DenominatorC * DenominatorD)
        BufferPPMCC[i] = _fdiv(Numerator, (Denominator if (Denominator != 0) else DBL_MIN))
    return rates_total

def SymbolCheck(symbol_name):
    select = Box(0)
    ResetLastError()
    if not SymbolInfoInteger(symbol_name, SYMBOL_SELECT, select):
        err = GetLastError()
        Print('Error: ', err, ' Symbol ', symbol_name, ' does not exist')
        return False
    else:
        if select.v:
            return True
        ResetLastError()
        if not SymbolSelect(symbol_name, True):
            err = GetLastError()
            Print('Error selected ', symbol_name, ': ', err)
    return False

def BarShift(symbol_name, timeframe, time, exact=False):
    last_bar = Box(0)
    if not SeriesInfoInteger(symbol_name, timeframe, SERIES_LASTBAR_DATE, last_bar):
        array = Arr(1, 0, dyn=False)
        if CopyTime(symbol_name, timeframe, 0, 1, array) == 1:
            last_bar.v = array[0]
        else:
            return WRONG_VALUE
    if time > last_bar.v:
        return 0
    shift = Bars(symbol_name, timeframe, time, last_bar.v)
    array = Arr(1, 0, dyn=False)
    if CopyTime(symbol_name, timeframe, _DT(time), 1, array) == 1:
        return ((shift - 1) if (array[0] == time) else WRONG_VALUE if (exact and time > (array[0] + PeriodSeconds(timeframe))) else shift)
    return WRONG_VALUE

def MAOnArray(array, total, period, ma_shift, ma_method, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period - ma_shift):
        return 0.0
    _sw1 = ma_method
    if _sw1 == MODE_SMA:
        total = ArrayCopy(arr, array, 0, shift + ma_shift, period)
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        i = 0
        pos = total - 1
        i = 1
        while i < period:
            sum_ += arr[pos]
            i += 1
            pos -= 1
        while pos >= 0:
            sum_ += arr[pos]
            buf[pos] = _fdiv(sum_, period)
            sum_ -= arr[pos + period - 1]
            pos -= 1
        return buf[0]
    elif _sw1 == MODE_EMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        pr = _fdiv(2.0, period + 1)
        pos = total - 2
        while pos >= 0:
            if pos == (total - 2):
                buf[pos + 1] = array[pos + 1]
            buf[pos] = (array[pos] * pr) + (buf[pos + 1] * (1 - pr))
            pos -= 1
        return buf[shift + ma_shift]
    elif _sw1 == MODE_SMMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        i = 0
        k = 0
        pos = 0
        pos = total - period
        while pos >= 0:
            if pos == (total - period):
                i = 0
                k = pos
                while i < period:
                    sum_ += array[k]
                    buf[k] = 0.0
                    i += 1
                    k += 1
            else:
                sum_ = (buf[pos + 1] * (period - 1)) + array[pos]
            buf[pos] = _fdiv(sum_, period)
            pos -= 1
        return buf[shift + ma_shift]
    elif _sw1 == MODE_LWMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        lsum = 0.0
        price = 0.0
        i = 0
        weight = 0
        pos = total - 1
        i = 1
        while i <= period:
            price = array[pos]
            sum_ += price * i
            lsum += price
            weight += i
            i += 1
            pos -= 1
        pos += 1
        i = pos + period
        while pos >= 0:
            buf[pos] = _fdiv(sum_, weight)
            if pos == 0:
                break
            pos -= 1
            i -= 1
            price = array[pos]
            sum_ = sum_ - lsum + (price * period)
            lsum -= array[i]
            lsum += price
        return buf[shift + ma_shift]
    else:
        return 0.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PPMCC(_MQL5Indicator):
    name = 'PPMCC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 50,  # Period
        'InpAppliedPriceX': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # First symbol applied price
        'InpAppliedPriceY': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Second symbol applied price
    }
    y_range = (-1.0, 1.0)

