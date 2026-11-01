"""tmfi — converted from MQL5: MQL5 Indicators/True MFI (Alternative to the standard MFI)/tmfi.mq5

True MFI. Based on code RSI.mq4
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2, 'version': '3.24'}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711935], 2: [13828244]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TMFI', 2: 'Signal'}, 'levels': [68.16901138162093, 50.0, 31.830988618379067], 'description': ['True MFI. Based on code RSI.mq4'], 'name': 'tmfi', 'source': 'MQL5 Indicators/True MFI (Alternative to the standard MFI)/tmfi.mq5', 'folder': 'True MFI (Alternative to the standard MFI)', 'inputs': [{'mql': 'TMFIPeriod', 'py': 'TMFIPeriod', 'param': 'TMFIPeriod', 'type': 'uint', 'default': 10, 'label': 'TMFI period', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'smoothing method', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 5, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'volume', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
TMFIPeriod = _input('TMFIPeriod', 10)  # TMFI period
XMA_Method = _input('XMA_Method', MODE_JJMA)  # smoothing method
XLength = _input('XLength', 5)  # smoothing depth
XPhase = _input('XPhase', 15)  # smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE)  # price constant
VolumeType = _input('VolumeType', VOLUME_TICK)  # volume
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
TMFIBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(TMFIPeriod + XMA.GetStartBars(XMA_Method, XLength, XPhase) + 1)
    XMA.XMALengthCheck('XLength', XLength)
    XMA.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    SetIndexBuffer(0, TMFIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = XMA.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'TMFI(', TMFIPeriod, ', ', Smooth, ', ', XLength, ', ', XPhase, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_negative_, _s_OnCalculate_positive_
    if rates_total < min_rates_total:
        return 0
    Volume = 0
    first = 0
    bar = 0
    bar1 = 0
    rel = 0.0
    negative = 0.0
    positive = 0.0
    sumn = 0.0
    sump = 0.0
    tmfi = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_negative_ = 50.0
        _s_OnCalculate_positive_ = 50.0
    else:
        first = prev_calculated - 1
    negative = _s_OnCalculate_negative_
    positive = _s_OnCalculate_positive_
    bar1 = rates_total - 2
    bar = first
    for bar in range(bar, rates_total):
        sumn = 0.0
        sump = 0.0
        rel = PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar - 1, open, low, high, close)
        if VolumeType == VOLUME_TICK:
            Volume = tick_volume[bar]
        else:
            Volume = volume[bar]
        if rel > 0:
            sump += float(Volume)
        else:
            sumn += float(Volume)
        positive = ((positive * (TMFIPeriod - 1)) + sump) / TMFIPeriod
        negative = ((negative * (TMFIPeriod - 1)) + sumn) / TMFIPeriod
        if negative:
            tmfi = 100.0 * (1.0 - _fdiv(1.0, 1.0 + _fdiv(positive, negative)))
        else:
            tmfi = 50.0
        TMFIBuffer[bar] = tmfi
        SignalBuffer[bar] = XMA.XMASeries(TMFIPeriod, prev_calculated, rates_total, XMA_Method, XPhase, XLength, tmfi, bar, False)
        if bar == bar1:
            _s_OnCalculate_negative_ = negative
            _s_OnCalculate_positive_ = positive
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()

# ---- static local variables
_s_OnCalculate_negative_ = 0.0
_s_OnCalculate_positive_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tmfi(_MQL5Indicator):
    name = 'tmfi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TMFIPeriod': 10,  # TMFI period
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # smoothing method
        'XLength': 5,  # smoothing depth
        'XPhase': 15,  # smoothing parameter,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # volume
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

