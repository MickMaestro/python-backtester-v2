"""magnified_market_price — converted from MQL5: MQL5 Indicators/Magnified Market Price/magnified_market_price.mq5

Copyright: Copyright © 2005, Habeeb; Link: http://www.metaquotes.net/; Version: 1.5

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Habeeb', 'link': 'http://www.metaquotes.net/', 'version': '1.5', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'magnified_market_price', 'source': 'MQL5 Indicators/Magnified Market Price/magnified_market_price.mq5', 'folder': 'Magnified Market Price', 'inputs': [{'mql': 'PriceType', 'py': 'PriceType', 'param': 'PriceType', 'type': 'int', 'default': 0, 'label': 'Displayed price type', 'sinput': False}, {'mql': 'CutPrice', 'py': 'CutPrice', 'param': 'CutPrice', 'type': 'bool', 'default': False, 'label': 'Last figure removal flag', 'sinput': False}, {'mql': 'ResetColors', 'py': 'ResetColors', 'param': 'ResetColors', 'type': 'bool', 'default': True, 'label': 'Colors reset flag', 'sinput': False}, {'mql': 'UpPriceColor', 'py': 'UpPriceColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Rising price color', 'sinput': False}, {'mql': 'PriceColor', 'py': 'PriceColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Unchanged price color', 'sinput': False}, {'mql': 'DnPriceColor', 'py': 'DnPriceColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Falling price color', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 24, 'label': 'Font size', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 7, 'label': 'Font type', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'Location corner', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Gray = 0x808080  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# enum type_price
MODE_BID = 0
MODE_ASK = 1
_enum('type_price', {0: 'MODE_BID', 1: 'MODE_ASK'})

# enum type_font
Font0 = 0
Font1 = 1
Font2 = 2
Font3 = 3
Font4 = 4
Font5 = 5
Font6 = 6
Font7 = 7
Font8 = 8
Font9 = 9
Font10 = 10
Font11 = 11
Font12 = 12
Font13 = 13
Font14 = 14
Font15 = 15
Font16 = 16
Font17 = 17
Font18 = 18
Font19 = 19
Font20 = 20
Font21 = 21
Font22 = 22
Font23 = 23
Font24 = 24
Font25 = 25
Font26 = 26
Font27 = 27
Font28 = 28
Font29 = 29
Font30 = 30
Font31 = 31
Font32 = 32
Font33 = 33
Font34 = 34
Font35 = 35
Font36 = 36
Font37 = 37
Font38 = 38
Font39 = 39
Font40 = 40
Font41 = 41
Font42 = 42
Font43 = 43
Font44 = 44
Font45 = 45
Font46 = 46
Font47 = 47
Font48 = 48
Font49 = 49
Font50 = 50
Font51 = 51
Font52 = 52
Font53 = 53
Font54 = 54
Font55 = 55
Font56 = 56
_enum('type_font', {0: 'Font0', 1: 'Font1', 2: 'Font2', 3: 'Font3', 4: 'Font4', 5: 'Font5', 6: 'Font6', 7: 'Font7', 8: 'Font8', 9: 'Font9', 10: 'Font10', 11: 'Font11', 12: 'Font12', 13: 'Font13', 14: 'Font14', 15: 'Font15', 16: 'Font16', 17: 'Font17', 18: 'Font18', 19: 'Font19', 20: 'Font20', 21: 'Font21', 22: 'Font22', 23: 'Font23', 24: 'Font24', 25: 'Font25', 26: 'Font26', 27: 'Font27', 28: 'Font28', 29: 'Font29', 30: 'Font30', 31: 'Font31', 32: 'Font32', 33: 'Font33', 34: 'Font34', 35: 'Font35', 36: 'Font36', 37: 'Font37', 38: 'Font38', 39: 'Font39', 40: 'Font40', 41: 'Font41', 42: 'Font42', 43: 'Font43', 44: 'Font44', 45: 'Font45', 46: 'Font46', 47: 'Font47', 48: 'Font48', 49: 'Font49', 50: 'Font50', 51: 'Font51', 52: 'Font52', 53: 'Font53', 54: 'Font54', 55: 'Font55', 56: 'Font56'})

# ---- inputs and global variables
PriceType = _input('PriceType', MODE_BID)  # Displayed price type
CutPrice = _input('CutPrice', False)  # Last figure removal flag
ResetColors = _input('ResetColors', True)  # Colors reset flag
FontSize = _input('FontSize', 24)  # Font size
FontType = _input('FontType', Font7)  # Font type
WhatCorner = _input('WhatCorner', CORNER_LEFT_LOWER)  # Location corner
Old_Price = 0.0
PriceColor_ = 0
sFontType = ""

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
    global PriceColor_, sFontType
    PriceColor_ = PriceColor
    FontTypes = Arr.of(['Arial', 'Arial Black', 'Arial Bold', 'Arial Bold Italic', 'Arial Italic', 'Comic Sans MS Bold', 'Courier', 'Courier New', 'Courier New Bold', 'Courier New Bold Italic', 'Courier New Italic', 'Estrangelo Edessa', 'Franklin Gothic Medium', 'Gautami', 'Georgia', 'Georgia Bold', 'Georgia Bold Italic', 'Georgia Italic', 'Georgia Italic Impact', 'Latha', 'Lucida Console', 'Lucida Sans Unicode', 'Modern MS Sans Serif', 'MS Sans Serif', 'Mv Boli', 'Palatino Linotype', 'Palatino Linotype Bold', 'Palatino Linotype Italic', 'Roman', 'Script', 'Small Fonts', 'Symbol', 'Tahoma', 'Tahoma Bold', 'Times New Roman', 'Times New Roman Bold', 'Times New Roman Bold Italic', 'Times New Roman Italic', 'Trebuchet MS', 'Trebuchet MS Bold', 'Trebuchet MS Bold Italic', 'Trebuchet MS Italic', 'Tunga', 'Verdana', 'Verdana Bold', 'Verdana Bold Italic', 'Verdana Italic', 'Webdings', 'Westminster', 'Wingdings', 'WST_Czech', 'WST_Engl', 'WST_Fren', 'WST_Germ', 'WST_Ital', 'WST_Span', 'WST_Swed'], fill="")
    sFontType = FontTypes[FontType]

def OnDeinit(reason):
    ObjectDelete(0, 'Market_Price_Label')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Old_Price, PriceColor_
    price = close[rates_total - 1] + (PriceType * Point() * spread[rates_total - 1])
    if ResetColors == True:
        PriceColor_ = PriceColor
        if price > Old_Price:
            PriceColor_ = UpPriceColor
        if price < Old_Price:
            PriceColor_ = DnPriceColor
        Old_Price = price
    Market_Price = DoubleToString(price, Digits() - CutPrice)
    SetTLabel(0, 'Market_Price_Label', 0, WhatCorner, 2 * WhatCorner, 5, 1, Market_Price, PriceColor_, sFontType, FontSize)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
UpPriceColor = _input('UpPriceColor', _uint(Lime))  # Rising price color
PriceColor = _input('PriceColor', _uint(Gray))  # Unchanged price color
DnPriceColor = _input('DnPriceColor', _uint(Magenta))  # Falling price color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MagnifiedMarketPrice(_MQL5Indicator):
    name = 'magnified_market_price'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PriceType': _Choice({0: 'Bid', 1: 'Ask'}, default=0),  # Displayed price type
        'CutPrice': False,  # Last figure removal flag
        'ResetColors': True,  # Colors reset flag
        'FontSize': 24,  # Font size
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=7),  # Font type
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Location corner
    }

