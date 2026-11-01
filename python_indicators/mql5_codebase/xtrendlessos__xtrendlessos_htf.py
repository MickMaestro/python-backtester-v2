"""XTrendlessOS — converted from MQL5: MQL5 Indicators/XTrendlessOS_HTF/XTrendlessOS.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711680, 65280, 8421504, 32768, 8721863, 255, 16711935]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'XTrendlessOS'}, 'levels': [], 'description': [], 'name': 'XTrendlessOS', 'source': 'MQL5 Indicators/XTrendlessOS_HTF/XTrendlessOS.mq5', 'folder': 'XTrendlessOS_HTF', 'inputs': [{'mql': 'TMA_Method', 'py': 'TMA_Method', 'param': 'TMA_Method', 'type': 'int', 'default': 5, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'TLength', 'py': 'TLength', 'param': 'TLength', 'type': 'int', 'default': 7, 'label': 'глубина  усреднения', 'sinput': False}, {'mql': 'TPhase', 'py': 'TPhase', 'param': 'TPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'OBLevel', 'py': 'OBLevel', 'param': 'OBLevel', 'type': 'double', 'default': 0.00473, 'label': 'граница уровня перекупленности', 'sinput': False}, {'mql': 'OSLevel', 'py': 'OSLevel', 'param': 'OSLevel', 'type': 'double', 'default': -0.00473, 'label': 'граница уровня перепроданности', 'sinput': False}, {'mql': 'LevelsColor', 'py': 'LevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'цвет уровней', 'sinput': False}, {'mql': 'LevelsStyle', 'py': 'LevelsStyle', 'param': 'LevelsStyle', 'type': 'int', 'default': 4, 'label': 'стиль уровней', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'толщина дневной линии', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

Red = 0x0000FF  # MQL4 colour name

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

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
TMA_Method = _input('TMA_Method', MODE_JurX)  # метод усреднения
TLength = _input('TLength', 7)  # глубина  усреднения
TPhase = _input('TPhase', 100)  # параметр усреднения,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
OBLevel = _input('OBLevel', 0.00473)  # граница уровня перекупленности
OSLevel = _input('OSLevel', -0.00473)  # граница уровня перепроданности
LevelsStyle = _input('LevelsStyle', STYLE_DASHDOTDOT)  # стиль уровней
LevelsWidth = _input('LevelsWidth', w_1)  # толщина дневной линии
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
OBLevel06 = 0.0
OBLevel08 = 0.0
OSLevel06 = 0.0
OSLevel08 = 0.0

def OnInit():
    global OBLevel06, OBLevel08, OSLevel06, OSLevel08, min_rates_total
    min_rates_total = XMA.GetStartBars(TMA_Method, TLength, TPhase)
    XMA.XMALengthCheck('TLength', TLength)
    XMA.XMAPhaseCheck('TPhase', TPhase, TMA_Method)
    OBLevel06 = 0.6 * OBLevel
    OBLevel08 = 0.8 * OBLevel
    OSLevel06 = 0.6 * OSLevel
    OSLevel08 = 0.8 * OSLevel
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    Smooth = XMA.GetString_MA_Method(TMA_Method)
    StringConcatenate(shortname, 'XTrendlessOS(', TLength, ', ', TLength, ', ', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 6)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, LevelsWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 3, LevelsWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 4, LevelsWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 5, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 5, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 5, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, OBLevel06)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, OBLevel08)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, OSLevel06)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, OSLevel08)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, OSLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, OBLevel)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price_ = 0.0
    xma = 0.0
    current = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMA.XMASeries(0, prev_calculated, rates_total, TMA_Method, TPhase, TLength, price_, bar, False)
        IndBuffer[bar] = price_ - xma
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        ColorIndBuffer[bar] = 0.0
        current = IndBuffer[bar]
        if current > OBLevel:
            ColorIndBuffer[bar] = 6.0
        elif current > OBLevel08:
            ColorIndBuffer[bar] = 5.0
        elif current > OBLevel06:
            ColorIndBuffer[bar] = 4.0
        if current < OSLevel:
            ColorIndBuffer[bar] = 1.0
        elif current < OSLevel08:
            ColorIndBuffer[bar] = 2.0
        elif current < OSLevel06:
            ColorIndBuffer[bar] = 3.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()
LevelsColor = _input('LevelsColor', _uint(Red))  # цвет уровней


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XTrendlessOS(_MQL5Indicator):
    name = 'XTrendlessOS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=5),  # метод усреднения
        'TLength': 7,  # глубина  усреднения
        'TPhase': 100,  # параметр усреднения,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'OBLevel': 0.00473,  # граница уровня перекупленности
        'OSLevel': -0.00473,  # граница уровня перепроданности
        'LevelsStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # стиль уровней
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина дневной линии
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

