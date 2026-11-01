"""stochastic_of_adaptive_smoother — converted from MQL5: MQL5 Indicators/Stochastic of Adaptive Smoother/stochastic_of_adaptive_smoother.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 11, 2: 8}, 'colors': {1: [42495], 2: [42495]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Super smoother stochastic', 2: 'Super smoother stochastic'}, 'levels': [10.0, 90.0, 100.0], 'description': [], 'name': 'stochastic_of_adaptive_smoother', 'source': 'MQL5 Indicators/Stochastic of Adaptive Smoother/stochastic_of_adaptive_smoother.mq5', 'folder': 'Stochastic of Adaptive Smoother', 'inputs': [{'mql': 'StochasticPeriod', 'py': 'StochasticPeriod', 'param': 'StochasticPeriod', 'type': 'int', 'default': 25, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'SmoothingPeriod', 'py': 'SmoothingPeriod', 'param': 'SmoothingPeriod', 'type': 'double', 'default': 25.0, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'AdaptivePeriod', 'py': 'AdaptivePeriod', 'param': 'AdaptivePeriod', 'type': 'int', 'default': 25, 'label': 'Period for smoother adapting', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 14053594, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Color Up', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
StochasticPeriod = _input('StochasticPeriod', 25)  # Stochastic period
Price = _input('Price', pr_close)  # Price to use
SmoothingPeriod = _input('SmoothingPeriod', 25.0)  # Smoothing period
AdaptivePeriod = _input('AdaptivePeriod', 25)  # Period for smoother adapting
ColorFrom = _input('ColorFrom', clrOrchid)  # Color down
ColorTo = _input('ColorTo', clrLime)  # Color Up
sto = Arr(0, 0.0)
stohv = Arr(0, 0.0)
stohm = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
colorBufferh = Arr(0, 0.0)
cSteps = 0
ssm = Arr(0, 0.0)
workSmooth = Arr(0, 0.0, dims=(5,))
workDev = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(4,))

def OnInit():
    global cSteps
    SetIndexBuffer(0, stohv, INDICATOR_DATA)
    SetIndexBuffer(1, stohm, INDICATOR_DATA)
    SetIndexBuffer(2, colorBufferh, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, sto, INDICATOR_DATA)
    SetIndexBuffer(4, colorBuffer, INDICATOR_COLOR_INDEX)
    cSteps = (StochasticPeriod if (StochasticPeriod > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps + 1)
    PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArrayRange(ssm, 0) != rates_total:
        ArrayResize(ssm, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        dev = iDeviation(price, iSma(price, AdaptivePeriod, rates_total, i, 0), AdaptivePeriod, rates_total, i)
        avg = iSma(dev, AdaptivePeriod, rates_total, i, 1)
        period = SmoothingPeriod
        if dev != 0:
            period = _fdiv(SmoothingPeriod * avg, dev)
        if period < 3:
            period = 3.0
        ssm[i] = iSmooth(price, period, i, rates_total, 0)
        min_ = ssm[i]
        max_ = ssm[i]
        k = 1
        while k < StochasticPeriod and (i - k) >= 0:
            min_ = (ssm[i - k] if (ssm[i - k] < min_) else min_)
            max_ = (ssm[i - k] if (ssm[i - k] > max_) else max_)
            k += 1
        if (max_ - min_) == 0:
            sto[i] = 50.0
        else:
            sto[i] = _fdiv(100 * (ssm[i] - min_), max_ - min_)
        colorBuffer[i] = MathFloor((sto[i] * cSteps) / 100.0)
        colorBufferh[i] = colorBuffer[i]
        stohv[i] = sto[i]
        stohm[i] = 50.0
    return rates_total

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticOfAdaptiveSmoother(_MQL5Indicator):
    name = 'stochastic_of_adaptive_smoother'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StochasticPeriod': 25,  # Stochastic period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=0),  # Price to use
        'SmoothingPeriod': 25.0,  # Smoothing period
        'AdaptivePeriod': 25,  # Period for smoother adapting
    }

