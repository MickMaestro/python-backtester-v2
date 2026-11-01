"""MTF_MA — converted from MQL5: MQL5 Indicators/MTF_MA/MTF_MA.mq5

Multitimeframe Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'MA'}, 'levels': [], 'description': ['Multitimeframe Moving Average'], 'name': 'MTF_MA', 'source': 'MQL5 Indicators/MTF_MA/MTF_MA.mq5', 'folder': 'MTF_MA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 16388, 'label': 'Timeframe', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpTimeframe = _input('InpTimeframe', PERIOD_H4)  # Timeframe
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
BufferTFMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
timeframe_g = 0
period_ma = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma, timeframe_g
    EventSetTimer(90)
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    timeframe_g = (InpTimeframe if (InpTimeframe > Period()) else Period())
    SetIndexBuffer(0, BufferTFMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_DATA)
    label = MethodToString(InpMethod) + ' (' + _str(period_ma) + ',' + TimeframeToString(timeframe_g) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, label)
    ArraySetAsSeries(BufferTFMA, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, timeframe_g, period_ma, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(' + _str(period_ma) + ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    Time("", timeframe_g, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 2
        ArrayInitialize(BufferTFMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    if Time("", timeframe_g, 1) == 0:
        return 0
    bars = (rates_total if (timeframe_g == Period()) else Bars(None, timeframe_g))
    count = (fmin(bars, rates_total) if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        time_g = Time("", timeframe_g, i)
        if time_g == 0:
            continue
        bar_curr = BarShift("", PERIOD_CURRENT, time_g)
        if bar_curr == WRONG_VALUE or bar_curr > (rates_total - period_ma - 2):
            continue
        shift = (1 if (i > 0) else 0)
        time_next = Time("", timeframe_g, i - shift)
        if time_next == 0:
            continue
        bar_next = (BarShift("", PERIOD_CURRENT, time_next) if (i > 0) else 0)
        if bar_next == WRONG_VALUE or bar_next > (rates_total - period_ma - 2):
            continue
        BufferTFMA[bar_curr] = BufferMA[i]
        if InpDrawMode == DRAW_MODE_STEPS:
            for j in range(bar_curr, bar_next - 1, -1):
                BufferTFMA[j] = BufferTFMA[bar_curr]
        else:
            time_prev = Time("", timeframe_g, i + 1)
            if time_prev == 0:
                continue
            bar_prev = BarShift("", PERIOD_CURRENT, time_prev)
            if bar_prev == WRONG_VALUE:
                continue
            for j in range(bar_prev, bar_curr - 1, -1):
                BufferTFMA[j] = EquationDirect(bar_prev, BufferTFMA[bar_prev], bar_curr, BufferTFMA[bar_curr], j)
    return rates_total

def OnTimer():
    Time("", timeframe_g, 1)

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

def MethodToString(method):
    return StringSubstr(EnumToString(method, 'ENUM_MA_METHOD'), 5)

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MTFMA(_MQL5Indicator):
    name = 'MTF_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Timeframe
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
    }

