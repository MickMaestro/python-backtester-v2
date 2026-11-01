"""xpvt — converted from MQL5: MQL5 Indicators/Price and Volume Trend/xpvt.mq5

Price and Volume Trend
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 4}, 'labels': {1: 'PVT', 2: 'Signal PVT'}, 'levels': [], 'description': ['Price and Volume Trend'], 'name': 'xpvt', 'source': 'MQL5 Indicators/Price and Volume Trend/xpvt.mq5', 'folder': 'Price and Volume Trend', 'inputs': [{'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'volume', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'averaging method', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 5, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
VolumeType = _input('VolumeType', VOLUME_TICK)  # volume
XMA_Method = _input('XMA_Method', MODE_EMA)  # averaging method
XLength = _input('XLength', 5)  # smoothing depth
XPhase = _input('XPhase', 15)  # smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE)  # price constant
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PVTBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = XMA.GetStartBars(XMA_Method, XLength, XPhase) + 1
    SetIndexBuffer(0, PVTBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Price and Volume Trend')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    dCurrentPrice = 0.0
    dPreviousPrice = 0.0
    first = 0
    bar = 0
    Vol = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        if VolumeType == VOLUME_TICK:
            PVTBuffer[0] = float(tick_volume[0])
        else:
            PVTBuffer[0] = float(volume[0])
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if VolumeType == VOLUME_TICK:
            Vol = tick_volume[bar]
        else:
            Vol = volume[bar]
        dCurrentPrice = PriceSeries(IPC, bar, open, low, high, close)
        dPreviousPrice = PriceSeries(IPC, bar - 1, open, low, high, close)
        PVTBuffer[bar] = PVTBuffer[bar - 1] + _fdiv(Vol * (dCurrentPrice - dPreviousPrice), dPreviousPrice)
        SignBuffer[bar] = XMA.XMASeries(1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, PVTBuffer[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xpvt(_MQL5Indicator):
    name = 'xpvt'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # volume
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # averaging method
        'XLength': 5,  # smoothing depth
        'XPhase': 15,  # smoothing parameter,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

