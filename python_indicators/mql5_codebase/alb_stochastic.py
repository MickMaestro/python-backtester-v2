"""Alb stochastic — converted from MQL5: MQL5 Indicators/Alb stochastic/Alb stochastic.mq5

Adaptive lookback stochastic
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 32768]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Stochastic'}, 'levels': [], 'description': ['Adaptive lookback stochastic'], 'name': 'Alb stochastic', 'source': 'MQL5 Indicators/Alb stochastic/Alb stochastic.mq5', 'folder': 'Alb stochastic', 'inputs': [{'mql': 'inpAlbSwingCount', 'py': 'inpAlbSwingCount', 'param': 'inpAlbSwingCount', 'type': 'int', 'default': 5, 'label': 'Alb swing count', 'sinput': False}, {'mql': 'inpAlbSpeed', 'py': 'inpAlbSpeed', 'param': 'inpAlbSpeed', 'type': 'double', 'default': 0.1, 'label': 'Alb "speed"', 'sinput': False}, {'mql': 'inpSlowing', 'py': 'inpSlowing', 'param': 'inpSlowing', 'type': 'int', 'default': 3, 'label': 'Slowing/smoothing period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAlbSwingCount = _input('inpAlbSwingCount', 5)  # Alb swing count
inpAlbSpeed = _input('inpAlbSpeed', 0.1)  # Alb "speed"
inpSlowing = _input('inpSlowing', 3)  # Slowing/smoothing period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
_albWork = Arr(0, 0.0)
workSto = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Alb adaptive stochastic (' + _str(inpAlbSwingCount) + ',' + _str(inpAlbSpeed) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iStoch(_price, _price, _price, _int(iAlb(high, low, inpAlbSwingCount, inpAlbSpeed, i, rates_total)), inpSlowing, i, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
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


class AlbStochastic(_MQL5Indicator):
    name = 'Alb stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpAlbSwingCount': 5,  # Alb swing count
        'inpAlbSpeed': 0.1,  # Alb "speed"
        'inpSlowing': 3,  # Slowing/smoothing period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

