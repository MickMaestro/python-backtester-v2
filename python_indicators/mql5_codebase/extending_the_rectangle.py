"""Extending the Rectangle — converted from MQL5: MQL5 Indicators/Extending the Rectangle/Extending the Rectangle.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Extending the Rectangle', 'source': 'MQL5 Indicators/Extending the Rectangle/Extending the Rectangle.mq5', 'folder': 'Extending the Rectangle', 'inputs': [{'mql': 'InpPrefix', 'py': 'InpPrefix', 'param': None, 'type': 'string', 'default': 'Rect_', 'label': 'Watch for a rectangle whose name starts with ...', 'sinput': False}, {'mql': 'Inp_Up_Prefix', 'py': 'Inp_Up_Prefix', 'param': None, 'type': 'string', 'default': 'Up Line', 'label': '"Up Line": Prefix', 'sinput': True}, {'mql': 'Inp_Up_Color', 'py': 'Inp_Up_Color', 'param': None, 'type': 'color', 'default': 13850042, 'label': '"Up Line": Line color', 'sinput': True}, {'mql': 'Inp_Up_Style', 'py': 'Inp_Up_Style', 'param': 'Inp_Up_Style', 'type': 'int', 'default': 1, 'label': '"Up Line": Line style', 'sinput': True}, {'mql': 'Inp_Up_Width', 'py': 'Inp_Up_Width', 'param': 'Inp_Up_Width', 'type': 'int', 'default': 2, 'label': '"Up Line": Line width', 'sinput': True}, {'mql': 'Inp_Up_Back', 'py': 'Inp_Up_Back', 'param': 'Inp_Up_Back', 'type': 'bool', 'default': False, 'label': '"Up Line": Background line', 'sinput': True}, {'mql': 'Inp_Up_Selection', 'py': 'Inp_Up_Selection', 'param': 'Inp_Up_Selection', 'type': 'bool', 'default': False, 'label': '"Up Line": Highlight to move', 'sinput': True}, {'mql': 'Inp_Up_RayLeft', 'py': 'Inp_Up_RayLeft', 'param': 'Inp_Up_RayLeft', 'type': 'bool', 'default': False, 'label': '"Up Line": Line\'s continuation to the left', 'sinput': True}, {'mql': 'Inp_Up_RayRight', 'py': 'Inp_Up_RayRight', 'param': 'Inp_Up_RayRight', 'type': 'bool', 'default': False, 'label': '"Up Line": Line\'s continuation to the right', 'sinput': True}, {'mql': 'Inp_Up_Hidden', 'py': 'Inp_Up_Hidden', 'param': 'Inp_Up_Hidden', 'type': 'bool', 'default': True, 'label': '"Up Line": Hidden in the object list', 'sinput': True}, {'mql': 'Inp_Up_ZOrder', 'py': 'Inp_Up_ZOrder', 'param': 'Inp_Up_ZOrder', 'type': 'long', 'default': 0, 'label': '"Up Line": Priority for mouse click', 'sinput': True}, {'mql': 'Inp_Down_Prefix', 'py': 'Inp_Down_Prefix', 'param': None, 'type': 'string', 'default': 'Down Line', 'label': '"Down Line": Prefix', 'sinput': True}, {'mql': 'Inp_Down_Color', 'py': 'Inp_Down_Color', 'param': None, 'type': 'color', 'default': 13850042, 'label': '"Down Line": Line color', 'sinput': True}, {'mql': 'Inp_Down_Style', 'py': 'Inp_Down_Style', 'param': 'Inp_Down_Style', 'type': 'int', 'default': 1, 'label': '"Down Line": Line style', 'sinput': True}, {'mql': 'Inp_Down_Width', 'py': 'Inp_Down_Width', 'param': 'Inp_Down_Width', 'type': 'int', 'default': 2, 'label': '"Down Line": Line width', 'sinput': True}, {'mql': 'Inp_Down_Back', 'py': 'Inp_Down_Back', 'param': 'Inp_Down_Back', 'type': 'bool', 'default': False, 'label': '"Down Line": Background line', 'sinput': True}, {'mql': 'Inp_Down_Selection', 'py': 'Inp_Down_Selection', 'param': 'Inp_Down_Selection', 'type': 'bool', 'default': False, 'label': '"Down Line": Highlight to move', 'sinput': True}, {'mql': 'Inp_Down_RayLeft', 'py': 'Inp_Down_RayLeft', 'param': 'Inp_Down_RayLeft', 'type': 'bool', 'default': False, 'label': '"Down Line": Line\'s continuation to the left', 'sinput': True}, {'mql': 'Inp_Down_RayRight', 'py': 'Inp_Down_RayRight', 'param': 'Inp_Down_RayRight', 'type': 'bool', 'default': False, 'label': '"Down Line": Line\'s continuation to the right', 'sinput': True}, {'mql': 'Inp_Down_Hidden', 'py': 'Inp_Down_Hidden', 'param': 'Inp_Down_Hidden', 'type': 'bool', 'default': True, 'label': '"Down Line": Hidden in the object list', 'sinput': True}, {'mql': 'Inp_Down_ZOrder', 'py': 'Inp_Down_ZOrder', 'param': 'Inp_Down_ZOrder', 'type': 'long', 'default': 0, 'label': '"Down Line": Priority for mouse click', 'sinput': True}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPrefix = _input('InpPrefix', 'Rect_')  # Watch for a rectangle whose name starts with ...
Inp_Up_Prefix = _input('Inp_Up_Prefix', 'Up Line')  # "Up Line": Prefix
Inp_Up_Color = _input('Inp_Up_Color', clrMediumOrchid)  # "Up Line": Line color
Inp_Up_Style = _input('Inp_Up_Style', STYLE_DASH)  # "Up Line": Line style
Inp_Up_Width = _input('Inp_Up_Width', 2)  # "Up Line": Line width
Inp_Up_Back = _input('Inp_Up_Back', False)  # "Up Line": Background line
Inp_Up_Selection = _input('Inp_Up_Selection', False)  # "Up Line": Highlight to move
Inp_Up_RayLeft = _input('Inp_Up_RayLeft', False)  # "Up Line": Line's continuation to the left
Inp_Up_RayRight = _input('Inp_Up_RayRight', False)  # "Up Line": Line's continuation to the right
Inp_Up_Hidden = _input('Inp_Up_Hidden', True)  # "Up Line": Hidden in the object list
Inp_Up_ZOrder = _input('Inp_Up_ZOrder', 0)  # "Up Line": Priority for mouse click
Inp_Down_Prefix = _input('Inp_Down_Prefix', 'Down Line')  # "Down Line": Prefix
Inp_Down_Color = _input('Inp_Down_Color', clrMediumOrchid)  # "Down Line": Line color
Inp_Down_Style = _input('Inp_Down_Style', STYLE_DASH)  # "Down Line": Line style
Inp_Down_Width = _input('Inp_Down_Width', 2)  # "Down Line": Line width
Inp_Down_Back = _input('Inp_Down_Back', False)  # "Down Line": Background line
Inp_Down_Selection = _input('Inp_Down_Selection', False)  # "Down Line": Highlight to move
Inp_Down_RayLeft = _input('Inp_Down_RayLeft', False)  # "Down Line": Line's continuation to the left
Inp_Down_RayRight = _input('Inp_Down_RayRight', False)  # "Down Line": Line's continuation to the right
Inp_Down_Hidden = _input('Inp_Down_Hidden', True)  # "Down Line": Hidden in the object list
Inp_Down_ZOrder = _input('Inp_Down_ZOrder', 0)  # "Down Line": Priority for mouse click

def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if (id_ == CHARTEVENT_OBJECT_CREATE or id_ == CHARTEVENT_OBJECT_CHANGE) or id_ == CHARTEVENT_OBJECT_DRAG:
        if StringFind(sparam, InpPrefix, 0) != 0:
            return
        if id_ == CHARTEVENT_OBJECT_CREATE:
            Print('Created object named ', sparam)
        if id_ == CHARTEVENT_OBJECT_CHANGE:
            Print('Changed object named ', sparam)
        if id_ == CHARTEVENT_OBJECT_DRAG:
            Print('Changing anchor points of object named ', sparam)
        postfix = StringSubstr(sparam, StringLen(InpPrefix) - 1, -1)
        chart_id = ChartID()
        price_modifier_0 = ObjectGetDouble(chart_id, sparam, OBJPROP_PRICE, 0)
        price_modifier_1 = ObjectGetDouble(chart_id, sparam, OBJPROP_PRICE, 1)
        price_up = 0.0
        price_down = 0.0
        if price_modifier_0 > price_modifier_1:
            price_up = price_modifier_0
            price_down = price_modifier_1
        else:
            price_up = price_modifier_1
            price_down = price_modifier_0
        time_modifier_0 = ObjectGetInteger(chart_id, sparam, OBJPROP_TIME, 0)
        time_modifier_1 = ObjectGetInteger(chart_id, sparam, OBJPROP_TIME, 1)
        time_left = (time_modifier_0 if (time_modifier_0 > time_modifier_1) else time_modifier_1)
        time_right = TimeCurrent()
        Print('time_left ', time_left, ', time_right ', time_right)
        if ObjectFind(chart_id, Inp_Up_Prefix + postfix) != 0:
            if TrendCreate(chart_id, Inp_Up_Prefix + postfix, 0, time_left, price_up, time_right, price_up, Inp_Up_Color, Inp_Up_Style, Inp_Up_Width, Inp_Up_Back, Inp_Up_Selection, Inp_Up_RayLeft, Inp_Up_RayRight, Inp_Up_Hidden, Inp_Up_ZOrder):
                Print("Create '", Inp_Up_Prefix, "' OK")
                ChartRedraw()
            else:
                Print("Create '", Inp_Up_Prefix, "' ERROR")
        else:
            TrendPointChange(chart_id, Inp_Up_Prefix + postfix, 0, time_left, price_up)
            TrendPointChange(chart_id, Inp_Up_Prefix + postfix, 1, time_right, price_up)
            ChartRedraw()
        if ObjectFind(chart_id, Inp_Down_Prefix + postfix) != 0:
            if TrendCreate(chart_id, Inp_Down_Prefix + postfix, 0, time_left, price_down, time_right, price_down, Inp_Down_Color, Inp_Down_Style, Inp_Down_Width, Inp_Down_Back, Inp_Down_Selection, Inp_Down_RayLeft, Inp_Down_RayRight, Inp_Down_Hidden, Inp_Down_ZOrder):
                Print("Create '", Inp_Down_Prefix, "' OK")
                ChartRedraw()
            else:
                Print("Create '", Inp_Down_Prefix, "' ERROR")
        else:
            TrendPointChange(chart_id, Inp_Down_Prefix + postfix, 0, time_left, price_down)
            TrendPointChange(chart_id, Inp_Down_Prefix + postfix, 1, time_right, price_down)
            ChartRedraw()

def TrendCreate(chart_ID=0, name='TrendLine', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=2, back=False, selection=False, ray_left=False, ray_right=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_TREND, sub_window, time1, price1, time2, price2):
        Print('TrendCreate', ': failed to create a trend line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_LEFT, ray_left)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_RIGHT, ray_right)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def TrendPointChange(chart_ID=0, name='TrendLine', point_index=0, time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, point_index, time, price):
        Print('TrendPointChange', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ExtendingTheRectangle(_MQL5Indicator):
    name = 'Extending the Rectangle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_Up_Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # "Up Line": Line style
        'Inp_Up_Width': 2,  # "Up Line": Line width
        'Inp_Up_Back': False,  # "Up Line": Background line
        'Inp_Up_Selection': False,  # "Up Line": Highlight to move
        'Inp_Up_RayLeft': False,  # "Up Line": Line's continuation to the left
        'Inp_Up_RayRight': False,  # "Up Line": Line's continuation to the right
        'Inp_Up_Hidden': True,  # "Up Line": Hidden in the object list
        'Inp_Up_ZOrder': 0,  # "Up Line": Priority for mouse click
        'Inp_Down_Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # "Down Line": Line style
        'Inp_Down_Width': 2,  # "Down Line": Line width
        'Inp_Down_Back': False,  # "Down Line": Background line
        'Inp_Down_Selection': False,  # "Down Line": Highlight to move
        'Inp_Down_RayLeft': False,  # "Down Line": Line's continuation to the left
        'Inp_Down_RayRight': False,  # "Down Line": Line's continuation to the right
        'Inp_Down_Hidden': True,  # "Down Line": Hidden in the object list
        'Inp_Down_ZOrder': 0,  # "Down Line": Priority for mouse click
    }

