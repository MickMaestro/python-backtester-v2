"""Blau_-_T3_ergodic_candlestick_oscillator_1.02 — converted from MQL5: MQL5 Indicators/Blau T3 ECO/Blau_-_T3_ergodic_candlestick_oscillator_1.02.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 1}, 'colors': {1: [14546909, 14804223], 2: [3329330, 9662683], 3: [9662683]}, 'widths': {2: 2, 3: 1}, 'styles': {2: 0, 3: 2}, 'labels': {1: 'eco trend', 2: 'eco', 3: 'eco signal'}, 'levels': [], 'description': [], 'name': 'Blau_-_T3_ergodic_candlestick_oscillator_1.02', 'source': 'MQL5 Indicators/Blau T3 ECO/Blau_-_T3_ergodic_candlestick_oscillator_1.02.mq5', 'folder': 'Blau T3 ECO', 'inputs': [{'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'double', 'default': 32.0, 'label': 'T3 period no.1', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'double', 'default': 5.0, 'label': 'T3 period no.2', 'sinput': False}, {'mql': 'Period3', 'py': 'Period3', 'param': 'Period3', 'type': 'double', 'default': 5.0, 'label': 'T3 signal line period', 'sinput': False}, {'mql': 'Hot', 'py': 'Hot', 'param': 'Hot', 'type': 'double', 'default': 0.4, 'label': 'T3 hot', 'sinput': False}, {'mql': 'Original', 'py': 'Original', 'param': 'Original', 'type': 'bool', 'default': False, 'label': 'T3 original Tim Tillson calculation', 'sinput': False}, {'mql': 'ColorOnSlope', 'py': 'ColorOnSlope', 'param': 'ColorOnSlope', 'type': 'int', 'default': 1, 'label': 'Color based on :', 'sinput': False}, {'mql': 'DisplayStyle', 'py': 'DisplayStyle', 'param': 'DisplayStyle', 'type': 'int', 'default': 1, 'label': 'Display style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enStyle
dis_tape = 0
dis_zero = 1
dis_line = 2
_enum('enStyle', {0: 'dis_tape', 1: 'dis_zero', 2: 'dis_line'})

# enum enColors
cl_onSlope = 0
cl_onZero = 1
_enum('enColors', {0: 'cl_onSlope', 1: 'cl_onZero'})

# ---- inputs and global variables
Period1 = _input('Period1', 32.0)  # T3 period no.1
Period2 = _input('Period2', 5.0)  # T3 period no.2
Period3 = _input('Period3', 5.0)  # T3 signal line period
Hot = _input('Hot', 0.4)  # T3 hot
Original = _input('Original', False)  # T3 original Tim Tillson calculation
ColorOnSlope = _input('ColorOnSlope', cl_onZero)  # Color based on :
DisplayStyle = _input('DisplayStyle', dis_zero)  # Display style
eco = Arr(0, 0.0)
sig = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
workT3 = Arr(0, 0.0, dims=(30,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, eco, INDICATOR_DATA)
    SetIndexBuffer(3, colorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, sig, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Blau T3 ergodic candlestick oscillator(' + DoubleToString(Period1, 1) + ',' + DoubleToString(Period1, 2) + ',' + DoubleToString(Period3, 1) + ',' + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        co = iT3(iT3(close[i] - open[i], Period1, Hot, Original, i, rates_total, 0), Period2, Hot, Original, i, rates_total, 1)
        hl = iT3(iT3(high[i] - low[i], Period1, Hot, Original, i, rates_total, 2), Period2, Hot, Original, i, rates_total, 3)
        if hl != 0:
            eco[i] = _fdiv(100.0 * co, hl)
        else:
            eco[i] = 0.0
        sig[i] = iT3(eco[i], Period3, Hot, Original, i, rates_total, 4)
        if i > 0:
            colorBuffer[i] = colorBuffer[i - 1]
            if ColorOnSlope == cl_onSlope:
                if eco[i] > eco[i - 1]:
                    colorBuffer[i] = 0.0
                if eco[i] < eco[i - 1]:
                    colorBuffer[i] = 1.0
            else:
                if eco[i] > 0:
                    colorBuffer[i] = 0.0
                if eco[i] < 0:
                    colorBuffer[i] = 1.0
        fill1[i] = EMPTY_VALUE
        fill2[i] = EMPTY_VALUE
        _sw1 = DisplayStyle
        if _sw1 == dis_tape:
            if colorBuffer[i] == 0:
                fill1[i] = MathMax(eco[i], sig[i])
                fill2[i] = MathMin(eco[i], sig[i])
            if colorBuffer[i] == 1:
                fill1[i] = MathMin(eco[i], sig[i])
                fill2[i] = MathMax(eco[i], sig[i])
        elif _sw1 == dis_zero:
            if ColorOnSlope == cl_onSlope:
                if colorBuffer[i] == 0 and eco[i] > 0:
                    fill1[i] = eco[i]
                    fill2[i] = 0.0
                if colorBuffer[i] == 0 and eco[i] < 0:
                    fill2[i] = eco[i]
                    fill1[i] = 0.0
                if colorBuffer[i] == 1 and eco[i] > 0:
                    fill2[i] = eco[i]
                    fill1[i] = 0.0
                if colorBuffer[i] == 1 and eco[i] < 0:
                    fill1[i] = eco[i]
                    fill2[i] = 0.0
            else:
                fill1[i] = MathMax(eco[i], 0)
                fill2[i] = MathMin(eco[i], 0)
        elif _sw1 == dis_line:
            pass
    return rates_total

def iT3(price, period, hot, original, r, total, instanceNo=0):
    if ArrayRange(workT3, 0) != total:
        ArrayResize(workT3, total)
    if ArrayRange(workT3Coeffs, 0) < (instanceNo + 1):
        ArrayResize(workT3Coeffs, instanceNo + 1)
    if workT3Coeffs[instanceNo][0] != period:
        workT3Coeffs[instanceNo][0] = period
        a = hot
        workT3Coeffs[instanceNo][1] = (-a) * a * a
        workT3Coeffs[instanceNo][2] = (3 * a * a) + (3 * a * a * a)
        workT3Coeffs[instanceNo][3] = (-6 * a * a) - (3 * a) - (3 * a * a * a)
        workT3Coeffs[instanceNo][4] = 1 + (3 * a) + (a * a * a) + (3 * a * a)
        if original:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 1.0 + period)
        else:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
    buffer = instanceNo * 6
    if r == 0:
        workT3[r][0 + buffer] = price
        workT3[r][1 + buffer] = price
        workT3[r][2 + buffer] = price
        workT3[r][3 + buffer] = price
        workT3[r][4 + buffer] = price
        workT3[r][5 + buffer] = price
    else:
        workT3[r][0 + buffer] = workT3[r - 1][0 + buffer] + (workT3Coeffs[instanceNo][5] * (price - workT3[r - 1][0 + buffer]))
        workT3[r][1 + buffer] = workT3[r - 1][1 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][0 + buffer] - workT3[r - 1][1 + buffer]))
        workT3[r][2 + buffer] = workT3[r - 1][2 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][1 + buffer] - workT3[r - 1][2 + buffer]))
        workT3[r][3 + buffer] = workT3[r - 1][3 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][2 + buffer] - workT3[r - 1][3 + buffer]))
        workT3[r][4 + buffer] = workT3[r - 1][4 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][3 + buffer] - workT3[r - 1][4 + buffer]))
        workT3[r][5 + buffer] = workT3[r - 1][5 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][4 + buffer] - workT3[r - 1][5 + buffer]))
    return (workT3Coeffs[instanceNo][1] * workT3[r][5 + buffer]) + (workT3Coeffs[instanceNo][2] * workT3[r][4 + buffer]) + (workT3Coeffs[instanceNo][3] * workT3[r][3 + buffer]) + (workT3Coeffs[instanceNo][4] * workT3[r][2 + buffer])


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauT3ErgodicCandlestickOscillator102(_MQL5Indicator):
    name = 'Blau_-_T3_ergodic_candlestick_oscillator_1.02'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period1': 32.0,  # T3 period no.1
        'Period2': 5.0,  # T3 period no.2
        'Period3': 5.0,  # T3 signal line period
        'Hot': 0.4,  # T3 hot
        'Original': False,  # T3 original Tim Tillson calculation
        'ColorOnSlope': _Choice({0: 'Color based on the slope of the oscillator', 1: 'Color based on zero cross'}, default=1),  # Color based on :
        'DisplayStyle': _Choice({0: 'Display as tape', 1: 'Display as zero based zone', 2: 'Display as lines'}, default=1),  # Display style
    }

