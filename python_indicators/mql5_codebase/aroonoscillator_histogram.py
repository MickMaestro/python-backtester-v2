"""AroonOscillator_Histogram — converted from MQL5: MQL5 Indicators/AroonOscillator_Histogram/AroonOscillator_Histogram.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16776960, 16711680, 8421504, 8388736, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'AroonOscillator'}, 'levels': [], 'description': [], 'name': 'AroonOscillator_Histogram', 'source': 'MQL5 Indicators/AroonOscillator_Histogram/AroonOscillator_Histogram.mq5', 'folder': 'AroonOscillator_Histogram', 'inputs': [{'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'int', 'default': 9, 'label': 'период индикатора', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 40, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -40, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'AroonShift', 'py': 'AroonShift', 'param': 'AroonShift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AroonPeriod = _input('AroonPeriod', 9)  # период индикатора
HighLevel = _input('HighLevel', 40)  # уровень перезакупа
LowLevel = _input('LowLevel', -40)  # уровень перепроданности
AroonShift = _input('AroonShift', 0)  # сдвиг индикатора по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)
ExtColorLineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtLineBuffer, True)
    SetIndexBuffer(1, ExtColorLineBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtColorLineBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'AroonOscillator(', AroonPeriod, ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, AroonShift)
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < AroonPeriod:
        return 0
    limit = 0
    highest = 0
    lowest = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - AroonPeriod - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        highest = ArrayMaximum(High, bar, AroonPeriod)
        lowest = ArrayMinimum(Low, bar, AroonPeriod)
        ExtLineBuffer[bar] = _idiv(-100 * (highest - lowest), AroonPeriod)
        clr = _int(2.0)
        if ExtLineBuffer[bar] > HighLevel:
            clr = _int(0.0)
        elif ExtLineBuffer[bar] > 0.0:
            clr = _int(1.0)
        elif ExtLineBuffer[bar] < LowLevel:
            clr = _int(4.0)
        elif ExtLineBuffer[bar] < 0:
            clr = _int(3.0)
        ExtColorLineBuffer[bar] = clr
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AroonOscillatorHistogram(_MQL5Indicator):
    name = 'AroonOscillator_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AroonPeriod': 9,  # период индикатора
        'HighLevel': 40,  # уровень перезакупа
        'LowLevel': -40,  # уровень перепроданности
        'AroonShift': 0,  # сдвиг индикатора по горизонтали в барах
    }

