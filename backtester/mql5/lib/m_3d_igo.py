"""IGO.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class sXY(MqlObject):
    _q_fields = ('X', 'Y')
    def __init__(self, *args):
        self.X = 0
        self.Y = 0

class CIGO(MqlObject):
    _q_fields = ('on_event', 'm_layer', 'm_name', 'm_price', 'm_angle')
    def __init__(self):
        self.on_event = False
        self.m_layer = 0
        self.m_name = ""
        self.m_price = 0.0
        self.m_angle = 0.0
        self.on_event = False
        self.m_layer = 0
    def _q_dtor(self):
        pass
    def SetPrice(self, def_, prop_modifier=0):
        if self.m_price == 0:
            self.m_price = ObjectGetDouble(0, self.m_name, OBJPROP_PRICE, prop_modifier)
        if self.m_price == 0:
            self.m_price = def_
        return self.m_price
    def Create(self, name):
        self.on_event = True
    def Redraw(self):
        ChartRedraw()
    def OnEvent(self, id_, lparam, dparam, sparam, iparamemr=0, dparametr=0.0):
        res = False
        if self.on_event:
            if id_ == CHARTEVENT_OBJECT_DELETE and sparam == self.m_name:
                self.Create(self.m_name)
            if id_ == CHARTEVENT_CHART_CHANGE:
                self.Redraw()
            if id_ == CHARTEVENT_OBJECT_DRAG:
                if ObjectGetInteger(0, sparam, OBJPROP_SELECTED) == 1 and sparam == self.m_name:
                    self.m_price = ObjectGetDouble(0, self.m_name, OBJPROP_PRICE)
                    self.Redraw()
                    res = True
            if id_ == CHARTEVENT_OBJECT_CLICK and sparam != self.m_name:
                ObjectSetInteger(0, self.m_name, OBJPROP_SELECTED, 0)
                ChartRedraw()
        return res

class C_OBJ_ARROW_RIGHT_PRICE(CIGO):
    _q_fields = ()
    def __init__(self, *args):
        CIGO.__init__(self)
    def Create(self, name):
        self.m_name = name
        self.m_price = self.SetPrice((ChartGetDouble(0, CHART_PRICE_MAX) + ChartGetDouble(0, CHART_PRICE_MIN)) / 2)
        ObjectCreate(0, self.m_name, OBJ_ARROW_RIGHT_PRICE, 0, 0, 0)
        ObjectSetInteger(0, self.m_name, OBJPROP_SELECTABLE, True)
        ObjectSetInteger(0, self.m_name, OBJPROP_WIDTH, 1)
        ObjectSetInteger(0, self.m_name, OBJPROP_COLOR, clrSilver)
        ObjectSetInteger(0, self.m_name, OBJPROP_TIME, 0, T_u(0))
        ObjectSetDouble(0, self.m_name, OBJPROP_PRICE, 0, self.m_price)
        ChartRedraw()
        self.on_event = True
    def Redraw(self):
        ObjectSetInteger(0, self.m_name, OBJPROP_TIME, 0, T_u(0))
        ChartRedraw()

class C_OBJ_TREND(CIGO):
    _q_fields = ()
    def __init__(self, *args):
        CIGO.__init__(self)
    def Create(self, name):
        self.m_name = name
        self.m_price = (ChartGetDouble(0, CHART_PRICE_MAX) + ChartGetDouble(0, CHART_PRICE_MIN)) / 2
        ObjectCreate(0, self.m_name, OBJ_TREND, 0, 0, 0)
        ObjectSetInteger(0, self.m_name, OBJPROP_COLOR, clrSilver)
        ObjectSetInteger(0, self.m_name, OBJPROP_WIDTH, 0)
        ObjectSetInteger(0, self.m_name, OBJPROP_STYLE, STYLE_DASH)
        ObjectSetDouble(0, self.m_name, OBJPROP_PRICE, 0, self.m_price)
        ObjectSetInteger(0, self.m_name, OBJPROP_TIME, 0, T_u(0))
        ObjectSetDouble(0, self.m_name, OBJPROP_PRICE, 1, self.m_price + 1)
        ObjectSetInteger(0, self.m_name, OBJPROP_TIME, 1, T_u(0))
        ObjectSetInteger(0, self.m_name, OBJPROP_RAY_RIGHT, True)
        ObjectSetInteger(0, self.m_name, OBJPROP_RAY_LEFT, True)
        ObjectSetInteger(0, self.m_name, OBJPROP_BACK, True)
        ObjectSetInteger(0, self.m_name, OBJPROP_SELECTABLE, False)
        ChartRedraw()
        self.on_event = True
    def Redraw(self):
        ObjectSetInteger(0, self.m_name, OBJPROP_TIME, 0, T_u(0))
        ObjectSetInteger(0, self.m_name, OBJPROP_TIME, 1, T_u(0))
        ChartRedraw()

class C_OBJ_TRENDBYANGLE(CIGO):
    _q_fields = ('m_bar',)
    def __init__(self):
        CIGO.__init__(self)
        self.m_bar = 0
        self.m_bar = 25
    def SetAngle(self, def_):
        if self.m_angle == 0:
            self.m_angle = ObjectGetDouble(0, self.m_name, OBJPROP_ANGLE)
        if self.m_angle == 0:
            self.m_angle = def_
        return self.m_angle
    def Create(self, name, price, angle):
        time = T_u(0)
        deltaT = T_u(self.m_bar) - time
        self.m_name = name
        self.m_price = self.SetPrice(price)
        self.m_angle = self.SetAngle(angle)
        ObjectCreate(0, self.m_name, OBJ_TRENDBYANGLE, 0, time, self.m_price, time + deltaT, self.m_price)
        ObjectSetInteger(0, self.m_name, OBJPROP_COLOR, clrSilver)
        ObjectSetInteger(0, self.m_name, OBJPROP_WIDTH, 0)
        ObjectSetInteger(0, self.m_name, OBJPROP_STYLE, STYLE_DASH)
        ObjectSetInteger(0, self.m_name, OBJPROP_RAY_RIGHT, True)
        ObjectSetInteger(0, self.m_name, OBJPROP_RAY_LEFT, True)
        ObjectSetInteger(0, self.m_name, OBJPROP_BACK, True)
        ObjectSetInteger(0, self.m_name, OBJPROP_SELECTABLE, True)
        ObjectSetDouble(0, self.m_name, OBJPROP_ANGLE, self.m_angle)
        ChartRedraw()
        self.on_event = True
    def Redraw(self):
        ObjectSetInteger(0, self.m_name, OBJPROP_TIME, T_u(0))
        ObjectSetInteger(0, self.m_name, OBJPROP_TIME, 1, T_u(0) + T_u(self.m_bar) - T_u(0))
        ObjectSetDouble(0, self.m_name, OBJPROP_PRICE, self.m_price)
        ObjectSetDouble(0, self.m_name, OBJPROP_ANGLE, self.m_angle)
        ChartRedraw()
    def OnEvent(self, id_, lparam, dparam, sparam, iparamemr=0, dparametr=0.0):
        res = False
        if self.on_event:
            if id_ == CHARTEVENT_OBJECT_DELETE and sparam == self.m_name:
                self.Create(self.m_name, self.m_price, self.m_angle)
            if id_ == CHARTEVENT_CHART_CHANGE:
                self.Redraw()
            if id_ == CHARTEVENT_OBJECT_DRAG:
                if ObjectGetInteger(0, sparam, OBJPROP_SELECTED) == 1 and sparam == self.m_name:
                    self.m_angle = ObjectGetDouble(0, self.m_name, OBJPROP_ANGLE)
                    self.Create(self.m_name, self.m_price, self.m_angle)
                    res = True
                if iparamemr == 1:
                    self.m_price = dparametr
                    self.Create(self.m_name, self.m_price, self.m_angle)
                if iparamemr == 2:
                    self.m_angle = dparametr
                    self.Create(self.m_name, self.m_price, self.m_angle)
            if id_ == CHARTEVENT_OBJECT_CLICK and sparam != self.m_name:
                ObjectSetInteger(0, self.m_name, OBJPROP_SELECTED, 0)
                ChartRedraw()
        return res

def TimePriceToXY(time, price, xy):
    res = _copy(xy)
    x = Box(0)
    y = Box(0)
    if ChartTimePriceToXY(0, 0, time, price, x, y):
        res.X = x.v
        res.Y = y.v
    return _copy(res)

def T_u(bar):
    m_time = Arr(0, 0)
    if ArraySetAsSeries(m_time, True) and CopyTime(Symbol(), Period(), bar, 1, m_time) > 0:
        return m_time[0]
    return -1

__all__ = ['sXY', 'CIGO', 'C_OBJ_ARROW_RIGHT_PRICE', 'C_OBJ_TREND', 'C_OBJ_TRENDBYANGLE', 'TimePriceToXY', 'T_u']
