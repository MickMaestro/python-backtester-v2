"""TrendLinearReg — converted from MQL5: MQL5 Indicators/TrendLinearReg - indicator for MetaTrader 5/TrendLinearReg.mq5

Copyright: Copyright 2022, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [3329330], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'TrendLinearReg', 'source': 'MQL5 Indicators/TrendLinearReg - indicator for MetaTrader 5/TrendLinearReg.mq5', 'folder': 'TrendLinearReg - indicator for MetaTrader 5', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
barsToCount = 34  # Bars to calculate
buffer0 = Arr(0, 0.0)
buffer1 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, buffer0)
    SetIndexBuffer(1, buffer1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    b = 0.0
    c = 0.0
    sumy = 0.0
    sumx = 0.0
    sumxy = 0.0
    sumx2 = 0.0
    prev = 0.0
    current = 0.0
    if rates_total <= barsToCount:
        return rates_total
    start = prev_calculated
    if prev_calculated < barsToCount:
        start = barsToCount
    for index in range(start, rates_total):
        sumy = 0.0
        sumx = 0.0
        sumxy = 0.0
        sumx2 = 0.0
        for i in range(0, barsToCount):
            sumy += close[index - i]
            sumxy += close[index - i] * (1 + i)
            sumx += 1 + i
            sumx2 += (1 + i) * (1 + i)
        c = (sumx2 * barsToCount) - (sumx * sumx)
        if c == 0:
            c = 0.1
        b = _fdiv((sumxy * barsToCount) - (sumx * sumy), c)
        current = -1000 * b
        prev = current
        if buffer1[index - 1] != EMPTY_VALUE:
            prev = buffer1[index - 1]
        elif buffer0[index - 1] != EMPTY_VALUE:
            prev = buffer0[index - 1]
        if current >= prev:
            buffer0[index] = current
            buffer1[index] = EMPTY_VALUE
        elif current < prev:
            buffer1[index] = current
            buffer0[index] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendLinearReg(_MQL5Indicator):
    name = 'TrendLinearReg'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

