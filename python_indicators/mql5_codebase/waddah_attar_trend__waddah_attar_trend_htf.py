"""Waddah_Attar_Trend — converted from MQL5: MQL5 Indicators/Waddah_Attar_Trend_HTF/Waddah_Attar_Trend.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16776960, 13850042]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Waddah_Attar_Trend'}, 'levels': [], 'description': [], 'name': 'Waddah_Attar_Trend', 'source': 'MQL5 Indicators/Waddah_Attar_Trend_HTF/Waddah_Attar_Trend.mq5', 'folder': 'Waddah_Attar_Trend_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'метод усреднения гистограммы', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'uint', 'default': 12, 'label': 'период быстрого мувинга MACD', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'uint', 'default': 26, 'label': 'период медленного мувинга MACD', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения мувингов MACD,', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'ценовая константа MACD', 'sinput': False}, {'mql': 'XXMethod', 'py': 'XXMethod', 'param': 'XXMethod', 'type': 'int', 'default': 4, 'label': 'метод усреднения MA', 'sinput': False}, {'mql': 'XXMA', 'py': 'XXMA', 'param': 'XXMA', 'type': 'int', 'default': 9, 'label': 'период MA', 'sinput': False}, {'mql': 'XXPhase', 'py': 'XXPhase', 'param': 'XXPhase', 'type': 'int', 'default': 100, 'label': 'параметр MA,', 'sinput': False}, {'mql': 'XXAppliedPrice', 'py': 'XXAppliedPrice', 'param': 'XXAppliedPrice', 'type': 'int', 'default': 1, 'label': 'ценовая константа MA', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_T3)  # метод усреднения гистограммы
Fast_XMA = _input('Fast_XMA', 12)  # период быстрого мувинга MACD
Slow_XMA = _input('Slow_XMA', 26)  # период медленного мувинга MACD
XPhase = _input('XPhase', 100)  # параметр усреднения мувингов MACD,
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # ценовая константа MACD
XXMethod = _input('XXMethod', MODE_JJMA)  # метод усреднения MA
XXMA = _input('XXMA', 9)  # период MA
XXPhase = _input('XXPhase', 100)  # параметр MA,
XXAppliedPrice = _input('XXAppliedPrice', PRICE_CLOSE_)  # ценовая константа MA
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Ind_Handle = 0

def OnInit():
    global min_rates_total
    min_rates_1 = MathMax(GetStartBars(XMA_Method, Fast_XMA, XPhase), GetStartBars(XMA_Method, Slow_XMA, XPhase))
    min_rates_2 = GetStartBars(XXMethod, XXMA, XXPhase)
    min_rates_total = MathMax(min_rates_1, min_rates_2)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Waddah_Attar_Trend')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    fast_xma = 0.0
    slow_xma = 0.0
    xmacd = 0.0
    xma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fast_xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, price, bar, False)
        slow_xma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, price, bar, False)
        xmacd = _fdiv(fast_xma - slow_xma, Point())
        price = PriceSeries(XXAppliedPrice, bar, open, low, high, close)
        xma = _fdiv(XMA3.XMASeries(0, prev_calculated, rates_total, XXMethod, XXPhase, XXMA, price, bar, False), Point())
        IndBuffer[bar] = xmacd * xma
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        if IndBuffer[bar] >= IndBuffer[bar - 1]:
            ColorIndBuffer[bar] = 0.0
        else:
            ColorIndBuffer[bar] = 1.0
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


class WaddahAttarTrend(_MQL5Indicator):
    name = 'Waddah_Attar_Trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения гистограммы
        'Fast_XMA': 12,  # период быстрого мувинга MACD
        'Slow_XMA': 26,  # период медленного мувинга MACD
        'XPhase': 100,  # параметр усреднения мувингов MACD,
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа MACD
        'XXMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения MA
        'XXMA': 9,  # период MA
        'XXPhase': 100,  # параметр MA,
        'XXAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа MA
    }

