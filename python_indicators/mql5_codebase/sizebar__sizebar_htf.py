"""SizeBar — converted from MQL5: MQL5 Indicators/SizeBar_HTF/SizeBar.mq5

Copyright: Copyright © 2011, zfs; Link: vasbsm@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, zfs', 'link': 'vasbsm@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [16748574]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'SizeBar'}, 'levels': [], 'description': [], 'name': 'SizeBar', 'source': 'MQL5 Indicators/SizeBar_HTF/SizeBar.mq5', 'folder': 'SizeBar_HTF', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SizeBar')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    max_ = 0.0
    x = 0.0
    y = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        x = _fdiv(high[bar] - close[bar - 1], Point()) - spread[bar]
        y = _fdiv(close[bar - 1] - low[bar], Point()) - spread[bar]
        if x > y:
            max_ = x
        else:
            max_ = y
        max_ = MathMax(max_, 0)
        IndBuffer[bar] = max_
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SizeBar(_MQL5Indicator):
    name = 'SizeBar'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

