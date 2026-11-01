"""T3 levels — converted from MQL5: MQL5 Indicators/T3 levels/T3 levels.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 3329330, 42495]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'T3'}, 'levels': [], 'description': [], 'name': 'T3 levels', 'source': 'MQL5 Indicators/T3 levels/T3 levels.mq5', 'folder': 'T3 levels', 'inputs': [{'mql': 'inpT3Period', 'py': 'inpT3Period', 'param': 'inpT3Period', 'type': 'int', 'default': 9, 'label': 'T3 period', 'sinput': False}, {'mql': 'inpT3Hot', 'py': 'inpT3Hot', 'param': 'inpT3Hot', 'type': 'double', 'default': 0.3, 'label': 'T3 "hot"', 'sinput': False}, {'mql': 'inpT3Type', 'py': 'inpT3Type', 'param': 'inpT3Type', 'type': 'int', 'default': 0, 'label': 'T3 type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# ---- inputs and global variables
inpT3Period = _input('inpT3Period', 9)  # T3 period
inpT3Hot = _input('inpT3Hot', 0.3)  # T3 "hot"
inpT3Type = _input('inpT3Type', t3_tillson)  # T3 type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
workT3 = Arr(0, 0.0, dims=(18,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3 levels (' + _str(inpT3Period) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iT3(close[i], inpT3Period, inpT3Hot, inpT3Type == t3_tillson, i, rates_total, False, 0)
        levelUp[i] = iT3(val[i], inpT3Period, inpT3Hot, inpT3Type == t3_tillson, i, rates_total, ((not (val[i] > levelDn[i - 1])) if (i > 0) else False), 1)
        levelDn[i] = iT3(val[i], inpT3Period, inpT3Hot, inpT3Type == t3_tillson, i, rates_total, ((not (val[i] < levelUp[i - 1])) if (i > 0) else False), 2)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

def iT3(price, period, hot, original, r, bars, copy=False, instanceNo=0):
    if ArrayRange(workT3, 0) != bars:
        ArrayResize(workT3, bars)
    if ArrayRange(workT3Coeffs, 0) < (instanceNo + 1):
        ArrayResize(workT3Coeffs, instanceNo + 1)
    if workT3Coeffs[instanceNo][0] != period:
        workT3Coeffs[instanceNo][0] = period
        workT3Coeffs[instanceNo][1] = (-hot) * hot * hot
        workT3Coeffs[instanceNo][2] = (3 * hot * hot) + (3 * hot * hot * hot)
        workT3Coeffs[instanceNo][3] = (-6 * hot * hot) - (3 * hot) - (3 * hot * hot * hot)
        workT3Coeffs[instanceNo][4] = 1 + (3 * hot) + (hot * hot * hot) + (3 * hot * hot)
        if original:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 1.0 + period)
        else:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
    buffer = instanceNo * 6
    for k in range(0, 6):
        workT3[r][k + buffer] = (workT3[r - 1][k + buffer] if (r > 0) else price)
    if ((not copy) and r > 0) and period > 1:
        workT3[r][0 + buffer] = workT3[r - 1][0 + buffer] + (workT3Coeffs[instanceNo][5] * (price - workT3[r - 1][0 + buffer]))
        workT3[r][1 + buffer] = workT3[r - 1][1 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][0 + buffer] - workT3[r - 1][1 + buffer]))
        workT3[r][2 + buffer] = workT3[r - 1][2 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][1 + buffer] - workT3[r - 1][2 + buffer]))
        workT3[r][3 + buffer] = workT3[r - 1][3 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][2 + buffer] - workT3[r - 1][3 + buffer]))
        workT3[r][4 + buffer] = workT3[r - 1][4 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][3 + buffer] - workT3[r - 1][4 + buffer]))
        workT3[r][5 + buffer] = workT3[r - 1][5 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][4 + buffer] - workT3[r - 1][5 + buffer]))
    return (workT3Coeffs[instanceNo][1] * workT3[r][5 + buffer]) + (workT3Coeffs[instanceNo][2] * workT3[r][4 + buffer]) + (workT3Coeffs[instanceNo][3] * workT3[r][3 + buffer]) + (workT3Coeffs[instanceNo][4] * workT3[r][2 + buffer])


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3Levels(_MQL5Indicator):
    name = 'T3 levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpT3Period': 9,  # T3 period
        'inpT3Hot': 0.3,  # T3 "hot"
        'inpT3Type': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=0),  # T3 type
    }

