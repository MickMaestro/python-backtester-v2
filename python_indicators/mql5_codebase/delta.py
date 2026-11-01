"""Delta — converted from MQL5: MQL5 Indicators/Delta/Delta.mq5

Delta indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Price', 2: 'Delta'}, 'levels': [], 'description': ['Delta indicator'], 'name': 'Delta', 'source': 'MQL5 Indicators/Delta/Delta.mq5', 'folder': 'Delta', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferPrice = Arr(0, 0.0)
BufferDelta = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferPrice, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDelta, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Delta')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferPrice, True)
    ArraySetAsSeries(BufferDelta, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferPrice, 0)
        ArrayInitialize(BufferDelta, 0)
    for i in range(limit, 0 - 1, -1):
        BufferPrice[i] = (open[i] + high[i] + low[i] + close[i]) / 4.0
        if BufferPrice[i] > 0 and BufferPrice[i + 1] > 0:
            BufferDelta[i] = BufferPrice[i] + log10(_fdiv(BufferPrice[i + 1], BufferPrice[i]))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Delta(_MQL5Indicator):
    name = 'Delta'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

