"""CandleDifference_Obj — converted from MQL5: MQL5 Indicators/CandleDifference_Obj/CandleDifference_Obj.mq5

Copyright: Copyright © 2016, Il Anokhin; Link: http://www.mql5.com/en/users/ilanokhin; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Il Anokhin', 'link': 'http://www.mql5.com/en/users/ilanokhin', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [''], 'name': 'CandleDifference_Obj', 'source': 'MQL5 Indicators/CandleDifference_Obj/CandleDifference_Obj.mq5', 'folder': 'CandleDifference_Obj', 'inputs': [{'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'P1', 'py': 'P1', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'Pair 1', 'sinput': False}, {'mql': 'P2', 'py': 'P2', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Pair 2', 'sinput': False}, {'mql': 'P3', 'py': 'P3', 'param': None, 'type': 'string', 'default': 'AUDUSD', 'label': 'Pair 3', 'sinput': False}, {'mql': 'P4', 'py': 'P4', 'param': None, 'type': 'string', 'default': 'GBPJPY', 'label': 'Pair 4', 'sinput': False}, {'mql': 'P5', 'py': 'P5', 'param': None, 'type': 'string', 'default': 'USDCHF', 'label': 'Pair 5', 'sinput': False}, {'mql': 'P6', 'py': 'P6', 'param': None, 'type': 'string', 'default': 'USDCAD', 'label': 'Pair 6', 'sinput': False}, {'mql': 'P7', 'py': 'P7', 'param': None, 'type': 'string', 'default': 'USDJPY', 'label': 'Pair 7', 'sinput': False}, {'mql': 'P8', 'py': 'P8', 'param': None, 'type': 'string', 'default': 'EURJPY', 'label': 'Pair 8', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'Номер бара для получения сигнала (0 - текущий бар)', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'CandleDifference_Label_', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'Ind_Color', 'py': 'Ind_Color', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'Цвет индикатора', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 15, 'label': 'Размер шрифта названия индикатора', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 30, 'label': 'Смещение по горизонтали', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 30, 'label': 'Смещение по вертикали', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Отображение названия индикатора', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Угол расположения', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Timeframe = _input('Timeframe', PERIOD_H6)  # Таймфрейм индикатора для расчета индикатора
P1 = _input('P1', 'EURUSD')  # Pair 1
P2 = _input('P2', 'GBPUSD')  # Pair 2
P3 = _input('P3', 'AUDUSD')  # Pair 3
P4 = _input('P4', 'GBPJPY')  # Pair 4
P5 = _input('P5', 'USDCHF')  # Pair 5
P6 = _input('P6', 'USDCAD')  # Pair 6
P7 = _input('P7', 'USDJPY')  # Pair 7
P8 = _input('P8', 'EURJPY')  # Pair 8
SignalBar = _input('SignalBar', 0)  # Номер бара для получения сигнала (0 - текущий бар)
Symbols_Sirname = _input('Symbols_Sirname', 'CandleDifference_Label_')  # Название для меток индикатора
Ind_Color = _input('Ind_Color', clrDarkOrchid)  # Цвет индикатора
Font_Size = _input('Font_Size', 15)  # Размер шрифта названия индикатора
X_ = _input('X_', 30)  # Смещение по горизонтали
Y_ = _input('Y_', 30)  # Смещение по вертикали
ShowIndName = _input('ShowIndName', True)  # Отображение названия индикатора
WhatCorner = _input('WhatCorner', CORNER_RIGHT_UPPER)  # Угол расположения
min_rates_total = 0
Y_N = Arr(8, 0, dyn=False)
d = Arr(8, 0.0, dyn=False)
pair = Arr(8, "", dyn=False)
lname = Arr(8, "", dyn=False)
data = Arr(8, "", dyn=False)

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
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

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
    global min_rates_total
    min_rates_total = 1 + _int(SignalBar)
    pair[0] = P1
    pair[1] = P2
    pair[2] = P3
    pair[3] = P4
    pair[4] = P5
    pair[5] = P6
    pair[6] = P7
    pair[7] = P8
    for numb in range(0, 8):
        lname[numb] = Symbols_Sirname + pair[numb]
    Y_N[0] = Y_
    for numb in range(1, 8):
        Y_N[numb] = Y_N[numb - 1] + _int(1.7 * Font_Size)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CandleDifference')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjectsDeleteAll(0, Symbols_Sirname, -1, -1)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    iOpen_ = Arr(1, 0.0, dyn=False)
    iClose_ = Arr(1, 0.0, dyn=False)
    for numb in range(0, 8):
        if CopyOpen(pair[numb], Timeframe, _int(SignalBar), 1, iOpen_) <= 0:
            return prev_calculated
        if CopyClose(pair[numb], Timeframe, _int(SignalBar), 1, iClose_) <= 0:
            return prev_calculated
        d[numb] = _fdiv(100 * iClose_[0], iOpen_[0]) - 100
    for numb in range(0, 8):
        data[numb] = ''
        if pair[numb] != '':
            data[numb] = pair[numb] + ': ' + DoubleToString(d[numb], 2) + '%'
    for numb in range(0, 8):
        SetTLabel(0, lname[numb], 0, WhatCorner, 2 * WhatCorner, X_, Y_N[numb], data[numb], data[numb], Ind_Color, 'Georgia', Font_Size)
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleDifferenceObj(_MQL5Indicator):
    name = 'CandleDifference_Obj'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Таймфрейм индикатора для расчета индикатора
        'SignalBar': 0,  # Номер бара для получения сигнала (0 - текущий бар)
        'Font_Size': 15,  # Размер шрифта названия индикатора
        'X_': 30,  # Смещение по горизонтали
        'Y_': 30,  # Смещение по вертикали
        'ShowIndName': True,  # Отображение названия индикатора
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Угол расположения
    }

