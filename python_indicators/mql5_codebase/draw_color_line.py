"""draw_color_line — converted from MQL5: MQL5 Indicators/DRAW_COLOR_LINE/draw_color_line.mq5

This indicator is a demo of DRAW_COLOR_LINE drawing style
It draws a line with different colors using the Close price
The line width, style and color are changed randomly after N ticks.
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [255, 16711680, 32768, 42495, 9639167]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ColorLine'}, 'levels': [], 'description': ['This indicator is a demo of DRAW_COLOR_LINE drawing style', 'It draws a line with different colors using the Close price', 'The line width, style and color are changed randomly after N ticks.'], 'name': 'draw_color_line', 'source': 'MQL5 Indicators/DRAW_COLOR_LINE/draw_color_line.mq5', 'folder': 'DRAW_COLOR_LINE', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Number of ticks to change properties', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 20, 'label': 'Same color interval (in bars)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 5)  # Number of ticks to change properties
Length = _input('Length', 20)  # Same color interval (in bars)
line_colors = 5  # Number of colors - see #property indicator_color1
ColorLineBuffer = Arr(0, 0.0)
ColorLineColors = Arr(0, 0.0)
colors = Arr.of([clrRed, clrBlue, clrGreen, clrChocolate, clrMagenta, clrDodgerBlue, clrGoldenrod], fill=0)
styles = Arr.of([STYLE_SOLID, STYLE_DASH, STYLE_DOT, STYLE_DASHDOT, STYLE_DASHDOTDOT], fill=0)

def OnInit():
    SetIndexBuffer(0, ColorLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorLineColors, INDICATOR_COLOR_INDEX)
    MathSrand(GetTickCount())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks
    _s_OnCalculate_ticks += 1
    if _s_OnCalculate_ticks >= N:
        ChangeLineAppearance()
        ChangeColors(colors, 5)
        _s_OnCalculate_ticks = 0
    for i in range(0, rates_total):
        ColorLineBuffer[i] = close[i]
        color_index = _imod(i, 5 * Length)
        color_index = _idiv(color_index, Length)
        ColorLineColors[i] = color_index
    return rates_total

def ChangeColors(cols, plot_colors):
    size = ArraySize(cols)
    comm = ChartGetString(0, CHART_COMMENT) + '\r\n\r\n'
    for plot_color_ind in range(0, plot_colors):
        number = MathRand()
        i = _imod(number, size)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, plot_color_ind, cols[i])
        comm = comm + StringFormat('LineColorIndex[%d]=%s \r\n', plot_color_ind, ColorToString(cols[i], True))
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


class DrawColorLine(_MQL5Indicator):
    name = 'draw_color_line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'N': 5,  # Number of ticks to change properties
        'Length': 20,  # Same color interval (in bars)
    }

