"""t3_ianchmom — converted from MQL5: MQL5 Indicators/T3_iAnchMom/t3_ianchmom.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [255, 16711935, 8421504, 16711680, 32768]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'T3_iAnchMom'}, 'levels': [], 'description': [], 'name': 't3_ianchmom', 'source': 'MQL5 Indicators/T3_iAnchMom/t3_ianchmom.mq5', 'folder': 'T3_iAnchMom', 'inputs': [{'mql': 'FastT3', 'py': 'FastT3', 'param': 'FastT3', 'type': 'uint', 'default': 3, 'label': 'Fast T3 period', 'sinput': False}, {'mql': 'SlowT3', 'py': 'SlowT3', 'param': 'SlowT3', 'type': 'uint', 'default': 8, 'label': 'Slow T3 period', 'sinput': False}, {'mql': 'T3Phase', 'py': 'T3Phase', 'param': 'T3Phase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
FastT3 = _input('FastT3', 3)  # Fast T3 period
SlowT3 = _input('SlowT3', 8)  # Slow T3 period
T3Phase = _input('T3Phase', 15)  # Smoothing parameter
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3_iAnchMom')
    IndicatorSetInteger(INDICATOR_DIGITS, 6)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    t3a = 0.0
    t3b = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        t3a = T3A.T3Series(0, prev_calculated, rates_total, 0, T3Phase, FastT3, close[bar], bar, False)
        t3b = T3B.T3Series(0, prev_calculated, rates_total, 0, SlowT3, T3Phase, close[bar], bar, False)
        if t3b:
            IndBuffer[bar] = 100 * (_fdiv(t3a, t3b) - 1)
        else:
            IndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
T3A = _alloc(CT3)
T3A.__init__()
T3B = _alloc(CT3)
T3B.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3Ianchmom(_MQL5Indicator):
    name = 't3_ianchmom'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'FastT3': 3,  # Fast T3 period
        'SlowT3': 8,  # Slow T3 period
        'T3Phase': 15,  # Smoothing parameter
    }

