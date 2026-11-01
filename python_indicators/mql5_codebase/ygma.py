"""YGMA — converted from MQL5: MQL5 Indicators/YGMA/YGMA.mq5

Copyright: Yuriy Tokman; Link: http://ytg.com.ua; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Yuriy Tokman', 'link': 'http://ytg.com.ua', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [65280]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'YGMA', 'source': 'MQL5 Indicators/YGMA/YGMA.mq5', 'folder': 'YGMA', 'inputs': [{'mql': 'YMA_Period', 'py': 'YMA_Period', 'param': 'YMA_Period', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'GMA_Period', 'py': 'GMA_Period', 'param': 'GMA_Period', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
YMA_Period = _input('YMA_Period', 5)
GMA_Period = _input('GMA_Period', 12)
Buffer = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, Buffer)
    SetIndexBuffer(1, Buffer2)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MathMax(YMA_Period, GMA_Period))
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, MathMax(YMA_Period, GMA_Period))
    short_name = 'YGMA'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, 'YMA')
    PlotIndexSetString(0, PLOT_LABEL, 'GMA')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    limit = 0
    if rates_total < MathMax(YMA_Period, GMA_Period):
        return 0
    if prev_calculated == 0:
        limit = MathMax(YMA_Period, GMA_Period)
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        MA = ma(open, high, low, close, i)
        Buffer[i] = MA
        MG = mg(open, high, low, close, i)
        Buffer2[i] = MG
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def ma(o, h, l, c, _i):
    res = 0.0
    j = _i
    while j > (_i - YMA_Period) and j > 0:
        res += (c[j] + o[j] + h[j] + l[j]) / 4.0
        j -= 1
    return res / YMA_Period

def mg(o, h, l, c, _i):
    res = 1.0
    j = _i
    while j > (_i - GMA_Period) and j > 0:
        res *= (c[j] + o[j] + h[j] + l[j]) / 4.0
        j -= 1
    return MathPow(res, 1.0 / GMA_Period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YGMA(_MQL5Indicator):
    name = 'YGMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'YMA_Period': 5,
        'GMA_Period': 12,
    }

