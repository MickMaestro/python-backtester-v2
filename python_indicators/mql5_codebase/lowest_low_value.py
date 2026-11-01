"""lowest_low_value — converted from MQL5: MQL5 Indicators/LOWEST_LOW_VALUE/lowest_low_value.mq5

Price minimum for the period specified in inputs
Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Price minimum for the period specified in inputs'], 'name': 'lowest_low_value', 'source': 'MQL5 Indicators/LOWEST_LOW_VALUE/lowest_low_value.mq5', 'folder': 'LOWEST_LOW_VALUE', 'inputs': [{'mql': 'level_name', 'py': 'level_name', 'param': None, 'type': 'string', 'default': 'Price_LOWEST_LOW_VALUE_1', 'label': 'Level name', 'sinput': False}, {'mql': 'level_comment', 'py': 'level_comment', 'param': None, 'type': 'string', 'default': 'trigger level', 'label': 'A comment to the level', 'sinput': False}, {'mql': 'level_period', 'py': 'level_period', 'param': 'level_period', 'type': 'uint', 'default': 5, 'label': 'Level search period', 'sinput': False}, {'mql': 'level_start', 'py': 'level_start', 'param': 'level_start', 'type': 'uint', 'default': 0, 'label': 'The number of the starting bar', 'sinput': False}, {'mql': 'level_color', 'py': 'level_color', 'param': None, 'type': 'color', 'default': 255, 'label': 'Level color', 'sinput': False}, {'mql': 'level_style', 'py': 'level_style', 'param': 'level_style', 'type': 'int', 'default': 0, 'label': 'The style of the trigger level', 'sinput': False}, {'mql': 'level_width', 'py': 'level_width', 'param': 'level_width', 'type': 'int', 'default': 3, 'label': 'The width of the trigger level', 'sinput': False}, {'mql': 'Deletelevel', 'py': 'Deletelevel', 'param': 'Deletelevel', 'type': 'bool', 'default': True, 'label': 'Deleting the level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# enum ENUM_ALERT_MODE
OnlySound = 0
OnlyAlert = 1
_enum('ENUM_ALERT_MODE', {0: 'OnlySound', 1: 'OnlyAlert'})

# ---- inputs and global variables
level_name = _input('level_name', 'Price_LOWEST_LOW_VALUE_1')  # Level name
level_comment = _input('level_comment', 'trigger level')  # A comment to the level
level_period = _input('level_period', 5)  # Level search period
level_start = _input('level_start', 0)  # The number of the starting bar
level_color = _input('level_color', clrRed)  # Level color
level_style = _input('level_style', STYLE_SOLID)  # The style of the trigger level
level_width = _input('level_width', w_3)  # The width of the trigger level
Deletelevel = _input('Deletelevel', True)  # Deleting the level
min_rates_total = 0

def CreateHline(chart_id, name, nwin, price, Color, style, width, background, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, nwin, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, background)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetHline(chart_id, name, nwin, price, Color, style, width, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnInit():
    global min_rates_total
    min_rates_total = _int(level_start + level_period)
    if ObjectFind(0, level_name) == -1:
        CreateHline(0, level_name, 0, 0.0, level_color, level_style, level_width, False, level_comment)

def OnDeinit(reason):
    if Deletelevel:
        ObjectDelete(0, level_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(low, True)
    LL = low[ArrayMinimum(low, level_start, level_period)]
    SetHline(0, level_name, 0, LL, level_color, level_style, level_width, False, level_comment)
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LowestLowValue(_MQL5Indicator):
    name = 'lowest_low_value'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'level_period': 5,  # Level search period
        'level_start': 0,  # The number of the starting bar
        'level_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # The style of the trigger level
        'level_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # The width of the trigger level
        'Deletelevel': True,  # Deleting the level
    }

