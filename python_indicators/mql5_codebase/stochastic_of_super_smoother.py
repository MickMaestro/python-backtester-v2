"""stochastic_of_super_smoother — converted from MQL5: MQL5 Indicators/Stochastic of Adaptive Super Smoother/stochastic_of_super_smoother.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Super smoother stochastic'}, 'levels': [10.0, 90.0, 100.0], 'description': [], 'name': 'stochastic_of_super_smoother', 'source': 'MQL5 Indicators/Stochastic of Adaptive Super Smoother/stochastic_of_super_smoother.mq5', 'folder': 'Stochastic of Adaptive Super Smoother', 'inputs': [{'mql': 'StochasticPeriod', 'py': 'StochasticPeriod', 'param': 'StochasticPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'SmoothingPeriod', 'py': 'SmoothingPeriod', 'param': 'SmoothingPeriod', 'type': 'double', 'default': 25.0, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'AdaptivePeriod', 'py': 'AdaptivePeriod', 'param': 'AdaptivePeriod', 'type': 'int', 'default': 25, 'label': 'Period for adapting', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Color Up', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
StochasticPeriod = _input('StochasticPeriod', 32)  # Stochastic period
Price = _input('Price', pr_close)  # Price to use
SmoothingPeriod = _input('SmoothingPeriod', 25.0)  # Smoothing period
AdaptivePeriod = _input('AdaptivePeriod', 25)  # Period for adapting
ColorFrom = _input('ColorFrom', clrOrange)  # Color down
ColorTo = _input('ColorTo', clrLimeGreen)  # Color Up
sto = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
cSteps = 0
ssm = Arr(0, 0.0)
workSsm = Arr(0, 0.0, dims=(4,))
workSsmCoeffs = Arr(0, 0.0, dims=(4,))

def OnInit():
    global cSteps
    SetIndexBuffer(0, sto, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    cSteps = (StochasticPeriod if (StochasticPeriod > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArrayRange(ssm, 0) != rates_total:
        ArrayResize(ssm, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        ssm[i] = iSsm(getPrice(Price, open, close, high, low, i, rates_total), SmoothingPeriod, i, rates_total, 0)
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
    return rates_total

def iSsm(price, period, i, bars, instanceNo=0):
    if ArrayRange(workSsm, 0) != bars:
        ArrayResize(workSsm, bars)
    if ArrayRange(workSsmCoeffs, 0) < (instanceNo + 1):
        ArrayResize(workSsmCoeffs, instanceNo + 1)
    if workSsmCoeffs[instanceNo][0] != period:
        workSsmCoeffs[instanceNo][0] = period
        a1 = MathExp(_fdiv(-1.414 * 3.141592653589793, period))
        b1 = 2.0 * a1 * MathCos(_fdiv(1.414 * 3.141592653589793, period))
        workSsmCoeffs[instanceNo][2] = b1
        workSsmCoeffs[instanceNo][3] = (-a1) * a1
        workSsmCoeffs[instanceNo][1] = 1.0 - workSsmCoeffs[instanceNo][2] - workSsmCoeffs[instanceNo][3]
    s = instanceNo * 2
    workSsm[i][s + 0] = price
    if i < 3:
        return workSsm[i][s + 0]
    workSsm[i][s + 1] = ((workSsmCoeffs[instanceNo][1] * (workSsm[i][s + 0] + workSsm[i - 1][s + 0])) / 2.0) + (workSsmCoeffs[instanceNo][2] * workSsm[i - 1][s + 1]) + (workSsmCoeffs[instanceNo][3] * workSsm[i - 2][s + 1])
    return workSsm[i][s + 1]

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


class StochasticOfSuperSmoother(_MQL5Indicator):
    name = 'stochastic_of_super_smoother'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'StochasticPeriod': 32,  # Stochastic period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=0),  # Price to use
        'SmoothingPeriod': 25.0,  # Smoothing period
        'AdaptivePeriod': 25,  # Period for adapting
    }

