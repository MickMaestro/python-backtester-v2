"""jmacandlesign — converted from MQL5: MQL5 Indicators/JMACandleSign/jmacandlesign.mq5

Семафорный сигнальный индикатор с использованием двух индикаторов JMA, построенных на Open и Close значениях ценового ряда
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [16748574]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'JMACandle Sell', 2: 'JMACandle Buy'}, 'levels': [], 'description': ['Семафорный сигнальный индикатор с использованием двух индикаторов JMA, построенных на Open и Close значениях ценового ряда'], 'name': 'jmacandlesign', 'source': 'MQL5 Indicators/JMACandleSign/jmacandlesign.mq5', 'folder': 'JMACandleSign', 'inputs': [{'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'int', 'default': 7, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
JLength = _input('JLength', 7)  # Глубина сглаживания
JPhase = _input('JPhase', 100)  # Параметр сглаживания
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
O_Handle = 0
C_Handle = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, C_Handle, O_Handle, min_rates_total
    min_rates_total = 30 + 1
    ATR_Period = 15
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    PRICE_CLOSE_ = 1
    PRICE_OPEN_ = 2
    O_Handle = iCustom(None, 0, 'JMA', JLength, JPhase, PRICE_OPEN_, 0, 0)
    if O_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iJMA[OPEN]!')
        return INIT_FAILED
    C_Handle = iCustom(None, 0, 'JMA', JLength, JPhase, PRICE_CLOSE_, 0, 0)
    if C_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iJMA[CLOSE]!')
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
    short_name = 'JMACandleSign'
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


class Jmacandlesign(_MQL5Indicator):
    name = 'jmacandlesign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JLength': 7,  # Глубина сглаживания
        'JPhase': 100,  # Параметр сглаживания
    }

