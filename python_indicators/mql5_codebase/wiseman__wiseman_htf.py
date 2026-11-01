"""Wiseman — converted from MQL5: MQL5 Indicators/Wiseman_HTF/Wiseman.mq5

Copyright: Copyright © 2005, Pavel Kulko; Link: polk@alba.dp.ua; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Pavel Kulko', 'link': 'polk@alba.dp.ua', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [3329330, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Wiseman'}, 'levels': [], 'description': [], 'name': 'Wiseman', 'source': 'MQL5 Indicators/Wiseman_HTF/Wiseman.mq5', 'folder': 'Wiseman_HTF', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    shortname = Box("")
    StringConcatenate(shortname, 'Wiseman(', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    median = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        UpBuffer[bar] = 0.0
        DnBuffer[bar] = 0.0
        median = (high[bar] + low[bar]) / 2.0
        if low[bar] < low[bar - 1] and close[bar] > median:
            UpBuffer[bar] = high[bar]
            DnBuffer[bar] = low[bar]
            ColorBuffer[bar] = 1.0
        if high[bar] > high[bar - 1] and close[bar] < median:
            UpBuffer[bar] = high[bar]
            DnBuffer[bar] = low[bar]
            ColorBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wiseman(_MQL5Indicator):
    name = 'Wiseman'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

