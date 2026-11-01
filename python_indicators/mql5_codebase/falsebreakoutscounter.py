"""falsebreakoutscounter — converted from MQL5: MQL5 Indicators/False Breakouts Counter/falsebreakoutscounter.mq5

The indicator counts the number of false breakthrough on the specified number of bars. By 
false breakthrough means a situation where the high(low) of current bar is above 
(below) the high(low) of previous bar, and the close of current bar is lower the high (higher the low) of previous bar. 
Note: if the bar is external to the previous one, then it can have 
a two false breakthrough.
Copyright: Copyright 2013, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3, 'indicator_minimum': 0.0}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [36095]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Up False Breakouts', 2: 'Down False Breakouts', 3: 'Sum False Breakouts'}, 'levels': [], 'description': ['The indicator counts the number of false breakthrough on the specified number of bars. By ', 'false breakthrough means a situation where the high(low) of current bar is above ', '(below) the high(low) of previous bar, and the close of current bar is lower the high (higher the low) of previous bar. ', 'Note: if the bar is external to the previous one, then it can have ', 'a two false breakthrough.'], 'name': 'falsebreakoutscounter', 'source': 'MQL5 Indicators/False Breakouts Counter/falsebreakoutscounter.mq5', 'folder': 'False Breakouts Counter', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 5, 'label': 'False Breakouts Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 5)  # False Breakouts Period
UpFalseBuffer = Arr(0, 0.0)
DownFalseBuffer = Arr(0, 0.0)
SumFalseBuffer = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    if InpPeriod < 1:
        period = 5
        printf('Incorrected input value InpPeriod = %d. Indicator will use value %d', InpPeriod, period)
    else:
        period = InpPeriod
    SetIndexBuffer(0, UpFalseBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DownFalseBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, SumFalseBuffer, INDICATOR_DATA)
    for plot in range(0, 3):
        PlotIndexSetInteger(plot, PLOT_DRAW_BEGIN, period)
        PlotIndexSetInteger(plot, PLOT_SHIFT, 0)
        PlotIndexSetDouble(plot, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'False Breakouts (' + _str(period) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        Print('Not enough bars for calculations.')
        return 0
    start_bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        start_bar = period
    else:
        start_bar = prev_calculated - 1
    for bar in range(start_bar, rates_total):
        up_sum = 0
        down_sum = 0
        for pos in range(bar - period + 1, bar + 1):
            prev = pos - 1
            if close[pos] <= high[prev] and high[pos] > high[prev]:
                up_sum += 1
            if close[pos] >= low[prev] and low[pos] < low[prev]:
                down_sum += 1
        UpFalseBuffer[bar] = up_sum
        DownFalseBuffer[bar] = down_sum
        SumFalseBuffer[bar] = up_sum + down_sum
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Falsebreakoutscounter(_MQL5Indicator):
    name = 'falsebreakoutscounter'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 5,  # False Breakouts Period
    }

