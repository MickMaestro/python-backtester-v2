"""atr_channels — converted from MQL5: MQL5 Indicators/ATR Channels/atr_channels.mq5

ATR Channels
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [14822282], 2: [8388736], 3: [255], 4: [16711680], 5: [16711680], 6: [255], 7: [8388736]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4}, 'labels': {1: 'XMA', 2: '+3 Envelope', 3: '+2 Envelope', 4: '+1 Envelope', 5: '-1 Envelope', 6: '-2 Envelope', 7: '-3 Envelope'}, 'levels': [], 'description': ['ATR Channels'], 'name': 'atr_channels', 'source': 'MQL5 Indicators/ATR Channels/atr_channels.mq5', 'folder': 'ATR Channels', 'inputs': [{'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 18, 'label': '', 'sinput': False}, {'mql': 'Mult_Factor1', 'py': 'Mult_Factor1', 'param': 'Mult_Factor1', 'type': 'double', 'default': 1.6, 'label': '', 'sinput': False}, {'mql': 'Mult_Factor2', 'py': 'Mult_Factor2', 'param': 'Mult_Factor2', 'type': 'double', 'default': 3.2, 'label': '', 'sinput': False}, {'mql': 'Mult_Factor3', 'py': 'Mult_Factor3', 'param': 'Mult_Factor3', 'type': 'double', 'default': 4.8, 'label': '', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'SmLength', 'py': 'SmLength', 'param': 'SmLength', 'type': 'int', 'default': 100, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'SmPhase', 'py': 'SmPhase', 'param': 'SmPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
ATRPeriod = _input('ATRPeriod', 18)
Mult_Factor1 = _input('Mult_Factor1', 1.6)
Mult_Factor2 = _input('Mult_Factor2', 3.2)
Mult_Factor3 = _input('Mult_Factor3', 4.8)
MA_SMethod = _input('MA_SMethod', MODE_SMA)  # Smoothing method
SmLength = _input('SmLength', 100)  # Smoothing depth
SmPhase = _input('SmPhase', 15)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
ExtLineBuffer0 = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
dPriceShift = 0.0
ATR_Handle = 0
StartBarsXMA = 0
StartBarsATR = 0
StartBars = 0

def OnInit():
    global ATR_Handle, StartBars, StartBarsATR, StartBarsXMA, dPriceShift
    ATR_Handle = iATR(None, PERIOD_CURRENT, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    StartBarsXMA = XMA.GetStartBars(MA_SMethod, SmLength, SmPhase) + 1
    StartBarsATR = StartBarsXMA + ATRPeriod
    StartBars = StartBarsXMA + StartBarsATR
    XMA.XMALengthCheck('Length', SmLength)
    XMA.XMAPhaseCheck('Phase', SmPhase, MA_SMethod)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'XMA')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(ExtLineBuffer0, True)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer6, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, '+3 Envelope')
    PlotIndexSetString(2, PLOT_LABEL, '+2 Envelope')
    PlotIndexSetString(3, PLOT_LABEL, '+1 Envelope')
    PlotIndexSetString(4, PLOT_LABEL, '-1 Envelope')
    PlotIndexSetString(5, PLOT_LABEL, '-2 Envelope')
    PlotIndexSetString(6, PLOT_LABEL, '-3 Envelope')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    shortname = Box("")
    Smooth = XMA.GetString_MA_Method(MA_SMethod)
    StringConcatenate(shortname, 'ATR Channels(', SmLength, ' ', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < StartBars:
        return 0
    price_ = 0.0
    xxma = 0.0
    Range = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, Range) <= 0:
        return 0
    ArraySetAsSeries(Range, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        xxma = XMA.XMASeries(rates_total - 1, prev_calculated, rates_total, MA_SMethod, SmPhase, SmLength, price_, bar, True)
        ExtLineBuffer0[bar] = xxma + dPriceShift
        ExtLineBuffer1[bar] = xxma + (Range[bar] * Mult_Factor3) + dPriceShift
        ExtLineBuffer2[bar] = xxma + (Range[bar] * Mult_Factor2) + dPriceShift
        ExtLineBuffer3[bar] = xxma + (Range[bar] * Mult_Factor1) + dPriceShift
        ExtLineBuffer4[bar] = xxma - (Range[bar] * Mult_Factor1) + dPriceShift
        ExtLineBuffer5[bar] = xxma - (Range[bar] * Mult_Factor2) + dPriceShift
        ExtLineBuffer6[bar] = xxma - (Range[bar] * Mult_Factor3) + dPriceShift
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AtrChannels(_MQL5Indicator):
    name = 'atr_channels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATRPeriod': 18,
        'Mult_Factor1': 1.6,
        'Mult_Factor2': 3.2,
        'Mult_Factor3': 4.8,
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'SmLength': 100,  # Smoothing depth
        'SmPhase': 15,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

