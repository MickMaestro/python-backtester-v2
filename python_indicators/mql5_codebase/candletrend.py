"""candletrend — converted from MQL5: MQL5 Indicators/CandleTrend/candletrend.mq5

The indicator shows the direction of candles on different timeframes
Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The indicator shows the direction of candles on different timeframes'], 'name': 'candletrend', 'source': 'MQL5 Indicators/CandleTrend/candletrend.mq5', 'folder': 'CandleTrend', 'inputs': [{'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'currency uptrend color', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'currency downtrend color', 'sinput': False}, {'mql': 'ZrColor', 'py': 'ZrColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'no change color', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 11, 'label': 'font size', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'font type', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'location corner', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'vertical location', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'horizontal location', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

Gray = 0x808080  # MQL4 colour name
LimeGreen = 0x32CD32  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
FontSize = _input('FontSize', 11)  # font size
FontType = _input('FontType', Font14)  # font type
WhatCorner = _input('WhatCorner', CORNER_LEFT_LOWER)  # location corner
Y_ = _input('Y_', 20)  # vertical location
X_ = _input('X_', 5)  # horizontal location
sFontType = ""
xshift = 0
shift_1 = 0
shift_2 = 0
shift_3 = 0
shift_4 = 0
shift_5 = 0
shift_6 = 0

def OnInit():
    global sFontType, shift_1, shift_2, shift_3, shift_4, shift_5, shift_6, xshift
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()
    xshift = _int(X_ + (5.7 * FontSize))
    _sw1 = WhatCorner
    if _sw1 == CORNER_RIGHT_LOWER:
        shift_1 = Y_ + 110
        shift_2 = Y_ + 88
        shift_3 = Y_ + 66
        shift_4 = Y_ + 44
        shift_5 = Y_ + 22
        shift_6 = Y_ + 0
    elif _sw1 == CORNER_LEFT_LOWER:
        shift_1 = Y_ + 110
        shift_2 = Y_ + 88
        shift_3 = Y_ + 66
        shift_4 = Y_ + 44
        shift_5 = Y_ + 22
        shift_6 = Y_ + 0
    else:
        shift_1 = Y_ + 0
        shift_2 = Y_ + 22
        shift_3 = Y_ + 44
        shift_4 = Y_ + 66
        shift_5 = Y_ + 88
        shift_6 = Y_ + 110

def OnDeinit(reason):
    Deinit()

def Deinit():
    ObjectDelete(0, 'H4Stat+')
    ObjectDelete(0, 'H8Stat+')
    ObjectDelete(0, 'H12Stat+')
    ObjectDelete(0, 'DailyStat+')
    ObjectDelete(0, 'WeeklyStat+')
    ObjectDelete(0, 'MonthlyStat+')
    ObjectDelete(0, 'H4Stat_')
    ObjectDelete(0, 'H8Stat_')
    ObjectDelete(0, 'H12Stat_')
    ObjectDelete(0, 'DailyStat_')
    ObjectDelete(0, 'WeeklyStat_')
    ObjectDelete(0, 'MonthlyStat_')

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
    H4OpPrice = Arr(1, 0.0, dyn=False)
    H4ClPrice = Arr(1, 0.0, dyn=False)
    H8OpPrice = Arr(1, 0.0, dyn=False)
    H8ClPrice = Arr(1, 0.0, dyn=False)
    H12OpPrice = Arr(1, 0.0, dyn=False)
    H12ClPrice = Arr(1, 0.0, dyn=False)
    DayOpPrice = Arr(1, 0.0, dyn=False)
    DayClPrice = Arr(1, 0.0, dyn=False)
    WeekOpPrice = Arr(1, 0.0, dyn=False)
    WeekClPrice = Arr(1, 0.0, dyn=False)
    MonthOpPrice = Arr(1, 0.0, dyn=False)
    MonthClPrice = Arr(1, 0.0, dyn=False)
    if CopyOpen(Symbol(), PERIOD_H4, 0, 1, H4OpPrice) <= 0:
        return 0
    if CopyClose(Symbol(), PERIOD_H4, 0, 1, H4ClPrice) <= 0:
        return 0
    if CopyOpen(Symbol(), PERIOD_H8, 0, 1, H8OpPrice) <= 0:
        return 0
    if CopyClose(Symbol(), PERIOD_H8, 0, 1, H8ClPrice) <= 0:
        return 0
    if CopyOpen(Symbol(), PERIOD_H12, 0, 1, H12OpPrice) <= 0:
        return 0
    if CopyClose(Symbol(), PERIOD_H12, 0, 1, H12ClPrice) <= 0:
        return 0
    if CopyOpen(Symbol(), PERIOD_D1, 0, 1, DayOpPrice) <= 0:
        return 0
    if CopyClose(Symbol(), PERIOD_D1, 0, 1, DayClPrice) <= 0:
        return 0
    if CopyOpen(Symbol(), PERIOD_W1, 0, 1, WeekOpPrice) <= 0:
        return 0
    if CopyClose(Symbol(), PERIOD_W1, 0, 1, WeekClPrice) <= 0:
        return 0
    if CopyOpen(Symbol(), PERIOD_MN1, 0, 1, MonthOpPrice) <= 0:
        return 0
    if CopyClose(Symbol(), PERIOD_MN1, 0, 1, MonthClPrice) <= 0:
        return 0
    ColorH4Gain = ZrColor
    ColorH8Gain = ZrColor
    ColorH12Gain = ZrColor
    ColorDailyGain = ZrColor
    ColorWeeklyGain = ZrColor
    ColorMonthlyGain = ZrColor
    if (H4ClPrice[0] - H4OpPrice[0]) < 0:
        ColorH4Gain = DnColor
    else:
        ColorH4Gain = UpColor
    if (H8ClPrice[0] - H8OpPrice[0]) < 0:
        ColorH8Gain = DnColor
    else:
        ColorH8Gain = UpColor
    if (H12ClPrice[0] - H12OpPrice[0]) < 0:
        ColorH12Gain = DnColor
    else:
        ColorH12Gain = UpColor
    if (DayClPrice[0] - DayOpPrice[0]) < 0:
        ColorDailyGain = DnColor
    else:
        ColorDailyGain = UpColor
    if (WeekClPrice[0] - WeekOpPrice[0]) < 0:
        ColorWeeklyGain = DnColor
    else:
        ColorWeeklyGain = UpColor
    if (MonthClPrice[0] - MonthOpPrice[0]) < 0:
        ColorMonthlyGain = DnColor
    else:
        ColorMonthlyGain = UpColor
    SetTLabel(0, 'H4Stat+', 0, WhatCorner, 2 * WhatCorner, X_, shift_1, 'H4: ', ColorH4Gain, sFontType, FontSize)
    SetTLabel(0, 'H4Stat_', 0, WhatCorner, 2 * WhatCorner, xshift, shift_1, 'n', ColorH4Gain, 'Wingdings', FontSize)
    SetTLabel(0, 'H8Stat+', 0, WhatCorner, 2 * WhatCorner, X_, shift_2, 'H8: ', ColorH8Gain, sFontType, FontSize)
    SetTLabel(0, 'H8Stat_', 0, WhatCorner, 2 * WhatCorner, xshift, shift_2, 'n', ColorH8Gain, 'Wingdings', FontSize)
    SetTLabel(0, 'H12Stat+', 0, WhatCorner, 2 * WhatCorner, X_, shift_3, 'H12: ', ColorH12Gain, sFontType, FontSize)
    SetTLabel(0, 'H12Stat_', 0, WhatCorner, 2 * WhatCorner, xshift, shift_3, 'n', ColorH12Gain, 'Wingdings', FontSize)
    SetTLabel(0, 'DailyStat+', 0, WhatCorner, 2 * WhatCorner, X_, shift_4, 'Daily: ', ColorDailyGain, sFontType, FontSize)
    SetTLabel(0, 'DailyStat_', 0, WhatCorner, 2 * WhatCorner, xshift, shift_4, 'n', ColorDailyGain, 'Wingdings', FontSize)
    SetTLabel(0, 'WeeklyStat+', 0, WhatCorner, 2 * WhatCorner, X_, shift_5, 'Weekly: ', ColorWeeklyGain, sFontType, FontSize)
    SetTLabel(0, 'WeeklyStat_', 0, WhatCorner, 2 * WhatCorner, xshift, shift_5, 'n', ColorWeeklyGain, 'Wingdings', FontSize)
    SetTLabel(0, 'MonthlyStat+', 0, WhatCorner, 2 * WhatCorner, X_, shift_6, 'Monthly: ', ColorMonthlyGain, sFontType, FontSize)
    SetTLabel(0, 'MonthlyStat_', 0, WhatCorner, 2 * WhatCorner, xshift, shift_6, 'n', ColorMonthlyGain, 'Wingdings', FontSize)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
UpColor = _input('UpColor', _uint(LimeGreen))  # currency uptrend color
DnColor = _input('DnColor', _uint(Red))  # currency downtrend color
ZrColor = _input('ZrColor', _uint(Gray))  # no change color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Candletrend(_MQL5Indicator):
    name = 'candletrend'
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

