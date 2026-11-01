"""Float_Pivot_Digit_Box — converted from MQL5: MQL5 Indicators/Float_Pivot_Digit_Box/Float_Pivot_Digit_Box.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Float_Pivot_Digit_Box', 'source': 'MQL5 Indicators/Float_Pivot_Digit_Box/Float_Pivot_Digit_Box.mq5', 'folder': 'Float_Pivot_Digit_Box', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'Float_Pivot_Digit_Box', 'label': 'Имя объекта', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16408, 'label': 'Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для расчета индикатора', 'sinput': False}, {'mql': 'IPeriod', 'py': 'IPeriod', 'param': 'IPeriod', 'type': 'int', 'default': 100, 'label': 'Период поиска экстремумов', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 5, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'Цвет верхней ценовой метки', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет средней ценовой метки', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет нижней ценовой метки', 'sinput': False}, {'mql': 'BarsTotal', 'py': 'BarsTotal', 'param': 'BarsTotal', 'type': 'uint', 'default': 30, 'label': 'количество баров прямоугольников', 'sinput': False}, {'mql': 'RightTail', 'py': 'RightTail', 'param': 'RightTail', 'type': 'uint', 'default': 5, 'label': 'выступ прямоугольников за нулевой бар вправо в барах текущего графика', 'sinput': False}, {'mql': 'Color_Res', 'py': 'Color_Res', 'param': None, 'type': 'color', 'default': 13303754, 'label': 'Цвет верхней коробки', 'sinput': False}, {'mql': 'Color_Sup', 'py': 'Color_Sup', 'param': None, 'type': 'color', 'default': 16756991, 'label': 'Цвет нижней коробки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_APPLIED_PRICE_
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
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
SirName = _input('SirName', 'Float_Pivot_Digit_Box')  # Имя объекта
Timeframe = _input('Timeframe', PERIOD_D1)  # Таймфрейм индикатора для расчета индикатора
NumberofBar = _input('NumberofBar', 1)  # Номер бара для расчета индикатора
IPeriod = _input('IPeriod', 100)  # Период поиска экстремумов
IPC = _input('IPC', PRICE_MEDIAN_)  # ценовая константа
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Upper_color = _input('Upper_color', clrTeal)  # Цвет верхней ценовой метки
Middle_color = _input('Middle_color', clrBlue)  # Цвет средней ценовой метки
Lower_color = _input('Lower_color', clrMagenta)  # Цвет нижней ценовой метки
BarsTotal = _input('BarsTotal', 30)  # количество баров прямоугольников
RightTail = _input('RightTail', 5)  # выступ прямоугольников за нулевой бар вправо в барах текущего графика
Color_Res = _input('Color_Res', 0xCAFFCA)  # Цвет верхней коробки
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
    Ind_Handle = iCustom(Symbol(), Timeframe, 'Float_Pivot_Digit', SirName, IPeriod, IPC, 0, Digit, False, Upper_color, Middle_color, Lower_color)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Float_Pivot_Digit')
        return INIT_FAILED
    SecondRightTail = RightTail * PeriodSeconds(PERIOD_CURRENT)
    upper_name = SirName + ' upper text lable'
    middle_name = SirName + ' middle text lable'
    lower_name = SirName + ' lower text lable'
    UpBoxName = SirName + '_Up'
    DnBoxName = SirName + '_Dn'
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Float_Pivot_Digit_Box')
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
    if CopyBuffer(Ind_Handle, 2, NumberofBar, 1, Up) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 3, NumberofBar, 1, Md) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 4, NumberofBar, 1, Dn) <= 0:
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


class FloatPivotDigitBox(_MQL5Indicator):
    name = 'Float_Pivot_Digit_Box'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Таймфрейм индикатора для расчета индикатора
        'NumberofBar': 1,  # Номер бара для расчета индикатора
        'IPeriod': 100,  # Период поиска экстремумов
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW0_2', 12: 'Demark Price'}, default=5),  # ценовая константа
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовые метки
        'BarsTotal': 30,  # количество баров прямоугольников
        'RightTail': 5,  # выступ прямоугольников за нулевой бар вправо в барах текущего графика
    }

