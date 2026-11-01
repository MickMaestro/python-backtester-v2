"""Laguerre_RSI_with_Laguerre_filter — converted from MQL5: MQL5 Indicators/Laguerre RSI with Laguerre filter/Laguerre_RSI_with_Laguerre_filter.mq5

Copyright: © mladen; Link: mladenfx@gmail.com www.forex-station.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen', 'link': 'mladenfx@gmail.com www.forex-station.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [13823743, 13823743], 2: [9662683], 3: [6908265]}, 'widths': {2: 2}, 'styles': {3: 4}, 'labels': {1: 'No trade zone', 2: 'Laguerre RSI', 3: 'Laguerre filter signal'}, 'levels': [], 'description': [], 'name': 'Laguerre_RSI_with_Laguerre_filter', 'source': 'MQL5 Indicators/Laguerre RSI with Laguerre filter/Laguerre_RSI_with_Laguerre_filter.mq5', 'folder': 'Laguerre RSI with Laguerre filter', 'inputs': [{'mql': 'RsiGamma', 'py': 'RsiGamma', 'param': 'RsiGamma', 'type': 'double', 'default': 0.8, 'label': 'Laguerre RSI gamma', 'sinput': False}, {'mql': 'RsiPrice', 'py': 'RsiPrice', 'param': 'RsiPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'RsiSmoothGamma', 'py': 'RsiSmoothGamma', 'param': 'RsiSmoothGamma', 'type': 'double', 'default': 0.001, 'label': 'Laguerre RSI smooth gamma', 'sinput': False}, {'mql': 'RsiSmoothSpeed', 'py': 'RsiSmoothSpeed', 'param': 'RsiSmoothSpeed', 'type': 'int', 'default': 2, 'label': 'Laguerre RSI smooth speed (min 0, max 6)', 'sinput': False}, {'mql': 'FilterGamma', 'py': 'FilterGamma', 'param': 'FilterGamma', 'type': 'double', 'default': 0.6, 'label': 'Laguerre filter gamma', 'sinput': False}, {'mql': 'FilterSpeed', 'py': 'FilterSpeed', 'param': 'FilterSpeed', 'type': 'int', 'default': 2, 'label': 'Laguerre filter speed (min 0, max 6)', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 0.85, 'label': 'Level up', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 0.15, 'label': 'Level down', 'sinput': False}, {'mql': 'NoTradeZoneVisible', 'py': 'NoTradeZoneVisible', 'param': 'NoTradeZoneVisible', 'type': 'bool', 'default': True, 'label': 'Display no trade zone?', 'sinput': False}, {'mql': 'NoTradeZoneUp', 'py': 'NoTradeZoneUp', 'param': 'NoTradeZoneUp', 'type': 'double', 'default': 0.65, 'label': 'No trade zone up', 'sinput': False}, {'mql': 'NoTradeZoneDown', 'py': 'NoTradeZoneDown', 'param': 'NoTradeZoneDown', 'type': 'double', 'default': 0.35, 'label': 'No trade zone down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
RsiGamma = _input('RsiGamma', 0.8)  # Laguerre RSI gamma
RsiPrice = _input('RsiPrice', 0)  # Price
RsiSmoothGamma = _input('RsiSmoothGamma', 0.001)  # Laguerre RSI smooth gamma
RsiSmoothSpeed = _input('RsiSmoothSpeed', 2)  # Laguerre RSI smooth speed (min 0, max 6)
FilterGamma = _input('FilterGamma', 0.6)  # Laguerre filter gamma
FilterSpeed = _input('FilterSpeed', 2)  # Laguerre filter speed (min 0, max 6)
LevelUp = _input('LevelUp', 0.85)  # Level up
LevelDown = _input('LevelDown', 0.15)  # Level down
NoTradeZoneVisible = _input('NoTradeZoneVisible', True)  # Display no trade zone?
NoTradeZoneUp = _input('NoTradeZoneUp', 0.65)  # No trade zone up
NoTradeZoneDown = _input('NoTradeZoneDown', 0.35)  # No trade zone down
osc = Arr(0, 0.0)
oscs = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
workLagRsi = Arr(0, 0.0, dims=(15,))
workLagFil = Arr(0, 0.0, dims=(8,))
workHa = Arr(0, 0.0, dims=(8,))

def OnInit():
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levd, INDICATOR_DATA)
    SetIndexBuffer(2, osc, INDICATOR_DATA)
    SetIndexBuffer(3, oscs, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, LevelUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, LevelDown)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Laguerre RSI with Laguerre filter(' + _str(RsiGamma) + ',' + _str(FilterGamma) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        osc[i] = LaGuerreRsi(getPrice(RsiPrice, open, close, high, low, i, rates_total), RsiGamma, RsiSmoothGamma, RsiSmoothSpeed, i, rates_total)
        oscs[i] = LaGuerreFil(osc[i], FilterGamma, FilterSpeed, i, rates_total)
        levu[i] = NoTradeZoneUp
        levd[i] = NoTradeZoneDown
    return rates_total

def LaGuerreRsi(price, gamma, smooth, smoothSpeed, i, bars, instanceNo=0):
    if ArrayRange(workLagRsi, 0) != bars:
        ArrayResize(workLagRsi, bars)
    instanceNo *= 5
    workLagRsi[i][instanceNo + 0] = ((((1.0 - gamma) * price) + (gamma * workLagRsi[i - 1][instanceNo + 0])) if (i > 0) else price)
    workLagRsi[i][instanceNo + 1] = ((((-gamma) * workLagRsi[i][instanceNo + 0]) + workLagRsi[i - 1][instanceNo + 0] + (gamma * workLagRsi[i - 1][instanceNo + 1])) if (i > 0) else price)
    workLagRsi[i][instanceNo + 2] = ((((-gamma) * workLagRsi[i][instanceNo + 1]) + workLagRsi[i - 1][instanceNo + 1] + (gamma * workLagRsi[i - 1][instanceNo + 2])) if (i > 0) else price)
    workLagRsi[i][instanceNo + 3] = ((((-gamma) * workLagRsi[i][instanceNo + 2]) + workLagRsi[i - 1][instanceNo + 2] + (gamma * workLagRsi[i - 1][instanceNo + 3])) if (i > 0) else price)
    CU = 0.0
    CD = 0.0
    if i > 0:
        if workLagRsi[i][instanceNo + 0] >= workLagRsi[i][instanceNo + 1]:
            CU = workLagRsi[i][instanceNo + 0] - workLagRsi[i][instanceNo + 1]
        else:
            CD = workLagRsi[i][instanceNo + 1] - workLagRsi[i][instanceNo + 0]
        if workLagRsi[i][instanceNo + 1] >= workLagRsi[i][instanceNo + 2]:
            CU = CU + workLagRsi[i][instanceNo + 1] - workLagRsi[i][instanceNo + 2]
        else:
            CD = CD + workLagRsi[i][instanceNo + 2] - workLagRsi[i][instanceNo + 1]
        if workLagRsi[i][instanceNo + 2] >= workLagRsi[i][instanceNo + 3]:
            CU = CU + workLagRsi[i][instanceNo + 2] - workLagRsi[i][instanceNo + 3]
        else:
            CD = CD + workLagRsi[i][instanceNo + 3] - workLagRsi[i][instanceNo + 2]
    if (CU + CD) != 0:
        workLagRsi[i][instanceNo + 4] = _fdiv(CU, CU + CD)
    else:
        workLagRsi[i][instanceNo + 4] = 0.0
    return LaGuerreFil(workLagRsi[i][instanceNo + 4], smooth, _int(smoothSpeed), i, bars, 1)

def LaGuerreFil(price, gamma, smoothSpeed, i, bars, instanceNo=0):
    if ArrayRange(workLagFil, 0) != bars:
        ArrayResize(workLagFil, bars)
    instanceNo *= 4
    if gamma <= 0:
        return price
    workLagFil[i][instanceNo + 0] = ((((1.0 - gamma) * price) + (gamma * workLagFil[i - 1][instanceNo + 0])) if (i > 0) else price)
    workLagFil[i][instanceNo + 1] = ((((-gamma) * workLagFil[i][instanceNo + 0]) + workLagFil[i - 1][instanceNo + 0] + (gamma * workLagFil[i - 1][instanceNo + 1])) if (i > 0) else price)
    workLagFil[i][instanceNo + 2] = ((((-gamma) * workLagFil[i][instanceNo + 1]) + workLagFil[i - 1][instanceNo + 1] + (gamma * workLagFil[i - 1][instanceNo + 2])) if (i > 0) else price)
    workLagFil[i][instanceNo + 3] = ((((-gamma) * workLagFil[i][instanceNo + 2]) + workLagFil[i - 1][instanceNo + 2] + (gamma * workLagFil[i - 1][instanceNo + 3])) if (i > 0) else price)
    coeffs = Arr.of([0.0, 0.0, 0.0, 0.0], fill=0.0)
    smoothSpeed = MathMax(MathMin(smoothSpeed, 6), 0)
    _sw1 = smoothSpeed
    if _sw1 == 0:
        coeffs[0] = 1.0
        coeffs[1] = 1.0
        coeffs[2] = 1.0
        coeffs[3] = 1.0
    elif _sw1 == 1:
        coeffs[0] = 1.0
        coeffs[1] = 1.0
        coeffs[2] = 2.0
        coeffs[3] = 1.0
    elif _sw1 == 2:
        coeffs[0] = 1.0
        coeffs[1] = 2.0
        coeffs[2] = 2.0
        coeffs[3] = 1.0
    elif _sw1 == 3:
        coeffs[0] = 2.0
        coeffs[1] = 2.0
        coeffs[2] = 2.0
        coeffs[3] = 1.0
    elif _sw1 == 4:
        coeffs[0] = 2.0
        coeffs[1] = 3.0
        coeffs[2] = 2.0
        coeffs[3] = 1.0
    elif _sw1 == 5:
        coeffs[0] = 3.0
        coeffs[1] = 3.0
        coeffs[2] = 2.0
        coeffs[3] = 1.0
    elif _sw1 == 6:
        coeffs[0] = 4.0
        coeffs[1] = 3.0
        coeffs[2] = 2.0
        coeffs[3] = 1.0
    sumc = 0.0
    for k in range(0, 4):
        sumc += coeffs[k]
    return _fdiv((coeffs[0] * workLagFil[i][instanceNo + 0]) + (coeffs[1] * workLagFil[i][instanceNo + 1]) + (coeffs[2] * workLagFil[i][instanceNo + 2]) + (coeffs[3] * workLagFil[i][instanceNo + 3]), sumc)

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


class LaguerreRSIWithLaguerreFilter(_MQL5Indicator):
    name = 'Laguerre_RSI_with_Laguerre_filter'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RsiGamma': 0.8,  # Laguerre RSI gamma
        'RsiPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'RsiSmoothGamma': 0.001,  # Laguerre RSI smooth gamma
        'RsiSmoothSpeed': 2,  # Laguerre RSI smooth speed (min 0, max 6)
        'FilterGamma': 0.6,  # Laguerre filter gamma
        'FilterSpeed': 2,  # Laguerre filter speed (min 0, max 6)
        'LevelUp': 0.85,  # Level up
        'LevelDown': 0.15,  # Level down
        'NoTradeZoneVisible': True,  # Display no trade zone?
        'NoTradeZoneUp': 0.65,  # No trade zone up
        'NoTradeZoneDown': 0.35,  # No trade zone down
    }

