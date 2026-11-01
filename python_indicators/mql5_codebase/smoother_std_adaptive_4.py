"""smoother_std_adaptive_4 — converted from MQL5: MQL5 Indicators/Smoother std adaptive/smoother_std_adaptive_4.mq5

Copyright: mladen @ mladenfx@gmail.com; Link: www.forex-station.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen @ mladenfx@gmail.com', 'link': 'www.forex-station.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Smoother std adaptive'}, 'levels': [], 'description': [], 'name': 'smoother_std_adaptive_4', 'source': 'MQL5 Indicators/Smoother std adaptive/smoother_std_adaptive_4.mq5', 'folder': 'Smoother std adaptive', 'inputs': [{'mql': 'SmtPeriod', 'py': 'SmtPeriod', 'param': 'SmtPeriod', 'type': 'double', 'default': 15.0, 'label': 'Calculation period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'AdaptivePeriod', 'py': 'AdaptivePeriod', 'param': 'AdaptivePeriod', 'type': 'int', 'default': 25, 'label': 'Period for adapting', 'sinput': False}, {'mql': 'DeviationType', 'py': 'DeviationType', 'param': 'DeviationType', 'type': 'int', 'default': 0, 'label': 'Deviation calculation type', 'sinput': False}, {'mql': 'ColorSteps', 'py': 'ColorSteps', 'param': 'ColorSteps', 'type': 'int', 'default': 50, 'label': 'Color steps for drawing', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Color Up', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enStdMethods
std_custSam = 0
std_custNos = 1
_enum('enStdMethods', {0: 'std_custSam', 1: 'std_custNos'})

# ---- inputs and global variables
SmtPeriod = _input('SmtPeriod', 15.0)  # Calculation period
Price = _input('Price', pr_close)  # Price to use
AdaptivePeriod = _input('AdaptivePeriod', 25)  # Period for adapting
DeviationType = _input('DeviationType', std_custSam)  # Deviation calculation type
ColorSteps = _input('ColorSteps', 50)  # Color steps for drawing
ColorFrom = _input('ColorFrom', clrOrange)  # Color down
ColorTo = _input('ColorTo', clrLime)  # Color Up
smt = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
cSteps = 0
workDev = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(4,))
workSmooth = Arr(0, 0.0, dims=(5,))
workHa = Arr(0, 0.0, dims=(12,))

def OnInit():
    global cSteps
    SetIndexBuffer(0, smt, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    cSteps = (ColorSteps if (ColorSteps > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        dev = iDeviation(price, AdaptivePeriod, DeviationType == std_custSam, i, rates_total)
        avg = iSma(dev, AdaptivePeriod, rates_total, i, 1)
        period = (MathMax(_fdiv(SmtPeriod * avg, dev), 2) if (dev != 0) else MathMax(SmtPeriod, 1))
        smt[i] = iSmooth(price, period, i, rates_total, 0)
        start = MathMax(i - ColorSteps + 1, 0)
        min_ = smt[ArrayMinimum(smt, start, ColorSteps)]
        max_ = smt[ArrayMaximum(smt, start, ColorSteps)]
        col = (_fdiv(100 * (smt[i] - min_), max_ - min_) if ((max_ - min_) != 0) else 50)
        colorBuffer[i] = MathFloor((col * cSteps) / 100.0)
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

def iSma(price, period, totalBars, r, instanceNo=0):
    if ArrayRange(workSma, 0) != totalBars:
        ArrayResize(workSma, totalBars)
    instanceNo *= 2
    k = 0
    workSma[r][instanceNo] = price
    if r >= period:
        workSma[r][instanceNo + 1] = workSma[r - 1][instanceNo + 1] + _fdiv(workSma[r][instanceNo] - workSma[r - period][instanceNo], period)
    else:
        workSma[r][instanceNo + 1] = 0.0
        k = 0
        while k < period and (r - k) >= 0:
            workSma[r][instanceNo + 1] += workSma[r - k][instanceNo]
            k += 1
        workSma[r][instanceNo + 1] = _fdiv(workSma[r][instanceNo + 1], k)
    return workSma[r][instanceNo + 1]

def iSmooth(price, length, r, bars, instanceNo=0):
    if ArrayRange(workSmooth, 0) != bars:
        ArrayResize(workSmooth, bars)
    instanceNo *= 5
    if r <= 2:
        workSmooth[r][instanceNo] = price
        workSmooth[r][instanceNo + 2] = price
        workSmooth[r][instanceNo + 4] = price
        return price
    alpha = _fdiv(0.45 * (length - 1.0), (0.45 * (length - 1.0)) + 2.0)
    workSmooth[r][instanceNo + 0] = price + (alpha * (workSmooth[r - 1][instanceNo] - price))
    workSmooth[r][instanceNo + 1] = ((price - workSmooth[r][instanceNo]) * (1 - alpha)) + (alpha * workSmooth[r - 1][instanceNo + 1])
    workSmooth[r][instanceNo + 2] = workSmooth[r][instanceNo + 0] + workSmooth[r][instanceNo + 1]
    workSmooth[r][instanceNo + 3] = ((workSmooth[r][instanceNo + 2] - workSmooth[r - 1][instanceNo + 4]) * MathPow(1.0 - alpha, 2)) + (MathPow(alpha, 2) * workSmooth[r - 1][instanceNo + 3])
    workSmooth[r][instanceNo + 4] = workSmooth[r][instanceNo + 3] + workSmooth[r - 1][instanceNo + 4]
    return workSmooth[r][instanceNo + 4]

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

def getColor(stepNo, totalSteps, from_, to):
    stes = float(totalSteps) - 1.0
    step = _fdiv(from_ - to, stes)
    return _uint(round(from_ - (step * stepNo)))

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmootherStdAdaptive4(_MQL5Indicator):
    name = 'smoother_std_adaptive_4'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'SmtPeriod': 15.0,  # Calculation period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price to use
        'AdaptivePeriod': 25,  # Period for adapting
        'DeviationType': _Choice({0: 'Custom - with sample correction', 1: 'Custom - without sample correction'}, default=0),  # Deviation calculation type
        'ColorSteps': 50,  # Color steps for drawing
    }

