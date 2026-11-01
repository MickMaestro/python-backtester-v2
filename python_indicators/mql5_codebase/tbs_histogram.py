"""TBS_Histogram — converted from MQL5: MQL5 Indicators/TBS_Histogram/TBS_Histogram.mq5

Tick Based Stochastic with histogram
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [32768], 2: [255], 3: [32768, 255, 11119017]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'TBSH %K', 2: 'TBSH %D', 3: 'Histogram'}, 'levels': [], 'description': ['Tick Based Stochastic with histogram'], 'name': 'TBS_Histogram', 'source': 'MQL5 Indicators/TBS_Histogram/TBS_Histogram.mq5', 'folder': 'TBS_Histogram', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 5, 'label': '%K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': '%D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpMethodK', 'py': 'InpMethodK', 'param': 'InpMethodK', 'type': 'int', 'default': 0, 'label': '%K method', 'sinput': False}, {'mql': 'InpMethodD', 'py': 'InpMethodD', 'param': 'InpMethodD', 'type': 'int', 'default': 0, 'label': '%D method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 30.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -30.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpShowK', 'py': 'InpShowK', 'param': 'InpShowK', 'type': 'int', 'default': 1, 'label': 'Show %K line', 'sinput': False}, {'mql': 'InpShowD', 'py': 'InpShowD', 'param': 'InpShowD', 'type': 'int', 'default': 1, 'label': 'Show %D line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

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
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
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
BufferMA = Arr(0, 0.0)
BufferRawK = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_k = 0
period_d = 0
slowing = 0
period_max = 0
weight_sum_k = 0
weight_sum_d = 0
handle_ma = 0

def OnInit():
    global handle_ma, overbought, oversold, period_d, period_k, period_max, slowing
    period_k = (2 if (InpPeriodK < 2) else InpPeriodK)
    period_d = (2 if (InpPeriodD < 2) else InpPeriodD)
    slowing = (2 if (InpSlowing < 2) else InpSlowing)
    period_max = fmax(period_k, slowing)
    overbought = (0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (-0.1 if (InpOversold > -0.1) else InpOversold)
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferMins, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMaxes, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferFastK, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferRawK, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TBSH(' + _str(period_k) + ',' + _str(period_d) + ',' + _str(slowing) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, (DRAW_LINE if InpShowK else DRAW_NONE))
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, (DRAW_LINE if InpShowD else DRAW_NONE))
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMins, True)
    ArraySetAsSeries(BufferMaxes, True)
    ArraySetAsSeries(BufferFastK, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferRawK, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_k - 2
        ArrayInitialize(BufferK, 0)
        ArrayInitialize(BufferD, 0)
        ArrayInitialize(BufferMins, 0)
        ArrayInitialize(BufferMaxes, 0)
        ArrayInitialize(BufferFastK, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        bl = ArrayMinimum(BufferMA, i, period_k)
        bh = ArrayMaximum(BufferMA, i, period_k)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferMA[bl]
        max_ = BufferMA[bh]
        BufferMins[i] = BufferMA[i] - min_
        BufferMaxes[i] = max_ - min_
        BufferFastK[i] = (_fdiv(100.0 * BufferMins[i], BufferMaxes[i]) if (BufferMaxes[i] > 0) else 50.0)
        if InpMethodK == METHOD_MT:
            max_ = GetSMA(rates_total, i, slowing, BufferMaxes)
            min_ = GetSMA(rates_total, i, slowing, BufferMins)
            BufferK[i] = ((_fdiv(100.0 * min_, max_) - 50.0) if (max_ != 0) else 0)
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


class TBSHistogram(_MQL5Indicator):
    name = 'TBS_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK': 5,  # %K period
        'InpPeriodD': 3,  # %D period
        'InpSlowing': 3,  # Slowing
        'InpMethodK': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothing', 3: 'Linear weighted', 4: 'MT algorithm'}, default=0),  # %K method
        'InpMethodD': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # %D method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 30.0,  # Overbought
        'InpOversold': -30.0,  # Oversold
        'InpShowK': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show %K line
        'InpShowD': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show %D line
    }

