"""roundprice-ext — converted from MQL5: MQL5 Indicators/RoundPrice-Ext/roundprice-ext.mq5

Copyright: Copyright © 2004, Tartan; Link: http://forum.alpari-idc.ru/viewtopic.php?t=48186/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, Tartan', 'link': 'http://forum.alpari-idc.ru/viewtopic.php?t=48186/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [55295], 2: [255], 3: [65280], 4: [16776960], 5: [16711680], 6: [16711935], 7: [8388736]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {1: 'Line 1', 2: 'Line 2', 3: 'Line 3', 4: 'Line 4', 5: 'Line 5', 6: 'Line 6', 7: 'Line 7'}, 'levels': [], 'description': [''], 'name': 'roundprice-ext', 'source': 'MQL5 Indicators/RoundPrice-Ext/roundprice-ext.mq5', 'folder': 'RoundPrice-Ext', 'inputs': [{'mql': 't3_period', 'py': 't3_period', 'param': 't3_period', 'type': 'double', 'default': 8.0, 'label': '', 'sinput': False}, {'mql': 'b', 'py': 'b', 'param': 'b', 'type': 'double', 'default': 0.7, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
t3_period = _input('t3_period', 8.0)
b = _input('b', 0.7)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
e0Buffer = Arr(0, 0.0)
e1Buffer = Arr(0, 0.0)
e2Buffer = Arr(0, 0.0)
e3Buffer = Arr(0, 0.0)
e4Buffer = Arr(0, 0.0)
e5Buffer = Arr(0, 0.0)
e6Buffer = Arr(0, 0.0)
c1 = 0.0
c2 = 0.0
c3 = 0.0
c4 = 0.0
n = 0.0
w1 = 0.0
w2 = 0.0
b2 = 0.0
b3 = 0.0
dpo = 0.0
t3 = 0.0
min_rates_total = 0

def IndicatorInit(number, shift, drawbegin, empty_value, Arrow):
    SetIndexBuffer(number, Arrow, INDICATOR_DATA)
    PlotIndexSetInteger(number, PLOT_SHIFT, shift)
    PlotIndexSetInteger(number, PLOT_DRAW_BEGIN, drawbegin)
    PlotIndexSetDouble(number, PLOT_EMPTY_VALUE, empty_value)

def OnInit():
    global b2, b3, c1, c2, c3, c4, min_rates_total, n, w1, w2
    min_rates_total = 2
    b2 = b * b
    b3 = b2 * b
    c1 = -b3
    c2 = 3 * (b2 + b3)
    c3 = -3 * ((2 * b2) + b + b3)
    c4 = 1 + (3 * b) + b3 + (3 * b2)
    n = t3_period
    if n < 1:
        n = 1.0
    n = 1 + (0.5 * (n - 1))
    w1 = _fdiv(2, n + 1)
    w2 = 1 - w1
    IndicatorInit(0, Shift, min_rates_total, 0.0, e0Buffer)
    IndicatorInit(1, Shift, min_rates_total, 0.0, e1Buffer)
    IndicatorInit(2, Shift, min_rates_total, 0.0, e2Buffer)
    IndicatorInit(3, Shift, min_rates_total, 0.0, e3Buffer)
    IndicatorInit(4, Shift, min_rates_total, 0.0, e4Buffer)
    IndicatorInit(5, Shift, min_rates_total, 0.0, e5Buffer)
    IndicatorInit(6, Shift, min_rates_total, 0.0, e6Buffer)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RoundPrice-Ext')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global dpo, t3
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1 + begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, first)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, first)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, first)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, first)
        PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, first)
        PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, first)
        PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, first)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dpo = price[bar]
        e1Buffer[bar] = (w1 * dpo) + (w2 * e1Buffer[bar - 1])
        e2Buffer[bar] = (w1 * e1Buffer[bar]) + (w2 * e2Buffer[bar - 1])
        e3Buffer[bar] = (w1 * e2Buffer[bar]) + (w2 * e3Buffer[bar - 1])
        e4Buffer[bar] = (w1 * e3Buffer[bar]) + (w2 * e4Buffer[bar - 1])
        e5Buffer[bar] = (w1 * e4Buffer[bar]) + (w2 * e5Buffer[bar - 1])
        e6Buffer[bar] = (w1 * e5Buffer[bar]) + (w2 * e6Buffer[bar - 1])
        t3 = (c1 * e6Buffer[bar]) + (c2 * e5Buffer[bar]) + (c3 * e4Buffer[bar]) + (c4 * e3Buffer[bar])
        if not t3:
            t3 = dpo
        e0Buffer[bar] = t3
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RoundpriceExt(_MQL5Indicator):
    name = 'roundprice-ext'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        't3_period': 8.0,
        'b': 0.7,
        'Shift': 0,  # horizontal shift of the indicator in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

