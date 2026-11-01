"""MTF_Stochastic_RSI — converted from MQL5: MQL5 Indicators/MTF_Stochastic_RSI/MTF_Stochastic_RSI.mq5

Multi timeframes Stochastic RSI oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 18, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [255], 2: [36095], 3: [32768], 4: [3329330], 5: [16711680], 6: [13422920]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'SK1', 2: 'SD1', 3: 'SK2', 4: 'SD2', 5: 'SK3', 6: 'SD3'}, 'levels': [], 'description': ['Multi timeframes Stochastic RSI oscillator'], 'name': 'MTF_Stochastic_RSI', 'source': 'MQL5 Indicators/MTF_Stochastic_RSI/MTF_Stochastic_RSI.mq5', 'folder': 'MTF_Stochastic_RSI', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 14, 'label': 'Stochastic %K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': 'Stochastic %D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 5, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}, {'mql': 'InpTimeframe1', 'py': 'InpTimeframe1', 'param': 'InpTimeframe1', 'type': 'int', 'default': 16385, 'label': 'First Stochastic RSI timeframe', 'sinput': False}, {'mql': 'InpTimeframe2', 'py': 'InpTimeframe2', 'param': 'InpTimeframe2', 'type': 'int', 'default': 16388, 'label': 'Second Stochastic RSI timeframe', 'sinput': False}, {'mql': 'InpTimeframe3', 'py': 'InpTimeframe3', 'param': 'InpTimeframe3', 'type': 'int', 'default': 16408, 'label': 'Third Stochastic RSI timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 14)  # Stochastic %K period
InpPeriodD = _input('InpPeriodD', 3)  # Stochastic %D period
InpSlowing = _input('InpSlowing', 5)  # Stochastic slowing
InpPeriodRSI = _input('InpPeriodRSI', 14)  # RSI period
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
InpTimeframe1 = _input('InpTimeframe1', PERIOD_H1)  # First Stochastic RSI timeframe
InpTimeframe2 = _input('InpTimeframe2', PERIOD_H4)  # Second Stochastic RSI timeframe
InpTimeframe3 = _input('InpTimeframe3', PERIOD_D1)  # Third Stochastic RSI timeframe
BufferSK1 = Arr(0, 0.0)
BufferSD1 = Arr(0, 0.0)
BufferSK2 = Arr(0, 0.0)
BufferSD2 = Arr(0, 0.0)
BufferSK3 = Arr(0, 0.0)
BufferSD3 = Arr(0, 0.0)
BufferSK1tmp = Arr(0, 0.0)
BufferSD1tmp = Arr(0, 0.0)
BufferSK2tmp = Arr(0, 0.0)
BufferSD2tmp = Arr(0, 0.0)
BufferSK3tmp = Arr(0, 0.0)
BufferSD3tmp = Arr(0, 0.0)
BufferRSI1 = Arr(0, 0.0)
BufferRSI2 = Arr(0, 0.0)
BufferRSI3 = Arr(0, 0.0)
BufferSKI1 = Arr(0, 0.0)
BufferSKI2 = Arr(0, 0.0)
BufferSKI3 = Arr(0, 0.0)
timeframe1 = 0
timeframe2 = 0
timeframe3 = 0
overbought = 0.0
oversold = 0.0
periodRSI = 0
periodK = 0
periodD = 0
slowing = 0
handle_rsi1 = 0
handle_rsi2 = 0
handle_rsi3 = 0

def OnInit():
    global handle_rsi1, handle_rsi2, handle_rsi3, overbought, oversold, periodD, periodK, periodRSI, slowing, timeframe1, timeframe2, timeframe3
    EventSetTimer(90)
    periodRSI = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    periodK = (1 if (InpPeriodK < 1) else InpPeriodK)
    periodD = (1 if (InpPeriodD < 1) else InpPeriodD)
    slowing = (1 if (InpSlowing < 1) else InpSlowing)
    timeframe1 = (InpTimeframe1 if (InpTimeframe1 > Period()) else Period())
    timeframe2 = (InpTimeframe2 if (InpTimeframe2 > Period()) else Period())
    timeframe3 = (InpTimeframe3 if (InpTimeframe3 > Period()) else Period())
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferSK1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSD1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSK2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSD2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferSK3, INDICATOR_DATA)
    SetIndexBuffer(5, BufferSD3, INDICATOR_DATA)
    SetIndexBuffer(6, BufferSK1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSD1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferSK2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferSD2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferSK3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferSD3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferRSI1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferRSI2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferRSI3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, BufferSKI1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, BufferSKI2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, BufferSKI3, INDICATOR_CALCULATIONS)
    label = TimeframeToString(timeframe1) + ',' + TimeframeToString(timeframe2) + ',' + TimeframeToString(timeframe3) + ' Stochastic RSI(' + _str(periodK) + ',' + _str(periodD) + ',' + _str(slowing) + ',' + _str(periodRSI) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframe1) + ' Sto%K(' + _str(periodK) + ',' + _str(periodD) + ',' + _str(slowing) + ',' + _str(periodRSI) + ')')
    PlotIndexSetString(1, PLOT_LABEL, TimeframeToString(timeframe1) + ' Sto%D(' + _str(periodK) + ',' + _str(periodD) + ',' + _str(slowing) + ',' + _str(periodRSI) + ')')
    PlotIndexSetString(2, PLOT_LABEL, TimeframeToString(timeframe2) + ' Sto%K(' + _str(periodK) + ',' + _str(periodD) + ',' + _str(slowing) + ',' + _str(periodRSI) + ')')
    PlotIndexSetString(3, PLOT_LABEL, TimeframeToString(timeframe2) + ' Sto%D(' + _str(periodK) + ',' + _str(periodD) + ',' + _str(slowing) + ',' + _str(periodRSI) + ')')
    PlotIndexSetString(4, PLOT_LABEL, TimeframeToString(timeframe3) + ' Sto%K(' + _str(periodK) + ',' + _str(periodD) + ',' + _str(slowing) + ',' + _str(periodRSI) + ')')
    PlotIndexSetString(5, PLOT_LABEL, TimeframeToString(timeframe3) + ' Sto%D(' + _str(periodK) + ',' + _str(periodD) + ',' + _str(slowing) + ',' + _str(periodRSI) + ')')
    ArraySetAsSeries(BufferSK1, True)
    ArraySetAsSeries(BufferSD1, True)
    ArraySetAsSeries(BufferSK2, True)
    ArraySetAsSeries(BufferSD2, True)
    ArraySetAsSeries(BufferSK3, True)
    ArraySetAsSeries(BufferSD3, True)
    ArraySetAsSeries(BufferSK1tmp, True)
    ArraySetAsSeries(BufferSD1tmp, True)
    ArraySetAsSeries(BufferSK2tmp, True)
    ArraySetAsSeries(BufferSD2tmp, True)
    ArraySetAsSeries(BufferSK3tmp, True)
    ArraySetAsSeries(BufferSD3tmp, True)
    ArraySetAsSeries(BufferRSI1, True)
    ArraySetAsSeries(BufferRSI2, True)
    ArraySetAsSeries(BufferRSI3, True)
    ArraySetAsSeries(BufferSKI1, True)
    ArraySetAsSeries(BufferSKI2, True)
    ArraySetAsSeries(BufferSKI3, True)
    ResetLastError()
    handle_rsi1 = iRSI(None, timeframe1, periodRSI, PRICE_CLOSE)
    if handle_rsi1 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe1), ' iRSI(' + _str(periodRSI) + ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi2 = iRSI(None, timeframe2, periodRSI, PRICE_CLOSE)
    if handle_rsi2 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe2), ' iRSI(' + _str(periodRSI) + ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi3 = iRSI(None, timeframe3, periodRSI, PRICE_CLOSE)
    if handle_rsi3 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe3), ' iRSI(' + _str(periodRSI) + ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    Time("", timeframe1, 1)
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(slowing, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferSK1, EMPTY_VALUE)
        ArrayInitialize(BufferSD1, EMPTY_VALUE)
        ArrayInitialize(BufferSK2, EMPTY_VALUE)
        ArrayInitialize(BufferSD2, EMPTY_VALUE)
        ArrayInitialize(BufferSK3, EMPTY_VALUE)
        ArrayInitialize(BufferSD3, EMPTY_VALUE)
        ArrayInitialize(BufferSK1tmp, 0)
        ArrayInitialize(BufferSD1tmp, 0)
        ArrayInitialize(BufferSK2tmp, 0)
        ArrayInitialize(BufferSD2tmp, 0)
        ArrayInitialize(BufferSK3tmp, 0)
        ArrayInitialize(BufferSD3tmp, 0)
        ArrayInitialize(BufferRSI1, 0)
        ArrayInitialize(BufferRSI2, 0)
        ArrayInitialize(BufferRSI3, 0)
        ArrayInitialize(BufferSKI1, 0)
        ArrayInitialize(BufferSKI2, 0)
        ArrayInitialize(BufferSKI3, 0)
    if (Time("", timeframe1, 1) == 0 or Time("", timeframe2, 1) == 0) or Time("", timeframe3, 1) == 0:
        return 0
    bars1 = (rates_total if (timeframe1 == Period()) else Bars(None, timeframe1))
    bars2 = (rates_total if (timeframe2 == Period()) else Bars(None, timeframe2))
    bars3 = (rates_total if (timeframe3 == Period()) else Bars(None, timeframe3))
    count1 = (fmin(bars1, rates_total) if (limit > 1) else 1)
    copied1 = CopyBuffer(handle_rsi1, 0, 0, count1, BufferRSI1)
    if copied1 != count1:
        return 0
    count2 = (fmin(bars2, rates_total) if (limit > 1) else 1)
    copied2 = CopyBuffer(handle_rsi2, 0, 0, count2, BufferRSI2)
    if copied2 != count2:
        return 0
    count3 = (fmin(bars3, rates_total) if (limit > 1) else 1)
    copied3 = CopyBuffer(handle_rsi3, 0, 0, count3, BufferRSI3)
    if copied3 != count3:
        return 0
    for i in range(limit, 0 - 1, -1):
        DataPreparing(count1, i, periodK, BufferRSI1, BufferSKI1)
        DataPreparing(count2, i, periodK, BufferRSI2, BufferSKI2)
        DataPreparing(count3, i, periodK, BufferRSI3, BufferSKI3)
    for i in range(limit, 0 - 1, -1):
        BufferSK1tmp[i] = GetSMA(count1, i, slowing, BufferSKI1)
        BufferSK2tmp[i] = GetSMA(count2, i, slowing, BufferSKI2)
        BufferSK3tmp[i] = GetSMA(count3, i, slowing, BufferSKI3)
    for i in range(limit, 0 - 1, -1):
        BufferSD1tmp[i] = GetSMA(count1, i, periodD, BufferSK1tmp)
        BufferSD2tmp[i] = GetSMA(count2, i, periodD, BufferSK2tmp)
        BufferSD3tmp[i] = GetSMA(count3, i, periodD, BufferSK3tmp)
    for i in range(limit, 0 - 1, -1):
        DataConversion(rates_total, "", timeframe1, i, BufferSK1tmp, BufferSK1, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferSK2tmp, BufferSK2, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferSK3tmp, BufferSK3, InpDrawMode)
        DataConversion(rates_total, "", timeframe1, i, BufferSD1tmp, BufferSD1, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferSD2tmp, BufferSD2, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferSD3tmp, BufferSD3, InpDrawMode)
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

def DataPreparing(rates_total, shift, period_k, buffer_rsi, buffer_ski):
    if shift > (rates_total - period_k - 1):
        return
    max_ = 0.0
    min_ = 0.0
    for j in range(shift + period_k - 1, shift - 1, -1):
        if j == (shift + period_k - 1):
            min_ = buffer_rsi[j]
            max_ = min_
        else:
            if buffer_rsi[j] > max_:
                max_ = buffer_rsi[j]
            if buffer_rsi[j] < min_:
                min_ = buffer_rsi[j]
    buffer_ski[shift] = ((_fdiv(buffer_rsi[shift] - min_, max_ - min_) * 100.0) if (max_ != min_) else 100.0)

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


class MTFStochasticRSI(_MQL5Indicator):
    name = 'MTF_Stochastic_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriodK': 14,  # Stochastic %K period
        'InpPeriodD': 3,  # Stochastic %D period
        'InpSlowing': 5,  # Stochastic slowing
        'InpPeriodRSI': 14,  # RSI period
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
        'InpTimeframe1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # First Stochastic RSI timeframe
        'InpTimeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Second Stochastic RSI timeframe
        'InpTimeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Third Stochastic RSI timeframe
    }

