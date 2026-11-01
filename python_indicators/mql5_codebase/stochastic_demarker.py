"""Stochastic DeMarker — converted from MQL5: MQL5 Indicators/Stochastic DeMarker/Stochastic DeMarker.mq5

Stochastic DeMarker
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2, 'indicator_maximum': 1.0, 'indicator_minimum': 0.0}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16760576, 8036607], 2: [11119017]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {1: 'Stochastic DeMarker', 2: 'Signal'}, 'levels': [0.7, 0.3], 'description': ['Stochastic DeMarker'], 'name': 'Stochastic DeMarker', 'source': 'MQL5 Indicators/Stochastic DeMarker/Stochastic DeMarker.mq5', 'folder': 'Stochastic DeMarker', 'inputs': [{'mql': 'inpDemPeriod', 'py': 'inpDemPeriod', 'param': 'inpDemPeriod', 'type': 'int', 'default': 14, 'label': 'DeMarker period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpDemPeriod = _input('inpDemPeriod', 14)  # DeMarker period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
dem = Arr(0, 0.0)
work = Arr(0, 0.0)
_demHandle = 0

def OnInit():
    global _demHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    SetIndexBuffer(3, dem, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, work, INDICATOR_CALCULATIONS)
    _demHandle = iDeMarker(Symbol(), 0, inpDemPeriod)
    if _demHandle == INVALID_HANDLE:
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic DeMarker (' + _str(inpDemPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_demHandle) < rates_total:
        return prev_calculated
    _demVal = Arr(1, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _demCopied = CopyBuffer(_demHandle, 0, _DT(time[i]), 1, _demVal)
        if _demCopied != 1:
            return prev_calculated
        dem[i] = _demVal[0]
        _start = MathMax(i - inpDemPeriod + 1, 0)
        _lo = dem[ArrayMinimum(dem, _start, inpDemPeriod)]
        _hi = dem[ArrayMaximum(dem, _start, inpDemPeriod)]
        work[i] = (_fdiv(dem[i] - _lo, _hi - _lo) if (_hi != _lo) else 0)
        val[i] = ((((4 * work[i]) + (3 * work[i - 1]) + (2 * work[i - 2]) + work[i - 3]) / 10) if (i > 3) else 0)
        signal[i] = (((0.96 * val[i - 1]) + 0.02) if (i > 0) else val[i])
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticDeMarker(_MQL5Indicator):
    name = 'Stochastic DeMarker'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDemPeriod': 14,  # DeMarker period
    }
    y_range = (0.0, 1.0)

