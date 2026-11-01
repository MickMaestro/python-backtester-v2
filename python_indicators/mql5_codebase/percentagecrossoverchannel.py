"""percentagecrossoverchannel — converted from MQL5: MQL5 Indicators/Percentage Crossover Channel/percentagecrossoverchannel.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [16711680], 3: [16711935]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper PC Channel', 2: 'Middle PC Channel', 3: 'Lower PC Channel'}, 'levels': [], 'description': [], 'name': 'percentagecrossoverchannel', 'source': 'MQL5 Indicators/Percentage Crossover Channel/percentagecrossoverchannel.mq5', 'folder': 'Percentage Crossover Channel', 'inputs': [{'mql': 'percent', 'py': 'percent', 'param': 'percent', 'type': 'double', 'default': 1.0, 'label': 'Percentage price deviation from the indicator previous value', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
percent = _input('percent', 1.0)  # Percentage price deviation from the indicator previous value
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpperBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
plusvar = 0.0
minusvar = 0.0
min_rates_total = 0

def OnInit():
    global min_rates_total, minusvar, plusvar
    min_rates_total = 2
    var1 = percent / 100
    plusvar = 1 + var1
    minusvar = 1 - var1
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Percentage Crossover Channel(percent = ', percent, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    bar1 = 0
    if prev_calculated == 0:
        first = 1 + begin
        MiddleBuffer[first - 1] = price[first - 1]
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + begin)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        bar1 = bar - 1
        if (price[bar] * minusvar) > MiddleBuffer[bar1]:
            MiddleBuffer[bar] = price[bar] * minusvar
        else:
            if (price[bar] * plusvar) < MiddleBuffer[bar1]:
                MiddleBuffer[bar] = price[bar] * plusvar
            else:
                MiddleBuffer[bar] = MiddleBuffer[bar1]
        UpperBuffer[bar] = MiddleBuffer[bar] + ((MiddleBuffer[bar] / 100) * percent)
        LowerBuffer[bar] = MiddleBuffer[bar] - ((MiddleBuffer[bar] / 100) * percent)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Percentagecrossoverchannel(_MQL5Indicator):
    name = 'percentagecrossoverchannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'percent': 1.0,  # Percentage price deviation from the indicator previous value
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

