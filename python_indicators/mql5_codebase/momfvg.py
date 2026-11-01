"""MomFVG — converted from MQL5: MQL5 Indicators/FVG based Momentum Detection/MomFVG.mq5

Copyright: Copyright 2025, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'UpMom', 2: 'DnMom'}, 'levels': [], 'description': [], 'name': 'MomFVG', 'source': 'MQL5 Indicators/FVG based Momentum Detection/MomFVG.mq5', 'folder': 'FVG based Momentum Detection', 'inputs': [{'mql': 'window_size', 'py': 'window_size', 'param': 'window_size', 'type': 'int', 'default': 50, 'label': 'window size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpMomBuffer = Arr(0, 0.0)
DnMomBuffer = Arr(0, 0.0)
window_size = _input('window_size', 50)  # window size

def OnInit():
    SetIndexBuffer(0, UpMomBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnMomBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpMomBuffer, True)
    ArraySetAsSeries(DnMomBuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    BARS = MathMax(rates_total - prev_calculated - window_size, 1)
    for i in range(BARS, 0 - 1, -1):
        UpMomBuffer[i] = 0.0
        for j in range(i + 1, i + window_size):
            UpMomBuffer[i] += FVGUpMom(j)
        DnMomBuffer[i] = 0.0
        for j in range(i + 1, i + window_size):
            DnMomBuffer[i] += FVGDnMom(j)
    return rates_total

def FVGUpMom(j):
    high = iHigh(Symbol(), PERIOD_CURRENT, j + 1)
    low = iLow(Symbol(), PERIOD_CURRENT, j - 1)
    return MathMax(low - high, 0)

def FVGDnMom(j):
    high = iHigh(Symbol(), PERIOD_CURRENT, j - 1)
    low = iLow(Symbol(), PERIOD_CURRENT, j + 1)
    return MathMax(low - high, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MomFVG(_MQL5Indicator):
    name = 'MomFVG'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'window_size': 50,  # window size
    }

