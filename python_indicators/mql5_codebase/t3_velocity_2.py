"""t3_velocity_2 — converted from MQL5: MQL5 Indicators/T3 Velocity V.2.0/t3_velocity_2.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [3329330, 42495], 2: [3329330, 42495]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'T3 velocity histo', 2: 'T3 velocity'}, 'levels': [], 'description': [], 'name': 't3_velocity_2', 'source': 'MQL5 Indicators/T3 Velocity V.2.0/t3_velocity_2.mq5', 'folder': 'T3 Velocity V.2.0', 'inputs': [{'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'double', 'default': 14.0, 'label': 'T3 velocity calculation period', 'sinput': False}, {'mql': 'T3Hot', 'py': 'T3Hot', 'param': 'T3Hot', 'type': 'double', 'default': 1.0, 'label': 'T3 hot value', 'sinput': False}, {'mql': 'T3Original', 'py': 'T3Original', 'param': 'T3Original', 'type': 'bool', 'default': False, 'label': 'T3 original Tillson calculation?', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'ColorNorm', 'py': 'ColorNorm', 'param': 'ColorNorm', 'type': 'int', 'default': 20, 'label': 'Colors normalization period', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 6333684, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Color Up', 'sinput': False}, {'mql': 'ColorSteps', 'py': 'ColorSteps', 'param': 'ColorSteps', 'type': 'int', 'default': 20, 'label': 'Color steps for drawing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
T3Period = _input('T3Period', 14.0)  # T3 velocity calculation period
T3Hot = _input('T3Hot', 1.0)  # T3 hot value
T3Original = _input('T3Original', False)  # T3 original Tillson calculation?
Price = _input('Price', pr_close)  # Price to use
ColorNorm = _input('ColorNorm', 20)  # Colors normalization period
ColorFrom = _input('ColorFrom', clrSandyBrown)  # Color down
ColorTo = _input('ColorTo', clrDeepSkyBlue)  # Color Up
ColorSteps = _input('ColorSteps', 20)  # Color steps for drawing
vel = Arr(0, 0.0)
velh = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
colorBufferh = Arr(0, 0.0)
cSteps = 0
workT3 = Arr(0, 0.0, dims=(12,))
workT3Coeffs = Arr(0, 0.0, dims=(12,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    global cSteps
    SetIndexBuffer(0, velh, INDICATOR_DATA)
    SetIndexBuffer(1, colorBufferh, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vel, INDICATOR_DATA)
    SetIndexBuffer(3, colorBuffer, INDICATOR_COLOR_INDEX)
    cSteps = (ColorSteps if (ColorSteps > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps + 1)
    PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        vel[i] = iT3(price, T3Period, T3Hot, T3Original, i, rates_total, 0) - iT3(price, T3Period, T3Hot / 2.0, T3Original, i, rates_total, 1)
        velh[i] = vel[i]
        min_ = vel[i]
        max_ = vel[i]
        sto = 50.0
        k = 1
        while k < ColorNorm and (i - k) >= 0:
            min_ = MathMin(min_, vel[i - k])
            max_ = MathMax(max_, vel[i - k])
            k += 1
        if max_ != min_:
            sto = _fdiv(100 * (vel[i] - min_), max_ - min_)
        colorBuffer[i] = MathFloor((sto * cSteps) / 100.0)
        colorBufferh[i] = MathFloor((sto * cSteps) / 100.0)
    return rates_total

def iT3(price, period, hot, original, r, bars, instanceNo=0):
    if ArrayRange(workT3, 0) != bars:
        ArrayResize(workT3, bars)
    if ArrayRange(workT3Coeffs, 0) < (instanceNo + 1):
        ArrayResize(workT3Coeffs, instanceNo + 1)
    if workT3Coeffs[instanceNo][0] != period:
        workT3Coeffs[instanceNo][0] = period
        a = hot
        workT3Coeffs[instanceNo][1] = (-a) * a * a
        workT3Coeffs[instanceNo][2] = (3 * a * a) + (3 * a * a * a)
        workT3Coeffs[instanceNo][3] = (-6 * a * a) - (3 * a) - (3 * a * a * a)
        workT3Coeffs[instanceNo][4] = 1 + (3 * a) + (a * a * a) + (3 * a * a)
        if original:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 1.0 + period)
        else:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
    buffer = instanceNo * 6
    if r == 0:
        workT3[r][0 + buffer] = price
        workT3[r][1 + buffer] = price
        workT3[r][2 + buffer] = price
        workT3[r][3 + buffer] = price
        workT3[r][4 + buffer] = price
        workT3[r][5 + buffer] = price
    else:
        workT3[r][0 + buffer] = workT3[r - 1][0 + buffer] + (workT3Coeffs[instanceNo][5] * (price - workT3[r - 1][0 + buffer]))
        workT3[r][1 + buffer] = workT3[r - 1][1 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][0 + buffer] - workT3[r - 1][1 + buffer]))
        workT3[r][2 + buffer] = workT3[r - 1][2 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][1 + buffer] - workT3[r - 1][2 + buffer]))
        workT3[r][3 + buffer] = workT3[r - 1][3 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][2 + buffer] - workT3[r - 1][3 + buffer]))
        workT3[r][4 + buffer] = workT3[r - 1][4 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][3 + buffer] - workT3[r - 1][4 + buffer]))
        workT3[r][5 + buffer] = workT3[r - 1][5 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][4 + buffer] - workT3[r - 1][5 + buffer]))
    return (workT3Coeffs[instanceNo][1] * workT3[r][5 + buffer]) + (workT3Coeffs[instanceNo][2] * workT3[r][4 + buffer]) + (workT3Coeffs[instanceNo][3] * workT3[r][3 + buffer]) + (workT3Coeffs[instanceNo][4] * workT3[r][2 + buffer])

def getPrice(price, open, close, high, low, i, bars, instanceNo=0):
    if price >= pr_haclose:
        if ArrayRange(workHa, 0) != bars:
            ArrayResize(workHa, bars)
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


class T3Velocity2(_MQL5Indicator):
    name = 't3_velocity_2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'T3Period': 14.0,  # T3 velocity calculation period
        'T3Hot': 1.0,  # T3 hot value
        'T3Original': False,  # T3 original Tillson calculation?
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=0),  # Price to use
        'ColorNorm': 20,  # Colors normalization period
        'ColorSteps': 20,  # Color steps for drawing
    }

