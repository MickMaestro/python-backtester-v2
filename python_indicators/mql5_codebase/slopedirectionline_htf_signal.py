"""slopedirectionline_htf_signal — converted from MQL5: MQL5 Indicators/SlopeDirectionLine_HTF_Signal/slopedirectionline_htf_signal.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'slopedirectionline_htf_signal', 'source': 'MQL5 Indicators/SlopeDirectionLine_HTF_Signal/slopedirectionline_htf_signal.mq5', 'folder': 'SlopeDirectionLine_HTF_Signal', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'Финансовый актив', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 3, 'label': 'Метод первого усреднения', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 12, 'label': 'Глубина первого усреднения', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр первого усреднения', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 0, 'label': 'Метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Параметр второго сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'On_Push', 'py': 'On_Push', 'param': 'On_Push', 'type': 'bool', 'default': False, 'label': 'Разрешение на передачу push-сообщений', 'sinput': False}, {'mql': 'On_Email', 'py': 'On_Email', 'param': 'On_Email', 'type': 'bool', 'default': False, 'label': 'Разрешение на отправку почты', 'sinput': False}, {'mql': 'On_Alert', 'py': 'On_Alert', 'param': 'On_Alert', 'type': 'bool', 'default': True, 'label': 'Разрешение на подачу алерта', 'sinput': False}, {'mql': 'On_Play_Sound', 'py': 'On_Play_Sound', 'param': 'On_Play_Sound', 'type': 'bool', 'default': False, 'label': 'Разрешение на подачу звукового сигнала', 'sinput': False}, {'mql': 'NameFileSound', 'py': 'NameFileSound', 'param': None, 'type': 'string', 'default': 'expert.wav', 'label': 'Имя для файла звукового сигнала', 'sinput': False}, {'mql': 'CommentSirName', 'py': 'CommentSirName', 'param': None, 'type': 'string', 'default': 'SlopeDirectionLine: ', 'label': 'Первая часть алерт-коммента', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для сигнала', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'SlopeDirectionLine_Label_', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'UpSymbol_Color', 'py': 'UpSymbol_Color', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет символа роста', 'sinput': False}, {'mql': 'DnSymbol_Color', 'py': 'DnSymbol_Color', 'param': None, 'type': 'color', 'default': 255, 'label': 'Цвет символа падения', 'sinput': False}, {'mql': 'IndName_Color', 'py': 'IndName_Color', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'Цвет названия индикатора', 'sinput': False}, {'mql': 'Symbols_Size', 'py': 'Symbols_Size', 'param': 'Symbols_Size', 'type': 'uint', 'default': 34, 'label': 'Размер символов сигнала', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 15, 'label': 'Размер шрифта названия индикатора', 'sinput': False}, {'mql': 'X_3', 'py': 'X_3', 'param': 'X_3', 'type': 'int', 'default': 120, 'label': 'Смещение названия по горизонтали', 'sinput': False}, {'mql': 'Y_3', 'py': 'Y_3', 'param': 'Y_3', 'type': 'int', 'default': 10, 'label': 'Смещение названия по вертикали', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Отображение названия индикатора', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Угол расположения', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 0, 'label': 'Смещение по горизонтали', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 0, 'label': 'Смещение по вертикали', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum APPLIED_PRICE
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('APPLIED_PRICE', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
Symbol_ = _input('Symbol_', '')  # Финансовый актив
Timeframe = _input('Timeframe', PERIOD_H6)  # Таймфрейм индикатора для расчета индикатора
MA_Method1 = _input('MA_Method1', MODE_LWMA)  # Метод первого усреднения
Length1 = _input('Length1', 12)  # Глубина первого усреднения
Phase1 = _input('Phase1', 15)  # Параметр первого усреднения
MA_Method2 = _input('MA_Method2', MODE_SMA)  # Метод усреднения второго сглаживания
Phase2 = _input('Phase2', 15)  # Параметр второго сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # ценовая константа
On_Push = _input('On_Push', False)  # Разрешение на передачу push-сообщений
On_Email = _input('On_Email', False)  # Разрешение на отправку почты
On_Alert = _input('On_Alert', True)  # Разрешение на подачу алерта
On_Play_Sound = _input('On_Play_Sound', False)  # Разрешение на подачу звукового сигнала
NameFileSound = _input('NameFileSound', 'expert.wav')  # Имя для файла звукового сигнала
CommentSirName = _input('CommentSirName', 'SlopeDirectionLine: ')  # Первая часть алерт-коммента
SignalBar = _input('SignalBar', 1)  # Номер бара для сигнала
Symbols_Sirname = _input('Symbols_Sirname', 'SlopeDirectionLine_Label_')  # Название для меток индикатора
UpSymbol_Color = _input('UpSymbol_Color', clrBlue)  # Цвет символа роста
DnSymbol_Color = _input('DnSymbol_Color', clrRed)  # Цвет символа падения
IndName_Color = _input('IndName_Color', clrDarkOrchid)  # Цвет названия индикатора
Symbols_Size = _input('Symbols_Size', 34)  # Размер символов сигнала
Font_Size = _input('Font_Size', 15)  # Размер шрифта названия индикатора
X_3 = _input('X_3', 120)  # Смещение названия по горизонтали
Y_3 = _input('Y_3', 10)  # Смещение названия по вертикали
ShowIndName = _input('ShowIndName', True)  # Отображение названия индикатора
WhatCorner = _input('WhatCorner', CORNER_RIGHT_UPPER)  # Угол расположения
X_ = _input('X_', 0)  # Смещение по горизонтали
Y_ = _input('Y_', 0)  # Смещение по вертикали
SlopeDirectionLine_Handle = 0
min_rates_total = 0
X_0 = 0
X_1 = 0
X_2 = 0
X_3_ = 0
Yn = 0
Y_3_ = 0
name0 = ""
name1 = ""
name2 = ""
name3 = ""
IndName = ""
Symb = ""

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

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
        ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)

def OnInit():
    global SlopeDirectionLine_Handle, Symb, X_0, X_1, X_2, X_3_, Y_3_, Yn, min_rates_total, name0, name1, name2, name3
    XMA = CXMA()
    LengthR = _int(MathMax(MathSqrt(Length1), 1))
    min_rates_total = GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_total += _int(GetStartBars(MA_Method2, LengthR, Phase2) + 4 + SignalBar)
    if Symbol_ != '':
        Symb = Symbol_
    else:
        Symb = Symbol()
    X_0 = X_
    X_1 = _uint(X_0 + (Symbols_Size * 1.1))
    X_2 = _uint(X_1 + (Symbols_Size * 1.1))
    Yn = Y_ + 5
    name0 = Symbols_Sirname + '0'
    name1 = Symbols_Sirname + '1'
    name2 = Symbols_Sirname + '2'
    if ShowIndName:
        Y_3_ = Yn + Y_3
        X_3_ = X_0 + X_3
        name3 = Symbols_Sirname + '3'
        StringConcatenate(_GlobRef(globals(), 'IndName'), 'SlopeDirectionLine(', Symb, ' ', GetStringTimeframe(Timeframe), ')')
    SlopeDirectionLine_Handle = iCustom(Symb, Timeframe, 'SlopeDirectionLine', MA_Method1, Length1, Phase1, MA_Method2, Phase2, IPC, 0, 0, On_Push, On_Email, On_Alert, On_Play_Sound, NameFileSound, CommentSirName, SignalBar)
    if SlopeDirectionLine_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора SlopeDirectionLine')
    shortname = Box("")
    Smooth1 = XMA.GetString_MA_Method(MA_Method1)
    Smooth2 = XMA.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'SlopeDirectionLine(', Length1, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def Deinit():
    if ObjectFind(0, name0) != -1:
        ObjectDelete(0, name0)
    if ObjectFind(0, name1) != -1:
        ObjectDelete(0, name1)
    if ObjectFind(0, name2) != -1:
        ObjectDelete(0, name2)
    if ObjectFind(0, name3) != -1:
        ObjectDelete(0, name3)

def OnDeinit(reason):
    Deinit()
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(SlopeDirectionLine_Handle) < min_rates_total:
        return 0
    if BarsCalculated(SlopeDirectionLine_Handle) < Bars(Symb, Timeframe):
        return prev_calculated
    to_copy = 4
    dind0 = 0.0
    dind1 = 0.0
    dind2 = 0.0
    SlopeDirectionLine = Arr(4, 0.0, dyn=False)
    Color0 = 0
    Color1 = 0
    Color2 = 0
    if CopyBuffer(SlopeDirectionLine_Handle, 0, SignalBar, to_copy, SlopeDirectionLine) <= 0:
        return 0
    dind0 = SlopeDirectionLine[3] - SlopeDirectionLine[2]
    dind1 = SlopeDirectionLine[2] - SlopeDirectionLine[1]
    dind2 = SlopeDirectionLine[1] - SlopeDirectionLine[0]
    if dind0 < 0:
        Color0 = DnSymbol_Color
    else:
        Color0 = UpSymbol_Color
    if dind1 < 0:
        Color1 = DnSymbol_Color
    else:
        Color1 = UpSymbol_Color
    if dind2 < 0:
        Color2 = DnSymbol_Color
    else:
        Color2 = UpSymbol_Color
    SetTLabel(0, name0, 0, WhatCorner, 2 * WhatCorner, X_0, Yn, 't', Color0, 'Wingdings 2', Symbols_Size)
    SetTLabel(0, name1, 0, WhatCorner, 2 * WhatCorner, X_1, Yn, 'u', Color1, 'Wingdings 2', Symbols_Size)
    SetTLabel(0, name2, 0, WhatCorner, 2 * WhatCorner, X_2, Yn, 'v', Color2, 'Wingdings 2', Symbols_Size)
    if ShowIndName:
        SetTLabel(0, name3, 0, WhatCorner, 2 * WhatCorner, X_3_, Y_3_, IndName, IndName_Color, 'Georgia', Font_Size)
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SlopedirectionlineHtfSignal(_MQL5Indicator):
    name = 'slopedirectionline_htf_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Таймфрейм индикатора для расчета индикатора
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод первого усреднения
        'Length1': 12,  # Глубина первого усреднения
        'Phase1': 15,  # Параметр первого усреднения
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения второго сглаживания
        'Phase2': 15,  # Параметр второго сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'On_Push': False,  # Разрешение на передачу push-сообщений
        'On_Email': False,  # Разрешение на отправку почты
        'On_Alert': True,  # Разрешение на подачу алерта
        'On_Play_Sound': False,  # Разрешение на подачу звукового сигнала
        'SignalBar': 1,  # Номер бара для сигнала
        'Symbols_Size': 34,  # Размер символов сигнала
        'Font_Size': 15,  # Размер шрифта названия индикатора
        'X_3': 120,  # Смещение названия по горизонтали
        'Y_3': 10,  # Смещение названия по вертикали
        'ShowIndName': True,  # Отображение названия индикатора
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Угол расположения
        'X_': 0,  # Смещение по горизонтали
        'Y_': 0,  # Смещение по вертикали
    }

