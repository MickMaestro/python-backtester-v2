"""mycarrow.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh


class MyCArrow(CObject):
    _q_fields = ('ArrowName', 'ArrowTip', 'ArrowPrice', 'ArrowTime', 'ArrowType', 'ArrowCode', 'ArrowColor', 'ArrowAnchor')
    def _q_ctor1(self):
        CObject.__init__(self)
        self.ArrowName = ""
        self.ArrowTip = ""
        self.ArrowPrice = 0.0
        self.ArrowTime = 0
        self.ArrowType = 0
        self.ArrowCode = 0
        self.ArrowColor = 0
        self.ArrowAnchor = 0
        last_tick = MqlTick()
        if SymbolInfoTick(Symbol(), last_tick):
            self.ArrowPrice = last_tick.ask
            self.ArrowTime = last_tick.time
        else:
            self.ArrowPrice = 0.0
            self.ArrowTime = 43200
        self.ArrowName = self.GenerateRandName()
        self.ArrowTip = 'No_Tip'
        self.ArrowType = OBJ_ARROW
        self.ArrowCode = 58
        self.ArrowColor = clrRed
        self.ArrowAnchor = ANCHOR_TOP
        self.CreateArrow()
    def _q_ctor2(self, APrice, ATime):
        CObject.__init__(self)
        self.ArrowName = ""
        self.ArrowTip = ""
        self.ArrowPrice = 0.0
        self.ArrowTime = 0
        self.ArrowType = 0
        self.ArrowCode = 0
        self.ArrowColor = 0
        self.ArrowAnchor = 0
        self.ArrowName = self.GenerateRandName()
        self.ArrowTip = 'No_Tip'
        self.ArrowPrice = APrice
        self.ArrowTime = ATime
        self.ArrowType = OBJ_ARROW
        self.ArrowCode = 58
        self.ArrowColor = clrRed
        self.ArrowAnchor = ANCHOR_TOP
        self.CreateArrow()
    def _q_ctor3(self, APrice, ATime, AType):
        CObject.__init__(self)
        self.ArrowName = ""
        self.ArrowTip = ""
        self.ArrowPrice = 0.0
        self.ArrowTime = 0
        self.ArrowType = 0
        self.ArrowCode = 0
        self.ArrowColor = 0
        self.ArrowAnchor = 0
        self.ArrowName = self.GenerateRandName()
        self.ArrowTip = 'No_Tip'
        self.ArrowPrice = APrice
        self.ArrowTime = ATime
        self.ArrowCode = 58
        self.ArrowColor = clrRed
        self.ArrowAnchor = ANCHOR_TOP
        _sw1 = AType
        if _sw1 in (OBJ_ARROW_BUY, OBJ_ARROW_SELL, OBJ_ARROW_STOP, OBJ_ARROW_CHECK, OBJ_ARROW_UP, OBJ_ARROW_DOWN, OBJ_ARROW_LEFT_PRICE, OBJ_ARROW_RIGHT_PRICE, OBJ_ARROW_THUMB_UP, OBJ_ARROW_THUMB_DOWN):
            self.ArrowType = AType
        else:
            self.ArrowType = OBJ_ARROW
        self.CreateArrow()
    def _q_ctor4(self, AName, ATip, APrice, ATime, AType):
        CObject.__init__(self)
        self.ArrowName = ""
        self.ArrowTip = ""
        self.ArrowPrice = 0.0
        self.ArrowTime = 0
        self.ArrowType = 0
        self.ArrowCode = 0
        self.ArrowColor = 0
        self.ArrowAnchor = 0
        if ObjectFind(0, AName) < 0:
            self.ArrowName = AName
        else:
            self.ArrowName = self.GenerateRandName()
        self.ArrowTip = ATip
        self.ArrowPrice = APrice
        self.ArrowTime = ATime
        self.ArrowCode = 58
        self.ArrowColor = clrRed
        self.ArrowAnchor = ANCHOR_TOP
        _sw2 = AType
        if _sw2 in (OBJ_ARROW_BUY, OBJ_ARROW_SELL, OBJ_ARROW_STOP, OBJ_ARROW_CHECK, OBJ_ARROW_UP, OBJ_ARROW_DOWN, OBJ_ARROW_LEFT_PRICE, OBJ_ARROW_RIGHT_PRICE, OBJ_ARROW_THUMB_UP, OBJ_ARROW_THUMB_DOWN):
            self.ArrowType = AType
        else:
            self.ArrowType = OBJ_ARROW
        self.CreateArrow()
    def __init__(self, *args):
        if 0 <= len(args) <= 0:
            self._q_ctor1(*args)
            return
        if 2 <= len(args) <= 2 and (len(args) == 0 or isinstance(args[0], float)):
            self._q_ctor2(*args)
            return
        if 3 <= len(args) <= 3 and (len(args) == 0 or isinstance(args[0], float)):
            self._q_ctor3(*args)
            return
        if 5 <= len(args) <= 5 and (len(args) == 0 or isinstance(args[0], str)):
            self._q_ctor4(*args)
            return
        self._q_ctor1(*args)
    def _q_dtor(self):
        if ObjectFind(0, self.ArrowName) >= 0:
            self.DeletArrow()
    def SetName(self, NewName):
        if ObjectSetString(0, self.ArrowName, OBJPROP_NAME, NewName):
            self.ArrowName = NewName
            ChartRedraw(0)
            return True
        Print('MyCArrow::SetName', ' ERROR: ', GetLastError())
        return False
    def SetTip(self, NewTip):
        if ObjectSetString(0, self.ArrowName, OBJPROP_TOOLTIP, NewTip):
            self.ArrowTip = NewTip
            ChartRedraw(0)
            return True
        Print('MyCArrow::SetTip', ' ERROR: ', GetLastError())
        return False
    def SetPrice(self, NewPrice):
        if ObjectSetDouble(0, self.ArrowName, OBJPROP_PRICE, NewPrice):
            self.ArrowPrice = NewPrice
            ChartRedraw(0)
            return True
        Print('MyCArrow::SetPrice', ' ERROR: ', GetLastError())
        return False
    def SetTime(self, NewTime):
        if ObjectSetInteger(0, self.ArrowName, OBJPROP_TIME, NewTime):
            self.ArrowTime = NewTime
            ChartRedraw(0)
            return True
        Print('MyCArrow::SetTime', ' ERROR: ', GetLastError())
        return False
    def SetType(self, NewType):
        self.DeletArrow()
        self.ArrowType = NewType
        self.CreateArrow()
        return True
    def SetCode(self, NewCode):
        if self.ArrowType == OBJ_ARROW:
            if NewCode >= 32 and NewCode <= 255:
                self.ArrowCode = NewCode
            else:
                return False
            ret = ObjectSetInteger(0, self.ArrowName, OBJPROP_ARROWCODE, self.ArrowCode)
            ChartRedraw(0)
            return ret
        return False
    def SetColor(self, NewColor):
        self.ArrowColor = NewColor
        ret = ObjectSetInteger(0, self.ArrowName, OBJPROP_COLOR, self.ArrowColor)
        ChartRedraw(0)
        return ret
    def SetAnchor(self, Anchor):
        if ObjectSetInteger(0, self.ArrowName, OBJPROP_ANCHOR, Anchor):
            self.ArrowAnchor = Anchor
            ChartRedraw(0)
            return True
        Print('MyCArrow::SetAnchor', ' ERROR: ', GetLastError())
        return False
    def GetName(self):
        return self.ArrowName
    def GetTip(self):
        return self.ArrowTip
    def GetPrice(self):
        return self.ArrowPrice
    def GetTime(self):
        return self.ArrowTime
    def GetType(self):
        return self.ArrowType
    def GetCode(self):
        return self.ArrowCode
    def GetColor(self):
        return self.ArrowColor
    def GetAnchor(self):
        return self.ArrowAnchor
    def CreateArrow(self):
        ObjectCreate(0, self.ArrowName, self.ArrowType, 0, self.ArrowTime, self.ArrowPrice)
        if self.ArrowType == OBJ_ARROW:
            ObjectSetInteger(0, self.ArrowName, OBJPROP_ARROWCODE, self.ArrowCode)
        ObjectSetInteger(0, self.ArrowName, OBJPROP_COLOR, self.ArrowColor)
        ObjectSetString(0, self.ArrowName, OBJPROP_TOOLTIP, self.ArrowTip)
        ObjectSetInteger(0, self.ArrowName, OBJPROP_ANCHOR, self.ArrowAnchor)
        ChartRedraw(0)
    def DeletArrow(self):
        ObjectDelete(0, self.ArrowName)
        ChartRedraw(0)
    def GenerateRandName(self):
        ind = 0
        RandName = ""
        MathSrand(GetTickCount())
        while ind < 32767:
            RandName = 'No_Name_Arrow_' + IntegerToString(MathRand())
            if ObjectFind(0, RandName) < 0:
                return RandName
            ind += 1
        return 'Error'

__all__ = ['MyCArrow']
