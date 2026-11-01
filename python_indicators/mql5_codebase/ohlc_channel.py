"""OHLC Channel — converted from MQL5: MQL5 Indicators/OHLC Channel/OHLC Channel.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65407], 2: [9639167]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Up', 2: 'Down'}, 'levels': [], 'description': [], 'name': 'OHLC Channel', 'source': 'MQL5 Indicators/OHLC Channel/OHLC Channel.mq5', 'folder': 'OHLC Channel', 'inputs': [{'mql': 'InpUp', 'py': 'InpUp', 'param': 'InpUp', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'InpDown', 'py': 'InpDown', 'param': 'InpDown', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PRICE
open_price = 0
high_price = 1
low_price = 2
close_price = 3
_enum('ENUM_PRICE', {0: 'open_price', 1: 'high_price', 2: 'low_price', 3: 'close_price'})

# ---- inputs and global variables
InpUp = _input('InpUp', high_price)
InpDown = _input('InpDown', low_price)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowBuffer, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        _sw1 = InpUp
        if _sw1 == open_price:
            HighBuffer[i] = open[i]
        elif _sw1 == high_price:
            HighBuffer[i] = high[i]
        elif _sw1 == low_price:
            HighBuffer[i] = low[i]
        elif _sw1 == close_price:
            HighBuffer[i] = close[i]
        _sw2 = InpDown
        if _sw2 == open_price:
            LowBuffer[i] = open[i]
        elif _sw2 == high_price:
            LowBuffer[i] = high[i]
        elif _sw2 == low_price:
            LowBuffer[i] = low[i]
        elif _sw2 == close_price:
            LowBuffer[i] = close[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OHLCChannel(_MQL5Indicator):
    name = 'OHLC Channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpUp': _Choice({0: 'Open', 1: 'High', 2: 'Low', 3: 'Close'}, default=1),
        'InpDown': _Choice({0: 'Open', 1: 'High', 2: 'Low', 3: 'Close'}, default=2),
    }

