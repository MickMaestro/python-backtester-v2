"""draw_color_section — converted from MQL5: MQL5 Indicators/DRAW_COLOR_SECTION/draw_color_section.mq5

This indicator is a demo of DRAW_COLOR_SECTION drawing style
It plots color sections with specified number of bars
The section color, width and line style
are changed randomly after N ticks
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 9}, 'colors': {1: [255, 55295, 13434880, 65280, 16711935, 2763429, 9221330, 8721863]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ColorSection'}, 'levels': [], 'description': ['This indicator is a demo of DRAW_COLOR_SECTION drawing style', 'It plots color sections with specified number of bars', 'The section color, width and line style', 'are changed randomly after N ticks'], 'name': 'draw_color_section', 'source': 'MQL5 Indicators/DRAW_COLOR_SECTION/draw_color_section.mq5', 'folder': 'DRAW_COLOR_SECTION', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Ticks to change properties', 'sinput': False}, {'mql': 'bars_in_section', 'py': 'bars_in_section', 'param': 'bars_in_section', 'type': 'int', 'default': 5, 'label': 'Section width in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 5)  # Ticks to change properties
bars_in_section = _input('bars_in_section', 5)  # Section width in bars
divider = 0
color_sections = 0
ColorSectionBuffer = Arr(0, 0.0)
ColorSectionColors = Arr(0, 0.0)
colors = Arr.of([clrRed, clrBlue, clrGreen, clrChocolate, clrMagenta, clrDodgerBlue, clrGoldenrod, clrIndigo, clrLightBlue, clrAliceBlue, clrMoccasin, clrWhiteSmoke, clrCyan, clrMediumPurple], fill=0)
styles = Arr.of([STYLE_SOLID, STYLE_DASH, STYLE_DOT, STYLE_DASHDOT, STYLE_DASHDOTDOT], fill=0)

def OnInit():
    global color_sections, divider
    SetIndexBuffer(0, ColorSectionBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorSectionColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    color_sections = 8
    if bars_in_section <= 0:
        PrintFormat('Invalid section width=%d', bars_in_section)
        return INIT_PARAMETERS_INCORRECT
    else:
        divider = color_sections * bars_in_section
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
        if _imod(i, bars_in_section) == 0:
            ColorSectionBuffer[i] = high[i]
            rest = _imod(i, divider)
            color_indext = _idiv(rest, bars_in_section)
            ColorSectionColors[i] = color_indext
        else:
            ColorSectionBuffer[i] = 0.0
    return rates_total

def ChangeColors(cols, plot_colors):
    size = ArraySize(cols)
    comm = ChartGetString(0, CHART_COMMENT) + '\r\n\r\n'
    for plot_color_ind in range(0, plot_colors):
        number = MathRand()
        i = _imod(number, size)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, plot_color_ind, cols[i])
        comm = comm + StringFormat('SectionColorIndex[%d]=%s \r\n', plot_color_ind, ColorToString(cols[i], True))
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


class DrawColorSection(_MQL5Indicator):
    name = 'draw_color_section'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 5,  # Ticks to change properties
        'bars_in_section': 5,  # Section width in bars
    }

