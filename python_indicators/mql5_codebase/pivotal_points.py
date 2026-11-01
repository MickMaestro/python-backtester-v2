"""Pivotal points — converted from MQL5: MQL5 Indicators/Pivotal Points/Pivotal points.mq5

Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 4}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Pivotal points'}, 'levels': [], 'description': [], 'name': 'Pivotal points', 'source': 'MQL5 Indicators/Pivotal Points/Pivotal points.mq5', 'folder': 'Pivotal Points', 'inputs': [{'mql': 'inpLookBackBars', 'py': 'inpLookBackBars', 'param': 'inpLookBackBars', 'type': 'int', 'default': 200, 'label': 'Look back bars', 'sinput': False}, {'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 1, 'label': 'ATR period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpLookBackBars = _input('inpLookBackBars', 200)  # Look back bars
inpAtrPeriod = _input('inpAtrPeriod', 1)  # ATR period
ih = Arr(0, 0.0)
il = Arr(0, 0.0)
atr = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ih)
    SetIndexBuffer(1, il)
    SetIndexBuffer(2, atr, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        atr[i] = 0.0
        k = 0
        while k < inpAtrPeriod and (i - k) >= 0:
            atr[i] += ((MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])) if (i > 0) else (high[i] - low[i]))
            k += 1
        atr[i] = atr[i] / inpAtrPeriod
        il[i] = EMPTY_VALUE
        ih[i] = il[i]
        _start = MathMax(i - inpLookBackBars + 1, 0)
        if ArrayMaximum(atr, _start, inpLookBackBars) == i:
            ih[i] = high[i]
            il[i] = low[i]
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PivotalPoints(_MQL5Indicator):
    name = 'Pivotal points'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpLookBackBars': 200,  # Look back bars
        'inpAtrPeriod': 1,  # ATR period
    }

