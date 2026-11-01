"""MACrossAlerterV2 — converted from MQL5: MQL5 Indicators/Moving Average with alerts on price crossovers/MACrossAlerterV2.mq5

Copyright: Copyright 2023, https://www.mql5.com/en/users/phade/; Link: https://www.mql5.com/en/users/phade/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, https://www.mql5.com/en/users/phade/', 'link': 'https://www.mql5.com/en/users/phade/', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 1}, 'colors': {1: [8388736], 2: [0], 3: [8421504]}, 'widths': {1: 3, 2: 3, 3: 1}, 'styles': {3: 2}, 'labels': {1: 'Buy', 2: 'Sell', 3: 'Line'}, 'levels': [], 'description': [], 'name': 'MACrossAlerterV2', 'source': 'MQL5 Indicators/Moving Average with alerts on price crossovers/MACrossAlerterV2.mq5', 'folder': 'Moving Average with alerts on price crossovers', 'inputs': [{'mql': 'slowPeriod', 'py': 'slowPeriod', 'param': 'slowPeriod', 'type': 'int', 'default': 200, 'label': 'Moving Average Length', 'sinput': False}, {'mql': 'pointNum', 'py': 'pointNum', 'param': 'pointNum', 'type': 'int', 'default': 130, 'label': 'Amount of points on MA crossover that should enable a signal', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
indvalue = Arr(0, 0.0)
slowma = Arr(0, 0.0)
handle = 0
max_bars = 0
slowPeriod = _input('slowPeriod', 200)  # Moving Average Length
pointNum = _input('pointNum', 130)  # Amount of points on MA crossover that should enable a signal
value_buf_a = Arr(0, 0.0)
value_buf_b = Arr(0, 0.0)

def OnInit():
    global handle
    SetIndexBuffer(0, value_buf_a)
    SetIndexBuffer(1, value_buf_b)
    SetIndexBuffer(2, indvalue)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    handle = iMA(Symbol(), PERIOD_CURRENT, slowPeriod, 0, MODE_SMA, PRICE_CLOSE)
    if handle == INVALID_HANDLE:
        Print('Get MA Handle failed!')
        return INIT_FAILED
    ArrayInitialize(value_buf_a, 0.0)
    ArrayInitialize(value_buf_b, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    CopyBuffer(handle, 0, 0, rates_total, slowma)
    for i in range(prev_calculated - (rates_total == prev_calculated), rates_total):
        indvalue[i] = slowma[i]
        value_buf_a[i] = 0.0
        value_buf_b[i] = 0.0
        if ((i >= 0 and (i - 2) >= 0) and close[i] > (indvalue[i] + (pointNum * Point()))) and close[i - 2] < indvalue[i]:
            value_buf_a[i] = low[i]
        else:
            value_buf_a[i] = 0.0
        if ((i >= 0 and (i - 2) >= 0) and close[i] < (indvalue[i] - (pointNum * Point()))) and close[i - 2] > indvalue[i]:
            value_buf_b[i] = high[i]
        else:
            value_buf_b[i] = 0.0
    return rates_total

def OnDeinit(reason):
    ArrayFree(slowma)
    IndicatorRelease(handle)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACrossAlerterV2(_MQL5Indicator):
    name = 'MACrossAlerterV2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'slowPeriod': 200,  # Moving Average Length
        'pointNum': 130,  # Amount of points on MA crossover that should enable a signal
    }

