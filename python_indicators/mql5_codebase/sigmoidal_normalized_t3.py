"""Sigmoidal normalized T3 — converted from MQL5: MQL5 Indicators/Log Sigmoidal Normalized T3/Sigmoidal normalized T3.mq5

Log sigmoidal normalized T3
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 3329330, 3937500]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'T3'}, 'levels': [], 'description': ['Log sigmoidal normalized T3'], 'name': 'Sigmoidal normalized T3', 'source': 'MQL5 Indicators/Log Sigmoidal Normalized T3/Sigmoidal normalized T3.mq5', 'folder': 'Log Sigmoidal Normalized T3', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'T3 period', 'sinput': False}, {'mql': 'inpHot', 'py': 'inpHot', 'param': 'inpHot', 'type': 'double', 'default': 0.7, 'label': 'T3 "hot"', 'sinput': False}, {'mql': 'inpType', 'py': 'inpType', 'param': 'inpType', 'type': 'int', 'default': 0, 'label': 'T3 type', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpNormalizeLength', 'py': 'inpNormalizeLength', 'param': 'inpNormalizeLength', 'type': 'int', 'default': 30, 'label': 'Normalization length', 'sinput': False}, {'mql': 'inpNormalizeHyperbolic', 'py': 'inpNormalizeHyperbolic', 'param': 'inpNormalizeHyperbolic', 'type': 'bool', 'default': False, 'label': 'Hyperbolic normalization?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # T3 period
inpHot = _input('inpHot', 0.7)  # T3 "hot"
inpType = _input('inpType', t3_tillson)  # T3 type
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpNormalizeLength = _input('inpNormalizeLength', 30)  # Normalization length
inpNormalizeHyperbolic = _input('inpNormalizeHyperbolic', False)  # Hyperbolic normalization?
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
values = Arr(0, 0.0)
workT3 = Arr(0, 0.0, dims=(6,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))
workSma = Arr(0, 0.0, dims=(1,))
workDev = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, values, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Log sigmoidal normalized T3 (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        values[i] = iT3(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, inpHot, inpType == t3_tillson, i, rates_total)
        mean = iSma(values[i], inpNormalizeLength, i, rates_total)
        deviation = iDeviation(values[i], inpNormalizeLength, i, rates_total)
        zeroMean = 0.0
        if deviation != 0:
            zeroMean = _fdiv(values[i] - mean, deviation)
        val[i] = (_fdiv(1.0 - MathExp(-zeroMean), 1.0 + MathExp(-zeroMean)) if inpNormalizeHyperbolic else _fdiv(1.0, 1.0 + MathExp(-zeroMean)))
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iT3(price, period, hot, original, r, bars, copy=False, instanceNo=0):
    if ArrayRange(workT3, 0) != bars:
        ArrayResize(workT3, bars)
    if ArrayRange(workT3Coeffs, 0) < (instanceNo + 1):
        ArrayResize(workT3Coeffs, instanceNo + 1)
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
    if ((not copy) and r > 0) and period > 1:
        workT3[r][0 + buffer] = workT3[r - 1][0 + buffer] + (workT3Coeffs[instanceNo][5] * (price - workT3[r - 1][0 + buffer]))
        workT3[r][1 + buffer] = workT3[r - 1][1 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][0 + buffer] - workT3[r - 1][1 + buffer]))
        workT3[r][2 + buffer] = workT3[r - 1][2 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][1 + buffer] - workT3[r - 1][2 + buffer]))
        workT3[r][3 + buffer] = workT3[r - 1][3 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][2 + buffer] - workT3[r - 1][3 + buffer]))
        workT3[r][4 + buffer] = workT3[r - 1][4 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][3 + buffer] - workT3[r - 1][4 + buffer]))
        workT3[r][5 + buffer] = workT3[r - 1][5 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][4 + buffer] - workT3[r - 1][5 + buffer]))
    return (workT3Coeffs[instanceNo][1] * workT3[r][5 + buffer]) + (workT3Coeffs[instanceNo][2] * workT3[r][4 + buffer]) + (workT3Coeffs[instanceNo][3] * workT3[r][3 + buffer]) + (workT3Coeffs[instanceNo][4] * workT3[r][2 + buffer])

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo + 0] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    return _fdiv(avg, float(k))

def iDeviation(value, length, i, bars, isSample=False):
    if ArraySize(workDev) != bars:
        ArrayResize(workDev, bars)
    workDev[i] = value
    sumx = 0.0
    sumxx = 0.0
    k = 0
    while k < length and (i - k) >= 0:
        pass
        sumx += workDev[i - k]
        sumxx += workDev[i - k] * workDev[i - k]
        k += 1
    return MathSqrt(_fdiv(sumxx - _fdiv(sumx * sumx, length), MathMax(length - isSample, 1)))

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


class SigmoidalNormalizedT3(_MQL5Indicator):
    name = 'Sigmoidal normalized T3'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # T3 period
        'inpHot': 0.7,  # T3 "hot"
        'inpType': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=0),  # T3 type
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpNormalizeLength': 30,  # Normalization length
        'inpNormalizeHyperbolic': False,  # Hyperbolic normalization?
    }

