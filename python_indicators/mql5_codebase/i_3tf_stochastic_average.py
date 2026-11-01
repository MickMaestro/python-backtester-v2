"""3TF_Stochastic_Average — converted from MQL5: MQL5 Indicators/3TF_Stochastic_Average/3TF_Stochastic_Average.mq5

Three timeframes Stochastic Average oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 14, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [255], 2: [255], 3: [32768], 4: [32768], 5: [8421504], 6: [8421504], 7: [16711680], 8: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 2, 8: 1}, 'styles': {1: 0, 2: 2, 3: 0, 4: 2, 5: 0, 6: 2, 7: 0, 8: 0}, 'labels': {1: 'Stoch1', 2: 'Signal1', 3: 'Stoch2', 4: 'Signal2', 5: 'Stoch3', 6: 'Signal3', 7: 'AvgSto', 8: 'AvgSig'}, 'levels': [], 'description': ['Three timeframes Stochastic Average oscillator'], 'name': '3TF_Stochastic_Average', 'source': 'MQL5 Indicators/3TF_Stochastic_Average/3TF_Stochastic_Average.mq5', 'folder': '3TF_Stochastic_Average', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 5, 'label': 'Stochastic %K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': 'Stochastic %D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Stochastic Slowing', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}, {'mql': 'InpTimeframe1', 'py': 'InpTimeframe1', 'param': 'InpTimeframe1', 'type': 'int', 'default': 16385, 'label': 'First Stochastic timeframe', 'sinput': False}, {'mql': 'InpTimeframe2', 'py': 'InpTimeframe2', 'param': 'InpTimeframe2', 'type': 'int', 'default': 16388, 'label': 'Second Stochastic timeframe', 'sinput': False}, {'mql': 'InpTimeframe3', 'py': 'InpTimeframe3', 'param': 'InpTimeframe3', 'type': 'int', 'default': 16408, 'label': 'Third Stochastic timeframe', 'sinput': False}, {'mql': 'InpShowSto1', 'py': 'InpShowSto1', 'param': 'InpShowSto1', 'type': 'int', 'default': 1, 'label': 'Show first Stochastic', 'sinput': False}, {'mql': 'InpShowSto2', 'py': 'InpShowSto2', 'param': 'InpShowSto2', 'type': 'int', 'default': 1, 'label': 'Show second Stochastic', 'sinput': False}, {'mql': 'InpShowSto3', 'py': 'InpShowSto3', 'param': 'InpShowSto3', 'type': 'int', 'default': 1, 'label': 'Show third Stochastic', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 5)  # Stochastic %K period
InpPeriodD = _input('InpPeriodD', 3)  # Stochastic %D period
InpSlowing = _input('InpSlowing', 3)  # Stochastic Slowing
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
InpTimeframe1 = _input('InpTimeframe1', PERIOD_H1)  # First Stochastic timeframe
InpTimeframe2 = _input('InpTimeframe2', PERIOD_H4)  # Second Stochastic timeframe
InpTimeframe3 = _input('InpTimeframe3', PERIOD_D1)  # Third Stochastic timeframe
InpShowSto1 = _input('InpShowSto1', INPUT_YES)  # Show first Stochastic
InpShowSto2 = _input('InpShowSto2', INPUT_YES)  # Show second Stochastic
InpShowSto3 = _input('InpShowSto3', INPUT_YES)  # Show third Stochastic
BufferStoch1 = Arr(0, 0.0)
BufferSignal1 = Arr(0, 0.0)
BufferStoch2 = Arr(0, 0.0)
BufferSignal2 = Arr(0, 0.0)
BufferStoch3 = Arr(0, 0.0)
BufferSignal3 = Arr(0, 0.0)
BufferAvgSto = Arr(0, 0.0)
BufferAvgSig = Arr(0, 0.0)
BufferStoch1tmp = Arr(0, 0.0)
BufferSignal1tmp = Arr(0, 0.0)
BufferStoch2tmp = Arr(0, 0.0)
BufferSignal2tmp = Arr(0, 0.0)
BufferStoch3tmp = Arr(0, 0.0)
BufferSignal3tmp = Arr(0, 0.0)
timeframe1 = 0
timeframe2 = 0
timeframe3 = 0
overbought = 0.0
oversold = 0.0
periodK = 0
periodD = 0
slowing = 0
handle_sto1 = 0
handle_sto2 = 0
handle_sto3 = 0

def OnInit():
    global handle_sto1, handle_sto2, handle_sto3, overbought, oversold, periodD, periodK, slowing, timeframe1, timeframe2, timeframe3
    EventSetTimer(90)
    periodK = (1 if (InpPeriodK < 1) else InpPeriodK)
    periodD = (1 if (InpPeriodD < 1) else InpPeriodD)
    slowing = (1 if (InpSlowing < 1) else InpSlowing)
    timeframe1 = (InpTimeframe1 if (InpTimeframe1 > Period()) else Period())
    timeframe2 = (InpTimeframe2 if (InpTimeframe2 > Period()) else Period())
    timeframe3 = (InpTimeframe3 if (InpTimeframe3 > Period()) else Period())
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferStoch1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferStoch2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSignal2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferStoch3, INDICATOR_DATA)
    SetIndexBuffer(5, BufferSignal3, INDICATOR_DATA)
    SetIndexBuffer(6, BufferAvgSto, INDICATOR_DATA)
    SetIndexBuffer(7, BufferAvgSig, INDICATOR_DATA)
    SetIndexBuffer(8, BufferStoch1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferSignal1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferStoch2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferSignal2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferStoch3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferSignal3tmp, INDICATOR_CALCULATIONS)
    label = TimeframeToString(timeframe1) + ',' + TimeframeToString(timeframe2) + ',' + TimeframeToString(timeframe3) + ' Stochastic(' + _str(periodK) + ',' + _str(periodD) + ',' + _str(slowing) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframe1) + ' Stochastic')
    PlotIndexSetString(1, PLOT_LABEL, TimeframeToString(timeframe1) + ' Signal')
    PlotIndexSetString(2, PLOT_LABEL, TimeframeToString(timeframe2) + ' Stochastic')
    PlotIndexSetString(3, PLOT_LABEL, TimeframeToString(timeframe2) + ' Signal')
    PlotIndexSetString(4, PLOT_LABEL, TimeframeToString(timeframe3) + ' Stochastic')
    PlotIndexSetString(5, PLOT_LABEL, TimeframeToString(timeframe3) + ' Signal')
    PlotIndexSetString(6, PLOT_LABEL, 'AvgSto(' + TimeframeToString(timeframe1) + ',' + TimeframeToString(timeframe2) + ',' + TimeframeToString(timeframe3) + ')')
    PlotIndexSetString(7, PLOT_LABEL, 'AvgSig(' + TimeframeToString(timeframe1) + ',' + TimeframeToString(timeframe2) + ',' + TimeframeToString(timeframe3) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, InpShowSto1)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, InpShowSto1)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, InpShowSto2)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, InpShowSto2)
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, InpShowSto3)
    PlotIndexSetInteger(5, PLOT_DRAW_TYPE, InpShowSto3)
    ArraySetAsSeries(BufferStoch1, True)
    ArraySetAsSeries(BufferSignal1, True)
    ArraySetAsSeries(BufferStoch2, True)
    ArraySetAsSeries(BufferSignal2, True)
    ArraySetAsSeries(BufferStoch3, True)
    ArraySetAsSeries(BufferSignal3, True)
    ArraySetAsSeries(BufferAvgSto, True)
    ArraySetAsSeries(BufferAvgSig, True)
    ArraySetAsSeries(BufferStoch1tmp, True)
    ArraySetAsSeries(BufferSignal1tmp, True)
    ArraySetAsSeries(BufferStoch2tmp, True)
    ArraySetAsSeries(BufferSignal2tmp, True)
    ArraySetAsSeries(BufferStoch3tmp, True)
    ArraySetAsSeries(BufferSignal3tmp, True)
    ResetLastError()
    handle_sto1 = iStochastic(None, timeframe1, periodK, periodD, slowing, MODE_SMA, STO_LOWHIGH)
    if handle_sto1 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe1), ' iStochastic(', _str(periodK), ',', _str(periodD), ',', _str(slowing), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto2 = iStochastic(None, timeframe2, periodK, periodD, slowing, MODE_SMA, STO_LOWHIGH)
    if handle_sto2 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe2), ' iStochastic(', _str(periodK), ',', _str(periodD), ',', _str(slowing), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto3 = iStochastic(None, timeframe3, periodK, periodD, slowing, MODE_SMA, STO_LOWHIGH)
    if handle_sto3 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe3), ' iStochastic(', _str(periodK), ',', _str(periodD), ',', _str(slowing), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    Time("", timeframe1, 1)
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferStoch1, 0)
        ArrayInitialize(BufferSignal1, 0)
        ArrayInitialize(BufferStoch2, 0)
        ArrayInitialize(BufferSignal2, 0)
        ArrayInitialize(BufferStoch3, 0)
        ArrayInitialize(BufferSignal3, 0)
        ArrayInitialize(BufferAvgSto, 0)
        ArrayInitialize(BufferAvgSig, 0)
        ArrayInitialize(BufferStoch1tmp, 0)
        ArrayInitialize(BufferSignal1tmp, 0)
        ArrayInitialize(BufferStoch2tmp, 0)
        ArrayInitialize(BufferSignal2tmp, 0)
        ArrayInitialize(BufferStoch3tmp, 0)
        ArrayInitialize(BufferSignal3tmp, 0)
    if (Time("", timeframe1, 1) == 0 or Time("", timeframe2, 1) == 0) or Time("", timeframe3, 1) == 0:
        return 0
    bars1 = (rates_total if (timeframe1 == Period()) else Bars(None, timeframe1))
    bars2 = (rates_total if (timeframe2 == Period()) else Bars(None, timeframe2))
    bars3 = (rates_total if (timeframe3 == Period()) else Bars(None, timeframe3))
    count1 = (fmin(bars1, rates_total) if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_sto1, MAIN_LINE, 0, count1, BufferStoch1tmp)
    if copied != count1:
        return 0
    copied = CopyBuffer(handle_sto1, SIGNAL_LINE, 0, count1, BufferSignal1tmp)
    if copied != count1:
        return 0
    count2 = (fmin(bars2, rates_total) if (limit > 1) else 1)
    copied = CopyBuffer(handle_sto2, MAIN_LINE, 0, count2, BufferStoch2tmp)
    if copied != count2:
        return 0
    copied = CopyBuffer(handle_sto2, SIGNAL_LINE, 0, count2, BufferSignal2tmp)
    if copied != count2:
        return 0
    count3 = (fmin(bars3, rates_total) if (limit > 1) else 1)
    copied = CopyBuffer(handle_sto3, MAIN_LINE, 0, count3, BufferStoch3tmp)
    if copied != count3:
        return 0
    copied = CopyBuffer(handle_sto3, SIGNAL_LINE, 0, count3, BufferSignal3tmp)
    if copied != count3:
        return 0
    for i in range(limit, 0 - 1, -1):
        DataConversion(rates_total, "", timeframe1, i, BufferStoch1tmp, BufferStoch1, InpDrawMode)
        DataConversion(rates_total, "", timeframe1, i, BufferSignal1tmp, BufferSignal1, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferStoch2tmp, BufferStoch2, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferSignal2tmp, BufferSignal2, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferStoch3tmp, BufferStoch3, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferSignal3tmp, BufferSignal3, InpDrawMode)
    for i in range(limit, 0 - 1, -1):
        BufferAvgSto[i] = (BufferStoch1[i] + BufferStoch2[i] + BufferStoch3[i]) / 3.0
        BufferAvgSig[i] = (BufferSignal1[i] + BufferSignal2[i] + BufferSignal3[i]) / 3.0
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


class Ind3TFStochasticAverage(_MQL5Indicator):
    name = '3TF_Stochastic_Average'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriodK': 5,  # Stochastic %K period
        'InpPeriodD': 3,  # Stochastic %D period
        'InpSlowing': 3,  # Stochastic Slowing
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
        'InpTimeframe1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # First Stochastic timeframe
        'InpTimeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Second Stochastic timeframe
        'InpTimeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Third Stochastic timeframe
        'InpShowSto1': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show first Stochastic
        'InpShowSto2': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show second Stochastic
        'InpShowSto3': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show third Stochastic
    }

