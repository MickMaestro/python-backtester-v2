"""ytg_change_price_percent — converted from MQL5: MQL5 Indicators/ytg_Change_Price_Percent/ytg_change_price_percent.mq5

Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [''], 'name': 'ytg_change_price_percent', 'source': 'MQL5 Indicators/ytg_Change_Price_Percent/ytg_change_price_percent.mq5', 'folder': 'ytg_Change_Price_Percent', 'inputs': [{'mql': 'Symbol1', 'py': 'Symbol1', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': '', 'sinput': False}, {'mql': 'Symbol2', 'py': 'Symbol2', 'param': None, 'type': 'string', 'default': 'USDCHF', 'label': '', 'sinput': False}, {'mql': 'Symbol3', 'py': 'Symbol3', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': '', 'sinput': False}, {'mql': 'Symbol4', 'py': 'Symbol4', 'param': None, 'type': 'string', 'default': 'USDJPY', 'label': '', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'color for the upward move', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'color for the downward move', 'sinput': False}, {'mql': 'ZrColor', 'py': 'ZrColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'color for no change', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 11, 'label': 'font size', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'font type', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'location corner', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'vertical location', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'horizontal location', 'sinput': False}, {'mql': 'LableSirname', 'py': 'LableSirname', 'param': None, 'type': 'string', 'default': 'ytg_Change_Price_Percent 1', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

Gray = 0x808080  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Teal = 0x808000  # MQL4 colour name

# ---- inputs and global variables
Symbol1 = _input('Symbol1', 'EURUSD')
Symbol2 = _input('Symbol2', 'USDCHF')
Symbol3 = _input('Symbol3', 'GBPUSD')
Symbol4 = _input('Symbol4', 'USDJPY')
FontSize = _input('FontSize', 11)  # font size
FontType = _input('FontType', Font14)  # font type
WhatCorner = _input('WhatCorner', CORNER_LEFT_LOWER)  # location corner
Y_ = _input('Y_', 20)  # vertical location
X_ = _input('X_', 5)  # horizontal location
LableSirname = _input('LableSirname', 'ytg_Change_Price_Percent 1')
sFontType = ""
Lable1 = ""
Lable2 = ""
Lable3 = ""
Lable4 = ""
shift_1 = 0
shift_2 = 0
shift_3 = 0
shift_4 = 0

def OnInit():
    global Lable1, Lable2, Lable3, Lable4, sFontType, shift_1, shift_2, shift_3, shift_4
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()
    Lable1 = LableSirname + '_' + _str(1)
    Lable2 = LableSirname + '_' + _str(2)
    Lable3 = LableSirname + '_' + _str(3)
    Lable4 = LableSirname + '_' + _str(4)
    if not SymbolInfoInteger(Symbol1, SYMBOL_SELECT):
        if GetLastError() == ERR_MARKET_UNKNOWN_SYMBOL:
            Print('OnInit', '(): There is no such a symbol  - ', Symbol1, '!!!')
        if not SymbolSelect(Symbol1, True):
            Print('OnInit', '(): Failed to add a symbol ', Symbol1, ' to the MarketWatch window!!!')
    if not SymbolInfoInteger(Symbol2, SYMBOL_SELECT):
        if GetLastError() == ERR_MARKET_UNKNOWN_SYMBOL:
            Print('OnInit', '(): There is no such a symbol - ', Symbol2, '!!!')
        if not SymbolSelect(Symbol2, True):
            Print('OnInit', '(): Failed to add a symbol ', Symbol2, ' to the MarketWatch window!!!')
    if not SymbolInfoInteger(Symbol3, SYMBOL_SELECT):
        if GetLastError() == ERR_MARKET_UNKNOWN_SYMBOL:
            Print('OnInit', '(): There is no such a symbol - ', Symbol3, '!!!')
        if not SymbolSelect(Symbol3, True):
            Print('OnInit', '(): Failed to add a symbol ', Symbol3, ' to the MarketWatch window')
    if not SymbolInfoInteger(Symbol4, SYMBOL_SELECT):
        if GetLastError() == ERR_MARKET_UNKNOWN_SYMBOL:
            Print('OnInit', '(): There is no such a symbol  - ', Symbol4, '!!!')
        if not SymbolSelect(Symbol4, True):
            Print('OnInit', '(): Failed to add a symbol ', Symbol4, ' to the MarketWatch window!!!')
    _sw1 = WhatCorner
    if _sw1 == CORNER_RIGHT_LOWER:
        shift_1 = Y_ + 60
        shift_2 = Y_ + 40
        shift_3 = Y_ + 20
        shift_4 = Y_ + 0
    elif _sw1 == CORNER_LEFT_LOWER:
        shift_1 = Y_ + 60
        shift_2 = Y_ + 40
        shift_3 = Y_ + 20
        shift_4 = Y_ + 0
    else:
        shift_1 = Y_ + 0
        shift_2 = Y_ + 20
        shift_3 = Y_ + 40
        shift_4 = Y_ + 60

def OnDeinit(reason):
    Deinit()

def Deinit():
    ObjectDelete(0, Lable1)
    ObjectDelete(0, Lable2)
    ObjectDelete(0, Lable3)
    ObjectDelete(0, Lable4)

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

def StringWordConvertor(Name, OpPrice, ClPrice, digits):
    word = Name
    word = word + DoubleToString(OpPrice, digits) + '/'
    word = word + DoubleToString(ClPrice, digits) + ' ['
    dPrice = ClPrice - OpPrice
    word = word + DoubleToString(MathPow(10, digits) * MathAbs(dPrice), 0) + '|'
    word = word + DoubleToString(100 * _fdiv(MathAbs(dPrice), OpPrice), 2) + '%]'
    return word

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    Price1 = Arr(2, 0.0, dyn=False)
    Price2 = Arr(2, 0.0, dyn=False)
    Price3 = Arr(2, 0.0, dyn=False)
    Price4 = Arr(2, 0.0, dyn=False)
    if CopyClose(Symbol1, PERIOD_D1, 0, 2, Price1) <= 0:
        return 0
    if CopyClose(Symbol2, PERIOD_D1, 0, 2, Price2) <= 0:
        return 0
    if CopyClose(Symbol3, PERIOD_D1, 0, 2, Price3) <= 0:
        return 0
    if CopyClose(Symbol4, PERIOD_D1, 0, 2, Price4) <= 0:
        return 0
    sym_1 = _fdiv((Price1[1] - Price1[0]) * 100, Price1[0])
    sym_2 = _fdiv((Price2[1] - Price2[0]) * 100, Price2[0])
    sym_3 = _fdiv((Price3[1] - Price3[0]) * 100, Price3[0])
    sym_4 = _fdiv((Price4[1] - Price4[0]) * 100, Price4[0])
    ColorGain1 = ZrColor
    ColorGain2 = ZrColor
    ColorGain3 = ZrColor
    ColorGain4 = ZrColor
    Symbol_1 = Symbol1 + ' = ' + DoubleToString(sym_1, 4) + ' %'
    Symbol_2 = Symbol2 + ' = ' + DoubleToString(sym_2, 4) + ' %'
    Symbol_3 = Symbol3 + ' = ' + DoubleToString(sym_3, 4) + ' %'
    Symbol_4 = Symbol4 + ' = ' + DoubleToString(sym_4, 4) + ' %'
    if sym_1 < 0:
        ColorGain1 = DnColor
    else:
        ColorGain1 = UpColor
    if sym_2 < 0:
        ColorGain2 = DnColor
    else:
        ColorGain2 = UpColor
    if sym_3 < 0:
        ColorGain3 = DnColor
    else:
        ColorGain3 = UpColor
    if sym_4 < 0:
        ColorGain4 = DnColor
    else:
        ColorGain4 = UpColor
    SetTLabel(0, Lable1, 0, WhatCorner, 2 * WhatCorner, X_, shift_1, Symbol_1, ColorGain1, sFontType, FontSize)
    SetTLabel(0, Lable2, 0, WhatCorner, 2 * WhatCorner, X_, shift_2, Symbol_2, ColorGain2, sFontType, FontSize)
    SetTLabel(0, Lable3, 0, WhatCorner, 2 * WhatCorner, X_, shift_3, Symbol_3, ColorGain3, sFontType, FontSize)
    SetTLabel(0, Lable4, 0, WhatCorner, 2 * WhatCorner, X_, shift_4, Symbol_4, ColorGain4, sFontType, FontSize)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
UpColor = _input('UpColor', _uint(Teal))  # color for the upward move
DnColor = _input('DnColor', _uint(Magenta))  # color for the downward move
ZrColor = _input('ZrColor', _uint(Gray))  # color for no change


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YtgChangePricePercent(_MQL5Indicator):
    name = 'ytg_change_price_percent'
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

