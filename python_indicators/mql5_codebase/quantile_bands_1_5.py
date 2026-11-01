"""Quantile_bands_1.5 — converted from MQL5: MQL5 Indicators/Quantile bands - 1.5/Quantile_bands_1.5.mq5

Copyright: © mladen, 2017; Link: www.forex-station.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017', 'link': 'www.forex-station.com', 'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 8}, 'colors': {1: [13628367], 2: [12052223], 3: [12632256, 3329330, 36095], 4: [12632256, 3329330, 36095], 5: [12632256, 3329330, 36095]}, 'widths': {5: 4}, 'styles': {}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Middle value'}, 'levels': [], 'description': [], 'name': 'Quantile_bands_1.5', 'source': 'MQL5 Indicators/Quantile bands - 1.5/Quantile_bands_1.5.mq5', 'folder': 'Quantile bands - 1.5', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'Periods', 'py': 'Periods', 'param': 'Periods', 'type': 'int', 'default': 35, 'label': 'Quantile period', 'sinput': False}, {'mql': 'PriceUp', 'py': 'PriceUp', 'param': 'PriceUp', 'type': 'int', 'default': 2, 'label': 'Price to use for high quantile value', 'sinput': False}, {'mql': 'PriceMid', 'py': 'PriceMid', 'param': 'PriceMid', 'type': 'int', 'default': 4, 'label': 'Price to use for middle quantile value', 'sinput': False}, {'mql': 'PriceDown', 'py': 'PriceDown', 'param': 'PriceDown', 'type': 'int', 'default': 3, 'label': 'Price to use for low quantile value', 'sinput': False}, {'mql': 'UpperBandPercent', 'py': 'UpperBandPercent', 'param': 'UpperBandPercent', 'type': 'double', 'default': 90.0, 'label': 'Upper band percent', 'sinput': False}, {'mql': 'MedianBandPercent', 'py': 'MedianBandPercent', 'param': 'MedianBandPercent', 'type': 'double', 'default': 50.0, 'label': 'Middle band percent', 'sinput': False}, {'mql': 'LowerBandPercent', 'py': 'LowerBandPercent', 'param': 'LowerBandPercent', 'type': 'double', 'default': 10.0, 'label': 'Lower band percent', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter
MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

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
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
Periods = _input('Periods', 35)  # Quantile period
PriceUp = _input('PriceUp', pr_high)  # Price to use for high quantile value
PriceMid = _input('PriceMid', pr_median)  # Price to use for middle quantile value
PriceDown = _input('PriceDown', pr_low)  # Price to use for low quantile value
UpperBandPercent = _input('UpperBandPercent', 90.0)  # Upper band percent
MedianBandPercent = _input('MedianBandPercent', 50.0)  # Middle band percent
LowerBandPercent = _input('LowerBandPercent', 10.0)  # Lower band percent
Interpolate = _input('Interpolate', True)  # Interpolate in multi time frame mode?
bufferUp = Arr(0, 0.0)
bufferUpc = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferDnc = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
bufferMec = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
quantileValues = Arr(0, 0.0, dims=(3,))
quantileArray = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(12,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global timeFrame
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferUpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(7, bufferDnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, bufferMe, INDICATOR_DATA)
    SetIndexBuffer(9, bufferMec, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(10, count, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(Period(), TimeFrame)
    return 0

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _mtfHandle
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if timeFrame != Period():
        result = Arr(0, 0.0)
        currTime = Arr(0, 0)
        nextTime = Arr(0, 0)
        if not timeFrameCheck(timeFrame, time):
            return 0
        if _mtfHandle == INVALID_HANDLE:
            _mtfHandle = iCustom(Symbol(), timeFrame, getName(), PERIOD_CURRENT, Periods, PriceUp, PriceMid, PriceDown, UpperBandPercent, MedianBandPercent, LowerBandPercent)
        if _mtfHandle == INVALID_HANDLE:
            return 0
        if CopyBuffer(_mtfHandle, 7, 0, 1, result) == -1:
            return 0
        k = 0
        n = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _idiv(_int(result[0]) * PeriodSeconds(timeFrame), PeriodSeconds(Period())) - 1, 0))
        while i < rates_total:
            if CopyBuffer(_mtfHandle, 4, _DT(time[i]), 1, result) == -1:
                break
            bufferUp[i] = result[0]
            if CopyBuffer(_mtfHandle, 5, _DT(time[i]), 1, result) == -1:
                break
            bufferUpc[i] = result[0]
            if CopyBuffer(_mtfHandle, 6, _DT(time[i]), 1, result) == -1:
                break
            bufferDn[i] = result[0]
            if CopyBuffer(_mtfHandle, 7, _DT(time[i]), 1, result) == -1:
                break
            bufferDnc[i] = result[0]
            if CopyBuffer(_mtfHandle, 8, _DT(time[i]), 1, result) == -1:
                break
            bufferMe[i] = result[0]
            if CopyBuffer(_mtfHandle, 9, _DT(time[i]), 1, result) == -1:
                break
            bufferMec[i] = result[0]
            fupd[i] = bufferMe[i]
            fupu[i] = bufferUp[i]
            fdnu[i] = bufferMe[i]
            fdnd[i] = bufferDn[i]
            if not Interpolate:
                i += 1
                continue
            CopyTime(Symbol(), timeFrame, _DT(time[i]), 1, currTime)
            if i < (rates_total - 1):
                CopyTime(Symbol(), timeFrame, _DT(time[i + 1]), 1, nextTime)
                if currTime[0] == nextTime[0]:
                    i += 1
                    continue
            n = 1
            while (i - n) > 0 and time[i - n] >= currTime[0]:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                bufferMe[i - k] = bufferMe[i] + _fdiv((bufferMe[i - n] - bufferMe[i]) * k, n)
                bufferMe[i - k] = bufferMe[i] + _fdiv((bufferMe[i - n] - bufferMe[i]) * k, n)
                bufferDn[i - k] = bufferDn[i] + _fdiv((bufferDn[i - n] - bufferDn[i]) * k, n)
                fupd[i - k] = bufferMe[i - k]
                fupu[i - k] = bufferUp[i - k]
                fdnu[i - k] = bufferMe[i - k]
                fdnd[i - k] = bufferDn[i - k]
                k += 1
            i += 1
        return i
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        prices = Arr(3, 0.0, dyn=False)
        prices[0] = getPrice(PriceUp, open, close, high, low, i, rates_total, 0)
        prices[1] = getPrice(PriceDown, open, close, high, low, i, rates_total, 1)
        prices[2] = getPrice(PriceMid, open, close, high, low, i, rates_total, 2)
        ArraySort(prices)
        bufferUp[i] = iQuantile(prices[2], Periods, UpperBandPercent, i, rates_total, 0)
        bufferMe[i] = iQuantile(prices[1], Periods, MedianBandPercent, i, rates_total, 2)
        bufferDn[i] = iQuantile(prices[0], Periods, LowerBandPercent, i, rates_total, 1)
        fupd[i] = bufferMe[i]
        fupu[i] = bufferUp[i]
        fdnu[i] = bufferMe[i]
        fdnd[i] = bufferDn[i]
        bufferUpc[i] = ((1 if (bufferUp[i] > bufferUp[i - 1]) else 2 if (bufferUp[i] < bufferUp[i - 1]) else bufferUpc[i - 1]) if (i > 0) else 0)
        bufferDnc[i] = ((1 if (bufferDn[i] > bufferDn[i - 1]) else 2 if (bufferDn[i] < bufferDn[i - 1]) else bufferDnc[i - 1]) if (i > 0) else 0)
        bufferMec[i] = (1 if (bufferUpc[i] == 1 and bufferDnc[i] == 1) else 2 if (bufferUpc[i] == 2 and bufferDnc[i] == 2) else 0)
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
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
    return ((1.0 - delta) * quantileArray[ind]) + (delta * quantileArray[ind + 1])

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

def getName():
    path = MQL5InfoString(MQL5_PROGRAM_PATH)
    data = TerminalInfoString(TERMINAL_DATA_PATH) + '\\MQL5\\Indicators\\'
    name = StringSubstr(path, StringLen(data))
    return name

def getIndicatorName():
    path = MQL5InfoString(MQL5_PROGRAM_PATH)
    data = TerminalInfoString(TERMINAL_DATA_PATH) + '\\MQL5\\Indicators\\'
    name = StringSubstr(path, StringLen(data))
    return name

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsStr[i]

def timeFrameCheck(_timeFrame, time):
    global _s_timeFrameCheck_warned
    if time[0] < SeriesInfoInteger(Symbol(), _timeFrame, SERIES_FIRSTDATE):
        startTime = Box(0)
        testTime = Arr(0, 0)
        if SeriesInfoInteger(Symbol(), PERIOD_M1, SERIES_TERMINAL_FIRSTDATE, startTime):
            if startTime.v > 0:
                CopyTime(Symbol(), _timeFrame, _DT(time[0]), 1, testTime)
                SeriesInfoInteger(Symbol(), _timeFrame, SERIES_FIRSTDATE, startTime)
        if startTime.v <= 0 or startTime.v > time[0]:
            Comment(MQL5InfoString(MQL5_PROGRAM_NAME) + '\nMissing data for ' + timeFrameToString(_timeFrame) + ' time frame\nRe-trying on next tick')
            _s_timeFrameCheck_warned = True
            return False
    if _s_timeFrameCheck_warned:
        Comment('')
        _s_timeFrameCheck_warned = False
    return True

# ---- static local variables
_s_timeFrameCheck_warned = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class QuantileBands15(_MQL5Indicator):
    name = 'Quantile_bands_1.5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'Periods': 35,  # Quantile period
        'PriceUp': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=2),  # Price to use for high quantile value
        'PriceMid': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=4),  # Price to use for middle quantile value
        'PriceDown': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=3),  # Price to use for low quantile value
        'UpperBandPercent': 90.0,  # Upper band percent
        'MedianBandPercent': 50.0,  # Middle band percent
        'LowerBandPercent': 10.0,  # Lower band percent
        'Interpolate': True,  # Interpolate in multi time frame mode?
    }

