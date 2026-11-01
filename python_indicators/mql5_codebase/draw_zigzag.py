"""draw_zigzag — converted from MQL5: MQL5 Indicators/DRAW_ZIGZAG/draw_zigzag.mq5

This indicator is a demo of DRAW_ZIGZAG drawing style
It plots a \\"saw\\", using the High/Low of the bar
There is a week day with invisible values (defined randomly at the start)
The sections color, width and style changed randomly
after N ticks
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ZigZag'}, 'levels': [], 'description': ['This indicator is a demo of DRAW_ZIGZAG drawing style', 'It plots a \\"saw\\", using the High/Low of the bar', 'There is a week day with invisible values (defined randomly at the start)', 'The sections color, width and style changed randomly', 'after N ticks'], 'name': 'draw_zigzag', 'source': 'MQL5 Indicators/DRAW_ZIGZAG/draw_zigzag.mq5', 'folder': 'DRAW_ZIGZAG', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Ticks to change properties', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 5)  # Ticks to change properties
ZigZagBuffer1 = Arr(0, 0.0)
ZigZagBuffer2 = Arr(0, 0.0)
invisible_day = 0
colors = Arr.of([clrRed, clrBlue, clrGreen], fill=0)
styles = Arr.of([STYLE_SOLID, STYLE_DASH, STYLE_DOT, STYLE_DASHDOT, STYLE_DASHDOTDOT], fill=0)

def OnInit():
    global invisible_day
    SetIndexBuffer(0, ZigZagBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ZigZagBuffer2, INDICATOR_DATA)
    invisible_day = _imod(MathRand(), 6)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'ZigZag1;ZigZag2')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks
    _s_OnCalculate_ticks += 1
    if _s_OnCalculate_ticks >= N:
        ChangeLineAppearance()
        _s_OnCalculate_ticks = 0
    dt = MqlDateTime()
    start = 0
    if prev_calculated != 0:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        TimeToStruct(time[i], dt)
        if dt.day_of_week == invisible_day:
            ZigZagBuffer1[i] = 0.0
            ZigZagBuffer2[i] = 0.0
        else:
            if _imod(i, 2) == 0:
                ZigZagBuffer1[i] = high[i]
                ZigZagBuffer2[i] = low[i]
            else:
                ZigZagBuffer1[i] = low[i]
                ZigZagBuffer2[i] = high[i]
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
    comm = '\r\nInvisible day - ' + EnumToString(invisible_day, 'ENUM_DAY_OF_WEEK') + comm
    Comment(comm)

# ---- static local variables
_s_OnCalculate_ticks = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DrawZigzag(_MQL5Indicator):
    name = 'draw_zigzag'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'N': 5,  # Ticks to change properties
    }

