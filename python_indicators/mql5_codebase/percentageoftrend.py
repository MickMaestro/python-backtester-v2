"""percentageoftrend — converted from MQL5: MQL5 Indicators/Percentage of Trend/percentageoftrend.mq5

Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_minimum': -1.0, 'indicator_maximum': 1.0, 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 3, 2: 3}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Period1', 2: 'Period2'}, 'levels': [0.2, 0.8, -0.2, -0.8], 'description': [], 'name': 'percentageoftrend', 'source': 'MQL5 Indicators/Percentage of Trend/percentageoftrend.mq5', 'folder': 'Percentage of Trend', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'int', 'default': 20, 'label': 'Period1', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'int', 'default': 100, 'label': 'Period2', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 20)  # Period1
InpPeriod2 = _input('InpPeriod2', 100)  # Period2
Period1Buffer = Arr(0, 0.0)
Period2Buffer = Arr(0, 0.0)

def OnInit():
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    SetIndexBuffer(0, Period1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Period2Buffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = MathMax(InpPeriod1, InpPeriod2)
    pos = 0
    bars = Bars(Symbol(), Period())
    if bars < max_:
        return 0
    if prev_calculated > max_:
        pos = prev_calculated
    else:
        pos = max_
    for i in range(pos, rates_total):
        HighValue1 = 0.0
        LowValue1 = 0.0
        for cnt in range(i - InpPeriod1 + 1, i + 1):
            if high[cnt] > HighValue1:
                HighValue1 = high[cnt]
        for cnt in range(i - InpPeriod1 + 1, i + 1):
            if cnt == (i - InpPeriod1 + 1):
                LowValue1 = low[cnt]
            if low[cnt] < LowValue1:
                LowValue1 = low[cnt]
        HighValue2 = 0.0
        LowValue2 = 0.0
        for cnt in range(i - InpPeriod2 + 1, i + 1):
            if high[cnt] > HighValue2:
                HighValue2 = high[cnt]
        for cnt in range(i - InpPeriod2 + 1, i + 1):
            if cnt == (i - InpPeriod2 + 1):
                LowValue2 = low[cnt]
            if low[cnt] < LowValue2:
                LowValue2 = low[cnt]
        Period1Buffer[i] = _fdiv(close[i] - LowValue1, HighValue1 - LowValue1)
        Period2Buffer[i] = _fdiv((close[i] - LowValue2) * -1, HighValue2 - LowValue2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Percentageoftrend(_MQL5Indicator):
    name = 'percentageoftrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 20,  # Period1
        'InpPeriod2': 100,  # Period2
    }
    y_range = (-1.0, 1.0)

