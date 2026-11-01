"""RAVI_Histogram — converted from MQL5: MQL5 Indicators/RAVI_Histogram_HTF/RAVI_Histogram.mq5

Range Action Verification Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 16748574, 8421504, 9639167, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'RAVI_Histogram'}, 'levels': [], 'description': ['Range Action Verification Index'], 'name': 'RAVI_Histogram', 'source': 'MQL5 Indicators/RAVI_Histogram_HTF/RAVI_Histogram.mq5', 'folder': 'RAVI_Histogram_HTF', 'inputs': [{'mql': 'FastMethod', 'py': 'FastMethod', 'param': 'FastMethod', 'type': 'int', 'default': 1, 'label': 'метод быстрого усреднения', 'sinput': False}, {'mql': 'FastLength', 'py': 'FastLength', 'param': 'FastLength', 'type': 'uint', 'default': 7, 'label': 'глубина быстрого усреднения', 'sinput': False}, {'mql': 'FastPhase', 'py': 'FastPhase', 'param': 'FastPhase', 'type': 'int', 'default': 15, 'label': 'параметр быстрого усреднения,', 'sinput': False}, {'mql': 'SlowMethod', 'py': 'SlowMethod', 'param': 'SlowMethod', 'type': 'int', 'default': 1, 'label': 'метод медленного усреднения', 'sinput': False}, {'mql': 'SlowLength', 'py': 'SlowLength', 'param': 'SlowLength', 'type': 'uint', 'default': 65, 'label': 'глубина медленного усреднения', 'sinput': False}, {'mql': 'SlowPhase', 'py': 'SlowPhase', 'param': 'SlowPhase', 'type': 'int', 'default': 15, 'label': 'параметр медленного усреднения,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'ExtraHighLevel', 'py': 'ExtraHighLevel', 'param': 'ExtraHighLevel', 'type': 'double', 'default': 0.3, 'label': 'уровень максимального тренда вверх', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 0.1, 'label': 'уровень сильного тренда вверх', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -0.1, 'label': 'уровень слабого тренда вниз', 'sinput': False}, {'mql': 'ExtraLowLevel', 'py': 'ExtraLowLevel', 'param': 'ExtraLowLevel', 'type': 'double', 'default': -0.3, 'label': 'уровень максимального тренда вниз', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
FastMethod = _input('FastMethod', MODE_EMA_)  # метод быстрого усреднения
FastLength = _input('FastLength', 7)  # глубина быстрого усреднения
FastPhase = _input('FastPhase', 15)  # параметр быстрого усреднения,
SlowMethod = _input('SlowMethod', MODE_EMA_)  # метод медленного усреднения
SlowLength = _input('SlowLength', 65)  # глубина медленного усреднения
SlowPhase = _input('SlowPhase', 15)  # параметр медленного усреднения,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtraHighLevel = _input('ExtraHighLevel', 0.3)  # уровень максимального тренда вверх
HighLevel = _input('HighLevel', 0.1)  # уровень сильного тренда вверх
LowLevel = _input('LowLevel', -0.1)  # уровень слабого тренда вниз
ExtraLowLevel = _input('ExtraLowLevel', -0.3)  # уровень максимального тренда вниз
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = MathMax(GetStartBars(FastMethod, FastLength, FastPhase), GetStartBars(SlowMethod, SlowLength, SlowPhase))
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RAVI_Histogram')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, ExtraHighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, LowLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, ExtraLowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrDodgerBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        fast = XMA1.XMASeries(0, prev_calculated, rates_total, FastMethod, FastPhase, FastLength, price, bar, False)
        slow = XMA2.XMASeries(0, prev_calculated, rates_total, SlowMethod, SlowPhase, SlowLength, price, bar, False)
        if not slow:
            slow = 1.0
        ravi = _fdiv(100 * (fast - slow), slow)
        IndBuffer[bar] = ravi
        clr = 2
        if ravi > ExtraHighLevel:
            clr = 0
        elif ravi > HighLevel:
            clr = 1
        elif ravi < ExtraLowLevel:
            clr = 4
        elif ravi < LowLevel:
            clr = 3
        ColorIndBuffer[bar] = clr
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RAVIHistogram(_MQL5Indicator):
    name = 'RAVI_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод быстрого усреднения
        'FastLength': 7,  # глубина быстрого усреднения
        'FastPhase': 15,  # параметр быстрого усреднения,
        'SlowMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод медленного усреднения
        'SlowLength': 65,  # глубина медленного усреднения
        'SlowPhase': 15,  # параметр медленного усреднения,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'ExtraHighLevel': 0.3,  # уровень максимального тренда вверх
        'HighLevel': 0.1,  # уровень сильного тренда вверх
        'LowLevel': -0.1,  # уровень слабого тренда вниз
        'ExtraLowLevel': -0.3,  # уровень максимального тренда вниз
    }

