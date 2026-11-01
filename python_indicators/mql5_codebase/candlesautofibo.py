"""CandlesAutoFibo — converted from MQL5: MQL5 Indicators/CandlesAutoFibo/CandlesAutoFibo.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'CandlesAutoFibo', 'source': 'MQL5 Indicators/CandlesAutoFibo/CandlesAutoFibo.mq5', 'folder': 'CandlesAutoFibo', 'inputs': [{'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16408, 'label': 'Таймфрейм индикатора для расчета уровней Фибоначи', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для расчета уровней Фибоначи', 'sinput': False}, {'mql': 'FiboColor', 'py': 'FiboColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Цвет Фибо', 'sinput': False}, {'mql': 'FiboLevel1', 'py': 'FiboLevel1', 'param': 'FiboLevel1', 'type': 'double', 'default': 0.0, 'label': 'значение фибоуровня 1', 'sinput': False}, {'mql': 'Color_Level1', 'py': 'Color_Level1', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет фибоуровня 1', 'sinput': False}, {'mql': 'FiboLevel2', 'py': 'FiboLevel2', 'param': 'FiboLevel2', 'type': 'double', 'default': 0.236, 'label': 'значение фибоуровня 2', 'sinput': False}, {'mql': 'Color_Level2', 'py': 'Color_Level2', 'param': None, 'type': 'color', 'default': 13828244, 'label': 'цвет фибоуровня 2', 'sinput': False}, {'mql': 'FiboLevel3', 'py': 'FiboLevel3', 'param': 'FiboLevel3', 'type': 'double', 'default': 0.382, 'label': 'значение фибоуровня 3', 'sinput': False}, {'mql': 'Color_Level3', 'py': 'Color_Level3', 'param': None, 'type': 'color', 'default': 42495, 'label': 'цвет фибоуровня 3', 'sinput': False}, {'mql': 'FiboLevel4', 'py': 'FiboLevel4', 'param': 'FiboLevel4', 'type': 'double', 'default': 0.5, 'label': 'значение фибоуровня 4', 'sinput': False}, {'mql': 'Color_Level4', 'py': 'Color_Level4', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет фибоуровня 4', 'sinput': False}, {'mql': 'FiboLevel5', 'py': 'FiboLevel5', 'param': 'FiboLevel5', 'type': 'double', 'default': 0.618, 'label': 'значение фибоуровня 5', 'sinput': False}, {'mql': 'Color_Level5', 'py': 'Color_Level5', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет фибоуровня 5', 'sinput': False}, {'mql': 'FiboLevel6', 'py': 'FiboLevel6', 'param': 'FiboLevel6', 'type': 'double', 'default': 1.0, 'label': 'значение фибоуровня 6', 'sinput': False}, {'mql': 'Color_Level6', 'py': 'Color_Level6', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет фибоуровня 6', 'sinput': False}, {'mql': 'FiboLevel7', 'py': 'FiboLevel7', 'param': 'FiboLevel7', 'type': 'double', 'default': 1.236, 'label': 'значение фибоуровня 7', 'sinput': False}, {'mql': 'Color_Level7', 'py': 'Color_Level7', 'param': None, 'type': 'color', 'default': 13828244, 'label': 'цвет фибоуровня 7', 'sinput': False}, {'mql': 'FiboLevel8', 'py': 'FiboLevel8', 'param': 'FiboLevel8', 'type': 'double', 'default': 1.382, 'label': 'значение фибоуровня 8', 'sinput': False}, {'mql': 'Color_Level8', 'py': 'Color_Level8', 'param': None, 'type': 'color', 'default': 42495, 'label': 'цвет фибоуровня 8', 'sinput': False}, {'mql': 'FiboLevel9', 'py': 'FiboLevel9', 'param': 'FiboLevel9', 'type': 'double', 'default': 1.5, 'label': 'значение фибоуровня 9', 'sinput': False}, {'mql': 'Color_Level9', 'py': 'Color_Level9', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет фибоуровня 9', 'sinput': False}, {'mql': 'FiboLevel10', 'py': 'FiboLevel10', 'param': 'FiboLevel10', 'type': 'double', 'default': 1.618, 'label': 'значение фибоуровня 10', 'sinput': False}, {'mql': 'Color_Level10', 'py': 'Color_Level10', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет фибоуровня 10', 'sinput': False}, {'mql': 'FiboLevel11', 'py': 'FiboLevel11', 'param': 'FiboLevel11', 'type': 'double', 'default': 2.0, 'label': 'значение фибоуровня 11', 'sinput': False}, {'mql': 'Color_Level11', 'py': 'Color_Level11', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет фибоуровня 11', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Timeframe = _input('Timeframe', PERIOD_D1)  # Таймфрейм индикатора для расчета уровней Фибоначи
NumberofBar = _input('NumberofBar', 1)  # Номер бара для расчета уровней Фибоначи
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
Values = Arr(11, 0.0, dyn=False)
Colors = Arr(11, 0, dyn=False)
Styles = Arr(11, 0, dyn=False)
Widths = Arr(11, 0, dyn=False)

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
    if not FiboLevelsCreate(0, 'FIBO', 0, 0, 0.0, 0, 0.0, FiboColor, STYLE_SOLID, 0, True, False, False, True, False, 0):
        Print('Не удалось создать Фибо!')
        return INIT_FAILED
    if not FiboLevelsSet(11, Values, Colors, Styles, Widths, 0, 'FIBO'):
        Print('Не удалось настроить Фибо!')
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'CandlesAutoFibo')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    FiboLevelsDelete(0, 'FIBO')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    nOpen = Arr(1, 0.0, dyn=False)
    nClose = Arr(1, 0.0, dyn=False)
    nHigh = Arr(1, 0.0, dyn=False)
    nLow = Arr(1, 0.0, dyn=False)
    P1 = 0.0
    P2 = 0.0
    nTime = Arr(1, 0, dyn=False)
    to_copy = 0
    D1 = 0
    D2 = 0
    ArraySetAsSeries(time, True)
    to_copy = 1
    if CopyTime(None, Timeframe, NumberofBar, to_copy, nTime) < to_copy:
        return 0
    if CopyOpen(None, Timeframe, NumberofBar, to_copy, nOpen) < to_copy:
        return 0
    if CopyHigh(None, Timeframe, NumberofBar, to_copy, nHigh) < to_copy:
        return 0
    if CopyLow(None, Timeframe, NumberofBar, to_copy, nLow) < to_copy:
        return 0
    if CopyClose(None, Timeframe, NumberofBar, to_copy, nClose) < to_copy:
        return 0
    if nOpen[0] > nClose[0]:
        P1 = nHigh[0]
        P2 = nLow[0]
    else:
        P1 = nLow[0]
        P2 = nHigh[0]
    D1 = nTime[0]
    D2 = TimeCurrent()
    if not FiboLevelsPointChange(0, 'FIBO', 0, D1, P1):
        return rates_total
    if not FiboLevelsPointChange(0, 'FIBO', 1, D2, P2):
        return rates_total
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandlesAutoFibo(_MQL5Indicator):
    name = 'CandlesAutoFibo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Таймфрейм индикатора для расчета уровней Фибоначи
        'NumberofBar': 1,  # Номер бара для расчета уровней Фибоначи
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
    }

