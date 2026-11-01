"""Choppy market index smooth — converted from MQL5: MQL5 Indicators/Choppy market index - smoothed/Choppy market index smooth.mq5

Choppy market index - smoothed
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [3937500]}, 'widths': {1: 2}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'Choppy market index', 2: 'Choppy market index signal line'}, 'levels': [], 'description': ['Choppy market index - smoothed'], 'name': 'Choppy market index smooth', 'source': 'MQL5 Indicators/Choppy market index - smoothed/Choppy market index smooth.mq5', 'folder': 'Choppy market index - smoothed', 'inputs': [{'mql': 'inpChoPeriod', 'py': 'inpChoPeriod', 'param': 'inpChoPeriod', 'type': 'int', 'default': 60, 'label': 'Choppy index period', 'sinput': False}, {'mql': 'inpSigPeriod', 'py': 'inpSigPeriod', 'param': 'inpSigPeriod', 'type': 'int', 'default': 10, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpSigMethod', 'py': 'inpSigMethod', 'param': 'inpSigMethod', 'type': 'int', 'default': 0, 'label': 'Signal method', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpSmoothMethod', 'py': 'inpSmoothMethod', 'param': 'inpSmoothMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'inpLevel1', 'py': 'inpLevel1', 'param': 'inpLevel1', 'type': 'double', 'default': 40.0, 'label': 'Level 1', 'sinput': False}, {'mql': 'inpLevel2', 'py': 'inpLevel2', 'param': 'inpLevel2', 'type': 'double', 'default': 50.0, 'label': 'Level 2', 'sinput': False}, {'mql': 'inpLevel3', 'py': 'inpLevel3', 'param': 'inpLevel3', 'type': 'double', 'default': 60.0, 'label': 'Level 3', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpChoPeriod = _input('inpChoPeriod', 60)  # Choppy index period
inpSigPeriod = _input('inpSigPeriod', 10)  # Signal period
inpSigMethod = _input('inpSigMethod', ma_sma)  # Signal method
inpSmoothPeriod = _input('inpSmoothPeriod', 5)  # Smoothing period
inpSmoothMethod = _input('inpSmoothMethod', ma_sma)  # Smoothing method
inpLevel1 = _input('inpLevel1', 40.0)  # Level 1
inpLevel2 = _input('inpLevel2', 50.0)  # Level 2
inpLevel3 = _input('inpLevel3', 60.0)  # Level 3
csi = Arr(0, 0.0)
sig = Arr(0, 0.0)
whigh = Arr(0, 0.0)
wlow = Arr(0, 0.0)
wclose = Arr(0, 0.0)
_maNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
workSma = Arr(0, 0.0, dims=(14,))
workEma = Arr(0, 0.0, dims=(14,))
workSmma = Arr(0, 0.0, dims=(14,))
workLwma = Arr(0, 0.0, dims=(14,))

def OnInit():
    SetIndexBuffer(0, csi, INDICATOR_DATA)
    SetIndexBuffer(1, sig, INDICATOR_DATA)
    SetIndexBuffer(2, whigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, wlow, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, wclose, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevel1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpLevel2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, inpLevel3)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Choppy market index (' + _str(inpChoPeriod) + ',' + _str(inpSigPeriod) + ', ' + _maNames[inpSmoothMethod] + ' ' + _str(inpSmoothPeriod) + ' smoothed)')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _prices = Arr(3, 0.0, dyn=False)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _start = MathMax(i - inpChoPeriod + 1, 0)
        _prices[0] = iCustomMa(inpSmoothMethod, high[i], inpSmoothPeriod, i, rates_total, 1)
        _prices[1] = iCustomMa(inpSmoothMethod, low[i], inpSmoothPeriod, i, rates_total, 2)
        _prices[2] = iCustomMa(inpSmoothMethod, close[i], inpSmoothPeriod, i, rates_total, 3)
        ArraySort(_prices)
        wlow[i] = _prices[0]
        wclose[i] = _prices[1]
        whigh[i] = _prices[2]
        hi = whigh[ArrayMaximum(whigh, _start, inpChoPeriod)]
        lo = wlow[ArrayMinimum(wlow, _start, inpChoPeriod)]
        csi[i] = (_fdiv(100.0 * MathAbs(wclose[i] - wclose[i - inpChoPeriod]), hi - lo) if (hi != lo and i >= inpChoPeriod) else 0)
        sig[i] = iCustomMa(inpSigMethod, csi[i], inpSigPeriod, i, rates_total)
    return rates_total

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


class ChoppyMarketIndexSmooth(_MQL5Indicator):
    name = 'Choppy market index smooth'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpChoPeriod': 60,  # Choppy index period
        'inpSigPeriod': 10,  # Signal period
        'inpSigMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Signal method
        'inpSmoothPeriod': 5,  # Smoothing period
        'inpSmoothMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Smoothing method
        'inpLevel1': 40.0,  # Level 1
        'inpLevel2': 50.0,  # Level 2
        'inpLevel3': 60.0,  # Level 3
    }

