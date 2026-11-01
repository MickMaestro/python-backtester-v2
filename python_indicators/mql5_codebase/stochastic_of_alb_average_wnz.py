"""Stochastic of alb average - wnz — converted from MQL5: MQL5 Indicators/Stochastic of alb - wnz/Stochastic of alb average - wnz.mq5

Stochastic of adaptive lookback average - with normalized zones
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [15128749, 12180223], 2: [11119017], 3: [11119017, 16760576, 6333684]}, 'widths': {3: 3}, 'styles': {2: 2}, 'labels': {1: 'Normalized zones', 2: 'Normalized stochastic', 3: 'Stochastic'}, 'levels': [], 'description': ['Stochastic of adaptive lookback average - with normalized zones'], 'name': 'Stochastic of alb average - wnz', 'source': 'MQL5 Indicators/Stochastic of alb - wnz/Stochastic of alb average - wnz.mq5', 'folder': 'Stochastic of alb - wnz', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Stochastic  period', 'sinput': False}, {'mql': 'inpSlowing', 'py': 'inpSlowing', 'param': 'inpSlowing', 'type': 'int', 'default': 3, 'label': 'Stochastic slowing/smoothing period', 'sinput': False}, {'mql': 'inpAlbSwingCount', 'py': 'inpAlbSwingCount', 'param': 'inpAlbSwingCount', 'type': 'int', 'default': 5, 'label': 'Average alb swing count', 'sinput': False}, {'mql': 'inpAlbSpeed', 'py': 'inpAlbSpeed', 'param': 'inpAlbSpeed', 'type': 'double', 'default': 1.0, 'label': 'Average alb "speed"', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 0, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpNormPeriod', 'py': 'inpNormPeriod', 'param': 'inpNormPeriod', 'type': 'int', 'default': 10, 'label': 'Normalization period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Stochastic  period
inpSlowing = _input('inpSlowing', 3)  # Stochastic slowing/smoothing period
inpAlbSwingCount = _input('inpAlbSwingCount', 5)  # Average alb swing count
inpAlbSpeed = _input('inpAlbSpeed', 1.0)  # Average alb "speed"
inpMaMethod = _input('inpMaMethod', ma_sma)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpNormPeriod = _input('inpNormPeriod', 10)  # Normalization period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valn = Arr(0, 0.0)
valfu = Arr(0, 0.0)
valfd = Arr(0, 0.0)
_avgNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
_albWork = Arr(0, 0.0)
workSto = Arr(0, 0.0, dims=(5,))
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, valfu, INDICATOR_DATA)
    SetIndexBuffer(1, valfd, INDICATOR_DATA)
    SetIndexBuffer(2, valn, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic of alb adaptive ' + _avgNames[inpMaMethod] + ' (' + _str(inpPeriod) + ',' + _str(inpSlowing) + ',' + _str(inpAlbSwingCount) + ',' + _str(inpAlbSpeed) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = iCustomMa(inpMaMethod, getPrice(inpPrice, open, close, high, low, i, rates_total), _int(iAlb(high, low, inpAlbSwingCount, inpAlbSpeed, i, rates_total)), i, rates_total)
        val[i] = iStoch(_price, _price, _price, inpPeriod, inpSlowing, i, rates_total) - 50
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        valn[i] = 0.0
        _start = MathMax(i - inpNormPeriod + 1, 0)
        if val[i] > 0:
            hi = val[ArrayMaximum(val, _start, inpNormPeriod)]
            if hi != 0:
                valn[i] = _fdiv(50 * val[i], hi)
        if val[i] < 0:
            lo = val[ArrayMinimum(val, _start, inpNormPeriod)]
            if lo != 0:
                valn[i] = _fdiv(50 * val[i], -lo)
        valfu[i] = valn[i]
        valfd[i] = val[i]
    return rates_total

def iAlb(high, low, swingCount, speed, i, bars):
    if ArraySize(_albWork) != bars:
        ArrayResize(_albWork, bars)
    _albWork[i] = 0.0
    if (((i > 3 and high[i] > high[i - 1]) and high[i - 1] > high[i - 2]) and low[i - 2] < low[i - 3]) and low[i - 3] < low[i - 4]:
        _albWork[i] = -1.0
    if (((i > 3 and low[i] < low[i - 1]) and low[i - 1] < low[i - 2]) and high[i - 2] > high[i - 3]) and high[i - 3] > high[i - 4]:
        _albWork[i] = 1.0
    k = i
    n = 0
    while k >= 0 and n < swingCount:
        if _albWork[k] != 0:
            n += 1
        k -= 1
    return MathMax(MathRound((_fdiv(_fdiv(float(i - k), swingCount), speed) if (speed != 0 and swingCount != 0) else _fdiv(float(i - k), swingCount))), 1)

def iStoch(priceR, priceH, priceL, period, slowing, i, bars, instanceNo=0):
    if ArrayRange(workSto, 0) != bars:
        ArrayResize(workSto, bars)
    instanceNo *= 5
    workSto[i][0 + instanceNo] = priceH
    workSto[i][1 + instanceNo] = priceL
    workSto[i][2 + instanceNo] = priceR
    workSto[i][3 + instanceNo] = priceH
    workSto[i][4 + instanceNo] = priceL
    k = 1
    while k < period and (i - k) >= 0:
        workSto[i][4 + instanceNo] = MathMin(workSto[i][4 + instanceNo], workSto[i - k][instanceNo + 1])
        workSto[i][3 + instanceNo] = MathMax(workSto[i][3 + instanceNo], workSto[i - k][instanceNo + 0])
        k += 1
    sumlow = 0.0
    sumhigh = 0.0
    k = 0
    while k < slowing and (i - k) >= 0:
        sumlow += workSto[i - k][2 + instanceNo] - workSto[i - k][4 + instanceNo]
        sumhigh += workSto[i - k][3 + instanceNo] - workSto[i - k][4 + instanceNo]
        k += 1
    if sumhigh != 0.0:
        return _fdiv(100.0 * sumlow, sumhigh)
    else:
        return 0.0

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


class StochasticOfAlbAverageWnz(_MQL5Indicator):
    name = 'Stochastic of alb average - wnz'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Stochastic  period
        'inpSlowing': 3,  # Stochastic slowing/smoothing period
        'inpAlbSwingCount': 5,  # Average alb swing count
        'inpAlbSpeed': 1.0,  # Average alb "speed"
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpNormPeriod': 10,  # Normalization period
    }

