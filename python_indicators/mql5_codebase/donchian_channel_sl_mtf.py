"""Donchian channel (sl)(mtf) — converted from MQL5: MQL5 Indicators/Donchian channel - extended, multi time frame version/Donchian channel (sl)(mtf).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [14478300], 2: [14474475], 3: [7451452], 4: [7451452], 5: [17919], 6: [17919]}, 'widths': {}, 'styles': {4: 2, 6: 2}, 'labels': {1: 'High fill', 2: 'Low fill', 3: 'Highest high', 4: 'Lowest high', 5: 'Lowest low', 6: 'Highest low'}, 'levels': [], 'description': [], 'name': 'Donchian channel (sl)(mtf)', 'source': 'MQL5 Indicators/Donchian channel - extended, multi time frame version/Donchian channel (sl)(mtf).mq5', 'folder': 'Donchian channel - extended, multi time frame version', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpChannelPeriod', 'py': 'inpChannelPeriod', 'param': 'inpChannelPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'int', 'default': 1, 'label': 'Interpolation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

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

# enum enIterpolate
interolate_yes = 1
interolate_no = 0
_enum('enIterpolate', {1: 'interolate_yes', 0: 'interolate_no'})

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', tf_cu)  # Time frame
inpChannelPeriod = _input('inpChannelPeriod', 20)  # Period
inpInterpolate = _input('inpInterpolate', interolate_yes)  # Interpolation
valuu = Arr(0, 0.0)
valud = Arr(0, 0.0)
valdd = Arr(0, 0.0)
valdu = Arr(0, 0.0)
filluu = Arr(0, 0.0)
fillud = Arr(0, 0.0)
filldd = Arr(0, 0.0)
filldu = Arr(0, 0.0)
count = Arr(0, 0.0)
ª_mtfHandle = 0
_indicatorTimeFrame = 0
_indicatorName = ""
_indicatorShortName = ""
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _indicatorName, _indicatorTimeFrame, ª_mtfHandle
    SetIndexBuffer(0, filluu, INDICATOR_DATA)
    SetIndexBuffer(1, fillud, INDICATOR_DATA)
    SetIndexBuffer(2, filldu, INDICATOR_DATA)
    SetIndexBuffer(3, filldd, INDICATOR_DATA)
    SetIndexBuffer(4, valuu, INDICATOR_DATA)
    SetIndexBuffer(5, valud, INDICATOR_DATA)
    SetIndexBuffer(6, valdd, INDICATOR_DATA)
    SetIndexBuffer(7, valdu, INDICATOR_DATA)
    SetIndexBuffer(8, count, INDICATOR_CALCULATIONS)
    _indicatorTimeFrame = MathMax(Period(), timeFrameGet(inpTimeFrame))
    if _indicatorTimeFrame != Period():
        _indicatorName = getIndicatorName()
        ª_mtfHandle = iCustom(Symbol(), _indicatorTimeFrame, _indicatorName, 0, inpChannelPeriod)
        if not _checkHandle(ª_mtfHandle, 'Target ' + timeFrameToString(_indicatorTimeFrame) + ' time frame instance'):
            return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_hh, _s_OnCalculate_prev_hl, _s_OnCalculate_prev_lh, _s_OnCalculate_prev_ll
    if _indicatorTimeFrame != Period():
        result = Arr(1, 0.0, dyn=False)
        if CopyBuffer(ª_mtfHandle, 2, 0, 1, result) < 0:
            result[0] = rates_total
        n = 0
        k = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _int(_fdiv(result[0] * float(PeriodSeconds(_indicatorTimeFrame)), PeriodSeconds(Period()))) - 1, 0))
        _prevMark = -99
        _prevTime = 0
        while i < rates_total:
            _currMark = iBarShift(Symbol(), _indicatorTimeFrame, time[i])
            if _currMark < 0:
                i += 1
                continue
            if _currMark != _prevMark:
                _prevMark = _currMark
                _prevTime = time[i]
                if CopyBuffer(ª_mtfHandle, 0, _currMark, 1, result) < 1:
                    break
                filluu[i] = result[0]
                valuu[i] = filluu[i]
                if CopyBuffer(ª_mtfHandle, 1, _currMark, 1, result) < 1:
                    break
                fillud[i] = result[0]
                valud[i] = fillud[i]
                if CopyBuffer(ª_mtfHandle, 2, _currMark, 1, result) < 1:
                    break
                filldu[i] = result[0]
                valdu[i] = filldu[i]
                if CopyBuffer(ª_mtfHandle, 3, _currMark, 1, result) < 1:
                    break
                filldd[i] = result[0]
                valdd[i] = filldd[i]
            else:
                filluu[i] = filluu[i - 1]
                valuu[i] = filluu[i]
                fillud[i] = fillud[i - 1]
                valud[i] = fillud[i]
                filldu[i] = filldu[i - 1]
                valdu[i] = filldu[i]
                filldd[i] = filldd[i - 1]
                valdd[i] = filldd[i]
            if not inpInterpolate:
                i += 1
                continue
            _nextMark = (iBarShift(Symbol(), _indicatorTimeFrame, time[i + 1]) if (i < (rates_total - 1)) else (_prevMark + 1))
            if _nextMark == _prevMark:
                i += 1
                continue
            n = 1
            while (i - n) > 0 and time[i - n] >= _prevTime:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                filluu[i - k] = filluu[i] + _fdiv((filluu[i - n] - filluu[i]) * k, n)
                valuu[i - k] = filluu[i - k]
                fillud[i - k] = fillud[i] + _fdiv((fillud[i - n] - fillud[i]) * k, n)
                valud[i - k] = fillud[i - k]
                filldu[i - k] = filldu[i] + _fdiv((filldu[i - n] - filldu[i]) * k, n)
                valdu[i - k] = filldu[i - k]
                filldd[i - k] = filldd[i] + _fdiv((filldd[i - n] - filldd[i]) * k, n)
                valdd[i - k] = filldd[i - k]
                k += 1
            i += 1
        return i
    i = prev_calculated
    while i < rates_total:
        if _s_OnCalculate_prev_i != i:
            start = i - inpChannelPeriod
            if start < 0:
                start = 0
            _s_OnCalculate_prev_hh = high[ArrayMaximum(high, start, inpChannelPeriod)]
            _s_OnCalculate_prev_hl = low[ArrayMaximum(low, start, inpChannelPeriod)]
            _s_OnCalculate_prev_ll = low[ArrayMinimum(low, start, inpChannelPeriod)]
            _s_OnCalculate_prev_lh = high[ArrayMinimum(high, start, inpChannelPeriod)]
        filluu[i] = _s_OnCalculate_prev_hh
        valuu[i] = filluu[i]
        fillud[i] = _s_OnCalculate_prev_hl
        valud[i] = fillud[i]
        filldd[i] = _s_OnCalculate_prev_ll
        valdd[i] = filldd[i]
        filldu[i] = _s_OnCalculate_prev_lh
        valdu[i] = filldu[i]
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
    if period <= 0:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsPer[MathMin(i + _shift, ArraySize(_tfsPer) - 1)]

def getIndicatorName():
    _path = Box(MQL5InfoString(MQL5_PROGRAM_PATH))
    StringToLower(_path)
    _partsA = Arr(0, "")
    _partsN = StringSplit(_path.v, StringGetCharacter('\\', 0), _partsA)
    name = _partsA[_partsN - 1]
    n = _partsN - 2
    while n >= 0 and _partsA[n] != 'indicators':
        name = _partsA[n] + '\\' + name
        n -= 1
    return name

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__chandles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__chandles, _size + 1)
        _s__checkHandle__chandles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__chandles[i])
        ArrayResize(_s__checkHandle__chandles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_hh = 0.0
_s_OnCalculate_prev_hl = 0.0
_s_OnCalculate_prev_ll = 0.0
_s_OnCalculate_prev_lh = 0.0
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianChannelSlMtf(_MQL5Indicator):
    name = 'Donchian channel (sl)(mtf)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpChannelPeriod': 20,  # Period
        'inpInterpolate': _Choice({1: 'Interpolate data when in multi time frame', 0: 'Do not interpolate data when in multi time frame'}, default=1),  # Interpolation
    }

