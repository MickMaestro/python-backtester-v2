"""ZeroLagMACD — converted from MQL5: MQL5 Indicators/ZeroLagMACD/ZeroLagMACD.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [255], 2: [16711680], 3: [3329330, 17919]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'MACD', 2: 'Signal', 3: 'Histogram'}, 'levels': [], 'description': [], 'name': 'ZeroLagMACD', 'source': 'MQL5 Indicators/ZeroLagMACD/ZeroLagMACD.mq5', 'folder': 'ZeroLagMACD', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 12, 'label': 'Period of the Fast EMA', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 24, 'label': 'Period of the Slow EMA', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 9, 'label': 'Period of the signal line', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 12)  # Period of the Fast EMA
InpPeriodSlow = _input('InpPeriodSlow', 24)  # Period of the Slow EMA
InpPeriodSig = _input('InpPeriodSig', 9)  # Period of the signal line
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferMACD = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferHistogram = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferFastEMA = Arr(0, 0.0)
BufferSlowEMA = Arr(0, 0.0)
BufferFastOnArray = Arr(0, 0.0)
BufferSlowOnArray = Arr(0, 0.0)
BufferSignalOnArray = Arr(0, 0.0)
handle_fast_ema = 0
handle_slow_ema = 0
handle_fast_on_array = 0
handle_slow_on_array = 0
period_fast_ema = 0
period_slow_ema = 0
period_signal = 0

def OnInit():
    global handle_fast_ema, handle_fast_on_array, handle_slow_ema, handle_slow_on_array, period_fast_ema, period_signal, period_slow_ema
    period_fast_ema = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow_ema = (1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_signal = (1 if (InpPeriodSig < 1) else InpPeriodSig)
    SetIndexBuffer(0, BufferMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHistogram, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferFastEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSlowEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferFastOnArray, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSlowOnArray, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferSignalOnArray, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Zero lag MACD(' + _str(period_fast_ema) + ',' + _str(period_slow_ema) + ',' + _str(period_signal) + ')')
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferHistogram, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferFastEMA, True)
    ArraySetAsSeries(BufferSlowEMA, True)
    ArraySetAsSeries(BufferFastOnArray, True)
    ArraySetAsSeries(BufferSlowOnArray, True)
    ArraySetAsSeries(BufferSignalOnArray, True)
    ResetLastError()
    handle_fast_ema = iMA(Symbol(), PERIOD_CURRENT, period_fast_ema, 0, MODE_EMA, InpAppliedPrice)
    if handle_fast_ema == INVALID_HANDLE:
        Print('The iMA(', _str(period_fast_ema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_slow_ema = iMA(Symbol(), PERIOD_CURRENT, period_slow_ema, 0, MODE_EMA, InpAppliedPrice)
    if handle_slow_ema == INVALID_HANDLE:
        Print('The iMA(', _str(period_slow_ema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_fast_on_array = iMA(Symbol(), PERIOD_CURRENT, period_fast_ema, 0, MODE_EMA, handle_fast_ema)
    if handle_fast_on_array == INVALID_HANDLE:
        Print('The iMAOnArray(', _str(period_fast_ema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_slow_on_array = iMA(Symbol(), PERIOD_CURRENT, period_slow_ema, 0, MODE_EMA, handle_slow_ema)
    if handle_slow_on_array == INVALID_HANDLE:
        Print('The iMAOnArray(', _str(period_slow_ema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    limit2 = limit
    if limit > 1:
        limit = rates_total - 1
        limit2 = rates_total - 2
        ArrayInitialize(BufferMACD, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferHistogram, EMPTY_VALUE)
        ArrayInitialize(BufferColors, EMPTY_VALUE)
        ArrayInitialize(BufferFastEMA, EMPTY_VALUE)
        ArrayInitialize(BufferSlowEMA, EMPTY_VALUE)
        ArrayInitialize(BufferFastOnArray, EMPTY_VALUE)
        ArrayInitialize(BufferSlowOnArray, EMPTY_VALUE)
        ArrayInitialize(BufferSignalOnArray, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_fast_ema, 0, 0, count, BufferFastEMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_slow_ema, 0, 0, count, BufferSlowEMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_fast_on_array, 0, 0, count, BufferFastOnArray)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_slow_on_array, 0, 0, count, BufferSlowOnArray)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMACD[i] = _fdiv((2 * BufferFastEMA[i]) - BufferFastOnArray[i] - (2 * BufferSlowEMA[i]) + BufferSlowOnArray[i], Point())
    for i in range(limit, 0 - 1, -1):
        BufferSignalOnArray[i] = iMAOnArray_u(BufferMACD, 0, period_signal, 0, MODE_EMA, i)
    for i in range(limit2, 0 - 1, -1):
        BufferSignal[i] = (2 * BufferSignalOnArray[i]) - iMAOnArray_u(BufferSignalOnArray, 0, period_signal, 0, MODE_EMA, i)
        BufferHistogram[i] = BufferMACD[i] - BufferSignal[i]
        if BufferHistogram[i] < BufferHistogram[i + 1]:
            BufferColors[i] = 1.0
        else:
            BufferColors[i] = 0.0
    return rates_total

def iMAOnArray_u(array, total, period, ma_shift, ma_method, shift):
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


class ZeroLagMACD(_MQL5Indicator):
    name = 'ZeroLagMACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 12,  # Period of the Fast EMA
        'InpPeriodSlow': 24,  # Period of the Slow EMA
        'InpPeriodSig': 9,  # Period of the signal line
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

