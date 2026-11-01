"""draw_color_arrow — converted from MQL5: MQL5 Indicators/DRAW_COLOR_ARROW/draw_color_arrow.mq5

This indicator is a demo of DRAW_COLOR_ARROW drawing style
It plots arrows on the chart, using the symbols from Windings font
The color, char size and shift are changed randomly after N ticks
The code parameter is used to specify the base code: code=159 (circle)
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [255, 16711680, 5737262, 55295, 36095, 16711935, 3329434, 1993170]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ColorArrow'}, 'levels': [], 'description': ['This indicator is a demo of DRAW_COLOR_ARROW drawing style', 'It plots arrows on the chart, using the symbols from Windings font', 'The color, char size and shift are changed randomly after N ticks', 'The code parameter is used to specify the base code: code=159 (circle)'], 'name': 'draw_color_arrow', 'source': 'MQL5 Indicators/DRAW_COLOR_ARROW/draw_color_arrow.mq5', 'folder': 'DRAW_COLOR_ARROW', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Ticks to change', 'sinput': False}, {'mql': 'code', 'py': 'code', 'param': 'code', 'type': 'ushort', 'default': 159, 'label': 'Symbol code for DRAW_ARROW', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 5)  # Ticks to change
code = _input('code', 159)  # Symbol code for DRAW_ARROW
color_sections = 0
ColorArrowBuffer = Arr(0, 0.0)
ColorArrowColors = Arr(0, 0.0)
colors = Arr.of([clrRed, clrBlue, clrGreen, clrChocolate, clrMagenta, clrDodgerBlue, clrGoldenrod, clrIndigo, clrLightBlue, clrAliceBlue, clrMoccasin, clrWhiteSmoke, clrCyan, clrMediumPurple], fill=0)

def OnInit():
    global color_sections
    SetIndexBuffer(0, ColorArrowBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorArrowColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_ARROW, code)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, 5)
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
    start = 1
    if prev_calculated > 0:
        start = prev_calculated - 1
    for i in range(1, rates_total):
        if close[i] > close[i - 1]:
            ColorArrowBuffer[i] = close[i]
        else:
            ColorArrowBuffer[i] = 0.0
        index = _imod(i, color_sections)
        ColorArrowColors[i] = index
    return rates_total

def ChangeColors(cols, plot_colors):
    size = ArraySize(cols)
    comm = ChartGetString(0, CHART_COMMENT) + '\r\n\r\n'
    for plot_color_ind in range(0, plot_colors):
        number = MathRand()
        i = _imod(number, size)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, plot_color_ind, cols[i])
        comm = comm + StringFormat('ArrowColorIndex[%d]=%s \r\n', plot_color_ind, ColorToString(cols[i], True))
        ChartSetString(0, CHART_COMMENT, comm)

def ChangeLineAppearance():
    comm = ''
    number = MathRand()
    width = _imod(number, 5)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, width)
    comm = comm + ' Width=' + IntegerToString(width)
    number = MathRand()
    code_add = _imod(number, 20)
    PlotIndexSetInteger(0, PLOT_ARROW, code + code_add)
    comm = '\r\n' + 'PLOT_ARROW=' + IntegerToString(code + code_add) + comm
    number = MathRand()
    shift = 20 - _imod(number, 41)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, shift)
    comm = '\r\n' + 'PLOT_ARROW_SHIFT=' + IntegerToString(shift) + comm
    Comment(comm)

# ---- static local variables
_s_OnCalculate_ticks = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DrawColorArrow(_MQL5Indicator):
    name = 'draw_color_arrow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 5,  # Ticks to change
        'code': 159,  # Symbol code for DRAW_ARROW
    }

