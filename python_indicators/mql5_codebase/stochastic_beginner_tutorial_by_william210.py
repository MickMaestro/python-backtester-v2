"""Stochastic beginner tutorial by William210 — converted from MQL5: MQL5 Indicators/Stochastic code for beginners by William210/Stochastic beginner tutorial by William210.mq5

My apologies, this code is no longer available and I don't know how to remove/hide it from codebase
Copyright: Copyright 2023, GwDs; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.02', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'Stochastic', 2: 'Stochastic Signal'}, 'levels': [80.0, 20.0], 'description': ["My apologies, this code is no longer available and I don't know how to remove/hide it from codebase"], 'name': 'Stochastic beginner tutorial by William210', 'source': 'MQL5 Indicators/Stochastic code for beginners by William210/Stochastic beginner tutorial by William210.mq5', 'folder': 'Stochastic code for beginners by William210', 'inputs': [{'mql': 'g_StoKPeriod', 'py': 'g_StoKPeriod', 'param': 'g_StoKPeriod', 'type': 'uchar', 'default': 5, 'label': 'K-period (number of bars for calculations', 'sinput': False}, {'mql': 'g_StoDPeriod', 'py': 'g_StoDPeriod', 'param': 'g_StoDPeriod', 'type': 'uchar', 'default': 3, 'label': 'D period (the period of primary', 'sinput': False}, {'mql': 'g_StoSlowing', 'py': 'g_StoSlowing', 'param': 'g_StoSlowing', 'type': 'uchar', 'default': 3, 'label': 'Period of final smoothing', 'sinput': False}, {'mql': 'g_StoMethod', 'py': 'g_StoMethod', 'param': 'g_StoMethod', 'type': 'int', 'default': 0, 'label': 'Type of smoothing', 'sinput': False}, {'mql': 'g_StoPrice_field', 'py': 'g_StoPrice_field', 'param': 'g_StoPrice_field', 'type': 'int', 'default': 0, 'label': 'Method of calculation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_StoKPeriod = _input('g_StoKPeriod', 5)  # K-period (number of bars for calculations
g_StoDPeriod = _input('g_StoDPeriod', 3)  # D period (the period of primary
g_StoSlowing = _input('g_StoSlowing', 3)  # Period of final smoothing
g_StoMethod = _input('g_StoMethod', MODE_SMA)  # Type of smoothing
g_StoPrice_field = _input('g_StoPrice_field', STO_LOWHIGH)  # Method of calculation
g_ptStochastic = INVALID_HANDLE  # Pointer of the Stochastic
g_BuffSto = Arr(0, 0.0)  # Buffer Stochastic
g_BuffStoSignal = Arr(0, 0.0)  # Buffer Stochastic Signal

def OnInit():
    Comment("My apologies, this code is no longer available and I don't know how to remove/hide it from codebase")
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticBeginnerTutorialByWilliam210(_MQL5Indicator):
    name = 'Stochastic beginner tutorial by William210'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_StoKPeriod': 5,  # K-period (number of bars for calculations
        'g_StoDPeriod': 3,  # D period (the period of primary
        'g_StoSlowing': 3,  # Period of final smoothing
        'g_StoMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Type of smoothing
        'g_StoPrice_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Method of calculation
    }
    y_range = (0.0, 100.0)

