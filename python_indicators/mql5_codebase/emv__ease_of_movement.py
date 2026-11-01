"""emv — converted from MQL5: MQL5 Indicators/Ease of Movement/emv.mq5

Ease of Movement Value
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [15624315]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Ease of Movement Value'}, 'levels': [], 'description': ['Ease of Movement Value'], 'name': 'emv', 'source': 'MQL5 Indicators/Ease of Movement/emv.mq5', 'folder': 'Ease of Movement', 'inputs': [{'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'SmLength', 'py': 'SmLength', 'param': 'SmLength', 'type': 'int', 'default': 14, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'SmPhase', 'py': 'SmPhase', 'param': 'SmPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 9, 'label': 'Price constant', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Volume', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MA_SMethod = _input('MA_SMethod', MODE_SMA)  # Smoothing method
SmLength = _input('SmLength', 14)  # Smoothing depth
SmPhase = _input('SmPhase', 15)  # Smoothing parameter
IPC = _input('IPC', PRICE_QUARTER_)  # Price constant
VolumeType = _input('VolumeType', VOLUME_TICK)  # Volume
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
EMVBuffer = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = XMA1.GetStartBars(MA_SMethod, SmLength, SmPhase) + 1
    XMA1.XMALengthCheck('Length', SmLength)
    XMA1.XMAPhaseCheck('Phase', SmPhase, MA_SMethod)
    SetIndexBuffer(0, EMVBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ease of Movement Value')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    first = 0
    bar = 0
    price0 = 0.0
    price1 = 0.0
    EMV = 0.0
    Volume = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price0 = PriceSeries(PRICE_MEDIAN, bar, open, low, high, close)
        price1 = PriceSeries(PRICE_MEDIAN, bar - 1, open, low, high, close)
        if VolumeType == VOLUME_TICK:
            Volume = tick_volume[bar]
        else:
            Volume = volume[bar]
        if Volume != 0:
            EMV = _fdiv((price0 - price1) * price0, 2 * Volume)
        else:
            EMV = 0.0
        EMVBuffer[bar] = XMA1.XMASeries(1, prev_calculated, rates_total, MA_SMethod, SmPhase, SmLength, EMV, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Emv(_MQL5Indicator):
    name = 'emv'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'SmLength': 14,  # Smoothing depth
        'SmPhase': 15,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=9),  # Price constant
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

