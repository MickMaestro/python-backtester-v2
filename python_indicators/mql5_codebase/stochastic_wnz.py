"""Stochastic - wnz — converted from MQL5: MQL5 Indicators/Stochastic - with normalized zones/Stochastic - wnz.mq5

Stochastic - with normalized zones
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [15128749, 12180223], 2: [11119017], 3: [11119017, 16760576, 6333684]}, 'widths': {3: 3}, 'styles': {2: 2}, 'labels': {1: 'Normalized zones', 2: 'Normalized stochastic', 3: 'Stochastic'}, 'levels': [], 'description': ['Stochastic - with normalized zones'], 'name': 'Stochastic - wnz', 'source': 'MQL5 Indicators/Stochastic - with normalized zones/Stochastic - wnz.mq5', 'folder': 'Stochastic - with normalized zones', 'inputs': [{'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 34, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpStoSlowing', 'py': 'inpStoSlowing', 'param': 'inpStoSlowing', 'type': 'int', 'default': 9, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpNormPeriod', 'py': 'inpNormPeriod', 'param': 'inpNormPeriod', 'type': 'int', 'default': 20, 'label': 'Normalization period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpStoPeriod = _input('inpStoPeriod', 34)  # Stochastic period
inpStoSlowing = _input('inpStoSlowing', 9)  # Stochastic slowing
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpNormPeriod = _input('inpNormPeriod', 20)  # Normalization period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valn = Arr(0, 0.0)
valfu = Arr(0, 0.0)
valfd = Arr(0, 0.0)
workSto = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, valfu, INDICATOR_DATA)
    SetIndexBuffer(1, valfd, INDICATOR_DATA)
    SetIndexBuffer(2, valn, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic - wnz  (' + _str(inpStoPeriod) + ',' + _str(inpNormPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iStoch(_price, _price, _price, inpStoPeriod, inpStoSlowing, i, rates_total) - 50
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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
        i += 1
    return i

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


class StochasticWnz(_MQL5Indicator):
    name = 'Stochastic - wnz'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStoPeriod': 34,  # Stochastic period
        'inpStoSlowing': 9,  # Stochastic slowing
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpNormPeriod': 20,  # Normalization period
    }

