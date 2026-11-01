"""ID_Close_Rectangle_TL_AL — converted from MQL5: MQL5 Indicators/ID_Close_Rectangle_TL_AL/ID_Close_Rectangle_TL_AL.mq5

Copyright: Dina Paches; Link: https://login.mql5.com/ru/users/dipach; Version: 1.119

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Dina Paches', 'link': 'https://login.mql5.com/ru/users/dipach', 'version': '1.119', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ID_Close_Rectangle_TL_AL', 'source': 'MQL5 Indicators/ID_Close_Rectangle_TL_AL/ID_Close_Rectangle_TL_AL.mq5', 'folder': 'ID_Close_Rectangle_TL_AL', 'inputs': [{'mql': 'i_prefix_add_to_object_name', 'py': 'i_prefix_add_to_object_name', 'param': 'i_prefix_add_to_object_name', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'i_prefix_add_to_object_text', 'py': 'i_prefix_add_to_object_text', 'param': 'i_prefix_add_to_object_text', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'i_prefix_add_to_object_tooltip', 'py': 'i_prefix_add_to_object_tooltip', 'param': 'i_prefix_add_to_object_tooltip', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'i_alert_if_obj_inverted', 'py': 'i_alert_if_obj_inverted', 'param': 'i_alert_if_obj_inverted', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'i_font_size', 'py': 'i_font_size', 'param': 'i_font_size', 'type': 'uchar', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'i_y_distance', 'py': 'i_y_distance', 'param': 'i_y_distance', 'type': 'ushort', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'i_x_distance', 'py': 'i_x_distance', 'param': 'i_x_distance', 'type': 'ushort', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'i_button_size_base', 'py': 'i_button_size_base', 'param': 'i_button_size_base', 'type': 'ushort', 'default': 23, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
gp_name = ""
gp_t = 0
gp_t0 = 0
gp_t1 = 0
gp_p = 0.0
gp_p0 = 0.0
gp_p1 = 0.0
gp_prop_modif = 0
gp_ps = 0
gp_dig = 0
gp_type = 0
gp_prefix_add = False
gp_inverted = False
ge_flag_click = 0

def OnInit():
    global ge_flag_click, gp_dig, gp_prefix_add, gp_ps
    if not IndicatorShortNameSet('ID Cl RTA'):
        return INIT_FAILED
    InitVarStrct()
    ge_flag_click = STOP_
    gp_ps = PeriodSeconds()
    gp_dig = Digits()
    gp_prefix_add = (i_prefix_add_to_object_name or i_prefix_add_to_object_text) or i_prefix_add_to_object_tooltip
    PreparePanel()
    ge_flag_click = PANEL_
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'ID Cl RTA', 0)
    if reason == REASON_INITFAILED:
        ChIndicatorDelete('ID Cl RTA')
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global ge_flag_click
    if id_ == CHARTEVENT_OBJECT_CLICK:
        if ge_flag_click == STOP_:
            return
        if StringFind(sparam, 'ID Cl RTA') != 0:
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
                ChIndicatorDelete('ID Cl RTA')
    return

def ActionsIfObjClick(name, x, y):
    InitVarStrct(name)
    if not TypeObjCheck():
        return False
    ChartXYToTimeAndPrice(x, y)
    TimesObjGet()
    if gp_t0 > gp_t1:
        PreparePreInvertValues()
    if not FurtherActionsDependingOnTheObjectType():
        return False
    if gp_prefix_add:
        if not ActionsIfPrefixAddToObjText():
            return False
    InitVarStrct()
    return True

def Message(text):
    if i_alert_if_obj_inverted:
        Alert(text)
    else:
        Print(text)

def InitVarStrct(name=None):
    global gp_inverted, gp_name, gp_p, gp_p0, gp_p1, gp_prop_modif, gp_t, gp_t0, gp_t1, gp_type
    gp_name = name
    gp_t1 = 0
    gp_t0 = gp_t1
    gp_t = gp_t0
    gp_p1 = 0.0
    gp_p0 = gp_p1
    gp_p = gp_p0
    gp_prop_modif = 1
    gp_type = -1
    gp_inverted = False

def TypeObjCheck():
    global gp_type
    gp_type = ObjectGetInteger(0, gp_name, OBJPROP_TYPE)
    if (gp_type == OBJ_RECTANGLE or gp_type == OBJ_ARROWED_LINE) or gp_type == OBJ_TREND:
        return True
    Print('The object "', gp_name, '" is not a rectangle, a trend line or an arrowed line')
    return False

def TimesObjGet():
    global gp_t0, gp_t1
    gp_t0 = ObjectGetInteger(0, gp_name, OBJPROP_TIME, 0)
    gp_t1 = ObjectGetInteger(0, gp_name, OBJPROP_TIME, 1)

def PricesObjGet():
    global gp_p0, gp_p1
    gp_p0 = ObjectGetDouble(0, gp_name, OBJPROP_PRICE, 0)
    gp_p1 = ObjectGetDouble(0, gp_name, OBJPROP_PRICE, 1)

def PreparePreInvertValues():
    global gp_inverted, gp_prop_modif
    gp_inverted = True
    gp_prop_modif = 0
    Message(gp_name + ': first point time >= second point time')

def ChartXYToTimeAndPrice(x, y):
    sw = Box(0)
    ChartXYToTimePrice(0, x, y, sw, _GlobRef(globals(), 'gp_t'), _GlobRef(globals(), 'gp_p'))

def FurtherActionsDependingOnTheObjectType():
    global gp_t
    if gp_type == OBJ_RECTANGLE:
        if not ActionsIfRectangle():
            return False
    else:
        PricesObjGet()
        equal_t0_t1 = Equal_1(gp_t0, gp_t1)
        equal_p0_p1 = Equal_2(gp_p0, gp_p1)
        if equal_t0_t1:
            if equal_p0_p1:
                return False
            if not Equal_1(gp_t, gp_t1):
                gp_t = gp_t1
        if gp_type == OBJ_TREND:
            is_ray_right = (ObjectGetInteger(0, gp_name, OBJPROP_RAY_RIGHT) != 0)
            is_ray_left = (ObjectGetInteger(0, gp_name, OBJPROP_RAY_LEFT) != 0)
            if (not is_ray_left) and (not is_ray_right):
                if not ActionsIfLineHowArrowedLine(equal_t0_t1, equal_p0_p1):
                    return False
            else:
                if not ActionsIfTrendLine(equal_t0_t1, equal_p0_p1, is_ray_right, is_ray_left):
                    return False
        elif gp_type == OBJ_ARROWED_LINE:
            if not ActionsIfLineHowArrowedLine(equal_t0_t1, equal_p0_p1):
                return False
    return True

def Equal_1(t0, t1):
    return t0 == t1

def Equal_2(v0, v1):
    return NormalizeDouble(v0 - v1, gp_dig) == 0

def InvertValues(v0, v1):
    v_ch = v0.v
    v0.v = v1.v
    v1.v = v_ch

def ActionsIfRectangle():
    if Equal_1(gp_t0, gp_t1):
        Message(gp_name + ': time_0 and time_1 = same bar')
        return False
    if gp_inverted:
        InvertValues(_GlobRef(globals(), 'gp_t0'), _GlobRef(globals(), 'gp_t1'))
    if gp_t >= gp_t1:
        return False
    if not ObSetIntegerTimeMod(0, gp_name, gp_prop_modif, gp_t):
        return False
    return True

def ActionsIfLineHowArrowedLine(equal_t0_t1, equal_p0_p1):
    if gp_inverted:
        if not equal_t0_t1:
            InvertValues(_GlobRef(globals(), 'gp_t0'), _GlobRef(globals(), 'gp_t1'))
        if not equal_p0_p1:
            InvertValues(_GlobRef(globals(), 'gp_p0'), _GlobRef(globals(), 'gp_p1'))
    if Equal_1(gp_t, gp_t1) and Equal_2(gp_p, gp_p1):
        return False
    price_new_set = True
    time_new_set = True
    if equal_t0_t1:
        time_new_set = False
    elif equal_p0_p1:
        price_new_set = False
    if price_new_set:
        if not ObSetDoubleMod(0, gp_name, OBJPROP_PRICE, gp_prop_modif, NormalizeDouble(gp_p, gp_dig)):
            return False
    if time_new_set:
        if not ObSetIntegerTimeMod(0, gp_name, gp_prop_modif, gp_t):
            return False
    return True

def ActionsIfTrendLine(equal_t0_t1, equal_p0_p1, is_ray_right, is_ray_left):
    global gp_prefix_add
    is_ray_ls = is_ray_left
    if gp_inverted:
        if not equal_t0_t1:
            InvertValues(_GlobRef(globals(), 'gp_t0'), _GlobRef(globals(), 'gp_t1'))
        if not equal_p0_p1:
            InvertValues(_GlobRef(globals(), 'gp_p0'), _GlobRef(globals(), 'gp_p1'))
        is_ray_ls = is_ray_right
    res = Box(0)
    if equal_t0_t1:
        if not TrendLineVerticalChange(res, is_ray_ls):
            return False
    elif equal_p0_p1:
        if not TrendLineHorisontalChange(res, is_ray_ls):
            return False
    elif not TrendLineCrnrChange(res, is_ray_ls, equal_p0_p1):
        return False
    if not gp_inverted:
        if is_ray_right:
            if not ObSetIntegerBool(0, gp_name, OBJPROP_RAY_RIGHT, False):
                return False
        elif res.v == 8:
            if gp_prefix_add:
                gp_prefix_add = False
    else:
        if is_ray_left:
            if not ObSetIntegerBool(0, gp_name, OBJPROP_RAY_LEFT, False):
                return False
        elif res.v == 8:
            if gp_prefix_add:
                gp_prefix_add = False
    return True

def TrendLineHorisontalChange(res, is_ray_ls):
    time_new_set = True
    move_left_ray_h_c = False
    if gp_t == gp_t1:
        time_new_set = False
        res.v = 8
    elif gp_t < (gp_t0 + gp_ps):
        if is_ray_ls:
            move_left_ray_h_c = True
    if move_left_ray_h_c:
        if not MoveLeftRaytForLineHorizontalOrCorner():
            return False
    if time_new_set:
        if not ObSetIntegerTimeMod(0, gp_name, gp_prop_modif, gp_t):
            return False
    return True

def TrendLineCrnrChange(res, is_ray_ls, equal_p0_p1):
    p_set = False
    p_new_set = False
    time_new_set = True
    move_left_ray_h_c = False
    res.v = LittleDistanceCheckT()
    if gp_t > gp_t1:
        if not equal_p0_p1:
            if res.v == 5:
                p_set = True
            else:
                p_new_set = True
    elif gp_t == gp_t1:
        if Equal_2(gp_p, gp_p1):
            res.v = 8
            return True
        else:
            time_new_set = False
            p_set = True
    elif gp_t > (gp_t0 + gp_ps):
        if res.v == 5:
            p_set = True
        else:
            p_new_set = True
    else:
        if is_ray_ls:
            move_left_ray_h_c = True
            if res.v == 5:
                p_set = True
            else:
                p_new_set = True
    if move_left_ray_h_c:
        if not MoveLeftRaytForLineHorizontalOrCorner():
            return False
    if p_set:
        if not ObSetDoubleMod(0, gp_name, OBJPROP_PRICE, gp_prop_modif, NormalizeDouble(gp_p, gp_dig)):
            return False
    elif p_new_set:
        if not ObjPriceNewSet(gp_t, gp_prop_modif):
            return False
    if time_new_set or res.v != 8:
        if not ObSetIntegerTimeMod(0, gp_name, gp_prop_modif, gp_t):
            return False
    return True

def TrendLineVerticalChange(res, is_ray_ls):
    delta = gp_p1 - gp_p0
    move_left_point_v = False
    if NormalizeDouble(delta, gp_dig) > 0:
        delta = gp_p - gp_p1
        if NormalizeDouble(delta, gp_dig) == 0:
            res.v = 8
            return True
        elif delta < 0:
            delta = gp_p - gp_p0
            if NormalizeDouble(delta, gp_dig) <= 0 and is_ray_ls:
                move_left_point_v = True
                delta = Point() * 6
    else:
        delta = gp_p1 - gp_p
        if NormalizeDouble(delta, gp_dig) == 0:
            res.v = 8
            return True
        elif delta < 0:
            delta = gp_p0 - gp_p
            if NormalizeDouble(delta, gp_dig) <= 0 and is_ray_ls:
                move_left_point_v = True
                delta = -(Point() * 6)
    if not ObSetDoubleMod(0, gp_name, OBJPROP_PRICE, gp_prop_modif, NormalizeDouble(gp_p, gp_dig)):
        return False
    if move_left_point_v:
        if not MoveLeftRayForLineVertical(gp_p, delta):
            return False
    return True

def LittleDistanceCheckT():
    delta = gp_t1 - gp_t0
    if (gp_t > gp_t0 and (gp_t - gp_t0) <= delta) or (gp_t > gp_t1 and (gp_t - gp_t1) <= delta):
        return 5
    return 0

def MoveLeftRayForLineVertical(p, delta):
    prop_modif = (0 if (gp_prop_modif == 1) else 1)
    if not ObSetDoubleMod(0, gp_name, OBJPROP_PRICE, prop_modif, NormalizeDouble(p - delta, gp_dig)):
        return False
    return True

def MoveLeftRaytForLineHorizontalOrCorner():
    bars = Bars(Symbol(), Period(), gp_t, TimeCurrent())
    res = BarTimeGet(bars + 5, _GlobRef(globals(), 'gp_t0'))
    if res < bars:
        return False
    res = (0 if (gp_prop_modif == 1) else 1)
    if not ObjPriceNewSet(gp_t0, res):
        return False
    if not ObSetIntegerTimeMod(0, gp_name, res, gp_t0):
        return False
    return True

def BarTimeGet(bars, t):
    arr = Arr(0, 0)
    ArrayResize(arr, bars, bars)
    c = CopyTime(Symbol(), Period(), 0, bars, arr)
    if c < bars:
        Print('Error CopyTime')
        return c
    t.v = arr[0]
    return c

def ObjPriceNewSet(time, prop_modif):
    p = ObjectGetValueByTime(0, gp_name, time)
    if not ObSetDoubleMod(0, gp_name, OBJPROP_PRICE, prop_modif, NormalizeDouble(p, gp_dig)):
        return False
    return True

def ActionsIfPrefixAddToObjText():
    if i_prefix_add_to_object_text:
        if not PrefixAddToObjText(gp_name, 'cl ', _int(OBJPROP_TEXT)):
            return False
    if i_prefix_add_to_object_tooltip:
        if not PrefixAddToObjText(gp_name, 'cl ', _int(OBJPROP_TOOLTIP)):
            return False
    if i_prefix_add_to_object_name:
        if not PrefixAddToObjText(gp_name, 'cl ', _int(OBJPROP_NAME)):
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
        Print('Line: ', 546, ', ', 'IndicatorShortNameSet', ', Error Code = ', GetLastError())
        return False
    return True

def PreparePanel():
    ObjNameCreate(_GlobRef(globals(), 'gp_name_butt_work'), 'ID Cl RTA', 'cl ')
    ObjNameCreate(_GlobRef(globals(), 'gp_name_butt_del_ind'), 'ID Cl RTA', 'del ind')
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
        ButtonCreate(0, gp_name_butt_work, 0, x_dis, i_y_distance, w, h, CORNER_RIGHT_UPPER, 'Close R, TL, AL', '\n', 'Arial', fs, 0x3B3B3B, 0xE1DADA)
    return

def ChIndicatorDelete(sh_name):
    sw = ChartWindowFind()
    if not ChartIndicatorDelete(0, sw, sh_name):
        Print('Line: ', 594, ', ', 'ChIndicatorDelete', ', Error Code = ', GetLastError(), '. Failed to delete indicator:"', sh_name, '"')
        return False
    return True

def ObSetIntegerColor(chart_id, name, prop_id, prop_value):
    if not ObjectSetInteger(chart_id, name, prop_id, prop_value):
        Print('Line: ', 606, ', ', 'ObSetIntegerColor', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetIntegerTimeMod(chart_id, name, prop_modifier, prop_value):
    if not ObjectSetInteger(chart_id, name, OBJPROP_TIME, prop_modifier, prop_value):
        Print('Line: ', 615, ', ', 'ObSetIntegerTimeMod', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetDoubleMod(chart_id, name, prop_id, prop_modifier, prop_value):
    if not ObjectSetDouble(chart_id, name, prop_id, prop_modifier, prop_value):
        Print('Line: ', 625, ', ', 'ObSetDoubleMod', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetIntegerBool(chart_id, name, prop_id, prop_value):
    if not ObjectSetInteger(chart_id, name, prop_id, prop_value):
        Print('Line: ', 634, ', ', 'ObSetIntegerBool', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetString(chart_id, name, prop_id, prop_value):
    if not ObjectSetString(chart_id, name, prop_id, prop_value):
        Print('Line: ', 645, ', ', 'ObSetString', ', Error Code = ', GetLastError(), ', ', name, ', ', EnumToString(prop_id, 'ENUM_OBJECT_PROPERTY_STRING'))
        return False
    return True

def ObSetIntegerInt(chart_id, name, prop_id, prop_value):
    if not ObjectSetInteger(chart_id, name, prop_id, prop_value):
        Print('Line: ', 655, ', ', 'ObSetIntegerInt', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetIntegerCorner(chart_id, name, prop_value):
    if not ObjectSetInteger(chart_id, name, OBJPROP_CORNER, prop_value):
        Print('Line: ', 663, ', ', 'ObSetIntegerCorner', ', Error Code = ', GetLastError())
        return False
    return True

def ObSetIntegerLong(chart_id, name, prop_id, prop_value):
    if not ObjectSetInteger(chart_id, name, prop_id, prop_value):
        Print('Line: ', 672, ', ', 'ObSetIntegerLong', ', Error Code = ', GetLastError())
        return False
    return True

def ButtonCreate(chart_id=0, name='Button', sw=0, x=0, y=0, w=50, h=18, corner=CORNER_LEFT_UPPER, text='Button', toolTip='\n', font='Arial', fs=10, clr=clrBlack, back_clr=0xD8E9EC, border_clr=clrNONE, state=False, back=False, selection=False, hidden=True, z_order=0, tf=_int(OBJ_ALL_PERIODS)):
    if not ObjectCreate(chart_id, name, OBJ_BUTTON, sw, 0, 0):
        Print('Line: ', 698, ', ', 'ButtonCreate', ', Error Code = ', GetLastError())
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


class IDCloseRectangleTLAL(_MQL5Indicator):
    name = 'ID_Close_Rectangle_TL_AL'
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

