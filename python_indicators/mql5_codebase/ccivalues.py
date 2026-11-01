"""CCIValues — converted from MQL5: MQL5 Indicators/CCIValues/CCIValues.mq5

Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'CCIValues', 'source': 'MQL5 Indicators/CCIValues/CCIValues.mq5', 'folder': 'CCIValues', 'inputs': [{'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'CCIValues_Label_CCIValues_', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'ShowTimeframe1', 'py': 'ShowTimeframe1', 'param': 'ShowTimeframe1', 'type': 'bool', 'default': True, 'label': '1 Отображение таймфрейма', 'sinput': False}, {'mql': 'Timeframe1', 'py': 'Timeframe1', 'param': 'Timeframe1', 'type': 'int', 'default': 1, 'label': '1 Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iPeriod1', 'py': 'iPeriod1', 'param': 'iPeriod1', 'type': 'uint', 'default': 10, 'label': '1 Период индикатора', 'sinput': False}, {'mql': 'ShowTimeframe2', 'py': 'ShowTimeframe2', 'param': 'ShowTimeframe2', 'type': 'bool', 'default': True, 'label': '2 Отображение таймфрейма', 'sinput': False}, {'mql': 'Timeframe2', 'py': 'Timeframe2', 'param': 'Timeframe2', 'type': 'int', 'default': 5, 'label': '2 Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iPeriod2', 'py': 'iPeriod2', 'param': 'iPeriod2', 'type': 'uint', 'default': 10, 'label': '2 Период индикатора', 'sinput': False}, {'mql': 'ShowTimeframe3', 'py': 'ShowTimeframe3', 'param': 'ShowTimeframe3', 'type': 'bool', 'default': True, 'label': '3 Отображение таймфрейма', 'sinput': False}, {'mql': 'Timeframe3', 'py': 'Timeframe3', 'param': 'Timeframe3', 'type': 'int', 'default': 15, 'label': '3 Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iPeriod3', 'py': 'iPeriod3', 'param': 'iPeriod3', 'type': 'uint', 'default': 10, 'label': '3 Период индикатора', 'sinput': False}, {'mql': 'ShowTimeframe4', 'py': 'ShowTimeframe4', 'param': 'ShowTimeframe4', 'type': 'bool', 'default': True, 'label': '4 Отображение таймфрейма', 'sinput': False}, {'mql': 'Timeframe4', 'py': 'Timeframe4', 'param': 'Timeframe4', 'type': 'int', 'default': 30, 'label': '4 Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iPeriod4', 'py': 'iPeriod4', 'param': 'iPeriod4', 'type': 'uint', 'default': 10, 'label': '4 Период индикатора для расчета индикатора', 'sinput': False}, {'mql': 'ShowTimeframe5', 'py': 'ShowTimeframe5', 'param': 'ShowTimeframe5', 'type': 'bool', 'default': True, 'label': '5 Отображение таймфрейма', 'sinput': False}, {'mql': 'Timeframe5', 'py': 'Timeframe5', 'param': 'Timeframe5', 'type': 'int', 'default': 16385, 'label': '5 Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iPeriod5', 'py': 'iPeriod5', 'param': 'iPeriod5', 'type': 'uint', 'default': 10, 'label': '5 Период индикатора для расчета индикатора', 'sinput': False}, {'mql': 'ShowTimeframe6', 'py': 'ShowTimeframe6', 'param': 'ShowTimeframe6', 'type': 'bool', 'default': True, 'label': '6 Отображение таймфрейма', 'sinput': False}, {'mql': 'Timeframe6', 'py': 'Timeframe6', 'param': 'Timeframe6', 'type': 'int', 'default': 16386, 'label': '6 Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iPeriod6', 'py': 'iPeriod6', 'param': 'iPeriod6', 'type': 'uint', 'default': 10, 'label': '6 Период индикатора для расчета индикатора', 'sinput': False}, {'mql': 'ShowTimeframe7', 'py': 'ShowTimeframe7', 'param': 'ShowTimeframe7', 'type': 'bool', 'default': True, 'label': '7 Отображение таймфрейма', 'sinput': False}, {'mql': 'Timeframe7', 'py': 'Timeframe7', 'param': 'Timeframe7', 'type': 'int', 'default': 16388, 'label': '7 Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iPeriod7', 'py': 'iPeriod7', 'param': 'iPeriod7', 'type': 'uint', 'default': 10, 'label': '7 Период индикатора для расчета индикатора', 'sinput': False}, {'mql': 'ShowTimeframe8', 'py': 'ShowTimeframe8', 'param': 'ShowTimeframe8', 'type': 'bool', 'default': True, 'label': '8 Отображение таймфрейма', 'sinput': False}, {'mql': 'Timeframe8', 'py': 'Timeframe8', 'param': 'Timeframe8', 'type': 'int', 'default': 16396, 'label': '8 Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iPeriod8', 'py': 'iPeriod8', 'param': 'iPeriod8', 'type': 'uint', 'default': 10, 'label': '8 Период индикатора для расчета индикатора', 'sinput': False}, {'mql': 'ShowTimeframe9', 'py': 'ShowTimeframe9', 'param': 'ShowTimeframe9', 'type': 'bool', 'default': True, 'label': '9 Отображение таймфрейма', 'sinput': False}, {'mql': 'Timeframe9', 'py': 'Timeframe9', 'param': 'Timeframe9', 'type': 'int', 'default': 16408, 'label': '9 Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iPeriod9', 'py': 'iPeriod9', 'param': 'iPeriod9', 'type': 'uint', 'default': 10, 'label': '9 Период индикатора для расчета индикатора', 'sinput': False}, {'mql': 'ShowTimeframe10', 'py': 'ShowTimeframe10', 'param': 'ShowTimeframe10', 'type': 'bool', 'default': True, 'label': '10 Отображение таймфрейма', 'sinput': False}, {'mql': 'Timeframe10', 'py': 'Timeframe10', 'param': 'Timeframe10', 'type': 'int', 'default': 32769, 'label': '10 Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iPeriod10', 'py': 'iPeriod10', 'param': 'iPeriod10', 'type': 'uint', 'default': 10, 'label': '10 Период индикатора для расчета индикатора', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 5, 'label': 'Цена CCI индикатора', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'Номер бара для получения сигнала (0 - текущий бар)', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 0, 'label': 'Угол расположения индикатора', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 10, 'label': 'Смещение по горизонтали индикатора', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 25, 'label': 'Смещение по вертикали индикатора', 'sinput': False}, {'mql': 'Font_Type', 'py': 'Font_Type', 'param': 'Font_Type', 'type': 'int', 'default': 14, 'label': 'Шрифт отображения индикатора', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 13, 'label': 'Размер шрифта', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 100, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -100, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'HighColor', 'py': 'HighColor', 'param': None, 'type': 'color', 'default': 11186720, 'label': 'цвет перекупленности', 'sinput': False}, {'mql': 'MiddleColor', 'py': 'MiddleColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет вне тренда', 'sinput': False}, {'mql': 'LowColor', 'py': 'LowColor', 'param': None, 'type': 'color', 'default': 42495, 'label': 'цвет перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

# ---- inputs and global variables
Symbols_Sirname = _input('Symbols_Sirname', 'CCIValues_Label_CCIValues_')  # Название для меток индикатора
ShowTimeframe1 = _input('ShowTimeframe1', True)  # 1 Отображение таймфрейма
Timeframe1 = _input('Timeframe1', PERIOD_M1)  # 1 Таймфрейм индикатора для расчета индикатора
iPeriod1 = _input('iPeriod1', 10)  # 1 Период индикатора
ShowTimeframe2 = _input('ShowTimeframe2', True)  # 2 Отображение таймфрейма
Timeframe2 = _input('Timeframe2', PERIOD_M5)  # 2 Таймфрейм индикатора для расчета индикатора
iPeriod2 = _input('iPeriod2', 10)  # 2 Период индикатора
ShowTimeframe3 = _input('ShowTimeframe3', True)  # 3 Отображение таймфрейма
Timeframe3 = _input('Timeframe3', PERIOD_M15)  # 3 Таймфрейм индикатора для расчета индикатора
iPeriod3 = _input('iPeriod3', 10)  # 3 Период индикатора
ShowTimeframe4 = _input('ShowTimeframe4', True)  # 4 Отображение таймфрейма
Timeframe4 = _input('Timeframe4', PERIOD_M30)  # 4 Таймфрейм индикатора для расчета индикатора
iPeriod4 = _input('iPeriod4', 10)  # 4 Период индикатора для расчета индикатора
ShowTimeframe5 = _input('ShowTimeframe5', True)  # 5 Отображение таймфрейма
Timeframe5 = _input('Timeframe5', PERIOD_H1)  # 5 Таймфрейм индикатора для расчета индикатора
iPeriod5 = _input('iPeriod5', 10)  # 5 Период индикатора для расчета индикатора
ShowTimeframe6 = _input('ShowTimeframe6', True)  # 6 Отображение таймфрейма
Timeframe6 = _input('Timeframe6', PERIOD_H2)  # 6 Таймфрейм индикатора для расчета индикатора
iPeriod6 = _input('iPeriod6', 10)  # 6 Период индикатора для расчета индикатора
ShowTimeframe7 = _input('ShowTimeframe7', True)  # 7 Отображение таймфрейма
Timeframe7 = _input('Timeframe7', PERIOD_H4)  # 7 Таймфрейм индикатора для расчета индикатора
iPeriod7 = _input('iPeriod7', 10)  # 7 Период индикатора для расчета индикатора
ShowTimeframe8 = _input('ShowTimeframe8', True)  # 8 Отображение таймфрейма
Timeframe8 = _input('Timeframe8', PERIOD_H12)  # 8 Таймфрейм индикатора для расчета индикатора
iPeriod8 = _input('iPeriod8', 10)  # 8 Период индикатора для расчета индикатора
ShowTimeframe9 = _input('ShowTimeframe9', True)  # 9 Отображение таймфрейма
Timeframe9 = _input('Timeframe9', PERIOD_D1)  # 9 Таймфрейм индикатора для расчета индикатора
iPeriod9 = _input('iPeriod9', 10)  # 9 Период индикатора для расчета индикатора
ShowTimeframe10 = _input('ShowTimeframe10', True)  # 10 Отображение таймфрейма
Timeframe10 = _input('Timeframe10', PERIOD_W1)  # 10 Таймфрейм индикатора для расчета индикатора
iPeriod10 = _input('iPeriod10', 10)  # 10 Период индикатора для расчета индикатора
CCIPrice = _input('CCIPrice', PRICE_MEDIAN)  # Цена CCI индикатора
SignalBar = _input('SignalBar', 0)  # Номер бара для получения сигнала (0 - текущий бар)
WhatCorner = _input('WhatCorner', CORNER_LEFT_UPPER)  # Угол расположения индикатора
X_ = _input('X_', 10)  # Смещение по горизонтали индикатора
Y_ = _input('Y_', 25)  # Смещение по вертикали индикатора
Font_Type = _input('Font_Type', Font14)  # Шрифт отображения индикатора
Font_Size = _input('Font_Size', 13)  # Размер шрифта
HighLevel = _input('HighLevel', 100)  # уровень перекупленности
LowLevel = _input('LowLevel', -100)  # уровень перепроданности
HighColor = _input('HighColor', clrLightSeaGreen)  # цвет перекупленности
MiddleColor = _input('MiddleColor', clrGray)  # цвет вне тренда
LowColor = _input('LowColor', clrOrange)  # цвет перепроданности
CCI_Handle = Arr(10, 0, dyn=False)
min_rates_total = Arr(10, 0, dyn=False)
Name = Arr(10, "", dyn=False)
Text = Arr(10, "", dyn=False)
ShowTimeframe = Arr(10, False, dyn=False)
Timeframe = Arr(10, 0, dyn=False)
iPeriod = Arr(10, 0, dyn=False)
iX = Arr(10, 0, dyn=False)
iY = Arr(10, 0, dyn=False)
sFontType = ""

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, textTT, Color, Font, Size):
    ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chart_id, name, OBJPROP_CORNER, corner)
    ObjectSetInteger(chart_id, name, OBJPROP_ANCHOR, point)
    ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
    ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, textTT)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)

def SetTLabel(chart_id, name, nwin, corner, point, X, Y, text, textTT, Color, Font, Size):
    if ObjectFind(chart_id, name) == -1:
        CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, textTT, Color, Font, Size)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
        ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)

def OnInit():
    global sFontType
    ArrayInitialize(iX, X_)
    ShowTimeframe[0] = ShowTimeframe1
    Timeframe[0] = Timeframe1
    iPeriod[0] = iPeriod1
    iY[0] = Y_
    ShowTimeframe[1] = ShowTimeframe2
    Timeframe[1] = Timeframe2
    iPeriod[1] = iPeriod2
    if ShowTimeframe[1]:
        iY[1] = iY[0] + 20
    else:
        iY[1] = iY[0]
    ShowTimeframe[2] = ShowTimeframe3
    Timeframe[2] = Timeframe3
    iPeriod[2] = iPeriod3
    if ShowTimeframe[2]:
        iY[2] = iY[1] + 20
    else:
        iY[2] = iY[1]
    ShowTimeframe[3] = ShowTimeframe4
    Timeframe[3] = Timeframe4
    iPeriod[3] = iPeriod4
    if ShowTimeframe[3]:
        iY[3] = iY[2] + 20
    else:
        iY[3] = iY[2]
    ShowTimeframe[4] = ShowTimeframe5
    Timeframe[4] = Timeframe5
    iPeriod[4] = iPeriod5
    if ShowTimeframe[4]:
        iY[4] = iY[3] + 20
    else:
        iY[4] = iY[3]
    ShowTimeframe[5] = ShowTimeframe6
    Timeframe[5] = Timeframe6
    iPeriod[5] = iPeriod6
    if ShowTimeframe[5]:
        iY[5] = iY[4] + 20
    else:
        iY[5] = iY[4]
    ShowTimeframe[6] = ShowTimeframe7
    Timeframe[6] = Timeframe7
    iPeriod[6] = iPeriod7
    if ShowTimeframe[6]:
        iY[6] = iY[5] + 20
    else:
        iY[6] = iY[5]
    ShowTimeframe[7] = ShowTimeframe8
    Timeframe[7] = Timeframe8
    iPeriod[7] = iPeriod8
    if ShowTimeframe[7]:
        iY[7] = iY[6] + 20
    else:
        iY[7] = iY[6]
    ShowTimeframe[8] = ShowTimeframe9
    Timeframe[8] = Timeframe9
    iPeriod[8] = iPeriod9
    if ShowTimeframe[8]:
        iY[8] = iY[7] + 20
    else:
        iY[8] = iY[7]
    ShowTimeframe[9] = ShowTimeframe10
    Timeframe[9] = Timeframe10
    iPeriod[9] = iPeriod10
    if ShowTimeframe[9]:
        iY[9] = iY[8] + 20
    else:
        iY[9] = iY[8]
    for count in range(0, 10):
        if not ShowTimeframe[count]:
            continue
        CCI_Handle[count] = iCCI(Symbol(), Timeframe[count], iPeriod[count], CCIPrice)
        if CCI_Handle[count] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора CCI ' + _str(count + 1))
            return INIT_FAILED
    for count in range(0, 10):
        if ShowTimeframe[count]:
            min_rates_total[count] = _int(iPeriod[count]) + _int(SignalBar)
    for count in range(0, 10):
        if ShowTimeframe[count]:
            Name[count] = Symbols_Sirname + ' ' + _str(count + 1)
    for count in range(0, 10):
        if ShowTimeframe[count]:
            Text[count] = 'CCI(' + GetStringTimeframe(Timeframe[count]) + ',' + _str(iPeriod[count]) + ')' + '='
    sFontType = FONT.GetFontName(Font_Type)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, Symbols_Sirname, -1, -1)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for count in range(0, 10):
        if ShowTimeframe[count]:
            if BarsCalculated(CCI_Handle[count]) < min_rates_total[count]:
                return prev_calculated
            if BarsCalculated(CCI_Handle[count]) < Bars(Symbol(), Timeframe[count]):
                return prev_calculated
    for count in range(0, 10):
        if ShowTimeframe[count]:
            CCI = Arr(1, 0.0, dyn=False)
            if CopyBuffer(CCI_Handle[count], 0, SignalBar, 1, CCI) <= 0:
                return prev_calculated
            Col = MiddleColor
            if CCI[0] > HighLevel:
                Col = HighColor
            if CCI[0] < LowLevel:
                Col = LowColor
            info = Text[count] + DoubleToString(CCI[0], 0)
            SetTLabel(0, Name[count], 0, WhatCorner, 2 * WhatCorner, iX[count], iY[count], info, info, Col, sFontType, Font_Size)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
FONT = _alloc(CFontName)
FONT.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIValues(_MQL5Indicator):
    name = 'CCIValues'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ShowTimeframe1': True,  # 1 Отображение таймфрейма
        'Timeframe1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=1),  # 1 Таймфрейм индикатора для расчета индикатора
        'iPeriod1': 10,  # 1 Период индикатора
        'ShowTimeframe2': True,  # 2 Отображение таймфрейма
        'Timeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=5),  # 2 Таймфрейм индикатора для расчета индикатора
        'iPeriod2': 10,  # 2 Период индикатора
        'ShowTimeframe3': True,  # 3 Отображение таймфрейма
        'Timeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=15),  # 3 Таймфрейм индикатора для расчета индикатора
        'iPeriod3': 10,  # 3 Период индикатора
        'ShowTimeframe4': True,  # 4 Отображение таймфрейма
        'Timeframe4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # 4 Таймфрейм индикатора для расчета индикатора
        'iPeriod4': 10,  # 4 Период индикатора для расчета индикатора
        'ShowTimeframe5': True,  # 5 Отображение таймфрейма
        'Timeframe5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # 5 Таймфрейм индикатора для расчета индикатора
        'iPeriod5': 10,  # 5 Период индикатора для расчета индикатора
        'ShowTimeframe6': True,  # 6 Отображение таймфрейма
        'Timeframe6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16386),  # 6 Таймфрейм индикатора для расчета индикатора
        'iPeriod6': 10,  # 6 Период индикатора для расчета индикатора
        'ShowTimeframe7': True,  # 7 Отображение таймфрейма
        'Timeframe7': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # 7 Таймфрейм индикатора для расчета индикатора
        'iPeriod7': 10,  # 7 Период индикатора для расчета индикатора
        'ShowTimeframe8': True,  # 8 Отображение таймфрейма
        'Timeframe8': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # 8 Таймфрейм индикатора для расчета индикатора
        'iPeriod8': 10,  # 8 Период индикатора для расчета индикатора
        'ShowTimeframe9': True,  # 9 Отображение таймфрейма
        'Timeframe9': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # 9 Таймфрейм индикатора для расчета индикатора
        'iPeriod9': 10,  # 9 Период индикатора для расчета индикатора
        'ShowTimeframe10': True,  # 10 Отображение таймфрейма
        'Timeframe10': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=32769),  # 10 Таймфрейм индикатора для расчета индикатора
        'iPeriod10': 10,  # 10 Период индикатора для расчета индикатора
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Цена CCI индикатора
        'SignalBar': 0,  # Номер бара для получения сигнала (0 - текущий бар)
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=0),  # Угол расположения индикатора
        'X_': 10,  # Смещение по горизонтали индикатора
        'Y_': 25,  # Смещение по вертикали индикатора
        'Font_Type': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # Шрифт отображения индикатора
        'Font_Size': 13,  # Размер шрифта
        'HighLevel': 100,  # уровень перекупленности
        'LowLevel': -100,  # уровень перепроданности
    }

