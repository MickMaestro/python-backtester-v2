"""x-bars_fractals — converted from MQL5: MQL5 Indicators/X-bars Fractals/x-bars_fractals.mq5

The indicator allows to separately set the number of bars from the left and right of the fractal. Well suited 
to define local and global extremums.
Copyright: Copyright 2011, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16748574], 2: [4678655]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Up Fractals', 2: 'Down Fractals'}, 'levels': [], 'description': ['The indicator allows to separately set the number of bars from the left and right of the fractal. Well suited ', 'to define local and global extremums.'], 'name': 'x-bars_fractals', 'source': 'MQL5 Indicators/X-bars Fractals/x-bars_fractals.mq5', 'folder': 'X-bars Fractals', 'inputs': [{'mql': 'InpLeftSide', 'py': 'InpLeftSide', 'param': 'InpLeftSide', 'type': 'int', 'default': 3, 'label': 'Number of bars from the left of fractal', 'sinput': False}, {'mql': 'InpRightSide', 'py': 'InpRightSide', 'param': 'InpRightSide', 'type': 'int', 'default': 3, 'label': 'Number of bars from the right of fractal', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpLeftSide = _input('InpLeftSide', 3)  # Number of bars from the left of fractal
InpRightSide = _input('InpRightSide', 3)  # Number of bars from the right of fractal
UpFractalsBuffer = Arr(0, 0.0)
DnFractalsBuffer = Arr(0, 0.0)
minRequiredBars = 0
leftSide = 0
rightSide = 0
maxSide = 0

def OnInit():
    global leftSide, maxSide, minRequiredBars, rightSide
    if InpLeftSide < 1:
        leftSide = 2
        printf('The "Number of bars from the left of fractal" parameter is specified incorrectly: %d. the: %d. value will be used', InpLeftSide, leftSide)
    else:
        leftSide = InpLeftSide
    if InpRightSide < 1:
        rightSide = 2
        printf('The "Number of bars from the right of fractal" parameter is specified incorrectly: %d. the: %d. value will be used', InpRightSide, rightSide)
    else:
        rightSide = InpRightSide
    minRequiredBars = leftSide + rightSide + 1
    maxSide = MathMax(leftSide, rightSide)
    SetIndexBuffer(0, UpFractalsBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnFractalsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 217)
    PlotIndexSetInteger(1, PLOT_ARROW, 218)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, 10)
    for i in range(0, 2):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'X-bars Fractals (' + _str(leftSide) + ', ' + _str(rightSide) + ')')
    return 0

def isUpFractal(bar, max_, High):
    for i in range(1, max_ + 1):
        if i <= leftSide and High[bar] < High[bar - i]:
            return False
        if i <= rightSide and High[bar] <= High[bar + i]:
            return False
    return True

def isDnFractal(bar, max_, Low):
    for i in range(1, max_ + 1):
        if i <= leftSide and Low[bar] > Low[bar - i]:
            return False
        if i <= rightSide and Low[bar] >= Low[bar + i]:
            return False
    return True

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    startBar = 0
    lastBar = 0
    if rates_total < minRequiredBars:
        Print('Not enough data to calculate')
        return 0
    if prev_calculated < minRequiredBars:
        startBar = leftSide
        ArrayInitialize(UpFractalsBuffer, 0.0)
        ArrayInitialize(DnFractalsBuffer, 0.0)
    else:
        startBar = rates_total - minRequiredBars
    lastBar = rates_total - rightSide
    for bar in range(startBar, lastBar):
        if isUpFractal(bar, maxSide, high):
            UpFractalsBuffer[bar] = high[bar]
        else:
            UpFractalsBuffer[bar] = 0.0
        if isDnFractal(bar, maxSide, low):
            DnFractalsBuffer[bar] = low[bar]
        else:
            DnFractalsBuffer[bar] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XBarsFractals(_MQL5Indicator):
    name = 'x-bars_fractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpLeftSide': 3,  # Number of bars from the left of fractal
        'InpRightSide': 3,  # Number of bars from the right of fractal
    }

