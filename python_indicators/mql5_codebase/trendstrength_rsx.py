"""TrendStrength rsx — converted from MQL5: MQL5 Indicators/Trend Strength RSX/TrendStrength rsx.mq5

TrendStrength rsx
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11119017], 2: [16748574], 3: [6333684]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'rsx', 2: 'trend up', 3: 'trend down'}, 'levels': [], 'description': ['TrendStrength rsx'], 'name': 'TrendStrength rsx', 'source': 'MQL5 Indicators/Trend Strength RSX/TrendStrength rsx.mq5', 'folder': 'Trend Strength RSX', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 32.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpStrength', 'py': 'inpStrength', 'param': 'inpStrength', 'type': 'double', 'default': 4.236, 'label': 'Strength', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32.0)  # Period
inpStrength = _input('inpStrength', 4.236)  # Strength
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
rsx = Arr(0, 0.0)
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
smin = Arr(0, 0.0)
smax = Arr(0, 0.0)
trend = Arr(0, 0.0)
workRsx = Arr(0, 0.0, dims=(13,))

def OnInit():
    SetIndexBuffer(0, rsx, INDICATOR_DATA)
    SetIndexBuffer(1, valu, INDICATOR_DATA)
    SetIndexBuffer(2, vald, INDICATOR_DATA)
    SetIndexBuffer(3, smin, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, smax, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, trend, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendStrength (rsx) (' + _str(inpPeriod) + ',' + _str(inpStrength) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        rsx[i] = iRsx(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i, rates_total)
        valu[i] = EMPTY_VALUE
        vald[i] = EMPTY_VALUE
        trend[i] = 0.0
        if i > 0:
            hrsx = rsx[i]
            lrsx = rsx[i]
            if rsx[i] > rsx[i - 1]:
                hrsx = rsx[i]
                lrsx = rsx[i - 1]
            if rsx[i] < rsx[i - 1]:
                hrsx = rsx[i - 1]
                lrsx = rsx[i]
            delta = hrsx - lrsx
            smin[i] = rsx[i] - (inpStrength * delta)
            smax[i] = rsx[i] + (inpStrength * delta)
            trend[i] = trend[i - 1]
            if rsx[i] > smax[i - 1]:
                trend[i] = 1.0
            if rsx[i] < smin[i - 1]:
                trend[i] = -1.0
            if trend[i] > 0:
                if smin[i] < smin[i - 1]:
                    smin[i] = smin[i - 1]
                valu[i] = smin[i]
            if trend[i] < 0:
                if smax[i] > smax[i - 1]:
                    smax[i] = smax[i - 1]
                vald[i] = smax[i]
    return rates_total

def iRsx(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsx, 0) != bars:
        ArrayResize(workRsx, bars)
    z = instanceNo * 13
    workRsx[r][z + 0] = price
    Kg = _fdiv(3.0, 2.0 + period)
    Hg = 1.0 - Kg
    if r < period:
        for k in range(1, 13):
            workRsx[r][k + z] = 0.0
        return 50.0
    mom = workRsx[r][0 + z] - workRsx[r - 1][0 + z]
    moa = MathAbs(mom)
    for k in range(0, 3):
        kk = k * 2
        workRsx[r][z + kk + 1] = (Kg * mom) + (Hg * workRsx[r - 1][z + kk + 1])
        workRsx[r][z + kk + 2] = (Kg * workRsx[r][z + kk + 1]) + (Hg * workRsx[r - 1][z + kk + 2])
        mom = (1.5 * workRsx[r][z + kk + 1]) - (0.5 * workRsx[r][z + kk + 2])
        workRsx[r][z + kk + 7] = (Kg * moa) + (Hg * workRsx[r - 1][z + kk + 7])
        workRsx[r][z + kk + 8] = (Kg * workRsx[r][z + kk + 7]) + (Hg * workRsx[r - 1][z + kk + 8])
        moa = (1.5 * workRsx[r][z + kk + 7]) - (0.5 * workRsx[r][z + kk + 8])
    return MathMax(MathMin((_fdiv(mom, MathMax(moa, DBL_MIN)) + 1.0) * 50.0, 100.0), 0.0)

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw1 = tprice
        if _sw1 == PRICE_CLOSE:
            return close[i]
        elif _sw1 == PRICE_OPEN:
            return open[i]
        elif _sw1 == PRICE_HIGH:
            return high[i]
        elif _sw1 == PRICE_LOW:
            return low[i]
        elif _sw1 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendStrengthRsx(_MQL5Indicator):
    name = 'TrendStrength rsx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32.0,  # Period
        'inpStrength': 4.236,  # Strength
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

