"""Reverse No Repair — converted from MQL5: MQL5 Indicators/Reverse No Repair/Reverse No Repair.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Reverse No Repair', 'source': 'MQL5 Indicators/Reverse No Repair/Reverse No Repair.mq5', 'folder': 'Reverse No Repair', 'inputs': [{'mql': 'FilterCandle', 'py': 'FilterCandle', 'param': 'FilterCandle', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FilterCandle = _input('FilterCandle', 12)
bufferUp = Arr(0, 0.0)
bufferDown = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(1, bufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(bufferDown, True)
    ArraySetAsSeries(bufferUp, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    limit = 0
    if prev_calculated > 0:
        limit = rates_total - prev_calculated - 1
    else:
        limit = rates_total - 1
    for i in range(limit, 0 - 1, -1):
        bufferUp[i] = 0.0
        bufferDown[i] = 0.0
        if (i + FilterCandle + 2) < rates_total:
            if isUp(i + 1):
                bufferUp[i + 2] = low[i + 2]
            if isDown(i + 1):
                bufferDown[i + 2] = high[i + 2]
    return rates_total

def isUp(index):
    flag = True
    preIndex = index + 1
    if (iLow(Symbol(), 0, index) > iLow(Symbol(), 0, preIndex) and iHigh(Symbol(), 0, index) > iHigh(Symbol(), 0, preIndex)) and iClose(Symbol(), 0, index) > iClose(Symbol(), 0, preIndex):
        startIndex = preIndex + 1
        endIndex = preIndex + FilterCandle - 1
        for i in range(startIndex, endIndex + 1):
            if iLow(Symbol(), 0, i) < iLow(Symbol(), 0, preIndex):
                flag = False
                break
    else:
        flag = False
    return flag

def isDown(index):
    flag = True
    preIndex = index + 1
    if (iLow(Symbol(), 0, index) < iLow(Symbol(), 0, preIndex) and iHigh(Symbol(), 0, index) < iHigh(Symbol(), 0, preIndex)) and iClose(Symbol(), 0, index) < iClose(Symbol(), 0, preIndex):
        start = preIndex + 1
        end = preIndex + FilterCandle - 1
        for i in range(start, end + 1):
            if iHigh(Symbol(), 0, i) > iHigh(Symbol(), 0, preIndex):
                flag = False
                break
    else:
        flag = False
    return flag


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ReverseNoRepair(_MQL5Indicator):
    name = 'Reverse No Repair'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FilterCandle': 12,
    }

