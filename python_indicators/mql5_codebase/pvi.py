"""PVI — converted from MQL5: MQL5 Indicators/PVI/PVI.mq5

Positive Volume Index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'PVI'}, 'levels': [], 'description': ['Positive Volume Index'], 'name': 'PVI', 'source': 'MQL5 Indicators/PVI/PVI.mq5', 'folder': 'PVI', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferPVI = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferPVI, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PVI')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPVI, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferPVI, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferPVI[i] = (1 if (i == (rates_total - 2)) else (BufferPVI[i + 1] * (1 + _fdiv(close[i] - close[i + 1], close[i + 1]))) if (tick_volume[i] > tick_volume[i + 1]) else BufferPVI[i + 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PVI(_MQL5Indicator):
    name = 'PVI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

