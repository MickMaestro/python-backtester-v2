"""Adx trend smoothed mtf — converted from MQL5: MQL5 Indicators/ADX trend smoothed - multi time frame/Adx trend smoothed mtf.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 7, 2: 10, 3: 8}, 'colors': {1: [10545056, 10526951], 2: [8421504, 3329330, 32768, 255, 128], 3: [8421504, 3329330, 255]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Adx trend filling', 2: 'Adx trend histogram', 3: 'Adx trend'}, 'levels': [], 'description': [], 'name': 'Adx trend smoothed mtf', 'source': 'MQL5 Indicators/ADX trend smoothed - multi time frame/Adx trend smoothed mtf.mq5', 'folder': 'ADX trend smoothed - multi time frame', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'AdxVmaPeriod', 'py': 'AdxVmaPeriod', 'param': 'AdxVmaPeriod', 'type': 'double', 'default': 10.0, 'label': 'AdxVma period', 'sinput': False}, {'mql': 'AdxVmaPrice', 'py': 'AdxVmaPrice', 'param': 'AdxVmaPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'int', 'default': 5, 'label': 'Smoothing period (<=1 for no smoothing)', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter
MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
pr_medianb = 8
pr_tbiased = 9
pr_tbiased2 = 10
pr_haclose = 11
pr_haopen = 12
pr_hahigh = 13
pr_halow = 14
pr_hamedian = 15
pr_hatypical = 16
pr_haweighted = 17
pr_haaverage = 18
pr_hamedianb = 19
pr_hatbiased = 20
pr_hatbiased2 = 21
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_medianb', 9: 'pr_tbiased', 10: 'pr_tbiased2', 11: 'pr_haclose', 12: 'pr_haopen', 13: 'pr_hahigh', 14: 'pr_halow', 15: 'pr_hamedian', 16: 'pr_hatypical', 17: 'pr_haweighted', 18: 'pr_haaverage', 19: 'pr_hamedianb', 20: 'pr_hatbiased', 21: 'pr_hatbiased2'})

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
AdxVmaPeriod = _input('AdxVmaPeriod', 10.0)  # AdxVma period
AdxVmaPrice = _input('AdxVmaPrice', pr_close)  # Price
SmoothPeriod = _input('SmoothPeriod', 5)  # Smoothing period (<=1 for no smoothing)
inpInterpolate = _input('inpInterpolate', True)  # Interpolate in multi time frame mode?
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valfu = Arr(0, 0.0)
valfd = Arr(0, 0.0)
histo = Arr(0, 0.0)
histoc = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
_indicatorTimeFrame = 0
_indicatorName = ""
_adxvmaWork = Arr(0, 0.0, dims=(14,))
m_wrk = Arr(0, 0.0, dims=(10,))
m_size = 0
workHa = Arr(0, 0.0, dims=(4,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _indicatorName, _indicatorTimeFrame, _mtfHandle
    SetIndexBuffer(0, valfu, INDICATOR_DATA)
    SetIndexBuffer(1, valfd, INDICATOR_DATA)
    SetIndexBuffer(2, histo, INDICATOR_DATA)
    SetIndexBuffer(3, histoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, count, INDICATOR_CALCULATIONS)
    for k in range(0, 2):
        PlotIndexSetInteger(k, PLOT_SHOW_DATA, False)
    _indicatorTimeFrame = MathMax(timeFrameGet(inpTimeFrame), Period())
    _indicatorName = getIndicatorName()
    if _indicatorTimeFrame != Period():
        _mtfHandle = iCustom(Symbol(), _indicatorTimeFrame, _indicatorName, 0, AdxVmaPeriod, AdxVmaPrice, SmoothPeriod)
        if _mtfHandle == INVALID_HANDLE:
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(_indicatorTimeFrame) + ' Adx trend (' + _str(AdxVmaPeriod) + ',' + _str(SmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if _indicatorTimeFrame != Period():
        result = Arr(0, 0.0)
        if BarsCalculated(_mtfHandle) < 0:
            return prev_calculated
        if not timeFrameCheck(_indicatorTimeFrame, time):
            return prev_calculated
        if CopyBuffer(_mtfHandle, 6, 0, 1, result) == -1:
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
                valfu[i] = result[0]
                if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) <= 0:
                    break
                valfd[i] = result[0]
                if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) <= 0:
                    break
                histo[i] = result[0]
                if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) <= 0:
                    break
                histoc[i] = result[0]
                if CopyBuffer(_mtfHandle, 4, _DT(time[i]), 1, result) <= 0:
                    break
                val[i] = result[0]
                if CopyBuffer(_mtfHandle, 5, _DT(time[i]), 1, result) <= 0:
                    break
                valc[i] = result[0]
            else:
                val[i] = val[i - 1]
                valc[i] = valc[i - 1]
                histo[i] = histo[i - 1]
                histoc[i] = histoc[i - 1]
                valfu[i] = valfu[i - 1]
                valfd[i] = valfd[i - 1]
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
                histo[i - k] = val[i - k]
                if valfu[i] != 0:
                    valfu[i - k] = val[i - k]
                if valfd[i] != 0:
                    valfd[i - k] = val[i - k]
                k += 1
            i += 1
        return i
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        trendup = Box(0.0)
        trenddn = Box(0.0)
        iAdxvma(getPrice(AdxVmaPrice, open, close, high, low, i, rates_total), AdxVmaPeriod, i, rates_total, trendup, trenddn, 1)
        val[i] = (iSmooth(trendup.v, SmoothPeriod, 0.0, i, rates_total, 0) if (trendup.v > 0) else iSmooth(trenddn.v, SmoothPeriod, 0.0, i, rates_total, 0))
        valc[i] = (1 if (trendup.v > 0) else 2 if (trenddn.v > 0) else valc[i - 1] if (i > 0) else 0)
        valfu[i] = (val[i] if (trendup.v > 0) else 0)
        valfd[i] = (0 if (trendup.v > 0) else val[i])
        histo[i] = val[i]
        histoc[i] = (((1 if (val[i] > val[i - 1]) else 2) if (valc[i] == 1) else 4 if (val[i] < val[i - 1]) else 3) if (i > 0) else 0)
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return i

def iAdxvma(price, period, i, bars, trendp, trendm, instanceNo=0):
    if ArrayRange(_adxvmaWork, 0) != bars:
        ArrayResize(_adxvmaWork, bars)
    instanceNo *= 7
    for k in range(0, 7):
        _adxvmaWork[i][instanceNo + k] = price
    if period > 1:
        diff = ((_adxvmaWork[i][instanceNo + 0] - _adxvmaWork[i - 1][instanceNo + 0]) if (i > 0) else 0)
        tpdm = (diff if (diff > 0) else 0)
        tmdm = ((-diff) if (diff < 0) else 0)
        _adxvmaWork[i][instanceNo + 1] = (_fdiv(((period - 1.0) * _adxvmaWork[i - 1][instanceNo + 1]) + tpdm, period) if (i > 0) else tpdm)
        _adxvmaWork[i][instanceNo + 2] = (_fdiv(((period - 1.0) * _adxvmaWork[i - 1][instanceNo + 2]) + tmdm, period) if (i > 0) else tmdm)
        trueRange = _adxvmaWork[i][instanceNo + 1] + _adxvmaWork[i][instanceNo + 2]
        tpdi = (_fdiv(_adxvmaWork[i][instanceNo + 1], trueRange) if (trueRange > 0) else 0)
        tmdi = (_fdiv(_adxvmaWork[i][instanceNo + 2], trueRange) if (trueRange > 0) else 0)
        _adxvmaWork[i][instanceNo + 3] = (_fdiv(((period - 1.0) * _adxvmaWork[i - 1][instanceNo + 3]) + tpdi, period) if (i > 0) else tpdi)
        _adxvmaWork[i][instanceNo + 4] = (_fdiv(((period - 1.0) * _adxvmaWork[i - 1][instanceNo + 4]) + tmdi, period) if (i > 0) else tmdi)
        trendp.v = _adxvmaWork[i][instanceNo + 3] - 0.5
        trendm.v = _adxvmaWork[i][instanceNo + 4] - 0.5
        tout = 0.0
        if (_adxvmaWork[i][instanceNo + 3] + _adxvmaWork[i][instanceNo + 4]) > 0:
            tout = _fdiv(MathAbs(_adxvmaWork[i][instanceNo + 3] - _adxvmaWork[i][instanceNo + 4]), _adxvmaWork[i][instanceNo + 3] + _adxvmaWork[i][instanceNo + 4])
        _adxvmaWork[i][instanceNo + 5] = (_fdiv(((period - 1.0) * _adxvmaWork[i - 1][instanceNo + 5]) + tout, period) if (i > 0) else tout)
        thi = (MathMax(_adxvmaWork[i][instanceNo + 5], _adxvmaWork[i - 1][instanceNo + 5]) if (i > 0) else _adxvmaWork[i][instanceNo + 5])
        tlo = (MathMin(_adxvmaWork[i][instanceNo + 5], _adxvmaWork[i - 1][instanceNo + 5]) if (i > 0) else _adxvmaWork[i][instanceNo + 5])
        k = 2
        while k < period and (i - k) >= 0:
            thi = MathMax(_adxvmaWork[i - k][instanceNo + 5], thi)
            tlo = MathMin(_adxvmaWork[i - k][instanceNo + 5], tlo)
            k += 1
        vi = (_fdiv(_adxvmaWork[i][instanceNo + 5] - tlo, thi - tlo) if ((thi - tlo) > 0) else 0)
        _adxvmaWork[i][instanceNo + 6] = (_fdiv(((period - vi) * _adxvmaWork[i - 1][instanceNo + 6]) + (vi * _adxvmaWork[i][instanceNo + 0]), period) if (i > 0) else price)
    return _adxvmaWork[i][instanceNo + 6]

def iSmooth(price, length, phase, r, bars, instanceNo=0):
    if ArrayRange(m_wrk, 0) != bars:
        ArrayResize(m_wrk, bars)
    if ArrayRange(m_wrk, 0) != bars:
        return price
    instanceNo *= 10
    if r == 0 or length <= 1:
        k = 0
        while k < 7:
            m_wrk[r][instanceNo + k] = price
            k += 1
        while k < 10:
            m_wrk[r][instanceNo + k] = 0.0
            k += 1
        return price
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = price - m_wrk[r - 1][instanceNo + 5]
    del2 = price - m_wrk[r - 1][instanceNo + 6]
    forBar = MathMin(r, 10)
    m_wrk[r][instanceNo + 7] = 0.0
    if MathAbs(del1) > MathAbs(del2):
        m_wrk[r][instanceNo + 7] = MathAbs(del1)
    if MathAbs(del1) < MathAbs(del2):
        m_wrk[r][instanceNo + 7] = MathAbs(del2)
    m_wrk[r][instanceNo + 8] = m_wrk[r - 1][instanceNo + 8] + ((m_wrk[r][instanceNo + 7] - m_wrk[r - forBar][instanceNo + 7]) * 0.1)
    m_wrk[r][instanceNo + 9] = m_wrk[r - 1][instanceNo + 9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (m_wrk[r][instanceNo + 8] - m_wrk[r - 1][instanceNo + 9]))
    dVolty = (_fdiv(m_wrk[r][instanceNo + 7], m_wrk[r][instanceNo + 9]) if (m_wrk[r][instanceNo + 9] > 0) else 0)
    if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
        dVolty = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty < 1:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    if del1 > 0:
        m_wrk[r][instanceNo + 5] = price
    else:
        m_wrk[r][instanceNo + 5] = price - (Kv * del1)
    if del2 < 0:
        m_wrk[r][instanceNo + 6] = price
    else:
        m_wrk[r][instanceNo + 6] = price - (Kv * del2)
    corr = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    m_wrk[r][instanceNo + 0] = price + (alpha * (m_wrk[r - 1][instanceNo + 0] - price))
    m_wrk[r][instanceNo + 1] = ((price - m_wrk[r][instanceNo + 0]) * (1 - beta)) + (beta * m_wrk[r - 1][instanceNo + 1])
    m_wrk[r][instanceNo + 2] = m_wrk[r][instanceNo + 0] + (corr * m_wrk[r][instanceNo + 1])
    m_wrk[r][instanceNo + 3] = ((m_wrk[r][instanceNo + 2] - m_wrk[r - 1][instanceNo + 4]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * m_wrk[r - 1][instanceNo + 3])
    m_wrk[r][instanceNo + 4] = m_wrk[r - 1][instanceNo + 4] + m_wrk[r][instanceNo + 3]
    return m_wrk[r][instanceNo + 4]

def getPrice(tprice, open, close, high, low, i, _bars, instanceNo=0):
    if tprice >= pr_haclose:
        if ArrayRange(workHa, 0) != _bars:
            ArrayResize(workHa, _bars)
        instanceNo *= 4
        haOpen = 0.0
        if i > 0:
            haOpen = (workHa[i - 1][instanceNo + 2] + workHa[i - 1][instanceNo + 3]) / 2.0
        else:
            haOpen = (open[i] + close[i]) / 2
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][instanceNo + 0] = haLow
            workHa[i][instanceNo + 1] = haHigh
        else:
            workHa[i][instanceNo + 0] = haHigh
            workHa[i][instanceNo + 1] = haLow
        workHa[i][instanceNo + 2] = haOpen
        workHa[i][instanceNo + 3] = haClose
        _sw1 = tprice
        if _sw1 == pr_haclose:
            return haClose
        elif _sw1 == pr_haopen:
            return haOpen
        elif _sw1 == pr_hahigh:
            return haHigh
        elif _sw1 == pr_halow:
            return haLow
        elif _sw1 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw1 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw1 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw1 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw1 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw1 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw1 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw2 = tprice
    if _sw2 == pr_close:
        return close[i]
    elif _sw2 == pr_open:
        return open[i]
    elif _sw2 == pr_high:
        return high[i]
    elif _sw2 == pr_low:
        return low[i]
    elif _sw2 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw2 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw2 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw2 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0

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


class AdxTrendSmoothedMtf(_MQL5Indicator):
    name = 'Adx trend smoothed mtf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'AdxVmaPeriod': 10.0,  # AdxVma period
        'AdxVmaPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'SmoothPeriod': 5,  # Smoothing period (<=1 for no smoothing)
        'inpInterpolate': True,  # Interpolate in multi time frame mode?
    }

