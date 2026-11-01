"""Flight_smiles — converted from MQL5: MQL5 Indicators/Flight smiles/Flight_smiles.mq5

Copyright: Copyright 2013,Viktor Moss; Link: https://login.mql5.com/ru/users/vicmos; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013,Viktor Moss', 'link': 'https://login.mql5.com/ru/users/vicmos', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Flight_smiles', 'source': 'MQL5 Indicators/Flight smiles/Flight_smiles.mq5', 'folder': 'Flight smiles', 'inputs': [{'mql': 'NSn', 'py': 'NSn', 'param': 'NSn', 'type': 'int', 'default': 10, 'label': 'Number of smiles', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 16, 'label': 'Size', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
NSn = _input('NSn', 10)  # Number of smiles
FontSize = _input('FontSize', 16)  # Size
Text = 'J'
CoorX = Arr(0, 0)
CoorY = Arr(0, 0)
cl = Arr.of([clrYellow, clrAqua, clrLime, clrRed, clrBlue, clrLawnGreen, clrMagenta], fill=0)

class CSnow(MqlObject):
    _q_fields = ('m_Num', 'm_Name', 'm_Color', 'm_X', 'm_Size', 'm_Speed', 'm_SmX')
    def __init__(self, *args):
        self.m_Num = 0
        self.m_Name = ""
        self.m_Color = 0
        self.m_X = 0
        self.m_Size = 0
        self.m_Speed = 0
        self.m_SmX = 0
    def _q_dtor(self):
        if ObjectFind(0, self.m_Name) >= 0:
            ObjectDelete(0, self.m_Name)
        ChartRedraw()
    def CSnowCreate(self, n):
        self.m_Num = n
        self.m_Color = cl[_imod(n, 7)]
        xch = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
        if xch != 0:
            self.m_X = _imod(MathRand(), xch)
        else:
            self.m_X = 100
        self.m_Size = _imod(MathRand(), FontSize) + 6
        self.m_Speed = _imod(MathRand(), 7) + 2
        while True:
            self.m_SmX = _imod(MathRand(), 6) - 3
            if not (self.m_SmX == 0):
                break
        self.m_Name = 'Snow-' + IntegerToString(GetTickCount(), 7, 48) + Symbol() + IntegerToString(n, 3, 48)
        if ObjectFind(0, self.m_Name) < 0:
            ObjectCreate(0, self.m_Name, OBJ_LABEL, 0, 0, 0)
        ObjectSetString(0, self.m_Name, OBJPROP_TEXT, Text)
        ObjectSetInteger(0, self.m_Name, OBJPROP_XDISTANCE, self.m_X)
        ObjectSetInteger(0, self.m_Name, OBJPROP_YDISTANCE, 0)
        ObjectSetString(0, self.m_Name, OBJPROP_FONT, 'Wingdings')
        ObjectSetInteger(0, self.m_Name, OBJPROP_FONTSIZE, self.m_Size)
        ObjectSetInteger(0, self.m_Name, OBJPROP_COLOR, self.m_Color)
        ObjectSetInteger(0, self.m_Name, OBJPROP_SELECTABLE, False)
    def SnowNext(self):
        yp = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
        xp = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
        y = ObjectGetInteger(0, self.m_Name, OBJPROP_YDISTANCE)
        x = ObjectGetInteger(0, self.m_Name, OBJPROP_XDISTANCE)
        if (x + self.m_SmX) < 0:
            self.m_SmX = -self.m_SmX
        if (x + self.m_SmX) >= (xp - ObjectGetInteger(0, self.m_Name, OBJPROP_XSIZE)):
            self.m_SmX = -self.m_SmX
        if (x + ObjectGetInteger(0, self.m_Name, OBJPROP_XSIZE)) > xp:
            x -= ObjectGetInteger(0, self.m_Name, OBJPROP_XSIZE) + 2
        if (y + self.m_Speed) > (yp - ObjectGetInteger(0, self.m_Name, OBJPROP_YSIZE) + 1):
            self.m_Speed = -self.m_Speed
        if y > yp:
            y = yp - ObjectGetInteger(0, self.m_Name, OBJPROP_YSIZE) + 1
        if (y + self.m_Speed) < 0:
            self.m_Speed = Sign(self.m_Speed) * (_imod(MathRand(), 8) + 1)
            self.m_Speed = -self.m_Speed
            self.m_Size = _imod(MathRand(), FontSize) + 5
            self.m_Color = cl[_imod(MathRand(), 7)]
            ObjectSetInteger(0, self.m_Name, OBJPROP_FONTSIZE, self.m_Size)
            ObjectSetInteger(0, self.m_Name, OBJPROP_COLOR, self.m_Color)
        ObjectSetInteger(0, self.m_Name, OBJPROP_YDISTANCE, y + self.m_Speed)
        ObjectSetInteger(0, self.m_Name, OBJPROP_XDISTANCE, x + self.m_SmX)
        CoorX[self.m_Num] = _int(x)
        CoorY[self.m_Num] = _int(y)
        ChartRedraw()

def OnInit():
    EventSetMillisecondTimer(50)
    ArrayResize(Sn, NSn)
    ArrayResize(CoorX, NSn)
    ArrayResize(CoorY, NSn)
    MathSrand(GetTickCount())
    for i in range(0, NSn):
        Sn[i].CSnowCreate(i)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    EventKillTimer()

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnTimer():
    for i in range(0, NSn):
        Sn[i].SnowNext()

def Sign(C):
    return (1 if (C >= 0) else -1)

def DelAllObjects(name):
    vName = ""
    tot = ObjectsTotal(0)
    for i in range(tot, 0 - 1, -1):
        vName = ObjectName(0, i)
        if StringSubstr(vName, 0, StringLen(name)) == name:
            ObjectDelete(0, vName)

# ---- global variables initialised from expressions
Sn = Arr(0, 0, factory=CSnow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FlightSmiles(_MQL5Indicator):
    name = 'Flight_smiles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'NSn': 10,  # Number of smiles
        'FontSize': 16,  # Size
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

