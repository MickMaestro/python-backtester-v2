"""ParTest — converted from MQL5: MQL5 Indicators/ParTest/ParTest.mq5

Copyright: Copyright © 2005, Danilla; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Danilla', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ParTest', 'source': 'MQL5 Indicators/ParTest/ParTest.mq5', 'folder': 'ParTest', 'inputs': [{'mql': 'IndicatorSirname', 'py': 'IndicatorSirname', 'param': None, 'type': 'string', 'default': 'Paramon', 'label': '', 'sinput': False}, {'mql': 'Up_Color', 'py': 'Up_Color', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'цвет верхнего уровня', 'sinput': False}, {'mql': 'UpFill_Color', 'py': 'UpFill_Color', 'param': None, 'type': 'color', 'default': 10025880, 'label': 'цвет заливки верхнего уровня', 'sinput': False}, {'mql': 'Md_Color', 'py': 'Md_Color', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет среднего уровня', 'sinput': False}, {'mql': 'Dn_Color', 'py': 'Dn_Color', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет  нижнего уровня', 'sinput': False}, {'mql': 'DnFill_Color', 'py': 'DnFill_Color', 'param': None, 'type': 'color', 'default': 14524637, 'label': 'цвет заливки нижнего уровня', 'sinput': False}, {'mql': 'DayColor', 'py': 'DayColor', 'param': None, 'type': 'color', 'default': 14822282, 'label': 'цвет уровня начала дня', 'sinput': False}, {'mql': 'Up_Style', 'py': 'Up_Style', 'param': 'Up_Style', 'type': 'int', 'default': 0, 'label': 'стиль вернего уровня', 'sinput': False}, {'mql': 'Md_Style', 'py': 'Md_Style', 'param': 'Md_Style', 'type': 'int', 'default': 4, 'label': 'стиль среднего уровня', 'sinput': False}, {'mql': 'Dn_Style', 'py': 'Dn_Style', 'param': 'Dn_Style', 'type': 'int', 'default': 0, 'label': 'стиль нижнего уровня', 'sinput': False}, {'mql': 'DayStyle', 'py': 'DayStyle', 'param': 'DayStyle', 'type': 'int', 'default': 0, 'label': 'стиль уровня начала дня', 'sinput': False}, {'mql': 'Up_Width', 'py': 'Up_Width', 'param': 'Up_Width', 'type': 'int', 'default': 3, 'label': 'толщина вернего уровня', 'sinput': False}, {'mql': 'Md_Width', 'py': 'Md_Width', 'param': 'Md_Width', 'type': 'int', 'default': 1, 'label': 'толщина среднего уровня', 'sinput': False}, {'mql': 'Dn_Width', 'py': 'Dn_Width', 'param': 'Dn_Width', 'type': 'int', 'default': 3, 'label': 'толщина нижнего уровня', 'sinput': False}, {'mql': 'DayWidth', 'py': 'DayWidth', 'param': 'DayWidth', 'type': 'int', 'default': 3, 'label': 'толщина уровня начала дня', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
IndicatorSirname = _input('IndicatorSirname', 'Paramon')
Up_Color = _input('Up_Color', clrMediumSeaGreen)  # цвет верхнего уровня
UpFill_Color = _input('UpFill_Color', clrPaleGreen)  # цвет заливки верхнего уровня
Md_Color = _input('Md_Color', clrBlue)  # цвет среднего уровня
Dn_Color = _input('Dn_Color', clrMagenta)  # цвет  нижнего уровня
DnFill_Color = _input('DnFill_Color', clrPlum)  # цвет заливки нижнего уровня
DayColor = _input('DayColor', clrBlueViolet)  # цвет уровня начала дня
Up_Style = _input('Up_Style', SOLID_)  # стиль вернего уровня
Md_Style = _input('Md_Style', DASHDOTDOT_)  # стиль среднего уровня
Dn_Style = _input('Dn_Style', SOLID_)  # стиль нижнего уровня
DayStyle = _input('DayStyle', SOLID_)  # стиль уровня начала дня
Up_Width = _input('Up_Width', Width_3)  # толщина вернего уровня
Md_Width = _input('Md_Width', Width_1)  # толщина среднего уровня
Dn_Width = _input('Dn_Width', Width_3)  # толщина нижнего уровня
DayWidth = _input('DayWidth', Width_3)  # толщина уровня начала дня
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
DayExtremumsOffset = 3600
UpLineName = ""
MiddleLineName = ""
DownLineName = ""
DayLineName = ""
UpRectangleName = ""
DnRectangleName = ""

def OnInit():
    global DayLineName, DnRectangleName, DownLineName, MiddleLineName, UpLineName, UpRectangleName
    UpLineName = IndicatorSirname + ' UpLine'
    MiddleLineName = IndicatorSirname + ' MiddleLine'
    DownLineName = IndicatorSirname + ' DownLine'
    DayLineName = IndicatorSirname + ' DayLine'
    UpRectangleName = IndicatorSirname + ' UpRectangle'
    DnRectangleName = IndicatorSirname + ' DownRectangle'
    IndicatorSetString(INDICATOR_SHORTNAME, 'Paramon')

def OnDeinit(reason):
    ObjectDelete(0, UpLineName)
    ObjectDelete(0, MiddleLineName)
    ObjectDelete(0, DownLineName)
    ObjectDelete(0, DayLineName)
    ObjectDelete(0, UpRectangleName)
    ObjectDelete(0, DnRectangleName)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    lowprice = 0.0
    highprice = 0.0
    avprice = 0.0
    DayExtremumsBarOffset = 0
    iTime_ = Arr(0, 0)
    if CopyTime(Symbol(), PERIOD_D1, 0, 1, iTime_) <= 0:
        return 0
    bar = 0
    while time[bar] >= iTime_[0]:
        bar += 1
    if bar:
        bar -= 1
    if (_imod(TimeCurrent(), 60) * 60 * 24) > (60 * 60 * 10):
        while (time[0] - time[DayExtremumsBarOffset]) < DayExtremumsOffset and (_imod(time[DayExtremumsBarOffset], 60) * 60 * 24) > (60 * 60 * 10):
            DayExtremumsBarOffset += 1
        if DayExtremumsBarOffset:
            DayExtremumsBarOffset -= 1
    lowprice = low[ArrayMinimum(low, DayExtremumsBarOffset, bar - DayExtremumsBarOffset)]
    highprice = high[ArrayMaximum(high, DayExtremumsBarOffset, bar - DayExtremumsBarOffset)]
    avprice = (highprice + lowprice) / 2
    SetRectangle(0, UpRectangleName, 0, time[bar], avprice, time[0] + PeriodSeconds(), highprice, UpFill_Color, SOLID_, Width_1, UpRectangleName + DoubleToString(highprice, Digits()))
    SetRectangle(0, DnRectangleName, 0, time[bar], avprice, time[0] + PeriodSeconds(), lowprice, DnFill_Color, SOLID_, Width_1, DnRectangleName + DoubleToString(lowprice, Digits()))
    SetHline(0, UpLineName, 0, highprice, Up_Color, Up_Style, Up_Width, UpLineName + DoubleToString(highprice, Digits()))
    SetHline(0, MiddleLineName, 0, avprice, Md_Color, Md_Style, Md_Width, MiddleLineName + DoubleToString(avprice, Digits()))
    SetHline(0, DownLineName, 0, lowprice, Dn_Color, Dn_Style, Dn_Width, DownLineName + DoubleToString(lowprice, Digits()))
    SetVline(0, DayLineName, 0, time[bar], DayColor, DayStyle, DayWidth, True, 'дневной бар')
    ChartRedraw(0)
    return rates_total

def CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_RECTANGLE, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)

def SetRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

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

def CreateVline(chart_id, name, nwin, time1, Color, style, width, background, text):
    ObjectCreate(chart_id, name, OBJ_VLINE, nwin, time1, 999999999)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, background)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetVline(chart_id, name, nwin, time1, Color, style, width, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateVline(chart_id, name, nwin, time1, Color, style, width, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, 999999999)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ParTest(_MQL5Indicator):
    name = 'ParTest'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Up_Style': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль вернего уровня
        'Md_Style': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=4),  # стиль среднего уровня
        'Dn_Style': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль нижнего уровня
        'DayStyle': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль уровня начала дня
        'Up_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # толщина вернего уровня
        'Md_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина среднего уровня
        'Dn_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # толщина нижнего уровня
        'DayWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # толщина уровня начала дня
    }

