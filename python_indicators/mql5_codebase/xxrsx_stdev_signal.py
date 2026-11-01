"""xxrsx_stdev_signal — converted from MQL5: MQL5 Indicators/XXRSX_StDev_Signal/xxrsx_stdev_signal.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16760576]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'XXRSX_StDev Sell', 2: 'XXRSX_StDev Buy'}, 'levels': [], 'description': [], 'name': 'xxrsx_stdev_signal', 'source': 'MQL5 Indicators/XXRSX_StDev_Signal/xxrsx_stdev_signal.mq5', 'folder': 'XXRSX_StDev_Signal', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 4, 'label': 'Вариант алгоритма', 'sinput': False}, {'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'Метод усреднения цены', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 15, 'label': 'Период средней', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'SSmoothMethod', 'py': 'SSmoothMethod', 'param': 'SSmoothMethod', 'type': 'int', 'default': 5, 'label': 'Метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'SPeriod', 'py': 'SPeriod', 'param': 'SPeriod', 'type': 'int', 'default': 7, 'label': 'Период сигнальной линии', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сигнальной линии', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'dK', 'py': 'dK', 'param': 'dK', 'type': 'double', 'default': 1.5, 'label': 'Коэффициент для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'Период квадратичного фильтра', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'int', 'default': 50, 'label': 'Уровень перекупленности', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'int', 'default': -50, 'label': 'Уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price
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
_enum('Applied_price', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# enum Applied_Mode
Mode_OnlyLevels = 1
Mode_OnlyStDev = 2
Mode_LevelsStDev = 3
Mode_LevelsStDev_On = 4
Mode_LevelsStDev_Out = 5
_enum('Applied_Mode', {1: 'Mode_OnlyLevels', 2: 'Mode_OnlyStDev', 3: 'Mode_LevelsStDev', 4: 'Mode_LevelsStDev_On', 5: 'Mode_LevelsStDev_Out'})

# ---- inputs and global variables
Mode = _input('Mode', Mode_LevelsStDev_On)  # Вариант алгоритма
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # Метод усреднения цены
DPeriod = _input('DPeriod', 15)  # Период средней
DPhase = _input('DPhase', 100)  # Параметр усреднения
SSmoothMethod = _input('SSmoothMethod', MODE_JurX)  # Метод усреднения сигнальной линии
SPeriod = _input('SPeriod', 7)  # Период сигнальной линии
SPhase = _input('SPhase', 100)  # Параметр сигнальной линии
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
dK = _input('dK', 1.5)  # Коэффициент для квадратичного фильтра
std_period = _input('std_period', 9)  # Период квадратичного фильтра
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpLevel = _input('UpLevel', 50)  # Уровень перекупленности
DnLevel = _input('DnLevel', -50)  # Уровень перепроданности
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
Ind_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, Ind_Handle, min_rates_total
    StartBarsD = GetStartBars(DSmoothMethod, DPeriod, DPhase) + 1
    StartBarsS = StartBarsD + GetStartBars(SSmoothMethod, SPeriod, SPhase)
    min_rates_total = StartBarsS + 1 + _int(std_period)
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, min_rates_total)
    ATR_Handle = iATR(Symbol(), PERIOD_CURRENT, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'XXRSX_StDev', DSmoothMethod, DPeriod, DPhase, SSmoothMethod, SPeriod, SPhase, IPC, dK, std_period, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XXRSX_StDev')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'XXRSX_StDev_Signal'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Ind_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Ind = Arr(0, 0.0)
    Up = Arr(0, 0.0)
    Dn = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    _sw1 = Mode
    if _sw1 == Mode_OnlyLevels:
        if CopyBuffer(Ind_Handle, 0, 0, to_copy, Ind) <= 0:
            return 0
        ArraySetAsSeries(Ind, True)
    elif _sw1 == Mode_OnlyStDev:
        if CopyBuffer(Ind_Handle, 3, 0, to_copy, Up) <= 0:
            return 0
        if CopyBuffer(Ind_Handle, 2, 0, to_copy, Dn) <= 0:
            return 0
        ArraySetAsSeries(Up, True)
        ArraySetAsSeries(Dn, True)
    elif _sw1 == Mode_LevelsStDev:
        if CopyBuffer(Ind_Handle, 0, 0, to_copy, Ind) <= 0:
            return 0
        if CopyBuffer(Ind_Handle, 3, 0, to_copy, Up) <= 0:
            return 0
        if CopyBuffer(Ind_Handle, 2, 0, to_copy, Dn) <= 0:
            return 0
        ArraySetAsSeries(Ind, True)
        ArraySetAsSeries(Up, True)
        ArraySetAsSeries(Dn, True)
    elif _sw1 == Mode_LevelsStDev_On:
        if CopyBuffer(Ind_Handle, 0, 0, to_copy, Ind) <= 0:
            return 0
        if CopyBuffer(Ind_Handle, 3, 0, to_copy, Up) <= 0:
            return 0
        if CopyBuffer(Ind_Handle, 2, 0, to_copy, Dn) <= 0:
            return 0
        ArraySetAsSeries(Ind, True)
        ArraySetAsSeries(Up, True)
        ArraySetAsSeries(Dn, True)
    elif _sw1 == Mode_LevelsStDev_Out:
        if CopyBuffer(Ind_Handle, 0, 0, to_copy, Ind) <= 0:
            return 0
        if CopyBuffer(Ind_Handle, 3, 0, to_copy, Up) <= 0:
            return 0
        if CopyBuffer(Ind_Handle, 2, 0, to_copy, Dn) <= 0:
            return 0
        ArraySetAsSeries(Ind, True)
        ArraySetAsSeries(Up, True)
        ArraySetAsSeries(Dn, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        _sw2 = Mode
        if _sw2 == Mode_OnlyLevels:
            if Ind[bar] > UpLevel:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Ind[bar] < DnLevel:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        elif _sw2 == Mode_OnlyStDev:
            if Up[bar] != EMPTY_VALUE:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Dn[bar] != EMPTY_VALUE:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        elif _sw2 == Mode_LevelsStDev:
            if Ind[bar] > UpLevel and Up[bar] != EMPTY_VALUE:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Ind[bar] < DnLevel and Up[bar] != EMPTY_VALUE:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Ind[bar] > UpLevel and Dn[bar] != EMPTY_VALUE:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
            if Ind[bar] < DnLevel and Dn[bar] != EMPTY_VALUE:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        elif _sw2 == Mode_LevelsStDev_On:
            if Ind[bar] > UpLevel and Up[bar] != EMPTY_VALUE:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Ind[bar] < DnLevel and Dn[bar] != EMPTY_VALUE:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        elif _sw2 == Mode_LevelsStDev_Out:
            if Ind[bar] > UpLevel and Dn[bar] != EMPTY_VALUE:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Ind[bar] < DnLevel and Up[bar] != EMPTY_VALUE:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XxrsxStdevSignal(_MQL5Indicator):
    name = 'xxrsx_stdev_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Mode': _Choice({1: 'Только уровни', 2: 'Только девиация', 3: 'Уровни плюс отклонение', 4: 'Уровни плюс отклонение по тренду', 5: 'Уровни плюс отклонение против тренда'}, default=4),  # Вариант алгоритма
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения цены
        'DPeriod': 15,  # Период средней
        'DPhase': 100,  # Параметр усреднения
        'SSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=5),  # Метод усреднения сигнальной линии
        'SPeriod': 7,  # Период сигнальной линии
        'SPhase': 100,  # Параметр сигнальной линии
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'dK': 1.5,  # Коэффициент для квадратичного фильтра
        'std_period': 9,  # Период квадратичного фильтра
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'UpLevel': 50,  # Уровень перекупленности
        'DnLevel': -50,  # Уровень перепроданности
    }

