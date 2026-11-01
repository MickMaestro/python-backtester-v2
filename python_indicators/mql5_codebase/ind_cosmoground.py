"""ind_-_cosmoground — converted from MQL5: MQL5 Indicators/Ind - CosmoGround/ind_-_cosmoground.mq5

Copyright: Copyright 2012, expforex.; Link: http://www.expforex.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, expforex.', 'link': 'http://www.expforex.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ind_-_cosmoground', 'source': 'MQL5 Indicators/Ind - CosmoGround/ind_-_cosmoground.mq5', 'folder': 'Ind - CosmoGround', 'inputs': [{'mql': 'CountStars', 'py': 'CountStars', 'param': 'CountStars', 'type': 'int', 'default': 1000, 'label': 'Number of stars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CountStars = _input('CountStars', 1000)  # Number of stars

def OnDeinit(reason):
    ObjectsDelete()
    ChartRedraw()
    EventKillTimer()

def ObjectsDelete():
    for i in range(ObjectsTotal(0), 0 - 1, -1):
        if StringFind(ObjectName(0, i), 'Stars') != -1:
            ObjectDelete(0, ObjectName(0, i))

def OnInit():
    MathSrand(GetTickCount())
    StarsCreate()
    EventSetTimer(1)
    return 0

def StarsActivateLight():
    Size = 0
    name = _str(_imod(MathRand(), CountStars))
    Comment(name)
    Size = ObjectGetInteger(0, 'Stars' + name, OBJPROP_FONTSIZE)
    u = _imod(MathRand(), 2)
    if u == 1:
        ObjectSetInteger(0, 'Stars' + name, OBJPROP_FONTSIZE, Size + 1)
    elif u == 0:
        ObjectSetInteger(0, 'Stars' + name, OBJPROP_FONTSIZE, Size - 1)
    ChartRedraw()
    Y = ObjectGetInteger(0, 'Stars' + name, OBJPROP_YDISTANCE)
    r = Y
    while r < ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS):
        ObjectSetInteger(0, 'Stars' + name, OBJPROP_YDISTANCE, r + 1)
        ChartRedraw()
        Sleep(25)
        r += 1

def StarsCreate():
    i = 0
    i = 0
    for i in range(i, CountStars + 1):
        SetLabel('Stars' + _str(i), 'T', RandomX(), RandomY(), RandomSize(5), RandomColor())
    else:
        i = _range_end(i, CountStars + 1, 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnTimer():
    StarsActivateLight()

def RandomX():
    x = 0
    x = _imod(MathRand(), ChartGetInteger(0, CHART_WIDTH_IN_PIXELS))
    return x

def RandomY():
    y = 0
    y = _imod(MathRand(), ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS))
    return y

def RandomSize(si):
    s = 0
    s = _imod(MathRand(), si)
    return s

def RandomColor():
    c = 0
    c = _imod(MathRand(), 10)
    if c == 0:
        return clrDarkSlateGray
    if c == 1:
        return clrMidnightBlue
    if c == 2:
        return clrMediumBlue
    if c == 3:
        return clrDarkTurquoise
    if c == 4:
        return clrAqua
    if c == 5:
        return clrDodgerBlue
    if c == 6:
        return clrRoyalBlue
    if c == 7:
        return clrLightGray
    if c == 8:
        return clrLightCyan
    if c == 9:
        return clrSnow
    return clrLightSkyBlue

def SetLabel(nm, tx, xd, yd, fs, ct):
    if fs < 1:
        fs = 1
    cn = 0
    cr = 0
    cn = CORNER_LEFT_UPPER
    cr = ANCHOR_LEFT_UPPER
    if ObjectFind(0, nm) < 0:
        ObjectCreate(0, nm, OBJ_LABEL, 0, 0, 0)
    ObjectSetString(0, nm, OBJPROP_TEXT, '*')
    ObjectSetInteger(0, nm, OBJPROP_CORNER, cn)
    ObjectSetInteger(0, nm, OBJPROP_ANCHOR, cr)
    ObjectSetInteger(0, nm, OBJPROP_XDISTANCE, xd)
    ObjectSetInteger(0, nm, OBJPROP_YDISTANCE, yd)
    ObjectSetString(0, nm, OBJPROP_FONT, 'Verdana')
    ObjectSetInteger(0, nm, OBJPROP_FONTSIZE, fs)
    ObjectSetInteger(0, nm, OBJPROP_COLOR, ct)
    ObjectSetInteger(0, nm, OBJPROP_SELECTABLE, False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IndCosmoground(_MQL5Indicator):
    name = 'ind_-_cosmoground'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CountStars': 1000,  # Number of stars
    }

