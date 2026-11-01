"""CandlesAutoFibo_Grand_xN — converted from MQL5: MQL5 Indicators/CandlesAutoFibo_Grand_xN/CandlesAutoFibo_Grand_xN.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'CandlesAutoFibo_Grand_xN', 'source': 'MQL5 Indicators/CandlesAutoFibo_Grand_xN/CandlesAutoFibo_Grand_xN.mq5', 'folder': 'CandlesAutoFibo_Grand_xN', 'inputs': [{'mql': 'FiboName', 'py': 'FiboName', 'param': None, 'type': 'string', 'default': 'CandlesAutoFibo_Grand_xN', 'label': 'Имя Фибо-объекта', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16408, 'label': 'Таймфрейм индикатора для расчета уровней Фибоначи', 'sinput': False}, {'mql': 'FiboRatio', 'py': 'FiboRatio', 'param': 'FiboRatio', 'type': 'double', 'default': 1.0, 'label': 'Коэффициент домножения всех фибоуровней', 'sinput': False}, {'mql': 'FiboLevelsShift', 'py': 'FiboLevelsShift', 'param': 'FiboLevelsShift', 'type': 'double', 'default': 0.0, 'label': 'Сдвиг по вертикали всех фибоуровней в Фибах от нулевого уровня', 'sinput': False}, {'mql': 'FiboTotal', 'py': 'FiboTotal', 'param': 'FiboTotal', 'type': 'uint', 'default': 1, 'label': 'Количество дополнительных секторов Фибо сверху или снизу', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для расчета уровней Фибоначи', 'sinput': False}, {'mql': 'FiboColor', 'py': 'FiboColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Цвет Фибо', 'sinput': False}, {'mql': 'FiboLevel1', 'py': 'FiboLevel1', 'param': 'FiboLevel1', 'type': 'double', 'default': 0.0, 'label': 'значение фибоуровня 1', 'sinput': False}, {'mql': 'StyleLevel1', 'py': 'StyleLevel1', 'param': 'StyleLevel1', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 1', 'sinput': False}, {'mql': 'WidthLevel1', 'py': 'WidthLevel1', 'param': 'WidthLevel1', 'type': 'uint', 'default': 4, 'label': 'толщина линии фибоуровня 1', 'sinput': False}, {'mql': 'Color_Level1', 'py': 'Color_Level1', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'цвет фибоуровня 1', 'sinput': False}, {'mql': 'FiboLevel2', 'py': 'FiboLevel2', 'param': 'FiboLevel2', 'type': 'double', 'default': 0.236, 'label': 'значение фибоуровня 2', 'sinput': False}, {'mql': 'StyleLevel2', 'py': 'StyleLevel2', 'param': 'StyleLevel2', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 2', 'sinput': False}, {'mql': 'WidthLevel2', 'py': 'WidthLevel2', 'param': 'WidthLevel2', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 2', 'sinput': False}, {'mql': 'Color_Level2', 'py': 'Color_Level2', 'param': None, 'type': 'color', 'default': 13828244, 'label': 'цвет фибоуровня 2', 'sinput': False}, {'mql': 'FiboLevel3', 'py': 'FiboLevel3', 'param': 'FiboLevel3', 'type': 'double', 'default': 0.382, 'label': 'значение фибоуровня 3', 'sinput': False}, {'mql': 'StyleLevel3', 'py': 'StyleLevel3', 'param': 'StyleLevel3', 'type': 'int', 'default': 1, 'label': 'стиль линии фибоуровня 3', 'sinput': False}, {'mql': 'WidthLevel3', 'py': 'WidthLevel3', 'param': 'WidthLevel3', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 3', 'sinput': False}, {'mql': 'Color_Level3', 'py': 'Color_Level3', 'param': None, 'type': 'color', 'default': 42495, 'label': 'цвет фибоуровня 3', 'sinput': False}, {'mql': 'FiboLevel4', 'py': 'FiboLevel4', 'param': 'FiboLevel4', 'type': 'double', 'default': 0.5, 'label': 'значение фибоуровня 4', 'sinput': False}, {'mql': 'StyleLevel4', 'py': 'StyleLevel4', 'param': 'StyleLevel4', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 4', 'sinput': False}, {'mql': 'WidthLevel4', 'py': 'WidthLevel4', 'param': 'WidthLevel4', 'type': 'uint', 'default': 2, 'label': 'толщина линии фибоуровня 4', 'sinput': False}, {'mql': 'Color_Level4', 'py': 'Color_Level4', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет фибоуровня 4', 'sinput': False}, {'mql': 'FiboLevel5', 'py': 'FiboLevel5', 'param': 'FiboLevel5', 'type': 'double', 'default': 0.618, 'label': 'значение фибоуровня 5', 'sinput': False}, {'mql': 'StyleLevel5', 'py': 'StyleLevel5', 'param': 'StyleLevel5', 'type': 'int', 'default': 1, 'label': 'стиль линии фибоуровня 5', 'sinput': False}, {'mql': 'WidthLevel5', 'py': 'WidthLevel5', 'param': 'WidthLevel5', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 5', 'sinput': False}, {'mql': 'Color_Level5', 'py': 'Color_Level5', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет фибоуровня 5', 'sinput': False}, {'mql': 'FiboLevel6', 'py': 'FiboLevel6', 'param': 'FiboLevel6', 'type': 'double', 'default': 0.764, 'label': 'значение фибоуровня 6', 'sinput': False}, {'mql': 'StyleLevel6', 'py': 'StyleLevel6', 'param': 'StyleLevel6', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 6', 'sinput': False}, {'mql': 'WidthLevel6', 'py': 'WidthLevel6', 'param': 'WidthLevel6', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 6', 'sinput': False}, {'mql': 'Color_Level6', 'py': 'Color_Level6', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет фибоуровня 6', 'sinput': False}, {'mql': 'FiboLevel7', 'py': 'FiboLevel7', 'param': 'FiboLevel7', 'type': 'double', 'default': 1.0, 'label': 'значение фибоуровня 7', 'sinput': False}, {'mql': 'StyleLevel7', 'py': 'StyleLevel7', 'param': 'StyleLevel7', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 7', 'sinput': False}, {'mql': 'WidthLevel7', 'py': 'WidthLevel7', 'param': 'WidthLevel7', 'type': 'uint', 'default': 4, 'label': 'толщина линии фибоуровня 7', 'sinput': False}, {'mql': 'Color_Level7', 'py': 'Color_Level7', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'цвет фибоуровня 7', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FiboName = _input('FiboName', 'CandlesAutoFibo_Grand_xN')  # Имя Фибо-объекта
Timeframe = _input('Timeframe', PERIOD_D1)  # Таймфрейм индикатора для расчета уровней Фибоначи
FiboRatio = _input('FiboRatio', 1.0)  # Коэффициент домножения всех фибоуровней
FiboLevelsShift = _input('FiboLevelsShift', 0.0)  # Сдвиг по вертикали всех фибоуровней в Фибах от нулевого уровня
FiboTotal = _input('FiboTotal', 1)  # Количество дополнительных секторов Фибо сверху или снизу
NumberofBar = _input('NumberofBar', 1)  # Номер бара для расчета уровней Фибоначи
FiboColor = _input('FiboColor', clrGray)  # Цвет Фибо
FiboLevel1 = _input('FiboLevel1', 0.0)  # значение фибоуровня 1
StyleLevel1 = _input('StyleLevel1', STYLE_SOLID)  # стиль линии фибоуровня 1
WidthLevel1 = _input('WidthLevel1', 4)  # толщина линии фибоуровня 1
Color_Level1 = _input('Color_Level1', clrLimeGreen)  # цвет фибоуровня 1
FiboLevel2 = _input('FiboLevel2', 0.236)  # значение фибоуровня 2
StyleLevel2 = _input('StyleLevel2', STYLE_SOLID)  # стиль линии фибоуровня 2
WidthLevel2 = _input('WidthLevel2', 1)  # толщина линии фибоуровня 2
Color_Level2 = _input('Color_Level2', clrDarkViolet)  # цвет фибоуровня 2
FiboLevel3 = _input('FiboLevel3', 0.382)  # значение фибоуровня 3
StyleLevel3 = _input('StyleLevel3', STYLE_DASH)  # стиль линии фибоуровня 3
WidthLevel3 = _input('WidthLevel3', 1)  # толщина линии фибоуровня 3
Color_Level3 = _input('Color_Level3', clrOrange)  # цвет фибоуровня 3
FiboLevel4 = _input('FiboLevel4', 0.5)  # значение фибоуровня 4
StyleLevel4 = _input('StyleLevel4', STYLE_SOLID)  # стиль линии фибоуровня 4
WidthLevel4 = _input('WidthLevel4', 2)  # толщина линии фибоуровня 4
Color_Level4 = _input('Color_Level4', clrMagenta)  # цвет фибоуровня 4
FiboLevel5 = _input('FiboLevel5', 0.618)  # значение фибоуровня 5
StyleLevel5 = _input('StyleLevel5', STYLE_DASH)  # стиль линии фибоуровня 5
WidthLevel5 = _input('WidthLevel5', 1)  # толщина линии фибоуровня 5
Color_Level5 = _input('Color_Level5', clrBlue)  # цвет фибоуровня 5
FiboLevel6 = _input('FiboLevel6', 0.764)  # значение фибоуровня 6
StyleLevel6 = _input('StyleLevel6', STYLE_SOLID)  # стиль линии фибоуровня 6
WidthLevel6 = _input('WidthLevel6', 1)  # толщина линии фибоуровня 6
Color_Level6 = _input('Color_Level6', clrGray)  # цвет фибоуровня 6
FiboLevel7 = _input('FiboLevel7', 1.0)  # значение фибоуровня 7
StyleLevel7 = _input('StyleLevel7', STYLE_SOLID)  # стиль линии фибоуровня 7
WidthLevel7 = _input('WidthLevel7', 4)  # толщина линии фибоуровня 7
Color_Level7 = _input('Color_Level7', clrLimeGreen)  # цвет фибоуровня 7
Values = Arr(0, 0.0)
Colors = Arr(0, 0)
Styles = Arr(0, 0)
Widths = Arr(0, 0)

def FiboLevelsCreate(chart_ID=0, name='FiboLevels', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrLimeGreen, style=STYLE_SOLID, width=1, back=False, selection=True, ray_left=False, ray_right=False, hidden=True, z_order=0):
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
    ArrayResize(Values, (7 * (1 + (FiboTotal * 2))) - (FiboTotal * 2))
    ArrayResize(Colors, (7 * (1 + (FiboTotal * 2))) - (FiboTotal * 2))
    ArrayResize(Styles, (7 * (1 + (FiboTotal * 2))) - (FiboTotal * 2))
    ArrayResize(Widths, (7 * (1 + (FiboTotal * 2))) - (FiboTotal * 2))
    Values[0] = FiboLevel1 * FiboRatio
    Values[1] = FiboLevel2 * FiboRatio
    Values[2] = FiboLevel3 * FiboRatio
    Values[3] = FiboLevel4 * FiboRatio
    Values[4] = FiboLevel5 * FiboRatio
    Values[5] = FiboLevel6 * FiboRatio
    Values[6] = FiboLevel7 * FiboRatio
    Colors[0] = Color_Level1
    Colors[1] = Color_Level2
    Colors[2] = Color_Level3
    Colors[3] = Color_Level4
    Colors[4] = Color_Level5
    Colors[5] = Color_Level6
    Colors[6] = Color_Level7
    Styles[0] = StyleLevel1
    Styles[1] = StyleLevel2
    Styles[2] = StyleLevel3
    Styles[3] = StyleLevel4
    Styles[4] = StyleLevel5
    Styles[5] = StyleLevel6
    Styles[6] = StyleLevel7
    Widths[0] = WidthLevel1
    Widths[1] = WidthLevel2
    Widths[2] = WidthLevel3
    Widths[3] = WidthLevel4
    Widths[4] = WidthLevel5
    Widths[5] = WidthLevel6
    Widths[6] = WidthLevel7
    for count in range(1, _int(FiboTotal) + 1):
        for lev in range(1, 7):
            kkk = lev + (6 * ((2 * count) - 1))
            Values[kkk] = Values[lev] + count
            Colors[kkk] = Colors[lev]
            Styles[kkk] = Styles[lev]
            Widths[kkk] = Widths[lev]
            kkk = lev + (6 * (2 * count))
            Values[kkk] = (-Values[7 - lev]) - count + 1
            Colors[kkk] = Colors[lev - 1]
            Styles[kkk] = Styles[lev - 1]
            Widths[kkk] = Widths[lev - 1]
    if not FiboLevelsCreate(0, FiboName, 0, 0, 0.0, 0, 0.0, FiboColor, STYLE_SOLID, 0, True, False, False, True, False, 0):
        Print('Не удалось создать Фибо!')
        return INIT_FAILED
    if not FiboLevelsSet((7 * (1 + (FiboTotal * 2))) - (FiboTotal * 2), Values, Colors, Styles, Widths, 0, FiboName):
        Print('Не удалось настроить Фибо!')
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'CandlesAutoFibo_Grand_xN')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    FiboLevelsDelete(0, FiboName)
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
    vertSfift = (P2 - P1) * FiboLevelsShift
    P1 += vertSfift
    P2 += vertSfift
    D1 = nTime[0]
    D2 = TimeCurrent()
    if not FiboLevelsPointChange(0, FiboName, 0, D1, P1):
        return rates_total
    if not FiboLevelsPointChange(0, FiboName, 1, D2, P2):
        return rates_total
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandlesAutoFiboGrandXN(_MQL5Indicator):
    name = 'CandlesAutoFibo_Grand_xN'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Таймфрейм индикатора для расчета уровней Фибоначи
        'FiboRatio': 1.0,  # Коэффициент домножения всех фибоуровней
        'FiboLevelsShift': 0.0,  # Сдвиг по вертикали всех фибоуровней в Фибах от нулевого уровня
        'FiboTotal': 1,  # Количество дополнительных секторов Фибо сверху или снизу
        'NumberofBar': 1,  # Номер бара для расчета уровней Фибоначи
        'FiboLevel1': 0.0,  # значение фибоуровня 1
        'StyleLevel1': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 1
        'WidthLevel1': 4,  # толщина линии фибоуровня 1
        'FiboLevel2': 0.236,  # значение фибоуровня 2
        'StyleLevel2': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 2
        'WidthLevel2': 1,  # толщина линии фибоуровня 2
        'FiboLevel3': 0.382,  # значение фибоуровня 3
        'StyleLevel3': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # стиль линии фибоуровня 3
        'WidthLevel3': 1,  # толщина линии фибоуровня 3
        'FiboLevel4': 0.5,  # значение фибоуровня 4
        'StyleLevel4': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 4
        'WidthLevel4': 2,  # толщина линии фибоуровня 4
        'FiboLevel5': 0.618,  # значение фибоуровня 5
        'StyleLevel5': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # стиль линии фибоуровня 5
        'WidthLevel5': 1,  # толщина линии фибоуровня 5
        'FiboLevel6': 0.764,  # значение фибоуровня 6
        'StyleLevel6': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 6
        'WidthLevel6': 1,  # толщина линии фибоуровня 6
        'FiboLevel7': 1.0,  # значение фибоуровня 7
        'StyleLevel7': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 7
        'WidthLevel7': 4,  # толщина линии фибоуровня 7
    }

