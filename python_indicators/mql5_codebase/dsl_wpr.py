"""Dsl - WPR — converted from MQL5: MQL5 Indicators/DSL - WPR/Dsl - WPR.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 3329330, 42495]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'value'}, 'levels': [], 'description': [], 'name': 'Dsl - WPR', 'source': 'MQL5 Indicators/DSL - WPR/Dsl - WPR.mq5', 'folder': 'DSL - WPR', 'inputs': [{'mql': 'inpWprPeriod', 'py': 'inpWprPeriod', 'param': 'inpWprPeriod', 'type': 'int', 'default': 14, 'label': 'WPR period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpWprPeriod = _input('inpWprPeriod', 14)  # WPR period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # Signal period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    for i in range(0, 2):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, '(dsl) WPR (' + _str(inpWprPeriod) + ',' + _str(inpSignalPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alpha = _fdiv(2.0, 1.0 + inpSignalPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - inpWprPeriod + 1, 0)
        _max = high[ArrayMaximum(high, _start, inpWprPeriod)]
        _min = low[ArrayMinimum(low, _start, inpWprPeriod)]
        val[i] = (_fdiv((-(_max - close[i])) * 100, _max - _min) if (_max != _min) else 0)
        levelUp[i] = (((levelUp[i - 1] + (alpha * (val[i] - levelUp[i - 1]))) if (val[i] > -50) else levelUp[i - 1]) if (i > 0) else 0)
        levelDn[i] = (((levelDn[i - 1] + (alpha * (val[i] - levelDn[i - 1]))) if (val[i] < -50) else levelDn[i - 1]) if (i > 0) else 0)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DslWPR(_MQL5Indicator):
    name = 'Dsl - WPR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpWprPeriod': 14,  # WPR period
        'inpSignalPeriod': 9,  # Signal period
    }

