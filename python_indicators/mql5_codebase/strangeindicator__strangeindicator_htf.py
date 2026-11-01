"""StrangeIndicator — converted from MQL5: MQL5 Indicators/StrangeIndicator_HTF/StrangeIndicator.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [13749760, 8421376, 8421504, 2763429, 36095]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'StrangeIndicator'}, 'levels': [], 'description': [], 'name': 'StrangeIndicator', 'source': 'MQL5 Indicators/StrangeIndicator_HTF/StrangeIndicator.mq5', 'folder': 'StrangeIndicator_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'глубина усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'XXPeriod', 'py': 'XXPeriod', 'param': 'XXPeriod', 'type': 'uint', 'default': 12, 'label': 'период индикатора', 'sinput': False}, {'mql': 'XXMA_Method', 'py': 'XXMA_Method', 'param': 'XXMA_Method', 'type': 'int', 'default': 4, 'label': 'метод сглаживания', 'sinput': False}, {'mql': 'XXLength', 'py': 'XXLength', 'param': 'XXLength', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XXPhase', 'py': 'XXPhase', 'param': 'XXPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 1, 'label': 'метод цветовой индикации', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -15, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# enum ENUM_COLOR_MODE
ENUM_LEVELES = 1
ENUM_DIRECT = 2
_enum('ENUM_COLOR_MODE', {1: 'ENUM_LEVELES', 2: 'ENUM_DIRECT'})

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 5)  # глубина усреднения
XPhase = _input('XPhase', 15)  # параметр усреднения,
XXPeriod = _input('XXPeriod', 12)  # период индикатора
XXMA_Method = _input('XXMA_Method', MODE_JJMA)  # метод сглаживания
XXLength = _input('XXLength', 5)  # глубина сглаживания
XXPhase = _input('XXPhase', 15)  # параметр сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Mode = _input('Mode', ENUM_LEVELES)  # метод цветовой индикации
HighLevel = _input('HighLevel', 15)
MiddleLevel = _input('MiddleLevel', 0)
LowLevel = _input('LowLevel', -15)
ExtIndBuffer = Arr(0, 0.0)
ColorExtIndBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_total = min_rates_1 + GetStartBars(XXMA_Method, XXLength, XXPhase)
    SetIndexBuffer(0, ExtIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorExtIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'StrangeIndicator')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ExtStrange = 0.0
    ExtStrange_prev = 0.0
    XMAclose = 0.0
    XMAlow = 0.0
    XMAhigh = 0.0
    diff = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        XMAclose = CLXMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, close[bar], bar, False)
        XMAlow = LXMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, low[bar], bar, False)
        XMAhigh = HXMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, high[bar], bar, False)
        diff = MathMax(XMAhigh - XMAlow, Point())
        ExtStrange = _fdiv(100 * (XMAclose - XMAlow), diff)
        ExtIndBuffer[bar] = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, ExtStrange, bar, False) - 50.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        ExtStrange = ExtIndBuffer[bar]
        if Mode == ENUM_DIRECT:
            ExtStrange_prev = ExtIndBuffer[bar - 1]
            if ExtStrange > MiddleLevel:
                if ExtStrange_prev < ExtStrange:
                    clr = 0
                if ExtStrange_prev > ExtStrange:
                    clr = 3
            elif ExtStrange < MiddleLevel:
                if ExtStrange_prev < ExtStrange:
                    clr = 1
                if ExtStrange_prev > ExtStrange:
                    clr = 4
        else:
            if ExtStrange > HighLevel:
                clr = 0
            elif ExtStrange > MiddleLevel:
                clr = 1
            elif ExtStrange < LowLevel:
                clr = 4
            elif ExtStrange < MiddleLevel:
                clr = 3
        ColorExtIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
HXMA = _alloc(CXMA)
HXMA.__init__()
LXMA = _alloc(CXMA)
LXMA.__init__()
CLXMA = _alloc(CXMA)
CLXMA.__init__()
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StrangeIndicator(_MQL5Indicator):
    name = 'StrangeIndicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 5,  # глубина усреднения
        'XPhase': 15,  # параметр усреднения,
        'XXPeriod': 12,  # период индикатора
        'XXMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод сглаживания
        'XXLength': 5,  # глубина сглаживания
        'XXPhase': 15,  # параметр сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Mode': _Choice({1: 'по уровням перекупленности/перепроданности', 2: 'по направлению движения гистограммы'}, default=1),  # метод цветовой индикации
        'HighLevel': 15,
        'MiddleLevel': 0,
        'LowLevel': -15,
    }

