"""Keltner Channel for beginners by William210 — converted from MQL5: MQL5 Indicators/Keltner Channel code for beginners by William210/Keltner Channel for beginners by William210.mq5

My apologies, this code is no longer available and I don't know how to remove/hide it from codebase
Copyright: Copyright 2023, GwDs; Version: 1.03

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.03', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8421504], 2: [32768], 3: [255]}, 'widths': {3: 1, 2: 1}, 'styles': {1: 2, 2: 0, 3: 0}, 'labels': {1: 'Band Keltner Middle', 2: 'Band Keltner upper', 3: 'Band Keltner Lower'}, 'levels': [], 'description': ["My apologies, this code is no longer available and I don't know how to remove/hide it from codebase"], 'name': 'Keltner Channel for beginners by William210', 'source': 'MQL5 Indicators/Keltner Channel code for beginners by William210/Keltner Channel for beginners by William210.mq5', 'folder': 'Keltner Channel code for beginners by William210', 'inputs': [{'mql': 'g_KeltnerRatio', 'py': 'g_KeltnerRatio', 'param': 'g_KeltnerRatio', 'type': 'double', 'default': 2.0, 'label': 'Width of the channel', 'sinput': False}, {'mql': 'g_MAPeriod', 'py': 'g_MAPeriod', 'param': 'g_MAPeriod', 'type': 'uchar', 'default': 20, 'label': 'Period for averaging', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_KeltnerRatio = _input('g_KeltnerRatio', 2.0)  # Width of the channel
g_MAPeriod = _input('g_MAPeriod', 20)  # Period for averaging
g_PtMA = INVALID_HANDLE  # Pointer of the iMA function
g_PtATR = INVALID_HANDLE  # Pointer of the iRsi function
g_BufferATR = Arr(0, 0.0)  # Buffer for ATR data
g_BuffKeltnerMD = Arr(0, 0.0)  # Midlle band
g_BuffKeltnerUp = Arr(0, 0.0)  # Upper band
g_BuffKeltnerDW = Arr(0, 0.0)  # lower band

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


class KeltnerChannelForBeginnersByWilliam210(_MQL5Indicator):
    name = 'Keltner Channel for beginners by William210'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_KeltnerRatio': 2.0,  # Width of the channel
        'g_MAPeriod': 20,  # Period for averaging
    }

