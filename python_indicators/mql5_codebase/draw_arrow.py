"""draw_arrow — converted from MQL5: MQL5 Indicators/DRAW_ARROW/draw_arrow.mq5

This indicator is a demo of DRAW_ARROW drawing style
It draws arrows, defined by Unicode symbols
The color, width, shift and symbol code changed randomly
after N ticks
Code of the base char : code=159 (circle)
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Arrows'}, 'levels': [], 'description': ['This indicator is a demo of DRAW_ARROW drawing style', 'It draws arrows, defined by Unicode symbols', 'The color, width, shift and symbol code changed randomly', 'after N ticks', 'Code of the base char : code=159 (circle)'], 'name': 'draw_arrow', 'source': 'MQL5 Indicators/DRAW_ARROW/draw_arrow.mq5', 'folder': 'DRAW_ARROW', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Ticks to change properties', 'sinput': False}, {'mql': 'code', 'py': 'code', 'param': 'code', 'type': 'ushort', 'default': 159, 'label': 'Code of the char to draw (DRAW_ARROW style)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 5)  # Ticks to change properties
code = _input('code', 159)  # Code of the char to draw (DRAW_ARROW style)
ArrowsBuffer = Arr(0, 0.0)
colors = Arr.of([clrRed, clrBlue, clrGreen], fill=0)

def OnInit():
    SetIndexBuffer(0, ArrowsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, code)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, 5)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks
    _s_OnCalculate_ticks += 1
    if _s_OnCalculate_ticks >= N:
        ChangeLineAppearance()
        _s_OnCalculate_ticks = 0
    start = 1
    if prev_calculated > 0:
        start = prev_calculated - 1
    for i in range(1, rates_total):
        if close[i] > close[i - 1]:
            ArrowsBuffer[i] = close[i]
        else:
            ArrowsBuffer[i] = 0.0
    return rates_total

def ChangeLineAppearance():
    comm = ''
    number = MathRand()
    size = ArraySize(colors)
    color_index = _imod(number, size)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, colors[color_index])
    comm = comm + '\r\n' + _str(colors[color_index])
    number = MathRand()
    width = _imod(number, 5)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, width)
    comm = comm + '\r\nWidth=' + IntegerToString(width)
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


class DrawArrow(_MQL5Indicator):
    name = 'draw_arrow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 5,  # Ticks to change properties
        'code': 159,  # Code of the char to draw (DRAW_ARROW style)
    }

