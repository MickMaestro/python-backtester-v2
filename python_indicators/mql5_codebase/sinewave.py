"""Sinewave — converted from MQL5: MQL5 Indicators/Sine Wave Cloud HTF/Sinewave.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.10', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Sinewave', 2: 'LeadSinewave'}, 'levels': [0.0], 'description': [], 'name': 'Sinewave', 'source': 'MQL5 Indicators/Sine Wave Cloud HTF/Sinewave.mq5', 'folder': 'Sine Wave Cloud HTF', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 0.07, 'label': 'коэффициент индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha = _input('Alpha', 0.07)  # коэффициент индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
SineBuffer = Arr(0, 0.0)
LeadSineBuffer = Arr(0, 0.0)
CP_Handle = 0
min_rates_total = 0
Count = Arr(0, 0)
Smooth = Arr(0, 0.0)
Price = Arr(0, 0.0)
Cycle = Arr(0, 0.0)
K0 = 0.0
K1 = 0.0
K2 = 0.0
K3 = 0.0
rad2Deg = 0.0
deg2Rad = 0.0

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
    return (High[bar] + Low[bar]) / 2.0

def Get_SmoothVelue(PriceArray, CountArray, bar):
    return (PriceArray[CountArray[0]] + (2 * PriceArray[CountArray[1]]) + (2 * PriceArray[CountArray[2]]) + PriceArray[CountArray[3]]) / 6

def OnInit():
    global CP_Handle, K0, K1, K2, K3, deg2Rad, min_rates_total, rad2Deg
    min_rates_total = 7
    CP_Handle = iCustom(None, 0, 'CyclePeriod', Alpha)
    if CP_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CyclePeriod')
    K0 = MathPow(1.0 - (0.5 * Alpha), 2)
    K1 = 2.0
    K2 = K1 * (1.0 - Alpha)
    K3 = MathPow(1.0 - Alpha, 2)
    rad2Deg = _fdiv(45.0, MathArctan(1.0))
    deg2Rad = _fdiv(1.0, rad2Deg)
    ArrayResize(Count, 100)
    ArrayResize(Price, 100)
    ArrayResize(Smooth, 100)
    ArrayResize(Cycle, 100)
    SetIndexBuffer(0, SineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, LeadSineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    shortname = Box("")
    StringConcatenate(shortname, 'Sinewave(', DoubleToString(Alpha, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(CP_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    DcPeriod = 0
    bar0 = 0
    bar1 = 0
    bar2 = 0
    bar3 = 0
    RealPart = 0.0
    ImagPart = 0.0
    DCPhase = 0.0
    Arg = 0.0
    period = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 3
        ArrayInitialize(Count, 0.0)
        ArrayInitialize(Price, 0.0)
        ArrayInitialize(Smooth, 0.0)
        ArrayInitialize(Cycle, 0.0)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        bar0 = Count[0]
        bar1 = Count[1]
        bar2 = Count[2]
        bar3 = Count[3]
        Price[bar0] = Get_Price(high, low, bar)
        Smooth[bar0] = Get_SmoothVelue(Price, Count, 0)
        if bar > min_rates_total:
            Cycle[bar0] = (K0 * (Smooth[bar0] - (K1 * Smooth[bar1]) + Smooth[bar2])) + (K2 * Cycle[bar1]) - (K3 * Cycle[bar2])
        else:
            Cycle[bar0] = (Price[bar0] - (2.0 * Price[bar1]) + Price[bar2]) / 4.0
        if CopyBuffer(CP_Handle, 0, rates_total - 1 - bar, 1, period) <= 0:
            return 0
        DcPeriod = _int(MathFloor(period[0]))
        DcPeriod = MathMin(DcPeriod, bar)
        RealPart = 0.0
        ImagPart = 0.0
        for iii in range(0, DcPeriod):
            Arg = _fdiv(deg2Rad * 360.0 * iii, DcPeriod)
            RealPart += MathSin(Arg) * Cycle[Count[iii]]
            ImagPart += MathCos(Arg) * Cycle[Count[iii]]
        DCPhase = 0.0
        if MathAbs(ImagPart) > 0.001:
            DCPhase = rad2Deg * MathArctan(_fdiv(RealPart, ImagPart))
        else:
            if RealPart >= 0.0:
                DCPhase = 90.0
            else:
                DCPhase = -90.0
        DCPhase += 90.0
        if ImagPart < 0:
            DCPhase += 180.0
        if DCPhase > 315.0:
            DCPhase -= 360.0
        SineBuffer[bar] = MathSin(DCPhase * deg2Rad)
        LeadSineBuffer[bar] = MathSin((DCPhase + 45.0) * deg2Rad)
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


class Sinewave(_MQL5Indicator):
    name = 'Sinewave'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 0.07,  # коэффициент индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

