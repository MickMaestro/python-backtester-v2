"""ForceTrend — converted from MQL5: MQL5 Indicators/ForceTrend_HTF/ForceTrend.mq5

Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_maximum': 1.1, 'indicator_minimum': 0.0}, 'types': {1: 10}, 'colors': {1: [16748574, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ForceTrend'}, 'levels': [], 'description': [], 'name': 'ForceTrend', 'source': 'MQL5 Indicators/ForceTrend_HTF/ForceTrend.mq5', 'folder': 'ForceTrend_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 13, 'label': 'Период для поиска экстремумов', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 13)  # Период для поиска экстремумов
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(Length) + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'ForceTrend(', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Force1_prev, _s_OnCalculate_Ind_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Ind = 0.0
    Force1 = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        _s_OnCalculate_Ind_prev = 0.0
        _s_OnCalculate_Force1_prev = 0.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        barx = rates_total - 1 - bar
        high1 = high[ArrayMaximum(high, barx, Length)]
        low1 = low[ArrayMinimum(low, barx, Length)]
        Avrg = (high[barx] + low[barx]) / 2.0
        Res = high1 - low1
        if Res:
            Force1 = (0.66 * (_fdiv(Avrg - low1, Res) - 0.5)) + (0.67 * _s_OnCalculate_Force1_prev)
        else:
            Force1 = (0.67 * _s_OnCalculate_Force1_prev) + -0.33
        Force1 = MathMin(MathMax(Force1, -0.999), 0.999)
        Res = 1 - Force1
        if Res:
            Ind = (MathLog(_fdiv(Force1 + 1.0, Res)) / 2.0) + (_s_OnCalculate_Ind_prev / 2.0)
        else:
            Ind = (_s_OnCalculate_Ind_prev / 2.0) + 0.5
        IndBuffer[bar] = 1.0
        if Ind < 0:
            ColorIndBuffer[bar] = 1.0
        elif Ind > 0:
            ColorIndBuffer[bar] = 0.0
        else:
            ColorIndBuffer[bar] = ColorIndBuffer[bar - 1]
        if bar < (rates_total - 1):
            _s_OnCalculate_Force1_prev = Force1
            _s_OnCalculate_Ind_prev = Ind
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Ind_prev = 0.0
_s_OnCalculate_Force1_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ForceTrend(_MQL5Indicator):
    name = 'ForceTrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 13,  # Период для поиска экстремумов
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (0.0, 1.1)

