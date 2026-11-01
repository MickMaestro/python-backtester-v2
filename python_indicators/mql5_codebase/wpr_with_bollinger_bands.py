"""WPR with Bollinger bands — converted from MQL5: MQL5 Indicators/WPR with Bollinger bands/WPR with Bollinger bands.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [3329330], 2: [11119017], 3: [42495], 4: [12632256, 3329330, 42495]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'up level', 2: 'down level', 4: 'value'}, 'levels': [], 'description': [], 'name': 'WPR with Bollinger bands', 'source': 'MQL5 Indicators/WPR with Bollinger bands/WPR with Bollinger bands.mq5', 'folder': 'WPR with Bollinger bands', 'inputs': [{'mql': 'inpWprPeriod', 'py': 'inpWprPeriod', 'param': 'inpWprPeriod', 'type': 'int', 'default': 14, 'label': 'WPR period', 'sinput': False}, {'mql': 'inpBBPeriod', 'py': 'inpBBPeriod', 'param': 'inpBBPeriod', 'type': 'int', 'default': 20, 'label': 'Bollinger bands period', 'sinput': False}, {'mql': 'inpBBDeviations', 'py': 'inpBBDeviations', 'param': 'inpBBDeviations', 'type': 'double', 'default': 2.0, 'label': 'Bollinger bands deviations', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpWprPeriod = _input('inpWprPeriod', 14)  # WPR period
inpBBPeriod = _input('inpBBPeriod', 20)  # Bollinger bands period
inpBBDeviations = _input('inpBBDeviations', 2.0)  # Bollinger bands deviations
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
workDev = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelMi, INDICATOR_DATA)
    SetIndexBuffer(2, levelDn, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WPR + Bollineg bands (' + _str(inpWprPeriod) + ',' + _str(inpBBPeriod) + ',' + _str(inpBBDeviations) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - inpWprPeriod + 1, 0)
        _max = high[ArrayMaximum(high, _start, inpWprPeriod)]
        _min = low[ArrayMinimum(low, _start, inpWprPeriod)]
        val[i] = (_fdiv((-(_max - close[i])) * 100, _max - _min) if (_max != _min) else 0)
        levelMi[i] = iSma(val[i], inpBBPeriod, i, rates_total)
        deviation = iDeviation(val[i], inpBBPeriod, i, rates_total)
        levelUp[i] = levelMi[i] + (inpBBDeviations * deviation)
        levelDn[i] = levelMi[i] - (inpBBDeviations * deviation)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

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

def iDeviation(value, length, i, bars, isSample=False):
    if ArraySize(workDev) != bars:
        ArrayResize(workDev, bars)
    workDev[i] = value
    sumx = 0.0
    sumxx = 0.0
    k = 0
    while k < length and (i - k) >= 0:
        pass
        sumx += workDev[i - k]
        sumxx += workDev[i - k] * workDev[i - k]
        k += 1
    return MathSqrt(_fdiv(sumxx - _fdiv(sumx * sumx, length), MathMax(length - isSample, 1)))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WPRWithBollingerBands(_MQL5Indicator):
    name = 'WPR with Bollinger bands'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpWprPeriod': 14,  # WPR period
        'inpBBPeriod': 20,  # Bollinger bands period
        'inpBBDeviations': 2.0,  # Bollinger bands deviations
    }

