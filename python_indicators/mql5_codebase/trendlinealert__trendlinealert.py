"""trendlinealert — converted from MQL5: MQL5 Indicators/TrendLineAlert/trendlinealert.mq5

The indicator gives signals in case of a trend line breakout
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The indicator gives signals in case of a trend line breakout'], 'name': 'trendlinealert', 'source': 'MQL5 Indicators/TrendLineAlert/trendlinealert.mq5', 'folder': 'TrendLineAlert', 'inputs': [{'mql': 'level_name', 'py': 'level_name', 'param': None, 'type': 'string', 'default': 'Trend_Level_1', 'label': 'Actuation level name', 'sinput': False}, {'mql': 'level_comment', 'py': 'level_comment', 'param': None, 'type': 'string', 'default': 'trend level', 'label': 'Actuation level comment', 'sinput': False}, {'mql': 'active_level_color', 'py': 'active_level_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Active level color', 'sinput': False}, {'mql': 'inactive_level_color', 'py': 'inactive_level_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Inactive level color', 'sinput': False}, {'mql': 'level_style', 'py': 'level_style', 'param': 'level_style', 'type': 'int', 'default': 0, 'label': 'Actuation level style', 'sinput': False}, {'mql': 'level_width', 'py': 'level_width', 'param': 'level_width', 'type': 'int', 'default': 3, 'label': 'Actuation level width', 'sinput': False}, {'mql': 'alert_mode', 'py': 'alert_mode', 'param': 'alert_mode', 'type': 'int', 'default': 1, 'label': 'Actuation indication version', 'sinput': False}, {'mql': 'AlertTotal', 'py': 'AlertTotal', 'param': 'AlertTotal', 'type': 'uint', 'default': 10, 'label': 'Number of alerts', 'sinput': False}, {'mql': 'Deletelevel', 'py': 'Deletelevel', 'param': 'Deletelevel', 'type': 'bool', 'default': True, 'label': 'Level deletion', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
level_name = _input('level_name', 'Trend_Level_1')  # Actuation level name
level_comment = _input('level_comment', 'trend level')  # Actuation level comment
level_style = _input('level_style', STYLE_SOLID)  # Actuation level style
level_width = _input('level_width', w_3)  # Actuation level width
alert_mode = _input('alert_mode', OnlyAlert)  # Actuation indication version
AlertTotal = _input('AlertTotal', 10)  # Number of alerts
Deletelevel = _input('Deletelevel', True)  # Level deletion

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
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

def TlineMoveCheck(chart_id, name, nwin, time1, price1, time2, price2):
    global _s_TlineMoveCheck_price1_, _s_TlineMoveCheck_price2_, _s_TlineMoveCheck_time1_, _s_TlineMoveCheck_time2_
    if ObjectFind(chart_id, name) != -1:
        time1.v = ObjectGetInteger(chart_id, name, OBJPROP_TIME, 0)
        time2.v = ObjectGetInteger(chart_id, name, OBJPROP_TIME, 1)
        price1.v = ObjectGetDouble(chart_id, name, OBJPROP_PRICE, 0)
        price2.v = ObjectGetDouble(chart_id, name, OBJPROP_PRICE, 1)
        if ((time1.v != _s_TlineMoveCheck_time1_ or time2.v != _s_TlineMoveCheck_time2_) or price1.v != _s_TlineMoveCheck_price1_) or price2.v != _s_TlineMoveCheck_price2_:
            _s_TlineMoveCheck_time1_ = time1.v
            _s_TlineMoveCheck_time2_ = time2.v
            _s_TlineMoveCheck_price1_ = price1.v
            _s_TlineMoveCheck_price2_ = price2.v
            return True
    return False

def FindBar(endtbar, startbar, bartime, time):
    for bar in range(startbar, endtbar - 1, -1):
        if time[bar] <= bartime:
            return bar
    return endtbar

def OnInit():
    if ObjectFind(0, level_name) == -1:
        SetTline(0, level_name, 0, 0, 0.0, 0, 0.0, inactive_level_color, level_style, level_width, level_comment)

def OnDeinit(reason):
    if Deletelevel:
        ObjectDelete(0, level_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_K, _s_OnCalculate_bar1, _s_OnCalculate_bar2, _s_OnCalculate_count, _s_OnCalculate_dbar, _s_OnCalculate_price1, _s_OnCalculate_price2, _s_OnCalculate_startpos, _s_OnCalculate_time1, _s_OnCalculate_time2
    if rates_total < 20:
        return 0
    level = 0.0
    price0 = 0.0
    bar0 = 0
    if ObjectFind(0, level_name) == -1:
        if _s_OnCalculate_count:
            SetTline(0, level_name, 0, _s_OnCalculate_time1, _s_OnCalculate_price1, _s_OnCalculate_time2, _s_OnCalculate_price2, active_level_color, level_style, level_width, level_comment)
        else:
            SetTline(0, level_name, 0, _s_OnCalculate_time1, _s_OnCalculate_price1, _s_OnCalculate_time2, _s_OnCalculate_price2, inactive_level_color, level_style, level_width, level_comment)
    bar0 = rates_total - 1
    price0 = close[bar0]
    if prev_calculated > rates_total or prev_calculated <= 0:
        TlineMoveCheck(0, level_name, 0, _GlobRef(globals(), '_s_OnCalculate_time1'), _GlobRef(globals(), '_s_OnCalculate_price1'), _GlobRef(globals(), '_s_OnCalculate_time2'), _GlobRef(globals(), '_s_OnCalculate_price2'))
        if (((not _s_OnCalculate_price1) or (not _s_OnCalculate_price2)) or (not _s_OnCalculate_time1)) or (not _s_OnCalculate_time2):
            _s_OnCalculate_bar1 = rates_total - 20
            _s_OnCalculate_bar2 = rates_total - 1
            _s_OnCalculate_time1 = time[_s_OnCalculate_bar1]
            _s_OnCalculate_time2 = time[_s_OnCalculate_bar2]
            _s_OnCalculate_price1 = close[_s_OnCalculate_bar1]
            _s_OnCalculate_price2 = close[_s_OnCalculate_bar2]
            SetTline(0, level_name, 0, _s_OnCalculate_time1, _s_OnCalculate_price1, _s_OnCalculate_time2, _s_OnCalculate_price2, inactive_level_color, level_style, level_width, level_comment)
            TlineMoveCheck(0, level_name, 0, _GlobRef(globals(), '_s_OnCalculate_time1'), _GlobRef(globals(), '_s_OnCalculate_price1'), _GlobRef(globals(), '_s_OnCalculate_time2'), _GlobRef(globals(), '_s_OnCalculate_price2'))
            _s_OnCalculate_count = 0
    if TlineMoveCheck(0, level_name, 0, _GlobRef(globals(), '_s_OnCalculate_time1'), _GlobRef(globals(), '_s_OnCalculate_price1'), _GlobRef(globals(), '_s_OnCalculate_time2'), _GlobRef(globals(), '_s_OnCalculate_price2')):
        _s_OnCalculate_bar1 = FindBar(0, bar0, _s_OnCalculate_time1, time)
        _s_OnCalculate_time1 = time[_s_OnCalculate_bar1]
        _s_OnCalculate_bar2 = FindBar(0, bar0, _s_OnCalculate_time2, time)
        _s_OnCalculate_time2 = time[_s_OnCalculate_bar2]
        SetTline(0, level_name, 0, _s_OnCalculate_time1, _s_OnCalculate_price1, _s_OnCalculate_time2, _s_OnCalculate_price2, active_level_color, level_style, level_width, level_comment)
        _s_OnCalculate_count = AlertTotal
        _s_OnCalculate_dbar = _s_OnCalculate_bar2 - _s_OnCalculate_bar1
        if not _s_OnCalculate_dbar:
            _s_OnCalculate_dbar = 1
        _s_OnCalculate_K = _fdiv(_s_OnCalculate_price2 - _s_OnCalculate_price1, _s_OnCalculate_dbar)
        level = (_s_OnCalculate_K * (bar0 - _s_OnCalculate_bar1)) + _s_OnCalculate_price1
        if price0 > level:
            _s_OnCalculate_startpos = 1
        else:
            _s_OnCalculate_startpos = -1
    level = (_s_OnCalculate_K * (bar0 - _s_OnCalculate_bar1)) + _s_OnCalculate_price1
    if _s_OnCalculate_count:
        if (price0 >= level and _s_OnCalculate_startpos < 0) or (price0 <= level and _s_OnCalculate_startpos > 0):
            if alert_mode == OnlyAlert:
                Alert('Trend line breakout at the level ' + DoubleToString(level, Digits()))
            if alert_mode == OnlySound:
                PlaySound('alert.wav')
            _s_OnCalculate_count -= 1
            if not _s_OnCalculate_count:
                SetTline(0, level_name, 0, _s_OnCalculate_time1, _s_OnCalculate_price1, _s_OnCalculate_time2, _s_OnCalculate_price2, inactive_level_color, level_style, level_width, level_comment)
    return rates_total

# ---- global variables initialised from expressions
active_level_color = _input('active_level_color', _uint(Red))  # Active level color
inactive_level_color = _input('inactive_level_color', _uint(Gray))  # Inactive level color

# ---- static local variables
_s_TlineMoveCheck_price1_ = 0.0
_s_TlineMoveCheck_price2_ = 0.0
_s_TlineMoveCheck_time1_ = 0
_s_TlineMoveCheck_time2_ = 0
_s_OnCalculate_price2 = 0.0
_s_OnCalculate_price1 = 0.0
_s_OnCalculate_K = 0.0
_s_OnCalculate_time1 = 0
_s_OnCalculate_time2 = 0
_s_OnCalculate_count = 0
_s_OnCalculate_bar1 = 0
_s_OnCalculate_bar2 = 0
_s_OnCalculate_dbar = 0
_s_OnCalculate_startpos = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendlinealert(_MQL5Indicator):
    name = 'trendlinealert'
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

