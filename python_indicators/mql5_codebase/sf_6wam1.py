"""sf-6wam1 — converted from MQL5: MQL5 Indicators/SF-6(AM)/sf-6wam1.mq5

Copyright: Copyright © 2010, Andrey Matvievskiy; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Andrey Matvievskiy', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2, 'indicator_maximum': 1.0, 'indicator_minimum': -1.0}, 'types': {1: 10, 2: 10}, 'colors': {1: [16711935, 65280], 2: [255, 16711680]}, 'widths': {1: 5, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Up SF-6(AM)', 2: 'Down SF-6(AM)'}, 'levels': [0.0], 'description': [], 'name': 'sf-6wam1', 'source': 'MQL5 Indicators/SF-6(AM)/sf-6wam1.mq5', 'folder': 'SF-6(AM)', 'inputs': [{'mql': 'A1', 'py': 'A1', 'param': 'A1', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'A2', 'py': 'A2', 'param': 'A2', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'A3', 'py': 'A3', 'param': 'A3', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
A1 = _input('A1', 3.0)
A2 = _input('A2', 2.0)
A3 = _input('A3', 1.0)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtMapBuffer1 = Arr(0, 0.0)
ColorExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ColorExtMapBuffer2 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 3
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ColorExtMapBuffer1, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtMapBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, ColorExtMapBuffer2, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'SF-6(AM)( A1 = ', A1, ', A2 = ', A2, ', A3 = ', A3, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    A = 0.0
    B = 0.0
    close1 = 0.0
    open1 = 0.0
    median1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        close1 = (Close[bar] * A1) + (Close[bar - 1] * A2) + (Close[bar - 2] * A3)
        open1 = (Open[bar] * A1) + (Open[bar - 1] * A2) + (Open[bar - 2] * A3)
        median1 = (((High[bar] + Low[bar]) / 2) * A1) + (((High[bar - 1] + Low[bar - 1]) / 2) * A2) + (((High[bar - 2] + Low[bar - 2]) / 2) * A3)
        ExtMapBuffer1[bar] = 0.0
        ExtMapBuffer2[bar] = 0.0
        A = median1 - open1 + (close1 - median1)
        B = median1 - close1
        if A > 0:
            ExtMapBuffer2[bar] = 1.0
            ColorExtMapBuffer2[bar] = 1.0
        else:
            ExtMapBuffer2[bar] = -1.0
            ColorExtMapBuffer2[bar] = 0.0
        if B < 0:
            ExtMapBuffer1[bar] = 1.0
            ColorExtMapBuffer1[bar] = 1.0
        else:
            ExtMapBuffer1[bar] = -1.0
            ColorExtMapBuffer1[bar] = 0.0
        if ExtMapBuffer1[bar] == ExtMapBuffer2[bar]:
            ExtMapBuffer2[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Sf6wam1(_MQL5Indicator):
    name = 'sf-6wam1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'A1': 3.0,
        'A2': 2.0,
        'A3': 1.0,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }
    y_range = (-1.0, 1.0)

