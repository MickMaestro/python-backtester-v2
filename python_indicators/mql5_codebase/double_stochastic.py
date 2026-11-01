"""double_stochastic — converted from MQL5: MQL5 Indicators/Double Stochastic/double_stochastic.mq5

Copyright: mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_minimum': -1.0, 'indicator_maximum': 101.0}, 'types': {1: 8}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Stochastic'}, 'levels': [20.0, 50.0, 80.0], 'description': [], 'name': 'double_stochastic', 'source': 'MQL5 Indicators/Double Stochastic/double_stochastic.mq5', 'folder': 'Double Stochastic', 'inputs': [{'mql': 'StochasticPeriod', 'py': 'StochasticPeriod', 'param': 'StochasticPeriod', 'type': 'int', 'default': 55, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'EMAPeriod', 'py': 'EMAPeriod', 'param': 'EMAPeriod', 'type': 'int', 'default': 15, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 0, 'label': 'Oversold color', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 0, 'label': 'Overbought color', 'sinput': False}, {'mql': 'ColorSteps', 'py': 'ColorSteps', 'param': 'ColorSteps', 'type': 'int', 'default': 20, 'label': 'Color steps for drawing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Lime = 0x00FF00  # MQL4 colour name
MediumVioletRed = 0x8515C7  # MQL4 colour name

# ---- inputs and global variables
StochasticPeriod = _input('StochasticPeriod', 55)  # Stochastic period
EMAPeriod = _input('EMAPeriod', 15)  # Smoothing period
ColorSteps = _input('ColorSteps', 20)  # Color steps for drawing
StochasticBuffer = Arr(0, 0.0)
Colors = Arr(0, 0.0)
calcBuffer1 = Arr(0, 0.0)
cSteps = 0

def OnInit():
    global cSteps
    SetIndexBuffer(0, StochasticBuffer, INDICATOR_DATA)
    ArraySetAsSeries(StochasticBuffer, True)
    SetIndexBuffer(1, Colors, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(Colors, True)
    SetIndexBuffer(2, calcBuffer1, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(calcBuffer1, True)
    cSteps = (ColorSteps if (ColorSteps > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps)
    i = 0
    while i < cSteps:
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps, ColorFrom, ColorTo))
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not ArrayGetAsSeries(close):
        ArraySetAsSeries(close, True)
    if not ArrayGetAsSeries(high):
        ArraySetAsSeries(high, True)
    if not ArrayGetAsSeries(low):
        ArraySetAsSeries(low, True)
    max_ = 0.0
    min_ = 0.0
    sto = 0.0
    alpha = _fdiv(2.0, 1.0 + EMAPeriod)
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    if prev_calculated == 0:
        limit -= StochasticPeriod
        for i in range(1, StochasticPeriod + 1):
            StochasticBuffer[rates_total - i] = 0.0
    for i in range(limit, 0 - 1, -1):
        max_ = high[i]
        for k in range(1, StochasticPeriod):
            max_ = MathMax(max_, high[i + k])
        min_ = low[i]
        for k in range(1, StochasticPeriod):
            min_ = MathMin(min_, low[i + k])
        if max_ != min_:
            sto = _fdiv(close[i] - min_, max_ - min_) * 100.0
        else:
            sto = 0.0
        calcBuffer1[i] = calcBuffer1[i + 1] + (alpha * (sto - calcBuffer1[i + 1]))
        max_ = calcBuffer1[i]
        for k in range(1, StochasticPeriod):
            max_ = MathMax(max_, calcBuffer1[i + k])
        min_ = calcBuffer1[i]
        for k in range(1, StochasticPeriod):
            min_ = MathMin(min_, calcBuffer1[i + k])
        if max_ != min_:
            sto = _fdiv(calcBuffer1[i] - min_, max_ - min_) * 100.0
        else:
            sto = 0.0
        StochasticBuffer[i] = StochasticBuffer[i + 1] + (alpha * (sto - StochasticBuffer[i + 1]))
        Colors[i] = MathFloor((StochasticBuffer[i] * cSteps) / 100.0)
    return rates_total

def getColor(stepNo, totalSteps, from_, to):
    stes = float(totalSteps) - 1.0
    step = _fdiv(from_ - to, stes)
    return _uint(round(from_ - (step * stepNo)))

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed

# ---- global variables initialised from expressions
ColorFrom = _input('ColorFrom', _uint(Lime))  # Oversold color
ColorTo = _input('ColorTo', _uint(MediumVioletRed))  # Overbought color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DoubleStochastic(_MQL5Indicator):
    name = 'double_stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StochasticPeriod': 55,  # Stochastic period
        'EMAPeriod': 15,  # Smoothing period
        'ColorSteps': 20,  # Color steps for drawing
    }
    y_range = (-1.0, 101.0)

