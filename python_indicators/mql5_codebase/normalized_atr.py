"""Normalized ATR — converted from MQL5: MQL5 Indicators/Normalized ATR/Normalized ATR.mq5

Normalized ATR
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Normalized ATR'}, 'levels': [], 'description': ['Normalized ATR'], 'name': 'Normalized ATR', 'source': 'MQL5 Indicators/Normalized ATR/Normalized ATR.mq5', 'folder': 'Normalized ATR', 'inputs': [{'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 14, 'label': 'ATR period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAtrPeriod = _input('inpAtrPeriod', 14)  # ATR period
val = Arr(0, 0.0)
atr = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, atr, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        atr[i] = 0.0
        k = 0
        while k < inpAtrPeriod and (i - k - 1) >= 0:
            atr[i] += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
            k += 1
        atr[i] = atr[i] / inpAtrPeriod
        _start = MathMax(i - inpAtrPeriod + 1, 0)
        _max = atr[ArrayMaximum(atr, _start, inpAtrPeriod)]
        _min = atr[ArrayMinimum(atr, _start, inpAtrPeriod)]
        if _min != _max:
            val[i] = _fdiv(atr[i] - _min, _max - _min)
        else:
            val[i] = 0.5
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NormalizedATR(_MQL5Indicator):
    name = 'Normalized ATR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpAtrPeriod': 14,  # ATR period
    }

