"""rabbit — converted from MQL5: MQL5 Indicators/Rabbit/rabbit.mq5

Copyright: Jon Katana, VDV Soft (vdv_2001@mail.ru)

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Jon Katana, VDV Soft (vdv_2001@mail.ru)', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'rabbit', 'source': 'MQL5 Indicators/Rabbit/rabbit.mq5', 'folder': 'Rabbit', 'inputs': [{'mql': 'Yesterday', 'py': 'Yesterday', 'param': 'Yesterday', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Levels', 'py': 'Levels', 'param': 'Levels', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 16, 'label': '', 'sinput': False}, {'mql': 'FontColor', 'py': 'FontColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LineColor', 'py': 'LineColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DeepSkyBlue = 0xFFBF00  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name

# ---- inputs and global variables
Yesterday = _input('Yesterday', 0)
Levels = _input('Levels', 20)
FontSize = _input('FontSize', 16)
Prefix = 'Rabbit '

def OnInit():
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    rates = Arr(0, 0, factory=MqlRates)
    obj_name = ""
    shift = Yesterday + 1
    if CopyRates(None, PERIOD_D1, 0, shift + 1, rates) <= 0:
        return 0
    S = NormalizeDouble((rates[0].high - rates[0].low) * 0.236, Digits())
    D = NormalizeDouble(rates[0].low + ((rates[0].high - rates[0].low) * (0.618 - (Levels * 0.236))), Digits())
    obj_name = Prefix + 'S'
    if ObjectFind(0, obj_name) == -1:
        ObjectCreate(0, obj_name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, obj_name, OBJPROP_XDISTANCE, 5)
    ObjectSetInteger(0, obj_name, OBJPROP_YDISTANCE, _int(MathCeil(1.5 * FontSize)))
    ObjectSetInteger(0, obj_name, OBJPROP_COLOR, FontColor)
    ObjectSetInteger(0, obj_name, OBJPROP_FONTSIZE, FontSize)
    ObjectSetString(0, obj_name, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, obj_name, OBJPROP_TEXT, 'S = ' + DoubleToString(S, Digits()))
    for z in range(0, Levels * 2):
        U = NormalizeDouble(D + ((rates[0].high - rates[0].low) * z * 0.236), Digits())
        obj_name = Prefix + 'U' + _str(z)
        if ObjectFind(0, obj_name) == -1:
            ObjectCreate(0, obj_name, OBJ_TEXT, 0, time[rates_total - 1], U)
        ObjectSetInteger(0, obj_name, OBJPROP_TIME, 0, time[rates_total - 1] - PeriodSeconds(PERIOD_CURRENT))
        ObjectSetDouble(0, obj_name, OBJPROP_PRICE, 0, U)
        ObjectSetString(0, obj_name, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, obj_name, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
        ObjectSetInteger(0, obj_name, OBJPROP_FONTSIZE, FontSize)
        ObjectSetInteger(0, obj_name, OBJPROP_COLOR, FontColor)
        ObjectSetString(0, obj_name, OBJPROP_TEXT, DoubleToString(U, Digits()))
        obj_name = Prefix + 'U Line' + _str(z)
        if ObjectFind(0, obj_name) == -1:
            ObjectCreate(0, obj_name, OBJ_HLINE, 0, time[rates_total - 1], U)
        ObjectSetInteger(0, obj_name, OBJPROP_TIME, 0, time[rates_total - 1])
        ObjectSetDouble(0, obj_name, OBJPROP_PRICE, 0, U)
        ObjectSetInteger(0, obj_name, OBJPROP_COLOR, LineColor)
    return rates_total

def OnDeinit(reason):
    DeleteObjectPrefix(Prefix)

def DeleteObjectPrefix(prefix):
    i = 0
    objname = ""
    i = ObjectsTotal(0, 0, -1) - 1
    for i in range(i, 0 - 1, -1):
        objname = ObjectName(0, i)
        if StringFind(objname, prefix) == -1:
            continue
        else:
            ObjectDelete(0, objname)
    else:
        i = _range_end(i, 0 - 1, -1)

# ---- global variables initialised from expressions
FontColor = _input('FontColor', _uint(White))
LineColor = _input('LineColor', _uint(DeepSkyBlue))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rabbit(_MQL5Indicator):
    name = 'rabbit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Yesterday': 0,
        'Levels': 20,
        'FontSize': 16,
    }

