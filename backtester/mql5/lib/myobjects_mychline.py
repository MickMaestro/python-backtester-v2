"""mychline.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh


class MyCHLine(CObject):
    _q_fields = ('HLineName', 'HLinePrice', 'HLineStyle', 'HLineColor', 'HLineWidth', 'HLineBack', 'HLineHidden', 'HLineText', 'HLineTip')
    def _q_ctor1(self):
        CObject.__init__(self)
        self.HLineName = ""
        self.HLinePrice = 0.0
        self.HLineStyle = 0
        self.HLineColor = 0
        self.HLineWidth = 0
        self.HLineBack = False
        self.HLineHidden = False
        self.HLineText = ""
        self.HLineTip = ""
        last_tick = MqlTick()
        self.HLineName = self.GenerateRandName()
        if SymbolInfoTick(Symbol(), last_tick):
            self.HLinePrice = last_tick.ask
        else:
            self.HLinePrice = 0.0
        self.HLineStyle = STYLE_SOLID
        self.HLineColor = clrRed
        self.HLineWidth = 1
        self.HLineBack = False
        self.HLineHidden = True
        self.HLineText = ""
        self.HLineTip = ""
        self.CreateHLine()
    def _q_ctor2(self, price):
        CObject.__init__(self)
        self.HLineName = ""
        self.HLinePrice = 0.0
        self.HLineStyle = 0
        self.HLineColor = 0
        self.HLineWidth = 0
        self.HLineBack = False
        self.HLineHidden = False
        self.HLineText = ""
        self.HLineTip = ""
        self.HLineName = self.GenerateRandName()
        self.HLinePrice = price
        self.HLineStyle = STYLE_SOLID
        self.HLineColor = clrRed
        self.HLineWidth = 1
        self.HLineBack = False
        self.HLineHidden = True
        self.HLineText = ""
        self.HLineTip = ""
        self.CreateHLine()
    def _q_ctor3(self, price, style):
        CObject.__init__(self)
        self.HLineName = ""
        self.HLinePrice = 0.0
        self.HLineStyle = 0
        self.HLineColor = 0
        self.HLineWidth = 0
        self.HLineBack = False
        self.HLineHidden = False
        self.HLineText = ""
        self.HLineTip = ""
        self.HLineName = self.GenerateRandName()
        self.HLinePrice = price
        self.HLineStyle = style
        self.HLineColor = clrRed
        self.HLineWidth = 1
        self.HLineBack = False
        self.HLineHidden = True
        self.HLineText = ""
        self.HLineTip = ""
        self.CreateHLine()
    def _q_ctor4(self, name, price, style):
        CObject.__init__(self)
        self.HLineName = ""
        self.HLinePrice = 0.0
        self.HLineStyle = 0
        self.HLineColor = 0
        self.HLineWidth = 0
        self.HLineBack = False
        self.HLineHidden = False
        self.HLineText = ""
        self.HLineTip = ""
        self.HLineName = name
        self.HLinePrice = price
        self.HLineStyle = style
        self.HLineColor = clrRed
        self.HLineWidth = 1
        self.HLineBack = False
        self.HLineHidden = True
        self.HLineText = ""
        self.HLineTip = ""
        self.CreateHLine()
    def __init__(self, *args):
        if 0 <= len(args) <= 0:
            self._q_ctor1(*args)
            return
        if 1 <= len(args) <= 1 and (len(args) == 0 or isinstance(args[0], float)):
            self._q_ctor2(*args)
            return
        if 2 <= len(args) <= 2 and (len(args) == 0 or isinstance(args[0], float)):
            self._q_ctor3(*args)
            return
        if 3 <= len(args) <= 3 and (len(args) == 0 or isinstance(args[0], str)):
            self._q_ctor4(*args)
            return
        self._q_ctor1(*args)
    def _q_dtor(self):
        if ObjectFind(0, self.HLineName) >= 0:
            self.DeletHLine()
    def SetName(self, name):
        if ObjectSetString(0, self.HLineName, OBJPROP_NAME, name):
            self.HLineName = name
            ChartRedraw(0)
            return True
        Print('MyCHLine::SetName', ' ERROR: ', GetLastError())
        return False
    def SetPrice(self, price):
        if ObjectSetDouble(0, self.HLineName, OBJPROP_PRICE, 0, price):
            self.HLinePrice = price
            ChartRedraw(0)
            return True
        Print('MyCHLine::SetPrice', ' ERROR: ', GetLastError())
        return False
    def SetColor(self, col):
        if ObjectSetInteger(0, self.HLineName, OBJPROP_COLOR, col):
            self.HLineColor = col
            ChartRedraw(0)
            return True
        Print('MyCHLine::SetColor', ' ERROR: ', GetLastError())
        return False
    def SetStyle(self, style):
        if ObjectSetInteger(0, self.HLineName, OBJPROP_STYLE, style):
            self.HLineStyle = style
            ChartRedraw(0)
            return True
        Print('MyCHLine::SetStyle', ' ERROR: ', GetLastError())
        return False
    def SetWidth(self, width):
        if ObjectSetInteger(0, self.HLineName, OBJPROP_WIDTH, width):
            self.HLineWidth = width
            ChartRedraw(0)
            return True
        Print('MyCHLine::SetWidth', ' ERROR: ', GetLastError())
        return False
    def SetBack(self, back):
        if ObjectSetInteger(0, self.HLineName, OBJPROP_BACK, back):
            self.HLineBack = back
            ChartRedraw(0)
            return True
        Print('MyCHLine::SetBack', ' ERROR: ', GetLastError())
        return False
    def SetHidden(self, hidden):
        if ObjectSetInteger(0, self.HLineName, OBJPROP_HIDDEN, hidden):
            self.HLineHidden = hidden
            ChartRedraw(0)
            return True
        Print('MyCHLine::SetHidden', ' ERROR: ', GetLastError())
        return False
    def SetText(self, text):
        if text != "":
            ObjectSetString(0, self.HLineName, OBJPROP_TEXT, self.HLineText)
            ChartSetInteger(0, CHART_SHOW_OBJECT_DESCR, True)
            self.HLineText = text
            ChartRedraw(0)
            return True
        return False
    def SetTip(self, tip):
        if tip != "":
            ObjectSetString(0, self.HLineName, OBJPROP_TOOLTIP, self.HLineTip)
            ChartSetInteger(0, CHART_SHOW_OBJECT_DESCR, True)
            self.HLineTip = tip
            ChartRedraw(0)
            return True
        return False
    def GetName(self):
        return self.HLineName
    def GetPrice(self):
        return self.HLinePrice
    def GetColor(self):
        return self.HLineColor
    def GetStyle(self):
        return self.HLineStyle
    def GetWidth(self):
        return self.HLineWidth
    def GetBack(self):
        return self.HLineBack
    def GetHidden(self):
        return self.HLineHidden
    def GetText(self):
        return self.HLineText
    def GetTip(self):
        return self.HLineTip
    def GenerateRandName(self):
        ind = 0
        RandName = ""
        MathSrand(GetTickCount())
        while ind < 32767:
            RandName = 'No_Name_HLine_' + IntegerToString(MathRand())
            if ObjectFind(0, RandName) < 0:
                return RandName
            ind += 1
        return 'Error'
    def CreateHLine(self):
        ObjectCreate(0, self.HLineName, OBJ_HLINE, 0, 0, self.HLinePrice)
        ObjectSetInteger(0, self.HLineName, OBJPROP_STYLE, self.HLineStyle)
        ObjectSetInteger(0, self.HLineName, OBJPROP_COLOR, self.HLineColor)
        ObjectSetInteger(0, self.HLineName, OBJPROP_WIDTH, self.HLineWidth)
        ObjectSetInteger(0, self.HLineName, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, self.HLineName, OBJPROP_SELECTED, False)
        ObjectSetInteger(0, self.HLineName, OBJPROP_BACK, self.HLineBack)
        ObjectSetInteger(0, self.HLineName, OBJPROP_HIDDEN, self.HLineHidden)
        if self.HLineText != "":
            ObjectSetString(0, self.HLineName, OBJPROP_TEXT, self.HLineText)
            ChartSetInteger(0, CHART_SHOW_OBJECT_DESCR, True)
        if self.HLineTip != "":
            ObjectSetString(0, self.HLineName, OBJPROP_TOOLTIP, self.HLineTip)
            ChartSetInteger(0, CHART_SHOW_OBJECT_DESCR, True)
        ChartRedraw(0)
    def DeletHLine(self):
        ObjectDelete(0, self.HLineName)
        ChartRedraw(0)

__all__ = ['MyCHLine']
