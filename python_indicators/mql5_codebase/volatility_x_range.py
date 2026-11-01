"""Volatility_x_Range — converted from MQL5: MQL5 Indicators/Volatility vs Range/Volatility_x_Range.mq5

Copyright: Created by TheCoder; Link: https://www.mql5.com/en/users/brazilianguy3; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Created by TheCoder', 'link': 'https://www.mql5.com/en/users/brazilianguy3', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16755200]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Ratio'}, 'levels': [], 'description': [''], 'name': 'Volatility_x_Range', 'source': 'MQL5 Indicators/Volatility vs Range/Volatility_x_Range.mq5', 'folder': 'Volatility vs Range', 'inputs': [{'mql': 'Periods', 'py': 'Periods', 'param': 'Periods', 'type': 'int', 'default': 2000, 'label': 'Amount of candles to be considered', 'sinput': False}, {'mql': 'ShowCalculationLimits', 'py': 'ShowCalculationLimits', 'param': 'ShowCalculationLimits', 'type': 'bool', 'default': True, 'label': 'Show range of candles on the screen', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Periods = _input('Periods', 2000)  # Amount of candles to be considered
ShowCalculationLimits = _input('ShowCalculationLimits', True)  # Show range of candles on the screen
myPoint = 0.0  # initialized in OnInit
ATR_handle = 0
ATR = Arr(0, 0.0)

def myAlert(type_, message):
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | Volatility_x_Range @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass

def DrawLine(objname, price, count, start_index):
    if price < 0 and ObjectFind(0, objname) >= 0:
        ObjectDelete(0, objname)
    elif ObjectFind(0, objname) >= 0 and ObjectGetInteger(0, objname, OBJPROP_TYPE) == OBJ_TREND:
        cTime = Arr(0, 0)
        ArraySetAsSeries(cTime, True)
        CopyTime(Symbol(), Period(), 0, start_index + count, cTime)
        ObjectSetInteger(0, objname, OBJPROP_TIME, cTime[start_index])
        ObjectSetDouble(0, objname, OBJPROP_PRICE, price)
        ObjectSetInteger(0, objname, OBJPROP_TIME, 1, cTime[start_index + count - 1])
        ObjectSetDouble(0, objname, OBJPROP_PRICE, 1, price)
    else:
        cTime = Arr(0, 0)
        ArraySetAsSeries(cTime, True)
        CopyTime(Symbol(), Period(), 0, start_index + count, cTime)
        ObjectCreate(0, objname, OBJ_TREND, 0, cTime[start_index], price, cTime[start_index + count - 1], price)
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
        cTime = Arr(0, 0)
        ArraySetAsSeries(cTime, True)
        CopyTime(Symbol(), Period(), 0, Bars(Symbol(), Period()) - count, cTime)
        if shift == 0:
            start_time = TimeCurrent()
        else:
            start_time = cTime[shift - 1]
        dt = StringToTime(TimeToString(start_time, TIME_DATE) + ' ' + IntegerToString(hh) + ':' + IntegerToString(mm))
        if dt > start_time:
            dt -= 86400
        dt_index = iBarShift(Symbol(), Period(), dt, True)
        dt2 = dt
        while dt_index < 0 and dt > cTime[Bars(Symbol(), Period()) - 1 - count]:
            dt -= 86400
            dt_index = iBarShift(Symbol(), Period(), dt, True)
        if dt_index < 0:
            dt_index = iBarShift(Symbol(), Period(), dt2, False)
        start_index = dt_index + 1
    cLow = Arr(0, 0.0)
    ArraySetAsSeries(cLow, True)
    CopyLow(Symbol(), Period(), start_index, count, cLow)
    ret = cLow[ArrayMinimum(cLow, 0, count)]
    if draw:
        DrawLine('Support', ret, count, start_index)
    return ret

def Resistance(time_interval, fixed_tod, hh, mm, draw, shift):
    start_index = shift
    count = _idiv(time_interval, PeriodSeconds())
    if fixed_tod:
        start_time = 0
        cTime = Arr(0, 0)
        ArraySetAsSeries(cTime, True)
        CopyTime(Symbol(), Period(), 0, Bars(Symbol(), Period()) - count, cTime)
        if shift == 0:
            start_time = TimeCurrent()
        else:
            start_time = cTime[shift - 1]
        dt = StringToTime(TimeToString(start_time, TIME_DATE) + ' ' + IntegerToString(hh) + ':' + IntegerToString(mm))
        if dt > start_time:
            dt -= 86400
        dt_index = iBarShift(Symbol(), Period(), dt, True)
        dt2 = dt
        while dt_index < 0 and dt > cTime[Bars(Symbol(), Period()) - 1 - count]:
            dt -= 86400
            dt_index = iBarShift(Symbol(), Period(), dt, True)
        if dt_index < 0:
            dt_index = iBarShift(Symbol(), Period(), dt2, False)
        start_index = dt_index + 1
    cHigh = Arr(0, 0.0)
    ArraySetAsSeries(cHigh, True)
    CopyHigh(Symbol(), Period(), start_index, count, cHigh)
    ret = cHigh[ArrayMaximum(cHigh, 0, count)]
    if draw:
        DrawLine('Resistance', ret, count, start_index)
    return ret

def OnInit():
    global ATR_handle, myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    ATR_handle = iATR(None, PERIOD_CURRENT, Periods)
    if ATR_handle < 0:
        Print('The creation of iATR has failed: ATR_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = rates_total - prev_calculated
    ArraySetAsSeries(Buffer1, True)
    if prev_calculated < 1:
        ArrayInitialize(Buffer1, 0)
    else:
        limit += 1
    if BarsCalculated(ATR_handle) <= 0:
        return 0
    if CopyBuffer(ATR_handle, 0, 0, rates_total, ATR) <= 0:
        return rates_total
    ArraySetAsSeries(ATR, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if True:
            Buffer1[i] = _fdiv(Resistance(Periods * PeriodSeconds(), False, 0, 0, ShowCalculationLimits, i) - Support(Periods * PeriodSeconds(), False, 0, 0, ShowCalculationLimits, i), ATR[i] * Periods)
        else:
            Buffer1[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityXRange(_MQL5Indicator):
    name = 'Volatility_x_Range'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Periods': 2000,  # Amount of candles to be considered
        'ShowCalculationLimits': True,  # Show range of candles on the screen
    }

