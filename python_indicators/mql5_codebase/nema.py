"""Nema — converted from MQL5: MQL5 Indicators/Nema/Nema.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'nema'}, 'levels': [], 'description': [], 'name': 'Nema', 'source': 'MQL5 Indicators/Nema/Nema.mq5', 'folder': 'Nema', 'inputs': [{'mql': 'NemaPeriod', 'py': 'NemaPeriod', 'param': 'NemaPeriod', 'type': 'double', 'default': 14.0, 'label': 'NEMA period', 'sinput': False}, {'mql': 'NemaDepth', 'py': 'NemaDepth', 'param': 'NemaDepth', 'type': 'int', 'default': 1, 'label': 'NEMA depth', 'sinput': False}, {'mql': 'NemaPrice', 'py': 'NemaPrice', 'param': 'NemaPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
NemaPeriod = _input('NemaPeriod', 14.0)  # NEMA period
NemaDepth = _input('NemaDepth', 1)  # NEMA depth
NemaPrice = _input('NemaPrice', pr_close)  # Price
nema = Arr(0, 0.0)
nemac = Arr(0, 0.0)
x = Arr(0, 0.0)
xp = Arr(0, 0.0)
xf = Arr(0, 0.0)
_workNema = Arr(0, 0.0, dims=(51,))
_workNemc = Arr(0, 0.0, dims=(51,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, nema, INDICATOR_DATA)
    SetIndexBuffer(1, nemac, INDICATOR_COLOR_INDEX)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return 0
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        nema[i] = iNema(getPrice(NemaPrice, open, close, high, low, i, rates_total), NemaPeriod, NemaDepth, i, rates_total)
        nemac[i] = ((1 if (nema[i] > nema[i - 1]) else 2 if (nema[i] < nema[i - 1]) else nemac[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iNema(value, period, depth, i, bars, instanceNo=0):
    depth = MathMax(MathMin(depth, 51 - 1), 1)
    cInstance = instanceNo
    instanceNo *= 51
    if ArrayRange(_workNema, 0) != bars:
        ArrayResize(_workNema, bars)
    if ArrayRange(_workNemc, 0) < (cInstance + 1):
        ArrayResize(_workNemc, cInstance + 1)
        _workNemc[cInstance][0] = -1.0
    if _workNemc[cInstance][0] != depth:
        _workNemc[cInstance][0] = depth
        for k in range(1, depth + 1):
            _workNemc[cInstance][k] = _fdiv(factorial(depth), factorial(depth - k) * factorial(k))
    _workNema[i][instanceNo + 50] = value
    if period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        sign = 1.0
        _workNema[i][instanceNo + 50] = 0.0
        k = 0
        while k < depth:
            _workNema[i][instanceNo + k] = ((_workNema[i - 1][instanceNo + k] + (alpha * (value - _workNema[i - 1][instanceNo + k]))) if (i > 0) else value)
            value = _workNema[i][instanceNo + k]
            _workNema[i][instanceNo + 50] += value * sign * _workNemc[cInstance][k + 1]
            k += 1
            sign *= -1
    return _workNema[i][instanceNo + 50]

def factorial(n):
    a = 1.0
    for i in range(1, n + 1):
        a *= i
    return a

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


class Nema(_MQL5Indicator):
    name = 'Nema'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'NemaPeriod': 14.0,  # NEMA period
        'NemaDepth': 1,  # NEMA depth
        'NemaPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
    }

