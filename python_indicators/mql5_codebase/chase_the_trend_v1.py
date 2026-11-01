"""chase_the_trend_v1 — converted from MQL5: MQL5 Indicators/Chase the trend 1.0/chase_the_trend_v1.mq5

Copyright: Lazarev Denis; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Lazarev Denis', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [55295]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LINE'}, 'levels': [], 'description': [], 'name': 'chase_the_trend_v1', 'source': 'MQL5 Indicators/Chase the trend 1.0/chase_the_trend_v1.mq5', 'folder': 'Chase the trend 1.0', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 10, 'label': 'averaging period', 'sinput': False}, {'mql': 'USE_LIMIT', 'py': 'USE_LIMIT', 'param': 'USE_LIMIT', 'type': 'bool', 'default': False, 'label': 'limiting on/off', 'sinput': False}, {'mql': 'use_limit', 'py': 'use_limit', 'param': 'use_limit', 'type': 'double', 'default': 5e-05, 'label': 'Maximal value', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 10)  # averaging period
USE_LIMIT = _input('USE_LIMIT', False)  # limiting on/off
use_limit = _input('use_limit', 5e-05)  # Maximal value
Buffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, Buffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    start = 0
    if prev_calculated > 0:
        start = prev_calculated - 1
    for i in range(start, rates_total - 1):
        Buffer[0] = price[0]
        delta = (price[i] - Buffer[i]) / period
        if USE_LIMIT and delta > use_limit:
            delta = use_limit
        if USE_LIMIT and delta < (-use_limit):
            delta = -use_limit
        Buffer[i + 1] = Buffer[i] + delta
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChaseTheTrendV1(_MQL5Indicator):
    name = 'chase_the_trend_v1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 10,  # averaging period
        'USE_LIMIT': False,  # limiting on/off
        'use_limit': 5e-05,  # Maximal value
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

