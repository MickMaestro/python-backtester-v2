"""Waddah_Attar_Trend_Candles — converted from MQL5: MQL5 Indicators/Waddah_Attar_Trend_Candles_HTF/Waddah_Attar_Trend_Candles.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16748574, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Waddah_Attar_Trend_Open;Waddah_Attar_Trend_High;Waddah_Attar_Trend_Low;Waddah_Attar_Trend_Close'}, 'levels': [], 'description': [], 'name': 'Waddah_Attar_Trend_Candles', 'source': 'MQL5 Indicators/Waddah_Attar_Trend_Candles_HTF/Waddah_Attar_Trend_Candles.mq5', 'folder': 'Waddah_Attar_Trend_Candles_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'метод усреднения гистограммы', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'uint', 'default': 12, 'label': 'период быстрого мувинга MACD', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'uint', 'default': 26, 'label': 'период медленного мувинга MACD', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения мувингов MACD,', 'sinput': False}, {'mql': 'XXMethod', 'py': 'XXMethod', 'param': 'XXMethod', 'type': 'int', 'default': 4, 'label': 'метод усреднения MA', 'sinput': False}, {'mql': 'XXMA', 'py': 'XXMA', 'param': 'XXMA', 'type': 'int', 'default': 9, 'label': 'период MA', 'sinput': False}, {'mql': 'XXPhase', 'py': 'XXPhase', 'param': 'XXPhase', 'type': 'int', 'default': 100, 'label': 'параметр MA,', 'sinput': False}, {'mql': 'GapMinimum', 'py': 'GapMinimum', 'param': 'GapMinimum', 'type': 'uint', 'default': 10, 'label': 'минимальный гэп в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XXMethod = _input('XXMethod', MODE_JJMA)  # метод усреднения MA
XXMA = _input('XXMA', 9)  # период MA
XXPhase = _input('XXPhase', 100)  # параметр MA,
GapMinimum = _input('GapMinimum', 10)  # минимальный гэп в пунктах
min_rates_total = 0
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_1 = MathMax(GetStartBars(XMA_Method, Fast_XMA, XPhase), GetStartBars(XMA_Method, Slow_XMA, XPhase))
    min_rates_2 = GetStartBars(XXMethod, XXMA, XXPhase)
    min_rates_total = MathMax(min_rates_1, min_rates_2)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Waddah_Attar_Trend_Candles')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    price = Arr(4, 0.0, dyn=False)
    fast_xma = 0.0
    slow_xma = 0.0
    xmacd = 0.0
    xma = 0.0
    watrend = Arr(4, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        ArrayInitialize(watrend, None)
        ExtCloseBuffer[first - 1] = 0.0
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        price[0] = open[bar]
        price[1] = high[bar]
        price[2] = low[bar]
        price[3] = close[bar]
        ArrayInitialize(watrend, None)
        for count in range(0, 4):
            fast_xma = XMA1[count].XMASeries(1, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, price[count], bar, False)
            slow_xma = XMA2[count].XMASeries(1, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, price[count], bar, False)
            xmacd = _fdiv(fast_xma - slow_xma, Point())
            xma = _fdiv(XMA3[count].XMASeries(1, prev_calculated, rates_total, XXMethod, XXPhase, XXMA, price[count], bar, False), Point())
            watrend[count] = xmacd * xma
        if MathAbs(open[bar] - close[bar - 1]) < GapMinimum:
            watrend[0] = ExtCloseBuffer[bar - 1]
        ExtHighBuffer[bar] = watrend[3 - ArrayMaximum(watrend)]
        ExtLowBuffer[bar] = watrend[3 - ArrayMinimum(watrend)]
        ExtOpenBuffer[bar] = watrend[0]
        ExtCloseBuffer[bar] = watrend[3]
        if ExtCloseBuffer[bar] >= ExtOpenBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    return rates_total

# ---- global variables initialised from expressions
XMA1 = Arr(4, 0, dyn=False, factory=CXMA)
XMA2 = Arr(4, 0, dyn=False, factory=CXMA)
XMA3 = Arr(4, 0, dyn=False, factory=CXMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WaddahAttarTrendCandles(_MQL5Indicator):
    name = 'Waddah_Attar_Trend_Candles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения гистограммы
        'Fast_XMA': 12,  # период быстрого мувинга MACD
        'Slow_XMA': 26,  # период медленного мувинга MACD
        'XPhase': 100,  # параметр усреднения мувингов MACD,
        'XXMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения MA
        'XXMA': 9,  # период MA
        'XXPhase': 100,  # параметр MA,
        'GapMinimum': 10,  # минимальный гэп в пунктах
    }

