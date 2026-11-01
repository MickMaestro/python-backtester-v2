"""WmiVol — converted from MQL5: MQL5 Indicators/WmiVol_HTF/WmiVol.mq5

Copyright: Copyright 2014, Murad Ismayilov; Link: http://www.mql4.com/ru/users/wmlab; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, Murad Ismayilov', 'link': 'http://www.mql4.com/ru/users/wmlab', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_maximum': 1.1, 'indicator_minimum': 0.0}, 'types': {1: 10}, 'colors': {1: [16748574, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'WmiVol'}, 'levels': [], 'description': [], 'name': 'WmiVol', 'source': 'MQL5 Indicators/WmiVol_HTF/WmiVol.mq5', 'folder': 'WmiVol_HTF', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
barVols = Arr(0, 0.0)
avgVol = 0.0
barsInDay = 0
barCounts = Arr(0, 0)

def OnInit():
    global barsInDay, min_rates_total
    if Period() > PERIOD_H12:
        Print('Период графика не может быть больше H12!')
        return INIT_FAILED
    barsInDay = _idiv(1440, _idiv(PeriodSeconds(PERIOD_CURRENT), 60))
    if not barsInDay:
        return INIT_FAILED
    min_rates_total = barsInDay
    if ArrayResize(barCounts, barsInDay) < barsInDay:
        Print('Не удалось распределить память под массив barCounts[]')
        return INIT_FAILED
    if ArrayResize(barVols, barsInDay) < barsInDay:
        Print('Не удалось распределить память под массив barVols[]')
        return INIT_FAILED
    ArrayInitialize(barCounts, 0)
    ArrayInitialize(barVols, 0.0)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global avgVol
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        bar = rates_total - 1
        for bar in range(bar, 0, -1):
            barOfDay = iBarOfDay(time[bar])
            barVols[barOfDay] += high[bar] - low[bar]
            barCounts[barOfDay] += 1
        else:
            bar = _range_end(bar, 0, -1)
        bar = 0
        for bar in range(bar, barsInDay):
            if barCounts[bar]:
                barVols[bar] = _fdiv(barVols[bar], barCounts[bar])
        else:
            bar = _range_end(bar, barsInDay, 1)
        minVol = barVols[ArrayMinimum(barVols)]
        maxVol = barVols[ArrayMaximum(barVols)]
        avgVol = 0.0
        bar = 0
        for bar in range(bar, barsInDay):
            if maxVol > minVol:
                avgVol += _setitem(barVols, bar, _fdiv(barVols[bar] - minVol, maxVol - minVol))
        else:
            bar = _range_end(bar, barsInDay, 1)
        avgVol = _fdiv(avgVol, barsInDay)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        barOfDay = iBarOfDay(time[bar])
        vol = barVols[barOfDay]
        IndBuffer[bar] = vol
        if vol >= avgVol:
            ColorIndBuffer[bar] = 0.0
        else:
            ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def iBarOfDay(timeOpenBar):
    minutesInPeriod = _idiv(PeriodSeconds(), 60)
    minutesSinceMidnight = MathMod(_idiv(timeOpenBar, 60), 1440)
    barsSinceMidnight = _int(MathFloor(_fdiv(minutesSinceMidnight, minutesInPeriod)))
    return barsSinceMidnight


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WmiVol(_MQL5Indicator):
    name = 'WmiVol'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }
    y_range = (0.0, 1.1)

