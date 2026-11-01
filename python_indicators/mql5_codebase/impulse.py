"""impulse — converted from MQL5: MQL5 Indicators/Impulse/impulse.mq5

Copyright: Copyright © 2006, Gep; Link: http://www.arkworldmarket.ru/forum/showthread.php?t=966&page=2&pp=10; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Gep', 'link': 'http://www.arkworldmarket.ru/forum/showthread.php?t=966&page=2&pp=10', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Impulse'}, 'levels': [0.0], 'description': [], 'name': 'impulse', 'source': 'MQL5 Indicators/Impulse/impulse.mq5', 'folder': 'Impulse', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 14, 'label': 'Period of calculation', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 14)  # Period of calculation
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
LenPoint = 0.0
min_rates_total = 0
Len = 0

def OnInit():
    global Len, LenPoint, min_rates_total
    min_rates_total = _int(Length + 1)
    LenPoint = Length * Point()
    Len = _int(Length - 1)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'Impulse(', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dif = 0.0
        for i in range(bar - Len, bar + 1):
            dif += close[i] - open[i]
        IndBuffer[bar] = MathRound(_fdiv(dif, LenPoint))
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Impulse(_MQL5Indicator):
    name = 'impulse'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 14,  # Period of calculation
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

