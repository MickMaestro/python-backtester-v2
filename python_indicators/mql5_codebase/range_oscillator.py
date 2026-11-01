"""Range oscillator — converted from MQL5: MQL5 Indicators/Range Oscillator/Range oscillator.mq5

Range oscillator
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Range oscillator'}, 'levels': [], 'description': ['Range oscillator'], 'name': 'Range oscillator', 'source': 'MQL5 Indicators/Range Oscillator/Range oscillator.mq5', 'folder': 'Range Oscillator', 'inputs': [{'mql': 'inpRngPeriod', 'py': 'inpRngPeriod', 'param': 'inpRngPeriod', 'type': 'int', 'default': 40, 'label': 'Range oscillator period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRngPeriod = _input('inpRngPeriod', 40)  # Range oscillator period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range oscillator (' + _str(inpRngPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _start = MathMax(i - inpRngPeriod + 1, 0)
        _max = high[ArrayMaximum(high, _start, inpRngPeriod)]
        _min = low[ArrayMinimum(low, _start, inpRngPeriod)]
        _med = (high[i] + low[i]) / 2
        val[i] = (_fdiv(100 * (_med - _min), _max - _min) if (_max != _min) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangeOscillator(_MQL5Indicator):
    name = 'Range oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRngPeriod': 40,  # Range oscillator period
    }
    y_range = (0.0, 100.0)

