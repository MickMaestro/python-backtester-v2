"""Triple DSEMA — converted from MQL5: MQL5 Indicators/Triple DSEMA/Triple DSEMA.mq5

Triple DSEMA (double smoothed EMA)
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 8, 2: 8, 3: 8}, 'colors': {1: [11119017, 9639167, 3329330], 2: [11119017, 9639167, 3329330], 3: [11119017, 9639167, 3329330]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'DSEMA high', 2: 'DSEMA close', 3: 'DSEMA low'}, 'levels': [], 'description': ['Triple DSEMA (double smoothed EMA)'], 'name': 'Triple DSEMA', 'source': 'MQL5 Indicators/Triple DSEMA/Triple DSEMA.mq5', 'folder': 'Triple DSEMA', 'inputs': [{'mql': 'inpDsemaPeriod', 'py': 'inpDsemaPeriod', 'param': 'inpDsemaPeriod', 'type': 'double', 'default': 27.0, 'label': 'DSEMA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpDsemaPeriod = _input('inpDsemaPeriod', 27.0)  # DSEMA period
dsemau = Arr(0, 0.0)
dsemauc = Arr(0, 0.0)
dsemac = Arr(0, 0.0)
dsemacc = Arr(0, 0.0)
dsemad = Arr(0, 0.0)
dsemadc = Arr(0, 0.0)
workDsema = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, dsemau, INDICATOR_DATA)
    SetIndexBuffer(1, dsemauc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, dsemac, INDICATOR_DATA)
    SetIndexBuffer(3, dsemacc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, dsemad, INDICATOR_DATA)
    SetIndexBuffer(5, dsemadc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Triple Dsema (' + _str(inpDsemaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        dsemau[i] = iDsema(high[i], inpDsemaPeriod, i, rates_total, 0)
        dsemac[i] = iDsema(close[i], inpDsemaPeriod, i, rates_total, 1)
        dsemad[i] = iDsema(low[i], inpDsemaPeriod, i, rates_total, 2)
        dsemauc[i] = ((2 if (dsemau[i] > dsemau[i - 1]) else 1 if (dsemau[i] < dsemau[i - 1]) else dsemauc[i - 1]) if (i > 0) else 0)
        dsemacc[i] = ((2 if (dsemac[i] > dsemac[i - 1]) else 1 if (dsemac[i] < dsemac[i - 1]) else dsemacc[i - 1]) if (i > 0) else 0)
        dsemadc[i] = ((2 if (dsemad[i] > dsemad[i - 1]) else 1 if (dsemad[i] < dsemad[i - 1]) else dsemadc[i - 1]) if (i > 0) else 0)
    return rates_total

def iDsema(price, period, r, bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workDsema, 0) != bars:
        ArrayResize(workDsema, bars)
    instanceNo *= 2
    workDsema[r][0 + instanceNo] = price
    workDsema[r][1 + instanceNo] = price
    alpha = _fdiv(2.0, 1.0 + MathSqrt(period))
    if r > 0:
        workDsema[r][0 + instanceNo] = workDsema[r - 1][0 + instanceNo] + (alpha * (price - workDsema[r - 1][0 + instanceNo]))
        workDsema[r][1 + instanceNo] = workDsema[r - 1][1 + instanceNo] + (alpha * (workDsema[r][0 + instanceNo] - workDsema[r - 1][1 + instanceNo]))
    return workDsema[r][1 + instanceNo]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TripleDSEMA(_MQL5Indicator):
    name = 'Triple DSEMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDsemaPeriod': 27.0,  # DSEMA period
    }

