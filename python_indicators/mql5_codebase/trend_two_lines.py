"""Trend Two Lines — converted from MQL5: MQL5 Indicators/Trend Two Lines/Trend Two Lines.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 3.0, 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 12, 2: 12}, 'colors': {1: [255, 16711680], 2: [255, 16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'High', 2: 'Low'}, 'levels': [], 'description': [], 'name': 'Trend Two Lines', 'source': 'MQL5 Indicators/Trend Two Lines/Trend Two Lines.mq5', 'folder': 'Trend Two Lines', 'inputs': [{'mql': 'Input1', 'py': 'Input1', 'param': 'Input1', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Input1 = _input('Input1', 9)
HighBuffer = Arr(0, 0.0)
HighColors = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
LowColors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, LowColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_ARROW, 174)
    PlotIndexSetInteger(1, PLOT_ARROW, 174)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        HighBuffer[0] = 0.0
        HighColors[0] = 0.0
        LowBuffer[0] = 0.0
        LowColors[0] = 0.0
        limit = 1
    for i in range(limit, rates_total):
        HighBuffer[i] = 0.0
        HighColors[i] = 0.0
        LowBuffer[i] = 0.0
        LowColors[i] = 0.0
        if high[i] > high[i - 1]:
            HighBuffer[i] = 1.0
            HighColors[i] = 1.0
        if high[i] < high[i - 1]:
            HighBuffer[i] = 1.0
            HighColors[i] = 0.0
        if low[i] > low[i - 1]:
            LowBuffer[i] = 2.0
            LowColors[i] = 1.0
        if low[i] < low[i - 1]:
            LowBuffer[i] = 2.0
            LowColors[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendTwoLines(_MQL5Indicator):
    name = 'Trend Two Lines'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Input1': 9,
    }
    y_range = (0.0, 3.0)

