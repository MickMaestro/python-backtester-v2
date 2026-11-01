"""Candle_Ratio — converted from MQL5: MQL5 Indicators/Candle_Ratio/Candle_Ratio.mq5

Candle ratio
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Ratio', 2: 'MA'}, 'levels': [], 'description': ['Candle ratio'], 'name': 'Candle_Ratio', 'source': 'MQL5 Indicators/Candle_Ratio/Candle_Ratio.mq5', 'folder': 'Candle_Ratio', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 21, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 21, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 21)  # Period
InpPeriodMA = _input('InpPeriodMA', 21)  # Smoothing period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
BufferRatio = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
period_ma = 0
period_ma_sm = 0

def OnInit():
    global period_ma, period_ma_sm
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    period_ma_sm = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    SetIndexBuffer(0, BufferRatio, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(2, BufferUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferDN, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Candle ratio(' + _str(period_ma) + ',' + _str(period_ma_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRatio, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferRatio, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferUP, 0)
        ArrayInitialize(BufferDN, 0)
    for i in range(limit, 0 - 1, -1):
        if close[i] > open[i]:
            BufferUP[i] = close[i] - open[i]
            BufferDN[i] = 0.0
        else:
            BufferDN[i] = open[i] - close[i]
            BufferUP[i] = 0.0
    for i in range(limit, 0 - 1, -1):
        SUp = MAOnArray(BufferUP, 0, period_ma, 0, MODE_SMA, i)
        SDn = MAOnArray(BufferDN, 0, period_ma, 0, MODE_SMA, i)
        BufferRatio[i] = (_fdiv(SUp, SDn) if (SDn != 0) else 0)
    for i in range(limit, 0 - 1, -1):
        BufferMA[i] = MAOnArray(BufferRatio, 0, period_ma_sm, 0, InpMethod, i)
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


class CandleRatio(_MQL5Indicator):
    name = 'Candle_Ratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 21,  # Period
        'InpPeriodMA': 21,  # Smoothing period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
    }

