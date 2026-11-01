"""colorxosma — converted from MQL5: MQL5 Indicators/ColorXOSMA_HTF/colorxosma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 2330219, 16748574, 9639167, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'XOSMA'}, 'levels': [], 'description': [], 'name': 'colorxosma', 'source': 'MQL5 Indicators/ColorXOSMA_HTF/colorxosma.mq5', 'folder': 'ColorXOSMA_HTF', 'inputs': [{'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 7, 'label': 'histogram smoothing method', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'int', 'default': 12, 'label': '/Fast moving average period', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'int', 'default': 26, 'label': 'Slow moving average period', 'sinput': False}, {'mql': 'Phase', 'py': 'Phase', 'param': 'Phase', 'type': 'int', 'default': 100, 'label': 'moving averages smoothing parameter', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 4, 'label': 'Signal line smoothing method', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 9, 'label': 'signal line period', 'sinput': False}, {'mql': 'Signal_Phase', 'py': 'Signal_Phase', 'param': 'Signal_Phase', 'type': 'int', 'default': 100, 'label': 'signal line parameter', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'Smooth_XMA', 'py': 'Smooth_XMA', 'param': 'Smooth_XMA', 'type': 'int', 'default': 9, 'label': 'period of the indicator smoothing', 'sinput': False}, {'mql': 'Smooth_Phase', 'py': 'Smooth_Phase', 'param': 'Smooth_Phase', 'type': 'int', 'default': 100, 'label': 'indicator parameter,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
MA_Method = _input('MA_Method', MODE_T3)  # histogram smoothing method
Fast_XMA = _input('Fast_XMA', 12)  # /Fast moving average period
Slow_XMA = _input('Slow_XMA', 26)  # Slow moving average period
Phase = _input('Phase', 100)  # moving averages smoothing parameter
Signal_Method = _input('Signal_Method', MODE_JJMA)  # Signal line smoothing method
Signal_XMA = _input('Signal_XMA', 9)  # signal line period
Signal_Phase = _input('Signal_Phase', 100)  # signal line parameter
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # price constant
Smooth_XMA = _input('Smooth_XMA', 9)  # period of the indicator smoothing
Smooth_Phase = _input('Smooth_Phase', 100)  # indicator parameter,
start = 0
macd_start = 0
jmacd_start = 0
XOSMABuffer = Arr(0, 0.0)
ColorXOSMABuffer = Arr(0, 0.0)

def OnInit():
    global jmacd_start, macd_start, start
    macd_start = MathMax(XMA1.GetStartBars(MA_Method, Fast_XMA, Phase), XMA1.GetStartBars(MA_Method, Slow_XMA, Phase))
    jmacd_start = macd_start + XMA1.GetStartBars(Signal_Method, Signal_XMA, Signal_Phase)
    start = jmacd_start + 30
    SetIndexBuffer(0, XOSMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, macd_start)
    PlotIndexSetString(0, PLOT_LABEL, 'XOSMA')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorXOSMABuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, macd_start + 1)
    XMA1.XMALengthCheck('Fast_XMA', Fast_XMA)
    XMA1.XMALengthCheck('Slow_XMA', Slow_XMA)
    XMA1.XMALengthCheck('Signal_XMA', Signal_XMA)
    XMA1.XMALengthCheck('Smooth_XMA', Smooth_XMA)
    XMA1.XMAPhaseCheck('Phase', Phase, MA_Method)
    XMA1.XMAPhaseCheck('Signal_Phase', Signal_Phase, Signal_Method)
    XMA1.XMAPhaseCheck('Smooth_Phase', Smooth_Phase, MODE_JJMA)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method)
    Smooth2 = XMA1.GetString_MA_Method(Signal_Method)
    StringConcatenate(shortname, 'XOSMA( ', Fast_XMA, ', ', Slow_XMA, ', ', Signal_XMA, ', ', Smooth1, ', ', Smooth2, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < start:
        return 0
    first1 = 0
    first2 = 0
    bar = 0
    price_ = 0.0
    fast_xma = 0.0
    slow_xma = 0.0
    xmacd = 0.0
    sign_xma = 0.0
    xosma = 0.0
    jxosma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = macd_start + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
    bar = first1
    for bar in range(bar, rates_total):
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fast_xma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method, Phase, Fast_XMA, price_, bar, False)
        slow_xma = XMA2.XMASeries(0, prev_calculated, rates_total, MA_Method, Phase, Slow_XMA, price_, bar, False)
        xmacd = fast_xma - slow_xma
        sign_xma = XMA3.XMASeries(macd_start, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, xmacd, bar, False)
        xosma = xmacd - sign_xma
        jxosma = XMA4.XMASeries(jmacd_start, prev_calculated, rates_total, MODE_JJMA, Smooth_Phase, Smooth_XMA, xosma, bar, False)
        if bar >= start:
            XOSMABuffer[bar] = jxosma
        else:
            XOSMABuffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorXOSMABuffer[bar] = 0.0
        if XOSMABuffer[bar] > 0:
            if XOSMABuffer[bar] > XOSMABuffer[bar - 1]:
                ColorXOSMABuffer[bar] = 1.0
            if XOSMABuffer[bar] < XOSMABuffer[bar - 1]:
                ColorXOSMABuffer[bar] = 2.0
        if XOSMABuffer[bar] < 0:
            if XOSMABuffer[bar] < XOSMABuffer[bar - 1]:
                ColorXOSMABuffer[bar] = 3.0
            if XOSMABuffer[bar] > XOSMABuffer[bar - 1]:
                ColorXOSMABuffer[bar] = 4.0
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


class Colorxosma(_MQL5Indicator):
    name = 'colorxosma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # histogram smoothing method
        'Fast_XMA': 12,  # /Fast moving average period
        'Slow_XMA': 26,  # Slow moving average period
        'Phase': 100,  # moving averages smoothing parameter
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Signal line smoothing method
        'Signal_XMA': 9,  # signal line period
        'Signal_Phase': 100,  # signal line parameter
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
        'Smooth_XMA': 9,  # period of the indicator smoothing
        'Smooth_Phase': 100,  # indicator parameter,
    }

