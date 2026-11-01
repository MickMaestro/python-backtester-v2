"""aroon_oscillator_line — converted from MQL5: MQL5 Indicators/Aroon Oscillator Line/aroon_oscillator_line.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': -101.0, 'indicator_maximum': 101.0}, 'types': {1: 8}, 'colors': {1: [11119017, 3329330, 9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'aroon oscillator line'}, 'levels': [], 'description': [], 'name': 'aroon_oscillator_line', 'source': 'MQL5 Indicators/Aroon Oscillator Line/aroon_oscillator_line.mq5', 'folder': 'Aroon Oscillator Line', 'inputs': [{'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'int', 'default': 25, 'label': 'Aroon period', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'double', 'default': 50.0, 'label': 'Level filter value', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AroonPeriod = _input('AroonPeriod', 25)  # Aroon period
Filter = _input('Filter', 50.0)  # Level filter value
osc = Arr(0, 0.0)
oscc = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, osc, INDICATOR_DATA)
    SetIndexBuffer(1, oscc, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Filter)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -Filter)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrDimGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrDimGray)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Arron oscillator(' + DoubleToString(AroonPeriod, 0) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        max_ = high[i]
        maxi = 0.0
        min_ = low[i]
        mini = 0.0
        k = 1
        while k < AroonPeriod and (i - k) >= 0:
            if max_ < high[i - k]:
                maxi = k
                max_ = high[i - k]
            if min_ > low[i - k]:
                mini = k
                min_ = low[i - k]
            k += 1
        osc[i] = (100.0 * (mini - maxi)) / float(AroonPeriod)
        if i > 0:
            oscc[i] = 0.0
            if osc[i] > Filter:
                oscc[i] = 1.0
            if osc[i] < (-Filter):
                oscc[i] = 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AroonOscillatorLine(_MQL5Indicator):
    name = 'aroon_oscillator_line'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AroonPeriod': 25,  # Aroon period
        'Filter': 50.0,  # Level filter value
    }
    y_range = (-101.0, 101.0)

