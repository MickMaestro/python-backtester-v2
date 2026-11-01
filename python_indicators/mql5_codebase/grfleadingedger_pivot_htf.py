"""GRFLeadingEdger_Pivot_HTF — converted from MQL5: MQL5 Indicators/GRFLeadingEdger_Pivot_HTF/GRFLeadingEdger_Pivot_HTF.mq5

GRFLeadingEdger Bands Pivot
Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['GRFLeadingEdger Bands Pivot'], 'name': 'GRFLeadingEdger_Pivot_HTF', 'source': 'MQL5 Indicators/GRFLeadingEdger_Pivot_HTF/GRFLeadingEdger_Pivot_HTF.mq5', 'folder': 'GRFLeadingEdger_Pivot_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'GRFLeadingEdger_Pivot_', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'Samples', 'py': 'Samples', 'param': 'Samples', 'type': 'uint', 'default': 60, 'label': '', 'sinput': False}, {'mql': 'LookAhead', 'py': 'LookAhead', 'param': 'LookAhead', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'StdLevel1', 'py': 'StdLevel1', 'param': 'StdLevel1', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'StdLevel2', 'py': 'StdLevel2', 'param': 'StdLevel2', 'type': 'double', 'default': 4.0, 'label': '', 'sinput': False}, {'mql': 'Up_Color', 'py': 'Up_Color', 'param': None, 'type': 'color', 'default': 8388352, 'label': 'Цвет верхней полосы индикатора', 'sinput': False}, {'mql': 'Dn_Color', 'py': 'Dn_Color', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Цвет нижней полосы индикатора', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'номер бара для получения значений индикатора', 'sinput': False}, {'mql': 'SignalLen', 'py': 'SignalLen', 'param': 'SignalLen', 'type': 'uint', 'default': 40, 'label': 'Длина полос индикатора', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'Upper_color1', 'py': 'Upper_color1', 'param': None, 'type': 'color', 'default': 7451452, 'label': '', 'sinput': False}, {'mql': 'Lower_color1', 'py': 'Lower_color1', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'Upper_color2', 'py': 'Upper_color2', 'param': None, 'type': 'color', 'default': 16748574, 'label': '', 'sinput': False}, {'mql': 'Lower_color2', 'py': 'Lower_color2', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
Symbols_Sirname = _input('Symbols_Sirname', 'GRFLeadingEdger_Pivot_')  # Название для меток индикатора
Samples = _input('Samples', 60)
LookAhead = _input('LookAhead', 0)
StdLevel1 = _input('StdLevel1', 2.0)
StdLevel2 = _input('StdLevel2', 4.0)
Up_Color = _input('Up_Color', clrSpringGreen)  # Цвет верхней полосы индикатора
Dn_Color = _input('Dn_Color', clrYellow)  # Цвет нижней полосы индикатора
SignalBar = _input('SignalBar', 0)  # номер бара для получения значений индикатора
SignalLen = _input('SignalLen', 40)  # Длина полос индикатора
Middle_color = _input('Middle_color', clrBlue)
Upper_color1 = _input('Upper_color1', clrMediumSeaGreen)
Lower_color1 = _input('Lower_color1', clrRed)
Upper_color2 = _input('Upper_color2', clrDodgerBlue)
Lower_color2 = _input('Lower_color2', clrMagenta)
min_rates_total = 0
min_rates_1 = 0
UpName = ""
MiddleName = ""
DnName = ""
upper_name1 = ""
middle_name = ""
lower_name1 = ""
upper_name2 = ""
lower_name2 = ""
PerSignalLen = 0
Ind_Handle = 0

def OnInit():
    global DnName, Ind_Handle, MiddleName, PerSignalLen, UpName, lower_name1, lower_name2, middle_name, min_rates_total, upper_name1, upper_name2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'GRFLeadingEdge', Samples, LookAhead, StdLevel1, StdLevel2, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора GRFLeadingEdge')
        return INIT_FAILED
    min_rates_total = _int(SignalLen)
    UpName = Symbols_Sirname + 'Upper Band'
    MiddleName = Symbols_Sirname + 'Middle Band'
    DnName = Symbols_Sirname + 'Lower Band'
    PerSignalLen = _int(SignalLen) * PeriodSeconds()
    upper_name1 = Symbols_Sirname + ' upper text lable 1'
    middle_name = Symbols_Sirname + ' middle text lable'
    lower_name1 = Symbols_Sirname + ' lower text lable 1'
    upper_name2 = Symbols_Sirname + ' upper text lable 2'
    lower_name2 = Symbols_Sirname + ' lower text lable 2'
    IndicatorSetString(INDICATOR_SHORTNAME, 'GRFLeadingEdger_Pivot_HTF')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, Symbols_Sirname, -1, -1)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    if CopyBuffer(Ind_Handle, 1, SignalBar, 1, _s_OnCalculate_Up2) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 2, SignalBar, 1, _s_OnCalculate_Up1) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 0, SignalBar, 1, _s_OnCalculate_Middle) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 3, SignalBar, 1, _s_OnCalculate_Dn1) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 4, SignalBar, 1, _s_OnCalculate_Dn2) <= 0:
        return 0
    bar0 = rates_total - 1
    bar1 = rates_total - _int(MathMax(SignalLen - 1, 0))
    time0 = time[bar0] + (2 * PeriodSeconds())
    time1 = time0 - PerSignalLen
    SetRectangle(0, UpName, 0, time1, _s_OnCalculate_Up1[0], time0, _s_OnCalculate_Up2[0], Up_Color, STYLE_SOLID, 1, UpName)
    SetRectangle(0, DnName, 0, time1, _s_OnCalculate_Dn1[0], time0, _s_OnCalculate_Dn2[0], Dn_Color, STYLE_SOLID, 1, DnName)
    SetTline(0, MiddleName, 0, time1, _s_OnCalculate_Middle[0], time0, _s_OnCalculate_Middle[0], Middle_color, STYLE_SOLID, 1, MiddleName)
    SetRightPrice(0, upper_name1, 0, time[bar0], _s_OnCalculate_Up1[0], Upper_color1, 'Georgia')
    SetRightPrice(0, lower_name1, 0, time[bar0], _s_OnCalculate_Dn1[0], Lower_color1, 'Georgia')
    SetRightPrice(0, middle_name, 0, time[bar0], _s_OnCalculate_Middle[0], Middle_color, 'Georgia')
    SetRightPrice(0, upper_name2, 0, time[bar0], _s_OnCalculate_Up2[0], Upper_color2, 'Georgia')
    SetRightPrice(0, lower_name2, 0, time[bar0], _s_OnCalculate_Dn2[0], Lower_color2, 'Georgia')
    ChartRedraw(0)
    return rates_total

def CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_RECTANGLE, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)

def SetRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

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

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

# ---- static local variables
_s_OnCalculate_Up1 = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Up2 = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Middle = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Dn1 = Arr(1, 0.0, dyn=False)
_s_OnCalculate_Dn2 = Arr(1, 0.0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GRFLeadingEdgerPivotHTF(_MQL5Indicator):
    name = 'GRFLeadingEdger_Pivot_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'Samples': 60,
        'LookAhead': 0,
        'StdLevel1': 2.0,
        'StdLevel2': 4.0,
        'SignalBar': 0,  # номер бара для получения значений индикатора
        'SignalLen': 40,  # Длина полос индикатора
    }

