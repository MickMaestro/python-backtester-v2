"""Mikahekin — converted from MQL5: MQL5 Indicators/Mikahekin_HTF/Mikahekin.mq5

Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 11, 2: 5, 3: 5}, 'colors': {1: [8421504, 255, 65280], 2: [16711935], 3: [16711680]}, 'widths': {1: 5, 2: 1, 3: 1}, 'styles': {1: 0}, 'labels': {1: 'Signal', 2: 'Buy StopLoss', 3: 'Sell StopLoss'}, 'levels': [], 'description': [], 'name': 'Mikahekin', 'source': 'MQL5 Indicators/Mikahekin_HTF/Mikahekin.mq5', 'folder': 'Mikahekin_HTF', 'inputs': [{'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'JPeriod', 'py': 'JPeriod', 'param': 'JPeriod', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
KPeriod = _input('KPeriod', 3)
JPeriod = _input('JPeriod', 7)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
OpMiddleBuffer = Arr(0, 0.0)
ClMiddleBuffer = Arr(0, 0.0)
ColorMiddleBuffer = Arr(0, 0.0)
Count = Arr(0, 0)
Highest = Arr(0, 0.0)
Lowest = Arr(0, 0.0)
min_rates_total = 0

def Recount_ArrayZeroPos(CoArr):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = MathMax(KPeriod, JPeriod)
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global min_rates_total
    min_rates_total = KPeriod + JPeriod
    ArrayResize(Count, JPeriod)
    ArrayResize(Highest, JPeriod)
    ArrayResize(Lowest, JPeriod)
    SetIndexBuffer(0, OpMiddleBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(OpMiddleBuffer, True)
    SetIndexBuffer(1, ClMiddleBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ClMiddleBuffer, True)
    SetIndexBuffer(2, ColorMiddleBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorMiddleBuffer, True)
    SetIndexBuffer(3, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(4, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowerBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Mikahekin( ', KPeriod, ', ', JPeriod, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    sumlow = 0.0
    sumhigh = 0.0
    sumopen = 0.0
    sumclose = 0.0
    Max = 0.0
    Min = 0.0
    Op = 0.0
    Cl = 0.0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - KPeriod - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Highest[Count[0]] = high[ArrayMaximum(high, bar, KPeriod)]
        Lowest[Count[0]] = low[ArrayMinimum(low, bar, KPeriod)]
        if bar > (rates_total - min_rates_total - 1):
            Recount_ArrayZeroPos(Count)
            continue
        sumlow = 0.0
        sumhigh = 0.0
        sumopen = 0.0
        sumclose = 0.0
        for kkk in range(0, JPeriod):
            sumopen += open[bar + kkk]
            sumclose += close[bar + kkk]
            sumlow += Lowest[Count[kkk]]
            sumhigh += Highest[Count[kkk]]
        Op = sumopen / JPeriod
        Cl = sumclose / JPeriod
        Max = MathMax(Op, Cl)
        Min = MathMin(Op, Cl)
        if not (Max - Min):
            Max += Point()
        ClMiddleBuffer[bar] = Max
        OpMiddleBuffer[bar] = Min
        ColorMiddleBuffer[bar] = 0.0
        if Cl > Op:
            ColorMiddleBuffer[bar] = 2.0
        if Cl < Op:
            ColorMiddleBuffer[bar] = 1.0
        UpperBuffer[bar] = sumhigh / JPeriod
        LowerBuffer[bar] = sumlow / JPeriod
        if bar > 0:
            Recount_ArrayZeroPos(Count)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Mikahekin(_MQL5Indicator):
    name = 'Mikahekin'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KPeriod': 3,
        'JPeriod': 7,
    }

