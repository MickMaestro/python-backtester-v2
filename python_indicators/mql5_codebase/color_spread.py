"""Color_Spread — converted from MQL5: MQL5 Indicators/Color_Spread/Color_Spread.mq5

Copyright: Copyright © 2017, SelfTraders; Link: http://www.stfx.tk; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, SelfTraders', 'link': 'http://www.stfx.tk', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [''], 'name': 'Color_Spread', 'source': 'MQL5 Indicators/Color_Spread/Color_Spread.mq5', 'folder': 'Color_Spread', 'inputs': [{'mql': 'Spread_Mode', 'py': 'Spread_Mode', 'param': 'Spread_Mode', 'type': 'int', 'default': 1, 'label': 'вариант индикации спреда', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'Color_Spread_', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'Spread_Color', 'py': 'Spread_Color', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Цвет спреда', 'sinput': False}, {'mql': 'Right_Color', 'py': 'Right_Color', 'param': None, 'type': 'color', 'default': 9109504, 'label': 'Цвет правой части индикатора', 'sinput': False}, {'mql': 'Left_Color', 'py': 'Left_Color', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Цвет левой части индикатора', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 15, 'label': 'Размер шрифта для отображеня спреда', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum SpreadMode
ENUM_POINT_SPREAD = 0
ENUM_TRUE_SPREAD = 1
_enum('SpreadMode', {0: 'ENUM_POINT_SPREAD', 1: 'ENUM_TRUE_SPREAD'})

# ---- inputs and global variables
Spread_Mode = _input('Spread_Mode', ENUM_TRUE_SPREAD)  # вариант индикации спреда
Symbols_Sirname = _input('Symbols_Sirname', 'Color_Spread_')  # Название для меток индикатора
Spread_Color = _input('Spread_Color', clrLime)  # Цвет спреда
Right_Color = _input('Right_Color', clrDarkBlue)  # Цвет правой части индикатора
Left_Color = _input('Left_Color', clrDodgerBlue)  # Цвет левой части индикатора
Font_Size = _input('Font_Size', 15)  # Размер шрифта для отображеня спреда
min_rates_total = 0
RightName = ""
LeftName = ""
SpreadName = ""
PerSec5 = 0
PerSec10 = 0
PerSec400 = 0

def CreateText(chart_id, name, nwin, time, price, text, textTT, Color, Font, Size):
    ObjectCreate(chart_id, name, OBJ_TEXT, nwin, time, price)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, textTT)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetText(chart_id, name, nwin, time, price, text, textTT, Color, Font, Size):
    if ObjectFind(chart_id, name) == -1:
        CreateText(chart_id, name, nwin, time, price, text, textTT, Color, Font, Size)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, nwin, time, price)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)

def CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_RECTANGLE, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)

def SetRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnInit():
    global LeftName, PerSec10, PerSec400, PerSec5, RightName, SpreadName, min_rates_total
    min_rates_total = 300
    RightName = Symbols_Sirname + 'Right'
    LeftName = Symbols_Sirname + 'Left'
    SpreadName = Symbols_Sirname + 'Lable'
    PerSec5 = 5 * PeriodSeconds()
    PerSec10 = 10 * PeriodSeconds()
    PerSec400 = 400 * PeriodSeconds()
    IndicatorSetString(INDICATOR_SHORTNAME, 'Color_Spread')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjectsDeleteAll(0, Symbols_Sirname, -1, -1)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    bar0 = rates_total - 1
    bar1 = rates_total - MathMin(300, bar0)
    Bid = close[bar0]
    Spread = spread[bar0] * Point()
    Ask = Bid + Spread
    dSpread = Bid + (Spread / 1.05)
    sSpread = ""
    if Spread_Mode == ENUM_TRUE_SPREAD:
        sSpread = DoubleToString(Spread, Digits())
    else:
        sSpread = _str(spread[bar0])
    SetRectangle(0, LeftName, 0, time[0], Bid, time[bar0] + PerSec5, Ask, Left_Color, STYLE_SOLID, 1, LeftName)
    SetRectangle(0, RightName, 0, time[bar0] + PerSec5, Bid, time[bar0] + PerSec400, Ask, Right_Color, STYLE_SOLID, 1, RightName)
    SetText(0, SpreadName, 0, time[bar0] + PerSec10, dSpread, sSpread, sSpread, Spread_Color, 'Georgia', Font_Size)
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorSpread(_MQL5Indicator):
    name = 'Color_Spread'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Spread_Mode': _Choice({0: 'в пунктах', 1: 'в единицах ценового графика'}, default=1),  # вариант индикации спреда
        'Font_Size': 15,  # Размер шрифта для отображеня спреда
    }

