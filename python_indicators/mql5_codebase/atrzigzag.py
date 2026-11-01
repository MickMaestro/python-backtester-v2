"""ATRZigZag — converted from MQL5: MQL5 Indicators/ATR ZigZag/ATRZigZag.mq5

ATR-based ZigZag implementation.
Copyright: Copyright 2018, Andre S. Enger.; Link: andre_enger@hotmail.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, Andre S. Enger.', 'link': 'andre_enger@hotmail.com', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [3329434]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Zig Zag'}, 'levels': [], 'description': ['ATR-based ZigZag implementation.'], 'name': 'ATRZigZag', 'source': 'MQL5 Indicators/ATR ZigZag/ATRZigZag.mq5', 'folder': 'ATR ZigZag', 'inputs': [{'mql': 'AtrMultiplier', 'py': 'AtrMultiplier', 'param': 'AtrMultiplier', 'type': 'double', 'default': 1.5, 'label': 'ATR threshold for directional change', 'sinput': False}, {'mql': 'AtrPeriod', 'py': 'AtrPeriod', 'param': 'AtrPeriod', 'type': 'int', 'default': 50, 'label': 'Period for ATR calculation', 'sinput': False}, {'mql': 'MaxPeriod', 'py': 'MaxPeriod', 'param': 'MaxPeriod', 'type': 'int', 'default': 10, 'label': 'Max bar period before directional change', 'sinput': False}, {'mql': 'MinPeriod', 'py': 'MinPeriod', 'param': 'MinPeriod', 'type': 'int', 'default': 3, 'label': 'Min bar period before directional change', 'sinput': False}, {'mql': 'RealTimeMode', 'py': 'RealTimeMode', 'param': 'RealTimeMode', 'type': 'bool', 'default': True, 'label': 'Draw tentative zigzag at newest bar', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AtrMultiplier = _input('AtrMultiplier', 1.5)  # ATR threshold for directional change
AtrPeriod = _input('AtrPeriod', 50)  # Period for ATR calculation
MaxPeriod = _input('MaxPeriod', 10)  # Max bar period before directional change
MinPeriod = _input('MinPeriod', 3)  # Min bar period before directional change
RealTimeMode = _input('RealTimeMode', True)  # Draw tentative zigzag at newest bar
ExtPeaksBuffer = Arr(0, 0.0)
ExtTroughsBuffer = Arr(0, 0.0)
_lastDirection = False
_realtimeChange = False
_lastIndex = 0
_lastIndex2 = 0
_contraIndex = 0
_atr = 0.0

def OnInit():
    SetIndexBuffer(0, ExtPeaksBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTroughsBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _atr, _contraIndex, _lastDirection, _lastIndex, _lastIndex2, _realtimeChange
    start = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        start = 1
        _lastIndex = 0
        _lastIndex2 = 0
        _contraIndex = 0
        _atr = 0.0
        _realtimeChange = False
    else:
        start = MathMax(1, prev_calculated - 1)
    atr = _atr
    bar = start
    while bar < (rates_total - (0 if RealTimeMode else 1)):
        realtimeBar = bar == (rates_total - 1)
        if not realtimeBar:
            tr = MathMax(high[bar], close[bar - 1]) - MathMin(low[bar], close[bar - 1])
            atr += (tr - atr) * _fdiv(2.0, 1.0 + AtrPeriod)
            _atr = atr
            if _realtimeChange and RealTimeMode:
                if _lastDirection:
                    ExtPeaksBuffer[_lastIndex] = high[_lastIndex]
                else:
                    ExtTroughsBuffer[_lastIndex] = low[_lastIndex]
                ExtPeaksBuffer[rates_total - 1] = 0.0
                ExtTroughsBuffer[rates_total - 1] = 0.0
                _realtimeChange = False
            ExtTroughsBuffer[bar] = 0.0
            ExtPeaksBuffer[bar] = 0.0
        shouldntChange = (bar - _lastIndex) < MinPeriod
        shallChange = (bar - _lastIndex) > MaxPeriod
        mustChange = False
        shouldChange = False
        canChange = False
        if _lastDirection:
            mustChange = low[bar] < low[_lastIndex2]
            shouldChange = (ExtPeaksBuffer[_lastIndex] - low[bar]) > (atr * AtrMultiplier)
            canChange = low[bar] < low[_contraIndex]
        else:
            mustChange = high[bar] > high[_lastIndex2]
            shouldChange = (high[bar] - ExtTroughsBuffer[_lastIndex]) > (atr * AtrMultiplier)
            canChange = high[bar] > high[_contraIndex]
        changeNow = mustChange or ((canChange and shouldChange) and (not shouldntChange))
        if realtimeBar and RealTimeMode:
            if _lastDirection:
                if (not _realtimeChange) and high[bar] > ExtPeaksBuffer[_lastIndex]:
                    ExtPeaksBuffer[_lastIndex] = 0.0
                    ExtPeaksBuffer[bar] = high[bar]
                    _realtimeChange = True
                elif _realtimeChange and high[bar] > ExtPeaksBuffer[bar]:
                    ExtPeaksBuffer[bar] = high[bar]
            else:
                if (not _realtimeChange) and low[bar] < ExtTroughsBuffer[_lastIndex]:
                    ExtTroughsBuffer[_lastIndex] = 0.0
                    ExtTroughsBuffer[bar] = low[bar]
                    _realtimeChange = True
                elif _realtimeChange and low[bar] < ExtTroughsBuffer[bar]:
                    ExtTroughsBuffer[bar] = low[bar]
        else:
            if canChange:
                _contraIndex = bar
            if _lastDirection:
                if high[bar] > ExtPeaksBuffer[_lastIndex]:
                    ExtPeaksBuffer[_lastIndex] = 0.0
                    ExtPeaksBuffer[bar] = high[bar]
                    if open[bar] > close[bar]:
                        shouldntChange = 0 < MinPeriod
                        shouldChange = (ExtPeaksBuffer[bar] - low[bar]) > (atr * AtrMultiplier)
                        changeNow = mustChange or ((canChange and shouldChange) and (not shouldntChange))
                        if changeNow:
                            ExtTroughsBuffer[bar] = low[bar]
                            _lastDirection = False
                            _lastIndex2 = bar
                    elif changeNow:
                        ExtPeaksBuffer[_lastIndex] = high[_lastIndex]
                        ExtTroughsBuffer[bar] = low[bar]
                        _lastIndex2 = bar
                    _lastIndex = bar
                    _contraIndex = bar
                elif changeNow:
                    ExtTroughsBuffer[bar] = low[bar]
                    _lastDirection = False
                    _lastIndex2 = _lastIndex
                    _lastIndex = bar
                    _contraIndex = bar
                elif shallChange:
                    startSkip = (0 if (ExtTroughsBuffer[_lastIndex] == 0) else 1)
                    if open[_lastIndex] < close[_lastIndex] and startSkip == 0:
                        startSkip += 1
                    bar = ArrayMinimum(low, _lastIndex + startSkip, bar - _lastIndex - startSkip + 1)
                    ExtTroughsBuffer[bar] = low[bar]
                    _lastDirection = False
                    _lastIndex2 = _lastIndex
                    _lastIndex = bar
                    _contraIndex = bar
            else:
                if low[bar] < ExtTroughsBuffer[_lastIndex]:
                    ExtTroughsBuffer[_lastIndex] = 0.0
                    ExtTroughsBuffer[bar] = low[bar]
                    if open[bar] < close[bar]:
                        shouldntChange = 0 < MinPeriod
                        shouldChange = (high[bar] - ExtTroughsBuffer[bar]) > (atr * AtrMultiplier)
                        changeNow = mustChange or ((canChange and shouldChange) and (not shouldntChange))
                        if changeNow:
                            ExtPeaksBuffer[bar] = high[bar]
                            _lastDirection = True
                            _lastIndex2 = bar
                    elif changeNow:
                        ExtTroughsBuffer[_lastIndex] = low[_lastIndex]
                        ExtPeaksBuffer[bar] = high[bar]
                        _lastIndex2 = bar
                    _lastIndex = bar
                    _contraIndex = bar
                elif changeNow:
                    ExtPeaksBuffer[bar] = high[bar]
                    _lastDirection = True
                    _lastIndex2 = _lastIndex
                    _lastIndex = bar
                    _contraIndex = bar
                elif shallChange:
                    startSkip = (0 if (ExtPeaksBuffer[_lastIndex] == 0) else 1)
                    if open[_lastIndex] > close[_lastIndex] and startSkip == 0:
                        startSkip += 1
                    bar = ArrayMaximum(high, _lastIndex + startSkip, bar - _lastIndex - startSkip + 1)
                    ExtPeaksBuffer[bar] = high[bar]
                    _lastDirection = True
                    _lastIndex2 = _lastIndex
                    _lastIndex = bar
                    _contraIndex = bar
            ExtPeaksBuffer[rates_total - 1] = 0.0
            ExtTroughsBuffer[rates_total - 1] = 0.0
        bar += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRZigZag(_MQL5Indicator):
    name = 'ATRZigZag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'AtrMultiplier': 1.5,  # ATR threshold for directional change
        'AtrPeriod': 50,  # Period for ATR calculation
        'MaxPeriod': 10,  # Max bar period before directional change
        'MinPeriod': 3,  # Min bar period before directional change
        'RealTimeMode': True,  # Draw tentative zigzag at newest bar
    }

