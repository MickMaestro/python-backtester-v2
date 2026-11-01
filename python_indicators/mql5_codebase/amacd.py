"""AMACD — converted from MQL5: MQL5 Indicators/AMACD/AMACD.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 10, 2: 1}, 'colors': {1: [3329330, 255], 2: [16711680]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'MACD', 2: 'Signal'}, 'levels': [], 'description': [], 'name': 'AMACD', 'source': 'MQL5 Indicators/AMACD/AMACD.mq5', 'folder': 'AMACD', 'inputs': [{'mql': 'InpPeriodFastAMA', 'py': 'InpPeriodFastAMA', 'param': 'InpPeriodFastAMA', 'type': 'uint', 'default': 6, 'label': 'Period of the Fast AMA', 'sinput': False}, {'mql': 'InpFastFastAMA', 'py': 'InpFastFastAMA', 'param': 'InpFastFastAMA', 'type': 'uint', 'default': 2, 'label': 'Fast EMA of the Fast AMA', 'sinput': False}, {'mql': 'InpSlowFastAMA', 'py': 'InpSlowFastAMA', 'param': 'InpSlowFastAMA', 'type': 'uint', 'default': 13, 'label': 'Slow EMA of the Fast AMA', 'sinput': False}, {'mql': 'InpPeriodSlowAMA', 'py': 'InpPeriodSlowAMA', 'param': 'InpPeriodSlowAMA', 'type': 'uint', 'default': 13, 'label': 'Period of the Slow AMA', 'sinput': False}, {'mql': 'InpFastSlowAMA', 'py': 'InpFastSlowAMA', 'param': 'InpFastSlowAMA', 'type': 'uint', 'default': 6, 'label': 'Fast EMA of the Slow AMA', 'sinput': False}, {'mql': 'InpSlowSlowAMA', 'py': 'InpSlowSlowAMA', 'param': 'InpSlowSlowAMA', 'type': 'uint', 'default': 30, 'label': 'Slow EMA of the Slow AMA', 'sinput': False}, {'mql': 'InpPeriodSignal', 'py': 'InpPeriodSignal', 'param': 'InpPeriodSignal', 'type': 'uint', 'default': 5, 'label': 'The signal line period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFastAMA = _input('InpPeriodFastAMA', 6)  # Period of the Fast AMA
InpFastFastAMA = _input('InpFastFastAMA', 2)  # Fast EMA of the Fast AMA
InpSlowFastAMA = _input('InpSlowFastAMA', 13)  # Slow EMA of the Fast AMA
InpPeriodSlowAMA = _input('InpPeriodSlowAMA', 13)  # Period of the Slow AMA
InpFastSlowAMA = _input('InpFastSlowAMA', 6)  # Fast EMA of the Slow AMA
InpSlowSlowAMA = _input('InpSlowSlowAMA', 30)  # Slow EMA of the Slow AMA
InpPeriodSignal = _input('InpPeriodSignal', 5)  # The signal line period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferMACD = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferFastAMA = Arr(0, 0.0)
BufferSlowAMA = Arr(0, 0.0)
period_fast_ama = 0
fast_fast_ama = 0
slow_fast_ama = 0
period_slow_ama = 0
fast_slow_ama = 0
slow_slow_ama = 0
period_signal = 0
handle_fast_ama = 0
handle_slow_ama = 0

def OnInit():
    global fast_fast_ama, fast_slow_ama, handle_fast_ama, handle_slow_ama, period_fast_ama, period_signal, period_slow_ama, slow_fast_ama, slow_slow_ama
    period_fast_ama = (1 if (InpPeriodFastAMA < 1) else InpPeriodFastAMA)
    period_slow_ama = ((period_fast_ama + 1) if (InpPeriodSlowAMA <= _uint(period_fast_ama)) else InpPeriodSlowAMA)
    fast_fast_ama = (1 if (InpFastFastAMA < 1) else InpFastFastAMA)
    slow_fast_ama = (1 if (InpSlowFastAMA < 1) else InpSlowFastAMA)
    fast_slow_ama = (1 if (InpFastSlowAMA < 1) else InpFastSlowAMA)
    slow_slow_ama = (1 if (InpSlowSlowAMA < 1) else InpSlowSlowAMA)
    period_signal = (1 if (InpPeriodSignal < 1) else InpPeriodSignal)
    short_name = 'AMACD(' + _str(period_fast_ama) + ',' + _str(fast_fast_ama) + ',' + _str(slow_fast_ama) + ',' + _str(period_slow_ama) + ',' + _str(fast_slow_ama) + ',' + _str(slow_slow_ama) + ',' + _str(period_signal) + ')'
    SetIndexBuffer(0, BufferMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(3, BufferFastAMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSlowAMA, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferFastAMA, True)
    ArraySetAsSeries(BufferSlowAMA, True)
    ResetLastError()
    handle_fast_ama = iAMA(Symbol(), PERIOD_CURRENT, period_fast_ama, fast_fast_ama, slow_fast_ama, 0, InpAppliedPrice)
    if handle_fast_ama == INVALID_HANDLE:
        Print('The iAMA(', _str(period_fast_ama), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_slow_ama = iAMA(Symbol(), PERIOD_CURRENT, period_slow_ama, fast_slow_ama, slow_slow_ama, 0, InpAppliedPrice)
    if handle_fast_ama == INVALID_HANDLE:
        Print('The iAMA(', _str(period_slow_ama), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_slow_ama:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMACD, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 0)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferFastAMA, EMPTY_VALUE)
        ArrayInitialize(BufferSlowAMA, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_fast_ama, 0, 0, count, BufferFastAMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_slow_ama, 0, 0, count, BufferSlowAMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMACD[i] = BufferFastAMA[i] - BufferSlowAMA[i]
    for i in range(limit, 0 - 1, -1):
        BufferSignal[i] = iMAOnArray_u(BufferMACD, 0, period_signal, 0, MODE_SMA, i)
        hist = BufferMACD[i] - BufferSignal[i]
        if hist < 0:
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


class AMACD(_MQL5Indicator):
    name = 'AMACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastAMA': 6,  # Period of the Fast AMA
        'InpFastFastAMA': 2,  # Fast EMA of the Fast AMA
        'InpSlowFastAMA': 13,  # Slow EMA of the Fast AMA
        'InpPeriodSlowAMA': 13,  # Period of the Slow AMA
        'InpFastSlowAMA': 6,  # Fast EMA of the Slow AMA
        'InpSlowSlowAMA': 30,  # Slow EMA of the Slow AMA
        'InpPeriodSignal': 5,  # The signal line period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

