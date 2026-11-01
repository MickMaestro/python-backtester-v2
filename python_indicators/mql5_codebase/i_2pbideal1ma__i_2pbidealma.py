"""2pbideal1ma — converted from MQL5: MQL5 Indicators/2pbIdealMA/2pbideal1ma.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: '2pbIdealMA'}, 'levels': [], 'description': [], 'name': '2pbideal1ma', 'source': 'MQL5 Indicators/2pbIdealMA/2pbideal1ma.mq5', 'folder': '2pbIdealMA', 'inputs': [{'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'int', 'default': 10, 'label': 'Rough smoothing', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'int', 'default': 10, 'label': 'Adjusting smoothing', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the average in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period1 = _input('Period1', 10)  # Rough smoothing
Period2 = _input('Period2', 10)  # Adjusting smoothing
MAShift = _input('MAShift', 0)  # Horizontal shift of the average in bars
ExtLineBuffer = Arr(0, 0.0)
w1 = 0.0
w2 = 0.0

def GetIdealMASmooth(W1_, W2_, Series1, Series0, Resalt1):
    Resalt0 = 0.0
    dSeries = 0.0
    dSeries2 = 0.0
    dSeries = Series0 - Series1
    dSeries2 = (dSeries * dSeries) - 1.0
    Resalt0 = _fdiv((W1_ * (Series0 - Resalt1)) + Resalt1 + (W2_ * Resalt1 * dSeries2), 1.0 + (W2_ * dSeries2))
    return Resalt0

def OnInit():
    global w1, w2
    w1 = 1.0 / Period1
    w2 = 1.0 / Period2
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, MAShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1)
    shortname = Box("")
    StringConcatenate(shortname, '2pbIdealMA(', w1, ',', w2, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (1 + begin):
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + 1)
        ExtLineBuffer[begin] = price[begin]
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtLineBuffer[bar] = GetIdealMASmooth(w1, w2, price[bar - 1], price[bar], ExtLineBuffer[bar - 1])
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2pbideal1ma(_MQL5Indicator):
    name = '2pbideal1ma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period1': 10,  # Rough smoothing
        'Period2': 10,  # Adjusting smoothing
        'MAShift': 0,  # Horizontal shift of the average in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

