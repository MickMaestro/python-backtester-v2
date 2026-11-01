"""fishercgoscillator — converted from MQL5: MQL5 Indicators/FisherCGOscillator_HTF/fishercgoscillator.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fisher CG Oscillator', 2: 'Trigger'}, 'levels': [0.0], 'description': [], 'name': 'fishercgoscillator', 'source': 'MQL5 Indicators/FisherCGOscillator_HTF/fishercgoscillator.mq5', 'folder': 'FisherCGOscillator_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 10)  # Indicator period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
FCGBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
Count1 = Arr(0, 0)
Count2 = Arr(0, 0)
CG = Arr(0, 0.0)
Value1 = Arr(0, 0.0)
CGshift = 0.0

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
    global CGshift, min_rates_total
    min_rates_total = Length
    CGshift = (Length + 1.0) / 2.0
    ArrayResize(Count1, Length)
    ArrayResize(CG, Length)
    ArrayResize(Count2, 4)
    ArrayResize(Value1, 4)
    ArrayInitialize(Count1, 0)
    ArrayInitialize(CG, 0.0)
    ArrayInitialize(Count2, 0)
    ArrayInitialize(Value1, 0.0)
    SetIndexBuffer(0, FCGBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 3)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 3)
    shortname = Box("")
    StringConcatenate(shortname, 'Fisher CG Oscillator(', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    Num = 0.0
    Denom = 0.0
    hh = 0.0
    ll = 0.0
    tmp = 0.0
    Value2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Num = 0.0
        Denom = 0.0
        for count in range(0, Length):
            price = (high[bar - count] + low[bar - count]) / 2.0
            Num += (1.0 + count) * price
            Denom += price
        if Denom != 0.0:
            CG[Count1[0]] = _fdiv(-Num, Denom) + CGshift
        else:
            CG[Count1[0]] = 0.0
        hh = CG[Count1[0]]
        ll = CG[Count1[0]]
        for iii in range(0, Length):
            tmp = CG[Count1[iii]]
            hh = MathMax(hh, tmp)
            ll = MathMin(ll, tmp)
        if hh != ll:
            Value1[Count2[0]] = _fdiv(CG[Count1[0]] - ll, hh - ll)
        else:
            Value1[Count2[0]] = 0.0
        Value2 = ((4.0 * Value1[Count2[0]]) + (3.0 * Value1[Count2[1]]) + (2.0 * Value1[Count2[2]]) + Value1[Count2[3]]) / 10.0
        FCGBuffer[bar] = 0.5 * MathLog(_fdiv(1.0 + (1.98 * (Value2 - 0.5)), 1.0 - (1.98 * (Value2 - 0.5))))
        TriggerBuffer[bar] = FCGBuffer[bar - 1]
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


class Fishercgoscillator(_MQL5Indicator):
    name = 'fishercgoscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Indicator period
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

