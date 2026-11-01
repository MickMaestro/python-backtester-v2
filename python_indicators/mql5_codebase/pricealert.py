"""pricealert — converted from MQL5: MQL5 Indicators/PriceAlert/pricealert.mq5

The indicator gives signals in case of the horizontal level breakage
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The indicator gives signals in case of the horizontal level breakage'], 'name': 'pricealert', 'source': 'MQL5 Indicators/PriceAlert/pricealert.mq5', 'folder': 'PriceAlert', 'inputs': [{'mql': 'level_name', 'py': 'level_name', 'param': None, 'type': 'string', 'default': 'Price_Level_1', 'label': 'Actuation level name', 'sinput': False}, {'mql': 'level_comment', 'py': 'level_comment', 'param': None, 'type': 'string', 'default': 'actuation level', 'label': 'Actuation level comment', 'sinput': False}, {'mql': 'active_level_color', 'py': 'active_level_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Active level color', 'sinput': False}, {'mql': 'inactive_level_color', 'py': 'inactive_level_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Inactive level color', 'sinput': False}, {'mql': 'level_style', 'py': 'level_style', 'param': 'level_style', 'type': 'int', 'default': 0, 'label': 'Actuation level style', 'sinput': False}, {'mql': 'level_width', 'py': 'level_width', 'param': 'level_width', 'type': 'int', 'default': 3, 'label': 'Actuation level width', 'sinput': False}, {'mql': 'alert_mode', 'py': 'alert_mode', 'param': 'alert_mode', 'type': 'int', 'default': 1, 'label': 'Actuation indication version', 'sinput': False}, {'mql': 'AlertTotal', 'py': 'AlertTotal', 'param': 'AlertTotal', 'type': 'uint', 'default': 10, 'label': 'Number of alerts', 'sinput': False}, {'mql': 'Deletelevel', 'py': 'Deletelevel', 'param': 'Deletelevel', 'type': 'bool', 'default': True, 'label': 'Level deletion', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Gray = 0x808080  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

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
level_name = _input('level_name', 'Price_Level_1')  # Actuation level name
level_comment = _input('level_comment', 'actuation level')  # Actuation level comment
level_style = _input('level_style', STYLE_SOLID)  # Actuation level style
level_width = _input('level_width', w_3)  # Actuation level width
alert_mode = _input('alert_mode', OnlyAlert)  # Actuation indication version
AlertTotal = _input('AlertTotal', 10)  # Number of alerts
Deletelevel = _input('Deletelevel', True)  # Level deletion

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
    if ObjectFind(0, level_name) == -1:
        CreateHline(0, level_name, 0, 0.0, inactive_level_color, level_style, level_width, False, level_comment)

def OnDeinit(reason):
    if Deletelevel:
        ObjectDelete(0, level_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_count, _s_OnCalculate_oldlevel, _s_OnCalculate_startprice
    level = 0.0
    price0 = close[rates_total - 1]
    if ObjectFind(0, level_name) == -1:
        if _s_OnCalculate_count:
            CreateHline(0, level_name, 0, _s_OnCalculate_oldlevel, active_level_color, level_style, level_width, False, level_comment)
        else:
            CreateHline(0, level_name, 0, _s_OnCalculate_oldlevel, inactive_level_color, level_style, level_width, False, level_comment)
    if prev_calculated > rates_total or prev_calculated <= 0:
        level = ObjectGetDouble(0, level_name, OBJPROP_PRICE)
        if not level:
            level = price0
            SetHline(0, level_name, 0, level, inactive_level_color, level_style, level_width, False, level_comment)
            _s_OnCalculate_oldlevel = level
            _s_OnCalculate_count = 0
    level = ObjectGetDouble(0, level_name, OBJPROP_PRICE)
    if level != _s_OnCalculate_oldlevel:
        SetHline(0, level_name, 0, level, active_level_color, level_style, level_width, False, level_comment)
        _s_OnCalculate_oldlevel = level
        _s_OnCalculate_count = AlertTotal
        _s_OnCalculate_startprice = price0
    if _s_OnCalculate_count:
        if (price0 >= level and _s_OnCalculate_startprice < level) or (price0 <= level and _s_OnCalculate_startprice > level):
            if alert_mode == OnlyAlert:
                Alert('Level breakout ' + DoubleToString(level, Digits()))
            if alert_mode == OnlySound:
                PlaySound('alert.wav')
            _s_OnCalculate_count -= 1
            if not _s_OnCalculate_count:
                SetHline(0, level_name, 0, level, inactive_level_color, level_style, level_width, False, level_comment)
    return rates_total

# ---- global variables initialised from expressions
active_level_color = _input('active_level_color', _uint(Red))  # Active level color
inactive_level_color = _input('inactive_level_color', _uint(Gray))  # Inactive level color

# ---- static local variables
_s_OnCalculate_startprice = 0.0
_s_OnCalculate_oldlevel = 0.0
_s_OnCalculate_count = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pricealert(_MQL5Indicator):
    name = 'pricealert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'level_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Actuation level style
        'level_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Actuation level width
        'alert_mode': _Choice({0: 'only sound', 1: 'only alert'}, default=1),  # Actuation indication version
        'AlertTotal': 10,  # Number of alerts
        'Deletelevel': True,  # Level deletion
    }

