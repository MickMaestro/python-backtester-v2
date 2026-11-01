"""ac_htf — converted from MQL5: MQL5 Indicators/AC_HTF/ac_htf.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 65280, 8721863, 255, 8421376]}, 'widths': {1: 5}, 'styles': {1: 0}, 'labels': {1: 'AC HTF'}, 'levels': [], 'description': [], 'name': 'ac_htf', 'source': 'MQL5 Indicators/AC_HTF/ac_htf.mq5', 'folder': 'AC_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'repeat display of information in the empty bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
ReDraw = _input('ReDraw', True)  # repeat display of information in the empty bars
Init = False
min_rates_total = 0
AC_Handle = 0
ACBuffer = Arr(0, 0.0)
ColorACBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global AC_Handle, Init, min_rates_total
    min_rates_total = 3
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Accelerator Oscillator indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    AC_Handle = iAC(Symbol(), TimeFrame)
    if AC_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Accelerator Oscillator indicator')
        Init = False
        return INIT_FAILED
    SetIndexBuffer(0, ACBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, ' Accelerator Oscillator  HTF')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ACBuffer, True)
    SetIndexBuffer(1, ColorACBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorACBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, ' Accelerator Oscillator HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    if BarsCalculated(AC_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    AC = Arr(2, 0.0, dyn=False)
    ACTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ACBuffer[bar] = EMPTY_VALUE
        ColorACBuffer[bar] = 0.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, ACTime) <= 0:
            return 0
        if time[bar] >= ACTime[0] and time[bar + 1] < ACTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(AC_Handle, 0, _DT(time[bar]), 2, AC) <= 0:
                return 0
            ACBuffer[bar] = AC[1]
            if ACBuffer[bar] > 0:
                if AC[1] > AC[0]:
                    ColorACBuffer[bar] = 1.0
                if AC[1] < AC[0]:
                    ColorACBuffer[bar] = 2.0
            if ACBuffer[bar] < 0:
                if AC[1] < AC[0]:
                    ColorACBuffer[bar] = 3.0
                if AC[1] > AC[0]:
                    ColorACBuffer[bar] = 4.0
        if ReDraw:
            if ACBuffer[bar + 1] != EMPTY_VALUE and ACBuffer[bar] == EMPTY_VALUE:
                ACBuffer[bar] = ACBuffer[bar + 1]
                ColorACBuffer[bar] = ColorACBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AcHtf(_MQL5Indicator):
    name = 'ac_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'ReDraw': True,  # repeat display of information in the empty bars
    }

