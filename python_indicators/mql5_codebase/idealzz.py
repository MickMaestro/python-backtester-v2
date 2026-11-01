"""idealzz — converted from MQL5: MQL5 Indicators/Ideal ZigZag/idealzz.mq5

Copyright: Copyright 2012, TheXpert; Link: https://login.mql5.com/ru/users/TheXpert; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, TheXpert', 'link': 'https://login.mql5.com/ru/users/TheXpert', 'version': '1.00', 'window': 'chart', 'indicator_plots': 4, 'indicator_buffers': 5}, 'types': {1: 6, 2: 0, 3: 0, 4: 0}, 'colors': {1: [8421504], 2: [4294967295], 3: [4294967295], 4: [4294967295]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Ideal ZZ', 2: 'Ideal ZZ', 3: 'Ideal ZZ', 4: 'Ideal ZZ'}, 'levels': [], 'description': [], 'name': 'idealzz', 'source': 'MQL5 Indicators/Ideal ZigZag/idealzz.mq5', 'folder': 'Ideal ZigZag', 'inputs': [{'mql': 'ChannelPoints', 'py': 'ChannelPoints', 'param': 'ChannelPoints', 'type': 'int', 'default': 100, 'label': 'Minimum points in a ray', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ChannelPoints = _input('ChannelPoints', 100)  # Minimum points in a ray
DrawZeroBar = False
Maxs = Arr(0, 0.0)
Mins = Arr(0, 0.0)
Direction = Arr(0, 0.0)
MaxTime = Arr(0, 0.0)
MinTime = Arr(0, 0.0)
symbol = ""
Inited = False
LastTime = 0

def OnInit():
    global Inited, LastTime
    SetIndexBuffer(0, Maxs, INDICATOR_DATA)
    SetIndexBuffer(1, Mins, INDICATOR_DATA)
    SetIndexBuffer(2, MinTime, INDICATOR_DATA)
    SetIndexBuffer(3, MaxTime, INDICATOR_DATA)
    SetIndexBuffer(4, Direction, INDICATOR_DATA)
    Inited = False
    LastTime = 0
    ArraySetAsSeries(Maxs, True)
    ArraySetAsSeries(Mins, True)
    ArraySetAsSeries(Direction, True)
    ArraySetAsSeries(MaxTime, True)
    ArraySetAsSeries(MinTime, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(bars, counted, T_, O, H, L, C, TV, V, S):
    global LastTime
    if not Inited:
        ArrayInitialize(Mins, EMPTY_VALUE)
        ArrayInitialize(Maxs, EMPTY_VALUE)
        ArrayInitialize(MinTime, EMPTY_VALUE)
        ArrayInitialize(MaxTime, EMPTY_VALUE)
        ArrayInitialize(Direction, EMPTY_VALUE)
    ArraySetAsSeries(T_, True)
    ArraySetAsSeries(O, True)
    ArraySetAsSeries(H, True)
    ArraySetAsSeries(L, True)
    ArraySetAsSeries(C, True)
    ToCount = MathMin(bars - 1, bars - MathMax(counted, 0))
    for i in range(ToCount, 0, -1):
        if i < (bars - 1):
            MinTime[i] = MinTime[i + 1]
            MaxTime[i] = MaxTime[i + 1]
            Direction[i] = Direction[i + 1]
            Maxs[i] = EMPTY_VALUE
            Mins[i] = EMPTY_VALUE
        if C[i] < O[i]:
            CheckPrice(i, H[i], T_, H, L)
            CheckPrice(i, L[i], T_, H, L)
        else:
            CheckPrice(i, L[i], T_, H, L)
            CheckPrice(i, H[i], T_, H, L)
    if DrawZeroBar:
        if LastTime != T_[0]:
            LastTime = T_[0]
            MinTime[0] = MinTime[1]
            MaxTime[0] = MaxTime[1]
            Direction[0] = Direction[1]
            Maxs[0] = EMPTY_VALUE
            Mins[0] = EMPTY_VALUE
        CheckPrice(0, C[0], T_, H, L)
    else:
        Maxs[0] = EMPTY_VALUE
        Mins[0] = EMPTY_VALUE
    return bars

def CheckPrice(offset, p, T_, H, L):
    global Inited
    if not Inited:
        CheckInit(offset, p, T_)
        Inited = True
    else:
        if Direction[offset] == 0.0001:
            CheckUp(offset, p, T_, H)
        elif Direction[offset] == -0.0001:
            CheckDn(offset, p, T_, L)

def CheckInit(offset, c, T_):
    MaxTime[offset] = float(T_[offset])
    MinTime[offset] = float(T_[offset])
    Maxs[offset] = c
    Mins[offset] = c
    Direction[offset] = 0.0001

def CheckUp(offset, c, T_, H):
    lastOffset = ArrayBsearch(T_, _long(MaxTime[offset]))
    if Maxs[lastOffset] == EMPTY_VALUE:
        Maxs[lastOffset] = H[lastOffset]
    if c > Maxs[lastOffset]:
        Maxs[lastOffset] = EMPTY_VALUE
        Maxs[offset] = c
        MaxTime[offset] = float(T_[offset])
        lastOffset = offset
    if (c + (ChannelPoints * Point())) < Maxs[lastOffset]:
        Direction[offset] = -0.0001
        Mins[offset] = c
        MinTime[offset] = float(T_[offset])

def CheckDn(offset, c, T_, L):
    lastOffset = ArrayBsearch(T_, _long(MinTime[offset]))
    if Mins[lastOffset] == EMPTY_VALUE:
        Mins[lastOffset] = L[lastOffset]
    if c < Mins[lastOffset]:
        Mins[lastOffset] = EMPTY_VALUE
        Mins[offset] = c
        MinTime[offset] = float(T_[offset])
        lastOffset = offset
    if (c - (ChannelPoints * Point())) > Mins[lastOffset]:
        Direction[offset] = 0.0001
        Maxs[offset] = c
        MaxTime[offset] = float(T_[offset])


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Idealzz(_MQL5Indicator):
    name = 'idealzz'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ChannelPoints': 100,  # Minimum points in a ray
    }

