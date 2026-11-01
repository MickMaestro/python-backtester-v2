"""Stochastic Custom — converted from MQL5: MQL5 Indicators/Stochastic Custom/Stochastic Custom.mq5

Stochastic Custom
Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [11186720], 2: [255]}, 'widths': {}, 'styles': {2: 2}, 'labels': {}, 'levels': [], 'description': ['Stochastic Custom'], 'name': 'Stochastic Custom', 'source': 'MQL5 Indicators/Stochastic Custom/Stochastic Custom.mq5', 'folder': 'Stochastic Custom', 'inputs': [{'mql': 'Inp_STO_KPeriod', 'py': 'Inp_STO_KPeriod', 'param': 'Inp_STO_KPeriod', 'type': 'int', 'default': 5, 'label': 'K period', 'sinput': False}, {'mql': 'Inp_STO_DPeriod', 'py': 'Inp_STO_DPeriod', 'param': 'Inp_STO_DPeriod', 'type': 'int', 'default': 3, 'label': 'D period', 'sinput': False}, {'mql': 'Inp_STO_Slowing', 'py': 'Inp_STO_Slowing', 'param': 'Inp_STO_Slowing', 'type': 'int', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'Inp_STO_Level1', 'py': 'Inp_STO_Level1', 'param': 'Inp_STO_Level1', 'type': 'int', 'default': 25, 'label': 'Value Level #1', 'sinput': False}, {'mql': 'Inp_STO_Level2', 'py': 'Inp_STO_Level2', 'param': 'Inp_STO_Level2', 'type': 'double', 'default': 75.0, 'label': 'Value Level #2', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_STO_KPeriod = _input('Inp_STO_KPeriod', 5)  # K period
Inp_STO_DPeriod = _input('Inp_STO_DPeriod', 3)  # D period
Inp_STO_Slowing = _input('Inp_STO_Slowing', 3)  # Slowing
Inp_STO_Level1 = _input('Inp_STO_Level1', _int(25.0))  # Value Level #1
Inp_STO_Level2 = _input('Inp_STO_Level2', 75.0)  # Value Level #2
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
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Inp_STO_Level1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Inp_STO_Level2)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stoch(' + _str(Inp_STO_KPeriod) + ',' + _str(Inp_STO_DPeriod) + ',' + _str(Inp_STO_Slowing) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'Main')
    PlotIndexSetString(1, PLOT_LABEL, 'Signal')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Inp_STO_KPeriod + Inp_STO_Slowing - 2)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Inp_STO_KPeriod + Inp_STO_DPeriod)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    k = 0
    start = 0
    if rates_total <= (Inp_STO_KPeriod + Inp_STO_DPeriod + Inp_STO_Slowing):
        return 0
    start = Inp_STO_KPeriod - 1
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
        k = i - Inp_STO_KPeriod + 1
        for k in range(k, i + 1):
            if dmin > low[k]:
                dmin = low[k]
            if dmax < high[k]:
                dmax = high[k]
        else:
            k = _range_end(k, i + 1, 1)
        ExtLowesBuffer[i] = dmin
        ExtHighesBuffer[i] = dmax
    else:
        i = _range_end(i, rates_total, 1)
    start = Inp_STO_KPeriod - 1 + Inp_STO_Slowing - 1
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
        k = i - Inp_STO_Slowing + 1
        for k in range(k, i + 1):
            sumlow += close[k] - ExtLowesBuffer[k]
            sumhigh += ExtHighesBuffer[k] - ExtLowesBuffer[k]
        else:
            k = _range_end(k, i + 1, 1)
        if sumhigh == 0.0:
            ExtMainBuffer[i] = 100.0
        else:
            ExtMainBuffer[i] = _fdiv(sumlow, sumhigh) * 100
    else:
        i = _range_end(i, rates_total, 1)
    start = Inp_STO_DPeriod - 1
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
        for k in range(k, Inp_STO_DPeriod):
            sum_ += ExtMainBuffer[i - k]
        else:
            k = _range_end(k, Inp_STO_DPeriod, 1)
        ExtSignalBuffer[i] = sum_ / Inp_STO_DPeriod
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticCustom(_MQL5Indicator):
    name = 'Stochastic Custom'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_STO_KPeriod': 5,  # K period
        'Inp_STO_DPeriod': 3,  # D period
        'Inp_STO_Slowing': 3,  # Slowing
        'Inp_STO_Level1': 25,  # Value Level #1
        'Inp_STO_Level2': 75.0,  # Value Level #2
    }

