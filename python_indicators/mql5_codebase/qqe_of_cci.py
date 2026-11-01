"""QQE of CCI — converted from MQL5: MQL5 Indicators/QQE of CCI/QQE of CCI.mq5

QQE of CCI
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [11119017], 2: [11119017], 3: [11119017, 16760576, 8036607]}, 'widths': {3: 2}, 'styles': {1: 2}, 'labels': {1: 'QQE fast', 2: 'QQE slow', 3: 'QQE'}, 'levels': [], 'description': ['QQE of CCI'], 'name': 'QQE of CCI', 'source': 'MQL5 Indicators/QQE of CCI/QQE of CCI.mq5', 'folder': 'QQE of CCI', 'inputs': [{'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 50, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpCciSmoothingFactor', 'py': 'inpCciSmoothingFactor', 'param': 'inpCciSmoothingFactor', 'type': 'int', 'default': 5, 'label': 'CCI smoothing factor', 'sinput': False}, {'mql': 'inpWPFast', 'py': 'inpWPFast', 'param': 'inpWPFast', 'type': 'double', 'default': 2.618, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpWPSlow', 'py': 'inpWPSlow', 'param': 'inpWPSlow', 'type': 'double', 'default': 4.236, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpCciPrice', 'py': 'inpCciPrice', 'param': 'inpCciPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpCciPeriod = _input('inpCciPeriod', 50)  # CCI period
inpCciSmoothingFactor = _input('inpCciSmoothingFactor', 5)  # CCI smoothing factor
inpWPFast = _input('inpWPFast', 2.618)  # Fast period
inpWPSlow = _input('inpWPSlow', 4.236)  # Slow period
inpCciPrice = _input('inpCciPrice', PRICE_CLOSE)  # Price
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
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'QQE of CCI(' + _str(inpCciPeriod) + ',' + _str(inpCciSmoothingFactor) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = getPrice(inpCciPrice, open, close, high, low, i, rates_total)
        avg = 0.0
        k = 0
        while k < inpCciPeriod and (i - k) >= 0:
            avg += prices[i - k]
            k += 1
        avg = avg / inpCciPeriod
        dev = 0.0
        k = 0
        while k < inpCciPeriod and (i - k) >= 0:
            dev += MathAbs(prices[i - k] - avg)
            k += 1
        dev = dev / inpCciPeriod
        val[i] = iEma((_fdiv(prices[i] - avg, 0.015 * dev) if (dev != 0) else 0), inpCciSmoothingFactor, i, rates_total, 0)
        _iEma = iEma((MathAbs(val[i - 1] - val[i]) if (i > 0) else 0), inpCciPeriod, i, rates_total, 1)
        _iEmm = iEma(_iEma, inpCciPeriod, i, rates_total, 2)
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


class QQEOfCCI(_MQL5Indicator):
    name = 'QQE of CCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCciPeriod': 50,  # CCI period
        'inpCciSmoothingFactor': 5,  # CCI smoothing factor
        'inpWPFast': 2.618,  # Fast period
        'inpWPSlow': 4.236,  # Slow period
        'inpCciPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

