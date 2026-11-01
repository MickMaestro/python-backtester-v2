"""Custom Moving Average Inputs — converted from MQL5: MQL5 Indicators/Custom Moving Average Inputs/Custom Moving Average Inputs.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Custom Moving Average Inputs', 'source': 'MQL5 Indicators/Custom Moving Average Inputs/Custom Moving Average Inputs.mq5', 'folder': 'Custom Moving Average Inputs', 'inputs': [{'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'int', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'InpMAShift', 'py': 'InpMAShift', 'param': 'InpMAShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 2, 'label': 'Method', 'sinput': False}, {'mql': 'InpColor', 'py': 'InpColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Color', 'sinput': False}, {'mql': 'InpWidth', 'py': 'InpWidth', 'param': 'InpWidth', 'type': 'int', 'default': 1, 'label': 'Width', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMAPeriod = _input('InpMAPeriod', 13)  # Period
InpMAShift = _input('InpMAShift', 0)  # Shift
InpMAMethod = _input('InpMAMethod', MODE_SMMA)  # Method
InpColor = _input('InpColor', clrBlue)  # Color
InpWidth = _input('InpWidth', 1)  # Width
ExtLineBuffer = Arr(0, 0.0)

def CalculateSimpleMA(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    if prev_calculated == 0:
        limit = InpMAPeriod + begin
        i = 0
        for i in range(i, limit - 1):
            ExtLineBuffer[i] = 0.0
        else:
            i = _range_end(i, limit - 1, 1)
        firstValue = 0.0
        i = begin
        for i in range(i, limit):
            firstValue += price[i]
        else:
            i = _range_end(i, limit, 1)
        firstValue = firstValue / InpMAPeriod
        ExtLineBuffer[limit - 1] = firstValue
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtLineBuffer[i] = ExtLineBuffer[i - 1] + ((price[i] - price[i - InpMAPeriod]) / InpMAPeriod)
    else:
        i = _range_end(i, rates_total, 1)

def CalculateEMA(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    SmoothFactor = _fdiv(2.0, 1.0 + InpMAPeriod)
    if prev_calculated == 0:
        limit = InpMAPeriod + begin
        ExtLineBuffer[begin] = price[begin]
        i = begin + 1
        for i in range(i, limit):
            ExtLineBuffer[i] = (price[i] * SmoothFactor) + (ExtLineBuffer[i - 1] * (1.0 - SmoothFactor))
        else:
            i = _range_end(i, limit, 1)
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtLineBuffer[i] = (price[i] * SmoothFactor) + (ExtLineBuffer[i - 1] * (1.0 - SmoothFactor))
    else:
        i = _range_end(i, rates_total, 1)

def CalculateLWMA(rates_total, prev_calculated, begin, price):
    global _s_CalculateLWMA_weightsum
    i = 0
    limit = 0
    sum_ = 0.0
    if prev_calculated == 0:
        _s_CalculateLWMA_weightsum = 0
        limit = InpMAPeriod + begin
        i = 0
        for i in range(i, limit):
            ExtLineBuffer[i] = 0.0
        else:
            i = _range_end(i, limit, 1)
        firstValue = 0.0
        i = begin
        for i in range(i, limit):
            k = i - begin + 1
            _s_CalculateLWMA_weightsum += k
            firstValue += k * price[i]
        else:
            i = _range_end(i, limit, 1)
        firstValue = _fdiv(firstValue, float(_s_CalculateLWMA_weightsum))
        ExtLineBuffer[limit - 1] = firstValue
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        sum_ = 0.0
        for j in range(0, InpMAPeriod):
            sum_ += (InpMAPeriod - j) * price[i - j]
        ExtLineBuffer[i] = _fdiv(sum_, _s_CalculateLWMA_weightsum)
    else:
        i = _range_end(i, rates_total, 1)

def CalculateSmoothedMA(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    if prev_calculated == 0:
        limit = InpMAPeriod + begin
        i = 0
        for i in range(i, limit - 1):
            ExtLineBuffer[i] = 0.0
        else:
            i = _range_end(i, limit - 1, 1)
        firstValue = 0.0
        i = begin
        for i in range(i, limit):
            firstValue += price[i]
        else:
            i = _range_end(i, limit, 1)
        firstValue = firstValue / InpMAPeriod
        ExtLineBuffer[limit - 1] = firstValue
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtLineBuffer[i] = ((ExtLineBuffer[i - 1] * (InpMAPeriod - 1)) + price[i]) / InpMAPeriod
    else:
        i = _range_end(i, rates_total, 1)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpMAPeriod)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpMAShift)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, InpColor)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, InpWidth)
    short_name = 'unknown ma'
    _sw1 = InpMAMethod
    if _sw1 == MODE_EMA:
        short_name = 'EMA'
    elif _sw1 == MODE_LWMA:
        short_name = 'LWMA'
    elif _sw1 == MODE_SMA:
        short_name = 'SMA'
    elif _sw1 == MODE_SMMA:
        short_name = 'SMMA'
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

# ---- static local variables
_s_CalculateLWMA_weightsum = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomMovingAverageInputs(_MQL5Indicator):
    name = 'Custom Moving Average Inputs'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAPeriod': 13,  # Period
        'InpMAShift': 0,  # Shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method
        'InpWidth': 1,  # Width
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

