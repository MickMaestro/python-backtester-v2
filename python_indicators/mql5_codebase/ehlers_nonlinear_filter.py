"""Ehlers nonlinear filter — converted from MQL5: MQL5 Indicators/Ehlers Nonlinear Filter/Ehlers nonlinear filter.mq5

Ehlers nonlinear filter
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Ehelers nonlinear filter'}, 'levels': [], 'description': ['Ehlers nonlinear filter'], 'name': 'Ehlers nonlinear filter', 'source': 'MQL5 Indicators/Ehlers Nonlinear Filter/Ehlers nonlinear filter.mq5', 'folder': 'Ehlers Nonlinear Filter', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Nonlinear filter period', 'sinput': False}, {'mql': 'inpMomentum', 'py': 'inpMomentum', 'param': 'inpMomentum', 'type': 'int', 'default': 5, 'label': 'Momentum period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Nonlinear filter period
inpMomentum = _input('inpMomentum', 5)  # Momentum period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workEnlf = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ehlers nonlinear filter (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        val[i] = iEnlf(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, inpMomentum, i, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iEnlf(price, length, momentumLength, r, bars, instanceNo=0):
    if ArrayRange(workEnlf, 0) != bars:
        ArrayResize(workEnlf, bars)
    workEnlf[r][instanceNo] = price
    sumCoef = 0.0
    num = 0.0
    k = 0
    while k < length and (r - k - momentumLength) >= 0:
        coeff = MathAbs(workEnlf[r - k][instanceNo] - workEnlf[r - k - momentumLength][instanceNo])
        sumCoef += coeff
        num += coeff * workEnlf[r - k][instanceNo]
        k += 1
    return (_fdiv(num, sumCoef) if (sumCoef != 0) else price)

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


class EhlersNonlinearFilter(_MQL5Indicator):
    name = 'Ehlers nonlinear filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Nonlinear filter period
        'inpMomentum': 5,  # Momentum period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

