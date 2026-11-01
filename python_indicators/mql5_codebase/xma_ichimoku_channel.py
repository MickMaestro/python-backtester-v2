"""xma_ichimoku_channel — converted from MQL5: MQL5 Indicators/XMA Ichimoku Channel/xma_ichimoku_channel.mq5

XMA Ichimoku Convert Channel
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [7451452], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 4, 2: 0, 3: 0}, 'labels': {1: 'Ichimoku XMA', 2: 'Up Ichimoku Convert', 3: 'Down Ichimoku Convert'}, 'levels': [], 'description': ['XMA Ichimoku Convert Channel'], 'name': 'xma_ichimoku_channel', 'source': 'MQL5 Indicators/XMA Ichimoku Channel/xma_ichimoku_channel.mq5', 'folder': 'XMA Ichimoku Channel', 'inputs': [{'mql': 'Up_period', 'py': 'Up_period', 'param': 'Up_period', 'type': 'uint', 'default': 3, 'label': 'High price calculation period', 'sinput': False}, {'mql': 'Dn_period', 'py': 'Dn_period', 'param': 'Dn_period', 'type': 'uint', 'default': 3, 'label': 'Low price calculation period', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 100, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'Up_percent', 'py': 'Up_percent', 'param': 'Up_percent', 'type': 'double', 'default': 1.0, 'label': 'Percentage of the deviation from the average for building the channel upper border', 'sinput': False}, {'mql': 'Dn_percent', 'py': 'Dn_percent', 'param': 'Dn_percent', 'type': 'double', 'default': 1.0, 'label': 'Percentage of the deviation from the average for building the channel lower border', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum MODE_PRICE
OPEN = 0
LOW = 1
HIGH = 2
CLOSE = 3
_enum('MODE_PRICE', {0: 'OPEN', 1: 'LOW', 2: 'HIGH', 3: 'CLOSE'})

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
Up_period = _input('Up_period', 3)  # High price calculation period
Dn_period = _input('Dn_period', 3)  # Low price calculation period
Up_mode = HIGH  # Highs searching prices
Dn_mode = LOW  # Lows searching prices
XMA_Method = _input('XMA_Method', MODE_SMA)  # Smoothing method
XLength = _input('XLength', 100)  # Smoothing depth
XPhase = _input('XPhase', 15)  # Smoothing parameter
Up_percent = _input('Up_percent', 1.0)  # Percentage of the deviation from the average for building the channel upper border
Dn_percent = _input('Dn_percent', 1.0)  # Percentage of the deviation from the average for building the channel lower border
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
XMA = Arr(0, 0.0)
UpLineBuffer = Arr(0, 0.0)
DnLineBuffer = Arr(0, 0.0)
dPriceShift = 0.0
StartBars = 0
StartBars1 = 0

def OnInit():
    global StartBars, StartBars1, dPriceShift
    StartBars1 = _int(MathMax(Up_period, Dn_period))
    StartBars = StartBars1 + XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, XMA, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(XMA, True)
    SetIndexBuffer(1, UpLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, DnLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpLineBuffer, True)
    ArraySetAsSeries(DnLineBuffer, True)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'XMA Ichimoku Convert Channel(', XLength, ', ', XPhase, ', ', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def FindMaximum(Open, High, Low, Close, Mode, index, period):
    max_ = 0
    Mode_ = Mode
    _sw1 = Mode_
    if _sw1 == OPEN:
        max_ = ArrayMaximum(Open, index, period)
    elif _sw1 == LOW:
        max_ = ArrayMaximum(Low, index, period)
    elif _sw1 == HIGH:
        max_ = ArrayMaximum(High, index, period)
    elif _sw1 == CLOSE:
        max_ = ArrayMaximum(Close, index, period)
    return max_

def FindMinimum(Open, High, Low, Close, Mode, index, period):
    min_ = 0
    Mode_ = Mode
    _sw2 = Mode_
    if _sw2 == OPEN:
        min_ = ArrayMinimum(Open, index, period)
    elif _sw2 == LOW:
        min_ = ArrayMinimum(Low, index, period)
    elif _sw2 == HIGH:
        min_ = ArrayMinimum(High, index, period)
    elif _sw2 == CLOSE:
        min_ = ArrayMinimum(Close, index, period)
    return min_

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    Ich_Up = 0.0
    Ich_Dn = 0.0
    limit = 0
    maxbar = 0
    maxbar = rates_total - 1 - StartBars1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    for bar in range(limit, 0 - 1, -1):
        Ich_Up = high[FindMaximum(open, high, low, close, Up_mode, bar, Up_period)]
        Ich_Dn = low[FindMinimum(open, high, low, close, Dn_mode, bar, Dn_period)]
        XMA[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, (Ich_Up + Ich_Dn) / 2, bar, True) + PriceShift
        UpLineBuffer[bar] = (1 + (Up_percent / 100)) * XMA[bar]
        DnLineBuffer[bar] = (1 - (Dn_percent / 100)) * XMA[bar]
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XmaIchimokuChannel(_MQL5Indicator):
    name = 'xma_ichimoku_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Up_period': 3,  # High price calculation period
        'Dn_period': 3,  # Low price calculation period
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'XLength': 100,  # Smoothing depth
        'XPhase': 15,  # Smoothing parameter
        'Up_percent': 1.0,  # Percentage of the deviation from the average for building the channel upper border
        'Dn_percent': 1.0,  # Percentage of the deviation from the average for building the channel lower border
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

