"""Ichimoku beginner tutorial by William210 — converted from MQL5: MQL5 Indicators/Ichimoku code for beginners by William210/Ichimoku beginner tutorial by William210.mq5

My apologies, this code is no longer available and I don't know how to remove/hide it from codebase
Copyright: Copyright 2023, GwDs; Version: 1.03

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.03', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 7, 4: 1}, 'colors': {1: [255], 2: [16711680], 3: [6333684, 14204888], 4: [65280]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Tenkan_sen', 2: 'Kijun_sen', 3: 'Senkou Span A;Senkou Span B', 4: 'Chinkou_Span'}, 'levels': [], 'description': ["My apologies, this code is no longer available and I don't know how to remove/hide it from codebase"], 'name': 'Ichimoku beginner tutorial by William210', 'source': 'MQL5 Indicators/Ichimoku code for beginners by William210/Ichimoku beginner tutorial by William210.mq5', 'folder': 'Ichimoku code for beginners by William210', 'inputs': [{'mql': 'g_tenkan_sen', 'py': 'g_tenkan_sen', 'param': 'g_tenkan_sen', 'type': 'uchar', 'default': 9, 'label': 'Period of Tenkan-sen', 'sinput': False}, {'mql': 'g_kijun_sen', 'py': 'g_kijun_sen', 'param': 'g_kijun_sen', 'type': 'uchar', 'default': 26, 'label': 'Period of Kijun-sen', 'sinput': False}, {'mql': 'g_senkou_span_b', 'py': 'g_senkou_span_b', 'param': 'g_senkou_span_b', 'type': 'uchar', 'default': 52, 'label': 'Period of Senkou Span B', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_tenkan_sen = _input('g_tenkan_sen', 9)  # Period of Tenkan-sen
g_kijun_sen = _input('g_kijun_sen', 26)  # Period of Kijun-sen
g_senkou_span_b = _input('g_senkou_span_b', 52)  # Period of Senkou Span B
g_ptIshimoku = INVALID_HANDLE  # Pointer of the Ishimoku function
g_BuffTenkan_sen = Arr(0, 0.0)  # Buffer TENKANSEN
g_BuffKijun_sen = Arr(0, 0.0)  # Buffer KIJUNSEN
g_BuffSenkou_Span_A = Arr(0, 0.0)  # Buffer SENKOU
g_BuffSenkou_Span_B = Arr(0, 0.0)  # Buffer SENKOU
g_BuffChinkou = Arr(0, 0.0)  # Buffer CHIKOU

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


class IchimokuBeginnerTutorialByWilliam210(_MQL5Indicator):
    name = 'Ichimoku beginner tutorial by William210'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_tenkan_sen': 9,  # Period of Tenkan-sen
        'g_kijun_sen': 26,  # Period of Kijun-sen
        'g_senkou_span_b': 52,  # Period of Senkou Span B
    }

