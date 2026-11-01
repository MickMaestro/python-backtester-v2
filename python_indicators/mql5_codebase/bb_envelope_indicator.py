"""bb envelope indicator — converted from MQL5: MQL5 Indicators/Bollinger and Envelope candle extremes/bb envelope indicator.mq5

Vist Mql4 Mql5 website market here for more
Copyright: https://www.mql5.com/en/users/paultraderone/seller; Link: https://www.mql5.com/en/users/paultraderone/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://www.mql5.com/en/users/paultraderone/seller', 'link': 'https://www.mql5.com/en/users/paultraderone/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [12320512], 2: [2230251]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Buy', 2: 'sell'}, 'levels': [], 'description': ['Vist Mql4 Mql5 website market here for more'], 'name': 'bb envelope indicator', 'source': 'MQL5 Indicators/Bollinger and Envelope candle extremes/bb envelope indicator.mq5', 'folder': 'Bollinger and Envelope candle extremes', 'inputs': [{'mql': 'bbperiod', 'py': 'bbperiod', 'param': 'bbperiod', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'bbDeviations', 'py': 'bbDeviations', 'param': 'bbDeviations', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'envelopeperiod', 'py': 'envelopeperiod', 'param': 'envelopeperiod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'envelopeDeviation', 'py': 'envelopeDeviation', 'param': 'envelopeDeviation', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'Send_Email', 'py': 'Send_Email', 'param': 'Send_Email', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Audible_Alerts', 'py': 'Audible_Alerts', 'param': 'Audible_Alerts', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Push_Notifications', 'py': 'Push_Notifications', 'param': 'Push_Notifications', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
bbperiod = _input('bbperiod', 20)
bbDeviations = _input('bbDeviations', 2.0)
envelopeperiod = _input('envelopeperiod', 14)
envelopeDeviation = _input('envelopeDeviation', 0.5)
time_alert = 0  # used when sending alert
Send_Email = _input('Send_Email', True)
Audible_Alerts = _input('Audible_Alerts', True)
Push_Notifications = _input('Push_Notifications', True)
myPoint = 0.0  # initialized in OnInit
Open = Arr(0, 0.0)
Bands_handle = 0
Bands_Lower = Arr(0, 0.0)
Close = Arr(0, 0.0)
Envelopes_handle = 0
Envelopes_Lower = Arr(0, 0.0)
Low = Arr(0, 0.0)
Bands_Upper = Arr(0, 0.0)
Envelopes_Upper = Arr(0, 0.0)
High = Arr(0, 0.0)

def myAlert(type_, message):
    handle = 0
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | bb envelope ind @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass
    elif type_ == 'indicator':
        Print(type_ + ' | bb envelope ind @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Audible_Alerts:
            Alert(type_ + ' | bb envelope ind @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Send_Email:
            SendMail('bb envelope ind', type_ + ' | bb envelope ind @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        handle = FileOpen('bb envelope ind.txt', (((FILE_TXT | FILE_READ) | FILE_WRITE) | FILE_SHARE_READ) | FILE_SHARE_WRITE, 59)
        if handle != INVALID_HANDLE:
            FileSeek(handle, 0, SEEK_END)
            FileWrite(handle, type_ + ' | bb envelope ind @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
            FileClose(handle)
        if Push_Notifications:
            SendNotification(type_ + ' | bb envelope ind @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)

def OnInit():
    global Bands_handle, Envelopes_handle, myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    SetIndexBuffer(1, Buffer2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    Bands_handle = iBands(None, PERIOD_CURRENT, bbperiod, 0, bbDeviations, PRICE_CLOSE)
    if Bands_handle < 0:
        Print('The creation of iBands has failed: Bands_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    Envelopes_handle = iEnvelopes(None, PERIOD_CURRENT, envelopeperiod, 0, MODE_SMA, PRICE_CLOSE, envelopeDeviation)
    if Envelopes_handle < 0:
        Print('The creation of iEnvelopes has failed: Envelopes_handle=', INVALID_HANDLE)
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
    if CopyOpen(Symbol(), PERIOD_CURRENT, 0, rates_total, Open) <= 0:
        return rates_total
    ArraySetAsSeries(Open, True)
    if BarsCalculated(Bands_handle) <= 0:
        return 0
    if CopyBuffer(Bands_handle, LOWER_BAND, 0, rates_total, Bands_Lower) <= 0:
        return rates_total
    ArraySetAsSeries(Bands_Lower, True)
    if CopyClose(Symbol(), PERIOD_CURRENT, 0, rates_total, Close) <= 0:
        return rates_total
    ArraySetAsSeries(Close, True)
    if BarsCalculated(Envelopes_handle) <= 0:
        return 0
    if CopyBuffer(Envelopes_handle, LOWER_LINE, 0, rates_total, Envelopes_Lower) <= 0:
        return rates_total
    ArraySetAsSeries(Envelopes_Lower, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, 0, rates_total, Low) <= 0:
        return rates_total
    ArraySetAsSeries(Low, True)
    if BarsCalculated(Bands_handle) <= 0:
        return 0
    if CopyBuffer(Bands_handle, UPPER_BAND, 0, rates_total, Bands_Upper) <= 0:
        return rates_total
    ArraySetAsSeries(Bands_Upper, True)
    if BarsCalculated(Envelopes_handle) <= 0:
        return 0
    if CopyBuffer(Envelopes_handle, UPPER_LINE, 0, rates_total, Envelopes_Upper) <= 0:
        return rates_total
    ArraySetAsSeries(Envelopes_Upper, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, 0, rates_total, High) <= 0:
        return rates_total
    ArraySetAsSeries(High, True)
    if CopyTime(Symbol(), Period(), 0, rates_total, Time) <= 0:
        return rates_total
    ArraySetAsSeries(Time, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if (((Open[1 + i] < Bands_Lower[1 + i] and Close[1 + i] < Bands_Lower[1 + i]) and Open[1 + i] < Envelopes_Lower[1 + i]) and Close[1 + i] < Envelopes_Lower[1 + i]) and Open[1 + i] < Close[1 + i]:
            Buffer1[i] = Low[1 + i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Buy')
            time_alert = Time[1]
        else:
            Buffer1[i] = EMPTY_VALUE
        if (((Open[1 + i] > Bands_Upper[1 + i] and Close[1 + i] > Bands_Upper[1 + i]) and Open[1 + i] > Envelopes_Upper[1 + i]) and Close[1 + i] > Envelopes_Upper[1 + i]) and Open[1 + i] > Close[1 + i]:
            Buffer2[i] = High[1 + i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'sell')
            time_alert = Time[1]
        else:
            Buffer2[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BbEnvelopeIndicator(_MQL5Indicator):
    name = 'bb envelope indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'bbperiod': 20,
        'bbDeviations': 2.0,
        'envelopeperiod': 14,
        'envelopeDeviation': 0.5,
        'Send_Email': True,
        'Audible_Alerts': True,
        'Push_Notifications': True,
    }

