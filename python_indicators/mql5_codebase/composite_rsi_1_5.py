"""Composite_RSI_1_5 — converted from MQL5: MQL5 Indicators/Composite RSI/Composite_RSI_1_5.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8}, 'colors': {1: [16760576, 6333684], 2: [16748574], 3: [12632256], 4: [6333684], 5: [16760576, 6333684, 12632256]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2, 5: 0}, 'labels': {1: 'Composite RSI', 2: 'CompositeRSI level up', 3: 'Composite RSI middle level', 4: 'Composite RSI level down', 5: 'Composite RSI'}, 'levels': [], 'description': [], 'name': 'Composite_RSI_1_5', 'source': 'MQL5 Indicators/Composite RSI/Composite_RSI_1_5.mq5', 'folder': 'Composite RSI', 'inputs': [{'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 14, 'label': 'Rsi calculation period', 'sinput': False}, {'mql': 'RsiDepth', 'py': 'RsiDepth', 'param': 'RsiDepth', 'type': 'int', 'default': 10, 'label': 'Rsi calculation depth', 'sinput': False}, {'mql': 'RsiFast', 'py': 'RsiFast', 'param': 'RsiFast', 'type': 'bool', 'default': False, 'label': 'Use "fast" claculation', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'PriceSmooth', 'py': 'PriceSmooth', 'param': 'PriceSmooth', 'type': 'int', 'default': 9, 'label': 'Price smoothing period', 'sinput': False}, {'mql': 'PriceSmoothMethod', 'py': 'PriceSmoothMethod', 'param': 'PriceSmoothMethod', 'type': 'int', 'default': 3, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'flLookBack', 'py': 'flLookBack', 'param': 'flLookBack', 'type': 'int', 'default': 25, 'label': 'Floating levels look back period', 'sinput': False}, {'mql': 'flLevelUp', 'py': 'flLevelUp', 'param': 'flLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up level %', 'sinput': False}, {'mql': 'flLevelDown', 'py': 'flLevelDown', 'param': 'flLevelDown', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enumAveragesType
avgSma = 0
avgEma = 1
avgSmma = 2
avgLwma = 3
_enum('enumAveragesType', {0: 'avgSma', 1: 'avgEma', 2: 'avgSmma', 3: 'avgLwma'})

# ---- inputs and global variables
RsiPeriod = _input('RsiPeriod', 14)  # Rsi calculation period
RsiDepth = _input('RsiDepth', 10)  # Rsi calculation depth
RsiFast = _input('RsiFast', False)  # Use "fast" claculation
Price = _input('Price', pr_close)  # Price to use
PriceSmooth = _input('PriceSmooth', 9)  # Price smoothing period
PriceSmoothMethod = _input('PriceSmoothMethod', avgLwma)  # Price smoothing method
flLookBack = _input('flLookBack', 25)  # Floating levels look back period
flLevelUp = _input('flLevelUp', 90.0)  # Floating levels up level %
flLevelDown = _input('flLevelDown', 10.0)  # Floating levels down level %
rsi = Arr(0, 0.0)
fillup = Arr(0, 0.0)
filldn = Arr(0, 0.0)
levelup = Arr(0, 0.0)
levelmi = Arr(0, 0.0)
leveldn = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
workCompRsi = Arr(0, 0.0, dims=(26,))
workSma = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, fillup, INDICATOR_DATA)
    SetIndexBuffer(1, filldn, INDICATOR_DATA)
    SetIndexBuffer(2, levelup, INDICATOR_DATA)
    SetIndexBuffer(3, levelmi, INDICATOR_DATA)
    SetIndexBuffer(4, leveldn, INDICATOR_DATA)
    SetIndexBuffer(5, rsi, INDICATOR_DATA)
    SetIndexBuffer(6, colorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Composite RSI (' + _str(RsiPeriod) + ',' + _str(RsiDepth) + ',' + _str(PriceSmooth) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        rsi[i] = iCompRsi(iCustomMa(PriceSmoothMethod, getPrice(Price, open, close, high, low, i, rates_total), PriceSmooth, rates_total, i), RsiPeriod, RsiDepth, RsiFast, rates_total, i, 0)
        min_ = rsi[i]
        max_ = rsi[i]
        k = 1
        while k < flLookBack and (i - k) >= 0:
            min_ = MathMin(rsi[i - k], min_)
            max_ = MathMax(rsi[i - k], max_)
            k += 1
        range_ = max_ - min_
        levelup[i] = min_ + ((flLevelUp * range_) / 100.0)
        leveldn[i] = min_ + ((flLevelDown * range_) / 100.0)
        levelmi[i] = min_ + (0.5 * range_)
        fillup[i] = rsi[i]
        filldn[i] = MathMin(MathMax(rsi[i], leveldn[i]), levelup[i])
        if i > 0:
            colorBuffer[i] = 2.0
            if rsi[i] > levelup[i] or rsi[i] < leveldn[i]:
                if rsi[i] > rsi[i - 1]:
                    colorBuffer[i] = 0.0
                if rsi[i] < rsi[i - 1]:
                    colorBuffer[i] = 1.0
    return rates_total

def iCompRsi(price, period, depth, fast, total, i, instanceNo=0):
    if ArrayRange(workCompRsi, 0) != total:
        ArrayResize(workCompRsi, total)
    alpha = _fdiv(2.0, 1.0 + period)
    if fast:
        alpha = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
    instanceNo *= 26
    depth = MathMin(depth, 25)
    CU = 0.0
    CD = 0.0
    for k in range(0, depth + 1):
        if i == 0:
            workCompRsi[i][instanceNo + k] = price
        else:
            workCompRsi[i][instanceNo + k] = workCompRsi[i - 1][instanceNo + k] + (alpha * (price - workCompRsi[i - 1][instanceNo + k]))
        price = workCompRsi[i][k + instanceNo]
        if k > 0:
            if workCompRsi[i][instanceNo + k - 1] >= workCompRsi[i][instanceNo + k]:
                CU += workCompRsi[i][instanceNo + k - 1] - workCompRsi[i][instanceNo + k]
            else:
                CD += workCompRsi[i][instanceNo + k] - workCompRsi[i][instanceNo + k - 1]
    trsi = 0.0
    if (CU + CD) != 0:
        trsi = _fdiv(CU, CU + CD)
    return trsi

def iCustomMa(mode, price, length, bars, r, instanceNo=0):
    _sw1 = mode
    if _sw1 == avgSma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == avgEma:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == avgSmma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == avgLwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    instanceNo *= 2
    k = 0
    workSma[r][instanceNo + 0] = price
    workSma[r][instanceNo + 1] = price
    k = 1
    while k < period and (r - k) >= 0:
        workSma[r][instanceNo + 1] += workSma[r - k][instanceNo + 0]
        k += 1
    workSma[r][instanceNo + 1] = _fdiv(workSma[r][instanceNo + 1], 1.0 * k)
    return workSma[r][instanceNo + 1]

def iEma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    alpha = _fdiv(2.0, 1.0 + period)
    if r > 0:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    if r < period:
        workSmma[r][instanceNo] = price
    else:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def getPrice(tprice, open, close, high, low, i, _tbars, instanceNo=0):
    if tprice >= pr_haclose:
        if ArrayRange(workHa, 0) != _tbars:
            ArrayResize(workHa, _tbars)
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
        _sw2 = tprice
        if _sw2 == pr_haclose:
            return haClose
        elif _sw2 == pr_haopen:
            return haOpen
        elif _sw2 == pr_hahigh:
            return haHigh
        elif _sw2 == pr_halow:
            return haLow
        elif _sw2 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw2 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw2 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw2 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw2 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw2 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw2 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw3 = tprice
    if _sw3 == pr_close:
        return close[i]
    elif _sw3 == pr_open:
        return open[i]
    elif _sw3 == pr_high:
        return high[i]
    elif _sw3 == pr_low:
        return low[i]
    elif _sw3 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw3 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw3 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw3 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw3 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw3 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw3 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CompositeRSI15(_MQL5Indicator):
    name = 'Composite_RSI_1_5'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'RsiPeriod': 14,  # Rsi calculation period
        'RsiDepth': 10,  # Rsi calculation depth
        'RsiFast': False,  # Use "fast" claculation
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price to use
        'PriceSmooth': 9,  # Price smoothing period
        'PriceSmoothMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=3),  # Price smoothing method
        'flLookBack': 25,  # Floating levels look back period
        'flLevelUp': 90.0,  # Floating levels up level %
        'flLevelDown': 10.0,  # Floating levels down level %
    }

