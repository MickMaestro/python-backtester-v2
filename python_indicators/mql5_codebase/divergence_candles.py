"""Divergence_Candles — converted from MQL5: MQL5 Indicators/Divergence_Candles/Divergence_Candles.mq5

Divergence Candles
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Up', 2: 'Down'}, 'levels': [], 'description': ['Divergence Candles'], 'name': 'Divergence_Candles', 'source': 'MQL5 Indicators/Divergence_Candles/Divergence_Candles.mq5', 'folder': 'Divergence_Candles', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferArrUP = Arr(0, 0.0)
BufferArrDN = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferArrUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferArrDN, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Divergence Candles')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferArrUP, True)
    ArraySetAsSeries(BufferArrDN, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferArrUP, EMPTY_VALUE)
        ArrayInitialize(BufferArrDN, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        if high[i] > high[i + 1] and close[i] <= close[i + 1]:
            BufferArrDN[i] = high[i]
        else:
            BufferArrDN[i] = EMPTY_VALUE
        if low[i] < low[i + 1] and close[i] >= close[i + 1]:
            BufferArrUP[i] = low[i]
        else:
            BufferArrUP[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DivergenceCandles(_MQL5Indicator):
    name = 'Divergence_Candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

