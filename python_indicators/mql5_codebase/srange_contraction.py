"""SRange_Contraction — converted from MQL5: MQL5 Indicators/SRange_Contraction/SRange_Contraction.mq5

Signal Range Contraction indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 5}, 'colors': {1: [13688896], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Range', 2: 'Breakout'}, 'levels': [], 'description': ['Signal Range Contraction indicator'], 'name': 'SRange_Contraction', 'source': 'MQL5 Indicators/SRange_Contraction/SRange_Contraction.mq5', 'folder': 'SRange_Contraction', 'inputs': [{'mql': 'InpThreshold', 'py': 'InpThreshold', 'param': 'InpThreshold', 'type': 'double', 'default': 50.0, 'label': 'Threshold', 'sinput': False}, {'mql': 'InpShowRC', 'py': 'InpShowRC', 'param': 'InpShowRC', 'type': 'int', 'default': 1, 'label': 'Show Small Range', 'sinput': False}, {'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Calculation period mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE
MODE_CURRENT = 0
MODE_PREVIOUS = 1
_enum('ENUM_MODE', {0: 'MODE_CURRENT', 1: 'MODE_PREVIOUS'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpThreshold = _input('InpThreshold', 50.0)  # Threshold
InpShowRC = _input('InpShowRC', INPUT_YES)  # Show Small Range
InpMode = _input('InpMode', MODE_CURRENT)  # Calculation period mode
BufferRC = Arr(0, 0.0)
BufferC = Arr(0, 0.0)
threshold = 0.0
period = 0

def OnInit():
    global period, threshold
    period = InpMode
    threshold = fabs(InpThreshold)
    SetIndexBuffer(0, BufferRC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferC, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SRange Contraction (' + DoubleToString(threshold, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, threshold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Threshold (' + DoubleToString(threshold, 2) + ')')
    ArraySetAsSeries(BufferRC, True)
    ArraySetAsSeries(BufferC, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - (2 + period)
        ArrayInitialize(BufferRC, EMPTY_VALUE)
        ArrayInitialize(BufferC, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        if high[i + 1 + period] != low[i + 1 + period]:
            BufferRC[i] = _fdiv(100.0 * (high[i + period] - low[i + period]), high[i + 1 + period] - low[i + 1 + period])
        BufferC[i] = (BufferRC[i] if (InpShowRC and BufferRC[i] < threshold) else EMPTY_VALUE)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SRangeContraction(_MQL5Indicator):
    name = 'SRange_Contraction'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpThreshold': 50.0,  # Threshold
        'InpShowRC': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Small Range
        'InpMode': _Choice({0: 'Current', 1: 'Previous'}, default=0),  # Calculation period mode
    }

