"""vdirection — converted from MQL5: MQL5 Indicators/Multi-Williams Percent Range trend indicator/vdirection.mq5

Direction indicator. Multi-'Williams Percent Range'.
Copyright: 2012, victorg.; Link: http://www.mql5.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2012, victorg.', 'link': 'http://www.mql5.com', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ["Direction indicator. Multi-'Williams Percent Range'."], 'name': 'vdirection', 'source': 'MQL5 Indicators/Multi-Williams Percent Range trend indicator/vdirection.mq5', 'folder': 'Multi-Williams Percent Range trend indicator', 'inputs': [{'mql': 'TMode', 'py': 'TMode', 'param': 'TMode', 'type': 'int', 'default': 1, 'label': 'Mode: 0 - fast, 1 - normal, 2 - slow', 'sinput': False}, {'mql': 'InpXCoord', 'py': 'InpXCoord', 'param': 'InpXCoord', 'type': 'int', 'default': 35, 'label': 'X Coordinate', 'sinput': False}, {'mql': 'InpYCoord', 'py': 'InpYCoord', 'param': 'InpYCoord', 'type': 'int', 'default': 0, 'label': 'Y Coordinate', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TMode = _input('TMode', 1)  # Mode: 0 - fast, 1 - normal, 2 - slow
InpXCoord = _input('InpXCoord', 35)  # X Coordinate
InpYCoord = _input('InpYCoord', 0)  # Y Coordinate
XCoord = 0
YCoord = 0
T1 = 0
T2 = 0
T3 = 0
T4 = 0
T5 = 0
ShortName = ""
IndColor = Arr(64, 0, dyn=False)

def OnInit():
    global ShortName, T1, T2, T3, T4, T5, XCoord, YCoord
    T1 = 12
    T2 = 15
    T3 = 20
    T4 = 30
    T5 = 60
    if TMode == 0:
        T1 = 6
        T2 = 8
        T3 = 10
        T4 = 15
        T5 = 30
    if TMode == 2:
        T1 = 24
        T2 = 30
        T3 = 40
        T4 = 60
        T5 = 120
    XCoord = InpXCoord
    YCoord = InpYCoord
    ShortName = 'VDir'
    IndicatorSetString(INDICATOR_SHORTNAME, ShortName)
    initGraph()
    return 0

def OnDeinit(reason):
    i = 0
    nam = ""
    i = 0
    for i in range(i, 184 + 1):
        nam = ShortName + _str(i)
        ObjectDelete(0, nam)
    else:
        i = _range_end(i, 184 + 1, 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    min_ = 0.0
    max_ = 0.0
    chan = 0.0
    v = 0.0
    val = Arr(5, 0.0, dyn=False)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    min_ = Low[0]
    max_ = High[0]
    i = 1
    for i in range(i, T5):
        if i == T1:
            chan = (max_ - min_) / 2.0
            v = Close[0] - ((max_ + min_) / 2.0)
            if chan == 0:
                val[0] = 0.0
            else:
                val[0] = _fdiv(v, chan)
        if i == T2:
            chan = (max_ - min_) / 2.0
            v = Close[0] - ((max_ + min_) / 2.0)
            if chan == 0:
                val[1] = 0.0
            else:
                val[1] = _fdiv(v, chan)
        if i == T3:
            chan = (max_ - min_) / 2.0
            v = Close[0] - ((max_ + min_) / 2.0)
            if chan == 0:
                val[2] = 0.0
            else:
                val[2] = _fdiv(v, chan)
        if i == T4:
            chan = (max_ - min_) / 2.0
            v = Close[0] - ((max_ + min_) / 2.0)
            if chan == 0:
                val[3] = 0.0
            else:
                val[3] = _fdiv(v, chan)
        if Low[i] < min_:
            min_ = Low[i]
        if High[i] > max_:
            max_ = High[i]
    else:
        i = _range_end(i, T5, 1)
    chan = (max_ - min_) / 2.0
    v = Close[0] - ((max_ + min_) / 2.0)
    if chan == 0:
        val[4] = 0.0
    else:
        val[4] = _fdiv(v, chan)
    drawGraph(val)
    return rates_total

def drawGraph(val):
    i = 0
    j = 0
    p = 0
    c = 0
    nam = ""
    j = 0
    for j in range(j, 5):
        p = _int(11.1 * val[4 - j]) + 11
        i = 0
        for i in range(i, 23):
            c = i + 23
            if i <= p and i > 11:
                c = i
            if i >= p and i < 11:
                c = i
            nam = ShortName + _str(i + (j * 23))
            ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[c])
        else:
            i = _range_end(i, 23, 1)
    else:
        j = _range_end(j, 5, 1)

def initGraph():
    i = 0
    j = 0
    k = 0
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
    IndColor[24] = 0x2D2D1E
    IndColor[25] = 0x2D2D1E
    IndColor[26] = 0x2D2D1E
    IndColor[27] = 0x2D2D1E
    IndColor[28] = 0x2D2D1E
    IndColor[29] = 0x2D2D1E
    IndColor[30] = 0x2D2D1E
    IndColor[31] = 0x2D2D1E
    IndColor[32] = 0x2D2D1E
    IndColor[33] = 0x2D2D1E
    IndColor[34] = 0x188282
    IndColor[35] = 0x2D2D1E
    IndColor[36] = 0x2D2D1E
    IndColor[37] = 0x2D2D1E
    IndColor[38] = 0x2D2D1E
    IndColor[39] = 0x2D2D1E
    IndColor[40] = 0x2D2D1E
    IndColor[41] = 0x2D2D1E
    IndColor[42] = 0x2D2D1E
    IndColor[43] = 0x2D2D1E
    IndColor[44] = 0x2D2D1E
    IndColor[45] = 0x181838
    IndColor[62] = 0x0A3636
    IndColor[63] = 0x188282
    i = 0
    for i in range(i, 23):
        j = 0
        for j in range(j, 5):
            nam = ShortName + _str(i + (j * 23))
            ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
            ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_LEFT_LOWER)
            ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
            ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 31)
            ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord + (j * 13))
            ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + (i * 4))
            ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[i + 23])
            ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
            ObjectSetString(0, nam, OBJPROP_TEXT, '-')
        else:
            j = _range_end(j, 5, 1)
    else:
        i = _range_end(i, 23, 1)
    nam = ShortName + _str(115)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord + 67)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 18)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '-')
    nam = ShortName + _str(116)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord + 67)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 58)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '-')
    nam = ShortName + _str(117)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord + 67)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 98)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '-')
    nam = ShortName + _str(118)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord - 14)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 18)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '1 -')
    nam = ShortName + _str(119)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord - 14)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 58)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '0 -')
    nam = ShortName + _str(120)
    ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord - 14)
    ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 98)
    ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[63])
    ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, nam, OBJPROP_TEXT, '1 -')
    i = 121
    j = 0
    while i <= 125:
        nam = ShortName + _str(i)
        ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_LEFT_LOWER)
        ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
        ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
        ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord + (j * 13))
        ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 13)
        ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[62])
        ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
        ObjectSetString(0, nam, OBJPROP_TEXT, '__')
        i += 1
        j += 1
    i = 126
    j = 0
    while i <= 130:
        nam = ShortName + _str(i)
        ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_LEFT_LOWER)
        ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
        ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
        ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord + (j * 13))
        ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 111)
        ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[62])
        ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
        ObjectSetString(0, nam, OBJPROP_TEXT, '__')
        i += 1
        j += 1
    k = 131
    i = 0
    for i in range(i, 9):
        j = 0
        for j in range(j, 6):
            nam = ShortName + _str(k + i + (j * 9))
            ObjectCreate(0, nam, OBJ_LABEL, 0, 0, 0)
            ObjectSetInteger(0, nam, OBJPROP_CORNER, CORNER_LEFT_LOWER)
            ObjectSetInteger(0, nam, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
            ObjectSetInteger(0, nam, OBJPROP_FONTSIZE, 9)
            ObjectSetInteger(0, nam, OBJPROP_XDISTANCE, XCoord - 1 + (j * 13))
            ObjectSetInteger(0, nam, OBJPROP_YDISTANCE, YCoord + 13 + (i * 11))
            ObjectSetInteger(0, nam, OBJPROP_COLOR, IndColor[62])
            ObjectSetString(0, nam, OBJPROP_FONT, 'Arial')
            ObjectSetString(0, nam, OBJPROP_TEXT, '|')
        else:
            j = _range_end(j, 6, 1)
    else:
        i = _range_end(i, 9, 1)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vdirection(_MQL5Indicator):
    name = 'vdirection'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TMode': 1,  # Mode: 0 - fast, 1 - normal, 2 - slow
        'InpXCoord': 35,  # X Coordinate
        'InpYCoord': 0,  # Y Coordinate
    }

