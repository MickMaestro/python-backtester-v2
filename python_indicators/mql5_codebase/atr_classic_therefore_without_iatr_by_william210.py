"""ATR classic therefore without IATR by William210 — converted from MQL5: MQL5 Indicators/ATR classic therefore without iATR by William210/ATR classic therefore without IATR by William210.mq5

My apologies, this code is no longer available and I don't know how to remove/hide it from codebase
Copyright: Copyright 2024, William210; Link: https://www.mql5.com/fr/users/william210; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, William210', 'link': 'https://www.mql5.com/fr/users/william210', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11186720]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Old ATR '}, 'levels': [], 'description': ["My apologies, this code is no longer available and I don't know how to remove/hide it from codebase"], 'name': 'ATR classic therefore without IATR by William210', 'source': 'MQL5 Indicators/ATR classic therefore without iATR by William210/ATR classic therefore without IATR by William210.mq5', 'folder': 'ATR classic therefore without iATR by William210', 'inputs': [{'mql': 'g_ATRPeriod', 'py': 'g_ATRPeriod', 'param': 'g_ATRPeriod', 'type': 'uchar', 'default': 14, 'label': 'ATR Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_ATROld = Arr(0, 0.0)  # Oldest ATR
g_TRCal = Arr(0, 0.0)  # ATR Calculations
g_ATRPeriod = _input('g_ATRPeriod', 14)  # ATR Period

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


class ATRClassicThereforeWithoutIATRByWilliam210(_MQL5Indicator):
    name = 'ATR classic therefore without IATR by William210'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_ATRPeriod': 14,  # ATR Period
    }

