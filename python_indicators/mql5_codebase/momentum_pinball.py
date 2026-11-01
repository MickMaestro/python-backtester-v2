"""Momentum_pinball — converted from MQL5: MQL5 Indicators/Momentum Pinball v.2/Momentum_pinball.mq5

Original idea for the indicator by Nicolas
Copyright: mladen; Link: www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 7, 2: 8}, 'colors': {1: [14474460], 2: [12632256, 3329330, 17919]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'mpb zone', 2: 'Momentum pinball'}, 'levels': [], 'description': ['Original idea for the indicator by Nicolas'], 'name': 'Momentum_pinball', 'source': 'MQL5 Indicators/Momentum Pinball v.2/Momentum_pinball.mq5', 'folder': 'Momentum Pinball v.2', 'inputs': [{'mql': 'MomentumPeriod', 'py': 'MomentumPeriod', 'param': 'MomentumPeriod', 'type': 'int', 'default': 14, 'label': 'Momentum period', 'sinput': False}, {'mql': 'AvgPeriod', 'py': 'AvgPeriod', 'param': 'AvgPeriod', 'type': 'int', 'default': 0, 'label': 'Momentum average period (0 -> same as momentum period', 'sinput': False}, {'mql': 'AvgType', 'py': 'AvgType', 'param': 'AvgType', 'type': 'int', 'default': 1, 'label': 'Momentum average method', 'sinput': False}, {'mql': 'ZoneUp', 'py': 'ZoneUp', 'param': 'ZoneUp', 'type': 'double', 'default': 70.0, 'label': 'Upper zone limit', 'sinput': False}, {'mql': 'ZoneDown', 'py': 'ZoneDown', 'param': 'ZoneDown', 'type': 'double', 'default': 30.0, 'label': 'Lower zone limit', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
avgSma = 0
avgEma = 1
avgSmma = 2
avgLwma = 3
_enum('enMaTypes', {0: 'avgSma', 1: 'avgEma', 2: 'avgSmma', 3: 'avgLwma'})

# ---- inputs and global variables
MomentumPeriod = _input('MomentumPeriod', 14)  # Momentum period
AvgPeriod = _input('AvgPeriod', 0)  # Momentum average period (0 -> same as momentum period
AvgType = _input('AvgType', avgEma)  # Momentum average method
ZoneUp = _input('ZoneUp', 70.0)  # Upper zone limit
ZoneDown = _input('ZoneDown', 30.0)  # Lower zone limit
mom = Arr(0, 0.0)
momc = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
diff = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, mom, INDICATOR_DATA)
    SetIndexBuffer(3, momc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, diff, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Momentum pinball (' + _str(MomentumPeriod) + ',' + _str(AvgPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    avgPeriod = AvgPeriod
    if avgPeriod <= 1:
        avgPeriod = MomentumPeriod
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        if i <= MomentumPeriod:
            diff[i] = 0.0
            iCustomMa(AvgType, 0.0, avgPeriod, i, rates_total, 0)
            iCustomMa(AvgType, 0.0, avgPeriod, i, rates_total, 1)
            continue
        diff[i] = close[i] - close[i - MomentumPeriod]
        u = 0.0
        d = 0.0
        if diff[i] > diff[i - 1]:
            u = diff[i] - diff[i - 1]
        if diff[i] < diff[i - 1]:
            d = diff[i - 1] - diff[i]
        avgu = iCustomMa(AvgType, u, avgPeriod, i, rates_total, 0)
        avgd = iCustomMa(AvgType, d, avgPeriod, i, rates_total, 1)
        if avgd != 0:
            mom[i] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(avgu, avgd))
        else:
            mom[i] = 50.0
        fup[i] = ZoneUp
        fdn[i] = ZoneDown
        momc[i] = 0.0
        if mom[i] > fup[i]:
            momc[i] = 1.0
        if mom[i] < fdn[i]:
            momc[i] = 2.0
    return rates_total

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == avgSma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == avgEma:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == avgSmma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == avgLwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    instanceNo *= 2
    k = 0
    workSma[r][instanceNo + 0] = price
    workSma[r][instanceNo + 1] = price
    k = 1
    while k < period and (r - k) >= 0:
        workSma[r][instanceNo + 1] += workSma[r - k][instanceNo + 0]
        k += 1
    workSma[r][instanceNo + 1] = _fdiv(workSma[r][instanceNo + 1], 1.0 * k)
    return workSma[r][instanceNo + 1]

def iEma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    alpha = _fdiv(2.0, 1.0 + period)
    if r > 0:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    if r < period:
        workSmma[r][instanceNo] = price
    else:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
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


class MomentumPinball(_MQL5Indicator):
    name = 'Momentum_pinball'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MomentumPeriod': 14,  # Momentum period
        'AvgPeriod': 0,  # Momentum average period (0 -> same as momentum period
        'AvgType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Momentum average method
        'ZoneUp': 70.0,  # Upper zone limit
        'ZoneDown': 30.0,  # Lower zone limit
    }
    y_range = (0.0, 100.0)

