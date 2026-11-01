"""Fractals at Close prices — converted from MQL5: MQL5 Indicators/Fractals at Close prices/Fractals at Close prices.mq5

Fractals at prices Close
Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [32768], 2: [32768]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Fractal Up', 2: 'Fractal Down'}, 'levels': [], 'description': ['Fractals at prices Close'], 'name': 'Fractals at Close prices', 'source': 'MQL5 Indicators/Fractals at Close prices/Fractals at Close prices.mq5', 'folder': 'Fractals at Close prices', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtUpperBuffer = Arr(0, 0.0)
ExtLowerBuffer = Arr(0, 0.0)
ExtArrowShift = -10

def OnInit():
    SetIndexBuffer(0, ExtUpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLowerBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_ARROW, 217)
    PlotIndexSetInteger(1, PLOT_ARROW, 218)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, ExtArrowShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -ExtArrowShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    limit = 0
    if rates_total < 5:
        return 0
    if prev_calculated < 7:
        limit = 2
        ArrayInitialize(ExtUpperBuffer, EMPTY_VALUE)
        ArrayInitialize(ExtLowerBuffer, EMPTY_VALUE)
    else:
        limit = rates_total - 5
    i = limit
    for i in range(i, rates_total - 3):
        if ((close[i] > close[i + 1] and close[i] > close[i + 2]) and close[i] >= close[i - 1]) and close[i] >= close[i - 2]:
            ExtUpperBuffer[i] = close[i]
        else:
            ExtUpperBuffer[i] = EMPTY_VALUE
        if ((close[i] < close[i + 1] and close[i] < close[i + 2]) and close[i] <= close[i - 1]) and close[i] <= close[i - 2]:
            ExtLowerBuffer[i] = close[i]
        else:
            ExtLowerBuffer[i] = EMPTY_VALUE
    else:
        i = _range_end(i, rates_total - 3, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalsAtClosePrices(_MQL5Indicator):
    name = 'Fractals at Close prices'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

