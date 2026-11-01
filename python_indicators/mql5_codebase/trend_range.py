"""Trend_Range — converted from MQL5: MQL5 Indicators/Trend Range/Trend_Range.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [16711680], 2: [255], 3: [16711680, 255, 8421504]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Max', 2: 'Flat', 3: 'Range'}, 'levels': [], 'description': [], 'name': 'Trend_Range', 'source': 'MQL5 Indicators/Trend Range/Trend_Range.mq5', 'folder': 'Trend Range', 'inputs': [{'mql': 'InpPeriodTR', 'py': 'InpPeriodTR', 'param': 'InpPeriodTR', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 1.0, 'label': 'Deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodTR = _input('InpPeriodTR', 10)  # Period
InpMethod = _input('InpMethod', MODE_EMA)  # Method
InpDeviation = _input('InpDeviation', 1.0)  # Deviation
BufferMax = Arr(0, 0.0)
BufferFlat = Arr(0, 0.0)
BufferHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferMADevTmp = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
period_tr = 0
deviation = 0.0

def OnInit():
    global deviation, period_tr
    period_tr = (1 if (InpPeriodTR < 1) else InpPeriodTR)
    deviation = InpDeviation
    SetIndexBuffer(0, BufferMax, INDICATOR_DATA)
    SetIndexBuffer(1, BufferFlat, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMADevTmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferDev, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Range(' + _str(period_tr) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMax, True)
    ArraySetAsSeries(BufferFlat, True)
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferMADevTmp, True)
    ArraySetAsSeries(BufferDev, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 2 or Point() == 0:
        return rates_total
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMax, EMPTY_VALUE)
        ArrayInitialize(BufferFlat, EMPTY_VALUE)
        ArrayInitialize(BufferHist, 0)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferMADevTmp, EMPTY_VALUE)
        ArrayInitialize(BufferDev, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferHist[i] = _fdiv(high[i] - low[i], Point()) * tick_volume[i]
    StdDevOnArray(rates_total, prev_calculated, 0, period_tr, InpMethod, BufferMADevTmp, BufferHist, BufferDev)
    for i in range(limit, 0 - 1, -1):
        BufferMA[i] = MAOnArray(BufferHist, 0, period_tr, 0, InpMethod, i)
    for i in range(limit, 0 - 1, -1):
        MA = BufferMA[i]
        StdDev = BufferDev[i]
        max_ = MA + (StdDev * deviation)
        flat = max_ / 2
        BufferFlat[i] = flat
        BufferMax[i] = max_
        BufferColors[i] = (0 if (BufferHist[i] > max_) else 1 if (BufferHist[i] > flat) else 2)
    return rates_total

def StdDevOnArray(rates_total, prev_calculated, begin, period, method, buffer_ma_tmp, src_array, dest_buffer):
    pos = 0
    if rates_total < period:
        return 0
    as_series_arr = ArrayGetAsSeries(src_array)
    as_series_dev = ArrayGetAsSeries(dest_buffer)
    as_series_ma = ArrayGetAsSeries(buffer_ma_tmp)
    if as_series_arr:
        ArraySetAsSeries(src_array, False)
    if as_series_dev:
        ArraySetAsSeries(dest_buffer, False)
    if as_series_ma:
        ArraySetAsSeries(buffer_ma_tmp, False)
    pos = prev_calculated - 1
    if pos < period:
        pos = period - 1
        ArrayInitialize(dest_buffer, 0.0)
        ArrayInitialize(buffer_ma_tmp, 0.0)
    _sw1 = method
    if _sw1 == MODE_EMA:
        for i in range(pos, rates_total):
            if i == (period - 1):
                buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            else:
                buffer_ma_tmp[i] = ExponentialMA(i, period, buffer_ma_tmp[i - 1], src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    elif _sw1 == MODE_SMMA:
        for i in range(pos, rates_total):
            if i == (period - 1):
                buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            else:
                buffer_ma_tmp[i] = SmoothedMA(i, period, buffer_ma_tmp[i - 1], src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    elif _sw1 == MODE_LWMA:
        for i in range(pos, rates_total):
            buffer_ma_tmp[i] = LinearWeightedMA(i, period, src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    else:
        for i in range(pos, rates_total):
            buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    if as_series_arr:
        ArraySetAsSeries(src_array, True)
    if as_series_dev:
        ArraySetAsSeries(dest_buffer, True)
    if as_series_ma:
        ArraySetAsSeries(buffer_ma_tmp, True)
    return rates_total

def StdDevFunc(price, price_ma, period, position):
    dev = 0.0
    for i in range(0, period):
        dev += pow(price[position - i] - price_ma[position], 2)
    dev = sqrt(_fdiv(dev, period))
    return dev

def MAOnArray(array, total, period, ma_shift, ma_method, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period - ma_shift):
        return 0.0
    _sw2 = ma_method
    if _sw2 == MODE_SMA:
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
    elif _sw2 == MODE_EMA:
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
    elif _sw2 == MODE_SMMA:
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
    elif _sw2 == MODE_LWMA:
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


class TrendRange(_MQL5Indicator):
    name = 'Trend_Range'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodTR': 10,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
        'InpDeviation': 1.0,  # Deviation
    }

