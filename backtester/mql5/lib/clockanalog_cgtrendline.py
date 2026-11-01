"""CGTrendLine.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.clockanalog_cgraphbase import *  # CGraphBase.mqh


class CGTrendline(MqlObject):
    _q_fields = ('m_name', 'm_id', 'm_subwin', 'm_created', 'm_time1', 'm_price1', 'm_time2', 'm_price2', 'm_color', 'm_style', 'm_width', 'm_back', 'm_selected', 'm_selectable', 'm_ray_right', 'm_hidden', 'm_zorder', 'm_graph_base')
    _q_ptrs = ('m_graph_base',)
    def __init__(self, aName, aID=0, aSubWin=0):
        self.m_name = ""
        self.m_id = 0
        self.m_subwin = 0
        self.m_created = False
        self.m_time1 = 0
        self.m_price1 = 0.0
        self.m_time2 = 0
        self.m_price2 = 0.0
        self.m_color = 0
        self.m_style = 0
        self.m_width = 0
        self.m_back = False
        self.m_selected = False
        self.m_selectable = False
        self.m_ray_right = False
        self.m_hidden = False
        self.m_zorder = 0
        self.m_graph_base = None
        self.m_created = False
        self.m_name = aName
        self.m_id = aID
        self.m_subwin = aSubWin
        self.m_graph_base = CGraphBase(self.m_name, self.m_id, self.m_subwin, True)
    def _q_dtor(self):
        _delete(self.m_graph_base)
    def Create(self):
        self.m_created = False
        if self.m_graph_base.CreateTrend():
            self.m_created = True
    def DeleteTrend(self):
        if self.m_created:
            self.m_graph_base.Delete()
    def SetLeftPos(self, aTime, aPrice):
        if self.m_created:
            self.m_time1 = aTime
            self.m_price1 = aPrice
            self.m_graph_base.SetTimePrice(0, self.m_time1, self.m_price1)
    def SetRightPos(self, aTime, aPrice):
        if self.m_created:
            self.m_time2 = aTime
            self.m_price2 = aPrice
            self.m_graph_base.SetTimePrice(1, self.m_time2, self.m_price2)
    def SetPositions(self, aTime1, aPrice1, aTime2, aPrice2):
        self.SetLeftPos(aTime1, aPrice1)
        self.SetRightPos(aTime2, aPrice2)
    def SetColor(self, aColor=255):
        if self.m_created:
            self.m_color = aColor
            self.m_graph_base.SetColor(self.m_color)
    def SetStyle(self, aStyle=0):
        if self.m_created:
            self.m_style = aStyle
            self.m_graph_base.SetStyle(self.m_style)
    def SetWidth(self, aWidth=1):
        if self.m_created:
            self.m_width = aWidth
            self.m_graph_base.SetWidth(self.m_width)
    def SetBack(self, aValue=False):
        if self.m_created:
            self.m_back = aValue
            self.m_graph_base.SetBack(self.m_back)
    def SetSelected(self, aValue=False):
        if self.m_created:
            self.m_selected = aValue
            self.m_graph_base.SetSelected(self.m_selected)
    def SetSelectable(self, aValue=True):
        if self.m_created:
            self.m_selectable = aValue
            self.m_graph_base.SetSelectable(self.m_selectable)
    def SetRay(self, aValue=False):
        if self.m_created:
            self.m_ray_right = aValue
            self.m_graph_base.SetRayRight(self.m_ray_right)
    def SetHidden(self, aValue=False):
        if self.m_created:
            self.m_hidden = aValue
            self.m_graph_base.SetHidden(self.m_hidden)
    def SetZOrder(self, aValue=0):
        if self.m_created:
            self.m_zorder = aValue
            self.m_graph_base.SetZOrder(self.m_zorder)
    def Name(self):
        return self.m_name
    def Selected(self):
        pass
    def PriceByTime(self, aTime):
        pass

__all__ = ['CGTrendline']
