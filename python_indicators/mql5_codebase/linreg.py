"""linreg — converted from MQL5: MQL5 Indicators/Linear Regression calculation based on pine script v4/linreg.mq5

Copyright: Copyright 2022, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MA'}, 'levels': [], 'description': [], 'name': 'linreg', 'source': 'MQL5 Indicators/Linear Regression calculation based on pine script v4/linreg.mq5', 'folder': 'Linear Regression calculation based on pine script v4', 'inputs': [{'mql': 'src', 'py': 'src', 'param': 'src', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'len', 'py': 'len_', 'param': 'len_', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'offset', 'py': 'offset', 'param': 'offset', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
src = _input('src', PRICE_CLOSE)
len_ = _input('len_', 10)
offset = _input('offset', 0)
MABuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, MABuffer, INDICATOR_DATA)
    ArraySetAsSeries(MABuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    BARS = MathMax(Bars(Symbol(), PERIOD_CURRENT) - len_ - prev_calculated, 1)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    _sw1 = src
    if _sw1 == PRICE_CLOSE:
        linreg(close, MABuffer, 0, BARS, len_, offset)
    elif _sw1 == PRICE_OPEN:
        linreg(open, MABuffer, 0, BARS, len_, offset)
    elif _sw1 == PRICE_HIGH:
        linreg(high, MABuffer, 0, BARS, len_, offset)
    elif _sw1 == PRICE_LOW:
        linreg(low, MABuffer, 0, BARS, len_, offset)
    else:
        linreg(close, MABuffer, 0, BARS, len_, offset)
    return rates_total

def linreg(input_src, output, start_pos, count, _len, _offset):
    for index in range(start_pos, start_pos + count):
        sum_y = 0.0
        sum_x = 0.0
        sum_y2 = 0.0
        sum_x2 = 0.0
        sum_xy = 0.0
        for i in range(index, index + _len):
            sum_y += input_src[i]
            sum_x += i
            sum_y2 += input_src[i] * input_src[i]
            sum_x2 += i * i
            sum_xy += i * input_src[i]
        a = _fdiv((sum_y * sum_x2) - (sum_x * sum_xy), (_len * sum_x2) - (sum_x * sum_x))
        b = _fdiv((_len * sum_xy) - (sum_x * sum_y), (_len * sum_x2) - (sum_x * sum_x))
        output[index] = a + (b * (index + _offset))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Linreg(_MQL5Indicator):
    name = 'linreg'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'src': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'len_': 10,
        'offset': 0,
    }

