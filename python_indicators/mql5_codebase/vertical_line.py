"""Vertical_line — converted from MQL5: MQL5 Indicators/Vertical line/Vertical_line.mq5

Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Vertical_line', 'source': 'MQL5 Indicators/Vertical line/Vertical_line.mq5', 'folder': 'Vertical line', 'inputs': [{'mql': '_0_', 'py': '_0_', 'param': None, 'type': 'string', 'default': 'time setting', 'label': '*-*-*-*', 'sinput': True}, {'mql': 'InpTime', 'py': 'InpTime', 'param': None, 'type': 'datetime', 'default': 1495478400, 'label': 'Use only Hours and minutes', 'sinput': False}, {'mql': '_1_', 'py': '_1_', 'param': None, 'type': 'string', 'default': 'vertical line setting', 'label': '*-*-*-*', 'sinput': True}, {'mql': 'InpName', 'py': 'InpName', 'param': None, 'type': 'string', 'default': 'Vertical line', 'label': 'Line name', 'sinput': False}, {'mql': 'InpColor', 'py': 'InpColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Line color', 'sinput': False}, {'mql': 'InpStyle', 'py': 'InpStyle', 'param': 'InpStyle', 'type': 'int', 'default': 1, 'label': 'Line style', 'sinput': False}, {'mql': 'InpWidth', 'py': 'InpWidth', 'param': 'InpWidth', 'type': 'int', 'default': 3, 'label': 'Line width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
_0_ = _input('_0_', 'time setting')  # *-*-*-*
InpTime = _input('InpTime', 1495478400)  # Use only Hours and minutes
_1_ = _input('_1_', 'vertical line setting')  # *-*-*-*
InpName = _input('InpName', 'Vertical line')  # Line name
InpColor = _input('InpColor', clrRed)  # Line color
InpStyle = _input('InpStyle', STYLE_DASH)  # Line style
InpWidth = _input('InpWidth', 3)  # Line width
prev_date = 0

def OnInit():
    if not EventSetTimer(5):
        Print('Error create a Timer!')
        return INIT_FAILED
    if ObjectFind(0, InpName) < 0:
        VLineCreate(0, InpName, 0, _long(0.0), InpColor, InpStyle, InpWidth)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if reason == 1:
        VLineDelete(0, InpName)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global prev_date
    str_to_draw = MqlDateTime()
    TimeToStruct(TimeCurrent(), str_to_draw)
    if prev_date == 0:
        str_input = MqlDateTime()
        TimeToStruct(InpTime, str_input)
        str_to_draw.hour = str_input.hour
        str_to_draw.min = str_input.min
        str_to_draw.sec = 0
        prev_date = StructToTime(str_to_draw)
        VLineMove(0, InpName, prev_date)
        return rates_total
    str_prev_date = MqlDateTime()
    TimeToStruct(prev_date, str_prev_date)
    if str_to_draw.day == str_prev_date.day:
        return rates_total
    else:
        str_input = MqlDateTime()
        TimeToStruct(InpTime, str_input)
        str_to_draw.hour = str_input.hour
        str_to_draw.min = str_input.min
        str_to_draw.sec = 0
        prev_date = StructToTime(str_to_draw)
        VLineMove(0, InpName, prev_date)
    return rates_total

def OnTimer():
    global prev_date
    if ObjectFind(0, InpName) < 0:
        prev_date = 0
        VLineCreate(0, InpName, 0, _long(0.0), InpColor, InpStyle, InpWidth)

def VLineCreate(chart_ID=0, name='VLine', sub_window=0, time=0, clr=clrRed, style=STYLE_SOLID, width=1):
    if not time:
        time = TimeCurrent()
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_VLINE, sub_window, time, 0):
        Print('VLineCreate', ': failed to create a vertical line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    return True

def VLineMove(chart_ID=0, name='VLine', time=0):
    if not time:
        time = TimeCurrent()
    ResetLastError()
    if not ObjectMove(chart_ID, name, 0, time, 0):
        Print('VLineMove', ': failed to move the vertical line! Error code = ', GetLastError())
        return False
    return True

def VLineDelete(chart_ID=0, name='VLine'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('VLineDelete', ': failed to delete the vertical line! Error code = ', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VerticalLine(_MQL5Indicator):
    name = 'Vertical_line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # Line style
        'InpWidth': 3,  # Line width
    }

