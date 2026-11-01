"""maksigen_range_move — converted from MQL5: MQL5 Indicators/MaksiGen_Range_Move/maksigen_range_move.mq5

Flat determining indicator
Copyright: Copyright © 2006, MaksiGen; Link: olegvs2003@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, MaksiGen', 'link': 'olegvs2003@yahoo.com', 'version': '1.00', 'indicator_buffers': 0, 'indicator_plots': 0, 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Flat determining indicator'], 'name': 'maksigen_range_move', 'source': 'MQL5 Indicators/MaksiGen_Range_Move/maksigen_range_move.mq5', 'folder': 'MaksiGen_Range_Move', 'inputs': [{'mql': 'LinesSirname', 'py': 'LinesSirname', 'param': None, 'type': 'string', 'default': 'MaksiGen_Range_Move', 'label': 'Line name', 'sinput': False}, {'mql': 'Pfast', 'py': 'Pfast', 'param': 'Pfast', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Pslow', 'py': 'Pslow', 'param': 'Pslow', 'type': 'uint', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'K_RangeOpen', 'py': 'K_RangeOpen', 'param': 'K_RangeOpen', 'type': 'double', 'default': 1.4, 'label': '', 'sinput': False}, {'mql': 'Line_Color_1', 'py': 'Line_Color_1', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'Line color of hi1', 'sinput': False}, {'mql': 'Line_Style_1', 'py': 'Line_Style_1', 'param': 'Line_Style_1', 'type': 'int', 'default': 2, 'label': 'Line style of hi1', 'sinput': False}, {'mql': 'Line_Width_1', 'py': 'Line_Width_1', 'param': 'Line_Width_1', 'type': 'int', 'default': 1, 'label': 'Line width of hi1', 'sinput': False}, {'mql': 'Line_Background_1', 'py': 'Line_Background_1', 'param': 'Line_Background_1', 'type': 'bool', 'default': True, 'label': 'Background mode for the hi1 line', 'sinput': False}, {'mql': 'Line_Color_2', 'py': 'Line_Color_2', 'param': None, 'type': 'color', 'default': 255, 'label': 'Line color of lo1', 'sinput': False}, {'mql': 'Line_Style_2', 'py': 'Line_Style_2', 'param': 'Line_Style_2', 'type': 'int', 'default': 2, 'label': 'Line style of lo1', 'sinput': False}, {'mql': 'Line_Width_2', 'py': 'Line_Width_2', 'param': 'Line_Width_2', 'type': 'int', 'default': 1, 'label': 'Line width of lo1', 'sinput': False}, {'mql': 'Line_Background_2', 'py': 'Line_Background_2', 'param': 'Line_Background_2', 'type': 'bool', 'default': True, 'label': 'Background mode for the lo1 line', 'sinput': False}, {'mql': 'Line_Color_3', 'py': 'Line_Color_3', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'Line color of hi2', 'sinput': False}, {'mql': 'Line_Style_3', 'py': 'Line_Style_3', 'param': 'Line_Style_3', 'type': 'int', 'default': 1, 'label': 'Line style of hi2', 'sinput': False}, {'mql': 'Line_Width_3', 'py': 'Line_Width_3', 'param': 'Line_Width_3', 'type': 'int', 'default': 1, 'label': 'Line width of hi2', 'sinput': False}, {'mql': 'Line_Background_3', 'py': 'Line_Background_3', 'param': 'Line_Background_3', 'type': 'bool', 'default': True, 'label': 'Background mode for the hi2 line', 'sinput': False}, {'mql': 'Line_Color_4', 'py': 'Line_Color_4', 'param': None, 'type': 'color', 'default': 255, 'label': 'Line color of lo2', 'sinput': False}, {'mql': 'Line_Style_4', 'py': 'Line_Style_4', 'param': 'Line_Style_4', 'type': 'int', 'default': 1, 'label': 'Line style of lo2', 'sinput': False}, {'mql': 'Line_Width_4', 'py': 'Line_Width_4', 'param': 'Line_Width_4', 'type': 'int', 'default': 1, 'label': 'Line width of lo2', 'sinput': False}, {'mql': 'Line_Background_4', 'py': 'Line_Background_4', 'param': 'Line_Background_4', 'type': 'bool', 'default': True, 'label': 'Background mode for the lo2 line', 'sinput': False}, {'mql': 'Line_Color_5', 'py': 'Line_Color_5', 'param': None, 'type': 'color', 'default': 55295, 'label': 'Line color of Bar#1', 'sinput': False}, {'mql': 'Line_Style_5', 'py': 'Line_Style_5', 'param': 'Line_Style_5', 'type': 'int', 'default': 2, 'label': 'Line style of Bar#1', 'sinput': False}, {'mql': 'Line_Width_5', 'py': 'Line_Width_5', 'param': 'Line_Width_5', 'type': 'int', 'default': 1, 'label': 'Line width of Bar#1', 'sinput': False}, {'mql': 'Line_Background_5', 'py': 'Line_Background_5', 'param': 'Line_Background_5', 'type': 'bool', 'default': True, 'label': 'Background mode for the Bar#1 line', 'sinput': False}, {'mql': 'Line_Color_6', 'py': 'Line_Color_6', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Line color of Bar#Pfast', 'sinput': False}, {'mql': 'Line_Style_6', 'py': 'Line_Style_6', 'param': 'Line_Style_6', 'type': 'int', 'default': 2, 'label': 'Line style of Bar#Pfast', 'sinput': False}, {'mql': 'Line_Width_6', 'py': 'Line_Width_6', 'param': 'Line_Width_6', 'type': 'int', 'default': 1, 'label': 'Line width of Bar#Pfast', 'sinput': False}, {'mql': 'Line_Background_6', 'py': 'Line_Background_6', 'param': 'Line_Background_6', 'type': 'bool', 'default': True, 'label': 'Background mode for the Bar#Pfast line', 'sinput': False}, {'mql': 'Line_Color_7', 'py': 'Line_Color_7', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Line color of Bar#Pslow', 'sinput': False}, {'mql': 'Line_Style_7', 'py': 'Line_Style_7', 'param': 'Line_Style_7', 'type': 'int', 'default': 2, 'label': 'Line style of Bar#Pslow', 'sinput': False}, {'mql': 'Line_Width_7', 'py': 'Line_Width_7', 'param': 'Line_Width_7', 'type': 'int', 'default': 1, 'label': 'Line width of Bar#Pslow', 'sinput': False}, {'mql': 'Line_Background_7', 'py': 'Line_Background_7', 'param': 'Line_Background_7', 'type': 'bool', 'default': True, 'label': 'Background mode for the Bar#Pslow line', 'sinput': False}, {'mql': 'Line_Color_8', 'py': 'Line_Color_8', 'param': None, 'type': 'color', 'default': 14822282, 'label': 'Line color of TrendHIGH', 'sinput': False}, {'mql': 'Line_Style_8', 'py': 'Line_Style_8', 'param': 'Line_Style_8', 'type': 'int', 'default': 0, 'label': 'Line style of TrendHIGH', 'sinput': False}, {'mql': 'Line_Width_8', 'py': 'Line_Width_8', 'param': 'Line_Width_8', 'type': 'int', 'default': 1, 'label': 'Line width of TrendHIGH', 'sinput': False}, {'mql': 'Line_Background_8', 'py': 'Line_Background_8', 'param': 'Line_Background_8', 'type': 'bool', 'default': True, 'label': 'Background mode for the TrendHIGH line', 'sinput': False}, {'mql': 'Line_Color_9', 'py': 'Line_Color_9', 'param': None, 'type': 'color', 'default': 14822282, 'label': 'Line color of Trend_LOW', 'sinput': False}, {'mql': 'Line_Style_9', 'py': 'Line_Style_9', 'param': 'Line_Style_9', 'type': 'int', 'default': 0, 'label': 'Line style of Trend_LOW', 'sinput': False}, {'mql': 'Line_Width_9', 'py': 'Line_Width_9', 'param': 'Line_Width_9', 'type': 'int', 'default': 1, 'label': 'Line width of Trend_LOW', 'sinput': False}, {'mql': 'Line_Background_9', 'py': 'Line_Background_9', 'param': 'Line_Background_9', 'type': 'bool', 'default': True, 'label': 'Background mode for the Trend_LOW line', 'sinput': False}, {'mql': 'Line_Color_10', 'py': 'Line_Color_10', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Line color of SELL_STOP', 'sinput': False}, {'mql': 'Line_Style_10', 'py': 'Line_Style_10', 'param': 'Line_Style_10', 'type': 'int', 'default': 2, 'label': 'Line style of SELL_STOP', 'sinput': False}, {'mql': 'Line_Width_10', 'py': 'Line_Width_10', 'param': 'Line_Width_10', 'type': 'int', 'default': 1, 'label': 'Line width of SELL_STOP', 'sinput': False}, {'mql': 'Line_Background_10', 'py': 'Line_Background_10', 'param': 'Line_Background_10', 'type': 'bool', 'default': True, 'label': 'Background mode for the SELL_STOP line', 'sinput': False}, {'mql': 'Line_Color_11', 'py': 'Line_Color_11', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'Line color of BUY_STOP', 'sinput': False}, {'mql': 'Line_Style_11', 'py': 'Line_Style_11', 'param': 'Line_Style_11', 'type': 'int', 'default': 2, 'label': 'Line style of BUY_STOP', 'sinput': False}, {'mql': 'Line_Width_11', 'py': 'Line_Width_11', 'param': 'Line_Width_11', 'type': 'int', 'default': 1, 'label': 'Line width of BUY_STOP', 'sinput': False}, {'mql': 'Line_Background_11', 'py': 'Line_Background_11', 'param': 'Line_Background_11', 'type': 'bool', 'default': True, 'label': 'Background mode for the BUY_STOP line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
LinesSirname = _input('LinesSirname', 'MaksiGen_Range_Move')  # Line name
Pfast = _input('Pfast', 5)
Pslow = _input('Pslow', 8)
K_RangeOpen = _input('K_RangeOpen', 1.4)
Line_Color_1 = _input('Line_Color_1', clrTeal)  # Line color of hi1
Line_Style_1 = _input('Line_Style_1', DOT_)  # Line style of hi1
Line_Width_1 = _input('Line_Width_1', w_1)  # Line width of hi1
Line_Background_1 = _input('Line_Background_1', True)  # Background mode for the hi1 line
Line_Color_2 = _input('Line_Color_2', clrRed)  # Line color of lo1
Line_Style_2 = _input('Line_Style_2', DOT_)  # Line style of lo1
Line_Width_2 = _input('Line_Width_2', w_1)  # Line width of lo1
Line_Background_2 = _input('Line_Background_2', True)  # Background mode for the lo1 line
Line_Color_3 = _input('Line_Color_3', clrTeal)  # Line color of hi2
Line_Style_3 = _input('Line_Style_3', DASH_)  # Line style of hi2
Line_Width_3 = _input('Line_Width_3', w_1)  # Line width of hi2
Line_Background_3 = _input('Line_Background_3', True)  # Background mode for the hi2 line
Line_Color_4 = _input('Line_Color_4', clrRed)  # Line color of lo2
Line_Style_4 = _input('Line_Style_4', DASH_)  # Line style of lo2
Line_Width_4 = _input('Line_Width_4', w_1)  # Line width of lo2
Line_Background_4 = _input('Line_Background_4', True)  # Background mode for the lo2 line
Line_Color_5 = _input('Line_Color_5', clrGold)  # Line color of Bar#1
Line_Style_5 = _input('Line_Style_5', DOT_)  # Line style of Bar#1
Line_Width_5 = _input('Line_Width_5', w_1)  # Line width of Bar#1
Line_Background_5 = _input('Line_Background_5', True)  # Background mode for the Bar#1 line
Line_Color_6 = _input('Line_Color_6', clrMagenta)  # Line color of Bar#Pfast
Line_Style_6 = _input('Line_Style_6', DOT_)  # Line style of Bar#Pfast
Line_Width_6 = _input('Line_Width_6', w_1)  # Line width of Bar#Pfast
Line_Background_6 = _input('Line_Background_6', True)  # Background mode for the Bar#Pfast line
Line_Color_7 = _input('Line_Color_7', clrBlue)  # Line color of Bar#Pslow
Line_Style_7 = _input('Line_Style_7', DOT_)  # Line style of Bar#Pslow
Line_Width_7 = _input('Line_Width_7', w_1)  # Line width of Bar#Pslow
Line_Background_7 = _input('Line_Background_7', True)  # Background mode for the Bar#Pslow line
Line_Color_8 = _input('Line_Color_8', clrBlueViolet)  # Line color of TrendHIGH
Line_Style_8 = _input('Line_Style_8', SOLID_)  # Line style of TrendHIGH
Line_Width_8 = _input('Line_Width_8', w_1)  # Line width of TrendHIGH
Line_Background_8 = _input('Line_Background_8', True)  # Background mode for the TrendHIGH line
Line_Color_9 = _input('Line_Color_9', clrBlueViolet)  # Line color of Trend_LOW
Line_Style_9 = _input('Line_Style_9', SOLID_)  # Line style of Trend_LOW
Line_Width_9 = _input('Line_Width_9', w_1)  # Line width of Trend_LOW
Line_Background_9 = _input('Line_Background_9', True)  # Background mode for the Trend_LOW line
Line_Color_10 = _input('Line_Color_10', clrMagenta)  # Line color of SELL_STOP
Line_Style_10 = _input('Line_Style_10', DOT_)  # Line style of SELL_STOP
Line_Width_10 = _input('Line_Width_10', w_1)  # Line width of SELL_STOP
Line_Background_10 = _input('Line_Background_10', True)  # Background mode for the SELL_STOP line
Line_Color_11 = _input('Line_Color_11', clrTeal)  # Line color of BUY_STOP
Line_Style_11 = _input('Line_Style_11', DOT_)  # Line style of BUY_STOP
Line_Width_11 = _input('Line_Width_11', w_1)  # Line width of BUY_STOP
Line_Background_11 = _input('Line_Background_11', True)  # Background mode for the BUY_STOP line
name_1 = ""
name_2 = ""
name_3 = ""
name_4 = ""
name_5 = ""
name_6 = ""
name_7 = ""
name_8 = ""
name_9 = ""
name_10 = ""
name_11 = ""
min_rates_total = 0

def Deinit():
    ObjectDelete(0, name_1)
    ObjectDelete(0, name_2)
    ObjectDelete(0, name_3)
    ObjectDelete(0, name_4)
    ObjectDelete(0, name_5)
    ObjectDelete(0, name_6)
    ObjectDelete(0, name_7)
    ObjectDelete(0, name_8)
    ObjectDelete(0, name_9)
    ObjectDelete(0, name_10)
    ObjectDelete(0, name_11)
    ChartRedraw(0)

def OnInit():
    global min_rates_total, name_1, name_10, name_11, name_2, name_3, name_4, name_5, name_6, name_7, name_8, name_9
    min_rates_total = _int(MathMax(Pfast, Pslow))
    name_1 = LinesSirname + ' hi1'
    name_2 = LinesSirname + ' lo1'
    name_3 = LinesSirname + ' hi2'
    name_4 = LinesSirname + ' lo2'
    name_5 = LinesSirname + ' Bar#1'
    name_6 = LinesSirname + ' Bar#Pfast'
    name_7 = LinesSirname + ' Bar#Pslow'
    name_8 = LinesSirname + ' TrendHIGH'
    name_9 = LinesSirname + ' TrendLOW'
    name_10 = LinesSirname + ' SELL_STOP'
    name_11 = LinesSirname + ' BUY_STOP'
    IndicatorSetString(INDICATOR_SHORTNAME, 'MaksiGen_Range_Move')

def OnDeinit(reason):
    Deinit()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or rates_total == prev_calculated:
        return 0
    hi1 = 0.0
    hi2 = 0.0
    lo1 = 0.0
    lo2 = 0.0
    ftime = 0
    stime = 0
    time1 = 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    hi1 = high[ArrayMaximum(high, 1, Pfast)]
    lo1 = low[ArrayMinimum(low, 1, Pfast)]
    hi2 = high[ArrayMaximum(high, 1, Pslow)]
    lo2 = low[ArrayMinimum(low, 1, Pslow)]
    ftime = time[Pfast]
    stime = time[Pslow]
    time1 = time[1]
    SetHline(0, name_1, 0, hi1, Line_Color_1, Line_Style_1, Line_Width_1, name_1)
    SetHline(0, name_2, 0, lo1, Line_Color_2, Line_Style_2, Line_Width_2, name_2)
    SetHline(0, name_3, 0, hi2, Line_Color_3, Line_Style_3, Line_Width_3, name_3)
    SetHline(0, name_4, 0, lo2, Line_Color_4, Line_Style_4, Line_Width_4, name_4)
    SetVline(0, name_5, 0, time1, Line_Color_5, Line_Style_5, Line_Width_5, name_5)
    SetVline(0, name_6, 0, ftime, Line_Color_6, Line_Style_6, Line_Width_6, name_6)
    SetVline(0, name_7, 0, stime, Line_Color_7, Line_Style_7, Line_Width_7, name_7)
    SetTline(0, name_8, 0, time[Pslow], hi2, time[Pfast], hi1, Line_Color_8, Line_Style_8, Line_Width_8, name_8)
    SetTline(0, name_9, 0, time[Pslow], lo2, time[Pfast], lo1, Line_Color_9, Line_Style_9, Line_Width_9, name_9)
    if (hi1 - lo1) == (hi2 - lo2):
        Range = (hi1 - lo1) * K_RangeOpen
        SetHline(0, name_10, 0, lo1 - Range, Line_Color_10, Line_Style_10, Line_Width_10, name_10)
        SetHline(0, name_11, 0, hi1 + Range, Line_Color_11, Line_Style_11, Line_Width_11, name_11)
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

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)

def CreateVline(chart_id, name, nwin, time1, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_VLINE, nwin, time1, 999999999)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetVline(chart_id, name, nwin, time1, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateVline(chart_id, name, nwin, time1, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, 999999999)

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


class MaksigenRangeMove(_MQL5Indicator):
    name = 'maksigen_range_move'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Pfast': 5,
        'Pslow': 8,
        'K_RangeOpen': 1.4,
        'Line_Style_1': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=2),  # Line style of hi1
        'Line_Width_1': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of hi1
        'Line_Background_1': True,  # Background mode for the hi1 line
        'Line_Style_2': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=2),  # Line style of lo1
        'Line_Width_2': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of lo1
        'Line_Background_2': True,  # Background mode for the lo1 line
        'Line_Style_3': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # Line style of hi2
        'Line_Width_3': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of hi2
        'Line_Background_3': True,  # Background mode for the hi2 line
        'Line_Style_4': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # Line style of lo2
        'Line_Width_4': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of lo2
        'Line_Background_4': True,  # Background mode for the lo2 line
        'Line_Style_5': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=2),  # Line style of Bar#1
        'Line_Width_5': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of Bar#1
        'Line_Background_5': True,  # Background mode for the Bar#1 line
        'Line_Style_6': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=2),  # Line style of Bar#Pfast
        'Line_Width_6': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of Bar#Pfast
        'Line_Background_6': True,  # Background mode for the Bar#Pfast line
        'Line_Style_7': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=2),  # Line style of Bar#Pslow
        'Line_Width_7': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of Bar#Pslow
        'Line_Background_7': True,  # Background mode for the Bar#Pslow line
        'Line_Style_8': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Line style of TrendHIGH
        'Line_Width_8': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of TrendHIGH
        'Line_Background_8': True,  # Background mode for the TrendHIGH line
        'Line_Style_9': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Line style of Trend_LOW
        'Line_Width_9': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of Trend_LOW
        'Line_Background_9': True,  # Background mode for the Trend_LOW line
        'Line_Style_10': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=2),  # Line style of SELL_STOP
        'Line_Width_10': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of SELL_STOP
        'Line_Background_10': True,  # Background mode for the SELL_STOP line
        'Line_Style_11': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=2),  # Line style of BUY_STOP
        'Line_Width_11': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width of BUY_STOP
        'Line_Background_11': True,  # Background mode for the BUY_STOP line
    }

