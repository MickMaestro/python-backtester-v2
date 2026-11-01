"""Rsi Engulfing Alert v2 — converted from MQL5: MQL5 Indicators/Rsi Engulfing Bar V2/Rsi Engulfing Alert v2.mq5

Check Out Honeygain It's a Software for Windows Andoid IOS + more devices - Download Free & Earn Passive Income- Also Earn 25% On referalls - Currently there is a $4 sign up bonus 
Copyright: https://bit.ly/4e0wwMk; Link: https://bit.ly/4e0wwMk; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://bit.ly/4e0wwMk', 'link': 'https://bit.ly/4e0wwMk', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16755200], 2: [255]}, 'widths': {1: 5, 2: 5}, 'styles': {}, 'labels': {1: 'Buy', 2: 'Sell'}, 'levels': [], 'description': ["Check Out Honeygain It's a Software for Windows Andoid IOS + more devices - Download Free & Earn Passive Income- Also Earn 25% On referalls - Currently there is a $4 sign up bonus "], 'name': 'Rsi Engulfing Alert v2', 'source': 'MQL5 Indicators/Rsi Engulfing Bar V2/Rsi Engulfing Alert v2.mq5', 'folder': 'Rsi Engulfing Bar V2', 'inputs': [{'mql': 'RsiLow', 'py': 'RsiLow', 'param': 'RsiLow', 'type': 'double', 'default': 30.0, 'label': '', 'sinput': False}, {'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'RsiHigh', 'py': 'RsiHigh', 'param': 'RsiHigh', 'type': 'double', 'default': 70.0, 'label': '', 'sinput': False}, {'mql': 'Send_Email', 'py': 'Send_Email', 'param': 'Send_Email', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Audible_Alerts', 'py': 'Audible_Alerts', 'param': 'Audible_Alerts', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Push_Notifications', 'py': 'Push_Notifications', 'param': 'Push_Notifications', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
RsiLow = _input('RsiLow', 30.0)
RsiPeriod = _input('RsiPeriod', 10)
RsiHigh = _input('RsiHigh', 70.0)
time_alert = 0  # used when sending alert
Send_Email = _input('Send_Email', True)
Audible_Alerts = _input('Audible_Alerts', True)
Push_Notifications = _input('Push_Notifications', True)
myPoint = 0.0  # initialized in OnInit
RSI_handle = 0
RSI = Arr(0, 0.0)
Close = Arr(0, 0.0)
Open = Arr(0, 0.0)
High = Arr(0, 0.0)
Low = Arr(0, 0.0)

def myAlert(type_, message):
    handle = 0
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | Rsi Plus @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass
    elif type_ == 'indicator':
        Print(type_ + ' | Rsi Plus @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Audible_Alerts:
            Alert(type_ + ' | Rsi Plus @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Send_Email:
            SendMail('Rsi Plus', type_ + ' | Rsi Plus @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        handle = FileOpen('Rsi Plus.txt', (((FILE_TXT | FILE_READ) | FILE_WRITE) | FILE_SHARE_READ) | FILE_SHARE_WRITE, 59)
        if handle != INVALID_HANDLE:
            FileSeek(handle, 0, SEEK_END)
            FileWrite(handle, type_ + ' | Rsi Plus @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
            FileClose(handle)
        if Push_Notifications:
            SendNotification(type_ + ' | Rsi Plus @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)

def OnInit():
    global RSI_handle, myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MathMax(Bars(Symbol(), PERIOD_CURRENT) - 5000 + 1, 50 + 1))
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    SetIndexBuffer(1, Buffer2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, MathMax(Bars(Symbol(), PERIOD_CURRENT) - 5000 + 1, 50 + 1))
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    RSI_handle = iRSI(None, PERIOD_CURRENT, RsiPeriod, PRICE_CLOSE)
    if RSI_handle < 0:
        Print('The creation of iRSI has failed: RSI_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global time_alert
    limit = rates_total - prev_calculated
    ArraySetAsSeries(Buffer1, True)
    ArraySetAsSeries(Buffer2, True)
    if prev_calculated < 1:
        ArrayInitialize(Buffer1, EMPTY_VALUE)
        ArrayInitialize(Buffer2, EMPTY_VALUE)
    else:
        limit += 1
    Time = Arr(0, 0)
    if BarsCalculated(RSI_handle) <= 0:
        return 0
    if CopyBuffer(RSI_handle, 0, 0, rates_total, RSI) <= 0:
        return rates_total
    ArraySetAsSeries(RSI, True)
    if CopyClose(Symbol(), PERIOD_CURRENT, 0, rates_total, Close) <= 0:
        return rates_total
    ArraySetAsSeries(Close, True)
    if CopyOpen(Symbol(), PERIOD_CURRENT, 0, rates_total, Open) <= 0:
        return rates_total
    ArraySetAsSeries(Open, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, 0, rates_total, High) <= 0:
        return rates_total
    ArraySetAsSeries(High, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, 0, rates_total, Low) <= 0:
        return rates_total
    ArraySetAsSeries(Low, True)
    if CopyTime(Symbol(), Period(), 0, rates_total, Time) <= 0:
        return rates_total
    ArraySetAsSeries(Time, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if (((RSI[i] < RsiLow and Close[1 + i] > Open[1 + i]) and Close[2 + i] < Open[2 + i]) and Close[1 + i] > Open[2 + i]) and Close[1 + i] < High[2 + i]:
            Buffer1[i] = Low[i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Buy')
            time_alert = Time[1]
        else:
            Buffer1[i] = EMPTY_VALUE
        if (((RSI[i] > RsiHigh and Close[1 + i] < Open[1 + i]) and Close[2 + i] > Open[2 + i]) and Close[1 + i] < Open[2 + i]) and Close[1 + i] > Low[2 + i]:
            Buffer2[i] = High[i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Sell')
            time_alert = Time[1]
        else:
            Buffer2[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiEngulfingAlertV2(_MQL5Indicator):
    name = 'Rsi Engulfing Alert v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RsiLow': 30.0,
        'RsiPeriod': 10,
        'RsiHigh': 70.0,
        'Send_Email': True,
        'Audible_Alerts': True,
        'Push_Notifications': True,
    }

