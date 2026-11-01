"""MTF_LRMA — converted from MQL5: MQL5 Indicators/MTF_LRMA/MTF_LRMA.mq5

Multi Timeframe Linear Regression Moving Average with signal line
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329330], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'LRMA', 2: 'Signal'}, 'levels': [], 'description': ['Multi Timeframe Linear Regression Moving Average with signal line'], 'name': 'MTF_LRMA', 'source': 'MQL5 Indicators/MTF_LRMA/MTF_LRMA.mq5', 'folder': 'MTF_LRMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 34, 'label': 'LRMA period', 'sinput': False}, {'mql': 'InpSignal', 'py': 'InpSignal', 'param': 'InpSignal', 'type': 'uint', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 16385, 'label': 'LRMA timeframe', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 34)  # LRMA period
InpSignal = _input('InpSignal', 5)  # Signal period
InpTimeframe = _input('InpTimeframe', PERIOD_H1)  # LRMA timeframe
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
BufferLRMA = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferLRMATmp = Arr(0, 0.0)
BufferSignalTmp = Arr(0, 0.0)
BufferLWMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
timeframe1 = 0
period_lrma = 0
signal = 0
handle_lwma = 0
handle_sma = 0

def OnInit():
    global handle_lwma, handle_sma, period_lrma, signal, timeframe1
    EventSetTimer(90)
    period_lrma = (1 if (InpPeriod < 1) else InpPeriod)
    signal = (1 if (InpSignal < 1) else InpSignal)
    timeframe1 = (InpTimeframe if (InpTimeframe > Period()) else Period())
    SetIndexBuffer(0, BufferLRMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLRMATmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSignalTmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferLWMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSMA, INDICATOR_CALCULATIONS)
    label = TimeframeToString(timeframe1) + ' LRMA(' + _str(period_lrma) + ',' + _str(signal) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframe1) + ' LRMA(' + _str(period_lrma) + ')')
    PlotIndexSetString(1, PLOT_LABEL, TimeframeToString(timeframe1) + ' Signal(' + _str(signal) + ')')
    ArraySetAsSeries(BufferLRMA, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferLRMATmp, True)
    ArraySetAsSeries(BufferSignalTmp, True)
    ArraySetAsSeries(BufferLWMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ResetLastError()
    handle_lwma = iMA(None, timeframe1, period_lrma, 0, MODE_LWMA, PRICE_CLOSE)
    if handle_lwma == INVALID_HANDLE:
        Print(86, ': The ', TimeframeToString(timeframe1), ' iMA(', _str(period_lrma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, timeframe1, period_lrma, 0, MODE_SMA, PRICE_CLOSE)
    if handle_sma == INVALID_HANDLE:
        Print(92, ': The ', TimeframeToString(timeframe1), ' iMA(', _str(period_lrma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    Time("", timeframe1, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(signal, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - signal - 2
        ArrayInitialize(BufferLRMA, 0)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferLRMATmp, 0)
        ArrayInitialize(BufferSignalTmp, 0)
        ArrayInitialize(BufferLWMA, 0)
        ArrayInitialize(BufferSMA, 0)
    if Time("", timeframe1, 1) == 0:
        return 0
    bars = (rates_total if (timeframe1 == Period()) else Bars(None, timeframe1))
    count = (fmin(bars, rates_total) if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_lwma, 0, 0, count, BufferLWMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferLRMATmp[i] = (3.0 * BufferLWMA[i]) - (2.0 * BufferSMA[i])
        BufferSignalTmp[i] = GetSMA(bars, i, signal, BufferLRMATmp)
    for i in range(limit, 0 - 1, -1):
        DataConversion(rates_total, "", timeframe1, i, BufferLRMATmp, BufferLRMA, InpDrawMode)
        DataConversion(rates_total, "", timeframe1, i, BufferSignalTmp, BufferSignal, InpDrawMode)
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


class MTFLRMA(_MQL5Indicator):
    name = 'MTF_LRMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 34,  # LRMA period
        'InpSignal': 5,  # Signal period
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # LRMA timeframe
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
    }

