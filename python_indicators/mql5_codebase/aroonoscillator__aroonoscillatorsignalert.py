"""AroonOscillator — converted from MQL5: MQL5 Indicators/AroonOscillatorSignAlert/AroonOscillator.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'AroonOscillator'}, 'levels': [50.0, 0.0, -50.0], 'description': [], 'name': 'AroonOscillator', 'source': 'MQL5 Indicators/AroonOscillatorSignAlert/AroonOscillator.mq5', 'folder': 'AroonOscillatorSignAlert', 'inputs': [{'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'int', 'default': 9, 'label': 'период индикатора', 'sinput': False}, {'mql': 'AroonShift', 'py': 'AroonShift', 'param': 'AroonShift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AroonPeriod = _input('AroonPeriod', 9)  # период индикатора
AroonShift = _input('AroonShift', 0)  # сдвиг индикатора по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)

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
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'AroonOscillator(', AroonPeriod, ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, AroonShift)
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < AroonPeriod:
        return 0
    first = 0
    bar = 0
    highest = 0
    lowest = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = AroonPeriod - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        highest = iHighest_u(high, AroonPeriod, bar)
        lowest = iLowest_u(low, AroonPeriod, bar)
        ExtLineBuffer[bar] = _idiv(100 * (highest - lowest), AroonPeriod)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AroonOscillator(_MQL5Indicator):
    name = 'AroonOscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AroonPeriod': 9,  # период индикатора
        'AroonShift': 0,  # сдвиг индикатора по горизонтали в барах
    }

