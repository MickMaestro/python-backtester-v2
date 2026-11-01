"""Intrabar Volume — converted from MQL5: MQL5 Indicators/Intrabar Volume Flow/Intrabar Volume.mq5

Incoming tick volume in a rolling histogram format
Copyright: Copyright 2025, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Incoming tick volume in a rolling histogram format'], 'name': 'Intrabar Volume', 'source': 'MQL5 Indicators/Intrabar Volume Flow/Intrabar Volume.mq5', 'folder': 'Intrabar Volume Flow', 'inputs': [{'mql': 'granularTrend', 'py': 'granularTrend', 'param': 'granularTrend', 'type': 'bool', 'default': False, 'label': 'Granular trend', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
plot = Arr(0, 0.0)
col = Arr(0, 0.0)
incomingVolume = Arr(0, 0.0)
ma = Arr(0, 0.0)
closes = Arr(0, 0.0)
granularTrend = _input('granularTrend', False)  # Granular trend
period = 20

def OnInit():
    SetIndexBuffer(0, plot, INDICATOR_DATA)
    SetIndexBuffer(1, col, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, incomingVolume, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, closes, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    buffSize = ArraySize(incomingVolume)
    ArrayCopy(incomingVolume, tick_volume, 0, rates_total - 1)
    ArrayCopy(closes, close, 0, rates_total - 1)
    volumeThreshold = 0
    sum_ = 0
    if prev_calculated == 0:
        initialzeBuffers()
    for j in range(buffSize - 20, buffSize):
        sum_ += tick_volume[j]
    volumeThreshold = _idiv(sum_, 20)
    empty_data = rates_total - buffSize
    start = rates_total - 2
    for i in range(buffSize - 1, empty_data - 1, -1):
        plot[i] = (incomingVolume[buffSize - i - 1] if ((buffSize - i) > 0) else 0)
        if granularTrend:
            trend(period, i, ma, closes, buffSize)
        else:
            trend(period, i, ma, close, buffSize)
        if i > 1:
            if granularTrend:
                col[i] = (0 if (tick_volume[i] >= volumeThreshold and ma[buffSize - i] > ma[buffSize - i - 1]) else 1)
            else:
                col[i] = (0 if (ma[buffSize - 1] > ma[buffSize - 2]) else 1)
    shift(incomingVolume)
    shift(col)
    shift(closes)
    shift(ma)
    return buffSize

def initialzeBuffers():
    ArrayInitialize(plot, EMPTY_VALUE)
    ArrayInitialize(col, EMPTY_VALUE)
    ArrayInitialize(ma, EMPTY_VALUE)
    ArrayInitialize(incomingVolume, EMPTY_VALUE)
    ArrayInitialize(closes, EMPTY_VALUE)

def shift(arr):
    ArrayCopy(arr, arr, 1, 0, ArraySize(arr))

def trend(per, idx, arr, close, buffsize):
    sum_ = 0.0
    j = 1
    while j < per and (idx - j) > 0:
        sum_ += close[idx - j]
        j += 1
    arr[idx] = _fdiv(sum_, per)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IntrabarVolume(_MQL5Indicator):
    name = 'Intrabar Volume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'granularTrend': False,  # Granular trend
    }

