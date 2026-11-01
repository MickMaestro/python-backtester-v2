"""Volume_Accumulation — converted from MQL5: MQL5 Indicators/Volume_Accumulation/Volume_Accumulation.mq5

Volume Accumulation
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'VA'}, 'levels': [], 'description': ['Volume Accumulation'], 'name': 'Volume_Accumulation', 'source': 'MQL5 Indicators/Volume_Accumulation/Volume_Accumulation.mq5', 'folder': 'Volume_Accumulation', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferVA = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferVA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volume Accumulation')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferVA, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferVA, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferVA[i] = (_fdiv(tick_volume[i] * ((2 * close[i]) - high[i] - low[i]), high[i] - low[i]) if ((high[i] - low[i]) != 0) else 0)
        BufferColors[i] = (1 if (BufferVA[i] < BufferVA[i + 1]) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeAccumulation(_MQL5Indicator):
    name = 'Volume_Accumulation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

