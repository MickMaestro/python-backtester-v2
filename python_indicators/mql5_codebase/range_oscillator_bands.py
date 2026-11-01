"""Range oscillator + bands — converted from MQL5: MQL5 Indicators/Range Oscillator + Bands/Range oscillator + bands.mq5

Range oscillator with bands
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [16748574], 2: [11119017], 3: [6333684], 4: [11119017, 16748574, 6333684]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Band up', 2: 'Average range oscillator', 3: 'Band down', 4: 'Range oscillator'}, 'levels': [], 'description': ['Range oscillator with bands'], 'name': 'Range oscillator + bands', 'source': 'MQL5 Indicators/Range Oscillator + Bands/Range oscillator + bands.mq5', 'folder': 'Range Oscillator + Bands', 'inputs': [{'mql': 'inpRngPeriod', 'py': 'inpRngPeriod', 'param': 'inpRngPeriod', 'type': 'int', 'default': 40, 'label': 'Range oscillator period', 'sinput': False}, {'mql': 'inpBandsPeriod', 'py': 'inpBandsPeriod', 'param': 'inpBandsPeriod', 'type': 'int', 'default': 20, 'label': 'Bands period', 'sinput': False}, {'mql': 'inpBandsDeviations', 'py': 'inpBandsDeviations', 'param': 'inpBandsDeviations', 'type': 'double', 'default': 2.0, 'label': 'Bands deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRngPeriod = _input('inpRngPeriod', 40)  # Range oscillator period
inpBandsPeriod = _input('inpBandsPeriod', 20)  # Bands period
inpBandsDeviations = _input('inpBandsDeviations', 2.0)  # Bands deviation
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
bandu = Arr(0, 0.0)
bandm = Arr(0, 0.0)
bandd = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
workDev = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, bandu, INDICATOR_DATA)
    SetIndexBuffer(1, bandm, INDICATOR_DATA)
    SetIndexBuffer(2, bandd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range oscillator + bands (' + _str(inpRngPeriod) + ',' + _str(inpBandsPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _start = MathMax(i - inpRngPeriod + 1, 0)
        _max = high[ArrayMaximum(high, _start, inpRngPeriod)]
        _min = low[ArrayMinimum(low, _start, inpRngPeriod)]
        _med = (high[i] + low[i]) / 2
        val[i] = (_fdiv(100 * (_med - _min), _max - _min) if (_max != _min) else 0)
        bandm[i] = iSma(val[i], inpBandsPeriod, i, rates_total)
        _dev = iDeviation(val[i], inpBandsPeriod, i, rates_total)
        bandu[i] = bandm[i] + (inpBandsDeviations * _dev)
        bandd[i] = bandm[i] - (inpBandsDeviations * _dev)
        valc[i] = (1 if (val[i] > bandu[i]) else 2 if (val[i] < bandd[i]) else 0)
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


class RangeOscillatorBands(_MQL5Indicator):
    name = 'Range oscillator + bands'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRngPeriod': 40,  # Range oscillator period
        'inpBandsPeriod': 20,  # Bands period
        'inpBandsDeviations': 2.0,  # Bands deviation
    }

