"""adxvma_1_1 — converted from MQL5: MQL5 Indicators/ADXVMA/adxvma_1_1.mq5

Copyright: mladen; Link: www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Adxvma'}, 'levels': [], 'description': [], 'name': 'adxvma_1_1', 'source': 'MQL5 Indicators/ADXVMA/adxvma_1_1.mq5', 'folder': 'ADXVMA', 'inputs': [{'mql': 'AdxVmaPeriod', 'py': 'AdxVmaPeriod', 'param': 'AdxVmaPeriod', 'type': 'int', 'default': 14, 'label': 'Calculation period', 'sinput': False}, {'mql': 'AdxvmaPrice', 'py': 'AdxvmaPrice', 'param': 'AdxvmaPrice', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
AdxVmaPeriod = _input('AdxVmaPeriod', 14)  # Calculation period
AdxvmaPrice = _input('AdxvmaPrice', pr_close)  # Price to use
MaBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
totalBars = 0
adxvmaWork = Arr(0, 0.0, dims=(7,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, MaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adxvma (' + _str(AdxVmaPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, TickVolume, Volume, Spread):
    global totalBars
    totalBars = rates_total
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(AdxvmaPrice, open, close, high, low, rates_total, i)
        MaBuffer[i] = iAdxvma(price, AdxVmaPeriod, rates_total, i)
        if i > 0:
            ColorBuffer[i] = ColorBuffer[i - 1]
            if MaBuffer[i] > MaBuffer[i - 1]:
                ColorBuffer[i] = 0.0
            if MaBuffer[i] < MaBuffer[i - 1]:
                ColorBuffer[i] = 1.0
        else:
            ColorBuffer[i] = 0.0
    return rates_total

def iAdxvma(price, period, bars, r, instanceNo=0):
    if ArrayRange(adxvmaWork, 0) != bars:
        ArrayResize(adxvmaWork, bars)
    instanceNo *= 7
    adxvmaWork[r][instanceNo + 0] = price
    if r < 1:
        adxvmaWork[r][instanceNo + 6] = adxvmaWork[r][instanceNo + 0]
        return adxvmaWork[r][6]
    tpdm = 0.0
    tmdm = 0.0
    diff = adxvmaWork[r][instanceNo + 0] - adxvmaWork[r - 1][instanceNo + 0]
    if diff > 0:
        tpdm = diff
    else:
        tmdm = -diff
    adxvmaWork[r][instanceNo + 1] = (((AdxVmaPeriod - 1.0) * adxvmaWork[r - 1][instanceNo + 1]) + tpdm) / AdxVmaPeriod
    adxvmaWork[r][instanceNo + 2] = (((AdxVmaPeriod - 1.0) * adxvmaWork[r - 1][instanceNo + 2]) + tmdm) / AdxVmaPeriod
    trueRange = adxvmaWork[r][instanceNo + 1] + adxvmaWork[r][instanceNo + 2]
    tpdi = 0.0
    tmdi = 0.0
    if trueRange > 0:
        tpdi = _fdiv(adxvmaWork[r][instanceNo + 1], trueRange)
        tmdi = _fdiv(adxvmaWork[r][instanceNo + 2], trueRange)
    adxvmaWork[r][instanceNo + 3] = (((AdxVmaPeriod - 1.0) * adxvmaWork[r - 1][instanceNo + 3]) + tpdi) / AdxVmaPeriod
    adxvmaWork[r][instanceNo + 4] = (((AdxVmaPeriod - 1.0) * adxvmaWork[r - 1][instanceNo + 4]) + tmdi) / AdxVmaPeriod
    tout = 0.0
    if (adxvmaWork[r][instanceNo + 3] + adxvmaWork[r][instanceNo + 4]) > 0:
        tout = _fdiv(MathAbs(adxvmaWork[r][instanceNo + 3] - adxvmaWork[r][instanceNo + 4]), adxvmaWork[r][instanceNo + 3] + adxvmaWork[r][instanceNo + 4])
    adxvmaWork[r][instanceNo + 5] = (((AdxVmaPeriod - 1.0) * adxvmaWork[r - 1][instanceNo + 5]) + tout) / AdxVmaPeriod
    thi = MathMax(adxvmaWork[r][instanceNo + 5], adxvmaWork[r - 1][instanceNo + 5])
    tlo = MathMin(adxvmaWork[r][instanceNo + 5], adxvmaWork[r - 1][instanceNo + 5])
    j = 2
    while j < AdxVmaPeriod and (r - j) >= 0:
        thi = MathMax(adxvmaWork[r - j][instanceNo + 5], thi)
        tlo = MathMin(adxvmaWork[r - j][instanceNo + 5], tlo)
        j += 1
    vi = 0.0
    if (thi - tlo) > 0:
        vi = _fdiv(adxvmaWork[r][instanceNo + 5] - tlo, thi - tlo)
    adxvmaWork[r][instanceNo + 6] = (((AdxVmaPeriod - vi) * adxvmaWork[r - 1][instanceNo + 6]) + (vi * adxvmaWork[r][instanceNo + 0])) / AdxVmaPeriod
    return adxvmaWork[r][instanceNo + 6]

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


class Adxvma11(_MQL5Indicator):
    name = 'adxvma_1_1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AdxVmaPeriod': 14,  # Calculation period
        'AdxvmaPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=0),  # Price to use
    }

