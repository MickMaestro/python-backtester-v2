"""Vidya_zone — converted from MQL5: MQL5 Indicators/Vidya zone/Vidya_zone.mq5

Copyright: © mladen, 2017; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 8}, 'colors': {1: [13628367], 2: [12052223], 3: [12632256, 3329330, 36095], 4: [12632256, 3329330, 36095], 5: [12632256, 3329330, 36095]}, 'widths': {5: 4}, 'styles': {}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Middle value'}, 'levels': [], 'description': [], 'name': 'Vidya_zone', 'source': 'MQL5 Indicators/Vidya zone/Vidya_zone.mq5', 'folder': 'Vidya zone', 'inputs': [{'mql': 'Periodv', 'py': 'Periodv', 'param': 'Periodv', 'type': 'int', 'default': 25, 'label': 'Vidya period', 'sinput': False}, {'mql': 'Periods', 'py': 'Periods', 'param': 'Periods', 'type': 'int', 'default': 9, 'label': 'Smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Periodv = _input('Periodv', 25)  # Vidya period
Periods = _input('Periods', 9)  # Smoothing period
bufferUp = Arr(0, 0.0)
bufferUpc = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferDnc = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
bufferMec = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
vidya_work = Arr(0, 0.0, dims=(9,))

def OnInit():
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferUpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(7, bufferDnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, bufferMe, INDICATOR_DATA)
    SetIndexBuffer(9, bufferMec, INDICATOR_COLOR_INDEX)
    return 0

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        median = (high[i] + low[i]) / 2.0
        bufferUp[i] = iVidya(high[i], median, Periodv, Periods, i, rates_total, 0)
        bufferMe[i] = iVidya(median, median, Periodv, Periods, i, rates_total, 1)
        bufferDn[i] = iVidya(low[i], median, Periodv, Periods, i, rates_total, 2)
        fupd[i] = bufferMe[i]
        fupu[i] = bufferUp[i]
        fdnu[i] = bufferMe[i]
        fdnd[i] = bufferDn[i]
        bufferUpc[i] = ((1 if (bufferUp[i] > bufferUp[i - 1]) else 2 if (bufferUp[i] < bufferUp[i - 1]) else bufferUpc[i - 1]) if (i > 0) else 0)
        bufferDnc[i] = ((1 if (bufferDn[i] > bufferDn[i - 1]) else 2 if (bufferDn[i] < bufferDn[i - 1]) else bufferDnc[i - 1]) if (i > 0) else 0)
        bufferMec[i] = (1 if (bufferUpc[i] == 1 and bufferDnc[i] == 1) else 2 if (bufferUpc[i] == 2 and bufferDnc[i] == 2) else 0)
    return rates_total

def iVidya(price, pricc, cmoPeriods, smoothPeriod, r, bars, instanceNo=0):
    if ArrayRange(vidya_work, 0) != bars:
        ArrayResize(vidya_work, bars)
    s = instanceNo * 3
    vidya_work[r][s + 0] = price
    vidya_work[r][s + 1] = pricc
    sumUp = 0.0
    sumDo = 0.0
    k = 0
    while k < cmoPeriods and (r - k - 1) >= 0:
        diff = vidya_work[r - k][s + 1] - vidya_work[r - k - 1][s + 1]
        if diff > 0:
            sumUp += diff
        else:
            sumDo -= diff
        k += 1
    vidya_work[r][s + 2] = ((vidya_work[r - 1][s + 2] + (_fdiv((MathAbs(_fdiv(sumUp - sumDo, sumUp + sumDo)) if ((sumUp + sumDo) != 0) else 1) * 2.0, 1.0 + MathMax(smoothPeriod, 1)) * (vidya_work[r][s + 0] - vidya_work[r - 1][s + 2]))) if (r > 0) else price)
    return vidya_work[r][s + 2]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VidyaZone(_MQL5Indicator):
    name = 'Vidya_zone'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Periodv': 25,  # Vidya period
        'Periods': 9,  # Smoothing period
    }

