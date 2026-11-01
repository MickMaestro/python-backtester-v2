"""xkri_histogram — converted from MQL5: MQL5 Indicators/XKRI_Histogram_HTF/xkri_histogram.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 2330219, 16748574, 9639167, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'XKRI'}, 'levels': [], 'description': [], 'name': 'xkri_histogram', 'source': 'MQL5 Indicators/XKRI_Histogram_HTF/xkri_histogram.mq5', 'folder': 'XKRI_Histogram_HTF', 'inputs': [{'mql': 'KRIPeriod', 'py': 'KRIPeriod', 'param': 'KRIPeriod', 'type': 'uint', 'default': 20, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'Ratio', 'py': 'Ratio', 'param': 'Ratio', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 7, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 1.0, 'label': 'Уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -1.0, 'label': 'Уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_PRICE_TYPE
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
_enum('ENUM_PRICE_TYPE', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
KRIPeriod = _input('KRIPeriod', 20)  # Период усреднения
MA_Method_ = _input('MA_Method_', MODE_SMA)  # Метод усреднения
Ratio = _input('Ratio', 1.0)
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
XMA_Method = _input('XMA_Method', MODE_JJMA)  # Метод усреднения
XLength = _input('XLength', 7)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
HighLevel = _input('HighLevel', 1.0)  # Уровень перекупленности
LowLevel = _input('LowLevel', -1.0)  # Уровень перепроданности
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = _int(KRIPeriod + 1)
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method, XLength, XPhase)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    shortname = Box("")
    StringConcatenate(shortname, 'XKRI( KRIPeriod = ', KRIPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    KRI = 0.0
    mov = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated == 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        mov = MA.MASeries(0, prev_calculated, rates_total, KRIPeriod, MA_Method_, price, bar, False)
        KRI = _fdiv(100 * (price - mov), mov)
        IndBuffer[bar] = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, KRI, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 0
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 1
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 2
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 3
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 4
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
MA = _alloc(CMoving_Average)
MA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XkriHistogram(_MQL5Indicator):
    name = 'xkri_histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KRIPeriod': 20,  # Период усреднения
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Метод усреднения
        'Ratio': 1.0,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'XLength': 7,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'HighLevel': 1.0,  # Уровень перекупленности
        'LowLevel': -1.0,  # Уровень перепроданности
    }

