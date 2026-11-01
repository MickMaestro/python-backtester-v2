"""binarywave_htf_signal — converted from MQL5: MQL5 Indicators/BinaryWave_HTF_Signal/binarywave_htf_signal.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'binarywave_htf_signal', 'source': 'MQL5 Indicators/BinaryWave_HTF_Signal/binarywave_htf_signal.mq5', 'folder': 'BinaryWave_HTF_Signal', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'Финансовый актив', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Таймфрейм для расчета индикатора', 'sinput': False}, {'mql': 'WeightMA', 'py': 'WeightMA', 'param': 'WeightMA', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightMACD', 'py': 'WeightMACD', 'param': 'WeightMACD', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightOsMA', 'py': 'WeightOsMA', 'param': 'WeightOsMA', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightCCI', 'py': 'WeightCCI', 'param': 'WeightCCI', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightMOM', 'py': 'WeightMOM', 'param': 'WeightMOM', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightRSI', 'py': 'WeightRSI', 'param': 'WeightRSI', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightADX', 'py': 'WeightADX', 'param': 'WeightADX', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastMACD', 'py': 'FastMACD', 'param': 'FastMACD', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowMACD', 'py': 'SlowMACD', 'param': 'SlowMACD', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalMACD', 'py': 'SignalMACD', 'param': 'SignalMACD', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'PriceMACD', 'py': 'PriceMACD', 'param': 'PriceMACD', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalPeriod', 'py': 'SignalPeriod', 'param': 'SignalPeriod', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'OsMAPrice', 'py': 'OsMAPrice', 'param': 'OsMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'MOMPeriod', 'py': 'MOMPeriod', 'param': 'MOMPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MOMPrice', 'py': 'MOMPrice', 'param': 'MOMPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'bMA_Method', 'py': 'bMA_Method', 'param': 'bMA_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'bLength', 'py': 'bLength', 'param': 'bLength', 'type': 'int', 'default': 5, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'bPhase', 'py': 'bPhase', 'param': 'bPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'Номер бара для получения сигнала (0 - текущий бар)', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'BinaryWave_Label_', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'Upsymbol_Color', 'py': 'Upsymbol_Color', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Цвет символа роста', 'sinput': False}, {'mql': 'Dnsymbol_Color', 'py': 'Dnsymbol_Color', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет символа падения', 'sinput': False}, {'mql': 'IndName_Color', 'py': 'IndName_Color', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'Цвет названия индикатора', 'sinput': False}, {'mql': 'Symbols_Size', 'py': 'Symbols_Size', 'param': 'Symbols_Size', 'type': 'uint', 'default': 60, 'label': 'Размер символов сигнала', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 10, 'label': 'Размер шрифта названия индикатора', 'sinput': False}, {'mql': 'X_1', 'py': 'X_1', 'param': 'X_1', 'type': 'int', 'default': 5, 'label': 'Смещение названия по горизонтали', 'sinput': False}, {'mql': 'Y_1', 'py': 'Y_1', 'param': 'Y_1', 'type': 'int', 'default': -15, 'label': 'Смещение названия по вертикали', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Отображение названия индикатора', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Угол расположения', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 0, 'label': 'Смещение по горизонтали', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'Смещение по вертикали', 'sinput': False}, {'mql': 'alert_mode', 'py': 'alert_mode', 'param': 'alert_mode', 'type': 'int', 'default': 0, 'label': 'Вариант индикации срабатывания', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Количество подаваемых алертов', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_ALERT_MODE
OnlySound = 0
OnlyAlert = 1
_enum('ENUM_ALERT_MODE', {0: 'OnlySound', 1: 'OnlyAlert'})

# ---- inputs and global variables
Symbol_ = _input('Symbol_', '')  # Финансовый актив
Timeframe = _input('Timeframe', PERIOD_H6)  # Таймфрейм для расчета индикатора
WeightMA = _input('WeightMA', 1.0)
WeightMACD = _input('WeightMACD', 1.0)
WeightOsMA = _input('WeightOsMA', 1.0)
WeightCCI = _input('WeightCCI', 1.0)
WeightMOM = _input('WeightMOM', 1.0)
WeightRSI = _input('WeightRSI', 1.0)
WeightADX = _input('WeightADX', 1.0)
MAPeriod = _input('MAPeriod', 13)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
FastMACD = _input('FastMACD', 12)
SlowMACD = _input('SlowMACD', 26)
SignalMACD = _input('SignalMACD', 9)
PriceMACD = _input('PriceMACD', PRICE_CLOSE)
FastPeriod = _input('FastPeriod', 12)
SlowPeriod = _input('SlowPeriod', 26)
SignalPeriod = _input('SignalPeriod', 9)
OsMAPrice = _input('OsMAPrice', PRICE_CLOSE)
CCIPeriod = _input('CCIPeriod', 14)
CCIPrice = _input('CCIPrice', PRICE_MEDIAN)
MOMPeriod = _input('MOMPeriod', 14)
MOMPrice = _input('MOMPrice', PRICE_CLOSE)
RSIPeriod = _input('RSIPeriod', 14)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
ADXPeriod = _input('ADXPeriod', 14)
bMA_Method = _input('bMA_Method', MODE_JJMA)  # Метод усреднения
bLength = _input('bLength', 5)  # Глубина сглаживания
bPhase = _input('bPhase', 100)  # Параметр сглаживания
SignalBar = _input('SignalBar', 0)  # Номер бара для получения сигнала (0 - текущий бар)
Symbols_Sirname = _input('Symbols_Sirname', 'BinaryWave_Label_')  # Название для меток индикатора
Upsymbol_Color = _input('Upsymbol_Color', clrLimeGreen)  # Цвет символа роста
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
    min_rates_total_1 = MathMax(MAPeriod, MathMax(SlowPeriod, MathMax(CCIPeriod, MathMax(SlowMACD, MOMPeriod)))) + 1
    min_rates_total = min_rates_total_1 + GetStartBars(bMA_Method, bLength, bPhase)
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 3 + _int(SignalBar)
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
        StringConcatenate(_GlobRef(globals(), 'IndName'), 'BinaryWave', '(', Symb, ' ', GetStringTimeframe(Timeframe), ')')
    Ind_Handle = iCustom(Symb, Timeframe, 'BinaryWaveSign', WeightMA, WeightMACD, WeightOsMA, WeightCCI, WeightMOM, WeightRSI, WeightADX, MAPeriod, MAType, MAPrice, FastMACD, SlowMACD, SignalMACD, PriceMACD, FastPeriod, SlowPeriod, SignalPeriod, OsMAPrice, CCIPeriod, CCIPrice, MOMPeriod, MOMPrice, RSIPeriod, RSIPrice, ADXPeriod, bMA_Method, bLength, bPhase, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора BinaryWaveSign')
    shortname = Box("")
    StringConcatenate(shortname, 'BinaryWave', '( ', GetStringTimeframe(Timeframe), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

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


class BinarywaveHtfSignal(_MQL5Indicator):
    name = 'binarywave_htf_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Таймфрейм для расчета индикатора
        'WeightMA': 1.0,
        'WeightMACD': 1.0,
        'WeightOsMA': 1.0,
        'WeightCCI': 1.0,
        'WeightMOM': 1.0,
        'WeightRSI': 1.0,
        'WeightADX': 1.0,
        'MAPeriod': 13,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'FastMACD': 12,
        'SlowMACD': 26,
        'SignalMACD': 9,
        'PriceMACD': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'FastPeriod': 12,
        'SlowPeriod': 26,
        'SignalPeriod': 9,
        'OsMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'CCIPeriod': 14,
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),
        'MOMPeriod': 14,
        'MOMPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSIPeriod': 14,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'ADXPeriod': 14,
        'bMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'bLength': 5,  # Глубина сглаживания
        'bPhase': 100,  # Параметр сглаживания
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

