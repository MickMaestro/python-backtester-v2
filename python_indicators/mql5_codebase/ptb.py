"""PTB — converted from MQL5: MQL5 Indicators/PTB/PTB.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 9}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'colors': {1: [255], 2: [16711680], 3: [32768], 4: [42495], 5: [8388736], 6: [16776960], 7: [65535], 8: [2763429], 9: [16777215]}, 'widths': {1: 3, 2: 3, 3: 3, 4: 3, 5: 1, 6: 1, 7: 1, 8: 1, 9: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'labels': {1: 'shortHigh', 2: 'shortLow', 3: 'longHigh', 4: 'longLow', 5: 'fibo786', 6: 'fibo236', 7: 'fibo382', 8: 'fibo618', 9: 'fibo50'}, 'levels': [], 'description': [], 'name': 'PTB', 'source': 'MQL5 Indicators/PTB/PTB.mq5', 'folder': 'PTB', 'inputs': [{'mql': 'shortLength', 'py': 'shortLength', 'param': 'shortLength', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'longLength', 'py': 'longLength', 'param': 'longLength', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
shortLength = _input('shortLength', 0)
longLength = _input('longLength', 0)
shortHighBuffer = Arr(0, 0.0)
shortLowBuffer = Arr(0, 0.0)
longHighBuffer = Arr(0, 0.0)
longLowBuffer = Arr(0, 0.0)
fibo786Buffer = Arr(0, 0.0)
fibo236Buffer = Arr(0, 0.0)
fibo382Buffer = Arr(0, 0.0)
fibo618Buffer = Arr(0, 0.0)
fibo50Buffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, shortHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, shortLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, longHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, longLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, fibo786Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, fibo236Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, fibo382Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, fibo618Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, fibo50Buffer, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < shortLength or rates_total < longLength:
        return 0
    start = ((prev_calculated - 1) if (prev_calculated > 0) else MathMax(shortLength, longLength))
    for i in range(start, rates_total):
        highestHigh = high[i]
        lowestLow = low[i]
        for j in range(1, shortLength):
            if high[i - j] > highestHigh:
                highestHigh = high[i - j]
            if low[i - j] < lowestLow:
                lowestLow = low[i - j]
        shortHighBuffer[i] = highestHigh
        shortLowBuffer[i] = lowestLow
        longHighestHigh = high[i]
        longLowestLow = low[i]
        for j in range(1, longLength):
            if high[i - j] > longHighestHigh:
                longHighestHigh = high[i - j]
            if low[i - j] < longLowestLow:
                longLowestLow = low[i - j]
        longHighBuffer[i] = longHighestHigh
        longLowBuffer[i] = longLowestLow
        range_ = longHighestHigh - longLowestLow
        fibo236Buffer[i] = longLowestLow + (range_ * 0.236)
        fibo382Buffer[i] = longLowestLow + (range_ * 0.382)
        fibo50Buffer[i] = longLowestLow + (range_ * 0.5)
        fibo618Buffer[i] = longLowestLow + (range_ * 0.618)
        fibo786Buffer[i] = longLowestLow + (range_ * 0.786)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PTB(_MQL5Indicator):
    name = 'PTB'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'shortLength': 0,
        'longLength': 0,
    }

