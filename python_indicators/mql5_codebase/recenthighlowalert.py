"""RecentHighLowAlert — converted from MQL5: MQL5 Indicators/Recent High_Low Alert MT5/RecentHighLowAlert.mq5

Draws lines on the High/Low of the recent N bars.
Alerts when the Bid price of the current bar crosses previous High/Low.
Copyright: https://t.me/ForexEaPremium; Link: https://t.me/ForexEaPremium; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'link': 'https://t.me/ForexEaPremium', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [65535]}, 'widths': {}, 'styles': {}, 'labels': {1: 'High', 2: 'Low'}, 'levels': [], 'description': ['Draws lines on the High/Low of the recent N bars.', 'Alerts when the Bid price of the current bar crosses previous High/Low.'], 'name': 'RecentHighLowAlert', 'source': 'MQL5 Indicators/Recent High_Low Alert MT5/RecentHighLowAlert.mq5', 'folder': 'Recent High_Low Alert MT5', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_candle_to_check
Current = 0
Previous = 1
_enum('enum_candle_to_check', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
N = _input('N', 20)
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
TriggerCandle = _input('TriggerCandle', Previous)
HighBuf = Arr(0, 0.0)
LowBuf = Arr(0, 0.0)
LastHighAlert = 0
LastLowAlert = 0

def OnInit():
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, N)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, N)
    SetIndexBuffer(0, HighBuf, INDICATOR_DATA)
    SetIndexBuffer(1, LowBuf, INDICATOR_DATA)

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, close, tick_volume, volume, spread):
    if rates_total <= N:
        return 0
    start = prev_calculated - 1
    if start < N:
        start = N
    for i in range(start, rates_total):
        HighBuf[i] = High[ArrayMaximum(High, i - N + 1, N)]
        LowBuf[i] = Low[ArrayMinimum(Low, i - N + 1, N)]
    Bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    if Bid > HighBuf[rates_total - 1 - TriggerCandle] and LastHighAlert != Time[rates_total - 1]:
        SendAlert(1, HighBuf[rates_total - 1 - TriggerCandle], Time[rates_total - 1])
    elif Bid < LowBuf[rates_total - 1 - TriggerCandle] and LastLowAlert != Time[rates_total - 1]:
        SendAlert(0, LowBuf[rates_total - 1 - TriggerCandle], Time[rates_total - 1])
    return rates_total

def SendAlert(direction, price, time):
    global LastHighAlert, LastLowAlert
    alert = 'Local '
    subject = ""
    if direction == 1:
        alert = alert + 'high'
        subject = 'High broken @ ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7)
        LastHighAlert = time
    elif direction == 0:
        alert = alert + 'low'
        subject = 'Low broken @ ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7)
        LastLowAlert = time
    alert = alert + ' broken at ' + DoubleToString(price, Digits()) + '.'
    if EnableNativeAlerts:
        Alert(alert)
    if EnableEmailAlerts:
        SendMail(subject, TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS) + ' ' + alert)
    if EnablePushAlerts:
        SendNotification(subject + ' @ ' + DoubleToString(price, Digits()))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RecentHighLowAlert(_MQL5Indicator):
    name = 'RecentHighLowAlert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 20,
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'TriggerCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),
    }

