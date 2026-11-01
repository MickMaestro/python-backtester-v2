"""neoparabolic — converted from MQL5: MQL5 Indicators/Simple Continuous ParabolicSAR/neoparabolic.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'neoparabolic', 'source': 'MQL5 Indicators/Simple Continuous ParabolicSAR/neoparabolic.mq5', 'folder': 'Simple Continuous ParabolicSAR', 'inputs': [{'mql': 'ParabolicSARPeriod', 'py': 'ParabolicSARPeriod', 'param': 'ParabolicSARPeriod', 'type': 'int', 'default': 10, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ParabolicSARPeriod = _input('ParabolicSARPeriod', 10)  # Period
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
max_ = 0.0
min_ = 0.0

def OnInit():
    SetIndexBuffer(0, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLowBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ParabolicSARPeriod)
    PlotIndexSetInteger(0, PLOT_SHIFT, 2)
    PlotIndexSetInteger(1, PLOT_SHIFT, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Parabolic(' + _str(ParabolicSARPeriod) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'Channel(' + _str(ParabolicSARPeriod) + ') max')
    PlotIndexSetString(1, PLOT_LABEL, ' Channel(' + _str(ParabolicSARPeriod) + ') min')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)

def Highest(array, range_, fromIndex):
    res = 0.0
    i = 0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res < array[i]:
            res = array[i]
        i -= 1
    return res

def Lowest(array, range_, fromIndex):
    res = 0.0
    i = 0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res > array[i]:
            res = array[i]
        i -= 1
    return res

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global max_, min_
    i = 0
    limit = 0
    if rates_total < ParabolicSARPeriod:
        return 0
    if prev_calculated == 0:
        limit = ParabolicSARPeriod
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        max_ = 0.0
        min_ = 0.0
        for j in range(1, ParabolicSARPeriod + 1):
            max_ = max_ + (Highest(High, j, i) / ParabolicSARPeriod)
            min_ = min_ + (Lowest(Low, j, i) / ParabolicSARPeriod)
        max_ = NormalizeDouble(max_, Digits())
        min_ = NormalizeDouble(min_, Digits())
        ExtHighBuffer[i] = max_
        ExtLowBuffer[i] = min_
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Neoparabolic(_MQL5Indicator):
    name = 'neoparabolic'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ParabolicSARPeriod': 10,  # Period
    }

