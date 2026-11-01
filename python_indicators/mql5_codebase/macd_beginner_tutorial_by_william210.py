"""MACD beginner tutorial by William210 — converted from MQL5: MQL5 Indicators/MACD code for beginners by William210/MACD beginner tutorial by William210.mq5

My apologies, this code is no longer available and I don't know how to remove/hide it from codebase
Copyright: Copyright 2023, GwDs; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.02', 'window': 'separate', 'indicator_plots': 2, 'indicator_buffers': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MACD', 2: 'Signal'}, 'levels': [], 'description': ["My apologies, this code is no longer available and I don't know how to remove/hide it from codebase"], 'name': 'MACD beginner tutorial by William210', 'source': 'MQL5 Indicators/MACD code for beginners by William210/MACD beginner tutorial by William210.mq5', 'folder': 'MACD code for beginners by William210', 'inputs': [{'mql': 'g_MACDFast', 'py': 'g_MACDFast', 'param': 'g_MACDFast', 'type': 'uchar', 'default': 12, 'label': 'Period of fast ma', 'sinput': False}, {'mql': 'g_MACDLow', 'py': 'g_MACDLow', 'param': 'g_MACDLow', 'type': 'uchar', 'default': 26, 'label': 'Period of slow ma', 'sinput': False}, {'mql': 'g_MACDSignal', 'py': 'g_MACDSignal', 'param': 'g_MACDSignal', 'type': 'uchar', 'default': 9, 'label': 'Period of averaging of difference', 'sinput': False}, {'mql': 'g_MACDApplied', 'py': 'g_MACDApplied', 'param': 'g_MACDApplied', 'type': 'int', 'default': 1, 'label': 'Type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_MACDFast = _input('g_MACDFast', 12)  # Period of fast ma
g_MACDLow = _input('g_MACDLow', 26)  # Period of slow ma
g_MACDSignal = _input('g_MACDSignal', 9)  # Period of averaging of difference
g_MACDApplied = _input('g_MACDApplied', PRICE_CLOSE)  # Type of price
g_PtMACD = INVALID_HANDLE  # Pointer of the BB function
g_BuffMACD = Arr(0, 0.0)  # Data buffer MACD
g_BuffMACDSig = Arr(0, 0.0)  # Data buffer MACD Signal

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


class MACDBeginnerTutorialByWilliam210(_MQL5Indicator):
    name = 'MACD beginner tutorial by William210'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_MACDFast': 12,  # Period of fast ma
        'g_MACDLow': 26,  # Period of slow ma
        'g_MACDSignal': 9,  # Period of averaging of difference
        'g_MACDApplied': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Type of price
    }

