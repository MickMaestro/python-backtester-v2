"""kajan trade expert — converted from MQL5: MQL5 Indicators/Kajan trade expert/kajan trade expert.mq5

Copyright: Copyright 2021, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16755200], 2: [255]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Buy', 2: 'Sell'}, 'levels': [], 'description': [], 'name': 'kajan trade expert', 'source': 'MQL5 Indicators/Kajan trade expert/kajan trade expert.mq5', 'folder': 'Kajan trade expert', 'inputs': [{'mql': 'Audible_Alerts', 'py': 'Audible_Alerts', 'param': 'Audible_Alerts', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
time_alert = 0  # used when sending alert
Audible_Alerts = _input('Audible_Alerts', True)
myPoint = 0.0  # initialized in OnInit
Stochastic_handle = 0
Stochastic_Main = Arr(0, 0.0)
Stochastic_Signal = Arr(0, 0.0)
Low = Arr(0, 0.0)
ATR_handle = 0
ATR = Arr(0, 0.0)
High = Arr(0, 0.0)

def myAlert(type_, message):
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | kajan trade expert @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass
    elif type_ == 'indicator':
        if Audible_Alerts:
            Alert(type_ + ' | kajan trade expert @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)

def OnInit():
    global ATR_handle, Stochastic_handle, myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    SetIndexBuffer(1, Buffer2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    Stochastic_handle = iStochastic(None, PERIOD_CURRENT, 5, 3, 3, MODE_SMA, STO_LOWHIGH)
    if Stochastic_handle < 0:
        Print('The creation of iStochastic has failed: Stochastic_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    ATR_handle = iATR(None, PERIOD_CURRENT, 14)
    if ATR_handle < 0:
        Print('The creation of iATR has failed: ATR_handle=', INVALID_HANDLE)
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
    if BarsCalculated(Stochastic_handle) <= 0:
        return 0
    if CopyBuffer(Stochastic_handle, MAIN_LINE, 0, rates_total, Stochastic_Main) <= 0:
        return rates_total
    ArraySetAsSeries(Stochastic_Main, True)
    if BarsCalculated(Stochastic_handle) <= 0:
        return 0
    if CopyBuffer(Stochastic_handle, SIGNAL_LINE, 0, rates_total, Stochastic_Signal) <= 0:
        return rates_total
    ArraySetAsSeries(Stochastic_Signal, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, 0, rates_total, Low) <= 0:
        return rates_total
    ArraySetAsSeries(Low, True)
    if BarsCalculated(ATR_handle) <= 0:
        return 0
    if CopyBuffer(ATR_handle, 0, 0, rates_total, ATR) <= 0:
        return rates_total
    ArraySetAsSeries(ATR, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, 0, rates_total, High) <= 0:
        return rates_total
    ArraySetAsSeries(High, True)
    if CopyTime(Symbol(), Period(), 0, rates_total, Time) <= 0:
        return rates_total
    ArraySetAsSeries(Time, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if (Stochastic_Main[i] > Stochastic_Signal[i] and Stochastic_Main[i + 1] < Stochastic_Signal[i + 1]) and Stochastic_Main[i] < 20:
            Buffer1[i] = Low[i] - ATR[i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Buy')
            time_alert = Time[1]
        else:
            Buffer1[i] = EMPTY_VALUE
        if (Stochastic_Main[i] < Stochastic_Signal[i] and Stochastic_Main[i + 1] > Stochastic_Signal[i + 1]) and Stochastic_Main[i] > 20:
            Buffer2[i] = High[i] + ATR[i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Sell')
            time_alert = Time[1]
        else:
            Buffer2[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KajanTradeExpert(_MQL5Indicator):
    name = 'kajan trade expert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Audible_Alerts': True,
    }

