"""Key_Reversal — converted from MQL5: MQL5 Indicators/Key_Reversal/Key_Reversal.mq5

Key Reversal indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Top KR', 2: 'Bottom KR'}, 'levels': [], 'description': ['Key Reversal indicator'], 'name': 'Key_Reversal', 'source': 'MQL5 Indicators/Key_Reversal/Key_Reversal.mq5', 'folder': 'Key_Reversal', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 2, 'label': 'Trend detection period', 'sinput': False}, {'mql': 'InpUseFilter', 'py': 'InpUseFilter', 'param': 'InpUseFilter', 'type': 'int', 'default': 1, 'label': 'Use trend detection filter', 'sinput': False}, {'mql': 'InpUseAlert', 'py': 'InpUseAlert', 'param': 'InpUseAlert', 'type': 'int', 'default': 1, 'label': 'Show alerts', 'sinput': False}, {'mql': 'InpSendMail', 'py': 'InpSendMail', 'param': 'InpSendMail', 'type': 'int', 'default': 0, 'label': 'Send mails', 'sinput': False}, {'mql': 'InpSendPush', 'py': 'InpSendPush', 'param': 'InpSendPush', 'type': 'int', 'default': 1, 'label': 'Send push-notifications', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 2)  # Trend detection period
InpUseFilter = _input('InpUseFilter', INPUT_YES)  # Use trend detection filter
InpUseAlert = _input('InpUseAlert', INPUT_YES)  # Show alerts
InpSendMail = _input('InpSendMail', INPUT_NO)  # Send mails
InpSendPush = _input('InpSendPush', INPUT_YES)  # Send push-notifications
BufferTKR = Arr(0, 0.0)
BufferBKR = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferTKR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBKR, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Key Reversal' + ((' (' + _str(period) + ' bars trend)') if InpUseFilter else ''))
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTKR, True)
    ArraySetAsSeries(BufferBKR, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_time
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferTKR, EMPTY_VALUE)
        ArrayInitialize(BufferBKR, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferBKR[i] = (low[i] if (Verification(i, open, high, low, close) == 1) else EMPTY_VALUE)
        BufferTKR[i] = (high[i] if (Verification(i, open, high, low, close) == -1) else EMPTY_VALUE)
    Alerts = ''
    if time[0] > _s_OnCalculate_last_time and (BufferTKR[1] != EMPTY_VALUE or BufferBKR[1] != EMPTY_VALUE):
        dir = ('Up' if (BufferBKR[1] != EMPTY_VALUE) else 'Down' if (BufferTKR[1] != EMPTY_VALUE) else '')
        message = Symbol() + ', ' + TimeframeToString(Period()) + ': Key Reversal ' + dir + ' Signal.'
        if InpUseAlert:
            Alert(message)
        if InpSendMail and TerminalInfoInteger(TERMINAL_EMAIL_ENABLED):
            SendMail('Key Reversal indicator Signal', message)
        if InpSendPush and TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED):
            SendNotification(message)
        _s_OnCalculate_last_time = TimeCurrent()
    return rates_total

def Verification(shift, open, high, low, close):
    signal = (1 if (close[shift] > high[shift + 1]) else -1 if (close[shift] < low[shift + 1]) else 0)
    if not InpUseFilter:
        return signal
    for i in range(1, period + 1):
        check = (1 if (close[shift + i] > open[shift + i]) else -1 if (close[shift + i] < open[shift + i]) else 0)
        if (signal == 1 and check == 1) or (signal == -1 and check == -1):
            return 0
    return signal

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

# ---- static local variables
_s_OnCalculate_last_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KeyReversal(_MQL5Indicator):
    name = 'Key_Reversal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 2,  # Trend detection period
        'InpUseFilter': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use trend detection filter
        'InpUseAlert': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show alerts
        'InpSendMail': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Send mails
        'InpSendPush': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Send push-notifications
    }

