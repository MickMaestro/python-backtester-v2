"""Smoothed Kijun-Sen — converted from MQL5: MQL5 Indicators/Smoothed Kijun-Sen/Smoothed Kijun-Sen.mq5

Smoothed Kijun-sen
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Kijun-sen'}, 'levels': [], 'description': ['Smoothed Kijun-sen'], 'name': 'Smoothed Kijun-Sen', 'source': 'MQL5 Indicators/Smoothed Kijun-Sen/Smoothed Kijun-Sen.mq5', 'folder': 'Smoothed Kijun-Sen', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 26, 'label': 'Kijun', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 26)  # Kijun
inpMaPeriod = _input('inpMaPeriod', 5)  # Smoothing period
inpMaMethod = _input('inpMaMethod', ma_sma)  # Smoothing method
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
pricesh = Arr(0, 0.0)
pricesl = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, pricesh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, pricesl, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoothed Kijun-sen(' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        pricesh[i] = iCustomMa(inpMaMethod, high[i], inpMaPeriod, i, rates_total, 0)
        pricesl[i] = iCustomMa(inpMaMethod, low[i], inpMaPeriod, i, rates_total, 1)
        _start = MathMax(i - inpPeriod + 1, 0)
        if i < inpPeriod:
            i += 1
            continue
        khi = pricesh[ArrayMaximum(pricesh, _start, inpPeriod)]
        klo = pricesl[ArrayMinimum(pricesl, _start, inpPeriod)]
        val[i] = (((khi + klo) / 2) if ((khi + klo) != 0) else 0)
        valc[i] = ((0 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmoothedKijunSen(_MQL5Indicator):
    name = 'Smoothed Kijun-Sen'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 26,  # Kijun
        'inpMaPeriod': 5,  # Smoothing period
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Smoothing method
    }

