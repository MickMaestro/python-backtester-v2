"""candle-closing-time-remaining-cctr-v3 — converted from MQL5: MQL5 Indicators/Candle Closing Time Remaining (CCTR) MT5/candle-closing-time-remaining-cctr-v3.mq5

Copyright: Copyright 2013-2018,Foad Tahmasebi; Version: 3.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013-2018,Foad Tahmasebi', 'version': '3.0', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'candle-closing-time-remaining-cctr-v3', 'source': 'MQL5 Indicators/Candle Closing Time Remaining (CCTR) MT5/candle-closing-time-remaining-cctr-v3.mq5', 'folder': 'Candle Closing Time Remaining (CCTR) MT5', 'inputs': [{'mql': 'location', 'py': 'location', 'param': 'location', 'type': 'int', 'default': 0, 'label': 'Lable Location', 'sinput': False}, {'mql': 'displayServerTime', 'py': 'displayServerTime', 'param': 'displayServerTime', 'type': 'int', 'default': 1, 'label': 'Display Server Time', 'sinput': False}, {'mql': 'playAlert', 'py': 'playAlert', 'param': 'playAlert', 'type': 'int', 'default': 0, 'label': 'Sound alert when the candle is closed', 'sinput': False}, {'mql': 'customAlertSound', 'py': 'customAlertSound', 'param': None, 'type': 'string', 'default': '', 'label': 'Custom alert sound', 'sinput': False}, {'mql': 'fontSize', 'py': 'fontSize', 'param': 'fontSize', 'type': 'int', 'default': 9, 'label': 'Font Size', 'sinput': False}, {'mql': 'colour', 'py': 'colour', 'param': None, 'type': 'color', 'default': 0, 'label': 'Colour', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Silver = 0xC0C0C0  # MQL4 colour name

# enum lctn
l1 = 0
l2 = 3
l3 = 1
l4 = 2
_enum('lctn', {0: 'l1', 3: 'l2', 1: 'l3', 2: 'l4'})

# enum onoff
on = 1
off = 0
_enum('onoff', {1: 'on', 0: 'off'})

# ---- inputs and global variables
location = _input('location', l1)  # Lable Location
displayServerTime = _input('displayServerTime', on)  # Display Server Time
playAlert = _input('playAlert', off)  # Sound alert when the candle is closed
customAlertSound = _input('customAlertSound', '')  # Custom alert sound
fontSize = _input('fontSize', 9)  # Font Size
leftTime = 0
sTime = ""
days = 0
sCurrentTime = ""
alert_played = False

def OnInit():
    if location != l1:
        if ObjectCreate(0, 'CandleClosingTimeRemaining-CCTR', OBJ_LABEL, 0, 0, 0):
            ObjectSetInteger(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_CORNER, location)
            _sw1 = location
            if _sw1 == l2:
                ObjectSetInteger(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
            elif _sw1 == l3:
                ObjectSetInteger(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
            elif _sw1 == l4:
                ObjectSetInteger(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
            ObjectSetInteger(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_XDISTANCE, 5)
            ObjectSetInteger(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_YDISTANCE, 3)
            ObjectSetString(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_FONT, 'verdana')
            ObjectSetInteger(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_COLOR, colour)
        else:
            printf('Failed to create the object OBJ_LABEL CandleClosingTimeRemaining-CCTR, Error code = ', GetLastError())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, 'CandleClosingTimeRemaining-CCTR')
    Comment(' ')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global alert_played, days, leftTime, sCurrentTime, sTime
    sCurrentTime = TimeToString(TimeCurrent(), TIME_SECONDS)
    ArraySetAsSeries(time, True)
    leftTime = PeriodSeconds(Period()) - _int(TimeCurrent() - time[0])
    if (playAlert == 1 and (not alert_played)) and leftTime <= 5:
        if customAlertSound != '':
            PlaySound(customAlertSound)
        else:
            PlaySound('alert2.wav')
        alert_played = True
    if leftTime > 5:
        alert_played = False
    sTime = TimeToString(leftTime, TIME_SECONDS)
    if DayOfWeek() == 0 or DayOfWeek() == 6:
        if location == 0:
            Comment('CCTR: ' + 'Market Is Closed')
        else:
            ObjectSetString(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_TEXT, OBJ_LABEL, 'Market Is Closed')
    else:
        if Period() == PERIOD_MN1 or Period() == PERIOD_W1:
            days = _idiv(_idiv(_idiv(leftTime, 60), 60), 24)
            if location == 0:
                if not displayServerTime:
                    Comment('CCTR: ' + _str(days) + 'D - ' + sTime)
                else:
                    Comment('CCTR: ' + _str(days) + 'D - ' + sTime + ' [' + sCurrentTime + ']')
            else:
                if not displayServerTime:
                    ObjectSetString(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_TEXT, OBJ_LABEL, _str(days) + 'D - ' + sTime)
                else:
                    ObjectSetString(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_TEXT, OBJ_LABEL, _str(days) + 'D - ' + sTime + ' [' + sCurrentTime + ']')
        else:
            if location == 0:
                if not displayServerTime:
                    Comment('CCTR: ' + sTime)
                else:
                    Comment('CCTR: ' + sTime + ' [' + sCurrentTime + ']')
            else:
                if not displayServerTime:
                    ObjectSetString(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_TEXT, OBJ_LABEL, sTime)
                else:
                    ObjectSetString(0, 'CandleClosingTimeRemaining-CCTR', OBJPROP_TEXT, OBJ_LABEL, sTime + ' [' + sCurrentTime + ']')
    return rates_total

def DayOfWeek():
    tm = MqlDateTime()
    TimeCurrent(tm)
    return tm.day_of_week

# ---- global variables initialised from expressions
colour = _input('colour', _uint(Silver))  # Colour


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleClosingTimeRemainingCctrV3(_MQL5Indicator):
    name = 'candle-closing-time-remaining-cctr-v3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'location': _Choice({0: 'Top-Left', 3: 'Top-Right', 1: 'Bottom-Left', 2: 'Bottom-Right'}, default=0),  # Lable Location
        'displayServerTime': _Choice({1: 'On', 0: 'Off'}, default=1),  # Display Server Time
        'playAlert': _Choice({1: 'On', 0: 'Off'}, default=0),  # Sound alert when the candle is closed
        'fontSize': 9,  # Font Size
    }

