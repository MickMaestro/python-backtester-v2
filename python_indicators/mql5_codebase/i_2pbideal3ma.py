"""2pbideal3ma — converted from MQL5: MQL5 Indicators/2pbIdealMA/2pbideal3ma.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [65535]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: '2pbIdeal3MA'}, 'levels': [], 'description': [], 'name': '2pbideal3ma', 'source': 'MQL5 Indicators/2pbIdealMA/2pbideal3ma.mq5', 'folder': '2pbIdealMA', 'inputs': [{'mql': 'PeriodX1', 'py': 'PeriodX1', 'param': 'PeriodX1', 'type': 'int', 'default': 10, 'label': 'First rough smoothing', 'sinput': False}, {'mql': 'PeriodX2', 'py': 'PeriodX2', 'param': 'PeriodX2', 'type': 'int', 'default': 10, 'label': 'First adjusting smoothing', 'sinput': False}, {'mql': 'PeriodY1', 'py': 'PeriodY1', 'param': 'PeriodY1', 'type': 'int', 'default': 10, 'label': 'Second rough smoothing', 'sinput': False}, {'mql': 'PeriodY2', 'py': 'PeriodY2', 'param': 'PeriodY2', 'type': 'int', 'default': 10, 'label': 'Second adjusting smoothing', 'sinput': False}, {'mql': 'PeriodZ1', 'py': 'PeriodZ1', 'param': 'PeriodZ1', 'type': 'int', 'default': 10, 'label': 'Third rough smoothing', 'sinput': False}, {'mql': 'PeriodZ2', 'py': 'PeriodZ2', 'param': 'PeriodZ2', 'type': 'int', 'default': 10, 'label': 'Third adjusting smoothing', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the average in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodX1 = _input('PeriodX1', 10)  # First rough smoothing
PeriodX2 = _input('PeriodX2', 10)  # First adjusting smoothing
PeriodY1 = _input('PeriodY1', 10)  # Second rough smoothing
PeriodY2 = _input('PeriodY2', 10)  # Second adjusting smoothing
PeriodZ1 = _input('PeriodZ1', 10)  # Third rough smoothing
PeriodZ2 = _input('PeriodZ2', 10)  # Third adjusting smoothing
MAShift = _input('MAShift', 0)  # Horizontal shift of the average in bars
ExtLineBuffer = Arr(0, 0.0)
wX1 = 0.0
wX2 = 0.0
wY1 = 0.0
wY2 = 0.0
wZ1 = 0.0
wZ2 = 0.0
Moving01_ = 0.0
Moving11_ = 0.0
Moving21_ = 0.0

def GetIdealMASmooth(W1_, W2_, Series1, Series0, Resalt1):
    Resalt0 = 0.0
    dSeries = 0.0
    dSeries2 = 0.0
    dSeries = Series0 - Series1
    dSeries2 = (dSeries * dSeries) - 1.0
    Resalt0 = _fdiv((W1_ * (Series0 - Resalt1)) + Resalt1 + (W2_ * Resalt1 * dSeries2), 1.0 + (W2_ * dSeries2))
    return Resalt0

def OnInit():
    global wX1, wX2, wY1, wY2, wZ1, wZ2
    wX1 = 1.0 / PeriodX1
    wX2 = 1.0 / PeriodX2
    wY1 = 1.0 / PeriodY1
    wY2 = 1.0 / PeriodY2
    wZ1 = 1.0 / PeriodZ1
    wZ2 = 1.0 / PeriodZ2
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, MAShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1)
    shortname = '2pbIdeal3MA'
    PlotIndexSetString(0, PLOT_LABEL, shortname)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global Moving01_, Moving11_, Moving21_
    if rates_total < (1 + begin):
        return 0
    first = 0
    bar = 0
    Moving00 = 0.0
    Moving10 = 0.0
    Moving20 = 0.0
    Moving01 = 0.0
    Moving11 = 0.0
    Moving21 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + 1)
        ExtLineBuffer[begin] = price[begin]
        Moving01_ = price[begin]
        Moving11_ = price[begin]
        Moving21_ = price[begin]
    else:
        first = prev_calculated - 1
    Moving01 = Moving01_
    Moving11 = Moving11_
    Moving21 = Moving21_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            Moving01_ = Moving01
            Moving11_ = Moving11
            Moving21_ = Moving21
        Moving00 = GetIdealMASmooth(wX1, wX2, price[bar - 1], price[bar], Moving01)
        Moving10 = GetIdealMASmooth(wY1, wY2, Moving01, Moving00, Moving11)
        Moving20 = GetIdealMASmooth(wZ1, wZ2, Moving11, Moving10, Moving21)
        Moving01 = Moving00
        Moving11 = Moving10
        Moving21 = Moving20
        ExtLineBuffer[bar] = Moving20
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2pbideal3ma(_MQL5Indicator):
    name = '2pbideal3ma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodX1': 10,  # First rough smoothing
        'PeriodX2': 10,  # First adjusting smoothing
        'PeriodY1': 10,  # Second rough smoothing
        'PeriodY2': 10,  # Second adjusting smoothing
        'PeriodZ1': 10,  # Third rough smoothing
        'PeriodZ2': 10,  # Third adjusting smoothing
        'MAShift': 0,  # Horizontal shift of the average in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

