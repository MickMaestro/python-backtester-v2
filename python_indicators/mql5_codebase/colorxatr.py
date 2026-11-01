"""colorxatr — converted from MQL5: MQL5 Indicators/ColorXATR/colorxatr.mq5

Color smoothed ATR
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 55295, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'XATR'}, 'levels': [], 'description': ['Color smoothed ATR'], 'name': 'colorxatr', 'source': 'MQL5 Indicators/ColorXATR/colorxatr.mq5', 'folder': 'ColorXATR', 'inputs': [{'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 12, 'label': 'ATR period', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'smoothing method', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 5, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
ATRPeriod = _input('ATRPeriod', 12)  # ATR period
XMA_Method = _input('XMA_Method', MODE_JJMA)  # smoothing method
XLength = _input('XLength', 5)  # smoothing depth
XPhase = _input('XPhase', 15)  # smoothing parameter,
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Handle = iATR(None, PERIOD_CURRENT, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get the ATR indicator handle')
    min_rates_total = XMA.GetStartBars(XMA_Method, XLength, XPhase) + ATRPeriod + 1
    XMA.XMALengthCheck('XLength', XLength)
    XMA.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    Smooth = XMA.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'XATR(', ATRPeriod, ', ', Smooth, ', ', XLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ATR = Arr(0, 0.0)
    xatr = 0.0
    maxbar = 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = rates_total - ATRPeriod - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(ATR, True)
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        xatr = XMA.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, ATR[bar], bar, True)
        IndBuffer[bar] = NormalizeDouble(_fdiv(xatr, Point()), 0)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if not prev_calculated:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if IndBuffer[bar + 1] < IndBuffer[bar]:
            ColorIndBuffer[bar] = 2.0
        elif IndBuffer[bar + 1] > IndBuffer[bar]:
            ColorIndBuffer[bar] = 1.0
        else:
            ColorIndBuffer[limit] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorxatr(_MQL5Indicator):
    name = 'colorxatr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATRPeriod': 12,  # ATR period
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # smoothing method
        'XLength': 5,  # smoothing depth
        'XPhase': 15,  # smoothing parameter,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

