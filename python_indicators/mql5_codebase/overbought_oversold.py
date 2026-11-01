"""Overbought_Oversold — converted from MQL5: MQL5 Indicators/Overbought_Oversold/Overbought_Oversold.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com/', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [8421504], 3: [8421504]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'OB/OS', 2: 'OB', 3: 'OS'}, 'levels': [], 'description': [], 'name': 'Overbought_Oversold', 'source': 'MQL5 Indicators/Overbought_Oversold/Overbought_Oversold.mq5', 'folder': 'Overbought_Oversold', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpMethod = _input('InpMethod', 0)  # Method
InpOverbought = _input('InpOverbought', 70.0)  # Overbought
InpOversold = _input('InpOversold', 30.0)  # Oversold
BufferObOs = Arr(0, 0.0)
BufferOB = Arr(0, 0.0)
BufferOS = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferST = Arr(0, 0.0)
period_ma = 0
handle_atr = 0
overbought = 0.0
oversold = 0.0

def OnInit():
    global handle_atr, overbought, oversold, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferObOs, INDICATOR_DATA)
    SetIndexBuffer(1, BufferOB, INDICATOR_DATA)
    SetIndexBuffer(2, BufferOS, INDICATOR_DATA)
    SetIndexBuffer(3, BufferATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferST, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_ma)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, period_ma)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, period_ma)
    IndicatorSetString(INDICATOR_SHORTNAME, 'OB/OS')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferObOs, True)
    ArraySetAsSeries(BufferOB, True)
    ArraySetAsSeries(BufferOS, True)
    ArraySetAsSeries(BufferATR, True)
    ArraySetAsSeries(BufferST, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_ma)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (period_ma + 1):
        return 0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferObOs, EMPTY_VALUE)
        ArrayInitialize(BufferOB, EMPTY_VALUE)
        ArrayInitialize(BufferOS, EMPTY_VALUE)
        ArrayInitialize(BufferATR, EMPTY_VALUE)
        ArrayInitialize(BufferST, EMPTY_VALUE)
    copied = 0
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferST[i] = close[i] - low[i]
    for i in range(limit, 0 - 1, -1):
        BufferObOs[i] = _fdiv(100 * MAOnArray(BufferST, 0, period_ma, 0, InpMethod, i), (BufferATR[i] if (BufferATR[i] > 0) else DBL_MIN))
    for i in range(limit, 0 - 1, -1):
        BufferOB[i] = 50 + (((overbought - 50) / 100) * MAOnArray(BufferObOs, 0, 1, 0, InpMethod, i))
        BufferOS[i] = 50 + (((oversold - 50) / 100) * MAOnArray(BufferObOs, 0, 1, 0, InpMethod, i))
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


class OverboughtOversold(_MQL5Indicator):
    name = 'Overbought_Oversold'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpOverbought': 70.0,  # Overbought
        'InpOversold': 30.0,  # Oversold
    }
    y_range = (0.0, 100.0)

