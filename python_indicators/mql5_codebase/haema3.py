"""HAEMA3 — converted from MQL5: MQL5 Indicators/HA EMA3 Indicator/HAEMA3.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [255], 3: [3329330]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'EMA0', 2: 'EMA1', 3: 'EMA2'}, 'levels': [], 'description': [], 'name': 'HAEMA3', 'source': 'MQL5 Indicators/HA EMA3 Indicator/HAEMA3.mq5', 'folder': 'HA EMA3 Indicator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpMethod = _input('InpMethod', MODE_EMA)  # Method
BufferEMA0 = Arr(0, 0.0)
BufferEMA1 = Arr(0, 0.0)
BufferEMA2 = Arr(0, 0.0)
BufferOpen = Arr(0, 0.0)
BufferClose = Arr(0, 0.0)
period_ma = 0

def OnInit():
    global period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferEMA0, INDICATOR_DATA)
    SetIndexBuffer(1, BufferEMA1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferEMA2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferOpen, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferClose, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'HAEma3(' + _str(period_ma) + ')')
    ArraySetAsSeries(BufferEMA0, True)
    ArraySetAsSeries(BufferEMA1, True)
    ArraySetAsSeries(BufferEMA2, True)
    ArraySetAsSeries(BufferOpen, True)
    ArraySetAsSeries(BufferClose, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferEMA0, EMPTY_VALUE)
        ArrayInitialize(BufferEMA1, EMPTY_VALUE)
        ArrayInitialize(BufferEMA2, EMPTY_VALUE)
        ArrayInitialize(BufferOpen, 0)
        ArrayInitialize(BufferClose, 0)
    for i in range(limit, 0 - 1, -1):
        BufferOpen[i] = (((open[i + 1] + high[i + 1] + low[i + 1] + close[i + 1]) / 4) + BufferOpen[i + 1]) / 2
        BufferClose[i] = (((open[i] + high[i] + low[i] + close[i]) / 4) + BufferOpen[i] + fmax(high[i], BufferOpen[i]) + fmin(low[i], BufferOpen[i])) / 4
    for i in range(limit, 0 - 1, -1):
        BufferEMA1[i] = MAOnArray(BufferClose, 0, period_ma, 0, InpMethod, i)
    for i in range(limit, 0 - 1, -1):
        BufferEMA2[i] = MAOnArray(BufferEMA1, 0, period_ma, 0, InpMethod, i)
    for i in range(limit, 0 - 1, -1):
        BufferEMA0[i] = MAOnArray(BufferEMA2, 0, period_ma, 0, InpMethod, i)
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


class HAEMA3(_MQL5Indicator):
    name = 'HAEMA3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
    }

