"""stalin — converted from MQL5: MQL5 Indicators/Stalin/stalin.mq5

Copyright: Copyright © 2011, Andrey Vassiliev (MoneyJinn); Link: http://www.vassiliev.ru/; Version: 2.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Andrey Vassiliev (MoneyJinn)', 'link': 'http://www.vassiliev.ru/', 'version': '2.0', 'window': 'chart', 'indicator_plots': 2, 'indicator_buffers': 2}, 'types': {}, 'colors': {1: [16436871], 2: [12695295]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'stalin', 'source': 'MQL5 Indicators/Stalin/stalin.mq5', 'folder': 'Stalin', 'inputs': [{'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Fast', 'py': 'Fast', 'param': 'Fast', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Slow', 'py': 'Slow', 'param': 'Slow', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'RSI', 'py': 'RSI', 'param': 'RSI', 'type': 'int', 'default': 17, 'label': '', 'sinput': False}, {'mql': 'Confirm', 'py': 'Confirm', 'param': 'Confirm', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'Flat', 'py': 'Flat', 'param': 'Flat', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'SoundAlert', 'py': 'SoundAlert', 'param': 'SoundAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EmailAlert', 'py': 'EmailAlert', 'param': 'EmailAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAMethod = _input('MAMethod', 1)
MAShift = _input('MAShift', 0)
Fast = _input('Fast', 14)
Slow = _input('Slow', 21)
RSI = _input('RSI', 17)
Confirm = _input('Confirm', 0.0)
Flat = _input('Flat', 0.0)
SoundAlert = _input('SoundAlert', False)
EmailAlert = _input('EmailAlert', False)
MA1 = 0
MA2 = 0
RS = 0
B1 = Arr(0, 0.0)
B2 = Arr(0, 0.0)
IUP = 0.0
IDN = 0.0
E1 = 0.0
E2 = 0.0
Confirm2 = 0.0
Flat2 = 0.0
MAMethod2 = 0

def OnInit():
    global Confirm2, Flat2, MA1, MA2, MAMethod2, RS
    CLR()
    if Digits() == 3 or Digits() == 5:
        Confirm2 = Confirm * 10
        Flat2 = Flat * 10
    else:
        Confirm2 = Confirm
        Flat2 = Flat
    MAMethod2 = MethodMigrate(MAMethod)
    SetIndexBuffer(0, B1, INDICATOR_DATA)
    ArraySetAsSeries(B1, True)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    SetIndexBuffer(1, B2, INDICATOR_DATA)
    ArraySetAsSeries(B2, True)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    MA1 = iMA(None, 0, Fast, MAShift, MAMethod2, PRICE_CLOSE)
    MA2 = iMA(None, 0, Slow, MAShift, MAMethod2, PRICE_CLOSE)
    if RSI > 0:
        RS = iRSI(None, 0, RSI, PRICE_CLOSE)

def CLR():
    global E1, E2, IDN, IUP
    if ArraySize(B1) > 0:
        ArrayInitialize(B1, 0)
        ArrayInitialize(B2, 0)
    IUP = 0.0
    IDN = 0.0
    E1 = 0.0
    E2 = 0.0

def iMA1(bar):
    IB = Arr(1, 0.0, dyn=False)
    CopyBuffer(MA1, 0, bar, 1, IB)
    return IB[0]

def iMA2(bar):
    IB = Arr(1, 0.0, dyn=False)
    CopyBuffer(MA2, 0, bar, 1, IB)
    return IB[0]

def eRSI(bar):
    if RSI == 0:
        return 0.0
    IB = Arr(1, 0.0, dyn=False)
    CopyBuffer(RS, 0, bar, 1, IB)
    return IB[0]

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global IDN, IUP
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    IndCounted = prev_calculated
    if IndCounted < 0:
        return 0
    if IndCounted == 0:
        CLR()
    pos = rates_total - 1
    if IndCounted > 0:
        pos = rates_total - IndCounted
    for i in range(pos, 0, -1):
        B1[i] = 0.0
        B2[i] = 0.0
        if (iMA1(i + 1) < iMA2(i + 1) and iMA1(i) > iMA2(i)) and (eRSI(i) > 50 or RSI == 0):
            if Confirm2 == 0:
                BU(i, Time, High, Low)
            else:
                IUP = Low[i]
                IDN = 0.0
        if (iMA1(i + 1) > iMA2(i + 1) and iMA1(i) < iMA2(i)) and (eRSI(i) < 50 or RSI == 0):
            if Confirm2 == 0:
                BD(i, Time, High, Low)
            else:
                IDN = High[i]
                IUP = 0.0
        if IUP != 0:
            if (High[i] - IUP) >= (Confirm2 * Point()) and Open[i] <= Close[i]:
                BU(i, Time, High, Low)
                IUP = 0.0
        if IDN != 0:
            if (IDN - Low[i]) >= (Confirm2 * Point()) and Open[i] >= Close[i]:
                BD(i, Time, High, Low)
                IDN = 0.0
    return rates_total

def BU(i, Time, High, Low):
    global E1
    if Low[i] >= (E1 + (Flat2 * Point())) or Low[i] <= (E1 - (Flat2 * Point())):
        B1[i] = Low[i]
        E1 = B1[i]
        Alerts(i, 'UP ' + Symbol() + ' ' + TimeToString(Time[i]))

def BD(i, Time, High, Low):
    global E2
    if High[i] >= (E2 + (Flat2 * Point())) or High[i] <= (E2 - (Flat2 * Point())):
        B2[i] = High[i]
        E2 = B2[i]
        Alerts(i, 'DN ' + Symbol() + ' ' + TimeToString(Time[i]))

def Alerts(pos, txt):
    if SoundAlert == True and pos == 1:
        PlaySound('alert.wav')
    if EmailAlert == True and pos == 1:
        SendMail('Stalin alert signal: ' + txt, txt)

def MethodMigrate(method):
    _sw1 = method
    if _sw1 == 0:
        return MODE_SMA
    elif _sw1 == 1:
        return MODE_EMA
    elif _sw1 == 2:
        return MODE_SMMA
    elif _sw1 == 3:
        return MODE_LWMA
    else:
        return MODE_SMA


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stalin(_MQL5Indicator):
    name = 'stalin'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAMethod': 1,
        'MAShift': 0,
        'Fast': 14,
        'Slow': 21,
        'RSI': 17,
        'Confirm': 0.0,
        'Flat': 0.0,
        'SoundAlert': False,
        'EmailAlert': False,
    }

