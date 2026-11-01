"""myctrendline.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh


class MyCTrendLine(CObject):
    _q_fields = ('TrendLineName', 'TrendLinePrice1', 'TrendLineTime1', 'TrendLinePrice2', 'TrendLineTime2', 'TrendLineStyle', 'TrendLineColor', 'TrendLineWidth', 'TrendLineBack', 'TrendLineRayLeft', 'TrendLineRayRight', 'TrendLineHidden')
    def _q_ctor1(self):
        CObject.__init__(self)
        self.TrendLineName = ""
        self.TrendLinePrice1 = 0.0
        self.TrendLineTime1 = 0
        self.TrendLinePrice2 = 0.0
        self.TrendLineTime2 = 0
        self.TrendLineStyle = 0
        self.TrendLineColor = 0
        self.TrendLineWidth = 0
        self.TrendLineBack = False
        self.TrendLineRayLeft = False
        self.TrendLineRayRight = False
        self.TrendLineHidden = False
        last_tick = MqlTick()
        self.TrendLineName = self.GenerateRandName()
        if SymbolInfoTick(Symbol(), last_tick):
            self.TrendLinePrice1 = last_tick.ask
            self.TrendLineTime1 = last_tick.time
            self.TrendLinePrice2 = last_tick.bid
            self.TrendLineTime2 = last_tick.time - Period()
        else:
            self.TrendLinePrice1 = 0.0
            self.TrendLineTime1 = 43200
            self.TrendLinePrice2 = 0.01
            self.TrendLineTime2 = 43200 + Period()
        self.TrendLineStyle = STYLE_SOLID
        self.TrendLineColor = clrRed
        self.TrendLineWidth = 1
        self.TrendLineBack = False
        self.TrendLineRayLeft = False
        self.TrendLineRayRight = False
        self.TrendLineHidden = True
        self.CreateTrend()
    def _q_ctor2(self, price1, time1, price2, time2):
        CObject.__init__(self)
        self.TrendLineName = ""
        self.TrendLinePrice1 = 0.0
        self.TrendLineTime1 = 0
        self.TrendLinePrice2 = 0.0
        self.TrendLineTime2 = 0
        self.TrendLineStyle = 0
        self.TrendLineColor = 0
        self.TrendLineWidth = 0
        self.TrendLineBack = False
        self.TrendLineRayLeft = False
        self.TrendLineRayRight = False
        self.TrendLineHidden = False
        self.TrendLineName = self.GenerateRandName()
        self.TrendLinePrice1 = price1
        self.TrendLineTime1 = time1
        self.TrendLinePrice2 = price2
        self.TrendLineTime2 = time2
        self.TrendLineStyle = STYLE_SOLID
        self.TrendLineColor = clrRed
        self.TrendLineWidth = 1
        self.TrendLineBack = False
        self.TrendLineRayLeft = False
        self.TrendLineRayRight = False
        self.TrendLineHidden = True
        self.CreateTrend()
    def _q_ctor3(self, price1, time1, price2, time2, style):
        CObject.__init__(self)
        self.TrendLineName = ""
        self.TrendLinePrice1 = 0.0
        self.TrendLineTime1 = 0
        self.TrendLinePrice2 = 0.0
        self.TrendLineTime2 = 0
        self.TrendLineStyle = 0
        self.TrendLineColor = 0
        self.TrendLineWidth = 0
        self.TrendLineBack = False
        self.TrendLineRayLeft = False
        self.TrendLineRayRight = False
        self.TrendLineHidden = False
        self.TrendLineName = self.GenerateRandName()
        self.TrendLinePrice1 = price1
        self.TrendLineTime1 = time1
        self.TrendLinePrice2 = price2
        self.TrendLineTime2 = time2
        self.TrendLineStyle = style
        self.TrendLineColor = clrRed
        self.TrendLineWidth = 1
        self.TrendLineBack = False
        self.TrendLineRayLeft = False
        self.TrendLineRayRight = False
        self.TrendLineHidden = True
        self.CreateTrend()
    def _q_ctor4(self, name, price1, time1, price2, time2, style):
        CObject.__init__(self)
        self.TrendLineName = ""
        self.TrendLinePrice1 = 0.0
        self.TrendLineTime1 = 0
        self.TrendLinePrice2 = 0.0
        self.TrendLineTime2 = 0
        self.TrendLineStyle = 0
        self.TrendLineColor = 0
        self.TrendLineWidth = 0
        self.TrendLineBack = False
        self.TrendLineRayLeft = False
        self.TrendLineRayRight = False
        self.TrendLineHidden = False
        if ObjectFind(0, name) < 0:
            self.TrendLineName = name
        else:
            self.TrendLineName = self.GenerateRandName()
        self.TrendLinePrice1 = price1
        self.TrendLineTime1 = time1
        self.TrendLinePrice2 = price2
        self.TrendLineTime2 = time2
        self.TrendLineStyle = style
        self.TrendLineColor = clrRed
        self.TrendLineWidth = 1
        self.TrendLineBack = False
        self.TrendLineRayLeft = False
        self.TrendLineRayRight = False
        self.TrendLineHidden = True
        self.CreateTrend()
    def __init__(self, *args):
        if 0 <= len(args) <= 0:
            self._q_ctor1(*args)
            return
        if 4 <= len(args) <= 4 and (len(args) == 0 or isinstance(args[0], float)):
            self._q_ctor2(*args)
            return
        if 5 <= len(args) <= 5 and (len(args) == 0 or isinstance(args[0], float)):
            self._q_ctor3(*args)
            return
        if 6 <= len(args) <= 6 and (len(args) == 0 or isinstance(args[0], str)):
            self._q_ctor4(*args)
            return
        self._q_ctor1(*args)
    def _q_dtor(self):
        if ObjectFind(0, self.TrendLineName) >= 0:
            self.DeletTrend()
    def SetName(self, name):
        if ObjectSetString(0, self.TrendLineName, OBJPROP_NAME, name):
            self.TrendLineName = name
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetName', ' ERROR: ', GetLastError())
        return False
    def SetPrice1(self, price1):
        if ObjectSetDouble(0, self.TrendLineName, OBJPROP_PRICE, 0, price1):
            self.TrendLinePrice1 = price1
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetPrice1', ' ERROR: ', GetLastError())
        return False
    def SetTime1(self, time1):
        if ObjectSetInteger(0, self.TrendLineName, OBJPROP_TIME, 0, time1):
            self.TrendLineTime1 = time1
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetTime1', ' ERROR: ', GetLastError())
        return False
    def SetPrice2(self, price2):
        if ObjectSetDouble(0, self.TrendLineName, OBJPROP_PRICE, 1, price2):
            self.TrendLinePrice2 = price2
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetPrice2', ' ERROR: ', GetLastError())
        return False
    def SetTime2(self, time2):
        if ObjectSetInteger(0, self.TrendLineName, OBJPROP_TIME, 1, time2):
            self.TrendLineTime2 = time2
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetTime2', ' ERROR: ', GetLastError())
        return False
    def SetColor(self, col):
        if ObjectSetInteger(0, self.TrendLineName, OBJPROP_COLOR, col):
            self.TrendLineColor = col
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetColor', ' ERROR: ', GetLastError())
        return False
    def SetStyle(self, style):
        if ObjectSetInteger(0, self.TrendLineName, OBJPROP_STYLE, style):
            self.TrendLineStyle = style
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetStyle', ' ERROR: ', GetLastError())
        return False
    def SetWidth(self, width):
        if ObjectSetInteger(0, self.TrendLineName, OBJPROP_WIDTH, width):
            self.TrendLineWidth = width
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetWidth', ' ERROR: ', GetLastError())
        return False
    def SetBack(self, back):
        if ObjectSetInteger(0, self.TrendLineName, OBJPROP_BACK, back):
            self.TrendLineBack = back
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetBack', ' ERROR: ', GetLastError())
        return False
    def SetRayLeft(self, left):
        if ObjectSetInteger(0, self.TrendLineName, OBJPROP_RAY_LEFT, left):
            self.TrendLineRayLeft = left
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetRayLeft', ' ERROR: ', GetLastError())
        return False
    def SetRayRight(self, right):
        if ObjectSetInteger(0, self.TrendLineName, OBJPROP_RAY_RIGHT, right):
            self.TrendLineRayRight = right
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetRayRight', ' ERROR: ', GetLastError())
        return False
    def SetHidden(self, hidden):
        if ObjectSetInteger(0, self.TrendLineName, OBJPROP_HIDDEN, hidden):
            self.TrendLineHidden = hidden
            ChartRedraw(0)
            return True
        Print('MyCTrendLine::SetHidden', ' ERROR: ', GetLastError())
        return False
    def GetName(self):
        return self.TrendLineName
    def GetPrice1(self):
        return self.TrendLinePrice1
    def GetTime1(self):
        return self.TrendLineTime1
    def GetPrice2(self):
        return self.TrendLinePrice2
    def GetTime2(self):
        return self.TrendLineTime2
    def GetColor(self):
        return self.TrendLineColor
    def GetStyle(self):
        return self.TrendLineStyle
    def GetWidth(self):
        return self.TrendLineWidth
    def GetBack(self):
        return self.TrendLineBack
    def GetRayLeft(self):
        return self.TrendLineRayLeft
    def GetRayRight(self):
        return self.TrendLineRayRight
    def GetHidden(self):
        return self.TrendLineHidden
    def CreateTrend(self):
        ObjectCreate(0, self.TrendLineName, OBJ_TREND, 0, self.TrendLineTime1, self.TrendLinePrice1, self.TrendLineTime2, self.TrendLinePrice2)
        ObjectSetInteger(0, self.TrendLineName, OBJPROP_STYLE, self.TrendLineStyle)
        ObjectSetInteger(0, self.TrendLineName, OBJPROP_COLOR, self.TrendLineColor)
        ObjectSetInteger(0, self.TrendLineName, OBJPROP_WIDTH, self.TrendLineWidth)
        ObjectSetInteger(0, self.TrendLineName, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, self.TrendLineName, OBJPROP_SELECTED, False)
        ObjectSetInteger(0, self.TrendLineName, OBJPROP_BACK, self.TrendLineBack)
        ObjectSetInteger(0, self.TrendLineName, OBJPROP_RAY_LEFT, self.TrendLineRayLeft)
        ObjectSetInteger(0, self.TrendLineName, OBJPROP_RAY_RIGHT, self.TrendLineRayRight)
        ObjectSetInteger(0, self.TrendLineName, OBJPROP_HIDDEN, self.TrendLineHidden)
        ChartRedraw(0)
    def DeletTrend(self):
        ObjectDelete(0, self.TrendLineName)
        ChartRedraw(0)
    def GenerateRandName(self):
        ind = 0
        RandName = ""
        MathSrand(GetTickCount())
        while ind < 32767:
            RandName = 'No_Name_Trend_' + IntegerToString(MathRand())
            if ObjectFind(0, RandName) < 0:
                return RandName
            ind += 1
        return 'Error'

__all__ = ['MyCTrendLine']
