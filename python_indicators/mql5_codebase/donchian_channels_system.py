"""Donchian_Channels_System — converted from MQL5: MQL5 Indicators/Donchian Channels System/Donchian_Channels_System.mq5

Пробойная система с использованием индикатора Donchian_Channels
Copyright: Copyright © 2013, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 17}, 'colors': {1: [16119285], 2: [7451452], 3: [16711935], 4: [9639167, 8388736, 8421504, 13434880, 16748574]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Donchian_Channels', 2: 'Upper Donchian_Channels', 3: 'Lower Donchian_Channels', 4: 'Donchian_Channels_BARS'}, 'levels': [], 'description': ['Пробойная система с использованием индикатора Donchian_Channels'], 'name': 'Donchian_Channels_System', 'source': 'MQL5 Indicators/Donchian Channels System/Donchian_Channels_System.mq5', 'folder': 'Donchian Channels System', 'inputs': [{'mql': 'DonchianPeriod', 'py': 'DonchianPeriod', 'param': 'DonchianPeriod', 'type': 'uint', 'default': 20, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'Extremes', 'py': 'Extremes', 'param': 'Extremes', 'type': 'int', 'default': 0, 'label': 'Тип экстремумов', 'sinput': False}, {'mql': 'Margins', 'py': 'Margins', 'param': 'Margins', 'type': 'int', 'default': -2, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 2, 'label': 'сдвиг канала по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
Shift = _input('Shift', 2)  # сдвиг канала по горизонтали в барах
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Up2Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(DonchianPeriod + 1 + Shift)
    SetIndexBuffer(0, Up1Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Up1Buffer, True)
    SetIndexBuffer(1, Dn1Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn1Buffer, True)
    SetIndexBuffer(2, Up2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Up2Buffer, True)
    SetIndexBuffer(3, Dn2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn2Buffer, True)
    SetIndexBuffer(4, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtCloseBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    SetIndexBuffer(8, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtColorBuffer, True)
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
    StringConcatenate(shortname, 'Donchian_Channels(', DonchianPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = 0
    smin = 0.0
    smax = 0.0
    SsMax = 0.0
    SsMin = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    for bar in range(limit, 0 - 1, -1):
        _sw1 = Extremes
        if _sw1 == HIGH_LOW:
            SsMax = high[ArrayMaximum(high, bar, DonchianPeriod)]
            SsMin = low[ArrayMinimum(low, bar, DonchianPeriod)]
        elif _sw1 == HIGH_LOW_OPEN:
            SsMax = (open[ArrayMaximum(open, bar, DonchianPeriod)] + high[ArrayMaximum(high, bar, DonchianPeriod)]) / 2
            SsMin = (open[ArrayMinimum(open, bar, DonchianPeriod)] + low[ArrayMinimum(low, bar, DonchianPeriod)]) / 2
        elif _sw1 == HIGH_LOW_CLOSE:
            SsMax = (close[ArrayMaximum(close, bar, DonchianPeriod)] + high[ArrayMaximum(high, bar, DonchianPeriod)]) / 2
            SsMin = (close[ArrayMinimum(close, bar, DonchianPeriod)] + low[ArrayMinimum(low, bar, DonchianPeriod)]) / 2
        elif _sw1 == OPEN_HIGH_LOW:
            SsMax = open[ArrayMaximum(open, bar, DonchianPeriod)]
            SsMin = open[ArrayMinimum(open, bar, DonchianPeriod)]
        elif _sw1 == CLOSE_HIGH_LOW:
            SsMax = close[ArrayMaximum(close, bar, DonchianPeriod)]
            SsMin = close[ArrayMinimum(close, bar, DonchianPeriod)]
        smin = SsMin + (((SsMax - SsMin) * Margins) / 100)
        smax = SsMax - (((SsMax - SsMin) * Margins) / 100)
        Up1Buffer[bar] = smax
        Dn1Buffer[bar] = smin
        Up2Buffer[bar] = smax
        Dn2Buffer[bar] = smin
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= _int(Shift)
    for bar in range(limit, 0 - 1, -1):
        clr = 2
        ExtOpenBuffer[bar] = 0.0
        ExtCloseBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        ExtLowBuffer[bar] = 0.0
        if close[bar] > Up1Buffer[bar + Shift]:
            if open[bar] <= close[bar]:
                clr = 4
            else:
                clr = 3
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
        if close[bar] < Dn1Buffer[bar + Shift]:
            if open[bar] > close[bar]:
                clr = 0
            else:
                clr = 1
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
        ExtColorBuffer[bar] = clr
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianChannelsSystem(_MQL5Indicator):
    name = 'Donchian_Channels_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DonchianPeriod': 20,  # Период усреднения
        'Extremes': _Choice({0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'}, default=0),  # Тип экстремумов
        'Margins': -2,
        'Shift': 2,  # сдвиг канала по горизонтали в барах
    }

