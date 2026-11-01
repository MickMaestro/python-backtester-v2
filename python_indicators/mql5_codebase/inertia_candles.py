"""Inertia_Candles — converted from MQL5: MQL5 Indicators/Inertia_Candles/Inertia_Candles.mq5

Copyright: Copyright © 2008, NICTRADER; Link: http://nyctrader.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, NICTRADER', 'link': 'http://nyctrader.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [255, 8421504, 16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Inertia_Candles Open;Inertia_Candles High;Inertia_Candles Low;Inertia_Candles Close'}, 'levels': [], 'description': [''], 'name': 'Inertia_Candles', 'source': 'MQL5 Indicators/Inertia_Candles/Inertia_Candles.mq5', 'folder': 'Inertia_Candles', 'inputs': [{'mql': 'body', 'py': 'body', 'param': 'body', 'type': 'uint', 'default': 100, 'label': 'Размер изменения цены в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
body = _input('body', 100)  # Размер изменения цены в пунктах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
dBody = 0.0
min_rates_total = 0

def OnInit():
    global dBody, min_rates_total
    min_rates_total = 1
    dBody = body * Point()
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Inertia_Candles(' + _str(body) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtLowBuffer[bar] = 0.0
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtCloseBuffer[bar] = ExtHighBuffer[bar]
        ExtOpenBuffer[bar] = ExtCloseBuffer[bar]
        clr = 1
        if close[bar] > open[bar] and (close[bar] - open[bar]) > dBody:
            clr = 2
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
        if close[bar] < open[bar] and (open[bar] - close[bar]) > dBody:
            clr = 0
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
        ExtColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class InertiaCandles(_MQL5Indicator):
    name = 'Inertia_Candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'body': 100,  # Размер изменения цены в пунктах
    }

