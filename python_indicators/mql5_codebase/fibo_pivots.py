"""Fibo pivots — converted from MQL5: MQL5 Indicators/Fibo Pivots/Fibo pivots.mq5

Fibo pivots
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Fibo pivots'], 'name': 'Fibo pivots', 'source': 'MQL5 Indicators/Fibo Pivots/Fibo pivots.mq5', 'folder': 'Fibo Pivots', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 16408, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpLevels', 'py': 'inpLevels', 'param': None, 'type': 'string', 'default': '0.382;0.618;1', 'label': 'Levels', 'sinput': False}, {'mql': 'inpPivot', 'py': 'inpPivot', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Pivot color', 'sinput': False}, {'mql': 'inpFiboUp', 'py': 'inpFiboUp', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Upper fibo level', 'sinput': False}, {'mql': 'inpFiboDown', 'py': 'inpFiboDown', 'param': None, 'type': 'color', 'default': 6333684, 'label': 'Lower fibo level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
inpTimeFrame = _input('inpTimeFrame', tf_d1)  # Time frame
inpLevels = _input('inpLevels', '0.382;0.618;1')  # Levels
inpPivot = _input('inpPivot', clrGray)  # Pivot color
inpFiboUp = _input('inpFiboUp', clrDodgerBlue)  # Upper fibo level
inpFiboDown = _input('inpFiboDown', clrSandyBrown)  # Lower fibo level
_levels = Arr(0, 0.0)
_levelsSize = 0
timeFrame = 0
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _levelsSize, timeFrame
    timeFrame = MathMax(timeFrameGet(inpTimeFrame), Period())
    _sep = StringGetCharacter(';', 0)
    _levelsStrings = Arr(0, "")
    _levelsSize = StringSplit(inpLevels, _sep, _levelsStrings)
    ArrayResize(_levels, _levelsSize)
    for i in range(0, _levelsSize):
        _levels[i] = StringToDouble(_levelsStrings[i])
    if _levelsSize <= 0:
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'fibo pivots:')
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _prevMark = 0
    _seconds = PeriodSeconds(timeFrame)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _currMark = _int(_idiv(time[i], _seconds))
        if _currMark != _prevMark:
            _prevMark = _currMark
            _rates = Arr(2, 0, dyn=False, factory=MqlRates)
            _copiedRates = CopyRates(Symbol(), timeFrame, _DT(time[i]), 2, _rates)
            if _copiedRates == 2:
                pivot = (_rates[0].high + _rates[0].low + _rates[1].open) / 3
                range_ = _rates[0].high - _rates[0].low
                _namep = 'fibo pivots:' + _str(_rates[0].time) + ':p'
                ObjectDelete(0, _namep)
                ObjectCreate(0, _namep, OBJ_TREND, 0, _rates[1].time, pivot, _rates[1].time + _seconds, pivot)
                ObjectSetInteger(0, _namep, OBJPROP_COLOR, inpPivot)
                ObjectSetInteger(0, _namep, OBJPROP_WIDTH, 1)
                ObjectSetInteger(0, _namep, OBJPROP_STYLE, STYLE_DOT)
                for k in range(0, _levelsSize):
                    _nameu = 'fibo pivots:' + _str(_rates[0].time) + ':u' + _str(k)
                    _named = 'fibo pivots:' + _str(_rates[0].time) + ':d' + _str(k)
                    ObjectDelete(0, _nameu)
                    ObjectDelete(0, _named)
                    ObjectCreate(0, _nameu, OBJ_TREND, 0, _rates[1].time, pivot + (range_ * _levels[k]), _rates[1].time + _seconds, pivot + (range_ * _levels[k]))
                    ObjectSetInteger(0, _nameu, OBJPROP_COLOR, inpFiboUp)
                    ObjectSetInteger(0, _nameu, OBJPROP_WIDTH, 1)
                    ObjectCreate(0, _named, OBJ_TREND, 0, _rates[1].time, pivot - (range_ * _levels[k]), _rates[1].time + _seconds, pivot - (range_ * _levels[k]))
                    ObjectSetInteger(0, _named, OBJPROP_COLOR, inpFiboDown)
                    ObjectSetInteger(0, _named, OBJPROP_WIDTH, 1)
        i += 1
    return i

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsStr[i]

def timeFrameGet(period):
    _shift = (MathAbs(period) if (period < 0) else 0)
    if _shift > 0 or period == tf_cu:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsPer[MathMin(i + _shift, ArraySize(_tfsPer) - 1)]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FiboPivots(_MQL5Indicator):
    name = 'Fibo pivots'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=16408),  # Time frame
    }

