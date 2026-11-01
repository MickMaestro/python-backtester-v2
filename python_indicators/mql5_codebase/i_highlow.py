"""i-highlow — converted from MQL5: MQL5 Indicators/i-HighLow/i-highlow.mq5

Copyright: Copyright © 2007, RickD; Link: http://www.e2e-fx.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, RickD', 'link': 'http://www.e2e-fx.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [9470064], 2: [16748574], 3: [16711935]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'i-HighLow Middle', 2: 'i-HighLow Upper', 3: 'i-HighLow Lower'}, 'levels': [], 'description': [''], 'name': 'i-highlow', 'source': 'MQL5 Indicators/i-HighLow/i-highlow.mq5', 'folder': 'i-HighLow', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 20, 'label': 'The number of candlesticks for determining extremum', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'uint', 'default': 50, 'label': 'Width of the offset from the candlestick in points', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 20)  # The number of candlesticks for determining extremum
Filter = _input('Filter', 50)  # Width of the offset from the candlestick in points
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
dFilter = 0.0
min_rates_total = 0

def OnInit():
    global dFilter, min_rates_total
    min_rates_total = _int(period)
    dFilter = Filter * Point()
    SetIndexBuffer(0, MiddleBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowestBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(MiddleBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'i-HighLow_Channel(', Filter, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    HH = 0.0
    LL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, period)]
        LL = low[ArrayMinimum(low, bar, period)]
        HighestBuffer[bar] = HH + dFilter
        LowestBuffer[bar] = LL - dFilter
        MiddleBuffer[bar] = (HH + LL) / 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IHighlow(_MQL5Indicator):
    name = 'i-highlow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 20,  # The number of candlesticks for determining extremum
        'Filter': 50,  # Width of the offset from the candlestick in points
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

