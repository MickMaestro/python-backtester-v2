"""PercentageCrossover — converted from MQL5: MQL5 Indicators/PercentageCrossover/PercentageCrossover.mq5

Copyright: Copyright © 2009, Vic2008; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Vic2008', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [14822282, 42495]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'PercentageCrossover'}, 'levels': [], 'description': [], 'name': 'PercentageCrossover', 'source': 'MQL5 Indicators/PercentageCrossover/PercentageCrossover.mq5', 'folder': 'PercentageCrossover', 'inputs': [{'mql': 'percent', 'py': 'percent', 'param': 'percent', 'type': 'double', 'default': 1.0, 'label': 'процентное отклонение цены от предыдущего значения индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
percent = _input('percent', 1.0)  # процентное отклонение цены от предыдущего значения индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
plusvar = 0.0
minusvar = 0.0
min_rates_total = 0

def OnInit():
    global min_rates_total, minusvar, plusvar
    min_rates_total = 2
    var1 = percent / 100
    plusvar = 1 + var1
    minusvar = 1 - var1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    shortname = Box("")
    StringConcatenate(shortname, 'Percentage Crossover(percent = ', percent, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    bar1 = 0
    Middle = 0.0
    if prev_calculated == 0:
        first = 1 + begin
        IndBuffer[first - 1] = price[first - 1]
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        bar1 = bar - 1
        if (price[bar] * minusvar) > IndBuffer[bar1]:
            Middle = price[bar] * minusvar
        else:
            if (price[bar] * plusvar) < IndBuffer[bar1]:
                Middle = price[bar] * plusvar
            else:
                Middle = IndBuffer[bar1]
        IndBuffer[bar] = Middle
        ColorIndBuffer[bar] = ColorIndBuffer[bar - 1]
        if Middle > IndBuffer[bar - 1]:
            ColorIndBuffer[bar] = 0.0
        if Middle < IndBuffer[bar - 1]:
            ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PercentageCrossover(_MQL5Indicator):
    name = 'PercentageCrossover'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'percent': 1.0,  # процентное отклонение цены от предыдущего значения индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

