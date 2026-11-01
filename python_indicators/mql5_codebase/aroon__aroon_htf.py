"""aroon — converted from MQL5: MQL5 Indicators/Aroon_HTF/aroon.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65280], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'BullsAroon', 2: 'BearsAroon'}, 'levels': [70.0, 50.0, 30.0], 'description': [], 'name': 'aroon', 'source': 'MQL5 Indicators/Aroon_HTF/aroon.mq5', 'folder': 'Aroon_HTF', 'inputs': [{'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'int', 'default': 9, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'AroonShift', 'py': 'AroonShift', 'param': 'AroonShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AroonPeriod = _input('AroonPeriod', 9)  # Период индикатора
AroonShift = _input('AroonShift', 0)  # Сдвиг индикатора по горизонтали в барах
BullsAroonBuffer = Arr(0, 0.0)
BearsAroonBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BullsAroonBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, AroonShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, AroonPeriod)
    PlotIndexSetString(0, PLOT_LABEL, 'BearsAroon')
    SetIndexBuffer(1, BearsAroonBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, AroonShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, AroonPeriod)
    PlotIndexSetString(1, PLOT_LABEL, 'BullsAroon')
    shortname = Box("")
    StringConcatenate(shortname, 'Aroon(', AroonPeriod, ', ', AroonShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

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

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (AroonPeriod - 1):
        return 0
    first = 0
    bar = 0
    BULLS = 0.0
    BEARS = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = AroonPeriod - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        BULLS = 100 - (((bar - iHighest_u(high, AroonPeriod, bar) + 0.5) * 100) / AroonPeriod)
        BEARS = 100 - (((bar - iLowest_u(low, AroonPeriod, bar) + 0.5) * 100) / AroonPeriod)
        BullsAroonBuffer[bar] = BULLS
        BearsAroonBuffer[bar] = BEARS
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Aroon(_MQL5Indicator):
    name = 'aroon'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AroonPeriod': 9,  # Период индикатора
        'AroonShift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

