"""Autoscaling Zigzag — converted from MQL5: MQL5 Indicators/Autoscaling Zigzag/Autoscaling Zigzag.mq5

ZigZag with automatic step size detection for changing wave direction.
Copyright: Evgeniy Chumakov | © Copyright 2024; Link: https://www.mql5.com/en/users/jack857752; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Evgeniy Chumakov | © Copyright 2024', 'version': '1.0', 'link': 'https://www.mql5.com/en/users/jack857752', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [8421504, 15631086]}, 'widths': {}, 'styles': {1: 0}, 'labels': {1: 'ZigZag'}, 'levels': [], 'description': ['ZigZag with automatic step size detection for changing wave direction.'], 'name': 'Autoscaling Zigzag', 'source': 'MQL5 Indicators/Autoscaling Zigzag/Autoscaling Zigzag.mq5', 'folder': 'Autoscaling Zigzag', 'inputs': [{'mql': 'ZZScale', 'py': 'ZZScale', 'param': 'ZZScale', 'type': 'double', 'default': 1.0, 'label': 'Scale', 'sinput': False}, {'mql': 'ZZLineWidth', 'py': 'ZZLineWidth', 'param': 'ZZLineWidth', 'type': 'int', 'default': 2, 'label': 'Line Width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ZZScale = _input('ZZScale', 1.0)  # Scale
ZZLineWidth = _input('ZZLineWidth', 2)  # Line Width
ArrayHighZZ = Arr(0, 0.0)  # High point ZZ
ArrayLowZZ = Arr(0, 0.0)  # Low point ZZ
ArrayTypeZZ = Arr(0, 0.0)  # ZigZag direction buffer
ArrayHighBarZZ = Arr(0, 0.0)  # ZigZag maximum bar location
ArrayLowBarZZ = Arr(0, 0.0)  # ZigZag minimum bar location
ArrayHighLast = Arr(0, 0.0)  # Last maximum value
ArrayLowLast = Arr(0, 0.0)  # Last minimum value
ArrayLegCol = Arr(0, 0.0)  # Leg color
SpecDivSymb = 1.0  # Special Divider / Symbol Correction

def OnInit():
    global SpecDivSymb
    SetIndexBuffer(0, ArrayHighZZ, INDICATOR_DATA)
    SetIndexBuffer(1, ArrayLowZZ, INDICATOR_DATA)
    SetIndexBuffer(2, ArrayLegCol, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, ArrayTypeZZ, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ArrayHighBarZZ, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ArrayLowBarZZ, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ArrayHighLast, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ArrayLowLast, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ArrayHighZZ, True)
    ArraySetAsSeries(ArrayLowZZ, True)
    ArraySetAsSeries(ArrayTypeZZ, True)
    ArraySetAsSeries(ArrayHighBarZZ, True)
    ArraySetAsSeries(ArrayLowBarZZ, True)
    ArraySetAsSeries(ArrayHighLast, True)
    ArraySetAsSeries(ArrayLowLast, True)
    ArraySetAsSeries(ArrayLegCol, True)
    PlotIndexSetString(0, PLOT_LABEL, 'High Point ZZ;Low Point ZZ')
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, ZZLineWidth)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'AutoScaleZigZag')
    Find = StringFind(Symbol(), 'JPY', 0)
    if Find != -1:
        SpecDivSymb = 100.0
    else:
        SpecDivSymb = 1.0
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    total = rates_total - 2
    limit = (rates_total if (prev_calculated == 0) else (rates_total - prev_calculated + 1))
    if limit > 1:
        limit = total
        ArrayInitialize(ArrayHighZZ, EMPTY_VALUE)
        ArrayInitialize(ArrayLowZZ, EMPTY_VALUE)
        ArrayInitialize(ArrayTypeZZ, EMPTY_VALUE)
        ArrayInitialize(ArrayHighBarZZ, EMPTY_VALUE)
        ArrayInitialize(ArrayLowBarZZ, EMPTY_VALUE)
        ArrayInitialize(ArrayHighLast, EMPTY_VALUE)
        ArrayInitialize(ArrayLowLast, EMPTY_VALUE)
        CalcStartingExtremes(rates_total, high, low)
    for i in range(limit - 1, 0 - 1, -1):
        ArrayHighZZ[i] = EMPTY_VALUE
        ArrayLowZZ[i] = EMPTY_VALUE
        if ArrayTypeZZ[i + 1] != EMPTY_VALUE and ArrayTypeZZ[i + 1] > 0:
            HighZZPoint(i, high, low)
        if ArrayTypeZZ[i + 1] != EMPTY_VALUE and ArrayTypeZZ[i + 1] < 0:
            LowZZPoint(i, high, low)
    return rates_total

def HighZZPoint(index, high, low):
    PriceHigh = high[index]
    PriceLow = low[index]
    EventHigh = False
    EventLow = False
    R_Step = MathAbs(_fdiv(ArrayHighLast[index + 1] - PriceLow, PriceLow)) * 100.0
    StepDownLevel = _fdiv(PriceLow, SpecDivSymb) / ZZScale
    if PriceHigh > ArrayHighLast[index + 1]:
        EventHigh = True
        ArrayTypeZZ[index] = 1.0
        prev_high_index = _int(ArrayHighBarZZ[index + 1])
        if prev_high_index >= 0:
            ArrayHighZZ[prev_high_index] = EMPTY_VALUE
        ArrayHighZZ[index] = PriceHigh
        ArrayHighBarZZ[index] = index
        ArrayLowBarZZ[index] = ArrayLowBarZZ[index + 1]
        ArrayHighLast[index] = PriceHigh
        ArrayLowLast[index] = ArrayLowLast[index + 1]
        ArrayLegCol[index] = 1.0
    if R_Step >= StepDownLevel and (not EventHigh):
        EventLow = True
        ArrayTypeZZ[index] = -1.0
        ArrayLowZZ[index] = PriceLow
        ArrayLowLast[index] = PriceLow
        ArrayHighLast[index] = ArrayHighLast[index + 1]
        ArrayHighBarZZ[index] = ArrayHighBarZZ[index + 1]
        ArrayLowBarZZ[index] = index
        ArrayLegCol[index] = 0.0
    if (not EventHigh) and (not EventLow):
        ArrayTypeZZ[index] = ArrayTypeZZ[index + 1]
        ArrayHighBarZZ[index] = ArrayHighBarZZ[index + 1]
        ArrayLowBarZZ[index] = ArrayLowBarZZ[index + 1]
        ArrayHighLast[index] = ArrayHighLast[index + 1]
        ArrayLowLast[index] = ArrayLowLast[index + 1]
    return

def LowZZPoint(index, high, low):
    PriceHigh = high[index]
    PriceLow = low[index]
    EventLow = False
    EventHigh = False
    R_Step = MathAbs(_fdiv(ArrayLowLast[index + 1] - PriceHigh, PriceHigh)) * 100.0
    StepUpLevel = _fdiv(PriceHigh, SpecDivSymb) / ZZScale
    if PriceLow < ArrayLowLast[index + 1]:
        EventLow = True
        ArrayTypeZZ[index] = -1.0
        prev_low_index = _int(ArrayLowBarZZ[index + 1])
        if prev_low_index >= 0:
            ArrayLowZZ[prev_low_index] = EMPTY_VALUE
        ArrayLowZZ[index] = PriceLow
        ArrayLowBarZZ[index] = index
        ArrayHighBarZZ[index] = ArrayHighBarZZ[index + 1]
        ArrayHighLast[index] = ArrayHighLast[index + 1]
        ArrayLowLast[index] = PriceLow
        ArrayLegCol[index] = 0.0
    if R_Step >= StepUpLevel and (not EventLow):
        EventHigh = True
        ArrayTypeZZ[index] = 1.0
        ArrayHighZZ[index] = PriceHigh
        ArrayHighLast[index] = PriceHigh
        ArrayLowLast[index] = ArrayLowLast[index + 1]
        ArrayHighBarZZ[index] = index
        ArrayLowBarZZ[index] = ArrayLowBarZZ[index + 1]
        ArrayLegCol[index] = 1.0
    if (not EventHigh) and (not EventLow):
        ArrayTypeZZ[index] = ArrayTypeZZ[index + 1]
        ArrayHighBarZZ[index] = ArrayHighBarZZ[index + 1]
        ArrayLowBarZZ[index] = ArrayLowBarZZ[index + 1]
        ArrayHighLast[index] = ArrayHighLast[index + 1]
        ArrayLowLast[index] = ArrayLowLast[index + 1]
    return

def CalcStartingExtremes(limit, high, low):
    init_index = 0
    for i in range(limit - 1, 0 - 1, -1):
        period_start = i
        MaxBar = ArrayMaximum(high, period_start, limit)
        MinBar = ArrayMinimum(low, period_start, limit)
        Max_Price = high[MaxBar]
        Min_Price = low[MinBar]
        R_Step = MathAbs(_fdiv(Max_Price - Min_Price, Min_Price)) * 100.0
        StepUpLevel = _fdiv(Max_Price, SpecDivSymb) / ZZScale
        StepDownLevel = _fdiv(Min_Price, SpecDivSymb) / ZZScale
        if (MaxBar != MinBar and MaxBar < MinBar) and R_Step >= StepUpLevel:
            ArrayTypeZZ[period_start] = 1.0
            ArrayHighZZ[MaxBar] = Max_Price
            ArrayLowZZ[MinBar] = Min_Price
            ArrayHighBarZZ[period_start] = MaxBar
            ArrayLowBarZZ[period_start] = MinBar
            ArrayHighLast[period_start] = Max_Price
            ArrayLowLast[period_start] = Min_Price
            init_index = period_start
        if init_index != 0:
            break
        if (MaxBar != MinBar and MinBar < MaxBar) and R_Step >= StepDownLevel:
            ArrayTypeZZ[period_start] = -1.0
            ArrayHighZZ[MaxBar] = Max_Price
            ArrayLowZZ[MinBar] = Min_Price
            ArrayHighBarZZ[period_start] = MaxBar
            ArrayLowBarZZ[period_start] = MinBar
            ArrayHighLast[period_start] = Max_Price
            ArrayLowLast[period_start] = Min_Price
            init_index = period_start
        if init_index != 0:
            break
    return init_index


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AutoscalingZigzag(_MQL5Indicator):
    name = 'Autoscaling Zigzag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ZZScale': 1.0,  # Scale
        'ZZLineWidth': 2,  # Line Width
    }

