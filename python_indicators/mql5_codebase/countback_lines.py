"""Countback lines — converted from MQL5: MQL5 Indicators/Count Back Lines/Countback lines.mq5

Countback lines
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16760576], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Hi', 2: 'Low'}, 'levels': [], 'description': ['Countback lines'], 'name': 'Countback lines', 'source': 'MQL5 Indicators/Count Back Lines/Countback lines.mq5', 'folder': 'Count Back Lines', 'inputs': [{'mql': 'inpCblPeriod', 'py': 'inpCblPeriod', 'param': 'inpCblPeriod', 'type': 'int', 'default': 13, 'label': 'Countback lines period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpCblPeriod = _input('inpCblPeriod', 13)  # Countback lines period
cblu = Arr(0, 0.0)
cbld = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, cblu, INDICATOR_DATA)
    SetIndexBuffer(1, cbld, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Countback lines (' + _str(inpCblPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _start = MathMax(i - inpCblPeriod + 1, 0)
        hi = high[ArrayMaximum(high, _start, inpCblPeriod)]
        lo = low[ArrayMinimum(low, _start, inpCblPeriod)]
        cblu[i] = (cblu[i - 1] if (i > 0) else lo)
        while True:
            if high[i] < hi:
                break
            if checkLowStrict(2, i, low) and checkLowRef(2, i, low):
                cblu[i] = low[i - 2]
                break
            if checkLowStrict(3, i, low) and checkLowRef(3, i, low):
                cblu[i] = low[i - 3]
                break
            if checkLowStrict(4, i, low) and checkLowRef(4, i, low):
                cblu[i] = low[i - 4]
                break
            if checkLowStrict(5, i, low) and checkLowRef(5, i, low):
                cblu[i] = low[i - 5]
                break
            break
        cbld[i] = (cbld[i - 1] if (i > 0) else hi)
        while True:
            if low[i] > lo:
                break
            if checkHighStrict(2, i, high) and checkHighRef(2, i, high):
                cbld[i] = high[i - 2]
                break
            if checkHighStrict(3, i, high) and checkHighRef(3, i, high):
                cbld[i] = high[i - 3]
                break
            if checkHighStrict(4, i, high) and checkHighRef(4, i, high):
                cbld[i] = high[i - 4]
                break
            if checkHighStrict(5, i, high) and checkHighRef(5, i, high):
                cbld[i] = high[i - 5]
                break
            break
        i += 1
    return i

def checkLowStrict(count, i, low):
    k = count - 1
    while (k >= 0 and (i - k) >= 0) and (i - count) >= 0:
        if low[i - count] >= low[i - k]:
            break
        k -= 1
    return k == -1

def checkLowRef(count, i, low):
    k = count - 1
    while k > 0 and (i - k) >= 0:
        if low[i - k] < low[i]:
            break
        k -= 1
    return k > 0

def checkHighStrict(count, i, high):
    k = count - 1
    while (k >= 0 and (i - k) >= 0) and (i - count) >= 0:
        if high[i - count] <= high[i - k]:
            break
        k -= 1
    return k == -1

def checkHighRef(count, i, high):
    k = count - 1
    while k > 0 and (i - k) >= 0:
        if high[i - k] > high[i]:
            break
        k -= 1
    return k > 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CountbackLines(_MQL5Indicator):
    name = 'Countback lines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCblPeriod': 13,  # Countback lines period
    }

