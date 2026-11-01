"""extremline — converted from MQL5: MQL5 Indicators/ExtremLine/extremline.mq5

Copyright: Copyright © 2014 Serkov Alexandr; Link: serkov-alexandr@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014 Serkov Alexandr', 'link': 'serkov-alexandr@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65280], 2: [255]}, 'widths': {1: 4, 2: 4}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bulls ExtremLine', 2: 'Bears ExtremLine'}, 'levels': [], 'description': [], 'name': 'extremline', 'source': 'MQL5 Indicators/ExtremLine/extremline.mq5', 'folder': 'ExtremLine', 'inputs': [{'mql': 'IndPeriod', 'py': 'IndPeriod', 'param': 'IndPeriod', 'type': 'uint', 'default': 10, 'label': 'период индикатора', 'sinput': False}, {'mql': 'IndShift', 'py': 'IndShift', 'param': 'IndShift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
IndPeriod = _input('IndPeriod', 10)  # период индикатора
IndShift = _input('IndShift', 0)  # сдвиг индикатора по горизонтали в барах
BullsIndBuffer = Arr(0, 0.0)
BearsIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(IndPeriod)
    SetIndexBuffer(0, BullsIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, IndShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, BearsIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, IndShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'ExtremLine(', IndPeriod, ', ', IndShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    dir = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if high[bar] > high[bar - IndPeriod]:
            dir = True
        if low[bar] < low[bar - IndPeriod]:
            dir = False
        if dir == True:
            BullsIndBuffer[bar] = high[bar]
            BullsIndBuffer[bar - 1] = high[bar - 1]
            BearsIndBuffer[bar] = 0.0
        else:
            BearsIndBuffer[bar] = low[bar]
            BearsIndBuffer[bar - 1] = low[bar - 1]
            BullsIndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Extremline(_MQL5Indicator):
    name = 'extremline'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IndPeriod': 10,  # период индикатора
        'IndShift': 0,  # сдвиг индикатора по горизонтали в барах
    }

