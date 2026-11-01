"""Ema levels — converted from MQL5: MQL5 Indicators/EMA levels/Ema levels.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 3329330, 42495]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'EMA'}, 'levels': [], 'description': [], 'name': 'Ema levels', 'source': 'MQL5 Indicators/EMA levels/Ema levels.mq5', 'folder': 'EMA levels', 'inputs': [{'mql': 'inpEmaPeriod', 'py': 'inpEmaPeriod', 'param': 'inpEmaPeriod', 'type': 'int', 'default': 9, 'label': 'Ema period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpEmaPeriod = _input('inpEmaPeriod', 9)  # Ema period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    for i in range(0, 2):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ema levels (' + _str(inpEmaPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alpha = _fdiv(2.0, 1.0 + inpEmaPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iEma(close[i], inpEmaPeriod, i, rates_total, 0)
        levelUp[i] = (((levelUp[i - 1] + (alpha * (val[i] - levelUp[i - 1]))) if (val[i] > levelDn[i - 1]) else levelUp[i - 1]) if (i > 0) else val[i])
        levelDn[i] = (((levelDn[i - 1] + (alpha * (val[i] - levelDn[i - 1]))) if (val[i] < levelUp[i - 1]) else levelDn[i - 1]) if (i > 0) else val[i])
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EmaLevels(_MQL5Indicator):
    name = 'Ema levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpEmaPeriod': 9,  # Ema period
    }

