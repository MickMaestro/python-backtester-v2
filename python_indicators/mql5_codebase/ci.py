"""CI — converted from MQL5: MQL5 Indicators/CI/CI.mq5

Congestion Identifier indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [16748574], 2: [32768], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Counter graph', 2: 'Out', 3: 'In'}, 'levels': [], 'description': ['Congestion Identifier indicator'], 'name': 'CI', 'source': 'MQL5 Indicators/CI/CI.mq5', 'folder': 'CI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 28, 'label': 'Period', 'sinput': False}, {'mql': 'InpDelta', 'py': 'InpDelta', 'param': 'InpDelta', 'type': 'double', 'default': 100.0, 'label': 'Delta', 'sinput': False}, {'mql': 'InpLevel', 'py': 'InpLevel', 'param': 'InpLevel', 'type': 'uint', 'default': 14, 'label': 'Level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 28)  # Period
InpDelta = _input('InpDelta', 100.0)  # Delta
InpLevel = _input('InpLevel', 14)  # Level
BufferCI = Arr(0, 0.0)
BufferINC = Arr(0, 0.0)
BufferDEC = Arr(0, 0.0)
period = 0
level = 0
delta = 0.0

def OnInit():
    global delta, level, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    level = (1 if (InpLevel < 1) else InpLevel)
    delta = (1 if (InpDelta < 1) else InpDelta) * Point()
    SetIndexBuffer(0, BufferCI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferINC, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDEC, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Congestion Identifier (' + _str(period) + ',' + DoubleToString(level, 1) + ',' + DoubleToString(delta, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, level)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    ArraySetAsSeries(BufferCI, True)
    ArraySetAsSeries(BufferINC, True)
    ArraySetAsSeries(BufferDEC, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferCI, EMPTY_VALUE)
        ArrayInitialize(BufferINC, EMPTY_VALUE)
        ArrayInitialize(BufferDEC, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        top = close[i] + delta
        bottom = close[i] - delta
        count = 0
        for j in range(0, period):
            if close[i + j] < top and close[i + j] > bottom:
                count += 1
        BufferCI[i] = count
        BufferINC[i] = (level if (BufferCI[i + 1] < level and BufferCI[i] > level) else EMPTY_VALUE)
        BufferDEC[i] = (level if (BufferCI[i + 1] > level and BufferCI[i] < level) else EMPTY_VALUE)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CI(_MQL5Indicator):
    name = 'CI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 28,  # Period
        'InpDelta': 100.0,  # Delta
        'InpLevel': 14,  # Level
    }

