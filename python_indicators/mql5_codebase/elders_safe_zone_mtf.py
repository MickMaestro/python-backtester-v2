"""Elders_Safe_Zone_MTF — converted from MQL5: MQL5 Indicators/Elders_Safe_Zone_MTF/Elders_Safe_Zone_MTF.mq5

Multi timeframe Elder's Safe Zone indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [32768], 3: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'ESZ 1', 2: 'ESZ 2', 3: 'ESZ 3'}, 'levels': [], 'description': ["Multi timeframe Elder's Safe Zone indicator"], 'name': 'Elders_Safe_Zone_MTF', 'source': 'MQL5 Indicators/Elders_Safe_Zone_MTF/Elders_Safe_Zone_MTF.mq5', 'folder': 'Elders_Safe_Zone_MTF', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'ESZ Period', 'sinput': False}, {'mql': 'InpStopFactor', 'py': 'InpStopFactor', 'param': 'InpStopFactor', 'type': 'uint', 'default': 3, 'label': 'Stop factor', 'sinput': False}, {'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'uint', 'default': 13, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}, {'mql': 'InpTimeframe1', 'py': 'InpTimeframe1', 'param': 'InpTimeframe1', 'type': 'int', 'default': 16385, 'label': 'First ESZ timeframe', 'sinput': False}, {'mql': 'InpTimeframe2', 'py': 'InpTimeframe2', 'param': 'InpTimeframe2', 'type': 'int', 'default': 16388, 'label': 'Second ESZ timeframe', 'sinput': False}, {'mql': 'InpTimeframe3', 'py': 'InpTimeframe3', 'param': 'InpTimeframe3', 'type': 'int', 'default': 16408, 'label': 'Third ESZ timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # ESZ Period
InpStopFactor = _input('InpStopFactor', 3)  # Stop factor
InpPeriodEMA = _input('InpPeriodEMA', 13)  # EMA period
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
InpTimeframe1 = _input('InpTimeframe1', PERIOD_H1)  # First ESZ timeframe
InpTimeframe2 = _input('InpTimeframe2', PERIOD_H4)  # Second ESZ timeframe
InpTimeframe3 = _input('InpTimeframe3', PERIOD_D1)  # Third ESZ timeframe
BufferESZ1 = Arr(0, 0.0)
BufferESZ2 = Arr(0, 0.0)
BufferESZ3 = Arr(0, 0.0)
BufferESZ1tmp = Arr(0, 0.0)
BufferESZ2tmp = Arr(0, 0.0)
BufferESZ3tmp = Arr(0, 0.0)
BufferEMA1 = Arr(0, 0.0)
BufferEMA2 = Arr(0, 0.0)
BufferEMA3 = Arr(0, 0.0)
timeframe1 = 0
timeframe2 = 0
timeframe3 = 0
period_esz = 0
period_ema = 0
stop_factor = 0
handle_ma1 = 0
handle_ma2 = 0
handle_ma3 = 0

def OnInit():
    global handle_ma1, handle_ma2, handle_ma3, period_ema, period_esz, stop_factor, timeframe1, timeframe2, timeframe3
    EventSetTimer(90)
    period_esz = (1 if (InpPeriod < 1) else InpPeriod)
    period_ema = (1 if (InpPeriodEMA < 1) else InpPeriodEMA)
    stop_factor = (1 if (InpStopFactor < 1) else InpStopFactor)
    timeframe1 = (InpTimeframe1 if (InpTimeframe1 > Period()) else Period())
    timeframe2 = (InpTimeframe2 if (InpTimeframe2 > Period()) else Period())
    timeframe3 = (InpTimeframe3 if (InpTimeframe3 > Period()) else Period())
    SetIndexBuffer(0, BufferESZ1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferESZ2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferESZ3, INDICATOR_DATA)
    SetIndexBuffer(3, BufferESZ1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferESZ2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferESZ3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferEMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferEMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferEMA3, INDICATOR_CALCULATIONS)
    label = TimeframeToString(timeframe1) + ',' + TimeframeToString(timeframe2) + ',' + TimeframeToString(timeframe3) + " Elder's Safe Zone (" + _str(period_esz) + ',' + _str(stop_factor) + ',' + _str(period_ema) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframe1) + ' ESZ(' + _str(period_esz) + ',' + _str(stop_factor) + ',' + _str(period_ema) + ')')
    PlotIndexSetString(1, PLOT_LABEL, TimeframeToString(timeframe2) + ' ESZ(' + _str(period_esz) + ',' + _str(stop_factor) + ',' + _str(period_ema) + ')')
    PlotIndexSetString(2, PLOT_LABEL, TimeframeToString(timeframe3) + ' ESZ(' + _str(period_esz) + ',' + _str(stop_factor) + ',' + _str(period_ema) + ')')
    ArraySetAsSeries(BufferESZ1, True)
    ArraySetAsSeries(BufferESZ2, True)
    ArraySetAsSeries(BufferESZ3, True)
    ArraySetAsSeries(BufferESZ1tmp, True)
    ArraySetAsSeries(BufferESZ2tmp, True)
    ArraySetAsSeries(BufferESZ3tmp, True)
    ArraySetAsSeries(BufferEMA1, True)
    ArraySetAsSeries(BufferEMA2, True)
    ArraySetAsSeries(BufferEMA3, True)
    ResetLastError()
    handle_ma1 = iMA(None, timeframe1, period_ema, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma1 == INVALID_HANDLE:
        Print(112, ': The iMA(', _str(period_ema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, timeframe2, period_ema, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma2 == INVALID_HANDLE:
        Print(118, ': The iMA(', _str(period_ema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma3 = iMA(None, timeframe3, period_ema, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma3 == INVALID_HANDLE:
        Print(124, ': The iMA(', _str(period_ema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    Time("", timeframe1, 1)
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_esz, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_esz - 3
        ArrayInitialize(BufferESZ1, EMPTY_VALUE)
        ArrayInitialize(BufferESZ2, EMPTY_VALUE)
        ArrayInitialize(BufferESZ3, EMPTY_VALUE)
        ArrayInitialize(BufferESZ1tmp, 0)
        ArrayInitialize(BufferESZ2tmp, 0)
        ArrayInitialize(BufferESZ3tmp, 0)
        ArrayInitialize(BufferEMA1, 0)
        ArrayInitialize(BufferEMA2, 0)
        ArrayInitialize(BufferEMA3, 0)
    if (Time("", timeframe1, 1) == 0 or Time("", timeframe2, 1) == 0) or Time("", timeframe3, 1) == 0:
        return 0
    bars1 = (rates_total if (timeframe1 == Period()) else Bars(None, timeframe1))
    bars2 = (rates_total if (timeframe2 == Period()) else Bars(None, timeframe2))
    bars3 = (rates_total if (timeframe3 == Period()) else Bars(None, timeframe3))
    count1 = (fmin(bars1, rates_total) if (limit > 1) else 1)
    copied1 = CopyBuffer(handle_ma1, 0, 0, count1, BufferEMA1)
    if copied1 != count1:
        return 0
    count2 = (fmin(bars2, rates_total) if (limit > 1) else 1)
    copied2 = CopyBuffer(handle_ma2, 0, 0, count2, BufferEMA2)
    if copied2 != count2:
        return 0
    count3 = (fmin(bars3, rates_total) if (limit > 1) else 1)
    copied3 = CopyBuffer(handle_ma3, 0, 0, count3, BufferEMA3)
    if copied3 != count3:
        return 0
    for i in range(limit, 0 - 1, -1):
        ESZ("", timeframe1, count1, i, period_esz, BufferEMA1, BufferESZ1tmp)
        ESZ("", timeframe2, count2, i, period_esz, BufferEMA2, BufferESZ2tmp)
        ESZ("", timeframe3, count3, i, period_esz, BufferEMA3, BufferESZ3tmp)
    for i in range(limit, 0 - 1, -1):
        DataConversion(rates_total, "", timeframe1, i, BufferESZ1tmp, BufferESZ1, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferESZ2tmp, BufferESZ2, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferESZ3tmp, BufferESZ3, InpDrawMode)
    return rates_total

def OnTimer():
    Time("", timeframe1, 1)
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)

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

def ESZ(symbol_name, timeframe, rates_total, shift, period, buffer_ema, buffer_esz):
    if shift > (rates_total - period - 3):
        return
    PreSafeStop = buffer_esz[shift + 1]
    Pen = 0.0
    Counter = 0.0
    SafeStop = 0.0
    low = Low(symbol_name, timeframe, shift)
    if low == 0:
        return
    high = High(symbol_name, timeframe, shift)
    if high == 0:
        return
    close = Close(symbol_name, timeframe, shift)
    if close == 0:
        return
    if buffer_ema[shift] > buffer_ema[shift + 1]:
        for j in range(0, period):
            pl0 = Low(symbol_name, timeframe, shift + j)
            pl1 = Low(symbol_name, timeframe, shift + j + 1)
            if pl0 == 0 or pl1 == 0:
                continue
            if pl0 < pl1:
                Pen = pl1 - pl0 + Pen
                Counter += 1
        if Counter > 0:
            SafeStop = close - (stop_factor * _fdiv(Pen, Counter))
        else:
            SafeStop = close - (stop_factor * Pen)
        if SafeStop < PreSafeStop and buffer_ema[shift + 1] > buffer_ema[shift + 2]:
            SafeStop = PreSafeStop
    elif buffer_ema[shift] < buffer_ema[shift + 1]:
        for j in range(0, period):
            ph0 = High(symbol_name, timeframe, shift + j)
            ph1 = High(symbol_name, timeframe, shift + j + 1)
            if ph0 > ph1:
                Pen = ph0 - ph1 + Pen
                Counter += 1
        if Counter > 0:
            SafeStop = close + (stop_factor * _fdiv(Pen, Counter))
        else:
            SafeStop = close + (stop_factor * Pen)
        if SafeStop > PreSafeStop and buffer_ema[shift + 1] < buffer_ema[shift + 2]:
            SafeStop = PreSafeStop
    PreSafeStop = SafeStop
    buffer_esz[shift] = SafeStop


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EldersSafeZoneMTF(_MQL5Indicator):
    name = 'Elders_Safe_Zone_MTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # ESZ Period
        'InpStopFactor': 3,  # Stop factor
        'InpPeriodEMA': 13,  # EMA period
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
        'InpTimeframe1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # First ESZ timeframe
        'InpTimeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Second ESZ timeframe
        'InpTimeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Third ESZ timeframe
    }

