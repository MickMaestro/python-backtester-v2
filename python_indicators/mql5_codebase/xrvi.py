"""xrvi — converted from MQL5: MQL5 Indicators/XRVI/xrvi.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [14822282]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 4, 2: 0}, 'labels': {1: 'XRVI', 2: 'Signal line'}, 'levels': [], 'description': [], 'name': 'xrvi', 'source': 'MQL5 Indicators/XRVI/xrvi.mq5', 'folder': 'XRVI', 'inputs': [{'mql': 'RviMethod', 'py': 'RviMethod', 'param': 'RviMethod', 'type': 'int', 'default': 5, 'label': 'First smoothing averaging method', 'sinput': False}, {'mql': 'RviPeriod', 'py': 'RviPeriod', 'param': 'RviPeriod', 'type': 'int', 'default': 10, 'label': 'First smoothing depth', 'sinput': False}, {'mql': 'RviPhase', 'py': 'RviPhase', 'param': 'RviPhase', 'type': 'int', 'default': 15, 'label': 'First smoothing parameter', 'sinput': False}, {'mql': 'SignMethod', 'py': 'SignMethod', 'param': 'SignMethod', 'type': 'int', 'default': 5, 'label': 'Second smoothing averaging method', 'sinput': False}, {'mql': 'SignPeriod', 'py': 'SignPeriod', 'param': 'SignPeriod', 'type': 'int', 'default': 5, 'label': 'Second smoothing depth', 'sinput': False}, {'mql': 'SignPhase', 'py': 'SignPhase', 'param': 'SignPhase', 'type': 'int', 'default': 15, 'label': 'Second smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
RviMethod = _input('RviMethod', MODE_JurX)  # First smoothing averaging method
RviPeriod = _input('RviPeriod', 10)  # First smoothing depth
RviPhase = _input('RviPhase', 15)  # First smoothing parameter
SignMethod = _input('SignMethod', MODE_JurX)  # Second smoothing averaging method
SignPeriod = _input('SignPeriod', 5)  # Second smoothing depth
SignPhase = _input('SignPhase', 15)  # Second smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
XRVI = Arr(0, 0.0)
SIGN = Arr(0, 0.0)
StartBars = 0
StartBars1 = 0
StartBars2 = 0

def OnInit():
    global StartBars, StartBars1, StartBars2
    StartBars1 = XMA1.GetStartBars(RviMethod, RviPeriod, RviPhase)
    StartBars2 = XMA2.GetStartBars(SignMethod, SignPeriod, SignPhase)
    StartBars = StartBars1 + StartBars2
    XMA1.XMALengthCheck('RviPeriod', RviPeriod)
    XMA2.XMALengthCheck('SignPeriod', SignPeriod)
    XMA1.XMAPhaseCheck('RviPhase', RviPhase, RviMethod)
    XMA2.XMAPhaseCheck('SignPhase', SignPhase, SignMethod)
    SetIndexBuffer(0, XRVI, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, SIGN, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(RviMethod)
    Smooth2 = XMA1.GetString_MA_Method(SignMethod)
    StringConcatenate(shortname, 'XRVI(', RviPeriod, ', ', SignPeriod, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    rvi = 0.0
    xrvi = 0.0
    signal = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if (high[bar] - low[bar]) != 0:
            rvi = _fdiv(close[bar] - open[bar], high[bar] - low[bar])
        else:
            rvi = 0.0
        xrvi = XMA1.XMASeries(0, prev_calculated, rates_total, RviMethod, RviPhase, RviPeriod, rvi, bar, False)
        signal = XMA2.XMASeries(StartBars1, prev_calculated, rates_total, SignMethod, SignPhase, SignPeriod, xrvi, bar, False)
        XRVI[bar] = xrvi
        SIGN[bar] = signal
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


class Xrvi(_MQL5Indicator):
    name = 'xrvi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RviMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=5),  # First smoothing averaging method
        'RviPeriod': 10,  # First smoothing depth
        'RviPhase': 15,  # First smoothing parameter
        'SignMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=5),  # Second smoothing averaging method
        'SignPeriod': 5,  # Second smoothing depth
        'SignPhase': 15,  # Second smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

