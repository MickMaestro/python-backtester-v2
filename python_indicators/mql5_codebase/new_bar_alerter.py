"""New_bar_alerter — converted from MQL5: MQL5 Indicators/New Bar Alerter/New_bar_alerter.mq5

Copyright: mladen; Link: www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'New_bar_alerter', 'source': 'MQL5 Indicators/New Bar Alerter/New_bar_alerter.mq5', 'folder': 'New Bar Alerter', 'inputs': [{'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'alertsShow', 'py': 'alertsShow', 'param': 'alertsShow', 'type': 'bool', 'default': False, 'label': 'Display alerter comment text?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
alertsOn = _input('alertsOn', False)  # Turn alerts on?
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
alertsShow = _input('alertsShow', False)  # Display alerter comment text?

def OnInit():
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, TickVolume, Volume, Spread):
    global _s_OnCalculate_prevTime
    if _s_OnCalculate_prevTime != time[rates_total - 1]:
        if _s_OnCalculate_prevTime != 0:
            doAlert(time[rates_total - 1], 'new bar formed')
    _s_OnCalculate_prevTime = time[rates_total - 1]
    if alertsShow:
        Comment('New bar alerter last checked status at : ' + TimeToString(TimeLocal(), TIME_SECONDS))
    return rates_total

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    message = ""
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = TimeToString(TimeLocal(), TIME_SECONDS) + ' ' + Symbol() + ' new bar alerter : ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' new bar alerter', message)
        if alertsSound:
            PlaySound('alert2.wav')

# ---- static local variables
_s_OnCalculate_prevTime = 0
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NewBarAlerter(_MQL5Indicator):
    name = 'New_bar_alerter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'alertsOn': False,  # Turn alerts on?
        'alertsMessage': True,  # Display messageas on alerts?
        'alertsSound': False,  # Play sound on alerts?
        'alertsEmail': False,  # Send email on alerts?
        'alertsShow': False,  # Display alerter comment text?
    }

