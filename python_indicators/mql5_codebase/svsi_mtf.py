"""SVSI_MTF — converted from MQL5: MQL5 Indicators/SVSI_MTF/SVSI_MTF.mq5

Multi timeframe Slow Volume Strength Index oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 15, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [32768], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'SVSI 1', 2: 'SVSI 2', 3: 'SVSI 3'}, 'levels': [], 'description': ['Multi timeframe Slow Volume Strength Index oscillator'], 'name': 'SVSI_MTF', 'source': 'MQL5 Indicators/SVSI_MTF/SVSI_MTF.mq5', 'folder': 'SVSI_MTF', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 6, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 14, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpMiddle', 'py': 'InpMiddle', 'param': 'InpMiddle', 'type': 'double', 'default': 50.0, 'label': 'Middle', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}, {'mql': 'InpTimeframe1', 'py': 'InpTimeframe1', 'param': 'InpTimeframe1', 'type': 'int', 'default': 16385, 'label': 'First SVSI timeframe', 'sinput': False}, {'mql': 'InpTimeframe2', 'py': 'InpTimeframe2', 'param': 'InpTimeframe2', 'type': 'int', 'default': 16388, 'label': 'Second SVSI timeframe', 'sinput': False}, {'mql': 'InpTimeframe3', 'py': 'InpTimeframe3', 'param': 'InpTimeframe3', 'type': 'int', 'default': 16408, 'label': 'Third SVSI timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 6)  # EMA period
InpPeriodSm = _input('InpPeriodSm', 14)  # Smoothing
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpMiddle = _input('InpMiddle', 50.0)  # Middle
InpOversold = _input('InpOversold', 20.0)  # Oversold
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
InpTimeframe1 = _input('InpTimeframe1', PERIOD_H1)  # First SVSI timeframe
InpTimeframe2 = _input('InpTimeframe2', PERIOD_H4)  # Second SVSI timeframe
InpTimeframe3 = _input('InpTimeframe3', PERIOD_D1)  # Third SVSI timeframe
BufferSVSI1 = Arr(0, 0.0)
BufferSVSI2 = Arr(0, 0.0)
BufferSVSI3 = Arr(0, 0.0)
BufferSVSI1tmp = Arr(0, 0.0)
BufferSVSI2tmp = Arr(0, 0.0)
BufferSVSI3tmp = Arr(0, 0.0)
BufferPos1 = Arr(0, 0.0)
BufferNeg1 = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferPos2 = Arr(0, 0.0)
BufferNeg2 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferPos3 = Arr(0, 0.0)
BufferNeg3 = Arr(0, 0.0)
BufferMA3 = Arr(0, 0.0)
timeframe1 = 0
timeframe2 = 0
timeframe3 = 0
overbought = 0.0
middle = 0.0
oversold = 0.0
period_ma = 0
period_sm = 0
handle_ma1 = 0
handle_ma2 = 0
handle_ma3 = 0

def OnInit():
    global handle_ma1, handle_ma2, handle_ma3, middle, overbought, oversold, period_ma, period_sm, timeframe1, timeframe2, timeframe3
    EventSetTimer(90)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_sm = (1 if (InpPeriodSm < 1) else InpPeriodSm)
    timeframe1 = (InpTimeframe1 if (InpTimeframe1 > Period()) else Period())
    timeframe2 = (InpTimeframe2 if (InpTimeframe2 > Period()) else Period())
    timeframe3 = (InpTimeframe3 if (InpTimeframe3 > Period()) else Period())
    middle = (99.9 if (InpMiddle > 99.9) else 0.1 if (InpMiddle < 0.1) else InpMiddle)
    overbought = (100 if (InpOverbought > 100) else (middle + 0.1) if (InpOverbought <= middle) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (middle - 0.1) if (InpOversold >= middle) else InpOversold)
    SetIndexBuffer(0, BufferSVSI1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSVSI2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSVSI3, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSVSI1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSVSI2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSVSI3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferPos1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferNeg1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferPos2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferNeg2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferPos3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferNeg3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferMA3, INDICATOR_CALCULATIONS)
    label = TimeframeToString(timeframe1) + ',' + TimeframeToString(timeframe2) + ',' + TimeframeToString(timeframe3) + ' SVSI(' + _str(period_ma) + ',' + _str(period_sm) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, middle)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframe1) + ' SVSI(' + _str(period_ma) + ',' + _str(period_sm) + ')')
    PlotIndexSetString(1, PLOT_LABEL, TimeframeToString(timeframe2) + ' SVSI(' + _str(period_ma) + ',' + _str(period_sm) + ')')
    PlotIndexSetString(2, PLOT_LABEL, TimeframeToString(timeframe3) + ' SVSI(' + _str(period_ma) + ',' + _str(period_sm) + ')')
    ArraySetAsSeries(BufferSVSI1, True)
    ArraySetAsSeries(BufferSVSI2, True)
    ArraySetAsSeries(BufferSVSI3, True)
    ArraySetAsSeries(BufferSVSI1tmp, True)
    ArraySetAsSeries(BufferSVSI2tmp, True)
    ArraySetAsSeries(BufferSVSI3tmp, True)
    ArraySetAsSeries(BufferPos1, True)
    ArraySetAsSeries(BufferNeg1, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferPos2, True)
    ArraySetAsSeries(BufferNeg2, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferPos3, True)
    ArraySetAsSeries(BufferNeg3, True)
    ArraySetAsSeries(BufferMA3, True)
    ResetLastError()
    handle_ma1 = iMA(None, timeframe1, period_ma, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma1 == INVALID_HANDLE:
        Print(142, ': The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, timeframe2, period_ma, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma2 == INVALID_HANDLE:
        Print(148, ': The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma3 = iMA(None, timeframe3, period_ma, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma3 == INVALID_HANDLE:
        Print(154, ': The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    Time("", timeframe1, 1)
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_sm, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_sm - 1
        ArrayInitialize(BufferSVSI1, EMPTY_VALUE)
        ArrayInitialize(BufferSVSI2, EMPTY_VALUE)
        ArrayInitialize(BufferSVSI3, EMPTY_VALUE)
        ArrayInitialize(BufferSVSI1tmp, 0)
        ArrayInitialize(BufferSVSI2tmp, 0)
        ArrayInitialize(BufferSVSI3tmp, 0)
        ArrayInitialize(BufferPos1, 0)
        ArrayInitialize(BufferNeg1, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferPos2, 0)
        ArrayInitialize(BufferNeg2, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferPos3, 0)
        ArrayInitialize(BufferNeg3, 0)
        ArrayInitialize(BufferMA3, 0)
    if (Time("", timeframe1, 1) == 0 or Time("", timeframe2, 1) == 0) or Time("", timeframe3, 1) == 0:
        return 0
    bars1 = (rates_total if (timeframe1 == Period()) else Bars(None, timeframe1))
    bars2 = (rates_total if (timeframe2 == Period()) else Bars(None, timeframe2))
    bars3 = (rates_total if (timeframe3 == Period()) else Bars(None, timeframe3))
    count1 = (fmin(bars1, rates_total) if (limit > 1) else 1)
    copied1 = CopyBuffer(handle_ma1, 0, 0, count1, BufferMA1)
    if copied1 != count1:
        return 0
    count2 = (fmin(bars2, rates_total) if (limit > 1) else 1)
    copied2 = CopyBuffer(handle_ma2, 0, 0, count2, BufferMA2)
    if copied2 != count2:
        return 0
    count3 = (fmin(bars3, rates_total) if (limit > 1) else 1)
    copied3 = CopyBuffer(handle_ma3, 0, 0, count3, BufferMA3)
    if copied3 != count3:
        return 0
    for i in range(limit, 0 - 1, -1):
        if not DataPreparing(i, timeframe1, BufferMA1, BufferPos1, BufferNeg1):
            continue
        if not DataPreparing(i, timeframe2, BufferMA2, BufferPos2, BufferNeg2):
            continue
        if not DataPreparing(i, timeframe3, BufferMA3, BufferPos3, BufferNeg3):
            continue
    for i in range(limit, 0 - 1, -1):
        SVSI(rates_total, i, period_sm, BufferPos1, BufferNeg1, BufferSVSI1tmp)
        SVSI(rates_total, i, period_sm, BufferPos2, BufferNeg2, BufferSVSI2tmp)
        SVSI(rates_total, i, period_sm, BufferPos3, BufferNeg3, BufferSVSI3tmp)
    for i in range(limit, 0 - 1, -1):
        DataConversion(rates_total, "", timeframe1, i, BufferSVSI1tmp, BufferSVSI1, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferSVSI2tmp, BufferSVSI2, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferSVSI3tmp, BufferSVSI3, InpDrawMode)
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

def Close(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyClose(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def TickVolume(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTickVolume(symbol_name, timeframe, shift, 1, array) == 1) else 0)

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

def SVSI(rates_total, shift, smoothihg, buffer_pos, buffer_neg, buffer_svsi):
    AvgPosVol = GetSMA(rates_total, shift, smoothihg, buffer_pos)
    AvgNegVol = GetSMA(rates_total, shift, smoothihg, buffer_neg)
    svs = (_fdiv(AvgPosVol, AvgNegVol) if (AvgNegVol != 0) else 100.0)
    buffer_svsi[shift] = 100.0 - _fdiv(100.0, 1.0 + svs)

def DataPreparing(shift, timeframe, buffer_ma, buffer_pos, buffer_neg):
    close = Close("", timeframe, shift)
    volume = TickVolume("", timeframe, shift)
    if close == 0 or volume == 0:
        return False
    if close > buffer_ma[shift]:
        buffer_pos[shift] = volume / 1000000.0
        buffer_neg[shift] = 0.0
    elif close < buffer_ma[shift]:
        buffer_neg[shift] = volume / 1000000.0
        buffer_pos[shift] = 0.0
    else:
        buffer_neg[shift] = 0.0
        buffer_pos[shift] = buffer_neg[shift]
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SVSIMTF(_MQL5Indicator):
    name = 'SVSI_MTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriodMA': 6,  # EMA period
        'InpPeriodSm': 14,  # Smoothing
        'InpOverbought': 80.0,  # Overbought
        'InpMiddle': 50.0,  # Middle
        'InpOversold': 20.0,  # Oversold
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
        'InpTimeframe1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # First SVSI timeframe
        'InpTimeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Second SVSI timeframe
        'InpTimeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Third SVSI timeframe
    }

