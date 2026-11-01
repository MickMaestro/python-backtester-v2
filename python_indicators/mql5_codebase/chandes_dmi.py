"""Chandes DMI — converted from MQL5: MQL5 Indicators/Chande's DMI (Dynamic Momentum Index)/Chandes DMI.mq5

Chande's Dynamic Momentum Index
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'DMI'}, 'levels': [], 'description': ["Chande's Dynamic Momentum Index"], 'name': 'Chandes DMI', 'source': "MQL5 Indicators/Chande's DMI (Dynamic Momentum Index)/Chandes DMI.mq5", 'folder': "Chande's DMI (Dynamic Momentum Index)", 'inputs': [{'mql': 'inpDmiPeriod', 'py': 'inpDmiPeriod', 'param': 'inpDmiPeriod', 'type': 'int', 'default': 14, 'label': 'Dynamic Momentum Index period', 'sinput': False}, {'mql': 'inpDmiLowerLimit', 'py': 'inpDmiLowerLimit', 'param': 'inpDmiLowerLimit', 'type': 'int', 'default': 3, 'label': 'Dynamic Momentum Index lower limit', 'sinput': False}, {'mql': 'inpDmiUpperLimit', 'py': 'inpDmiUpperLimit', 'param': 'inpDmiUpperLimit', 'type': 'int', 'default': 30, 'label': 'Dynamic Momentum Index upper limit', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDevPeriod', 'py': 'inpDevPeriod', 'param': 'inpDevPeriod', 'type': 'int', 'default': 5, 'label': 'Standard deviation period', 'sinput': False}, {'mql': 'inpMaDevPeriod', 'py': 'inpMaDevPeriod', 'param': 'inpMaDevPeriod', 'type': 'int', 'default': 10, 'label': 'Standard deviation smoothing period', 'sinput': False}, {'mql': 'inpMaDevMode', 'py': 'inpMaDevMode', 'param': 'inpMaDevMode', 'type': 'int', 'default': 0, 'label': 'Standard deviation smoothing metyhod', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpDmiPeriod = _input('inpDmiPeriod', 14)  # Dynamic Momentum Index period
inpDmiLowerLimit = _input('inpDmiLowerLimit', 3)  # Dynamic Momentum Index lower limit
inpDmiUpperLimit = _input('inpDmiUpperLimit', 30)  # Dynamic Momentum Index upper limit
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDevPeriod = _input('inpDevPeriod', 5)  # Standard deviation period
inpMaDevPeriod = _input('inpMaDevPeriod', 10)  # Standard deviation smoothing period
inpMaDevMode = _input('inpMaDevMode', ma_sma)  # Standard deviation smoothing metyhod
dmi = Arr(0, 0.0)
dmic = Arr(0, 0.0)
prices = Arr(0, 0.0)
values = Arr(0, 0.0, dims=(4,))
workRsi = Arr(0, 0.0, dims=(3,))
workSma = Arr(0, 0.0, dims=(3,))
workEma = Arr(0, 0.0, dims=(3,))
workSmma = Arr(0, 0.0, dims=(3,))
workLwma = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, dmi, INDICATOR_DATA)
    SetIndexBuffer(1, dmic, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, "Chande's DMI (" + _str(inpDmiPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(values, 0) != rates_total:
        ArrayResize(values, rates_total)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        avg = prices[i]
        n = 1
        while n < inpDevPeriod and (i - n) >= 0:
            avg += prices[i - n]
            n += 1
        avg = _fdiv(avg, n)
        dev = MathPow(prices[i] - avg, 2)
        n = 1
        while n < inpDevPeriod and (i - n) >= 0:
            dev += (prices[i - n] - avg) * (prices[i - n] - avg)
            n += 1
        dev = MathSqrt(_fdiv(dev, n))
        devma = iCustomMa(inpMaDevMode, dev, inpMaDevPeriod, i, rates_total, 0)
        _vi = (_fdiv(dev, devma) if (devma != 0) else 0)
        _td = (_int(MathMin(MathMax(MathRound(_fdiv(inpDmiPeriod, _vi)), inpDmiLowerLimit), inpDmiUpperLimit)) if (_vi != 0) else inpDmiPeriod)
        dmi[i] = iRsi(prices[i], _td, i, rates_total)
        dmic[i] = ((1 if (dmi[i] > dmi[i - 1]) else 2 if (dmi[i] < dmi[i - 1]) else dmic[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iRsi(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 3
    workRsi[r][z + 0] = price
    alpha = _fdiv(1.0, MathMax(period, 1))
    if r < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (r - k - 1) >= 0:
            sum_ += MathAbs(workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0])
            k += 1
        workRsi[r][z + 1] = _fdiv(workRsi[r][z + 0] - workRsi[0][z + 0], MathMax(k, 1))
        workRsi[r][z + 2] = _fdiv(sum_, MathMax(k, 1))
    else:
        change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
        workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
        workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
    return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], DBL_MIN)) + 1)

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


class ChandesDMI(_MQL5Indicator):
    name = 'Chandes DMI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDmiPeriod': 14,  # Dynamic Momentum Index period
        'inpDmiLowerLimit': 3,  # Dynamic Momentum Index lower limit
        'inpDmiUpperLimit': 30,  # Dynamic Momentum Index upper limit
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDevPeriod': 5,  # Standard deviation period
        'inpMaDevPeriod': 10,  # Standard deviation smoothing period
        'inpMaDevMode': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Standard deviation smoothing metyhod
    }

