"""ColorJJRSX — converted from MQL5: MQL5 Indicators/ColorJJRSX_HTF/ColorJJRSX.mq5

Relative Strenght Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 10}, 'colors': {1: [8421504], 2: [255, 36095, 8421504, 8421376, 65280]}, 'widths': {1: 1, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'JJRSX', 2: 'High Short;Short;Flat;Long;High Long'}, 'levels': [], 'description': ['Relative Strenght Index'], 'name': 'ColorJJRSX', 'source': 'MQL5 Indicators/ColorJJRSX_HTF/ColorJJRSX.mq5', 'folder': 'ColorJJRSX_HTF', 'inputs': [{'mql': 'JurXPeriod', 'py': 'JurXPeriod', 'param': 'JurXPeriod', 'type': 'uint', 'default': 8, 'label': 'период JurX', 'sinput': False}, {'mql': 'JMAPeriod', 'py': 'JMAPeriod', 'param': 'JMAPeriod', 'type': 'uint', 'default': 3, 'label': 'период JMA', 'sinput': False}, {'mql': 'JMAPhase', 'py': 'JMAPhase', 'param': 'JMAPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения JMA,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Style', 'py': 'Style', 'param': 'Style', 'type': 'int', 'default': 10, 'label': 'стиль отображения JJRSX', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 20, 'label': 'верхний уровень срабатывания', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': 'середина диапазона', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -20, 'label': 'нижний уровень срабатывания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# enum IndStyle
COLOR_LINE = 8
COLOR_HISTOGRAM = 10
COLOR_ARROW = 12
_enum('IndStyle', {8: 'COLOR_LINE', 10: 'COLOR_HISTOGRAM', 12: 'COLOR_ARROW'})

# ---- inputs and global variables
JurXPeriod = _input('JurXPeriod', 8)  # период JurX
JMAPeriod = _input('JMAPeriod', 3)  # период JMA
JMAPhase = _input('JMAPhase', 100)  # параметр усреднения JMA,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Style = _input('Style', COLOR_HISTOGRAM)  # стиль отображения JJRSX
HighLevel = _input('HighLevel', 20)  # верхний уровень срабатывания
MiddleLevel = _input('MiddleLevel', 0)  # середина диапазона
LowLevel = _input('LowLevel', -20)  # нижний уровень срабатывания
JJRSX = Arr(0, 0.0)
JJRSX_ = Arr(0, 0.0)
ColorJJRSX = Arr(0, 0.0)
min_rates_total = 0
min_rates_ = 0

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = 2
    min_rates_total = min_rates_ + 30
    SetIndexBuffer(0, JJRSX_, INDICATOR_DATA)
    SetIndexBuffer(1, JJRSX, INDICATOR_DATA)
    SetIndexBuffer(2, ColorJJRSX, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, Style)
    shortname = Box("")
    StringConcatenate(shortname, 'Relative Strenght Index(', _str(JurXPeriod), ',', _str(JMAPeriod), ',', _str(JMAPhase), ',', EnumToString(IPC, 'Applied_price_'), ',', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    dPrice = 0.0
    AbsdPrice = 0.0
    jrsx = 0.0
    uprsx = 0.0
    dnrsx = 0.0
    first = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        dPrice = PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar - 1, open, low, high, close)
        AbsdPrice = MathAbs(dPrice)
        if not AbsdPrice:
            AbsdPrice = Point()
        JJRSX[bar] = EMPTY_VALUE
        uprsx = UpJurX.JurXSeries(1, prev_calculated, rates_total, 0, JurXPeriod, dPrice, bar, False)
        dnrsx = DnJurX.JurXSeries(1, prev_calculated, rates_total, 0, JurXPeriod, AbsdPrice, bar, False)
        jrsx = _fdiv(100 * uprsx, dnrsx)
        JJRSX[bar] = JMA.JJMASeries(min_rates_, prev_calculated, rates_total, 0, JMAPhase, JMAPeriod, jrsx, bar, False)
        JJRSX_[bar] = JJRSX[bar]
        clr = 2
        if JJRSX[bar] > JJRSX[bar - 1]:
            if JJRSX[bar] > HighLevel:
                clr = 4
            else:
                clr = 3
        if JJRSX[bar] < JJRSX[bar - 1]:
            if JJRSX[bar] < LowLevel:
                clr = 0
            else:
                clr = 1
        ColorJJRSX[bar] = clr
    return rates_total

# ---- global variables initialised from expressions
JMA = _alloc(CJJMA)
JMA.__init__()
UpJurX = _alloc(CJurX)
UpJurX.__init__()
DnJurX = _alloc(CJurX)
DnJurX.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorJJRSXIndicator(_MQL5Indicator):
    name = 'ColorJJRSX'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JurXPeriod': 8,  # период JurX
        'JMAPeriod': 3,  # период JMA
        'JMAPhase': 100,  # параметр усреднения JMA,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Style': _Choice({8: 'Цветная линия', 10: 'Цветная гистограмма', 12: 'Цветные значки'}, default=10),  # стиль отображения JJRSX
        'HighLevel': 20,  # верхний уровень срабатывания
        'MiddleLevel': 0,  # середина диапазона
        'LowLevel': -20,  # нижний уровень срабатывания
    }

