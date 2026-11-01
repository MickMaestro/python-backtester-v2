"""Custom_Moving_Average_sep_win — converted from MQL5: MQL5 Indicators/Brooky Trend Strength for MT5/Custom_Moving_Average_sep_win.mq5

Copyright: © 2023, Ryan Lawrence Johnson; Link: https://www.mql5.com/en/users/rjo/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© 2023, Ryan Lawrence Johnson', 'link': 'https://www.mql5.com/en/users/rjo/seller', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Custom_Moving_Average_sep_win', 'source': 'MQL5 Indicators/Brooky Trend Strength for MT5/Custom_Moving_Average_sep_win.mq5', 'folder': 'Brooky Trend Strength for MT5', 'inputs': [{'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'int', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'InpMAShift', 'py': 'InpMAShift', 'param': 'InpMAShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 2, 'label': 'Method', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMAPeriod = _input('InpMAPeriod', 13)  # Period
InpMAShift = _input('InpMAShift', 0)  # Shift
InpMAMethod = _input('InpMAMethod', MODE_SMMA)  # Method
ExtLineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpMAPeriod)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpMAShift)
    short_name = ""
    _sw1 = InpMAMethod
    if _sw1 == MODE_EMA:
        short_name = 'EMA'
    elif _sw1 == MODE_LWMA:
        short_name = 'LWMA'
    elif _sw1 == MODE_SMA:
        short_name = 'SMA'
    elif _sw1 == MODE_SMMA:
        short_name = 'SMMA'
    else:
        short_name = 'unknown ma'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + '(' + _str(InpMAPeriod) + ')')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (InpMAPeriod - 1 + begin):
        return 0
    if prev_calculated == 0:
        ArrayInitialize(ExtLineBuffer, 0)
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpMAPeriod - 1 + begin)
    _sw2 = InpMAMethod
    if _sw2 == MODE_EMA:
        CalculateEMA(rates_total, prev_calculated, begin, price)
    elif _sw2 == MODE_LWMA:
        CalculateLWMA(rates_total, prev_calculated, begin, price)
    elif _sw2 == MODE_SMMA:
        CalculateSmoothedMA(rates_total, prev_calculated, begin, price)
    elif _sw2 == MODE_SMA:
        CalculateSimpleMA(rates_total, prev_calculated, begin, price)
    return rates_total

def CalculateSimpleMA(rates_total, prev_calculated, begin, price):
    i = 0
    start = 0
    if prev_calculated == 0:
        start = InpMAPeriod + begin
        i = 0
        for i in range(i, start - 1):
            ExtLineBuffer[i] = 0.0
        else:
            i = _range_end(i, start - 1, 1)
        first_value = 0.0
        i = begin
        for i in range(i, start):
            first_value += price[i]
        else:
            i = _range_end(i, start, 1)
        first_value = first_value / InpMAPeriod
        ExtLineBuffer[start - 1] = first_value
    else:
        start = prev_calculated - 1
    i = start
    for i in range(i, rates_total):
        ExtLineBuffer[i] = ExtLineBuffer[i - 1] + ((price[i] - price[i - InpMAPeriod]) / InpMAPeriod)
    else:
        i = _range_end(i, rates_total, 1)

def CalculateEMA(rates_total, prev_calculated, begin, price):
    i = 0
    start = 0
    SmoothFactor = _fdiv(2.0, 1.0 + InpMAPeriod)
    if prev_calculated == 0:
        start = InpMAPeriod + begin
        ExtLineBuffer[begin] = price[begin]
        i = begin + 1
        for i in range(i, start):
            ExtLineBuffer[i] = (price[i] * SmoothFactor) + (ExtLineBuffer[i - 1] * (1.0 - SmoothFactor))
        else:
            i = _range_end(i, start, 1)
    else:
        start = prev_calculated - 1
    i = start
    for i in range(i, rates_total):
        ExtLineBuffer[i] = (price[i] * SmoothFactor) + (ExtLineBuffer[i - 1] * (1.0 - SmoothFactor))
    else:
        i = _range_end(i, rates_total, 1)

def CalculateLWMA(rates_total, prev_calculated, begin, price):
    weight = 0
    i = 0
    l = 0
    start = 0
    sum_ = 0.0
    lsum = 0.0
    if prev_calculated <= (InpMAPeriod + begin + 2):
        start = InpMAPeriod + begin
        i = 0
        for i in range(i, start):
            ExtLineBuffer[i] = 0.0
        else:
            i = _range_end(i, start, 1)
    else:
        start = prev_calculated - 1
    i = start - InpMAPeriod
    l = 1
    while i < start:
        sum_ += price[i] * l
        lsum += price[i]
        weight += l
        i += 1
        l += 1
    ExtLineBuffer[start - 1] = _fdiv(sum_, weight)
    i = start
    for i in range(i, rates_total):
        sum_ = sum_ - lsum + (price[i] * InpMAPeriod)
        lsum = lsum - price[i - InpMAPeriod] + price[i]
        ExtLineBuffer[i] = _fdiv(sum_, weight)
    else:
        i = _range_end(i, rates_total, 1)

def CalculateSmoothedMA(rates_total, prev_calculated, begin, price):
    i = 0
    start = 0
    if prev_calculated == 0:
        start = InpMAPeriod + begin
        i = 0
        for i in range(i, start - 1):
            ExtLineBuffer[i] = 0.0
        else:
            i = _range_end(i, start - 1, 1)
        first_value = 0.0
        i = begin
        for i in range(i, start):
            first_value += price[i]
        else:
            i = _range_end(i, start, 1)
        first_value = first_value / InpMAPeriod
        ExtLineBuffer[start - 1] = first_value
    else:
        start = prev_calculated - 1
    i = start
    for i in range(i, rates_total):
        ExtLineBuffer[i] = ((ExtLineBuffer[i - 1] * (InpMAPeriod - 1)) + price[i]) / InpMAPeriod
    else:
        i = _range_end(i, rates_total, 1)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomMovingAverageSepWin(_MQL5Indicator):
    name = 'Custom_Moving_Average_sep_win'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAPeriod': 13,  # Period
        'InpMAShift': 0,  # Shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

