"""Chaos zone — converted from MQL5: MQL5 Indicators/Chaos zone/Chaos zone.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 10}, 'colors': {1: [12632256, 3329330, 14053594]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Chaos zone'}, 'levels': [], 'description': [], 'name': 'Chaos zone', 'source': 'MQL5 Indicators/Chaos zone/Chaos zone.mq5', 'folder': 'Chaos zone', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
_aoHandle = 0
_acHandle = 0

def OnInit():
    global _acHandle, _aoHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    _aoHandle = iAO(Symbol(), 0)
    if _aoHandle == INVALID_HANDLE:
        return INIT_FAILED
    _acHandle = iAC(Symbol(), 0)
    if _acHandle == INVALID_HANDLE:
        IndicatorRelease(_aoHandle)
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Chaos zone')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if BarsCalculated(_aoHandle) < rates_total:
        return prev_calculated
    if BarsCalculated(_acHandle) < rates_total:
        return prev_calculated
    _aoVal = Arr(2, 0.0, dyn=False)
    _acVal = Arr(2, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        valc[i] = 0.0
        _aoCopied = CopyBuffer(_aoHandle, 0, _DT(time[i]), 2, _aoVal)
        _acCopied = CopyBuffer(_acHandle, 0, _DT(time[i]), 2, _acVal)
        if _aoCopied == 2 and _acCopied == 2:
            valc[i] = (1 if (_aoVal[1] > _aoVal[0] and _acVal[1] > _acVal[0]) else 2 if (_aoVal[1] < _aoVal[0] and _acVal[1] < _acVal[0]) else 0)
        val[i] = (0.5 if (valc[i] == 0) else 1)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChaosZone(_MQL5Indicator):
    name = 'Chaos zone'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }
    y_range = (0.0, 1.0)

