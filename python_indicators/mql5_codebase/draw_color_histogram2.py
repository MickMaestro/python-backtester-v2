"""draw_color_histogram2 — converted from MQL5: MQL5 Indicators/DRAW_COLOR_HISTOGRAM2/draw_color_histogram2.mq5

This indicator is a demo of DRAW_COLOR_HISTOGRAM2 drawing style
For each bar it plots a section between the Open and Close prices
The colors, width and line style are changed randomly after N ticks
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [255, 16711680, 32768, 65535, 16711935]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ColorHistogram_2'}, 'levels': [], 'description': ['This indicator is a demo of DRAW_COLOR_HISTOGRAM2 drawing style', 'For each bar it plots a section between the Open and Close prices', 'The colors, width and line style are changed randomly after N ticks'], 'name': 'draw_color_histogram2', 'source': 'MQL5 Indicators/DRAW_COLOR_HISTOGRAM2/draw_color_histogram2.mq5', 'folder': 'DRAW_COLOR_HISTOGRAM2', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Number of ticks to change histogram properties', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 5)  # Number of ticks to change histogram properties
color_sections = 0
ColorHistogram_2Buffer1 = Arr(0, 0.0)
ColorHistogram_2Buffer2 = Arr(0, 0.0)
ColorHistogram_2Colors = Arr(0, 0.0)
colors = Arr.of([clrRed, clrBlue, clrGreen, clrChocolate, clrMagenta, clrDodgerBlue, clrGoldenrod, clrIndigo, clrLightBlue, clrAliceBlue, clrMoccasin, clrWhiteSmoke, clrCyan, clrMediumPurple], fill=0)
styles = Arr.of([STYLE_SOLID, STYLE_DASH, STYLE_DOT, STYLE_DASHDOT, STYLE_DASHDOTDOT], fill=0)

def OnInit():
    global color_sections
    SetIndexBuffer(0, ColorHistogram_2Buffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ColorHistogram_2Buffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ColorHistogram_2Colors, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    color_sections = 8
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks
    _s_OnCalculate_ticks += 1
    if _s_OnCalculate_ticks >= N:
        ChangeLineAppearance()
        ChangeColors(colors, color_sections)
        _s_OnCalculate_ticks = 0
    start = 0
    dt = MqlDateTime()
    if prev_calculated > 0:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        TimeToStruct(time[i], dt)
        ColorHistogram_2Buffer1[i] = high[i]
        ColorHistogram_2Buffer2[i] = low[i]
        day = dt.day_of_week
        ColorHistogram_2Colors[i] = day
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


class DrawColorHistogram2(_MQL5Indicator):
    name = 'draw_color_histogram2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 5,  # Number of ticks to change histogram properties
    }

