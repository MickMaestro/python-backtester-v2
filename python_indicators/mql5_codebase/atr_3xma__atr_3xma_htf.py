"""atr_3xma — converted from MQL5: MQL5 Indicators/ATR_3XMA_HTF/atr_3xma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [65280], 2: [255], 3: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Fast ATR', 2: ' Medium ATR', 3: 'Slow ATR'}, 'levels': [], 'description': [], 'name': 'atr_3xma', 'source': 'MQL5 Indicators/ATR_3XMA_HTF/atr_3xma.mq5', 'folder': 'ATR_3XMA_HTF', 'inputs': [{'mql': 'FastATRPeriod', 'py': 'FastATRPeriod', 'param': 'FastATRPeriod', 'type': 'uint', 'default': 14, 'label': 'Период быстрого ATR', 'sinput': False}, {'mql': 'MediumATRPeriod', 'py': 'MediumATRPeriod', 'param': 'MediumATRPeriod', 'type': 'uint', 'default': 25, 'label': 'Период умеренного ATR', 'sinput': False}, {'mql': 'SlowATRPeriod', 'py': 'SlowATRPeriod', 'param': 'SlowATRPeriod', 'type': 'uint', 'default': 50, 'label': 'Период медленного ATR', 'sinput': False}, {'mql': 'SmoothRatio', 'py': 'SmoothRatio', 'param': 'SmoothRatio', 'type': 'double', 'default': 5.0, 'label': 'Коэффициент уменьшения периода', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 4, 'label': 'Метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр первого сглаживания', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 0, 'label': 'Метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Параметр второго сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
FastATRPeriod = _input('FastATRPeriod', 14)  # Период быстрого ATR
MediumATRPeriod = _input('MediumATRPeriod', 25)  # Период умеренного ATR
SlowATRPeriod = _input('SlowATRPeriod', 50)  # Период медленного ATR
SmoothRatio = _input('SmoothRatio', 5.0)  # Коэффициент уменьшения периода
MA_Method1 = _input('MA_Method1', MODE_JJMA)  # Метод усреднения первого сглаживания
Phase1 = _input('Phase1', 15)  # Параметр первого сглаживания
MA_Method2 = _input('MA_Method2', MODE_SMA_)  # Метод усреднения второго сглаживания
Phase2 = _input('Phase2', 15)  # Параметр второго сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
FastSmoothPeriod = 0
MediumSmoothPeriod = 0
SlowSmoothPeriod = 0

def OnInit():
    global FastSmoothPeriod, MediumSmoothPeriod, SlowSmoothPeriod, min_rates_1, min_rates_total
    max1 = _int(MathMax(FastATRPeriod, MathMax(MediumATRPeriod, SlowATRPeriod)))
    min_rates_1 = 1 + GetStartBars(MA_Method1, max1, Phase1)
    Ratio = MathMax(1, SmoothRatio)
    FastSmoothPeriod = _int(MathCeil(_fdiv(FastATRPeriod, Ratio)))
    MediumSmoothPeriod = _int(MathCeil(_fdiv(MediumATRPeriod, Ratio)))
    SlowSmoothPeriod = _int(MathCeil(_fdiv(SlowATRPeriod, Ratio)))
    max2 = _int(MathMax(FastSmoothPeriod, MathMax(MediumSmoothPeriod, SlowSmoothPeriod)))
    min_rates_total = min_rates_1 + GetStartBars(MA_Method2, max2, Phase2)
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, IndBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'ATR_3XMA(', FastATRPeriod, ', ', MediumATRPeriod, ', ', SlowATRPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 5)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    atr = 0.0
    xatr1 = 0.0
    xatr2 = 0.0
    xatr3 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        atr = calc_atr(bar, high, low, close)
        xatr1 = XMA1.XMASeries(1, prev_calculated, rates_total, MA_Method1, Phase1, FastATRPeriod, atr, bar, False)
        xatr2 = XMA2.XMASeries(1, prev_calculated, rates_total, MA_Method1, Phase1, MediumATRPeriod, atr, bar, False)
        xatr3 = XMA3.XMASeries(1, prev_calculated, rates_total, MA_Method1, Phase1, SlowATRPeriod, atr, bar, False)
        IndBuffer1[bar] = XMA4.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method1, Phase1, FastSmoothPeriod, xatr1, bar, False)
        IndBuffer2[bar] = XMA5.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method1, Phase1, MediumSmoothPeriod, xatr2, bar, False)
        IndBuffer3[bar] = XMA6.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method1, Phase1, SlowSmoothPeriod, xatr3, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def calc_atr(index, h, l, c):
    return MathMax(h[index], c[index - 1]) - MathMin(l[index], c[index - 1])

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
XMA4 = _alloc(CXMA)
XMA4.__init__()
XMA5 = _alloc(CXMA)
XMA5.__init__()
XMA6 = _alloc(CXMA)
XMA6.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Atr3xma(_MQL5Indicator):
    name = 'atr_3xma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastATRPeriod': 14,  # Период быстрого ATR
        'MediumATRPeriod': 25,  # Период умеренного ATR
        'SlowATRPeriod': 50,  # Период медленного ATR
        'SmoothRatio': 5.0,  # Коэффициент уменьшения периода
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения первого сглаживания
        'Phase1': 15,  # Параметр первого сглаживания
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения второго сглаживания
        'Phase2': 15,  # Параметр второго сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

