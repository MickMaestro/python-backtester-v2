"""murrey_math_fixperiod — converted from MQL5: MQL5 Indicators/Murrey Math FixPeriod/murrey_math_fixperiod.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 13}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1}, 'colors': {1: [9109504], 2: [13828244], 3: [16776960], 4: [4163021], 5: [255], 6: [65280], 7: [11119017], 8: [65280], 9: [255], 10: [4163021], 11: [16776960], 12: [13828244], 13: [9109504]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0}, 'labels': {1: 'Pivot, reverse [-2/8]', 2: 'Weak, stall and reverse [-1/8]', 3: 'Ultimate resistance [0/8]', 4: 'Weak, stall and reverse [1/8]', 5: 'Вращение, разворот [2/8]', 6: 'Bottom of Trading Range [3/8]', 7: 'Major Support/Resistance Pivotal Point [4/8]', 8: 'Top of Trading Range [5/8]', 9: 'Pivot, Reverse [6/8]', 10: 'Weak, Stall and Reverse - [7/8]', 11: 'Ultimate Resistance [8/8]', 12: 'Weak, stall and reverse [+1/8]', 13: 'Pivot, reverse [+2/8]'}, 'levels': [], 'description': [], 'name': 'murrey_math_fixperiod', 'source': 'MQL5 Indicators/Murrey Math FixPeriod/murrey_math_fixperiod.mq5', 'folder': 'Murrey Math FixPeriod', 'inputs': [{'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16408, 'label': 'Indicator timeframe for lines calculation', 'sinput': False}, {'mql': 'CalculationPeriod', 'py': 'CalculationPeriod', 'param': 'CalculationPeriod', 'type': 'int', 'default': 64, 'label': 'P calculation period', 'sinput': False}, {'mql': 'StepBack', 'py': 'StepBack', 'param': 'StepBack', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Timeframe = _input('Timeframe', PERIOD_D1)  # Indicator timeframe for lines calculation
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
Init = False
ShiftBarsForward = 0
Murrey_Handle = 0
min_rates_total = 0
Murrey_Calculated = 0

def BufferRecount(Number, Buffer, Time, bar):
    Murrey = Arr(2, 0.0, dyn=False)
    if CopyBuffer(Murrey_Handle, Number, _DT(Time), 2, Murrey) <= 0:
        return (0 != 0)
    if Murrey[1] != EMPTY_VALUE:
        Buffer[bar] = Murrey[1]
    else:
        Buffer[bar] = Murrey[0]
    return True

def OnInit():
    global Init, Murrey_Calculated, Murrey_Handle, min_rates_total
    Murrey_Calculated = CalculationPeriod + StepBack + 3
    min_rates_total = _idiv(Murrey_Calculated * PeriodSeconds(Timeframe), PeriodSeconds(PERIOD_CURRENT))
    Init = True
    if Timeframe < Period() and Timeframe != PERIOD_CURRENT:
        Print('Murrey_Math indicator chart period cannot be less than the current chart period')
        Init = False
        return
    Murrey_Handle = iCustom(None, Timeframe, 'Murrey_Math', CalculationPeriod, StepBack)
    if Murrey_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Murrey_Math indicator')
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
    ArraySetAsSeries(Buffer1, True)
    ArraySetAsSeries(Buffer2, True)
    ArraySetAsSeries(Buffer3, True)
    ArraySetAsSeries(Buffer4, True)
    ArraySetAsSeries(Buffer5, True)
    ArraySetAsSeries(Buffer6, True)
    ArraySetAsSeries(Buffer7, True)
    ArraySetAsSeries(Buffer8, True)
    ArraySetAsSeries(Buffer9, True)
    ArraySetAsSeries(Buffer10, True)
    ArraySetAsSeries(Buffer11, True)
    ArraySetAsSeries(Buffer12, True)
    ArraySetAsSeries(Buffer13, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Murrey_Math_MT5(' + EnumToString(Timeframe, 'ENUM_TIMEFRAMES') + ', ' + _str(CalculationPeriod) + ', ' + _str(StepBack) + ')')
    for i in range(0, 13):
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Murrey_Handle) < Murrey_Calculated or rates_total < min_rates_total) or (not Init):
        return 0
    if prev_calculated == rates_total:
        return rates_total
    limit = 0
    bar1 = 0
    Time = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
        bar = limit
        while bar <= (limit - min_rates_total):
            Buffer1[bar] = EMPTY_VALUE
            Buffer2[bar] = EMPTY_VALUE
            Buffer3[bar] = EMPTY_VALUE
            Buffer4[bar] = EMPTY_VALUE
            Buffer5[bar] = EMPTY_VALUE
            Buffer6[bar] = EMPTY_VALUE
            Buffer7[bar] = EMPTY_VALUE
            Buffer8[bar] = EMPTY_VALUE
            Buffer9[bar] = EMPTY_VALUE
            Buffer10[bar] = EMPTY_VALUE
            Buffer11[bar] = EMPTY_VALUE
            Buffer12[bar] = EMPTY_VALUE
            Buffer13[bar] = EMPTY_VALUE
            bar -= 1
        limit -= min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    for bar in range(limit, 0 - 1, -1):
        Time = time[bar]
        if not BufferRecount(0, Buffer1, Time, bar):
            return 0
        if not BufferRecount(1, Buffer2, Time, bar):
            return 0
        if not BufferRecount(2, Buffer3, Time, bar):
            return 0
        if not BufferRecount(3, Buffer4, Time, bar):
            return 0
        if not BufferRecount(4, Buffer5, Time, bar):
            return 0
        if not BufferRecount(5, Buffer6, Time, bar):
            return 0
        if not BufferRecount(6, Buffer7, Time, bar):
            return 0
        if not BufferRecount(7, Buffer8, Time, bar):
            return 0
        if not BufferRecount(8, Buffer9, Time, bar):
            return 0
        if not BufferRecount(9, Buffer10, Time, bar):
            return 0
        if not BufferRecount(10, Buffer11, Time, bar):
            return 0
        if not BufferRecount(11, Buffer12, Time, bar):
            return 0
        if not BufferRecount(12, Buffer13, Time, bar):
            return 0
        bar1 = bar + 1
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
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MurreyMathFixperiod(_MQL5Indicator):
    name = 'murrey_math_fixperiod'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Indicator timeframe for lines calculation
        'CalculationPeriod': 64,  # P calculation period
        'StepBack': 0,
    }

