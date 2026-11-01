"""Reversal — converted from MQL5: MQL5 Indicators/Reversal/Reversal.mq5

Copyright: Sergey Vradiy; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Sergey Vradiy', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16755200]}, 'widths': {1: 3, 2: 3}, 'styles': {}, 'labels': {1: 'Sell', 2: 'Buy'}, 'levels': [], 'description': [''], 'name': 'Reversal', 'source': 'MQL5 Indicators/Reversal/Reversal.mq5', 'folder': 'Reversal', 'inputs': [{'mql': 'Interval', 'py': 'Interval', 'param': 'Interval', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Send_Email', 'py': 'Send_Email', 'param': 'Send_Email', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
Interval = _input('Interval', 10)
time_alert = 0  # used when sending alert
Send_Email = _input('Send_Email', True)
myPoint = 0.0  # initialized in OnInit
High = Arr(0, 0.0)
Close = Arr(0, 0.0)
Open = Arr(0, 0.0)
Low = Arr(0, 0.0)

def myAlert(type_, message):
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | reversal @ ' + Symbol() + ',' + _str(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass
    elif type_ == 'indicator':
        if Send_Email:
            SendMail('reversal', type_ + ' | reversal @ ' + Symbol() + ',' + _str(Period()) + ' | ' + message)

def DrawLine(objname, price, count, start_index):
    if price < 0 and ObjectFind(0, objname) >= 0:
        ObjectDelete(0, objname)
    elif ObjectFind(0, objname) >= 0 and ObjectGetInteger(0, objname, OBJPROP_TYPE) == OBJ_TREND:
        Time = Arr(0, 0)
        ArraySetAsSeries(Time, True)
        CopyTime(Symbol(), Period(), 0, start_index + count, Time)
        ObjectSetInteger(0, objname, OBJPROP_TIME, Time[start_index])
        ObjectSetDouble(0, objname, OBJPROP_PRICE, price)
        ObjectSetInteger(0, objname, OBJPROP_TIME, 1, Time[start_index + count - 1])
        ObjectSetDouble(0, objname, OBJPROP_PRICE, 1, price)
    else:
        Time = Arr(0, 0)
        ArraySetAsSeries(Time, True)
        CopyTime(Symbol(), Period(), 0, start_index + count, Time)
        ObjectCreate(0, objname, OBJ_TREND, 0, Time[start_index], price, Time[start_index + count - 1], price)
        ObjectSetInteger(0, objname, OBJPROP_RAY_LEFT, 0)
        ObjectSetInteger(0, objname, OBJPROP_RAY_RIGHT, 0)
        ObjectSetInteger(0, objname, OBJPROP_COLOR, 0xFF0000)
        ObjectSetInteger(0, objname, OBJPROP_STYLE, STYLE_SOLID)
        ObjectSetInteger(0, objname, OBJPROP_WIDTH, 2)

def Support(time_interval, fixed_tod, hh, mm, draw, shift):
    start_index = shift
    count = _idiv(time_interval, PeriodSeconds())
    if fixed_tod:
        start_time = 0
        Time = Arr(0, 0)
        ArraySetAsSeries(Time, True)
        CopyTime(Symbol(), Period(), 0, Bars(Symbol(), Period()) - count, Time)
        if shift == 0:
            start_time = TimeCurrent()
        else:
            start_time = Time[shift - 1]
        dt = StringToTime(TimeToString(start_time, TIME_DATE) + ' ' + _str(hh) + ':' + _str(mm))
        if dt > start_time:
            dt -= 86400
        dt_index = iBarShift_u(Symbol(), Period(), dt, True)
        dt2 = dt
        while dt_index < 0 and dt > Time[Bars(Symbol(), Period()) - 1 - count]:
            dt -= 86400
            dt_index = iBarShift_u(Symbol(), Period(), dt, True)
        if dt_index < 0:
            dt_index = iBarShift_u(Symbol(), Period(), dt2, False)
        start_index = dt_index + 1
    _Low = Arr(0, 0.0)
    ArraySetAsSeries(_Low, True)
    CopyLow(Symbol(), Period(), start_index, count, _Low)
    ret = _Low[ArrayMinimum(_Low, 0, count)]
    if draw:
        DrawLine('Support', ret, count, start_index)
    return ret

def Resistance(time_interval, fixed_tod, hh, mm, draw, shift):
    start_index = shift
    count = _idiv(time_interval, PeriodSeconds())
    if fixed_tod:
        start_time = 0
        Time = Arr(0, 0)
        ArraySetAsSeries(Time, True)
        CopyTime(Symbol(), Period(), 0, Bars(Symbol(), Period()) - count, Time)
        if shift == 0:
            start_time = TimeCurrent()
        else:
            start_time = Time[shift - 1]
        dt = StringToTime(TimeToString(start_time, TIME_DATE) + ' ' + _str(hh) + ':' + _str(mm))
        if dt > start_time:
            dt -= 86400
        dt_index = iBarShift_u(Symbol(), Period(), dt, True)
        dt2 = dt
        while dt_index < 0 and dt > Time[Bars(Symbol(), Period()) - 1 - count]:
            dt -= 86400
            dt_index = iBarShift_u(Symbol(), Period(), dt, True)
        if dt_index < 0:
            dt_index = iBarShift_u(Symbol(), Period(), dt2, False)
        start_index = dt_index + 1
    _High = Arr(0, 0.0)
    ArraySetAsSeries(_High, True)
    CopyHigh(Symbol(), Period(), start_index, count, _High)
    ret = _High[ArrayMaximum(_High, 0, count)]
    if draw:
        DrawLine('Resistance', ret, count, start_index)
    return ret

def iBarShift_u(symbol, timeframe, time, exact=False):
    LastBar = Box(0)
    if not SeriesInfoInteger(symbol, timeframe, SERIES_LASTBAR_DATE, LastBar):
        opentimelastbar = Arr(1, 0, dyn=False)
        if CopyTime(symbol, timeframe, 0, 1, opentimelastbar) == 1:
            LastBar.v = opentimelastbar[0]
        else:
            return -1
    shift = Bars(symbol, timeframe, time, LastBar.v)
    checkcandle = Arr(1, 0, dyn=False)
    if CopyTime(symbol, timeframe, _DT(time), 1, checkcandle) == 1:
        if checkcandle[0] == time:
            return shift - 1
        elif exact and time > (checkcandle[0] + PeriodSeconds(timeframe)):
            return -1
        else:
            return shift
    return -1

def OnInit():
    global myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_ARROW, 242)
    SetIndexBuffer(1, Buffer2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_ARROW, 241)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global time_alert
    limit = rates_total - prev_calculated
    ArraySetAsSeries(Buffer1, True)
    ArraySetAsSeries(Buffer2, True)
    if prev_calculated < 1:
        ArrayInitialize(Buffer1, 0)
        ArrayInitialize(Buffer2, 0)
    else:
        limit += 1
    Time = Arr(0, 0)
    if CopyHigh(Symbol(), PERIOD_H6, 0, rates_total, High) <= 0:
        return rates_total
    ArraySetAsSeries(High, True)
    if CopyClose(Symbol(), PERIOD_H6, 0, rates_total, Close) <= 0:
        return rates_total
    ArraySetAsSeries(Close, True)
    if CopyOpen(Symbol(), PERIOD_H6, 0, rates_total, Open) <= 0:
        return rates_total
    ArraySetAsSeries(Open, True)
    if CopyLow(Symbol(), PERIOD_H6, 0, rates_total, Low) <= 0:
        return rates_total
    ArraySetAsSeries(Low, True)
    if CopyTime(Symbol(), Period(), 0, rates_total, Time) <= 0:
        return rates_total
    ArraySetAsSeries(Time, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if High[1 + i] == Resistance(Interval * PeriodSeconds(), False, 0, 0, False, i) and Close[1 + i] < Open[1 + i]:
            Buffer1[i] = High[i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Sell')
            time_alert = Time[1]
        else:
            Buffer1[i] = 0.0
        if Low[1 + i] == Support(Interval * PeriodSeconds(), False, 0, 0, False, i) and Close[1 + i] > Open[1 + i]:
            Buffer2[i] = Low[i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'Buy')
            time_alert = Time[1]
        else:
            Buffer2[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Reversal(_MQL5Indicator):
    name = 'Reversal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Interval': 10,
        'Send_Email': True,
    }

