"""FloatPivot — converted from MQL5: MQL5 Indicators/FloatPivot_HTF/FloatPivot.mq5

Copyright: Copyright © 2006, Nick A. Zhilin; Link: rebus@dialup.etr.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Nick A. Zhilin', 'link': 'rebus@dialup.etr.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 7}, 'colors': {1: [10025880], 2: [3329330], 3: [13458026], 4: [16711935], 5: [15631086]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper Cloud', 2: 'Upper FloatPivot', 3: 'Middle FloatPivot', 4: 'Lower FloatPivot', 5: 'Lower Cloud'}, 'levels': [], 'description': [], 'name': 'FloatPivot', 'source': 'MQL5 Indicators/FloatPivot_HTF/FloatPivot.mq5', 'folder': 'FloatPivot_HTF', 'inputs': [{'mql': 'IPeriod', 'py': 'IPeriod', 'param': 'IPeriod', 'type': 'int', 'default': 100, 'label': 'Период поиска экстремумов', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
IPeriod = _input('IPeriod', 100)  # Период поиска экстремумов
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtUp1Buffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtDn1Buffer = Arr(0, 0.0)
ExtDn2Buffer = Arr(0, 0.0)
min_rates_total = 0

def iHighest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Неверное значение в функции iHighest, startPos = ', startPos)
        return 0
    if (startPos - count) < 0:
        count = startPos
    max_ = array[startPos]
    for i in range(startPos, startPos - count, -1):
        if array[i] > max_:
            index = i
            max_ = array[i]
    return index

def iLowest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Неверное значение в функции iLowest, startPos = ', startPos)
        return 0
    if (startPos - count) < 0:
        count = startPos
    min_ = array[startPos]
    for i in range(startPos, startPos - count, -1):
        if array[i] < min_:
            index = i
            min_ = array[i]
    return index

def OnInit():
    global min_rates_total
    min_rates_total = MathMax(3, IPeriod)
    SetIndexBuffer(0, ExtUp1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(2, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    SetIndexBuffer(3, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    SetIndexBuffer(4, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    SetIndexBuffer(5, ExtDn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtDn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'FloatPivot( IPeriod = ', IPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        max_ = high[iHighest_u(high, IPeriod, bar)]
        min_ = low[iLowest_u(low, IPeriod, bar)]
        pivot = (close[bar - 1] + close[bar - 2] + close[bar - 3]) / 3
        res = (max_ + min_ + pivot) / 3
        ExtUp1Buffer[bar] = ((2 * res) - min_ + res) / 2
        ExtABuffer[bar] = ExtUp1Buffer[bar]
        ExtDn2Buffer[bar] = (res + ((2 * res) - max_)) / 2
        ExtCBuffer[bar] = ExtDn2Buffer[bar]
        ExtDn1Buffer[bar] = res
        ExtUp2Buffer[bar] = ExtDn1Buffer[bar]
        ExtBBuffer[bar] = ExtUp2Buffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FloatPivot(_MQL5Indicator):
    name = 'FloatPivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IPeriod': 100,  # Период поиска экстремумов
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

