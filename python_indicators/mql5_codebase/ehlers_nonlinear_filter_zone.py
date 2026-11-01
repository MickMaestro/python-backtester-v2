"""Ehlers nonlinear filter zone — converted from MQL5: MQL5 Indicators/Ehlers Nonlinear Filter Zone/Ehlers nonlinear filter zone.mq5

Ehlers nonlinear filter zone
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 8}, 'colors': {1: [13628367], 2: [12052223], 3: [12632256, 3329330, 36095], 4: [12632256, 3329330, 36095], 5: [12632256, 3329330, 36095]}, 'widths': {5: 4}, 'styles': {}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Middle value'}, 'levels': [], 'description': ['Ehlers nonlinear filter zone'], 'name': 'Ehlers nonlinear filter zone', 'source': 'MQL5 Indicators/Ehlers Nonlinear Filter Zone/Ehlers nonlinear filter zone.mq5', 'folder': 'Ehlers Nonlinear Filter Zone', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Nonlinear filter period', 'sinput': False}, {'mql': 'inpMomentum', 'py': 'inpMomentum', 'param': 'inpMomentum', 'type': 'int', 'default': 5, 'label': 'Momentum period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Nonlinear filter period
inpMomentum = _input('inpMomentum', 5)  # Momentum period
bufferUp = Arr(0, 0.0)
bufferUpc = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferDnc = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
bufferMec = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
workEnlf = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferUpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(7, bufferDnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, bufferMe, INDICATOR_DATA)
    SetIndexBuffer(9, bufferMec, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ehlers nonlinear filter zone (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        bufferUp[i] = iEnlf(high[i], inpPeriod, inpMomentum, i, rates_total, 0)
        bufferMe[i] = iEnlf((high[i] + low[i]) / 2, inpPeriod, inpMomentum, i, rates_total, 1)
        bufferDn[i] = iEnlf(low[i], inpPeriod, inpMomentum, i, rates_total, 2)
        fupd[i] = bufferMe[i]
        fupu[i] = bufferUp[i]
        fdnu[i] = bufferMe[i]
        fdnd[i] = bufferDn[i]
        bufferUpc[i] = ((1 if (bufferUp[i] > bufferUp[i - 1]) else 2 if (bufferUp[i] < bufferUp[i - 1]) else bufferUpc[i - 1]) if (i > 0) else 0)
        bufferDnc[i] = ((1 if (bufferDn[i] > bufferDn[i - 1]) else 2 if (bufferDn[i] < bufferDn[i - 1]) else bufferDnc[i - 1]) if (i > 0) else 0)
        bufferMec[i] = (1 if (bufferUpc[i] == 1 and bufferDnc[i] == 1) else 2 if (bufferUpc[i] == 2 and bufferDnc[i] == 2) else 0)
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


class EhlersNonlinearFilterZone(_MQL5Indicator):
    name = 'Ehlers nonlinear filter zone'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Nonlinear filter period
        'inpMomentum': 5,  # Momentum period
    }

