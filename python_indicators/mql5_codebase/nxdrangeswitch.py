"""nxdrangeswitch — converted from MQL5: MQL5 Indicators/NxDRangeSwitch/nxdrangeswitch.mq5

Copyright: Copyright © 2009, Vic2008; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Vic2008', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [11186720], 2: [8721863], 3: [5737262], 4: [9639167]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 4, 2: 4}, 'labels': {1: 'Upper NxDRangeSwitch', 2: 'Lower NxDRangeSwitch', 3: 'Buy NxDRangeSwitch', 4: 'Sell NxDRangeSwitch'}, 'levels': [], 'description': [], 'name': 'nxdrangeswitch', 'source': 'MQL5 Indicators/NxDRangeSwitch/nxdrangeswitch.mq5', 'folder': 'NxDRangeSwitch', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 4, 'label': 'calculation period (not less than two)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 4)  # calculation period (not less than two)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ExtMapBufferUp1 = Arr(0, 0.0)
ExtMapBufferDown1 = Arr(0, 0.0)
ExtCalcBuffer = Arr(0, 0.0)
min_rates_total = 0
period0 = 0
period1 = 0

def OnInit():
    global min_rates_total, period0, period1
    period0 = _int(MathMax(2, period))
    min_rates_total = period0 + 1
    period1 = period0 - 1
    SetIndexBuffer(0, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, ExtMapBufferUp1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp1, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_ARROW, 167)
    SetIndexBuffer(3, ExtMapBufferDown1, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown1, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(3, PLOT_ARROW, 167)
    SetIndexBuffer(4, ExtCalcBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtCalcBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'NxDRangeSwitch(', period, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    HHp1 = 0.0
    HHp0 = 0.0
    LLp1 = 0.0
    LLp0 = 0.0
    Val = 0.0
    Val1 = 0.0
    limit = 0
    bar = 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HHp0 = high[ArrayMaximum(high, bar + 1, period0)]
        LLp0 = low[ArrayMinimum(low, bar + 1, period0)]
        HHp1 = high[ArrayMaximum(high, bar + 1, period1)]
        LLp1 = low[ArrayMinimum(low, bar + 1, period1)]
        ExtCalcBuffer[bar] = ExtCalcBuffer[bar + 1]
        ExtMapBufferDown1[bar] = 0.0
        ExtMapBufferUp1[bar] = 0.0
        if close[bar] > HHp0:
            ExtCalcBuffer[bar] = LLp1
        if close[bar] < LLp0:
            ExtCalcBuffer[bar] = HHp1
        Val = ExtCalcBuffer[bar]
        if close[bar] > Val:
            Val1 = ExtMapBufferUp[bar + 1]
            if (Val1 and Val1 <= Val) or (not Val1):
                ExtMapBufferUp[bar] = Val
            if Val1 and Val1 > Val:
                ExtMapBufferUp[bar] = Val1
            ExtMapBufferDown[bar] = 0.0
        if close[bar] < Val:
            Val1 = ExtMapBufferDown[bar + 1]
            if (Val1 and Val1 >= Val) or (not Val1):
                ExtMapBufferDown[bar] = Val
            if Val1 and Val1 < Val:
                ExtMapBufferDown[bar] = Val1
            ExtMapBufferUp[bar] = 0.0
        if (not ExtMapBufferUp[bar + 1]) and ExtMapBufferUp[bar]:
            ExtMapBufferUp1[bar] = Val
        if (not ExtMapBufferDown[bar + 1]) and ExtMapBufferDown[bar]:
            ExtMapBufferDown1[bar] = Val
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Nxdrangeswitch(_MQL5Indicator):
    name = 'nxdrangeswitch'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 4,  # calculation period (not less than two)
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

