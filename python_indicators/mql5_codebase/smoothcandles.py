"""smoothcandles — converted from MQL5: MQL5 Indicators/Smooth Candle S/smoothcandles.mq5

Averaging price timeseries using four MAs
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711935], 2: [16748574], 3: [65280], 4: [14822282]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Open', 2: 'Low', 3: 'High', 4: 'Close'}, 'levels': [], 'description': ['Averaging price timeseries using four MAs'], 'name': 'smoothcandles', 'source': 'MQL5 Indicators/Smooth Candle S/smoothcandles.mq5', 'folder': 'Smooth Candle S', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 5, 'label': 'Averaging depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'Averaging parameter', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA)  # Method of averaging
XLength = _input('XLength', 5)  # Averaging depth
XPhase = _input('XPhase', 100)  # Averaging parameter
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
HBuffer = Arr(0, 0.0)
LBuffer = Arr(0, 0.0)
OBuffer = Arr(0, 0.0)
CBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase) + 1
    IndInit(0, OBuffer, 0.0, min_rates_total, Shift)
    IndInit(1, LBuffer, 0.0, min_rates_total, Shift)
    IndInit(2, HBuffer, 0.0, min_rates_total, Shift)
    IndInit(3, CBuffer, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'SmoothCandleS', '(', XLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        OBuffer[bar] = XMAO.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, open[bar], bar, False)
        CBuffer[bar] = XMAC.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, close[bar], bar, False)
        HBuffer[bar] = XMAH.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, high[bar], bar, False)
        LBuffer[bar] = XMAL.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, low[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

# ---- global variables initialised from expressions
XMAO = _alloc(CXMA)
XMAO.__init__()
XMAL = _alloc(CXMA)
XMAL.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAC = _alloc(CXMA)
XMAC.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Smoothcandles(_MQL5Indicator):
    name = 'smoothcandles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Method of averaging
        'XLength': 5,  # Averaging depth
        'XPhase': 100,  # Averaging parameter
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

