"""emvcandlesign — converted from MQL5: MQL5 Indicators/EMVCandleSign/emvcandlesign.mq5

Семафорный сигнальный индикатор с использованием двух индикаторов EMV, построенных на Open и Close значениях ценового ряда
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [36095], 2: [13749760]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'EMVCandle Sell', 2: 'EMVCandle Buy'}, 'levels': [], 'description': ['Семафорный сигнальный индикатор с использованием двух индикаторов EMV, построенных на Open и Close значениях ценового ряда'], 'name': 'emvcandlesign', 'source': 'MQL5 Indicators/EMVCandleSign/emvcandlesign.mq5', 'folder': 'EMVCandleSign', 'inputs': [{'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'SmLength', 'py': 'SmLength', 'param': 'SmLength', 'type': 'uint', 'default': 14, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'SmPhase', 'py': 'SmPhase', 'param': 'SmPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 9, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объем', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
MA_SMethod = _input('MA_SMethod', MODE_SMA)  # Метод усреднения
SmLength = _input('SmLength', 14)  # Глубина сглаживания
SmPhase = _input('SmPhase', 15)  # Параметр сглаживания
IPC = _input('IPC', PRICE_QUARTER_)  # Ценовая константа
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объем
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
O_Handle = 0
C_Handle = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, C_Handle, O_Handle, min_rates_total
    min_rates_total = GetStartBars(MA_SMethod, SmLength, SmPhase) + 1 + 1
    ATR_Period = 15
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    O_Handle = iCustom(None, 0, 'EMV', MA_SMethod, SmLength, SmPhase, PRICE_OPEN, VolumeType, 0)
    if O_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iEMV[OPEN]!')
        return INIT_FAILED
    C_Handle = iCustom(None, 0, 'EMV', MA_SMethod, SmLength, SmPhase, PRICE_CLOSE, VolumeType, 0)
    if C_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iEMV[CLOSE]!')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 172)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 172)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'EMVCandle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(O_Handle) < rates_total or BarsCalculated(C_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    FOpen = Arr(0, 0.0)
    FClose = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(O_Handle, 0, 0, to_copy, FOpen) <= 0:
        return 0
    if CopyBuffer(C_Handle, 0, 0, to_copy, FClose) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(FOpen, True)
    ArraySetAsSeries(FClose, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if FOpen[bar + 1] >= FClose[bar + 1] and FOpen[bar] < FClose[bar]:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if FOpen[bar + 1] <= FClose[bar + 1] and FOpen[bar] > FClose[bar]:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Emvcandlesign(_MQL5Indicator):
    name = 'emvcandlesign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'SmLength': 14,  # Глубина сглаживания
        'SmPhase': 15,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=9),  # Ценовая константа
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объем
    }

