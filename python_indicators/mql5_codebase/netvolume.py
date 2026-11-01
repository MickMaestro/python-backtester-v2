"""NetVolume — converted from MQL5: MQL5 Indicators/Net Volume/NetVolume.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'NV'}, 'levels': [], 'description': [], 'name': 'NetVolume', 'source': 'MQL5 Indicators/Net Volume/NetVolume.mq5', 'folder': 'Net Volume', 'inputs': [{'mql': 'InpVolume', 'py': 'InpVolume', 'param': 'InpVolume', 'type': 'int', 'default': 0, 'label': 'Volume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpVolume = _input('InpVolume', VOLUME_TICK)  # Volume
ExtBufferNV = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtBufferNV, INDICATOR_DATA)
    ArraySetAsSeries(ExtBufferNV, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Net Volume')
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 2:
        return 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(volume, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(ExtBufferNV, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        v = close[i] - close[i + 1]
        sign = (-1 if (v < 0) else 1 if (v > 0) else 0)
        ExtBufferNV[i] = float(sign * (tick_volume[i] if (InpVolume == VOLUME_TICK) else volume[i]))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NetVolume(_MQL5Indicator):
    name = 'NetVolume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume
    }

