"""Engulfing — converted from MQL5: MQL5 Indicators/Engulfing Indicator/Engulfing.mq5

Copyright: Copyright 2024, hieuhoangcntt@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, hieuhoangcntt@gmail.com', 'window': 'chart', 'indicator_buffers': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Engulfing', 'source': 'MQL5 Indicators/Engulfing Indicator/Engulfing.mq5', 'folder': 'Engulfing Indicator', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
object_names = Arr(0, "")

def isGreenCandle(open, close):
    return open < close

def isRedCandle(open, close):
    return not isGreenCandle(open, close)

def isBullishEngulfing(index, open, close):
    if ((isGreenCandle(open[index], close[index]) and isRedCandle(open[index - 1], close[index - 1])) and open[index] <= close[index - 1]) and close[index] > open[index - 1]:
        return True
    return False

def isBearishEngulfing(index, open, close):
    if ((isRedCandle(open[index], close[index]) and isGreenCandle(open[index - 1], close[index - 1])) and open[index] >= close[index - 1]) and close[index] < open[index - 1]:
        return True
    return False

def OnInit():
    ObjectsDeleteAll(0)
    return INIT_SUCCEEDED

def create_object(name, obj_type, time, price):
    ObjectCreate(0, name, obj_type, 0, time, price)
    ArrayResize(object_names, ArraySize(object_names) + 1)
    object_names[ArraySize(object_names) - 1] = name

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = (1 if (prev_calculated == 0) else (prev_calculated - 1))
    while i < rates_total:
        if isBullishEngulfing(i, open, close):
            create_object('Buy at ' + _str(close[i]), OBJ_ARROW_BUY, time[i], low[i])
        elif isBearishEngulfing(i, open, close):
            create_object('Sell at ' + _str(close[i]), OBJ_ARROW_SELL, time[i], high[i])
        i += 1
    return rates_total

def delete_objects():
    for i in range(0, ArraySize(object_names)):
        ObjectDelete(0, object_names[i])
    ArrayResize(object_names, 0)

def OnDeinit(reason):
    delete_objects()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Engulfing(_MQL5Indicator):
    name = 'Engulfing'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

