"""Custom_Moving_Average_Levels — converted from MQL5: MQL5 Indicators/Custom Moving Average Levels/Custom_Moving_Average_Levels.mq5

Standart Moving Average and two levels
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8421504], 2: [255], 3: [8421504]}, 'widths': {}, 'styles': {1: 2, 3: 2}, 'labels': {1: 'UP', 2: 'Middle', 3: 'Down'}, 'levels': [], 'description': ['Standart Moving Average and two levels'], 'name': 'Custom_Moving_Average_Levels', 'source': 'MQL5 Indicators/Custom Moving Average Levels/Custom_Moving_Average_Levels.mq5', 'folder': 'Custom Moving Average Levels', 'inputs': [{'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'int', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'InpMAShift', 'py': 'InpMAShift', 'param': 'InpMAShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 2, 'label': 'Method', 'sinput': False}, {'mql': 'InpLevelUp', 'py': 'InpLevelUp', 'param': 'InpLevelUp', 'type': 'int', 'default': 100, 'label': 'Level Up (in pips)', 'sinput': False}, {'mql': 'InpLevelDown', 'py': 'InpLevelDown', 'param': 'InpLevelDown', 'type': 'int', 'default': -100, 'label': 'Level Down (in pips)', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMAPeriod = _input('InpMAPeriod', 13)  # Period
InpMAShift = _input('InpMAShift', 0)  # Shift
InpMAMethod = _input('InpMAMethod', MODE_SMMA)  # Method
InpLevelUp = _input('InpLevelUp', 100)  # Level Up (in pips)
InpLevelDown = _input('InpLevelDown', -100)  # Level Down (in pips)
ExtLineBufferUp = Arr(0, 0.0)
ExtLineBufferMiddle = Arr(0, 0.0)
ExtLineBufferDown = Arr(0, 0.0)
ExtInpLevelUp = 0.0
ExtInpLevelDown = 0.0

def CalculateSimpleMA(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    if prev_calculated == 0:
        limit = InpMAPeriod + begin
        i = 0
        for i in range(i, limit - 1):
            ExtLineBufferMiddle[i] = 0.0
            ExtLineBufferUp[i] = 0.0
            ExtLineBufferDown[i] = 0.0
        else:
            i = _range_end(i, limit - 1, 1)
        firstValue = 0.0
        i = begin
        for i in range(i, limit):
            firstValue += price[i]
        else:
            i = _range_end(i, limit, 1)
        firstValue = firstValue / InpMAPeriod
        ExtLineBufferMiddle[limit - 1] = firstValue
        ExtLineBufferUp[limit - 1] = firstValue + ExtInpLevelUp
        ExtLineBufferDown[limit - 1] = firstValue + ExtInpLevelDown
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtLineBufferMiddle[i] = ExtLineBufferMiddle[i - 1] + ((price[i] - price[i - InpMAPeriod]) / InpMAPeriod)
        ExtLineBufferUp[i] = ExtLineBufferMiddle[i] + ExtInpLevelUp
        ExtLineBufferDown[i] = ExtLineBufferMiddle[i] + ExtInpLevelDown
    else:
        i = _range_end(i, rates_total, 1)

def CalculateEMA(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    SmoothFactor = _fdiv(2.0, 1.0 + InpMAPeriod)
    if prev_calculated == 0:
        limit = InpMAPeriod + begin
        ExtLineBufferMiddle[begin] = price[begin]
        ExtLineBufferUp[begin] = ExtLineBufferMiddle[begin] + ExtInpLevelUp
        ExtLineBufferDown[begin] = ExtLineBufferMiddle[begin] + ExtInpLevelDown
        i = begin + 1
        for i in range(i, limit):
            ExtLineBufferMiddle[i] = (price[i] * SmoothFactor) + (ExtLineBufferMiddle[i - 1] * (1.0 - SmoothFactor))
            ExtLineBufferUp[i] = ExtLineBufferMiddle[i] + ExtInpLevelUp
            ExtLineBufferDown[i] = ExtLineBufferMiddle[i] + ExtInpLevelDown
        else:
            i = _range_end(i, limit, 1)
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtLineBufferMiddle[i] = (price[i] * SmoothFactor) + (ExtLineBufferMiddle[i - 1] * (1.0 - SmoothFactor))
        ExtLineBufferUp[i] = ExtLineBufferMiddle[i] + ExtInpLevelUp
        ExtLineBufferDown[i] = ExtLineBufferMiddle[i] + ExtInpLevelDown
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
            ExtLineBufferMiddle[i] = 0.0
            ExtLineBufferUp[i] = 0.0
            ExtLineBufferDown[i] = 0.0
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
        ExtLineBufferMiddle[limit - 1] = firstValue
        ExtLineBufferUp[limit - 1] = firstValue + ExtInpLevelUp
        ExtLineBufferDown[limit - 1] = firstValue + ExtInpLevelDown
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        sum_ = 0.0
        for j in range(0, InpMAPeriod):
            sum_ += (InpMAPeriod - j) * price[i - j]
        ExtLineBufferMiddle[i] = _fdiv(sum_, _s_CalculateLWMA_weightsum)
        ExtLineBufferUp[i] = ExtLineBufferMiddle[i] + ExtInpLevelUp
        ExtLineBufferDown[i] = ExtLineBufferMiddle[i] + ExtInpLevelDown
    else:
        i = _range_end(i, rates_total, 1)

def CalculateSmoothedMA(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    if prev_calculated == 0:
        limit = InpMAPeriod + begin
        i = 0
        for i in range(i, limit - 1):
            ExtLineBufferMiddle[i] = 0.0
            ExtLineBufferUp[i] = 0.0
            ExtLineBufferDown[i] = 0.0
        else:
            i = _range_end(i, limit - 1, 1)
        firstValue = 0.0
        i = begin
        for i in range(i, limit):
            firstValue += price[i]
        else:
            i = _range_end(i, limit, 1)
        firstValue = firstValue / InpMAPeriod
        ExtLineBufferMiddle[limit - 1] = firstValue
        ExtLineBufferUp[limit - 1] = firstValue + ExtInpLevelUp
        ExtLineBufferDown[limit - 1] = firstValue + ExtInpLevelDown
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtLineBufferMiddle[i] = ((ExtLineBufferMiddle[i - 1] * (InpMAPeriod - 1)) + price[i]) / InpMAPeriod
        ExtLineBufferUp[i] = ExtLineBufferMiddle[i] + ExtInpLevelUp
        ExtLineBufferDown[i] = ExtLineBufferMiddle[i] + ExtInpLevelDown
    else:
        i = _range_end(i, rates_total, 1)

def OnInit():
    global ExtInpLevelDown, ExtInpLevelUp
    SetIndexBuffer(0, ExtLineBufferUp, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBufferDown, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpMAPeriod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpMAPeriod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpMAPeriod)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpMAShift)
    PlotIndexSetInteger(1, PLOT_SHIFT, InpMAShift)
    PlotIndexSetInteger(2, PLOT_SHIFT, InpMAShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    ExtInpLevelUp = InpLevelUp * Point()
    ExtInpLevelDown = InpLevelDown * Point()

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (InpMAPeriod - 1 + begin):
        return 0
    if prev_calculated == 0:
        ArrayInitialize(ExtLineBufferUp, 0)
        ArrayInitialize(ExtLineBufferMiddle, 0)
        ArrayInitialize(ExtLineBufferDown, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpMAPeriod - 1 + begin)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpMAPeriod - 1 + begin)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpMAPeriod - 1 + begin)
    _sw1 = InpMAMethod
    if _sw1 == MODE_EMA:
        CalculateEMA(rates_total, prev_calculated, begin, price)
    elif _sw1 == MODE_LWMA:
        CalculateLWMA(rates_total, prev_calculated, begin, price)
    elif _sw1 == MODE_SMMA:
        CalculateSmoothedMA(rates_total, prev_calculated, begin, price)
    elif _sw1 == MODE_SMA:
        CalculateSimpleMA(rates_total, prev_calculated, begin, price)
    return rates_total

# ---- static local variables
_s_CalculateLWMA_weightsum = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomMovingAverageLevels(_MQL5Indicator):
    name = 'Custom_Moving_Average_Levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAPeriod': 13,  # Period
        'InpMAShift': 0,  # Shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method
        'InpLevelUp': 100,  # Level Up (in pips)
        'InpLevelDown': -100,  # Level Down (in pips)
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

