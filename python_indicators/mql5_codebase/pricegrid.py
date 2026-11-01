"""PriceGrid — converted from MQL5: MQL5 Indicators/PriceGrid/PriceGrid.mq5

Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'PriceGrid', 'source': 'MQL5 Indicators/PriceGrid/PriceGrid.mq5', 'folder': 'PriceGrid', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'PriceGrid', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'Digits_', 'py': 'Digits_', 'param': 'Digits_', 'type': 'uint', 'default': 2, 'label': 'разряд сетки', 'sinput': False}, {'mql': 'Total', 'py': 'Total', 'param': 'Total', 'type': 'uint', 'default': 20, 'label': 'количество блоков сетки сверху или снизу от цены', 'sinput': False}, {'mql': 'Color_', 'py': 'Color_', 'param': None, 'type': 'color', 'default': 14822282, 'label': 'цвет уровня', 'sinput': False}, {'mql': 'Style_', 'py': 'Style_', 'param': 'Style_', 'type': 'int', 'default': 4, 'label': 'стиль линии уровня', 'sinput': False}, {'mql': 'Width_', 'py': 'Width_', 'param': 'Width_', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Number
Number_0 = 0
Number_1 = 1
Number_2 = 2
Number_3 = 3
_enum('Number', {0: 'Number_0', 1: 'Number_1', 2: 'Number_2', 3: 'Number_3'})

# enum Width
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('Width', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
SirName = _input('SirName', 'PriceGrid')  # Первая часть имени графических объектов
Digits_ = _input('Digits_', 2)  # разряд сетки
Total = _input('Total', 20)  # количество блоков сетки сверху или снизу от цены
Color_ = _input('Color_', clrBlueViolet)  # цвет уровня
Style_ = _input('Style_', DASHDOTDOT_)  # стиль линии уровня
Width_ = _input('Width_', Width_1)  # толщина линии уровня
middle = 0
size = 0
ObjectNames = Arr(0, "")
Pow10 = 0.0
PointPow10 = 0.0
PriceGrid = Arr(0, 0.0)
Price = Arr(0, 0.0)

def OnInit():
    global PointPow10, Pow10, middle, size
    size = _int(Total * 2)
    ArrayResize(ObjectNames, size)
    ArrayResize(PriceGrid, size)
    ArrayResize(Price, size)
    for count in range(0, size):
        ObjectNames[count] = SirName + ' PriceLine ' + _str(count)
    Pow10 = MathPow(10, Digits_)
    PointPow10 = Point() * Pow10
    middle = _idiv(size, 2) - 1
    for count in range(middle, size):
        PriceGrid[count] = PointPow10 * (count - middle)
    for count in range(middle - 1, 0 - 1, -1):
        PriceGrid[count] = (-PointPow10) * (middle - count)

def OnDeinit(reason):
    for count in range(0, size):
        ObjectDelete(0, ObjectNames[count])

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    res = PointPow10 * MathFloor(_fdiv(close[rates_total - 1], PointPow10))
    for count in range(0, size):
        Price[count] = res + PriceGrid[count]
    count = 0
    while count < size:
        SetHline(0, ObjectNames[count], 0, Price[count], Color_, Style_, Width_, ObjectNames[count] + DoubleToString(Price[count], Digits()))
        count += 1
    ChartRedraw(0)
    return rates_total

def CreateHline(chart_id, name, nwin, price, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, 0, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetHline(chart_id, name, nwin, price, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceGridIndicator(_MQL5Indicator):
    name = 'PriceGrid'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Digits_': 2,  # разряд сетки
        'Total': 20,  # количество блоков сетки сверху или снизу от цены
        'Style_': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=4),  # стиль линии уровня
        'Width_': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня
    }

