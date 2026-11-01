"""xccx_stdev_signal — converted from MQL5: MQL5 Indicators/XCCX_StDev_Signal/xccx_stdev_signal.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'XCCX_StDev Sell', 2: 'XCCX_StDev Buy'}, 'levels': [], 'description': [], 'name': 'xccx_stdev_signal', 'source': 'MQL5 Indicators/XCCX_StDev_Signal/xccx_stdev_signal.mq5', 'folder': 'XCCX_StDev_Signal', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 4, 'label': 'Вариант алгоритма', 'sinput': False}, {'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'Метод усреднения цены', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 15, 'label': 'Период средней', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'MSmoothMethod', 'py': 'MSmoothMethod', 'param': 'MSmoothMethod', 'type': 'int', 'default': 7, 'label': 'Метод усреднения отклонения', 'sinput': False}, {'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'uint', 'default': 15, 'label': 'Период среднего отклонения', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'int', 'default': 15, 'label': 'Параметр среднего отклонения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 6, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'dK', 'py': 'dK', 'param': 'dK', 'type': 'double', 'default': 2.0, 'label': 'Коэффициент для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'Период квадратичного фильтра', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'int', 'default': 50, 'label': 'Уровень перезакупа', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'int', 'default': -50, 'label': 'Уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
DPhase = _input('DPhase', 15)  # Параметр усреднения
MSmoothMethod = _input('MSmoothMethod', MODE_T3)  # Метод усреднения отклонения
MPeriod = _input('MPeriod', 15)  # Период среднего отклонения
MPhase = _input('MPhase', 15)  # Параметр среднего отклонения
IPC = _input('IPC', PRICE_TYPICAL)  # Ценовая константа
dK = _input('dK', 2.0)  # Коэффициент для квадратичного фильтра
std_period = _input('std_period', 9)  # Период квадратичного фильтра
UpLevel = _input('UpLevel', 50)  # Уровень перезакупа
DnLevel = _input('DnLevel', -50)  # Уровень перепроданности
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
Ind_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, Ind_Handle, min_rates_total
    min_rates_D = GetStartBars(DSmoothMethod, DPeriod, DPhase)
    min_rates_M = GetStartBars(MSmoothMethod, MPeriod, MPhase)
    min_rates_total = min_rates_D + min_rates_M + 1 + _int(std_period)
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, min_rates_total)
    ATR_Handle = iATR(Symbol(), PERIOD_CURRENT, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'XCCX_StDev', DSmoothMethod, DPeriod, DPhase, MSmoothMethod, MPeriod, MPhase, IPC, dK, std_period, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XCCX_StDev')
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
    short_name = 'XCCX_StDev_Signal'
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
            if Up[bar]:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Dn[bar]:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        elif _sw2 == Mode_LevelsStDev:
            if Ind[bar] > UpLevel and Up[bar]:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Ind[bar] < DnLevel and Up[bar]:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Ind[bar] > UpLevel and Dn[bar]:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
            if Ind[bar] < DnLevel and Dn[bar]:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        elif _sw2 == Mode_LevelsStDev_On:
            if Ind[bar] > UpLevel and Up[bar]:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Ind[bar] < DnLevel and Dn[bar]:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        elif _sw2 == Mode_LevelsStDev_Out:
            if Ind[bar] > UpLevel and Dn[bar]:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Ind[bar] < DnLevel and Up[bar]:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XccxStdevSignal(_MQL5Indicator):
    name = 'xccx_stdev_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Mode': _Choice({1: 'Только уровни', 2: 'Только девиация', 3: 'Уровни плюс отклонение', 4: 'Уровни плюс отклонение по тренду', 5: 'Уровни плюс отклонение против тренда'}, default=4),  # Вариант алгоритма
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения цены
        'DPeriod': 15,  # Период средней
        'DPhase': 15,  # Параметр усреднения
        'MSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения отклонения
        'MPeriod': 15,  # Период среднего отклонения
        'MPhase': 15,  # Параметр среднего отклонения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=6),  # Ценовая константа
        'dK': 2.0,  # Коэффициент для квадратичного фильтра
        'std_period': 9,  # Период квадратичного фильтра
        'UpLevel': 50,  # Уровень перезакупа
        'DnLevel': -50,  # Уровень перепроданности
    }

