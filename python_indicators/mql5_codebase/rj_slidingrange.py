"""rj_slidingrange — converted from MQL5: MQL5 Indicators/Rj_SlidingRange/rj_slidingrange.mq5

Copyright: Copyright © 2011,RJ Rjabkov Alexander; Link: rj-a@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011,RJ Rjabkov Alexander', 'link': 'rj-a@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 8, 3: 1}, 'colors': {1: [65280], 2: [42495, 16711680], 3: [16711935]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper Rj_SlidingRange', 2: 'Middle Rj_SlidingRange', 3: 'Lower Rj_SlidingRange'}, 'levels': [], 'description': [], 'name': 'rj_slidingrange', 'source': 'MQL5 Indicators/Rj_SlidingRange/rj_slidingrange.mq5', 'folder': 'Rj_SlidingRange', 'inputs': [{'mql': 'CalcPeriodRange', 'py': 'CalcPeriodRange', 'param': 'CalcPeriodRange', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CalcPeriodRange = _input('CalcPeriodRange', 5)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpperBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
ColorMiddleBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(CalcPeriodRange + 1)
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(1, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(MiddleBuffer, True)
    SetIndexBuffer(2, ColorMiddleBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorMiddleBuffer, True)
    SetIndexBuffer(3, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    ArraySetAsSeries(LowerBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Rj_SlidingRange(', CalcPeriodRange, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        iii = bar + _int(CalcPeriodRange) - 1
        b1 = 0.0
        b2 = 0.0
        while iii >= bar:
            b1 += High[ArrayMaximum(High, iii, CalcPeriodRange)]
            b2 += Low[ArrayMinimum(Low, iii, CalcPeriodRange)]
            iii -= 1
        UpperBuffer[bar] = b1 / CalcPeriodRange
        LowerBuffer[bar] = b2 / CalcPeriodRange
        MiddleBuffer[bar] = NormalizeDouble((UpperBuffer[bar] + LowerBuffer[bar]) / 2, Digits())
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    for bar in range(limit, 0 - 1, -1):
        if MiddleBuffer[bar + 1] < MiddleBuffer[bar]:
            ColorMiddleBuffer[bar] = 1.0
        if MiddleBuffer[bar + 1] > MiddleBuffer[bar]:
            ColorMiddleBuffer[bar] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RjSlidingrange(_MQL5Indicator):
    name = 'rj_slidingrange'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CalcPeriodRange': 5,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

