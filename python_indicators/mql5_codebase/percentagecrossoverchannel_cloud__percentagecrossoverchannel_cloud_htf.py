"""PercentageCrossoverChannel_Cloud — converted from MQL5: MQL5 Indicators/PercentageCrossoverChannel_Cloud_HTF/PercentageCrossoverChannel_Cloud.mq5

Copyright: Copyright © 2009, Vic2008; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Vic2008', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1}, 'colors': {1: [64636], 2: [13353215], 3: [32768], 4: [16711680], 5: [16711935]}, 'widths': {3: 1, 4: 1, 5: 1}, 'styles': {3: 0, 4: 0, 5: 0}, 'labels': {1: 'Upper Cloud', 2: 'Lower Cloud', 3: 'Upper PC Channel', 4: 'Middle PC Channel', 5: 'Lower PC Channel'}, 'levels': [], 'description': [], 'name': 'PercentageCrossoverChannel_Cloud', 'source': 'MQL5 Indicators/PercentageCrossoverChannel_Cloud_HTF/PercentageCrossoverChannel_Cloud.mq5', 'folder': 'PercentageCrossoverChannel_Cloud_HTF', 'inputs': [{'mql': 'percent', 'py': 'percent', 'param': 'percent', 'type': 'double', 'default': 1.0, 'label': 'процентное отклонение цены от предыдущего значения индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
percent = _input('percent', 1.0)  # процентное отклонение цены от предыдущего значения индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpperBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
UpBuffer1 = Arr(0, 0.0)
UpBuffer2 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
DnBuffer2 = Arr(0, 0.0)
plusvar = 0.0
minusvar = 0.0
min_rates_total = 0

def OnInit():
    global min_rates_total, minusvar, plusvar
    min_rates_total = 2
    var1 = percent / 100
    plusvar = 1 + var1
    minusvar = 1 - var1
    SetIndexBuffer(0, UpBuffer2, INDICATOR_DATA)
    SetIndexBuffer(1, UpBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, DnBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, DnBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(6, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Percentage Crossover Channel(percent = ', percent, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    bar1 = 0
    if prev_calculated == 0:
        first = 1 + begin
        MiddleBuffer[first - 1] = price[first - 1]
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + begin)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        bar1 = bar - 1
        if (price[bar] * minusvar) > MiddleBuffer[bar1]:
            MiddleBuffer[bar] = price[bar] * minusvar
        else:
            if (price[bar] * plusvar) < MiddleBuffer[bar1]:
                MiddleBuffer[bar] = price[bar] * plusvar
            else:
                MiddleBuffer[bar] = MiddleBuffer[bar1]
        DnBuffer1[bar] = MiddleBuffer[bar]
        UpBuffer1[bar] = DnBuffer1[bar]
        UpBuffer2[bar] = MiddleBuffer[bar] + ((MiddleBuffer[bar] / 100) * percent)
        UpperBuffer[bar] = UpBuffer2[bar]
        DnBuffer2[bar] = MiddleBuffer[bar] - ((MiddleBuffer[bar] / 100) * percent)
        LowerBuffer[bar] = DnBuffer2[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PercentageCrossoverChannelCloud(_MQL5Indicator):
    name = 'PercentageCrossoverChannel_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'percent': 1.0,  # процентное отклонение цены от предыдущего значения индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

