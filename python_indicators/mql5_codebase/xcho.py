"""xcho — converted from MQL5: MQL5 Indicators/Chaikin Oscillator/xcho.mq5

Chaikin Oscillator
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [42495]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'XCHO'}, 'levels': [], 'description': ['Chaikin Oscillator'], 'name': 'xcho', 'source': 'MQL5 Indicators/Chaikin Oscillator/xcho.mq5', 'folder': 'Chaikin Oscillator', 'inputs': [{'mql': 'FastMA', 'py': 'FastMA', 'param': 'FastMA', 'type': 'int', 'default': 3, 'label': 'Fast average period', 'sinput': False}, {'mql': 'SlowMA', 'py': 'SlowMA', 'param': 'SlowMA', 'type': 'int', 'default': 10, 'label': 'Slow average period', 'sinput': False}, {'mql': 'Phase_', 'py': 'Phase_', 'param': 'Phase_', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter,', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 7, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Volume', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
FastMA = _input('FastMA', 3)  # Fast average period
SlowMA = _input('SlowMA', 10)  # Slow average period
Phase_ = _input('Phase_', 15)  # Smoothing parameter,
SmoothMethod = _input('SmoothMethod', MODE_T3)  # Smoothing method
VolumeType = _input('VolumeType', VOLUME_TICK)  # Volume
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
XCHO = Arr(0, 0.0)
StartBars = 0

def GetAD(high, low, close, tick_volume, volume, bar):
    vol = 0
    res = 0.0
    if VolumeType == VOLUME_TICK:
        vol = tick_volume[bar]
    else:
        vol = volume[bar]
    if high[bar] != low[bar]:
        res = _fdiv((2 * close[bar]) - high[bar] - low[bar], high[bar] - low[bar]) * vol
    return res

def OnInit():
    global StartBars
    StartBars = MathMax(XMA1.GetStartBars(SmoothMethod, FastMA, Phase_), XMA2.GetStartBars(SmoothMethod, SlowMA, Phase_))
    XMA1.XMALengthCheck('FastMA', FastMA)
    XMA2.XMALengthCheck('SlowMA', SlowMA)
    XMA1.XMAPhaseCheck('Phase_', Phase_, SmoothMethod)
    SetIndexBuffer(0, XCHO, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'XCHO')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(SmoothMethod)
    StringConcatenate(shortname, 'Chaikin Oscillator(', _str(SlowMA), ',', _str(FastMA), ',', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ad_
    if rates_total < StartBars:
        return 0
    ad = 0.0
    slowma = 0.0
    fastma = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_ad_ = GetAD(high, low, close, tick_volume, volume, 0)
    else:
        first = prev_calculated - 1
    ad = _s_OnCalculate_ad_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate_ad_ = ad
        ad += GetAD(high, low, close, tick_volume, volume, bar)
        fastma = XMA1.XMASeries(0, prev_calculated, rates_total, SmoothMethod, Phase_, FastMA, ad, bar, False)
        slowma = XMA2.XMASeries(0, prev_calculated, rates_total, SmoothMethod, Phase_, SlowMA, ad, bar, False)
        if bar < StartBars:
            XCHO[bar] = EMPTY_VALUE
            continue
        XCHO[bar] = fastma - slowma
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_OnCalculate_ad_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xcho(_MQL5Indicator):
    name = 'xcho'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastMA': 3,  # Fast average period
        'SlowMA': 10,  # Slow average period
        'Phase_': 15,  # Smoothing parameter,
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Smoothing method
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

