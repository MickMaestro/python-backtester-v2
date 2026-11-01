"""stochastic — converted from MQL5: MQL5 Indicators/Stochastic Oscillator/stochastic.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [11186720], 2: [255]}, 'widths': {}, 'styles': {2: 2}, 'labels': {}, 'levels': [], 'description': [], 'name': 'stochastic', 'source': 'MQL5 Indicators/Stochastic Oscillator/stochastic.mq5', 'folder': 'Stochastic Oscillator', 'inputs': [{'mql': 'InpKPeriod', 'py': 'InpKPeriod', 'param': 'InpKPeriod', 'type': 'int', 'default': 5, 'label': 'K period', 'sinput': False}, {'mql': 'InpDPeriod', 'py': 'InpDPeriod', 'param': 'InpDPeriod', 'type': 'int', 'default': 3, 'label': 'D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'int', 'default': 3, 'label': 'Slowing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpKPeriod = _input('InpKPeriod', 5)  # K period
InpDPeriod = _input('InpDPeriod', 3)  # D period
InpSlowing = _input('InpSlowing', 3)  # Slowing
ExtMainBuffer = Arr(0, 0.0)
ExtSignalBuffer = Arr(0, 0.0)
ExtHighesBuffer = Arr(0, 0.0)
ExtLowesBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtMainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtSignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtHighesBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtLowesBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 20)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 80)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stoch(' + _str(InpKPeriod) + ',' + _str(InpDPeriod) + ',' + _str(InpSlowing) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'Main')
    PlotIndexSetString(1, PLOT_LABEL, 'Signal')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpKPeriod + InpSlowing - 2)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpKPeriod + InpDPeriod)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    k = 0
    start = 0
    if rates_total <= (InpKPeriod + InpDPeriod + InpSlowing):
        return 0
    start = InpKPeriod - 1
    if (start + 1) < prev_calculated:
        start = prev_calculated - 2
    else:
        i = 0
        for i in range(i, start):
            ExtLowesBuffer[i] = 0.0
            ExtHighesBuffer[i] = 0.0
        else:
            i = _range_end(i, start, 1)
    i = start
    for i in range(i, rates_total):
        dmin = 1000000.0
        dmax = -1000000.0
        k = i - InpKPeriod + 1
        for k in range(k, i + 1):
            if dmin > Low[k]:
                dmin = Low[k]
            if dmax < High[k]:
                dmax = High[k]
        else:
            k = _range_end(k, i + 1, 1)
        ExtLowesBuffer[i] = dmin
        ExtHighesBuffer[i] = dmax
    else:
        i = _range_end(i, rates_total, 1)
    start = InpKPeriod - 1 + InpSlowing - 1
    if (start + 1) < prev_calculated:
        start = prev_calculated - 2
    else:
        i = 0
        for i in range(i, start):
            ExtMainBuffer[i] = 0.0
        else:
            i = _range_end(i, start, 1)
    i = start
    for i in range(i, rates_total):
        sumlow = 0.0
        sumhigh = 0.0
        k = i - InpSlowing + 1
        for k in range(k, i + 1):
            sumlow += Close[k] - ExtLowesBuffer[k]
            sumhigh += ExtHighesBuffer[k] - ExtLowesBuffer[k]
        else:
            k = _range_end(k, i + 1, 1)
        if sumhigh == 0.0:
            ExtMainBuffer[i] = 100.0
        else:
            ExtMainBuffer[i] = _fdiv(sumlow, sumhigh) * 100
    else:
        i = _range_end(i, rates_total, 1)
    start = InpDPeriod - 1
    if (start + 1) < prev_calculated:
        start = prev_calculated - 2
    else:
        i = 0
        for i in range(i, start):
            ExtSignalBuffer[i] = 0.0
        else:
            i = _range_end(i, start, 1)
    i = start
    for i in range(i, rates_total):
        sum_ = 0.0
        k = 0
        for k in range(k, InpDPeriod):
            sum_ += ExtMainBuffer[i - k]
        else:
            k = _range_end(k, InpDPeriod, 1)
        ExtSignalBuffer[i] = sum_ / InpDPeriod
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stochastic(_MQL5Indicator):
    name = 'stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpKPeriod': 5,  # K period
        'InpDPeriod': 3,  # D period
        'InpSlowing': 3,  # Slowing
    }

