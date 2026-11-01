"""histvolatility_htf — converted from MQL5: MQL5 Indicators/HistVolatility_HTF/histvolatility_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 8388736, 13749760]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [], 'description': [], 'name': 'histvolatility_htf', 'source': 'MQL5 Indicators/HistVolatility_HTF/histvolatility_htf.mq5', 'folder': 'HistVolatility_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Scale', 'py': 'Scale', 'param': 'Scale', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Trading_Day_In_Year', 'py': 'Trading_Day_In_Year', 'param': 'Trading_Day_In_Year', 'type': 'int', 'default': 365, 'label': '', 'sinput': False}, {'mql': 'Percent', 'py': 'Percent', 'param': 'Percent', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'Coeff', 'py': 'Coeff', 'param': 'Coeff', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Scale_
S1_ = 1
S2_ = 2
S3_ = 3
_enum('Scale_', {1: 'S1_', 2: 'S2_', 3: 'S3_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
Per = _input('Per', 21)
Scale = _input('Scale', S3_)
Trading_Day_In_Year = _input('Trading_Day_In_Year', 365)
Percent = _input('Percent', 100)
Coeff = _input('Coeff', 1.0)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора HistVolatility не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'HistVolatility' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol_, TimeFrame, 'HistVolatility', Per, Scale, Trading_Day_In_Year, Percent, Coeff, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора HistVolatility')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'HistVolatility')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
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
        IndBuffer[bar] = EMPTY_VALUE
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, IndTime) <= 0:
            return 0
        if time[bar] >= IndTime[0] and time[bar + 1] < IndTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 1, Ind) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 1, _DT(time[bar]), 1, Col) <= 0:
                return 0
            IndBuffer[bar] = Ind[0]
            ColorIndBuffer[bar] = Col[0]
        else:
            IndBuffer[bar] = IndBuffer[bar + 1]
            ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HistvolatilityHtf(_MQL5Indicator):
    name = 'histvolatility_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'Per': 21,
        'Scale': _Choice({1: '1', 2: '2', 3: '3'}, default=3),
        'Trading_Day_In_Year': 365,
        'Percent': 100,
        'Coeff': 1.0,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

