"""StandardDeviationChannel — converted from MQL5: MQL5 Indicators/Standard Deviation Channel MT5/StandardDeviationChannel.mq5

Copyright: Copyright 2017,fxMeter.; Link: https://www.mql5.com/en/users/fxmeter; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2017,fxMeter.', 'link': 'https://www.mql5.com/en/users/fxmeter', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16760576], 2: [16760576], 3: [16760576], 4: [16760576], 5: [16760576]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 2, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'mid', 2: 'top', 3: 'btm', 4: 'top2', 5: 'bmt2'}, 'levels': [], 'description': [], 'name': 'StandardDeviationChannel', 'source': 'MQL5 Indicators/Standard Deviation Channel MT5/StandardDeviationChannel.mq5', 'folder': 'Standard Deviation Channel MT5', 'inputs': [{'mql': 'InputStarBar', 'py': 'InputStarBar', 'param': 'InputStarBar', 'type': 'int', 'default': 0, 'label': 'StarBar', 'sinput': False}, {'mql': 'InputCalcBars', 'py': 'InputCalcBars', 'param': 'InputCalcBars', 'type': 'int', 'default': 120, 'label': 'Bars for Calculation', 'sinput': False}, {'mql': 'f1', 'py': 'f1', 'param': 'f1', 'type': 'double', 'default': 1.0, 'label': 'Inner Channel Multiplier', 'sinput': False}, {'mql': 'f2', 'py': 'f2', 'param': 'f2', 'type': 'double', 'default': 2.0, 'label': 'Outer Channel Multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InputStarBar = _input('InputStarBar', 0)  # StarBar
InputCalcBars = _input('InputCalcBars', 120)  # Bars for Calculation
f1 = _input('f1', 1.0)  # Inner Channel Multiplier
f2 = _input('f2', 2.0)  # Outer Channel Multiplier
midBuffer = Arr(0, 0.0)
topBuffer = Arr(0, 0.0)
btmBuffer = Arr(0, 0.0)
topBuffer2 = Arr(0, 0.0)
btmBuffer2 = Arr(0, 0.0)
sample = Arr(0, 0.0)  # sample data for calculating linear regression
StarBar = 0
CalcBars = 0

def OnInit():
    global CalcBars, StarBar
    SetIndexBuffer(0, midBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, topBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, btmBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, topBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, btmBuffer2, INDICATOR_DATA)
    for i in range(0, 5):
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(midBuffer, True)
    ArraySetAsSeries(topBuffer, True)
    ArraySetAsSeries(btmBuffer, True)
    ArraySetAsSeries(topBuffer2, True)
    ArraySetAsSeries(btmBuffer2, True)
    StarBar = InputStarBar
    CalcBars = InputCalcBars
    if CalcBars < 2:
        CalcBars = 120
    if StarBar < 0:
        StarBar = 0
    ArrayResize(sample, CalcBars)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastTotalBars
    i = 0
    A = Box(0.0)
    B = Box(0.0)
    stdev = 0.0
    if (StarBar + CalcBars) > (rates_total - 1):
        return 0
    if prev_calculated == 0:
        ArrayInitialize(midBuffer, 0.0)
        ArrayInitialize(topBuffer, 0.0)
        ArrayInitialize(btmBuffer, 0.0)
        ArrayInitialize(topBuffer2, 0.0)
        ArrayInitialize(btmBuffer2, 0.0)
    if CopyClose(Symbol(), PERIOD_CURRENT, StarBar, CalcBars, sample) != CalcBars:
        return 0
    CalcAB(sample, CalcBars, A, B)
    i = StarBar
    while i < (StarBar + CalcBars) and i < rates_total:
        midBuffer[i] = (A.v * (StarBar + CalcBars - i - 1)) + B.v
        i += 1
    stdev = GetStdDev(sample, CalcBars)
    i = StarBar
    while i < (StarBar + CalcBars) and i < rates_total:
        topBuffer[i] = midBuffer[i] + (stdev * f1)
        btmBuffer[i] = midBuffer[i] - (stdev * f1)
        topBuffer2[i] = midBuffer[i] + (stdev * f2)
        btmBuffer2[i] = midBuffer[i] - (stdev * f2)
        i += 1
    if i < rates_total and _s_OnCalculate_LastTotalBars != rates_total:
        midBuffer[i] = 0.0
        topBuffer[i] = 0.0
        btmBuffer[i] = 0.0
        topBuffer2[i] = 0.0
        btmBuffer2[i] = 0.0
        _s_OnCalculate_LastTotalBars = rates_total
    return rates_total

def CalcAB(arr, size, a, b):
    a.v = 0.0
    b.v = 0.0
    if size < 2:
        return
    sumxy = 0.0
    sumx = 0.0
    sumy = 0.0
    sumx2 = 0.0
    for i in range(0, size):
        sumxy += i * arr[i]
        sumy += arr[i]
        sumx += i
        sumx2 += i * i
    M = (size * sumx2) - (sumx * sumx)
    if M == 0.0:
        return
    a.v = _fdiv((size * sumxy) - (sumx * sumy), M)
    b.v = _fdiv(sumy - (a.v * sumx), size)

def GetStdDev(arr, size):
    if size < 2:
        return 0.0
    sum_ = 0.0
    for i in range(0, size):
        sum_ = sum_ + arr[i]
    sum_ = _fdiv(sum_, size)
    sum2 = 0.0
    for i in range(0, size):
        sum2 = sum2 + ((arr[i] - sum_) * (arr[i] - sum_))
    sum2 = _fdiv(sum2, size - 1)
    sum2 = MathSqrt(sum2)
    return sum2

# ---- static local variables
_s_OnCalculate_LastTotalBars = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StandardDeviationChannel(_MQL5Indicator):
    name = 'StandardDeviationChannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InputStarBar': 0,  # StarBar
        'InputCalcBars': 120,  # Bars for Calculation
        'f1': 1.0,  # Inner Channel Multiplier
        'f2': 2.0,  # Outer Channel Multiplier
    }

