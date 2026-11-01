"""Trend direction and force - smoothed — converted from MQL5: MQL5 Indicators/Trend direction and force - smoothed/Trend direction and force - smoothed.mq5

Trend direction and force - smoothed
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 8}, 'colors': {1: [14474460], 2: [11119017, 6333684, 16760576]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'No trend zone', 2: 'Trend direction and force'}, 'levels': [], 'description': ['Trend direction and force - smoothed'], 'name': 'Trend direction and force - smoothed', 'source': 'MQL5 Indicators/Trend direction and force - smoothed/Trend direction and force - smoothed.mq5', 'folder': 'Trend direction and force - smoothed', 'inputs': [{'mql': 'trendPeriod', 'py': 'trendPeriod', 'param': 'trendPeriod', 'type': 'int', 'default': 20, 'label': 'Trend period', 'sinput': False}, {'mql': 'smoothPeriod', 'py': 'smoothPeriod', 'param': 'smoothPeriod', 'type': 'int', 'default': 3, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'smoothType', 'py': 'smoothType', 'param': 'smoothType', 'type': 'int', 'default': 1, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'TriggerUp', 'py': 'TriggerUp', 'param': 'TriggerUp', 'type': 'double', 'default': 0.05, 'label': 'Trigger up level', 'sinput': False}, {'mql': 'TriggerDown', 'py': 'TriggerDown', 'param': 'TriggerDown', 'type': 'double', 'default': -0.05, 'label': 'Trigger down level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
trendPeriod = _input('trendPeriod', 20)  # Trend period
smoothPeriod = _input('smoothPeriod', 3)  # Smoothing period
smoothType = _input('smoothType', ma_ema)  # Smoothing type
TriggerUp = _input('TriggerUp', 0.05)  # Trigger up level
TriggerDown = _input('TriggerDown', -0.05)  # Trigger down level
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levup = Arr(0, 0.0)
levdn = Arr(0, 0.0)
workTrend = Arr(0, 0.0, dims=(3,))
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, levup, INDICATOR_DATA)
    SetIndexBuffer(1, levdn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend direction and force smoothed (' + _str(trendPeriod) + ',' + _str(smoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(workTrend, 0) != rates_total:
        ArrayResize(workTrend, rates_total)
    _alpha = 2.0 / (1 + trendPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        workTrend[i][0] = ((workTrend[i - 1][0] + (_alpha * (close[i] - workTrend[i - 1][0]))) if (i > 0) else close[i])
        workTrend[i][1] = ((workTrend[i - 1][1] + (_alpha * (workTrend[i][0] - workTrend[i - 1][1]))) if (i > 0) else workTrend[i][0])
        impetmma = ((workTrend[i][0] - workTrend[i - 1][0]) if (i > 0) else 0)
        impetsmma = ((workTrend[i][1] - workTrend[i - 1][1]) if (i > 0) else 0)
        divma = _fdiv(MathAbs(workTrend[i][0] - workTrend[i][1]), Point())
        averimpet = _fdiv(impetmma + impetsmma, 2 * Point())
        workTrend[i][2] = divma * MathPow(averimpet, 3)
        absValue = 0.0
        k = 0
        while k < (trendPeriod * 3) and (i - k) >= 0:
            absValue = MathMax(absValue, MathAbs(workTrend[i - k][2]))
            k += 1
        val[i] = iCustomMa(smoothType, (_fdiv(workTrend[i][2], absValue) if (absValue > 0) else 0), smoothPeriod, i, rates_total)
        levup[i] = TriggerUp
        levdn[i] = TriggerDown
        valc[i] = (2 if (val[i] > levup[i]) else 1 if (val[i] < levdn[i]) else 0)
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


class TrendDirectionAndForceSmoothed(_MQL5Indicator):
    name = 'Trend direction and force - smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'trendPeriod': 20,  # Trend period
        'smoothPeriod': 3,  # Smoothing period
        'smoothType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Smoothing type
        'TriggerUp': 0.05,  # Trigger up level
        'TriggerDown': -0.05,  # Trigger down level
    }

