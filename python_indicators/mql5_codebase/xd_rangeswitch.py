"""xd-rangeswitch — converted from MQL5: MQL5 Indicators/BackgroundСandle_XD-RangeSwitch_HTF/xd-rangeswitch.mq5

Copyright: Copyright © 2009, Vic2008; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Vic2008', 'link': '', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [2763429], 2: [8421376], 3: [1993170], 4: [10526303]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper XD-RangeSwitch', 2: 'Lower XD-RangeSwitch', 3: 'Sell XD-RangeSwitch', 4: 'Buy XD-RangeSwitch'}, 'levels': [], 'description': [], 'name': 'xd-rangeswitch', 'source': 'MQL5 Indicators/BackgroundСandle_XD-RangeSwitch_HTF/xd-rangeswitch.mq5', 'folder': 'BackgroundСandle_XD-RangeSwitch_HTF', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 4, 'label': 'number of peaks', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 4)  # number of peaks
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ExtMapBufferUp1 = Arr(0, 0.0)
ExtMapBufferDown1 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = N
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
    PlotIndexSetInteger(2, PLOT_ARROW, 110)
    SetIndexBuffer(3, ExtMapBufferDown1, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown1, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 110)
    shortname = Box("")
    StringConcatenate(shortname, 'XD-RangeSwitch(', N, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtMapBufferUp[bar] = EMPTY_VALUE
        ExtMapBufferDown[bar] = EMPTY_VALUE
        ExtMapBufferUp1[bar] = EMPTY_VALUE
        ExtMapBufferDown1[bar] = EMPTY_VALUE
        if close[bar] > high[ArrayMaximum(high, bar + 1, N)]:
            ExtMapBufferDown[bar] = low[ArrayMinimum(low, bar, N)]
        else:
            if close[bar] < low[ArrayMinimum(low, bar + 1, N)]:
                ExtMapBufferUp[bar] = high[ArrayMaximum(high, bar, N)]
            else:
                ExtMapBufferUp[bar] = ExtMapBufferUp[bar + 1]
                ExtMapBufferDown[bar] = ExtMapBufferDown[bar + 1]
        if ExtMapBufferUp[bar + 1] == EMPTY_VALUE and ExtMapBufferUp[bar] != EMPTY_VALUE:
            ExtMapBufferUp1[bar] = ExtMapBufferUp[bar]
        if ExtMapBufferDown[bar + 1] == EMPTY_VALUE and ExtMapBufferDown[bar] != EMPTY_VALUE:
            ExtMapBufferDown1[bar] = ExtMapBufferDown[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XdRangeswitch(_MQL5Indicator):
    name = 'xd-rangeswitch'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 4,  # number of peaks
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

