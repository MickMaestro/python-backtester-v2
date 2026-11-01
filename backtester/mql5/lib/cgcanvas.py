"""CGCanvas.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.cgraphbase import *  # CGraphBase.mqh


class CGCanvas(MqlObject):
    _q_fields = ('m_name', 'm_id', 'm_subwin', 'm_created', 'm_xdist', 'm_ydist', 'm_xsize', 'm_ysize', 'm_color_bg', 'm_color_bd', 'm_corner', 'm_fontname', 'm_fontsize', 'm_selected', 'm_selectable', 'm_back', 'm_readonly', 'm_zorder', 'm_hidden', 'm_graph_base')
    _q_ptrs = ('m_graph_base',)
    def __init__(self, aName='Canvas_', aID=0, aSubWin=0):
        self.m_name = ""
        self.m_id = 0
        self.m_subwin = 0
        self.m_created = False
        self.m_xdist = 0
        self.m_ydist = 0
        self.m_xsize = 0
        self.m_ysize = 0
        self.m_color_bg = 0
        self.m_color_bd = 0
        self.m_corner = 0
        self.m_fontname = ""
        self.m_fontsize = 0
        self.m_selected = False
        self.m_selectable = False
        self.m_back = False
        self.m_readonly = False
        self.m_zorder = 0
        self.m_hidden = False
        self.m_graph_base = None
        self.m_name = aName
        self.m_id = aID
        self.m_subwin = aSubWin
        self.m_created = False
        self.m_graph_base = CGraphBase(self.m_name, self.m_id, self.m_subwin)
        if self.m_graph_base.CreateEdit():
            self.m_created = True
    def _q_dtor(self):
        self.Deinit()
    def SetXDist(self, aDist=10):
        if self.m_created:
            self.m_xdist = aDist
            self.m_graph_base.SetXDistance(self.m_xdist)
    def SetYDist(self, aDist=15):
        if self.m_created:
            self.m_ydist = aDist
            self.m_graph_base.SetYDistance(self.m_ydist)
    def SetXSize(self, aWidth=100):
        if self.m_created:
            self.m_xsize = aWidth
            self.m_graph_base.SetXSize(self.m_xsize)
    def SetYSize(self, aHeight=100):
        if self.m_created:
            self.m_ysize = aHeight
            self.m_graph_base.SetYSize(self.m_ysize)
    def SetColorBG(self, aColor=5197615):
        if self.m_created:
            self.m_color_bg = aColor
            self.m_graph_base.SetBgColor(self.m_color_bg)
    def SetColorBorder(self, aColor=16448255):
        if self.m_created:
            self.m_color_bd = aColor
            self.m_graph_base.SetBorderColor(self.m_color_bd)
    def SetCorner(self, aCorner=0):
        if self.m_created:
            self.m_corner = aCorner
            self.m_graph_base.SetCorner(self.m_corner)
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
    def SetReadOnly(self, aValue=True):
        if self.m_created:
            self.m_readonly = aValue
            self.m_graph_base.SetReadOnly(self.m_readonly)
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
            Print('CGCanvas::MoveXY', ': Cannot move to X! Error code:', GetLastError())
            return False
        if not self.m_graph_base.SetYDistance(aPosY):
            Print('CGCanvas::MoveXY', ': Cannot move to Y! Error code:', GetLastError())
            return False
        self.m_xdist = aPosX
        self.m_ydist = aPosY
        return True
    def MoveX(self, aPosX=0):
        ResetLastError()
        if not self.m_graph_base.SetXDistance(aPosX):
            Print('CGCanvas::MoveX', ': Cannot move to X! Error code:', GetLastError())
            return False
        self.m_xdist = aPosX
        return True
    def MoveY(self, aPosY=0):
        ResetLastError()
        if not self.m_graph_base.SetYDistance(aPosY):
            Print('CGCanvas::MoveY', ': Cannot move to Y! Error code:', GetLastError())
            return False
        self.m_ydist = aPosY
        return True
    def PtrGraphBase(self):
        return self.m_graph_base
    def Init(self):
        pass
    def Deinit(self):
        self.m_graph_base.Delete()
        _delete(self.m_graph_base)
    def ReDraw(self):
        self.m_graph_base.Redraw()
    def Name(self):
        return self.m_graph_base.Name()
    def Chart_ID(self):
        return self.m_graph_base.Chart_ID()
    def SubWindow(self):
        return self.m_graph_base.SubWindow()
    def Created(self):
        return self.m_created

__all__ = ['CGCanvas']
