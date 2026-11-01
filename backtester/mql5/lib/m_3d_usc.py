"""USC.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.m_3d_igo import *  # IGO.mqh
from backtester.mql5.lib.m_3d_gm import *  # GM.mqh


class sPointCoordinates(MqlObject):
    _q_fields = ('time', 'price')
    def __init__(self, *args):
        self.time = 0
        self.price = 0.0

class CUSC(CIGO):
    _q_fields = ('m_prev_bar', 'm_next_bar', 'Centr', 'AxisZ', 'AxisY', 'AxisX', 'gCentr', 'gAxisY', 'gAxisX')
    def __init__(self):
        CIGO.__init__(self)
        self.m_prev_bar = 0
        self.m_next_bar = 0
        self.Centr = C_OBJ_ARROW_RIGHT_PRICE()
        self.AxisZ = C_OBJ_TREND()
        self.AxisY = C_OBJ_TRENDBYANGLE()
        self.AxisX = C_OBJ_TRENDBYANGLE()
        self.gCentr = CGM()
        self.gAxisY = CGM()
        self.gAxisX = CGM()
        ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, 0, False)
        ChartSetInteger(0, CHART_EVENT_OBJECT_CREATE, 0, True)
        ChartSetInteger(0, CHART_EVENT_OBJECT_DELETE, 0, True)
        ChartSetInteger(0, CHART_COLOR_GRID, clrNONE)
        ChartSetInteger(0, CHART_COLOR_CHART_UP, clrNONE)
        ChartSetInteger(0, CHART_COLOR_CHART_DOWN, clrNONE)
        ChartSetInteger(0, CHART_COLOR_CHART_LINE, clrNONE)
        ChartSetInteger(0, CHART_COLOR_CANDLE_BULL, clrNONE)
        ChartSetInteger(0, CHART_COLOR_CANDLE_BEAR, clrNONE)
    def _q_dtor(self):
        pass
    def Z(self, price, barX, barY):
        res = sPointCoordinates()
        res.price = 0.0
        res.time = 0
        dX = 0.0
        dY = 0.0
        dX = 0.0
        dX = self.gAxisX.R_ValueByTime(T_u(barX)) - self.m_price
        dY = 0.0
        dY = self.gAxisY.R_ValueByTime(T_u(-barY)) - self.m_price
        res.price = price + dX - dY
        res.time = T_u(barX - barY)
        return _copy(res)
    def on_bar(self):
        self.m_next_bar = T_u(0)
        if self.m_next_bar > self.m_prev_bar:
            self.m_prev_bar = self.m_next_bar
            return True
        return False
    def Create(self, name):
        self.Centr.Create('Axis XYZ')
        self.gCentr.Create(self.Centr.m_name)
        self.m_price = self.gCentr.R_OBJPROP_PRICE()
        self.AxisZ.Create('Axis Z')
        self.AxisY.Create('Axis Y', self.gCentr.R_OBJPROP_PRICE(), 30.0)
        self.gAxisY.Create(self.AxisY.m_name)
        self.m_angle = self.gAxisY.R_OBJPROP_ANGLE()
        self.AxisX.Create('Axis X', self.gCentr.R_OBJPROP_PRICE(), self.gAxisY.R_OBJPROP_ANGLE() + 120)
        self.gAxisX.Create(self.AxisX.m_name)
        ChartRedraw()
        self.on_event = True
    def OnEvent(self, id_, lparam, dparam, sparam):
        if self.on_event:
            self.AxisZ.OnEvent(id_, lparam, dparam, sparam)
            if self.Centr.OnEvent(id_, lparam, dparam, sparam):
                self.AxisY.OnEvent(id_, lparam, dparam, sparam, 1, self.gCentr.R_OBJPROP_PRICE())
                self.AxisX.OnEvent(id_, lparam, dparam, sparam, 1, self.gCentr.R_OBJPROP_PRICE())
            else:
                if self.AxisY.OnEvent(id_, lparam, dparam, sparam):
                    self.AxisX.OnEvent(id_, lparam, dparam, sparam, 2, self.gAxisY.R_OBJPROP_ANGLE() + 120)
                else:
                    if self.AxisX.OnEvent(id_, lparam, dparam, sparam):
                        self.AxisY.OnEvent(id_, lparam, dparam, sparam, 2, self.gAxisX.R_OBJPROP_ANGLE() - 120)
            ChartRedraw()
            self.m_price = self.gCentr.R_OBJPROP_PRICE()
            self.m_angle = self.gAxisY.R_OBJPROP_ANGLE()

__all__ = ['sPointCoordinates', 'CUSC']
