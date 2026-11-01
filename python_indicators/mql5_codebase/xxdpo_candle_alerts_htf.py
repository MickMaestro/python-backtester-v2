"""XXDPO_Candle_Alerts_HTF — converted from MQL5: MQL5 Indicators/XXDPO_Candle_Alerts_HTF/XXDPO_Candle_Alerts_HTF.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 2763429, 8421504, 16711680, 16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XXDPO_Candle_Alerts_Open;XXDPO_Candle_Alerts_High;XXDPO_Candle_Alerts_Low;XXDPO_Candle_Alerts_Close'}, 'levels': [], 'description': [], 'name': 'XXDPO_Candle_Alerts_HTF', 'source': 'MQL5 Indicators/XXDPO_Candle_Alerts_HTF/XXDPO_Candle_Alerts_HTF.mq5', 'folder': 'XXDPO_Candle_Alerts_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 7, 'label': 'метод усреднения DPO', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 21, 'label': 'глубина  усреднения DPO', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр усреднения DPO,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'метод сглаживания индикатора', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 13, 'label': 'глубина сглаживания индикатора', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвигиндикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 0.6, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -0.6, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
MA_Method1 = _input('MA_Method1', MODE_T3)  # метод усреднения DPO
Length1 = _input('Length1', 21)  # глубина  усреднения DPO
Phase1 = _input('Phase1', 15)  # параметр усреднения DPO,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # метод сглаживания индикатора
Length2 = _input('Length2', 13)  # глубина сглаживания индикатора
Phase2 = _input('Phase2', 100)  # параметр сглаживания индикатора
Shift = _input('Shift', 0)  # сдвигиндикатора по горизонтали в барах
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
HighLevel = _input('HighLevel', 0.6)  # уровень перекупленности
LowLevel = _input('LowLevel', -0.6)  # уровень перепроданности
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 2
    short_name = 'XXDPO_Candle_Alerts' + ' ' + Symbol() + '(' + GetStringTimeframe(Period()) + ')'
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'XXDPO_Candle_Alerts', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, 0, Gap, HighLevel, LowLevel, NumberofBar, SoundON, NumberofAlerts, EMailON, PushON)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XXDPO_Candle_Alerts')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLimeGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('XXDPO_Candle_Alerts', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicatorBar("", TimeFrame, Ind_Handle, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicatorBar(Symb, TFrame, IndHandle, Time, Rates_Total, Prev_Calculated, Min_Rates_Total):
    global _s_CountIndicatorBar_LastCountBar
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicatorBar_LastCountBar = limit
    else:
        limit = _s_CountIndicatorBar_LastCountBar + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TimeFrame, _DT(Time[bar]), 1, IndTime) <= 0:
            return False
        if Time[bar] >= IndTime[0] and Time[bar + 1] < IndTime[0]:
            _s_CountIndicatorBar_LastCountBar = bar
            Col = Arr(1, 0.0, dyn=False)
            O = Arr(1, 0.0, dyn=False)
            H = Arr(1, 0.0, dyn=False)
            L = Arr(1, 0.0, dyn=False)
            C = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, 4, _DT(Time[bar]), 1, Col) <= 0:
                return False
            if CopyBuffer(IndHandle, 0, _DT(Time[bar]), 1, O) <= 0:
                return False
            if CopyBuffer(IndHandle, 1, _DT(Time[bar]), 1, H) <= 0:
                return False
            if CopyBuffer(IndHandle, 2, _DT(Time[bar]), 1, L) <= 0:
                return False
            if CopyBuffer(IndHandle, 3, _DT(Time[bar]), 1, C) <= 0:
                return False
            ExtColorBuffer[bar] = Col[0]
            ExtOpenBuffer[bar] = O[0]
            ExtLowBuffer[bar] = L[0]
            ExtHighBuffer[bar] = H[0]
            ExtCloseBuffer[bar] = C[0]
        else:
            ExtColorBuffer[bar] = ExtColorBuffer[bar + 1]
            ExtOpenBuffer[bar] = ExtOpenBuffer[bar + 1]
            ExtLowBuffer[bar] = ExtLowBuffer[bar + 1]
            ExtHighBuffer[bar] = ExtHighBuffer[bar + 1]
            ExtCloseBuffer[bar] = ExtCloseBuffer[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return False
    return True

# ---- static local variables
_s_CountIndicatorBar_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XXDPOCandleAlertsHTF(_MQL5Indicator):
    name = 'XXDPO_Candle_Alerts_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения DPO
        'Length1': 21,  # глубина  усреднения DPO
        'Phase1': 15,  # параметр усреднения DPO,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод сглаживания индикатора
        'Length2': 13,  # глубина сглаживания индикатора
        'Phase2': 100,  # параметр сглаживания индикатора
        'Shift': 0,  # сдвигиндикатора по горизонтали в барах
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'HighLevel': 0.6,  # уровень перекупленности
        'LowLevel': -0.6,  # уровень перепроданности
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

