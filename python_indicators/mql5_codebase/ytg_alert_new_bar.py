"""ytg_alert_new_bar — converted from MQL5: MQL5 Indicators/ytg_Alert_New_Bar/ytg_alert_new_bar.mq5

Sound signal of new bar
Copyright: Copyright © 2009, Yuriy Tokman; Link: yuriytokman@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Yuriy Tokman', 'link': 'yuriytokman@gmail.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Sound signal of new bar'], 'name': 'ytg_alert_new_bar', 'source': 'MQL5 Indicators/ytg_Alert_New_Bar/ytg_alert_new_bar.mq5', 'folder': 'ytg_Alert_New_Bar', 'inputs': [{'mql': 'On_Alert', 'py': 'On_Alert', 'param': 'On_Alert', 'type': 'bool', 'default': False, 'label': 'making an alert', 'sinput': False}, {'mql': 'On_Play_Sound', 'py': 'On_Play_Sound', 'param': 'On_Play_Sound', 'type': 'bool', 'default': False, 'label': 'making a sound signal', 'sinput': False}, {'mql': 'NameFileSound', 'py': 'NameFileSound', 'param': None, 'type': 'string', 'default': 'expert.wav', 'label': 'name of the file with sound', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
On_Alert = _input('On_Alert', False)  # making an alert
On_Play_Sound = _input('On_Play_Sound', False)  # making a sound signal
NameFileSound = _input('NameFileSound', 'expert.wav')  # name of the file with sound
min_rates_total = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global min_rates_total
    min_rates_total = 2
    IndicatorSetString(INDICATOR_SHORTNAME, 'ytg_Alert_New_Bar')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    if rates_total != prev_calculated and prev_calculated > 0:
        if On_Play_Sound:
            PlaySound(NameFileSound)
        if On_Alert:
            Alert('New bar!', ' Time Frame - ', GetStringTimeframe(PERIOD_CURRENT), '; CurTime=', TimeToString(TimeCurrent(), TIME_MINUTES))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YtgAlertNewBar(_MQL5Indicator):
    name = 'ytg_alert_new_bar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'On_Alert': False,  # making an alert
        'On_Play_Sound': False,  # making a sound signal
    }

