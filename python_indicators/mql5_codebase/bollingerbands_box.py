"""BollingerBands_Box — converted from MQL5: MQL5 Indicators/BollingerBands_Box/BollingerBands_Box.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'BollingerBands_Box', 'source': 'MQL5 Indicators/BollingerBands_Box/BollingerBands_Box.mq5', 'folder': 'BollingerBands_Box', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'BollingerBands_Box', 'label': 'Имя объекта', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16408, 'label': 'Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для расчета индикатора', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 20, 'label': 'Период для расчета средней линии', 'sinput': False}, {'mql': 'StdDeviation', 'py': 'StdDeviation', 'param': 'StdDeviation', 'type': 'double', 'default': 2.0001, 'label': 'Кол-во отклонений', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Цвет верхней ценовой метки', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 9470064, 'label': 'Цвет средней ценовой метки', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 255, 'label': 'Цвет нижней ценовой метки', 'sinput': False}, {'mql': 'BarsTotal', 'py': 'BarsTotal', 'param': 'BarsTotal', 'type': 'uint', 'default': 30, 'label': 'количество баров прямоугольников', 'sinput': False}, {'mql': 'RightTail', 'py': 'RightTail', 'param': 'RightTail', 'type': 'uint', 'default': 5, 'label': 'выступ прямоугольников за нулевой бар вправо в барах текущего графика', 'sinput': False}, {'mql': 'Color_Res', 'py': 'Color_Res', 'param': None, 'type': 'color', 'default': 16777117, 'label': 'Цвет верхней коробки', 'sinput': False}, {'mql': 'Color_Sup', 'py': 'Color_Sup', 'param': None, 'type': 'color', 'default': 16756991, 'label': 'Цвет нижней коробки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SirName = _input('SirName', 'BollingerBands_Box')  # Имя объекта
Timeframe = _input('Timeframe', PERIOD_D1)  # Таймфрейм индикатора для расчета индикатора
NumberofBar = _input('NumberofBar', 1)  # Номер бара для расчета индикатора
BBPeriod = _input('BBPeriod', 20)  # Период для расчета средней линии
StdDeviation = _input('StdDeviation', 2.0001)  # Кол-во отклонений
applied_price = _input('applied_price', PRICE_CLOSE)  # Тип цены
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Upper_color = _input('Upper_color', clrLimeGreen)  # Цвет верхней ценовой метки
Middle_color = _input('Middle_color', clrSlateGray)  # Цвет средней ценовой метки
Lower_color = _input('Lower_color', clrRed)  # Цвет нижней ценовой метки
BarsTotal = _input('BarsTotal', 30)  # количество баров прямоугольников
RightTail = _input('RightTail', 5)  # выступ прямоугольников за нулевой бар вправо в барах текущего графика
Color_Res = _input('Color_Res', 0xFFFF9D)  # Цвет верхней коробки
Color_Sup = _input('Color_Sup', 0xFFB0FF)  # Цвет нижней коробки
Ind_Handle = 0
UpBoxName = ""
DnBoxName = ""
upper_name = ""
middle_name = ""
lower_name = ""
SecondRightTail = 0
SecondLeftTail = 0

def OnInit():
    global DnBoxName, Ind_Handle, SecondRightTail, UpBoxName, lower_name, middle_name, upper_name
    Ind_Handle = iBands(Symbol(), Timeframe, BBPeriod, 0, StdDeviation, applied_price)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора BollingerBands')
        return INIT_FAILED
    SecondRightTail = RightTail * PeriodSeconds(PERIOD_CURRENT)
    upper_name = SirName + ' upper text lable'
    middle_name = SirName + ' middle text lable'
    lower_name = SirName + ' lower text lable'
    UpBoxName = SirName + '_Up'
    DnBoxName = SirName + '_Dn'
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'BollingerBands_Box')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, SirName, 0, -1)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), Timeframe):
        return prev_calculated
    Up = Arr(1, 0.0, dyn=False)
    Md = Arr(1, 0.0, dyn=False)
    Dn = Arr(1, 0.0, dyn=False)
    to_copy = 0
    ArraySetAsSeries(time, True)
    to_copy = 1
    if CopyBuffer(Ind_Handle, UPPER_BAND, NumberofBar, 1, Up) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, BASE_LINE, NumberofBar, 1, Md) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, LOWER_BAND, NumberofBar, 1, Dn) <= 0:
        return 0
    time0 = time[0] + SecondRightTail
    SetRectangle(0, UpBoxName, 0, time[BarsTotal - 1], Md[0], time0, Up[0], Color_Res, True, UpBoxName)
    SetRectangle(0, DnBoxName, 0, time[BarsTotal - 1], Md[0], time0, Dn[0], Color_Sup, True, DnBoxName)
    if ShowPrice:
        SetRightPrice(0, upper_name, 0, time0, Up[0], Upper_color)
        SetRightPrice(0, middle_name, 0, time0, Md[0], Middle_color)
        SetRightPrice(0, lower_name, 0, time0, Dn[0], Lower_color)
    ChartRedraw(0)
    return rates_total

def CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, background, text):
    ObjectCreate(chart_id, name, OBJ_RECTANGLE, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, background)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerBandsBox(_MQL5Indicator):
    name = 'BollingerBands_Box'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Таймфрейм индикатора для расчета индикатора
        'NumberofBar': 1,  # Номер бара для расчета индикатора
        'BBPeriod': 20,  # Период для расчета средней линии
        'StdDeviation': 2.0001,  # Кол-во отклонений
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'ShowPrice': True,  # показывать ценовые метки
        'BarsTotal': 30,  # количество баров прямоугольников
        'RightTail': 5,  # выступ прямоугольников за нулевой бар вправо в барах текущего графика
    }

