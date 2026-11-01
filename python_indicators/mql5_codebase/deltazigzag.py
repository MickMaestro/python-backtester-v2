"""deltazigzag — converted from MQL5: MQL5 Indicators/Delta ZigZag/deltazigzag.mq5

Delta ZigZag determines a reversal by the minimal height of swing, and also identifies 
a trend by breakthrough of the local minimum/maximum levels and colors 
the zigzag sections to the current trend color.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 13, 2: 5, 3: 5}, 'colors': {1: [255, 16711680], 2: [16748574], 3: [4678655]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'ZigZag Bottom;ZigZag Top', 2: 'Reverse to Down', 3: 'Reverse to Up'}, 'levels': [], 'description': ['Delta ZigZag determines a reversal by the minimal height of swing, and also identifies ', 'a trend by breakthrough of the local minimum/maximum levels and colors ', 'the zigzag sections to the current trend color.'], 'name': 'deltazigzag', 'source': 'MQL5 Indicators/Delta ZigZag/deltazigzag.mq5', 'folder': 'Delta ZigZag', 'inputs': [{'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Apply to price', 'sinput': False}, {'mql': 'InpReversalMode', 'py': 'InpReversalMode', 'param': 'InpReversalMode', 'type': 'int', 'default': 0, 'label': 'Reversal mode', 'sinput': False}, {'mql': 'InpPips', 'py': 'InpPips', 'param': 'InpPips', 'type': 'int', 'default': 500, 'label': 'Reversal in pips', 'sinput': False}, {'mql': 'InpPercent', 'py': 'InpPercent', 'param': 'InpPercent', 'type': 'double', 'default': 0.5, 'label': 'Reversal in %', 'sinput': False}, {'mql': 'InpLevels', 'py': 'InpLevels', 'param': 'InpLevels', 'type': 'int', 'default': 1, 'label': 'Levels number', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum APPLIED_PRICE
CLOSE_CLOSE = 0
HIGH_LOW = 1
_enum('APPLIED_PRICE', {0: 'CLOSE_CLOSE', 1: 'HIGH_LOW'})

# enum REVERSAL_MODE
PIPS = 0
PERCENT = 1
_enum('REVERSAL_MODE', {0: 'PIPS', 1: 'PERCENT'})

# ---- inputs and global variables
InpAppliedPrice = _input('InpAppliedPrice', HIGH_LOW)  # Apply to price
InpReversalMode = _input('InpReversalMode', PIPS)  # Reversal mode
InpPips = _input('InpPips', 500)  # Reversal in pips
InpPercent = _input('InpPercent', 0.5)  # Reversal in %
InpLevels = _input('InpLevels', 1)  # Levels number
ZzBtmBuffer = Arr(0, 0.0)
ZzTopBuffer = Arr(0, 0.0)
ZigZagColors = Arr(0, 0.0)
ReverseToDownBuffer = Arr(0, 0.0)
ReverseToUpBuffer = Arr(0, 0.0)
minLevels = Arr(0, 0.0)
maxLevels = Arr(0, 0.0)

class zzData(MqlObject):
    _q_fields = ('highBar', 'lowBar', 'highValue', 'lowValue', 'up')
    def __init__(self, *args):
        self.highBar = 0
        self.lowBar = 0
        self.highValue = 0.0
        self.lowValue = 0.0
        self.up = False

def OnInit():
    SetIndexBuffer(0, ZzBtmBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ZzTopBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ZigZagColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, ReverseToUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ReverseToDownBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    for i in range(0, 3):
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
    ArrayResize(minLevels, InpLevels)
    ArrayResize(maxLevels, InpLevels)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    modeData = ((_str(InpPips) + ' pips') if (InpReversalMode == PIPS) else (DoubleToString(InpPercent, 2) + '%'))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Delta ZigZag (' + modeData + ', ' + _str(InpLevels) + ')')
    return 0

def getReversal(price):
    if InpReversalMode == PIPS:
        return InpPips * Point()
    return NormalizeDouble((price / 100) * InpPercent, Digits())

def addLevelToArray(array, price):
    for i in range(InpLevels - 1, 1 - 1, -1):
        array[i] = array[i - 1]
    array[0] = price

def arrayMaxValue(array):
    max_ = array[0]
    for i in range(InpLevels - 1, 0, -1):
        if array[i] > max_:
            max_ = array[i]
    return max_

def arrayMinValue(array):
    min_ = array[0]
    for i in range(InpLevels - 1, 0, -1):
        if array[i] < min_:
            min_ = array[i]
    return min_

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate__upTrend, last
    startBar = 0
    lastBar = 0
    upTrend = False
    reversal = 0.0
    current = zzData()
    lastBar = rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        ArrayInitialize(ZzBtmBuffer, 0.0)
        ArrayInitialize(ZzTopBuffer, 0.0)
        ArrayInitialize(ZigZagColors, 0.0)
        ArrayInitialize(ReverseToUpBuffer, 0.0)
        ArrayInitialize(ReverseToDownBuffer, 0.0)
        reversal = getReversal(close[0])
        startBar = 1
        while (MathAbs(close[startBar] - close[0]) - reversal) <= 1e-05:
            pass
            startBar += 1
        if close[startBar] > close[0]:
            _s_OnCalculate__upTrend = True
            last.up = _s_OnCalculate__upTrend
            last.highBar = startBar
            last.lowBar = 0
            ZzTopBuffer[startBar] = close[startBar]
            last.highValue = ZzTopBuffer[startBar]
            ZzBtmBuffer[0] = close[0]
            last.lowValue = ZzBtmBuffer[0]
        else:
            _s_OnCalculate__upTrend = False
            last.up = _s_OnCalculate__upTrend
            last.highBar = 0
            ZzTopBuffer[0] = close[0]
            last.highValue = ZzTopBuffer[0]
            last.lowBar = startBar
            ZzBtmBuffer[startBar] = close[startBar]
            last.lowValue = ZzBtmBuffer[startBar]
        ArrayInitialize(minLevels, last.lowValue)
        ArrayInitialize(maxLevels, last.highValue)
    else:
        startBar = prev_calculated - 1
        ZzBtmBuffer[lastBar] = 0.0
        ZzTopBuffer[lastBar] = 0.0
        ZzBtmBuffer[last.lowBar] = last.lowValue
        ZzTopBuffer[last.highBar] = last.highValue
    _assign(current, last)
    upTrend = _s_OnCalculate__upTrend
    for bar in range(startBar, rates_total):
        curLow = 0.0
        curHigh = 0.0
        if InpAppliedPrice == HIGH_LOW:
            curLow = low[bar]
            curHigh = high[bar]
        else:
            curHigh = close[bar]
            curLow = curHigh
        if rates_total != prev_calculated and bar == lastBar:
            _assign(last, current)
            _s_OnCalculate__upTrend = upTrend
            if (current.up and ZzTopBuffer[bar - 1] != 0.0) and minLevels[0] != current.lowValue:
                addLevelToArray(minLevels, current.lowValue)
            if ((not current.up) and ZzBtmBuffer[bar - 1] != 0.0) and maxLevels[0] != current.highValue:
                addLevelToArray(maxLevels, current.highValue)
        if current.up:
            reversal = getReversal(current.highValue)
            if curHigh > current.highValue:
                ZzTopBuffer[current.highBar] = 0.0
                ZzTopBuffer[bar] = curHigh
                ZzBtmBuffer[bar] = 0.0
                current.highBar = bar
                current.highValue = curHigh
            else:
                if curLow < (current.highValue - reversal):
                    ZzBtmBuffer[bar] = curLow
                    current.lowBar = bar
                    current.lowValue = curLow
                    ZzTopBuffer[bar] = 0.0
                    current.up = False
                    if bar != lastBar and maxLevels[0] != current.highValue:
                        addLevelToArray(maxLevels, current.highValue)
                else:
                    ZzBtmBuffer[bar] = 0.0
                    ZzTopBuffer[bar] = 0.0
        else:
            reversal = getReversal(current.lowValue)
            if curLow < current.lowValue:
                ZzBtmBuffer[current.lowBar] = 0.0
                ZzBtmBuffer[bar] = curLow
                ZzTopBuffer[bar] = 0.0
                current.lowBar = bar
                current.lowValue = curLow
            else:
                if curHigh > (current.lowValue + reversal):
                    ZzTopBuffer[bar] = curHigh
                    current.highBar = bar
                    current.highValue = curHigh
                    ZzBtmBuffer[bar] = 0.0
                    current.up = True
                    if bar != lastBar and minLevels[0] != current.lowValue:
                        addLevelToArray(minLevels, current.lowValue)
                else:
                    ZzBtmBuffer[bar] = 0.0
                    ZzTopBuffer[bar] = 0.0
        if (not upTrend) and current.highValue > arrayMaxValue(maxLevels):
            upTrend = True
        elif upTrend and current.lowValue < arrayMinValue(minLevels):
            upTrend = False
        if upTrend:
            ReverseToDownBuffer[bar] = arrayMinValue(minLevels)
            ReverseToUpBuffer[bar] = 0.0
            ZigZagColors[bar] = 1.0
        else:
            ReverseToDownBuffer[bar] = 0.0
            ReverseToUpBuffer[bar] = arrayMaxValue(maxLevels)
            ZigZagColors[bar] = 0.0
    return rates_total

# ---- global variables initialised from expressions
last = _alloc(zzData)
last.__init__()

# ---- static local variables
_s_OnCalculate__upTrend = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Deltazigzag(_MQL5Indicator):
    name = 'deltazigzag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpAppliedPrice': _Choice({0: 'close', 1: 'high/low'}, default=1),  # Apply to price
        'InpReversalMode': _Choice({0: 'In pips', 1: 'In percentage'}, default=0),  # Reversal mode
        'InpPips': 500,  # Reversal in pips
        'InpPercent': 0.5,  # Reversal in %
        'InpLevels': 1,  # Levels number
    }

