"""alma_1_1 — converted from MQL5: MQL5 Indicators/ALMA 2.0/alma_1_1.mq5

Copyright: mladen; Link: www.forex-tsd.com; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'version': '1.1', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Alma'}, 'levels': [], 'description': [], 'name': 'alma_1_1', 'source': 'MQL5 Indicators/ALMA 2.0/alma_1_1.mq5', 'folder': 'ALMA 2.0', 'inputs': [{'mql': 'AlmaPeriod', 'py': 'AlmaPeriod', 'param': 'AlmaPeriod', 'type': 'int', 'default': 14, 'label': 'Calculation period', 'sinput': False}, {'mql': 'AlmaPrice', 'py': 'AlmaPrice', 'param': 'AlmaPrice', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'AlmaSigma', 'py': 'AlmaSigma', 'param': 'AlmaSigma', 'type': 'double', 'default': 6.0, 'label': 'Alma sigma', 'sinput': False}, {'mql': 'AlmaSample', 'py': 'AlmaSample', 'param': 'AlmaSample', 'type': 'double', 'default': 0.25, 'label': 'Alma sample', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
AlmaPeriod = _input('AlmaPeriod', 14)  # Calculation period
AlmaPrice = _input('AlmaPrice', pr_close)  # Price to use
AlmaSigma = _input('AlmaSigma', 6.0)  # Alma sigma
AlmaSample = _input('AlmaSample', 0.25)  # Alma sample
MaBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
totalBars = 0
almaWork = Arr(0, 0.0, dims=(1,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, MaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Alma (' + _str(AlmaPeriod) + ',' + _str(AlmaSigma) + _str(AlmaSample) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, TickVolume, Volume, Spread):
    global totalBars
    totalBars = rates_total
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(AlmaPrice, open, close, high, low, rates_total, i)
        MaBuffer[i] = iAlma(price, AlmaPeriod, AlmaSigma, AlmaSample, rates_total, i)
        if i > 0:
            ColorBuffer[i] = ColorBuffer[i - 1]
            if MaBuffer[i] > MaBuffer[i - 1]:
                ColorBuffer[i] = 0.0
            if MaBuffer[i] < MaBuffer[i - 1]:
                ColorBuffer[i] = 1.0
        else:
            ColorBuffer[i] = 0.0
    return rates_total

def iAlma(price, period, sigma, sample, bars, r, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(almaWork, 0) != bars:
        ArrayResize(almaWork, bars)
    almaWork[r][instanceNo] = price
    m = MathFloor(sample * (period - 1.0))
    s = _fdiv(period, sigma)
    sum_ = 0.0
    div = 0.0
    i = 0
    while i < period and (r - i) >= 0:
        coeff = MathExp(_fdiv(-((i - m) * (i - m)), 2.0 * s * s))
        sum_ += coeff * almaWork[r - i][instanceNo]
        div += coeff
        i += 1
    talma = price
    if div != 0:
        talma = _fdiv(sum_, div)
    return talma

def getPrice(price, open, close, high, low, bars, i, instanceNo=0):
    if price >= pr_haclose:
        if ArrayRange(workHa, 0) != bars:
            ArrayResize(workHa, bars)
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


class Alma11(_MQL5Indicator):
    name = 'alma_1_1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AlmaPeriod': 14,  # Calculation period
        'AlmaPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=0),  # Price to use
        'AlmaSigma': 6.0,  # Alma sigma
        'AlmaSample': 0.25,  # Alma sample
    }

