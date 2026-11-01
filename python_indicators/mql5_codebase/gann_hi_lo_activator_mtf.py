"""Gann_Hi_Lo_Activator_MTF — converted from MQL5: MQL5 Indicators/Gann_Hi_Lo_Activator_MTF/Gann_Hi_Lo_Activator_MTF.mq5

Multi timeframe Gann Hi Lo Activator indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 18, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3329330], 2: [16760576], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'GHLA1', 2: 'GHLA2', 3: 'GHLA3'}, 'levels': [], 'description': ['Multi timeframe Gann Hi Lo Activator indicator'], 'name': 'Gann_Hi_Lo_Activator_MTF', 'source': 'MQL5 Indicators/Gann_Hi_Lo_Activator_MTF/Gann_Hi_Lo_Activator_MTF.mq5', 'folder': 'Gann_Hi_Lo_Activator_MTF', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'GHLA period', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}, {'mql': 'InpTimeframe1', 'py': 'InpTimeframe1', 'param': 'InpTimeframe1', 'type': 'int', 'default': 16385, 'label': 'First GHLA timeframe', 'sinput': False}, {'mql': 'InpTimeframe2', 'py': 'InpTimeframe2', 'param': 'InpTimeframe2', 'type': 'int', 'default': 16388, 'label': 'Second GHLA timeframe', 'sinput': False}, {'mql': 'InpTimeframe3', 'py': 'InpTimeframe3', 'param': 'InpTimeframe3', 'type': 'int', 'default': 16408, 'label': 'Third GHLA timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # GHLA period
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
InpTimeframe1 = _input('InpTimeframe1', PERIOD_H1)  # First GHLA timeframe
InpTimeframe2 = _input('InpTimeframe2', PERIOD_H4)  # Second GHLA timeframe
InpTimeframe3 = _input('InpTimeframe3', PERIOD_D1)  # Third GHLA timeframe
BufferGHLA1 = Arr(0, 0.0)
BufferGHLA2 = Arr(0, 0.0)
BufferGHLA3 = Arr(0, 0.0)
BufferGHLA1tmp = Arr(0, 0.0)
BufferGHLA2tmp = Arr(0, 0.0)
BufferGHLA3tmp = Arr(0, 0.0)
BufferDir1 = Arr(0, 0.0)
BufferDir2 = Arr(0, 0.0)
BufferDir3 = Arr(0, 0.0)
BufferMAH1 = Arr(0, 0.0)
BufferMAL1 = Arr(0, 0.0)
BufferMAH2 = Arr(0, 0.0)
BufferMAL2 = Arr(0, 0.0)
BufferMAH3 = Arr(0, 0.0)
BufferMAL3 = Arr(0, 0.0)
BufferClose1 = Arr(0, 0.0)
BufferClose2 = Arr(0, 0.0)
BufferClose3 = Arr(0, 0.0)
timeframe1 = 0
timeframe2 = 0
timeframe3 = 0
period_ghla = 0
handle_mah1 = 0
handle_mal1 = 0
handle_mah2 = 0
handle_mal2 = 0
handle_mah3 = 0
handle_mal3 = 0
handle_cls1 = 0
handle_cls2 = 0
handle_cls3 = 0

def OnInit():
    global handle_cls1, handle_cls2, handle_cls3, handle_mah1, handle_mah2, handle_mah3, handle_mal1, handle_mal2, handle_mal3, period_ghla, timeframe1, timeframe2, timeframe3
    EventSetTimer(90)
    period_ghla = (1 if (InpPeriod < 1) else InpPeriod)
    timeframe1 = (InpTimeframe1 if (InpTimeframe1 > Period()) else Period())
    timeframe2 = (InpTimeframe2 if (InpTimeframe2 > Period()) else Period())
    timeframe3 = (InpTimeframe3 if (InpTimeframe3 > Period()) else Period())
    SetIndexBuffer(0, BufferGHLA1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferGHLA2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferGHLA3, INDICATOR_DATA)
    SetIndexBuffer(3, BufferGHLA1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferGHLA2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferGHLA3tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMAH1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferMAL1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMAH2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMAL2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferMAH3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferMAL3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferDir1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferDir2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferDir3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, BufferClose1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, BufferClose2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, BufferClose3, INDICATOR_CALCULATIONS)
    label = TimeframeToString(timeframe1) + ',' + TimeframeToString(timeframe2) + ',' + TimeframeToString(timeframe3) + ' Gann Hi Lo Activator(' + _str(period_ghla) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframe1) + ' GHLA(' + _str(period_ghla) + ')')
    PlotIndexSetString(1, PLOT_LABEL, TimeframeToString(timeframe2) + ' GHLA(' + _str(period_ghla) + ')')
    PlotIndexSetString(2, PLOT_LABEL, TimeframeToString(timeframe3) + ' GHLA(' + _str(period_ghla) + ')')
    ArraySetAsSeries(BufferGHLA1, True)
    ArraySetAsSeries(BufferGHLA2, True)
    ArraySetAsSeries(BufferGHLA3, True)
    ArraySetAsSeries(BufferGHLA1tmp, True)
    ArraySetAsSeries(BufferGHLA2tmp, True)
    ArraySetAsSeries(BufferGHLA3tmp, True)
    ArraySetAsSeries(BufferMAH1, True)
    ArraySetAsSeries(BufferMAL1, True)
    ArraySetAsSeries(BufferMAH2, True)
    ArraySetAsSeries(BufferMAL2, True)
    ArraySetAsSeries(BufferMAH3, True)
    ArraySetAsSeries(BufferMAL3, True)
    ArraySetAsSeries(BufferDir1, True)
    ArraySetAsSeries(BufferDir2, True)
    ArraySetAsSeries(BufferDir3, True)
    ArraySetAsSeries(BufferClose1, True)
    ArraySetAsSeries(BufferClose2, True)
    ArraySetAsSeries(BufferClose3, True)
    ResetLastError()
    handle_mah1 = iMA(None, timeframe1, period_ghla, 0, MODE_SMA, PRICE_HIGH)
    if handle_mah1 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe1), ' iMA(' + _str(period_ghla) + ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mal1 = iMA(None, timeframe1, period_ghla, 0, MODE_SMA, PRICE_LOW)
    if handle_mal1 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe1), ' iMA(' + _str(period_ghla) + ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mah2 = iMA(None, timeframe2, period_ghla, 0, MODE_SMA, PRICE_HIGH)
    if handle_mah2 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe2), ' iMA(' + _str(period_ghla) + ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mal2 = iMA(None, timeframe2, period_ghla, 0, MODE_SMA, PRICE_LOW)
    if handle_mal2 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe2), ' iMA(' + _str(period_ghla) + ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mah3 = iMA(None, timeframe3, period_ghla, 0, MODE_SMA, PRICE_HIGH)
    if handle_mah3 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe3), ' iMA(' + _str(period_ghla) + ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mal3 = iMA(None, timeframe3, period_ghla, 0, MODE_SMA, PRICE_LOW)
    if handle_mal3 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe3), ' iMA(' + _str(period_ghla) + ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_cls1 = iMA(None, timeframe1, 1, 0, MODE_SMA, PRICE_CLOSE)
    if handle_cls1 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe1), ' iMA(1) by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_cls2 = iMA(None, timeframe2, 1, 0, MODE_SMA, PRICE_CLOSE)
    if handle_cls2 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe2), ' iMA(1) by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_cls3 = iMA(None, timeframe3, 1, 0, MODE_SMA, PRICE_CLOSE)
    if handle_cls3 == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframe3), ' iMA(1) by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    Time("", timeframe1, 1)
    Time("", timeframe2, 1)
    Time("", timeframe3, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ghla, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferGHLA1, EMPTY_VALUE)
        ArrayInitialize(BufferGHLA2, EMPTY_VALUE)
        ArrayInitialize(BufferGHLA3, EMPTY_VALUE)
        ArrayInitialize(BufferGHLA1tmp, 0)
        ArrayInitialize(BufferGHLA2tmp, 0)
        ArrayInitialize(BufferGHLA3tmp, 0)
        ArrayInitialize(BufferMAH1, 0)
        ArrayInitialize(BufferMAL1, 0)
        ArrayInitialize(BufferMAH2, 0)
        ArrayInitialize(BufferMAL2, 0)
        ArrayInitialize(BufferMAH3, 0)
        ArrayInitialize(BufferMAL3, 0)
        ArrayInitialize(BufferDir1, 0)
        ArrayInitialize(BufferDir2, 0)
        ArrayInitialize(BufferDir3, 0)
        ArrayInitialize(BufferClose1, 0)
        ArrayInitialize(BufferClose2, 0)
        ArrayInitialize(BufferClose3, 0)
    if (Time("", timeframe1, 1) == 0 or Time("", timeframe2, 1) == 0) or Time("", timeframe3, 1) == 0:
        return 0
    bars1 = (rates_total if (timeframe1 == Period()) else Bars(None, timeframe1))
    bars2 = (rates_total if (timeframe2 == Period()) else Bars(None, timeframe2))
    bars3 = (rates_total if (timeframe3 == Period()) else Bars(None, timeframe3))
    count1 = (fmin(bars1, rates_total) if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_mah1, 0, 0, count1, BufferMAH1)
    if copied != count1:
        return 0
    copied = CopyBuffer(handle_mal1, 0, 0, count1, BufferMAL1)
    if copied != count1:
        return 0
    copied = CopyBuffer(handle_cls1, 0, 0, count1, BufferClose1)
    if copied != count1:
        return 0
    count2 = (fmin(bars2, rates_total) if (limit > 1) else 1)
    copied = CopyBuffer(handle_mah2, 0, 0, count2, BufferMAH2)
    if copied != count2:
        return 0
    copied = CopyBuffer(handle_mal2, 0, 0, count2, BufferMAL2)
    if copied != count2:
        return 0
    copied = CopyBuffer(handle_cls2, 0, 0, count2, BufferClose2)
    if copied != count2:
        return 0
    count3 = (fmin(bars3, rates_total) if (limit > 1) else 1)
    copied = CopyBuffer(handle_mah3, 0, 0, count3, BufferMAH3)
    if copied != count3:
        return 0
    copied = CopyBuffer(handle_mal3, 0, 0, count3, BufferMAL3)
    if copied != count3:
        return 0
    copied = CopyBuffer(handle_cls3, 0, 0, count3, BufferClose3)
    if copied != count3:
        return 0
    for i in range(limit, 0 - 1, -1):
        GHLA(rates_total, i, period_ghla, BufferClose1, BufferDir1, BufferMAH1, BufferMAL1, BufferGHLA1tmp)
        GHLA(rates_total, i, period_ghla, BufferClose2, BufferDir2, BufferMAH2, BufferMAL2, BufferGHLA2tmp)
        GHLA(rates_total, i, period_ghla, BufferClose3, BufferDir3, BufferMAH3, BufferMAL3, BufferGHLA3tmp)
    for i in range(limit, 0 - 1, -1):
        DataConversion(rates_total, "", timeframe1, i, BufferGHLA1tmp, BufferGHLA1, InpDrawMode)
        DataConversion(rates_total, "", timeframe2, i, BufferGHLA2tmp, BufferGHLA2, InpDrawMode)
        DataConversion(rates_total, "", timeframe3, i, BufferGHLA3tmp, BufferGHLA3, InpDrawMode)
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

def GHLA(rates_total, shift, period, buffer_close, buffer_dir, buffer_mah, buffer_mal, buffer_ghla):
    if shift > rates_total:
        return
    avgH = buffer_mah[shift]
    avgL = buffer_mal[shift]
    close = buffer_close[shift]
    if (avgH == 0 or avgL == 0) or close == 0:
        return
    sw = (1 if (close > avgH) else -1 if (close < avgL) else 0)
    buffer_dir[shift] = (sw if (sw != 0) else buffer_dir[shift + 1])
    buffer_ghla[shift] = (avgH if (buffer_dir[shift] < 0) else avgL)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GannHiLoActivatorMTF(_MQL5Indicator):
    name = 'Gann_Hi_Lo_Activator_MTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 10,  # GHLA period
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
        'InpTimeframe1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # First GHLA timeframe
        'InpTimeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Second GHLA timeframe
        'InpTimeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Third GHLA timeframe
    }

