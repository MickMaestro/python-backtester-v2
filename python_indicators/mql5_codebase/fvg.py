"""FVG — converted from MQL5: MQL5 Indicators/Fair Value Gap (FVG) Indicator/FVG.mq5

Copyright: Copyright 2024, hieuhoangcntt@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, hieuhoangcntt@gmail.com', 'window': 'chart', 'indicator_buffers': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'FVG', 'source': 'MQL5 Indicators/Fair Value Gap (FVG) Indicator/FVG.mq5', 'folder': 'Fair Value Gap (FVG) Indicator', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
_low = 0.0
_high = 0.0
object_names = Arr(0, "")
pre_time = 0
bull = 5
bear = 5
c_bull = 0
c_bear = 0

def isGreenCandle(open, close):
    return open < close

def isRedCandle(open, close):
    return not isGreenCandle(open, close)

def isBullFVG(index, open, high, low, close):
    if (isGreenCandle(open[index - 1], close[index - 1]) and high[index - 2] < low[index]) and high[index - 2] < _low:
        return True
    return False

def isBearFVG(index, open, high, low, close):
    if (isRedCandle(open[index - 1], close[index - 1]) and low[index - 2] > high[index]) and low[index - 2] > _high:
        return True
    return False

def OnInit():
    return INIT_SUCCEEDED

def create_object(name, clrColor, time1, time2, low, high):
    ArrayResize(object_names, ArraySize(object_names) + 1)
    object_names[ArraySize(object_names) - 1] = name
    ObjectCreate(0, name, OBJ_RECTANGLE, 0, time1, low, time2, high)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clrColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, name, OBJPROP_FILL, True)
    ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _high, _low, c_bear, c_bull, pre_time
    if pre_time == time[rates_total - 1]:
        return rates_total
    pre_time = time[rates_total - 1]
    delete_objects()
    _low = low[rates_total - 1]
    _high = high[rates_total - 1]
    c_bull = 0
    c_bear = 0
    for i in range(rates_total - 2, 2 - 1, -1):
        _low = (_low if (_low < low[i]) else low[i])
        _high = (_high if (_high > high[i]) else high[i])
        if c_bull < bull and isBullFVG(i, open, high, low, close):
            create_object('Buy range ' + _str(high[i - 2]) + ' ↗ ' + _str(low[i]), clrBlue, time[i - 2], time[rates_total - 1], low[i], high[i - 2])
            c_bull += 1
            if c_bull >= bull and c_bear >= bear:
                break
        elif c_bear < bear and isBearFVG(i, open, high, low, close):
            create_object('Sell range ' + _str(low[i - 2]) + ' ↘ ' + _str(high[i]), clrRed, time[i - 2], time[rates_total - 1], high[i], low[i - 2])
            c_bear += 1
            if c_bull >= bull and c_bear >= bear:
                break
    return rates_total

def delete_objects():
    for i in range(0, ArraySize(object_names)):
        ObjectDelete(0, object_names[i])
    ArrayResize(object_names, 0)

def OnDeinit(reason):
    global pre_time
    pre_time = 0
    delete_objects()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FVG(_MQL5Indicator):
    name = 'FVG'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

