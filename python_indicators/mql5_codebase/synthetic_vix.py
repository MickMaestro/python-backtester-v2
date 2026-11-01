"""Synthetic VIX — converted from MQL5: MQL5 Indicators/Synthetic VIX/Synthetic VIX.mq5

Synthetic VIX
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Synthetic VIX'}, 'levels': [], 'description': ['Synthetic VIX'], 'name': 'Synthetic VIX', 'source': 'MQL5 Indicators/Synthetic VIX/Synthetic VIX.mq5', 'folder': 'Synthetic VIX', 'inputs': [{'mql': 'inpVixPeriod', 'py': 'inpVixPeriod', 'param': 'inpVixPeriod', 'type': 'int', 'default': 20, 'label': 'Synthetic VIX period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVixPeriod = _input('inpVixPeriod', 20)  # Synthetic VIX period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Synthetic VIX (' + _str(inpVixPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - inpVixPeriod + 1, 0)
        _highest = high[ArrayMaximum(high, _start, inpVixPeriod)]
        val[i] = _fdiv(100.0 * (_highest - low[i]), _highest)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SyntheticVIX(_MQL5Indicator):
    name = 'Synthetic VIX'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpVixPeriod': 20,  # Synthetic VIX period
    }

