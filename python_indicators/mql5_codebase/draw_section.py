"""draw_section — converted from MQL5: MQL5 Indicators/DRAW_SECTION/draw_section.mq5

This indicator is a demo of DRAW_SECTION drawing style
It draws a sections
The color, width and style of the sections changes
every N ticks
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Section'}, 'levels': [], 'description': ['This indicator is a demo of DRAW_SECTION drawing style', 'It draws a sections', 'The color, width and style of the sections changes', 'every N ticks'], 'name': 'draw_section', 'source': 'MQL5 Indicators/DRAW_SECTION/draw_section.mq5', 'folder': 'DRAW_SECTION', 'inputs': [{'mql': 'bars', 'py': 'bars', 'param': 'bars', 'type': 'int', 'default': 5, 'label': 'Section length in bars', 'sinput': False}, {'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Number of ticks to change color/width/style of the section', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
bars = _input('bars', 5)  # Section length in bars
N = _input('N', 5)  # Number of ticks to change color/width/style of the section
SectionBuffer = Arr(0, 0.0)
divider = 0
colors = Arr.of([clrRed, clrBlue, clrGreen], fill=0)
styles = Arr.of([STYLE_SOLID, STYLE_DASH, STYLE_DOT, STYLE_DASHDOT, STYLE_DASHDOTDOT], fill=0)

def OnInit():
    global divider
    SetIndexBuffer(0, SectionBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    if bars <= 0:
        PrintFormat('Invalid input parameter bar=%d', bars)
        return INIT_PARAMETERS_INCORRECT
    else:
        divider = 2 * bars
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks
    _s_OnCalculate_ticks += 1
    if _s_OnCalculate_ticks >= N:
        ChangeLineAppearance()
        _s_OnCalculate_ticks = 0
    start = 0
    if prev_calculated > 0:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        rest = _imod(i, divider)
        if rest == 0:
            SectionBuffer[i] = high[i]
        else:
            if rest == bars:
                SectionBuffer[i] = low[i]
            else:
                SectionBuffer[i] = 0.0
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
    size = ArraySize(styles)
    style_index = _imod(number, size)
    PlotIndexSetInteger(0, PLOT_LINE_STYLE, styles[style_index])
    comm = '\r\n' + EnumToString(styles[style_index], 'ENUM_LINE_STYLE') + '' + comm
    Comment(comm)

# ---- static local variables
_s_OnCalculate_ticks = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DrawSection(_MQL5Indicator):
    name = 'draw_section'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'bars': 5,  # Section length in bars
        'N': 5,  # Number of ticks to change color/width/style of the section
    }

