"""draw_color_histogram — converted from MQL5: MQL5 Indicators/DRAW_COLOR_HISTOGRAM/draw_color_histogram.mq5

This indicator is a demo of DRAW_COLOR_HISTOGRAM drawing style
It plots a sin(x) function as a color histogram in a separate window
The color and width are changed randomly after N ticks
The bars parameter sets the period (in bars) of the sin(x) function
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 32768, 16711680, 65535, 16711935, 16776960, 7451452, 55295]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Color_Histogram'}, 'levels': [], 'description': ['This indicator is a demo of DRAW_COLOR_HISTOGRAM drawing style', 'It plots a sin(x) function as a color histogram in a separate window', 'The color and width are changed randomly after N ticks', 'The bars parameter sets the period (in bars) of the sin(x) function'], 'name': 'draw_color_histogram', 'source': 'MQL5 Indicators/DRAW_COLOR_HISTOGRAM/draw_color_histogram.mq5', 'folder': 'DRAW_COLOR_HISTOGRAM', 'inputs': [{'mql': 'bars', 'py': 'bars', 'param': 'bars', 'type': 'int', 'default': 30, 'label': 'Sin(x) period in bars', 'sinput': False}, {'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Ticks to change properties', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
bars = _input('bars', 30)  # Sin(x) period in bars
N = _input('N', 5)  # Ticks to change properties
Color_HistogramBuffer = Arr(0, 0.0)
Color_HistogramColors = Arr(0, 0.0)
multiplier = 0.0
color_sections = 0
colors = Arr.of([clrRed, clrBlue, clrGreen, clrChocolate, clrMagenta, clrDodgerBlue, clrGoldenrod, clrIndigo, clrLightBlue, clrAliceBlue, clrMoccasin, clrWhiteSmoke, clrCyan, clrMediumPurple], fill=0)
styles = Arr.of([STYLE_SOLID, STYLE_DASH, STYLE_DOT, STYLE_DASHDOT, STYLE_DASHDOTDOT], fill=0)

def OnInit():
    global color_sections, multiplier
    SetIndexBuffer(0, Color_HistogramBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Color_HistogramColors, INDICATOR_COLOR_INDEX)
    color_sections = 8
    if bars > 1:
        multiplier = (2.0 * M_PI) / bars
    else:
        PrintFormat('The bars should be greater than 1. bars=%d', bars)
        return INIT_PARAMETERS_INCORRECT
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks
    _s_OnCalculate_ticks += 1
    if _s_OnCalculate_ticks >= N:
        ChangeLineAppearance()
        ChangeColors(colors, color_sections)
        _s_OnCalculate_ticks = 0
    start = 0
    if prev_calculated > 0:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        Color_HistogramBuffer[i] = sin(i * multiplier)
        color_index = _imod(i, bars * color_sections)
        color_index = _idiv(color_index, bars)
        Color_HistogramColors[i] = color_index
    return rates_total

def ChangeColors(cols, plot_colors):
    size = ArraySize(cols)
    comm = ChartGetString(0, CHART_COMMENT) + '\r\n\r\n'
    for plot_color_ind in range(0, plot_colors):
        number = MathRand()
        i = _imod(number, size)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, plot_color_ind, cols[i])
        comm = comm + StringFormat('HistogramColorIndex[%d]=%s \r\n', plot_color_ind, ColorToString(cols[i], True))
        ChartSetString(0, CHART_COMMENT, comm)

def ChangeLineAppearance():
    comm = ''
    number = MathRand()
    width = _imod(number, 5)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, width)
    comm = comm + ' Width=' + IntegerToString(width)
    number = MathRand()
    size = ArraySize(styles)
    style_index = _imod(number, size)
    PlotIndexSetInteger(0, PLOT_LINE_STYLE, styles[style_index])
    comm = EnumToString(styles[style_index], 'ENUM_LINE_STYLE') + ', ' + comm
    Comment(comm)

# ---- static local variables
_s_OnCalculate_ticks = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DrawColorHistogram(_MQL5Indicator):
    name = 'draw_color_histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'bars': 30,  # Sin(x) period in bars
        'N': 5,  # Ticks to change properties
    }

