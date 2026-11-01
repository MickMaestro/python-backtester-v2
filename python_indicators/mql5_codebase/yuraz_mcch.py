"""YURAZ_MCCH — converted from MQL5: MQL5 Indicators/YURAZ_MCCH Calculation Indicator/YURAZ_MCCH.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'YURAZ_MCCH', 'source': 'MQL5 Indicators/YURAZ_MCCH Calculation Indicator/YURAZ_MCCH.mq5', 'folder': 'YURAZ_MCCH Calculation Indicator', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Aqua = 0xFFFF00  # MQL4 colour name
LimeGreen = 0x32CD32  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name


class SymbolStruct(MqlObject):
    _q_fields = ('work', 'sSymbol', 'y', 'x', 'CH')
    def __init__(self, *args):
        self.work = False
        self.sSymbol = ""
        self.y = 0
        self.x = 0
        self.CH = 0.0

class CChmcYZ(MqlObject):
    _q_fields = ('sSymb', 'lColorSym', 'lColorChPlus', 'lColorChMinus', 'lColorCH', 'indicatorWindow', 'lColor', 'dClose')
    def __init__(self, *args):
        self.sSymb = SymbolStruct()
        self.lColorSym = 0
        self.lColorChPlus = 0
        self.lColorChMinus = 0
        self.lColorCH = 0
        self.indicatorWindow = 0
        self.lColor = 0
        self.dClose = Arr(7000, 0.0, dyn=False)
    def CChmcYZ(self):
        self.indicatorWindow = 0
        self.lColorSym = _uint(Aqua)
        self.lColorCH = _uint(White)
        self.lColorChPlus = _uint(LimeGreen)
        self.lColorChMinus = _uint(Red)
    def RCH(self, sSymbol, DATEBEG, DATEEND):
        self.sSymb.CH = 0.0
        CountBar = 0
        DATEBEG = StringToTime(TimeToString(DATEBEG, TIME_DATE))
        DATEEND = StringToTime(TimeToString(DATEEND, TIME_DATE))
        CountBar = CopyClose(sSymbol, PERIOD_D1, _DT(DATEEND), 2, self.dClose)
        if CountBar >= 0:
            if NormalizeDouble(self.dClose[1], 5) != 0.0 and NormalizeDouble(self.dClose[0], 5) != 0.0:
                self.sSymb.CH = _fdiv(self.dClose[1] * 100, self.dClose[0]) - 100
    def RCHsay(self, sSym, db, de, XD, YD):
        self.RCH(sSym, db, de)
        if ObjectFind(self.indicatorWindow, 'oYZ' + sSym) == -1:
            ObjectCreate(self.indicatorWindow, 'oYZ' + sSym, OBJ_LABEL, self.indicatorWindow, 0, 0)
            ObjectSetInteger(self.indicatorWindow, 'oYZ' + sSym, OBJPROP_XDISTANCE, XD)
            ObjectSetInteger(self.indicatorWindow, 'oYZ' + sSym, OBJPROP_YDISTANCE, YD)
            ObjectSetInteger(self.indicatorWindow, 'oYZ' + sSym, OBJPROP_CORNER, CORNER_LEFT_UPPER)
            ObjectSetString(self.indicatorWindow, 'oYZ' + sSym, OBJPROP_TEXT, sSym)
            ObjectSetString(self.indicatorWindow, 'oYZ' + sSym, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(self.indicatorWindow, 'oYZ' + sSym, OBJPROP_FONTSIZE, 7)
            ObjectSetInteger(self.indicatorWindow, 'oYZ' + sSym, OBJPROP_COLOR, self.lColorSym)
            ObjectSetInteger(self.indicatorWindow, 'oYZ' + sSym, OBJPROP_SELECTABLE, True)
        if ObjectFind(self.indicatorWindow, 'oYZ_' + sSym) == -1:
            ObjectCreate(self.indicatorWindow, 'oYZ_' + sSym, OBJ_LABEL, self.indicatorWindow, 0, 0)
            ObjectSetInteger(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_XDISTANCE, XD + 45)
            ObjectSetInteger(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_YDISTANCE, YD)
            ObjectSetInteger(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_CORNER, CORNER_LEFT_UPPER)
            ObjectSetString(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_TEXT, sSym)
            ObjectSetString(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_FONTSIZE, 7)
            ObjectSetInteger(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_COLOR, self.lColorCH)
            ObjectSetInteger(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_SELECTABLE, True)
        YD = YD + 11
        self.lColor = self.lColorCH
        if self.sSymb.CH > 0:
            self.lColor = self.lColorChPlus
            ObjectSetString(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_TEXT, ' ' + DoubleToString(self.sSymb.CH, 5))
            ObjectSetInteger(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_XDISTANCE, XD + 45)
        if self.sSymb.CH < 0:
            self.lColor = self.lColorChMinus
            ObjectSetString(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_TEXT, DoubleToString(self.sSymb.CH, 5))
            ObjectSetInteger(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_XDISTANCE, XD + 46)
        ObjectSetInteger(self.indicatorWindow, 'oYZ_' + sSym, OBJPROP_COLOR, self.lColor)

def OnInit():
    chmc.RCHsay('EURUSD', TimeCurrent() - (86400 * 5), TimeCurrent(), 5, 16)
    chmc.RCHsay('AUDUSD', TimeCurrent() - (86400 * 5), TimeCurrent(), 5, 16 + 12)
    chmc.RCHsay('GBPUSD', TimeCurrent() - (86400 * 5), TimeCurrent(), 5, 16 + (12 * 2))
    chmc.RCHsay('USDCHF', TimeCurrent() - (86400 * 5), TimeCurrent(), 5, 16 + (12 * 3))
    chmc.RCHsay('USDCAD', TimeCurrent() - (86400 * 5), TimeCurrent(), 5, 16 + (12 * 4))
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    chmc.RCHsay('EURUSD', TimeCurrent() - (86400 * 5), TimeCurrent(), 5, 16)
    chmc.RCHsay('AUDUSD', TimeCurrent() - (86400 * 5), TimeCurrent(), 5, 16 + 12)
    chmc.RCHsay('GBPUSD', TimeCurrent() - (86400 * 5), TimeCurrent(), 5, 16 + (12 * 2))
    chmc.RCHsay('USDCHF', TimeCurrent() - (86400 * 5), TimeCurrent(), 5, 16 + (12 * 3))
    chmc.RCHsay('USDCAD', TimeCurrent() - (86400 * 5), TimeCurrent(), 5, 16 + (12 * 4))
    return rates_total

def OnDeinit():
    i = ObjectsTotal(0)
    while i > 0:
        if StringSubstr(ObjectName(0, i), 0, 3) == 'oYZ':
            ObjectDelete(0, ObjectName(0, i))
        i -= 1

# ---- global variables initialised from expressions
chmc = _alloc(CChmcYZ)
chmc.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YURAZMCCH(_MQL5Indicator):
    name = 'YURAZ_MCCH'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

