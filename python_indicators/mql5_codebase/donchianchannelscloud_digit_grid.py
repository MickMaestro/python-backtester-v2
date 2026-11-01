"""DonchianChannelsCloud_Digit_Grid — converted from MQL5: MQL5 Indicators/DonchianChannelsCloud_Digit_Grid/DonchianChannelsCloud_Digit_Grid.mq5

Copyright: Copyright © 2005, Luis Guilherme Damiani; Link: http://www.damianifx.com.br; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Luis Guilherme Damiani', 'link': 'http://www.damianifx.com.br', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 7}, 'colors': {1: [16436871], 2: [16748574], 3: [13828244], 4: [16711935], 5: [15631086]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper Cloud', 2: 'Upper Donchian', 3: 'Middle Donchian', 4: 'Lower Donchian', 5: 'Lower Cloud'}, 'levels': [], 'description': [], 'name': 'DonchianChannelsCloud_Digit_Grid', 'source': 'MQL5 Indicators/DonchianChannelsCloud_Digit_Grid/DonchianChannelsCloud_Digit_Grid.mq5', 'folder': 'DonchianChannelsCloud_Digit_Grid', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'DonchianChannelsCloud_Digit_Grid', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'DonchianPeriod', 'py': 'DonchianPeriod', 'param': 'DonchianPeriod', 'type': 'int', 'default': 20, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'Extremes', 'py': 'Extremes', 'param': 'Extremes', 'type': 'int', 'default': 0, 'label': 'Тип экстремумов', 'sinput': False}, {'mql': 'Margins', 'py': 'Margins', 'param': 'Margins', 'type': 'int', 'default': -2, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'RoundPrice', 'py': 'RoundPrice', 'param': 'RoundPrice', 'type': 'bool', 'default': True, 'label': 'округлять цены', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 13828244, 'label': '', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}, {'mql': 'Total', 'py': 'Total', 'param': 'Total', 'type': 'uint', 'default': 200, 'label': 'количество блоков сетки сверху или снизу от цены', 'sinput': False}, {'mql': 'Color_A', 'py': 'Color_A', 'param': None, 'type': 'color', 'default': 13458026, 'label': 'цвет уровня 1', 'sinput': False}, {'mql': 'Style_A', 'py': 'Style_A', 'param': 'Style_A', 'type': 'int', 'default': 4, 'label': 'стиль линии уровня 1', 'sinput': False}, {'mql': 'Width_A', 'py': 'Width_A', 'param': 'Width_A', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 1', 'sinput': False}, {'mql': 'Color_B', 'py': 'Color_B', 'param': None, 'type': 'color', 'default': 36095, 'label': 'цвет уровня 2', 'sinput': False}, {'mql': 'Style_B', 'py': 'Style_B', 'param': 'Style_B', 'type': 'int', 'default': 1, 'label': 'стиль линии уровня 2', 'sinput': False}, {'mql': 'Width_B', 'py': 'Width_B', 'param': 'Width_B', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 2', 'sinput': False}, {'mql': 'Color_C', 'py': 'Color_C', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет уровня 3', 'sinput': False}, {'mql': 'Style_C', 'py': 'Style_C', 'param': 'Style_C', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 3', 'sinput': False}, {'mql': 'Width_C', 'py': 'Width_C', 'param': 'Width_C', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 3', 'sinput': False}, {'mql': 'Color_D', 'py': 'Color_D', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет уровня 4', 'sinput': False}, {'mql': 'Style_D', 'py': 'Style_D', 'param': 'Style_D', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 4', 'sinput': False}, {'mql': 'Width_D', 'py': 'Width_D', 'param': 'Width_D', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 4', 'sinput': False}, {'mql': 'Color_E', 'py': 'Color_E', 'param': None, 'type': 'color', 'default': 65280, 'label': 'цвет уровня 5', 'sinput': False}, {'mql': 'Style_E', 'py': 'Style_E', 'param': 'Style_E', 'type': 'int', 'default': 0, 'label': 'стиль линии уровня 5', 'sinput': False}, {'mql': 'Width_E', 'py': 'Width_E', 'param': 'Width_E', 'type': 'int', 'default': 1, 'label': 'толщина линии уровня 5', 'sinput': False}, {'mql': 'Fontsizex', 'py': 'Fontsizex', 'param': 'Fontsizex', 'type': 'uint', 'default': 2, 'label': 'размер ценовых меток', 'sinput': False}, {'mql': 'ShowLineInfo', 'py': 'ShowLineInfo', 'param': 'ShowLineInfo', 'type': 'bool', 'default': True, 'label': 'отображение значения уровня на ценовом графике', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum Applied_Extrem
HIGH_LOW = 0
HIGH_LOW_OPEN = 1
HIGH_LOW_CLOSE = 2
OPEN_HIGH_LOW = 3
CLOSE_HIGH_LOW = 4
_enum('Applied_Extrem', {0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'})

# ---- inputs and global variables
SirName = _input('SirName', 'DonchianChannelsCloud_Digit_Grid')  # Первая часть имени графических объектов
DonchianPeriod = _input('DonchianPeriod', 20)  # Период усреднения
Extremes = _input('Extremes', HIGH_LOW)  # Тип экстремумов
Margins = _input('Margins', -2)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Digit = _input('Digit', 2)  # количество разрядов округления
RoundPrice = _input('RoundPrice', True)  # округлять цены
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Middle_color = _input('Middle_color', clrDarkViolet)
Upper_color = _input('Upper_color', clrBlue)
Lower_color = _input('Lower_color', clrMagenta)
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
ExtUp1Buffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtDn1Buffer = Arr(0, 0.0)
ExtDn2Buffer = Arr(0, 0.0)
min_rates_total = 0
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

def iHighest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Неверное значение в функции iHighest, startPos = ', startPos)
        return 0
    if (startPos - count) < 0:
        count = startPos
    max_ = array[startPos]
    for i in range(startPos, startPos - count, -1):
        if array[i] > max_:
            index = i
            max_ = array[i]
    return index

def iLowest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Неверное значение в функции iLowest, startPos = ', startPos)
        return 0
    if (startPos - count) < 0:
        count = startPos
    min_ = array[startPos]
    for i in range(startPos, startPos - count, -1):
        if array[i] < min_:
            index = i
            min_ = array[i]
    return index

def OnInit():
    global Count, Normalize, PointPow10, PointPow100, PointPow1000, PointPow10000, PointPow100000, lower_name, middle, middle_name, min_rates_total, sizex, upper_name
    min_rates_total = DonchianPeriod + 1
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
    SetIndexBuffer(2, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    SetIndexBuffer(3, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    SetIndexBuffer(4, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    SetIndexBuffer(5, ExtDn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtDn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'DonchianChannelsCloud_Digit_Grid( DonchianPeriod = ', DonchianPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

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
    smin = 0.0
    smax = 0.0
    SsMax = 0.0
    SsMin = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - 1
    ArraySetAsSeries(close, False)
    ArraySetAsSeries(time, False)
    bar = first
    for bar in range(bar, rates_total):
        _sw1 = Extremes
        if _sw1 == HIGH_LOW:
            SsMax = high[iHighest_u(high, DonchianPeriod, bar)]
            SsMin = low[iLowest_u(low, DonchianPeriod, bar)]
        elif _sw1 == HIGH_LOW_OPEN:
            SsMax = (open[iHighest_u(open, DonchianPeriod, bar)] + high[iHighest_u(high, DonchianPeriod, bar)]) / 2
            SsMin = (open[iLowest_u(open, DonchianPeriod, bar)] + low[iLowest_u(high, DonchianPeriod, bar)]) / 2
        elif _sw1 == HIGH_LOW_CLOSE:
            SsMax = (close[iHighest_u(close, DonchianPeriod, bar)] + high[iHighest_u(high, DonchianPeriod, bar)]) / 2
            SsMin = (close[iLowest_u(close, DonchianPeriod, bar)] + low[iLowest_u(high, DonchianPeriod, bar)]) / 2
        elif _sw1 == OPEN_HIGH_LOW:
            SsMax = open[iHighest_u(open, DonchianPeriod, bar)]
            SsMin = open[iLowest_u(open, DonchianPeriod, bar)]
        elif _sw1 == CLOSE_HIGH_LOW:
            SsMax = close[iHighest_u(close, DonchianPeriod, bar)]
            SsMin = close[iLowest_u(close, DonchianPeriod, bar)]
        smin = SsMin + (((SsMax - SsMin) * Margins) / 100)
        smax = SsMax - (((SsMax - SsMin) * Margins) / 100)
        ExtABuffer[bar] = smax
        ExtCBuffer[bar] = smin
        ExtBBuffer[bar] = (smax + smin) / 2.0
        if RoundPrice:
            ExtBBuffer[bar] = PointPow10 * MathRound(_fdiv(ExtBBuffer[bar], PointPow10))
            ExtABuffer[bar] = PointPow10 * MathCeil(_fdiv(ExtABuffer[bar], PointPow10))
            ExtCBuffer[bar] = PointPow10 * MathFloor(_fdiv(ExtCBuffer[bar], PointPow10))
        ExtUp1Buffer[bar] = ExtABuffer[bar]
        ExtUp2Buffer[bar] = ExtBBuffer[bar]
        ExtDn1Buffer[bar] = ExtBBuffer[bar]
        ExtDn2Buffer[bar] = ExtCBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (Shift * PeriodSeconds())
        SetRightPrice(0, middle_name, 0, time0, ExtBBuffer[bar0], Middle_color, 'Georgia')
        SetRightPrice(0, upper_name, 0, time0, ExtABuffer[bar0], Upper_color, 'Georgia')
        SetRightPrice(0, lower_name, 0, time0, ExtCBuffer[bar0], Lower_color, 'Georgia')
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


class DonchianChannelsCloudDigitGrid(_MQL5Indicator):
    name = 'DonchianChannelsCloud_Digit_Grid'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DonchianPeriod': 20,  # Период усреднения
        'Extremes': _Choice({0: 'HIGH_LOW', 1: 'HIGH_LOW_OPEN', 2: 'HIGH_LOW_CLOSE', 3: 'OPEN_HIGH_LOW', 4: 'CLOSE_HIGH_LOW'}, default=0),  # Тип экстремумов
        'Margins': -2,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
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

