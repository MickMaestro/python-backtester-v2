"""Triple Hull — converted from MQL5: MQL5 Indicators/Triple Hull/Triple Hull.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 8, 2: 8, 3: 8}, 'colors': {1: [11119017, 9639167, 3329330], 2: [11119017, 9639167, 3329330], 3: [11119017, 9639167, 3329330]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Hull high', 2: 'Hull close', 3: 'Hull low'}, 'levels': [], 'description': [], 'name': 'Triple Hull', 'source': 'MQL5 Indicators/Triple Hull/Triple Hull.mq5', 'folder': 'Triple Hull', 'inputs': [{'mql': 'inpHullPeriod', 'py': 'inpHullPeriod', 'param': 'inpHullPeriod', 'type': 'double', 'default': 27.0, 'label': 'Hull period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpHullPeriod = _input('inpHullPeriod', 27.0)  # Hull period
hullu = Arr(0, 0.0)
hulluc = Arr(0, 0.0)
hullc = Arr(0, 0.0)
hullcc = Arr(0, 0.0)
hulld = Arr(0, 0.0)
hulldc = Arr(0, 0.0)
workHull = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, hullu, INDICATOR_DATA)
    SetIndexBuffer(1, hulluc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, hullc, INDICATOR_DATA)
    SetIndexBuffer(3, hullcc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, hulld, INDICATOR_DATA)
    SetIndexBuffer(5, hulldc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Triple Hull (' + _str(inpHullPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        hullu[i] = iHull(high[i], inpHullPeriod, i, rates_total, 0)
        hullc[i] = iHull(close[i], inpHullPeriod, i, rates_total, 1)
        hulld[i] = iHull(low[i], inpHullPeriod, i, rates_total, 2)
        hulluc[i] = ((2 if (hullu[i] > hullu[i - 1]) else 1 if (hullu[i] < hullu[i - 1]) else hulluc[i - 1]) if (i > 0) else 0)
        hullcc[i] = ((2 if (hullc[i] > hullc[i - 1]) else 1 if (hullc[i] < hullc[i - 1]) else hullcc[i - 1]) if (i > 0) else 0)
        hulldc[i] = ((2 if (hulld[i] > hulld[i - 1]) else 1 if (hulld[i] < hulld[i - 1]) else hulldc[i - 1]) if (i > 0) else 0)
    return rates_total

def iHull(price, period, r, bars, instanceNo=0):
    if ArrayRange(workHull, 0) != bars:
        ArrayResize(workHull, bars)
    instanceNo *= 2
    workHull[r][instanceNo] = price
    if period <= 1:
        return price
    HmaPeriod = _int(MathMax(period, 2))
    HalfPeriod = _int(MathFloor(_idiv(HmaPeriod, 2)))
    HullPeriod = _int(MathFloor(MathSqrt(HmaPeriod)))
    hma = 0.0
    hmw = 0.0
    weight = 0.0
    hmw = HalfPeriod
    hma = hmw * price
    k = 1
    while k < HalfPeriod and (r - k) >= 0:
        weight = HalfPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][instanceNo]
        k += 1
    workHull[r][instanceNo + 1] = _fdiv(2.0 * hma, hmw)
    hmw = HmaPeriod
    hma = hmw * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = HmaPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][instanceNo]
        k += 1
    workHull[r][instanceNo + 1] -= _fdiv(hma, hmw)
    hmw = HullPeriod
    hma = hmw * workHull[r][instanceNo + 1]
    k = 1
    while k < HullPeriod and (r - k) >= 0:
        weight = HullPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][1 + instanceNo]
        k += 1
    return _fdiv(hma, hmw)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TripleHull(_MQL5Indicator):
    name = 'Triple Hull'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpHullPeriod': 27.0,  # Hull period
    }

