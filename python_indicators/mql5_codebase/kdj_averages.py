"""KDJ_Averages — converted from MQL5: MQL5 Indicators/KDJ_Averages/KDJ_Averages.mq5

KDJ averages oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [32768], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'K Avg', 2: 'D Avg', 3: 'J Avg'}, 'levels': [], 'description': ['KDJ averages oscillator'], 'name': 'KDJ_Averages', 'source': 'MQL5 Indicators/KDJ_Averages/KDJ_Averages.mq5', 'folder': 'KDJ_Averages', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 9, 'label': 'KDJ period', 'sinput': False}, {'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 3, 'label': 'K period', 'sinput': False}, {'mql': 'InpMethodK', 'py': 'InpMethodK', 'param': 'InpMethodK', 'type': 'int', 'default': 0, 'label': 'K method', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': 'D period', 'sinput': False}, {'mql': 'InpMethodD', 'py': 'InpMethodD', 'param': 'InpMethodD', 'type': 'int', 'default': 0, 'label': 'D method', 'sinput': False}, {'mql': 'InpThreshold', 'py': 'InpThreshold', 'param': 'InpThreshold', 'type': 'double', 'default': 50.0, 'label': 'Threshold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 9)  # KDJ period
InpPeriodK = _input('InpPeriodK', 3)  # K period
InpMethodK = _input('InpMethodK', MODE_SMA)  # K method
InpPeriodD = _input('InpPeriodD', 3)  # D period
InpMethodD = _input('InpMethodD', MODE_SMA)  # D method
InpThreshold = _input('InpThreshold', 50.0)  # Threshold
BufferK = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
BufferJ = Arr(0, 0.0)
BufferRSV = Arr(0, 0.0)
threshold = 0.0
period_kdj = 0
period_ksm = 0
period_dsm = 0
period_max = 0
weight_sum_k = 0
weight_sum_d = 0

def OnInit():
    global period_dsm, period_kdj, period_ksm, period_max, threshold
    period_kdj = _int(InpPeriod)
    period_ksm = (2 if (InpPeriodK < 2) else InpPeriodK)
    period_dsm = (2 if (InpPeriodD < 2) else InpPeriodD)
    period_max = fmax(period_kdj, fmax(period_ksm, period_dsm))
    threshold = (0 if (InpThreshold < 0) else 100 if (InpThreshold > 100) else InpThreshold)
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferJ, INDICATOR_DATA)
    SetIndexBuffer(3, BufferRSV, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KDJ averages (' + _str(period_kdj) + ',' + _str(period_ksm) + ',' + _str(period_dsm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, threshold)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferJ, True)
    ArraySetAsSeries(BufferRSV, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_kdj - 1
        ArrayInitialize(BufferK, 0)
        ArrayInitialize(BufferD, 0)
        ArrayInitialize(BufferJ, 0)
    for i in range(limit, 0 - 1, -1):
        Cn = close[i]
        bl = Lowest(period_kdj, i)
        bh = Highest(period_kdj, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        Ln = fmin(Cn, low[bl])
        Hn = fmax(Cn, high[bh])
        BufferRSV[i] = (_fdiv(100.0 * (Cn - Ln), Hn - Ln) if (Hn != Ln) else 50.0)
    _sw1 = InpMethodK
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_kdj, period_ksm, BufferRSV, BufferK) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_kdj, period_ksm, BufferRSV, BufferK) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_kdj, period_ksm, BufferRSV, BufferK, _GlobRef(globals(), 'weight_sum_k')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_kdj, period_ksm, BufferRSV, BufferK) == 0:
            return 0
    _sw2 = InpMethodD
    if _sw2 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_ksm, period_dsm, BufferK, BufferD) == 0:
            return 0
    elif _sw2 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_ksm, period_dsm, BufferK, BufferD) == 0:
            return 0
    elif _sw2 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ksm, period_dsm, BufferK, BufferD, _GlobRef(globals(), 'weight_sum_d')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_ksm, period_dsm, BufferK, BufferD) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferJ[i] = (3.0 * BufferD[i]) - (2.0 * BufferK[i])
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KDJAverages(_MQL5Indicator):
    name = 'KDJ_Averages'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 9,  # KDJ period
        'InpPeriodK': 3,  # K period
        'InpMethodK': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # K method
        'InpPeriodD': 3,  # D period
        'InpMethodD': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # D method
        'InpThreshold': 50.0,  # Threshold
    }

