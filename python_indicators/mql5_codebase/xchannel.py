"""xchannel — converted from MQL5: MQL5 Indicators/XChannel/xchannel.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [65535]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Up;Down'}, 'levels': [], 'description': [], 'name': 'xchannel', 'source': 'MQL5 Indicators/XChannel/xchannel.mq5', 'folder': 'XChannel', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 20, 'label': 'Depth of averaging', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'Delta', 'py': 'Delta', 'param': 'Delta', 'type': 'int', 'default': 100, 'label': 'Vertical shift of channels in points', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA)  # Smoothing method
XLength = _input('XLength', 20)  # Depth of averaging
XPhase = _input('XPhase', 15)  # Smoothing parameter
Delta = _input('Delta', 100)  # Vertical shift of channels in points
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
dDelta = 0.0
min_rates_total = 0

def OnInit():
    global dDelta, min_rates_total
    min_rates_total = XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    dDelta = Delta * Point()
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'XChannel(', XLength, ', ', Smooth, ', ', Delta, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    upxma = 0.0
    dnxma = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        upxma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, high[bar], bar, False)
        dnxma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, low[bar], bar, False)
        UpIndBuffer[bar] = upxma + dDelta
        DnIndBuffer[bar] = dnxma - dDelta
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


class Xchannel(_MQL5Indicator):
    name = 'xchannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'XLength': 20,  # Depth of averaging
        'XPhase': 15,  # Smoothing parameter
        'Delta': 100,  # Vertical shift of channels in points
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

