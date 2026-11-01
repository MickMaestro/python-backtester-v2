"""superzigzag — converted from MQL5: MQL5 Indicators/SuperZigZag/superzigzag.mq5

Copyright: Copyright 2012, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [16711680, 255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'superzigzag', 'source': 'MQL5 Indicators/SuperZigZag/superzigzag.mq5', 'folder': 'SuperZigZag', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ImportantPoint', 'py': 'ImportantPoint', 'param': 'ImportantPoint', 'type': 'int', 'default': 600, 'label': '"significative movement" in points', 'sinput': False}, {'mql': 'RangeBars', 'py': 'RangeBars', 'param': 'RangeBars', 'type': 'int', 'default': 35, 'label': '"significative movement" period in bars', 'sinput': False}, {'mql': 'RangeKoeff', 'py': 'RangeKoeff', 'param': 'RangeKoeff', 'type': 'double', 'default': 0.45, 'label': '"significative movement" coefficient', 'sinput': False}, {'mql': 'width', 'py': 'width', 'param': 'width', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Mode = _input('Mode', 0)
ImportantPoint = _input('ImportantPoint', 600)  # "significative movement" in points
RangeBars = _input('RangeBars', 35)  # "significative movement" period in bars
RangeKoeff = _input('RangeKoeff', 0.45)  # "significative movement" coefficient
width = _input('width', 2)
szz_up = Arr(0, 0.0)
szz_dn = Arr(0, 0.0)
color_buffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, szz_up, INDICATOR_DATA)
    SetIndexBuffer(1, szz_dn, INDICATOR_DATA)
    SetIndexBuffer(2, color_buffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'SZZ ' + Name())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, width)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    j = 0
    prev = 0
    extr = 0
    if prev_calculated == 0:
        ArrayInitialize(szz_up, 0.0)
        ArrayInitialize(szz_dn, 0.0)
        ArrayInitialize(color_buffer, 0.0)
        prev = 0
        if Mode == 0:
            i = 0
        if Mode == 1:
            i = RangeBars
    if prev_calculated > 0:
        j = rates_total - 1
        for j in range(j, 0 - 1, -1):
            if szz_up[j] == high[j]:
                i = j
                prev = 1
                break
            if szz_dn[j] == low[j]:
                i = j
                prev = 2
                break
        else:
            j = _range_end(j, 0 - 1, -1)
    j = i + 1
    while (j <= (rates_total - 1) and i <= (rates_total - 1)) and extr <= (rates_total - 1):
        while ((prev == 0 and j <= (rates_total - 1)) and i <= (rates_total - 1)) and extr <= (rates_total - 1):
            if NormalizeDouble(_fdiv(high[Highest(high, i + 1, j)] - low[i], Point()), 0) >= GetImpPoint(i, high, low):
                szz_up[j] = high[Highest(high, i + 1, j)]
                color_buffer[j] = 0.0
                szz_dn[Lowest(low, i, j)] = low[Lowest(low, i, j)]
                color_buffer[Lowest(low, i, j)] = 1.0
                prev = 1
                i = j
                extr = j
                j += 1
                break
            if NormalizeDouble(_fdiv(high[i] - low[Lowest(low, i + 1, j)], Point()), 0) >= GetImpPoint(i, high, low):
                szz_dn[j] = low[Lowest(low, i + 1, j)]
                color_buffer[j] = 1.0
                szz_up[Highest(high, i, j)] = high[Highest(high, i, j)]
                color_buffer[Highest(high, i, j)] = 0.0
                prev = 2
                i = j
                extr = j
                j += 1
                break
            j += 1
        while ((prev == 1 and j <= (rates_total - 1)) and i <= (rates_total - 1)) and extr <= (rates_total - 1):
            if NormalizeDouble(_fdiv(high[extr] - low[Lowest(low, i + 1, j)], Point()), 0) >= GetImpPoint(i, high, low):
                szz_dn[j] = low[Lowest(low, i + 1, j)]
                color_buffer[j] = 1.0
                prev = 2
                i = j
                extr = j
                j += 1
                break
            if high[Highest(high, i, j)] > high[extr]:
                szz_up[j] = high[Highest(high, i, j)]
                color_buffer[j] = 0.0
                szz_up[extr] = 0.0
                extr = j
                i = j
                j += 1
                continue
            j += 1
        while ((prev == 2 and j <= (rates_total - 1)) and i <= (rates_total - 1)) and extr <= (rates_total - 1):
            if NormalizeDouble(_fdiv(high[Highest(high, i + 1, j)] - low[extr], Point()), 0) >= GetImpPoint(i, high, low):
                szz_up[j] = high[Highest(high, i + 1, j)]
                color_buffer[j] = 0.0
                prev = 1
                i = j
                extr = j
                j += 1
                break
            if low[Lowest(low, i, j)] < low[extr]:
                szz_dn[j] = low[Lowest(low, i, j)]
                color_buffer[j] = 1.0
                szz_dn[extr] = 0.0
                extr = j
                i = j
                j += 1
                continue
            j += 1
    return rates_total

def GetImpPoint(i, arrhigh, arrlow):
    if Mode == 0:
        return ImportantPoint
    if Mode == 1:
        return _fdiv(arrhigh[Highest(arrhigh, i - RangeBars + 1, i)] - arrlow[Lowest(arrlow, i - RangeBars + 1, i)], Point()) * RangeKoeff
    return 0.0

def Highest(array, start, finish):
    res = start
    for i in range(start, finish + 1):
        if array[i] > array[res]:
            res = i
    return res

def Lowest(array, start, finish):
    res = start
    for i in range(start, finish + 1):
        if array[i] < array[res]:
            res = i
    return res

def Name():
    text = ""
    if Mode == 0:
        text = '(' + IntegerToString(ImportantPoint) + ')'
    if Mode == 1:
        text = '( ' + IntegerToString(RangeBars) + ',' + DoubleToString(RangeKoeff, 2) + ')'
    return text


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Superzigzag(_MQL5Indicator):
    name = 'superzigzag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Mode': 0,
        'ImportantPoint': 600,  # "significative movement" in points
        'RangeBars': 35,  # "significative movement" period in bars
        'RangeKoeff': 0.45,  # "significative movement" coefficient
        'width': 2,
    }

