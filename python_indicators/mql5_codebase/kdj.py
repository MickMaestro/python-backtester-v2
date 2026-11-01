"""KDJ — converted from MQL5: MQL5 Indicators/KDJ/KDJ.mq5

KDJ oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [32768], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'K', 2: 'D', 3: 'J'}, 'levels': [], 'description': ['KDJ oscillator'], 'name': 'KDJ', 'source': 'MQL5 Indicators/KDJ/KDJ.mq5', 'folder': 'KDJ', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 9, 'label': 'Period', 'sinput': False}, {'mql': 'InpFactor1', 'py': 'InpFactor1', 'param': 'InpFactor1', 'type': 'double', 'default': 0.666666, 'label': 'KFactor', 'sinput': False}, {'mql': 'InpFactor2', 'py': 'InpFactor2', 'param': 'InpFactor2', 'type': 'double', 'default': 0.333333, 'label': 'DFactor', 'sinput': False}, {'mql': 'InpThreshold', 'py': 'InpThreshold', 'param': 'InpThreshold', 'type': 'double', 'default': 50.0, 'label': 'Threshold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 9)  # Period
InpFactor1 = _input('InpFactor1', 0.666666)  # KFactor
InpFactor2 = _input('InpFactor2', 0.333333)  # DFactor
InpThreshold = _input('InpThreshold', 50.0)  # Threshold
BufferK = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
BufferJ = Arr(0, 0.0)
factor1 = 0.0
factor2 = 0.0
threshold = 0.0
period = 0

def OnInit():
    global factor1, factor2, period, threshold
    period = _int(InpPeriod)
    factor1 = (0.01 if (InpFactor1 < 0.01) else InpFactor1)
    factor2 = (0.01 if (InpFactor2 < 0.01) else InpFactor2)
    threshold = (0 if (InpThreshold < 0) else 100 if (InpThreshold > 100) else InpThreshold)
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferJ, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KDJ (' + _str(period) + ',' + DoubleToString(factor1, 6) + ',' + DoubleToString(factor2, 6) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, threshold)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferJ, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferK, 0)
        ArrayInitialize(BufferD, 0)
        ArrayInitialize(BufferJ, 0)
    for i in range(limit, 0 - 1, -1):
        Cn = close[i]
        bl = Lowest(period, i)
        bh = Highest(period, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        Ln = fmin(Cn, low[bl])
        Hn = fmax(Cn, high[bh])
        RSV = (_fdiv(100.0 * (Cn - Ln), Hn - Ln) if (Hn != Ln) else 50.0)
        BufferK[i] = (factor1 * BufferK[i + 1]) + (factor2 * RSV)
        BufferD[i] = (factor1 * BufferD[i + 1]) + (factor2 * BufferK[i])
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


class KDJ(_MQL5Indicator):
    name = 'KDJ'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 9,  # Period
        'InpFactor1': 0.666666,  # KFactor
        'InpFactor2': 0.333333,  # DFactor
        'InpThreshold': 50.0,  # Threshold
    }

