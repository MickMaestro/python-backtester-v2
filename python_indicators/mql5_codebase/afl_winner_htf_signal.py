"""afl_winner_htf_signal — converted from MQL5: MQL5 Indicators/AFL_Winner_HTF_Signal/afl_winner_htf_signal.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'afl_winner_htf_signal', 'source': 'MQL5 Indicators/AFL_Winner_HTF_Signal/afl_winner_htf_signal.mq5', 'folder': 'AFL_Winner_HTF_Signal', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'Финансовый актив', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'iAverage', 'py': 'iAverage', 'param': 'iAverage', 'type': 'uint', 'default': 5, 'label': 'Период для обработки входных данных', 'sinput': False}, {'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 10, 'label': 'Период поиска экстремумов', 'sinput': False}, {'mql': 'iMA_Method', 'py': 'iMA_Method', 'param': 'iMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'iLength', 'py': 'iLength', 'param': 'iLength', 'type': 'uint', 'default': 5, 'label': 'Глубина  сглаживания', 'sinput': False}, {'mql': 'iPhase', 'py': 'iPhase', 'param': 'iPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 7, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объем', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'Номер бара для получения сигнала (0 - текущий бар)', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'AFL_Winner_Label_', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'Upsymbol_Color', 'py': 'Upsymbol_Color', 'param': None, 'type': 'color', 'default': 14822282, 'label': 'Цвет символа роста', 'sinput': False}, {'mql': 'Dnsymbol_Color', 'py': 'Dnsymbol_Color', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет символа падения', 'sinput': False}, {'mql': 'IndName_Color', 'py': 'IndName_Color', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'Цвет названия индикатора', 'sinput': False}, {'mql': 'Symbols_Size', 'py': 'Symbols_Size', 'param': 'Symbols_Size', 'type': 'uint', 'default': 60, 'label': 'Размер символов сигнала', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 10, 'label': 'Размер шрифта названия индикатора', 'sinput': False}, {'mql': 'X_1', 'py': 'X_1', 'param': 'X_1', 'type': 'int', 'default': 5, 'label': 'Смещение названия по горизонтали', 'sinput': False}, {'mql': 'Y_1', 'py': 'Y_1', 'param': 'Y_1', 'type': 'int', 'default': -15, 'label': 'Смещение названия по вертикали', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Отображение названия индикатора', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Угол расположения', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 0, 'label': 'Смещение по горизонтали', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'Смещение по вертикали', 'sinput': False}, {'mql': 'alert_mode', 'py': 'alert_mode', 'param': 'alert_mode', 'type': 'int', 'default': 0, 'label': 'Вариант индикации срабатывания', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Количество подаваемых алертов', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_ALERT_MODE
OnlySound = 0
OnlyAlert = 1
_enum('ENUM_ALERT_MODE', {0: 'OnlySound', 1: 'OnlyAlert'})

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_JJMA = 4
MODE_JurX = 5
MODE_ParMA = 6
MODE_T3 = 7
MODE_VIDYA = 8
MODE_AMA = 9
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_JJMA', 5: 'MODE_JurX', 6: 'MODE_ParMA', 7: 'MODE_T3', 8: 'MODE_VIDYA', 9: 'MODE_AMA'})

# ---- inputs and global variables
Symbol_ = _input('Symbol_', '')  # Финансовый актив
Timeframe = _input('Timeframe', PERIOD_H6)  # Таймфрейм индикатора для расчета индикатора
iAverage = _input('iAverage', 5)  # Период для обработки входных данных
iPeriod = _input('iPeriod', 10)  # Период поиска экстремумов
iMA_Method = _input('iMA_Method', MODE_SMA)  # Метод усреднения первого сглаживания
iLength = _input('iLength', 5)  # Глубина  сглаживания
iPhase = _input('iPhase', 15)  # Параметр сглаживания
IPC = _input('IPC', PRICE_WEIGHTED)  # Ценовая константа
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объем
SignalBar = _input('SignalBar', 0)  # Номер бара для получения сигнала (0 - текущий бар)
Symbols_Sirname = _input('Symbols_Sirname', 'AFL_Winner_Label_')  # Название для меток индикатора
Upsymbol_Color = _input('Upsymbol_Color', clrBlueViolet)  # Цвет символа роста
Dnsymbol_Color = _input('Dnsymbol_Color', clrMagenta)  # Цвет символа падения
IndName_Color = _input('IndName_Color', clrDarkOrchid)  # Цвет названия индикатора
Symbols_Size = _input('Symbols_Size', 60)  # Размер символов сигнала
Font_Size = _input('Font_Size', 10)  # Размер шрифта названия индикатора
X_1 = _input('X_1', 5)  # Смещение названия по горизонтали
Y_1 = _input('Y_1', -15)  # Смещение названия по вертикали
ShowIndName = _input('ShowIndName', True)  # Отображение названия индикатора
WhatCorner = _input('WhatCorner', CORNER_RIGHT_UPPER)  # Угол расположения
X_ = _input('X_', 0)  # Смещение по горизонтали
Y_ = _input('Y_', 20)  # Смещение по вертикали
alert_mode = _input('alert_mode', OnlySound)  # Вариант индикации срабатывания
AlertCount = _input('AlertCount', 0)  # Количество подаваемых алертов
Ind_Handle = 0
min_rates_total = 0
X_0 = 0
Yn = 0
X_1_ = 0
Y_1_ = 0
name0 = ""
name1 = ""
IndName = ""
Symb = ""

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
    global Ind_Handle, Symb, X_0, X_1_, Y_1_, Yn, min_rates_total, name0, name1
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 7 + 1)
    min_rates_total = (min_rates_total + 1) + _int(SignalBar)
    if Symbol_ != '':
        Symb = Symbol_
    else:
        Symb = Symbol()
    X_0 = X_
    Yn = Y_ + 5
    name0 = Symbols_Sirname + '0'
    if ShowIndName:
        Y_1_ = Yn + Y_1
        X_1_ = X_0 + X_1
        name1 = Symbols_Sirname + '1'
        StringConcatenate(_GlobRef(globals(), 'IndName'), 'AFL_Winner', '(', Symb, ' ', GetStringTimeframe(Timeframe), ')')
    Ind_Handle = iCustom(Symb, Timeframe, 'AFL_WinnerSign', iAverage, iPeriod, iMA_Method, iLength, iPhase, IPC, VolumeType, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора AFL_WinnerSign')
        return INIT_FAILED
    shortname = IndName
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def Deinit():
    if ObjectFind(0, name0) != -1:
        ObjectDelete(0, name0)
    if ObjectFind(0, name1) != -1:
        ObjectDelete(0, name1)

def OnDeinit(reason):
    Deinit()
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_buycount, _s_OnCalculate_prev_time, _s_OnCalculate_sellcount, _s_OnCalculate_trend_
    if BarsCalculated(Ind_Handle) < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symb, Timeframe):
        return prev_calculated
    limit = 0
    trend = 0
    UpBTR = Arr(0, 0.0)
    DnBTR = Arr(0, 0.0)
    rates_time = 0
    TIME = Arr(1, 0, dyn=False)
    Color0 = clrNONE
    SignSymbol = ""
    signal = False
    if CopyTime(Symb, Timeframe, SignalBar, 1, TIME) <= 0:
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        _s_OnCalculate_prev_time = time[0]
        _s_OnCalculate_trend_ = 0
    rates_time = TimeCurrent()
    if CopyBuffer(Ind_Handle, 0, _DT(rates_time), _DT(_s_OnCalculate_prev_time), DnBTR) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 1, _DT(rates_time), _DT(_s_OnCalculate_prev_time), UpBTR) <= 0:
        return 0
    limit = ArraySize(UpBTR) - 1
    trend = _s_OnCalculate_trend_
    ArraySetAsSeries(DnBTR, True)
    ArraySetAsSeries(UpBTR, True)
    if TIME[0] != _s_OnCalculate_prev_time and AlertCount:
        _s_OnCalculate_buycount = AlertCount
        _s_OnCalculate_sellcount = AlertCount
    for bar in range(limit, 0 - 1, -1):
        if UpBTR[bar] and UpBTR[bar] != EMPTY_VALUE:
            trend = 1
            if not bar:
                signal = True
        if DnBTR[bar] and DnBTR[bar] != EMPTY_VALUE:
            trend = -1
            if not bar:
                signal = True
        if bar or SignalBar:
            _s_OnCalculate_trend_ = trend
    if trend > 0:
        Color0 = Upsymbol_Color
        if signal:
            SignSymbol = 'ж'
            if _s_OnCalculate_buycount:
                _sw1 = alert_mode
                if _sw1 == OnlyAlert:
                    Alert(IndName + ': ' + 'Buy signal')
                elif _sw1 == OnlySound:
                    PlaySound('alert.wav')
                _s_OnCalculate_buycount -= 1
        else:
            SignSymbol = 'в'
    if trend < 0:
        Color0 = Dnsymbol_Color
        if signal:
            SignSymbol = 'и'
            if _s_OnCalculate_sellcount:
                _sw2 = alert_mode
                if _sw2 == OnlyAlert:
                    Alert(IndName + ': ' + 'Sell signal')
                elif _sw2 == OnlySound:
                    PlaySound('alert.wav')
                _s_OnCalculate_sellcount -= 1
        else:
            SignSymbol = 'в'
    if trend:
        if ShowIndName:
            SetTLabel(0, name1, 0, WhatCorner, 2 * WhatCorner, X_1_, Y_1_, IndName, IndName, IndName_Color, 'Georgia', Font_Size)
        if signal:
            SetTLabel(0, name0, 0, WhatCorner, 2 * WhatCorner, X_0, Yn, SignSymbol, IndName, Color0, 'Wingdings 3', Symbols_Size)
        else:
            SetTLabel(0, name0, 0, WhatCorner, 2 * WhatCorner, X_0, Yn, SignSymbol, IndName, Color0, 'Wingdings 3', Symbols_Size)
    else:
        Deinit()
    ChartRedraw(0)
    _s_OnCalculate_prev_time = TIME[0]
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_time = 0
_s_OnCalculate_trend_ = 0
_s_OnCalculate_buycount = 0
_s_OnCalculate_sellcount = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AflWinnerHtfSignal(_MQL5Indicator):
    name = 'afl_winner_htf_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Таймфрейм индикатора для расчета индикатора
        'iAverage': 5,  # Период для обработки входных данных
        'iPeriod': 10,  # Период поиска экстремумов
        'iMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения первого сглаживания
        'iLength': 5,  # Глубина  сглаживания
        'iPhase': 15,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=7),  # Ценовая константа
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объем
        'SignalBar': 0,  # Номер бара для получения сигнала (0 - текущий бар)
        'Symbols_Size': 60,  # Размер символов сигнала
        'Font_Size': 10,  # Размер шрифта названия индикатора
        'X_1': 5,  # Смещение названия по горизонтали
        'Y_1': -15,  # Смещение названия по вертикали
        'ShowIndName': True,  # Отображение названия индикатора
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Угол расположения
        'X_': 0,  # Смещение по горизонтали
        'Y_': 20,  # Смещение по вертикали
        'alert_mode': _Choice({0: 'только звук', 1: 'только алерт'}, default=0),  # Вариант индикации срабатывания
        'AlertCount': 0,  # Количество подаваемых алертов
    }

