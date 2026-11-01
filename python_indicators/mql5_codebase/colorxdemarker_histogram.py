"""ColorXDeMarker_Histogram — converted from MQL5: MQL5 Indicators/ColorXDeMarker_Histogram/ColorXDeMarker_Histogram.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16776960, 2263842, 8421504, 42495, 65535]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'ColorXDeMarker_Histogram'}, 'levels': [], 'description': [], 'name': 'ColorXDeMarker_Histogram', 'source': 'MQL5 Indicators/ColorXDeMarker_Histogram/ColorXDeMarker_Histogram.mq5', 'folder': 'ColorXDeMarker_Histogram', 'inputs': [{'mql': 'XPeriod', 'py': 'XPeriod', 'param': 'XPeriod', 'type': 'uint', 'default': 12, 'label': 'период DeMarker', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 6, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 1, 'label': 'метод цветовой индикации', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
ENUM_LEVELS = 1
ENUM_DIRECT = 2
_enum('ENUM_COLOR_MODE', {1: 'ENUM_LEVELS', 2: 'ENUM_DIRECT'})

# ---- inputs and global variables
XPeriod = _input('XPeriod', 12)  # период DeMarker
XMA_Method = _input('XMA_Method', MODE_JJMA)  # метод усреднения
XLength = _input('XLength', 5)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_TYPICAL_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Mode = _input('Mode', ENUM_LEVELS)  # метод цветовой индикации
HighLevel = _input('HighLevel', 20)
MiddleLevel = _input('MiddleLevel', 0)
LowLevel = _input('LowLevel', -20)
ExtIndBuffer = Arr(0, 0.0)
ColorExtIndBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = _int(XPeriod) + 1
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase)
    SetIndexBuffer(0, ExtIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorExtIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'ColorXDeMarker_Histogram(' + _str(XPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBrown)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ExtDeMarker = 0.0
    ExtDeMarker_prev = 0.0
    ExtDeMax = 0.0
    ExtDeMin = 0.0
    ExtAvgDeMax = 0.0
    ExtAvgDeMin = 0.0
    dNum = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if high[bar] > high[bar - 1]:
            ExtDeMax = high[bar] - high[bar - 1]
        else:
            ExtDeMax = 0.0
        if low[bar - 1] > low[bar]:
            ExtDeMin = low[bar - 1] - low[bar]
        else:
            ExtDeMin = 0.0
        ExtAvgDeMax = XMA1.XMASeries(1, prev_calculated, rates_total, MODE_SMA_, 0, XPeriod, ExtDeMax, bar, False)
        ExtAvgDeMin = XMA2.XMASeries(1, prev_calculated, rates_total, MODE_SMA_, 0, XPeriod, ExtDeMin, bar, False)
        dNum = ExtAvgDeMax + ExtAvgDeMin
        if dNum:
            ExtDeMarker = _fdiv(ExtAvgDeMax, dNum)
        else:
            ExtDeMarker = 0.0
        ExtIndBuffer[bar] = XMA3.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, ExtDeMarker, bar, False)
        ExtIndBuffer[bar] *= 100
        ExtIndBuffer[bar] -= 50
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        ExtDeMarker = ExtIndBuffer[bar]
        if Mode == ENUM_DIRECT:
            ExtDeMarker_prev = ExtIndBuffer[bar - 1]
            if ExtDeMarker > MiddleLevel:
                if ExtDeMarker_prev < ExtDeMarker:
                    clr = 0
                if ExtDeMarker_prev > ExtDeMarker:
                    clr = 3
            elif ExtDeMarker < MiddleLevel:
                if ExtDeMarker_prev < ExtDeMarker:
                    clr = 1
                if ExtDeMarker_prev > ExtDeMarker:
                    clr = 4
        else:
            if ExtDeMarker > HighLevel:
                clr = 0
            elif ExtDeMarker > MiddleLevel:
                clr = 1
            elif ExtDeMarker < LowLevel:
                clr = 4
            elif ExtDeMarker < MiddleLevel:
                clr = 3
        ColorExtIndBuffer[bar] = clr
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorXDeMarkerHistogram(_MQL5Indicator):
    name = 'ColorXDeMarker_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XPeriod': 12,  # период DeMarker
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'XLength': 5,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=6),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Mode': _Choice({1: 'по уровням перекупленности/перепроданности', 2: 'по направлению движения гистограммы'}, default=1),  # метод цветовой индикации
        'HighLevel': 20,
        'MiddleLevel': 0,
        'LowLevel': -20,
    }

