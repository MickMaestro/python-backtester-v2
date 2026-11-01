"""xdinma — converted from MQL5: MQL5 Indicators/XdinMA/xdinma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [36095]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'XdinMA'}, 'levels': [], 'description': [], 'name': 'xdinma', 'source': 'MQL5 Indicators/XdinMA/xdinma.mq5', 'folder': 'XdinMA', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'Length_main', 'py': 'Length_main', 'param': 'Length_main', 'type': 'int', 'default': 10, 'label': 'main smoothing depth', 'sinput': False}, {'mql': 'Length_plus', 'py': 'Length_plus', 'param': 'Length_plus', 'type': 'int', 'default': 20, 'label': 'plus smoothing depth', 'sinput': False}, {'mql': 'PhaseX', 'py': 'PhaseX', 'param': 'PhaseX', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA)  # Smoothing method
Length_main = _input('Length_main', 10)  # main smoothing depth
Length_plus = _input('Length_plus', 20)  # plus smoothing depth
PhaseX = _input('PhaseX', 15)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Applied price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
XdinMA = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    StartBars1 = XMA1.GetStartBars(MA_Method1, Length_main, PhaseX)
    StartBars2 = XMA2.GetStartBars(MA_Method1, Length_plus, PhaseX)
    min_rates_total = MathMax(StartBars1, StartBars2)
    XMA1.XMALengthCheck('Length_main', Length_main)
    XMA2.XMALengthCheck('Length_plus', Length_plus)
    XMA1.XMAPhaseCheck('PhaseX', PhaseX, MA_Method1)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, XdinMA, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(MA_Method1)
    StringConcatenate(shortname, 'XdinMA(', Length_main, ', ', Length_plus, ', ', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price_ = 0.0
    ma_main = 0.0
    ma_plus = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        ma_main = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, PhaseX, Length_main, price_, bar, False)
        ma_plus = XMA2.XMASeries(0, prev_calculated, rates_total, MA_Method1, PhaseX, Length_plus, price_, bar, False)
        XdinMA[bar] = (ma_main * 2) - ma_plus + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xdinma(_MQL5Indicator):
    name = 'xdinma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'Length_main': 10,  # main smoothing depth
        'Length_plus': 20,  # plus smoothing depth
        'PhaseX': 15,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Applied price
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

