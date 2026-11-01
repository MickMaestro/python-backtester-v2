"""kaufwmacross — converted from MQL5: MQL5 Indicators/KaufWMAcross/kaufwmacross.mq5

Copyright: Copyright © 2007, John Smith; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, John Smith', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [7504122], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'KaufWMAcross Sell', 2: 'KaufWMAcross Buy'}, 'levels': [], 'description': [], 'name': 'kaufwmacross', 'source': 'MQL5 Indicators/KaufWMAcross/kaufwmacross.mq5', 'folder': 'KaufWMAcross', 'inputs': [{'mql': 'ama_period', 'py': 'ama_period', 'param': 'ama_period', 'type': 'uint', 'default': 9, 'label': 'Период AMA', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'uint', 'default': 2, 'label': 'Период быстрой скользящей', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'uint', 'default': 30, 'label': 'Период медленной скользящей', 'sinput': False}, {'mql': 'AMAPrice', 'py': 'AMAPrice', 'param': 'AMAPrice', 'type': 'int', 'default': 1, 'label': 'Цена AMA', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 13, 'label': 'Период MA', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 3, 'label': 'Метод усреднения MA', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'Цена MA', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ama_period = _input('ama_period', 9)  # Период AMA
fast_ma_period = _input('fast_ma_period', 2)  # Период быстрой скользящей
slow_ma_period = _input('slow_ma_period', 30)  # Период медленной скользящей
AMAPrice = _input('AMAPrice', PRICE_CLOSE)  # Цена AMA
MAPeriod = _input('MAPeriod', 13)  # Период MA
MAType = _input('MAType', MODE_LWMA)  # Метод усреднения MA
MAPrice = _input('MAPrice', PRICE_CLOSE)  # Цена MA
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0
AMA_Handle = 0
MA_Handle = 0

def OnInit():
    global AMA_Handle, ATR_Handle, MA_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(MathMax(ATR_Period, ama_period + 1), MAPeriod + 1))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    AMA_Handle = iAMA(None, 0, ama_period, fast_ma_period, slow_ma_period, 0, AMAPrice)
    if AMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iAMA')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'KaufWMAcross'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(AMA_Handle) < rates_total or BarsCalculated(MA_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    AMA = Arr(0, 0.0)
    MA = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    if CopyBuffer(AMA_Handle, 0, 0, to_copy, AMA) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(AMA, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if AMA[bar + 1] > MA[bar + 1] and AMA[bar] < MA[bar]:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if AMA[bar + 1] < MA[bar + 1] and AMA[bar] > MA[bar]:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Kaufwmacross(_MQL5Indicator):
    name = 'kaufwmacross'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ama_period': 9,  # Период AMA
        'fast_ma_period': 2,  # Период быстрой скользящей
        'slow_ma_period': 30,  # Период медленной скользящей
        'AMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена AMA
        'MAPeriod': 13,  # Период MA
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Метод усреднения MA
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена MA
    }

