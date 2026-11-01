"""double_smoothed_ema — converted from MQL5: MQL5 Indicators/Double Smooothed EMA/double_smoothed_ema.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Double smoothed EMA'}, 'levels': [], 'description': [], 'name': 'double_smoothed_ema', 'source': 'MQL5 Indicators/Double Smooothed EMA/double_smoothed_ema.mq5', 'folder': 'Double Smooothed EMA', 'inputs': [{'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'EmaPeriod', 'py': 'EmaPeriod', 'param': 'EmaPeriod', 'type': 'int', 'default': 20, 'label': 'EMA period', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 36095, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Color Up', 'sinput': False}, {'mql': 'ColorSteps', 'py': 'ColorSteps', 'param': 'ColorSteps', 'type': 'int', 'default': 50, 'label': 'Color steps for drawing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
Price = _input('Price', pr_close)  # Price to use
EmaPeriod = _input('EmaPeriod', 20)  # EMA period
ColorFrom = _input('ColorFrom', clrDarkOrange)  # Color down
ColorTo = _input('ColorTo', clrLimeGreen)  # Color Up
ColorSteps = _input('ColorSteps', 50)  # Color steps for drawing
ssm = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
cSteps = 0
totalBars = 0
workEma = Arr(0, 0.0, dims=(2,))

def OnInit():
    global cSteps
    SetIndexBuffer(0, ssm, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    cSteps = (ColorSteps if (ColorSteps > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global totalBars
    totalBars = rates_total
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        ssm[i] = iEma(iEma(getPrice(Price, open, close, high, low, i, rates_total), MathSqrt(EmaPeriod), i, 0), MathSqrt(EmaPeriod), i, 1)
        min_ = ssm[i]
        max_ = ssm[i]
        col = 0.0
        k = 1
        while k < ColorSteps and (i - k) >= 0:
            min_ = (ssm[i - k] if (ssm[i - k] < min_) else min_)
            max_ = (ssm[i - k] if (ssm[i - k] > max_) else max_)
            k += 1
        if (max_ - min_) == 0:
            col = 50.0
        else:
            col = _fdiv(100 * (ssm[i] - min_), max_ - min_)
        colorBuffer[i] = MathFloor((col * cSteps) / 100.0)
    return rates_total

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

def iEma(price, period, r, instanceNo=0):
    if ArrayRange(workEma, 0) != totalBars:
        ArrayResize(workEma, totalBars)
    alpha = _fdiv(2.0, 1.0 + period)
    workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DoubleSmoothedEma(_MQL5Indicator):
    name = 'double_smoothed_ema'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=0),  # Price to use
        'EmaPeriod': 20,  # EMA period
        'ColorSteps': 50,  # Color steps for drawing
    }

