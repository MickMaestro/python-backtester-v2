"""murrey_math_mt5 — converted from MQL5: MQL5 Indicators/Murrey Math Lines (support and resistance)/murrey_math_mt5.mq5

The indicator is created on a basis and with algorithm use
Vladislav Goshkov (VG) 4vg@mail.ru
Copyright: VDV Soft; Link: vdv_2001@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'VDV Soft', 'link': 'vdv_2001@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 13}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1}, 'colors': {1: [9109504], 2: [13828244], 3: [16776960], 4: [4163021], 5: [255], 6: [65280], 7: [11119017], 8: [65280], 9: [255], 10: [4163021], 11: [16776960], 12: [13828244], 13: [9109504]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0}, 'labels': {1: 'Extremely overshoot [-2/8]', 2: 'Overshoot [-1/8]', 3: 'Ultimate Support - extremely oversold [0/8]', 4: 'Weak, Stall and Reverse - [1/8]', 5: 'Pivot, Reverse - major [2/8]', 6: 'Bottom of Trading Range - [3/8], if 10-12 bars then 40% Time. BUY Premium Zone', 7: 'Major Support/Resistance Pivotal Point [4/8]- Best New BUY or SELL level', 8: 'Top of Trading Range - [5/8], if 10-12 bars then 40% Time. SELL Premium Zone', 9: 'Pivot, Reverse - major [6/8]', 10: 'Weak, Stall and Reverse - [7/8]', 11: 'Ultimate Resistance - extremely overbought [8/8]', 12: 'Overshoot [+1/8]', 13: 'Extremely overshoot [+2/8]'}, 'levels': [], 'description': ['The indicator is created on a basis and with algorithm use', 'Vladislav Goshkov (VG) 4vg@mail.ru'], 'name': 'murrey_math_mt5', 'source': 'MQL5 Indicators/Murrey Math Lines (support and resistance)/murrey_math_mt5.mq5', 'folder': 'Murrey Math Lines (support and resistance)', 'inputs': [{'mql': 'CalculationPeriod', 'py': 'CalculationPeriod', 'param': 'CalculationPeriod', 'type': 'int', 'default': 64, 'label': 'The calculation period P', 'sinput': False}, {'mql': 'StepBack', 'py': 'StepBack', 'param': 'StepBack', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CalculationPeriod = _input('CalculationPeriod', 64)  # The calculation period P
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

def OnInit():
    global ShiftBarsForward
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
    if rates_total < (CalculationPeriod + StepBack):
        return 0
    limit = 0
    if prev_calculated == 0:
        limit = CalculationPeriod + StepBack
        ArrayInitialize(Buffer1, EMPTY_VALUE)
        ArrayInitialize(Buffer2, EMPTY_VALUE)
        ArrayInitialize(Buffer3, EMPTY_VALUE)
        ArrayInitialize(Buffer4, EMPTY_VALUE)
        ArrayInitialize(Buffer5, EMPTY_VALUE)
        ArrayInitialize(Buffer6, EMPTY_VALUE)
        ArrayInitialize(Buffer7, EMPTY_VALUE)
        ArrayInitialize(Buffer8, EMPTY_VALUE)
        ArrayInitialize(Buffer9, EMPTY_VALUE)
        ArrayInitialize(Buffer10, EMPTY_VALUE)
        ArrayInitialize(Buffer11, EMPTY_VALUE)
        ArrayInitialize(Buffer12, EMPTY_VALUE)
        ArrayInitialize(Buffer13, EMPTY_VALUE)
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
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
    mx = mn + (2 * octave)
    if (mn + octave) >= max_:
        mx = mn + octave
    x2 = 0.0
    if min_ >= (((3 * (mx - mn)) / 16) + mn) and max_ <= (((9 * (mx - mn)) / 16) + mn):
        x2 = mn + ((mx - mn) / 2)
    x1 = 0.0
    if (min_ >= (mn - ((mx - mn) / 8)) and max_ <= (((5 * (mx - mn)) / 8) + mn)) and x2 == 0:
        x1 = mn + ((mx - mn) / 2)
    x4 = 0.0
    if min_ >= (mn + ((7 * (mx - mn)) / 16)) and max_ <= (((13 * (mx - mn)) / 16) + mn):
        x4 = mn + ((3 * (mx - mn)) / 4)
    x5 = 0.0
    if (min_ >= (mn + ((3 * (mx - mn)) / 8)) and max_ <= (((9 * (mx - mn)) / 8) + mn)) and x4 == 0:
        x5 = mx
    x3 = 0.0
    if ((((min_ >= (mn + ((mx - mn) / 8)) and max_ <= (((7 * (mx - mn)) / 8) + mn)) and x1 == 0) and x2 == 0) and x4 == 0) and x5 == 0:
        x3 = mn + ((3 * (mx - mn)) / 4)
    x6 = 0.0
    if (x1 + x2 + x3 + x4 + x5) == 0:
        x6 = mx
    finalH = x1 + x2 + x3 + x4 + x5 + x6
    y1 = 0.0
    if x1 > 0:
        y1 = mn
    y2 = 0.0
    if x2 > 0:
        y2 = mn + ((mx - mn) / 4)
    y3 = 0.0
    if x3 > 0:
        y3 = mn + ((mx - mn) / 4)
    y4 = 0.0
    if x4 > 0:
        y4 = mn + ((mx - mn) / 2)
    y5 = 0.0
    if x5 > 0:
        y5 = mn + ((mx - mn) / 2)
    y6 = 0.0
    if finalH > 0 and (y1 + y2 + y3 + y4 + y5) == 0:
        y6 = mn
    finalL = y1 + y2 + y3 + y4 + y5 + y6
    dmml = (finalH - finalL) / 8
    shift = index - ShiftBarsForward
    Buffer1[shift] = finalL - (dmml * 2)
    Buffer2[shift] = Buffer1[shift] + dmml
    Buffer3[shift] = Buffer2[shift] + dmml
    Buffer4[shift] = Buffer3[shift] + dmml
    Buffer5[shift] = Buffer4[shift] + dmml
    Buffer6[shift] = Buffer5[shift] + dmml
    Buffer7[shift] = Buffer6[shift] + dmml
    Buffer8[shift] = Buffer7[shift] + dmml
    Buffer9[shift] = Buffer8[shift] + dmml
    Buffer10[shift] = Buffer9[shift] + dmml
    Buffer11[shift] = Buffer10[shift] + dmml
    Buffer12[shift] = Buffer11[shift] + dmml
    Buffer13[shift] = Buffer12[shift] + dmml
    if Buffer1[shift] != Buffer1[shift - 1]:
        Buffer1[shift - 1] = EMPTY_VALUE
    if Buffer2[shift] != Buffer2[shift - 1]:
        Buffer2[shift - 1] = EMPTY_VALUE
    if Buffer3[shift] != Buffer3[shift - 1]:
        Buffer3[shift - 1] = EMPTY_VALUE
    if Buffer4[shift] != Buffer4[shift - 1]:
        Buffer4[shift - 1] = EMPTY_VALUE
    if Buffer5[shift] != Buffer5[shift - 1]:
        Buffer5[shift - 1] = EMPTY_VALUE
    if Buffer6[shift] != Buffer6[shift - 1]:
        Buffer6[shift - 1] = EMPTY_VALUE
    if Buffer7[shift] != Buffer7[shift - 1]:
        Buffer7[shift - 1] = EMPTY_VALUE
    if Buffer8[shift] != Buffer8[shift - 1]:
        Buffer8[shift - 1] = EMPTY_VALUE
    if Buffer9[shift] != Buffer9[shift - 1]:
        Buffer9[shift - 1] = EMPTY_VALUE
    if Buffer10[shift] != Buffer10[shift - 1]:
        Buffer10[shift - 1] = EMPTY_VALUE
    if Buffer11[shift] != Buffer11[shift - 1]:
        Buffer11[shift - 1] = EMPTY_VALUE
    if Buffer12[shift] != Buffer12[shift - 1]:
        Buffer12[shift - 1] = EMPTY_VALUE
    if Buffer13[shift] != Buffer13[shift - 1]:
        Buffer13[shift - 1] = EMPTY_VALUE

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


class MurreyMathMt5(_MQL5Indicator):
    name = 'murrey_math_mt5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CalculationPeriod': 64,  # The calculation period P
        'StepBack': 0,
    }

