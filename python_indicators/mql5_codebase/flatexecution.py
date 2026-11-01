"""flatexecution — converted from MQL5: MQL5 Indicators/Execution of Flat/flatexecution.mq5

Copyright: JLY; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'JLY', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'flatexecution', 'source': 'MQL5 Indicators/Execution of Flat/flatexecution.mq5', 'folder': 'Execution of Flat', 'inputs': [{'mql': 'accuracyTF', 'py': 'accuracyTF', 'param': 'accuracyTF', 'type': 'int', 'default': 0, 'label': 'Точность', 'sinput': False}, {'mql': 'Execut', 'py': 'Execut', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет исполнения', 'sinput': False}, {'mql': 'NotExecut', 'py': 'NotExecut', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет неисполнения', 'sinput': False}, {'mql': 'sub_window', 'py': 'sub_window', 'param': 'sub_window', 'type': 'int', 'default': 0, 'label': 'Подокно графика', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
accuracyTF = _input('accuracyTF', PERIOD_CURRENT)  # Точность
sub_window = _input('sub_window', 0)  # Подокно графика

def OnInit():
    ObjectsDeleteAll(0, sub_window, OBJ_ARROW)

def OnDeinit(reason):
    ObjectsDeleteAll(0, sub_window, OBJ_ARROW)

def TFMigrate(tf):
    _sw1 = tf
    if _sw1 == 0:
        return PERIOD_CURRENT
    elif _sw1 == 1:
        return PERIOD_M1
    elif _sw1 == 5:
        return PERIOD_M5
    elif _sw1 == 15:
        return PERIOD_M15
    elif _sw1 == 30:
        return PERIOD_M30
    elif _sw1 == 60:
        return PERIOD_H1
    elif _sw1 == 240:
        return PERIOD_H4
    elif _sw1 == 1440:
        return PERIOD_D1
    elif _sw1 == 10080:
        return PERIOD_W1
    elif _sw1 == 43200:
        return PERIOD_MN1
    elif _sw1 == 2:
        return PERIOD_M2
    elif _sw1 == 3:
        return PERIOD_M3
    elif _sw1 == 4:
        return PERIOD_M4
    elif _sw1 == 6:
        return PERIOD_M6
    elif _sw1 == 10:
        return PERIOD_M10
    elif _sw1 == 12:
        return PERIOD_M12
    elif _sw1 == 16385:
        return PERIOD_H1
    elif _sw1 == 16386:
        return PERIOD_H2
    elif _sw1 == 16387:
        return PERIOD_H3
    elif _sw1 == 16388:
        return PERIOD_H4
    elif _sw1 == 16390:
        return PERIOD_H6
    elif _sw1 == 16392:
        return PERIOD_H8
    elif _sw1 == 16396:
        return PERIOD_H12
    elif _sw1 == 16408:
        return PERIOD_D1
    elif _sw1 == 32769:
        return PERIOD_W1
    elif _sw1 == 49153:
        return PERIOD_MN1
    else:
        return PERIOD_CURRENT

def iBarShift_u(symbol, tf, time, exact=False):
    if time < 0:
        return -1
    timeframe = TFMigrate(tf)
    Arr_ = Arr(0, 0)
    time1 = 0
    CopyTime(symbol, timeframe, 0, 1, Arr_)
    time1 = Arr_[0]
    if CopyTime(symbol, timeframe, _DT(time), _DT(time1), Arr_) > 0:
        if ArraySize(Arr_) > 2:
            return ArraySize(Arr_) - 1
        if time < time1:
            return 1
        else:
            return 0
    else:
        return -1

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    name = ""
    time1NEW = 0
    time2NEW = 0
    price1NEW = 0.0
    price2NEW = 0.0
    price3 = 0.0
    i = 0
    while i < ObjectsTotal(0, sub_window, -1):
        if ObjectGetInteger(0, ObjectName(0, i, sub_window, -1), OBJPROP_TYPE, 0) == OBJ_TREND:
            name = ObjectName(0, i, sub_window, -1)
            price1NEW = ObjectGetDouble(0, name, OBJPROP_PRICE, 0)
            price2NEW = ObjectGetDouble(0, name, OBJPROP_PRICE, 1)
            time1NEW = ObjectGetInteger(0, name, OBJPROP_TIME, 0)
            time2NEW = ObjectGetInteger(0, name, OBJPROP_TIME, 1)
            price3 = price2NEW - (price1NEW - price2NEW)
            ObjectSetInteger(0, name, OBJPROP_COLOR, Execut)
            ObjectSetInteger(0, name, OBJPROP_WIDTH, 1)
            ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, True)
            ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DOT)
            Time = Arr(0, 0)
            Open = Arr(0, 0.0)
            bars = Bars(Symbol(), accuracyTF)
            ArraySetAsSeries(Time, True)
            CopyTime(Symbol(), accuracyTF, 0, bars, Time)
            time01 = time1NEW
            time02 = time2NEW
            shift01 = iBarShift_u(Symbol(), accuracyTF, time01, False)
            shift02 = iBarShift_u(Symbol(), accuracyTF, time02, False)
            timeCHANGE = shift01 - shift02
            T1970 = 0
            timeBAR1970 = iBarShift_u(Symbol(), accuracyTF, T1970, False)
            timeBAR = 0
            timeBAR = shift02 - timeCHANGE
            if timeBAR < 0:
                timeBAR = timeBAR1970
                ObjectSetInteger(0, name, OBJPROP_COLOR, NotExecut)
                ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID)
            timeBARsec = Time[timeBAR]
            ObjectSetString(0, name, OBJPROP_TEXT, IntegerToString(timeCHANGE - 1) + ' bars')
            ArraySetAsSeries(Open, True)
            CopyOpen(Symbol(), accuracyTF, 0, bars, Open)
            ObjectDelete(0, 'Execution ' + name)
            ObjectDelete(0, 'ExecutionOnLine ' + name)
            ET = TimeToString(timeBARsec, TIME_DATE | TIME_MINUTES)
            EP = DoubleToString(Open[timeBAR], 4)
            ObjectCreate(0, 'ExecutionOnLine ' + name, OBJ_ARROW, sub_window, timeBARsec, price3)
            ObjectSetInteger(0, 'ExecutionOnLine ' + name, OBJPROP_COLOR, Execut)
            ObjectSetInteger(0, 'ExecutionOnLine ' + name, OBJPROP_ARROWCODE, 85)
            ObjectSetInteger(0, 'ExecutionOnLine ' + name, OBJPROP_BACK, False)
            ObjectSetString(0, 'ExecutionOnLine ' + name, OBJPROP_TEXT, ET)
            ObjectCreate(0, 'Execution ' + name, OBJ_ARROW, 0, timeBARsec, Open[timeBAR])
            ObjectSetInteger(0, 'Execution ' + name, OBJPROP_COLOR, Execut)
            ObjectSetInteger(0, 'Execution ' + name, OBJPROP_ARROWCODE, 119)
            ObjectSetInteger(0, 'Execution ' + name, OBJPROP_BACK, False)
            ObjectSetString(0, 'Execution ' + name, OBJPROP_TEXT, ET + ' * ' + EP)
        i += 1
    return rates_total

# ---- global variables initialised from expressions
Execut = _input('Execut', _uint(Blue))  # Цвет исполнения
NotExecut = _input('NotExecut', _uint(Red))  # Цвет неисполнения


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Flatexecution(_MQL5Indicator):
    name = 'flatexecution'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'accuracyTF': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Точность
        'sub_window': 0,  # Подокно графика
    }

