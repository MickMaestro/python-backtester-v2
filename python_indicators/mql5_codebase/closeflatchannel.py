"""closeflatchannel — converted from MQL5: MQL5 Indicators/Close Flat Channel/closeflatchannel.mq5

Indicator of the flat channel. If the closing of the required number of bars are located
within the maximum width - draw the channel.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16748574], 2: [9639167]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper', 2: 'Lower'}, 'levels': [], 'description': ['Indicator of the flat channel. If the closing of the required number of bars are located', 'within the maximum width - draw the channel.'], 'name': 'closeflatchannel', 'source': 'MQL5 Indicators/Close Flat Channel/closeflatchannel.mq5', 'folder': 'Close Flat Channel', 'inputs': [{'mql': 'InpMaxRange', 'py': 'InpMaxRange', 'param': 'InpMaxRange', 'type': 'int', 'default': 100, 'label': 'Max range between the closing', 'sinput': False}, {'mql': 'InpBarsQuantity', 'py': 'InpBarsQuantity', 'param': 'InpBarsQuantity', 'type': 'int', 'default': 4, 'label': 'Number of bars', 'sinput': False}, {'mql': 'InpIndent', 'py': 'InpIndent', 'param': 'InpIndent', 'type': 'int', 'default': 50, 'label': 'Indent before the channel boundaries', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 1, 'label': 'horizontal shiftи', 'sinput': False}, {'mql': 'InpTakePrev', 'py': 'InpTakePrev', 'param': 'InpTakePrev', 'type': 'bool', 'default': True, 'label': 'consider the previous boundaries', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMaxRange = _input('InpMaxRange', 100)  # Max range between the closing
InpBarsQuantity = _input('InpBarsQuantity', 4)  # Number of bars
InpIndent = _input('InpIndent', 50)  # Indent before the channel boundaries
InpShift = _input('InpShift', 1)  # horizontal shiftи
InpTakePrev = _input('InpTakePrev', True)  # consider the previous boundaries
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
minRequiredBars = 0

def OnInit():
    global minRequiredBars
    minRequiredBars = InpBarsQuantity
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowerBuffer, INDICATOR_DATA)
    for i in range(0, 2):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(i, PLOT_SHIFT, InpShift)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = 'CloseFlatChannel (' + _str(InpMaxRange) + ', ' + _str(InpBarsQuantity) + ', ' + _str(InpIndent) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    return 0

def getArrayMax(array, curIndex, quantity):
    first = curIndex - quantity + 1
    max_ = array[first]
    for bar in range(first + 1, curIndex + 1):
        if array[bar] > max_:
            max_ = array[bar]
    return max_

def getArrayMin(array, curIndex, quantity):
    first = curIndex - quantity + 1
    min_ = array[first]
    for bar in range(first + 1, curIndex + 1):
        if array[bar] < min_:
            min_ = array[bar]
    return min_

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    startBar = 0
    if rates_total < minRequiredBars:
        Print('Not enough bars for the calculation.')
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        startBar = minRequiredBars
    else:
        startBar = prev_calculated - 1
    for bar in range(startBar, rates_total):
        maxClose = getArrayMax(close, bar, InpBarsQuantity)
        minClose = getArrayMin(close, bar, InpBarsQuantity)
        if (maxClose - minClose) <= (InpMaxRange * Point()):
            prevBar = bar - 1
            UpperBuffer[bar] = getArrayMax(high, bar, InpBarsQuantity) + ((spread[bar] + InpIndent) * Point())
            LowerBuffer[bar] = getArrayMin(low, bar, InpBarsQuantity) - (InpIndent * Point())
            if InpTakePrev:
                if UpperBuffer[prevBar] != 0.0 or LowerBuffer[prevBar] != 0.0:
                    UpperBuffer[bar] = MathMax(UpperBuffer[prevBar], high[bar] + ((spread[bar] + InpIndent) * Point()))
                    LowerBuffer[bar] = MathMin(LowerBuffer[prevBar], low[bar] - (InpIndent * Point()))
        else:
            UpperBuffer[bar] = 0.0
            LowerBuffer[bar] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Closeflatchannel(_MQL5Indicator):
    name = 'closeflatchannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMaxRange': 100,  # Max range between the closing
        'InpBarsQuantity': 4,  # Number of bars
        'InpIndent': 50,  # Indent before the channel boundaries
        'InpShift': 1,  # horizontal shiftи
        'InpTakePrev': True,  # consider the previous boundaries
    }

