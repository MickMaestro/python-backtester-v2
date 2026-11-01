"""Range_Volume_Ratio — converted from MQL5: MQL5 Indicators/Range_Volume_Ratio/Range_Volume_Ratio.mq5

Range Volume Ratio oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [10526303, 8721863]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'RV Ratio'}, 'levels': [], 'description': ['Range Volume Ratio oscillator'], 'name': 'Range_Volume_Ratio', 'source': 'MQL5 Indicators/Range_Volume_Ratio/Range_Volume_Ratio.mq5', 'folder': 'Range_Volume_Ratio', 'inputs': [{'mql': 'InpType', 'py': 'InpType', 'param': 'InpType', 'type': 'int', 'default': 0, 'label': 'Calculation type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_TYPE_CALC
TYPE_OC = 0
TYPE_HL = 1
_enum('ENUM_TYPE_CALC', {0: 'TYPE_OC', 1: 'TYPE_HL'})

# ---- inputs and global variables
InpType = _input('InpType', TYPE_OC)  # Calculation type
BufferRVR = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferRVR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range Volume Ratio')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    ArraySetAsSeries(BufferRVR, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferRVR, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferRVR[i] = (_fdiv((fabs(open[i] - close[i]) if (InpType == TYPE_OC) else (high[i] - low[i])), tick_volume[i] * Point()) if (tick_volume[i] != 0) else 0)
        BufferColors[i] = (1 if (BufferRVR[i] < BufferRVR[i + 1]) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangeVolumeRatio(_MQL5Indicator):
    name = 'Range_Volume_Ratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpType': _Choice({0: 'Open/Close', 1: 'High/Low'}, default=0),  # Calculation type
    }

