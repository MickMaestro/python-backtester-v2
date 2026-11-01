"""qqecandle — converted from MQL5: MQL5 Indicators/QQECandle/qqecandle.mq5

QQECandle
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 8421504, 14822282]}, 'widths': {}, 'styles': {}, 'labels': {1: 'QQECandle Open;QQECandle High;QQECandle Low;QQECandle Close'}, 'levels': [], 'description': ['QQECandle'], 'name': 'qqecandle', 'source': 'MQL5 Indicators/QQECandle/qqecandle.mq5', 'folder': 'QQECandle', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 2, 'label': 'Вариант алгоритма', 'sinput': False}, {'mql': 'RSI_Period', 'py': 'RSI_Period', 'param': 'RSI_Period', 'type': 'uint', 'default': 123, 'label': '', 'sinput': False}, {'mql': 'SF', 'py': 'SF', 'param': 'SF', 'type': 'uint', 'default': 41, 'label': '', 'sinput': False}, {'mql': 'DARFACTOR', 'py': 'DARFACTOR', 'param': 'DARFACTOR', 'type': 'double', 'default': 4.236, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum mode
MODE_MAIN = 0
MODE_SIGN = 1
MODE_DIFF = 2
_enum('mode', {0: 'MODE_MAIN', 1: 'MODE_SIGN', 2: 'MODE_DIFF'})

# ---- inputs and global variables
Mode = _input('Mode', MODE_DIFF)  # Вариант алгоритма
RSI_Period = _input('RSI_Period', 123)
SF = _input('SF', 41)
DARFACTOR = _input('DARFACTOR', 4.236)
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XPhase = _input('XPhase', 15)  # Параметр сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    Wilders_Period = _int((RSI_Period * 2) - 1)
    min_rates_total = _int(RSI_Period + 1)
    min_rates_total += GetStartBars(XMA_Method, SF, XPhase) + 1
    min_rates_total += GetStartBars(XMA_Method, Wilders_Period, XPhase)
    min_rates_total += GetStartBars(XMA_Method, Wilders_Period, XPhase)
    Ind_Handle[0] = iCustom(None, 0, 'QQECloudX', RSI_Period, SF, DARFACTOR, XMA_Method, XPhase, PRICE_OPEN, 0)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iQQE[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iCustom(None, 0, 'QQECloudX', RSI_Period, SF, DARFACTOR, XMA_Method, XPhase, PRICE_HIGH, 0)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iQQE[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iCustom(None, 0, 'QQECloudX', RSI_Period, SF, DARFACTOR, XMA_Method, XPhase, PRICE_LOW, 0)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iQQE[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iCustom(None, 0, 'QQECloudX', RSI_Period, SF, DARFACTOR, XMA_Method, XPhase, PRICE_CLOSE, 0)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iQQE[' + _str(3) + ']!')
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
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    short_name = 'QQECandle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
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
    _sw1 = Mode
    if _sw1 == MODE_MAIN:
        if CopyBuffer(Ind_Handle[0], MAIN_LINE, 0, to_copy, ExtOpenBuffer) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[1], MAIN_LINE, 0, to_copy, ExtHighBuffer) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[2], MAIN_LINE, 0, to_copy, ExtLowBuffer) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[3], MAIN_LINE, 0, to_copy, ExtCloseBuffer) <= 0:
            return 0
    elif _sw1 == MODE_SIGN:
        if CopyBuffer(Ind_Handle[0], SIGNAL_LINE, 0, to_copy, ExtOpenBuffer) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[1], SIGNAL_LINE, 0, to_copy, ExtHighBuffer) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[2], SIGNAL_LINE, 0, to_copy, ExtLowBuffer) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[3], SIGNAL_LINE, 0, to_copy, ExtCloseBuffer) <= 0:
            return 0
    elif _sw1 == MODE_DIFF:
        MOpen = Arr(0, 0.0)
        MHigh = Arr(0, 0.0)
        MLow = Arr(0, 0.0)
        MClose = Arr(0, 0.0)
        SOpen = Arr(0, 0.0)
        SHigh = Arr(0, 0.0)
        SLow = Arr(0, 0.0)
        SClose = Arr(0, 0.0)
        ArraySetAsSeries(MOpen, True)
        ArraySetAsSeries(MHigh, True)
        ArraySetAsSeries(MLow, True)
        ArraySetAsSeries(MClose, True)
        ArraySetAsSeries(SOpen, True)
        ArraySetAsSeries(SHigh, True)
        ArraySetAsSeries(SLow, True)
        ArraySetAsSeries(SClose, True)
        if CopyBuffer(Ind_Handle[0], MAIN_LINE, 0, to_copy, MOpen) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[1], MAIN_LINE, 0, to_copy, MHigh) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[2], MAIN_LINE, 0, to_copy, MLow) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[3], MAIN_LINE, 0, to_copy, MClose) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[0], SIGNAL_LINE, 0, to_copy, SOpen) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[1], SIGNAL_LINE, 0, to_copy, SHigh) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[2], SIGNAL_LINE, 0, to_copy, SLow) <= 0:
            return 0
        if CopyBuffer(Ind_Handle[3], SIGNAL_LINE, 0, to_copy, SClose) <= 0:
            return 0
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            ExtOpenBuffer[bar] = MOpen[bar] - SOpen[bar]
            ExtCloseBuffer[bar] = MClose[bar] - SClose[bar]
            ExtLowBuffer[bar] = MLow[bar] - SLow[bar]
            ExtHighBuffer[bar] = MHigh[bar] - SHigh[bar]
        else:
            bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        max_ = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        if ExtHighBuffer[bar] < max_:
            ExtHighBuffer[bar] = max_
        min_ = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        if ExtLowBuffer[bar] > min_:
            ExtLowBuffer[bar] = min_
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


class Qqecandle(_MQL5Indicator):
    name = 'qqecandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Mode': _Choice({0: 'расчет по основной линии', 1: 'расчет по сигнальной линии', 2: 'расчет по разности линий'}, default=2),  # Вариант алгоритма
        'RSI_Period': 123,
        'SF': 41,
        'DARFACTOR': 4.236,
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XPhase': 15,  # Параметр сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

