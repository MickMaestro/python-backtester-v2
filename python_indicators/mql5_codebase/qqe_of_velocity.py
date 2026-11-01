"""QQE of velocity — converted from MQL5: MQL5 Indicators/QQE of Velocity/QQE of velocity.mq5

QQE of velocity
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [11119017], 2: [11119017], 3: [11119017, 16760576, 8036607]}, 'widths': {3: 2}, 'styles': {1: 2}, 'labels': {1: 'QQE fast', 2: 'QQE slow', 3: 'QQE'}, 'levels': [], 'description': ['QQE of velocity'], 'name': 'QQE of velocity', 'source': 'MQL5 Indicators/QQE of Velocity/QQE of velocity.mq5', 'folder': 'QQE of Velocity', 'inputs': [{'mql': 'inpVelPeriod', 'py': 'inpVelPeriod', 'param': 'inpVelPeriod', 'type': 'int', 'default': 50, 'label': 'Velocity period', 'sinput': False}, {'mql': 'inpVelSmoothingFactor', 'py': 'inpVelSmoothingFactor', 'param': 'inpVelSmoothingFactor', 'type': 'int', 'default': 5, 'label': 'Velocity smoothing factor', 'sinput': False}, {'mql': 'inpWPFast', 'py': 'inpWPFast', 'param': 'inpWPFast', 'type': 'double', 'default': 2.618, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpWPSlow', 'py': 'inpWPSlow', 'param': 'inpWPSlow', 'type': 'double', 'default': 4.236, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpVelPrice', 'py': 'inpVelPrice', 'param': 'inpVelPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVelPeriod = _input('inpVelPeriod', 50)  # Velocity period
inpVelSmoothingFactor = _input('inpVelSmoothingFactor', 5)  # Velocity smoothing factor
inpWPFast = _input('inpWPFast', 2.618)  # Fast period
inpWPSlow = _input('inpWPSlow', 4.236)  # Slow period
inpVelPrice = _input('inpVelPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levs = Arr(0, 0.0)
levf = Arr(0, 0.0)
prices = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, levf, INDICATOR_DATA)
    SetIndexBuffer(1, levs, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'QQE of Velocity (' + _str(inpVelPeriod) + ',' + _str(inpVelSmoothingFactor) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iEma(iVelocity(getPrice(inpVelPrice, open, close, high, low, i, rates_total), inpVelPeriod, i, rates_total), inpVelSmoothingFactor, i, rates_total, 0)
        _iEma = iEma((MathAbs(val[i - 1] - val[i]) if (i > 0) else 0), inpVelPeriod, i, rates_total, 1)
        _iEmm = iEma(_iEma, inpVelPeriod, i, rates_total, 2)
        _iEmf = _iEmm * inpWPFast
        _iEms = _iEmm * inpWPSlow
        tr = (levs[i - 1] if (i > 0) else 0)
        dv = tr
        if val[i] < tr:
            tr = val[i] + _iEms
            if (i > 0 and val[i - 1] < dv) and tr > dv:
                tr = dv
        if val[i] > tr:
            tr = val[i] - _iEms
            if (i > 0 and val[i - 1] > dv) and tr < dv:
                tr = dv
        levs[i] = tr
        tr = (levf[i - 1] if (i > 0) else 0)
        dv = tr
        if val[i] < tr:
            tr = val[i] + _iEmf
            if (i > 0 and val[i - 1] < dv) and tr > dv:
                tr = dv
        if val[i] > tr:
            tr = val[i] - _iEmf
            if (i > 0 and val[i - 1] > dv) and tr < dv:
                tr = dv
        levf[i] = tr
        valc[i] = (1 if (val[i] > levf[i] and val[i] > levs[i]) else 2 if (val[i] < levf[i] and val[i] < levs[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i

def iVelocity(price, length, i, total):
    if ArraySize(prices) != total:
        ArrayResize(prices, total)
    prices[i] = price
    suma = 0.0
    sumwa = 0.0
    sumb = 0.0
    sumwb = 0.0
    k = 0
    while k < length and (i - k) >= 0:
        weight = length - k
        suma += prices[i - k] * weight
        sumb += prices[i - k] * weight * weight
        sumwa += weight
        sumwb += weight * weight
        k += 1
    return _fdiv(sumb, sumwb) - _fdiv(suma, sumwa)

def iEma(price, period, r, bars, instanceNo=0):
    if ArrayRange(workEma, 0) != bars:
        ArrayResize(workEma, bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

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


class QQEOfVelocity(_MQL5Indicator):
    name = 'QQE of velocity'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpVelPeriod': 50,  # Velocity period
        'inpVelSmoothingFactor': 5,  # Velocity smoothing factor
        'inpWPFast': 2.618,  # Fast period
        'inpWPSlow': 4.236,  # Slow period
        'inpVelPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

