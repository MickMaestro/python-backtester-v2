"""SwingHighLow_and_Fibonacci — converted from MQL5: MQL5 Indicators/Swing High Low and Fibonacci Retracement Indicator/SwingHighLow_and_Fibonacci.mq5

Copyright: Copyright 2024, hieuhoangcntt@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, hieuhoangcntt@gmail.com', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'SwingHighLow_and_Fibonacci', 'source': 'MQL5 Indicators/Swing High Low and Fibonacci Retracement Indicator/SwingHighLow_and_Fibonacci.mq5', 'folder': 'Swing High Low and Fibonacci Retracement Indicator', 'inputs': [{'mql': 'InpFiboLevelColor', 'py': 'InpFiboLevelColor', 'param': None, 'type': 'color', 'default': 3145645, 'label': 'Fibo level color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFiboLevelColor = _input('InpFiboLevelColor', clrGreenYellow)  # Fibo level color
clr = clrWhite
style = STYLE_SOLID
width = 2
swing_length = 5
c_low = DBL_MAX
c_high = DBL_MIN
tmp_high = 0.0
tmp_low = 0.0
tmp_time = 0
current_trend = -1
preObjName = ''
preObjName2 = ''
lastIndex = swing_length
objects_name = Arr(0, "")

def isLow(in_, low):
    for i in range(in_ - swing_length, in_ + swing_length + 1):
        if low[in_] > low[i]:
            return False
    return True

def isHigh(in_, high):
    for i in range(in_ - swing_length, in_ + swing_length + 1):
        if high[in_] < high[i]:
            return False
    return True

def addObject(name):
    ArrayResize(objects_name, ArraySize(objects_name) + 1)
    objects_name[ArraySize(objects_name) - 1] = name

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    for i in range(ArraySize(objects_name) - 1, 0 - 1, -1):
        ObjectDelete(0, objects_name[i])
    ArrayResize(objects_name, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global c_high, c_low, current_trend, lastIndex, preObjName, preObjName2, tmp_high, tmp_low, tmp_time
    i = lastIndex
    while i < (rates_total - swing_length - 2):
        if isHigh(i, high):
            if current_trend != 0 or high[i] > c_high:
                if current_trend == 0:
                    ObjectDelete(0, preObjName)
                preObjName = 'High ' + _str(i)
                ObjectCreate(0, preObjName, OBJ_ARROW_SELL, 0, time[i], high[i])
                addObject(preObjName)
                current_trend = 0
                c_high = high[i]
                c_low = DBL_MAX
                tmp_high = high[i]
                lastIndex = i + 1
        elif isLow(i, low):
            if current_trend != 1 or low[i] < c_low:
                if current_trend == 1:
                    ObjectDelete(0, preObjName)
                    ObjectSetInteger(0, preObjName2, OBJPROP_TIME, time[i])
                if 0 != tmp_high and current_trend != 1:
                    preObjName2 = 'Fibonacci Retracement ' + _str(i)
                    addObject(preObjName2)
                    ObjectCreate(0, preObjName2, OBJ_FIBO, 0, time[i], tmp_high, tmp_time, tmp_low)
                    ObjectSetInteger(0, preObjName2, OBJPROP_COLOR, clr)
                    ObjectSetInteger(0, preObjName2, OBJPROP_STYLE, style)
                    ObjectSetInteger(0, preObjName2, OBJPROP_WIDTH, width)
                    for i_2 in range(0, 9):
                        ObjectSetInteger(0, preObjName2, OBJPROP_LEVELCOLOR, i_2, InpFiboLevelColor)
                ObjectSetInteger(0, preObjName2, OBJPROP_RAY_RIGHT, False)
                preObjName = 'Low ' + _str(i)
                addObject(preObjName)
                ObjectCreate(0, preObjName, OBJ_ARROW_BUY, 0, time[i], low[i])
                current_trend = 1
                c_high = DBL_MIN
                c_low = low[i]
                tmp_low = low[i]
                tmp_time = time[i]
                lastIndex = i + 1
        i += 1
    ObjectSetInteger(0, preObjName2, OBJPROP_RAY_RIGHT, True)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SwingHighLowAndFibonacci(_MQL5Indicator):
    name = 'SwingHighLow_and_Fibonacci'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

