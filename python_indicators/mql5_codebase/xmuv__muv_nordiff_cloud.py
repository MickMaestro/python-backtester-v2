"""xmuv — converted from MQL5: MQL5 Indicators/MUV_NorDIFF_Cloud/xmuv.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'XMUV'}, 'levels': [], 'description': [], 'name': 'xmuv', 'source': 'MQL5 Indicators/MUV_NorDIFF_Cloud/xmuv.mq5', 'folder': 'MUV_NorDIFF_Cloud', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'method of averaging', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 14, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA)  # method of averaging
XLength = _input('XLength', 14)  # smoothing depth
XPhase = _input('XPhase', 15)  # smoothing parameter
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in points
XMA = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, XMA, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'XMUV(', XLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price_ = 0.0
    xmuv = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        x = 0.0
        h = high[bar]
        l = low[bar]
        o = open[bar]
        c = close[bar]
        if c < o:
            x = (h + l + c + l) / 2
        elif c > o:
            x = (h + l + c + h) / 2
        if c == o:
            x = (h + l + c + c) / 2
        price_ = (x - l + (x - h)) / 2
        if not price_:
            price_ = c
        xmuv = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price_, bar, False)
        XMA[bar] = xmuv + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xmuv(_MQL5Indicator):
    name = 'xmuv'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # method of averaging
        'XLength': 14,  # smoothing depth
        'XPhase': 15,  # smoothing parameter
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in points
    }

