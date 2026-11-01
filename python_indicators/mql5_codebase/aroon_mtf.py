"""Aroon (mtf) — converted from MQL5: MQL5 Indicators/Aroon - multi time frame version/Aroon (mtf).mq5

Multi time frame Aroon
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3, 'indicator_minimum': -5.0, 'indicator_maximum': 105.0}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16760576, 8894686], 2: [12632256], 3: [12632256]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Aroon filling', 2: 'Aroon up', 3: 'Aroon down'}, 'levels': [0.0, 100.0], 'description': ['Multi time frame Aroon'], 'name': 'Aroon (mtf)', 'source': 'MQL5 Indicators/Aroon - multi time frame version/Aroon (mtf).mq5', 'folder': 'Aroon - multi time frame version', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'int', 'default': 25, 'label': 'calculation period', 'sinput': False}, {'mql': 'PriceHigh', 'py': 'PriceHigh', 'param': 'PriceHigh', 'type': 'int', 'default': 3, 'label': 'Price to use for high', 'sinput': False}, {'mql': 'PriceLow', 'py': 'PriceLow', 'param': 'PriceLow', 'type': 'int', 'default': 4, 'label': 'Price to use for low', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'int', 'default': 1, 'label': 'Interpolation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
AroonPeriod = _input('AroonPeriod', 25)  # calculation period
PriceHigh = _input('PriceHigh', PRICE_HIGH)  # Price to use for high
PriceLow = _input('PriceLow', PRICE_LOW)  # Price to use for low
inpInterpolate = _input('inpInterpolate', interolate_yes)  # Interpolation
valueup = Arr(0, 0.0)
valuedn = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
prh = Arr(0, 0.0)
prl = Arr(0, 0.0)
count = Arr(0, 0.0)
_indicatorTimeFrame = 0
_indicatorName = ""
_indicatorHandle = 0
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _indicatorHandle, _indicatorName, _indicatorTimeFrame
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, valueup, INDICATOR_DATA)
    SetIndexBuffer(3, valuedn, INDICATOR_DATA)
    SetIndexBuffer(4, prh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, prl, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, count, INDICATOR_CALCULATIONS)
    _indicatorTimeFrame = MathMax(Period(), timeFrameGet(inpTimeFrame))
    if _indicatorTimeFrame != Period():
        _indicatorName = getIndicatorName()
        _indicatorHandle = iCustom(Symbol(), _indicatorTimeFrame, _indicatorName, 0, AroonPeriod, PriceHigh, PriceLow)
        if not _checkHandle(_indicatorHandle, 'Target time frame instance'):
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(_indicatorTimeFrame) + ' Aroon (' + DoubleToString(AroonPeriod, 0) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, TickVolume, Volume, Spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_maxk, _s_OnCalculate_prev_mink
    if _indicatorTimeFrame != Period():
        result = Arr(1, 0.0, dyn=False)
        if CopyBuffer(_indicatorHandle, 6, 0, 1, result) < 0:
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
                if CopyBuffer(_indicatorHandle, 2, _currMark, 1, result) < 1:
                    break
                valueup[i] = result[0]
                fill1[i] = valueup[i]
                if CopyBuffer(_indicatorHandle, 3, _currMark, 1, result) < 1:
                    break
                valuedn[i] = result[0]
                fill2[i] = valuedn[i]
            else:
                valueup[i] = valueup[i - 1]
                fill1[i] = valueup[i]
                valuedn[i] = valuedn[i - 1]
                fill2[i] = valuedn[i]
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
                valueup[i - k] = valueup[i] + _fdiv((valueup[i - n] - valueup[i]) * k, n)
                fill1[i - k] = valueup[i - k]
                valuedn[i - k] = valuedn[i] + _fdiv((valuedn[i - n] - valuedn[i]) * k, n)
                fill2[i - k] = valuedn[i - k]
                k += 1
            i += 1
        return i
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _sw1 = PriceHigh
        if _sw1 == PRICE_CLOSE:
            prh[i] = close[i]
        elif _sw1 == PRICE_OPEN:
            prh[i] = open[i]
        elif _sw1 == PRICE_HIGH:
            prh[i] = high[i]
        elif _sw1 == PRICE_LOW:
            prh[i] = low[i]
        elif _sw1 == PRICE_MEDIAN:
            prh[i] = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            prh[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            prh[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            prh[i] = 0.0
        _sw2 = PriceLow
        if _sw2 == PRICE_CLOSE:
            prl[i] = close[i]
        elif _sw2 == PRICE_OPEN:
            prl[i] = open[i]
        elif _sw2 == PRICE_HIGH:
            prl[i] = high[i]
        elif _sw2 == PRICE_LOW:
            prl[i] = low[i]
        elif _sw2 == PRICE_MEDIAN:
            prl[i] = (high[i] + low[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            prl[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            prl[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            prl[i] = 0.0
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - AroonPeriod
            if start < 0:
                start = 0
            _s_OnCalculate_prev_maxk = ArrayMaximum(prh, start, AroonPeriod + 1)
            _s_OnCalculate_prev_mink = ArrayMinimum(prl, start, AroonPeriod + 1)
        fill1[i] = _idiv(100 * (AroonPeriod - (i - _s_OnCalculate_prev_maxk)), AroonPeriod)
        valueup[i] = fill1[i]
        fill2[i] = _idiv(100 * (AroonPeriod - (i - _s_OnCalculate_prev_mink)), AroonPeriod)
        valuedn[i] = fill2[i]
        i += 1
    count[rates_total - 1] = MathMax(i - prev_calculated + 1, 1)
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
_s_OnCalculate_prev_maxk = 0
_s_OnCalculate_prev_mink = 0
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AroonMtf(_MQL5Indicator):
    name = 'Aroon (mtf)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'AroonPeriod': 25,  # calculation period
        'PriceHigh': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=3),  # Price to use for high
        'PriceLow': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=4),  # Price to use for low
        'inpInterpolate': _Choice({1: 'Interpolate data when in multi time frame', 0: 'Do not interpolate data when in multi time frame'}, default=1),  # Interpolation
    }
    y_range = (-5.0, 105.0)

