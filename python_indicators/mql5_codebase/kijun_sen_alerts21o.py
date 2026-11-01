"""Kijun-Sen_alerts21o — converted from MQL5: MQL5 Indicators/Kijun-Sen with alerts/Kijun-Sen_alerts21o.mq5

Copyright: mladen; Link: www.forex-tsd.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Kijun-sen'}, 'levels': [], 'description': [], 'name': 'Kijun-Sen_alerts21o', 'source': 'MQL5 Indicators/Kijun-Sen with alerts/Kijun-Sen_alerts21o.mq5', 'folder': 'Kijun-Sen with alerts', 'inputs': [{'mql': 'Kijun', 'py': 'Kijun', 'param': 'Kijun', 'type': 'int', 'default': 26, 'label': 'Calculation period', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'alertsNotify', 'py': 'alertsNotify', 'param': 'alertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Kijun = _input('Kijun', 26)  # Calculation period
alertsOn = _input('alertsOn', False)  # Turn alerts on?
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar?
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
alertsNotify = _input('alertsNotify', False)  # Send push notification on alerts?
MaBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, MaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Kijun-Sen (' + _str(Kijun) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, TickVolume, Volume, Spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        if i < Kijun:
            continue
        khi = high[i]
        klo = low[i]
        k = 1
        while k < Kijun and (i - k) >= 0:
            if khi < high[i - k]:
                khi = high[i - k]
            if klo > low[i - k]:
                klo = low[i - k]
            k += 1
        if (khi + klo) > 0.0:
            MaBuffer[i] = (khi + klo) / 2
        else:
            MaBuffer[i] = 0.0
        ColorBuffer[i] = (0 if (close[i] > MaBuffer[i]) else 1 if (close[i] < MaBuffer[i]) else ColorBuffer[i - 1])
    manageAlerts(time, ColorBuffer, rates_total)
    return rates_total

def manageAlerts(time, trend, bars):
    if alertsOn:
        whichBar = bars - 1
        if not alertsOnCurrent:
            whichBar = bars - 2
        time1 = time[whichBar]
        if trend[whichBar] != trend[whichBar - 1]:
            if trend[whichBar] == 0:
                doAlert(time1, 'up')
            if trend[whichBar] == 1:
                doAlert(time1, 'down')

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    message = ""
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = TimeToString(TimeLocal(), TIME_SECONDS) + ' ' + Symbol() + ' Kijun-Sen signal ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' Kijun-Sen', message)
        if alertsNotify:
            SendNotification(message)
        if alertsSound:
            PlaySound('alert2.wav')

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KijunSenAlerts21o(_MQL5Indicator):
    name = 'Kijun-Sen_alerts21o'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Kijun': 26,  # Calculation period
        'alertsOn': False,  # Turn alerts on?
        'alertsOnCurrent': True,  # Alert on current bar?
        'alertsMessage': True,  # Display messageas on alerts?
        'alertsSound': False,  # Play sound on alerts?
        'alertsEmail': False,  # Send email on alerts?
        'alertsNotify': False,  # Send push notification on alerts?
    }

