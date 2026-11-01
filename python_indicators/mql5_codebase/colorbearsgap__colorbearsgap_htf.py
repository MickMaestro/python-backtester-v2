"""colorbearsgap — converted from MQL5: MQL5 Indicators/ColorBearsGap_HTF/colorbearsgap.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16748574, 8421504, 9639167]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Bears'}, 'levels': [], 'description': [], 'name': 'colorbearsgap', 'source': 'MQL5 Indicators/ColorBearsGap_HTF/colorbearsgap.mq5', 'folder': 'ColorBearsGap_HTF', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения индикатора', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 12, 'label': 'Глубина усреднения индикатора', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения индикатора', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания итогового индикатора', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания итогового индикатора', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания итогового индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA)  # Метод усреднения индикатора
Length1 = _input('Length1', 12)  # Глубина усреднения индикатора
Phase1 = _input('Phase1', 15)  # Параметр усреднения индикатора
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # Метод сглаживания итогового индикатора
Length2 = _input('Length2', 5)  # Глубина сглаживания итогового индикатора
Phase2 = _input('Phase2', 15)  # Параметр сглаживания итогового индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total = min_rates_1 + min_rates_2 + 2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method1)
    Smooth2 = XMA1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'ColorBearsGap(', Length1, ', ', Smooth1, ', ', Length2, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_xbullsC1, _s_OnCalculate_xbullsO1
    if rates_total < min_rates_total:
        return 0
    xmaC = 0.0
    bullsC = 0.0
    xbullsC = 0.0
    xmaO = 0.0
    bullsO = 0.0
    xbullsO = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        xmaC = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, close[bar], bar, False)
        bullsC = high[bar] - xmaC
        xbullsC = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, bullsC, bar, False)
        xbullsC = _fdiv(xbullsC, Point())
        xmaO = XMA3.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, open[bar], bar, False)
        bullsO = high[bar] - xmaO
        xbullsO = XMA4.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, bullsO, bar, False)
        xbullsO = _fdiv(xbullsO, Point())
        IndBuffer[bar] = xbullsO - _s_OnCalculate_xbullsC1
        if bar < (rates_total - 1):
            _s_OnCalculate_xbullsC1 = xbullsC
            _s_OnCalculate_xbullsO1 = xbullsO
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 1
        if IndBuffer[bar] > 0:
            clr = 0
        if IndBuffer[bar] < 0:
            clr = 2
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
XMA4 = _alloc(CXMA)
XMA4.__init__()

# ---- static local variables
_s_OnCalculate_xbullsC1 = 0.0
_s_OnCalculate_xbullsO1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorbearsgap(_MQL5Indicator):
    name = 'colorbearsgap'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения индикатора
        'Length1': 12,  # Глубина усреднения индикатора
        'Phase1': 15,  # Параметр усреднения индикатора
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания итогового индикатора
        'Length2': 5,  # Глубина сглаживания итогового индикатора
        'Phase2': 15,  # Параметр сглаживания итогового индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

