"""fatlmacdcandlesign — converted from MQL5: MQL5 Indicators/FatlMacdCandleSign/fatlmacdcandlesign.mq5

Семафорный сигнальный индикатор с использованием двух индикаторов FatlMacd, построенных на Open и Close значениях ценового ряда
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'FatlMacdCandle Sell', 2: 'FatlMacdCandle Buy'}, 'levels': [], 'description': ['Семафорный сигнальный индикатор с использованием двух индикаторов FatlMacd, построенных на Open и Close значениях ценового ряда'], 'name': 'fatlmacdcandlesign', 'source': 'MQL5 Indicators/FatlMacdCandleSign/fatlmacdcandlesign.mq5', 'folder': 'FatlMacdCandleSign', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'Метод усреднения гистограммы', 'sinput': False}, {'mql': 'XMA_Lengh', 'py': 'XMA_Lengh', 'param': 'XMA_Lengh', 'type': 'int', 'default': 20, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'XMA_Phase', 'py': 'XMA_Phase', 'param': 'XMA_Phase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения скользящих средних', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_T3)  # Метод усреднения гистограммы
XMA_Lengh = _input('XMA_Lengh', 20)  # Период усреднения
XMA_Phase = _input('XMA_Phase', 100)  # Параметр усреднения скользящих средних
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
O_Handle = 0
C_Handle = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, C_Handle, O_Handle, min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XMA_Lengh, XMA_Phase) + 1
    ATR_Period = 15
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    PRICE_CLOSE_ = 1
    PRICE_OPEN_ = 2
    O_Handle = iCustom(None, 0, 'FatlMacd', XMA_Method, XMA_Lengh, XMA_Phase, PRICE_OPEN_)
    if O_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iFatlMacd[OPEN]!')
        return INIT_FAILED
    C_Handle = iCustom(None, 0, 'FatlMacd', XMA_Method, XMA_Lengh, XMA_Phase, PRICE_CLOSE_)
    if C_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iFatlMacd[CLOSE]!')
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
    short_name = 'FatlMacdCandle'
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


class Fatlmacdcandlesign(_MQL5Indicator):
    name = 'fatlmacdcandlesign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения гистограммы
        'XMA_Lengh': 20,  # Период усреднения
        'XMA_Phase': 100,  # Параметр усреднения скользящих средних
    }

