"""Gaps OHLC — converted from MQL5: MQL5 Indicators/Gaps OHLC/Gaps OHLC.mq5

Gaps OHLC
Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.002

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.002', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Gaps OHLC'}, 'levels': [], 'description': ['Gaps OHLC'], 'name': 'Gaps OHLC', 'source': 'MQL5 Indicators/Gaps OHLC/Gaps OHLC.mq5', 'folder': 'Gaps OHLC', 'inputs': [{'mql': 'InpTimeFrame', 'py': 'InpTimeFrame', 'param': 'InpTimeFrame', 'type': 'int', 'default': 0, 'label': 'TimeFrame on which we are looking for gep', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTimeFrame = _input('InpTimeFrame', PERIOD_CURRENT)  # TimeFrame on which we are looking for gep
Color_HistogramBuffer = Arr(0, 0.0)
Color_HistogramColors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, Color_HistogramBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Color_HistogramColors, INDICATOR_COLOR_INDEX)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= 1:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(0, rates_total):
        if i == 0:
            Color_HistogramBuffer[i] = 0.0
            Color_HistogramColors[i] = 0.0
            continue
        if open[i] < low[i - 1]:
            Color_HistogramBuffer[i] = _fdiv(open[i] - low[i - 1], Point())
            Color_HistogramColors[i] = 0.0
        elif open[i] > high[i - 1]:
            Color_HistogramBuffer[i] = _fdiv(open[i] - high[i - 1], Point())
            Color_HistogramColors[i] = 1.0
        else:
            Color_HistogramBuffer[i] = 0.0
            Color_HistogramColors[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GapsOHLC(_MQL5Indicator):
    name = 'Gaps OHLC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # TimeFrame on which we are looking for gep
    }

