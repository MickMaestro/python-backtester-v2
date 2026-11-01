"""ColorDay — converted from MQL5: MQL5 Indicators/Color Day/ColorDay.mq5

Copyright: Copyright 2016, AM2; Link: http://www.forexsystems.biz; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, AM2', 'link': 'http://www.forexsystems.biz', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ColorDay', 'source': 'MQL5 Indicators/Color Day/ColorDay.mq5', 'folder': 'Color Day', 'inputs': [{'mql': 'Days', 'py': 'Days', 'param': 'Days', 'type': 'int', 'default': 11, 'label': 'дней для расчета', 'sinput': False}, {'mql': 'UP', 'py': 'UP', 'param': None, 'type': 'color', 'default': 0, 'label': 'цвет бычьего дня', 'sinput': False}, {'mql': 'DN', 'py': 'DN', 'param': None, 'type': 'color', 'default': 0, 'label': 'цвет медвежьего дня', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
Days = _input('Days', 11)  # дней для расчета
tm = Arr(0, 0)
op = Arr(0, 0.0)
cl = Arr(0, 0.0)

def OnInit():
    Comment('')
    ArrayResize(tm, Days)
    ArrayResize(op, Days)
    ArrayResize(cl, Days)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    DeleteObjects()

def DeleteObjects():
    for i in range(ObjectsTotal(0, 0, OBJ_RECTANGLE) - 1, 0 - 1, -1):
        name = ObjectName(0, i, 0, OBJ_RECTANGLE)
        if StringFind(name, 'Rect', 0) >= 0:
            ObjectDelete(0, name)

def PutRect(name, t1, p1, t2, p2, clr):
    ObjectDelete(0, name)
    ObjectCreate(0, name, OBJ_RECTANGLE, 0, t1, p1, t2, p2)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, name, OBJPROP_FILL, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(0, Days + 1):
        CopyTime(None, PERIOD_D1, 0, Days + 1, tm)
        CopyOpen(None, PERIOD_D1, 0, Days + 1, op)
        CopyClose(None, PERIOD_D1, 0, Days + 1, cl)
        time0 = tm[i]
        time1 = time0 + (3600 * 24)
        dopen = op[i]
        dclose = cl[i]
        if dclose < dopen:
            PutRect('Rect' + _str(dopen), time0, dopen, time1, dclose, DN)
        if dclose > dopen:
            PutRect('Rect' + _str(dopen), time0, dopen, time1, dclose, UP)
    return rates_total

# ---- global variables initialised from expressions
UP = _input('UP', _uint(Blue))  # цвет бычьего дня
DN = _input('DN', _uint(Red))  # цвет медвежьего дня


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorDay(_MQL5Indicator):
    name = 'ColorDay'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Days': 11,  # дней для расчета
    }

