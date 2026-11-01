"""ttm_waves_2 — converted from MQL5: MQL5 Indicators/TTM Waves, v. 2.0/ttm_waves_2.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 8}, 'colors': {1: [65280, 42495], 2: [3329330, 9662683]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'TTM waves', 2: 'TTM waves'}, 'levels': [], 'description': [], 'name': 'ttm_waves_2', 'source': 'MQL5 Indicators/TTM Waves, v. 2.0/ttm_waves_2.mq5', 'folder': 'TTM Waves, v. 2.0', 'inputs': [{'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'int', 'default': 34, 'label': 'Period 1', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'int', 'default': 45, 'label': 'Period 2', 'sinput': False}, {'mql': 'Period3', 'py': 'Period3', 'param': 'Period3', 'type': 'int', 'default': 53, 'label': 'Period 3', 'sinput': False}, {'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'int', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Color Up', 'sinput': False}, {'mql': 'ColorSteps', 'py': 'ColorSteps', 'param': 'ColorSteps', 'type': 'int', 'default': 50, 'label': 'Color steps for drawing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period1 = _input('Period1', 34)  # Period 1
Period2 = _input('Period2', 45)  # Period 2
Period3 = _input('Period3', 53)  # Period 3
SmoothPeriod = _input('SmoothPeriod', 10)  # Smoothing period
ColorFrom = _input('ColorFrom', clrOrange)  # Color down
ColorTo = _input('ColorTo', clrLime)  # Color Up
ColorSteps = _input('ColorSteps', 50)  # Color steps for drawing
wave = Arr(0, 0.0)
wavec = Arr(0, 0.0)
wfu = Arr(0, 0.0)
wfd = Arr(0, 0.0)
cSteps = 0
totalBars = 0
work = Arr(0, 0.0, dims=(3,))
workLinr = Arr(0, 0.0, dims=(6,))

def OnInit():
    global cSteps
    SetIndexBuffer(0, wfu, INDICATOR_DATA)
    SetIndexBuffer(1, wfd, INDICATOR_DATA)
    SetIndexBuffer(2, wave, INDICATOR_DATA)
    SetIndexBuffer(3, wavec, INDICATOR_COLOR_INDEX)
    cSteps = (ColorSteps if (ColorSteps > 1) else 2)
    PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    IndicatorSetString(INDICATOR_SHORTNAME, 'TTM waves (' + _str(Period1) + ',' + _str(Period2) + ',' + _str(Period3) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global totalBars
    if ArrayRange(work, 0) != rates_total:
        ArrayResize(work, rates_total)
    totalBars = rates_total
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        price = ((open[i - 1] + close[i - 1]) * 0.375) + (close[i] * 0.25)
        xma1 = iLinr(price, Period1, i, 0)
        xma2 = iLinr(price, Period2, i, 1)
        xma3 = iLinr(price, Period3, i, 2)
        work[i][0] = iLinr(xma1 - price, SmoothPeriod, i, 3)
        work[i][1] = iLinr(xma2 - price, SmoothPeriod, i, 4)
        work[i][2] = iLinr(xma3 - price, SmoothPeriod, i, 5)
        wave[i] = 0.0
        k = 0
        while k < Period2 and (i - k) >= 0:
            wave[i] -= ((2.0 * work[i - k][0]) + work[i - k][1] + work[i - k][2]) / 4.0
            k += 1
        wfu[i] = 0.0
        wfd[i] = 0.0
        if wave[i] > 0 and wave[i] > wave[i - 1]:
            wfu[i] = wave[i]
        if wave[i] < 0 and wave[i] < wave[i - 1]:
            wfu[i] = wave[i]
        min_ = wave[i]
        max_ = wave[i]
        col = 0.0
        k = 1
        while k < ColorSteps and (i - k) >= 0:
            min_ = (wave[i - k] if (wave[i - k] < min_) else min_)
            max_ = (wave[i - k] if (wave[i - k] > max_) else max_)
            k += 1
        if (max_ - min_) == 0:
            col = 50.0
        else:
            col = _fdiv(100 * (wave[i] - min_), max_ - min_)
        wavec[i] = MathFloor((col * cSteps) / 100.0)
    return rates_total

def iLinr(price, period, r, instanceNo=0):
    if ArrayRange(workLinr, 0) != totalBars:
        ArrayResize(workLinr, totalBars)
    period = MathMax(period, 1)
    workLinr[r][instanceNo] = price
    lwmw = period
    lwma = lwmw * price
    sma = price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        lwmw += weight
        lwma += weight * workLinr[r - k][instanceNo]
        sma += workLinr[r - k][instanceNo]
        k += 1
    return _fdiv(3.0 * lwma, lwmw) - _fdiv(2.0 * sma, period)

def getColor(stepNo, totalSteps, from_, to):
    stes = float(totalSteps) - 1.0
    step = _fdiv(from_ - to, stes)
    return _uint(round(from_ - (step * stepNo)))

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TtmWaves2(_MQL5Indicator):
    name = 'ttm_waves_2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period1': 34,  # Period 1
        'Period2': 45,  # Period 2
        'Period3': 53,  # Period 3
        'SmoothPeriod': 10,  # Smoothing period
        'ColorSteps': 50,  # Color steps for drawing
    }

