"""VMA — converted from MQL5: MQL5 Indicators/VMA/VMA.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VMA'}, 'levels': [], 'description': [], 'name': 'VMA', 'source': 'MQL5 Indicators/VMA/VMA.mq5', 'folder': 'VMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 9, 'label': 'Period of calculation', 'sinput': False}, {'mql': 'InpSmoothing', 'py': 'InpSmoothing', 'param': 'InpSmoothing', 'type': 'uint', 'default': 2, 'label': 'Period of smoothing', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 9)  # Period of calculation
InpSmoothing = _input('InpSmoothing', 2)  # Period of smoothing
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferVMA = Arr(0, 0.0)
BufferCMO = Arr(0, 0.0)
BufferPOS = Arr(0, 0.0)
BufferNEG = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
handle_ma = 0
period_calc = 0
period_smooth = 0
sc = 0.0

def OnInit():
    global handle_ma, period_calc, period_smooth, sc
    period_calc = (1 if (InpPeriod < 1) else InpPeriod)
    period_smooth = (1 if (InpSmoothing < 1) else InpSmoothing)
    sc = _fdiv(2.0, period_smooth + 1.0)
    SetIndexBuffer(0, BufferVMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCMO, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferPOS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferNEG, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'VMA(' + _str(period_calc) + ')')
    ArraySetAsSeries(BufferVMA, True)
    ArraySetAsSeries(BufferCMO, True)
    ArraySetAsSeries(BufferPOS, True)
    ArraySetAsSeries(BufferNEG, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (period_smooth + 3):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferVMA, EMPTY_VALUE)
        ArrayInitialize(BufferCMO, EMPTY_VALUE)
        ArrayInitialize(BufferPOS, 0)
        ArrayInitialize(BufferNEG, 0)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        diff = BufferMA[i] - BufferMA[i + 1]
        if diff > 0:
            BufferPOS[i] = diff
            BufferNEG[i] = 0.0
        elif diff < 0:
            BufferPOS[i] = 0.0
            BufferNEG[i] = -diff
    for i in range(limit, 0 - 1, -1):
        s1 = iMAOnArray_u(BufferPOS, 0, period_calc, 0, MODE_SMA, i)
        s2 = iMAOnArray_u(BufferNEG, 0, period_calc, 0, MODE_SMA, i)
        value = (s1 + s2) * 100.0
        BufferCMO[i] = (_fdiv(s1 - s2, value) if (value != 0) else 0)
    abs_cmo = 0.0
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferVMA[i] = BufferMA[i]
        else:
            abs_cmo = fabs(BufferCMO[i]) * 100.0
            BufferVMA[i] = (sc * abs_cmo * BufferMA[i]) + ((1 - (sc * abs_cmo)) * BufferVMA[i + 1])
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


class VMA(_MQL5Indicator):
    name = 'VMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 9,  # Period of calculation
        'InpSmoothing': 2,  # Period of smoothing
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

