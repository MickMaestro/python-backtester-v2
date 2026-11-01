"""Directed_Movement_Candle — converted from MQL5: MQL5 Indicators/Directed_Movement_Candle/Directed_Movement_Candle.mq5

Directed_MovementCandle
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 8421504, 16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Directed_Movement_Candle Open;High;Low;Close'}, 'levels': [], 'description': ['Directed_MovementCandle'], 'name': 'Directed_Movement_Candle', 'source': 'MQL5 Indicators/Directed_Movement_Candle/Directed_Movement_Candle.mq5', 'folder': 'Directed_Movement_Candle', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 1, 'label': 'усреднение RSI', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 12, 'label': 'глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 5, 'label': 'глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'параметр второго сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 70, 'label': 'верхний уровень срабатывания', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 50, 'label': 'середина диапазона', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': 30, 'label': 'нижний уровень срабатывания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Smooth
MODE_FIRST = 0
MODE_SECOND = 1
_enum('Smooth', {0: 'MODE_FIRST', 1: 'MODE_SECOND'})

# ---- inputs and global variables
Mode = _input('Mode', MODE_SECOND)  # усреднение RSI
RSIPeriod = _input('RSIPeriod', 14)  # период индикатора
MA_Method1 = _input('MA_Method1', MODE_SMA_)  # метод усреднения первого сглаживания
Length1 = _input('Length1', 12)  # глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # параметр первого сглаживания,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # метод усреднения второго сглаживания
Length2 = _input('Length2', 5)  # глубина  второго сглаживания
Phase2 = _input('Phase2', 15)  # параметр второго сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
HighLevel = _input('HighLevel', 70)  # верхний уровень срабатывания
MiddleLevel = _input('MiddleLevel', 50)  # середина диапазона
LowLevel = _input('LowLevel', 30)  # нижний уровень срабатывания
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = _int(RSIPeriod)
    min_rates_total += GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_total += GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total += 2
    Ind_Handle[0] = iCustom(None, 0, 'Directed_Movement', RSIPeriod, PRICE_OPEN, MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, 0)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Directed_Movement[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iCustom(None, 0, 'Directed_Movement', RSIPeriod, PRICE_HIGH, MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, 0)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Directed_Movement[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iCustom(None, 0, 'Directed_Movement', RSIPeriod, PRICE_LOW, MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, 0)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Directed_Movement[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iCustom(None, 0, 'Directed_Movement', RSIPeriod, PRICE_CLOSE, MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, 0)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Directed_Movement[' + _str(3) + ']!')
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
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    short_name = 'Directed_Movement_Candl'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 70)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 30)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(Ind_Handle[0]) < rates_total or BarsCalculated(Ind_Handle[1]) < rates_total) or BarsCalculated(Ind_Handle[2]) < rates_total) or BarsCalculated(Ind_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle[0], Mode, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], Mode, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], Mode, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[3], Mode, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMin(MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar]), 100)
        Min = MathMax(MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar]), 0)
        ExtHighBuffer[bar] = MathMin(MathMax(Max, ExtHighBuffer[bar]), 100)
        ExtLowBuffer[bar] = MathMax(MathMin(Min, ExtLowBuffer[bar]), 0)
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DirectedMovementCandle(_MQL5Indicator):
    name = 'Directed_Movement_Candle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Mode': _Choice({0: 'первое', 1: 'второе'}, default=1),  # усреднение RSI
        'RSIPeriod': 14,  # период индикатора
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения первого сглаживания
        'Length1': 12,  # глубина  первого сглаживания
        'Phase1': 15,  # параметр первого сглаживания,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения второго сглаживания
        'Length2': 5,  # глубина  второго сглаживания
        'Phase2': 15,  # параметр второго сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'HighLevel': 70,  # верхний уровень срабатывания
        'MiddleLevel': 50,  # середина диапазона
        'LowLevel': 30,  # нижний уровень срабатывания
    }

