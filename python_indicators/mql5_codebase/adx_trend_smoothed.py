"""Adx trend smoothed — converted from MQL5: MQL5 Indicators/ADX trend - smoothed/Adx trend smoothed.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 10, 3: 8}, 'colors': {1: [10545056, 10526951], 2: [8421504, 3329330, 32768, 255, 128], 3: [8421504, 3329330, 255]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Adx trend filling', 2: 'Adx trend histogram', 3: 'Adx trend'}, 'levels': [], 'description': [], 'name': 'Adx trend smoothed', 'source': 'MQL5 Indicators/ADX trend - smoothed/Adx trend smoothed.mq5', 'folder': 'ADX trend - smoothed', 'inputs': [{'mql': 'AdxVmaPeriod', 'py': 'AdxVmaPeriod', 'param': 'AdxVmaPeriod', 'type': 'double', 'default': 10.0, 'label': 'AdxVma period', 'sinput': False}, {'mql': 'AdxVmaPrice', 'py': 'AdxVmaPrice', 'param': 'AdxVmaPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'int', 'default': 5, 'label': 'Smoothing period (<=1 for no smoothing)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# ---- inputs and global variables
AdxVmaPeriod = _input('AdxVmaPeriod', 10.0)  # AdxVma period
AdxVmaPrice = _input('AdxVmaPrice', pr_close)  # Price
SmoothPeriod = _input('SmoothPeriod', 5)  # Smoothing period (<=1 for no smoothing)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valfu = Arr(0, 0.0)
valfd = Arr(0, 0.0)
histo = Arr(0, 0.0)
histoc = Arr(0, 0.0)
_adxvmaWork = Arr(0, 0.0, dims=(14,))
m_wrk = Arr(0, 0.0, dims=(10,))
m_size = 0
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, valfu, INDICATOR_DATA)
    SetIndexBuffer(1, valfd, INDICATOR_DATA)
    SetIndexBuffer(2, histo, INDICATOR_DATA)
    SetIndexBuffer(3, histoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    for k in range(0, 2):
        PlotIndexSetInteger(k, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adx trend (' + _str(AdxVmaPeriod) + ',' + _str(SmoothPeriod) + ')')

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdxTrendSmoothed(_MQL5Indicator):
    name = 'Adx trend smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AdxVmaPeriod': 10.0,  # AdxVma period
        'AdxVmaPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'SmoothPeriod': 5,  # Smoothing period (<=1 for no smoothing)
    }

