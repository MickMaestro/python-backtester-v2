"""ytg_spread_stoplevel — converted from MQL5: MQL5 Indicators/ytg_Spread_StopLevel/ytg_spread_stoplevel.mq5

Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [''], 'name': 'ytg_spread_stoplevel', 'source': 'MQL5 Indicators/ytg_Spread_StopLevel/ytg_spread_stoplevel.mq5', 'folder': 'ytg_Spread_StopLevel', 'inputs': [{'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'up color', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'down color', 'sinput': False}, {'mql': 'ZrColor', 'py': 'ZrColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'color for no change', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 11, 'label': 'font size', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'font type', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'location corner', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'vertical location', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'horizontal location', 'sinput': False}, {'mql': 'LableSirname', 'py': 'LableSirname', 'param': None, 'type': 'string', 'default': 'ytg_Spread_StopLevel', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

Gray = 0x808080  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Teal = 0x808000  # MQL4 colour name

# ---- inputs and global variables
FontSize = _input('FontSize', 11)  # font size
FontType = _input('FontType', Font14)  # font type
WhatCorner = _input('WhatCorner', CORNER_LEFT_LOWER)  # location corner
Y_ = _input('Y_', 20)  # vertical location
X_ = _input('X_', 5)  # horizontal location
LableSirname = _input('LableSirname', 'ytg_Spread_StopLevel')
sFontType = ""
Lable1 = ""
Lable2 = ""
shift_1 = 0
shift_2 = 0

def OnInit():
    global Lable1, Lable2, sFontType, shift_1, shift_2
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()
    Lable1 = LableSirname + '_' + _str(1)
    Lable2 = LableSirname + '_' + _str(2)
    _sw1 = WhatCorner
    if _sw1 == CORNER_RIGHT_LOWER:
        shift_1 = Y_ + 20
        shift_2 = Y_ + 0
    elif _sw1 == CORNER_LEFT_LOWER:
        shift_1 = Y_ + 20
        shift_2 = Y_ + 0
    else:
        shift_1 = Y_ + 0
        shift_2 = Y_ + 20

def OnDeinit(reason):
    Deinit()

def Deinit():
    ObjectDelete(0, Lable1)
    ObjectDelete(0, Lable2)

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

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_spread, _s_OnCalculate_prev_stoplevel
    SPREAD = spread[rates_total - 1]
    STOPS_LEVEL = _int(SymbolInfoInteger(Symbol(), SYMBOL_TRADE_STOPS_LEVEL))
    ColorGain1 = 0
    ColorGain2 = 0
    if SPREAD > _s_OnCalculate_prev_spread:
        ColorGain1 = UpColor
    elif SPREAD < _s_OnCalculate_prev_spread:
        ColorGain1 = DnColor
    else:
        ColorGain1 = ZrColor
    if STOPS_LEVEL > _s_OnCalculate_prev_stoplevel:
        ColorGain2 = UpColor
    elif STOPS_LEVEL < _s_OnCalculate_prev_stoplevel:
        ColorGain2 = DnColor
    else:
        ColorGain2 = ZrColor
    _s_OnCalculate_prev_spread = SPREAD
    _s_OnCalculate_prev_stoplevel = STOPS_LEVEL
    text1 = 'Spread ' + _str(SPREAD)
    text2 = 'Stop level ' + _str(STOPS_LEVEL)
    SetTLabel(0, Lable1, 0, WhatCorner, 2 * WhatCorner, X_, shift_1, text1, ColorGain1, sFontType, FontSize)
    SetTLabel(0, Lable2, 0, WhatCorner, 2 * WhatCorner, X_, shift_2, text2, ColorGain2, sFontType, FontSize)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
UpColor = _input('UpColor', _uint(Teal))  # up color
DnColor = _input('DnColor', _uint(Magenta))  # down color
ZrColor = _input('ZrColor', _uint(Gray))  # color for no change

# ---- static local variables
_s_OnCalculate_prev_spread = 0
_s_OnCalculate_prev_stoplevel = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YtgSpreadStoplevel(_MQL5Indicator):
    name = 'ytg_spread_stoplevel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FontSize': 11,  # font size
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # font type
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # location corner
        'Y_': 20,  # vertical location
        'X_': 5,  # horizontal location
    }

