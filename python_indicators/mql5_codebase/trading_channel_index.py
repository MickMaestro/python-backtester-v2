"""Trading_Channel_Index — converted from MQL5: MQL5 Indicators/Trading_Channel_Index/Trading_Channel_Index.mq5

Trading Channel Index indicator
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_maximum': 70.0, 'indicator_minimum': -70.0}, 'types': {1: 10}, 'colors': {1: [3329330, 8421376, 8421504, 42495, 55295]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Trading Channel Index indicator'}, 'levels': [], 'description': ['Trading Channel Index indicator'], 'name': 'Trading_Channel_Index', 'source': 'MQL5 Indicators/Trading_Channel_Index/Trading_Channel_Index.mq5', 'folder': 'Trading_Channel_Index', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения индикатора', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 30, 'label': 'Глубина усреднения индикатора', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения индикатора,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания итогового индикатора', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 30, 'label': 'Глубина сглаживания итогового индикатора', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания итогового индикатора,', 'sinput': False}, {'mql': 'Coeff', 'py': 'Coeff', 'param': 'Coeff', 'type': 'double', 'default': 0.015, 'label': 'Coefficient', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 50, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -50, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MA_Method1 = _input('MA_Method1', MODE_SMA_)  # Метод усреднения индикатора
Length1 = _input('Length1', 30)  # Глубина усреднения индикатора
Phase1 = _input('Phase1', 15)  # Параметр усреднения индикатора,
MA_Method2 = _input('MA_Method2', MODE_SMA_)  # Метод сглаживания итогового индикатора
Length2 = _input('Length2', 30)  # Глубина сглаживания итогового индикатора
Phase2 = _input('Phase2', 100)  # Параметр сглаживания итогового индикатора,
Coeff = _input('Coeff', 0.015)  # Coefficient
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
HighLevel = _input('HighLevel', 50)  # уровень перезакупа
LowLevel = _input('LowLevel', -50)  # уровень перепроданности
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = min_rates_1 + min_rates_1
    min_rates_total = min_rates_2 + GetStartBars(MA_Method2, Length2, Phase2)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    shortname = Box("")
    StringConcatenate(shortname, 'Trading_Channel_Index(', Length1, ', ', Length2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
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
    price = 0.0
    xma = 0.0
    b1 = 0.0
    xb1 = 0.0
    b2 = 0.0
    tci = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price, bar, False)
        b1 = MathAbs(price - xma)
        if not b1:
            b1 = Point()
        xb1 = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, b1, bar, False)
        b2 = _fdiv(price - xma, b1 * Coeff)
        tci = XMA3.XMASeries(min_rates_2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, b2, bar, False)
        IndBuffer[bar] = tci
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        if IndBuffer[bar] > HighLevel:
            clr = 0
        elif IndBuffer[bar] > 0:
            clr = 1
        if IndBuffer[bar] < LowLevel:
            clr = 4
        elif IndBuffer[bar] < 0:
            clr = 3
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TradingChannelIndex(_MQL5Indicator):
    name = 'Trading_Channel_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения индикатора
        'Length1': 30,  # Глубина усреднения индикатора
        'Phase1': 15,  # Параметр усреднения индикатора,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания итогового индикатора
        'Length2': 30,  # Глубина сглаживания итогового индикатора
        'Phase2': 100,  # Параметр сглаживания итогового индикатора,
        'Coeff': 0.015,  # Coefficient
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'HighLevel': 50,  # уровень перезакупа
        'LowLevel': -50,  # уровень перепроданности
    }
    y_range = (-70.0, 70.0)

