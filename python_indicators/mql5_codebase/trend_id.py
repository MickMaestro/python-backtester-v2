"""Trend_ID — converted from MQL5: MQL5 Indicators/Trend_ID/Trend_ID.mq5

Trend identifier oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Plus deviation', 2: 'Signal', 3: 'Minus deviation'}, 'levels': [], 'description': ['Trend identifier oscillator'], 'name': 'Trend_ID', 'source': 'MQL5 Indicators/Trend_ID/Trend_ID.mq5', 'folder': 'Trend_ID', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 200, 'label': 'MA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'MA applied price', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 20, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpPeriodDev', 'py': 'InpPeriodDev', 'param': 'InpPeriodDev', 'type': 'uint', 'default': 20, 'label': 'Deviation period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 2.0, 'label': 'Deviation factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 200)  # MA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # MA applied price
InpPeriodSm = _input('InpPeriodSm', 20)  # Signal period
InpPeriodDev = _input('InpPeriodDev', 20)  # Deviation period
InpMultiplier = _input('InpMultiplier', 2.0)  # Deviation factor
BufferB1 = Arr(0, 0.0)
BufferB2 = Arr(0, 0.0)
BufferB3 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferAvgRAW = Arr(0, 0.0)
BufferDEV = Arr(0, 0.0)
BufferMADevTmp = Arr(0, 0.0)
multiplier = 0.0
period_ma = 0
period_dev = 0
period_sm = 0
handle_maP = 0
handle_ma1 = 0

def OnInit():
    global handle_ma1, handle_maP, multiplier, period_dev, period_ma, period_sm
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_dev = (1 if (InpPeriodDev < 1) else InpPeriodDev)
    period_sm = (1 if (InpPeriodSm < 1) else InpPeriodSm)
    multiplier = InpMultiplier
    SetIndexBuffer(0, BufferB1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferB2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferB3, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMAP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferAvgRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferDEV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMADevTmp, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend ID (' + _str(period_ma) + ',' + _str(period_dev) + ',' + _str(period_sm) + ',' + DoubleToString(multiplier, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferB1, True)
    ArraySetAsSeries(BufferB2, True)
    ArraySetAsSeries(BufferB3, True)
    ArraySetAsSeries(BufferMAP, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferAvgRAW, True)
    ArraySetAsSeries(BufferDEV, True)
    ArraySetAsSeries(BufferMADevTmp, True)
    ResetLastError()
    handle_maP = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 1
        ArrayInitialize(BufferB1, EMPTY_VALUE)
        ArrayInitialize(BufferB2, EMPTY_VALUE)
        ArrayInitialize(BufferB3, EMPTY_VALUE)
        ArrayInitialize(BufferMAP, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferAvgRAW, 0)
        ArrayInitialize(BufferDEV, 0)
        ArrayInitialize(BufferMADevTmp, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        MA = BufferMAP[i]
        BufferRAW[i] = (_fdiv(100.0 * (BufferMA1[i] - MA), MA) if (MA != 0) else 0)
        BufferAvgRAW[i] = GetSMA(rates_total, i, period_sm, BufferRAW)
    if StdDevOnArray(rates_total, prev_calculated, period_ma, period_dev, MODE_SMA, BufferMADevTmp, BufferAvgRAW, BufferDEV) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        StdDev = BufferDEV[i]
        BufferB1[i] = multiplier * StdDev
        BufferB2[i] = BufferAvgRAW[i]
        BufferB3[i] = -1.0 * multiplier * StdDev
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendID(_MQL5Indicator):
    name = 'Trend_ID'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 200,  # MA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA applied price
        'InpPeriodSm': 20,  # Signal period
        'InpPeriodDev': 20,  # Deviation period
        'InpMultiplier': 2.0,  # Deviation factor
    }

