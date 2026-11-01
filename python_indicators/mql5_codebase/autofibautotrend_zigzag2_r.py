"""AutoFibAutoTrend_Zigzag2_R — converted from MQL5: MQL5 Indicators/AutoFibAutoTrend_Zigzag2_R/AutoFibAutoTrend_Zigzag2_R.mq5

Copyright: Copyright © 2016, zzuegg; Link: when-money-makes-money.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, zzuegg', 'link': 'when-money-makes-money.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'AutoFibAutoTrend_Zigzag2_R', 'source': 'MQL5 Indicators/AutoFibAutoTrend_Zigzag2_R/AutoFibAutoTrend_Zigzag2_R.mq5', 'folder': 'AutoFibAutoTrend_Zigzag2_R', 'inputs': [{'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Таймфрейм Зигзага для расчета индикатора', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Sirname', 'py': 'Sirname', 'param': None, 'type': 'string', 'default': 'AutoFibAutoTrend_Zigzag2_R', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'ShowFib', 'py': 'ShowFib', 'param': 'ShowFib', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'FibColor', 'py': 'FibColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': '', 'sinput': False}, {'mql': 'FibSize', 'py': 'FibSize', 'param': 'FibSize', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ShowFibFan', 'py': 'ShowFibFan', 'param': 'ShowFibFan', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'FibFanColor', 'py': 'FibFanColor', 'param': None, 'type': 'color', 'default': 13828244, 'label': '', 'sinput': False}, {'mql': 'FibFanSize', 'py': 'FibFanSize', 'param': 'FibFanSize', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ShowTrend', 'py': 'ShowTrend', 'param': 'ShowTrend', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'TrendColor', 'py': 'TrendColor', 'param': None, 'type': 'color', 'default': 10156544, 'label': '', 'sinput': False}, {'mql': 'TrendSize', 'py': 'TrendSize', 'param': 'TrendSize', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Timeframe = _input('Timeframe', PERIOD_H6)  # Таймфрейм Зигзага для расчета индикатора
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
Sirname = _input('Sirname', 'AutoFibAutoTrend_Zigzag2_R')  # Название для меток индикатора
ShowFib = _input('ShowFib', True)
FibColor = _input('FibColor', clrDodgerBlue)
FibSize = _input('FibSize', 1)
ShowFibFan = _input('ShowFibFan', True)
FibFanColor = _input('FibFanColor', clrDarkViolet)
FibFanSize = _input('FibFanSize', 1)
ShowTrend = _input('ShowTrend', True)
TrendColor = _input('TrendColor', clrMediumSpringGreen)
TrendSize = _input('TrendSize', 5)
Ind_Handle = 0
min_rates_total = 0
fib1 = ''
trend = ''
fibf1 = ''

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, fib1, fibf1, min_rates_total, trend
    min_rates_total = 100
    fib1 = Sirname + ' fib1 ' + GetStringTimeframe(Timeframe)
    trend = Sirname + ' trend1 ' + GetStringTimeframe(Timeframe)
    fibf1 = Sirname + ' fibf1 ' + GetStringTimeframe(Timeframe)
    Ind_Handle = iCustom(Symbol(), Timeframe, 'Zigzag2_R_Color', ExtDepth, ExtDeviation, ExtBackstep)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Zigzag2_R_Color')
        return INIT_FAILED
    shortname = Box("")
    StringConcatenate(shortname, 'AutoFibAutoTrend_Zigzag2_R(ExtDepth=', ExtDepth, 'ExtDeviation = ', ExtDeviation, 'ExtBackstep = ', ExtBackstep, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, fib1)
    ObjectDelete(0, trend)
    ObjectDelete(0, fibf1)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_curr
    if BarsCalculated(Ind_Handle) < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), Timeframe):
        return prev_calculated
    UpSign = Arr(0, 0.0)
    DnSign = Arr(0, 0.0)
    if CopyBuffer(Ind_Handle, 0, 0, rates_total, DnSign) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 1, 0, rates_total, UpSign) <= 0:
        return 0
    if CopyTime(Symbol(), Timeframe, 0, rates_total, _s_OnCalculate_TIME) <= 0:
        return 0
    ArraySetAsSeries(DnSign, True)
    ArraySetAsSeries(UpSign, True)
    ArraySetAsSeries(_s_OnCalculate_TIME, True)
    if _s_OnCalculate_curr != _s_OnCalculate_TIME[0]:
        _s_OnCalculate_curr = _s_OnCalculate_TIME[0]
        swing_value = Arr.of([0.0, 0.0, 0.0, 0.0], fill=0.0, dyn=False, size=4)
        swing_date = Arr.of([0, 0, 0, 0], fill=0, dyn=False, size=4)
        found = 0
        tmp = 0.0
        bar = 0
        while found < 4 and bar < rates_total:
            if UpSign[bar]:
                swing_value[found] = UpSign[bar]
                swing_date[found] = _s_OnCalculate_TIME[bar]
                found += 1
            if DnSign[bar]:
                swing_value[found] = DnSign[bar]
                swing_date[found] = _s_OnCalculate_TIME[bar]
                found += 1
            bar += 1
        if ShowTrend:
            SetChannel(0, trend, 0, swing_date[3], swing_value[3], swing_date[1], swing_value[1], swing_date[2], swing_value[2], TrendColor, 0, TrendSize, True, trend)
        if ShowFib:
            SetFibo(0, fib1, 0, swing_date[2], swing_value[2], swing_date[1], swing_value[1], FibColor, 0, FibSize, True, fib1)
        if ShowFibFan:
            SetFiboFan(0, fibf1, 0, swing_date[2], swing_value[2], swing_date[1], swing_value[1], FibFanColor, 0, FibFanSize, True, fibf1)
    ChartRedraw(0)
    return rates_total

def CreateFibo(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, ray, text):
    ObjectCreate(chart_id, name, OBJ_FIBO, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    if ray > 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    if ray < 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, True)
    if ray == 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, False)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    for numb in range(0, 10):
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELCOLOR, numb, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELSTYLE, numb, style)
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELWIDTH, numb, width)

def SetFibo(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, ray, text):
    if ObjectFind(chart_id, name) == -1:
        CreateFibo(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, ray, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)

def CreateFiboFan(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, ray, text):
    ObjectCreate(chart_id, name, OBJ_FIBOFAN, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    if ray > 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    if ray < 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, True)
    if ray == 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, False)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    for numb in range(0, 10):
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELCOLOR, numb, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELSTYLE, numb, style)
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELWIDTH, numb, width)

def SetFiboFan(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, ray, text):
    if ObjectFind(chart_id, name) == -1:
        CreateFiboFan(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, ray, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)

def CreateChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, style, width, ray, text):
    ObjectCreate(chart_id, name, OBJ_CHANNEL, nwin, time1, price1, time2, price2, time3, price3)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    if ray > 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    if ray < 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, True)
    if ray == 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, False)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    for numb in range(0, 10):
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELCOLOR, numb, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELSTYLE, numb, style)
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELWIDTH, numb, width)

def SetChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, style, width, ray, text):
    if ObjectFind(chart_id, name) == -1:
        CreateChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, style, width, ray, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectMove(chart_id, name, 2, time3, price3)

# ---- static local variables
_s_OnCalculate_TIME = Arr(0, 0)
_s_OnCalculate_curr = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AutoFibAutoTrendZigzag2R(_MQL5Indicator):
    name = 'AutoFibAutoTrend_Zigzag2_R'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Таймфрейм Зигзага для расчета индикатора
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
        'ShowFib': True,
        'FibSize': 1,
        'ShowFibFan': True,
        'FibFanSize': 1,
        'ShowTrend': True,
        'TrendSize': 5,
    }

