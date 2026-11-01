"""zigzag_nk_mtf — converted from MQL5: MQL5 Indicators/ZigZag_NK_MTF/zigzag_nk_mtf.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6, 2: 6}, 'colors': {1: [255], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME', 2: 'INDICATOR_NAME'}, 'levels': [], 'description': [], 'name': 'zigzag_nk_mtf', 'source': 'MQL5 Indicators/ZigZag_NK_MTF/zigzag_nk_mtf.mq5', 'folder': 'ZigZag_NK_MTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
Init = False
min_rates_total = 0
LimitShift = 0
ZigZag_Handle = 0

def OnInit():
    global Init, LimitShift, ZigZag_Handle, min_rates_total
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('ZigZag_NK indicator chart period cannot be less than the current chart period')
        return 1
    timeratio = _idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT))
    min_rates_total = _int((ExtDepth + ExtBackstep) * timeratio)
    LimitShift = min_rates_total
    ZigZag_Handle = iCustom(None, TimeFrame, 'ZigZag_NK', ExtDepth, ExtDeviation, ExtBackstep)
    if ZigZag_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ZigZag_NK indicator')
        return 1
    SetIndexBuffer(0, HighBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(HighBuffer, True)
    SetIndexBuffer(1, LowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(LowBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ZigZag NK MTF', '(', Symbol(), StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def FindMax(Value, start, end, Array):
    for bar in range(start, end - 1, -1):
        if Array[bar] >= Value:
            return bar
    return ArrayMaximum(Array, end, start - end)

def FindMin(Value, start, end, Array):
    for bar in range(start, end - 1, -1):
        if Array[bar] <= Value:
            return bar
    return ArrayMinimum(Array, end, start - end)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(ZigZag_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    UpZigZag = Arr(1, 0.0, dyn=False)
    DnZigZag = Arr(1, 0.0, dyn=False)
    limit = 0
    bar = 0
    ZigZagTime = Arr(1, 0, dyn=False)
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
        if CopyTime(None, TimeFrame, _DT(time[bar]), 1, ZigZagTime) <= 0:
            return 0
        if time[bar + 1] < ZigZagTime[0] and time[bar] >= ZigZagTime[0]:
            if CopyBuffer(ZigZag_Handle, 1, _DT(time[bar]), 1, UpZigZag) <= 0:
                return 0
            if CopyBuffer(ZigZag_Handle, 0, _DT(time[bar]), 1, DnZigZag) <= 0:
                return 0
            if UpZigZag[0] != EMPTY_VALUE and UpZigZag[0]:
                maxbar = FindMax(UpZigZag[0], bar, 0, high)
                HighBuffer[maxbar] = UpZigZag[0]
            if DnZigZag[0] != EMPTY_VALUE and DnZigZag[0]:
                minbar = FindMin(DnZigZag[0], bar, 0, low)
                LowBuffer[minbar] = DnZigZag[0]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigzagNkMtf(_MQL5Indicator):
    name = 'zigzag_nk_mtf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
    }

