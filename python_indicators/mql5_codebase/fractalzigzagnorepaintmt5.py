"""FractalZigZagNoRepaintMt5 — converted from MQL5: MQL5 Indicators/Fractal ZigZag/FractalZigZagNoRepaintMt5.mq5

Copyright: pointzero-trading.com; Link: http://www.mql5.com; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'pointzero-trading.com', 'link': 'http://www.mql5.com', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper', 2: 'Lower'}, 'levels': [], 'description': [], 'name': 'FractalZigZagNoRepaintMt5', 'source': 'MQL5 Indicators/Fractal ZigZag/FractalZigZagNoRepaintMt5.mq5', 'folder': 'Fractal ZigZag', 'inputs': [{'mql': 'CalculateOnBarClose', 'py': 'CalculateOnBarClose', 'param': 'CalculateOnBarClose', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'ZZDepth', 'py': 'ZZDepth', 'param': 'ZZDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ZZDev', 'py': 'ZZDev', 'param': 'ZZDev', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'nShift', 'py': 'nShift', 'param': 'nShift', 'type': 'int', 'default': 5, 'label': 'ArrowShift_points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CalculateOnBarClose = _input('CalculateOnBarClose', True)
ZZDepth = _input('ZZDepth', 12)
ZZDev = _input('ZZDev', 5)
nShift = _input('nShift', 5)  # ArrowShift_points
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
zzup = Arr(0, 0.0)
zzdwn = Arr(0, 0.0)
zzhigh = 0.0
zzlow = 0.0
zzhandle = 0
fr_resistance = 0.0
fr_support = 0.0
fr_resistance_change = (EMPTY_VALUE != 0)
fr_support_change = (EMPTY_VALUE != 0)

def OnInit():
    global zzhandle
    zzhandle = iCustom(Symbol(), Period(), '::Indicators\\Examples\\ZigzagColor.ex5', ZZDepth, ZZDev, 1)
    if zzhandle == INVALID_HANDLE:
        Print('Error, invalid handle for indicator values')
        return INIT_FAILED
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, zzup, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, zzdwn, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 2)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 2)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(UpperBuffer, True)
    ArraySetAsSeries(LowerBuffer, True)
    ArraySetAsSeries(zzup, True)
    ArraySetAsSeries(zzdwn, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global zzhigh, zzlow
    limit = 0
    i = 0
    first = 0
    if prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = 1
    if CopyBuffer(zzhandle, 3, 0, limit, zzup) <= 0:
        return 0
    if CopyBuffer(zzhandle, 4, 0, limit, zzdwn) <= 0:
        return 0
    if CalculateOnBarClose:
        first = 1
    i = limit
    for i in range(i, first - 1, -1):
        UpperBuffer[i] = 0.0
        LowerBuffer[i] = 0.0
        if zzup[i] != 0:
            zzhigh = zzup[i]
        if zzdwn[i] != 0:
            zzlow = zzdwn[i]
        resistance = upper_fractal(i)
        support = lower_fractal(i)
        if fr_support_change == True and fr_support == zzlow:
            LowerBuffer[i + 2] = fr_support - (2 * nShift * Point())
            UpperBuffer[i + 2] = 0.0
        elif fr_resistance_change == True and fr_resistance == zzhigh:
            UpperBuffer[i + 2] = fr_resistance + (2 * nShift * Point())
            LowerBuffer[i + 2] = 0.0
    else:
        i = _range_end(i, first - 1, -1)
    return rates_total

def upper_fractal(shift=1):
    global fr_resistance, fr_resistance_change
    middle = iHigh(Symbol(), 0, shift + 2)
    v1 = iHigh(Symbol(), 0, shift)
    v2 = iHigh(Symbol(), 0, shift + 1)
    v3 = iHigh(Symbol(), 0, shift + 3)
    v4 = iHigh(Symbol(), 0, shift + 4)
    if ((middle > v1 and middle > v2) and middle > v3) and middle > v4:
        fr_resistance = middle
        fr_resistance_change = True
    else:
        fr_resistance_change = False
    return fr_resistance

def lower_fractal(shift=1):
    global fr_support, fr_support_change
    middle = iLow(Symbol(), 0, shift + 2)
    v1 = iLow(Symbol(), 0, shift)
    v2 = iLow(Symbol(), 0, shift + 1)
    v3 = iLow(Symbol(), 0, shift + 3)
    v4 = iLow(Symbol(), 0, shift + 4)
    if ((middle < v1 and middle < v2) and middle < v3) and middle < v4:
        fr_support = middle
        fr_support_change = True
    else:
        fr_support_change = False
    return fr_support


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalZigZagNoRepaintMt5(_MQL5Indicator):
    name = 'FractalZigZagNoRepaintMt5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CalculateOnBarClose': True,
        'ZZDepth': 12,
        'ZZDev': 5,
        'nShift': 5,  # ArrowShift_points
    }

