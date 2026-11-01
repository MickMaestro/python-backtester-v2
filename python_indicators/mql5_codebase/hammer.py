"""Hammer — converted from MQL5: MQL5 Indicators/Hammer Indicator/Hammer.mq5

Copyright: Copyright 2024, vilraxq

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, vilraxq', 'window': 'chart', 'indicator_buffers': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Hammer', 'source': 'MQL5 Indicators/Hammer Indicator/Hammer.mq5', 'folder': 'Hammer Indicator', 'inputs': [{'mql': 'MaxRatioShortWick', 'py': 'MaxRatioShortWick', 'param': 'MaxRatioShortWick', 'type': 'double', 'default': 0.05, 'label': '', 'sinput': False}, {'mql': 'MinRatioLongWick', 'py': 'MinRatioLongWick', 'param': 'MinRatioLongWick', 'type': 'double', 'default': 0.7, 'label': '', 'sinput': False}, {'mql': 'MinCandleSize', 'py': 'MinCandleSize', 'param': 'MinCandleSize', 'type': 'double', 'default': 10.0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
m_objectNames = Arr(0, "")
MaxRatioShortWick = _input('MaxRatioShortWick', 0.05)
MinRatioLongWick = _input('MinRatioLongWick', 0.7)
MinCandleSize = _input('MinCandleSize', 10.0)

def IsGreenCandle(open, close):
    return open < close

def IsRedCandle(open, close):
    return not IsGreenCandle(open, close)

def IsGreenHammer(index, open, close, high, low, maxRatioShortWick, minRatioLongWick, minCandleSize):
    candleSize = high[index] - low[index]
    if candleSize < (minCandleSize * Point()):
        return False
    return (IsGreenCandle(open[index], close[index]) and (high[index] - close[index]) < (candleSize * maxRatioShortWick)) and (open[index] - low[index]) > (candleSize * minRatioLongWick)

def IsRedHammer(index, open, close, high, low, maxRatioShortWick, minRatioLongWick, minCandleSize):
    candleSize = high[index] - low[index]
    if candleSize < (minCandleSize * Point()):
        return False
    return (IsRedCandle(open[index], close[index]) and (high[index] - open[index]) < (candleSize * maxRatioShortWick)) and (close[index] - low[index]) > (candleSize * minRatioLongWick)

def IsGreenInvertedHammer(index, open, close, high, low, maxRatioShortWick, minRatioLongWick, minCandleSize):
    candleSize = high[index] - low[index]
    if candleSize < (minCandleSize * Point()):
        return False
    return (IsGreenCandle(open[index], close[index]) and (close[index] - low[index]) < (candleSize * maxRatioShortWick)) and (high[index] - open[index]) > (candleSize * minRatioLongWick)

def IsRedInvertedHammer(index, open, close, high, low, maxRatioShortWick, minRatioLongWick, minCandleSize):
    candleSize = high[index] - low[index]
    if candleSize < (minCandleSize * Point()):
        return False
    return (IsRedCandle(open[index], close[index]) and (open[index] - low[index]) < (candleSize * maxRatioShortWick)) and (high[index] - close[index]) > (candleSize * minRatioLongWick)

def OnInit():
    ObjectsDeleteAll(0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = (1 if (prev_calculated == 0) else (prev_calculated - 1))
    while i < rates_total:
        if IsGreenHammer(i, open, close, high, low, MaxRatioShortWick, MinRatioLongWick, MinCandleSize):
            CreateObject(time[i], low[i], 233, 1, clrGreen, 'Green Hammer')
        elif IsRedHammer(i, open, close, high, low, MaxRatioShortWick, MinRatioLongWick, MinCandleSize):
            CreateObject(time[i], low[i], 233, 1, clrRed, 'Red Hammer')
        elif IsGreenInvertedHammer(i, open, close, high, low, MaxRatioShortWick, MinRatioLongWick, MinCandleSize):
            CreateObject(time[i], high[i], 234, -1, clrGreen, 'Green Inverted Hammer')
        elif IsRedInvertedHammer(i, open, close, high, low, MaxRatioShortWick, MinRatioLongWick, MinCandleSize):
            CreateObject(time[i], high[i], 234, -1, clrRed, 'Red Inverted Hammer')
        i += 1
    return rates_total

def DeleteObjects():
    for i in range(0, ArraySize(m_objectNames)):
        ObjectDelete(0, m_objectNames[i])
    ArrayResize(m_objectNames, 0)

def OnDeinit(reason):
    DeleteObjects()

def CreateObject(time, price, arrowCode, direction, clr, txt):
    objName = Box('')
    StringConcatenate(objName, 'Signal@', time, 'at', DoubleToString(price, Digits()), '(', arrowCode, ')')
    if ObjectCreate(0, objName.v, OBJ_ARROW, 0, time, price):
        ObjectSetInteger(0, objName.v, OBJPROP_ARROWCODE, arrowCode)
        ObjectSetInteger(0, objName.v, OBJPROP_COLOR, clr)
        if direction > 0:
            ObjectSetInteger(0, objName.v, OBJPROP_ANCHOR, ANCHOR_TOP)
        if direction < 0:
            ObjectSetInteger(0, objName.v, OBJPROP_ANCHOR, ANCHOR_BOTTOM)
    objNameDesc = objName.v + txt
    if ObjectCreate(0, objNameDesc, OBJ_TEXT, 0, time, price):
        ObjectSetString(0, objNameDesc, OBJPROP_TEXT, '  ' + txt)
        ObjectSetInteger(0, objNameDesc, OBJPROP_COLOR, clr)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Hammer(_MQL5Indicator):
    name = 'Hammer'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MaxRatioShortWick': 0.05,
        'MinRatioLongWick': 0.7,
        'MinCandleSize': 10.0,
    }

