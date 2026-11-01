"""demo_draw_zigzag — converted from MQL5: MQL5 Indicators/Demo_DRAW_ZIGZAG/demo_draw_zigzag.mq5

Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ZigZag'}, 'levels': [], 'description': [], 'name': 'demo_draw_zigzag', 'source': 'MQL5 Indicators/Demo_DRAW_ZIGZAG/demo_draw_zigzag.mq5', 'folder': 'Demo_DRAW_ZIGZAG', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ZigZagBuffer1 = Arr(0, 0.0)
ZigZagBuffer2 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ZigZagBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ZigZagBuffer2, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if prev_calculated == 0:
        ArrayInitialize(ZigZagBuffer1, 0)
        ArrayInitialize(ZigZagBuffer2, 0)
    start = prev_calculated
    if start != 0:
        start -= 1
    for i in range(start, rates_total):
        buff_index = _imod(i, 2)
        _sw1 = buff_index
        if _sw1 == 0:
            ZigZagBuffer1[i] = high[i]
        elif _sw1 == 1:
            ZigZagBuffer2[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DemoDrawZigzag(_MQL5Indicator):
    name = 'demo_draw_zigzag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

