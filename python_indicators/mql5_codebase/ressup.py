"""ressup — converted from MQL5: MQL5 Indicators/ResSup/ressup.mq5

Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ressup', 'source': 'MQL5 Indicators/ResSup/ressup.mq5', 'folder': 'ResSup', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ResSup', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16385, 'label': 'период графика для поиска экстремумов', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'номер бара для поиска экстремумов', 'sinput': False}, {'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 24, 'label': 'период поиска экстремумов цены', 'sinput': False}, {'mql': 'iSize', 'py': 'iSize', 'param': 'iSize', 'type': 'uint', 'default': 15, 'label': 'длина уровней в барах текущего графика', 'sinput': False}, {'mql': 'Digits_', 'py': 'Digits_', 'param': 'Digits_', 'type': 'uint', 'default': 0, 'label': 'разряд округления цены', 'sinput': False}, {'mql': 'Color_Bg', 'py': 'Color_Bg', 'param': None, 'type': 'color', 'default': 16443110, 'label': 'цвет фона', 'sinput': False}, {'mql': 'Color_Up', 'py': 'Color_Up', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'цвет линии сопротивления', 'sinput': False}, {'mql': 'Style_Up', 'py': 'Style_Up', 'param': 'Style_Up', 'type': 'int', 'default': 0, 'label': 'стиль линии сопротивления', 'sinput': False}, {'mql': 'Width_Up', 'py': 'Width_Up', 'param': 'Width_Up', 'type': 'int', 'default': 4, 'label': 'толщина линии сопротивления', 'sinput': False}, {'mql': 'Color_Dn', 'py': 'Color_Dn', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет линии поддержки', 'sinput': False}, {'mql': 'Style_Dn', 'py': 'Style_Dn', 'param': 'Style_Dn', 'type': 'int', 'default': 0, 'label': 'стиль линии поддержки', 'sinput': False}, {'mql': 'Width_Dn', 'py': 'Width_Dn', 'param': 'Width_Dn', 'type': 'int', 'default': 4, 'label': 'толщина линии поддержки', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'uint', 'default': 2, 'label': 'размер ценовых меток', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Number
Number_0 = 0
Number_1 = 1
Number_2 = 2
Number_3 = 3
_enum('Number', {0: 'Number_0', 1: 'Number_1', 2: 'Number_2', 3: 'Number_3'})

# enum Width
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('Width', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
SirName = _input('SirName', 'ResSup')  # Первая часть имени графических объектов
TimeFrame = _input('TimeFrame', PERIOD_H1)  # период графика для поиска экстремумов
SignalBar = _input('SignalBar', 1)  # номер бара для поиска экстремумов
iPeriod = _input('iPeriod', 24)  # период поиска экстремумов цены
iSize = _input('iSize', 15)  # длина уровней в барах текущего графика
Digits_ = _input('Digits_', 0)  # разряд округления цены
Color_Bg = _input('Color_Bg', clrLavender)  # цвет фона
Color_Up = _input('Color_Up', clrLimeGreen)  # цвет линии сопротивления
Style_Up = _input('Style_Up', SOLID_)  # стиль линии сопротивления
Width_Up = _input('Width_Up', Width_4)  # толщина линии сопротивления
Color_Dn = _input('Color_Dn', clrMagenta)  # цвет линии поддержки
Style_Dn = _input('Style_Dn', SOLID_)  # стиль линии поддержки
Width_Dn = _input('Width_Dn', Width_4)  # толщина линии поддержки
FontSize = _input('FontSize', 2)  # размер ценовых меток
iLow_v = Arr(0, 0.0)
iHigh_v = Arr(0, 0.0)
PointPow10 = 0.0
min_rates_total1 = 0
min_rates_total2 = 0
UpLinesName = ""
UpPriceName = ""
DnLinesName = ""
DnPriceName = ""
BgName = ""

def OnInit():
    global BgName, DnLinesName, DnPriceName, PointPow10, UpLinesName, UpPriceName, min_rates_total1, min_rates_total2
    ArrayResize(iLow_v, iPeriod)
    ArrayResize(iHigh_v, iPeriod)
    UpLinesName = SirName + ' UpLine'
    UpPriceName = SirName + ' UpPrice'
    DnLinesName = SirName + ' DnLine'
    DnPriceName = SirName + ' DnPrice'
    BgName = SirName + ' Bg'
    min_rates_total1 = _int(iPeriod + SignalBar)
    min_rates_total2 = _int(iSize)
    Pow10 = MathPow(10, Digits_)
    PointPow10 = Point() * Pow10

def OnDeinit(reason):
    ObjectDelete(0, UpLinesName)
    ObjectDelete(0, UpPriceName)
    ObjectDelete(0, DnLinesName)
    ObjectDelete(0, DnPriceName)
    ObjectDelete(0, BgName)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), TimeFrame) < min_rates_total1 or rates_total < min_rates_total2:
        return 0
    if CopyLow(Symbol(), TimeFrame, SignalBar, iPeriod, iLow_v) <= 0:
        return 0
    if CopyHigh(Symbol(), TimeFrame, SignalBar, iPeriod, iHigh_v) <= 0:
        return 0
    Min = PointPow10 * MathRound(_fdiv(iLow_v[ArrayMinimum(iLow_v, 0, WHOLE_ARRAY)], PointPow10))
    Max = PointPow10 * MathRound(_fdiv(iHigh_v[ArrayMaximum(iHigh_v, 0, WHOLE_ARRAY)], PointPow10))
    time1 = time[rates_total - iSize]
    time2 = time[rates_total - 1]
    SetRectangle(0, BgName, 0, time1, Min, time2, Max, Color_Bg, SOLID_, Width_1, '')
    SetTline(0, UpLinesName, 0, time1, Min, time2, Min, Color_Dn, Style_Dn, Width_Dn, DoubleToString(Min, Digits()))
    SetTline(0, DnLinesName, 0, time1, Max, time2, Max, Color_Up, Style_Up, Width_Up, DoubleToString(Max, Digits()))
    SetRightPrice(0, DnPriceName, 0, time2, Min, Color_Dn, FontSize)
    SetRightPrice(0, UpPriceName, 0, time2, Max, Color_Up, FontSize)
    ChartRedraw(0)
    return rates_total

def CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_RECTANGLE, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def CreateRightPrice(chart_id, name, nwin, time, price, Color, fontsize):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, fontsize)

def SetRightPrice(chart_id, name, nwin, time, price, Color, fontsize):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color, fontsize)
    else:
        ObjectMove(chart_id, name, 0, time, price)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ressup(_MQL5Indicator):
    name = 'ressup'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика для поиска экстремумов
        'SignalBar': 1,  # номер бара для поиска экстремумов
        'iPeriod': 24,  # период поиска экстремумов цены
        'iSize': 15,  # длина уровней в барах текущего графика
        'Digits_': 0,  # разряд округления цены
        'Style_Up': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль линии сопротивления
        'Width_Up': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=4),  # толщина линии сопротивления
        'Style_Dn': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль линии поддержки
        'Width_Dn': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=4),  # толщина линии поддержки
        'FontSize': 2,  # размер ценовых меток
    }

