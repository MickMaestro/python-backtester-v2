"""WmiVol_Pluse — converted from MQL5: MQL5 Indicators/WmiVol_Pluse/WmiVol_Pluse.mq5

Copyright: Copyright 2014, Murad Ismayilov; Link: http://www.mql4.com/ru/users/wmlab; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, Murad Ismayilov', 'link': 'http://www.mql4.com/ru/users/wmlab', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_maximum': 1.1, 'indicator_minimum': 0.0}, 'types': {1: 10}, 'colors': {1: [16748574, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'WmiVol_Pluse'}, 'levels': [], 'description': [], 'name': 'WmiVol_Pluse', 'source': 'MQL5 Indicators/WmiVol_Pluse/WmiVol_Pluse.mq5', 'folder': 'WmiVol_Pluse', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16408, 'label': 'Таймфрейм', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_D1)  # Таймфрейм
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
barVols = Arr(0, 0.0)
avgVol = 0.0
barsInDay = 0
barCounts = Arr(0, 0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global barsInDay, min_rates_total
    if Period() >= TimeFrame:
        Print('OnInit' + '(): Период графика должен быть меньше, чем ' + GetStringTimeframe(TimeFrame))
        Print('OnInit' + '(): Следует уменьшить период графика либо увеличить значение входного параметра индикатора <<TimeFrame>>!')
        return INIT_FAILED
    barsInDay = _idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT))
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
    shortname = Box("")
    StringConcatenate(shortname, 'WmiVol_Pluse(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
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
    minutesSinceMidnight = MathMod(_idiv(timeOpenBar, 60), _idiv(PeriodSeconds(TimeFrame), 60))
    barsSinceMidnight = _int(MathFloor(_fdiv(minutesSinceMidnight, minutesInPeriod)))
    return barsSinceMidnight


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WmiVolPluse(_MQL5Indicator):
    name = 'WmiVol_Pluse'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Таймфрейм
    }
    y_range = (0.0, 1.1)

