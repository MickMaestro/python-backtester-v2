"""Volatility_Band — converted from MQL5: MQL5 Indicators/Volatility_Band/Volatility_Band.mq5

Volatility Band
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [32768], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper', 2: 'Middle', 3: 'Lower'}, 'levels': [], 'description': ['Volatility Band'], 'name': 'Volatility_Band', 'source': 'MQL5 Indicators/Volatility_Band/Volatility_Band.mq5', 'folder': 'Volatility_Band', 'inputs': [{'mql': 'InpPeriodB', 'py': 'InpPeriodB', 'param': 'InpPeriodB', 'type': 'uint', 'default': 8, 'label': 'Period Band', 'sinput': False}, {'mql': 'InpPeriodV', 'py': 'InpPeriodV', 'param': 'InpPeriodV', 'type': 'uint', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 0.55, 'label': 'Deviation factor', 'sinput': False}, {'mql': 'InpAdjust', 'py': 'InpAdjust', 'param': 'InpAdjust', 'type': 'double', 'default': 0.9, 'label': 'Low band adjustment', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodB = _input('InpPeriodB', 8)  # Period Band
InpPeriodV = _input('InpPeriodV', 13)  # Period
InpDeviation = _input('InpDeviation', 0.55)  # Deviation factor
InpAdjust = _input('InpAdjust', 0.9)  # Low band adjustment
BufferUP = Arr(0, 0.0)
BufferMD = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferTMA = Arr(0, 0.0)
BufferLMA = Arr(0, 0.0)
BufferTSeries = Arr(0, 0.0)
BufferVSeries = Arr(0, 0.0)
period_b = 0
period_v = 0
deviation = 0.0
handle_tma = 0
handle_lma = 0
handle_ema = 0

def OnInit():
    global deviation, handle_ema, handle_lma, handle_tma, period_b, period_v
    period_b = (1 if (InpPeriodB < 1) else InpPeriodB)
    period_v = (1 if (InpPeriodV < 1) else InpPeriodV)
    deviation = (0.1 if (InpDeviation == 0) else InpDeviation)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(3, BufferTMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferLMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferTSeries, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferVSeries, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VBand')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferMD, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferTMA, True)
    ArraySetAsSeries(BufferLMA, True)
    ArraySetAsSeries(BufferTSeries, True)
    ArraySetAsSeries(BufferVSeries, True)
    ResetLastError()
    handle_tma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_TYPICAL)
    if handle_tma == INVALID_HANDLE:
        Print('The iMA(1) by PRICE_TYPICAL object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_lma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_LOW)
    if handle_lma == INVALID_HANDLE:
        Print('The iMA(1) by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ema = iMA(None, PERIOD_CURRENT, period_b, 0, MODE_EMA, PRICE_TYPICAL)
    if handle_ema == INVALID_HANDLE:
        Print('The iMA(', _str(period_b), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferMD, 0)
        ArrayInitialize(BufferDN, 0)
        ArrayInitialize(BufferTMA, 0)
        ArrayInitialize(BufferLMA, 0)
        ArrayInitialize(BufferTSeries, 0)
        ArrayInitialize(BufferVSeries, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ema, 0, 0, count, BufferMD)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_tma, 0, 0, count, BufferTMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_lma, 0, 0, count, BufferLMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        tp0 = BufferTMA[i]
        tp1 = BufferTMA[i + 1]
        l0 = BufferLMA[i]
        l1 = BufferLMA[i + 1]
        BufferTSeries[i] = ((tp0 - l1) if (tp0 >= tp1) else (tp1 - l0))
    for i in range(limit, 0 - 1, -1):
        BufferVSeries[i] = _fdiv(MAOnArray(BufferTSeries, 0, period_v, 0, MODE_SMA, i), deviation)
    for i in range(limit, 0 - 1, -1):
        devHigh = MAOnArray(BufferVSeries, 0, period_b, 0, MODE_EMA, i)
        devLow = devHigh * InpAdjust
        BufferDN[i] = BufferMD[i] - devLow
        BufferUP[i] = BufferMD[i] + devHigh
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


class VolatilityBand(_MQL5Indicator):
    name = 'Volatility_Band'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodB': 8,  # Period Band
        'InpPeriodV': 13,  # Period
        'InpDeviation': 0.55,  # Deviation factor
        'InpAdjust': 0.9,  # Low band adjustment
    }

