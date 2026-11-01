"""donchianchannels — converted from MQL5: MQL5 Indicators/DonchianChannels_HTF/donchianchannels.mq5

Copyright: Copyright © 2005, Luis Guilherme Damiani; Link: http://www.damianifx.com.br; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Luis Guilherme Damiani', 'link': 'http://www.damianifx.com.br', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [2330219], 2: [8421504], 3: [9662683]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper Donchian', 2: 'Middle Donchian', 3: 'Lower Donchian'}, 'levels': [], 'description': [], 'name': 'donchianchannels', 'source': 'MQL5 Indicators/DonchianChannels_HTF/donchianchannels.mq5', 'folder': 'DonchianChannels_HTF', 'inputs': [{'mql': 'DonchianPeriod', 'py': 'DonchianPeriod', 'param': 'DonchianPeriod', 'type': 'int', 'default': 20, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'Extremes', 'py': 'Extremes', 'param': 'Extremes', 'type': 'int', 'default': 0, 'label': 'Тип экстремумов', 'sinput': False}, {'mql': 'Margins', 'py': 'Margins', 'param': 'Margins', 'type': 'int', 'default': -2, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_Extrem
HIGH_LOW = 0
HIGH_LOW_OPEN = 1
HIGH_LOW_CLOSE = 2
OPEN_HIGH_LOW = 3
CLOSE_HIGH_LOW = 4
_enum('Applied_Extrem', {0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'})

# ---- inputs and global variables
DonchianPeriod = _input('DonchianPeriod', 20)  # Период усреднения
Extremes = _input('Extremes', HIGH_LOW)  # Тип экстремумов
Margins = _input('Margins', -2)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpperBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)

def iHighest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Неверное значение в функции iHighest, startPos = ', startPos)
        return 0
    if (startPos - count) < 0:
        count = startPos
    max_ = array[startPos]
    for i in range(startPos, startPos - count, -1):
        if array[i] > max_:
            index = i
            max_ = array[i]
    return index

def iLowest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Неверное значение в функции iLowest, startPos = ', startPos)
        return 0
    if (startPos - count) < 0:
        count = startPos
    min_ = array[startPos]
    for i in range(startPos, startPos - count, -1):
        if array[i] < min_:
            index = i
            min_ = array[i]
    return index

def OnInit():
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, DonchianPeriod - 1)
    PlotIndexSetString(0, PLOT_LABEL, 'Upper Donchian')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, DonchianPeriod - 1)
    PlotIndexSetString(1, PLOT_LABEL, 'Middle Donchian')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, DonchianPeriod - 1)
    PlotIndexSetString(2, PLOT_LABEL, 'Lower Donchian')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Donchian( DonchianPeriod = ', DonchianPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (DonchianPeriod + 1):
        return 0
    smin = 0.0
    smax = 0.0
    SsMax = 0.0
    SsMin = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = DonchianPeriod
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        _sw1 = Extremes
        if _sw1 == HIGH_LOW:
            SsMax = high[iHighest_u(high, DonchianPeriod, bar)]
            SsMin = low[iLowest_u(low, DonchianPeriod, bar)]
        elif _sw1 == HIGH_LOW_OPEN:
            SsMax = (open[iHighest_u(open, DonchianPeriod, bar)] + high[iHighest_u(high, DonchianPeriod, bar)]) / 2
            SsMin = (open[iLowest_u(open, DonchianPeriod, bar)] + low[iLowest_u(high, DonchianPeriod, bar)]) / 2
        elif _sw1 == HIGH_LOW_CLOSE:
            SsMax = (close[iHighest_u(close, DonchianPeriod, bar)] + high[iHighest_u(high, DonchianPeriod, bar)]) / 2
            SsMin = (close[iLowest_u(close, DonchianPeriod, bar)] + low[iLowest_u(high, DonchianPeriod, bar)]) / 2
        elif _sw1 == OPEN_HIGH_LOW:
            SsMax = open[iHighest_u(open, DonchianPeriod, bar)]
            SsMin = open[iLowest_u(open, DonchianPeriod, bar)]
        elif _sw1 == CLOSE_HIGH_LOW:
            SsMax = close[iHighest_u(close, DonchianPeriod, bar)]
            SsMin = close[iLowest_u(close, DonchianPeriod, bar)]
        smin = SsMin + (((SsMax - SsMin) * Margins) / 100)
        smax = SsMax - (((SsMax - SsMin) * Margins) / 100)
        UpperBuffer[bar] = smax
        LowerBuffer[bar] = smin
        MiddleBuffer[bar] = (smax + smin) / 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Donchianchannels(_MQL5Indicator):
    name = 'donchianchannels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DonchianPeriod': 20,  # Период усреднения
        'Extremes': _Choice({0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'}, default=0),  # Тип экстремумов
        'Margins': -2,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

