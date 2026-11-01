"""Stochastic extended — converted from MQL5: MQL5 Indicators/Stochastic extended/Stochastic extended.mq5

Extended stochastic
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16760576, 8036607], 2: [11119017]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {1: 'Stochastic', 2: 'Signal'}, 'levels': [], 'description': ['Extended stochastic'], 'name': 'Stochastic extended', 'source': 'MQL5 Indicators/Stochastic extended/Stochastic extended.mq5', 'folder': 'Stochastic extended', 'inputs': [{'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpStoSlowing', 'py': 'inpStoSlowing', 'param': 'inpStoSlowing', 'type': 'int', 'default': 9, 'label': 'Stochastic slowing period', 'sinput': False}, {'mql': 'inpStoMaType', 'py': 'inpStoMaType', 'param': 'inpStoMaType', 'type': 'int', 'default': 0, 'label': 'Stochastic average type', 'sinput': False}, {'mql': 'inpSigPeriod', 'py': 'inpSigPeriod', 'param': 'inpSigPeriod', 'type': 'int', 'default': 3, 'label': 'Stochastic signal period', 'sinput': False}, {'mql': 'inpSigMaType', 'py': 'inpSigMaType', 'param': 'inpSigMaType', 'type': 'int', 'default': 0, 'label': 'Signal average type', 'sinput': False}, {'mql': 'inpStoPrice', 'py': 'inpStoPrice', 'param': 'inpStoPrice', 'type': 'int', 'default': 0, 'label': 'Price :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# enum enStochPrice
sto_htl = 0
sto_ctc = 1
_enum('enStochPrice', {0: 'sto_htl', 1: 'sto_ctc'})

# ---- inputs and global variables
inpStoPeriod = _input('inpStoPeriod', 32)  # Stochastic period
inpStoSlowing = _input('inpStoSlowing', 9)  # Stochastic slowing period
inpStoMaType = _input('inpStoMaType', ma_sma)  # Stochastic average type
inpSigPeriod = _input('inpSigPeriod', 3)  # Stochastic signal period
inpSigMaType = _input('inpSigMaType', ma_sma)  # Signal average type
inpStoPrice = _input('inpStoPrice', sto_htl)  # Price :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
_avgNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
workSma = Arr(0, 0.0, dims=(3,))
workEma = Arr(0, 0.0, dims=(3,))
workSmma = Arr(0, 0.0, dims=(3,))
workLwma = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic (' + _avgNames[inpStoMaType] + ')(' + _str(inpStoPeriod) + ',' + _str(inpStoSlowing) + ',' + _str(inpSigPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _start = MathMax(i - inpStoPeriod + 1, 0)
        _lo = (low[ArrayMinimum(low, _start, inpStoPeriod)] if (inpStoPrice == sto_htl) else close[ArrayMinimum(close, _start, inpStoPeriod)])
        _hi = (high[ArrayMaximum(high, _start, inpStoPeriod)] if (inpStoPrice == sto_htl) else close[ArrayMaximum(close, _start, inpStoPeriod)])
        sumlow = iCustomMa(inpStoMaType, close[i] - _lo, inpStoSlowing, i, rates_total, 0)
        sumhigh = iCustomMa(inpStoMaType, _hi - _lo, inpStoSlowing, i, rates_total, 1)
        val[i] = (_fdiv(100 * sumlow, sumhigh) if (sumhigh != sumlow) else 100)
        signal[i] = iCustomMa(inpSigMaType, val[i], inpSigPeriod, i, rates_total, 2)
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
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


class StochasticExtended(_MQL5Indicator):
    name = 'Stochastic extended'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStoPeriod': 32,  # Stochastic period
        'inpStoSlowing': 9,  # Stochastic slowing period
        'inpStoMaType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Stochastic average type
        'inpSigPeriod': 3,  # Stochastic signal period
        'inpSigMaType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Signal average type
        'inpStoPrice': _Choice({0: 'High/low', 1: 'Close/close'}, default=0),  # Price :
    }

