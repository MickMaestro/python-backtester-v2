"""TripleBolling_Modified — converted from MQL5: MQL5 Indicators/TripleBolling_Modified/TripleBolling_Modified.mq5

Modified by Rudinei Felipetto to accept full Bollinger params.
Copyright: Snail000; Link: https://login.mql5.com/ru/users/Snail000; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Snail000', 'link': 'https://login.mql5.com/ru/users/Snail000', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [65535], 2: [255], 3: [255], 4: [8036607], 5: [8036607], 6: [65535], 7: [65535]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {1: 'Bollinger line', 2: 'Bollinger line', 3: 'Bollinger line', 4: 'Bollinger line', 5: 'Bollinger line', 6: 'Bollinger line', 7: 'Bollinger line'}, 'levels': [], 'description': ['Modified by Rudinei Felipetto to accept full Bollinger params.'], 'name': 'TripleBolling_Modified', 'source': 'MQL5 Indicators/TripleBolling_Modified/TripleBolling_Modified.mq5', 'folder': 'TripleBolling_Modified', 'inputs': [{'mql': 'timeframe', 'py': 'timeframe', 'param': 'timeframe', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'ma_shift', 'py': 'ma_shift', 'param': 'ma_shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'deviation', 'py': 'deviation', 'param': 'deviation', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'price', 'py': 'price', 'param': 'price', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
timeframe = _input('timeframe', PERIOD_CURRENT)
period = _input('period', 50)
ma_shift = _input('ma_shift', 0)
deviation = _input('deviation', 2.0)
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
    ma_handle = iBands(Symbol(), timeframe, period, ma_shift, deviation, price)
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


class TripleBollingModified(_MQL5Indicator):
    name = 'TripleBolling_Modified'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'period': 50,
        'ma_shift': 0,
        'deviation': 2.0,
        'price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),
    }

