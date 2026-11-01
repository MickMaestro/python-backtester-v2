"""Swami aroon — converted from MQL5: MQL5 Indicators/Swami Aroon/Swami aroon.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1}, 'colors': {1: [16777215]}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'Generic Aroon'}, 'levels': [], 'description': [], 'name': 'Swami aroon', 'source': 'MQL5 Indicators/Swami Aroon/Swami aroon.mq5', 'folder': 'Swami Aroon', 'inputs': [{'mql': 'StartFrom', 'py': 'StartFrom', 'param': 'StartFrom', 'type': 'int', 'default': 6, 'label': 'Start Aroon period', 'sinput': False}, {'mql': 'EndWith', 'py': 'EndWith', 'param': 'EndWith', 'type': 'int', 'default': 48, 'label': 'End  Aroon period', 'sinput': False}, {'mql': 'BarsToDraw', 'py': 'BarsToDraw', 'param': 'BarsToDraw', 'type': 'int', 'default': 350, 'label': 'Bars to draw on chart', 'sinput': False}, {'mql': 'BarsWidth', 'py': 'BarsWidth', 'param': 'BarsWidth', 'type': 'int', 'default': 4, 'label': '"Dots" width', 'sinput': False}, {'mql': 'UniqueID', 'py': 'UniqueID', 'param': None, 'type': 'string', 'default': 'SwamiArron1', 'label': 'Unique ID for objects', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StartFrom = _input('StartFrom', 6)  # Start Aroon period
EndWith = _input('EndWith', 48)  # End  Aroon period
BarsToDraw = _input('BarsToDraw', 350)  # Bars to draw on chart
BarsWidth = _input('BarsWidth', 4)  # "Dots" width
UniqueID = _input('UniqueID', 'SwamiArron1')  # Unique ID for objects
aroon = Arr(0, 0.0)
step = 0.0
totalSteps = 0.0
window = 0
_StartFrom = 0
_EndWith = 0

def OnInit():
    global _EndWith, _StartFrom, step, totalSteps
    SetIndexBuffer(0, aroon, INDICATOR_DATA)
    _StartFrom = MathMax(StartFrom, 6)
    _EndWith = MathMin(EndWith, 99)
    totalSteps = _EndWith - _StartFrom + 1.0
    step = _fdiv(100.0, totalSteps - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, UniqueID)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, UniqueID + ':')
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global window
    window = ChartWindowFind(0, UniqueID)
    for i in range(((prev_calculated - 1) if (prev_calculated > 0) else 0), rates_total):
        _high = high[i]
        _highest = _high
        _low = low[i]
        _lowest = _low
        aroon[i] = 0.0
        AroonOs = 0.0
        k = 1
        while k < _EndWith and i >= k:
            if high[i - k] > _high:
                _highest = k
                _high = high[i - k]
            if low[i - k] < _low:
                _lowest = k
                _low = low[i - k]
            if (rates_total - i - 1) < BarsToDraw:
                AroonUp = _fdiv(k - _highest + 1.0, k * 1.0)
                AroonDn = _fdiv(k - _lowest + 1.0, k * 1.0)
                AroonOs = (AroonUp - AroonDn) / 2.0
                plot(_str(k), time, (k - _StartFrom) * step, (k - _StartFrom + 1) * step, i, i, gradientColor(_int((AroonOs * 50.0) + 25.0), 50, clrRed, clrLimeGreen), BarsWidth)
            aroon[i] += AroonOs
            k += 1
        aroon[i] = MathMin(MathMax(_fdiv(100.0 * aroon[i], totalSteps) + 50.0, 0), 100)
    return rates_total

def plot(namex, time, valueA, valueB, shiftA, shiftB, theColor, width=0, style=STYLE_SOLID):
    name = UniqueID + ':' + namex + _str(time[shiftA])
    if ObjectFind(0, name) == -1:
        ObjectCreate(0, name, OBJ_TREND, window, time[shiftA], valueA, time[shiftB], valueB)
        ObjectSetInteger(0, name, OBJPROP_RAY, False)
        ObjectSetInteger(0, name, OBJPROP_BACK, True)
        ObjectSetInteger(0, name, OBJPROP_STYLE, style)
        ObjectSetInteger(0, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(0, name, OBJPROP_COLOR, theColor)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, valueA)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, valueB)

def gradientColor(_step, _totalSteps, from_, to):
    newBlue = getColor(_step, _totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(_step, _totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(_step, _totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed

def getColor(stepNo, _totalSteps, from_, to):
    _step = _fdiv(from_ - to, _totalSteps - 1.0)
    return _uint(from_ - (_step * stepNo))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SwamiAroon(_MQL5Indicator):
    name = 'Swami aroon'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'StartFrom': 6,  # Start Aroon period
        'EndWith': 48,  # End  Aroon period
        'BarsToDraw': 350,  # Bars to draw on chart
        'BarsWidth': 4,  # "Dots" width
    }
    y_range = (0.0, 100.0)

