"""colorcoppock — converted from MQL5: MQL5 Indicators/ColorCoppock/colorcoppock.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [9639167, 2237106, 8421504, 8421376, 8388352]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Coppock'}, 'levels': [], 'description': [], 'name': 'colorcoppock', 'source': 'MQL5 Indicators/ColorCoppock/colorcoppock.mq5', 'folder': 'ColorCoppock', 'inputs': [{'mql': 'ROC1Period', 'py': 'ROC1Period', 'param': 'ROC1Period', 'type': 'int', 'default': 14, 'label': 'first smoothing period', 'sinput': False}, {'mql': 'ROC2Period', 'py': 'ROC2Period', 'param': 'ROC2Period', 'type': 'int', 'default': 10, 'label': 'second smoothing period', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 3, 'label': 'histogram smoothing method', 'sinput': False}, {'mql': 'XMA_Period', 'py': 'XMA_Period', 'param': 'XMA_Period', 'type': 'int', 'default': 12, 'label': 'histogram smoothing period', 'sinput': False}, {'mql': 'XMA_Phase', 'py': 'XMA_Phase', 'param': 'XMA_Phase', 'type': 'int', 'default': 100, 'label': 'histogram smoothing parameter,', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
ROC1Period = _input('ROC1Period', 14)  # first smoothing period
ROC2Period = _input('ROC2Period', 10)  # second smoothing period
XMA_Method = _input('XMA_Method', MODE_LWMA)  # histogram smoothing method
XMA_Period = _input('XMA_Period', 12)  # histogram smoothing period
XMA_Phase = _input('XMA_Phase', 100)  # histogram smoothing parameter,
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # price constant
min_rates_ = 0
min_rates_total = 0
CoppBuffer = Arr(0, 0.0)
ColorCoppBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = MathMax(ROC1Period, ROC2Period)
    min_rates_total = min_rates_ + XMA1.GetStartBars(XMA_Method, XMA_Period, XMA_Phase)
    SetIndexBuffer(0, CoppBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorCoppBuffer, INDICATOR_COLOR_INDEX)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'Coppock( ', ROC1Period, ', ', ROC2Period, ', ', XMA_Period, ', ', XMA_Phase, ', ', Smooth, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price_0 = 0.0
    price_1 = 0.0
    price_2 = 0.0
    ROCSum = 0.0
    XROCSum = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_0 = PriceSeries(AppliedPrice, bar, open, low, high, close)
        price_1 = PriceSeries(AppliedPrice, bar - ROC1Period, open, low, high, close)
        price_2 = PriceSeries(AppliedPrice, bar - ROC2Period, open, low, high, close)
        ROCSum = _fdiv(price_0 - price_1, price_1) + _fdiv(price_0 - price_2, price_2)
        XROCSum = XMA1.XMASeries(min_rates_, prev_calculated, rates_total, XMA_Method, XMA_Phase, XMA_Period, ROCSum, bar, False)
        CoppBuffer[bar] = XROCSum
        ColorCoppBuffer[bar] = 2.0
        if XROCSum > 0:
            if XROCSum > CoppBuffer[bar - 1]:
                ColorCoppBuffer[bar] = 4.0
            if XROCSum < CoppBuffer[bar - 1]:
                ColorCoppBuffer[bar] = 3.0
        if XROCSum < 0:
            if XROCSum < CoppBuffer[bar - 1]:
                ColorCoppBuffer[bar] = 0.0
            if XROCSum > CoppBuffer[bar - 1]:
                ColorCoppBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorcoppock(_MQL5Indicator):
    name = 'colorcoppock'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ROC1Period': 14,  # first smoothing period
        'ROC2Period': 10,  # second smoothing period
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # histogram smoothing method
        'XMA_Period': 12,  # histogram smoothing period
        'XMA_Phase': 100,  # histogram smoothing parameter,
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # price constant
    }

