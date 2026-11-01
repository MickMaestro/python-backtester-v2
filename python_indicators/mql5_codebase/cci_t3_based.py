"""CCI - T3 based — converted from MQL5: MQL5 Indicators/CCI T3 Based/CCI - T3 based.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 3329330, 42495]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'value'}, 'levels': [], 'description': [], 'name': 'CCI - T3 based', 'source': 'MQL5 Indicators/CCI T3 Based/CCI - T3 based.mq5', 'folder': 'CCI T3 Based', 'inputs': [{'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 32, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpCciPrice', 'py': 'inpCciPrice', 'param': 'inpCciPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpT3Hot', 'py': 'inpT3Hot', 'param': 'inpT3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 "hot"', 'sinput': False}, {'mql': 'inpT3Type', 'py': 'inpT3Type', 'param': 'inpT3Type', 'type': 'int', 'default': 1, 'label': 'T3 type', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpSmoothT3Hot', 'py': 'inpSmoothT3Hot', 'param': 'inpSmoothT3Hot', 'type': 'double', 'default': 0.7, 'label': 'Smoothing T3 "hot"', 'sinput': False}, {'mql': 'inpSmoothT3Type', 'py': 'inpSmoothT3Type', 'param': 'inpSmoothT3Type', 'type': 'int', 'default': 1, 'label': 'Smoothing T3 type', 'sinput': False}, {'mql': 'inpLevelUp', 'py': 'inpLevelUp', 'param': 'inpLevelUp', 'type': 'double', 'default': 100.0, 'label': 'Level up', 'sinput': False}, {'mql': 'inpLevelDown', 'py': 'inpLevelDown', 'param': 'inpLevelDown', 'type': 'double', 'default': -100.0, 'label': 'Level down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# ---- inputs and global variables
inpCciPeriod = _input('inpCciPeriod', 32)  # CCI period
inpCciPrice = _input('inpCciPrice', PRICE_TYPICAL)  # Price
inpT3Hot = _input('inpT3Hot', 0.7)  # T3 "hot"
inpT3Type = _input('inpT3Type', t3_fulksmat)  # T3 type
inpSmoothPeriod = _input('inpSmoothPeriod', 10)  # Smoothing period
inpSmoothT3Hot = _input('inpSmoothT3Hot', 0.7)  # Smoothing T3 "hot"
inpSmoothT3Type = _input('inpSmoothT3Type', t3_fulksmat)  # Smoothing T3 type
inpLevelUp = _input('inpLevelUp', 100.0)  # Level up
inpLevelDown = _input('inpLevelDown', -100.0)  # Level down
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
workT3 = Arr(0, 0.0, dims=(12,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))
workEmaDeviation = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI - T3 based (' + _str(inpCciPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = iT3(getPrice(inpCciPrice, open, close, high, low, i, rates_total), inpSmoothPeriod, inpSmoothT3Hot, inpSmoothT3Type == t3_tillson, i, rates_total, 1)
        avg = iT3(_price, inpCciPeriod, inpT3Hot, inpT3Type == t3_tillson, i, rates_total, 0)
        dev = iEmaDeviation(_price, inpCciPeriod, i, rates_total)
        val[i] = (_fdiv(_price - avg, 0.015 * dev) if (dev != 0) else 0)
        levelUp[i] = inpLevelUp
        levelDn[i] = inpLevelDown
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

def iT3(price, period, hot, original, r, bars, instanceNo=0):
    if ArrayRange(workT3, 0) != bars:
        ArrayResize(workT3, bars)
    if ArrayRange(workT3Coeffs, 0) < (instanceNo + 1):
        ArrayResize(workT3Coeffs, instanceNo + 1)
    if period <= 1:
        return price
    if workT3Coeffs[instanceNo][0] != period:
        workT3Coeffs[instanceNo][0] = period
        workT3Coeffs[instanceNo][1] = (-hot) * hot * hot
        workT3Coeffs[instanceNo][2] = (3 * hot * hot) + (3 * hot * hot * hot)
        workT3Coeffs[instanceNo][3] = (-6 * hot * hot) - (3 * hot) - (3 * hot * hot * hot)
        workT3Coeffs[instanceNo][4] = 1 + (3 * hot) + (hot * hot * hot) + (3 * hot * hot)
        if original:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 1.0 + period)
        else:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
    buffer = instanceNo * 6
    for k in range(0, 6):
        workT3[r][k + buffer] = (workT3[r - 1][k + buffer] if (r > 0) else price)
    if r > 0 and period > 1:
        workT3[r][0 + buffer] = workT3[r - 1][0 + buffer] + (workT3Coeffs[instanceNo][5] * (price - workT3[r - 1][0 + buffer]))
        workT3[r][1 + buffer] = workT3[r - 1][1 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][0 + buffer] - workT3[r - 1][1 + buffer]))
        workT3[r][2 + buffer] = workT3[r - 1][2 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][1 + buffer] - workT3[r - 1][2 + buffer]))
        workT3[r][3 + buffer] = workT3[r - 1][3 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][2 + buffer] - workT3[r - 1][3 + buffer]))
        workT3[r][4 + buffer] = workT3[r - 1][4 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][3 + buffer] - workT3[r - 1][4 + buffer]))
        workT3[r][5 + buffer] = workT3[r - 1][5 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][4 + buffer] - workT3[r - 1][5 + buffer]))
    return (workT3Coeffs[instanceNo][1] * workT3[r][5 + buffer]) + (workT3Coeffs[instanceNo][2] * workT3[r][4 + buffer]) + (workT3Coeffs[instanceNo][3] * workT3[r][3 + buffer]) + (workT3Coeffs[instanceNo][4] * workT3[r][2 + buffer])

def iEmaDeviation(price, period, i, bars, instanceNo=0):
    if ArrayRange(workEmaDeviation, 0) != bars:
        ArrayResize(workEmaDeviation, bars)
    instanceNo *= 2
    workEmaDeviation[i][instanceNo + 0] = price
    workEmaDeviation[i][instanceNo + 1] = price
    if i > 0 and period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        workEmaDeviation[i][instanceNo + 0] = workEmaDeviation[i - 1][instanceNo + 0] + (alpha * (price - workEmaDeviation[i - 1][instanceNo + 0]))
        workEmaDeviation[i][instanceNo + 1] = workEmaDeviation[i - 1][instanceNo + 1] + (alpha * ((price * price) - workEmaDeviation[i - 1][instanceNo + 1]))
    return MathSqrt(_fdiv(period * (workEmaDeviation[i][instanceNo + 1] - (workEmaDeviation[i][instanceNo + 0] * workEmaDeviation[i][instanceNo + 0])), MathMax(period - 1, 1)))

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIT3Based(_MQL5Indicator):
    name = 'CCI - T3 based'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCciPeriod': 32,  # CCI period
        'inpCciPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpT3Hot': 0.7,  # T3 "hot"
        'inpT3Type': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=1),  # T3 type
        'inpSmoothPeriod': 10,  # Smoothing period
        'inpSmoothT3Hot': 0.7,  # Smoothing T3 "hot"
        'inpSmoothT3Type': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=1),  # Smoothing T3 type
        'inpLevelUp': 100.0,  # Level up
        'inpLevelDown': -100.0,  # Level down
    }

