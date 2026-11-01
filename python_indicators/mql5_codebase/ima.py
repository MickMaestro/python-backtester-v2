"""ima — converted from MQL5: MQL5 Indicators/Index Moving Average/ima.mq5

Copyright: Vladimir M.; Link: mikh.vl@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Vladimir M.', 'link': 'mikh.vl@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ima', 'source': 'MQL5 Indicators/Index Moving Average/ima.mq5', 'folder': 'Index Moving Average', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 5, 'label': 'Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 5)  # Period
imaBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, imaBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MAPeriod)

def OnCalculate(rates_total, prev_calculated, begin, price):
    start = 0
    j = 0
    i = 0
    sum_ = 0.0
    ma = 0.0
    if rates_total < (MAPeriod - 1):
        return 0
    if prev_calculated == 0:
        start = MAPeriod - 1
    else:
        start = prev_calculated - 1
    j = start
    for j in range(j, rates_total):
        sum_ = 0.0
        i = 0
        for i in range(i, MAPeriod):
            sum_ += price[j - i]
        else:
            i = _range_end(i, MAPeriod, 1)
        ma = sum_ / MAPeriod
        imaBuffer[j] = _fdiv(price[j], ma) - 1
    else:
        j = _range_end(j, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ima(_MQL5Indicator):
    name = 'ima'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 5,  # Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

