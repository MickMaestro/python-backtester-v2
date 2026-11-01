"""vindicat_005 — converted from MQL5: MQL5 Indicators/Position in channel/vindicat_005.mq5

VIndi

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 0}, 'colors': {1: [55295]}, 'widths': {}, 'styles': {}, 'labels': {1: 'VIndi'}, 'levels': [], 'description': ['VIndi'], 'name': 'vindicat_005', 'source': 'MQL5 Indicators/Position in channel/vindicat_005.mq5', 'folder': 'Position in channel', 'inputs': [{'mql': 'InpNBar', 'py': 'InpNBar', 'param': 'InpNBar', 'type': 'int', 'default': 4, 'label': 'Period', 'sinput': False}, {'mql': 'InpXCoord', 'py': 'InpXCoord', 'param': 'InpXCoord', 'type': 'int', 'default': 80, 'label': 'X Coordinate', 'sinput': False}, {'mql': 'InpYCoord', 'py': 'InpYCoord', 'param': 'InpYCoord', 'type': 'int', 'default': 20, 'label': 'Y Coordinate', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkKhaki = 0x6BB7BD  # MQL4 colour name

# ---- inputs and global variables
InpNBar = _input('InpNBar', 4)  # Period
InpXCoord = _input('InpXCoord', 80)  # X Coordinate
InpYCoord = _input('InpYCoord', 20)  # Y Coordinate
IBuf = Arr(0, 0.0)
NBar = 0
XCoord = 0
YCoord = 0
ShortName = ""
IndColor = Arr(64, 0, dyn=False)

def OnInit():
    global NBar, ShortName, XCoord, YCoord
    if InpNBar < 1:
        NBar = 1
    else:
        NBar = InpNBar
    XCoord = InpXCoord
    YCoord = InpYCoord
    SetIndexBuffer(0, IBuf, INDICATOR_DATA)
    ArraySetAsSeries(IBuf, True)
    ShortName = 'VIndi'
    IndicatorSetString(INDICATOR_SHORTNAME, ShortName)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    initGraph()
    return 0

def OnDeinit(reason):
    deleteGraph()

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    min_ = 0.0
    max_ = 0.0
    chan = 0.0
    val = 0.0
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    min_ = 10000.0
    max_ = 0.0
    i = 0
    for i in range(i, NBar):
        if Low[i] < min_:
            min_ = Low[i]
        if High[i] > max_:
            max_ = High[i]
    else:
        i = _range_end(i, NBar, 1)
    chan = (max_ - min_) / 2.0
    val = Close[0] - ((max_ + min_) / 2.0)
    if chan == 0:
        val = 1.0
    else:
        val = _fdiv(val, chan)
    if val > 0.99:
        val = 1.1
    if val < -0.99:
        val = -1.1
    drawGraph(val)
    return rates_total

def initGraph():
    i = 0
    nam = ""
    IndColor[0] = 0x0707FF
    IndColor[1] = 0x07FFFA
    IndColor[2] = 0x07FFE1
    IndColor[3] = 0x07FFC8
    IndColor[4] = 0x07FFAF
    IndColor[5] = 0x07FF96
    IndColor[6] = 0x07FF7D
    IndColor[7] = 0x07FF64
    IndColor[8] = 0x07FF4B
    IndColor[9] = 0x07FF32
    IndColor[10] = 0x07FF19
    IndColor[11] = 0x188282
    IndColor[12] = 0x07FF19
    IndColor[13] = 0x07FF32
    IndColor[14] = 0x07FF4B
    IndColor[15] = 0x07FF64
    IndColor[16] = 0x07FF7D
    IndColor[17] = 0x07FF96
    IndColor[18] = 0x07FFAF
    IndColor[19] = 0x07FFC8
    IndColor[20] = 0x07FFE1
    IndColor[21] = 0x07FFFA
    IndColor[22] = 0x0707FF
    IndColor[23] = 0x181838
    IndColor[24] = 0x303020
    IndColor[25] = 0x303020
    IndColor[26] = 0x303020
    IndColor[27] = 0x303020
    IndColor[28] = 0x303020
    IndColor[29] = 0x303020
    IndColor[30] = 0x303020
    IndColor[31] = 0x303020
    IndColor[32] = 0x303020
    IndColor[33] = 0x303020
    IndColor[34] = 0x188282
    IndColor[35] = 0x303020
    IndColor[36] = 0x303020
    IndColor[37] = 0x303020
    IndColor[38] = 0x303020
    IndColor[39] = 0x303020
    IndColor[40] = 0x303020
    IndColor[41] = 0x303020
    IndColor[42] = 0x303020
    IndColor[43] = 0x303020
    IndColor[44] = 0x303020
    IndColor[45] = 0x181838
    IndColor[62] = 0x0A3636
    IndColor[63] = _uint(DarkKhaki)
    i = 0
    for i in range(i, 23):
        nam = ShortName + IntegerToString(i)
        ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
        ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
        ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 31)
        ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord)
        ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + (i * 4))
        ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[i + 23])
        ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
        ObjectSetString(0, nam, OBJPROP_TEXT, '-')
    else:
        i = _range_end(i, 23, 1)
    nam = ShortName + IntegerToString(23)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord - 26)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 17)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '- -10')
    nam = ShortName + IntegerToString(24)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord - 14)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 57)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '- 0')
    nam = ShortName + IntegerToString(25)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord - 29)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 97)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '- +10')
    nam = ShortName + IntegerToString(26)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord + 14)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 17)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '-')
    nam = ShortName + IntegerToString(27)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord + 14)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 57)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '-')
    nam = ShortName + IntegerToString(28)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord + 14)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 97)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '-')
    nam = ShortName + IntegerToString(29)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 13)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[62])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '__')
    nam = ShortName + IntegerToString(30)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 111)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[62])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '__')
    i = 31
    for i in range(i, 39 + 1):
        nam = ShortName + IntegerToString(i)
        ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
        ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
        ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
        ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord - 2)
        ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 13 + ((i - 31) * 11))
        ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[62])
        ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
        ObjectSetString(0, nam, OBJPROP_TEXT, '|')
    else:
        i = _range_end(i, 39 + 1, 1)
    i = 40
    for i in range(i, 48 + 1):
        nam = ShortName + IntegerToString(i)
        ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
        ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
        ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
        ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord + 13)
        ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 13 + ((i - 40) * 11))
        ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[62])
        ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
        ObjectSetString(0, nam, OBJPROP_TEXT, '|')
    else:
        i = _range_end(i, 48 + 1, 1)
    nam = ShortName + IntegerToString(49)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord - 18)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 57)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, DarkKhaki)
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '')

def drawGraph(level):
    i = 0
    p = 0
    c = 0
    nam = ""
    st = ""
    p = _int(MathRound(10 * level))
    if level > 1.001:
        p = 11
    if level < -1.001:
        p = -11
    p = p + 11
    i = 0
    for i in range(i, 23):
        c = i + 23
        if i <= p and i > 11:
            c = i
        if i >= p and i < 11:
            c = i
        nam = ShortName + IntegerToString(i)
        ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[c])
    else:
        i = _range_end(i, 23, 1)
    nam = ShortName + IntegerToString(49)
    st = '(' + IntegerToString(p - 11) + ')'
    ObjectSetString(0, nam, OBJPROP_TEXT, st)

def deleteGraph():
    i = 0
    nam = ""
    i = 0
    for i in range(i, 49 + 1):
        nam = ShortName + IntegerToString(i)
        ObjectDelete(0, nam)
    else:
        i = _range_end(i, 49 + 1, 1)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vindicat005(_MQL5Indicator):
    name = 'vindicat_005'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpNBar': 4,  # Period
        'InpXCoord': 80,  # X Coordinate
        'InpYCoord': 20,  # Y Coordinate
    }

