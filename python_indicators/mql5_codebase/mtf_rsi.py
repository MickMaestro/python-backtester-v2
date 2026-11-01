"""MTF_RSI — converted from MQL5: MQL5 Indicators/MTF_RSI/MTF_RSI.mq5

Multi timeframes RSI oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [32768], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'RSI1', 2: 'RSI2', 3: 'RSI3'}, 'levels': [], 'description': ['Multi timeframes RSI oscillator'], 'name': 'MTF_RSI', 'source': 'MQL5 Indicators/MTF_RSI/MTF_RSI.mq5', 'folder': 'MTF_RSI', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}, {'mql': 'InpTimeframe1', 'py': 'InpTimeframe1', 'param': 'InpTimeframe1', 'type': 'int', 'default': 16385, 'label': 'First RSI timeframe', 'sinput': False}, {'mql': 'InpTimeframe2', 'py': 'InpTimeframe2', 'param': 'InpTimeframe2', 'type': 'int', 'default': 16388, 'label': 'Second RSI timeframe', 'sinput': False}, {'mql': 'InpTimeframe3', 'py': 'InpTimeframe3', 'param': 'InpTimeframe3', 'type': 'int', 'default': 16408, 'label': 'Third RSI timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 14)  # RSI period
InpOverbought = _input('InpOverbought', 70.0)  # Overbought
InpOversold = _input('InpOversold', 30.0)  # Oversold
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
InpTimeframe1 = _input('InpTimeframe1', PERIOD_H1)  # First RSI timeframe
InpTimeframe2 = _input('InpTimeframe2', PERIOD_H4)  # Second RSI timeframe
InpTimeframe3 = _input('InpTimeframe3', PERIOD_D1)  # Third RSI timeframe
BufferRSI1 = Arr(0, 0.0)
BufferRSI2 = Arr(0, 0.0)
BufferRSI3 = Arr(0, 0.0)
BufferRSI1tmp = Arr(0, 0.0)
BufferRSI2tmp = Arr(0, 0.0)
BufferRSI3tmp = Arr(0, 0.0)
timeframe1 = 0
timeframe2 = 0
timeframe3 = 0
overbought = 0.0
oversold = 0.0
period = 0
handle_rsi1 = 0
handle_rsi2 = 0
handle_rsi3 = 0

def OnInit():
    global handle_rsi1, handle_rsi2, handle_rsi3, overbought, oversold, period, timeframe1, timeframe2, timeframe3
    EventSetTimer(90)
    period = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    timeframe1 = (InpTimeframe1 if (InpTimeframe1 > Period()) else Period())
    timeframe2 = (InpTimeframe2 if (InpTimeframe2 > Period()) else Period())
    timeframe3 = (InpTimeframe3 if (InpTimeframe3 > Period()) else Period())
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferRSI1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRSI2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRSI3, INDICATOR_DATA)
    SetIndexBuffer(3, BufferRSI1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferRSI2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferRSI3tmp, INDICATOR_CALCULATIONS)
    label = TimeframeToString(timeframe1) + ',' + TimeframeToString(timeframe2) + ',' + TimeframeToString(timeframe3) + ' RSI(' + _str(period) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframe1) + ' RSI(' + _str(period) + ')')
    PlotIndexSetString(1, PLOT_LABEL, TimeframeToString(timeframe2) + ' RSI(' + _str(period) + ')')
    PlotIndexSetString(2, PLOT_LABEL, TimeframeToString(timeframe3) + ' RSI(' + _str(period) + ')')
    ArraySetAsSeries(BufferRSI1, True)
    ArraySetAsSeries(BufferRSI2, True)
    ArraySetAsSeries(BufferRSI3, True)
    ArraySetAsSeries(BufferRSI1tmp, True)
    ArraySetAsSeries(BufferRSI2tmp, True)
    ArraySetAsSeries(BufferRSI3tmp, True)
    ResetLastError()
    handle_rsi1 = iRSI(None, timeframe1, period, PRICE_CLOSE)
    if handle_rsi1 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe1), ' iRSI(' + _str(period) + ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi2 = iRSI(None, timeframe2, period, PRICE_CLOSE)
    if handle_rsi2 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe2), ' iRSI(' + _str(period) + ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi3 = iRSI(None, timeframe3, period, PRICE_CLOSE)
    if handle_rsi3 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe3), ' iRSI(' + _str(period) + ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    Time("", timeframe1, 1)
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferRSI1, 0)
        ArrayInitialize(BufferRSI2, 0)
        ArrayInitialize(BufferRSI3, 0)
        ArrayInitialize(BufferRSI1tmp, 0)
        ArrayInitialize(BufferRSI2tmp, 0)
        ArrayInitialize(BufferRSI3tmp, 0)
    if (Time("", timeframe1, 1) == 0 or Time("", timeframe2, 1) == 0) or Time("", timeframe3, 1) == 0:
        return 0
    bars1 = (rates_total if (timeframe1 == Period()) else Bars(None, timeframe1))
    bars2 = (rates_total if (timeframe2 == Period()) else Bars(None, timeframe2))
    bars3 = (rates_total if (timeframe3 == Period()) else Bars(None, timeframe3))
    count1 = (fmin(bars1, rates_total) if (limit > 1) else 1)
    copied1 = CopyBuffer(handle_rsi1, 0, 0, count1, BufferRSI1tmp)
    if copied1 != count1:
        return 0
    count2 = (fmin(bars2, rates_total) if (limit > 1) else 1)
    copied2 = CopyBuffer(handle_rsi2, 0, 0, count2, BufferRSI2tmp)
    if copied2 != count2:
        return 0
    count3 = (fmin(bars3, rates_total) if (limit > 1) else 1)
    copied3 = CopyBuffer(handle_rsi3, 0, 0, count3, BufferRSI3tmp)
    if copied3 != count3:
        return 0
    for i in range(limit, 0 - 1, -1):
        DataConversion(rates_total, "", timeframe1, i, BufferRSI1tmp, BufferRSI1, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferRSI2tmp, BufferRSI2, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferRSI3tmp, BufferRSI3, InpDrawMode)
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

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MTFRSI(_MQL5Indicator):
    name = 'MTF_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriodRSI': 14,  # RSI period
        'InpOverbought': 70.0,  # Overbought
        'InpOversold': 30.0,  # Oversold
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
        'InpTimeframe1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # First RSI timeframe
        'InpTimeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Second RSI timeframe
        'InpTimeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Third RSI timeframe
    }

