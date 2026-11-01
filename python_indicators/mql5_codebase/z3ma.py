"""Z3MA — converted from MQL5: MQL5 Indicators/Swing trading 3 EMA Crossover MQL5/Z3MA.mq5

Copyright: Copyright 2020, Hassane Zibara.; Link: https://www.mql5.com/en/users/377812; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Hassane Zibara.', 'link': 'https://www.mql5.com/en/users/377812', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16755200], 2: [255], 3: [61183], 4: [16755200], 5: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {3: 0, 4: 0, 5: 0}, 'labels': {1: 'Buy', 2: 'Sell', 3: 'long term', 4: 'fast', 5: 'slow'}, 'levels': [], 'description': [], 'name': 'Z3MA', 'source': 'MQL5 Indicators/Swing trading 3 EMA Crossover MQL5/Z3MA.mq5', 'folder': 'Swing trading 3 EMA Crossover MQL5', 'inputs': [{'mql': 'MA1_', 'py': 'MA1_', 'param': None, 'type': 'string', 'default': 'Gold', 'label': '', 'sinput': False}, {'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'MAMethod1', 'py': 'MAMethod1', 'param': 'MAMethod1', 'type': 'int', 'default': 1, 'label': 'MA1 method', 'sinput': False}, {'mql': 'MAPrice1', 'py': 'MAPrice1', 'param': 'MAPrice1', 'type': 'int', 'default': 1, 'label': 'MA1 price', 'sinput': False}, {'mql': 'MA2_', 'py': 'MA2_', 'param': None, 'type': 'string', 'default': 'blue', 'label': '', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'MAMethod2', 'py': 'MAMethod2', 'param': 'MAMethod2', 'type': 'int', 'default': 1, 'label': 'MA2 method', 'sinput': False}, {'mql': 'MAPrice2', 'py': 'MAPrice2', 'param': 'MAPrice2', 'type': 'int', 'default': 1, 'label': 'MA2 price', 'sinput': False}, {'mql': 'MA3_', 'py': 'MA3_', 'param': None, 'type': 'string', 'default': 'Red', 'label': '', 'sinput': False}, {'mql': 'Period3', 'py': 'Period3', 'param': 'Period3', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'MAMethod3', 'py': 'MAMethod3', 'param': 'MAMethod3', 'type': 'int', 'default': 1, 'label': 'MA3 method', 'sinput': False}, {'mql': 'MAPrice3', 'py': 'MAPrice3', 'param': 'MAPrice3', 'type': 'int', 'default': 1, 'label': 'MA3 price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
Buffer3 = Arr(0, 0.0)
Buffer4 = Arr(0, 0.0)
Buffer5 = Arr(0, 0.0)
MA1_ = _input('MA1_', 'Gold')
Period1 = _input('Period1', 55)
MAMethod1 = _input('MAMethod1', MODE_EMA)  # MA1 method
MAPrice1 = _input('MAPrice1', PRICE_CLOSE)  # MA1 price
MA2_ = _input('MA2_', 'blue')
Period2 = _input('Period2', 9)
MAMethod2 = _input('MAMethod2', MODE_EMA)  # MA2 method
MAPrice2 = _input('MAPrice2', PRICE_CLOSE)  # MA2 price
MA3_ = _input('MA3_', 'Red')
Period3 = _input('Period3', 21)
MAMethod3 = _input('MAMethod3', MODE_EMA)  # MA3 method
MAPrice3 = _input('MAPrice3', PRICE_CLOSE)  # MA3 price
time_alert = 0  # used when sending alert
Audible_Alerts = True
myPoint = 0.0  # initialized in OnInit
MA_handle = 0
MA = Arr(0, 0.0)
MA_handle2 = 0
MA2 = Arr(0, 0.0)
MA_handle3 = 0
MA3 = Arr(0, 0.0)
Low = Arr(0, 0.0)
High = Arr(0, 0.0)

def myAlert(type_, message):
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | Z3MA @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'indicator':
        Print(type_ + ' | Z3MA @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Audible_Alerts:
            Alert(type_ + ' | Z3MA @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)

def OnInit():
    global MA_handle, MA_handle2, MA_handle3, myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    SetIndexBuffer(1, Buffer2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    SetIndexBuffer(2, Buffer3)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, Buffer4)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, Buffer5)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    MA_handle = iMA(None, PERIOD_CURRENT, Period2, 0, MAMethod2, MAPrice2)
    if MA_handle < 0:
        Print('The creation of iMA has failed: MA_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    MA_handle2 = iMA(None, PERIOD_CURRENT, Period3, 0, MAMethod3, MAPrice3)
    if MA_handle2 < 0:
        Print('The creation of iMA has failed: MA_handle2=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    MA_handle3 = iMA(None, PERIOD_CURRENT, Period1, 0, MAMethod1, MAPrice1)
    if MA_handle3 < 0:
        Print('The creation of iMA has failed: MA_handle3=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global time_alert
    limit = rates_total - prev_calculated
    ArraySetAsSeries(Buffer1, True)
    ArraySetAsSeries(Buffer2, True)
    ArraySetAsSeries(Buffer3, True)
    ArraySetAsSeries(Buffer4, True)
    ArraySetAsSeries(Buffer5, True)
    if prev_calculated < 1:
        ArrayInitialize(Buffer1, EMPTY_VALUE)
        ArrayInitialize(Buffer2, EMPTY_VALUE)
        ArrayInitialize(Buffer3, EMPTY_VALUE)
        ArrayInitialize(Buffer4, EMPTY_VALUE)
        ArrayInitialize(Buffer5, EMPTY_VALUE)
    else:
        limit += 1
    Time = Arr(0, 0)
    if BarsCalculated(MA_handle) <= 0:
        return 0
    if CopyBuffer(MA_handle, 0, 0, rates_total, MA) <= 0:
        return rates_total
    ArraySetAsSeries(MA, True)
    if BarsCalculated(MA_handle2) <= 0:
        return 0
    if CopyBuffer(MA_handle2, 0, 0, rates_total, MA2) <= 0:
        return rates_total
    ArraySetAsSeries(MA2, True)
    if BarsCalculated(MA_handle3) <= 0:
        return 0
    if CopyBuffer(MA_handle3, 0, 0, rates_total, MA3) <= 0:
        return rates_total
    ArraySetAsSeries(MA3, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, 0, rates_total, Low) <= 0:
        return rates_total
    ArraySetAsSeries(Low, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, 0, rates_total, High) <= 0:
        return rates_total
    ArraySetAsSeries(High, True)
    if CopyTime(Symbol(), Period(), 0, rates_total, Time) <= 0:
        return rates_total
    ArraySetAsSeries(Time, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if ((MA[i] > MA2[i] and MA[i + 1] < MA2[i + 1]) and MA3[i] < MA[i]) and MA3[i] < MA2[i]:
            Buffer1[i] = Low[1 + i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Buy')
            time_alert = Time[1]
        else:
            Buffer1[i] = EMPTY_VALUE
        if ((MA[i] < MA2[i] and MA[i + 1] > MA2[i + 1]) and MA3[i] > MA[i]) and MA3[i] > MA2[i]:
            Buffer2[i] = High[1 + i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Sell')
            time_alert = Time[1]
        else:
            Buffer2[i] = EMPTY_VALUE
        if True:
            Buffer3[i] = MA3[i]
            if i == 1 and Time[1] != time_alert:
                time_alert = Time[1]
        else:
            Buffer3[i] = EMPTY_VALUE
        if True:
            Buffer4[i] = MA[i]
            if i == 1 and Time[1] != time_alert:
                time_alert = Time[1]
        else:
            Buffer4[i] = EMPTY_VALUE
        if True:
            Buffer5[i] = MA2[i]
            if i == 1 and Time[1] != time_alert:
                time_alert = Time[1]
        else:
            Buffer5[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Z3MA(_MQL5Indicator):
    name = 'Z3MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period1': 55,
        'MAMethod1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA1 method
        'MAPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA1 price
        'Period2': 9,
        'MAMethod2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA2 method
        'MAPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA2 price
        'Period3': 21,
        'MAMethod3': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA3 method
        'MAPrice3': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA3 price
    }

