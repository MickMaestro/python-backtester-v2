"""guppy_mma_of_double_smoothed_ema — converted from MQL5: MQL5 Indicators/Guppy MMA of Double Smoothed Ema/guppy_mma_of_double_smoothed_ema.mq5

Copyright: mladen; Link: wwww.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'wwww.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 12}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'guppy_mma_of_double_smoothed_ema', 'source': 'MQL5 Indicators/Guppy MMA of Double Smoothed Ema/guppy_mma_of_double_smoothed_ema.mq5', 'folder': 'Guppy MMA of Double Smoothed Ema', 'inputs': [{'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Starting color for MAs', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 255, 'label': 'Ending color for MAs', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
ColorFrom = _input('ColorFrom', clrLimeGreen)  # Starting color for MAs
ColorTo = _input('ColorTo', clrRed)  # Ending color for MAs
steps = 0
periods = Arr.of([3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60], fill=0)
workDsema = Arr(0, 0.0, dims=(24,))

class simpleMa(MqlObject):
    _q_fields = ('buffer',)
    def __init__(self, *args):
        self.buffer = Arr(0, 0.0)

def OnInit():
    global steps
    steps = ArraySize(periods)
    i = 0
    while i < steps:
        SetIndexBuffer(i, aBuffers[i].buffer, INDICATOR_DATA)
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(i, PLOT_COLOR_INDEXES, 1)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, gradientColor(i, steps, ColorFrom, ColorTo))
        PlotIndexSetString(i, PLOT_LABEL, 'Guppy MA ' + IntegerToString(periods[i]))
        i += 1
    IndicatorSetString(INDICATOR_SHORTNAME, 'Guppy MMA')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        k = 0
        while k < steps:
            aBuffers[k].buffer[i] = iDsema(price, periods[k], i, rates_total, k)
            k += 1
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

def iDsema(price, period, r, bars, instanceNo=0):
    if ArrayRange(workDsema, 0) != bars:
        ArrayResize(workDsema, bars)
    instanceNo *= 2
    alpha = _fdiv(2.0, 1.0 + MathSqrt(period))
    workDsema[r][0 + instanceNo] = workDsema[r - 1][0 + instanceNo] + (alpha * (price - workDsema[r - 1][0 + instanceNo]))
    workDsema[r][1 + instanceNo] = workDsema[r - 1][1 + instanceNo] + (alpha * (workDsema[r][0 + instanceNo] - workDsema[r - 1][1 + instanceNo]))
    return workDsema[r][1 + instanceNo]

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed

def getColor(stepNo, totalSteps, from_, to):
    step = _fdiv(from_ - to, totalSteps - 1.0)
    return _uint(round(from_ - (step * stepNo)))

# ---- global variables initialised from expressions
aBuffers = Arr(12, 0, dyn=False, factory=simpleMa)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GuppyMmaOfDoubleSmoothedEma(_MQL5Indicator):
    name = 'guppy_mma_of_double_smoothed_ema'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=0),  # Price to use
    }

