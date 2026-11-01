"""positioninfo — converted from MQL5: MQL5 Indicators/PositionInfo/positioninfo.mq5

Indicator of state of open position
Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Indicator of state of open position'], 'name': 'positioninfo', 'source': 'MQL5 Indicators/PositionInfo/positioninfo.mq5', 'folder': 'PositionInfo', 'inputs': [{'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'color of profitable position', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'color of unprofitable position', 'sinput': False}, {'mql': 'ZrColor', 'py': 'ZrColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'color of position without profit', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 15, 'label': 'font size', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'font type', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'location corner', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 1, 'label': 'vertical location', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'horizontal location', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

Gray = 0x808080  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
FontSize = _input('FontSize', 15)  # font size
FontType = _input('FontType', Font14)  # font type
WhatCorner = _input('WhatCorner', CORNER_LEFT_LOWER)  # location corner
Y_ = _input('Y_', 1)  # vertical location
X_ = _input('X_', 5)  # horizontal location
sFontType = ""

def OnInit():
    global sFontType
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()

def OnDeinit(reason):
    Deinit()

def Deinit():
    ObjectDelete(0, 'PositionInfo_Label_1')
    ObjectDelete(0, 'PositionInfo_Label_2')
    ObjectDelete(0, 'PositionInfo_Label_3')
    ObjectDelete(0, 'PositionInfo_Label_4')
    ObjectDelete(0, 'PositionInfo_Label_5')

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
    Res = PositionSelect(Symbol())
    PosType = PositionGetInteger(POSITION_TYPE)
    if (not Res) or (PosType != POSITION_TYPE_SELL and PosType != POSITION_TYPE_BUY):
        Deinit()
        return rates_total
    sPosType = ""
    Color = 0
    nStop = 0
    nTake = 0
    nProfit = 0
    point = 0.0
    price = 0.0
    Stop = 0.0
    Take = 0.0
    Profit = 0.0
    OpenPrice = 0.0
    point = SymbolInfoDouble(Symbol(), SYMBOL_POINT)
    digit = _int(SymbolInfoInteger(Symbol(), SYMBOL_DIGITS))
    if PosType == POSITION_TYPE_BUY:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    else:
        price = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
    if ((not digit) or (not point)) or (not price):
        return TRADE_RETCODE_ERROR
    Stop = PositionGetDouble(POSITION_SL)
    Take = PositionGetDouble(POSITION_TP)
    Profit = PositionGetDouble(POSITION_PROFIT)
    OpenPrice = PositionGetDouble(POSITION_PRICE_OPEN)
    if PosType == POSITION_TYPE_BUY:
        if Stop:
            nStop = _int(_fdiv(price - Stop, Point()))
        else:
            nStop = 0
        if Take:
            nTake = _int(_fdiv(Take - price, Point()))
        else:
            nTake = 0
        nProfit = _int(_fdiv(price - OpenPrice, Point()))
        sPosType = 'BUY'
    else:
        if Stop:
            nStop = _int(_fdiv(Stop - price, Point()))
        else:
            nStop = 0
        if Take:
            nTake = _int(_fdiv(price - Take, Point()))
        else:
            nTake = 0
        nProfit = _int(_fdiv(OpenPrice - price, Point()))
        sPosType = 'SELL'
    if Profit > 0:
        Color = UpColor
    elif Profit < 0:
        Color = DnColor
    else:
        Color = ZrColor
    sStop = ""
    sTake = ""
    sNProfit = ""
    sPProfit = ""
    sPProfit = 'Profit = ' + DoubleToString(Profit, 2)
    sNProfit = 'Point Profit = ' + _str(nProfit)
    if Stop:
        sStop = 'SL = ' + _str(nStop)
    else:
        sStop = 'SL = None'
    if Take:
        sTake = 'TP = ' + _str(nTake)
    else:
        sTake = 'TP = None'
    shift_1 = 0
    shift_2 = 0
    shift_3 = 0
    shift_4 = 0
    shift_5 = 0
    _sw1 = WhatCorner
    if _sw1 == CORNER_RIGHT_LOWER:
        shift_1 = 80
        shift_2 = 60
        shift_3 = 40
        shift_4 = 20
        shift_5 = 0
    elif _sw1 == CORNER_LEFT_LOWER:
        shift_1 = 80
        shift_2 = 60
        shift_3 = 40
        shift_4 = 20
        shift_5 = 0
    else:
        shift_1 = 0
        shift_2 = 20
        shift_3 = 40
        shift_4 = 60
        shift_5 = 80
    SetTLabel(0, 'PositionInfo_Label_1', 0, WhatCorner, 2 * WhatCorner, X_, Y_ + shift_1, sPosType, Color, sFontType, FontSize)
    SetTLabel(0, 'PositionInfo_Label_2', 0, WhatCorner, 2 * WhatCorner, X_, Y_ + shift_2, sPProfit, Color, sFontType, FontSize)
    SetTLabel(0, 'PositionInfo_Label_3', 0, WhatCorner, 2 * WhatCorner, X_, Y_ + shift_3, sNProfit, Color, sFontType, FontSize)
    SetTLabel(0, 'PositionInfo_Label_4', 0, WhatCorner, 2 * WhatCorner, X_, Y_ + shift_4, sTake, Color, sFontType, FontSize)
    SetTLabel(0, 'PositionInfo_Label_5', 0, WhatCorner, 2 * WhatCorner, X_, Y_ + shift_5, sStop, Color, sFontType, FontSize)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
UpColor = _input('UpColor', _uint(Lime))  # color of profitable position
DnColor = _input('DnColor', _uint(Red))  # color of unprofitable position
ZrColor = _input('ZrColor', _uint(Gray))  # color of position without profit


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Positioninfo(_MQL5Indicator):
    name = 'positioninfo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FontSize': 15,  # font size
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # font type
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # location corner
        'Y_': 1,  # vertical location
        'X_': 5,  # horizontal location
    }

