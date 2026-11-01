"""hulltrendosma — converted from MQL5: MQL5 Indicators/HullTrendOSMA_HTF/hulltrendosma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 16711935, 8421504, 16748574, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'HullTrendOSMA'}, 'levels': [], 'description': [], 'name': 'hulltrendosma', 'source': 'MQL5 Indicators/HullTrendOSMA_HTF/hulltrendosma.mq5', 'folder': 'HullTrendOSMA_HTF', 'inputs': [{'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 20, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Цена индикатора', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 5, 'label': 'Период сглаживания индикатора', 'sinput': False}, {'mql': 'XMA_Method1', 'py': 'XMA_Method1', 'param': 'XMA_Method1', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'XPhase1', 'py': 'XPhase1', 'param': 'XPhase1', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XPhase = _input('XPhase', 15)  # Параметр усреднения
XLength1 = _input('XLength1', 5)  # Период сглаживания индикатора
XMA_Method1 = _input('XMA_Method1', MODE_JJMA)  # Метод сглаживания
XPhase1 = _input('XPhase1', 100)  # Параметр сглаживания
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_2 = 0
min_rates_total = 0
XLength2 = 0
SqrXLength = 0

def OnInit():
    global SqrXLength, XLength2, min_rates_1, min_rates_2, min_rates_total
    XLength2 = _int(_idiv(XLength, 2))
    SqrXLength = _int(MathFloor(MathSqrt(XLength)))
    min_rates_1 = GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_2 = min_rates_1 + GetStartBars(XMA_Method, SqrXLength, XPhase)
    min_rates_total = min_rates_2 + GetStartBars(XMA_Method1, XLength1, XPhase1) + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'HullTrendOSMA')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    clr = 0
    price = 0.0
    xma = 0.0
    xma2 = 0.0
    hma = 0.0
    xhma = 0.0
    osma = 0.0
    xosma = 0.0
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
        xhma = XMA3.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, SqrXLength, hma, bar, False)
        osma = hma - xhma
        xosma = XMA4.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method1, XPhase1, XLength1, osma, bar, False)
        xosma = _fdiv(xosma, Point())
        IndBuffer[bar] = xosma
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        xosma = IndBuffer[bar]
        diff = xosma - IndBuffer[bar - 1]
        if xosma > 0:
            if diff > 0:
                clr = 4
            if diff < 0:
                clr = 3
        if xosma < 0:
            if diff < 0:
                clr = 0
            if diff > 0:
                clr = 1
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
XMA4 = _alloc(CXMA)
XMA4.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Hulltrendosma(_MQL5Indicator):
    name = 'hulltrendosma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XLength': 20,  # Период индикатора
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Цена индикатора
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения
        'XPhase': 15,  # Параметр усреднения
        'XLength1': 5,  # Период сглаживания индикатора
        'XMA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания
        'XPhase1': 100,  # Параметр сглаживания
    }

