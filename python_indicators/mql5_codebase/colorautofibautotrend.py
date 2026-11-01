"""ColorAutoFibAutoTrend — converted from MQL5: MQL5 Indicators/ColorAutoFibAutoTrend/ColorAutoFibAutoTrend.mq5

Copyright: Copyright © 2016, zzuegg; Link: when-money-makes-money.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, zzuegg', 'link': 'when-money-makes-money.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ColorAutoFibAutoTrend', 'source': 'MQL5 Indicators/ColorAutoFibAutoTrend/ColorAutoFibAutoTrend.mq5', 'folder': 'ColorAutoFibAutoTrend', 'inputs': [{'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Таймфрейм Зигзага для расчета индикатора', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Sirname', 'py': 'Sirname', 'param': None, 'type': 'string', 'default': 'AutoFibAutoTrend', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'ShowFib', 'py': 'ShowFib', 'param': 'ShowFib', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'FiboColor', 'py': 'FiboColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Цвет Фибо', 'sinput': False}, {'mql': 'FiboLevel1', 'py': 'FiboLevel1', 'param': 'FiboLevel1', 'type': 'double', 'default': 0.0, 'label': 'значение фибоуровня 1', 'sinput': False}, {'mql': 'Color_Level1', 'py': 'Color_Level1', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет фибоуровня 1', 'sinput': False}, {'mql': 'FiboLevel2', 'py': 'FiboLevel2', 'param': 'FiboLevel2', 'type': 'double', 'default': 0.236, 'label': 'значение фибоуровня 2', 'sinput': False}, {'mql': 'Color_Level2', 'py': 'Color_Level2', 'param': None, 'type': 'color', 'default': 13828244, 'label': 'цвет фибоуровня 2', 'sinput': False}, {'mql': 'FiboLevel3', 'py': 'FiboLevel3', 'param': 'FiboLevel3', 'type': 'double', 'default': 0.382, 'label': 'значение фибоуровня 3', 'sinput': False}, {'mql': 'Color_Level3', 'py': 'Color_Level3', 'param': None, 'type': 'color', 'default': 42495, 'label': 'цвет фибоуровня 3', 'sinput': False}, {'mql': 'FiboLevel4', 'py': 'FiboLevel4', 'param': 'FiboLevel4', 'type': 'double', 'default': 0.5, 'label': 'значение фибоуровня 4', 'sinput': False}, {'mql': 'Color_Level4', 'py': 'Color_Level4', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет фибоуровня 4', 'sinput': False}, {'mql': 'FiboLevel5', 'py': 'FiboLevel5', 'param': 'FiboLevel5', 'type': 'double', 'default': 0.618, 'label': 'значение фибоуровня 5', 'sinput': False}, {'mql': 'Color_Level5', 'py': 'Color_Level5', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет фибоуровня 5', 'sinput': False}, {'mql': 'FiboLevel6', 'py': 'FiboLevel6', 'param': 'FiboLevel6', 'type': 'double', 'default': 1.0, 'label': 'значение фибоуровня 6', 'sinput': False}, {'mql': 'Color_Level6', 'py': 'Color_Level6', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет фибоуровня 6', 'sinput': False}, {'mql': 'FiboLevel7', 'py': 'FiboLevel7', 'param': 'FiboLevel7', 'type': 'double', 'default': 1.236, 'label': 'значение фибоуровня 7', 'sinput': False}, {'mql': 'Color_Level7', 'py': 'Color_Level7', 'param': None, 'type': 'color', 'default': 13828244, 'label': 'цвет фибоуровня 7', 'sinput': False}, {'mql': 'FiboLevel8', 'py': 'FiboLevel8', 'param': 'FiboLevel8', 'type': 'double', 'default': 1.382, 'label': 'значение фибоуровня 8', 'sinput': False}, {'mql': 'Color_Level8', 'py': 'Color_Level8', 'param': None, 'type': 'color', 'default': 42495, 'label': 'цвет фибоуровня 8', 'sinput': False}, {'mql': 'FiboLevel9', 'py': 'FiboLevel9', 'param': 'FiboLevel9', 'type': 'double', 'default': 1.5, 'label': 'значение фибоуровня 9', 'sinput': False}, {'mql': 'Color_Level9', 'py': 'Color_Level9', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет фибоуровня 9', 'sinput': False}, {'mql': 'FiboLevel10', 'py': 'FiboLevel10', 'param': 'FiboLevel10', 'type': 'double', 'default': 1.618, 'label': 'значение фибоуровня 10', 'sinput': False}, {'mql': 'Color_Level10', 'py': 'Color_Level10', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет фибоуровня 10', 'sinput': False}, {'mql': 'FiboLevel11', 'py': 'FiboLevel11', 'param': 'FiboLevel11', 'type': 'double', 'default': 2.0, 'label': 'значение фибоуровня 11', 'sinput': False}, {'mql': 'Color_Level11', 'py': 'Color_Level11', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет фибоуровня 11', 'sinput': False}, {'mql': 'ShowFibFan', 'py': 'ShowFibFan', 'param': 'ShowFibFan', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'FibFanColor', 'py': 'FibFanColor', 'param': None, 'type': 'color', 'default': 7451452, 'label': '', 'sinput': False}, {'mql': 'FibFanSize', 'py': 'FibFanSize', 'param': 'FibFanSize', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ShowTrend', 'py': 'ShowTrend', 'param': 'ShowTrend', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'TrendColor', 'py': 'TrendColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'TrendSize', 'py': 'TrendSize', 'param': 'TrendSize', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Timeframe = _input('Timeframe', PERIOD_H6)  # Таймфрейм Зигзага для расчета индикатора
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
Sirname = _input('Sirname', 'AutoFibAutoTrend')  # Название для меток индикатора
ShowFib = _input('ShowFib', True)
FiboColor = _input('FiboColor', clrGray)  # Цвет Фибо
FiboLevel1 = _input('FiboLevel1', 0.0)  # значение фибоуровня 1
Color_Level1 = _input('Color_Level1', clrRed)  # цвет фибоуровня 1
FiboLevel2 = _input('FiboLevel2', 0.236)  # значение фибоуровня 2
Color_Level2 = _input('Color_Level2', clrDarkViolet)  # цвет фибоуровня 2
FiboLevel3 = _input('FiboLevel3', 0.382)  # значение фибоуровня 3
Color_Level3 = _input('Color_Level3', clrOrange)  # цвет фибоуровня 3
FiboLevel4 = _input('FiboLevel4', 0.5)  # значение фибоуровня 4
Color_Level4 = _input('Color_Level4', clrMagenta)  # цвет фибоуровня 4
FiboLevel5 = _input('FiboLevel5', 0.618)  # значение фибоуровня 5
Color_Level5 = _input('Color_Level5', clrBlue)  # цвет фибоуровня 5
FiboLevel6 = _input('FiboLevel6', 1.0)  # значение фибоуровня 6
Color_Level6 = _input('Color_Level6', clrRed)  # цвет фибоуровня 6
FiboLevel7 = _input('FiboLevel7', 1.236)  # значение фибоуровня 7
Color_Level7 = _input('Color_Level7', clrDarkViolet)  # цвет фибоуровня 7
FiboLevel8 = _input('FiboLevel8', 1.382)  # значение фибоуровня 8
Color_Level8 = _input('Color_Level8', clrOrange)  # цвет фибоуровня 8
FiboLevel9 = _input('FiboLevel9', 1.5)  # значение фибоуровня 9
Color_Level9 = _input('Color_Level9', clrMagenta)  # цвет фибоуровня 9
FiboLevel10 = _input('FiboLevel10', 1.618)  # значение фибоуровня 10
Color_Level10 = _input('Color_Level10', clrBlue)  # цвет фибоуровня 10
FiboLevel11 = _input('FiboLevel11', 2.0)  # значение фибоуровня 11
Color_Level11 = _input('Color_Level11', clrRed)  # цвет фибоуровня 11
ShowFibFan = _input('ShowFibFan', True)
FibFanColor = _input('FibFanColor', clrMediumSeaGreen)
FibFanSize = _input('FibFanSize', 1)
ShowTrend = _input('ShowTrend', True)
TrendColor = _input('TrendColor', clrBlue)
TrendSize = _input('TrendSize', 5)
Ind_Handle = 0
min_rates_total = 0
fib1 = ''
trend = ''
fibf1 = ''
Values = Arr(11, 0.0, dyn=False)
Colors = Arr(11, 0, dyn=False)
Styles = Arr(11, 0, dyn=False)
Widths = Arr(11, 0, dyn=False)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def FiboLevelsCreate(chart_ID=0, name='FiboLevels', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, ray_left=False, ray_right=False, hidden=True, z_order=0):
    time1 = Box(time1)
    price1 = Box(price1)
    time2 = Box(time2)
    price2 = Box(price2)
    ChangeFiboLevelsEmptyPoints(time1, price1, time2, price2)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_FIBO, sub_window, time1.v, price1.v, time2.v, price2.v):
        Print('FiboLevelsCreate', ': не удалось создать "Уровни Фибоначчи"! Код ошибки = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_LEFT, ray_left)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_RIGHT, ray_right)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def FiboLevelsSet(levels, values, colors, styles, widths, chart_ID=0, name='FiboLevels'):
    if ((levels != ArraySize(colors) or levels != ArraySize(styles)) or levels != ArraySize(widths)) or levels != ArraySize(widths):
        Print('FiboLevelsSet', ': длина массива не соответствует количеству уровней, ошибка!')
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_LEVELS, levels)
    for i in range(0, levels):
        ObjectSetDouble(chart_ID, name, OBJPROP_LEVELVALUE, i, values[i])
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELCOLOR, i, colors[i])
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELSTYLE, i, styles[i])
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELWIDTH, i, widths[i])
        ObjectSetString(chart_ID, name, OBJPROP_LEVELTEXT, i, DoubleToString(100 * values[i], 1))
    return True

def FiboLevelsPointChange(chart_ID=0, name='FiboLevels', point_index=0, time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, point_index, time, price):
        Print('FiboLevelsPointChange', ': не удалось переместить точку привязки! Код ошибки = ', GetLastError())
        return False
    return True

def FiboLevelsDelete(chart_ID=0, name='FiboLevels'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('FiboLevelsDelete', ': не удалось удалить "Уровни Фибоначчи"! Код ошибки = ', GetLastError())
        return False
    return True

def ChangeFiboLevelsEmptyPoints(time1, price1, time2, price2):
    if not time2.v:
        time2.v = TimeCurrent()
    if not price2.v:
        price2.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    if not time1.v:
        temp = Arr(10, 0, dyn=False)
        CopyTime(Symbol(), Period(), _DT(time2.v), 10, temp)
        time1.v = temp[0]
    if not price1.v:
        price1.v = price2.v - (200 * SymbolInfoDouble(Symbol(), SYMBOL_POINT))

def OnInit():
    global Ind_Handle, fib1, fibf1, min_rates_total, trend
    min_rates_total = 100
    fib1 = Sirname + ' fib1 ' + GetStringTimeframe(Timeframe)
    trend = Sirname + ' trend1 ' + GetStringTimeframe(Timeframe)
    fibf1 = Sirname + ' fibf1 ' + GetStringTimeframe(Timeframe)
    Ind_Handle = iCustom(Symbol(), Timeframe, 'ZigZag_NK_Color', ExtDepth, ExtDeviation, ExtBackstep)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ZigZag_NK_Color')
        return INIT_FAILED
    if ShowFib:
        Values[0] = FiboLevel1
        Values[1] = FiboLevel2
        Values[2] = FiboLevel3
        Values[3] = FiboLevel4
        Values[4] = FiboLevel5
        Values[5] = FiboLevel6
        Values[6] = FiboLevel7
        Values[7] = FiboLevel8
        Values[8] = FiboLevel9
        Values[9] = FiboLevel10
        Values[10] = FiboLevel11
        Colors[0] = Color_Level1
        Colors[1] = Color_Level2
        Colors[2] = Color_Level3
        Colors[3] = Color_Level4
        Colors[4] = Color_Level5
        Colors[5] = Color_Level6
        Colors[6] = Color_Level7
        Colors[7] = Color_Level8
        Colors[8] = Color_Level9
        Colors[9] = Color_Level10
        Colors[10] = Color_Level11
        Styles[0] = STYLE_SOLID
        Styles[1] = STYLE_DASHDOTDOT
        Styles[2] = STYLE_DASHDOTDOT
        Styles[3] = STYLE_DASH
        Styles[4] = STYLE_DASHDOTDOT
        Styles[5] = STYLE_SOLID
        Styles[6] = STYLE_DASHDOTDOT
        Styles[7] = STYLE_DASHDOTDOT
        Styles[8] = STYLE_DASH
        Styles[9] = STYLE_DASHDOTDOT
        Styles[10] = STYLE_SOLID
        ArrayInitialize(Widths, None)
        if not FiboLevelsCreate(0, fib1, 0, 0, 0.0, 0, 0.0, FiboColor, STYLE_SOLID, 2, True, False, False, True, False, 0):
            Print('Не удалось создать Фибо!')
            return INIT_FAILED
        if not FiboLevelsSet(11, Values, Colors, Styles, Widths, 0, fib1):
            Print('Не удалось настроить Фибо!')
            return INIT_FAILED
    shortname = Box("")
    StringConcatenate(shortname, 'ZigZag (ExtDepth=', ExtDepth, 'ExtDeviation = ', ExtDeviation, 'ExtBackstep = ', ExtBackstep, ')')
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
            if not FiboLevelsPointChange(0, fib1, 0, swing_date[2], swing_value[2]):
                return rates_total
            if not FiboLevelsPointChange(0, fib1, 1, swing_date[1], swing_value[1]):
                return rates_total
        if ShowFibFan:
            SetFiboFan(0, fibf1, 0, swing_date[2], swing_value[2], swing_date[1], swing_value[1], FibFanColor, 0, FibFanSize, True, fibf1)
    ChartRedraw(0)
    return rates_total

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


class ColorAutoFibAutoTrend(_MQL5Indicator):
    name = 'ColorAutoFibAutoTrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Таймфрейм Зигзага для расчета индикатора
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
        'ShowFib': True,
        'FiboLevel1': 0.0,  # значение фибоуровня 1
        'FiboLevel2': 0.236,  # значение фибоуровня 2
        'FiboLevel3': 0.382,  # значение фибоуровня 3
        'FiboLevel4': 0.5,  # значение фибоуровня 4
        'FiboLevel5': 0.618,  # значение фибоуровня 5
        'FiboLevel6': 1.0,  # значение фибоуровня 6
        'FiboLevel7': 1.236,  # значение фибоуровня 7
        'FiboLevel8': 1.382,  # значение фибоуровня 8
        'FiboLevel9': 1.5,  # значение фибоуровня 9
        'FiboLevel10': 1.618,  # значение фибоуровня 10
        'FiboLevel11': 2.0,  # значение фибоуровня 11
        'ShowFibFan': True,
        'FibFanSize': 1,
        'ShowTrend': True,
        'TrendSize': 5,
    }

