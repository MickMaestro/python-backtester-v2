"""fine_fractals_mtf — converted from MQL5: MQL5 Indicators/Fine_Fractals_MTF/fine_fractals_mtf.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Up ', 2: 'Down '}, 'levels': [], 'description': [], 'name': 'fine_fractals_mtf', 'source': 'MQL5 Indicators/Fine_Fractals_MTF/fine_fractals_mtf.mq5', 'folder': 'Fine_Fractals_MTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'Fine', 'py': 'Fine', 'param': 'Fine', 'type': 'bool', 'default': True, 'label': 'Sensibility', 'sinput': False}, {'mql': 'FlatShift', 'py': 'FlatShift', 'param': 'FlatShift', 'type': 'bool', 'default': True, 'label': 'Shift', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'int', 'default': 164, 'label': 'Upper fractal symbol code', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'int', 'default': 164, 'label': 'Lower fractal symbol code', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
Fine = _input('Fine', True)  # Sensibility
FlatShift = _input('FlatShift', True)  # Shift
UpLable = _input('UpLable', 164)  # Upper fractal symbol code
DnLable = _input('DnLable', 164)  # Lower fractal symbol code
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
Init = False
min_rates_total = 0
LimitShift = 0
FRA_Handle = 0

def OnInit():
    global FRA_Handle, Init, LimitShift, min_rates_total
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Fine_Fractals indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    timeratio = _idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT))
    min_rates_total = _int(5 * timeratio)
    LimitShift = _int(4 * timeratio)
    FRA_Handle = iCustom(None, TimeFrame, 'Fine_Fractals', Fine, FlatShift)
    if FRA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Fine_Fractals indicator')
        return INIT_FAILED
    SetIndexBuffer(0, HighBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_ARROW, UpLable)
    ArraySetAsSeries(HighBuffer, True)
    SetIndexBuffer(1, LowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_ARROW, DnLable)
    ArraySetAsSeries(LowBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Fine_Fractals MTF', '(', Symbol(), StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def FindMax(Velue, start, end, Array):
    for bar in range(start, end - 1, -1):
        if Array[bar] >= Velue:
            return bar
    return ArrayMaximum(Array, end, start - end)

def FindMin(Velue, start, end, Array):
    for bar in range(start, end - 1, -1):
        if Array[bar] <= Velue:
            return bar
    return ArrayMinimum(Array, end, start - end)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or (not Init):
        return 0
    if BarsCalculated(FRA_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    UpFrac = Arr(1, 0.0, dyn=False)
    DnFrac = Arr(1, 0.0, dyn=False)
    limit = 0
    bar = 0
    FracTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = LimitShift + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        LowBuffer[bar] = 0.0
        HighBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if CopyTime(None, TimeFrame, _DT(time[bar]), 1, FracTime) <= 0:
            return 0
        if time[bar] >= FracTime[0] and time[bar + 1] < FracTime[0]:
            if CopyBuffer(FRA_Handle, 0, _DT(time[bar]), 1, UpFrac) <= 0:
                return 0
            if CopyBuffer(FRA_Handle, 1, _DT(time[bar]), 1, DnFrac) <= 0:
                return 0
            if UpFrac[0] != EMPTY_VALUE and UpFrac[0]:
                HighBuffer[FindMax(UpFrac[0], bar, 0, high)] = UpFrac[0]
            if DnFrac[0] != EMPTY_VALUE and DnFrac[0]:
                LowBuffer[FindMin(DnFrac[0], bar, 0, low)] = DnFrac[0]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FineFractalsMtf(_MQL5Indicator):
    name = 'fine_fractals_mtf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'Fine': True,  # Sensibility
        'FlatShift': True,  # Shift
        'UpLable': 164,  # Upper fractal symbol code
        'DnLable': 164,  # Lower fractal symbol code
    }

