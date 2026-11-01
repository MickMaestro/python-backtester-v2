"""Bollinger Bands beginner tutorial by William210 — converted from MQL5: MQL5 Indicators/Bands Bollinger code for beginners by William210/Bollinger Bands beginner tutorial by William210.mq5

My apologies, this code is no longer available and I don't know how to remove/hide it from codebase
Copyright: Copyright 2023, GwDs; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8421504], 2: [32768], 3: [255]}, 'widths': {3: 1, 2: 1}, 'styles': {1: 2, 2: 0, 3: 0}, 'labels': {1: 'Band Bollinger Middle', 2: 'Band Bollinger upper', 3: 'Band Bollinger Lower'}, 'levels': [], 'description': ["My apologies, this code is no longer available and I don't know how to remove/hide it from codebase"], 'name': 'Bollinger Bands beginner tutorial by William210', 'source': 'MQL5 Indicators/Bands Bollinger code for beginners by William210/Bollinger Bands beginner tutorial by William210.mq5', 'folder': 'Bands Bollinger code for beginners by William210', 'inputs': [{'mql': 'g_BBPeriod', 'py': 'g_BBPeriod', 'param': 'g_BBPeriod', 'type': 'uchar', 'default': 20, 'label': 'Averaging period', 'sinput': False}, {'mql': 'g_BBShift', 'py': 'g_BBShift', 'param': 'g_BBShift', 'type': 'uchar', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'g_BBDeviation', 'py': 'g_BBDeviation', 'param': 'g_BBDeviation', 'type': 'double', 'default': 2.0, 'label': 'number of standard deviations', 'sinput': False}, {'mql': 'g_BBApplied', 'py': 'g_BBApplied', 'param': 'g_BBApplied', 'type': 'int', 'default': 1, 'label': 'Type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_BBPeriod = _input('g_BBPeriod', 20)  # Averaging period
g_BBShift = _input('g_BBShift', 0)  # Horizontal shift
g_BBDeviation = _input('g_BBDeviation', 2.0)  # number of standard deviations
g_BBApplied = _input('g_BBApplied', PRICE_CLOSE)  # Type of price
g_PtBB = INVALID_HANDLE  # Pointer of the BB function
g_BufferBBMi = Arr(0, 0.0)  # Data buffer middle
g_BufferBBUp = Arr(0, 0.0)  # Data buffer Upper
g_BufferBBLo = Arr(0, 0.0)  # Data buffer Lower

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


class BollingerBandsBeginnerTutorialByWilliam210(_MQL5Indicator):
    name = 'Bollinger Bands beginner tutorial by William210'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_BBPeriod': 20,  # Averaging period
        'g_BBShift': 0,  # Horizontal shift
        'g_BBDeviation': 2.0,  # number of standard deviations
        'g_BBApplied': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Type of price
    }

