"""XEnvelopes_Digit_Grid — converted from MQL5: MQL5 Indicators/XEnvelopes_Digit_Grid/XEnvelopes_Digit_Grid.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16443110], 2: [3329330], 3: [9639167]}, 'widths': {2: 2, 3: 2}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'XEnvelopes Cloud', 2: 'Upper XEnvelopes', 3: 'Lower XEnvelopes'}, 'levels': [], 'description': [''], 'name': 'XEnvelopes_Digit_Grid', 'source': 'MQL5 Indicators/XEnvelopes_Digit_Grid/XEnvelopes_Digit_Grid.mq5', 'folder': 'XEnvelopes_Digit_Grid', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'XEnvelopes_Digit_Grid', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 0.1, 'label': 'Девиация', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 7451452, 'label': '', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'Total', 'py': 'Total', 'param': 'Total', 'type': 'uint', 'default': 200, 'label': 'количество блоков сетки сверху или снизу от цены', 'sinput': False}, {'mql': 'Color_A', 'py': 'Color_A', 'param': None, 'type': 'color', 'default': 13458026, 'label': 'цвет уровня 1', 'sinput': False}, {'mql': 'Style_A', 'py': 'Style_A', 'param': 'Style_A', 'type': 'int', 'default': 4, 'label': 'стиль линии уровня 1', 'sinput': False}, {'mql': 'Width_A', 'py': 'Width_A', 'param': 'Width_A', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 1', 'sinput': False}, {'mql': 'Color_B', 'py': 'Color_B', 'param': None, 'type': 'color', 'default': 36095, 'label': 'цвет уровня 2', 'sinput': False}, {'mql': 'Style_B', 'py': 'Style_B', 'param': 'Style_B', 'type': 'int', 'default': 1, 'label': 'стиль линии уровня 2', 'sinput': False}, {'mql': 'Width_B', 'py': 'Width_B', 'param': 'Width_B', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 2', 'sinput': False}, {'mql': 'Color_C', 'py': 'Color_C', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет уровня 3', 'sinput': False}, {'mql': 'Style_C', 'py': 'Style_C', 'param': 'Style_C', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 3', 'sinput': False}, {'mql': 'Width_C', 'py': 'Width_C', 'param': 'Width_C', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 3', 'sinput': False}, {'mql': 'Color_D', 'py': 'Color_D', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет уровня 4', 'sinput': False}, {'mql': 'Style_D', 'py': 'Style_D', 'param': 'Style_D', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 4', 'sinput': False}, {'mql': 'Width_D', 'py': 'Width_D', 'param': 'Width_D', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 4', 'sinput': False}, {'mql': 'Color_E', 'py': 'Color_E', 'param': None, 'type': 'color', 'default': 65280, 'label': 'цвет уровня 5', 'sinput': False}, {'mql': 'Style_E', 'py': 'Style_E', 'param': 'Style_E', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 5', 'sinput': False}, {'mql': 'Width_E', 'py': 'Width_E', 'param': 'Width_E', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 5', 'sinput': False}, {'mql': 'ShowLineInfo', 'py': 'ShowLineInfo', 'param': 'ShowLineInfo', 'type': 'bool', 'default': True, 'label': 'отображение значения уровня на ценовом графике', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

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
SirName = _input('SirName', 'XEnvelopes_Digit_Grid')  # Первая часть имени графических объектов
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 12)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Deviation = _input('Deviation', 0.1)  # Девиация
Digit = _input('Digit', 2)  # количество разрядов округления
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Upper_color = _input('Upper_color', clrMediumSeaGreen)
Lower_color = _input('Lower_color', clrRed)
Total = _input('Total', 200)  # количество блоков сетки сверху или снизу от цены
Color_A = _input('Color_A', clrSlateBlue)  # цвет уровня 1
Style_A = _input('Style_A', DASHDOTDOT_)  # стиль линии уровня 1
Width_A = _input('Width_A', Width_1)  # толщина линии уровня 1
Color_B = _input('Color_B', clrDarkOrange)  # цвет уровня 2
Style_B = _input('Style_B', DASH_)  # стиль линии уровня 2
Width_B = _input('Width_B', Width_1)  # толщина линии уровня 2
Color_C = _input('Color_C', clrMagenta)  # цвет уровня 3
Style_C = _input('Style_C', SOLID_)  # стиль линии уровня 3
Width_C = _input('Width_C', Width_1)  # толщина линии уровня 3
Color_D = _input('Color_D', clrRed)  # цвет уровня 4
Style_D = _input('Style_D', SOLID_)  # стиль линии уровня 4
Width_D = _input('Width_D', Width_1)  # толщина линии уровня 4
Color_E = _input('Color_E', clrLime)  # цвет уровня 5
Style_E = _input('Style_E', SOLID_)  # стиль линии уровня 5
Width_E = _input('Width_E', Width_1)  # толщина линии уровня 5
ShowLineInfo = _input('ShowLineInfo', True)  # отображение значения уровня на ценовом графике
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpLineBuffer = Arr(0, 0.0)
DnLineBuffer = Arr(0, 0.0)
dPriceShift = 0.0
UpKdev = 0.0
DnKdev = 0.0
min_rates_total = 0
upper_name = ""
lower_name = ""
clr = 0
Style = 0
Width = 0
ShowPriceLable = False
middle = 0
sizex = 0
Normalize = 0
Count = 0
ObjectNames = Arr(0, "")
PointPow10 = 0.0
PointPow100 = 0.0
PointPow1000 = 0.0
PointPow10000 = 0.0
PointPow100000 = 0.0
PriceGrid = Arr(0, 0.0)
Price = Arr(0, 0.0)

def OnInit():
    global Count, DnKdev, Normalize, PointPow10, PointPow100, PointPow1000, PointPow10000, PointPow100000, UpKdev, dPriceShift, lower_name, middle, min_rates_total, sizex, upper_name
    min_rates_total = XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    UpKdev = 1 + (Deviation / 100.0)
    DnKdev = 1 - (Deviation / 100.0)
    PointPow10 = Point() * MathPow(10, Digit)
    upper_name = 'XEnvelopes upper text lable'
    lower_name = 'XEnvelopes lower text lable'
    sizex = _int(Total * 2)
    ArrayResize(ObjectNames, sizex)
    ArrayResize(PriceGrid, sizex)
    ArrayResize(Price, sizex)
    Count = 0
    while Count < sizex:
        ObjectNames[Count] = SirName + ' PriceLine ' + _str(Count)
        Count += 1
    PointPow10 = Point() * MathPow(10, Digit)
    PointPow100 = PointPow10 * 10
    PointPow1000 = PointPow10 * 100
    PointPow10000 = PointPow10 * 1000
    PointPow100000 = PointPow10 * 10000
    middle = _idiv(sizex, 2) - 1
    Normalize = _int(Digits() - Digit)
    Count = middle
    while Count < sizex:
        PriceGrid[Count] = NormalizeDouble(PointPow10 * (Count - middle), Normalize)
        Count += 1
    Count = middle - 1
    while Count >= 0:
        PriceGrid[Count] = -NormalizeDouble(PointPow10 * (middle - Count), Normalize)
        Count -= 1
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, UpLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DnLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Env(' + _str(XLength) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'Env(' + _str(XLength) + ')Cloud')
    PlotIndexSetString(1, PLOT_LABEL, 'Env(' + _str(XLength) + ')Upper')
    PlotIndexSetString(2, PLOT_LABEL, 'Env(' + _str(XLength) + ')Lower')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnDeinit(reason):
    global Count
    ObjectDelete(0, upper_name)
    ObjectDelete(0, lower_name)
    Count = 0
    while Count < sizex:
        ObjectDelete(0, ObjectNames[Count])
        Count += 1
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Count
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(close, False)
    ArraySetAsSeries(time, False)
    res = NormalizeDouble(PointPow10 * MathCeil(_fdiv(close[rates_total - 1], PointPow10)), Normalize)
    if prev_calculated != rates_total:
        Count = 0
        while Count < sizex:
            ObjectDelete(0, ObjectNames[Count])
            Count += 1
    Count = 0
    while Count < sizex:
        Price[Count] = NormalizeDouble(res + PriceGrid[Count], Normalize)
        Count += 1
    time0 = time[rates_total - 1] + (PeriodSeconds() * Shift)
    timeX = time[0]
    Count = 0
    while Count < sizex:
        info = ''
        if ShowLineInfo:
            info = ObjectNames[Count] + ' ' + DoubleToString(Price[Count], Normalize)
        if not NormalizeDouble(Price[Count] - (PointPow100000 * MathCeil(_fdiv(Price[Count], PointPow100000))), Normalize):
            SetTline(0, ObjectNames[Count], 0, timeX, Price[Count], time0, Price[Count], Color_E, Style_E, Width_E, info)
        elif not NormalizeDouble(Price[Count] - (PointPow10000 * MathCeil(_fdiv(Price[Count], PointPow10000))), Normalize):
            SetTline(0, ObjectNames[Count], 0, timeX, Price[Count], time0, Price[Count], Color_D, Style_D, Width_D, info)
        elif not NormalizeDouble(Price[Count] - (PointPow1000 * MathCeil(_fdiv(Price[Count], PointPow1000))), Normalize):
            SetTline(0, ObjectNames[Count], 0, timeX, Price[Count], time0, Price[Count], Color_C, Style_C, Width_C, info)
        elif not NormalizeDouble(Price[Count] - (PointPow100 * MathCeil(_fdiv(Price[Count], PointPow100))), Normalize):
            SetTline(0, ObjectNames[Count], 0, timeX, Price[Count], time0, Price[Count], Color_B, Style_B, Width_B, info)
        else:
            SetTline(0, ObjectNames[Count], 0, timeX, Price[Count], time0, Price[Count], Color_A, Style_A, Width_A, info)
        Count += 1
    ArraySetAsSeries(close, False)
    ArraySetAsSeries(time, False)
    price = 0.0
    xma = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, False)
        UpLineBuffer[bar] = (PointPow10 * MathCeil(_fdiv(UpKdev * xma, PointPow10))) + dPriceShift
        UpBuffer[bar] = UpLineBuffer[bar]
        DnLineBuffer[bar] = (PointPow10 * MathFloor(_fdiv(DnKdev * xma, PointPow10))) + dPriceShift
        DnBuffer[bar] = DnLineBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (Shift * PeriodSeconds())
        SetRightPrice(0, upper_name, 0, time0, UpBuffer[bar0], Upper_color)
        SetRightPrice(0, lower_name, 0, time0, DnBuffer[bar0], Lower_color)
    ChartRedraw(0)
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color)
    else:
        ObjectMove(chart_id, name, 0, time, price)

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, False)
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

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XEnvelopesDigitGrid(_MQL5Indicator):
    name = 'XEnvelopes_Digit_Grid'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 12,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Deviation': 0.1,  # Девиация
        'Digit': 2,  # количество разрядов округления
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'ShowPrice': True,  # показывать ценовые метки
        'Total': 200,  # количество блоков сетки сверху или снизу от цены
        'Style_A': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=4),  # стиль линии уровня 1
        'Width_A': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня 1
        'Style_B': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=1),  # стиль линии уровня 2
        'Width_B': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня 2
        'Style_C': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль линии уровня 3
        'Width_C': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня 3
        'Style_D': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль линии уровня 4
        'Width_D': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня 4
        'Style_E': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль линии уровня 5
        'Width_E': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии уровня 5
        'ShowLineInfo': True,  # отображение значения уровня на ценовом графике
    }

