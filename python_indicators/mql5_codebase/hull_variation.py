"""hull_variation — converted from MQL5: MQL5 Indicators/Hull Variation/hull_variation.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Hull'}, 'levels': [], 'description': [], 'name': 'hull_variation', 'source': 'MQL5 Indicators/Hull Variation/hull_variation.mq5', 'folder': 'Hull Variation', 'inputs': [{'mql': 'HullLength', 'py': 'HullLength', 'param': 'HullLength', 'type': 'int', 'default': 27, 'label': 'Hull MA calculaion period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'HullDivisor', 'py': 'HullDivisor', 'param': 'HullDivisor', 'type': 'double', 'default': 1.5, 'label': 'Hull calculation "speed"', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
pr_haclose = 8
pr_haopen = 9
pr_hahigh = 10
pr_halow = 11
pr_hamedian = 12
pr_hatypical = 13
pr_haweighted = 14
pr_haaverage = 15
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_haclose', 9: 'pr_haopen', 10: 'pr_hahigh', 11: 'pr_halow', 12: 'pr_hamedian', 13: 'pr_hatypical', 14: 'pr_haweighted', 15: 'pr_haaverage'})

# ---- inputs and global variables
HullLength = _input('HullLength', 27)  # Hull MA calculaion period
Price = _input('Price', pr_close)  # Price to use
HullDivisor = _input('HullDivisor', 1.5)  # Hull calculation "speed"
hull = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(4,))
workHull = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, hull, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, ' Hull trend (' + _str(HullLength) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        hull[i] = iHull(getPrice(Price, open, close, high, low, i, rates_total), HullLength, HullDivisor, i, rates_total, 0)
        if i > 0:
            colorBuffer[i] = colorBuffer[i - 1]
            if hull[i] > hull[i - 1]:
                colorBuffer[i] = 0.0
            if hull[i] < hull[i - 1]:
                colorBuffer[i] = 1.0
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
    elif _sw2 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    return 0.0

def iHull(price, period, divisor, r, total, instanceNo=0):
    if ArrayRange(workHull, 0) != total:
        ArrayResize(workHull, total)
    HmaPeriod = _int(MathMax(period, 2))
    HalfPeriod = _int(MathFloor(_fdiv(HmaPeriod, divisor)))
    HullPeriod = _int(MathFloor(MathSqrt(HmaPeriod)))
    weight = 0.0
    instanceNo *= 2
    workHull[r][instanceNo] = price
    hmw = HalfPeriod
    hma = hmw * price
    k = 1
    while k < HalfPeriod and (r - k) >= 0:
        weight = HalfPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][instanceNo]
        k += 1
    workHull[r][instanceNo + 1] = _fdiv(2.0 * hma, hmw)
    hmw = HmaPeriod
    hma = hmw * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = HmaPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][instanceNo]
        k += 1
    workHull[r][instanceNo + 1] -= _fdiv(hma, hmw)
    hmw = HullPeriod
    hma = hmw * workHull[r][instanceNo + 1]
    k = 1
    while k < HullPeriod and (r - k) >= 0:
        weight = HullPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][1 + instanceNo]
        k += 1
    return _fdiv(hma, hmw)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HullVariation(_MQL5Indicator):
    name = 'hull_variation'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HullLength': 27,  # Hull MA calculaion period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4', 8: 'Heiken ashi close', 9: 'Heiken ashi open', 10: 'Heiken ashi high', 11: 'Heiken ashi low', 12: 'Heiken ashi median', 13: 'Heiken ashi typical', 14: 'Heiken ashi weighted', 15: 'Heiken ashi average'}, default=0),  # Price to use
        'HullDivisor': 1.5,  # Hull calculation "speed"
    }

