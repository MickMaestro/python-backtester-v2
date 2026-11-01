"""Boa_ZigZag_HTF — converted from MQL5: MQL5 Indicators/Boa_ZigZag_HTF/Boa_ZigZag_HTF.mq5

Индикатор Boa_ZigZag с возможностью изменения таймфрейма во входных параметрах.
Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 9}, 'colors': {1: [13850042, 3329330]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'Boa_ZigZag_HTF'}, 'levels': [], 'description': ['Индикатор Boa_ZigZag с возможностью изменения таймфрейма во входных параметрах.'], 'name': 'Boa_ZigZag_HTF', 'source': 'MQL5 Indicators/Boa_ZigZag_HTF/Boa_ZigZag_HTF.mq5', 'folder': 'Boa_ZigZag_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
Length = _input('Length', 6)
IndBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_total = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = (_idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT)) * 2) + 1
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Boa_ZigZag', Length)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Boa_ZigZag')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(IndBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'Boa_ZigZag(', GetStringTimeframe(TimeFrame), ', ', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar, _s_OnCalculate_LastHighPos, _s_OnCalculate_LastLowPos
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ZigZag = Arr(1, 0.0, dyn=False)
    iHigh_ = Arr(1, 0.0, dyn=False)
    iLow_ = Arr(1, 0.0, dyn=False)
    limit = 0
    bar = 0
    ZigZagTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = 0
        _s_OnCalculate_LastHighPos = 0
        _s_OnCalculate_LastLowPos = 0
    else:
        limit = rates_total - prev_calculated
    _s_OnCalculate_LastHighPos += limit
    _s_OnCalculate_LastLowPos += limit
    limit += _s_OnCalculate_LastCountBar
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    IndBuffer[_s_OnCalculate_LastLowPos] = 0.0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if CopyTime(None, TimeFrame, _DT(time[bar]), 1, ZigZagTime) <= 0:
            return 0
        if CopyHigh(None, TimeFrame, _DT(time[bar]), 1, iHigh_) <= 0:
            return 0
        if CopyLow(None, TimeFrame, _DT(time[bar]), 1, iLow_) <= 0:
            return 0
        if time[bar + 1] < ZigZagTime[0] and time[bar] >= ZigZagTime[0]:
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 1, ZigZag) <= 0:
                return 0
            if ZigZag[0] and ZigZag[0] == iHigh_[0]:
                maxbar = FindMax(ZigZag[0], bar, 0, high)
                IndBuffer[maxbar] = ZigZag[0]
                _s_OnCalculate_LastHighPos = bar
            if ZigZag[0] and ZigZag[0] == iLow_[0]:
                minbar = FindMin(ZigZag[0], bar, 0, low)
                IndBuffer[minbar] = ZigZag[0]
                _s_OnCalculate_LastLowPos = bar
    else:
        bar = _range_end(bar, 0 - 1, -1)
    _s_OnCalculate_LastCountBar = MathMax(_s_OnCalculate_LastHighPos, _s_OnCalculate_LastLowPos)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if IndBuffer[bar]:
            if IndBuffer[bar] == high[bar]:
                ColorBuffer[bar] = 1.0
            if IndBuffer[bar] == low[bar]:
                ColorBuffer[bar] = 0.0
        else:
            ColorBuffer[bar] = ColorBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def FindMax(Value, start, end, Array):
    for bar in range(start, end - 1, -1):
        if Array[bar] >= Value:
            return bar
    return ArrayMaximum(Array, end, start - end)

def FindMin(Value, start, end, Array):
    for bar in range(start, end - 1, -1):
        if Array[bar] <= Value:
            return bar
    return ArrayMinimum(Array, end, start - end)

# ---- static local variables
_s_OnCalculate_LastCountBar = 0
_s_OnCalculate_LastHighPos = 0
_s_OnCalculate_LastLowPos = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BoaZigZagHTF(_MQL5Indicator):
    name = 'Boa_ZigZag_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'Length': 6,
    }

