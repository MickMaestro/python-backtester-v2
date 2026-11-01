"""Jurik volty mtf — converted from MQL5: MQL5 Indicators/Jurik Volty Multi Timeframe/Jurik volty mtf.mq5

Jurik volty
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [12632256, 3329330, 42495], 2: [12632256, 3329330, 42495]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Jurik volty', 2: 'Jurik volty signal'}, 'levels': [], 'description': ['Jurik volty'], 'name': 'Jurik volty mtf', 'source': 'MQL5 Indicators/Jurik Volty Multi Timeframe/Jurik volty mtf.mq5', 'folder': 'Jurik Volty Multi Timeframe', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Volty period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', tf_cu)  # Time frame
inpPeriod = _input('inpPeriod', 14)  # Volty period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpInterpolate = _input('inpInterpolate', True)  # Interpolate in multi time frame mode?
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
sig = Arr(0, 0.0)
sigc = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
_indicatorTimeFrame = 0
_indicatorName = ""
wrk = Arr(0, 0.0, dims=(5,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

class sVoltyAnswer(MqlObject):
    _q_fields = ('volty', 'voltySignal')
    def __init__(self, *args):
        self.volty = 0.0
        self.voltySignal = 0.0

def OnInit():
    global _indicatorName, _indicatorTimeFrame, _mtfHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, sig, INDICATOR_DATA)
    SetIndexBuffer(3, sigc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, count, INDICATOR_CALCULATIONS)
    _indicatorTimeFrame = MathMax(timeFrameGet(inpTimeFrame), Period())
    _indicatorName = getIndicatorName()
    if _indicatorTimeFrame != Period():
        _mtfHandle = iCustom(Symbol(), _indicatorTimeFrame, _indicatorName, tf_cu, inpPeriod, inpPrice)
        if _mtfHandle == INVALID_HANDLE:
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(_indicatorTimeFrame) + ' Jurik volty (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if _indicatorTimeFrame != Period():
        result = Arr(1, 0.0, dyn=False)
        if BarsCalculated(_mtfHandle) < 0:
            return prev_calculated
        if CopyBuffer(_mtfHandle, 4, 0, 1, result) != 1:
            return prev_calculated
        k = 0
        n = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _int(_fdiv(result[0] * float(PeriodSeconds(_indicatorTimeFrame)), PeriodSeconds(Period()))) - 1, 0))
        _prevMark = 0
        _seconds = PeriodSeconds(_indicatorTimeFrame)
        while i < rates_total:
            _currMark = _int(_idiv(time[i], _seconds))
            if _currMark != _prevMark:
                _prevMark = _currMark
                if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) <= 0:
                    break
                val[i] = result[0]
                if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) <= 0:
                    break
                valc[i] = result[0]
                if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) <= 0:
                    break
                sig[i] = result[0]
                if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) <= 0:
                    break
                sigc[i] = result[0]
            else:
                val[i] = val[i - 1]
                valc[i] = valc[i - 1]
                sig[i] = sig[i - 1]
                sigc[i] = sigc[i - 1]
            if not inpInterpolate:
                i += 1
                continue
            _nextMark = (_int(_idiv(time[i + 1], _seconds)) if (i < (rates_total - 1)) else (_prevMark + 1))
            if _nextMark == _prevMark:
                i += 1
                continue
            n = 1
            while (i - n) > 0 and time[i - n] >= (_prevMark * _seconds):
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                val[i - k] = val[i] + _fdiv((val[i - n] - val[i]) * k, n)
                sig[i - k] = sig[i] + _fdiv((sig[i - n] - sig[i]) * k, n)
                k += 1
            i += 1
        return i
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        _answer = iVolty(price, inpPeriod, i, rates_total)
        val[i] = _answer.volty
        sig[i] = _answer.voltySignal
        valc[i] = (1 if (val[i] > sig[i]) else 2 if (val[i] < sig[i]) else 0)
        sigc[i] = valc[i]
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return i

def iVolty(price, length, r, bars):
    if ArrayRange(wrk, 0) != bars:
        ArrayResize(wrk, bars)
    _answer = sVoltyAnswer()
    _answer.volty = 0.0
    _answer.voltySignal = 0.0
    if r == 0:
        for k in range(0, 5):
            wrk[0][k] = 0.0
        return _copy(_answer)
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = ((price - wrk[r - 1][0]) if (r > 0) else 0)
    del2 = ((price - wrk[r - 1][1]) if (r > 0) else 0)
    wrk[r][2] = 0.0
    if MathAbs(del1) > MathAbs(del2):
        wrk[r][2] = MathAbs(del1)
    if MathAbs(del1) < MathAbs(del2):
        wrk[r][2] = MathAbs(del2)
    wrk[r][3] = ((wrk[r - 1][3] + (0.1 * (wrk[r][2] - wrk[r - 10][2]))) if (r > 9) else wrk[r][2])
    avg = wrk[r][3]
    k = 1
    while k < 65 and (r - k) >= 0:
        avg += wrk[r - k][3]
        k += 1
    avg = _fdiv(avg, k)
    wrk[r][4] = avg
    dVolty = (_fdiv(wrk[r][2], wrk[r][4]) if (wrk[r][4] > 0) else 0)
    if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
        dVolty = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty < 1:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    if del1 > 0:
        wrk[r][0] = price
    else:
        wrk[r][0] = price - (Kv * del1)
    if del2 < 0:
        wrk[r][1] = price
    else:
        wrk[r][1] = price - (Kv * del2)
    _answer.voltySignal = wrk[r][4]
    _answer.volty = wrk[r][3]
    return _copy(_answer)

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

def getIndicatorName():
    _path = Box(MQL5InfoString(MQL5_PROGRAM_PATH))
    StringToLower(_path)
    _partsA = Arr(0, "")
    _partsS = StringGetCharacter('\\', 0)
    _partsN = StringSplit(_path.v, _partsS, _partsA)
    name = _partsA[_partsN - 1]
    n = _partsN - 2
    while n >= 0 and _partsA[n] != 'indicators':
        name = _partsA[n] + '\\' + name
        n -= 1
    return name

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JurikVoltyMtf(_MQL5Indicator):
    name = 'Jurik volty mtf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpPeriod': 14,  # Volty period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpInterpolate': True,  # Interpolate in multi time frame mode?
    }

