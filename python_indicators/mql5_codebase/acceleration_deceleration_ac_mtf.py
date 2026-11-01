"""Acceleration_Deceleration_AC_MTF — converted from MQL5: MQL5 Indicators/Acceleration_Deceleration_AC_MTF/Acceleration_Deceleration_AC_MTF.mq5

Multi timeframes Bill Williams Accelerator Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 8}, 'styles': {1: 0}, 'labels': {1: 'MTF AC'}, 'levels': [], 'description': ['Multi timeframes Bill Williams Accelerator Oscillator'], 'name': 'Acceleration_Deceleration_AC_MTF', 'source': 'MQL5 Indicators/Acceleration_Deceleration_AC_MTF/Acceleration_Deceleration_AC_MTF.mq5', 'folder': 'Acceleration_Deceleration_AC_MTF', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 5, 'label': 'AO Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 34, 'label': 'AO Slow MA period', 'sinput': False}, {'mql': 'InpPeriodACMA', 'py': 'InpPeriodACMA', 'param': 'InpPeriodACMA', 'type': 'uint', 'default': 5, 'label': 'AC MA period', 'sinput': False}, {'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 0, 'label': 'AC timeframe', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 5)  # AO Fast MA period
InpPeriodSlow = _input('InpPeriodSlow', 34)  # AO Slow MA period
InpPeriodACMA = _input('InpPeriodACMA', 5)  # AC MA period
InpTimeframe = _input('InpTimeframe', 0)  # AC timeframe
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
BufferADAC = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferADACtmp = Arr(0, 0.0)
BufferColorsTmp = Arr(0, 0.0)
BufferMedian = Arr(0, 0.0)
BufferAC = Arr(0, 0.0)
BufferAvgAC = Arr(0, 0.0)
BufferMAH = Arr(0, 0.0)
BufferMAL = Arr(0, 0.0)
timeframe1 = 0
period_fast = 0
period_slow = 0
period_acma = 0
handle_maH = 0
handle_maL = 0

def OnInit():
    global handle_maH, handle_maL, period_acma, period_fast, period_slow, timeframe1
    EventSetTimer(90)
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = (1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_acma = (1 if (InpPeriodACMA < 1) else InpPeriodACMA)
    timeframe1 = (InpTimeframe if (InpTimeframe > Period()) else Period())
    SetIndexBuffer(0, BufferADAC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferADACtmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferColorsTmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMedian, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferAC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferAvgAC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferMAH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMAL, INDICATOR_CALCULATIONS)
    label = TimeframeToString(timeframe1) + ' AC(' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_acma) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframe1) + ' AC')
    ArraySetAsSeries(BufferADAC, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferADACtmp, True)
    ArraySetAsSeries(BufferColorsTmp, True)
    ArraySetAsSeries(BufferMedian, True)
    ArraySetAsSeries(BufferAC, True)
    ArraySetAsSeries(BufferAvgAC, True)
    ArraySetAsSeries(BufferMAH, True)
    ArraySetAsSeries(BufferMAL, True)
    ResetLastError()
    handle_maH = iMA(None, timeframe1, 1, 0, MODE_SMA, PRICE_HIGH)
    if handle_maH == INVALID_HANDLE:
        Print(91, ': The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maL = iMA(None, timeframe1, 1, 0, MODE_SMA, PRICE_LOW)
    if handle_maL == INVALID_HANDLE:
        Print(97, ': The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    Time("", timeframe1, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferADAC, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferADACtmp, 0)
        ArrayInitialize(BufferColorsTmp, 2)
        ArrayInitialize(BufferMedian, 0)
        ArrayInitialize(BufferAC, 0)
        ArrayInitialize(BufferAvgAC, 0)
        ArrayInitialize(BufferMAH, 0)
        ArrayInitialize(BufferMAL, 0)
    if Time("", timeframe1, 1) == 0:
        return 0
    bars = (rates_total if (timeframe1 == Period()) else Bars(None, timeframe1))
    count = (fmin(bars, rates_total) if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_maH, 0, 0, count, BufferMAH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maL, 0, 0, count, BufferMAL)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMedian[i] = (BufferMAH[i] + BufferMAL[i]) / 2.0
        avg_median_fast = GetSMA(rates_total, i, period_fast, BufferMedian)
        avg_median_slow = GetSMA(rates_total, i, period_slow, BufferMedian)
        BufferAC[i] = avg_median_fast - avg_median_slow
        BufferAvgAC[i] = GetSMA(rates_total, i, period_acma, BufferAC)
        BufferADACtmp[i] = BufferAC[i] - BufferAvgAC[i]
    for i in range(limit, 0 - 1, -1):
        BufferColorsTmp[i] = (0 if (BufferADACtmp[i] > BufferADACtmp[i + 1]) else 1 if (BufferADACtmp[i] < BufferADACtmp[i + 1]) else 2)
    for i in range(limit, 0 - 1, -1):
        DataConversion(rates_total, "", timeframe1, i, BufferADACtmp, BufferADAC, InpDrawMode)
        DataConversion(rates_total, "", timeframe1, i, BufferColorsTmp, BufferColors, InpDrawMode)
    return rates_total

def OnTimer():
    Time("", timeframe1, 1)

def DataConversion(rates_total, symbol_name, timeframe_src, shift, buffer_src, buffer_dest, mode=DRAW_MODE_STEPS):
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

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def Close(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyClose(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result += (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AccelerationDecelerationACMTF(_MQL5Indicator):
    name = 'Acceleration_Deceleration_AC_MTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 5,  # AO Fast MA period
        'InpPeriodSlow': 34,  # AO Slow MA period
        'InpPeriodACMA': 5,  # AC MA period
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # AC timeframe
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
    }

