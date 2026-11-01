"""trendvalue — converted from MQL5: MQL5 Indicators/TrendValue_HTF/trendvalue.mq5

Copyright: Copyright © 2010, Ivan Kornilov; Link: excelf@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Ivan Kornilov', 'link': 'excelf@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [16711680], 2: [8721863], 3: [16760576], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 4, 2: 4}, 'labels': {1: 'Upper TrendValue', 2: 'Lower TrendValue', 3: 'Buy TrendValue', 4: 'Sell TrendValue'}, 'levels': [], 'description': [], 'name': 'trendvalue', 'source': 'MQL5 Indicators/TrendValue_HTF/trendvalue.mq5', 'folder': 'TrendValue_HTF', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 13, 'label': 'Moving averages period', 'sinput': False}, {'mql': 'shiftPercent', 'py': 'shiftPercent', 'param': 'shiftPercent', 'type': 'double', 'default': 0.0, 'label': 'Horizontal shift of the indicator in percents', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 15, 'label': 'ATR indicator period', 'sinput': False}, {'mql': 'ATRSensitivity', 'py': 'ATRSensitivity', 'param': 'ATRSensitivity', 'type': 'double', 'default': 1.5, 'label': 'ATR shift sensitivity', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 13)  # Moving averages period
shiftPercent = _input('shiftPercent', 0.0)  # Horizontal shift of the indicator in percents
ATRPeriod = _input('ATRPeriod', 15)  # ATR indicator period
ATRSensitivity = _input('ATRSensitivity', 1.5)  # ATR shift sensitivity
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ExtMapBufferUp1 = Arr(0, 0.0)
ExtMapBufferDown1 = Arr(0, 0.0)
ATR_Handle = 0
HMA_Handle = 0
LMA_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, HMA_Handle, LMA_Handle, min_rates_total
    ATR_Handle = iATR(None, 0, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return 1
    HMA_Handle = iMA(None, 0, period, 0, MODE_LWMA, PRICE_HIGH)
    if HMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the HMA indicator')
        return 1
    LMA_Handle = iMA(None, 0, period, 0, MODE_LWMA, PRICE_LOW)
    if LMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the LMA indicator')
        return 1
    min_rates_total = ATRPeriod + period
    SetIndexBuffer(0, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, ExtMapBufferUp1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp1, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_ARROW, 117)
    SetIndexBuffer(3, ExtMapBufferDown1, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown1, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 117)
    shortname = Box("")
    StringConcatenate(shortname, 'TrendValue(', period, ', ', shiftPercent, ', ', ATRPeriod, ', ', ATRSensitivity, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_highMoving1, _s_OnCalculate_lowMoving1, _s_OnCalculate_trend_
    if ((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(HMA_Handle) < rates_total) or BarsCalculated(LMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    ATR = Arr(0, 0.0)
    HMA = Arr(0, 0.0)
    LMA = Arr(0, 0.0)
    atr = 0.0
    highMoving0 = 0.0
    lowMoving0 = 0.0
    limit = 0
    to_copy = 0
    bar = 0
    trend = 0
    maxbar = 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(HMA, True)
    ArraySetAsSeries(LMA, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend_ = 0
    else:
        limit = rates_total - prev_calculated
    maxbar = rates_total - min_rates_total - 1
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(HMA_Handle, 0, 0, to_copy, HMA) <= 0:
        return 0
    if CopyBuffer(LMA_Handle, 0, 0, to_copy, LMA) <= 0:
        return 0
    trend = _s_OnCalculate_trend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_trend_ = trend
        atr = ATR[bar] * ATRSensitivity
        highMoving0 = (HMA[bar] * (1 + (shiftPercent / 100))) + atr
        lowMoving0 = (LMA[bar] * (1 - (shiftPercent / 100))) - atr
        if bar > maxbar:
            _s_OnCalculate_lowMoving1 = lowMoving0
            _s_OnCalculate_highMoving1 = highMoving0
            continue
        if close[bar] > _s_OnCalculate_highMoving1:
            trend = 1
        if close[bar] < _s_OnCalculate_lowMoving1:
            trend = -1
        if trend > 0.0:
            lowMoving0 = MathMax(lowMoving0, _s_OnCalculate_lowMoving1)
            ExtMapBufferUp[bar] = lowMoving0
            ExtMapBufferDown[bar] = EMPTY_VALUE
        if trend < 0.0:
            highMoving0 = MathMin(highMoving0, _s_OnCalculate_highMoving1)
            ExtMapBufferDown[bar] = highMoving0
            ExtMapBufferUp[bar] = EMPTY_VALUE
        if ExtMapBufferUp[bar + 1] == EMPTY_VALUE and ExtMapBufferUp[bar] != EMPTY_VALUE:
            ExtMapBufferUp1[bar] = ExtMapBufferUp[bar]
        if ExtMapBufferDown[bar + 1] == EMPTY_VALUE and ExtMapBufferDown[bar] != EMPTY_VALUE:
            ExtMapBufferDown1[bar] = ExtMapBufferDown[bar]
        if bar > 0:
            _s_OnCalculate_lowMoving1 = lowMoving0
            _s_OnCalculate_highMoving1 = highMoving0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_highMoving1 = 0.0
_s_OnCalculate_lowMoving1 = 0.0
_s_OnCalculate_trend_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendvalue(_MQL5Indicator):
    name = 'trendvalue'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 13,  # Moving averages period
        'shiftPercent': 0.0,  # Horizontal shift of the indicator in percents
        'ATRPeriod': 15,  # ATR indicator period
        'ATRSensitivity': 1.5,  # ATR shift sensitivity
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

