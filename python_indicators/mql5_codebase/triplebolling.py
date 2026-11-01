"""triplebolling — converted from MQL5: MQL5 Indicators/Triple Bolling/triplebolling.mq5

Copyright: Snail000; Link: https://login.mql5.com/ru/users/Snail000; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Snail000', 'link': 'https://login.mql5.com/ru/users/Snail000', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [65535], 2: [255], 3: [255], 4: [8036607], 5: [8036607], 6: [65535], 7: [65535]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {1: 'Bollinger line', 2: 'Bollinger line', 3: 'Bollinger line', 4: 'Bollinger line', 5: 'Bollinger line', 6: 'Bollinger line', 7: 'Bollinger line'}, 'levels': [], 'description': [], 'name': 'triplebolling', 'source': 'MQL5 Indicators/Triple Bolling/triplebolling.mq5', 'folder': 'Triple Bolling', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'price', 'py': 'price', 'param': 'price', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 50)
price = _input('price', PRICE_WEIGHTED)
MABuffer = Arr(0, 0.0)
Bolinger2h = Arr(0, 0.0)
Bolinger2l = Arr(0, 0.0)
Bolinger3h = Arr(0, 0.0)
Bolinger3l = Arr(0, 0.0)
Bolinger4h = Arr(0, 0.0)
Bolinger4l = Arr(0, 0.0)
eq = 0.0
ma_handle = 0
symbol = ""

def OnInit():
    global ma_handle
    SetIndexBuffer(0, MABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Bolinger2h, INDICATOR_DATA)
    SetIndexBuffer(2, Bolinger2l, INDICATOR_DATA)
    SetIndexBuffer(3, Bolinger3h, INDICATOR_DATA)
    SetIndexBuffer(4, Bolinger3l, INDICATOR_DATA)
    SetIndexBuffer(5, Bolinger4h, INDICATOR_DATA)
    SetIndexBuffer(6, Bolinger4l, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 5)
    ma_handle = iBands(Symbol(), 0, period, 0, 2, price)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global eq
    if BarsCalculated(ma_handle) < rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        to_copy += 1
    CopyBuffer(ma_handle, 0, 0, to_copy, MABuffer)
    CopyBuffer(ma_handle, 1, 0, to_copy, Bolinger2h)
    for i in range(0, rates_total):
        eq = Bolinger2h[i] - MABuffer[i]
        Bolinger2l[i] = MABuffer[i] - eq
        Bolinger3h[i] = MABuffer[i] + (eq * 1.5)
        Bolinger3l[i] = MABuffer[i] - (eq * 1.5)
        Bolinger4h[i] = MABuffer[i] + (eq * 2)
        Bolinger4l[i] = MABuffer[i] - (eq * 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Triplebolling(_MQL5Indicator):
    name = 'triplebolling'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 50,
        'price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),
    }

