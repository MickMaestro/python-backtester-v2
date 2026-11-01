"""candlesize — converted from MQL5: MQL5 Indicators/CandleSize/candlesize.mq5

The size in points of the last three candlesticks of the selected timeframe
Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The size in points of the last three candlesticks of the selected timeframe'], 'name': 'candlesize', 'source': 'MQL5 Indicators/CandleSize/candlesize.mq5', 'folder': 'CandleSize', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'financial asset', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Indicator timeframe for the indicator calculation', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'rising candlestick color', 'sinput': False}, {'mql': 'MdColor', 'py': 'MdColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'candlestick line color', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'falling candlestick color', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 13, 'label': 'font size', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'font type', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'location corner', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'vertical location', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'horizontal location', 'sinput': False}, {'mql': 'LableSirname', 'py': 'LableSirname', 'param': None, 'type': 'string', 'default': 'CandleSize 1', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

# ---- inputs and global variables
Symbol_ = _input('Symbol_', '')  # financial asset
Timeframe = _input('Timeframe', PERIOD_H6)  # Indicator timeframe for the indicator calculation
UpColor = _input('UpColor', clrTeal)  # rising candlestick color
MdColor = _input('MdColor', clrGray)  # candlestick line color
DnColor = _input('DnColor', clrMagenta)  # falling candlestick color
FontSize = _input('FontSize', 13)  # font size
FontType = _input('FontType', Font14)  # font type
WhatCorner = _input('WhatCorner', CORNER_LEFT_LOWER)  # location corner
Y_ = _input('Y_', 20)  # vertical location
X_ = _input('X_', 5)  # horizontal location
LableSirname = _input('LableSirname', 'CandleSize 1')
min_rates_total = 0
sFontType = ""
Lable1 = ""
Lable2 = ""
Lable3 = ""
Lable1_ = ""
Lable2_ = ""
Lable3_ = ""
symbol = ""
shift_1 = 0
shift_2 = 0
shift_3 = 0
X1 = 0
X2 = 0

def OnInit():
    global Lable1, Lable1_, Lable2, Lable2_, Lable3, Lable3_, X1, X2, min_rates_total, sFontType, shift_1, shift_2, shift_3, symbol
    min_rates_total = (1 + _idiv(PeriodSeconds(Timeframe), PeriodSeconds(PERIOD_CURRENT))) * 3
    if Symbol_ != '':
        symbol = Symbol_
    else:
        symbol = Symbol()
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()
    Lable1 = LableSirname + '_' + 'Candle_0'
    Lable2 = LableSirname + '_' + 'Candle_1'
    Lable3 = LableSirname + '_' + 'Candle_2'
    Lable1_ = LableSirname + '_' + 'Candle_0_'
    Lable2_ = LableSirname + '_' + 'Candle_1_'
    Lable3_ = LableSirname + '_' + 'Candle_2_'
    _sw1 = WhatCorner
    if _sw1 == CORNER_RIGHT_LOWER:
        shift_1 = _int(Y_ + (FontSize * 3.0))
        shift_2 = _int(Y_ + (FontSize * 1.5))
        shift_3 = _int(Y_ + 0)
        X1 = _int(X_ + (FontSize * 3))
        X2 = _int(X_)
    elif _sw1 == CORNER_LEFT_LOWER:
        shift_1 = _int(Y_ + (FontSize * 3.0))
        shift_2 = _int(Y_ + (FontSize * 1.5))
        shift_3 = _int(Y_ + 0)
        X1 = _int(X_)
        X2 = X_ + (FontSize * 5)
    elif _sw1 == CORNER_RIGHT_UPPER:
        shift_1 = _int(Y_ + 0)
        shift_2 = _int(Y_ + (FontSize * 1.5))
        shift_3 = _int(Y_ + (FontSize * 3.0))
        X1 = _int(X_ + (FontSize * 3))
        X2 = _int(X_)
    elif _sw1 == CORNER_LEFT_UPPER:
        shift_1 = _int(Y_ + 0)
        shift_2 = _int(Y_ + (FontSize * 1.5))
        shift_3 = _int(Y_ + (FontSize * 3.0))
        X1 = _int(X_)
        X2 = _int(X_ + (FontSize * 5))

def OnDeinit(reason):
    Deinit()
    ChartRedraw(0)

def Deinit():
    ObjectDelete(0, Lable1)
    ObjectDelete(0, Lable2)
    ObjectDelete(0, Lable3)
    ObjectDelete(0, Lable1_)
    ObjectDelete(0, Lable2_)
    ObjectDelete(0, Lable3_)

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
        ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
        ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    iHigh_ = Arr(3, 0.0, dyn=False)
    iLow_ = Arr(3, 0.0, dyn=False)
    iOpen_ = Arr(3, 0.0, dyn=False)
    iClose_ = Arr(3, 0.0, dyn=False)
    point = Box(0.0)
    Trend0 = 0.0
    Trend1 = 0.0
    Trend2 = 0.0
    Range0 = 0
    Range1 = 0
    Range2 = 0
    sRange0 = ""
    sRange1 = ""
    sRange2 = ""
    ColorX0 = 0
    ColorX1 = 0
    ColorX2 = 0
    if CopyLow(symbol, Timeframe, 0, 3, iLow_) <= 0:
        return 0
    if CopyHigh(symbol, Timeframe, 0, 3, iHigh_) <= 0:
        return 0
    if CopyOpen(symbol, Timeframe, 0, 3, iOpen_) <= 0:
        return 0
    if CopyClose(symbol, Timeframe, 0, 3, iClose_) <= 0:
        return 0
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return 0
    Range0 = _int(_fdiv(iHigh_[2] - iLow_[2], point.v))
    Range1 = _int(_fdiv(iHigh_[1] - iLow_[1], point.v))
    Range2 = _int(_fdiv(iHigh_[0] - iLow_[0], point.v))
    sRange0 = _str(Range0)
    sRange1 = _str(Range1)
    sRange2 = _str(Range2)
    Trend0 = iClose_[2] - iOpen_[2]
    Trend1 = iClose_[1] - iOpen_[1]
    Trend2 = iClose_[0] - iOpen_[0]
    if Trend0 > 0:
        ColorX0 = UpColor
    elif Trend0 < 0:
        ColorX0 = DnColor
    else:
        ColorX0 = MdColor
    if Trend1 > 0:
        ColorX1 = UpColor
    elif Trend1 < 0:
        ColorX1 = DnColor
    else:
        ColorX1 = MdColor
    if Trend2 > 0:
        ColorX2 = UpColor
    elif Trend2 < 0:
        ColorX2 = DnColor
    else:
        ColorX2 = MdColor
    SetTLabel(0, Lable1, 0, WhatCorner, 2 * WhatCorner, X1, shift_1, 'bar[0]: ', ColorX0, sFontType, FontSize)
    SetTLabel(0, Lable1_, 0, WhatCorner, 2 * WhatCorner, X2, shift_1, sRange0, ColorX0, sFontType, FontSize)
    SetTLabel(0, Lable2, 0, WhatCorner, 2 * WhatCorner, X1, shift_2, 'bar[1]: ', ColorX1, sFontType, FontSize)
    SetTLabel(0, Lable2_, 0, WhatCorner, 2 * WhatCorner, X2, shift_2, sRange1, ColorX1, sFontType, FontSize)
    SetTLabel(0, Lable3, 0, WhatCorner, 2 * WhatCorner, X1, shift_3, 'bar[2]: ', ColorX2, sFontType, FontSize)
    SetTLabel(0, Lable3_, 0, WhatCorner, 2 * WhatCorner, X2, shift_3, sRange2, ColorX2, sFontType, FontSize)
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Candlesize(_MQL5Indicator):
    name = 'candlesize'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Indicator timeframe for the indicator calculation
        'FontSize': 13,  # font size
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # font type
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # location corner
        'Y_': 20,  # vertical location
        'X_': 5,  # horizontal location
    }

