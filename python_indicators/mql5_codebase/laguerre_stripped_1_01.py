"""Laguerre stripped 1.01 — converted from MQL5: MQL5 Indicators/Laguerre stripped/Laguerre stripped 1.01.mq5

Copyright: © mladen, 2017; Link: www.forex-station.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017', 'link': 'www.forex-station.com', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 7}, 'types': {1: 7, 2: 7, 3: 7, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [8310016, 8257691], 2: [8303616, 8257716], 3: [8297216, 8257741], 4: [8421504], 5: [8421504], 6: [8421504], 7: [8421504]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Fill 1', 2: 'Fill 2', 3: 'Fill 3', 4: 'Laguerre 1', 5: 'Laguerre 2', 6: 'Laguerre 3', 7: 'Laguerre 4'}, 'levels': [], 'description': [], 'name': 'Laguerre stripped 1.01', 'source': 'MQL5 Indicators/Laguerre stripped/Laguerre stripped 1.01.mq5', 'folder': 'Laguerre stripped', 'inputs': [{'mql': 'Gamma', 'py': 'Gamma', 'param': 'Gamma', 'type': 'double', 'default': 0.75, 'label': 'Gamma', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
Gamma = _input('Gamma', 0.75)  # Gamma
Price = _input('Price', pr_close)  # Price
lagg1u = Arr(0, 0.0)
lagg1d = Arr(0, 0.0)
lagg2u = Arr(0, 0.0)
lagg2d = Arr(0, 0.0)
lagg3u = Arr(0, 0.0)
lagg3d = Arr(0, 0.0)
lagg1 = Arr(0, 0.0)
lagg2 = Arr(0, 0.0)
lagg3 = Arr(0, 0.0)
lagg4 = Arr(0, 0.0)
workLag = Arr(0, 0.0, dims=(4,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, lagg1u, INDICATOR_DATA)
    SetIndexBuffer(1, lagg1d, INDICATOR_DATA)
    SetIndexBuffer(2, lagg2u, INDICATOR_DATA)
    SetIndexBuffer(3, lagg2d, INDICATOR_DATA)
    SetIndexBuffer(4, lagg3u, INDICATOR_DATA)
    SetIndexBuffer(5, lagg3d, INDICATOR_DATA)
    SetIndexBuffer(6, lagg1, INDICATOR_DATA)
    SetIndexBuffer(7, lagg2, INDICATOR_DATA)
    SetIndexBuffer(8, lagg3, INDICATOR_DATA)
    SetIndexBuffer(9, lagg4, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        laga = Box(0.0)
        lagb = Box(0.0)
        lagc = Box(0.0)
        lagd = Box(0.0)
        iLaGuerre(getPrice(Price, open, close, high, low, i, rates_total), Gamma, laga, lagb, lagc, lagd, i, rates_total, 0)
        lagg1[i] = laga.v
        lagg2[i] = lagb.v
        lagg3[i] = lagc.v
        lagg4[i] = lagd.v
        lagg1u[i] = laga.v
        lagg1d[i] = lagb.v
        lagg2u[i] = lagb.v
        lagg2d[i] = lagc.v
        lagg3u[i] = lagc.v
        lagg3d[i] = lagd.v
        i += 1
    return i

def iLaGuerre(price, gamma, val1, val2, val3, val4, i, bars, instanceNo=0):
    if ArrayRange(workLag, 0) != bars:
        ArrayResize(workLag, bars)
    instanceNo *= 4
    gamma = MathMax(MathMin(gamma, 0.99), 0.01)
    if i > 0:
        workLag[i][instanceNo + 0] = ((1.0 - gamma) * price) + (gamma * workLag[i - 1][instanceNo + 0])
        workLag[i][instanceNo + 1] = ((-gamma) * workLag[i][instanceNo + 0]) + workLag[i - 1][instanceNo + 0] + (gamma * workLag[i - 1][instanceNo + 1])
        workLag[i][instanceNo + 2] = ((-gamma) * workLag[i][instanceNo + 1]) + workLag[i - 1][instanceNo + 1] + (gamma * workLag[i - 1][instanceNo + 2])
        workLag[i][instanceNo + 3] = ((-gamma) * workLag[i][instanceNo + 2]) + workLag[i - 1][instanceNo + 2] + (gamma * workLag[i - 1][instanceNo + 3])
    else:
        for k in range(0, 4):
            workLag[i][instanceNo + k] = price
    val1.v = workLag[i][instanceNo + 0]
    val2.v = workLag[i][instanceNo + 1]
    val3.v = workLag[i][instanceNo + 2]
    val4.v = workLag[i][instanceNo + 3]

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


class LaguerreStripped101(_MQL5Indicator):
    name = 'Laguerre stripped 1.01'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Gamma': 0.75,  # Gamma
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
    }

