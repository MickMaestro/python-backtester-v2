"""vwap_bands — converted from MQL5: MQL5 Indicators/VWAP bands/vwap_bands.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [3329330], 2: [3329330], 3: [3329330], 4: [12632256], 5: [6333684], 6: [6333684], 7: [6333684]}, 'widths': {1: 2, 7: 2}, 'styles': {3: 2, 4: 2, 5: 2}, 'labels': {}, 'levels': [], 'description': [], 'name': 'vwap_bands', 'source': 'MQL5 Indicators/VWAP bands/vwap_bands.mq5', 'folder': 'VWAP bands', 'inputs': [{'mql': 'AvgPeriod', 'py': 'AvgPeriod', 'param': 'AvgPeriod', 'type': 'int', 'default': 20, 'label': 'Volume weighted average period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'UseRealVolume', 'py': 'UseRealVolume', 'param': 'UseRealVolume', 'type': 'bool', 'default': False, 'label': 'Use real volume?', 'sinput': False}, {'mql': 'DeviationSample', 'py': 'DeviationSample', 'param': 'DeviationSample', 'type': 'bool', 'default': False, 'label': 'Deviation with sample correction?', 'sinput': False}, {'mql': 'DeviationMuliplier1', 'py': 'DeviationMuliplier1', 'param': 'DeviationMuliplier1', 'type': 'double', 'default': 1.0, 'label': 'First band(s) deviation', 'sinput': False}, {'mql': 'DeviationMuliplier2', 'py': 'DeviationMuliplier2', 'param': 'DeviationMuliplier2', 'type': 'double', 'default': 2.0, 'label': 'Second band(s) deviation', 'sinput': False}, {'mql': 'DeviationMuliplier3', 'py': 'DeviationMuliplier3', 'param': 'DeviationMuliplier3', 'type': 'double', 'default': 2.5, 'label': 'Third band(s) deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
AvgPeriod = _input('AvgPeriod', 20)  # Volume weighted average period
Price = _input('Price', pr_close)  # Price
UseRealVolume = _input('UseRealVolume', False)  # Use real volume?
DeviationSample = _input('DeviationSample', False)  # Deviation with sample correction?
DeviationMuliplier1 = _input('DeviationMuliplier1', 1.0)  # First band(s) deviation
DeviationMuliplier2 = _input('DeviationMuliplier2', 2.0)  # Second band(s) deviation
DeviationMuliplier3 = _input('DeviationMuliplier3', 2.5)  # Third band(s) deviation
bandm = Arr(0, 0.0)
bandu1 = Arr(0, 0.0)
bandu2 = Arr(0, 0.0)
bandu3 = Arr(0, 0.0)
bandd1 = Arr(0, 0.0)
bandd2 = Arr(0, 0.0)
bandd3 = Arr(0, 0.0)
prices = Arr(0, 0.0)
workDev = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, bandu3, INDICATOR_DATA)
    SetIndexBuffer(1, bandu2, INDICATOR_DATA)
    SetIndexBuffer(2, bandu1, INDICATOR_DATA)
    SetIndexBuffer(3, bandm, INDICATOR_DATA)
    SetIndexBuffer(4, bandd1, INDICATOR_DATA)
    SetIndexBuffer(5, bandd2, INDICATOR_DATA)
    SetIndexBuffer(6, bandd3, INDICATOR_DATA)
    SetIndexBuffer(7, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VWAP bands (' + _str(AvgPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, real_volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = getPrice(Price, open, close, high, low, i, rates_total)
        sum1 = 0.0
        sum2 = 0.0
        deviation = iDeviation(prices[i], AvgPeriod, DeviationSample, i, rates_total)
        k = 0
        while k < AvgPeriod and (i - k) >= 0:
            volume = (float(real_volume[i - k]) if UseRealVolume else float(tick_volume[i - k]))
            sum1 += volume * prices[i - k]
            sum2 += volume
            k += 1
        bandm[i] = (_fdiv(sum1, sum2) if (sum2 != 0) else prices[i])
        bandu1[i] = ((bandm[i] + (DeviationMuliplier1 * deviation)) if (DeviationMuliplier1 > 0) else EMPTY_VALUE)
        bandd1[i] = ((bandm[i] - (DeviationMuliplier1 * deviation)) if (DeviationMuliplier1 > 0) else EMPTY_VALUE)
        bandu2[i] = ((bandm[i] + (DeviationMuliplier2 * deviation)) if (DeviationMuliplier2 > 0) else EMPTY_VALUE)
        bandd2[i] = ((bandm[i] - (DeviationMuliplier2 * deviation)) if (DeviationMuliplier2 > 0) else EMPTY_VALUE)
        bandu3[i] = ((bandm[i] + (DeviationMuliplier3 * deviation)) if (DeviationMuliplier3 > 0) else EMPTY_VALUE)
        bandd3[i] = ((bandm[i] - (DeviationMuliplier3 * deviation)) if (DeviationMuliplier3 > 0) else EMPTY_VALUE)
        i += 1
    return i

def iDeviation(value, length, isSample, i, bars):
    if ArraySize(workDev) != bars:
        ArrayResize(workDev, bars)
    workDev[i] = value
    oldMean = value
    newMean = value
    squares = 0.0
    k = 0
    k = 1
    while k < length and (i - k) >= 0:
        newMean = _fdiv(workDev[i - k] - oldMean, k + 1) + oldMean
        squares += (workDev[i - k] - oldMean) * (workDev[i - k] - newMean)
        oldMean = newMean
        k += 1
    return MathSqrt(_fdiv(squares, MathMax(k - isSample, 1)))

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


class VwapBands(_MQL5Indicator):
    name = 'vwap_bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AvgPeriod': 20,  # Volume weighted average period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'UseRealVolume': False,  # Use real volume?
        'DeviationSample': False,  # Deviation with sample correction?
        'DeviationMuliplier1': 1.0,  # First band(s) deviation
        'DeviationMuliplier2': 2.0,  # Second band(s) deviation
        'DeviationMuliplier3': 2.5,  # Third band(s) deviation
    }

