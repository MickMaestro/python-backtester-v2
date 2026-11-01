"""fishercybercycle — converted from MQL5: MQL5 Indicators/Fisher Cyber Cycle/fishercybercycle.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fisher Cyber Cycle', 2: 'Trigger'}, 'levels': [0.7, 0.0, -0.7], 'description': [], 'name': 'fishercybercycle', 'source': 'MQL5 Indicators/Fisher Cyber Cycle/fishercybercycle.mq5', 'folder': 'Fisher Cyber Cycle', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 0.07, 'label': 'Indicator ratio', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 8, 'label': 'Indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha = _input('Alpha', 0.07)  # Indicator ratio
Length = _input('Length', 8)  # Indicator period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
FishCCBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
Count1 = Arr(0, 0)
Count2 = Arr(0, 0)
K0 = 0.0
K1 = 0.0
K2 = 0.0
K3 = 0.0
Smooth = Arr(0, 0.0)
Cycle = Arr(0, 0.0)
Value1 = Arr(0, 0.0)
Price = Arr(0, 0.0)

def Recount_ArrayZeroPos1(CoArr):
    global _s_Recount_ArrayZeroPos1_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max1 = Length + 1
    Max2 = Length + 2
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
    Max1 = Length + 2
    Max2 = Length + 3
    _s_Recount_ArrayZeroPos2_count -= 1
    if _s_Recount_ArrayZeroPos2_count < 0:
        _s_Recount_ArrayZeroPos2_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos2_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global K0, K1, K2, K3, min_rates_total
    min_rates_total = Length + 3
    K0 = MathPow(1.0 - (0.5 * Alpha), 2)
    K1 = 2.0
    K2 = 2.0 * (1.0 - Alpha)
    K3 = MathPow(1.0 - Alpha, 2)
    ArrayResize(Count1, Length + 2)
    ArrayResize(Cycle, Length + 2)
    ArrayResize(Count2, Length + 3)
    ArrayResize(Value1, Length + 3)
    ArrayResize(Price, Length + 3)
    ArrayResize(Smooth, Length + 3)
    SetIndexBuffer(0, FishCCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    shortname = Box("")
    StringConcatenate(shortname, 'Fisher Cyber Cycle(', DoubleToString(Alpha, 4), ', ', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    hh = 0.0
    ll = 0.0
    tmp = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 3
        for numb in range(0, Length + 2):
            Count1[numb] = numb
        for numb in range(0, Length + 3):
            Count2[numb] = numb
        val = (high[first] + low[first]) / 2.0
        ArrayInitialize(Price, val)
        ArrayInitialize(Smooth, val)
        ArrayInitialize(Cycle, val)
        ArrayInitialize(Value1, val)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Price[Count2[0]] = (high[bar] + low[bar]) / 2.0
        Smooth[Count2[0]] = (Price[Count2[0]] + (2.0 * Price[Count2[1]]) + (2.0 * Price[Count2[2]]) + Price[Count2[3]]) / 6.0
        if bar < 3:
            Recount_ArrayZeroPos1(Count1)
            Recount_ArrayZeroPos2(Count2)
            continue
        if bar < min_rates_total:
            Cycle[Count1[0]] = (Price[Count1[0]] + (2.0 * Price[Count2[1]]) + Price[Count2[2]]) / 4.0
        else:
            Cycle[Count1[0]] = (K0 * (Smooth[Count2[0]] - (K1 * Smooth[Count2[1]]) + Smooth[Count2[2]])) + (K2 * Cycle[Count1[1]]) - (K3 * Cycle[Count1[2]])
        hh = Cycle[Count1[0]]
        ll = Cycle[Count1[0]]
        for iii in range(0, Length):
            tmp = Cycle[Count1[iii]]
            hh = MathMax(hh, tmp)
            ll = MathMin(ll, tmp)
        if hh != ll:
            Value1[Count2[0]] = _fdiv(Cycle[Count1[0]] - ll, hh - ll)
        else:
            Value1[Count2[0]] = 0.0
        FishCCBuffer[bar] = ((4.0 * Value1[Count2[0]]) + (3.0 * Value1[Count2[1]]) + (2.0 * Value1[Count2[2]]) + Value1[Count2[3]]) / 10.0
        FishCCBuffer[bar] = 0.5 * MathLog(_fdiv(1.0 + (1.98 * (FishCCBuffer[bar] - 0.5)), 1.0 - (1.98 * (FishCCBuffer[bar] - 0.5))))
        TriggerBuffer[bar] = FishCCBuffer[bar - 1]
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


class Fishercybercycle(_MQL5Indicator):
    name = 'fishercybercycle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 0.07,  # Indicator ratio
        'Length': 8,  # Indicator period
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

