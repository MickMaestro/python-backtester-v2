"""ServerTimeIndicator — converted from MQL5: MQL5 Indicators/ServerTime/ServerTimeIndicator.mq5

Copyright: Copyright 2025; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ServerTimeIndicator', 'source': 'MQL5 Indicators/ServerTime/ServerTimeIndicator.mq5', 'folder': 'ServerTime', 'inputs': [{'mql': 'ShowDailyChange', 'py': 'ShowDailyChange', 'param': 'ShowDailyChange', 'type': 'bool', 'default': True, 'label': 'Display daily variation', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 12, 'label': 'Font size', 'sinput': False}, {'mql': 'TextColor', 'py': 'TextColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Text color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ShowDailyChange = _input('ShowDailyChange', True)  # Display daily variation
FontSize = _input('FontSize', 12)  # Font size
TextColor = _input('TextColor', clrRed)  # Text color
obj_name = 'ServerTimeLabel'
obj_name_daily = 'DailyChangeLabel'

def OnInit():
    if not ObjectCreate(0, obj_name, OBJ_LABEL, 0, 0, 0):
        Print('Failed to create server time label: ', GetLastError())
        return INIT_FAILED
    ObjectSetInteger(0, obj_name, OBJPROP_XDISTANCE, 250)
    ObjectSetInteger(0, obj_name, OBJPROP_YDISTANCE, 10)
    ObjectSetInteger(0, obj_name, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, obj_name, OBJPROP_FONTSIZE, FontSize)
    ObjectSetInteger(0, obj_name, OBJPROP_COLOR, TextColor)
    ObjectSetString(0, obj_name, OBJPROP_FONT, 'Arial')
    if ShowDailyChange:
        if not ObjectCreate(0, obj_name_daily, OBJ_LABEL, 0, 0, 0):
            Print('Failed to create daily change label: ', GetLastError())
            return INIT_FAILED
        ObjectSetInteger(0, obj_name_daily, OBJPROP_XDISTANCE, 250)
        ObjectSetInteger(0, obj_name_daily, OBJPROP_YDISTANCE, 30)
        ObjectSetInteger(0, obj_name_daily, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
        ObjectSetInteger(0, obj_name_daily, OBJPROP_FONTSIZE, FontSize)
        ObjectSetInteger(0, obj_name_daily, OBJPROP_COLOR, TextColor)
        ObjectSetString(0, obj_name_daily, OBJPROP_FONT, 'Arial')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, obj_name)
    if ShowDailyChange:
        ObjectDelete(0, obj_name_daily)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    server_time = TimeToString(TimeCurrent(), (TIME_DATE | TIME_MINUTES) | TIME_SECONDS)
    ObjectSetString(0, obj_name, OBJPROP_TEXT, 'Server Time: ' + server_time)
    if ShowDailyChange:
        close_price = close[rates_total - 1]
        open_price = iOpen(Symbol(), PERIOD_D1, 0)
        change = _fdiv(close_price - open_price, open_price) * 100
        change_text = StringFormat('Daily Change: %.2f%%', change)
        ObjectSetString(0, obj_name_daily, OBJPROP_TEXT, change_text)
    return rates_total

def OnTimer():
    EventSetTimer(1)
    server_time = TimeToString(TimeCurrent(), (TIME_DATE | TIME_MINUTES) | TIME_SECONDS)
    ObjectSetString(0, obj_name, OBJPROP_TEXT, 'Server Time: ' + server_time)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ServerTimeIndicator(_MQL5Indicator):
    name = 'ServerTimeIndicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ShowDailyChange': True,  # Display daily variation
        'FontSize': 12,  # Font size
    }

