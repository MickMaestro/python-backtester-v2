"""zigzag_nk_mtf_levels — converted from MQL5: MQL5 Indicators/ZigZag_NK_MTF_Levels/zigzag_nk_mtf_levels.mq5

Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'zigzag_nk_mtf_levels', 'source': 'MQL5 Indicators/ZigZag_NK_MTF_Levels/zigzag_nk_mtf_levels.mq5', 'folder': 'ZigZag_NK_MTF_Levels', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'levels_sirname', 'py': 'levels_sirname', 'param': None, 'type': 'string', 'default': 'ZigZag_NK_MTF_Level', 'label': 'A name for the group of levels', 'sinput': False}, {'mql': 'SuprTotal', 'py': 'SuprTotal', 'param': 'SuprTotal', 'type': 'uint', 'default': 6, 'label': 'The number of maxima and minima', 'sinput': False}, {'mql': 'Color_Res', 'py': 'Color_Res', 'param': None, 'type': 'color', 'default': 16776960, 'label': 'Color of resistance', 'sinput': False}, {'mql': 'Style_Res', 'py': 'Style_Res', 'param': 'Style_Res', 'type': 'int', 'default': 0, 'label': 'Style of the maximum line', 'sinput': False}, {'mql': 'Width_Res', 'py': 'Width_Res', 'param': 'Width_Res', 'type': 'int', 'default': 3, 'label': 'Width of the maximum line', 'sinput': False}, {'mql': 'Color_Sup', 'py': 'Color_Sup', 'param': None, 'type': 'color', 'default': 13850042, 'label': 'Color of support', 'sinput': False}, {'mql': 'Style_Sup', 'py': 'Style_Sup', 'param': 'Style_Sup', 'type': 'int', 'default': 0, 'label': 'Style of the minimum line', 'sinput': False}, {'mql': 'Width_Sup', 'py': 'Width_Sup', 'param': 'Width_Sup', 'type': 'int', 'default': 3, 'label': 'Width of the minimum line', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Width
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('Width', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum Style
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('Style', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
levels_sirname = _input('levels_sirname', 'ZigZag_NK_MTF_Level')  # A name for the group of levels
SuprTotal = _input('SuprTotal', 6)  # The number of maxima and minima
Color_Res = _input('Color_Res', clrAqua)  # Color of resistance
Style_Res = _input('Style_Res', SOLID_)  # Style of the maximum line
Width_Res = _input('Width_Res', Width_3)  # Width of the maximum line
Color_Sup = _input('Color_Sup', clrMediumOrchid)  # Color of support
Style_Sup = _input('Style_Sup', SOLID_)  # Style of the minimum line
Width_Sup = _input('Width_Sup', Width_3)  # Width of the minimum line
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
HighestBuffer = Arr(0, 0.0)
LowestBuffer = Arr(0, 0.0)
UpLinesName = Arr(0, "")
DnLinesName = Arr(0, "")
min_rates_total = 0
nSuprTotal = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, min_rates_total, nSuprTotal
    ArrayResize(UpLinesName, SuprTotal)
    ArrayResize(DnLinesName, SuprTotal)
    nSuprTotal = _int(SuprTotal)
    min_rates_total = _int(ExtDepth + ExtBackstep) * nSuprTotal * 2
    for count in range(0, nSuprTotal):
        UpLinesName[count] = levels_sirname + '_Up_' + _str(count)
    for count in range(0, nSuprTotal):
        DnLinesName[count] = levels_sirname + '_Dn_' + _str(count)
    Ind_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'ZigZag_NK_MTF', TimeFrame, ExtDepth, ExtDeviation, ExtBackstep)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the ZigZag_NK_MTF indicator')
        return INIT_FAILED
    SetIndexBuffer(0, LowestBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZigZag_NK_Levels(' + _str(SuprTotal) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    for count in range(0, nSuprTotal):
        ObjectDelete(0, UpLinesName[count])
    for count in range(0, nSuprTotal):
        ObjectDelete(0, DnLinesName[count])
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, 1, 0, to_copy, LowestBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, HighestBuffer) <= 0:
        return 0
    upcount = 0
    dncount = 0
    for bar in range(0, rates_total):
        if dncount < nSuprTotal and LowestBuffer[bar]:
            Min = LowestBuffer[bar]
            end = time[0] + PeriodSeconds(PERIOD_CURRENT)
            SetTline(0, DnLinesName[dncount], 0, time[bar], Min, end, Min, Color_Sup, Style_Sup, Width_Sup, DoubleToString(Min, Digits()))
            dncount += 1
        if upcount < nSuprTotal and HighestBuffer[bar]:
            Max = HighestBuffer[bar]
            end = time[0] + PeriodSeconds(PERIOD_CURRENT)
            SetTline(0, UpLinesName[upcount], 0, time[bar], Max, end, Max, Color_Res, Style_Res, Width_Res, DoubleToString(Max, Digits()))
            upcount += 1
        if dncount == nSuprTotal and upcount == nSuprTotal:
            break
    for count in range(dncount, nSuprTotal):
        ObjectDelete(0, DnLinesName[count])
    for count in range(upcount, nSuprTotal):
        ObjectDelete(0, UpLinesName[count])
    ChartRedraw(0)
    return rates_total

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigzagNkMtfLevels(_MQL5Indicator):
    name = 'zigzag_nk_mtf_levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'SuprTotal': 6,  # The number of maxima and minima
        'Style_Res': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Style of the maximum line
        'Width_Res': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Width of the maximum line
        'Style_Sup': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Style of the minimum line
        'Width_Sup': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Width of the minimum line
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
    }

