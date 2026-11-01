"""gator_htf — converted from MQL5: MQL5 Indicators/Gator_HTF/gator_htf.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [32768, 255], 2: [32768, 255]}, 'widths': {1: 5, 2: 5}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Gator Upper HTF', 2: 'Gator Lower HTF'}, 'levels': [], 'description': [], 'name': 'gator_htf', 'source': 'MQL5 Indicators/Gator_HTF/gator_htf.mq5', 'folder': 'Gator_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'JawsPeriod', 'py': 'JawsPeriod', 'param': 'JawsPeriod', 'type': 'int', 'default': 13, 'label': 'Jaws period', 'sinput': False}, {'mql': 'JawsShift', 'py': 'JawsShift', 'param': 'JawsShift', 'type': 'int', 'default': 8, 'label': 'Jaws shift', 'sinput': False}, {'mql': 'TeethPeriod', 'py': 'TeethPeriod', 'param': 'TeethPeriod', 'type': 'int', 'default': 8, 'label': 'Teeth period', 'sinput': False}, {'mql': 'TeethShift', 'py': 'TeethShift', 'param': 'TeethShift', 'type': 'int', 'default': 5, 'label': 'Teeth shift', 'sinput': False}, {'mql': 'LipsPeriod', 'py': 'LipsPeriod', 'param': 'LipsPeriod', 'type': 'int', 'default': 5, 'label': 'Lips period', 'sinput': False}, {'mql': 'LipsShift', 'py': 'LipsShift', 'param': 'LipsShift', 'type': 'int', 'default': 3, 'label': 'Lips shift', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 2, 'label': 'Moving average method', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 5, 'label': 'Applied price', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Repeat display of information in the empty bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
JawsPeriod = _input('JawsPeriod', 13)  # Jaws period
JawsShift = _input('JawsShift', 8)  # Jaws shift
TeethPeriod = _input('TeethPeriod', 8)  # Teeth period
TeethShift = _input('TeethShift', 5)  # Teeth shift
LipsPeriod = _input('LipsPeriod', 5)  # Lips period
LipsShift = _input('LipsShift', 3)  # Lips shift
MAMethod = _input('MAMethod', MODE_SMMA)  # Moving average method
AppliedPrice = _input('AppliedPrice', PRICE_MEDIAN)  # Applied price
ReDraw = _input('ReDraw', True)  # Repeat display of information in the empty bars
Init = False
perratio = 0.0
min_rates_total = 0
Gator_Handle = 0
UpperBuffer = Arr(0, 0.0)
ColorUpBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
ColorLoBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Gator_Handle, Init, min_rates_total, perratio
    perratio = _idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT))
    min_rates_total = _int(perratio * (MathMax(MathMax(JawsPeriod, TeethPeriod), LipsPeriod) + 3))
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Gator indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    Gator_Handle = iCustom(Symbol(), TimeFrame, 'GatorCalc', JawsPeriod, JawsShift, TeethPeriod, TeethShift, LipsPeriod, LipsShift, MAMethod, AppliedPrice, -TeethShift, -LipsShift)
    if Gator_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Gator indicator')
        Init = False
        return INIT_FAILED
    if not CheckForInput():
        Print('Indicator input parameters are incorrect. The indicator will not work!')
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, _int(perratio * TeethShift))
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(1, ColorUpBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorUpBuffer, True)
    SetIndexBuffer(2, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, _int(perratio * LipsShift))
    ArraySetAsSeries(LowerBuffer, True)
    SetIndexBuffer(3, ColorLoBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorLoBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Gator HTF( ', GetStringTimeframe(TimeFrame) + ',' + _str(JawsPeriod) + ',' + _str(TeethPeriod), ',', _str(LipsPeriod), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    if BarsCalculated(Gator_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    Upper = Arr(1, 0.0, dyn=False)
    Lower = Arr(1, 0.0, dyn=False)
    UpTrend = Arr(1, 0.0, dyn=False)
    LoTrend = Arr(1, 0.0, dyn=False)
    GatorTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpperBuffer[bar] = EMPTY_VALUE
        LowerBuffer[bar] = EMPTY_VALUE
        ColorUpBuffer[bar] = -1.0
        ColorLoBuffer[bar] = -1.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, GatorTime) <= 0:
            return 0
        if time[bar] >= GatorTime[0] and time[bar + 1] < GatorTime[0]:
            _s_OnCalculate_LastCountBar = bar + _int(perratio * MathMax(MathMax(JawsPeriod, TeethPeriod), LipsPeriod)) + 1
            if CopyBuffer(Gator_Handle, 0, _DT(time[bar]), 1, Upper) <= 0:
                return 0
            if CopyBuffer(Gator_Handle, 1, _DT(time[bar]), 1, UpTrend) <= 0:
                return 0
            if CopyBuffer(Gator_Handle, 2, _DT(time[bar]), 1, Lower) <= 0:
                return 0
            if CopyBuffer(Gator_Handle, 3, _DT(time[bar]), 1, LoTrend) <= 0:
                return 0
            UpperBuffer[bar] = Upper[0]
            LowerBuffer[bar] = Lower[0]
            ColorUpBuffer[bar] = UpTrend[0]
            ColorLoBuffer[bar] = LoTrend[0]
        if ReDraw:
            if ColorUpBuffer[bar + 1] != -1 and ColorUpBuffer[bar] == -1:
                UpperBuffer[bar] = UpperBuffer[bar + 1]
                ColorUpBuffer[bar] = ColorUpBuffer[bar + 1]
                LowerBuffer[bar] = LowerBuffer[bar + 1]
                ColorLoBuffer[bar] = ColorLoBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def CheckForInput():
    if JawsPeriod <= TeethPeriod or TeethPeriod <= LipsPeriod:
        return False
    if JawsShift <= TeethShift or TeethShift <= LipsShift:
        return False
    if JawsPeriod <= JawsShift:
        return False
    if TeethPeriod <= TeethShift:
        return False
    if LipsPeriod <= LipsShift:
        return False
    return True

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GatorHtf(_MQL5Indicator):
    name = 'gator_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'JawsPeriod': 13,  # Jaws period
        'JawsShift': 8,  # Jaws shift
        'TeethPeriod': 8,  # Teeth period
        'TeethShift': 5,  # Teeth shift
        'LipsPeriod': 5,  # Lips period
        'LipsShift': 3,  # Lips shift
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Moving average method
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Applied price
        'ReDraw': True,  # Repeat display of information in the empty bars
    }

