"""SHL_MA_Band — converted from MQL5: MQL5 Indicators/SHL_MA_Band/SHL_MA_Band.mq5

Smoothed High/Low Linear regression band
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 11, 2: 1, 3: 1}, 'colors': {1: [255, 55295, 16711935, 3329330, 7504122], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 2, 2: 0, 3: 0}, 'labels': {1: 'Upper Band;Lower Band', 2: 'High', 3: 'Low'}, 'levels': [], 'description': ['Smoothed High/Low Linear regression band'], 'name': 'SHL_MA_Band', 'source': 'MQL5 Indicators/SHL_MA_Band/SHL_MA_Band.mq5', 'folder': 'SHL_MA_Band', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 15, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 15)  # Period
InpMethod = _input('InpMethod', MODE_EMA)  # Method
BufferHIST1 = Arr(0, 0.0)
BufferHIST2 = Arr(0, 0.0)
BufferHISTColors = Arr(0, 0.0)
BufferH = Arr(0, 0.0)
BufferL = Arr(0, 0.0)
BufferMAH = Arr(0, 0.0)
BufferMAL = Arr(0, 0.0)
BufferLRLH = Arr(0, 0.0)
BufferLRLL = Arr(0, 0.0)
period_ma = 0
handle_mah = 0
handle_mal = 0

def OnInit():
    global handle_mah, handle_mal, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferHIST1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHIST2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHISTColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, BufferH, INDICATOR_DATA)
    SetIndexBuffer(4, BufferL, INDICATOR_DATA)
    SetIndexBuffer(5, BufferMAH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMAL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferLRLH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferLRLL, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SHLLRB(' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferHIST1, True)
    ArraySetAsSeries(BufferHIST2, True)
    ArraySetAsSeries(BufferHISTColors, True)
    ArraySetAsSeries(BufferH, True)
    ArraySetAsSeries(BufferL, True)
    ArraySetAsSeries(BufferMAH, True)
    ArraySetAsSeries(BufferMAL, True)
    ArraySetAsSeries(BufferLRLH, True)
    ArraySetAsSeries(BufferLRLL, True)
    ResetLastError()
    handle_mah = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_HIGH)
    if handle_mah == INVALID_HANDLE:
        Print('The iMA(1) by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_mal = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_LOW)
    if handle_mal == INVALID_HANDLE:
        Print('The iMA(1) by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 2
        ArrayInitialize(BufferHIST1, EMPTY_VALUE)
        ArrayInitialize(BufferHIST2, EMPTY_VALUE)
        ArrayInitialize(BufferH, EMPTY_VALUE)
        ArrayInitialize(BufferL, EMPTY_VALUE)
        ArrayInitialize(BufferMAH, EMPTY_VALUE)
        ArrayInitialize(BufferMAL, EMPTY_VALUE)
        ArrayInitialize(BufferLRLH, 0)
        ArrayInitialize(BufferLRLL, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_mah, 0, 0, count, BufferMAH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mal, 0, 0, count, BufferMAL)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        x = 0.0
        x2 = 0.0
        yH = 0.0
        xyH = 0.0
        yL = 0.0
        xyL = 0.0
        for j in range(0, period_ma):
            yH += BufferMAH[i + j]
            xyH += BufferMAH[i + j] * j
            yL += BufferMAL[i + j]
            xyL += BufferMAL[i + j] * j
            x += j
            x2 += j * j
        temp = (period_ma * x2) - (x * x)
        mH = _fdiv((period_ma * xyH) - (x * yH), (temp if (temp != 0) else DBL_MIN))
        yintH = _fdiv(yH + (mH * x), period_ma)
        mL = _fdiv((period_ma * xyL) - (x * yL), (temp if (temp != 0) else DBL_MIN))
        yintL = _fdiv(yL + (mL * x), period_ma)
        BufferLRLH[i] = yintH - (mH * period_ma)
        BufferLRLL[i] = yintL - (mL * period_ma)
    for i in range(limit, 0 - 1, -1):
        BufferHIST1[i] = MAOnArray(BufferLRLH, 0, period_ma, 0, InpMethod, i)
        BufferH[i] = BufferHIST1[i]
        BufferHIST2[i] = MAOnArray(BufferLRLL, 0, period_ma, 0, InpMethod, i)
        BufferL[i] = BufferHIST2[i]
        if BufferH[i] > BufferH[i + 1]:
            BufferHISTColors[i] = (1 if (BufferL[i] > BufferL[i + 1]) else 0)
        else:
            BufferHISTColors[i] = (3 if (BufferL[i] > BufferL[i + 1]) else 2)
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


class SHLMABand(_MQL5Indicator):
    name = 'SHL_MA_Band'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 15,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
    }

