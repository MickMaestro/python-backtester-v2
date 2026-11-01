"""Candle_Grids — converted from MQL5: MQL5 Indicators/Candle Grids/Candle_Grids.mq5

Copyright: Copyright 2024, Rajesh Kumar Nait; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Rajesh Kumar Nait', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Candle_Grids', 'source': 'MQL5 Indicators/Candle Grids/Candle_Grids.mq5', 'folder': 'Candle Grids', 'inputs': [{'mql': 'points', 'py': 'points', 'param': 'points', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'number_of_levels', 'py': 'number_of_levels', 'param': 'number_of_levels', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'is_range', 'py': 'is_range', 'param': 'is_range', 'type': 'bool', 'default': True, 'label': 'Use Rectangle Range for Grid?', 'sinput': False}, {'mql': 'Grid_up_color', 'py': 'Grid_up_color', 'param': None, 'type': 'color', 'default': 6908265, 'label': '', 'sinput': False}, {'mql': 'Grid_up_Style', 'py': 'Grid_up_Style', 'param': 'Grid_up_Style', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'Grid_dn_color', 'py': 'Grid_dn_color', 'param': None, 'type': 'color', 'default': 6908265, 'label': '', 'sinput': False}, {'mql': 'Grid_dn_Style', 'py': 'Grid_dn_Style', 'param': 'Grid_dn_Style', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
name_ = ""
prefix = ""
ciel_price = 0.0
floor_price = 0.0
range_ = 0.0
points = _input('points', 50)
number_of_levels = _input('number_of_levels', 50)
is_range = _input('is_range', True)  # Use Rectangle Range for Grid?
Grid_up_color = _input('Grid_up_color', clrDimGray)
Grid_up_Style = _input('Grid_up_Style', STYLE_DASHDOTDOT)
Grid_dn_color = _input('Grid_dn_color', clrDimGray)
Grid_dn_Style = _input('Grid_dn_Style', STYLE_DASHDOTDOT)

def OnInit():
    global prefix
    prefix = 'g_'
    ChartSetInteger(0, CHART_EVENT_OBJECT_CREATE, True)
    ChartSetInteger(0, CHART_EVENT_OBJECT_DELETE, True)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def DrawGrid():
    global ciel_price, floor_price, name_, range_
    ObjectsDeleteAll(0, prefix)
    name_ = ObjectName(0, 0, -1, OBJ_RECTANGLE)
    ciel_price = ObjectGetDouble(0, name_, OBJPROP_PRICE, 1)
    floor_price = ObjectGetDouble(0, name_, OBJPROP_PRICE, 0)
    range_ = ciel_price - floor_price
    for i in range(1, number_of_levels):
        if is_range == False:
            HLineCreate(0, prefix + 'Gridup_' + _str(i), 0, ciel_price + (i * points * Point()), Grid_up_color, Grid_up_Style, 1, True, False, True, 0)
            HLineCreate(0, prefix + 'Griddn_' + _str(i), 0, floor_price - (i * points * Point()), Grid_dn_color, Grid_dn_Style, 1, True, False, True, 0)
        else:
            HLineCreate(0, prefix + 'Gridup_' + _str(i), 0, ciel_price + (i * range_), Grid_up_color, Grid_up_Style, 1, True, False, True, 0)
            HLineCreate(0, prefix + 'Griddn_' + _str(i), 0, floor_price - (i * range_), Grid_dn_color, Grid_dn_Style, 1, True, False, True, 0)

def OnChartEvent(id_, lparam, dparam, sparam):
    global name_
    if id_ == CHARTEVENT_OBJECT_CREATE:
        if ObjectFind(0, ObjectName(0, 0, -1, OBJ_RECTANGLE)) != -1:
            DrawGrid()
    if id_ == CHARTEVENT_OBJECT_DRAG:
        if ObjectFind(0, ObjectName(0, 0, -1, OBJ_RECTANGLE)) != -1:
            ObjectsDeleteAll(0, prefix)
            DrawGrid()
        if id_ == CHARTEVENT_OBJECT_DELETE:
            if ObjectFind(0, ObjectName(0, 0, -1, OBJ_RECTANGLE)) == -1:
                ObjectsDeleteAll(0, prefix)
                name_ = ''

def HLineCreate(chart_ID=0, name='HLine', sub_window=0, price=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, hidden=True, z_order=0):
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_HLINE, sub_window, 0, price):
        Print('HLineCreate', ': failed to create a horizontal line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleGrids(_MQL5Indicator):
    name = 'Candle_Grids'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'points': 50,
        'number_of_levels': 50,
        'is_range': True,  # Use Rectangle Range for Grid?
        'Grid_up_Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),
        'Grid_dn_Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),
    }

