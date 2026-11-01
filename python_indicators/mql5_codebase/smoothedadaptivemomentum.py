"""smoothedadaptivemomentum — converted from MQL5: MQL5 Indicators/Smoothed Adaptive Momentum/smoothedadaptivemomentum.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Smoothed Adaptive Momentum'}, 'levels': [0.0], 'description': [], 'name': 'smoothedadaptivemomentum', 'source': 'MQL5 Indicators/Smoothed Adaptive Momentum/smoothedadaptivemomentum.mq5', 'folder': 'Smoothed Adaptive Momentum', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 0.07, 'label': 'Indicator ratio', 'sinput': False}, {'mql': 'Cutoff', 'py': 'Cutoff', 'param': 'Cutoff', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha = _input('Alpha', 0.07)  # Indicator ratio
Cutoff = _input('Cutoff', 8)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
MomentumBuffer = Arr(0, 0.0)
CP_Handle = 0
min_rates_total = 0
Count = Arr(0, 0)
Price = Arr(0, 0.0)
Momentum = Arr(0, 0.0)
coef1 = 0.0
coef2 = 0.0
coef3 = 0.0
coef4 = 0.0

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def Get_Price(High, Low, bar):
    return (High[bar] + Low[bar]) / 2

def OnInit():
    global CP_Handle, coef1, coef2, coef3, coef4, min_rates_total
    min_rates_total = 7
    CP_Handle = iCustom(None, 0, 'CyclePeriod', Alpha)
    if CP_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the CyclePeriod indicator')
    pi = MathArctan(1.0) * 4.0
    a1 = MathExp((-pi) / Cutoff)
    b1 = 2 * a1 * MathCos((MathSqrt(3.0) * pi) / Cutoff)
    c1 = a1 * a1
    coef2 = b1 + c1
    coef3 = -(c1 + (b1 * c1))
    coef4 = c1 * c1
    coef1 = 1.0 - coef2 - coef3 - coef4
    ArrayResize(Count, 100)
    ArrayResize(Price, 100)
    ArrayResize(Momentum, 100)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Price, 0)
    ArrayInitialize(Momentum, 0)
    SetIndexBuffer(0, MomentumBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'Smoothed Adaptive Momentum(', DoubleToString(Alpha, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(CP_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    period = Arr(1, 0.0, dyn=False)
    first = 0
    bar = 0
    Length = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 3
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Price[Count[0]] = Get_Price(high, low, bar)
        if CopyBuffer(CP_Handle, 0, rates_total - 1 - bar, 1, period) <= 0:
            return 0
        Length = _int(MathFloor(period[0]))
        Length = MathMax(Length, 1)
        Length = MathMin(Length, bar)
        Length = MathMin(Length, 100)
        Momentum[Count[0]] = Price[Count[0]] - Price[Count[Length - 1]]
        if bar > 8:
            MomentumBuffer[bar] = (coef1 * Momentum[Count[1]]) + (coef2 * MomentumBuffer[bar - 1]) + (coef3 * MomentumBuffer[bar - 2]) + (coef4 * MomentumBuffer[bar - 3])
        else:
            MomentumBuffer[bar] = Momentum[Count[0]]
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, 100)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Smoothedadaptivemomentum(_MQL5Indicator):
    name = 'smoothedadaptivemomentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 0.07,  # Indicator ratio
        'Cutoff': 8,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

