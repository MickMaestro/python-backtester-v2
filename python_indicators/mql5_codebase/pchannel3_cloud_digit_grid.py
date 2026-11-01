"""pchannel3_cloud_digit_grid — converted from MQL5: MQL5 Indicators/PChannel3_Cloud_Digit_Grid/pchannel3_cloud_digit_grid.mq5

Copyright: Copyright © 2005, Xaoc; Link: http://forex.xcd.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Xaoc', 'link': 'http://forex.xcd.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 7}, 'colors': {1: [10025880], 2: [8421376], 3: [16711680], 4: [255], 5: [13353215]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper Cloud', 2: 'TOPBAND', 3: 'MIDBAND', 4: 'BOTBAND', 5: 'Upper Cloud'}, 'levels': [], 'description': [], 'name': 'pchannel3_cloud_digit_grid', 'source': 'MQL5 Indicators/PChannel3_Cloud_Digit_Grid/pchannel3_cloud_digit_grid.mq5', 'folder': 'PChannel3_Cloud_Digit_Grid', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'PChannel3_Cloud_Digit_Grid', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'PCPeriod', 'py': 'PCPeriod', 'param': 'PCPeriod', 'type': 'uint', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'RoundPrice', 'py': 'RoundPrice', 'param': 'RoundPrice', 'type': 'bool', 'default': True, 'label': 'округлять цены', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 7451452, 'label': '', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'Total', 'py': 'Total', 'param': 'Total', 'type': 'uint', 'default': 200, 'label': 'количество блоков сетки сверху или снизу от цены', 'sinput': False}, {'mql': 'Color_A', 'py': 'Color_A', 'param': None, 'type': 'color', 'default': 13458026, 'label': 'цвет уровня 1', 'sinput': False}, {'mql': 'Style_A', 'py': 'Style_A', 'param': 'Style_A', 'type': 'int', 'default': 4, 'label': 'стиль линии уровня 1', 'sinput': False}, {'mql': 'Width_A', 'py': 'Width_A', 'param': 'Width_A', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 1', 'sinput': False}, {'mql': 'Color_B', 'py': 'Color_B', 'param': None, 'type': 'color', 'default': 36095, 'label': 'цвет уровня 2', 'sinput': False}, {'mql': 'Style_B', 'py': 'Style_B', 'param': 'Style_B', 'type': 'int', 'default': 1, 'label': 'стиль линии уровня 2', 'sinput': False}, {'mql': 'Width_B', 'py': 'Width_B', 'param': 'Width_B', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 2', 'sinput': False}, {'mql': 'Color_C', 'py': 'Color_C', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет уровня 3', 'sinput': False}, {'mql': 'Style_C', 'py': 'Style_C', 'param': 'Style_C', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 3', 'sinput': False}, {'mql': 'Width_C', 'py': 'Width_C', 'param': 'Width_C', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 3', 'sinput': False}, {'mql': 'Color_D', 'py': 'Color_D', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет уровня 4', 'sinput': False}, {'mql': 'Style_D', 'py': 'Style_D', 'param': 'Style_D', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 4', 'sinput': False}, {'mql': 'Width_D', 'py': 'Width_D', 'param': 'Width_D', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 4', 'sinput': False}, {'mql': 'Color_E', 'py': 'Color_E', 'param': None, 'type': 'color', 'default': 65280, 'label': 'цвет уровня 5', 'sinput': False}, {'mql': 'Style_E', 'py': 'Style_E', 'param': 'Style_E', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 5', 'sinput': False}, {'mql': 'Width_E', 'py': 'Width_E', 'param': 'Width_E', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 5', 'sinput': False}, {'mql': 'Fontsizex', 'py': 'Fontsizex', 'param': 'Fontsizex', 'type': 'uint', 'default': 2, 'label': 'размер ценовых меток', 'sinput': False}, {'mql': 'ShowLineInfo', 'py': 'ShowLineInfo', 'param': 'ShowLineInfo', 'type': 'bool', 'default': True, 'label': 'отображение значения уровня на ценовом графике', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
SirName = _input('SirName', 'PChannel3_Cloud_Digit_Grid')  # Первая часть имени графических объектов
PCPeriod = _input('PCPeriod', 55)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Digit = _input('Digit', 2)  # количество разрядов округления
RoundPrice = _input('RoundPrice', True)  # округлять цены
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Middle_color = _input('Middle_color', clrBlue)
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
Fontsizex = _input('Fontsizex', 2)  # размер ценовых меток
ShowLineInfo = _input('ShowLineInfo', True)  # отображение значения уровня на ценовом графике
min_rates_total = 0
ExtUp1Buffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtDn1Buffer = Arr(0, 0.0)
ExtDn2Buffer = Arr(0, 0.0)
upper_name = ""
middle_name = ""
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
    global Count, Normalize, PointPow10, PointPow100, PointPow1000, PointPow10000, PointPow100000, lower_name, middle, middle_name, min_rates_total, sizex, upper_name
    min_rates_total = _int(PCPeriod)
    upper_name = SirName + ' upper text lable'
    middle_name = SirName + ' middle text lable'
    lower_name = SirName + ' lower text lable'
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
    SetIndexBuffer(0, ExtUp1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtUp1Buffer, True)
    ArraySetAsSeries(ExtUp2Buffer, True)
    SetIndexBuffer(2, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(3, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtBBuffer, True)
    SetIndexBuffer(4, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtCBuffer, True)
    SetIndexBuffer(5, ExtDn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtDn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtDn1Buffer, True)
    ArraySetAsSeries(ExtDn2Buffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PChannel3_Cloud_Digit_Grid(' + _str(PCPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    global Count
    ObjectDelete(0, upper_name)
    ObjectDelete(0, middle_name)
    ObjectDelete(0, lower_name)
    Count = 0
    while Count < sizex:
        ObjectDelete(0, ObjectNames[Count])
        Count += 1
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global Count
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(Close, False)
    ArraySetAsSeries(Time, False)
    res = NormalizeDouble(PointPow10 * MathCeil(_fdiv(Close[rates_total - 1], PointPow10)), Normalize)
    if prev_calculated != rates_total:
        Count = 0
        while Count < sizex:
            ObjectDelete(0, ObjectNames[Count])
            Count += 1
    Count = 0
    while Count < sizex:
        Price[Count] = NormalizeDouble(res + PriceGrid[Count], Normalize)
        Count += 1
    Time0 = Time[rates_total - 1] + (PeriodSeconds() * Shift)
    TimeX = Time[0]
    Count = 0
    while Count < sizex:
        info = ''
        if ShowLineInfo:
            info = ObjectNames[Count] + ' ' + DoubleToString(Price[Count], Normalize)
        if not NormalizeDouble(Price[Count] - (PointPow100000 * MathCeil(_fdiv(Price[Count], PointPow100000))), Normalize):
            SetTline(0, ObjectNames[Count], 0, TimeX, Price[Count], Time0, Price[Count], Color_E, Style_E, Width_E, info)
        elif not NormalizeDouble(Price[Count] - (PointPow10000 * MathCeil(_fdiv(Price[Count], PointPow10000))), Normalize):
            SetTline(0, ObjectNames[Count], 0, TimeX, Price[Count], Time0, Price[Count], Color_D, Style_D, Width_D, info)
        elif not NormalizeDouble(Price[Count] - (PointPow1000 * MathCeil(_fdiv(Price[Count], PointPow1000))), Normalize):
            SetTline(0, ObjectNames[Count], 0, TimeX, Price[Count], Time0, Price[Count], Color_C, Style_C, Width_C, info)
        elif not NormalizeDouble(Price[Count] - (PointPow100 * MathCeil(_fdiv(Price[Count], PointPow100))), Normalize):
            SetTline(0, ObjectNames[Count], 0, TimeX, Price[Count], Time0, Price[Count], Color_B, Style_B, Width_B, info)
        else:
            SetTline(0, ObjectNames[Count], 0, TimeX, Price[Count], Time0, Price[Count], Color_A, Style_A, Width_A, info)
        Count += 1
    ArraySetAsSeries(Close, False)
    ArraySetAsSeries(Time, False)
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Time, True)
    for bar in range(limit, 0 - 1, -1):
        ExtABuffer[bar] = High[ArrayMaximum(High, bar, PCPeriod)]
        ExtCBuffer[bar] = Low[ArrayMinimum(Low, bar, PCPeriod)]
        ExtBBuffer[bar] = (ExtABuffer[bar] + ExtCBuffer[bar]) / 2.0
        if RoundPrice:
            ExtBBuffer[bar] = PointPow10 * MathRound(_fdiv(ExtBBuffer[bar], PointPow10))
            ExtABuffer[bar] = PointPow10 * MathCeil(_fdiv(ExtABuffer[bar], PointPow10))
            ExtCBuffer[bar] = PointPow10 * MathFloor(_fdiv(ExtCBuffer[bar], PointPow10))
        ExtUp1Buffer[bar] = ExtABuffer[bar]
        ExtUp2Buffer[bar] = ExtBBuffer[bar]
        ExtDn1Buffer[bar] = ExtBBuffer[bar]
        ExtDn2Buffer[bar] = ExtCBuffer[bar]
    if ShowPrice:
        bar0 = 0
        Time0 = Time[bar0] + (Shift * PeriodSeconds())
        SetRightPrice(0, middle_name, 0, Time0, ExtBBuffer[bar0], Middle_color, 'Georgia')
        SetRightPrice(0, upper_name, 0, Time0, ExtABuffer[bar0], Upper_color, 'Georgia')
        SetRightPrice(0, lower_name, 0, Time0, ExtCBuffer[bar0], Lower_color, 'Georgia')
    ChartRedraw(0)
    return rates_total

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

def CreateRightPrice(chart_id, name, nwin, time, price, Color, Font):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color, Font):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color, Font)
    else:
        ObjectMove(chart_id, name, 0, time, price)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pchannel3CloudDigitGrid(_MQL5Indicator):
    name = 'pchannel3_cloud_digit_grid'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PCPeriod': 55,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'Digit': 2,  # количество разрядов округления
        'RoundPrice': True,  # округлять цены
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
        'Fontsizex': 2,  # размер ценовых меток
        'ShowLineInfo': True,  # отображение значения уровня на ценовом графике
    }

