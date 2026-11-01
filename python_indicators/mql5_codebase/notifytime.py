"""NotifyTime — converted from MQL5: MQL5 Indicators/Candle Closing Time Notify Alarm/NotifyTime.mq5

Copyright: Copyright 2021, Dark Ryd3r; Link: https://twitter.com/DarkRyd3r; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, Dark Ryd3r', 'link': 'https://twitter.com/DarkRyd3r', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'NotifyTime', 'source': 'MQL5 Indicators/Candle Closing Time Notify Alarm/NotifyTime.mq5', 'folder': 'Candle Closing Time Notify Alarm', 'inputs': [{'mql': 'info', 'py': 'info', 'param': None, 'type': 'string', 'default': 'Add Closing time -5 minute in HH:MM format (Ignore the date)', 'label': '', 'sinput': False}, {'mql': 'T0', 'py': 'T0', 'param': None, 'type': 'datetime', 'default': 19500, 'label': 'Time 1', 'sinput': False}, {'mql': 'T1', 'py': 'T1', 'param': None, 'type': 'datetime', 'default': 33900, 'label': 'Time 2', 'sinput': False}, {'mql': 'T2', 'py': 'T2', 'param': None, 'type': 'datetime', 'default': 5100, 'label': 'Time 3', 'sinput': False}, {'mql': 'T3', 'py': 'T3', 'param': None, 'type': 'datetime', 'default': 62700, 'label': 'Time 4', 'sinput': False}, {'mql': 'T4', 'py': 'T4', 'param': None, 'type': 'datetime', 'default': 77100, 'label': 'Time 5', 'sinput': False}, {'mql': 'T5', 'py': 'T5', 'param': None, 'type': 'datetime', 'default': 5100, 'label': 'Time 6', 'sinput': False}, {'mql': 'message', 'py': 'message', 'param': None, 'type': 'string', 'default': '5min remaining in Closing of 4H Candle at', 'label': 'Enter your alert message here', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': True, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'alertsPopup', 'py': 'alertsPopup', 'param': 'alertsPopup', 'type': 'bool', 'default': True, 'label': 'Show Popup Window?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'alertsPrint', 'py': 'alertsPrint', 'param': 'alertsPrint', 'type': 'bool', 'default': True, 'label': 'Print the Message?', 'sinput': False}, {'mql': 'alertsPush', 'py': 'alertsPush', 'param': 'alertsPush', 'type': 'bool', 'default': False, 'label': 'Send Push Notification?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
timex = Arr(6, 0, dyn=False)
info = _input('info', 'Add Closing time -5 minute in HH:MM format (Ignore the date)')
T0 = _input('T0', 19500)  # Time 1
T1 = _input('T1', 33900)  # Time 2
T2 = _input('T2', 5100)  # Time 3
T3 = _input('T3', 62700)  # Time 4
T4 = _input('T4', 77100)  # Time 5
T5 = _input('T5', 5100)  # Time 6
message = _input('message', '5min remaining in Closing of 4H Candle at')  # Enter your alert message here
alertsOn = _input('alertsOn', True)  # Turn alerts on?
alertsPopup = _input('alertsPopup', True)  # Show Popup Window?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
alertsPrint = _input('alertsPrint', True)  # Print the Message?
alertsPush = _input('alertsPush', False)  # Send Push Notification?

def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    timex[0] = T0
    timex[1] = T1
    timex[2] = T2
    timex[3] = T3
    timex[4] = T4
    timex[5] = T5
    ArraySize(timex)
    tf = PERIOD_M1
    ClosingTime = iTime(Symbol(), tf, 0)
    for i in range(0, 6):
        if TimeToString(ClosingTime, TIME_MINUTES) == TimeToString(timex[i], TIME_MINUTES):
            doAlert(time[rates_total - 1], 'Alert : ')
    return rates_total

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        if alertsPopup:
            Alert(message, ' : ' + TimeToString(TimeLocal(), TIME_SECONDS))
        if alertsEmail:
            SendMail(Symbol() + ' : ', message)
        if alertsSound:
            PlaySound('alert.wav')
        if alertsPrint:
            Print(message, ' : ' + TimeToString(TimeLocal(), TIME_SECONDS))
        if alertsPush:
            SendNotification(message + ' : ' + TimeToString(TimeLocal(), TIME_SECONDS))

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NotifyTime(_MQL5Indicator):
    name = 'NotifyTime'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'alertsOn': True,  # Turn alerts on?
        'alertsPopup': True,  # Show Popup Window?
        'alertsSound': False,  # Play sound on alerts?
        'alertsEmail': False,  # Send email on alerts?
        'alertsPrint': True,  # Print the Message?
        'alertsPush': False,  # Send Push Notification?
    }

