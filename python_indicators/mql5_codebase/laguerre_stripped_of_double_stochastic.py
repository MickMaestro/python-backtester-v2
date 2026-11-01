"""Laguerre stripped of double stochastic — converted from MQL5: MQL5 Indicators/Laguerre stripped of double stochastic/Laguerre stripped of double stochastic.mq5

Copyright: © mladen, 2017; Link: www.forex-station.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017', 'link': 'www.forex-station.com', 'window': 'separate', 'indicator_buffers': 12, 'indicator_plots': 8}, 'types': {1: 7, 2: 7, 3: 7, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [8310016, 8257691], 2: [8303616, 8257716], 3: [8297216, 8257741], 4: [8421504], 5: [8421504], 6: [8421504], 7: [8421504], 8: [12632256]}, 'widths': {8: 2}, 'styles': {}, 'labels': {1: 'Fill 1', 2: 'Fill 2', 3: 'Fill 3', 4: 'Laguerre 1', 5: 'Laguerre 2', 6: 'Laguerre 3', 7: 'Laguerre 4', 8: 'Double stochastic'}, 'levels': [], 'description': [], 'name': 'Laguerre stripped of double stochastic', 'source': 'MQL5 Indicators/Laguerre stripped of double stochastic/Laguerre stripped of double stochastic.mq5', 'folder': 'Laguerre stripped of double stochastic', 'inputs': [{'mql': 'StochasticPeriod', 'py': 'StochasticPeriod', 'param': 'StochasticPeriod', 'type': 'int', 'default': 55, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'EMAPeriod', 'py': 'EMAPeriod', 'param': 'EMAPeriod', 'type': 'int', 'default': 15, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'Gamma', 'py': 'Gamma', 'param': 'Gamma', 'type': 'double', 'default': 0.75, 'label': 'Laguerre gamma', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StochasticPeriod = _input('StochasticPeriod', 55)  # Stochastic period
EMAPeriod = _input('EMAPeriod', 15)  # Smoothing period
Gamma = _input('Gamma', 0.75)  # Laguerre gamma
lagg1u = Arr(0, 0.0)
lagg1d = Arr(0, 0.0)
lagg2u = Arr(0, 0.0)
lagg2d = Arr(0, 0.0)
lagg3u = Arr(0, 0.0)
lagg3d = Arr(0, 0.0)
lagg1 = Arr(0, 0.0)
lagg2 = Arr(0, 0.0)
lagg3 = Arr(0, 0.0)
lagg4 = Arr(0, 0.0)
stow = Arr(0, 0.0)
stoch = Arr(0, 0.0)
workLag = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, lagg1u, INDICATOR_DATA)
    SetIndexBuffer(1, lagg1d, INDICATOR_DATA)
    SetIndexBuffer(2, lagg2u, INDICATOR_DATA)
    SetIndexBuffer(3, lagg2d, INDICATOR_DATA)
    SetIndexBuffer(4, lagg3u, INDICATOR_DATA)
    SetIndexBuffer(5, lagg3d, INDICATOR_DATA)
    SetIndexBuffer(6, lagg1, INDICATOR_DATA)
    SetIndexBuffer(7, lagg2, INDICATOR_DATA)
    SetIndexBuffer(8, lagg3, INDICATOR_DATA)
    SetIndexBuffer(9, lagg4, INDICATOR_DATA)
    SetIndexBuffer(10, stoch, INDICATOR_DATA)
    SetIndexBuffer(11, stow, INDICATOR_CALCULATIONS)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alpha = _fdiv(2.0, 1.0 + EMAPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        start = MathMax(i - StochasticPeriod + 1, 0)
        min_ = low[ArrayMinimum(low, start, StochasticPeriod)]
        max_ = high[ArrayMaximum(high, start, StochasticPeriod)]
        sto = ((_fdiv(close[i] - min_, max_ - min_) * 100.0) if (max_ != min_) else 0)
        stow[i] = ((stow[i - 1] + (alpha * (sto - stow[i - 1]))) if (i > 0) else sto)
        min_ = stow[ArrayMinimum(stow, start, StochasticPeriod)]
        max_ = stow[ArrayMaximum(stow, start, StochasticPeriod)]
        sto = ((_fdiv(stow[i] - min_, max_ - min_) * 100.0) if (max_ != min_) else 0)
        stoch[i] = ((stoch[i - 1] + (alpha * (sto - stoch[i - 1]))) if (i > 0) else sto)
        laga = Box(0.0)
        lagb = Box(0.0)
        lagc = Box(0.0)
        lagd = Box(0.0)
        iLaGuerre(stoch[i], Gamma, laga, lagb, lagc, lagd, i, rates_total, 0)
        lagg1[i] = laga.v
        lagg2[i] = lagb.v
        lagg3[i] = lagc.v
        lagg4[i] = lagd.v
        lagg1u[i] = laga.v
        lagg1d[i] = lagb.v
        lagg2u[i] = lagb.v
        lagg2d[i] = lagc.v
        lagg3u[i] = lagc.v
        lagg3d[i] = lagd.v
        i += 1
    return i

def iLaGuerre(price, gamma, val1, val2, val3, val4, i, bars, instanceNo=0):
    if ArrayRange(workLag, 0) != bars:
        ArrayResize(workLag, bars)
    instanceNo *= 4
    gamma = MathMax(MathMin(gamma, 0.99), 0.01)
    if i > 0:
        workLag[i][instanceNo + 0] = ((1.0 - gamma) * price) + (gamma * workLag[i - 1][instanceNo + 0])
        workLag[i][instanceNo + 1] = ((-gamma) * workLag[i][instanceNo + 0]) + workLag[i - 1][instanceNo + 0] + (gamma * workLag[i - 1][instanceNo + 1])
        workLag[i][instanceNo + 2] = ((-gamma) * workLag[i][instanceNo + 1]) + workLag[i - 1][instanceNo + 1] + (gamma * workLag[i - 1][instanceNo + 2])
        workLag[i][instanceNo + 3] = ((-gamma) * workLag[i][instanceNo + 2]) + workLag[i - 1][instanceNo + 2] + (gamma * workLag[i - 1][instanceNo + 3])
    else:
        for k in range(0, 4):
            workLag[i][instanceNo + k] = price
    val1.v = workLag[i][instanceNo + 0]
    val2.v = workLag[i][instanceNo + 1]
    val3.v = workLag[i][instanceNo + 2]
    val4.v = workLag[i][instanceNo + 3]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LaguerreStrippedOfDoubleStochastic(_MQL5Indicator):
    name = 'Laguerre stripped of double stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StochasticPeriod': 55,  # Stochastic period
        'EMAPeriod': 15,  # Smoothing period
        'Gamma': 0.75,  # Laguerre gamma
    }

