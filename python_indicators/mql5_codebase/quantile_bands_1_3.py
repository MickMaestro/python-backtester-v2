"""Quantile_bands_1.3 — converted from MQL5: MQL5 Indicators/Quantile Bands/Quantile_bands_1.3.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'www.forex-tsd.com', 'copyright': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 1}, 'colors': {1: [11988406], 2: [12901627], 3: [3329330, 6333684], 4: [3329330, 6333684], 5: [11119017]}, 'widths': {3: 3, 4: 3, 5: 2}, 'styles': {}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Middle value'}, 'levels': [], 'description': [], 'name': 'Quantile_bands_1.3', 'source': 'MQL5 Indicators/Quantile Bands/Quantile_bands_1.3.mq5', 'folder': 'Quantile Bands', 'inputs': [{'mql': 'Periods', 'py': 'Periods', 'param': 'Periods', 'type': 'int', 'default': 35, 'label': 'Quantile period', 'sinput': False}, {'mql': 'PriceUp', 'py': 'PriceUp', 'param': 'PriceUp', 'type': 'int', 'default': 2, 'label': 'Price to use for high quantile value', 'sinput': False}, {'mql': 'PriceMid', 'py': 'PriceMid', 'param': 'PriceMid', 'type': 'int', 'default': 4, 'label': 'Price to use for middle quantile value', 'sinput': False}, {'mql': 'PriceDown', 'py': 'PriceDown', 'param': 'PriceDown', 'type': 'int', 'default': 3, 'label': 'Price to use for low quantile value', 'sinput': False}, {'mql': 'UpperBandPercent', 'py': 'UpperBandPercent', 'param': 'UpperBandPercent', 'type': 'double', 'default': 90.0, 'label': 'Upper band percent', 'sinput': False}, {'mql': 'LowerBandPercent', 'py': 'LowerBandPercent', 'param': 'LowerBandPercent', 'type': 'double', 'default': 10.0, 'label': 'Lower band percent', 'sinput': False}, {'mql': 'MedianBandPercent', 'py': 'MedianBandPercent', 'param': 'MedianBandPercent', 'type': 'double', 'default': 50.0, 'label': 'Median percent', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
Periods = _input('Periods', 35)  # Quantile period
PriceUp = _input('PriceUp', pr_high)  # Price to use for high quantile value
PriceMid = _input('PriceMid', pr_median)  # Price to use for middle quantile value
PriceDown = _input('PriceDown', pr_low)  # Price to use for low quantile value
UpperBandPercent = _input('UpperBandPercent', 90.0)  # Upper band percent
LowerBandPercent = _input('LowerBandPercent', 10.0)  # Lower band percent
MedianBandPercent = _input('MedianBandPercent', 50.0)  # Median percent
bufferUp = Arr(0, 0.0)
bufferUpc = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferDnc = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
quantileValues = Arr(0, 0.0, dims=(3,))
quantileArray = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(12,))

def OnInit():
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferUpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(7, bufferDnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, bufferMe, INDICATOR_DATA)
    return 0

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        bufferUp[i] = iQuantile(getPrice(PriceUp, open, close, high, low, i, rates_total, 0), Periods, UpperBandPercent, i, rates_total, 0)
        bufferDn[i] = iQuantile(getPrice(PriceDown, open, close, high, low, i, rates_total, 1), Periods, LowerBandPercent, i, rates_total, 1)
        bufferMe[i] = iQuantile(getPrice(PriceMid, open, close, high, low, i, rates_total, 2), Periods, MedianBandPercent, i, rates_total, 2)
        fupd[i] = bufferMe[i]
        fupu[i] = bufferUp[i]
        fdnu[i] = bufferMe[i]
        fdnd[i] = bufferDn[i]
        if i > 0:
            bufferUpc[i] = bufferUpc[i - 1]
            bufferDnc[i] = bufferDnc[i - 1]
            if bufferUp[i] > bufferUp[i - 1]:
                bufferUpc[i] = 0.0
            if bufferUp[i] < bufferUp[i - 1]:
                bufferUpc[i] = 1.0
            if bufferDn[i] > bufferDn[i - 1]:
                bufferDnc[i] = 0.0
            if bufferDn[i] < bufferDn[i - 1]:
                bufferDnc[i] = 1.0
    return rates_total

def iQuantile(value, period, qp, i, bars, instanceNo=0):
    if ArrayRange(quantileArray, 0) != period:
        ArrayResize(quantileArray, period)
    if ArrayRange(quantileValues, 0) != bars:
        ArrayResize(quantileValues, bars)
    quantileValues[i][instanceNo] = value
    k = 0
    while k < period and (i - k) >= 0:
        quantileArray[k] = quantileValues[i - k][instanceNo]
        k += 1
    ArraySort(quantileArray)
    index = ((period - 1) * qp) / 100.0
    ind = _int(index)
    delta = index - ind
    if ind == NormalizeDouble(index, 5):
        return quantileArray[ind]
    else:
        return ((1.0 - delta) * quantileArray[ind]) + (delta * quantileArray[ind + 1])

def getPrice(tprice, open, close, high, low, i, bars, instanceNo=0):
    if tprice >= pr_haclose:
        if ArrayRange(workHa, 0) != bars:
            ArrayResize(workHa, bars)
        instanceNo *= 4
        r = i
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


class QuantileBands13(_MQL5Indicator):
    name = 'Quantile_bands_1.3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Periods': 35,  # Quantile period
        'PriceUp': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=2),  # Price to use for high quantile value
        'PriceMid': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=4),  # Price to use for middle quantile value
        'PriceDown': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=3),  # Price to use for low quantile value
        'UpperBandPercent': 90.0,  # Upper band percent
        'LowerBandPercent': 10.0,  # Lower band percent
        'MedianBandPercent': 50.0,  # Median percent
    }

