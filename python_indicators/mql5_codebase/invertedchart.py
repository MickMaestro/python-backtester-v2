"""invertedchart — converted from MQL5: MQL5 Indicators/Inverted Chart View/invertedchart.mq5

Copyright: J.S. 2013; Link: http://www.eselstreckdich.de; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'J.S. 2013', 'link': 'http://www.eselstreckdich.de', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: ''}, 'levels': [], 'description': [], 'name': 'invertedchart', 'source': 'MQL5 Indicators/Inverted Chart View/invertedchart.mq5', 'folder': 'Inverted Chart View', 'inputs': [{'mql': 'raise', 'py': 'raise_', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'fall', 'py': 'fall', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'doji', 'py': 'doji', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
DarkGray = 0xA9A9A9  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
buffer_open = Arr(0, 0.0)  # Buffers for data
buffer_high = Arr(0, 0.0)  # Buffers for data
buffer_low = Arr(0, 0.0)  # Buffers for data
buffer_close = Arr(0, 0.0)  # Buffers for data
buffer_color_line = Arr(0, 0.0)  # Buffer for color indexes

def OnInit():
    SetIndexBuffer(3, buffer_open, INDICATOR_DATA)
    SetIndexBuffer(1, buffer_high, INDICATOR_DATA)
    SetIndexBuffer(2, buffer_low, INDICATOR_DATA)
    SetIndexBuffer(0, buffer_close, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(4, buffer_color_line, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, raise_)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, fall)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, doji)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(prev_calculated, rates_total - 1 + 1):
        buffer_open[i] = -open[i]
        buffer_high[i] = -high[i]
        buffer_low[i] = -low[i]
        buffer_close[i] = -close[i]
        buffer_color_line[i] = 2.0
        if buffer_close[i] > buffer_open[i]:
            buffer_color_line[i] = 0.0
        if buffer_close[i] < buffer_open[i]:
            buffer_color_line[i] = 1.0
    return rates_total - 1

# ---- global variables initialised from expressions
raise_ = _input('raise_', _uint(Blue))
fall = _input('fall', _uint(Red))
doji = _input('doji', _uint(DarkGray))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Invertedchart(_MQL5Indicator):
    name = 'invertedchart'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

