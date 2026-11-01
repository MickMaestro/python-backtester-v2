"""Adaptable_MACD — converted from MQL5: MQL5 Indicators/Adaptable_MACD/Adaptable_MACD.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [255], 2: [16711680], 3: [32768, 255]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'MACD', 2: 'SIG', 3: 'HIST'}, 'levels': [], 'description': [], 'name': 'Adaptable_MACD', 'source': 'MQL5 Indicators/Adaptable_MACD/Adaptable_MACD.mq5', 'folder': 'Adaptable_MACD', 'inputs': [{'mql': 'InpPeriodFastMA', 'py': 'InpPeriodFastMA', 'param': 'InpPeriodFastMA', 'type': 'uint', 'default': 12, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlowMA', 'py': 'InpPeriodSlowMA', 'param': 'InpPeriodSlowMA', 'type': 'uint', 'default': 26, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpPeriodSignalMA', 'py': 'InpPeriodSignalMA', 'param': 'InpPeriodSignalMA', 'type': 'uint', 'default': 9, 'label': 'Signal line period', 'sinput': False}, {'mql': 'InpMethodFastMA', 'py': 'InpMethodFastMA', 'param': 'InpMethodFastMA', 'type': 'int', 'default': 0, 'label': 'Fast MA calculation method', 'sinput': False}, {'mql': 'InpMethodSlowMA', 'py': 'InpMethodSlowMA', 'param': 'InpMethodSlowMA', 'type': 'int', 'default': 0, 'label': 'Slow MA calculation method', 'sinput': False}, {'mql': 'InpMethodSignal', 'py': 'InpMethodSignal', 'param': 'InpMethodSignal', 'type': 'int', 'default': 0, 'label': 'Signal line calculation method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpAbsValue', 'py': 'InpAbsValue', 'param': 'InpAbsValue', 'type': 'int', 'default': 1, 'label': 'Use absolute values', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodFastMA = _input('InpPeriodFastMA', 12)  # Fast MA period
InpPeriodSlowMA = _input('InpPeriodSlowMA', 26)  # Slow MA period
InpPeriodSignalMA = _input('InpPeriodSignalMA', 9)  # Signal line period
InpMethodFastMA = _input('InpMethodFastMA', MODE_SMA)  # Fast MA calculation method
InpMethodSlowMA = _input('InpMethodSlowMA', MODE_SMA)  # Slow MA calculation method
InpMethodSignal = _input('InpMethodSignal', MODE_SMA)  # Signal line calculation method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpAbsValue = _input('InpAbsValue', INPUT_YES)  # Use absolute values
BufferMACD = Arr(0, 0.0)
BufferSIG = Arr(0, 0.0)
BufferHIST = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferFastMA = Arr(0, 0.0)
BufferSlowMA = Arr(0, 0.0)
period_fast_ma = 0
period_slow_ma = 0
period_signal = 0
handle_fast_ma = 0
handle_slow_ma = 0

def OnInit():
    global handle_fast_ma, handle_slow_ma, period_fast_ma, period_signal, period_slow_ma
    period_fast_ma = (1 if (InpPeriodFastMA < 1) else InpPeriodFastMA)
    period_slow_ma = (1 if (InpPeriodSlowMA < 1) else InpPeriodSlowMA)
    period_signal = (1 if (InpPeriodSignalMA < 1) else InpPeriodSignalMA)
    SetIndexBuffer(0, BufferMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSIG, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHIST, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferFastMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSlowMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adaptable MACD(' + _str(period_fast_ma) + ',' + _str(period_slow_ma) + ',' + _str(period_signal) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferSIG, True)
    ArraySetAsSeries(BufferHIST, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferFastMA, True)
    ArraySetAsSeries(BufferSlowMA, True)
    ResetLastError()
    handle_fast_ma = iMA(None, PERIOD_CURRENT, period_fast_ma, 0, InpMethodFastMA, InpAppliedPrice)
    if handle_fast_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fast_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_slow_ma = iMA(None, PERIOD_CURRENT, period_slow_ma, 0, InpMethodSlowMA, InpAppliedPrice)
    if handle_slow_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_slow_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferMACD, EMPTY_VALUE)
        ArrayInitialize(BufferSIG, EMPTY_VALUE)
        ArrayInitialize(BufferHIST, EMPTY_VALUE)
        ArrayInitialize(BufferFastMA, EMPTY_VALUE)
        ArrayInitialize(BufferSlowMA, EMPTY_VALUE)
    copied = 0
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_fast_ma, 0, 0, count, BufferFastMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_slow_ma, 0, 0, count, BufferSlowMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMACD[i] = ((BufferFastMA[i] - BufferSlowMA[i]) if InpAbsValue else _fdiv(BufferFastMA[i] - BufferSlowMA[i], (BufferSlowMA[i] if (BufferSlowMA[i] != 0) else DBL_MIN)))
    for i in range(limit, 0 - 1, -1):
        BufferSIG[i] = MAOnArray(BufferMACD, 0, period_signal, 0, InpMethodSignal, i)
        BufferHIST[i] = BufferMACD[i] - BufferSIG[i]
        if BufferHIST[i] > BufferHIST[i + 1]:
            BufferColors[i] = 0.0
        else:
            BufferColors[i] = 1.0
    return rates_total

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


class AdaptableMACD(_MQL5Indicator):
    name = 'Adaptable_MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastMA': 12,  # Fast MA period
        'InpPeriodSlowMA': 26,  # Slow MA period
        'InpPeriodSignalMA': 9,  # Signal line period
        'InpMethodFastMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Fast MA calculation method
        'InpMethodSlowMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Slow MA calculation method
        'InpMethodSignal': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal line calculation method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpAbsValue': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use absolute values
    }

