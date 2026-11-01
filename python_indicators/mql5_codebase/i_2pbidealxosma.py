"""2pbidealxosma — converted from MQL5: MQL5 Indicators/2pbIdealXOSMA/2pbidealxosma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 2330219, 16748574, 9639167, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: '2pbIdealXOSMA'}, 'levels': [], 'description': [], 'name': '2pbidealxosma', 'source': 'MQL5 Indicators/2pbIdealXOSMA/2pbidealxosma.mq5', 'folder': '2pbIdealXOSMA', 'inputs': [{'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'int', 'default': 10, 'label': 'rough smoothing', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'int', 'default': 10, 'label': 'adjusting smoothing', 'sinput': False}, {'mql': 'PeriodX1', 'py': 'PeriodX1', 'param': 'PeriodX1', 'type': 'int', 'default': 10, 'label': 'first rough smoothing', 'sinput': False}, {'mql': 'PeriodX2', 'py': 'PeriodX2', 'param': 'PeriodX2', 'type': 'int', 'default': 10, 'label': 'first adjusting smoothing', 'sinput': False}, {'mql': 'PeriodY1', 'py': 'PeriodY1', 'param': 'PeriodY1', 'type': 'int', 'default': 10, 'label': 'second rough smoothing', 'sinput': False}, {'mql': 'PeriodY2', 'py': 'PeriodY2', 'param': 'PeriodY2', 'type': 'int', 'default': 10, 'label': 'second adjusting smoothing', 'sinput': False}, {'mql': 'PeriodZ1', 'py': 'PeriodZ1', 'param': 'PeriodZ1', 'type': 'int', 'default': 10, 'label': 'third rough smoothing', 'sinput': False}, {'mql': 'PeriodZ2', 'py': 'PeriodZ2', 'param': 'PeriodZ2', 'type': 'int', 'default': 10, 'label': 'third adjusting smoothing', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'smoothing method', 'sinput': False}, {'mql': 'Smooth_XMA', 'py': 'Smooth_XMA', 'param': 'Smooth_XMA', 'type': 'int', 'default': 9, 'label': 'smoothing period', 'sinput': False}, {'mql': 'Smooth_Phase', 'py': 'Smooth_Phase', 'param': 'Smooth_Phase', 'type': 'int', 'default': 100, 'label': 'moving averages smoothing parameter,', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Period1 = _input('Period1', 10)  # rough smoothing
Period2 = _input('Period2', 10)  # adjusting smoothing
PeriodX1 = _input('PeriodX1', 10)  # first rough smoothing
PeriodX2 = _input('PeriodX2', 10)  # first adjusting smoothing
PeriodY1 = _input('PeriodY1', 10)  # second rough smoothing
PeriodY2 = _input('PeriodY2', 10)  # second adjusting smoothing
PeriodZ1 = _input('PeriodZ1', 10)  # third rough smoothing
PeriodZ2 = _input('PeriodZ2', 10)  # third adjusting smoothing
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # smoothing method
Smooth_XMA = _input('Smooth_XMA', 9)  # smoothing period
Smooth_Phase = _input('Smooth_Phase', 100)  # moving averages smoothing parameter,
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
w1 = 0.0
w2 = 0.0
wX1 = 0.0
wX2 = 0.0
wY1 = 0.0
wY2 = 0.0
wZ1 = 0.0
wZ2 = 0.0
Moving0_ = 0.0
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
    global min_rates_total, w1, w2, wX1, wX2, wY1, wY2, wZ1, wZ2
    min_rates_total = 2 + XMA1.GetStartBars(SmoothMethod, Smooth_XMA, Smooth_Phase)
    w1 = 1.0 / Period1
    w2 = 1.0 / Period2
    wX1 = 1.0 / PeriodX1
    wX2 = 1.0 / PeriodX2
    wY1 = 1.0 / PeriodY1
    wY2 = 1.0 / PeriodY2
    wZ1 = 1.0 / PeriodZ1
    wZ2 = 1.0 / PeriodZ2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'Ind')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    XMA1.XMALengthCheck('Smooth_XMA', Smooth_XMA)
    XMA1.XMAPhaseCheck('Smooth_Phase', Smooth_Phase, SmoothMethod)
    IndicatorSetString(INDICATOR_SHORTNAME, '2pbIdealXOSMA')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global Moving01_, Moving0_, Moving11_, Moving21_
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    Moving0 = 0.0
    SlowMA = 0.0
    FastMA = 0.0
    macd = 0.0
    Moving00 = 0.0
    Moving10 = 0.0
    Moving20 = 0.0
    Moving01 = 0.0
    Moving11 = 0.0
    Moving21 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
        Moving0_ = price[begin]
        Moving01_ = price[begin]
        Moving11_ = price[begin]
        Moving21_ = price[begin]
    else:
        first = prev_calculated - 1
    Moving0 = Moving0_
    Moving01 = Moving01_
    Moving11 = Moving11_
    Moving21 = Moving21_
    bar = first
    for bar in range(bar, rates_total):
        Moving0 = GetIdealMASmooth(w1, w2, price[bar - 1], price[bar], Moving0)
        Moving00 = GetIdealMASmooth(wX1, wX2, price[bar - 1], price[bar], Moving01)
        Moving10 = GetIdealMASmooth(wY1, wY2, Moving01, Moving00, Moving11)
        Moving20 = GetIdealMASmooth(wZ1, wZ2, Moving11, Moving10, Moving21)
        Moving01 = Moving00
        Moving11 = Moving10
        Moving21 = Moving20
        SlowMA = Moving20
        FastMA = Moving0
        macd = FastMA - SlowMA
        IndBuffer[bar] = XMA1.XMASeries(1 + begin, prev_calculated, rates_total, SmoothMethod, Smooth_Phase, Smooth_XMA, macd, bar, False)
        if bar == (rates_total - 2):
            Moving0_ = Moving0
            Moving01_ = Moving01
            Moving11_ = Moving11
            Moving21_ = Moving21
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        ColorIndBuffer[bar] = 0.0
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 1.0
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 2.0
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 3.0
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2pbidealxosma(_MQL5Indicator):
    name = '2pbidealxosma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period1': 10,  # rough smoothing
        'Period2': 10,  # adjusting smoothing
        'PeriodX1': 10,  # first rough smoothing
        'PeriodX2': 10,  # first adjusting smoothing
        'PeriodY1': 10,  # second rough smoothing
        'PeriodY2': 10,  # second adjusting smoothing
        'PeriodZ1': 10,  # third rough smoothing
        'PeriodZ2': 10,  # third adjusting smoothing
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # smoothing method
        'Smooth_XMA': 9,  # smoothing period
        'Smooth_Phase': 100,  # moving averages smoothing parameter,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

