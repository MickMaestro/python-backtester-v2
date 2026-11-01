"""ID_Close_Rectangle — converted from MQL5: MQL5 Indicators/ID_Close_Rectangle/ID_Close_Rectangle.mq5

Copyright: Dina Paches; Link: https://login.mql5.com/ru/users/dipach; Version: 1.008

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Dina Paches', 'link': 'https://login.mql5.com/ru/users/dipach', 'version': '1.008', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ID_Close_Rectangle', 'source': 'MQL5 Indicators/ID_Close_Rectangle/ID_Close_Rectangle.mq5', 'folder': 'ID_Close_Rectangle', 'inputs': [{'mql': 'i_prefix_add_to_object_name', 'py': 'i_prefix_add_to_object_name', 'param': 'i_prefix_add_to_object_name', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'i_prefix_add_to_object_text', 'py': 'i_prefix_add_to_object_text', 'param': 'i_prefix_add_to_object_text', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'i_prefix_add_to_object_tooltip', 'py': 'i_prefix_add_to_object_tooltip', 'param': 'i_prefix_add_to_object_tooltip', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'i_alert_if_obj_inverted', 'py': 'i_alert_if_obj_inverted', 'param': 'i_alert_if_obj_inverted', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'i_font_size', 'py': 'i_font_size', 'param': 'i_font_size', 'type': 'uchar', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'i_y_distance', 'py': 'i_y_distance', 'param': 'i_y_distance', 'type': 'ushort', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'i_x_distance', 'py': 'i_x_distance', 'param': 'i_x_distance', 'type': 'ushort', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'i_button_size_base', 'py': 'i_button_size_base', 'param': 'i_button_size_base', 'type': 'ushort', 'default': 23, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter

# enum enum_Flag_click
STOP_ = 0
PANEL_ = 1
CHART_ = 2
_enum('enum_Flag_click', {0: 'STOP_', 1: 'PANEL_', 2: 'CHART_'})

# ---- inputs and global variables
i_prefix_add_to_object_name = _input('i_prefix_add_to_object_name', True)
i_prefix_add_to_object_text = _input('i_prefix_add_to_object_text', True)
i_prefix_add_to_object_tooltip = _input('i_prefix_add_to_object_tooltip', False)
i_alert_if_obj_inverted = _input('i_alert_if_obj_inverted', False)
i_font_size = _input('i_font_size', 10)
i_y_distance = _input('i_y_distance', 5)
i_x_distance = _input('i_x_distance', 5)
i_button_size_base = _input('i_button_size_base', 23)
gp_name_butt_work = ""
gp_name_butt_del_ind = ""
gp_prefix_add = False
ge_flag_click = 0

def OnInit():
    global ge_flag_click, gp_prefix_add
    if not IndicatorShortNameSet('ID Cl R'):
        return INIT_FAILED
    ge_flag_click = STOP_
    gp_prefix_add = (i_prefix_add_to_object_name or i_prefix_add_to_object_text) or i_prefix_add_to_object_tooltip
    PreparePanel()
    ge_flag_click = PANEL_
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'ID Cl R', 0)
    if reason == REASON_INITFAILED:
        ChIndicatorDelete('ID Cl R')
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global ge_flag_click
    if id_ == CHARTEVENT_OBJECT_CLICK:
        if ge_flag_click == STOP_:
            return
        if StringFind(sparam, 'ID Cl R') != 0:
            if ge_flag_click == PANEL_:
                return
            if not ActionsIfObjClick(sparam, _int(lparam), _int(dparam)):
                return
            ObSetIntegerColor(0, gp_name_butt_work, OBJPROP_BGCOLOR, 0xE1DADA)
            ObSetIntegerBool(0, gp_name_butt_work, OBJPROP_STATE, False)
            ge_flag_click = PANEL_
            ChartRedraw()
        else:
            if StringCompare(sparam, gp_name_butt_work) == 0:
                butt_state = (ObjectGetInteger(0, gp_name_butt_work, OBJPROP_STATE) != 0)
                butt_clr = clrAntiqueWhite
                if butt_state:
                    ge_flag_click = CHART_
                else:
                    ge_flag_click = PANEL_
                    butt_clr = 0xE1DADA
                ObSetIntegerColor(0, gp_name_butt_work, OBJPROP_BGCOLOR, butt_clr)
                ChartRedraw()
            else:
                ge_flag_click = STOP_
                ChIndicatorDelete('ID Cl R')
    return

def ActionsIfObjClick(name, x, y):
    if not TypeObjCheck(name):
        return False
    t = Box(0)
    ChartXYToTime(x, y, t)
    if not ActionsIfRectangle(name, t.v):
        return False
    if gp_prefix_add:
        if not ActionsIfPrefixAddToObjText(name):
            return False
    return True

def Message(text):
    if i_alert_if_obj_inverted:
        Alert(text)
    else:
        Print(text)

def TypeObjCheck(name):
    type_ = ObjectGetInteger(0, name, OBJPROP_TYPE)
    if type_ == OBJ_RECTANGLE:
        return True
    Print('The object "', name, '" is not a rectangle')
    return False

def ChartXYToTime(x, y, t):
    p = Box(0.0)
    sw = Box(0)
    ChartXYToTimePrice(0, x, y, sw, t, p)

def ActionsIfRectangle(name, t):
    t0 = Box(0)
    t1 = Box(0)
    prop_modif = Box(1)
    inverted = Box(False)
    TimesObjGet(name, t0, t1)
    if t0.v > t1.v:
        PreparePreInvertValues(prop_modif, inverted)
        InvertValues(t0, t1)
        Message(name + ': first point time >= second point time')
    elif t0.v == t1.v:
        Message(name + ': time_0 and time_1 = same bar')
        return False
    if t >= t1.v:
        return False
    if not ObSetIntegerTimeMod(0, name, prop_modif.v, t):
        return False
    return True

def TimesObjGet(name, t0, t1):
    t0.v = ObjectGetInteger(0, name, OBJPROP_TIME, 0)
    t1.v = ObjectGetInteger(0, name, OBJPROP_TIME, 1)

def PreparePreInvertValues(prop_modif, inverted):
    prop_modif.v = 0
    inverted.v = True

def InvertValues(v0, v1):
    v_ch = v0.v
    v0.v = v1.v
    v1.v = v_ch

def ActionsIfPrefixAddToObjText(name):
    if i_prefix_add_to_object_text:
        if not PrefixAddToObjText(name, 'cl ', _int(OBJPROP_TEXT)):
            return False
    if i_prefix_add_to_object_tooltip:
        if not PrefixAddToObjText(name, 'cl ', _int(OBJPROP_TOOLTIP)):
            return False
    if i_prefix_add_to_object_name:
        if not PrefixAddToObjText(name, 'cl ', _int(OBJPROP_NAME)):
            return False
    return True

def PrefixAddToObjText(name, prefix, prop_string):
    text = Box(ObjectGetString(0, name, prop_string))
    StringConcatenate(text, prefix, text.v)
    if not ObSetString(0, name, prop_string, text.v):
        return False
    return True

def IndicatorShortNameSet(name):
    if not IndicatorSetString(INDICATOR_SHORTNAME, name):
        Print('Line: ', 235, ', ', 'IndicatorShortNameSet', ', Error Code = ', GetLastError())
        return False
    return True

def PreparePanel():
    ObjNameCreate(_GlobRef(globals(), 'gp_name_butt_work'), 'ID Cl R', 'cl ')
    ObjNameCreate(_GlobRef(globals(), 'gp_name_butt_del_ind'), 'ID Cl R', 'del ind')
    PanelCreate()
    return

def ObjNameCreate(name, prefix, dt):
    return StringConcatenate(name, prefix, '_', dt)

def PanelCreate():
    fs = (6 if (i_font_size < 6) else i_font_size)
    w = i_button_size_base
    h = i_button_size_base * _idiv(fs + _imod(fs, 11), 11)
    x_dis = i_x_distance + w
    if ObjectFind(0, gp_name_butt_del_ind) < 0:
        ButtonCreate(0, gp_name_butt_del_ind, 0, x_dis, i_y_distance, w, h, CORNER_RIGHT_UPPER, CharToString(251), '\n', 'Wingdings', fs, 0x3B3B3B, 0xB9B9EB)
    w *= _idiv(fs + _imod(fs, 2), 2)
    x_dis = i_x_distance + w + i_button_size_base
    if ObjectFind(0, gp_name_butt_work) < 0:
        ButtonCreate(0, gp_name_butt_work, 0, x_dis, i_y_distance, w, h, CORNER_RIGHT_UPPER, 'Close Rectangle', '\n', 'Arial', fs, 0x3B3B3B, 0xE1DADA)
    return

def ChIndicatorDelete(sh_name):
    sw = ChartWindowFind()
    if not ChartIndicatorDelete(0, sw, sh_name):
        Print('Line: ', 283, ', ', 'ChIndicatorDelete', ', Error Code = ', GetLastError(), '. Failed to delete indicator:"', sh_name, '"')
        return False
    return True

def ObSetIntegerColor(chart_id, name, prop_id, prop_value):
    if not ObjectSetInteger(chart_id, name, prop_id, prop_value):
        Print('Line: ', 295, ', ', 'ObSetIntegerColor', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetIntegerTimeMod(chart_id, name, prop_modifier, prop_value):
    if not ObjectSetInteger(chart_id, name, OBJPROP_TIME, prop_modifier, prop_value):
        Print('Line: ', 304, ', ', 'ObSetIntegerTimeMod', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetIntegerBool(chart_id, name, prop_id, prop_value):
    if not ObjectSetInteger(chart_id, name, prop_id, prop_value):
        Print('Line: ', 313, ', ', 'ObSetIntegerBool', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetString(chart_id, name, prop_id, prop_value):
    if not ObjectSetString(chart_id, name, prop_id, prop_value):
        Print('Line: ', 323, ', ', 'ObSetString', ', Error Code = ', GetLastError(), ', ', name, ', ', EnumToString(prop_id, 'ENUM_OBJECT_PROPERTY_STRING'))
        return False
    return True

def ObSetIntegerInt(chart_id, name, prop_id, prop_value):
    if not ObjectSetInteger(chart_id, name, prop_id, prop_value):
        Print('Line: ', 332, ', ', 'ObSetIntegerInt', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetIntegerCorner(chart_id, name, prop_value):
    if not ObjectSetInteger(chart_id, name, OBJPROP_CORNER, prop_value):
        Print('Line: ', 340, ', ', 'ObSetIntegerCorner', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetIntegerLong(chart_id, name, prop_id, prop_value):
    if not ObjectSetInteger(chart_id, name, prop_id, prop_value):
        Print('Line: ', 349, ', ', 'ObSetIntegerLong', ', Error Code = ', GetLastError())
        return False
    return True

def ButtonCreate(chart_id=0, name='Button', sw=0, x=0, y=0, w=50, h=18, corner=CORNER_LEFT_UPPER, text='Button', toolTip='\n', font='Arial', fs=10, clr=clrBlack, back_clr=0xD8E9EC, border_clr=clrNONE, state=False, back=False, selection=False, hidden=True, z_order=0, tf=_int(OBJ_ALL_PERIODS)):
    if not ObjectCreate(chart_id, name, OBJ_BUTTON, sw, 0, 0):
        Print('Line: ', 375, ', ', 'ButtonCreate', ', Error Code = ', GetLastError())
        return False
    ObSetIntegerInt(chart_id, name, OBJPROP_XDISTANCE, x)
    ObSetIntegerInt(chart_id, name, OBJPROP_YDISTANCE, y)
    ObSetIntegerInt(chart_id, name, OBJPROP_XSIZE, w)
    ObSetIntegerInt(chart_id, name, OBJPROP_YSIZE, h)
    ObSetIntegerCorner(chart_id, name, corner)
    ObSetString(chart_id, name, _int(OBJPROP_TEXT), text)
    ObSetString(chart_id, name, _int(OBJPROP_FONT), font)
    ObSetIntegerInt(chart_id, name, OBJPROP_FONTSIZE, fs)
    ObSetString(chart_id, name, _int(OBJPROP_TOOLTIP), toolTip)
    ObSetIntegerColor(chart_id, name, OBJPROP_COLOR, clr)
    ObSetIntegerColor(chart_id, name, OBJPROP_BGCOLOR, back_clr)
    ObSetIntegerColor(chart_id, name, OBJPROP_BORDER_COLOR, border_clr)
    ObSetIntegerBool(chart_id, name, OBJPROP_BACK, back)
    ObSetIntegerBool(chart_id, name, OBJPROP_STATE, state)
    ObSetIntegerBool(chart_id, name, OBJPROP_SELECTABLE, selection)
    ObSetIntegerBool(chart_id, name, OBJPROP_SELECTED, selection)
    ObSetIntegerBool(chart_id, name, OBJPROP_HIDDEN, hidden)
    ObSetIntegerLong(chart_id, name, OBJPROP_ZORDER, z_order)
    ObSetIntegerInt(chart_id, name, OBJPROP_TIMEFRAMES, tf)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IDCloseRectangle(_MQL5Indicator):
    name = 'ID_Close_Rectangle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'i_prefix_add_to_object_name': True,
        'i_prefix_add_to_object_text': True,
        'i_prefix_add_to_object_tooltip': False,
        'i_alert_if_obj_inverted': False,
        'i_font_size': 10,
        'i_y_distance': 5,
        'i_x_distance': 5,
        'i_button_size_base': 23,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

