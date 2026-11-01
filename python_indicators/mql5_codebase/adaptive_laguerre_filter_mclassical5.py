"""Adaptive_laguerre_filter_mclassical5 — converted from MQL5: MQL5 Indicators/Adaptive Laguerre/Adaptive_laguerre_filter_mclassical5.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Laguerre filter'}, 'levels': [], 'description': [], 'name': 'Adaptive_laguerre_filter_mclassical5', 'source': 'MQL5 Indicators/Adaptive Laguerre/Adaptive_laguerre_filter_mclassical5.mq5', 'folder': 'Adaptive Laguerre', 'inputs': [{'mql': 'LookBack', 'py': 'LookBack', 'param': 'LookBack', 'type': 'int', 'default': 20, 'label': 'Lookback period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'Median', 'py': 'Median', 'param': 'Median', 'type': 'int', 'default': 5, 'label': 'Median for adapting', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
pr_haclose = 10
pr_haopen = 11
pr_hahigh = 12
pr_halow = 13
pr_hamedian = 14
pr_hatypical = 15
pr_haweighted = 16
pr_haaverage = 17
pr_hamedianb = 18
pr_hatbiased = 19
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_medianb', 9: 'pr_tbiased', 10: 'pr_haclose', 11: 'pr_haopen', 12: 'pr_hahigh', 13: 'pr_halow', 14: 'pr_hamedian', 15: 'pr_hatypical', 16: 'pr_haweighted', 17: 'pr_haaverage', 18: 'pr_hamedianb', 19: 'pr_hatbiased'})

# ---- inputs and global variables
LookBack = _input('LookBack', 20)  # Lookback period
Price = _input('Price', pr_close)  # Price to use
Median = _input('Median', 5)  # Median for adapting
lf = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
diff = Arr(0, 0.0)
sortDiff = Arr(0, 0.0)
workLagFil = Arr(0, 0.0, dims=(4,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, lf, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, diff, INDICATOR_CALCULATIONS)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArraySize(sortDiff) != Median:
        ArrayResize(sortDiff, Median)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        if i > 0:
            diff[i] = MathAbs(price - lf[i - 1])
        else:
            diff[i] = 0.0
            lf[i] = price
            continue
        hi = diff[i]
        lo = diff[i]
        j = 1
        while j < LookBack and (i - j) >= 0:
            hi = MathMax(hi, diff[i - j])
            lo = MathMin(lo, diff[i - j])
            j += 1
        alpha = 0.0
        if hi != lo:
            j = 0
            while j < Median and (i - j) >= 0:
                sortDiff[j] = _fdiv(diff[i - j] - lo, hi - lo)
                j += 1
            ArraySort(sortDiff)
            if MathMod(Median, 2.0) != 0:
                alpha = sortDiff[_idiv(Median, 2)]
            else:
                alpha = (sortDiff[_idiv(Median, 2)] + sortDiff[_idiv(Median, 2) - 1]) / 2
        lf[i] = iLaGuerreFilter(price, 1 - alpha, rates_total, i, 0)
        if i > 0:
            colorBuffer[i] = colorBuffer[i - 1]
            if lf[i] > lf[i - 1]:
                colorBuffer[i] = 0.0
            if lf[i] < lf[i - 1]:
                colorBuffer[i] = 1.0
    return rates_total

def iLaGuerreFilter(price, gamma, bars, i, instanceNo=0):
    if ArrayRange(workLagFil, 0) != bars:
        ArrayResize(workLagFil, bars)
    instanceNo *= 4
    if price == EMPTY_VALUE:
        return 0.0
    if gamma <= 0:
        return price
    if i > 0:
        workLagFil[i][instanceNo + 0] = ((1.0 - gamma) * price) + (gamma * workLagFil[i - 1][instanceNo + 0])
        workLagFil[i][instanceNo + 1] = ((-gamma) * workLagFil[i][instanceNo + 0]) + workLagFil[i - 1][instanceNo + 0] + (gamma * workLagFil[i - 1][instanceNo + 1])
        workLagFil[i][instanceNo + 2] = ((-gamma) * workLagFil[i][instanceNo + 1]) + workLagFil[i - 1][instanceNo + 1] + (gamma * workLagFil[i - 1][instanceNo + 2])
        workLagFil[i][instanceNo + 3] = ((-gamma) * workLagFil[i][instanceNo + 2]) + workLagFil[i - 1][instanceNo + 2] + (gamma * workLagFil[i - 1][instanceNo + 3])
    else:
        workLagFil[i][instanceNo + 0] = price
        workLagFil[i][instanceNo + 1] = price
        workLagFil[i][instanceNo + 2] = price
        workLagFil[i][instanceNo + 3] = price
    return (workLagFil[i][instanceNo + 0] + (2.0 * workLagFil[i][instanceNo + 1]) + (2.0 * workLagFil[i][instanceNo + 2]) + workLagFil[i][instanceNo + 3]) / 6.0

def getPrice(tprice, open, close, high, low, i, _bars, instanceNo=0):
    if tprice >= pr_haclose:
        if ArrayRange(workHa, 0) != _bars:
            ArrayResize(workHa, _bars)
        r = i
        instanceNo *= 4
        haOpen = 0.0
        if r > 0:
            haOpen = (workHa[r - 1][instanceNo + 2] + workHa[r - 1][instanceNo + 3]) / 2.0
        else:
            haOpen = (open[i] + close[i]) / 2
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[r][instanceNo + 0] = haLow
            workHa[r][instanceNo + 1] = haHigh
        else:
            workHa[r][instanceNo + 0] = haHigh
            workHa[r][instanceNo + 1] = haLow
        workHa[r][instanceNo + 2] = haOpen
        workHa[r][instanceNo + 3] = haClose
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
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdaptiveLaguerreFilterMclassical5(_MQL5Indicator):
    name = 'Adaptive_laguerre_filter_mclassical5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'LookBack': 20,  # Lookback period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=0),  # Price to use
        'Median': 5,  # Median for adapting
    }

