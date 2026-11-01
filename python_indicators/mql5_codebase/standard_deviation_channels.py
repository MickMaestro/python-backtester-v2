"""standard_deviation_channels — converted from MQL5: MQL5 Indicators/Standard_Deviation_Channels/standard_deviation_channels.mq5

Standard_Deviation_Channels
Copyright: Copyright © 2006, tageiger, aka fxid10t@yahoo.com; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, tageiger, aka fxid10t@yahoo.com', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Standard_Deviation_Channels'], 'name': 'standard_deviation_channels', 'source': 'MQL5 Indicators/Standard_Deviation_Channels/standard_deviation_channels.mq5', 'folder': 'Standard_Deviation_Channels', 'inputs': [{'mql': 'lines_sirname', 'py': 'lines_sirname', 'param': None, 'type': 'string', 'default': 'Standard_Deviation_Channels', 'label': 'Graphic objects group name', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 0, 'label': 'Chart period', 'sinput': False}, {'mql': 'STD_Rgres_length', 'py': 'STD_Rgres_length', 'param': 'STD_Rgres_length', 'type': 'int', 'default': 56, 'label': 'Bars back regression begins', 'sinput': False}, {'mql': 'STD_Rgres_width', 'py': 'STD_Rgres_width', 'param': 'STD_Rgres_width', 'type': 'double', 'default': 1.618, 'label': 'Widest channel', 'sinput': False}, {'mql': 'STD_width', 'py': 'STD_width', 'param': 'STD_width', 'type': 'double', 'default': 0.618, 'label': 'Inside channel', 'sinput': False}, {'mql': 'widest_color', 'py': 'widest_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Widest color', 'sinput': False}, {'mql': 'widest_style', 'py': 'widest_style', 'param': 'widest_style', 'type': 'int', 'default': 0, 'label': 'Widest style', 'sinput': False}, {'mql': 'widest_width', 'py': 'widest_width', 'param': 'widest_width', 'type': 'int', 'default': 3, 'label': 'Widest width', 'sinput': False}, {'mql': 'inside_color', 'py': 'inside_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Inside color', 'sinput': False}, {'mql': 'inside_style', 'py': 'inside_style', 'param': 'inside_style', 'type': 'int', 'default': 0, 'label': 'Inside style', 'sinput': False}, {'mql': 'inside_width', 'py': 'inside_width', 'param': 'inside_width', 'type': 'int', 'default': 3, 'label': 'Inside width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
lines_sirname = _input('lines_sirname', 'Standard_Deviation_Channels')  # Graphic objects group name
period = _input('period', PERIOD_CURRENT)  # Chart period
STD_Rgres_length = _input('STD_Rgres_length', 56)  # Bars back regression begins
STD_Rgres_width = _input('STD_Rgres_width', 1.618)  # Widest channel
STD_width = _input('STD_width', 0.618)  # Inside channel
widest_color = _input('widest_color', clrBlue)  # Widest color
widest_style = _input('widest_style', STYLE_SOLID)  # Widest style
widest_width = _input('widest_width', w_3)  # Widest width
inside_color = _input('inside_color', clrBlue)  # Inside color
inside_style = _input('inside_style', STYLE_SOLID)  # Inside style
inside_width = _input('inside_width', w_3)  # Inside width
name1 = ""
name2 = ""

def CreateStdDevChannel(chart_id, name, nwin, time1, price1, time2, price2, stdwidth, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_STDDEVCHANNEL, nwin, time1, price1, time2, price2)
    ObjectSetDouble(chart_id, name, OBJPROP_DEVIATION, stdwidth)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetStdDevChannel(chart_id, name, nwin, time1, price1, time2, price2, stdwidth, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateStdDevChannel(chart_id, name, nwin, time1, price1, time2, price2, stdwidth, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
        ObjectSetDouble(chart_id, name, OBJPROP_DEVIATION, stdwidth)

def OnInit():
    global name1, name2
    name1 = lines_sirname + ' 1'
    name2 = lines_sirname + ' 2'

def OnDeinit(reason):
    ObjectDelete(0, name1)
    ObjectDelete(0, name2)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    iTime_ = Arr(0, 0)
    if CopyTime(None, period, STD_Rgres_length, 1, iTime_) <= 0:
        return 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    SetStdDevChannel(0, name1, 0, iTime_[0], close[STD_Rgres_length], time[0], close[0], STD_Rgres_width, inside_color, inside_style, inside_width, name1)
    SetStdDevChannel(0, name2, 0, iTime_[0], close[STD_Rgres_length], time[0], close[0], STD_width, widest_color, widest_style, widest_width, name2)
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StandardDeviationChannels(_MQL5Indicator):
    name = 'standard_deviation_channels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Chart period
        'STD_Rgres_length': 56,  # Bars back regression begins
        'STD_Rgres_width': 1.618,  # Widest channel
        'STD_width': 0.618,  # Inside channel
        'widest_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Widest style
        'widest_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Widest width
        'inside_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Inside style
        'inside_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Inside width
    }

