"""AO - Awesome Oscillator - beginner tutorial by William210 — converted from MQL5: MQL5 Indicators/AO - Awesome Oscillator  - without iAO() code for beginners by William210/AO - Awesome Oscillator - beginner tutorial by William210.mq5

My apologies, this code is no longer available and I don't know how to remove/hide it from codebase
Copyright: Copyright 2023, GwDs; Version: 1.04

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.04', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Awesome Oscillator'}, 'levels': [], 'description': ["My apologies, this code is no longer available and I don't know how to remove/hide it from codebase"], 'name': 'AO - Awesome Oscillator - beginner tutorial by William210', 'source': 'MQL5 Indicators/AO - Awesome Oscillator  - without iAO() code for beginners by William210/AO - Awesome Oscillator - beginner tutorial by William210.mq5', 'folder': 'AO - Awesome Oscillator  - without iAO() code for beginners by William210', 'inputs': [{'mql': 'g_AOMAPeriodFast', 'py': 'g_AOMAPeriodFast', 'param': 'g_AOMAPeriodFast', 'type': 'uchar', 'default': 5, 'label': 'Fast Moving Average Period', 'sinput': False}, {'mql': 'g_AOMaMethodFast', 'py': 'g_AOMaMethodFast', 'param': 'g_AOMaMethodFast', 'type': 'int', 'default': 0, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'g_AOapplied_priceFast', 'py': 'g_AOapplied_priceFast', 'param': 'g_AOapplied_priceFast', 'type': 'int', 'default': 5, 'label': 'Type of price or handle', 'sinput': False}, {'mql': 'g_AOMAPeriodSlow', 'py': 'g_AOMAPeriodSlow', 'param': 'g_AOMAPeriodSlow', 'type': 'uchar', 'default': 34, 'label': 'Fast Moving Average Period', 'sinput': False}, {'mql': 'g_AOMaMethodSlow', 'py': 'g_AOMaMethodSlow', 'param': 'g_AOMaMethodSlow', 'type': 'int', 'default': 0, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'g_AOapplied_priceSlow', 'py': 'g_AOapplied_priceSlow', 'param': 'g_AOapplied_priceSlow', 'type': 'int', 'default': 5, 'label': 'Type of price or handle', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_AOMAPeriodFast = _input('g_AOMAPeriodFast', 5)  # Fast Moving Average Period
g_AOMaMethodFast = _input('g_AOMaMethodFast', 0)  # Smoothing type
g_AOapplied_priceFast = _input('g_AOapplied_priceFast', PRICE_MEDIAN)  # Type of price or handle
g_AOMAPeriodSlow = _input('g_AOMAPeriodSlow', 34)  # Fast Moving Average Period
g_AOMaMethodSlow = _input('g_AOMaMethodSlow', 0)  # Smoothing type
g_AOapplied_priceSlow = _input('g_AOapplied_priceSlow', PRICE_MEDIAN)  # Type of price or handle
g_AOBuffer = Arr(0, 0.0)  # Buffer Awesome oscillator
g_AOBufferColor = Arr(0, 0.0)  # Buffer for path colors
g_PtMAFast = INVALID_HANDLE  # Pointer for the fast moving average
g_AOBufferFast = Arr(0, 0.0)  # Average calculation buffer
g_PtMASlow = INVALID_HANDLE  # Pointer for slow moving average
g_AOBufferSlow = Arr(0, 0.0)

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


class AOAwesomeOscillatorBeginnerTutorialByWilliam210(_MQL5Indicator):
    name = 'AO - Awesome Oscillator - beginner tutorial by William210'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_AOMAPeriodFast': 5,  # Fast Moving Average Period
        'g_AOMaMethodFast': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing type
        'g_AOapplied_priceFast': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Type of price or handle
        'g_AOMAPeriodSlow': 34,  # Fast Moving Average Period
        'g_AOMaMethodSlow': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing type
        'g_AOapplied_priceSlow': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Type of price or handle
    }

