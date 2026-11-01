"""PercentageCrossoverChannel_System — converted from MQL5: MQL5 Indicators/PercentageCrossoverChannel_System/PercentageCrossoverChannel_System.mq5

Пробойная система с использованием индикатора PercentageCrossoverChannel
Copyright: Copyright © 2009, Vic2008; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Vic2008', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 17}, 'colors': {1: [16119285], 2: [7451452], 3: [16711935], 4: [9639167, 8388736, 8421504, 13434880, 16748574]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'PercentageCrossoverChannel', 2: 'Upper PercentageCrossoverChannel', 3: 'Lower PercentageCrossoverChannel', 4: 'PercentageCrossoverChannel_BARS'}, 'levels': [], 'description': ['Пробойная система с использованием индикатора PercentageCrossoverChannel'], 'name': 'PercentageCrossoverChannel_System', 'source': 'MQL5 Indicators/PercentageCrossoverChannel_System/PercentageCrossoverChannel_System.mq5', 'folder': 'PercentageCrossoverChannel_System', 'inputs': [{'mql': 'percent', 'py': 'percent', 'param': 'percent', 'type': 'double', 'default': 1.0, 'label': 'процентное отклонение цены от предыдущего значения индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 1, 'label': 'сдвиг канала по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
percent = _input('percent', 1.0)  # процентное отклонение цены от предыдущего значения индикатора
Shift = _input('Shift', 1)  # сдвиг канала по горизонтали в барах
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Up2Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
plusvar = 0.0
minusvar = 0.0
min_rates_total = 0

def OnInit():
    global min_rates_total, minusvar, plusvar
    min_rates_total = 2
    var1 = percent / 100
    plusvar = 1 + var1
    minusvar = 1 - var1
    SetIndexBuffer(0, Up1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Dn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, Up2Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, Dn2Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_SHIFT, 0)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'Percentage Crossover Channel(percent = ', percent, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Middle_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Middle = 0.0
    if prev_calculated == 0:
        first = 1
        _s_OnCalculate_Middle_prev = close[first - 1]
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if (close[bar] * minusvar) > _s_OnCalculate_Middle_prev:
            Middle = close[bar] * minusvar
        else:
            if (close[bar] * plusvar) < _s_OnCalculate_Middle_prev:
                Middle = close[bar] * plusvar
            else:
                Middle = _s_OnCalculate_Middle_prev
        Up2Buffer[bar] = Middle + ((Middle / 100) * percent)
        Up1Buffer[bar] = Up2Buffer[bar]
        Dn2Buffer[bar] = Middle - ((Middle / 100) * percent)
        Dn1Buffer[bar] = Dn2Buffer[bar]
        if bar < (rates_total - 1):
            _s_OnCalculate_Middle_prev = Middle
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += Shift
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        ExtOpenBuffer[bar] = 0.0
        ExtCloseBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        ExtLowBuffer[bar] = 0.0
        if close[bar] > Up1Buffer[bar - Shift]:
            if open[bar] <= close[bar]:
                clr = 4
            else:
                clr = 3
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
        if close[bar] < Dn1Buffer[bar - Shift]:
            if open[bar] > close[bar]:
                clr = 0
            else:
                clr = 1
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
        ExtColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Middle_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PercentageCrossoverChannelSystem(_MQL5Indicator):
    name = 'PercentageCrossoverChannel_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'percent': 1.0,  # процентное отклонение цены от предыдущего значения индикатора
        'Shift': 1,  # сдвиг канала по горизонтали в барах
    }

