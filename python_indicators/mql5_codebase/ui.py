"""UI — converted from MQL5: MQL5 Indicators/UI/UI.mq5

Ulcer index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'UI'}, 'levels': [], 'description': ['Ulcer index'], 'name': 'UI', 'source': 'MQL5 Indicators/UI/UI.mq5', 'folder': 'UI', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpInvPair', 'py': 'InpInvPair', 'param': 'InpInvPair', 'type': 'int', 'default': 0, 'label': 'Inverse pair', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 14)  # Period
InpInvPair = _input('InpInvPair', INPUT_NO)  # Inverse pair
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferUI = Arr(0, 0.0)
BufferPD = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_ma = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    SetIndexBuffer(0, BufferUI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ulcer index(' + _str(period_ma) + ')')
    ArraySetAsSeries(BufferUI, True)
    ArraySetAsSeries(BufferPD, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 1
        ArrayInitialize(BufferUI, EMPTY_VALUE)
        ArrayInitialize(BufferPD, 0)
        ArrayInitialize(BufferMA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    index = 0
    max_ = 0.0
    Pr = 0.0
    for i in range(limit, 0 - 1, -1):
        if InpInvPair:
            index = Lowest("", PERIOD_CURRENT, InpAppliedPrice, period_ma, i)
            if index == WRONG_VALUE:
                return 0
            max_ = _fdiv(1, BufferMA[index])
            Pr = _fdiv(1, BufferMA[i])
        else:
            index = Highest("", PERIOD_CURRENT, InpAppliedPrice, period_ma, i)
            if index == WRONG_VALUE:
                return 0
            max_ = BufferMA[index]
            Pr = BufferMA[i]
        BufferPD[i] = pow(_fdiv(Pr - max_, (max_ if (max_ != 0) else DBL_MIN)), 2)
    for i in range(limit, 0 - 1, -1):
        MA = MAOnArray(BufferPD, 0, period_ma, 0, MODE_SMA, i)
        BufferUI[i] = sqrt(MA) * 100
    return rates_total

def Highest(symbol_name, timeframe, price_type, count, start):
    if symbol_name == '' or symbol_name == "":
        symbol_name = Symbol()
    array = Arr(0, 0.0)
    copied = 0
    ArraySetAsSeries(array, True)
    _sw1 = price_type
    if _sw1 == PRICE_OPEN:
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
        if CopyClose(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    return WRONG_VALUE

def Lowest(symbol_name, timeframe, price_type, count, start):
    if symbol_name == '' or symbol_name == "":
        symbol_name = Symbol()
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    _sw2 = price_type
    if _sw2 == PRICE_OPEN:
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
        if CopyClose(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
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


class UI(_MQL5Indicator):
    name = 'UI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 14,  # Period
        'InpInvPair': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Inverse pair
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

