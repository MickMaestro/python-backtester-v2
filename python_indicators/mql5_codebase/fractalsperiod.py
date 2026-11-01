"""fractalsperiod — converted from MQL5: MQL5 Indicators/FractalsPeriod/fractalsperiod.mq5

FractalsPeriod - Anzahl der Bars vor und nach
dem aktuellen Hoch/Tief(ermittelt Fraktal)
Copyright: Alexander Piechotta; Link: setchar@googlemail.com; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.calcfrac import *  # #include calcfrac.mqh

MQL5_META = {'props': {'copyright': 'Alexander Piechotta', 'link': 'setchar@googlemail.com', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [65535], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fractal Up', 2: 'Fractal Down'}, 'levels': [], 'description': ['FractalsPeriod - Anzahl der Bars vor und nach', 'dem aktuellen Hoch/Tief(ermittelt Fraktal)'], 'name': 'fractalsperiod', 'source': 'MQL5 Indicators/FractalsPeriod/fractalsperiod.mq5', 'folder': 'FractalsPeriod', 'inputs': [{'mql': 'CompleteBarsOnly', 'py': 'CompleteBarsOnly', 'param': 'CompleteBarsOnly', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'FractalsPeriodBefore', 'py': 'FractalsPeriodBefore', 'param': 'FractalsPeriodBefore', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'FractalsPeriodAfter', 'py': 'FractalsPeriodAfter', 'param': 'FractalsPeriodAfter', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'MaxBars', 'py': 'MaxBars', 'param': 'MaxBars', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['calcfrac.mqh']}

# ---- inputs and global variables
upper_fr = Arr(0, 0.0)
lower_fr = Arr(0, 0.0)
ExtArrowShift = -10
CompleteBarsOnly = _input('CompleteBarsOnly', True)
FractalsPeriodBefore = _input('FractalsPeriodBefore', 2)
FractalsPeriodAfter = _input('FractalsPeriodAfter', 5)
MaxBars = _input('MaxBars', 100)

def OnInit():
    SetIndexBuffer(0, upper_fr, INDICATOR_DATA)
    SetIndexBuffer(1, lower_fr, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_ARROW, 217)
    PlotIndexSetInteger(1, PLOT_ARROW, 218)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, ExtArrowShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -ExtArrowShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    Lower.before_period = FractalsPeriodBefore
    Lower.after_period = FractalsPeriodAfter
    Higher.before_period = FractalsPeriodBefore
    Higher.after_period = FractalsPeriodAfter

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    Limit = 0
    if rates_total < 5:
        return 0
    if CopyLow(None, None, 0, rates_total, Lower.values) <= 0:
        Print('Getting Low data is failed! Error', GetLastError())
        return 0
    if CopyHigh(None, None, 0, rates_total, Higher.values) <= 0:
        Print('Getting High data is failed! Error', GetLastError())
        return 0
    Limit = MathAbs(fmin(rates_total, MaxBars) - rates_total)
    if prev_calculated < 5:
        ArrayInitialize(upper_fr, 0.0)
        ArrayInitialize(lower_fr, 0.0)
    for i in range(Limit + FractalsPeriodBefore, rates_total - FractalsPeriodAfter - CompleteBarsOnly):
        if Higher.is_upper_fr(i):
            upper_fr[i] = high[i]
        else:
            upper_fr[i] = 0.0
        if Lower.is_lower_fr(i):
            lower_fr[i] = low[i]
        else:
            lower_fr[i] = 0.0
    return rates_total

# ---- global variables initialised from expressions
Higher = _alloc(CalcFrac)
Higher.__init__()
Lower = _alloc(CalcFrac)
Lower.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fractalsperiod(_MQL5Indicator):
    name = 'fractalsperiod'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'CompleteBarsOnly': True,
        'FractalsPeriodBefore': 2,
        'FractalsPeriodAfter': 5,
        'MaxBars': 100,
    }

