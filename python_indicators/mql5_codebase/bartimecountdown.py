"""BarTimeCountDown — converted from MQL5: MQL5 Indicators/Bar Time Count Down/BarTimeCountDown.mq5

Copyright: Copyright 2014,fxMeter.; Link: https://mql5.com/en/users/fxmeter; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014,fxMeter.', 'link': 'https://mql5.com/en/users/fxmeter', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'BarTimeCountDown', 'source': 'MQL5 Indicators/Bar Time Count Down/BarTimeCountDown.mq5', 'folder': 'Bar Time Count Down', 'inputs': [{'mql': 'LabelColor', 'py': 'LabelColor', 'param': None, 'type': 'color', 'default': 17919, 'label': '', 'sinput': False}, {'mql': 'LabelPosition', 'py': 'LabelPosition', 'param': 'LabelPosition', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_POS_TL
FOLLOW_PRICE = 0
FIXED_POSITION = 1
_enum('ENUM_POS_TL', {0: 'FOLLOW_PRICE', 1: 'FIXED_POSITION'})

# ---- inputs and global variables
LabelColor = _input('LabelColor', clrOrangeRed)
LabelPosition = _input('LabelPosition', FIXED_POSITION)

def DeleteLabel():
    try_ = 10
    while ObjectFind(0, 'time_left_label') == 0:
        ObjectDelete(0, 'time_left_label')
        if ((try_ := try_ - 1) + 1) <= 0:
            break

def OnInit():
    EventSetTimer(1)
    DeleteLabel()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    EventKillTimer()
    DeleteLabel()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnTimer():
    UpdateTimeLeft()

def UpdateTimeLeft():
    seconds = 0
    h = 0
    m = 0
    s = 0
    time = iTime(Symbol(), PERIOD_CURRENT, 0)
    close = iClose(Symbol(), PERIOD_CURRENT, 0)
    seconds = PeriodSeconds(PERIOD_CURRENT) - _int(TimeCurrent() - time)
    h = _idiv(seconds, 3600)
    m = _idiv(seconds - (h * 3600), 60)
    s = seconds - (h * 3600) - (m * 60)
    text = '  >>> ' + StringFormat('%02d', h) + ':' + StringFormat('%02d', m) + ':' + StringFormat('%02d', s)
    if LabelPosition == FOLLOW_PRICE:
        if ObjectFind(0, 'time_left_label') != 0:
            ObjectCreate(0, 'time_left_label', OBJ_TEXT, 0, time, close + Point())
            ObjectSetString(0, 'time_left_label', OBJPROP_TEXT, text)
            ObjectSetString(0, 'time_left_label', OBJPROP_FONT, 'Microsoft YaHei')
            ObjectSetInteger(0, 'time_left_label', OBJPROP_COLOR, LabelColor)
            ObjectSetInteger(0, 'time_left_label', OBJPROP_SELECTABLE, False)
            ObjectSetInteger(0, 'time_left_label', OBJPROP_FONTSIZE, 12)
        else:
            ObjectSetString(0, 'time_left_label', OBJPROP_TEXT, text)
            ObjectMove(0, 'time_left_label', 0, time, close + Point())
    elif LabelPosition == FIXED_POSITION:
        if ObjectFind(0, 'time_left_label') != 0:
            ObjectCreate(0, 'time_left_label', OBJ_LABEL, 0, 0, 0)
            ObjectSetInteger(0, 'time_left_label', OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
            ObjectSetInteger(0, 'time_left_label', OBJPROP_CORNER, CORNER_RIGHT_UPPER)
            ObjectSetInteger(0, 'time_left_label', OBJPROP_XDISTANCE, 200)
            ObjectSetInteger(0, 'time_left_label', OBJPROP_YDISTANCE, 2)
            ObjectSetString(0, 'time_left_label', OBJPROP_TEXT, text)
            ObjectSetString(0, 'time_left_label', OBJPROP_FONT, 'Microsoft YaHei')
            ObjectSetInteger(0, 'time_left_label', OBJPROP_COLOR, LabelColor)
            ObjectSetInteger(0, 'time_left_label', OBJPROP_SELECTABLE, True)
            ObjectSetInteger(0, 'time_left_label', OBJPROP_FONTSIZE, 12)
        else:
            ObjectSetString(0, 'time_left_label', OBJPROP_TEXT, text)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BarTimeCountDown(_MQL5Indicator):
    name = 'BarTimeCountDown'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LabelPosition': _Choice({0: 'FOLLOW_PRICE', 1: 'FIXED_POSITION'}, default=1),
    }

