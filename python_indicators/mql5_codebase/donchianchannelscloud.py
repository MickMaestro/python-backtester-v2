"""DonchianChannelsCloud — converted from MQL5: MQL5 Indicators/DonchianChannelsCloud/DonchianChannelsCloud.mq5

Copyright: Copyright © 2005, Luis Guilherme Damiani; Link: http://www.damianifx.com.br; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Luis Guilherme Damiani', 'link': 'http://www.damianifx.com.br', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 7}, 'colors': {1: [16436871], 2: [16748574], 3: [13828244], 4: [16711935], 5: [15631086]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper Cloud', 2: 'Upper Donchian', 3: 'Middle Donchian', 4: 'Lower Donchian', 5: 'Lower Cloud'}, 'levels': [], 'description': [], 'name': 'DonchianChannelsCloud', 'source': 'MQL5 Indicators/DonchianChannelsCloud/DonchianChannelsCloud.mq5', 'folder': 'DonchianChannelsCloud', 'inputs': [{'mql': 'DonchianPeriod', 'py': 'DonchianPeriod', 'param': 'DonchianPeriod', 'type': 'int', 'default': 20, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'Extremes', 'py': 'Extremes', 'param': 'Extremes', 'type': 'int', 'default': 0, 'label': 'Тип экстремумов', 'sinput': False}, {'mql': 'Margins', 'py': 'Margins', 'param': 'Margins', 'type': 'int', 'default': -2, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtUp1Buffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtDn1Buffer = Arr(0, 0.0)
ExtDn2Buffer = Arr(0, 0.0)
min_rates_total = 0

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
    global min_rates_total
    min_rates_total = DonchianPeriod + 1
    SetIndexBuffer(0, ExtUp1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(2, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    SetIndexBuffer(3, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    SetIndexBuffer(4, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    SetIndexBuffer(5, ExtDn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtDn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Donchian( DonchianPeriod = ', DonchianPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    smin = 0.0
    smax = 0.0
    SsMax = 0.0
    SsMin = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = min_rates_total - 1
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
        ExtABuffer[bar] = smax
        ExtCBuffer[bar] = smin
        ExtBBuffer[bar] = (smax + smin) / 2.0
        ExtUp1Buffer[bar] = ExtABuffer[bar]
        ExtUp2Buffer[bar] = ExtBBuffer[bar]
        ExtDn1Buffer[bar] = ExtBBuffer[bar]
        ExtDn2Buffer[bar] = ExtCBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianChannelsCloud(_MQL5Indicator):
    name = 'DonchianChannelsCloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DonchianPeriod': 20,  # Период усреднения
        'Extremes': _Choice({0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'}, default=0),  # Тип экстремумов
        'Margins': -2,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

