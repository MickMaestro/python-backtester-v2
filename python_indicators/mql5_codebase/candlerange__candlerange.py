"""CandleRange — converted from MQL5: MQL5 Indicators/CandleRange/CandleRange.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [65280, 8421376], 2: [16711935, 8388736]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'High', 2: 'Low'}, 'levels': [], 'description': [], 'name': 'CandleRange', 'source': 'MQL5 Indicators/CandleRange/CandleRange.mq5', 'folder': 'CandleRange', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения индикатора', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 7, 'label': 'Глубина усреднения индикатора', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения индикатора,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA_)  # Метод усреднения индикатора
Length1 = _input('Length1', 7)  # Глубина усреднения индикатора
Phase1 = _input('Phase1', 15)  # Параметр усреднения индикатора,
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
HIndBuffer = Arr(0, 0.0)
ColorHIndBuffer = Arr(0, 0.0)
LIndBuffer = Arr(0, 0.0)
ColorLIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(MA_Method1, Length1, Phase1)
    SetIndexBuffer(0, HIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorHIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, LIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorLIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method1)
    StringConcatenate(shortname, 'CandleRange(', Length1, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        HIndBuffer[bar] = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, high[bar] - open[bar], bar, False)
        HIndBuffer[bar] = _fdiv(HIndBuffer[bar], Point())
        LIndBuffer[bar] = XMA2.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, low[bar] - open[bar], bar, False)
        LIndBuffer[bar] = _fdiv(LIndBuffer[bar], Point())
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total + 1
    bar = first
    for bar in range(bar, rates_total):
        ColorHIndBuffer[bar] = ColorHIndBuffer[bar - 1]
        if HIndBuffer[bar - 1] < HIndBuffer[bar]:
            ColorHIndBuffer[bar] = 0.0
        elif HIndBuffer[bar - 1] > HIndBuffer[bar]:
            ColorHIndBuffer[bar] = 1.0
        ColorLIndBuffer[bar] = ColorLIndBuffer[bar - 1]
        if LIndBuffer[bar - 1] > LIndBuffer[bar]:
            ColorLIndBuffer[bar] = 0.0
        elif LIndBuffer[bar - 1] < LIndBuffer[bar]:
            ColorLIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleRange(_MQL5Indicator):
    name = 'CandleRange'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения индикатора
        'Length1': 7,  # Глубина усреднения индикатора
        'Phase1': 15,  # Параметр усреднения индикатора,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

