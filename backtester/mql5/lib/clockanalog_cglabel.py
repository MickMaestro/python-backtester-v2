"""CGLabel.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.clockanalog_cgraphbase import *  # CGraphBase.mqh


class CGLabel(MqlObject):
    _q_fields = ('m_name', 'm_id', 'm_subwin', 'm_created', 'm_xdist', 'm_ydist', 'm_color_fg', 'm_text', 'm_corner', 'm_anchor', 'm_angle', 'm_fontname', 'm_fontsize', 'm_selected', 'm_selectable', 'm_back', 'm_zorder', 'm_hidden', 'm_graph_base')
    _q_ptrs = ('m_graph_base',)
    def __init__(self, aName='Label_', aID=0, aSubWin=0):
        self.m_name = ""
        self.m_id = 0
        self.m_subwin = 0
        self.m_created = False
        self.m_xdist = 0
        self.m_ydist = 0
        self.m_color_fg = 0
        self.m_text = ""
        self.m_corner = 0
        self.m_anchor = 0
        self.m_angle = 0.0
        self.m_fontname = ""
        self.m_fontsize = 0
        self.m_selected = False
        self.m_selectable = False
        self.m_back = False
        self.m_zorder = 0
        self.m_hidden = False
        self.m_graph_base = None
        self.m_created = False
        self.m_name = aName
        self.m_id = aID
        self.m_subwin = aSubWin
        self.m_graph_base = CGraphBase(self.m_name, self.m_id, self.m_subwin)
    def _q_dtor(self):
        _delete(self.m_graph_base)
    def Create(self):
        self.m_created = False
        if self.m_graph_base.CreateLabel():
            self.m_created = True
    def SetXDist(self, aDist=10):
        if self.m_created:
            self.m_xdist = aDist
            self.m_graph_base.SetXDistance(self.m_xdist)
    def SetYDist(self, aDist=15):
        if self.m_created:
            self.m_ydist = aDist
            self.m_graph_base.SetYDistance(self.m_ydist)
    def SetColorText(self, aColor=65535):
        if self.m_created:
            self.m_color_fg = aColor
            self.m_graph_base.SetColor(self.m_color_fg)
    def SetText(self, aText='LABEL_'):
        if self.m_created:
            self.m_text = aText
            self.m_graph_base.SetText(self.m_text)
    def SetCorner(self, aCorner=0):
        if self.m_created:
            self.m_corner = aCorner
            self.m_graph_base.SetCorner(self.m_corner)
    def SetAnchor(self, anAnchor=0):
        if self.m_created:
            self.m_anchor = anAnchor
            self.m_graph_base.SetAnchor(self.m_anchor)
    def SetAngle(self, anAngle=0.0):
        if self.m_created:
            self.m_angle = anAngle
            self.m_graph_base.SetAngle(self.m_angle)
    def SetFontName(self, aFont='Calibri'):
        if self.m_created:
            self.m_fontname = aFont
            self.m_graph_base.SetFont(self.m_fontname)
    def SetFontSize(self, aSize=8):
        if self.m_created:
            self.m_fontsize = aSize
            self.m_graph_base.SetFontSize(self.m_fontsize)
    def SetSelected(self, aValue=False):
        if self.m_created:
            self.m_selected = aValue
            self.m_graph_base.SetSelected(self.m_selected)
    def SetSelectable(self, aValue=False):
        if self.m_created:
            self.m_selectable = aValue
            self.m_graph_base.SetSelectable(self.m_selectable)
    def SetBack(self, aBack=False):
        if self.m_created:
            self.m_back = aBack
            self.m_graph_base.SetBack(self.m_back)
    def SetZOrder(self, aOrder=0):
        if self.m_created:
            self.m_zorder = aOrder
            self.m_graph_base.SetZOrder(self.m_zorder)
    def SetHidden(self, aHidden=True):
        if self.m_created:
            self.m_hidden = aHidden
            self.m_graph_base.SetHidden(self.m_hidden)
    def MoveXY(self, aPosX=0, aPosY=0):
        ResetLastError()
        if not self.m_graph_base.SetXDistance(aPosX):
            Print('CGLabel::MoveXY', ': Cannot move to X! Error code:', GetLastError())
            return False
        if not self.m_graph_base.SetYDistance(aPosY):
            Print('CGLabel::MoveXY', ': Cannot move to Y! Error code:', GetLastError())
            return False
        self.m_xdist = aPosX
        self.m_ydist = aPosY
        return True
    def MoveX(self, aPosX=0):
        ResetLastError()
        if not self.m_graph_base.SetXDistance(aPosX):
            Print('CGLabel::MoveX', ': Cannot move to X! Error code:', GetLastError())
            return False
        self.m_xdist = aPosX
        return True
    def MoveY(self, aPosY=0):
        ResetLastError()
        if not self.m_graph_base.SetYDistance(aPosY):
            Print('CGLabel::MoveY', ': Cannot move to Y! Error code:', GetLastError())
            return False
        self.m_ydist = aPosY
        return True
    def Name(self):
        return self.m_name
    def XDist(self):
        return self.m_xdist
    def YDist(self):
        return self.m_ydist
    def ColorText(self):
        return self.m_color_fg
    def Text(self):
        return self.m_text
    def Corner(self):
        return self.m_corner
    def Anchor(self):
        return self.m_anchor
    def Angle(self):
        return self.m_angle
    def FontName(self):
        return self.m_fontname
    def FontSize(self):
        return self.m_fontsize
    def Selected(self):
        return self.m_selected
    def Selectable(self):
        return self.m_selectable
    def Back(self):
        return self.m_back
    def ZOrder(self):
        return self.m_zorder
    def Hidden(self, aHidden=True):
        return self.m_hidden
    def PtrGraphBase(self):
        return self.m_graph_base
    def Created(self):
        return self.m_created
    def ReDraw(self):
        self.m_graph_base.Redraw()

__all__ = ['CGLabel']
