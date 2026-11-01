"""CCI beginner tutorial by William210 — converted from MQL5: MQL5 Indicators/CCI beginner tutorial by William210/CCI beginner tutorial by William210.mq5

My apologies, this code is no longer available and I don't know how to remove/hide it from codebase
Copyright: Copyright 2024, GwDs; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, GwDs', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CCI'}, 'levels': [-100.0, 100.0, 0.0], 'description': ["My apologies, this code is no longer available and I don't know how to remove/hide it from codebase"], 'name': 'CCI beginner tutorial by William210', 'source': 'MQL5 Indicators/CCI beginner tutorial by William210/CCI beginner tutorial by William210.mq5', 'folder': 'CCI beginner tutorial by William210', 'inputs': [{'mql': 'g_CCIPeriod', 'py': 'g_CCIPeriod', 'param': 'g_CCIPeriod', 'type': 'uchar', 'default': 14, 'label': 'CCI Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_CCIPeriod = _input('g_CCIPeriod', 14)  # CCI Period
g_PtCCI = INVALID_HANDLE  # Pointer of the iCCI function
g_BufferCCI = Arr(0, 0.0)  # Data buffer

def OnInit():
    Comment("My apologies, this code is no longer available and I don't know how to remove/hide it from codebase")
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIBeginnerTutorialByWilliam210(_MQL5Indicator):
    name = 'CCI beginner tutorial by William210'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_CCIPeriod': 14,  # CCI Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

