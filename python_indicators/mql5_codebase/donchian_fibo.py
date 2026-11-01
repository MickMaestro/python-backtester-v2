"""donchian_fibo — converted from MQL5: MQL5 Indicators/Donchian Fibo/donchian_fibo.mq5

Copyright: Copyright © 2015, Guilherme Santos; Link: fishguil@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Guilherme Santos', 'link': 'fishguil@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [16711680], 2: [16760576], 3: [16776960], 4: [16777215], 5: [65535], 6: [42495], 7: [255]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 2, 5: 1, 6: 1, 7: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {1: 'Fibo 1.000', 2: 'Fibo 0.786', 3: 'Fibo 0.618', 4: 'Fibo 0.500', 5: 'Fibo 0.382', 6: 'Fibo 0.214', 7: 'Fibo 0.000'}, 'levels': [], 'description': [], 'name': 'donchian_fibo', 'source': 'MQL5 Indicators/Donchian Fibo/donchian_fibo.mq5', 'folder': 'Donchian Fibo', 'inputs': [{'mql': 'FiboPeriod', 'py': 'FiboPeriod', 'param': 'FiboPeriod', 'type': 'int', 'default': 72, 'label': 'Period of averaging', 'sinput': False}, {'mql': 'Extremes', 'py': 'Extremes', 'param': 'Extremes', 'type': 'int', 'default': 0, 'label': 'Type of extreme points', 'sinput': False}, {'mql': 'Margins', 'py': 'Margins', 'param': 'Margins', 'type': 'int', 'default': -2, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_Extrem
HIGH_LOW = 0
HIGH_LOW_OPEN = 1
HIGH_LOW_CLOSE = 2
OPEN_HIGH_LOW = 3
CLOSE_HIGH_LOW = 4
_enum('Applied_Extrem', {0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'})

# ---- inputs and global variables
FiboPeriod = _input('FiboPeriod', 72)  # Period of averaging
Extremes = _input('Extremes', HIGH_LOW)  # Type of extreme points
Margins = _input('Margins', -2)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Buffer1000 = Arr(0, 0.0)
Buffer0786 = Arr(0, 0.0)
Buffer0618 = Arr(0, 0.0)
Buffer0500 = Arr(0, 0.0)
Buffer0382 = Arr(0, 0.0)
Buffer0214 = Arr(0, 0.0)
Buffer0000 = Arr(0, 0.0)

def iHighest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Bad value in the function iHighest, startPos = ', startPos)
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
        Print('Bad value in the function iLowest, startPos = ', startPos)
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
    SetIndexBuffer(0, Buffer1000, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, FiboPeriod - 1)
    PlotIndexSetString(0, PLOT_LABEL, 'Fibo 1.000')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, Buffer0786, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, FiboPeriod - 1)
    PlotIndexSetString(1, PLOT_LABEL, 'Fibo 0.786')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, Buffer0618, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, FiboPeriod - 1)
    PlotIndexSetString(2, PLOT_LABEL, 'Fibo 0.618')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, Buffer0500, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, FiboPeriod - 1)
    PlotIndexSetString(3, PLOT_LABEL, 'Fibo 0.500')
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, Buffer0382, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, FiboPeriod - 1)
    PlotIndexSetString(4, PLOT_LABEL, 'Fibo 0.382')
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, Buffer0214, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, FiboPeriod - 1)
    PlotIndexSetString(5, PLOT_LABEL, 'Fibo 0.214')
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(6, Buffer0000, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, FiboPeriod - 1)
    PlotIndexSetString(6, PLOT_LABEL, 'Fibo 0.000')
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Donchian Fibo(Period = ', FiboPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (FiboPeriod + 1):
        return 0
    smin = 0.0
    smax = 0.0
    sdiff = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = FiboPeriod
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        _sw1 = Extremes
        if _sw1 == HIGH_LOW:
            smax = high[iHighest_u(high, FiboPeriod, bar)]
            smin = low[iLowest_u(low, FiboPeriod, bar)]
        elif _sw1 == HIGH_LOW_OPEN:
            smax = (open[iHighest_u(open, FiboPeriod, bar)] + high[iHighest_u(high, FiboPeriod, bar)]) / 2
            smin = (open[iLowest_u(open, FiboPeriod, bar)] + low[iLowest_u(low, FiboPeriod, bar)]) / 2
        elif _sw1 == HIGH_LOW_CLOSE:
            smax = (close[iHighest_u(close, FiboPeriod, bar)] + high[iHighest_u(high, FiboPeriod, bar)]) / 2
            smin = (close[iLowest_u(close, FiboPeriod, bar)] + low[iLowest_u(low, FiboPeriod, bar)]) / 2
        elif _sw1 == OPEN_HIGH_LOW:
            smax = open[iHighest_u(open, FiboPeriod, bar)]
            smin = open[iLowest_u(open, FiboPeriod, bar)]
        elif _sw1 == CLOSE_HIGH_LOW:
            smax = close[iHighest_u(close, FiboPeriod, bar)]
            smin = close[iLowest_u(close, FiboPeriod, bar)]
        sdiff = smax - smin
        Buffer1000[bar] = smax
        Buffer0786[bar] = smin + (sdiff * 0.786)
        Buffer0618[bar] = smin + (sdiff * 0.618)
        Buffer0500[bar] = smin + (sdiff * 0.5)
        Buffer0382[bar] = smin + (sdiff * 0.382)
        Buffer0214[bar] = smin + (sdiff * 0.214)
        Buffer0000[bar] = smin
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianFibo(_MQL5Indicator):
    name = 'donchian_fibo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FiboPeriod': 72,  # Period of averaging
        'Extremes': _Choice({0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'}, default=0),  # Type of extreme points
        'Margins': -2,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

