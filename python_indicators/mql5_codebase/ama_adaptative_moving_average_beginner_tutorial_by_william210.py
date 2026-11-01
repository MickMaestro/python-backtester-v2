"""AMA  -Adaptative Moving Average - beginner tutorial by William210 — converted from MQL5: MQL5 Indicators/AMA - Adaptive Moving Average - code for beginners by William210/AMA  -Adaptative Moving Average - beginner tutorial by William210.mq5

My apologies, this code is no longer available and I don't know how to remove/hide it from codebase
Copyright: Copyright 2023, GwDs; Version: 1.03

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.03', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'AMA'}, 'levels': [], 'description': ["My apologies, this code is no longer available and I don't know how to remove/hide it from codebase"], 'name': 'AMA  -Adaptative Moving Average - beginner tutorial by William210', 'source': 'MQL5 Indicators/AMA - Adaptive Moving Average - code for beginners by William210/AMA  -Adaptative Moving Average - beginner tutorial by William210.mq5', 'folder': 'AMA - Adaptive Moving Average - code for beginners by William210', 'inputs': [{'mql': 'g_ama_period', 'py': 'g_ama_period', 'param': 'g_ama_period', 'type': 'uchar', 'default': 9, 'label': 'Period of calculation', 'sinput': False}, {'mql': 'g_fast_ma_period', 'py': 'g_fast_ma_period', 'param': 'g_fast_ma_period', 'type': 'uchar', 'default': 2, 'label': 'Period of fast MA', 'sinput': False}, {'mql': 'g_slow_ma_period', 'py': 'g_slow_ma_period', 'param': 'g_slow_ma_period', 'type': 'uchar', 'default': 30, 'label': 'Period of slow MA', 'sinput': False}, {'mql': 'g_ama_shift', 'py': 'g_ama_shift', 'param': 'g_ama_shift', 'type': 'uchar', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'g_applied_price', 'py': 'g_applied_price', 'param': 'g_applied_price', 'type': 'int', 'default': 1, 'label': 'Type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_ama_period = _input('g_ama_period', 9)  # Period of calculation
g_fast_ma_period = _input('g_fast_ma_period', 2)  # Period of fast MA
g_slow_ma_period = _input('g_slow_ma_period', 30)  # Period of slow MA
g_ama_shift = _input('g_ama_shift', 0)  # Horizontal shift
g_applied_price = _input('g_applied_price', PRICE_CLOSE)  # Type of price
g_PtAMA = INVALID_HANDLE  # Pointer of the iRsi function
g_iAMABuffer = Arr(0, 0.0)  # Data buffer

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


class AMAAdaptativeMovingAverageBeginnerTutorialByWilliam210(_MQL5Indicator):
    name = 'AMA  -Adaptative Moving Average - beginner tutorial by William210'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_ama_period': 9,  # Period of calculation
        'g_fast_ma_period': 2,  # Period of fast MA
        'g_slow_ma_period': 30,  # Period of slow MA
        'g_ama_shift': 0,  # Horizontal shift
        'g_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Type of price
    }

