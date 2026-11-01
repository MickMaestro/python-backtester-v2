"""Difference — converted from MQL5: MQL5 Indicators/Difference/Difference.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 17919]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Difference'}, 'levels': [], 'description': [], 'name': 'Difference', 'source': 'MQL5 Indicators/Difference/Difference.mq5', 'folder': 'Difference', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Calculation method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_METHOD
METHOD_HIGH_LOW = 0
METHOD_OPEN_CLOSE = 1
_enum('ENUM_METHOD', {0: 'METHOD_HIGH_LOW', 1: 'METHOD_OPEN_CLOSE'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpMethod = _input('InpMethod', METHOD_HIGH_LOW)  # Calculation method
BufferDifference = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferData = Arr(0, 0.0)
period_ma = 0

def OnInit():
    global period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    short_name = 'Difference(' + _str(period_ma) + ')'
    SetIndexBuffer(0, BufferDifference, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferData, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    ArraySetAsSeries(BufferDifference, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferData, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferDifference, EMPTY_VALUE)
        ArrayInitialize(BufferData, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 0)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    for i in range(limit, 0 - 1, -1):
        BufferData[i] = _fdiv(((high[i] - low[i]) if (InpMethod == METHOD_HIGH_LOW) else (close[i] - open[i])), Point())
    count = (1 if (limit == 0) else rates_total)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferData, BufferDifference)
    for i in range(limit - 1, 0 - 1, -1):
        if BufferDifference[i] < BufferDifference[i + 1]:
            BufferColors[i] = 1.0
        else:
            BufferColors[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Difference(_MQL5Indicator):
    name = 'Difference'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpMethod': _Choice({0: 'High/Low', 1: 'Open/Close'}, default=0),  # Calculation method
    }

