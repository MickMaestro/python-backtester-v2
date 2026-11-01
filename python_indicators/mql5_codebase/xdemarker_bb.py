"""xdemarker_bb — converted from MQL5: MQL5 Indicators/XDeMarker_BB/xdemarker_bb.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 8}, 'types': {1: 8, 2: 1, 3: 12, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [8421504, 65280, 42495], 2: [8421504], 3: [8421504, 32768, 16711680, 255, 16711935], 4: [16711680], 5: [255], 6: [8421504], 7: [255], 8: [16711680]}, 'widths': {1: 2, 2: 1, 3: 3, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {1: 4, 2: 0, 3: 0, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4}, 'labels': {1: 'Signal line', 2: 'XDemark line', 3: 'XDemark arrow', 4: '+2Sigma', 5: '+Sigma', 6: 'Middle', 7: '-Sigma', 8: '-2Sigma'}, 'levels': [], 'description': [], 'name': 'xdemarker_bb', 'source': 'MQL5 Indicators/XDeMarker_BB/xdemarker_bb.mq5', 'folder': 'XDeMarker_BB', 'inputs': [{'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 5, 'label': 'DeMarker smoothing method', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 14, 'label': 'DeMarker period', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'Demarker smoothing parameter', 'sinput': False}, {'mql': 'SSmoothMethod', 'py': 'SSmoothMethod', 'param': 'SSmoothMethod', 'type': 'int', 'default': 4, 'label': 'Signal line smoothing method', 'sinput': False}, {'mql': 'SPeriod', 'py': 'SPeriod', 'param': 'SPeriod', 'type': 'int', 'default': 12, 'label': 'Signal line period', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'Signal line parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 100, 'label': 'Bollinger Bands period', 'sinput': False}, {'mql': 'BBDeviation1', 'py': 'BBDeviation1', 'param': 'BBDeviation1', 'type': 'double', 'default': 1.0, 'label': 'Small deviation value', 'sinput': False}, {'mql': 'BBDeviation2', 'py': 'BBDeviation2', 'param': 'BBDeviation2', 'type': 'double', 'default': 1.6, 'label': 'Big deviation value', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
DSmoothMethod = _input('DSmoothMethod', MODE_JurX)  # DeMarker smoothing method
DPeriod = _input('DPeriod', 14)  # DeMarker period
DPhase = _input('DPhase', 100)  # Demarker smoothing parameter
SSmoothMethod = _input('SSmoothMethod', MODE_JJMA)  # Signal line smoothing method
SPeriod = _input('SPeriod', 12)  # Signal line period
SPhase = _input('SPhase', 100)  # Signal line parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
BBPeriod = _input('BBPeriod', 100)  # Bollinger Bands period
BBDeviation1 = _input('BBDeviation1', 1.0)  # Small deviation value
BBDeviation2 = _input('BBDeviation2', 1.6)  # Big deviation value
XDemark = Arr(0, 0.0)
XDemarkLine = Arr(0, 0.0)
XXDemark = Arr(0, 0.0)
ColorXDemark = Arr(0, 0.0)
ColorXXDemark = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
quotient = 0.0
min_rates_total = 0
min_rates_totalD = 0
min_rates_totalS = 0
min_rates_totalB = 0

def OnInit():
    global min_rates_total, min_rates_totalB, min_rates_totalD, min_rates_totalS, quotient
    min_rates_totalD = UPXDemark.GetStartBars(DSmoothMethod, DPeriod, DPhase) + 1
    min_rates_totalS = min_rates_totalD + UPXDemark.GetStartBars(SSmoothMethod, SPeriod, SPhase)
    min_rates_totalB = min_rates_totalD + BBPeriod
    min_rates_total = MathMax(min_rates_totalS, min_rates_totalB)
    UPXDemark.XMALengthCheck('DPeriod', DPeriod)
    UPXDemark.XMALengthCheck('SPeriod', SPeriod)
    UPXDemark.XMAPhaseCheck('DPhase', DPhase, DSmoothMethod)
    UPXDemark.XMAPhaseCheck('SPhase', SPhase, SSmoothMethod)
    quotient = BBDeviation2 / BBDeviation1
    SetIndexBuffer(0, XXDemark, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_totalS + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorXXDemark, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_totalS + 1)
    SetIndexBuffer(2, XDemarkLine, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_totalD)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, XDemark, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_totalD + 1)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, ColorXDemark, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_totalD + 1)
    SetIndexBuffer(5, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(8, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(9, ExtLineBuffer5, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_totalB)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_totalB)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_totalB)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, min_rates_totalB)
    PlotIndexSetInteger(9, PLOT_DRAW_BEGIN, min_rates_totalB)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(9, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = ""
    Smooth = UPXDemark.GetString_MA_Method(DSmoothMethod)
    StringConcatenate(shortname, 'XDemark(', _str(DPeriod), ',', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    up_demark = 0.0
    dn_demark = 0.0
    up_xdemark = 0.0
    dn_xdemark = 0.0
    xdemark = 0.0
    xxdemark = 0.0
    xma = 0.0
    stdev1 = 0.0
    stdev2 = 0.0
    first1 = 0
    first2 = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 1
        first2 = min_rates_totalS + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
    bar = first1
    for bar in range(bar, rates_total):
        if high[bar] > high[bar - 1]:
            up_demark = high[bar] - high[bar - 1]
        else:
            up_demark = 0.0
        if low[bar] < low[bar - 1]:
            dn_demark = low[bar - 1] - low[bar]
        else:
            dn_demark = 0.0
        up_xdemark = UPXDemark.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, up_demark, bar, False)
        dn_xdemark = DNXDemark.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, dn_demark, bar, False)
        dn_xdemark += up_xdemark
        if dn_xdemark != 0:
            xdemark = _fdiv(up_xdemark, dn_xdemark)
        else:
            xdemark = EMPTY_VALUE
        XDemark[bar] = xdemark
        XDemarkLine[bar] = xdemark
        xxdemark = XSIGN.XMASeries(min_rates_totalD, prev_calculated, rates_total, SSmoothMethod, SPhase, SPeriod, xdemark, bar, False)
        XXDemark[bar] = xxdemark
        xma = XMA.XMASeries(min_rates_totalD + 1, prev_calculated, rates_total, MODE_SMA_, 0, BBPeriod, xdemark, bar, False)
        stdev1 = STD.StdDevSeries(min_rates_totalB, prev_calculated, rates_total, BBPeriod, BBDeviation1, xdemark, xma, bar, False)
        stdev2 = stdev1 * quotient
        if bar <= (min_rates_totalB + BBPeriod):
            xma = EMPTY_VALUE
            stdev1 = 0.0
            stdev2 = 0.0
        ExtLineBuffer1[bar] = xma + stdev2
        ExtLineBuffer2[bar] = xma + stdev1
        ExtLineBuffer3[bar] = xma
        ExtLineBuffer4[bar] = xma - stdev1
        ExtLineBuffer5[bar] = xma - stdev2
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorXDemark[bar] = 0.0
        if XDemark[bar] > ExtLineBuffer3[bar]:
            if XDemark[bar] > XDemark[bar - 1]:
                ColorXDemark[bar] = 1.0
            if XDemark[bar] < XDemark[bar - 1]:
                ColorXDemark[bar] = 2.0
        if XDemark[bar] < ExtLineBuffer3[bar]:
            if XDemark[bar] < XDemark[bar - 1]:
                ColorXDemark[bar] = 3.0
            if XDemark[bar] > XDemark[bar - 1]:
                ColorXDemark[bar] = 4.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorXXDemark[bar] = 0.0
        if XDemark[bar] > XXDemark[bar - 1]:
            ColorXXDemark[bar] = 1.0
        if XDemark[bar] < XXDemark[bar - 1]:
            ColorXXDemark[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
UPXDemark = _alloc(CXMA)
UPXDemark.__init__()
DNXDemark = _alloc(CXMA)
DNXDemark.__init__()
XSIGN = _alloc(CXMA)
XSIGN.__init__()
XMA = _alloc(CXMA)
XMA.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XdemarkerBb(_MQL5Indicator):
    name = 'xdemarker_bb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=5),  # DeMarker smoothing method
        'DPeriod': 14,  # DeMarker period
        'DPhase': 100,  # Demarker smoothing parameter
        'SSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Signal line smoothing method
        'SPeriod': 12,  # Signal line period
        'SPhase': 100,  # Signal line parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'BBPeriod': 100,  # Bollinger Bands period
        'BBDeviation1': 1.0,  # Small deviation value
        'BBDeviation2': 1.6,  # Big deviation value
    }

