"""Dynamic_Trend_MTF — converted from MQL5: MQL5 Indicators/Dynamic_Trend_MTF/Dynamic_Trend_MTF.mq5

Multi timeframe Dynamic Trend indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 24, 'indicator_plots': 9}, 'types': {1: 8, 2: 5, 3: 5, 4: 8, 5: 5, 6: 5, 7: 8, 8: 5, 9: 5}, 'colors': {1: [16711680, 255, 11119017], 2: [16711680], 3: [255], 4: [16760576, 42495, 11119017], 5: [16760576], 6: [42495], 7: [2330219, 55295, 11119017], 8: [2330219], 9: [55295]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 2, 5: 1, 6: 1, 7: 3, 8: 1, 9: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'labels': {1: 'DT 1', 2: 'Up 1', 3: 'Down 1', 4: 'DT 2', 5: 'Up 2', 6: 'Down 2', 7: 'DT 3', 8: 'Up 3', 9: 'Down 3'}, 'levels': [], 'description': ['Multi timeframe Dynamic Trend indicator'], 'name': 'Dynamic_Trend_MTF', 'source': 'MQL5 Indicators/Dynamic_Trend_MTF/Dynamic_Trend_MTF.mq5', 'folder': 'Dynamic_Trend_MTF', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpPercent', 'py': 'InpPercent', 'param': 'InpPercent', 'type': 'uint', 'default': 10, 'label': 'Percent', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}, {'mql': 'InpTimeframe1', 'py': 'InpTimeframe1', 'param': 'InpTimeframe1', 'type': 'int', 'default': 16385, 'label': 'First DT timeframe', 'sinput': False}, {'mql': 'InpTimeframe2', 'py': 'InpTimeframe2', 'param': 'InpTimeframe2', 'type': 'int', 'default': 16388, 'label': 'Second DT timeframe', 'sinput': False}, {'mql': 'InpTimeframe3', 'py': 'InpTimeframe3', 'param': 'InpTimeframe3', 'type': 'int', 'default': 16408, 'label': 'Third DT timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpPercent = _input('InpPercent', 10)  # Percent
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
InpTimeframe1 = _input('InpTimeframe1', PERIOD_H1)  # First DT timeframe
InpTimeframe2 = _input('InpTimeframe2', PERIOD_H4)  # Second DT timeframe
InpTimeframe3 = _input('InpTimeframe3', PERIOD_D1)  # Third DT timeframe
BufferLine1 = Arr(0, 0.0)
BufferColors1 = Arr(0, 0.0)
BufferUP1 = Arr(0, 0.0)
BufferDN1 = Arr(0, 0.0)
BufferLine2 = Arr(0, 0.0)
BufferColors2 = Arr(0, 0.0)
BufferUP2 = Arr(0, 0.0)
BufferDN2 = Arr(0, 0.0)
BufferLine3 = Arr(0, 0.0)
BufferColors3 = Arr(0, 0.0)
BufferUP3 = Arr(0, 0.0)
BufferDN3 = Arr(0, 0.0)
BufferLine1tmp = Arr(0, 0.0)
BufferLine2tmp = Arr(0, 0.0)
BufferLine3tmp = Arr(0, 0.0)
BufferColors1tmp = Arr(0, 0.0)
BufferColors2tmp = Arr(0, 0.0)
BufferColors3tmp = Arr(0, 0.0)
BufferUP1tmp = Arr(0, 0.0)
BufferDN1tmp = Arr(0, 0.0)
BufferUP2tmp = Arr(0, 0.0)
BufferDN2tmp = Arr(0, 0.0)
BufferUP3tmp = Arr(0, 0.0)
BufferDN3tmp = Arr(0, 0.0)
timeframe1 = 0
timeframe2 = 0
timeframe3 = 0
percent = 0
period_dt = 0

def OnInit():
    global percent, period_dt, timeframe1, timeframe2, timeframe3
    EventSetTimer(90)
    percent = _int(InpPercent)
    period_dt = (1 if (InpPeriod < 1) else InpPeriod)
    timeframe1 = (InpTimeframe1 if (InpTimeframe1 > Period()) else Period())
    timeframe2 = (InpTimeframe2 if (InpTimeframe2 > Period()) else Period())
    timeframe3 = (InpTimeframe3 if (InpTimeframe3 > Period()) else Period())
    SetIndexBuffer(0, BufferLine1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors1, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferUP1, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDN1, INDICATOR_DATA)
    SetIndexBuffer(4, BufferLine2, INDICATOR_DATA)
    SetIndexBuffer(5, BufferColors2, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, BufferUP2, INDICATOR_DATA)
    SetIndexBuffer(7, BufferDN2, INDICATOR_DATA)
    SetIndexBuffer(8, BufferLine3, INDICATOR_DATA)
    SetIndexBuffer(9, BufferColors3, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(10, BufferUP3, INDICATOR_DATA)
    SetIndexBuffer(11, BufferDN3, INDICATOR_DATA)
    SetIndexBuffer(12, BufferLine1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferLine2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferLine3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, BufferUP1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, BufferDN1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, BufferUP2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(18, BufferDN2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(19, BufferUP3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(20, BufferDN3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(21, BufferColors1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(22, BufferColors2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(23, BufferColors3tmp, INDICATOR_CALCULATIONS)
    if timeframe1 == Period():
        PlotIndexSetInteger(1, PLOT_ARROW, 233)
        PlotIndexSetInteger(2, PLOT_ARROW, 234)
    else:
        PlotIndexSetInteger(1, PLOT_ARROW, 159)
        PlotIndexSetInteger(2, PLOT_ARROW, 159)
    if timeframe2 == Period():
        PlotIndexSetInteger(4, PLOT_ARROW, 233)
        PlotIndexSetInteger(5, PLOT_ARROW, 234)
    else:
        PlotIndexSetInteger(4, PLOT_ARROW, 159)
        PlotIndexSetInteger(5, PLOT_ARROW, 159)
    if timeframe3 == Period():
        PlotIndexSetInteger(7, PLOT_ARROW, 233)
        PlotIndexSetInteger(8, PLOT_ARROW, 234)
    else:
        PlotIndexSetInteger(7, PLOT_ARROW, 159)
        PlotIndexSetInteger(8, PLOT_ARROW, 159)
    label = TimeframeToString(timeframe1) + ',' + TimeframeToString(timeframe2) + ',' + TimeframeToString(timeframe3) + ' Dynamic Trend (' + _str(period_dt) + ',' + _str(percent) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframe1) + ' DT(' + _str(period_dt) + ',' + _str(percent) + ')')
    PlotIndexSetString(1, PLOT_LABEL, TimeframeToString(timeframe1) + ' Up(' + _str(period_dt) + ',' + _str(percent) + ')')
    PlotIndexSetString(2, PLOT_LABEL, TimeframeToString(timeframe1) + ' Down(' + _str(period_dt) + ',' + _str(percent) + ')')
    PlotIndexSetString(3, PLOT_LABEL, TimeframeToString(timeframe2) + ' DT(' + _str(period_dt) + ',' + _str(percent) + ')')
    PlotIndexSetString(4, PLOT_LABEL, TimeframeToString(timeframe2) + ' Up(' + _str(period_dt) + ',' + _str(percent) + ')')
    PlotIndexSetString(5, PLOT_LABEL, TimeframeToString(timeframe2) + ' Down(' + _str(period_dt) + ',' + _str(percent) + ')')
    PlotIndexSetString(6, PLOT_LABEL, TimeframeToString(timeframe3) + ' DT(' + _str(period_dt) + ',' + _str(percent) + ')')
    PlotIndexSetString(7, PLOT_LABEL, TimeframeToString(timeframe3) + ' Up(' + _str(period_dt) + ',' + _str(percent) + ')')
    PlotIndexSetString(8, PLOT_LABEL, TimeframeToString(timeframe3) + ' Down(' + _str(period_dt) + ',' + _str(percent) + ')')
    ArraySetAsSeries(BufferLine1, True)
    ArraySetAsSeries(BufferColors1, True)
    ArraySetAsSeries(BufferUP1, True)
    ArraySetAsSeries(BufferDN1, True)
    ArraySetAsSeries(BufferLine2, True)
    ArraySetAsSeries(BufferColors2, True)
    ArraySetAsSeries(BufferUP2, True)
    ArraySetAsSeries(BufferDN2, True)
    ArraySetAsSeries(BufferLine3, True)
    ArraySetAsSeries(BufferColors3, True)
    ArraySetAsSeries(BufferUP3, True)
    ArraySetAsSeries(BufferDN3, True)
    ArraySetAsSeries(BufferLine1tmp, True)
    ArraySetAsSeries(BufferLine2tmp, True)
    ArraySetAsSeries(BufferLine3tmp, True)
    ArraySetAsSeries(BufferUP1tmp, True)
    ArraySetAsSeries(BufferDN1tmp, True)
    ArraySetAsSeries(BufferUP2tmp, True)
    ArraySetAsSeries(BufferDN2tmp, True)
    ArraySetAsSeries(BufferUP3tmp, True)
    ArraySetAsSeries(BufferDN3tmp, True)
    ArraySetAsSeries(BufferColors1tmp, True)
    ArraySetAsSeries(BufferColors2tmp, True)
    ArraySetAsSeries(BufferColors3tmp, True)
    Time("", timeframe1, 1)
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_dt, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 4
        ArrayInitialize(BufferLine1, 0)
        ArrayInitialize(BufferLine2, 0)
        ArrayInitialize(BufferLine3, 0)
        ArrayInitialize(BufferColors1, 2)
        ArrayInitialize(BufferColors2, 2)
        ArrayInitialize(BufferColors3, 2)
        ArrayInitialize(BufferUP1, EMPTY_VALUE)
        ArrayInitialize(BufferDN1, EMPTY_VALUE)
        ArrayInitialize(BufferUP2, EMPTY_VALUE)
        ArrayInitialize(BufferDN2, EMPTY_VALUE)
        ArrayInitialize(BufferUP3, EMPTY_VALUE)
        ArrayInitialize(BufferDN3, EMPTY_VALUE)
        ArrayInitialize(BufferLine1tmp, 0)
        ArrayInitialize(BufferLine2tmp, 0)
        ArrayInitialize(BufferLine3tmp, 0)
        ArrayInitialize(BufferUP1tmp, EMPTY_VALUE)
        ArrayInitialize(BufferDN1tmp, EMPTY_VALUE)
        ArrayInitialize(BufferUP2tmp, EMPTY_VALUE)
        ArrayInitialize(BufferDN2tmp, EMPTY_VALUE)
        ArrayInitialize(BufferUP3tmp, EMPTY_VALUE)
        ArrayInitialize(BufferDN3tmp, EMPTY_VALUE)
        ArrayInitialize(BufferColors1tmp, 2)
        ArrayInitialize(BufferColors2tmp, 2)
        ArrayInitialize(BufferColors3tmp, 2)
    for i in range(limit, 0 - 1, -1):
        DT("", timeframe1, period_dt, i, BufferLine1tmp, BufferUP1tmp, BufferDN1tmp, BufferColors1tmp)
        DT("", timeframe2, period_dt, i, BufferLine2tmp, BufferUP2tmp, BufferDN2tmp, BufferColors2tmp)
        DT("", timeframe3, period_dt, i, BufferLine3tmp, BufferUP3tmp, BufferDN3tmp, BufferColors3tmp)
    for i in range(limit, 0 - 1, -1):
        BufferColors3[i] = 2.0
        BufferColors2[i] = BufferColors3[i]
        BufferColors1[i] = BufferColors2[i]
        DataConversion(rates_total, "", timeframe1, i, BufferLine1tmp, BufferLine1, InpDrawMode)
        DataConversion(rates_total, "", timeframe1, i, BufferColors1tmp, BufferColors1, InpDrawMode)
        DataConversion(rates_total, "", timeframe1, i, BufferUP1tmp, BufferUP1, DRAW_MODE_STEPS)
        DataConversion(rates_total, "", timeframe1, i, BufferDN1tmp, BufferDN1, DRAW_MODE_STEPS)
        DataConversion(rates_total, "", timeframe2, i, BufferLine2tmp, BufferLine2, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferColors2tmp, BufferColors2, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferUP2tmp, BufferUP2, DRAW_MODE_STEPS)
        DataConversion(rates_total, "", timeframe2, i, BufferDN2tmp, BufferDN2, DRAW_MODE_STEPS)
        DataConversion(rates_total, "", timeframe3, i, BufferLine3tmp, BufferLine3, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferColors3tmp, BufferColors3, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferUP3tmp, BufferUP3, DRAW_MODE_STEPS)
        DataConversion(rates_total, "", timeframe3, i, BufferDN3tmp, BufferDN3, DRAW_MODE_STEPS)
    return rates_total

def OnTimer():
    Time("", timeframe1, 1)
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)

def DataConversion(rates_total, symbol_name, timeframe_src, shift, buffer_src, buffer_dest, mode=DRAW_MODE_STEPS):
    close = Close(symbol_name, timeframe_src, shift)
    if close == 0:
        return
    if timeframe_src == Period():
        buffer_dest[shift] = buffer_src[shift]
        return
    bar_curr = BarToCurrent(symbol_name, timeframe_src, shift)
    if bar_curr > (rates_total - 1):
        return
    bar_prev = BarToCurrent(symbol_name, timeframe_src, shift + 1)
    bar_next = (BarToCurrent(symbol_name, timeframe_src, shift - 1) if (shift > 0) else 0)
    if (bar_prev == WRONG_VALUE or bar_curr == WRONG_VALUE) or bar_next == WRONG_VALUE:
        return
    buffer_dest[bar_curr] = buffer_src[shift]
    if mode == DRAW_MODE_STEPS:
        for j in range(bar_curr, bar_next - 1, -1):
            buffer_dest[j] = buffer_dest[bar_curr]
    else:
        if bar_prev > (rates_total - 1):
            return
        for j in range(bar_prev, bar_curr - 1, -1):
            buffer_dest[j] = EquationDirect(bar_prev, buffer_dest[bar_prev], bar_curr, buffer_dest[bar_curr], j)
        if shift == 0:
            for j in range(bar_curr, 0 - 1, -1):
                buffer_dest[j] = buffer_dest[bar_curr]

def BarToCurrent(symbol_name, timeframe_src, shift, exact=False):
    time = Time(symbol_name, timeframe_src, shift)
    return (BarShift(symbol_name, Period(), time, exact) if (time != 0) else WRONG_VALUE)

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res

def Open(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyOpen(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def High(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyHigh(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def Low(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyLow(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def Close(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyClose(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

def HighestClose(symbol_name, timeframe, count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyClose(symbol_name, timeframe, start, count, array) == count) else WRONG_VALUE)

def LowestClose(symbol_name, timeframe, count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMinimum(array) + start) if (CopyClose(symbol_name, timeframe, start, count, array) == count) else WRONG_VALUE)
    return WRONG_VALUE

def DT(symbol_name, timeframe, period, shift, buffer_line, buffer_up, buffer_dn, buffer_color):
    bh = HighestClose(symbol_name, timeframe, period, shift + 1)
    bl = LowestClose(symbol_name, timeframe, period, shift + 1)
    open0 = Open(symbol_name, timeframe, shift)
    close0 = Close(symbol_name, timeframe, shift)
    close1 = Close(symbol_name, timeframe, shift + 1)
    close2 = Close(symbol_name, timeframe, shift + 2)
    close3 = Close(symbol_name, timeframe, shift + 3)
    if (((((bl == WRONG_VALUE or bh == WRONG_VALUE) or open0 == 0) or close0 == 0) or close1 == 0) or close2 == 0) or close3 == 0:
        return
    closeBH = Close(symbol_name, timeframe, bh)
    closeBL = Close(symbol_name, timeframe, bl)
    if closeBH == 0 or closeBL == 0:
        return
    buffer_color[shift] = 2.0
    if close0 < buffer_line[shift + 1]:
        buffer_line[shift] = closeBH - (percent * Point())
        buffer_color[shift] = 1.0
    else:
        buffer_line[shift] = closeBL + (percent * Point())
        buffer_color[shift] = 0.0
    buffer_dn[shift] = EMPTY_VALUE
    buffer_up[shift] = buffer_dn[shift]
    if close1 > buffer_line[shift + 1] and close2 <= buffer_line[shift + 2]:
        buffer_up[shift] = open0
    if close1 < buffer_line[shift + 1] and close2 >= buffer_line[shift + 2]:
        buffer_dn[shift] = open0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynamicTrendMTF(_MQL5Indicator):
    name = 'Dynamic_Trend_MTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpPercent': 10,  # Percent
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
        'InpTimeframe1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # First DT timeframe
        'InpTimeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Second DT timeframe
        'InpTimeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Third DT timeframe
    }

