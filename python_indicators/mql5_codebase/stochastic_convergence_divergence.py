"""Stochastic_Convergence_Divergence — converted from MQL5: MQL5 Indicators/Stochastic_Convergence_Divergence/Stochastic_Convergence_Divergence.mq5

Two Stochastics with MA Smoothing and Convergence Divergence line
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 12, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 8}, 'colors': {1: [3329330], 2: [255], 3: [16748574], 4: [17919], 5: [8388736, 11823615, 11119017]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Stoch %K1', 2: 'Stoch %D1', 3: 'Stoch %K2', 4: 'Stoch %D2', 5: 'Divergence'}, 'levels': [], 'description': ['Two Stochastics with MA Smoothing and Convergence Divergence line'], 'name': 'Stochastic_Convergence_Divergence', 'source': 'MQL5 Indicators/Stochastic_Convergence_Divergence/Stochastic_Convergence_Divergence.mq5', 'folder': 'Stochastic_Convergence_Divergence', 'inputs': [{'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 1, 'label': 'Calculation mode', 'sinput': False}, {'mql': 'InpPeriodK1', 'py': 'InpPeriodK1', 'param': 'InpPeriodK1', 'type': 'uint', 'default': 5, 'label': 'First stochastic %K period', 'sinput': False}, {'mql': 'InpPeriodD1', 'py': 'InpPeriodD1', 'param': 'InpPeriodD1', 'type': 'uint', 'default': 3, 'label': 'First stochastic %D period', 'sinput': False}, {'mql': 'InpSlowing1', 'py': 'InpSlowing1', 'param': 'InpSlowing1', 'type': 'uint', 'default': 3, 'label': 'First stochastic slowing', 'sinput': False}, {'mql': 'InpMethodK1', 'py': 'InpMethodK1', 'param': 'InpMethodK1', 'type': 'int', 'default': 0, 'label': 'First stochastic %K-smoothing type', 'sinput': False}, {'mql': 'InpMethodD1', 'py': 'InpMethodD1', 'param': 'InpMethodD1', 'type': 'int', 'default': 0, 'label': 'First stochastic %D-smoothing type', 'sinput': False}, {'mql': 'InpPeriodK2', 'py': 'InpPeriodK2', 'param': 'InpPeriodK2', 'type': 'uint', 'default': 21, 'label': 'Second stochastic %K period', 'sinput': False}, {'mql': 'InpPeriodD2', 'py': 'InpPeriodD2', 'param': 'InpPeriodD2', 'type': 'uint', 'default': 14, 'label': 'Second stochastic %D period', 'sinput': False}, {'mql': 'InpSlowing2', 'py': 'InpSlowing2', 'param': 'InpSlowing2', 'type': 'uint', 'default': 2, 'label': 'Second stochastic slowing', 'sinput': False}, {'mql': 'InpMethodK2', 'py': 'InpMethodK2', 'param': 'InpMethodK2', 'type': 'int', 'default': 0, 'label': 'Second stochastic %K-smoothing type', 'sinput': False}, {'mql': 'InpMethodD2', 'py': 'InpMethodD2', 'param': 'InpMethodD2', 'type': 'int', 'default': 0, 'label': 'Second stochastic %D-smoothing type', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_IND_MODE
IND_MODE_IND = 0
IND_MODE_DIV = 1
_enum('ENUM_IND_MODE', {0: 'IND_MODE_IND', 1: 'IND_MODE_DIV'})

# enum ENUM_TYPE_SMOOTH_K
TYPE_SMOOTH_K_SMA = 0
TYPE_SMOOTH_K_EMA = 1
TYPE_SMOOTH_K_FAST = 2
_enum('ENUM_TYPE_SMOOTH_K', {0: 'TYPE_SMOOTH_K_SMA', 1: 'TYPE_SMOOTH_K_EMA', 2: 'TYPE_SMOOTH_K_FAST'})

# enum ENUM_TYPE_SMOOTH_D
TYPE_SMOOTH_D_SMA = 0
TYPE_SMOOTH_D_EMA = 1
_enum('ENUM_TYPE_SMOOTH_D', {0: 'TYPE_SMOOTH_D_SMA', 1: 'TYPE_SMOOTH_D_EMA'})

# ---- inputs and global variables
InpMode = _input('InpMode', IND_MODE_DIV)  # Calculation mode
InpPeriodK1 = _input('InpPeriodK1', 5)  # First stochastic %K period
InpPeriodD1 = _input('InpPeriodD1', 3)  # First stochastic %D period
InpSlowing1 = _input('InpSlowing1', 3)  # First stochastic slowing
InpMethodK1 = _input('InpMethodK1', TYPE_SMOOTH_K_SMA)  # First stochastic %K-smoothing type
InpMethodD1 = _input('InpMethodD1', TYPE_SMOOTH_D_SMA)  # First stochastic %D-smoothing type
InpPeriodK2 = _input('InpPeriodK2', 21)  # Second stochastic %K period
InpPeriodD2 = _input('InpPeriodD2', 14)  # Second stochastic %D period
InpSlowing2 = _input('InpSlowing2', 2)  # Second stochastic slowing
InpMethodK2 = _input('InpMethodK2', TYPE_SMOOTH_K_SMA)  # Second stochastic %K-smoothing type
InpMethodD2 = _input('InpMethodD2', TYPE_SMOOTH_D_SMA)  # Second stochastic %D-smoothing type
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferSK1 = Arr(0, 0.0)
BufferSD1 = Arr(0, 0.0)
BufferSK2 = Arr(0, 0.0)
BufferSD2 = Arr(0, 0.0)
BufferDivergence = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMin1 = Arr(0, 0.0)
BufferMax1 = Arr(0, 0.0)
BufferFastK1 = Arr(0, 0.0)
BufferMin2 = Arr(0, 0.0)
BufferMax2 = Arr(0, 0.0)
BufferFastK2 = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
periodK1 = 0
periodK2 = 0
periodD1 = 0
periodD2 = 0
slowing1 = 0
slowing2 = 0

def OnInit():
    global overbought, oversold, periodD1, periodD2, periodK1, periodK2, slowing1, slowing2
    periodK1 = (1 if (InpPeriodK1 < 1) else InpPeriodK1)
    periodD1 = (1 if (InpPeriodD1 < 1) else InpPeriodD1)
    slowing1 = (1 if (InpSlowing1 < 1) else InpSlowing1)
    periodK2 = (1 if (InpPeriodK2 < 1) else InpPeriodK2)
    periodD2 = (1 if (InpPeriodD2 < 1) else InpPeriodD2)
    slowing2 = (1 if (InpSlowing2 < 1) else InpSlowing2)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferSK1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSD1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSK2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSD2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferDivergence, INDICATOR_DATA)
    SetIndexBuffer(5, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, BufferMax1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferMax2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMin1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMin2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferFastK1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferFastK2, INDICATOR_CALCULATIONS)
    label = (('Stochastic(' + _str(periodK1) + ',' + _str(periodD1) + ',' + _str(slowing1) + ')' + ', Stochastic(' + _str(periodK2) + ',' + _str(periodD2) + ',' + _str(slowing2) + ')') if (InpMode == IND_MODE_IND) else ('Convergence/Divergence between Stoch(' + _str(periodK1) + ',' + _str(periodD1) + ',' + _str(slowing1) + ')' + ', Stoch(' + _str(periodK2) + ',' + _str(periodD2) + ',' + _str(slowing2) + ')'))
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    if InpMode == IND_MODE_IND:
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(1, PLOT_SHOW_DATA, True)
        PlotIndexSetInteger(3, PLOT_SHOW_DATA, True)
        PlotIndexSetInteger(4, PLOT_SHOW_DATA, False)
    else:
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_COLOR_LINE)
        PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
        PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
        PlotIndexSetInteger(4, PLOT_SHOW_DATA, True)
    ArraySetAsSeries(BufferSK1, True)
    ArraySetAsSeries(BufferSD1, True)
    ArraySetAsSeries(BufferSK2, True)
    ArraySetAsSeries(BufferSD2, True)
    ArraySetAsSeries(BufferDivergence, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMax1, True)
    ArraySetAsSeries(BufferMax2, True)
    ArraySetAsSeries(BufferMin1, True)
    ArraySetAsSeries(BufferMin2, True)
    ArraySetAsSeries(BufferFastK1, True)
    ArraySetAsSeries(BufferFastK2, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferSK1, EMPTY_VALUE)
        ArrayInitialize(BufferSD1, EMPTY_VALUE)
        ArrayInitialize(BufferSK2, EMPTY_VALUE)
        ArrayInitialize(BufferSD2, EMPTY_VALUE)
        ArrayInitialize(BufferDivergence, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferMax1, 0)
        ArrayInitialize(BufferMax2, 0)
        ArrayInitialize(BufferMin1, 0)
        ArrayInitialize(BufferMin2, 0)
        ArrayInitialize(BufferFastK1, 0)
        ArrayInitialize(BufferFastK2, 0)
    for i in range(limit, 0 - 1, -1):
        DataPreparing(rates_total, i, periodK1, close, BufferMin1, BufferMax1, BufferFastK1)
        DataPreparing(rates_total, i, periodK2, close, BufferMin2, BufferMax2, BufferFastK2)
        CalculateSK(rates_total, i, InpMethodK1, periodK1, slowing1, BufferMin1, BufferMax1, BufferFastK1, BufferSK1)
        CalculateSK(rates_total, i, InpMethodK2, periodK2, slowing2, BufferMin2, BufferMax2, BufferFastK2, BufferSK2)
        if InpMethodD1 == TYPE_SMOOTH_D_SMA:
            BufferSD1[i] = GetSMA(rates_total, BufferSK1, periodD1, i)
            BufferSD2[i] = GetSMA(rates_total, BufferSK2, periodD2, i)
        else:
            BufferSD1[i] = GetEMA(rates_total, BufferSK1[i], BufferSD1[i + 1], periodD1, i)
            BufferSD2[i] = GetEMA(rates_total, BufferSK2[i], BufferSD2[i + 1], periodD2, i)
        BufferDivergence[i] = BufferSK1[i] - BufferSK2[i] + 50.0
        BufferColors[i] = (0 if (BufferDivergence[i] > 50) else 1 if (BufferDivergence[i] < 50) else 2)
    return rates_total

def DataPreparing(rates_total, shift, period_k, buffer_src, buffer_min, buffer_max, buffer_fast_k):
    if shift > (rates_total - period_k - 1):
        return
    max_ = 0.0
    min_ = 0.0
    for j in range(shift + period_k - 1, shift - 1, -1):
        if j == (shift + period_k - 1):
            min_ = buffer_src[j]
            max_ = min_
        else:
            if buffer_src[j] > max_:
                max_ = buffer_src[j]
            if buffer_src[j] < min_:
                min_ = buffer_src[j]
    buffer_min[shift] = buffer_src[shift] - min_
    buffer_max[shift] = max_ - min_
    buffer_fast_k[shift] = ((_fdiv(buffer_min[shift], buffer_max[shift]) * 100.0) if (buffer_max[shift] > 0) else 50.0)

def CalculateSK(rates_total, shift, type_smK, period_k, slowing, buffer_min, buffer_max, buffer_fast, buffer_sk):
    sum_max = 0.0
    sum_min = 0.0
    if type_smK == TYPE_SMOOTH_K_FAST:
        if shift > (rates_total - period_k - 1):
            return
        for j in range(shift + period_k - 1, shift - 1, -1):
            sum_max += buffer_max[j]
        if sum_max != 0:
            for j in range(shift + period_k - 1, shift - 1, -1):
                sum_min += buffer_min[j]
            buffer_sk[shift] = _fdiv(sum_min, sum_max) * 100.0
        else:
            buffer_sk[shift] = 50.0
    else:
        if shift > (rates_total - slowing - 1):
            return
        if type_smK == TYPE_SMOOTH_K_SMA:
            buffer_sk[shift] = GetSMA(rates_total, buffer_fast, slowing, shift)
        else:
            buffer_sk[shift] = GetEMA(rates_total, buffer_fast[shift], buffer_sk[shift + 1], slowing, shift)

def GetSMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return array_src[shift]
    sum_ = 0.0
    for i in range(0, period):
        sum_ += array_src[shift + i]
    return _fdiv(sum_, period)

def GetEMA(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + (_fdiv(2.0, 1 + period) * (price - prev))))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticConvergenceDivergence(_MQL5Indicator):
    name = 'Stochastic_Convergence_Divergence'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMode': _Choice({0: 'Two stochastics', 1: 'Stoch1/Stoch2 divergence'}, default=1),  # Calculation mode
        'InpPeriodK1': 5,  # First stochastic %K period
        'InpPeriodD1': 3,  # First stochastic %D period
        'InpSlowing1': 3,  # First stochastic slowing
        'InpMethodK1': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Fast'}, default=0),  # First stochastic %K-smoothing type
        'InpMethodD1': _Choice({0: 'Simple', 1: 'Exponential'}, default=0),  # First stochastic %D-smoothing type
        'InpPeriodK2': 21,  # Second stochastic %K period
        'InpPeriodD2': 14,  # Second stochastic %D period
        'InpSlowing2': 2,  # Second stochastic slowing
        'InpMethodK2': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Fast'}, default=0),  # Second stochastic %K-smoothing type
        'InpMethodD2': _Choice({0: 'Simple', 1: 'Exponential'}, default=0),  # Second stochastic %D-smoothing type
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

