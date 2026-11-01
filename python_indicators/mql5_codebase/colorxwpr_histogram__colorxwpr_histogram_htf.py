"""ColorXWPR_Histogram — converted from MQL5: MQL5 Indicators/ColorXWPR_Histogram_HTF/ColorXWPR_Histogram.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16776960, 14772545, 8421504, 255, 16711935]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'ColorXWPR_Histogram'}, 'levels': [], 'description': [], 'name': 'ColorXWPR_Histogram', 'source': 'MQL5 Indicators/ColorXWPR_Histogram_HTF/ColorXWPR_Histogram.mq5', 'folder': 'ColorXWPR_Histogram_HTF', 'inputs': [{'mql': 'XPeriod', 'py': 'XPeriod', 'param': 'XPeriod', 'type': 'uint', 'default': 12, 'label': 'период WPR', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 1, 'label': 'метод цветовой индикации', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_COLOR_MODE
ENUM_LEVELES = 1
ENUM_DIRECT = 2
_enum('ENUM_COLOR_MODE', {1: 'ENUM_LEVELES', 2: 'ENUM_DIRECT'})

# ---- inputs and global variables
XPeriod = _input('XPeriod', 12)  # период WPR
XMA_Method = _input('XMA_Method', MODE_JJMA)  # метод усреднения
XLength = _input('XLength', 5)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Mode = _input('Mode', ENUM_LEVELES)  # метод цветовой индикации
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
    shortname = 'ColorXWPR_Histogram(' + _str(XPeriod) + ')'
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
    global _s_OnCalculate_ExtWPR_prev
    if rates_total < min_rates_total:
        return 0
    dMaxHigh = 0.0
    dMinLow = 0.0
    diff = 0.0
    ExtWPR = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dMaxHigh = 0.0
        dMinLow = 9999999999.0
        for iii in range(0, _int(XPeriod)):
            dMaxHigh = MathMax(dMaxHigh, high[bar - iii])
            dMinLow = MathMin(dMinLow, low[bar - iii])
        diff = dMaxHigh - dMinLow
        if diff:
            ExtWPR = _fdiv((-(dMaxHigh - close[bar])) * 100, diff)
        else:
            ExtWPR = _s_OnCalculate_ExtWPR_prev
        ExtIndBuffer[bar] = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, ExtWPR, bar, False) + 50.0
        if bar < (rates_total - 1):
            _s_OnCalculate_ExtWPR_prev = ExtWPR
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        ExtWPR = ExtIndBuffer[bar]
        if Mode == ENUM_DIRECT:
            _s_OnCalculate_ExtWPR_prev = ExtIndBuffer[bar - 1]
            if ExtWPR > MiddleLevel:
                if _s_OnCalculate_ExtWPR_prev < ExtWPR:
                    clr = 0
                if _s_OnCalculate_ExtWPR_prev > ExtWPR:
                    clr = 3
            elif ExtWPR < MiddleLevel:
                if _s_OnCalculate_ExtWPR_prev < ExtWPR:
                    clr = 1
                if _s_OnCalculate_ExtWPR_prev > ExtWPR:
                    clr = 4
        else:
            if ExtWPR > HighLevel:
                clr = 0
            elif ExtWPR > MiddleLevel:
                clr = 1
            elif ExtWPR < LowLevel:
                clr = 4
            elif ExtWPR < MiddleLevel:
                clr = 3
        ColorExtIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_OnCalculate_ExtWPR_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorXWPRHistogram(_MQL5Indicator):
    name = 'ColorXWPR_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XPeriod': 12,  # период WPR
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'XLength': 5,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Mode': _Choice({1: 'по уровням перекупленности/перепроданности', 2: 'по направлению движения гистограммы'}, default=1),  # метод цветовой индикации
        'HighLevel': 20,
        'MiddleLevel': 0,
        'LowLevel': -20,
    }

