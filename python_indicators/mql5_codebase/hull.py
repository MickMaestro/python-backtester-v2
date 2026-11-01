"""hull_ — converted from MQL5: MQL5 Indicators/Hull Moving Average/hull_.mq5

Copyright: mladen; Link: mladen

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladen', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'hull'}, 'levels': [], 'description': [], 'name': 'hull_', 'source': 'MQL5 Indicators/Hull Moving Average/hull_.mq5', 'folder': 'Hull Moving Average', 'inputs': [{'mql': 'HmaLength', 'py': 'HmaLength', 'param': 'HmaLength', 'type': 'double', 'default': 14.0, 'label': 'Hull period', 'sinput': False}, {'mql': 'HmaPower', 'py': 'HmaPower', 'param': 'HmaPower', 'type': 'double', 'default': 1.0, 'label': 'Hull power', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
HmaLength = _input('HmaLength', 14.0)  # Hull period
HmaPower = _input('HmaPower', 1.0)  # Hull power
Price = _input('Price', pr_close)  # Price
hull = Arr(0, 0.0)
colorInd = Arr(0, 0.0)
workLwmp = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, hull, INDICATOR_DATA)
    SetIndexBuffer(1, colorInd, INDICATOR_COLOR_INDEX)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    HalfPeriod = _int(MathFloor(HmaLength / 2))
    HullPeriod = _int(MathFloor(MathSqrt(HmaLength)))
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        price = getPrice(Price, open, close, high, low, rates_total, i)
        hull[i] = iLwmp((2.0 * iLwmp(price, HalfPeriod, HmaPower, rates_total, i, 0)) - iLwmp(price, HmaLength, HmaPower, rates_total, i, 1), HullPeriod, HmaPower, rates_total, i, 2)
        colorInd[i] = colorInd[i - 1]
        if hull[i] > hull[i - 1]:
            colorInd[i] = 0.0
        if hull[i] < hull[i - 1]:
            colorInd[i] = 1.0
    return rates_total

def getPrice(price, open, close, high, low, bars, i):
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

def iLwmp(price, period, power, bars, r, instanceNo=0):
    if ArrayRange(workLwmp, 0) != bars:
        ArrayResize(workLwmp, bars)
    workLwmp[r][instanceNo] = price
    sumw = MathPow(period, power)
    sum_ = sumw * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += MathPow(weight, power)
        sum_ += MathPow(weight, power) * workLwmp[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Hull(_MQL5Indicator):
    name = 'hull_'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HmaLength': 14.0,  # Hull period
        'HmaPower': 1.0,  # Hull power
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=0),  # Price
    }

