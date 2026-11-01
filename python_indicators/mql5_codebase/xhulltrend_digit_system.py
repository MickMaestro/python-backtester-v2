"""XHullTrend_Digit_System — converted from MQL5: MQL5 Indicators/XHullTrend_Digit_System/XHullTrend_Digit_System.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 7, 2: 17}, 'colors': {1: [15794135, 16641277], 2: [16760576, 16711680, 8421504, 2763429, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XHullTrend_Digit', 2: 'XHullTrend_Digit Open;XHullTrend_Digit High;XHullTrend_Digit Low;XHullTrend_Digit Close'}, 'levels': [], 'description': [], 'name': 'XHullTrend_Digit_System', 'source': 'MQL5 Indicators/XHullTrend_Digit_System/XHullTrend_Digit_System.mq5', 'folder': 'XHullTrend_Digit_System', 'inputs': [{'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 20, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'HLength', 'py': 'HLength', 'param': 'HLength', 'type': 'uint', 'default': 5, 'label': 'Период сглаживания HMA', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Цена индикатора', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XLength = _input('XLength', 20)  # Период индикатора
HLength = _input('HLength', 5)  # Период сглаживания HMA
IPC = _input('IPC', PRICE_CLOSE_)  # Цена индикатора
XMA_Method = _input('XMA_Method', MODE_LWMA_)  # Метод усреднения
XPhase = _input('XPhase', 15)  # Параметр сглаживания
Digit = _input('Digit', 2)  # количество разрядов округления
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_2 = 0
min_rates_total = 0
PointPow10 = 0.0
XLength2 = 0
SqrXLength = 0

def OnInit():
    global PointPow10, SqrXLength, XLength2, min_rates_1, min_rates_2, min_rates_total
    XLength2 = _int(_idiv(XLength, 2))
    SqrXLength = _int(MathFloor(MathSqrt(XLength)))
    PointPow10 = Point() * MathPow(10, Digit)
    min_rates_1 = GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_2 = min_rates_1 + GetStartBars(XMA_Method, HLength, XPhase)
    min_rates_total = min_rates_2 + GetStartBars(XMA_Method, SqrXLength, XPhase)
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, OpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, CloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XHullTrend_Digit_System(' + _str(XLength) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_xhma_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    xma = 0.0
    xma2 = 0.0
    hma = 0.0
    xhma = 0.0
    xxhma = 0.0
    diff = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma2 = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, price, bar, False)
        xma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, False)
        hma = (2 * xma2) - xma
        xhma = XMA3.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, HLength, hma, bar, False)
        xxhma = XMA4.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, SqrXLength, xhma, bar, False)
        ExtABuffer[bar] = PointPow10 * MathRound(_fdiv(xhma, PointPow10))
        ExtBBuffer[bar] = PointPow10 * MathRound(_fdiv(xxhma, PointPow10))
        diff = xhma - xxhma
        if diff and (not (ExtABuffer[bar] - ExtBBuffer[bar])):
            if diff > 0.0:
                ExtABuffer[bar] += PointPow10
            else:
                ExtBBuffer[bar] += PointPow10
        CloseBuffer[bar] = EMPTY_VALUE
        LowBuffer[bar] = CloseBuffer[bar]
        HighBuffer[bar] = LowBuffer[bar]
        OpenBuffer[bar] = HighBuffer[bar]
        if close[bar] > ExtABuffer[bar] and close[bar] > ExtBBuffer[bar]:
            if close[bar] >= open[bar]:
                ColorBuffer[bar] = 0.0
            else:
                ColorBuffer[bar] = 1.0
            OpenBuffer[bar] = open[bar]
            HighBuffer[bar] = high[bar]
            LowBuffer[bar] = low[bar]
            CloseBuffer[bar] = close[bar]
        if close[bar] < ExtABuffer[bar] and close[bar] < ExtBBuffer[bar]:
            if close[bar] <= open[bar]:
                ColorBuffer[bar] = 4.0
            else:
                ColorBuffer[bar] = 3.0
            OpenBuffer[bar] = open[bar]
            HighBuffer[bar] = high[bar]
            LowBuffer[bar] = low[bar]
            CloseBuffer[bar] = close[bar]
        if CloseBuffer[bar] == EMPTY_VALUE:
            if ColorBuffer[bar - 1] == 3 or ColorBuffer[bar + 1] == 4:
                if close[bar] <= open[bar]:
                    ColorBuffer[bar] = 4.0
                else:
                    ColorBuffer[bar] = 3.0
            if ColorBuffer[bar - 1] == 1 or ColorBuffer[bar + 1] == 0:
                if close[bar] >= open[bar]:
                    ColorBuffer[bar] = 0.0
                else:
                    ColorBuffer[bar] = 1.0
            OpenBuffer[bar] = open[bar]
            HighBuffer[bar] = high[bar]
            LowBuffer[bar] = low[bar]
            CloseBuffer[bar] = close[bar]
        if bar < rates_total:
            _s_OnCalculate_xhma_prev = xhma
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
XMA4 = _alloc(CXMA)
XMA4.__init__()

# ---- static local variables
_s_OnCalculate_xhma_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XHullTrendDigitSystem(_MQL5Indicator):
    name = 'XHullTrend_Digit_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XLength': 20,  # Период индикатора
        'HLength': 5,  # Период сглаживания HMA
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Цена индикатора
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения
        'XPhase': 15,  # Параметр сглаживания
        'Digit': 2,  # количество разрядов округления
    }

