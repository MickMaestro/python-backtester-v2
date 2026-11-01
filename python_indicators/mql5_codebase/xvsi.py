"""xvsi — converted from MQL5: MQL5 Indicators/XVSI/xvsi.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 4, 2: 0}, 'labels': {1: 'XVSI', 2: 'Signal XVSI'}, 'levels': [], 'description': [], 'name': 'xvsi', 'source': 'MQL5 Indicators/XVSI/xvsi.mq5', 'folder': 'XVSI', 'inputs': [{'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 7, 'label': 'Indicator smoothing method', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 15, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Volume', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
DSmoothMethod = _input('DSmoothMethod', MODE_T3)  # Indicator smoothing method
DPeriod = _input('DPeriod', 15)  # Smoothing period
DPhase = _input('DPhase', 15)  # Smoothing parameter
VolumeType = _input('VolumeType', VOLUME_TICK)  # Volume
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
vsiBuffer = Arr(0, 0.0)
vsiMABuffer = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = XMA.GetStartBars(DSmoothMethod, DPeriod, DPhase) + 1
    XMA.XMALengthCheck('DPeriod', DPeriod)
    XMA.XMAPhaseCheck('DPhase', DPhase, DSmoothMethod)
    SetIndexBuffer(0, vsiBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, vsiMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = ""
    Smooth = XMA.GetString_MA_Method(DSmoothMethod)
    StringConcatenate(shortname, 'XVSI(', _str(DPeriod), ',', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    vol = 0.0
    first = 0
    bar = 0
    timeDiff = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if VolumeType == VOLUME_TICK:
            vol = float(tick_volume[bar])
        else:
            vol = float(volume[bar])
        if bar == (rates_total - 1):
            timeDiff = _int(TimeCurrent() - time[bar])
            if timeDiff > 0:
                vsiBuffer[bar] = _fdiv(vol, timeDiff)
        else:
            vsiBuffer[bar] = _fdiv(vol, time[bar] - time[bar - 1])
        vsiMABuffer[bar] = XMA.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, vsiBuffer[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xvsi(_MQL5Indicator):
    name = 'xvsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Indicator smoothing method
        'DPeriod': 15,  # Smoothing period
        'DPhase': 15,  # Smoothing parameter
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

