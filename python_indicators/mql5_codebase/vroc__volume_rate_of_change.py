"""VROC — converted from MQL5: MQL5 Indicators/Volume Rate of Change/VROC.mq5

Volume Rate of Change
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Volume Rate of Change'], 'name': 'VROC', 'source': 'MQL5 Indicators/Volume Rate of Change/VROC.mq5', 'folder': 'Volume Rate of Change', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'VROC period', 'sinput': False}, {'mql': 'inpVolumeType', 'py': 'inpVolumeType', 'param': 'inpVolumeType', 'type': 'int', 'default': 1, 'label': 'Volume type to use', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enVolumeType
vt_real = 0
vt_tick = 1
_enum('enVolumeType', {0: 'vt_real', 1: 'vt_tick'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # VROC period
inpVolumeType = _input('inpVolumeType', vt_tick)  # Volume type to use
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volume rate of change (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        val[i] = ((float(_idiv(100 * (volume[i] - volume[i - inpPeriod]), MathMax(volume[i], 1))) if (inpVolumeType == vt_real) else _fdiv(100.0 * (tick_volume[i] - tick_volume[i - inpPeriod]), tick_volume[i])) if (i > inpPeriod) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VROC(_MQL5Indicator):
    name = 'VROC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 14,  # VROC period
        'inpVolumeType': _Choice({0: 'Use real volume for calculation', 1: 'Use tick volume for calculation'}, default=1),  # Volume type to use
    }

