"""wajdyss_Ichimoku_Candle — converted from MQL5: MQL5 Indicators/Wajdyss_Ichimoku_Candle/wajdyss_Ichimoku_Candle.mq5

Copyright: Copyright © 2009, Wajdyss; Link: wajdyss@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Wajdyss', 'link': 'wajdyss@yahoo.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 2763429, 16711680, 16776960]}, 'widths': {}, 'styles': {}, 'labels': {1: 'wajdyss_Ichimoku Open;wajdyss_Ichimoku High;wajdyss_Ichimoku Low;wajdyss_Ichimoku Close'}, 'levels': [], 'description': [''], 'name': 'wajdyss_Ichimoku_Candle', 'source': 'MQL5 Indicators/Wajdyss_Ichimoku_Candle/wajdyss_Ichimoku_Candle.mq5', 'folder': 'Wajdyss_Ichimoku_Candle', 'inputs': [{'mql': 'Kijun', 'py': 'Kijun', 'param': 'Kijun', 'type': 'uint', 'default': 26, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Kijun = _input('Kijun', 26)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(Kijun)
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
    IndicatorSetString(INDICATOR_SHORTNAME, 'wajdyss_Ichimoku_Candle')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    kijun = 0.0
    price = 0.0
    High = 0.0
    Low = 0.0
    limit = 0
    bar = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        High = high[bar]
        Low = low[bar]
        index = bar + _int(Kijun) - 1
        while index > bar:
            price = high[index]
            if High < price:
                High = price
            price = low[index]
            if Low > price:
                Low = price
            index -= 1
        kijun = (High + Low) / 2
        ExtOpenBuffer[bar] = open[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        ExtCloseBuffer[bar] = close[bar]
        if close[bar] > kijun:
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if close[bar] < kijun:
            if close[bar] <= open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WajdyssIchimokuCandle(_MQL5Indicator):
    name = 'wajdyss_Ichimoku_Candle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Kijun': 26,
    }

