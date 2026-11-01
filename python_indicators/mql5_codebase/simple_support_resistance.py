"""Simple support resistance — converted from MQL5: MQL5 Indicators/Simple support resistance/Simple support resistance.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 7, 2: 1}, 'colors': {1: [13628367, 13492732], 2: [11119017]}, 'widths': {}, 'styles': {}, 'labels': {1: 'filling', 2: 'Value'}, 'levels': [], 'description': [], 'name': 'Simple support resistance', 'source': 'MQL5 Indicators/Simple support resistance/Simple support resistance.mq5', 'folder': 'Simple support resistance', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': -1, 'label': 'Time frame', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enTimeFrames
tf_cu = 0
tf_m1 = 1
tf_m2 = 2
tf_m3 = 3
tf_m4 = 4
tf_m5 = 5
tf_m6 = 6
tf_m10 = 10
tf_m12 = 12
tf_m15 = 15
tf_m20 = 20
tf_m30 = 30
tf_h1 = 16385
tf_h2 = 16386
tf_h3 = 16387
tf_h4 = 16388
tf_h6 = 16390
tf_h8 = 16392
tf_h12 = 16396
tf_d1 = 16408
tf_w1 = 32769
tf_mn = 49153
tf_cp1 = -1
tf_cp2 = -2
tf_cp3 = -3
_enum('enTimeFrames', {0: 'tf_cu', 1: 'tf_m1', 2: 'tf_m2', 3: 'tf_m3', 4: 'tf_m4', 5: 'tf_m5', 6: 'tf_m6', 10: 'tf_m10', 12: 'tf_m12', 15: 'tf_m15', 20: 'tf_m20', 30: 'tf_m30', 16385: 'tf_h1', 16386: 'tf_h2', 16387: 'tf_h3', 16388: 'tf_h4', 16390: 'tf_h6', 16392: 'tf_h8', 16396: 'tf_h12', 16408: 'tf_d1', 32769: 'tf_w1', 49153: 'tf_mn', -1: 'tf_cp1', -2: 'tf_cp2', -3: 'tf_cp3'})

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', tf_cp1)  # Time frame
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
val = Arr(0, 0.0)
hh = Arr(0, 0.0)
ll = Arr(0, 0.0)
_indicatorTimeFrame = 0
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _indicatorTimeFrame
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, hh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ll, INDICATOR_CALCULATIONS)
    _indicatorTimeFrame = MathMax(Period(), timeFrameGet(inpTimeFrame))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _currentBar = iBarShift(Symbol(), _indicatorTimeFrame, time[i])
        if _currentBar < 0:
            break
        if i == 0 or _currentBar != iBarShift(Symbol(), _indicatorTimeFrame, time[i - 1]):
            hh[i] = high[i]
            ll[i] = low[i]
        else:
            hh[i] = (high[i] if (high[i] > hh[i - 1]) else hh[i - 1])
            ll[i] = (low[i] if (low[i] < ll[i - 1]) else ll[i - 1])
        _middle = (hh[i] + ll[i]) / 2.0
        val[i] = _middle
        fup[i] = (low[i] if (high[i] > _middle) else high[i] if (low[i] < _middle) else fup[i - 1] if (i > 0) else close[i])
        fdn[i] = _middle
        i += 1
    return i

def timeFrameGet(period):
    _size = ArraySize(_tfsPer)
    _shift = (MathAbs(period) if (period < 0) else 0)
    if period <= 0:
        period = Period()
    i = 0
    i = 0
    for i in range(i, _size):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, _size, 1)
    return _tfsPer[MathMin(i + _shift, _size - 1)]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimpleSupportResistance(_MQL5Indicator):
    name = 'Simple support resistance'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=-1),  # Time frame
    }

