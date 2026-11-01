"""Universal_oscillator — converted from MQL5: MQL5 Indicators/UniOscillator/Universal_oscillator.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8}, 'colors': {1: [16748574, 6333684], 2: [16748574], 3: [12632256], 4: [6333684], 5: [12632256, 16748574, 6333684]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2, 5: 0}, 'labels': {1: 'universal oscillator level fill', 2: 'universal oscillator level up', 3: 'universal oscillator middle level', 4: 'universal oscillator level down', 5: 'universal oscillator'}, 'levels': [], 'description': [], 'name': 'Universal_oscillator', 'source': 'MQL5 Indicators/UniOscillator/Universal_oscillator.mq5', 'folder': 'UniOscillator', 'inputs': [{'mql': 'BandEdge', 'py': 'BandEdge', 'param': 'BandEdge', 'type': 'double', 'default': 20.0, 'label': 'Band edge', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 0.8, 'label': 'Upper level', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': -0.8, 'label': 'Lower level', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 2, 'label': 'Color change :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enColorOn
cc_onSlope = 0
cc_onMiddle = 1
cc_onLevels = 2
_enum('enColorOn', {0: 'cc_onSlope', 1: 'cc_onMiddle', 2: 'cc_onLevels'})

# ---- inputs and global variables
BandEdge = _input('BandEdge', 20.0)  # Band edge
Price = _input('Price', pr_close)  # Price to use
LevelUp = _input('LevelUp', 0.8)  # Upper level
LevelDown = _input('LevelDown', -0.8)  # Lower level
ColorOn = _input('ColorOn', cc_onLevels)  # Color change :
unio = Arr(0, 0.0)
levelup = Arr(0, 0.0)
levelmi = Arr(0, 0.0)
leveldn = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
trend = Arr(0, 0.0)
prices = Arr(0, 0.0)
peak = Arr(0, 0.0)
workSsm = Arr(0, 0.0, dims=(2,))
workSsmCoeffs = Arr(0, 0.0, dims=(4,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, levelup, INDICATOR_DATA)
    SetIndexBuffer(3, levelmi, INDICATOR_DATA)
    SetIndexBuffer(4, leveldn, INDICATOR_DATA)
    SetIndexBuffer(5, unio, INDICATOR_DATA)
    SetIndexBuffer(6, trend, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, peak, INDICATOR_CALCULATIONS)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        prices[i] = getPrice(Price, open, close, high, low, i, rates_total)
        if i < 2:
            peak[i] = 0.0
            continue
        whiteNoise = (prices[i] - prices[i - 2]) / 2.0
        filter_ = iSsm(whiteNoise, BandEdge, i, rates_total)
        peak[i] = 0.991 * peak[i - 1]
        if MathAbs(filter_) > peak[i]:
            peak[i] = MathAbs(filter_)
        unio[i] = _fdiv(filter_, peak[i])
        levelup[i] = LevelUp
        levelmi[i] = 0.0
        leveldn[i] = LevelDown
        trend[i] = 0.0
        _sw1 = ColorOn
        if _sw1 == cc_onLevels:
            if unio[i] > levelup[i]:
                trend[i] = 1.0
            if unio[i] < leveldn[i]:
                trend[i] = 2.0
        elif _sw1 == cc_onMiddle:
            if unio[i] > levelmi[i]:
                trend[i] = 1.0
            if unio[i] < levelmi[i]:
                trend[i] = 2.0
        else:
            if i > 0:
                if unio[i] > unio[i - 1]:
                    trend[i] = 1.0
                if unio[i] < unio[i - 1]:
                    trend[i] = 2.0
        fill1[i] = unio[i]
        fill2[i] = unio[i]
        if unio[i] > levelup[i]:
            fill2[i] = levelup[i]
        if unio[i] < leveldn[i]:
            fill2[i] = leveldn[i]
    return rates_total

def iSsm(price, period, i, TotalBars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSsm, 0) != TotalBars:
        ArrayResize(workSsm, TotalBars)
    if ArrayRange(workSsmCoeffs, 0) < (instanceNo + 1):
        ArrayResize(workSsmCoeffs, instanceNo + 1)
    if workSsmCoeffs[instanceNo][0] != period:
        workSsmCoeffs[instanceNo][0] = period
        a1 = MathExp(_fdiv(-1.414 * 3.141592653589793, period))
        b1 = 2.0 * a1 * MathCos(_fdiv(1.414 * 3.141592653589793, period))
        workSsmCoeffs[instanceNo][2] = b1
        workSsmCoeffs[instanceNo][3] = (-a1) * a1
        workSsmCoeffs[instanceNo][1] = 1.0 - workSsmCoeffs[instanceNo][2] - workSsmCoeffs[instanceNo][3]
    s = instanceNo * 2
    workSsm[i][s + 1] = price
    workSsm[i][s + 0] = price
    if i > 1:
        workSsm[i][s + 1] = ((workSsmCoeffs[instanceNo][1] * (workSsm[i][s + 0] + workSsm[i - 1][s + 0])) / 2.0) + (workSsmCoeffs[instanceNo][2] * workSsm[i - 1][s + 1]) + (workSsmCoeffs[instanceNo][3] * workSsm[i - 2][s + 1])
    return workSsm[i][s + 1]

def getPrice(tprice, open, close, high, low, i, _bars, instanceNo=0):
    if tprice >= pr_haclose:
        if ArrayRange(workHa, 0) != _bars:
            ArrayResize(workHa, _bars)
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


class UniversalOscillator(_MQL5Indicator):
    name = 'Universal_oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BandEdge': 20.0,  # Band edge
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price to use
        'LevelUp': 0.8,  # Upper level
        'LevelDown': -0.8,  # Lower level
        'ColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on middle line cross', 2: 'Change color on outer levels cross'}, default=2),  # Color change :
    }

