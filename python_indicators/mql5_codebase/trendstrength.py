"""trendstrength — converted from MQL5: MQL5 Indicators/TrendStrength/trendstrength.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TrendStrength'}, 'levels': [], 'description': [], 'name': 'trendstrength', 'source': 'MQL5 Indicators/TrendStrength/trendstrength.mq5', 'folder': 'TrendStrength', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'smoothing method', 'sinput': False}, {'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'uint', 'default': 10, 'label': 'first smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 10, 'label': 'smoothing step', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in pointsх', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_SMA)  # smoothing method
StartLength = _input('StartLength', 10)  # first smoothing depth
XPhase = _input('XPhase', 15)  # smoothing parameter,
Step = _input('Step', 10)  # smoothing step
IPC = _input('IPC', PRICE_CLOSE)  # price constant
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in pointsх
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
period = Arr(11, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = XMA[1].GetStartBars(XMA_Method, StartLength + (Step * 10), XPhase)
    XMA[1].XMALengthCheck('StartLength', StartLength)
    XMA[1].XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    for number in range(0, 11):
        period[number] = _int(StartLength + (Step * number))
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    Smooth1 = XMA[1].GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'TrendStrength(', Smooth1, ', ', StartLength, ', ', Step, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    x1xma = Arr(11, 0.0, dyn=False)
    res = 0.0
    ArrayInitialize(x1xma, 0.0)
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        for number in range(0, 11):
            x1xma[number] = XMA[number].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, period[number], price, bar, False)
        res = 10 * x1xma[0]
        for number in range(1, 11):
            res -= x1xma[number]
        IndBuffer[bar] = _fdiv(res, Point() * 10)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = Arr(11, 0, dyn=False, factory=CXMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendstrength(_MQL5Indicator):
    name = 'trendstrength'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # smoothing method
        'StartLength': 10,  # first smoothing depth
        'XPhase': 15,  # smoothing parameter,
        'Step': 10,  # smoothing step
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # price constant
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in pointsх
    }

