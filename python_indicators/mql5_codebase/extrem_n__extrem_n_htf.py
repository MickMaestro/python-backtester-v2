"""extrem_n — converted from MQL5: MQL5 Indicators/Extrem_N_HTF/extrem_n.mq5

Copyright: Copyright © 2014 Serkov Alexandr; Link: serkov-alexandr@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014 Serkov Alexandr', 'link': 'serkov-alexandr@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65280], 2: [255]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bulls', 2: 'Bears'}, 'levels': [], 'description': [], 'name': 'extrem_n', 'source': 'MQL5 Indicators/Extrem_N_HTF/extrem_n.mq5', 'folder': 'Extrem_N_HTF', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 9, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 9)  # Период индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period)
    PlotIndexSetString(0, PLOT_LABEL, 'Bears')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, period)
    PlotIndexSetString(1, PLOT_LABEL, 'Bulls')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, '(', period, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (period - 1):
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = period
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if high[bar] > high[bar - period]:
            BullsBuffer[bar] = high[bar]
        else:
            BullsBuffer[bar] = 0.0
        if low[bar] < low[bar - period]:
            BearsBuffer[bar] = low[bar]
        else:
            BearsBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ExtremN(_MQL5Indicator):
    name = 'extrem_n'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 9,  # Период индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

