"""murrey_math — converted from MQL5: MQL5 Indicators/Murrey Math FixPeriod/murrey_math.mq5

This indicator is created based on the algorithm
Vladislav Goshkov (VG) 4vg@mail.ru
The given indicator is created on a basis and with algorithm use
Vladislav Goshkov (VG) 4vg@mail.ru
Copyright: VDV Soft; Link: vdv_2001@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'VDV Soft', 'link': 'vdv_2001@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 13}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1}, 'colors': {1: [9109504], 2: [13828244], 3: [16776960], 4: [4163021], 5: [255], 6: [65280], 7: [11119017], 8: [65280], 9: [255], 10: [4163021], 11: [16776960], 12: [13828244], 13: [9109504]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0}, 'labels': {1: 'Pivot, reverse [-2/8]', 2: 'Weak, stall and reverse [-1/8]', 3: 'Ultimate resistance [0/8]', 4: 'Weak, stall and reverse [1/8]', 5: 'Вращение, разворот [2/8]', 6: 'Bottom of Trading Range [3/8]', 7: 'Major Support/Resistance Pivotal Point [4/8]', 8: 'Top of Trading Range [5/8]', 9: 'Pivot, Reverse [6/8]', 10: 'Weak, Stall and Reverse - [7/8]', 11: 'Ultimate Resistance [8/8]', 12: 'Weak, stall and reverse [+1/8]', 13: 'Pivot, reverse [+2/8]'}, 'levels': [], 'description': ['This indicator is created based on the algorithm', 'Vladislav Goshkov (VG) 4vg@mail.ru', 'The given indicator is created on a basis and with algorithm use', 'Vladislav Goshkov (VG) 4vg@mail.ru'], 'name': 'murrey_math', 'source': 'MQL5 Indicators/Murrey Math FixPeriod/murrey_math.mq5', 'folder': 'Murrey Math FixPeriod', 'inputs': [{'mql': 'CalculationPeriod', 'py': 'CalculationPeriod', 'param': 'CalculationPeriod', 'type': 'int', 'default': 64, 'label': 'P calculation period', 'sinput': False}, {'mql': 'StepBack', 'py': 'StepBack', 'param': 'StepBack', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CalculationPeriod = _input('CalculationPeriod', 64)  # P calculation period
StepBack = _input('StepBack', 0)
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
Buffer3 = Arr(0, 0.0)
Buffer4 = Arr(0, 0.0)
Buffer5 = Arr(0, 0.0)
Buffer6 = Arr(0, 0.0)
Buffer7 = Arr(0, 0.0)
Buffer8 = Arr(0, 0.0)
Buffer9 = Arr(0, 0.0)
Buffer10 = Arr(0, 0.0)
Buffer11 = Arr(0, 0.0)
Buffer12 = Arr(0, 0.0)
Buffer13 = Arr(0, 0.0)
ShiftBarsForward = 100
min_rates_total = 0

def OnInit():
    global ShiftBarsForward, min_rates_total
    min_rates_total = CalculationPeriod + StepBack
    SetIndexBuffer(0, Buffer1, INDICATOR_DATA)
    SetIndexBuffer(1, Buffer2, INDICATOR_DATA)
    SetIndexBuffer(2, Buffer3, INDICATOR_DATA)
    SetIndexBuffer(3, Buffer4, INDICATOR_DATA)
    SetIndexBuffer(4, Buffer5, INDICATOR_DATA)
    SetIndexBuffer(5, Buffer6, INDICATOR_DATA)
    SetIndexBuffer(6, Buffer7, INDICATOR_DATA)
    SetIndexBuffer(7, Buffer8, INDICATOR_DATA)
    SetIndexBuffer(8, Buffer9, INDICATOR_DATA)
    SetIndexBuffer(9, Buffer10, INDICATOR_DATA)
    SetIndexBuffer(10, Buffer11, INDICATOR_DATA)
    SetIndexBuffer(11, Buffer12, INDICATOR_DATA)
    SetIndexBuffer(12, Buffer13, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Murrey_Math_MT5(' + IntegerToString(CalculationPeriod) + ')')
    ShiftBarsForward = CalculationPeriod - 1
    for i in range(0, 13):
        PlotIndexSetInteger(i, PLOT_SHIFT, ShiftBarsForward)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = prev_calculated - 1
    if not prev_calculated:
        first = min_rates_total
        for i in range(0, min_rates_total + 1):
            Buffer1[i] = EMPTY_VALUE
            Buffer2[i] = EMPTY_VALUE
            Buffer3[i] = EMPTY_VALUE
            Buffer4[i] = EMPTY_VALUE
            Buffer5[i] = EMPTY_VALUE
            Buffer6[i] = EMPTY_VALUE
            Buffer7[i] = EMPTY_VALUE
            Buffer8[i] = EMPTY_VALUE
            Buffer9[i] = EMPTY_VALUE
            Buffer10[i] = EMPTY_VALUE
            Buffer11[i] = EMPTY_VALUE
            Buffer12[i] = EMPTY_VALUE
            Buffer13[i] = EMPTY_VALUE
    for i in range(first, rates_total):
        CalcMurreyMath(i, high, low)
    for i in range(1, ShiftBarsForward + 1):
        Buffer1[rates_total - i] = Buffer1[rates_total - ShiftBarsForward - 1]
        Buffer2[rates_total - i] = Buffer2[rates_total - ShiftBarsForward - 1]
        Buffer3[rates_total - i] = Buffer3[rates_total - ShiftBarsForward - 1]
        Buffer4[rates_total - i] = Buffer4[rates_total - ShiftBarsForward - 1]
        Buffer5[rates_total - i] = Buffer5[rates_total - ShiftBarsForward - 1]
        Buffer6[rates_total - i] = Buffer6[rates_total - ShiftBarsForward - 1]
        Buffer7[rates_total - i] = Buffer7[rates_total - ShiftBarsForward - 1]
        Buffer8[rates_total - i] = Buffer8[rates_total - ShiftBarsForward - 1]
        Buffer9[rates_total - i] = Buffer9[rates_total - ShiftBarsForward - 1]
        Buffer10[rates_total - i] = Buffer10[rates_total - ShiftBarsForward - 1]
        Buffer11[rates_total - i] = Buffer11[rates_total - ShiftBarsForward - 1]
        Buffer12[rates_total - i] = Buffer12[rates_total - ShiftBarsForward - 1]
        Buffer13[rates_total - i] = Buffer13[rates_total - ShiftBarsForward - 1]
    return rates_total

def CalcMurreyMath(index, high, low):
    min_ = low[ArrayMinimum(low, index - (CalculationPeriod + StepBack), CalculationPeriod + StepBack)]
    max_ = high[ArrayMaximum(high, index - (CalculationPeriod + StepBack), CalculationPeriod + StepBack)]
    fractal = DetermineFractal(max_)
    range_ = max_ - min_
    sum_ = MathFloor(_fdiv(MathLog(_fdiv(fractal, range_)), MathLog(2)))
    octave = fractal * MathPow(0.5, sum_)
    mn = MathFloor(_fdiv(min_, octave)) * octave
    mx = mn + octave
    if mx < max_:
        mx += octave
    x1 = 0.0
    x2 = 0.0
    x3 = 0.0
    x4 = 0.0
    x5 = 0.0
    x6 = 0.0
    y1 = 0.0
    y2 = 0.0
    y3 = 0.0
    y4 = 0.0
    y5 = 0.0
    y6 = 0.0
    dm = mx - mn
    dm2 = dm / 2
    dm4 = dm / 4
    dm8 = dm / 8
    dm16 = dm / 16
    if min_ >= (((3 * dm) / 16) + mn) and max_ <= ((9 * dm16) + mn):
        x2 = mn + dm2
    if (min_ >= (mn - dm8) and max_ <= ((5 * dm8) + mn)) and x2 == 0:
        x1 = mn + dm2
    if min_ >= (mn + (7 * dm16)) and max_ <= ((13 * dm16) + mn):
        x4 = mn + (3 * dm4)
    if (min_ >= (mn + (3 * dm8)) and max_ <= ((9 * dm8) + mn)) and x4 == 0:
        x5 = mx
    if ((((min_ >= (mn + dm8) and max_ <= ((7 * dm8) + mn)) and x1 == 0) and x2 == 0) and x4 == 0) and x5 == 0:
        x3 = mn + (3 * dm4)
    if (x1 + x2 + x3 + x4 + x5) == 0:
        x6 = mx
    finalH = x1 + x2 + x3 + x4 + x5 + x6
    if x1 > 0:
        y1 = mn
    if x2 > 0:
        y2 = mn + dm4
    if x3 > 0:
        y3 = mn + dm4
    if x4 > 0:
        y4 = mn + dm2
    if x5 > 0:
        y5 = mn + dm2
    finalL = y1 + y2 + y3 + y4 + y5
    if finalH > 0 and (not finalL):
        y6 = mn
    finalL += y6
    dmml = (finalH - finalL) / 8
    bar = index - ShiftBarsForward
    Buffer1[bar] = finalL - (dmml * 2)
    Buffer2[bar] = Buffer1[bar] + dmml
    Buffer3[bar] = Buffer2[bar] + dmml
    Buffer4[bar] = Buffer3[bar] + dmml
    Buffer5[bar] = Buffer4[bar] + dmml
    Buffer6[bar] = Buffer5[bar] + dmml
    Buffer7[bar] = Buffer6[bar] + dmml
    Buffer8[bar] = Buffer7[bar] + dmml
    Buffer9[bar] = Buffer8[bar] + dmml
    Buffer10[bar] = Buffer9[bar] + dmml
    Buffer11[bar] = Buffer10[bar] + dmml
    Buffer12[bar] = Buffer11[bar] + dmml
    Buffer13[bar] = Buffer12[bar] + dmml
    bar1 = bar - 1
    if (((((((((((Buffer1[bar] != Buffer1[bar1] or Buffer2[bar] != Buffer2[bar1]) or Buffer3[bar] != Buffer3[bar1]) or Buffer4[bar] != Buffer4[bar1]) or Buffer5[bar] != Buffer5[bar1]) or Buffer6[bar] != Buffer6[bar1]) or Buffer7[bar] != Buffer7[bar1]) or Buffer8[bar] != Buffer8[bar1]) or Buffer9[bar] != Buffer9[bar1]) or Buffer10[bar] != Buffer10[bar1]) or Buffer11[bar] != Buffer11[bar1]) or Buffer12[bar] != Buffer12[bar1]) or Buffer13[bar] != Buffer13[bar1]:
        Buffer1[bar1] = EMPTY_VALUE
        Buffer2[bar1] = EMPTY_VALUE
        Buffer3[bar1] = EMPTY_VALUE
        Buffer4[bar1] = EMPTY_VALUE
        Buffer5[bar1] = EMPTY_VALUE
        Buffer6[bar1] = EMPTY_VALUE
        Buffer7[bar1] = EMPTY_VALUE
        Buffer8[bar1] = EMPTY_VALUE
        Buffer9[bar1] = EMPTY_VALUE
        Buffer10[bar1] = EMPTY_VALUE
        Buffer11[bar1] = EMPTY_VALUE
        Buffer12[bar1] = EMPTY_VALUE
        Buffer13[bar1] = EMPTY_VALUE

def DetermineFractal(v):
    if v <= 250000 and v > 25000:
        return 100000.0
    if v <= 25000 and v > 2500:
        return 10000.0
    if v <= 2500 and v > 250:
        return 1000.0
    if v <= 250 and v > 25:
        return 100.0
    if v <= 25 and v > 12.5:
        return 12.5
    if v <= 12.5 and v > 6.25:
        return 12.5
    if v <= 6.25 and v > 3.125:
        return 6.25
    if v <= 3.125 and v > 1.5625:
        return 3.125
    if v <= 1.5625 and v > 0.390625:
        return 1.5625
    if v <= 0.390625 and v > 0:
        return 0.1953125
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MurreyMath(_MQL5Indicator):
    name = 'murrey_math'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CalculationPeriod': 64,  # P calculation period
        'StepBack': 0,
    }

