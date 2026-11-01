"""Bear_Bulls_Power_Candle — converted from MQL5: MQL5 Indicators/Bear_Bulls_Power_Candle/Bear_Bulls_Power_Candle.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [5737262, 3329434, 8421504, 12695295, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Bear_Bulls_Power_Open;Bear_Bulls_Power_High;Bear_Bulls_Power_Low;Bear_Bulls_Power_Close'}, 'levels': [], 'description': [], 'name': 'Bear_Bulls_Power_Candle', 'source': 'MQL5 Indicators/Bear_Bulls_Power_Candle/Bear_Bulls_Power_Candle.mq5', 'folder': 'Bear_Bulls_Power_Candle', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения индикатора', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 12, 'label': 'Глубина усреднения индикатора', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения индикатора,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания итогового индикатора', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания итогового индикатора', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания итогового индикатора,', 'sinput': False}, {'mql': 'Range', 'py': 'Range', 'param': 'Range', 'type': 'uint', 'default': 10, 'label': 'максимальный размер гепа между исходными свечками, не отображаемый на индикаторе', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA_)  # Метод усреднения индикатора
Length1 = _input('Length1', 12)  # Глубина усреднения индикатора
Phase1 = _input('Phase1', 15)  # Параметр усреднения индикатора,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # Метод сглаживания итогового индикатора
Length2 = _input('Length2', 5)  # Глубина сглаживания итогового индикатора
Phase2 = _input('Phase2', 15)  # Параметр сглаживания итогового индикатора,
Range = _input('Range', 10)  # максимальный размер гепа между исходными свечками, не отображаемый на индикаторе
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = GetStartBars(MA_Method1, Length1, Phase1) + 1
    min_rates_total = min_rates_1 + GetStartBars(MA_Method2, Length2, Phase2)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    shortname = Box("")
    Smooth1 = OXMA1.GetString_MA_Method(MA_Method1)
    Smooth2 = OXMA1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'Bear_Bulls_Power_Candle(', Length1, ', ', Smooth1, ', ', Length2, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    xma = 0.0
    bulls_bears = 0.0
    xbulls_bears = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        xma = OXMA1.XMASeries(1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, open[bar], bar, False)
        bulls_bears = (high[bar] + low[bar] - (2 * xma)) / 2.0
        xbulls_bears = OXMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, bulls_bears, bar, False)
        ExtOpenBuffer[bar] = _fdiv(xbulls_bears, Point())
        xma = HXMA1.XMASeries(1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, high[bar], bar, False)
        bulls_bears = (high[bar] + low[bar] - (2 * xma)) / 2.0
        xbulls_bears = HXMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, bulls_bears, bar, False)
        ExtHighBuffer[bar] = _fdiv(xbulls_bears, Point())
        xma = LXMA1.XMASeries(1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, low[bar], bar, False)
        bulls_bears = (high[bar] + low[bar] - (2 * xma)) / 2.0
        xbulls_bears = LXMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, bulls_bears, bar, False)
        ExtLowBuffer[bar] = _fdiv(xbulls_bears, Point())
        xma = CXMA1.XMASeries(1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, close[bar], bar, False)
        bulls_bears = (high[bar] + low[bar] - (2 * xma)) / 2.0
        xbulls_bears = CXMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, bulls_bears, bar, False)
        ExtCloseBuffer[bar] = _fdiv(xbulls_bears, Point())
        if MathAbs(close[bar - 1] - open[bar]) < (Range * Point()):
            ExtOpenBuffer[bar] = ExtCloseBuffer[bar - 1]
        ExtColorBuffer[bar] = 2.0
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            if ExtCloseBuffer[bar - 1] <= ExtCloseBuffer[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            if ExtCloseBuffer[bar - 1] >= ExtCloseBuffer[bar]:
                ExtColorBuffer[bar] = 4.0
            else:
                ExtColorBuffer[bar] = 3.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
OXMA1 = _alloc(CXMA)
OXMA1.__init__()
OXMA2 = _alloc(CXMA)
OXMA2.__init__()
HXMA1 = _alloc(CXMA)
HXMA1.__init__()
HXMA2 = _alloc(CXMA)
HXMA2.__init__()
LXMA1 = _alloc(CXMA)
LXMA1.__init__()
LXMA2 = _alloc(CXMA)
LXMA2.__init__()
CXMA1 = _alloc(CXMA)
CXMA1.__init__()
CXMA2 = _alloc(CXMA)
CXMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BearBullsPowerCandle(_MQL5Indicator):
    name = 'Bear_Bulls_Power_Candle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения индикатора
        'Length1': 12,  # Глубина усреднения индикатора
        'Phase1': 15,  # Параметр усреднения индикатора,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания итогового индикатора
        'Length2': 5,  # Глубина сглаживания итогового индикатора
        'Phase2': 15,  # Параметр сглаживания итогового индикатора,
        'Range': 10,  # максимальный размер гепа между исходными свечками, не отображаемый на индикаторе
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

