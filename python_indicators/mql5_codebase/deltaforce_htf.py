"""DeltaForce_HTF — converted from MQL5: MQL5 Indicators/DeltaForce_HTF/DeltaForce_HTF.mq5

Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [16711680, 16748574], 2: [16711935, 8388736]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'High', 2: 'Low'}, 'levels': [], 'description': [], 'name': 'DeltaForce_HTF', 'source': 'MQL5 Indicators/DeltaForce_HTF/DeltaForce_HTF.mq5', 'folder': 'DeltaForce_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer1 = Arr(0, 0.0)
ColorIndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
ColorIndBuffer2 = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора DeltaForce не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'DeltaForce' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol_, TimeFrame, 'DeltaForce', 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора DeltaForce')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer1, True)
    SetIndexBuffer(1, ColorIndBuffer1, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer1, True)
    SetIndexBuffer(2, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer2, True)
    SetIndexBuffer(3, ColorIndBuffer2, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer2, True)
    shortname = Box("")
    StringConcatenate(shortname, 'DeltaForce(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    Ind = Arr(1, 0.0, dyn=False)
    Col = Arr(1, 0.0, dyn=False)
    limit = 0
    bar = 0
    IndTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer1[bar] = 0.0
        IndBuffer2[bar] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, IndTime) <= 0:
            return 0
        if time[bar] >= IndTime[0] and time[bar + 1] < IndTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 1, Ind) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 1, _DT(time[bar]), 1, Col) <= 0:
                return 0
            IndBuffer1[bar] = Ind[0]
            ColorIndBuffer1[bar] = Col[0]
            if CopyBuffer(Ind_Handle, 2, _DT(time[bar]), 1, Ind) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 3, _DT(time[bar]), 1, Col) <= 0:
                return 0
            IndBuffer2[bar] = Ind[0]
            ColorIndBuffer2[bar] = Col[0]
        else:
            IndBuffer1[bar] = IndBuffer1[bar + 1]
            ColorIndBuffer1[bar] = ColorIndBuffer1[bar + 1]
            IndBuffer2[bar] = IndBuffer2[bar + 1]
            ColorIndBuffer2[bar] = ColorIndBuffer2[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DeltaForceHTF(_MQL5Indicator):
    name = 'DeltaForce_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

