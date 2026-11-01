"""VPS Monitor — converted from MQL5: MQL5 Indicators/VPS Monitor - Metatrader 5/VPS Monitor.mq5

Copyright: Stefanus Wardoyo; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Stefanus Wardoyo', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'VPS Monitor', 'source': 'MQL5 Indicators/VPS Monitor - Metatrader 5/VPS Monitor.mq5', 'folder': 'VPS Monitor - Metatrader 5', 'inputs': [{'mql': 'SendEmail', 'py': 'SendEmail', 'param': 'SendEmail', 'type': 'bool', 'default': False, 'label': 'Send Email', 'sinput': False}, {'mql': 'SendNotif', 'py': 'SendNotif', 'param': 'SendNotif', 'type': 'bool', 'default': True, 'label': 'Send Notification', 'sinput': False}, {'mql': 'ScheduleHour', 'py': 'ScheduleHour', 'param': 'ScheduleHour', 'type': 'int', 'default': 6, 'label': 'Period Active in Hour', 'sinput': False}, {'mql': 'Message', 'py': 'Message', 'param': None, 'type': 'string', 'default': 'Account XXX is ON', 'label': 'Message', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SendEmail = _input('SendEmail', False)  # Send Email
SendNotif = _input('SendNotif', True)  # Send Notification
ScheduleHour = _input('ScheduleHour', 6)  # Period Active in Hour
Message = _input('Message', 'Account XXX is ON')  # Message

def OnInit():
    OnTimer()
    EventSetTimer(ScheduleHour * 60 * 60)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnTimer():
    if SendNotif:
        SendNotification(Message)
        Print('Send Notification Last Error:' + _str(GetLastError()))
    if SendEmail:
        SendMail(Message, Message)
        Print('Send Email Last Error:' + _str(GetLastError()))
    Print(Message)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VPSMonitor(_MQL5Indicator):
    name = 'VPS Monitor'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SendEmail': False,  # Send Email
        'SendNotif': True,  # Send Notification
        'ScheduleHour': 6,  # Period Active in Hour
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

