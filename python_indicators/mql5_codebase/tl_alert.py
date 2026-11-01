"""TL ALERT — converted from MQL5: MQL5 Indicators/Trendline Alert V1/TL ALERT.mq5

Copyright: www.metatrader5software.store; Link: www.metatrader5software.store; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.metatrader5software.store', 'link': 'www.metatrader5software.store', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [27391], 2: [16774912]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'sell', 2: 'buy'}, 'levels': [], 'description': [''], 'name': 'TL ALERT', 'source': 'MQL5 Indicators/Trendline Alert V1/TL ALERT.mq5', 'folder': 'Trendline Alert V1', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
time_alert = 0  # used when sending alert
Send_Email = True
Audible_Alerts = True
Push_Notifications = True
myPoint = 0.0  # initialized in OnInit
Close = Arr(0, 0.0)
Low = Arr(0, 0.0)

def myAlert(type_, message):
    handle = 0
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | TL ALERT @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass
    elif type_ == 'indicator':
        Print(type_ + ' | TL ALERT @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Audible_Alerts:
            Alert(type_ + ' | TL ALERT @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        if Send_Email:
            SendMail('TL ALERT', type_ + ' | TL ALERT @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
        handle = FileOpen('TL ALERT.txt', (((FILE_TXT | FILE_READ) | FILE_WRITE) | FILE_SHARE_READ) | FILE_SHARE_WRITE, 59)
        if handle != INVALID_HANDLE:
            FileSeek(handle, 0, SEEK_END)
            FileWrite(handle, type_ + ' | TL ALERT @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
            FileClose(handle)
        if Push_Notifications:
            SendNotification(type_ + ' | TL ALERT @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)

def TrendlinePriceUpper(shift):
    obj_total = ObjectsTotal(0)
    maxprice = -1.0
    for i in range(obj_total - 1, 0 - 1, -1):
        name = ObjectName(0, i)
        price = 0.0
        if ((ObjectGetInteger(0, name, OBJPROP_TYPE) == OBJ_HLINE and StringFind(name, '#', 0) < 0) and (price := ObjectGetDouble(0, name, OBJPROP_PRICE)) > maxprice) and price > 0:
            maxprice = price
        elif ObjectGetInteger(0, name, OBJPROP_TYPE) == OBJ_TREND and StringFind(name, '#', 0) < 0:
            cTime = Arr(0, 0)
            ArraySetAsSeries(cTime, True)
            CopyTime(Symbol(), Period(), 0, 1, cTime)
            price = ObjectGetValueByTime(0, name, cTime[0], 0)
            if price > maxprice and price > 0:
                maxprice = price
    return maxprice

def TrendlinePriceLower(shift):
    obj_total = ObjectsTotal(0)
    minprice = MathPow(10, 308)
    for i in range(obj_total - 1, 0 - 1, -1):
        name = ObjectName(0, i)
        price = 0.0
        if ((ObjectGetInteger(0, name, OBJPROP_TYPE) == OBJ_HLINE and StringFind(name, '#', 0) < 0) and (price := ObjectGetDouble(0, name, OBJPROP_PRICE)) < minprice) and price > 0:
            minprice = price
        elif ObjectGetInteger(0, name, OBJPROP_TYPE) == OBJ_TREND and StringFind(name, '#', 0) < 0:
            cTime = Arr(0, 0)
            ArraySetAsSeries(cTime, True)
            CopyTime(Symbol(), Period(), 0, 1, cTime)
            price = ObjectGetValueByTime(0, name, cTime[0], 0)
            if price < minprice and price > 0:
                minprice = price
    if minprice > MathPow(10, 307):
        minprice = -1.0
    return minprice

def OnInit():
    global myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MathMax(Bars(Symbol(), PERIOD_CURRENT) - 5000 + 1, 50 + 1))
    SetIndexBuffer(1, Buffer2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, MathMax(Bars(Symbol(), PERIOD_CURRENT) - 5000 + 1, 50 + 1))
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
        ArrayInitialize(Buffer1, EMPTY_VALUE)
        ArrayInitialize(Buffer2, EMPTY_VALUE)
    else:
        limit += 1
    Time = Arr(0, 0)
    if TrendlinePriceUpper(0) < 0 and TrendlinePriceLower(0) < 0:
        return rates_total
    if CopyClose(Symbol(), PERIOD_CURRENT, 0, rates_total, Close) <= 0:
        return rates_total
    ArraySetAsSeries(Close, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, 0, rates_total, Low) <= 0:
        return rates_total
    ArraySetAsSeries(Low, True)
    if CopyTime(Symbol(), Period(), 0, rates_total, Time) <= 0:
        return rates_total
    ArraySetAsSeries(Time, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if Close[1 + i] < TrendlinePriceLower(i):
            Buffer1[i] = Low[1 + i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'sell')
            time_alert = Time[1]
        else:
            Buffer1[i] = EMPTY_VALUE
        if Close[1 + i] > TrendlinePriceUpper(i):
            Buffer2[i] = Low[1 + i]
            if i == 1 and Time[1] != time_alert:
                myAlert('indicator', 'buy')
            time_alert = Time[1]
        else:
            Buffer2[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TLALERT(_MQL5Indicator):
    name = 'TL ALERT'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

