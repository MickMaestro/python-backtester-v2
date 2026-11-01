"""Alert Crossing Moving Average Nth Bar — converted from MQL5: MQL5 Indicators/Alert Crossing Moving Average Nth Bar/Alert Crossing Moving Average Nth Bar.mq5

Alert when crossing the indicator Moving Average N-th bar
---
Play sound: The file must be located in terminal_directory \\\\Sounds or its sub-directory. Only WAV files are played
---
Send mail: Sends an email at the address specified in the settings window of the \\"Email\\" tab
---
Send notification: Sends push notifications to mobile terminals, whose MetaQuotes ID are specified in the \\"Notifications\\" tab
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Alert when crossing the indicator Moving Average N-th bar', '---', 'Play sound: The file must be located in terminal_directory \\\\Sounds or its sub-directory. Only WAV files are played', '---', 'Send mail: Sends an email at the address specified in the settings window of the \\"Email\\" tab', '---', 'Send notification: Sends push notifications to mobile terminals, whose MetaQuotes ID are specified in the \\"Notifications\\" tab'], 'name': 'Alert Crossing Moving Average Nth Bar', 'source': 'MQL5 Indicators/Alert Crossing Moving Average Nth Bar/Alert Crossing Moving Average Nth Bar.mq5', 'folder': 'Alert Crossing Moving Average Nth Bar', 'inputs': [{'mql': 'ma_period', 'py': 'ma_period', 'param': 'ma_period', 'type': 'int', 'default': 10, 'label': 'period of ma', 'sinput': False}, {'mql': 'ma_shift', 'py': 'ma_shift', 'param': 'ma_shift', 'type': 'int', 'default': 0, 'label': 'shift', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'type of smoothing', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}, {'mql': 'InpSound', 'py': 'InpSound', 'param': 'InpSound', 'type': 'bool', 'default': True, 'label': 'Play sound', 'sinput': False}, {'mql': 'sound_filename', 'py': 'sound_filename', 'param': None, 'type': 'string', 'default': 'wait.wav', 'label': 'Play sound file name', 'sinput': False}, {'mql': 'InpMail', 'py': 'InpMail', 'param': 'InpMail', 'type': 'bool', 'default': True, 'label': 'Send mail', 'sinput': False}, {'mql': 'InpNotification', 'py': 'InpNotification', 'param': 'InpNotification', 'type': 'bool', 'default': True, 'label': 'Send notification', 'sinput': False}, {'mql': 'InpN_Bar', 'py': 'InpN_Bar', 'param': 'InpN_Bar', 'type': 'uint', 'default': 1, 'label': 'N bar', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ma_period = _input('ma_period', 10)  # period of ma
ma_shift = _input('ma_shift', 0)  # shift
ma_method = _input('ma_method', MODE_SMA)  # type of smoothing
applied_price = _input('applied_price', PRICE_CLOSE)  # type of price
InpSound = _input('InpSound', True)  # Play sound
sound_filename = _input('sound_filename', 'wait.wav')  # Play sound file name
InpMail = _input('InpMail', True)  # Send mail
InpNotification = _input('InpNotification', True)  # Send notification
InpN_Bar = _input('InpN_Bar', 1)  # N bar
handle_iMA = 0  # variable for storing the handle of the iMA indicator

def OnInit():
    global handle_iMA
    handle_iMA = iMA(Symbol(), Period(), ma_period, ma_shift, ma_method, applied_price)
    if handle_iMA == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    if MQLInfoInteger(MQL_DEBUG):
        ChartIndicatorAdd(0, 0, handle_iMA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_PrevBars, _s_OnCalculate_alert_current_bar
    if prev_calculated == 0:
        return rates_total
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    if time[0] == _s_OnCalculate_PrevBars:
        return rates_total
    _s_OnCalculate_PrevBars = time[0]
    if time[0] == _s_OnCalculate_alert_current_bar:
        return rates_total
    ima_bar_N = iMAGet(InpN_Bar)
    if ima_bar_N == 0.0:
        _s_OnCalculate_PrevBars = time[1]
        return rates_total
    if (open[InpN_Bar] < ima_bar_N and close[InpN_Bar] > ima_bar_N) or (open[InpN_Bar] > ima_bar_N and close[InpN_Bar] < ima_bar_N):
        _s_OnCalculate_alert_current_bar = time[0]
        if InpSound:
            PlaySound(sound_filename)
        subject = 'Crossing ' + IntegerToString(InpN_Bar) + ' bar'
        some_text = Symbol() + ', ' + EnumToString(Period(), '') + '. ' + 'MA(' + IntegerToString(ma_period) + ')' + ' crossing ' + IntegerToString(InpN_Bar) + ' bar'
        if InpMail:
            SendMail(subject, some_text)
        if InpNotification:
            SendNotification(some_text)
    return rates_total

def iMAGet(index):
    MA = Arr(1, 0.0, dyn=False)
    ResetLastError()
    if CopyBuffer(handle_iMA, 0, index, 1, MA) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return 0.0
    return MA[0]

# ---- static local variables
_s_OnCalculate_alert_current_bar = 0
_s_OnCalculate_PrevBars = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AlertCrossingMovingAverageNthBar(_MQL5Indicator):
    name = 'Alert Crossing Moving Average Nth Bar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ma_period': 10,  # period of ma
        'ma_shift': 0,  # shift
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # type of smoothing
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
        'InpSound': True,  # Play sound
        'InpMail': True,  # Send mail
        'InpNotification': True,  # Send notification
        'InpN_Bar': 1,  # N bar
    }

