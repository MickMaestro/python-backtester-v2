"""RSdynamic_line — converted from MQL5: MQL5 Indicators/RSdynamic_line/RSdynamic_line.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [32768], 2: [255], 3: [16711680], 4: [16711935]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Support', 2: 'Resistance', 3: 'MA1', 4: 'MA2'}, 'levels': [], 'description': [], 'name': 'RSdynamic_line', 'source': 'MQL5 Indicators/RSdynamic_line/RSdynamic_line.mq5', 'folder': 'RSdynamic_line', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PRICE_CALC
PRICE_CALC_CLOSE = 1
PRICE_CALC_OPEN = 2
PRICE_CALC_HIGH = 3
PRICE_CALC_LOW = 4
_enum('ENUM_PRICE_CALC', {1: 'PRICE_CALC_CLOSE', 2: 'PRICE_CALC_OPEN', 3: 'PRICE_CALC_HIGH', 4: 'PRICE_CALC_LOW'})

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 14)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CALC_CLOSE)  # Applied price
BufferSupp = Arr(0, 0.0)
BufferResist = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferMATMP = Arr(0, 0.0)
BufferStream1 = Arr(0, 0.0)
BufferStream2 = Arr(0, 0.0)
BufferStream3 = Arr(0, 0.0)
handle_ma = 0
period_ma = 0

def OnInit():
    global handle_ma, period_ma
    period_ma = (2 if (InpPeriodMA < 2) else InpPeriodMA)
    SetIndexBuffer(0, BufferSupp, INDICATOR_DATA)
    SetIndexBuffer(1, BufferResist, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA1, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferMATMP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferStream1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferStream2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferStream3, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'RS dynamic line indicator')
    ArraySetAsSeries(BufferSupp, True)
    ArraySetAsSeries(BufferResist, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferMATMP, True)
    ArraySetAsSeries(BufferStream1, True)
    ArraySetAsSeries(BufferStream2, True)
    ArraySetAsSeries(BufferStream3, True)
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferSupp, EMPTY_VALUE)
        ArrayInitialize(BufferResist, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, EMPTY_VALUE)
        ArrayInitialize(BufferMA2, EMPTY_VALUE)
        ArrayInitialize(BufferMATMP, EMPTY_VALUE)
        ArrayInitialize(BufferStream1, EMPTY_VALUE)
        ArrayInitialize(BufferStream2, EMPTY_VALUE)
        ArrayInitialize(BufferStream3, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMATMP)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        HHVindex = Highest(Symbol(), PERIOD_CURRENT, InpAppliedPrice, period_ma, i)
        LLVindex = Lowest(Symbol(), PERIOD_CURRENT, InpAppliedPrice, period_ma, i)
        HHV2index = Highest(Symbol(), PERIOD_CURRENT, InpAppliedPrice, _idiv(period_ma, 2), i)
        LLV2index = Lowest(Symbol(), PERIOD_CURRENT, InpAppliedPrice, _idiv(period_ma, 2), i)
        if ((HHVindex == WRONG_VALUE or LLVindex == WRONG_VALUE) or HHV2index == WRONG_VALUE) or LLV2index == WRONG_VALUE:
            continue
        HHV = BufferMATMP[HHVindex]
        LLV = BufferMATMP[LLVindex]
        HHV2 = BufferMATMP[HHV2index]
        LLV2 = BufferMATMP[LLV2index]
        a1 = (HHV + LLV + BufferMATMP[i]) / 3
        BufferStream1[i] = (2 * a1) - HHV
        BufferStream2[i] = (2 * a1) - LLV
        BufferStream3[i] = (HHV2 + LLV2 + BufferMATMP[i]) / 3
    for i in range(limit, 0 - 1, -1):
        BufferSupp[i] = MAOnArray(BufferStream1, 0, period_ma, 0, MODE_SMA, i)
        BufferResist[i] = MAOnArray(BufferStream2, 0, period_ma, 0, MODE_SMA, i)
        BufferMA1[i] = MAOnArray(BufferStream3, 0, _idiv(period_ma, 2), 0, MODE_SMA, i)
        BufferMA2[i] = (BufferSupp[i] + BufferResist[i] + BufferMA1[i]) / 3
    return rates_total

def Highest(symbol_name, timeframe, price_type, count, start):
    if symbol_name == '' or symbol_name == "":
        symbol_name = Symbol()
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    _sw1 = price_type
    if _sw1 == PRICE_CLOSE:
        if CopyClose(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    elif _sw1 == PRICE_OPEN:
        if CopyOpen(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    elif _sw1 == PRICE_HIGH:
        if CopyHigh(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    elif _sw1 == PRICE_LOW:
        if CopyLow(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    else:
        return WRONG_VALUE
    return WRONG_VALUE

def Lowest(symbol_name, timeframe, price_type, count, start):
    if symbol_name == '' or symbol_name == "":
        symbol_name = Symbol()
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    _sw2 = price_type
    if _sw2 == PRICE_CLOSE:
        if CopyClose(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    elif _sw2 == PRICE_OPEN:
        if CopyOpen(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    elif _sw2 == PRICE_HIGH:
        if CopyHigh(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    elif _sw2 == PRICE_LOW:
        if CopyLow(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    else:
        return WRONG_VALUE
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
    _sw3 = ma_method
    if _sw3 == MODE_SMA:
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
    elif _sw3 == MODE_EMA:
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
    elif _sw3 == MODE_SMMA:
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
    elif _sw3 == MODE_LWMA:
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


class RSdynamicLine(_MQL5Indicator):
    name = 'RSdynamic_line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 14,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low'}, default=1),  # Applied price
    }

