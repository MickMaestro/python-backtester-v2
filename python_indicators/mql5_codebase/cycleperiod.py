"""cycleperiod — converted from MQL5: MQL5 Indicators/Adaptive CG Oscillator/cycleperiod.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Cycle Period'}, 'levels': [], 'description': [], 'name': 'cycleperiod', 'source': 'MQL5 Indicators/Adaptive CG Oscillator/cycleperiod.mq5', 'folder': 'Adaptive CG Oscillator', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 0.07, 'label': 'Indicator ratio', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha = _input('Alpha', 0.07)  # Indicator ratio
CPeriodBuffer = Arr(0, 0.0)
min_rates_total = 0
med2 = False
median = 0
median2 = 0
InstPeriod_ = 0.0
CPeriod_ = 0.0
Count1 = Arr(0, 0)
Count2 = Arr(0, 0)
K0 = 0.0
K1 = 0.0
K2 = 0.0
K3 = 0.0
F0 = 0.0
F1 = 0.0
F2 = 0.0
F3 = 0.0
Smooth = Arr(0, 0.0)
Cycle = Arr(0, 0.0)
Q1 = Arr(0, 0.0)
I1 = Arr(0, 0.0)
DeltaPhase = Arr(0, 0.0)
M = Arr(0, 0.0)
Price = Arr(0, 0.0)

def Recount_ArrayZeroPos1(CoArr):
    global _s_Recount_ArrayZeroPos1_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = 7
    Max1 = Max2 - 1
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
    Max2 = median
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos2_count -= 1
    if _s_Recount_ArrayZeroPos2_count < 0:
        _s_Recount_ArrayZeroPos2_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos2_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global F0, F1, F2, F3, K0, K1, K2, K3, med2, median, median2, min_rates_total
    K0 = MathPow(1.0 - (0.5 * Alpha), 2)
    K1 = 2.0
    K2 = K1 * (1.0 - Alpha)
    K3 = MathPow(1.0 - Alpha, 2)
    F0 = 0.0962
    F1 = 0.5769
    F2 = 0.5
    F3 = 0.08
    median = 5
    median2 = _idiv(median, 2)
    if _imod(median, 2) == 0:
        med2 = True
    else:
        med2 = False
    ArrayResize(Count1, 7)
    ArrayResize(Smooth, 7)
    ArrayResize(Cycle, 7)
    ArrayResize(Q1, 7)
    ArrayResize(I1, 7)
    ArrayResize(Price, 7)
    ArrayResize(Count2, median)
    ArrayResize(DeltaPhase, median)
    ArrayResize(M, median)
    ArrayInitialize(Count1, 0.0)
    ArrayInitialize(Smooth, 0.0)
    ArrayInitialize(Cycle, 0.0)
    ArrayInitialize(Q1, 0.0)
    ArrayInitialize(I1, 0.0)
    ArrayInitialize(Price, 0.0)
    ArrayInitialize(Count2, 0.0)
    ArrayInitialize(DeltaPhase, 0.0)
    ArrayInitialize(M, 0)
    min_rates_total = median + 16
    SetIndexBuffer(0, CPeriodBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'Cycle Period(', DoubleToString(Alpha, 4), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global CPeriod_, InstPeriod_
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    bar0 = 0
    bar1 = 0
    bar2 = 0
    bar3 = 0
    bar4 = 0
    bar6 = 0
    CPeriod = 0.0
    InstPeriod = 0.0
    MedianDelta = 0.0
    DC = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        CPeriod_ = 1.0
        InstPeriod_ = 1.0
        CPeriodBuffer[0] = 1.0
    else:
        first = prev_calculated - 1
    InstPeriod = InstPeriod_
    CPeriod = CPeriod_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            CPeriod_ = CPeriod
            InstPeriod_ = InstPeriod
        bar0 = Count1[0]
        bar1 = Count1[1]
        bar2 = Count1[2]
        bar3 = Count1[3]
        bar4 = Count1[4]
        bar6 = Count1[6]
        Price[bar0] = (high[bar] + low[bar]) / 2.0
        Smooth[bar0] = (Price[bar0] + (2.0 * Price[bar1]) + (2.0 * Price[bar2]) + Price[bar3]) / 6.0
        if bar < 6:
            Cycle[bar0] = (Price[bar0] - (2.0 * Price[bar1]) + Price[bar2]) / 4.0
        else:
            Cycle[bar0] = (K0 * (Smooth[bar0] - (K1 * Smooth[bar1]) + Smooth[bar2])) + (K2 * Cycle[bar1]) - (K3 * Cycle[bar2])
        Q1[bar0] = ((F0 * Cycle[bar0]) + (F1 * Cycle[bar2]) - (F1 * Cycle[bar4]) - (F0 * Cycle[bar6])) * (F2 + (F3 * InstPeriod))
        I1[bar0] = Cycle[Count1[3]]
        if Q1[bar0] and Q1[bar1]:
            DeltaPhase[Count2[0]] = _fdiv(_fdiv(I1[bar0], Q1[bar0]) - _fdiv(I1[bar1], Q1[bar1]), 1.0 + _fdiv(I1[bar0] * I1[bar1], Q1[bar0] * Q1[bar1]))
        bar0 = Count2[0]
        DeltaPhase[bar0] = MathMax(0.1, DeltaPhase[bar0])
        DeltaPhase[bar0] = MathMin(1.1, DeltaPhase[bar0])
        ArrayCopy(M, DeltaPhase, 0, 0, WHOLE_ARRAY)
        ArraySort(M)
        if med2:
            MedianDelta = (M[median2] + M[median2 + 1]) / 2.0
        else:
            MedianDelta = M[median2]
        if not MedianDelta:
            DC = 15.0
        else:
            DC = _fdiv(6.28318, MedianDelta) + 0.5
        InstPeriod = (0.67 * InstPeriod) + (0.33 * DC)
        CPeriod = (0.85 * CPeriod) + (0.15 * InstPeriod)
        CPeriodBuffer[bar] = CPeriod
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


class Cycleperiod(_MQL5Indicator):
    name = 'cycleperiod'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 0.07,  # Indicator ratio
    }

