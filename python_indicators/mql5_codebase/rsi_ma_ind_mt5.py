"""Rsi ma ind mt5 — converted from MQL5: MQL5 Indicators/Rsi alert plus/Rsi ma ind mt5.mq5

Copyright: *** Click here for more experts ***; Link: https://www.google.com/search?q=forexeas+payhip&rlz=1C1CHBF_en-GBAU972AU972&sxsrf=APq-WBtD_BRErb2qCXBGJg8Yh8QJmO9hng%3A1647519330253&ei=YiYzYoH9DoK_4-EP78-ZuAw&ved=0ahUKEwiBtsLjj832AhWC3zgGHe9nBscQ4dUDCA4&uact=5&oq=forexeas+payhip&gs_lcp=Cgdnd3Mtd2l6EAMyBQghEKABMgUIIRCgAToHCAAQRxCwAzoICAAQCBANEB46BAgAEA06BggAEA0QHjoHCCEQChCgAUoECEEYAEoECEYYAFCZC1j6GGCuIGgBcAF4AIAB3QKIAYgQkgEFMi00LjOYAQCgAQHIAQjAAQE&sclient=gws-wiz; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '*** Click here for more experts ***', 'link': 'https://www.google.com/search?q=forexeas+payhip&rlz=1C1CHBF_en-GBAU972AU972&sxsrf=APq-WBtD_BRErb2qCXBGJg8Yh8QJmO9hng%3A1647519330253&ei=YiYzYoH9DoK_4-EP78-ZuAw&ved=0ahUKEwiBtsLjj832AhWC3zgGHe9nBscQ4dUDCA4&uact=5&oq=forexeas+payhip&gs_lcp=Cgdnd3Mtd2l6EAMyBQghEKABMgUIIRCgAToHCAAQRxCwAzoICAAQCBANEB46BAgAEA06BggAEA0QHjoHCCEQChCgAUoECEEYAEoECEYYAFCZC1j6GGCuIGgBcAF4AIAB3QKIAYgQkgEFMi00LjOYAQCgAQHIAQjAAQE&sclient=gws-wiz', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16755200], 2: [1184478]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Buy', 2: 'Buy'}, 'levels': [], 'description': [''], 'name': 'Rsi ma ind mt5', 'source': 'MQL5 Indicators/Rsi alert plus/Rsi ma ind mt5.mq5', 'folder': 'Rsi alert plus', 'inputs': [{'mql': 'rsi', 'py': 'rsi', 'param': 'rsi', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'rsilvl', 'py': 'rsilvl', 'param': 'rsilvl', 'type': 'double', 'default': 30.0, 'label': '', 'sinput': False}, {'mql': 'rsilvl2', 'py': 'rsilvl2', 'param': 'rsilvl2', 'type': 'double', 'default': 70.0, 'label': '', 'sinput': False}, {'mql': 'mabuy', 'py': 'mabuy', 'param': 'mabuy', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'masell', 'py': 'masell', 'param': 'masell', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
rsi = _input('rsi', 14)
rsilvl = _input('rsilvl', 30.0)
rsilvl2 = _input('rsilvl2', 70.0)
mabuy = _input('mabuy', 8)
masell = _input('masell', 8)
time_alert = 0  # used when sending alert
Send_Email = True
Audible_Alerts = True
Push_Notifications = True
myPoint = 0.0  # initialized in OnInit
RSI_handle = 0
RSI = Arr(0, 0.0)
Open = Arr(0, 0.0)
MA_handle = 0
MA = Arr(0, 0.0)
Low = Arr(0, 0.0)
MA_handle2 = 0
MA2 = Arr(0, 0.0)
High = Arr(0, 0.0)

def myAlert(type_, message):
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | poo @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass
    elif type_ == 'indicator':
        if Audible_Alerts:
            Alert(type_ + ' | poo @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Send_Email:
            SendMail('poo', type_ + ' | poo @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Push_Notifications:
            SendNotification(type_ + ' | poo @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)

def CandlestickBodyLength(timeframe, shift):
    cOpen = Arr(0, 0.0)
    CopyOpen(Symbol(), timeframe, shift, 1, cOpen)
    ArraySetAsSeries(cOpen, True)
    cClose = Arr(0, 0.0)
    CopyClose(Symbol(), timeframe, shift, 1, cClose)
    ArraySetAsSeries(cClose, True)
    return MathAbs(cOpen[0] - cClose[0])

def CandlestickUpperWick(timeframe, shift):
    cHigh = Arr(0, 0.0)
    CopyHigh(Symbol(), timeframe, shift, 1, cHigh)
    ArraySetAsSeries(cHigh, True)
    cOpen = Arr(0, 0.0)
    CopyOpen(Symbol(), timeframe, shift, 1, cOpen)
    ArraySetAsSeries(cOpen, True)
    cClose = Arr(0, 0.0)
    CopyClose(Symbol(), timeframe, shift, 1, cClose)
    ArraySetAsSeries(cClose, True)
    return cHigh[0] - MathMax(cOpen[0], cClose[0])

def CandlestickLowerWick(timeframe, shift):
    cLow = Arr(0, 0.0)
    CopyLow(Symbol(), timeframe, shift, 1, cLow)
    ArraySetAsSeries(cLow, True)
    cOpen = Arr(0, 0.0)
    CopyOpen(Symbol(), timeframe, shift, 1, cOpen)
    ArraySetAsSeries(cOpen, True)
    cClose = Arr(0, 0.0)
    CopyClose(Symbol(), timeframe, shift, 1, cClose)
    ArraySetAsSeries(cClose, True)
    return MathMin(cOpen[0], cClose[0]) - cLow[0]

def OnInit():
    global MA_handle, MA_handle2, RSI_handle, myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    SetIndexBuffer(1, Buffer2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    RSI_handle = iRSI(None, PERIOD_CURRENT, rsi, PRICE_CLOSE)
    if RSI_handle < 0:
        Print('The creation of iRSI has failed: RSI_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    MA_handle = iMA(None, PERIOD_CURRENT, mabuy, 0, MODE_SMA, PRICE_CLOSE)
    if MA_handle < 0:
        Print('The creation of iMA has failed: MA_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    MA_handle2 = iMA(None, PERIOD_CURRENT, masell, 0, MODE_SMA, PRICE_CLOSE)
    if MA_handle2 < 0:
        Print('The creation of iMA has failed: MA_handle2=', INVALID_HANDLE)
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
    if CopyOpen(Symbol(), PERIOD_CURRENT, 0, rates_total, Open) <= 0:
        return rates_total
    ArraySetAsSeries(Open, True)
    if BarsCalculated(MA_handle) <= 0:
        return 0
    if CopyBuffer(MA_handle, 0, 0, rates_total, MA) <= 0:
        return rates_total
    ArraySetAsSeries(MA, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, 0, rates_total, Low) <= 0:
        return rates_total
    ArraySetAsSeries(Low, True)
    if BarsCalculated(MA_handle2) <= 0:
        return 0
    if CopyBuffer(MA_handle2, 0, 0, rates_total, MA2) <= 0:
        return rates_total
    ArraySetAsSeries(MA2, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, 0, rates_total, High) <= 0:
        return rates_total
    ArraySetAsSeries(High, True)
    if CopyTime(Symbol(), Period(), 0, rates_total, Time) <= 0:
        return rates_total
    ArraySetAsSeries(Time, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if ((RSI[i] < rsilvl and RSI[1 + i] <= RSI[2 + i]) and CandlestickUpperWick(PERIOD_CURRENT, 1 + i) >= CandlestickBodyLength(PERIOD_CURRENT, 1 + i)) and Open[1 + i] >= MA[i]:
            Buffer1[i] = Low[i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Buy')
            time_alert = Time[1]
        else:
            Buffer1[i] = EMPTY_VALUE
        if ((RSI[i] > rsilvl2 and RSI[1 + i] >= RSI[2 + i]) and CandlestickLowerWick(PERIOD_CURRENT, 1 + i) >= CandlestickBodyLength(PERIOD_CURRENT, 1 + i)) and Open[1 + i] <= MA2[i]:
            Buffer2[i] = High[i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Buy')
            time_alert = Time[1]
        else:
            Buffer2[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiMaIndMt5(_MQL5Indicator):
    name = 'Rsi ma ind mt5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'rsi': 14,
        'rsilvl': 30.0,
        'rsilvl2': 70.0,
        'mabuy': 8,
        'masell': 8,
    }

