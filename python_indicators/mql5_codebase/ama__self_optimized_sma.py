"""AMA — converted from MQL5: MQL5 Indicators/Self Optimized SMA/AMA.mq5

Copyright: Copyright 2025, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65535], 2: [42495]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'AMALower', 2: 'AMAUpper'}, 'levels': [], 'description': [], 'name': 'AMA', 'source': 'MQL5 Indicators/Self Optimized SMA/AMA.mq5', 'folder': 'Self Optimized SMA', 'inputs': [{'mql': 'MAX_PERIOD', 'py': 'MAX_PERIOD', 'param': 'MAX_PERIOD', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'MIN_PERIOD', 'py': 'MIN_PERIOD', 'param': 'MIN_PERIOD', 'type': 'int', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'DIST_LOOKBACK', 'py': 'DIST_LOOKBACK', 'param': 'DIST_LOOKBACK', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AMALowerBuffer = Arr(0, 0.0)
AMAUpperBuffer = Arr(0, 0.0)
MAX_PERIOD = _input('MAX_PERIOD', 50)
MIN_PERIOD = _input('MIN_PERIOD', 25)
DIST_LOOKBACK = _input('DIST_LOOKBACK', 100)

def OnInit():
    SetIndexBuffer(0, AMALowerBuffer, INDICATOR_DATA)
    ArraySetAsSeries(AMALowerBuffer, True)
    SetIndexBuffer(1, AMAUpperBuffer, INDICATOR_DATA)
    ArraySetAsSeries(AMAUpperBuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    BARS = MathMax(rates_total - prev_calculated - (2 * DIST_LOOKBACK), 1)
    for i in range(BARS, 0 - 1, -1):
        AMALowerBuffer[i] = AMALower(i, open, high, low, close)
        AMAUpperBuffer[i] = AMAUpper(i, open, high, low, close)
    return rates_total

def AMALower(index, open, high, low, close):
    for len_ in range(MAX_PERIOD, MIN_PERIOD - 1, -1):
        for i in range(index, index + DIST_LOOKBACK):
            if close[i] < sma(close, len_, i) and close[i + 1] < sma(close, len_, i + 1):
                break
            if BounceUp(i, len_, open, high, low, close):
                return sma(close, len_, index)
    return EMPTY_VALUE

def AMAUpper(index, open, high, low, close):
    for len_ in range(MAX_PERIOD, MIN_PERIOD - 1, -1):
        for i in range(index, index + DIST_LOOKBACK):
            if close[i] > sma(close, len_, i) and close[i + 1] > sma(close, len_, i + 1):
                break
            if BounceDown(i, len_, open, high, low, close):
                return sma(close, len_, index)
    return EMPTY_VALUE

def BounceUp(index, len_, open, high, low, close):
    if close[index] < sma(close, len_, index):
        return False
    if low[index + 1] > sma(close, len_, index + 1):
        return False
    if close[index + 2] < sma(close, len_, index + 2):
        return False
    return True

def BounceDown(index, len_, open, high, low, close):
    if close[index] > sma(close, len_, index):
        return False
    if high[index + 1] < sma(close, len_, index + 1):
        return False
    if close[index + 2] > sma(close, len_, index + 2):
        return False
    return True

def sma(src, length, index):
    sum_ = 0.0
    for i in range(index, index + length):
        sum_ = sum_ + _fdiv(src[i], length)
    return sum_


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AMA(_MQL5Indicator):
    name = 'AMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAX_PERIOD': 50,
        'MIN_PERIOD': 25,
        'DIST_LOOKBACK': 100,
    }

