"""fisherrvi — converted from MQL5: MQL5 Indicators/FisherRVI_HTF/fisherrvi.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fisher RVI', 2: 'Trigger'}, 'levels': [0.0], 'description': [], 'name': 'fisherrvi', 'source': 'MQL5 Indicators/FisherRVI_HTF/fisherrvi.mq5', 'folder': 'FisherRVI_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 8, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 8)  # Период индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
FRVIBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
Count1 = Arr(0, 0)
Count2 = Arr(0, 0)
RVI = Arr(0, 0.0)
Value1 = Arr(0, 0.0)
Value2 = Arr(0, 0.0)
Value3 = Arr(0, 0.0)

def Recount_ArrayZeroPos1(CoArr):
    global _s_Recount_ArrayZeroPos1_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max1 = Length - 1
    Max2 = Length
    _s_Recount_ArrayZeroPos1_count -= 1
    if _s_Recount_ArrayZeroPos1_count < 0:
        _s_Recount_ArrayZeroPos1_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos1_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def Recount_ArrayZeroPos2(CoArr):
    global _s_Recount_ArrayZeroPos2_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max1 = 3
    Max2 = 4
    _s_Recount_ArrayZeroPos2_count -= 1
    if _s_Recount_ArrayZeroPos2_count < 0:
        _s_Recount_ArrayZeroPos2_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos2_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global min_rates_total
    min_rates_total = Length + 3
    ArrayResize(Count1, Length)
    ArrayResize(Value1, Length)
    ArrayResize(Value2, Length)
    ArrayResize(RVI, Length)
    ArrayResize(Count2, 4)
    ArrayResize(Value3, 4)
    SetIndexBuffer(0, FRVIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    shortname = Box("")
    StringConcatenate(shortname, 'Fisher RVI(', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Num = 0.0
    Denom = 0.0
    hh = 0.0
    ll = 0.0
    tmp = 0.0
    rvi = 0.0
    Value4 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 3
        for numb in range(0, Length):
            Count1[numb] = numb
        for numb in range(0, 4):
            Count2[numb] = numb
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Value1[Count1[0]] = (close[bar] - open[bar] + (2.0 * (close[bar - 1] - open[bar - 1])) + (2.0 * (close[bar - 2] - open[bar - 2])) + (close[bar - 3] - open[bar - 3])) / 6.0
        Value2[Count1[0]] = (high[bar] - low[bar] + (2.0 * (high[bar - 1] - low[bar - 1])) + (2.0 * (high[bar - 2] - low[bar - 2])) + (high[bar - 3] - low[bar - 3])) / 6.0
        if bar < (Length + 4):
            Recount_ArrayZeroPos1(Count1)
            Recount_ArrayZeroPos2(Count2)
            continue
        Num = 0.0
        Denom = 0.0
        for iii in range(0, Length):
            Num += Value1[Count1[iii]]
            Denom += Value2[Count1[iii]]
        if Denom != 0.0:
            rvi = _fdiv(Num, Denom)
        else:
            rvi = 0.0
        RVI[Count1[0]] = rvi
        hh = rvi
        ll = rvi
        for iii in range(0, Length):
            tmp = RVI[Count1[iii]]
            hh = MathMax(hh, tmp)
            ll = MathMin(ll, tmp)
        if hh != ll:
            Value3[Count2[0]] = _fdiv(rvi - ll, hh - ll)
        else:
            Value3[Count2[0]] = 0.0
        Value4 = ((4.0 * Value3[Count2[0]]) + (3.0 * Value3[Count2[1]]) + (2.0 * Value3[Count2[2]]) + Value3[Count2[3]]) / 10.0
        res = 1.0 - (1.98 * (Value4 - 0.5))
        if res:
            FRVIBuffer[bar] = 0.5 * MathLog(_fdiv(1.0 + (1.98 * (Value4 - 0.5)), res))
        else:
            FRVIBuffer[bar] = 0.0
        TriggerBuffer[bar] = FRVIBuffer[bar - 1]
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos1(Count1)
            Recount_ArrayZeroPos2(Count2)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos1_count = 1
_s_Recount_ArrayZeroPos2_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fisherrvi(_MQL5Indicator):
    name = 'fisherrvi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 8,  # Период индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

