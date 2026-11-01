"""stochastic_histogram — converted from MQL5: MQL5 Indicators/Stochastic_Histogram/stochastic_histogram.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 7, 2: 11}, 'colors': {1: [65280, 15631086], 2: [16748574, 8421504, 9639167]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'Stochastic Signal', 2: 'Stochastic_Histogram'}, 'levels': [], 'description': [], 'name': 'stochastic_histogram', 'source': 'MQL5 Indicators/Stochastic_Histogram/stochastic_histogram.mq5', 'folder': 'Stochastic_Histogram', 'inputs': [{'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
MA_Method = _input('MA_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
HighLevel = _input('HighLevel', 60)  # уровень перекупленности
LowLevel = _input('LowLevel', 40)  # уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
UpBuffer1 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
Stochastic_Handle = 0

def OnInit():
    global Stochastic_Handle, min_rates_total
    min_rates_total = KPeriod + DPeriod + Slowing
    Stochastic_Handle = iStochastic(None, 0, KPeriod, DPeriod, Slowing, MA_Method, Price_field)
    if Stochastic_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iStochastic')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpBuffer1, True)
    SetIndexBuffer(1, DnBuffer1, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer1, True)
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(3, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(4, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic_Histogram(' + _str(KPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLimeGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(Stochastic_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Stochastic_Handle, MAIN_LINE, 0, to_copy, UpBuffer) <= 0:
        return 0
    if CopyBuffer(Stochastic_Handle, MAIN_LINE, 0, to_copy, UpBuffer1) <= 0:
        return 0
    if CopyBuffer(Stochastic_Handle, SIGNAL_LINE, 0, to_copy, DnBuffer1) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        DnBuffer[bar] = 50.0
        clr = _int(1.0)
        if UpBuffer[bar] > HighLevel:
            clr = _int(0.0)
        elif UpBuffer[bar] < LowLevel:
            clr = _int(2.0)
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticHistogram(_MQL5Indicator):
    name = 'stochastic_histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'HighLevel': 60,  # уровень перекупленности
        'LowLevel': 40,  # уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

