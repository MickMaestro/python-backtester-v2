"""Volume Average percent — converted from MQL5: MQL5 Indicators/Volume Average percent/Volume Average percent.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [11119017, 3329434, 42495, 32768, 255], 2: [11119017]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Volume average percent', 2: 'Average'}, 'levels': [], 'description': [], 'name': 'Volume Average percent', 'source': 'MQL5 Indicators/Volume Average percent/Volume Average percent.mq5', 'folder': 'Volume Average percent', 'inputs': [{'mql': 'inpVolumeType', 'py': 'inpVolumeType', 'param': 'inpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volume type to use', 'sinput': False}, {'mql': 'inpAveragePeriod', 'py': 'inpAveragePeriod', 'param': 'inpAveragePeriod', 'type': 'int', 'default': 50, 'label': 'Average period', 'sinput': False}, {'mql': 'inpAverageMethod', 'py': 'inpAverageMethod', 'param': 'inpAverageMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpBreakoutPercent', 'py': 'inpBreakoutPercent', 'param': 'inpBreakoutPercent', 'type': 'double', 'default': 50.0, 'label': 'Breakout percentage', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# enum enVolumeType
vol_ticks = 0
vol_volume = 1
_enum('enVolumeType', {0: 'vol_ticks', 1: 'vol_volume'})

# ---- inputs and global variables
inpVolumeType = _input('inpVolumeType', vol_ticks)  # Volume type to use
inpAveragePeriod = _input('inpAveragePeriod', 50)  # Average period
inpAverageMethod = _input('inpAverageMethod', ma_ema)  # Average method
inpBreakoutPercent = _input('inpBreakoutPercent', 50.0)  # Breakout percentage
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
average = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, average, INDICATOR_DATA)
    _avgNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volume ' + _avgNames[inpAverageMethod] + ' average percent (' + _str(inpAveragePeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _volume = float((tick_volume[i] if (inpVolumeType == vol_ticks) else volume[i]))
        _avg = iCustomMa(inpAverageMethod, _volume, inpAveragePeriod, i, rates_total)
        average[i] = 100.0
        val[i] = (_fdiv(100 * _volume, _avg) if (_avg != 0) else 0)
        valc[i] = 0.0
        if i > 0 and close[i] > close[i - 1]:
            valc[i] = (3 if (_volume > (_avg * (1 + (inpBreakoutPercent * 0.01)))) else 1)
        if i > 0 and close[i] < close[i - 1]:
            valc[i] = (4 if (_volume > (_avg * (1 + (inpBreakoutPercent * 0.01)))) else 2)
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


class VolumeAveragePercent(_MQL5Indicator):
    name = 'Volume Average percent'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpVolumeType': _Choice({0: 'Use ticks', 1: 'Use real volume'}, default=0),  # Volume type to use
        'inpAveragePeriod': 50,  # Average period
        'inpAverageMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Average method
        'inpBreakoutPercent': 50.0,  # Breakout percentage
    }

