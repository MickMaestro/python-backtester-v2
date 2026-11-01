"""PriceGrid1_Plus — converted from MQL5: MQL5 Indicators/PriceGrid1_Plus/PriceGrid1_Plus.mq5

Сетка из круглых ценовых уровней
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Сетка из круглых ценовых уровней'], 'name': 'PriceGrid1_Plus', 'source': 'MQL5 Indicators/PriceGrid1_Plus/PriceGrid1_Plus.mq5', 'folder': 'PriceGrid1_Plus', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'PriceGrid1_Plus', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'Digits_', 'py': 'Digits_', 'param': 'Digits_', 'type': 'uint', 'default': 2, 'label': 'разряд сетки', 'sinput': False}, {'mql': 'Total', 'py': 'Total', 'param': 'Total', 'type': 'uint', 'default': 200, 'label': 'количество блоков сетки сверху или снизу от цены', 'sinput': False}, {'mql': 'Color_A', 'py': 'Color_A', 'param': None, 'type': 'color', 'default': 13458026, 'label': 'цвет уровня 1', 'sinput': False}, {'mql': 'ShowPriceLable_A', 'py': 'ShowPriceLable_A', 'param': 'ShowPriceLable_A', 'type': 'bool', 'default': True, 'label': 'отображение значения ценовой метки 1 на ценовом графике', 'sinput': False}, {'mql': 'Color_AL', 'py': 'Color_AL', 'param': None, 'type': 'color', 'default': 14822282, 'label': 'цвет ценовой метки 1', 'sinput': False}, {'mql': 'Style_A', 'py': 'Style_A', 'param': 'Style_A', 'type': 'int', 'default': 4, 'label': 'стиль линии уровня 1', 'sinput': False}, {'mql': 'Width_A', 'py': 'Width_A', 'param': 'Width_A', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 1', 'sinput': False}, {'mql': 'Color_B', 'py': 'Color_B', 'param': None, 'type': 'color', 'default': 36095, 'label': 'цвет уровня 2', 'sinput': False}, {'mql': 'ShowPriceLable_B', 'py': 'ShowPriceLable_B', 'param': 'ShowPriceLable_B', 'type': 'bool', 'default': True, 'label': 'отображение значения ценовой метки 2 на ценовом графике', 'sinput': False}, {'mql': 'Color_BL', 'py': 'Color_BL', 'param': None, 'type': 'color', 'default': 55295, 'label': 'цвет ценовой метки 2', 'sinput': False}, {'mql': 'Style_B', 'py': 'Style_B', 'param': 'Style_B', 'type': 'int', 'default': 1, 'label': 'стиль линии уровня 2', 'sinput': False}, {'mql': 'Width_B', 'py': 'Width_B', 'param': 'Width_B', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 2', 'sinput': False}, {'mql': 'Color_C', 'py': 'Color_C', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет уровня 3', 'sinput': False}, {'mql': 'ShowPriceLable_C', 'py': 'ShowPriceLable_C', 'param': 'ShowPriceLable_C', 'type': 'bool', 'default': True, 'label': 'отображение значения ценовой метки 3 на ценовом графике', 'sinput': False}, {'mql': 'Color_CL', 'py': 'Color_CL', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет ценовой метки 3', 'sinput': False}, {'mql': 'Style_C', 'py': 'Style_C', 'param': 'Style_C', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 3', 'sinput': False}, {'mql': 'Width_C', 'py': 'Width_C', 'param': 'Width_C', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 3', 'sinput': False}, {'mql': 'Color_D', 'py': 'Color_D', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет уровня 4', 'sinput': False}, {'mql': 'ShowPriceLable_D', 'py': 'ShowPriceLable_D', 'param': 'ShowPriceLable_D', 'type': 'bool', 'default': True, 'label': 'отображение значения ценовой метки 4 на ценовом графике', 'sinput': False}, {'mql': 'Color_DL', 'py': 'Color_DL', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет ценовой метки 4', 'sinput': False}, {'mql': 'Style_D', 'py': 'Style_D', 'param': 'Style_D', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 4', 'sinput': False}, {'mql': 'Width_D', 'py': 'Width_D', 'param': 'Width_D', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 4', 'sinput': False}, {'mql': 'Color_E', 'py': 'Color_E', 'param': None, 'type': 'color', 'default': 65280, 'label': 'цвет уровня 5', 'sinput': False}, {'mql': 'ShowPriceLable_E', 'py': 'ShowPriceLable_E', 'param': 'ShowPriceLable_E', 'type': 'bool', 'default': True, 'label': 'отображение значения ценовой метки 5 на ценовом графике', 'sinput': False}, {'mql': 'Color_EL', 'py': 'Color_EL', 'param': None, 'type': 'color', 'default': 65280, 'label': 'цвет ценовой метки 5', 'sinput': False}, {'mql': 'Style_E', 'py': 'Style_E', 'param': 'Style_E', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 5', 'sinput': False}, {'mql': 'Width_E', 'py': 'Width_E', 'param': 'Width_E', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 5', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'uint', 'default': 2, 'label': 'размер ценовых меток', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 5, 'label': 'Сдвиг ценовых меток по горизонтали в барах', 'sinput': False}, {'mql': 'ShowLineInfo', 'py': 'ShowLineInfo', 'param': 'ShowLineInfo', 'type': 'bool', 'default': True, 'label': 'отображение значения уровня на ценовом графике', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Number
Number_0 = 0
Number_1 = 1
Number_2 = 2
Number_3 = 3
_enum('Number', {0: 'Number_0', 1: 'Number_1', 2: 'Number_2', 3: 'Number_3'})

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
SirName = _input('SirName', 'PriceGrid1_Plus')  # Первая часть имени графических объектов
Digits_ = _input('Digits_', 2)  # разряд сетки
Total = _input('Total', 200)  # количество блоков сетки сверху или снизу от цены
Color_A = _input('Color_A', clrSlateBlue)  # цвет уровня 1
ShowPriceLable_A = _input('ShowPriceLable_A', True)  # отображение значения ценовой метки 1 на ценовом графике
Color_AL = _input('Color_AL', clrBlueViolet)  # цвет ценовой метки 1
Style_A = _input('Style_A', DASHDOTDOT_)  # стиль линии уровня 1
Width_A = _input('Width_A', Width_1)  # толщина линии уровня 1
Color_B = _input('Color_B', clrDarkOrange)  # цвет уровня 2
ShowPriceLable_B = _input('ShowPriceLable_B', True)  # отображение значения ценовой метки 2 на ценовом графике
Color_BL = _input('Color_BL', clrGold)  # цвет ценовой метки 2
Style_B = _input('Style_B', DASH_)  # стиль линии уровня 2
Width_B = _input('Width_B', Width_1)  # толщина линии уровня 2
Color_C = _input('Color_C', clrMagenta)  # цвет уровня 3
ShowPriceLable_C = _input('ShowPriceLable_C', True)  # отображение значения ценовой метки 3 на ценовом графике
Color_CL = _input('Color_CL', clrMagenta)  # цвет ценовой метки 3
Style_C = _input('Style_C', SOLID_)  # стиль линии уровня 3
Width_C = _input('Width_C', Width_1)  # толщина линии уровня 3
Color_D = _input('Color_D', clrRed)  # цвет уровня 4
ShowPriceLable_D = _input('ShowPriceLable_D', True)  # отображение значения ценовой метки 4 на ценовом графике
Color_DL = _input('Color_DL', clrRed)  # цвет ценовой метки 4
Style_D = _input('Style_D', SOLID_)  # стиль линии уровня 4
Width_D = _input('Width_D', Width_1)  # толщина линии уровня 4
Color_E = _input('Color_E', clrLime)  # цвет уровня 5
ShowPriceLable_E = _input('ShowPriceLable_E', True)  # отображение значения ценовой метки 5 на ценовом графике
Color_EL = _input('Color_EL', clrLime)  # цвет ценовой метки 5
Style_E = _input('Style_E', SOLID_)  # стиль линии уровня 5
Width_E = _input('Width_E', Width_1)  # толщина линии уровня 5
FontSize = _input('FontSize', 2)  # размер ценовых меток
Shift = _input('Shift', 5)  # Сдвиг ценовых меток по горизонтали в барах
ShowLineInfo = _input('ShowLineInfo', True)  # отображение значения уровня на ценовом графике
clr = 0
clrl = 0
Style = 0
Width = 0
ShowPriceLable = False
middle = 0
size = 0
Normalize = 0
ObjectNames = Arr(0, "", dims=(2,))
PointPow10 = 0.0
PointPow100 = 0.0
PointPow1000 = 0.0
PointPow10000 = 0.0
PointPow100000 = 0.0
PriceGrid = Arr(0, 0.0)
Price = Arr(0, 0.0)

def OnInit():
    global Normalize, PointPow10, PointPow100, PointPow1000, PointPow10000, PointPow100000, middle, size
    size = _int(Total * 2)
    ArrayResize(ObjectNames, size)
    ArrayResize(PriceGrid, size)
    ArrayResize(Price, size)
    for count in range(0, size):
        ObjectNames[count][0] = SirName + ' PriceLine ' + _str(count)
    for count in range(0, size):
        ObjectNames[count][1] = SirName + ' PriceLable ' + _str(count)
    PointPow10 = Point() * MathPow(10, Digits_)
    PointPow100 = PointPow10 * 10
    PointPow1000 = PointPow10 * 100
    PointPow10000 = PointPow10 * 1000
    PointPow100000 = PointPow10 * 10000
    middle = _idiv(size, 2) - 1
    Normalize = _int(Digits() - Digits_)
    for count in range(middle, size):
        PriceGrid[count] = NormalizeDouble(PointPow10 * (count - middle), Normalize)
    for count in range(middle - 1, 0 - 1, -1):
        PriceGrid[count] = -NormalizeDouble(PointPow10 * (middle - count), Normalize)

def OnDeinit(reason):
    for count in range(0, size):
        ObjectDelete(0, ObjectNames[count][0])
    for count in range(0, size):
        ObjectDelete(0, ObjectNames[count][1])
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ShowPriceLable, Style, Width, _s_OnCalculate_res_prev, clr, clrl
    res = NormalizeDouble(PointPow10 * MathCeil(_fdiv(close[rates_total - 1], PointPow10)), Normalize)
    if not (res - _s_OnCalculate_res_prev):
        return rates_total
    _s_OnCalculate_res_prev = res
    for count in range(0, size):
        Price[count] = NormalizeDouble(res + PriceGrid[count], Normalize)
    time0 = time[rates_total - 1] + (PeriodSeconds() * Shift)
    timeX = time[0]
    count = 0
    while count < size:
        if not NormalizeDouble(Price[count] - (PointPow100000 * MathCeil(_fdiv(Price[count], PointPow100000))), Normalize):
            clr = Color_E
            clrl = Color_EL
            ShowPriceLable = ShowPriceLable_E
            Style = Style_E
            Width = Width_E
        elif not NormalizeDouble(Price[count] - (PointPow10000 * MathCeil(_fdiv(Price[count], PointPow10000))), Normalize):
            clr = Color_D
            clrl = Color_DL
            ShowPriceLable = ShowPriceLable_D
            Style = Style_D
            Width = Width_D
        elif not NormalizeDouble(Price[count] - (PointPow1000 * MathCeil(_fdiv(Price[count], PointPow1000))), Normalize):
            clr = Color_C
            clrl = Color_CL
            ShowPriceLable = ShowPriceLable_C
            Style = Style_C
            Width = Width_C
        elif not NormalizeDouble(Price[count] - (PointPow100 * MathCeil(_fdiv(Price[count], PointPow100))), Normalize):
            clr = Color_B
            clrl = Color_BL
            ShowPriceLable = ShowPriceLable_B
            Style = Style_B
            Width = Width_B
        else:
            clr = Color_A
            clrl = Color_AL
            ShowPriceLable = ShowPriceLable_A
            Style = Style_A
            Width = Width_A
        info = ''
        if ShowLineInfo:
            info = ObjectNames[count][0] + ' ' + DoubleToString(Price[count], Normalize)
        SetTline(0, ObjectNames[count][0], 0, timeX, Price[count], time0, Price[count], clr, Style, Width, info)
        if ShowPriceLable:
            if ShowLineInfo:
                info = ObjectNames[count][1] + ' ' + DoubleToString(Price[count], Normalize)
            SetRightPrice(0, ObjectNames[count][1], 0, time0, Price[count], clrl, FontSize, info)
        count += 1
    ChartRedraw(0)
    return rates_total

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
        ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)

def CreateRightPrice(chart_id, name, nwin, time, price, Color, fontsize, text):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, fontsize)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)

def SetRightPrice(chart_id, name, nwin, time, price, Color, fontsize, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color, fontsize, text)
    else:
        ObjectMove(chart_id, name, 0, time, price)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

# ---- static local variables
_s_OnCalculate_res_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceGrid1Plus(_MQL5Indicator):
    name = 'PriceGrid1_Plus'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Digits_': 2,  # разряд сетки
        'Total': 200,  # количество блоков сетки сверху или снизу от цены
        'ShowPriceLable_A': True,  # отображение значения ценовой метки 1 на ценовом графике
        'Style_A': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=4),  # стиль линии уровня 1
        'Width_A': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня 1
        'ShowPriceLable_B': True,  # отображение значения ценовой метки 2 на ценовом графике
        'Style_B': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=1),  # стиль линии уровня 2
        'Width_B': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня 2
        'ShowPriceLable_C': True,  # отображение значения ценовой метки 3 на ценовом графике
        'Style_C': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль линии уровня 3
        'Width_C': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня 3
        'ShowPriceLable_D': True,  # отображение значения ценовой метки 4 на ценовом графике
        'Style_D': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль линии уровня 4
        'Width_D': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня 4
        'ShowPriceLable_E': True,  # отображение значения ценовой метки 5 на ценовом графике
        'Style_E': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль линии уровня 5
        'Width_E': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня 5
        'FontSize': 2,  # размер ценовых меток
        'Shift': 5,  # Сдвиг ценовых меток по горизонтали в барах
        'ShowLineInfo': True,  # отображение значения уровня на ценовом графике
    }

