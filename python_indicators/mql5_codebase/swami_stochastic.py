"""Swami stochastic — converted from MQL5: MQL5 Indicators/Swami stochastic/Swami stochastic.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1}, 'colors': {1: [16777215]}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'Generic stochastic'}, 'levels': [], 'description': [], 'name': 'Swami stochastic', 'source': 'MQL5 Indicators/Swami stochastic/Swami stochastic.mq5', 'folder': 'Swami stochastic', 'inputs': [{'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'StartFrom', 'py': 'StartFrom', 'param': 'StartFrom', 'type': 'int', 'default': 6, 'label': 'Start stochastic period', 'sinput': False}, {'mql': 'EndWith', 'py': 'EndWith', 'param': 'EndWith', 'type': 'int', 'default': 48, 'label': 'End stochastic period', 'sinput': False}, {'mql': 'BarsToDraw', 'py': 'BarsToDraw', 'param': 'BarsToDraw', 'type': 'int', 'default': 350, 'label': 'Bars to draw on chart', 'sinput': False}, {'mql': 'BarsWidth', 'py': 'BarsWidth', 'param': 'BarsWidth', 'type': 'int', 'default': 4, 'label': '"Dots" width', 'sinput': False}, {'mql': 'UniqueID', 'py': 'UniqueID', 'param': None, 'type': 'string', 'default': 'SwamiStoch1', 'label': 'Unique ID for objects', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Price = _input('Price', PRICE_CLOSE)  # Price
StartFrom = _input('StartFrom', 6)  # Start stochastic period
EndWith = _input('EndWith', 48)  # End stochastic period
BarsToDraw = _input('BarsToDraw', 350)  # Bars to draw on chart
BarsWidth = _input('BarsWidth', 4)  # "Dots" width
UniqueID = _input('UniqueID', 'SwamiStoch1')  # Unique ID for objects
stochastic = Arr(0, 0.0)
prices = Arr(0, 0.0)
step = 0.0
totalSteps = 0.0
window = 0
_StartFrom = 0
_EndWith = 0
avgDen = Arr(0, 0.0, dims=(100,))
avgNum = Arr(0, 0.0, dims=(100,))
avgSto = Arr(0, 0.0, dims=(100,))

def OnInit():
    global _EndWith, _StartFrom, step, totalSteps
    SetIndexBuffer(0, stochastic, INDICATOR_DATA)
    SetIndexBuffer(1, prices, INDICATOR_CALCULATIONS)
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
    global _s_OnCalculate__arrayResizedTo, window
    if _s_OnCalculate__arrayResizedTo < rates_total:
        _res = (rates_total + 500) * 3
        _res -= ArrayResize(avgDen, rates_total + 500)
        _res -= ArrayResize(avgNum, rates_total + 500)
        _res -= ArrayResize(avgSto, rates_total + 500)
        if _res:
            return prev_calculated
        _s_OnCalculate__arrayResizedTo = rates_total + 500
    window = ChartWindowFind(0, UniqueID)
    for i in range(((prev_calculated - 1) if (prev_calculated > 0) else 0), rates_total):
        _sw1 = Price
        if _sw1 == PRICE_CLOSE:
            prices[i] = close[i]
        elif _sw1 == PRICE_OPEN:
            prices[i] = open[i]
        elif _sw1 == PRICE_HIGH:
            prices[i] = high[i]
        elif _sw1 == PRICE_LOW:
            prices[i] = low[i]
        elif _sw1 == PRICE_MEDIAN:
            prices[i] = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            prices[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            prices[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            prices[i] = 0.0
    for i in range(((prev_calculated - 1) if (prev_calculated > 0) else 0), rates_total):
        _high = prices[i]
        _low = prices[i]
        stochastic[i] = 0.0
        k = 1
        while k < _EndWith and i >= k:
            _high = MathMax(_high, prices[i - k])
            _low = MathMin(_low, prices[i - k])
            if k >= _StartFrom:
                avgNum[i][k] = (0.5 * avgNum[i - 1][k]) + (0.5 * (prices[i] - _low))
                avgDen[i][k] = (0.5 * avgDen[i - 1][k]) + (0.5 * (_high - _low))
                avgSto[i][k] = 0.0
                if avgDen[i][k] != 0:
                    avgSto[i][k] = (0.2 * _fdiv(avgNum[i][k], avgDen[i][k])) + (0.8 * avgSto[i - 1][k])
                if (rates_total - i - 1) < BarsToDraw:
                    colorR = 255.0
                    colorG = 255.0
                    colorB = 0.0
                    if avgSto[i][k] >= 0.5:
                        colorR = 255.0 * (2.0 - (2.0 * avgSto[i][k]))
                    else:
                        colorG = 255.0 * 2.0 * avgSto[i][k]
                    plot(_str(k), time, (k - StartFrom) * step, (k - StartFrom + 1) * step, i, i, rgb(_int(colorR), _int(colorG), _int(colorB)), BarsWidth)
            stochastic[i] += avgSto[i][k]
            k += 1
        stochastic[i] = _fdiv(stochastic[i], totalSteps / 100.0)
    return rates_total

def plot(namex, time, valueA, valueB, shiftA, shiftB, theColor, width=0, style=STYLE_SOLID):
    name = UniqueID + ':' + namex + _str(time[shiftA])
    if ObjectFind(0, name) == -1:
        ObjectCreate(0, name, OBJ_TREND, window, time[shiftA], valueA, time[shiftB], valueB)
        ObjectSetInteger(0, name, OBJPROP_RAY, False)
        ObjectSetInteger(0, name, OBJPROP_BACK, True)
        ObjectSetInteger(0, name, OBJPROP_FILL, True)
        ObjectSetInteger(0, name, OBJPROP_STYLE, style)
        ObjectSetInteger(0, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(0, name, OBJPROP_COLOR, theColor)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, valueA)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, valueB)

def rgb(red, green, blue):
    red = MathMax(MathMin(red, 255), 0)
    green = MathMax(MathMin(green, 255), 0)
    blue = MathMax(MathMin(blue, 255), 0)
    return _uint(red + _int(green << 8) + _int(blue << 16))

# ---- static local variables
_s_OnCalculate__arrayResizedTo = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SwamiStochastic(_MQL5Indicator):
    name = 'Swami stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'StartFrom': 6,  # Start stochastic period
        'EndWith': 48,  # End stochastic period
        'BarsToDraw': 350,  # Bars to draw on chart
        'BarsWidth': 4,  # "Dots" width
    }
    y_range = (0.0, 100.0)

