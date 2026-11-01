"""zpf — converted from MQL5: MQL5 Indicators/Zero Point Force/zpf.mq5

ZPF
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [255, 8421376]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ZPF'}, 'levels': [0.0], 'description': ['ZPF'], 'name': 'zpf', 'source': 'MQL5 Indicators/Zero Point Force/zpf.mq5', 'folder': 'Zero Point Force', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'method of averaging of the first smoothing', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 12, 'label': 'first smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'first smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'volume', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_SMA)  # method of averaging of the first smoothing
XLength = _input('XLength', 12)  # first smoothing depth
XPhase = _input('XPhase', 15)  # first smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE)  # price constant
VolumeType = _input('VolumeType', VOLUME_TICK)  # volume
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
Line1Buffer = Arr(0, 0.0)
Line2Buffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
X2Length = 0

def OnInit():
    global X2Length, min_rates_total
    X2Length = 2 * XLength
    min_rates_total = XMA2.GetStartBars(XMA_Method, X2Length, XPhase)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    SetIndexBuffer(0, Line1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Line2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'ZPF(', XLength, ', ', EnumToString(VolumeType, 'ENUM_APPLIED_VOLUME'), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price_ = 0.0
    x1ma = 0.0
    x2ma = 0.0
    xvol = 0.0
    zpf = 0.0
    first = 0
    bar = 0
    vol = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if VolumeType == VOLUME_TICK:
            vol = tick_volume[bar]
        else:
            vol = volume[bar]
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        x1ma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price_, bar, False)
        x2ma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, X2Length, price_, bar, False)
        xvol = XMA3.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, float(vol), bar, False)
        zpf = (xvol * (x1ma - x2ma)) / 2
        Line1Buffer[bar] = -zpf
        Line2Buffer[bar] = zpf
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


class Zpf(_MQL5Indicator):
    name = 'zpf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # method of averaging of the first smoothing
        'XLength': 12,  # first smoothing depth
        'XPhase': 15,  # first smoothing parameter,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # volume
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

