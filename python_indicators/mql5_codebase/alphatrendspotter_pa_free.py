"""alphatrendspotter-pa_free — converted from MQL5: MQL5 Indicators/AlphaTrendSpotter-pa_free/alphatrendspotter-pa_free.mq5

Alpha Trend Spotter Price Action
Suplement for Alpha Trend Spotter Indicator
Suitable for 5M to above timeframe
Suitable for 5 minutes Binary Option
Copyright: Copyright © 2015, Andy Ismail; Link: http://fbsbroker.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Andy Ismail', 'link': 'http://fbsbroker.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [13353215], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'AlphaTrendSpotter-pa_free Sell', 2: 'AlphaTrendSpotter-pa_free Buy'}, 'levels': [], 'description': ['Alpha Trend Spotter Price Action', 'Suplement for Alpha Trend Spotter Indicator', 'Suitable for 5M to above timeframe', 'Suitable for 5 minutes Binary Option'], 'name': 'alphatrendspotter-pa_free', 'source': 'MQL5 Indicators/AlphaTrendSpotter-pa_free/alphatrendspotter-pa_free.mq5', 'folder': 'AlphaTrendSpotter-pa_free', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 3)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(iPeriod + iPeriod)
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
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
    short_name = 'AlphaTrendSpotter-pa_free'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    CandleOpen = 0.0
    CandleOpen1 = 0.0
    CandleHigh = 0.0
    CandleHigh1 = 0.0
    CandleLow = 0.0
    CandleLow1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        CandleHigh = high[ArrayMaximum(high, bar, iPeriod)]
        CandleLow = low[ArrayMinimum(low, bar, iPeriod)]
        CandleOpen = open[bar]
        CandleHigh1 = high[ArrayMaximum(high, bar + iPeriod, iPeriod)]
        CandleLow1 = low[ArrayMinimum(low, bar + iPeriod, iPeriod)]
        CandleOpen1 = open[bar + iPeriod]
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if CandleLow < CandleLow1 and CandleOpen > CandleHigh1:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if CandleHigh > CandleHigh1 and CandleOpen < CandleLow1:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AlphatrendspotterPaFree(_MQL5Indicator):
    name = 'alphatrendspotter-pa_free'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 3,
    }

