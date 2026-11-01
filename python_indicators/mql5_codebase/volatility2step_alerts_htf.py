"""Volatility2Step_Alerts_HTF — converted from MQL5: MQL5 Indicators/Volatility2Step_Alerts_HTF/Volatility2Step_Alerts_HTF.mq5

Volatility2Step_Alerts с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_minimum': 0.0}, 'types': {1: 3}, 'colors': {1: [14822282]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'Volatility2Step_Alerts'}, 'levels': [], 'description': ['Volatility2Step_Alerts с возможностью изменения таймфрейма во входных параметрах'], 'name': 'Volatility2Step_Alerts_HTF', 'source': 'MQL5 Indicators/Volatility2Step_Alerts_HTF/Volatility2Step_Alerts_HTF.mq5', 'folder': 'Volatility2Step_Alerts_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'VolatilityPeriod', 'py': 'VolatilityPeriod', 'param': 'VolatilityPeriod', 'type': 'uint', 'default': 5, 'label': 'период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'LevelsTotal', 'py': 'LevelsTotal', 'param': 'LevelsTotal', 'type': 'uint', 'default': 20, 'label': 'количество уровеней', 'sinput': False}, {'mql': 'StartLevel', 'py': 'StartLevel', 'param': 'StartLevel', 'type': 'uint', 'default': 25, 'label': 'стартовый уровень', 'sinput': False}, {'mql': 'LevelsStep', 'py': 'LevelsStep', 'param': 'LevelsStep', 'type': 'uint', 'default': 25, 'label': 'расстояние между уровнями', 'sinput': False}, {'mql': 'LevelsColor', 'py': 'LevelsColor', 'param': None, 'type': 'color', 'default': 36095, 'label': 'цвет уровеней', 'sinput': False}, {'mql': 'AlertLevel', 'py': 'AlertLevel', 'param': 'AlertLevel', 'type': 'uint', 'default': 150, 'label': 'Уровень срабатывания', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}, {'mql': 'AlertLevelColor', 'py': 'AlertLevelColor', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'цвет уровня срабатывания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
MAType = _input('MAType', MODE_SMA)  # метод усреднения
VolatilityPeriod = _input('VolatilityPeriod', 5)  # период индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
LevelsTotal = _input('LevelsTotal', 20)  # количество уровеней
StartLevel = _input('StartLevel', 25)  # стартовый уровень
LevelsStep = _input('LevelsStep', 25)  # расстояние между уровнями
LevelsColor = _input('LevelsColor', clrDarkOrange)  # цвет уровеней
AlertLevel = _input('AlertLevel', 150)  # Уровень срабатывания
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
AlertLevelColor = _input('AlertLevelColor', clrMediumSeaGreen)  # цвет уровня срабатывания
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0
LastCountBar = Arr(1, 0, dyn=False)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Volatility2Step_Alerts', MAType, VolatilityPeriod, 0, LevelsTotal, StartLevel, LevelsStep, LevelsColor, AlertLevel, NumberofBar, SoundON, NumberofAlerts, EMailON, PushON, AlertLevelColor)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Volatility2Step_Alerts')
        return INIT_FAILED
    IndInit(0, IndBuffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Volatility2Step_Alerts', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, LevelsTotal + 1)
    for numb in range(0, _int(LevelsTotal)):
        level = _int(StartLevel + (LevelsStep * numb))
        IndicatorSetDouble(INDICATOR_LEVELVALUE, numb, level)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, numb, LevelsColor)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, numb, STYLE_DASHDOTDOT)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, LevelsTotal, AlertLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, LevelsTotal, AlertLevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, LevelsTotal, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, LevelsTotal, 3)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('Volatility2Step_Alerts', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return 0
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, nTime, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        LastCountBar[Numb] = limit
    else:
        limit = LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(nTime[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if nTime[bar] >= IndTime[0] and nTime[bar + 1] < IndTime[0]:
            LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(nTime[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Volatility2StepAlertsHTF(_MQL5Indicator):
    name = 'Volatility2Step_Alerts_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # метод усреднения
        'VolatilityPeriod': 5,  # период индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'LevelsTotal': 20,  # количество уровеней
        'StartLevel': 25,  # стартовый уровень
        'LevelsStep': 25,  # расстояние между уровнями
        'AlertLevel': 150,  # Уровень срабатывания
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

