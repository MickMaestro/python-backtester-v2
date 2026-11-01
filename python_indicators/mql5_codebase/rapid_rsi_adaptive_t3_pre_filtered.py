"""rapid_rsi_adaptive_t3_pre-filtered — converted from MQL5: MQL5 Indicators/Rapid RSI/rapid_rsi_adaptive_t3_pre-filtered.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_minimum': -1.0, 'indicator_maximum': 101.0}, 'types': {1: 8}, 'colors': {1: [3329330, 42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Rapid RSi of adaptive T3'}, 'levels': [], 'description': [], 'name': 'rapid_rsi_adaptive_t3_pre-filtered', 'source': 'MQL5 Indicators/Rapid RSI/rapid_rsi_adaptive_t3_pre-filtered.mq5', 'folder': 'Rapid RSI', 'inputs': [{'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 25, 'label': 'Rsi period', 'sinput': False}, {'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'double', 'default': 15.0, 'label': 'T3 Calculation period', 'sinput': False}, {'mql': 'T3Hot', 'py': 'T3Hot', 'param': 'T3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 hot value', 'sinput': False}, {'mql': 'T3Original', 'py': 'T3Original', 'param': 'T3Original', 'type': 'bool', 'default': True, 'label': 'T3 original Tillson calculation?', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'AdaptivePeriod', 'py': 'AdaptivePeriod', 'param': 'AdaptivePeriod', 'type': 'int', 'default': 25, 'label': 'Period for adapting', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 14053594, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Color Up', 'sinput': False}, {'mql': 'ColorSteps', 'py': 'ColorSteps', 'param': 'ColorSteps', 'type': 'int', 'default': 20, 'label': 'Color steps for drawing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average'})

# ---- inputs and global variables
RsiPeriod = _input('RsiPeriod', 25)  # Rsi period
T3Period = _input('T3Period', 15.0)  # T3 Calculation period
T3Hot = _input('T3Hot', 0.7)  # T3 hot value
T3Original = _input('T3Original', True)  # T3 original Tillson calculation?
Price = _input('Price', pr_close)  # Price to use
AdaptivePeriod = _input('AdaptivePeriod', 25)  # Period for adapting
ColorFrom = _input('ColorFrom', clrOrchid)  # Color down
ColorTo = _input('ColorTo', clrLime)  # Color Up
ColorSteps = _input('ColorSteps', 20)  # Color steps for drawing
rsi = Arr(0, 0.0)
t3 = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
cSteps = 0
workDev = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(4,))
workT3 = Arr(0, 0.0, dims=(6,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))

def OnInit():
    global cSteps
    SetIndexBuffer(0, rsi, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, t3, INDICATOR_CALCULATIONS)
    cSteps = (ColorSteps if (ColorSteps > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        dev = iDeviation(price, iSma(price, AdaptivePeriod, rates_total, i, 0), AdaptivePeriod, rates_total, i)
        avg = iSma(dev, AdaptivePeriod, rates_total, i, 1)
        period = T3Period
        if dev != 0:
            period = _fdiv(T3Period * avg, dev)
        if period < 3:
            period = 3.0
        t3[i] = iT3(price, period, T3Hot, T3Original, i, rates_total, 0)
        up = 0.0
        down = 0.0
        diff = 0.0
        k = 0
        while k < RsiPeriod and (i - k - 1) >= 0:
            diff = t3[i - k] - t3[i - k - 1]
            if diff > 0:
                up += diff
            else:
                down -= diff
            k += 1
        if (up + down) == 0:
            rsi[i] = 50.0
        else:
            rsi[i] = _fdiv(100 * up, up + down)
        colorBuffer[i] = MathFloor((rsi[i] * cSteps) / 100.0)
    return rates_total

def iDeviation(price, dMA, period, totalBars, i):
    if ArrayRange(workDev, 0) != totalBars:
        ArrayResize(workDev, totalBars)
    workDev[i] = price
    dSum = 0.0
    k = 0
    while (i - k) >= 0 and k < period:
        dSum += (workDev[i - k] - dMA) * (workDev[i - k] - dMA)
        k += 1
    return MathSqrt(_fdiv(dSum, period))

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

def getPrice(price, open, close, high, low, i, bars):
    _sw1 = price
    if _sw1 == pr_close:
        return close[i]
    elif _sw1 == pr_open:
        return open[i]
    elif _sw1 == pr_high:
        return high[i]
    elif _sw1 == pr_low:
        return low[i]
    elif _sw1 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw1 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
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


class RapidRsiAdaptiveT3PreFiltered(_MQL5Indicator):
    name = 'rapid_rsi_adaptive_t3_pre-filtered'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'RsiPeriod': 25,  # Rsi period
        'T3Period': 15.0,  # T3 Calculation period
        'T3Hot': 0.7,  # T3 hot value
        'T3Original': True,  # T3 original Tillson calculation?
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=0),  # Price to use
        'AdaptivePeriod': 25,  # Period for adapting
        'ColorSteps': 20,  # Color steps for drawing
    }
    y_range = (-1.0, 101.0)

