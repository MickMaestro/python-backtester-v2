"""drsi_2 — converted from MQL5: MQL5 Indicators/Directional RSI/drsi_2.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 12}, 'colors': {1: [11119017], 2: [9662683, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'drsi_2', 'source': 'MQL5 Indicators/Directional RSI/drsi_2.mq5', 'folder': 'Directional RSI', 'inputs': [{'mql': 'DrsiPeriod', 'py': 'DrsiPeriod', 'param': 'DrsiPeriod', 'type': 'int', 'default': 14, 'label': 'Dynamic rsi calculation period', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'double', 'default': 10.0, 'label': 'Filter', 'sinput': False}, {'mql': 'SARStep', 'py': 'SARStep', 'param': 'SARStep', 'type': 'double', 'default': 0.02, 'label': 'Parabolic SAR step', 'sinput': False}, {'mql': 'SARMaximum', 'py': 'SARMaximum', 'param': 'SARMaximum', 'type': 'double', 'default': 0.1, 'label': 'Parabolic SAR maximum', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
DrsiPeriod = _input('DrsiPeriod', 14)  # Dynamic rsi calculation period
Filter = _input('Filter', 10.0)  # Filter
SARStep = _input('SARStep', 0.02)  # Parabolic SAR step
SARMaximum = _input('SARMaximum', 0.1)  # Parabolic SAR maximum
drsi = Arr(0, 0.0)
sar = Arr(0, 0.0)
colors = Arr(0, 0.0)
workDrsi = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(2,))
workSar = Arr(0, 0.0, dims=(7,))

def OnInit():
    SetIndexBuffer(0, drsi)
    SetIndexBuffer(1, sar)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    SetIndexBuffer(2, colors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Directional RSI 2 (' + _str(DrsiPeriod) + ',' + _str(Filter) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickVolume, volume, spread):
    if ArrayRange(workDrsi, 0) != rates_total:
        ArrayResize(workDrsi, rates_total)
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        workDrsi[i][2] = iEma(high[i], Filter, rates_total, i, 0)
        workDrsi[i][3] = iEma(low[i], Filter, rates_total, i, 1)
        lm = workDrsi[i - 1][3] - workDrsi[i][3]
        hm = workDrsi[i][2] - workDrsi[i - 1][2]
        if hm > 0 and hm > lm:
            workDrsi[i][0] = hm
        else:
            workDrsi[i][0] = 0.0
        if lm > 0 and lm > hm:
            workDrsi[i][1] = lm
        else:
            workDrsi[i][1] = 0.0
        dmp = 0.0
        dmm = 0.0
        k = 0
        while k < DrsiPeriod and (i - k) >= 0:
            dmp += workDrsi[i - k][0]
            dmm += workDrsi[i - k][1]
            k += 1
        if dmm != 0:
            drsi[i] = 100 - _fdiv(100, 1.0 + _fdiv(dmp, dmm))
        else:
            drsi[i] = drsi[i - 1]
        sarOpen = Box(0.0)
        sarPosition = Box(0.0)
        sarChange = Box(0.0)
        sar[i] = iParabolic(drsi[i], drsi[i], SARStep, SARMaximum, sarOpen, sarPosition, sarChange, i, rates_total)
        if sarPosition.v == 1:
            colors[i] = 1.0
        else:
            colors[i] = 0.0
    return rates_total

def iEma(price, period, totalBars, r, instanceNo=0):
    if ArrayRange(workEma, 0) != totalBars:
        ArrayResize(workEma, totalBars)
    alpha = _fdiv(2.0, 1.0 + period)
    workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iParabolic(high, low, step, limit, pOpen, pPosition, pChange, i, total):
    if ArrayRange(workSar, 0) != total:
        ArrayResize(workSar, total)
    if high < low:
        temp = high
        high = low
        low = temp
    pClose = high
    pChange.v = 0.0
    workSar[i][2] = high
    workSar[i][3] = low
    if i < 1:
        workSar[i][0] = high
        workSar[i][1] = low
        workSar[i][4] = high
        workSar[i][5] = -1.0
        return EMPTY_VALUE
    workSar[i][4] = workSar[i - 1][4]
    workSar[i][6] = workSar[i - 1][6]
    workSar[i][5] = workSar[i - 1][5]
    workSar[i][0] = MathMax(workSar[i - 1][0], high)
    workSar[i][1] = MathMin(workSar[i - 1][1], low)
    if workSar[i][5] == 1:
        if low <= workSar[i][4]:
            workSar[i][5] = -1.0
            pChange.v = -1.0
            pClose = workSar[i][0]
            workSar[i][0] = high
            workSar[i][1] = low
            workSar[i][6] = step
            workSar[i][4] = pClose + (workSar[i][6] * (workSar[i][1] - pClose))
            if workSar[i][4] < workSar[i][2]:
                workSar[i][4] = workSar[i][2]
            if workSar[i][4] < workSar[i - 1][2]:
                workSar[i][4] = workSar[i - 1][2]
        else:
            pClose = workSar[i][4]
            if workSar[i][0] > workSar[i - 1][0] and workSar[i][6] < limit:
                workSar[i][6] = MathMin(workSar[i][6] + step, limit)
            workSar[i][4] = pClose + (workSar[i][6] * (workSar[i][0] - pClose))
            if workSar[i][4] > workSar[i][3]:
                workSar[i][4] = workSar[i][3]
            if workSar[i][4] > workSar[i - 1][3]:
                workSar[i][4] = workSar[i - 1][3]
    elif high >= workSar[i][4]:
        workSar[i][5] = 1.0
        pChange.v = 1.0
        pClose = workSar[i][1]
        workSar[i][1] = low
        workSar[i][0] = high
        workSar[i][6] = step
        workSar[i][4] = pClose + (workSar[i][6] * (workSar[i][0] - pClose))
        if workSar[i][4] > workSar[i][3]:
            workSar[i][4] = workSar[i][3]
        if workSar[i][4] > workSar[i - 1][3]:
            workSar[i][4] = workSar[i - 1][3]
    else:
        pClose = workSar[i][4]
        if workSar[i][1] < workSar[i - 1][1] and workSar[i][6] < limit:
            workSar[i][6] = MathMin(workSar[i][6] + step, limit)
        workSar[i][4] = pClose + (workSar[i][6] * (workSar[i][1] - pClose))
        if workSar[i][4] < workSar[i][2]:
            workSar[i][4] = workSar[i][2]
        if workSar[i][4] < workSar[i - 1][2]:
            workSar[i][4] = workSar[i - 1][2]
    pOpen.v = workSar[i][4]
    pPosition.v = workSar[i][5]
    return pClose


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Drsi2(_MQL5Indicator):
    name = 'drsi_2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DrsiPeriod': 14,  # Dynamic rsi calculation period
        'Filter': 10.0,  # Filter
        'SARStep': 0.02,  # Parabolic SAR step
        'SARMaximum': 0.1,  # Parabolic SAR maximum
    }

