"""t3_velocity — converted from MQL5: MQL5 Indicators/T3 Velocity/t3_velocity.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [3329330, 9662683], 2: [3329330, 9662683]}, 'widths': {1: 1, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'T3 velocity histo', 2: 'T3 velocity'}, 'levels': [], 'description': [], 'name': 't3_velocity', 'source': 'MQL5 Indicators/T3 Velocity/t3_velocity.mq5', 'folder': 'T3 Velocity', 'inputs': [{'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'double', 'default': 14.0, 'label': 'T3 velocity calculation period', 'sinput': False}, {'mql': 'T3Hot', 'py': 'T3Hot', 'param': 'T3Hot', 'type': 'double', 'default': 1.0, 'label': 'T3 hot value', 'sinput': False}, {'mql': 'T3Original', 'py': 'T3Original', 'param': 'T3Original', 'type': 'bool', 'default': False, 'label': 'T3 original Tillson calculation?', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
T3Period = _input('T3Period', 14.0)  # T3 velocity calculation period
T3Hot = _input('T3Hot', 1.0)  # T3 hot value
T3Original = _input('T3Original', False)  # T3 original Tillson calculation?
Price = _input('Price', pr_close)  # Price to use
vel = Arr(0, 0.0)
velh = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
colorBufferh = Arr(0, 0.0)
workT3 = Arr(0, 0.0, dims=(12,))
workT3Coeffs = Arr(0, 0.0, dims=(12,))

def OnInit():
    SetIndexBuffer(0, velh, INDICATOR_DATA)
    SetIndexBuffer(1, colorBufferh, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vel, INDICATOR_DATA)
    SetIndexBuffer(3, colorBuffer, INDICATOR_COLOR_INDEX)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        vel[i] = iT3(price, T3Period, T3Hot, T3Original, i, rates_total, 0) - iT3(price, T3Period, T3Hot / 2.0, T3Original, i, rates_total, 1)
        velh[i] = vel[i]
        if i > 0:
            colorBuffer[i] = colorBuffer[i - 1]
            colorBufferh[i] = colorBufferh[i - 1]
            if vel[i] > vel[i - 1]:
                colorBuffer[i] = 0.0
            if vel[i] < vel[i - 1]:
                colorBuffer[i] = 1.0
            if vel[i] > 0:
                colorBufferh[i] = 0.0
            if vel[i] < 0:
                colorBufferh[i] = 1.0
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3Velocity(_MQL5Indicator):
    name = 't3_velocity'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'T3Period': 14.0,  # T3 velocity calculation period
        'T3Hot': 1.0,  # T3 hot value
        'T3Original': False,  # T3 original Tillson calculation?
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=0),  # Price to use
    }

