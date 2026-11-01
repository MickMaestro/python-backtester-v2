"""ADXm smoothed mtf — converted from MQL5: MQL5 Indicators/ADXm Smoothed - MTF/ADXm smoothed mtf.mq5

ADXm smoothed - multi time frame version
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [11119017], 2: [11119017, 16748574, 6333684]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'DI', 2: 'ADXm'}, 'levels': [], 'description': ['ADXm smoothed - multi time frame version'], 'name': 'ADXm smoothed mtf', 'source': 'MQL5 Indicators/ADXm Smoothed - MTF/ADXm smoothed mtf.mq5', 'folder': 'ADXm Smoothed - MTF', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpAdxmPeriod', 'py': 'inpAdxmPeriod', 'param': 'inpAdxmPeriod', 'type': 'int', 'default': 14, 'label': 'ADXm period', 'sinput': False}, {'mql': 'inpAdxmSmooth', 'py': 'inpAdxmSmooth', 'param': 'inpAdxmSmooth', 'type': 'int', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpAdxmSmoothPhase', 'py': 'inpAdxmSmoothPhase', 'param': 'inpAdxmSmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Smoothing phase', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
inpAdxmPeriod = _input('inpAdxmPeriod', 14)  # ADXm period
inpAdxmSmooth = _input('inpAdxmSmooth', 5)  # Smoothing period
inpAdxmSmoothPhase = _input('inpAdxmSmoothPhase', 0.0)  # Smoothing phase
inpInterpolate = _input('inpInterpolate', True)  # Interpolate in multi time frame mode?
adxm = Arr(0, 0.0)
adxmc = Arr(0, 0.0)
di = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
_adxmWork = Arr(0, 0.0, dims=(8,))
m_wrk = Arr(0, 0.0, dims=(10,))
m_size = 0
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _mtfHandle, timeFrame
    SetIndexBuffer(0, di, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, adxm, INDICATOR_DATA)
    SetIndexBuffer(2, adxmc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, count, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(timeFrameGet(inpTimeFrame), Period())
    if timeFrame != Period():
        _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), tf_cu, inpAdxmPeriod, inpAdxmSmooth, inpAdxmSmoothPhase)
        if _mtfHandle == INVALID_HANDLE:
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' ADXm smoothed (' + _str(inpAdxmPeriod) + ',' + _str(inpAdxmSmooth) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if timeFrame != Period():
        if BarsCalculated(_mtfHandle) < 0:
            return prev_calculated
        result = Arr(0, 0.0)
        currTime = Arr(0, 0)
        nextTime = Arr(0, 0)
        if not timeFrameCheck(timeFrame, time):
            return prev_calculated
        if CopyBuffer(_mtfHandle, 3, 0, 1, result) == -1:
            return prev_calculated
        k = 0
        n = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _idiv(_int(result[0]) * PeriodSeconds(timeFrame), PeriodSeconds(Period())) - 1, 0))
        while i < rates_total:
            if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) == -1:
                break
            di[i] = result[0]
            if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            adxm[i] = result[0]
            if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            adxmc[i] = result[0]
            if not inpInterpolate:
                i += 1
                continue
            _timeCopied = CopyTime(Symbol(), timeFrame, _DT(time[i]), 1, currTime)
            if _timeCopied != 1:
                break
            if i < (rates_total - 1):
                CopyTime(Symbol(), timeFrame, _DT(time[i + 1]), 1, nextTime)
                if currTime[0] == nextTime[0]:
                    i += 1
                    continue
            n = 1
            while (i - n) > 0 and time[i - n] >= currTime[0]:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                adxm[i - k] = adxm[i] + _fdiv((adxm[i - n] - adxm[i]) * k, n)
                di[i - k] = di[i] + _fdiv((di[i - n] - di[i]) * k, n)
                k += 1
            i += 1
        return i
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _di = Box(0.0)
        adxm[i] = iSmooth(iAdxm(close[i], high[i], low[i], inpAdxmPeriod, _di, i, rates_total), inpAdxmSmooth, inpAdxmSmoothPhase, i, rates_total)
        di[i] = _di.v
        adxmc[i] = ((1 if (adxm[i] > adxm[i - 1]) else 2 if (adxm[i] < adxm[i - 1]) else adxmc[i - 1]) if (i > 0) else 0)
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return i

def iAdxm(_close, _high, _low, _period, _di, i, bars, instanceNo=0):
    if ArrayRange(_adxmWork, 0) != bars:
        ArrayResize(_adxmWork, bars)
    instanceNo *= 8
    _adxmWork[i][instanceNo + 3] = _close
    _adxmWork[i][instanceNo + 4] = _high
    _adxmWork[i][instanceNo + 5] = _low
    hc = _adxmWork[i][instanceNo + 4]
    lc = _adxmWork[i][instanceNo + 5]
    cp = (_adxmWork[i - 1][instanceNo + 3] if (i > 0) else _adxmWork[i][instanceNo + 3])
    hp = (_adxmWork[i - 1][instanceNo + 4] if (i > 0) else _adxmWork[i][instanceNo + 4])
    lp = (_adxmWork[i - 1][instanceNo + 5] if (i > 0) else _adxmWork[i][instanceNo + 5])
    dh = MathMax(hc - hp, 0)
    dl = MathMax(lp - lc, 0)
    if dh == dl:
        dh = 0.0
        dl = 0.0
    elif dh < dl:
        dh = 0.0
    elif dl < dh:
        dl = 0.0
    tr = MathMax(hc, cp) - MathMin(lc, cp)
    dhk = (_fdiv(100.0 * dh, tr) if (tr != 0) else 0)
    dlk = (_fdiv(100.0 * dl, tr) if (tr != 0) else 0)
    alpha = _fdiv(2.0, _period + 1.0)
    _adxmWork[i][instanceNo + 0] = ((_adxmWork[i - 1][instanceNo + 0] + (alpha * (dhk - _adxmWork[i - 1][instanceNo + 0]))) if (i > 0) else dhk)
    _adxmWork[i][instanceNo + 1] = ((_adxmWork[i - 1][instanceNo + 1] + (alpha * (dlk - _adxmWork[i - 1][instanceNo + 1]))) if (i > 0) else dlk)
    _adxmWork[i][instanceNo + 6] = _adxmWork[i][instanceNo + 0] - _adxmWork[i][instanceNo + 1]
    div = MathAbs(_adxmWork[i][instanceNo + 0] + _adxmWork[i][instanceNo + 1])
    temp = (_fdiv(100 * _adxmWork[i][instanceNo + 6], div) if (div != 0.0) else 0)
    _adxmWork[i][instanceNo + 7] = ((_adxmWork[i - 1][instanceNo + 7] + (alpha * (temp - _adxmWork[i - 1][instanceNo + 7]))) if (i > 0) else 0)
    _di.v = _adxmWork[i][instanceNo + 6]
    return _adxmWork[i][instanceNo + 7]

def iSmooth(price, length, phase, r, bars):
    global m_size
    if m_size != bars:
        ArrayResize(m_wrk, bars)
    if ArrayRange(m_wrk, 0) != bars:
        return price
    m_size = bars
    if r == 0 or length <= 1:
        k = 0
        while k < 7:
            m_wrk[r][k] = price
            k += 1
        while k < 10:
            m_wrk[r][k] = 0.0
            k += 1
        return price
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = price - m_wrk[r - 1][5]
    del2 = price - m_wrk[r - 1][6]
    forBar = MathMin(r, 10)
    m_wrk[r][7] = 0.0
    if MathAbs(del1) > MathAbs(del2):
        m_wrk[r][7] = MathAbs(del1)
    if MathAbs(del1) < MathAbs(del2):
        m_wrk[r][7] = MathAbs(del2)
    m_wrk[r][8] = m_wrk[r - 1][8] + ((m_wrk[r][7] - m_wrk[r - forBar][7]) * 0.1)
    m_wrk[r][9] = m_wrk[r - 1][9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (m_wrk[r][8] - m_wrk[r - 1][9]))
    dVolty = (_fdiv(m_wrk[r][7], m_wrk[r][9]) if (m_wrk[r][9] > 0) else 0)
    if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
        dVolty = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty < 1:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    if del1 > 0:
        m_wrk[r][5] = price
    else:
        m_wrk[r][5] = price - (Kv * del1)
    if del2 < 0:
        m_wrk[r][6] = price
    else:
        m_wrk[r][6] = price - (Kv * del2)
    corr = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    m_wrk[r][0] = price + (alpha * (m_wrk[r - 1][0] - price))
    m_wrk[r][1] = ((price - m_wrk[r][0]) * (1 - beta)) + (beta * m_wrk[r - 1][1])
    m_wrk[r][2] = m_wrk[r][0] + (corr * m_wrk[r][1])
    m_wrk[r][3] = ((m_wrk[r][2] - m_wrk[r - 1][4]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * m_wrk[r - 1][3])
    m_wrk[r][4] = m_wrk[r - 1][4] + m_wrk[r][3]
    return m_wrk[r][4]

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

# ---- static local variables
_s_timeFrameCheck_warned = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADXmSmoothedMtf(_MQL5Indicator):
    name = 'ADXm smoothed mtf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpAdxmPeriod': 14,  # ADXm period
        'inpAdxmSmooth': 5,  # Smoothing period
        'inpAdxmSmoothPhase': 0.0,  # Smoothing phase
        'inpInterpolate': True,  # Interpolate in multi time frame mode?
    }

