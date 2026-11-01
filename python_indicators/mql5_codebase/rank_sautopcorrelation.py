"""Rank_sautopcorrelation — converted from MQL5: MQL5 Indicators/Rank AutoCorrelation/Rank_sautopcorrelation.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 5, 'indicator_minimum': -1.0, 'indicator_maximum': 1.0}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [3329330, 9662683], 2: [3329330], 3: [12632256], 4: [9662683], 5: [6908265]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'Spearman levels', 2: 'Spearman  level up', 3: 'Spearman  middle level', 4: 'Spearman  level down', 5: 'Spearman'}, 'levels': [], 'description': [], 'name': 'Rank_sautopcorrelation', 'source': 'MQL5 Indicators/Rank AutoCorrelation/Rank_sautopcorrelation.mq5', 'folder': 'Rank AutoCorrelation', 'inputs': [{'mql': 'Rank', 'py': 'Rank', 'param': 'Rank', 'type': 'int', 'default': 32, 'label': 'Rank period', 'sinput': False}, {'mql': 'CorType', 'py': 'CorType', 'param': 'CorType', 'type': 'int', 'default': 0, 'label': 'Correlation type', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'flLookBack', 'py': 'flLookBack', 'param': 'flLookBack', 'type': 'int', 'default': 25, 'label': 'Floating levels look back period (<0 for fixed levels, 0 to use rank period)', 'sinput': False}, {'mql': 'flLevelUp', 'py': 'flLevelUp', 'param': 'flLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up level %', 'sinput': False}, {'mql': 'flLevelDown', 'py': 'flLevelDown', 'param': 'flLevelDown', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enCorrType
cor_spe = 0
cor_pea = 1
_enum('enCorrType', {0: 'cor_spe', 1: 'cor_pea'})

# ---- inputs and global variables
Rank = _input('Rank', 32)  # Rank period
CorType = _input('CorType', cor_spe)  # Correlation type
Price = _input('Price', pr_close)  # Price to use
flLookBack = _input('flLookBack', 25)  # Floating levels look back period (<0 for fixed levels, 0 to use rank period)
flLevelUp = _input('flLevelUp', 90.0)  # Floating levels up level %
flLevelDown = _input('flLevelDown', 10.0)  # Floating levels down level %
sr = Arr(0, 0.0)
levelup = Arr(0, 0.0)
levelmi = Arr(0, 0.0)
leveldn = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(4,))
workPearson = Arr(0, 0.0, dims=(4,))
workSpearman = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, levelup, INDICATOR_DATA)
    SetIndexBuffer(3, levelmi, INDICATOR_DATA)
    SetIndexBuffer(4, leveldn, INDICATOR_DATA)
    SetIndexBuffer(5, sr, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, getCorrelationName(CorType) + ' rank (auto)correlation (' + _str(Rank) + ',' + _str(flLookBack) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    flperiod = flLookBack
    if flperiod == 0:
        flperiod = Rank
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        sr[i] = iCorrelation(CorType, getPrice(Price, open, close, high, low, i, rates_total), Rank, i, rates_total)
        if flperiod > 0:
            min_ = sr[i]
            max_ = sr[i]
            k = 1
            while k < flperiod and (i - k) >= 0:
                min_ = MathMin(sr[i - k], min_)
                max_ = MathMax(sr[i - k], max_)
                k += 1
            range_ = max_ - min_
            levelup[i] = min_ + ((flLevelUp * range_) / 100.0)
            leveldn[i] = min_ + ((flLevelDown * range_) / 100.0)
            levelmi[i] = min_ + (0.5 * range_)
        else:
            levelup[i] = ((2 * flLevelUp) / 100.0) - 1
            leveldn[i] = ((2 * flLevelDown) / 100.0) - 1
            levelmi[i] = (levelup[i] + leveldn[i]) * 0.5
        fill2[i] = sr[i]
        fill1[i] = fill2[i]
        if sr[i] > levelup[i]:
            fill2[i] = levelup[i]
        if sr[i] < leveldn[i]:
            fill2[i] = leveldn[i]
    return rates_total

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

def getCorrelationName(mode):
    _sw3 = mode
    if _sw3 == cor_pea:
        return 'Pearson'
    elif _sw3 == cor_spe:
        return 'Spearman'
    else:
        return ''

def iCorrelation(mode, price, length, r, bars, instanceNo=0):
    _sw4 = mode
    if _sw4 == cor_pea:
        return iPearson(price, _int(length), r, bars, instanceNo)
    elif _sw4 == cor_spe:
        return iSpearman(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iPearson(value, period, i, bars, instanceNo=0):
    if ArrayRange(workPearson, 0) != bars:
        ArrayResize(workPearson, bars)
    workPearson[i][instanceNo] = value
    SumXY = 0.0
    SumXX = 0.0
    SumYY = 0.0
    SumY = 0.0
    SumX = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        val = workPearson[i - k][instanceNo]
        SumX += val
        SumY += k
        SumXX += val * val
        SumYY += k * k
        SumXY += val * k
        k += 1
    SXY = (period * SumXY) - (SumY * SumX)
    SXXYY = ((period * SumXX) - (SumX * SumX)) * ((period * SumYY) - (SumY * SumY))
    result = (_fdiv(-SXY, MathSqrt(MathAbs(SXXYY))) if (SXXYY != 0) else 0)
    return result

def iSpearman(value, period, i, bars, instanceNo=0):
    if ArrayRange(workSpearman, 0) != bars:
        ArrayResize(workSpearman, bars)
    workSpearman[i][instanceNo] = value
    total = 0.0
    data = Arr(0, 0.0)
    ArrayResize(data, period)
    ArrayInitialize(data, 0)
    k = 0
    while k < period and (i - k) >= 0:
        data[k] = workSpearman[i - k][instanceNo]
        k += 1
    for k in range(0, period):
        max_ = ArrayMaximum(data)
        total += (max_ - k) * (max_ - k)
        data[max_] = 0.0
    return 1.0 - _fdiv(6.0 * total, period * ((period * period) - 1.0))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RankSautopcorrelation(_MQL5Indicator):
    name = 'Rank_sautopcorrelation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Rank': 32,  # Rank period
        'CorType': _Choice({0: 'Spearman rank correlation', 1: 'Pearson rank correlation'}, default=0),  # Correlation type
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price to use
        'flLookBack': 25,  # Floating levels look back period (<0 for fixed levels, 0 to use rank period)
        'flLevelUp': 90.0,  # Floating levels up level %
        'flLevelDown': 10.0,  # Floating levels down level %
    }
    y_range = (-1.0, 1.0)

