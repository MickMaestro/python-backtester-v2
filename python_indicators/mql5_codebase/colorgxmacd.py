"""colorgxmacd — converted from MQL5: MQL5 Indicators/GMACD/colorgxmacd.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 10, 3: 1, 4: 1}, 'colors': {1: [14822282, 16711935], 2: [8421504, 8421376, 14822282, 6053069, 16711935], 3: [65280], 4: [255]}, 'widths': {2: 2, 3: 1, 4: 1}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'GXMACD Cloud', 2: 'GXMACD', 3: 'Line', 4: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'colorgxmacd', 'source': 'MQL5 Indicators/GMACD/colorgxmacd.mq5', 'folder': 'GMACD', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'histogram smoothing method', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'int', 'default': 12, 'label': 'fast moving average period', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'int', 'default': 26, 'label': 'slow moving average period', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'moving averages smoothing parameter,', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 4, 'label': 'signal line smoothing method', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 9, 'label': 'signal line period', 'sinput': False}, {'mql': 'Signal_Phase', 'py': 'Signal_Phase', 'param': 'Signal_Phase', 'type': 'int', 'default': 100, 'label': 'signal line parameter,', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_T3)  # histogram smoothing method
Fast_XMA = _input('Fast_XMA', 12)  # fast moving average period
Slow_XMA = _input('Slow_XMA', 26)  # slow moving average period
XPhase = _input('XPhase', 100)  # moving averages smoothing parameter,
Signal_Method = _input('Signal_Method', MODE_JJMA)  # signal line smoothing method
Signal_XMA = _input('Signal_XMA', 9)  # signal line period
Signal_Phase = _input('Signal_Phase', 100)  # signal line parameter,
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # price constant
start = 0
macd_start = 0
LineBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
CLineBuffer = Arr(0, 0.0)
CSignBuffer = Arr(0, 0.0)
XMACDBuffer = Arr(0, 0.0)
ColorXMACDBuffer = Arr(0, 0.0)

def OnInit():
    global macd_start, start
    macd_start = MathMax(XMA1.GetStartBars(XMA_Method, Fast_XMA, XPhase), XMA1.GetStartBars(XMA_Method, Slow_XMA, XPhase))
    start = macd_start + XMA1.GetStartBars(Signal_Method, Signal_XMA, Signal_Phase)
    SetIndexBuffer(0, CLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
    SetIndexBuffer(1, CSignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
    SetIndexBuffer(2, XMACDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, macd_start)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ColorXMACDBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, macd_start + 1)
    SetIndexBuffer(4, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, macd_start)
    SetIndexBuffer(5, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, macd_start)
    XMA1.XMALengthCheck('Fast_XMA', Fast_XMA)
    XMA1.XMALengthCheck('Slow_XMA', Slow_XMA)
    XMA1.XMALengthCheck('Signal_XMA', Signal_XMA)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    XMA1.XMAPhaseCheck('Signal_Phase', Signal_Phase, Signal_Method)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    Smooth2 = XMA1.GetString_MA_Method(Signal_Method)
    StringConcatenate(shortname, 'GXMACD( ', Fast_XMA, ', ', Slow_XMA, ', ', Signal_XMA, ', ', Smooth1, ', ', Smooth2, ' )')
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
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = macd_start + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
    bar = first1
    for bar in range(bar, rates_total):
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fast_xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, price_, bar, False)
        slow_xma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, price_, bar, False)
        xmacd = fast_xma - slow_xma
        LineBuffer[bar] = xmacd
        CLineBuffer[bar] = xmacd
        sign_xma = XMA3.XMASeries(macd_start, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, xmacd, bar, False)
        XMACDBuffer[bar] = xmacd - sign_xma
        SignBuffer[bar] = sign_xma
        CSignBuffer[bar] = sign_xma
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorXMACDBuffer[bar] = 0.0
        if XMACDBuffer[bar] > 0:
            if XMACDBuffer[bar] > XMACDBuffer[bar - 1]:
                ColorXMACDBuffer[bar] = 1.0
            if XMACDBuffer[bar] < XMACDBuffer[bar - 1]:
                ColorXMACDBuffer[bar] = 2.0
        if XMACDBuffer[bar] < 0:
            if XMACDBuffer[bar] < XMACDBuffer[bar - 1]:
                ColorXMACDBuffer[bar] = 3.0
            if XMACDBuffer[bar] > XMACDBuffer[bar - 1]:
                ColorXMACDBuffer[bar] = 4.0
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


class Colorgxmacd(_MQL5Indicator):
    name = 'colorgxmacd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # histogram smoothing method
        'Fast_XMA': 12,  # fast moving average period
        'Slow_XMA': 26,  # slow moving average period
        'XPhase': 100,  # moving averages smoothing parameter,
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # signal line smoothing method
        'Signal_XMA': 9,  # signal line period
        'Signal_Phase': 100,  # signal line parameter,
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
    }

