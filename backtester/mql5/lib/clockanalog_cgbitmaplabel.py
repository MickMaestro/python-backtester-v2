"""CGBitmapLabel.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.clockanalog_cgraphbase import *  # CGraphBase.mqh


class CGBitmapLabel(MqlObject):
    _q_fields = ('m_name', 'm_id', 'm_subwin', 'm_created', 'm_file_on', 'm_file_off', 'm_xdist', 'm_ydist', 'm_xsize', 'm_ysize', 'm_xoffset', 'm_yoffset', 'm_state', 'm_corner', 'm_anchor', 'm_colorBD', 'm_style', 'm_point_width', 'm_back', 'm_selected', 'm_selectable', 'm_zorder', 'm_hidden', 'm_graph_base')
    _q_ptrs = ('m_graph_base',)
    def __init__(self, aName='BitmapLabel_', file_on='', file_off='', aID=0, aSubWin=0):
        self.m_name = ""
        self.m_id = 0
        self.m_subwin = 0
        self.m_created = False
        self.m_file_on = ""
        self.m_file_off = ""
        self.m_xdist = 0
        self.m_ydist = 0
        self.m_xsize = 0
        self.m_ysize = 0
        self.m_xoffset = 0
        self.m_yoffset = 0
        self.m_state = False
        self.m_corner = 0
        self.m_anchor = 0
        self.m_colorBD = 0
        self.m_style = 0
        self.m_point_width = 0
        self.m_back = False
        self.m_selected = False
        self.m_selectable = False
        self.m_zorder = 0
        self.m_hidden = False
        self.m_graph_base = None
        self.m_created = False
        self.m_file_on = file_on
        self.m_file_off = file_off
        self.m_name = aName
        self.m_id = aID
        self.m_subwin = aSubWin
        self.m_graph_base = CGraphBase(self.m_name, self.m_id, self.m_subwin)
    def _q_dtor(self):
        _delete(self.m_graph_base)
    def Create(self):
        self.m_created = False
        if self.m_graph_base.CreateBitmapLabel():
            self.m_created = True
    def SetFileOn(self, value):
        if self.m_created:
            self.m_file_on = value
            self.m_graph_base.SetBmpFileOn(self.m_file_on)
    def SetFileOff(self, value):
        if self.m_created:
            self.m_file_off = value
            self.m_graph_base.SetBmpFileOff(self.m_file_on)
    def SetXDist(self, value):
        if self.m_created:
            self.m_xdist = value
            self.m_graph_base.SetXDistance(self.m_xdist)
    def SetYDist(self, value):
        if self.m_created:
            self.m_ydist = value
            self.m_graph_base.SetYDistance(self.m_ydist)
    def SetXSize(self, value):
        if self.m_created:
            self.m_xsize = value
            self.m_graph_base.SetXSize(self.m_xsize)
    def SetYSize(self, value):
        if self.m_created:
            self.m_ysize = value
            self.m_graph_base.SetYSize(self.m_ysize)
    def SetXOffset(self, value):
        if self.m_created:
            self.m_xoffset = value
            self.m_graph_base.SetXOffset(self.m_xoffset)
    def SetYOffset(self, value):
        if self.m_created:
            self.m_yoffset = value
            self.m_graph_base.SetYOffset(self.m_yoffset)
    def SetState(self, value):
        if self.m_created:
            self.m_state = value
            self.m_graph_base.SetState(self.m_state)
    def SetCorner(self, value):
        if self.m_created:
            self.m_corner = value
            self.m_graph_base.SetColor(self.m_corner)
    def SetAnchor(self, value):
        if self.m_created:
            self.m_anchor = value
            self.m_graph_base.SetAnchor(self.m_anchor)
    def SetColor(self, value):
        if self.m_created:
            self.m_colorBD = value
            self.m_graph_base.SetColor(self.m_colorBD)
    def SetStyle(self, value):
        if self.m_created:
            self.m_style = value
            self.m_graph_base.SetStyle(self.m_style)
    def SetPointWidth(self, value):
        if self.m_created:
            self.m_point_width = value
            self.m_graph_base.SetWidth(self.m_point_width)
    def SetBack(self, value):
        if self.m_created:
            self.m_back = value
            self.m_graph_base.SetBack(self.m_back)
    def SetSelected(self, value):
        if self.m_created:
            self.m_selected = value
            self.m_graph_base.SetSelected(self.m_selected)
    def SetSelectable(self, value):
        if self.m_created:
            self.m_selected = value
            self.m_graph_base.SetSelected(self.m_selected)
    def SetZOrder(self, value):
        if self.m_created:
            self.m_zorder = value
            self.m_graph_base.SetZOrder(self.m_zorder)
    def SetHidden(self, value):
        if self.m_created:
            self.m_hidden = value
            self.m_graph_base.SetHidden(self.m_hidden)
    def GetFileOn(self):
        return self.m_graph_base.BmpFileOn()
    def GetFileOff(self):
        return self.m_graph_base.BmpFileOff()

__all__ = ['CGBitmapLabel']
