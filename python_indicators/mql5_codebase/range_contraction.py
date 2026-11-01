"""Range_Contraction — converted from MQL5: MQL5 Indicators/Range_Contraction/Range_Contraction.mq5

Range Contraction indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [3329330]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Threshold', 2: 'Range'}, 'levels': [], 'description': ['Range Contraction indicator'], 'name': 'Range_Contraction', 'source': 'MQL5 Indicators/Range_Contraction/Range_Contraction.mq5', 'folder': 'Range_Contraction', 'inputs': [{'mql': 'InpThreshold', 'py': 'InpThreshold', 'param': 'InpThreshold', 'type': 'double', 'default': 50.0, 'label': 'Threshold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpThreshold = _input('InpThreshold', 50.0)  # Threshold
BufferThreshold = Arr(0, 0.0)
BufferRange = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferThreshold, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRange, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range Contraction (' + DoubleToString(InpThreshold, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    ArraySetAsSeries(BufferThreshold, True)
    ArraySetAsSeries(BufferRange, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferThreshold, EMPTY_VALUE)
        ArrayInitialize(BufferRange, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferThreshold[i] = InpThreshold
        hl = high[i + 1] - low[i + 1]
        BufferRange[i] = _fdiv(high[i] - low[i], (hl if (hl != 0) else DBL_MIN) / 100.0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangeContraction(_MQL5Indicator):
    name = 'Range_Contraction'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpThreshold': 50.0,  # Threshold
    }

