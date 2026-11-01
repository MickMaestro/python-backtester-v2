"""Mikahekin_System — converted from MQL5: MQL5 Indicators/Mikahekin_System/Mikahekin_System.mq5

Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 5}, 'types': {1: 7, 2: 11, 3: 1, 4: 1, 5: 17}, 'colors': {1: [16443110], 2: [8421504, 255, 65280], 3: [16711680], 4: [16711935], 5: [65535, 12180223, 8421504, 15130800, 16760576]}, 'widths': {2: 5, 3: 1, 4: 1, 5: 2}, 'styles': {2: 0, 5: 0}, 'labels': {1: 'Mikahekin_System Cloud', 2: 'Signal', 3: 'Buy StopLoss', 4: 'Sell StopLoss', 5: 'Mikahekin_System_BARS'}, 'levels': [], 'description': [], 'name': 'Mikahekin_System', 'source': 'MQL5 Indicators/Mikahekin_System/Mikahekin_System.mq5', 'folder': 'Mikahekin_System', 'inputs': [{'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'JPeriod', 'py': 'JPeriod', 'param': 'JPeriod', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 1, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
KPeriod = _input('KPeriod', 3)
JPeriod = _input('JPeriod', 7)
Shift = _input('Shift', 1)  # сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
OpMiddleBuffer = Arr(0, 0.0)
ClMiddleBuffer = Arr(0, 0.0)
ColorMiddleBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
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
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, OpMiddleBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(OpMiddleBuffer, True)
    SetIndexBuffer(3, ClMiddleBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ClMiddleBuffer, True)
    SetIndexBuffer(4, ColorMiddleBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorMiddleBuffer, True)
    SetIndexBuffer(5, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(6, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    ArraySetAsSeries(LowerBuffer, True)
    SetIndexBuffer(7, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(9, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(10, ExtCloseBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    SetIndexBuffer(11, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    shortname = Box("")
    StringConcatenate(shortname, 'Mikahekin( ', KPeriod, ', ', JPeriod, ', ', Shift, ' )')
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
        UpBuffer[bar] = sumhigh / JPeriod
        UpperBuffer[bar] = UpBuffer[bar]
        DnBuffer[bar] = sumlow / JPeriod
        LowerBuffer[bar] = DnBuffer[bar]
        if bar:
            Recount_ArrayZeroPos(Count)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= Shift
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        ExtOpenBuffer[bar] = 0.0
        ExtCloseBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        ExtLowBuffer[bar] = 0.0
        if close[bar] > UpBuffer[bar + Shift]:
            if open[bar] <= close[bar]:
                clr = 4
            else:
                clr = 3
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
        if close[bar] < DnBuffer[bar + Shift]:
            if open[bar] > close[bar]:
                clr = 0
            else:
                clr = 1
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
        ExtColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MikahekinSystem(_MQL5Indicator):
    name = 'Mikahekin_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KPeriod': 3,
        'JPeriod': 7,
        'Shift': 1,  # сдвиг индикатора по горизонтали в барах
    }

