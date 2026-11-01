"""notches — converted from MQL5: MQL5 Indicators/Notches/notches.mq5

Copyright: Copyright © 2014 Serkov Alexandr; Link: serkov-alexandr@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014 Serkov Alexandr', 'link': 'serkov-alexandr@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16760576], 2: [16711935], 3: [65280], 4: [255]}, 'widths': {1: 4, 2: 4, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Bulls Notches 1', 2: 'Bears Notches 1', 3: 'Bulls Notches 1', 4: 'Bears Notches 1'}, 'levels': [], 'description': [], 'name': 'notches', 'source': 'MQL5 Indicators/Notches/notches.mq5', 'folder': 'Notches', 'inputs': [{'mql': 'IndShift', 'py': 'IndShift', 'param': 'IndShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
IndShift = _input('IndShift', 0)  # Сдвиг индикатора по горизонтали в барах
BullsIndBuffer1 = Arr(0, 0.0)
BearsIndBuffer1 = Arr(0, 0.0)
BullsIndBuffer2 = Arr(0, 0.0)
BearsIndBuffer2 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, BullsIndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, IndShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, BearsIndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, IndShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(2, BullsIndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, IndShift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, BearsIndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, IndShift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'Notches(', IndShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_x_, _s_OnCalculate_y_
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    x = 0
    y = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        _s_OnCalculate_x_ = 0
        _s_OnCalculate_y_ = 0
    else:
        first = prev_calculated - 1
    x = _s_OnCalculate_x_
    y = _s_OnCalculate_y_
    bar = first
    for bar in range(bar, rates_total):
        BearsIndBuffer1[bar] = 0.0
        BullsIndBuffer1[bar] = 0.0
        BearsIndBuffer2[bar] = 0.0
        BullsIndBuffer2[bar] = 0.0
        if high[bar] > high[bar - 1]:
            if x == 1:
                BullsIndBuffer1[bar] = high[bar]
                BullsIndBuffer1[bar - 1] = high[bar - 1]
                x = 2
            else:
                BullsIndBuffer2[bar] = high[bar]
                BullsIndBuffer2[bar - 1] = high[bar - 1]
                x = 1
        if low[bar] < low[bar - 1]:
            if y == 1:
                BearsIndBuffer1[bar] = low[bar]
                BearsIndBuffer1[bar - 1] = low[bar - 1]
                y = 2
            else:
                BearsIndBuffer2[bar] = low[bar]
                BearsIndBuffer2[bar - 1] = low[bar - 1]
                y = 1
        if bar < (rates_total - 1):
            _s_OnCalculate_x_ = x
            _s_OnCalculate_y_ = y
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_x_ = 0
_s_OnCalculate_y_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Notches(_MQL5Indicator):
    name = 'notches'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'IndShift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

