"""pivots — converted from MQL5: MQL5 Indicators/pivots calculation based on pine script v4/pivots.mq5

Copyright: Copyright 2022, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 2, 2: 2}, 'colors': {1: [255], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'ph', 2: 'pl'}, 'levels': [], 'description': [], 'name': 'pivots', 'source': 'MQL5 Indicators/pivots calculation based on pine script v4/pivots.mq5', 'folder': 'pivots calculation based on pine script v4', 'inputs': [{'mql': '_right', 'py': '_right', 'param': '_right', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': '_left', 'py': '_left', 'param': '_left', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
_right = _input('_right', 10)
_left = _input('_left', 10)
phBuffer = Arr(0, 0.0)
plBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, phBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, plBuffer, INDICATOR_DATA)
    ArraySetAsSeries(phBuffer, True)
    ArraySetAsSeries(plBuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    BARS = MathMax(Bars(Symbol(), PERIOD_CURRENT) - (_right + _left) - prev_calculated, 1)
    pivothigh(high, phBuffer, _left, _right, 0, BARS)
    pivotlow(low, plBuffer, _left, _right, 0, BARS)
    return rates_total

def pivothigh(high, output, left, right, start_pos, count):
    for index in range(start_pos, start_pos + count):
        next_index = False
        i = index + right
        for j in range(i + 1, i + 1 + left):
            if j > (Bars(Symbol(), PERIOD_CURRENT) - 1):
                break
            if high[j] > high[i]:
                output[index] = EMPTY_VALUE
                next_index = True
                break
        if next_index == True:
            continue
        for j in range(i - 1, i - 1 - right, -1):
            if j < 0:
                break
            if high[j] > high[i]:
                output[index] = EMPTY_VALUE
                next_index = True
                break
        if next_index == True:
            continue
        output[index] = high[i]

def pivotlow(low, output, left, right, start_pos, count):
    for index in range(start_pos, start_pos + count):
        next_index = False
        i = index + right
        for j in range(i + 1, i + 1 + left):
            if j > (Bars(Symbol(), PERIOD_CURRENT) - 1):
                break
            if low[j] < low[i]:
                output[index] = EMPTY_VALUE
                next_index = True
                break
        if next_index == True:
            continue
        for j in range(i - 1, i - 1 - right, -1):
            if j < 0:
                break
            if low[j] < low[i]:
                output[index] = EMPTY_VALUE
                next_index = True
                break
        if next_index == True:
            continue
        output[index] = low[i]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pivots(_MQL5Indicator):
    name = 'pivots'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        '_right': 10,
        '_left': 10,
    }

