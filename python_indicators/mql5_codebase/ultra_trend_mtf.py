"""Ultra trend mtf — converted from MQL5: MQL5 Indicators/Ultra Trend MTF/Ultra trend mtf.mq5

Ultra trend
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 8}, 'colors': {1: [9498256, 11788021], 2: [11119017, 3329330, 42495], 3: [11119017, 3329330, 42495]}, 'widths': {2: 3, 3: 1}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Ultra trend +', 3: 'Ultra trend -'}, 'levels': [], 'description': ['Ultra trend'], 'name': 'Ultra trend mtf', 'source': 'MQL5 Indicators/Ultra Trend MTF/Ultra trend mtf.mq5', 'folder': 'Ultra Trend MTF', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpUtrPeriod', 'py': 'inpUtrPeriod', 'param': 'inpUtrPeriod', 'type': 'int', 'default': 3, 'label': 'Start period', 'sinput': False}, {'mql': 'inpProgression', 'py': 'inpProgression', 'param': 'inpProgression', 'type': 'int', 'default': 5, 'label': 'Step', 'sinput': False}, {'mql': 'inpInstances', 'py': 'inpInstances', 'param': 'inpInstances', 'type': 'int', 'default': 30, 'label': 'Instances', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'int', 'default': 5, 'label': 'Ultra trend smoothing period', 'sinput': False}, {'mql': 'inpSmoothPhase', 'py': 'inpSmoothPhase', 'param': 'inpSmoothPhase', 'type': 'int', 'default': 100, 'label': 'Ultra trend smoothing phase', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter
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
inpUtrPeriod = _input('inpUtrPeriod', 3)  # Start period
inpProgression = _input('inpProgression', 5)  # Step
inpInstances = _input('inpInstances', 30)  # Instances
inpSmooth = _input('inpSmooth', 5)  # Ultra trend smoothing period
inpSmoothPhase = _input('inpSmoothPhase', 100)  # Ultra trend smoothing phase
inpInterpolate = _input('inpInterpolate', True)  # Interpolate in multi time frame mode?
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
valp = Arr(0, 0.0)
valpc = Arr(0, 0.0)
valm = Arr(0, 0.0)
valmc = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

class CJurikSmooth(MqlObject):
    _q_fields = ('m_size', 'm_wrk')
    def __init__(self):
        self.m_size = 0
        self.m_wrk = Arr(0, 0.0, dims=(10,))
        self.m_size = 0
        return
    def _q_dtor(self):
        return
    def CalculateValue(self, price, length, phase, r, bars):
        if self.m_size != bars:
            ArrayResize(self.m_wrk, bars)
        if ArrayRange(self.m_wrk, 0) != bars:
            return price
        self.m_size = bars
        if r == 0 or length <= 1:
            k = 0
            while k < 7:
                self.m_wrk[r][k] = price
                k += 1
            while k < 10:
                self.m_wrk[r][k] = 0.0
                k += 1
            return price
        len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
        pow1 = MathMax(len1 - 2.0, 0.5)
        del1 = price - self.m_wrk[r - 1][5]
        del2 = price - self.m_wrk[r - 1][6]
        forBar = MathMin(r, 10)
        self.m_wrk[r][7] = 0.0
        if MathAbs(del1) > MathAbs(del2):
            self.m_wrk[r][7] = MathAbs(del1)
        if MathAbs(del1) < MathAbs(del2):
            self.m_wrk[r][7] = MathAbs(del2)
        self.m_wrk[r][8] = self.m_wrk[r - 1][8] + ((self.m_wrk[r][7] - self.m_wrk[r - forBar][7]) * 0.1)
        self.m_wrk[r][9] = self.m_wrk[r - 1][9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (self.m_wrk[r][8] - self.m_wrk[r - 1][9]))
        dVolty = (_fdiv(self.m_wrk[r][7], self.m_wrk[r][9]) if (self.m_wrk[r][9] > 0) else 0)
        if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
            dVolty = MathPow(len1, _fdiv(1.0, pow1))
        if dVolty < 1:
            dVolty = 1.0
        pow2 = MathPow(dVolty, pow1)
        len2 = MathSqrt(0.5 * (length - 1)) * len1
        Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
        if del1 > 0:
            self.m_wrk[r][5] = price
        else:
            self.m_wrk[r][5] = price - (Kv * del1)
        if del2 < 0:
            self.m_wrk[r][6] = price
        else:
            self.m_wrk[r][6] = price - (Kv * del2)
        corr = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
        beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
        alpha = MathPow(beta, pow2)
        self.m_wrk[r][0] = price + (alpha * (self.m_wrk[r - 1][0] - price))
        self.m_wrk[r][1] = ((price - self.m_wrk[r][0]) * (1 - beta)) + (beta * self.m_wrk[r - 1][1])
        self.m_wrk[r][2] = self.m_wrk[r][0] + (corr * self.m_wrk[r][1])
        self.m_wrk[r][3] = ((self.m_wrk[r][2] - self.m_wrk[r - 1][4]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * self.m_wrk[r - 1][3])
        self.m_wrk[r][4] = self.m_wrk[r - 1][4] + self.m_wrk[r][3]
        return self.m_wrk[r][4]

def OnInit():
    global _mtfHandle, timeFrame
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, valp, INDICATOR_DATA)
    SetIndexBuffer(3, valpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, valm, INDICATOR_DATA)
    SetIndexBuffer(5, valmc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, count, INDICATOR_CALCULATIONS)
    ArrayResize(_iSmooth, inpInstances + 3)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    timeFrame = MathMax(timeFrameGet(inpTimeFrame), Period())
    if timeFrame != Period():
        _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), 0, inpUtrPeriod, inpProgression, inpInstances, inpSmooth, inpSmoothPhase)
        if _mtfHandle == INVALID_HANDLE:
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' Ultra trend (' + _str(inpUtrPeriod) + ',' + _str(inpProgression) + ',' + _str(inpInstances) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if timeFrame != Period():
        result = Arr(0, 0.0)
        if BarsCalculated(_mtfHandle) < 0:
            return prev_calculated
        if not timeFrameCheck(timeFrame, time):
            return prev_calculated
        if CopyBuffer(_mtfHandle, 6, 0, 1, result) == -1:
            return prev_calculated
        k = 0
        n = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _idiv(_int(result[0]) * PeriodSeconds(timeFrame), PeriodSeconds(Period())) - 1, 0))
        _prevMark = 0
        _seconds = PeriodSeconds(timeFrame)
        while i < rates_total:
            _currMark = _int(_idiv(time[i], _seconds))
            if _currMark != _prevMark:
                _prevMark = _currMark
                if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) == -1:
                    break
                fillu[i] = result[0]
                if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                    break
                filld[i] = result[0]
                if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) == -1:
                    break
                valp[i] = result[0]
                if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) == -1:
                    break
                valpc[i] = result[0]
                if CopyBuffer(_mtfHandle, 4, _DT(time[i]), 1, result) == -1:
                    break
                valm[i] = result[0]
                if CopyBuffer(_mtfHandle, 5, _DT(time[i]), 1, result) == -1:
                    break
                valmc[i] = result[0]
            else:
                fillu[i] = fillu[i - 1]
                filld[i] = filld[i - 1]
                valp[i] = valp[i - 1]
                valpc[i] = valpc[i - 1]
                valm[i] = valm[i - 1]
                valmc[i] = valmc[i - 1]
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
                fillu[i - k] = fillu[i] + _fdiv((fillu[i - n] - fillu[i]) * k, n)
                filld[i - k] = filld[i] + _fdiv((filld[i - n] - filld[i]) * k, n)
                valp[i - k] = valp[i] + _fdiv((valp[i - n] - valp[i]) * k, n)
                valm[i - k] = valm[i] + _fdiv((valm[i - n] - valm[i]) * k, n)
                k += 1
            i += 1
        return i
    endLength = inpUtrPeriod + (inpProgression * inpInstances)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        valueUp = 0.0
        valueDn = 0.0
        k = inpUtrPeriod
        instance = 2
        while k <= endLength and i > 0:
            if _iSmooth[instance].CalculateValue(close[i - 1], k, inpSmoothPhase, i - 1, rates_total) < _iSmooth[instance].CalculateValue(close[i], k, inpSmoothPhase, i, rates_total):
                valueUp += 1
            else:
                valueDn += 1
            k += inpProgression
            instance += 1
        valp[i] = _iSmooth[0].CalculateValue(valueUp, inpSmooth, inpSmoothPhase, i, rates_total)
        valm[i] = _iSmooth[1].CalculateValue(valueDn, inpSmooth, inpSmoothPhase, i, rates_total)
        valpc[i] = (1 if (valp[i] > valm[i]) else 2)
        valmc[i] = valpc[i]
        fillu[i] = valp[i]
        filld[i] = valm[i]
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
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

def getIndicatorName():
    _path = MQL5InfoString(MQL5_PROGRAM_PATH)
    _partsA = Arr(0, "")
    _partsS = StringGetCharacter('\\', 0)
    _partsN = StringSplit(_path, _partsS, _partsA)
    name = _partsA[_partsN - 1]
    n = _partsN - 2
    while n >= 0 and _toLower(_partsA[n]) != 'indicators':
        name = _partsA[n] + '\\' + name
        n -= 1
    return name

def _toLower(_toConvert):
    _toConvert = Box(_toConvert)
    StringToLower(_toConvert)
    return _toConvert.v

def timeFrameCheck(_timeFrame, time):
    global _s_timeFrameCheck_warned
    if time[0] < SeriesInfoInteger(Symbol(), _timeFrame, SERIES_FIRSTDATE):
        startTime = Box(0)
        testTime = Arr(0, 0)
        if SeriesInfoInteger(Symbol(), PERIOD_M1, SERIES_TERMINAL_FIRSTDATE, startTime):
            if startTime.v > 0:
                CopyTime(Symbol(), _timeFrame, _DT(time[0]), 1, testTime)
                SeriesInfoInteger(Symbol(), _timeFrame, SERIES_FIRSTDATE, startTime)
        if startTime.v <= 0 or startTime.v > time[0]:
            Comment(MQL5InfoString(MQL5_PROGRAM_NAME) + '\nMissing data for ' + timeFrameToString(_timeFrame) + ' time frame\nRe-trying on next tick')
            _s_timeFrameCheck_warned = True
            return False
    if _s_timeFrameCheck_warned:
        Comment('')
        _s_timeFrameCheck_warned = False
    return True

# ---- global variables initialised from expressions
_iSmooth = Arr(0, 0, factory=CJurikSmooth)

# ---- static local variables
_s_timeFrameCheck_warned = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UltraTrendMtf(_MQL5Indicator):
    name = 'Ultra trend mtf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpUtrPeriod': 3,  # Start period
        'inpProgression': 5,  # Step
        'inpInstances': 30,  # Instances
        'inpSmooth': 5,  # Ultra trend smoothing period
        'inpSmoothPhase': 100,  # Ultra trend smoothing phase
        'inpInterpolate': True,  # Interpolate in multi time frame mode?
    }

