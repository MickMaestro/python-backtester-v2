"""spreadinfo — converted from MQL5: MQL5 Indicators/SpreadInfo/spreadinfo.mq5

The indicator displays spread, averaged spread and their ratio in one of the chart corners
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The indicator displays spread, averaged spread and their ratio in one of the chart corners'], 'name': 'spreadinfo', 'source': 'MQL5 Indicators/SpreadInfo/spreadinfo.mq5', 'folder': 'SpreadInfo', 'inputs': [{'mql': 'SpName', 'py': 'SpName', 'param': None, 'type': 'string', 'default': 'Spread', 'label': 'Spread name', 'sinput': False}, {'mql': 'MaSpName', 'py': 'MaSpName', 'param': None, 'type': 'string', 'default': 'MASpread', 'label': 'Average spread name', 'sinput': False}, {'mql': 'RatioName', 'py': 'RatioName', 'param': None, 'type': 'string', 'default': 'Ratio', 'label': 'Spread and its average value ratio name', 'sinput': False}, {'mql': 'TextColor1', 'py': 'TextColor1', 'param': None, 'type': 'color', 'default': 0, 'label': 'Spread color', 'sinput': False}, {'mql': 'TextColor2', 'py': 'TextColor2', 'param': None, 'type': 'color', 'default': 0, 'label': 'Average spread color', 'sinput': False}, {'mql': 'TextColor3', 'py': 'TextColor3', 'param': None, 'type': 'color', 'default': 0, 'label': 'Spread and its average value ratio color', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 15, 'label': 'Font size', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'Font type', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Location corner', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 1, 'label': 'Vertical location', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'Horizontal location', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 100, 'label': 'Spread smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh', 'SmoothAlgorithms.mqh']}

Blue = 0xFF0000  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
SpName = _input('SpName', 'Spread')  # Spread name
MaSpName = _input('MaSpName', 'MASpread')  # Average spread name
RatioName = _input('RatioName', 'Ratio')  # Spread and its average value ratio name
FontSize = _input('FontSize', 15)  # Font size
FontType = _input('FontType', Font14)  # Font type
WhatCorner = _input('WhatCorner', CORNER_RIGHT_UPPER)  # Location corner
Y_ = _input('Y_', 1)  # Vertical location
X_ = _input('X_', 5)  # Horizontal location
period = _input('period', 100)  # Spread smoothing period
sFontType = ""
min_rates_total = 0

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
    global min_rates_total, sFontType
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    min_rates_total = period
    Deinit()

def Deinit():
    ObjectDelete(0, 'Spread_Label_1')
    ObjectDelete(0, 'Spread_Label_2')
    ObjectDelete(0, 'Spread_Label_3')

def OnDeinit(reason):
    Deinit()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ratio = 0.0
    MaSpread = 0.0
    first = 0
    bar = 0
    sMaSpread = ""
    sSpread = ""
    sRatio = ""
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        MaSpread = _s_OnCalculate_SMA.SMASeries(0, prev_calculated, rates_total, period, spread[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    sMaSpread = MaSpName + ': ' + DoubleToString(MaSpread, 0)
    sSpread = SpName + ': ' + _str(spread[rates_total - 1])
    ratio = _fdiv(spread[rates_total - 1], MaSpread)
    sRatio = RatioName + ': ' + DoubleToString(ratio, 2)
    SetTLabel(0, 'Spread_Label_1', 0, WhatCorner, 2 * WhatCorner, X_, Y_ + 0, sSpread, TextColor1, sFontType, FontSize)
    SetTLabel(0, 'Spread_Label_2', 0, WhatCorner, 2 * WhatCorner, X_, Y_ + 20, sMaSpread, TextColor2, sFontType, FontSize)
    SetTLabel(0, 'Spread_Label_3', 0, WhatCorner, 2 * WhatCorner, X_, Y_ + 40, sRatio, TextColor3, sFontType, FontSize)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
TextColor1 = _input('TextColor1', _uint(Magenta))  # Spread color
TextColor2 = _input('TextColor2', _uint(Blue))  # Average spread color
TextColor3 = _input('TextColor3', _uint(Red))  # Spread and its average value ratio color

# ---- static local variables
_s_OnCalculate_SMA = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Spreadinfo(_MQL5Indicator):
    name = 'spreadinfo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FontSize': 15,  # Font size
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # Font type
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Location corner
        'Y_': 1,  # Vertical location
        'X_': 5,  # Horizontal location
        'period': 100,  # Spread smoothing period
    }

