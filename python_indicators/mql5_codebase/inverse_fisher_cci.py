"""Inverse Fisher CCI — converted from MQL5: MQL5 Indicators/Inverse Fisher CCI/Inverse Fisher CCI.mq5

Inverse Fisher CCI
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16760576, 8036607], 2: [11119017]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {1: 'Inverse Fisher of CCI', 2: 'Signal'}, 'levels': [], 'description': ['Inverse Fisher CCI'], 'name': 'Inverse Fisher CCI', 'source': 'MQL5 Indicators/Inverse Fisher CCI/Inverse Fisher CCI.mq5', 'folder': 'Inverse Fisher CCI', 'inputs': [{'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 50, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpCciPrice', 'py': 'inpCciPrice', 'param': 'inpCciPrice', 'type': 'int', 'default': 6, 'label': 'CCI price', 'sinput': False}, {'mql': 'inpCciSmooth', 'py': 'inpCciSmooth', 'param': 'inpCciSmooth', 'type': 'int', 'default': 5, 'label': 'CCI smoothing', 'sinput': False}, {'mql': 'inpCciSmoothType', 'py': 'inpCciSmoothType', 'param': 'inpCciSmoothType', 'type': 'int', 'default': 1, 'label': 'CCI smoothing type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpCciPeriod = _input('inpCciPeriod', 50)  # CCI period
inpCciPrice = _input('inpCciPrice', PRICE_TYPICAL)  # CCI price
inpCciSmooth = _input('inpCciSmooth', 5)  # CCI smoothing
inpCciSmoothType = _input('inpCciSmoothType', ma_ema)  # CCI smoothing type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
cci = Arr(0, 0.0)
prices = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    SetIndexBuffer(3, cci, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Inverse Fisher CCI (' + _str(inpCciPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
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
        if dev != 0:
            cci[i] = iCustomMa(inpCciSmoothType, _fdiv(0.1 * (prices[i] - avg), 0.015 * dev), inpCciSmooth, i, rates_total)
        else:
            cci[i] = iCustomMa(inpCciSmoothType, 0.0, inpCciSmooth, i, rates_total)
        val[i] = _fdiv(MathExp(2 * cci[i]) - 1, MathExp(2 * cci[i]) + 1)
        signal[i] = (val[i - 1] if (i > 0) else val[i])
        valc[i] = (1 if (NormalizeDouble(val[i], Digits()) > NormalizeDouble(signal[i], Digits())) else 2 if (NormalizeDouble(val[i], Digits()) < NormalizeDouble(signal[i], Digits())) else valc[i - 1] if (i > 0) else 0)
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

def getPrice(tprice, open, close, high, low, i, _bars):
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


class InverseFisherCCI(_MQL5Indicator):
    name = 'Inverse Fisher CCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCciPeriod': 50,  # CCI period
        'inpCciPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # CCI price
        'inpCciSmooth': 5,  # CCI smoothing
        'inpCciSmoothType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # CCI smoothing type
    }

