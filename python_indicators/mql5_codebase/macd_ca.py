"""MACD_ca — converted from MQL5: MQL5 Indicators/MACD ca/MACD_ca.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [8421504, 3329330, 6333684], 2: [8421504, 3329330, 6333684]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'MACD', 2: 'corrected macd'}, 'levels': [], 'description': [], 'name': 'MACD_ca', 'source': 'MQL5 Indicators/MACD ca/MACD_ca.mq5', 'folder': 'MACD ca', 'inputs': [{'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'CorrectionPeriod', 'py': 'CorrectionPeriod', 'param': 'CorrectionPeriod', 'type': 'int', 'default': 0, 'label': 'Correction period (<0 no correction =0 same as slow EMA)', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 2, 'label': 'Color change on :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
cc_onZero = 1
cc_onOrig = 2
_enum('enColorOn', {0: 'cc_onSlope', 1: 'cc_onZero', 2: 'cc_onOrig'})

# ---- inputs and global variables
FastEMA = _input('FastEMA', 12)  # Fast EMA period
SlowEMA = _input('SlowEMA', 26)  # Slow EMA period
CorrectionPeriod = _input('CorrectionPeriod', 0)  # Correction period (<0 no correction =0 same as slow EMA)
Price = _input('Price', pr_close)  # Price
ColorOn = _input('ColorOn', cc_onOrig)  # Color change on :
macd = Arr(0, 0.0)
macdc = Arr(0, 0.0)
corrm = Arr(0, 0.0)
corrmc = Arr(0, 0.0)
workDev = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(2,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, macd, INDICATOR_DATA)
    SetIndexBuffer(1, macdc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, corrm, INDICATOR_DATA)
    SetIndexBuffer(3, corrmc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, '"Corrected" MACD (' + _str(FastEMA) + ',' + _str(SlowEMA) + ',' + _str(CorrectionPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    deviationsPeriod = (CorrectionPeriod if (CorrectionPeriod > 0) else 0 if (CorrectionPeriod < 0) else SlowEMA)
    colorOn = (ColorOn if (deviationsPeriod > 0) else ColorOn if (ColorOn != cc_onOrig) else cc_onSlope)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        macd[i] = iEma(price, FastEMA, i, rates_total, 0) - iEma(price, SlowEMA, i, rates_total, 1)
        v1 = MathPow(iDeviation(macd[i], deviationsPeriod, False, i, rates_total), 2)
        v2 = (MathPow(corrm[i - 1] - macd[i], 2) if (i > 0) else 0)
        c = (0 if (v2 < v1 or v2 == 0) else (1 - _fdiv(v1, v2)))
        corrm[i] = ((corrm[i - 1] + (c * (macd[i] - corrm[i - 1]))) if (i > 0) else macd[i])
        macdc[i] = ((1 if (macd[i] > macd[i - 1]) else 2 if (macd[i] < macd[i - 1]) else macdc[i - 1]) if (i > 0) else 0)
        _sw1 = colorOn
        if _sw1 == cc_onOrig:
            corrmc[i] = (1 if (corrm[i] < macd[i]) else 2 if (corrm[i] > macd[i]) else corrmc[i - 1] if (i > 0) else 0)
        elif _sw1 == cc_onZero:
            corrmc[i] = (1 if (corrm[i] > 0) else 2 if (corrm[i] < 0) else corrmc[i - 1] if (i > 0) else 0)
        else:
            corrmc[i] = ((1 if (corrm[i] > corrm[i - 1]) else 2 if (corrm[i] < corrm[i - 1]) else corrmc[i - 1]) if (i > 0) else 0)
        i += 1
    return rates_total

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

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

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


class MACDCa(_MQL5Indicator):
    name = 'MACD_ca'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastEMA': 12,  # Fast EMA period
        'SlowEMA': 26,  # Slow EMA period
        'CorrectionPeriod': 0,  # Correction period (<0 no correction =0 same as slow EMA)
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'ColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color zero cross', 2: 'Change color original macd value cross'}, default=2),  # Color change on :
    }

