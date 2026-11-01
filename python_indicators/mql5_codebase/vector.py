"""Vector — converted from MQL5: MQL5 Indicators/Vector/Vector.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'WP', 2: 'WN'}, 'levels': [], 'description': [], 'name': 'Vector', 'source': 'MQL5 Indicators/Vector/Vector.mq5', 'folder': 'Vector', 'inputs': [{'mql': 'InpColorH1', 'py': 'InpColorH1', 'param': None, 'type': 'color', 'default': 255, 'label': 'Inertia osc color', 'sinput': False}, {'mql': 'InpColorH2', 'py': 'InpColorH2', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Trend osc color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpColorH1 = _input('InpColorH1', clrRed)  # Inertia osc color
InpColorH2 = _input('InpColorH2', clrGreen)  # Trend osc color
BufferWP = Arr(0, 0.0)
BufferWN = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferWP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferWN, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, InpColorH1)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, InpColorH2)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Vector')
    ArraySetAsSeries(BufferWP, True)
    ArraySetAsSeries(BufferWN, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 17:
        return 0
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 17
        ArrayInitialize(BufferWP, 0)
        ArrayInitialize(BufferWN, 0)
    for i in range(limit, 0 - 1, -1):
        BufferWP[i] = close[i] - ((close[i + 2] + close[i + 4] + close[i + 8] + close[i + 16]) / 4)
        BufferWN[i] = (0.9375 * close[i]) - (0.5 * close[i + 2]) - (0.25 * close[i + 4]) - (0.125 * close[i + 8]) - (0.0625 * close[i + 16])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vector(_MQL5Indicator):
    name = 'Vector'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

