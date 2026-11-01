"""bartimer — converted from MQL5: MQL5 Indicators/BarTimer/bartimer.mq5

Copyright: Copyright © 2008, Art Royal s.r.o.; Link: http://www.jiport.com/; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Art Royal s.r.o.', 'link': 'http://www.jiport.com/', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'bartimer', 'source': 'MQL5 Indicators/BarTimer/bartimer.mq5', 'folder': 'BarTimer', 'inputs': [{'mql': 'Corner', 'py': 'Corner', 'param': 'Corner', 'type': 'int', 'default': 1, 'label': 'Location corner', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'Font type', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 14, 'label': 'Font size', 'sinput': False}, {'mql': 'FontColor', 'py': 'FontColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Text color', 'sinput': False}, {'mql': 'XDistance', 'py': 'XDistance', 'param': 'XDistance', 'type': 'int', 'default': 250, 'label': 'X distance from the reference angle', 'sinput': False}, {'mql': 'YDistance', 'py': 'YDistance', 'param': 'YDistance', 'type': 'int', 'default': 0, 'label': 'Y distance from the reference angle', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
Corner = _input('Corner', CORNER_LEFT_LOWER)  # Location corner
FontType = _input('FontType', 'Arial')  # Font type
FontSize = _input('FontSize', 14)  # Font size
XDistance = _input('XDistance', 250)  # X distance from the reference angle
YDistance = _input('YDistance', 0)  # Y distance from the reference angle
lenbase = 0
s_base = ':...:...:...:...:'  # the string for the informer with a slider

def CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size):
    ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chart_id, name, OBJPROP_CORNER, corner)
    ObjectSetInteger(chart_id, name, OBJPROP_ANCHOR, point)
    ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
    ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size):
    if ObjectFind(chart_id, name) == -1:
        CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
        ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnInit():
    global lenbase
    lenbase = StringLen(s_base)

def OnDeinit(reason):
    if ObjectFind(0, 'BarTimer') != -1:
        ObjectDelete(0, 'BarTimer')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    sec = 0
    pc = 0.0
    Time = Box('')
    s_end = ''
    s_beg = ''
    sec = _int(TimeCurrent() - time[rates_total - 1])
    i = _idiv((lenbase - 1) * sec, PeriodSeconds())
    pc = _fdiv(100.0 * sec, PeriodSeconds())
    if i > (lenbase - 1):
        i = lenbase - 1
    if i > 0:
        s_beg = StringSubstr(s_base, 0, i)
    if i < (lenbase - 1):
        s_end = StringSubstr(s_base, i + 1, lenbase - i - 1)
    StringConcatenate(Time, s_beg, '|', s_end, '  ', DoubleToString(pc, 0), '%')
    SetTLabel(0, 'BarTimer', 0, Corner, 2 * Corner, XDistance, YDistance, Time.v, FontColor, FontType, FontSize)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
FontColor = _input('FontColor', _uint(Red))  # Text color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bartimer(_MQL5Indicator):
    name = 'bartimer'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Corner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Location corner
        'FontSize': 14,  # Font size
        'XDistance': 250,  # X distance from the reference angle
        'YDistance': 0,  # Y distance from the reference angle
    }

