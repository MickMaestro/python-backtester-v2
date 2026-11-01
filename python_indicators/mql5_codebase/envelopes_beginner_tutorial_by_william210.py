"""Envelopes beginner tutorial by William210 — converted from MQL5: MQL5 Indicators/Envelopes beginner tutorial By William210/Envelopes beginner tutorial by William210.mq5

My apologies, this code is no longer available and I don't know how to remove/hide it from codebase
Copyright: Copyright 2023, GwDs; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper', 2: 'Lower'}, 'levels': [], 'description': ["My apologies, this code is no longer available and I don't know how to remove/hide it from codebase"], 'name': 'Envelopes beginner tutorial by William210', 'source': 'MQL5 Indicators/Envelopes beginner tutorial By William210/Envelopes beginner tutorial by William210.mq5', 'folder': 'Envelopes beginner tutorial By William210', 'inputs': [{'mql': 'g_period', 'py': 'g_period', 'param': 'g_period', 'type': 'int', 'default': 14, 'label': 'Period of moving average', 'sinput': False}, {'mql': 'g__shift', 'py': 'g__shift', 'param': 'g__shift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'g__method', 'py': 'g__method', 'param': 'g__method', 'type': 'int', 'default': 0, 'label': 'Type of smoothing', 'sinput': False}, {'mql': 'g_applied_price', 'py': 'g_applied_price', 'param': 'g_applied_price', 'type': 'int', 'default': 1, 'label': 'Type of price', 'sinput': False}, {'mql': 'g_deviation', 'py': 'g_deviation', 'param': 'g_deviation', 'type': 'double', 'default': 0.1, 'label': 'deviation of borders from the moving average', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_period = _input('g_period', 14)  # Period of moving average
g__shift = _input('g__shift', 0)  # Shift
g__method = _input('g__method', MODE_SMA)  # Type of smoothing
g_applied_price = _input('g_applied_price', PRICE_CLOSE)  # Type of price
g_deviation = _input('g_deviation', 0.1)  # deviation of borders from the moving average
g_PtEnvelope = INVALID_HANDLE
g_EnvBuffUp = Arr(0, 0.0)  # Data buffer
g_EnvBuffDw = Arr(0, 0.0)  # Data buffer

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


class EnvelopesBeginnerTutorialByWilliam210(_MQL5Indicator):
    name = 'Envelopes beginner tutorial by William210'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_period': 14,  # Period of moving average
        'g__shift': 0,  # Shift
        'g__method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Type of smoothing
        'g_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Type of price
        'g_deviation': 0.1,  # deviation of borders from the moving average
    }

