"""hulltrend — converted from MQL5: MQL5 Indicators/BackgroundCandle_HullTrend_HTF/hulltrend.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [10156544, 15631086]}, 'widths': {}, 'styles': {}, 'labels': {1: 'HullTrend'}, 'levels': [], 'description': [], 'name': 'hulltrend', 'source': 'MQL5 Indicators/BackgroundCandle_HullTrend_HTF/hulltrend.mq5', 'folder': 'BackgroundCandle_HullTrend_HTF', 'inputs': [{'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 20, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Цена индикатора', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
IPC = _input('IPC', PRICE_CLOSE)  # Цена индикатора
XMA_Method = _input('XMA_Method', MODE_LWMA)  # Метод усреднения
XPhase = _input('XPhase', 15)  # Параметр сглаживания
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_2 = 0
min_rates_total = 0
XLength2 = 0
SqrXLength = 0

def OnInit():
    global SqrXLength, XLength2, min_rates_1, min_rates_total
    XLength2 = _int(_idiv(XLength, 2))
    SqrXLength = _int(MathFloor(MathSqrt(XLength)))
    min_rates_1 = XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_total = min_rates_1 + XMA1.GetStartBars(XMA_Method, SqrXLength, XPhase)
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'HullTrend')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    xma = 0.0
    xma2 = 0.0
    hma = 0.0
    xhma = 0.0
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
        xhma = XMA3.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, SqrXLength, hma, bar, False)
        ExtABuffer[bar] = hma
        ExtBBuffer[bar] = xhma
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


class Hulltrend(_MQL5Indicator):
    name = 'hulltrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XLength': 20,  # Период индикатора
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Цена индикатора
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения
        'XPhase': 15,  # Параметр сглаживания
    }

