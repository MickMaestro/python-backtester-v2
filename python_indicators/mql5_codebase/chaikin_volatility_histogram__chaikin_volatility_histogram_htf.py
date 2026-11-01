"""Chaikin_Volatility_Histogram — converted from MQL5: MQL5 Indicators/Chaikin_Volatility_Histogram_HTF/Chaikin_Volatility_Histogram.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16776960, 7451452, 8421504, 13458026, 16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Chaikin_Volatility_Histogram'}, 'levels': [], 'description': [], 'name': 'Chaikin_Volatility_Histogram', 'source': 'MQL5 Indicators/Chaikin_Volatility_Histogram_HTF/Chaikin_Volatility_Histogram.mq5', 'folder': 'Chaikin_Volatility_Histogram_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 10, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'ROCPeriod', 'py': 'ROCPeriod', 'param': 'ROCPeriod', 'type': 'uint', 'default': 10, 'label': 'глубина  второго сглаживания', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 50, 'label': 'уровень наивысшей волатильности', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'uint', 'default': 20, 'label': 'уровень средней волатильности', 'sinput': False}, {'mql': 'ZeroLevel', 'py': 'ZeroLevel', 'param': 'ZeroLevel', 'type': 'uint', 'default': 0, 'label': 'уровень нулевой волатильности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -20, 'label': 'уровень минимальной волатильности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_EMA_)  # метод усреднения
XLength = _input('XLength', 10)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
ROCPeriod = _input('ROCPeriod', 10)  # глубина  второго сглаживания
HighLevel = _input('HighLevel', 50)  # уровень наивысшей волатильности
MiddleLevel = _input('MiddleLevel', 20)  # уровень средней волатильности
ZeroLevel = _input('ZeroLevel', 0)  # уровень нулевой волатильности
LowLevel = _input('LowLevel', -20)  # уровень минимальной волатильности
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
Count = Arr(0, 0)
xrange = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = 7
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_total = min_rates_1 + _int(ROCPeriod + 1)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    ArrayResize(Count, ROCPeriod + 1)
    ArrayResize(xrange, ROCPeriod + 1)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Chaikin_Volatility_Histogram')
    IndicatorSetInteger(INDICATOR_LEVELS, 4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, ZeroLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrDodgerBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    range_ = 0.0
    xrangeX = 0.0
    ratio = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        ArrayInitialize(Count, None)
        ArrayInitialize(xrange, None)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        range_ = high[bar] - low[bar]
        xrange[Count[0]] = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, range_, bar, False)
        xrangeX = xrange[Count[ROCPeriod]]
        if not xrangeX:
            xrangeX = Point()
        ratio = _fdiv(xrange[Count[0]] - xrangeX, xrangeX) * 100
        IndBuffer[bar] = ratio
        clr = 4
        if ratio > HighLevel:
            clr = 0
        elif ratio > MiddleLevel:
            clr = 1
        elif ratio > ZeroLevel:
            clr = 2
        elif ratio > LowLevel:
            clr = 3
        ColorIndBuffer[bar] = clr
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChaikinVolatilityHistogram(_MQL5Indicator):
    name = 'Chaikin_Volatility_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод усреднения
        'XLength': 10,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'ROCPeriod': 10,  # глубина  второго сглаживания
        'HighLevel': 50,  # уровень наивысшей волатильности
        'MiddleLevel': 20,  # уровень средней волатильности
        'ZeroLevel': 0,  # уровень нулевой волатильности
        'LowLevel': -20,  # уровень минимальной волатильности
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

