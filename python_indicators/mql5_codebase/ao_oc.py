"""AO oc — converted from MQL5: MQL5 Indicators/AO Rsi/AO oc.mq5

Forex Experts & Indicators
Copyright: *** Click here for more experts ***; Link: https://www.google.com/search?q=forexeas+payhip&rlz=1C1CHBF_en-GBAU972AU972&sxsrf=APq-WBtD_BRErb2qCXBGJg8Yh8QJmO9hng%3A1647519330253&ei=YiYzYoH9DoK_4-EP78-ZuAw&ved=0ahUKEwiBtsLjj832AhWC3zgGHe9nBscQ4dUDCA4&uact=5&oq=forexeas+payhip&gs_lcp=Cgdnd3Mtd2l6EAMyBQghEKABMgUIIRCgAToHCAAQRxCwAzoICAAQCBANEB46BAgAEA06BggAEA0QHjoHCCEQChCgAUoECEEYAEoECEYYAFCZC1j6GGCuIGgBcAF4AIAB3QKIAYgQkgEFMi00LjOYAQCgAQHIAQjAAQE&sclient=gws-wiz; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '*** Click here for more experts ***', 'link': 'https://www.google.com/search?q=forexeas+payhip&rlz=1C1CHBF_en-GBAU972AU972&sxsrf=APq-WBtD_BRErb2qCXBGJg8Yh8QJmO9hng%3A1647519330253&ei=YiYzYoH9DoK_4-EP78-ZuAw&ved=0ahUKEwiBtsLjj832AhWC3zgGHe9nBscQ4dUDCA4&uact=5&oq=forexeas+payhip&gs_lcp=Cgdnd3Mtd2l6EAMyBQghEKABMgUIIRCgAToHCAAQRxCwAzoICAAQCBANEB46BAgAEA06BggAEA0QHjoHCCEQChCgAUoECEEYAEoECEYYAFCZC1j6GGCuIGgBcAF4AIAB3QKIAYgQkgEFMi00LjOYAQCgAQHIAQjAAQE&sclient=gws-wiz', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16755200], 2: [255]}, 'widths': {1: 5, 2: 5}, 'styles': {}, 'labels': {1: 'Buy', 2: 'Sell'}, 'levels': [], 'description': ['Forex Experts & Indicators'], 'name': 'AO oc', 'source': 'MQL5 Indicators/AO Rsi/AO oc.mq5', 'folder': 'AO Rsi', 'inputs': [{'mql': 'Aolvl', 'py': 'Aolvl', 'param': 'Aolvl', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'rsiupperlimit', 'py': 'rsiupperlimit', 'param': 'rsiupperlimit', 'type': 'double', 'default': 100.0, 'label': '', 'sinput': False}, {'mql': 'rsilowerlimit', 'py': 'rsilowerlimit', 'param': 'rsilowerlimit', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'rsiperiod', 'py': 'rsiperiod', 'param': 'rsiperiod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Send_Email', 'py': 'Send_Email', 'param': 'Send_Email', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Audible_Alerts', 'py': 'Audible_Alerts', 'param': 'Audible_Alerts', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Push_Notifications', 'py': 'Push_Notifications', 'param': 'Push_Notifications', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
Aolvl = _input('Aolvl', 0.0)
rsiupperlimit = _input('rsiupperlimit', 100.0)
rsilowerlimit = _input('rsilowerlimit', 0.0)
rsiperiod = _input('rsiperiod', 14)
time_alert = 0  # used when sending alert
Send_Email = _input('Send_Email', True)
Audible_Alerts = _input('Audible_Alerts', True)
Push_Notifications = _input('Push_Notifications', True)
myPoint = 0.0  # initialized in OnInit
AO_handle = 0
AO = Arr(0, 0.0)
RSI_handle = 0
RSI = Arr(0, 0.0)
Close = Arr(0, 0.0)
High = Arr(0, 0.0)
Low = Arr(0, 0.0)

def myAlert(type_, message):
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | AO oc @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass
    elif type_ == 'indicator':
        if Audible_Alerts:
            Alert(type_ + ' | AO oc @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Send_Email:
            SendMail('AO oc', type_ + ' | AO oc @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Push_Notifications:
            SendNotification(type_ + ' | AO oc @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)

def OnInit():
    global AO_handle, RSI_handle, myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    SetIndexBuffer(1, Buffer2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    AO_handle = iAO(None, PERIOD_CURRENT)
    if AO_handle < 0:
        Print('The creation of iAO has failed: AO_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    RSI_handle = iRSI(None, PERIOD_CURRENT, rsiperiod, PRICE_CLOSE)
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
    if BarsCalculated(AO_handle) <= 0:
        return 0
    if CopyBuffer(AO_handle, 0, 0, rates_total, AO) <= 0:
        return rates_total
    ArraySetAsSeries(AO, True)
    if BarsCalculated(RSI_handle) <= 0:
        return 0
    if CopyBuffer(RSI_handle, 0, 0, rates_total, RSI) <= 0:
        return rates_total
    ArraySetAsSeries(RSI, True)
    if CopyClose(Symbol(), PERIOD_CURRENT, 0, rates_total, Close) <= 0:
        return rates_total
    ArraySetAsSeries(Close, True)
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
        if (((((AO[2 + i] > AO[1 + i] and AO[i] > AO[1 + i]) and AO[i] > Aolvl) and RSI[i] < rsiupperlimit) and RSI[i] > rsilowerlimit) and AO[3 + i] > AO[2 + i]) and Close[i] > High[1 + i]:
            Buffer1[i] = Low[1 + i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Buy')
            time_alert = Time[1]
        else:
            Buffer1[i] = EMPTY_VALUE
        if (((((AO[2 + i] < AO[1 + i] and AO[i] < AO[1 + i]) and AO[i] < Aolvl) and RSI[i] < rsiupperlimit) and RSI[i] > rsilowerlimit) and AO[3 + i] < AO[2 + i]) and Close[i] < Low[1 + i]:
            Buffer2[i] = High[1 + i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Sell')
            time_alert = Time[1]
        else:
            Buffer2[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AOOc(_MQL5Indicator):
    name = 'AO oc'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Aolvl': 0.0,
        'rsiupperlimit': 100.0,
        'rsilowerlimit': 0.0,
        'rsiperiod': 14,
        'Send_Email': True,
        'Audible_Alerts': True,
        'Push_Notifications': True,
    }

