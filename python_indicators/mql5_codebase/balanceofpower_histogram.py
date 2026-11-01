"""BalanceOfPower_Histogram — converted from MQL5: MQL5 Indicators/BalanceOfPower_Histogram/BalanceOfPower_Histogram.mq5

Индикатор Balance of Power (BOP), описанный Игорем Лившином, измеряет силу быков и медведей оценивая способность тех и других толкать цены до предельного уровня
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 16760576, 8421376, 16711680, 8388736, 8721863, 16711935, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'BalanceOfPower_Histogram'}, 'levels': [], 'description': ['Индикатор Balance of Power (BOP), описанный Игорем Лившином, измеряет силу быков и медведей оценивая способность тех и других толкать цены до предельного уровня'], 'name': 'BalanceOfPower_Histogram', 'source': 'MQL5 Indicators/BalanceOfPower_Histogram/BalanceOfPower_Histogram.mq5', 'folder': 'BalanceOfPower_Histogram', 'inputs': [{'mql': 'XMethod', 'py': 'XMethod', 'param': 'XMethod', 'type': 'int', 'default': 7, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 15, 'label': 'глубина усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 20, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -20, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMethod = _input('XMethod', MODE_T3)  # метод усреднения
XLength = _input('XLength', 15)  # глубина усреднения
XPhase = _input('XPhase', 15)  # параметр усреднения,
HighLevel = _input('HighLevel', 20)  # уровень перекупленности
LowLevel = _input('LowLevel', -20)  # уровень перепроданности
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(XMethod, XLength, XPhase) + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BalanceOfPower_Histogram')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    diff = 0.0
    bop = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        diff = high[bar] - low[bar]
        if not diff:
            diff = Point()
        bop = _fdiv(close[bar] - open[bar], diff)
        IndBuffer[bar] = 100 * XMA1.XMASeries(0, prev_calculated, rates_total, XMethod, XPhase, XLength, bop, bar, False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    for bar in range(first, rates_total):
        clr = 10
        bop = IndBuffer[bar]
        diff = IndBuffer[bar] - IndBuffer[bar - 1]
        if bop > 0:
            if diff > 0.0:
                if bop > HighLevel:
                    clr = 0
                else:
                    clr = 2
            if diff < 0.0:
                if bop > HighLevel:
                    clr = 1
                else:
                    clr = 3
        if bop < 0:
            if diff < 0.0:
                if bop < LowLevel:
                    clr = 7
                else:
                    clr = 5
            if diff > 0.0:
                if bop < LowLevel:
                    clr = 6
                else:
                    clr = 4
        ColorIndBuffer[bar] = clr
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BalanceOfPowerHistogram(_MQL5Indicator):
    name = 'BalanceOfPower_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения
        'XLength': 15,  # глубина усреднения
        'XPhase': 15,  # параметр усреднения,
        'HighLevel': 20,  # уровень перекупленности
        'LowLevel': -20,  # уровень перепроданности
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

