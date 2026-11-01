"""medianpricechart — converted from MQL5: MQL5 Indicators/MedianPriceChart/medianpricechart.mq5

Copyright: Copyright 2010, Alf; Link: http://forum.liteforex.org/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, Alf', 'link': 'http://forum.liteforex.org/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16777215]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Mpc'}, 'levels': [], 'description': [], 'name': 'medianpricechart', 'source': 'MQL5 Indicators/MedianPriceChart/medianpricechart.mq5', 'folder': 'MedianPriceChart', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MpcBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, MpcBuffer, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, False)
    ArraySetAsSeries(low, False)
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        MpcBuffer[i] = (high[i] + low[i]) / 2
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Medianpricechart(_MQL5Indicator):
    name = 'medianpricechart'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

