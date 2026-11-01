"""spearman_rank_autocorrelation — converted from MQL5: MQL5 Indicators/Spearman Rank Autocorrelation/spearman_rank_autocorrelation.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2, 'indicator_minimum': -1.0, 'indicator_maximum': 1.0}, 'types': {1: 7, 2: 1}, 'colors': {1: [3329330, 9662683], 2: [6908265]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Spearman levels', 2: 'Spearman'}, 'levels': [], 'description': [], 'name': 'spearman_rank_autocorrelation', 'source': 'MQL5 Indicators/Spearman Rank Autocorrelation/spearman_rank_autocorrelation.mq5', 'folder': 'Spearman Rank Autocorrelation', 'inputs': [{'mql': 'SpearmanRank', 'py': 'SpearmanRank', 'param': 'SpearmanRank', 'type': 'int', 'default': 14, 'label': 'Spearman rank', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'double', 'default': 0.85, 'label': 'Up level', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'double', 'default': -0.85, 'label': 'Down level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DimGray = 0x696969  # MQL4 colour name

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_haclose = 7
pr_haopen = 8
pr_hahigh = 9
pr_halow = 10
pr_hamedian = 11
pr_hatypical = 12
pr_haweighted = 13
pr_haaverage = 14
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_haclose', 8: 'pr_haopen', 9: 'pr_hahigh', 10: 'pr_halow', 11: 'pr_hamedian', 12: 'pr_hatypical', 13: 'pr_haweighted', 14: 'pr_haaverage'})

# ---- inputs and global variables
SpearmanRank = _input('SpearmanRank', 14)  # Spearman rank
Price = _input('Price', pr_close)  # Price to use
UpLevel = _input('UpLevel', 0.85)  # Up level
DnLevel = _input('DnLevel', -0.85)  # Down level
sr = Arr(0, 0.0)
lvla = Arr(0, 0.0)
lvlb = Arr(0, 0.0)
sort = Arr(0, 0.0, dims=(3,))
prices = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, lvla, INDICATOR_DATA)
    SetIndexBuffer(1, lvlb, INDICATOR_DATA)
    SetIndexBuffer(2, sr, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, DnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, DimGray)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Spearman rank (auto)correlation (' + _str(SpearmanRank) + ',' + DoubleToString(DnLevel, 2) + ',' + DoubleToString(UpLevel, 2) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArraySize(prices) != rates_total:
        ArrayResize(prices, rates_total)
    if ArrayRange(sort, 0) != SpearmanRank:
        ArrayResize(sort, SpearmanRank)
    coef = MathPow(SpearmanRank, 3) - SpearmanRank
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        prices[i] = getPrice(Price, open, close, high, low, i, rates_total)
        k = 0
        while k < SpearmanRank and (i - k) >= 0:
            sort[k][0] = prices[i - k]
            sort[k][1] = k + 1
            k += 1
        SortIt(sort, SpearmanRank)
        sum_ = 0.0
        for k in range(0, SpearmanRank):
            sum_ += MathPow(sort[k][1] - sort[k][2], 2)
        sr[i] = 1.0 - _fdiv(6.0 * sum_, coef)
        lvla[i] = sr[i]
        lvlb[i] = sr[i]
        if sr[i] > UpLevel:
            lvlb[i] = UpLevel
        if sr[i] < DnLevel:
            lvlb[i] = DnLevel
    return rates_total

def getPrice(price, open, close, high, low, i, bars):
    if price >= pr_haclose and price <= pr_haaverage:
        if ArrayRange(workHa, 0) != bars:
            ArrayResize(workHa, bars)
        haOpen = 0.0
        if i > 0:
            haOpen = (workHa[i - 1][2] + workHa[i - 1][3]) / 2.0
        else:
            haOpen = open[i] + close[i]
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][0] = haLow
            workHa[i][1] = haHigh
        else:
            workHa[i][0] = haHigh
            workHa[i][1] = haLow
        workHa[i][2] = haOpen
        workHa[i][3] = haClose
        _sw1 = price
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
        elif _sw1 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw1 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw1 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
    _sw2 = price
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
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

def SortIt(array, Rank):
    size = ArrayRange(array, 0)
    increment = _idiv(size, 2)
    while increment > 0:
        for i in range(increment, Rank):
            j = i
            temp = array[i][0]
            temi = array[i][1]
            while j >= increment and array[j - increment][0] < temp:
                array[j][0] = array[j - increment][0]
                array[j][1] = array[j - increment][1]
                j = j - increment
            array[j][0] = temp
            array[j][1] = temi
        if increment == 2:
            increment = 1
        else:
            increment = _int(increment / 2.2)
    i = 0
    while i < (size - 1):
        array[i][2] = i + 1
        if array[i][0] != array[i + 1][0]:
            i += 1
            continue
        j = 0
        temp = i + 1
        temi = 1.0
        j = i + 1
        while j < size:
            if array[j][0] == array[i][0]:
                temp += j + 1
            else:
                break
            j += 1
            temi += 1
        temp = _fdiv(temp, temi)
        while i < j:
            array[i][2] = temp
            i += 1
        i += 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpearmanRankAutocorrelation(_MQL5Indicator):
    name = 'spearman_rank_autocorrelation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SpearmanRank': 14,  # Spearman rank
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Heiken ashi close', 8: 'Heiken ashi open', 9: 'Heiken ashi high', 10: 'Heiken ashi low', 11: 'Heiken ashi median', 12: 'Heiken ashi typical', 13: 'Heiken ashi weighted', 14: 'Heiken ashi average'}, default=0),  # Price to use
        'UpLevel': 0.85,  # Up level
        'DnLevel': -0.85,  # Down level
    }
    y_range = (-1.0, 1.0)

