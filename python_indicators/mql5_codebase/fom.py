"""FoM — converted from MQL5: MQL5 Indicators/FoM/FoM.mq5

Freedom of Movement oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14772545]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'FoM'}, 'levels': [], 'description': ['Freedom of Movement oscillator'], 'name': 'FoM', 'source': 'MQL5 Indicators/FoM/FoM.mq5', 'folder': 'FoM', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
BufferFoM = Arr(0, 0.0)
BufferRV = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferAMove = Arr(0, 0.0)
BufferVByM = Arr(0, 0.0)
BufferMADevTmp = Arr(0, 0.0)
BufferAvgVol = Arr(0, 0.0)
BufferDevVol = Arr(0, 0.0)
BufferAvgVByM = Arr(0, 0.0)
BufferDevVByM = Arr(0, 0.0)
K = 0.0
period_ind = 0
weight_sum = 0
weight_sum2 = 0

def OnInit():
    global period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferFoM, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAMove, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferVByM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMADevTmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferAvgVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferDevVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferAvgVByM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferDevVByM, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FoM (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferFoM, True)
    ArraySetAsSeries(BufferRV, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferAMove, True)
    ArraySetAsSeries(BufferVByM, True)
    ArraySetAsSeries(BufferMADevTmp, True)
    ArraySetAsSeries(BufferAvgVol, True)
    ArraySetAsSeries(BufferDevVol, True)
    ArraySetAsSeries(BufferAvgVByM, True)
    ArraySetAsSeries(BufferDevVByM, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global K
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_ind, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ind - 2
        ArrayInitialize(BufferFoM, EMPTY_VALUE)
        ArrayInitialize(BufferRV, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferAMove, 0)
        ArrayInitialize(BufferVByM, 0)
        ArrayInitialize(BufferMADevTmp, 0)
        ArrayInitialize(BufferAvgVol, 0)
        ArrayInitialize(BufferDevVol, 0)
        ArrayInitialize(BufferAvgVByM, 0)
        ArrayInitialize(BufferDevVByM, 0)
    K = ceil(100.0 * tick_volume[0])
    for i in range(limit, 0 - 1, -1):
        BufferVol[i] = _fdiv(tick_volume[i], K)
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVol, BufferAvgVol) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVol, BufferAvgVol) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferVol, BufferAvgVol, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVol, BufferAvgVol) == 0:
            return 0
    if StdDevOnArray(rates_total, prev_calculated, 0, period_ind, InpMethod, BufferMADevTmp, BufferVol, BufferDevVol) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        MA = BufferAvgVol[i]
        StdDev = BufferDevVol[i]
        BufferRV[i] = (_fdiv(BufferVol[i] - MA, StdDev) if (StdDev != 0) else 0)
        BufferAMove[i] = (_fdiv(fabs(close[i] - close[i + 1]), close[i + 1]) if (close[i + 1] != 0) else 0)
        bl = ArrayMinimum(BufferAMove, i, period_ind)
        bh = ArrayMaximum(BufferAMove, i, period_ind)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        Min = BufferAMove[bl]
        Max = BufferAMove[bh]
        denom = ((Max - Min) if ((Max - Min) != 0) else -1)
        Move = 1.0 + _fdiv(9.0 * (BufferAMove[i] - Min), fabs(denom))
        bl = ArrayMinimum(BufferRV, i, period_ind)
        bh = ArrayMaximum(BufferRV, i, period_ind)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        MinV = BufferRV[bl]
        MaxV = BufferRV[bh]
        denomV = ((MaxV - MinV) if ((MaxV - MinV) != 0) else -1)
        V = 1.0 + _fdiv(9.0 * (BufferRV[i] - MinV), fabs(denomV))
        BufferVByM[i] = _fdiv(V, 10.0 * Move)
    _sw2 = InpMethod
    if _sw2 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVByM, BufferAvgVByM) == 0:
            return 0
    elif _sw2 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVByM, BufferAvgVByM) == 0:
            return 0
    elif _sw2 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferVByM, BufferAvgVByM, _GlobRef(globals(), 'weight_sum2')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVByM, BufferAvgVByM) == 0:
            return 0
    if StdDevOnArray(rates_total, prev_calculated, 0, period_ind, InpMethod, BufferMADevTmp, BufferVByM, BufferDevVByM) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferFoM[i] = (_fdiv(BufferVByM[i] - BufferAvgVByM[i], BufferDevVByM[i]) if (BufferDevVByM[i] != 0) else 0)
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
    _sw3 = method
    if _sw3 == MODE_EMA:
        for i in range(pos, rates_total):
            if i == (period - 1):
                buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            else:
                buffer_ma_tmp[i] = ExponentialMA(i, period, buffer_ma_tmp[i - 1], src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    elif _sw3 == MODE_SMMA:
        for i in range(pos, rates_total):
            if i == (period - 1):
                buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            else:
                buffer_ma_tmp[i] = SmoothedMA(i, period, buffer_ma_tmp[i - 1], src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    elif _sw3 == MODE_LWMA:
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


class FoM(_MQL5Indicator):
    name = 'FoM'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
    }

