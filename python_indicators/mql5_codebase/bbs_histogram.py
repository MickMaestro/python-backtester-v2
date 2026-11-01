"""BBS_Histogram — converted from MQL5: MQL5 Indicators/BBS_Histogram/BBS_Histogram.mq5

Bar Based Stochastic with histogram
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [32768], 2: [255], 3: [32768, 255, 11119017]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'BBSH %K', 2: 'BBSH %D', 3: 'Histogram'}, 'levels': [], 'description': ['Bar Based Stochastic with histogram'], 'name': 'BBS_Histogram', 'source': 'MQL5 Indicators/BBS_Histogram/BBS_Histogram.mq5', 'folder': 'BBS_Histogram', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 5, 'label': '%K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': '%D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpMethodK', 'py': 'InpMethodK', 'param': 'InpMethodK', 'type': 'int', 'default': 0, 'label': '%K method', 'sinput': False}, {'mql': 'InpMethodD', 'py': 'InpMethodD', 'param': 'InpMethodD', 'type': 'int', 'default': 0, 'label': '%D method', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 30.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -30.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpShowK', 'py': 'InpShowK', 'param': 'InpShowK', 'type': 'int', 'default': 1, 'label': 'Show %K line', 'sinput': False}, {'mql': 'InpShowD', 'py': 'InpShowD', 'param': 'InpShowD', 'type': 'int', 'default': 1, 'label': 'Show %D line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# enum ENUM_METHOD
METHOD_SMA = 0
METHOD_EMA = 1
METHOD_SMMA = 2
METHOD_LWMA = 3
METHOD_MT = 4
_enum('ENUM_METHOD', {0: 'METHOD_SMA', 1: 'METHOD_EMA', 2: 'METHOD_SMMA', 3: 'METHOD_LWMA', 4: 'METHOD_MT'})

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 5)  # %K period
InpPeriodD = _input('InpPeriodD', 3)  # %D period
InpSlowing = _input('InpSlowing', 3)  # Slowing
InpMethodK = _input('InpMethodK', METHOD_SMA)  # %K method
InpMethodD = _input('InpMethodD', MODE_SMA)  # %D method
InpOverbought = _input('InpOverbought', 30.0)  # Overbought
InpOversold = _input('InpOversold', -30.0)  # Oversold
InpShowK = _input('InpShowK', INPUT_YES)  # Show %K line
InpShowD = _input('InpShowD', INPUT_YES)  # Show %D line
BufferK = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
BufferHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMins = Arr(0, 0.0)
BufferMaxes = Arr(0, 0.0)
BufferFastK = Arr(0, 0.0)
BufferAvgFastK = Arr(0, 0.0)
BufferRawK = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_k = 0
period_d = 0
slowing = 0
weight_sum_k = 0
weight_sum_d = 0

def OnInit():
    global overbought, oversold, period_d, period_k, slowing
    period_k = (2 if (InpPeriodK < 2) else InpPeriodK)
    period_d = (2 if (InpPeriodD < 2) else InpPeriodD)
    slowing = (2 if (InpSlowing < 2) else InpSlowing)
    overbought = (0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (-0.1 if (InpOversold > -0.1) else InpOversold)
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferMins, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMaxes, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferFastK, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferAvgFastK, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferRawK, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BBSH(' + _str(period_k) + ',' + _str(period_d) + ',' + _str(slowing) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, (DRAW_LINE if InpShowK else DRAW_NONE))
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, (DRAW_LINE if InpShowD else DRAW_NONE))
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMins, True)
    ArraySetAsSeries(BufferMaxes, True)
    ArraySetAsSeries(BufferFastK, True)
    ArraySetAsSeries(BufferAvgFastK, True)
    ArraySetAsSeries(BufferRawK, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_k, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_k - 2
        ArrayInitialize(BufferK, 0)
        ArrayInitialize(BufferD, 0)
        ArrayInitialize(BufferHist, 0)
        ArrayInitialize(BufferMins, 0)
        ArrayInitialize(BufferMaxes, 0)
        ArrayInitialize(BufferFastK, 0)
        ArrayInitialize(BufferAvgFastK, 0)
        ArrayInitialize(BufferRawK, 0)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period_k, i)
        bh = Highest(period_k, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        minLow = low[bl]
        maxHigh = high[bh]
        BufferMins[i] = close[i] - minLow
        BufferMaxes[i] = maxHigh - minLow
        BufferFastK[i] = (_fdiv(100.0 * BufferMins[i], BufferMaxes[i]) if (BufferMaxes[i] > 0) else 50.0)
        if InpMethodK == METHOD_MT:
            avgMax = GetSMA(rates_total, i, slowing, BufferMaxes)
            avgMin = GetSMA(rates_total, i, slowing, BufferMins)
            BufferK[i] = ((_fdiv(100.0 * avgMin, avgMax) - 50.0) if (avgMax != 0) else 0)
    if InpMethodK < METHOD_MT:
        _sw1 = InpMethodK
        if _sw1 == METHOD_EMA:
            if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, slowing, BufferFastK, BufferRawK) == 0:
                return 0
        elif _sw1 == METHOD_SMMA:
            if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, slowing, BufferFastK, BufferRawK) == 0:
                return 0
        elif _sw1 == METHOD_LWMA:
            if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, slowing, BufferFastK, BufferRawK, _GlobRef(globals(), 'weight_sum_k')) == 0:
                return 0
        else:
            if SimpleMAOnBuffer(rates_total, prev_calculated, 0, slowing, BufferFastK, BufferRawK) == 0:
                return 0
        for i in range(limit, 0 - 1, -1):
            BufferK[i] = BufferRawK[i] - 50.0
    _sw2 = InpMethodD
    if _sw2 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, slowing, period_d, BufferK, BufferD) == 0:
            return 0
    elif _sw2 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, slowing, period_d, BufferK, BufferD) == 0:
            return 0
    elif _sw2 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, slowing, period_d, BufferK, BufferD, _GlobRef(globals(), 'weight_sum_d')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, slowing, period_d, BufferK, BufferD) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferHist[i] = BufferK[i] - BufferD[i]
        BufferColors[i] = (0 if (BufferHist[i] > BufferHist[i + 1]) else 1 if (BufferHist[i] < BufferHist[i + 1]) else 2)
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

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBSHistogram(_MQL5Indicator):
    name = 'BBS_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK': 5,  # %K period
        'InpPeriodD': 3,  # %D period
        'InpSlowing': 3,  # Slowing
        'InpMethodK': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothing', 3: 'Linear weighted', 4: 'MT algorithm'}, default=0),  # %K method
        'InpMethodD': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # %D method
        'InpOverbought': 30.0,  # Overbought
        'InpOversold': -30.0,  # Oversold
        'InpShowK': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show %K line
        'InpShowD': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show %D line
    }

