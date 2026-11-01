"""Dema trend — converted from MQL5: MQL5 Indicators/DEMA trend/Dema trend.mq5

DEMA trend
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 11, 2: 8, 3: 8}, 'colors': {1: [11119017, 9639167, 3329330], 2: [11119017, 9639167, 3329330], 3: [11119017, 9639167, 3329330]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Envelope histogram', 2: 'Upper envelope line', 3: 'Lower envelope line'}, 'levels': [], 'description': ['DEMA trend'], 'name': 'Dema trend', 'source': 'MQL5 Indicators/DEMA trend/Dema trend.mq5', 'folder': 'DEMA trend', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 21.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpEnvPeriod', 'py': 'inpEnvPeriod', 'param': 'inpEnvPeriod', 'type': 'int', 'default': 40, 'label': 'Envelopes period', 'sinput': False}, {'mql': 'inpEnvMethod', 'py': 'inpEnvMethod', 'param': 'inpEnvMethod', 'type': 'int', 'default': 3, 'label': 'Envelopes method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 21.0)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpEnvPeriod = _input('inpEnvPeriod', 40)  # Envelopes period
inpEnvMethod = _input('inpEnvMethod', ma_lwma)  # Envelopes method
histou = Arr(0, 0.0)
histod = Arr(0, 0.0)
histoc = Arr(0, 0.0)
valu = Arr(0, 0.0)
valuc = Arr(0, 0.0)
vald = Arr(0, 0.0)
valdc = Arr(0, 0.0)
dema = Arr(0, 0.0)
workDema = Arr(0, 0.0, dims=(2,))
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, histou, INDICATOR_DATA)
    SetIndexBuffer(1, histod, INDICATOR_DATA)
    SetIndexBuffer(2, histoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, valu, INDICATOR_DATA)
    SetIndexBuffer(4, valuc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, vald, INDICATOR_DATA)
    SetIndexBuffer(6, valdc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, dema, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DEMA trend (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        dema[i] = iDema(_price, inpPeriod, i, rates_total)
        valu[i] = iCustomMa(inpEnvMethod, high[i], inpEnvPeriod, i, rates_total, 0)
        vald[i] = iCustomMa(inpEnvMethod, low[i], inpEnvPeriod, i, rates_total, 1)
        valuc[i] = ((2 if (dema[i] > dema[i - 1]) else 1 if (dema[i] < dema[i - 1]) else valuc[i - 1]) if (i > 0) else 0)
        valdc[i] = valuc[i]
        histou[i] = valu[i]
        histod[i] = vald[i]
        histoc[i] = valuc[i]
    return rates_total

def iDema(price, period, r, bars, instanceNo=0):
    if ArrayRange(workDema, 0) != bars:
        ArrayResize(workDema, bars)
    instanceNo *= 2
    workDema[r][0 + instanceNo] = price
    workDema[r][1 + instanceNo] = price
    if r > 0 and period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        workDema[r][0 + instanceNo] = workDema[r - 1][0 + instanceNo] + (alpha * (price - workDema[r - 1][0 + instanceNo]))
        workDema[r][1 + instanceNo] = workDema[r - 1][1 + instanceNo] + (alpha * (workDema[r][0 + instanceNo] - workDema[r - 1][1 + instanceNo]))
    return (workDema[r][0 + instanceNo] * 2.0) - workDema[r][1 + instanceNo]

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period < 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw2 = tprice
        if _sw2 == PRICE_CLOSE:
            return close[i]
        elif _sw2 == PRICE_OPEN:
            return open[i]
        elif _sw2 == PRICE_HIGH:
            return high[i]
        elif _sw2 == PRICE_LOW:
            return low[i]
        elif _sw2 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DemaTrend(_MQL5Indicator):
    name = 'Dema trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 21.0,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpEnvPeriod': 40,  # Envelopes period
        'inpEnvMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=3),  # Envelopes method
    }

