"""CGButton.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.clockanalog_cgraphbase import *  # CGraphBase.mqh


class CGButton(MqlObject):
    _q_fields = ('m_name', 'm_id', 'm_subwin', 'm_created', 'm_xdist', 'm_ydist', 'm_xsize', 'm_ysize', 'm_color_fg', 'm_color_bg', 'm_color_bd', 'm_text', 'm_char', 'm_corner', 'm_fontname', 'm_state', 'm_fontsize', 'm_selected', 'm_selectable', 'm_back', 'm_readonly', 'm_zorder', 'm_hidden', 'm_graph_base')
    _q_ptrs = ('m_graph_base',)
    def __init__(self, aName='Button_', aID=0, aSubWin=0):
        self.m_name = ""
        self.m_id = 0
        self.m_subwin = 0
        self.m_created = False
        self.m_xdist = 0
        self.m_ydist = 0
        self.m_xsize = 0
        self.m_ysize = 0
        self.m_color_fg = 0
        self.m_color_bg = 0
        self.m_color_bd = 0
        self.m_text = ""
        self.m_char = 0
        self.m_corner = 0
        self.m_fontname = ""
        self.m_state = False
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
        self.m_graph_base = CGraphBase(self.m_name, self.m_id, self.m_subwin)
    def _q_dtor(self):
        _delete(self.m_graph_base)
    def Create(self):
        self.m_created = False
        if self.m_graph_base.CreateButton():
            self.m_created = True
    def SetXDist(self, aDist=10):
        if self.m_created:
            self.m_xdist = aDist
            self.m_graph_base.SetXDistance(self.m_xdist)
    def SetYDist(self, aDist=15):
        if self.m_created:
            self.m_ydist = aDist
            self.m_graph_base.SetYDistance(self.m_ydist)
    def SetXSize(self, aSize=10):
        if self.m_created:
            self.m_xsize = aSize
            self.m_graph_base.SetXSize(self.m_xsize)
    def SetYSize(self, aSize=10):
        if self.m_created:
            self.m_ysize = aSize
            self.m_graph_base.SetYSize(self.m_ysize)
    def SetBack(self, aBack=False):
        if self.m_created:
            self.m_back = aBack
            self.m_graph_base.SetBack(self.m_back)
    def SetState(self, aState=True):
        if self.m_created:
            self.m_state = aState
            self.m_graph_base.SetState(self.m_state)
    def SetChar(self, aChar=73):
        if self.m_created:
            self.m_char = aChar
            self.m_graph_base.SetText(CharToString(self.m_char))
    def SetText(self, aText=''):
        if self.m_created:
            self.m_text = aText
            self.m_graph_base.SetText(self.m_text)
    def SetColorFG(self, aColor=clrWhite):
        if self.m_created:
            self.m_color_fg = aColor
            self.m_graph_base.SetColor(self.m_color_fg)
    def SetColorBG(self, aColor=clrFireBrick):
        if self.m_created:
            self.m_color_bg = aColor
            self.m_graph_base.SetBgColor(self.m_color_bg)
    def SetColorBD(self, aColor=clrSnow):
        if self.m_created:
            self.m_color_bd = aColor
            self.m_graph_base.SetBorderColor(self.m_color_bd)
    def SetCorner(self, aCorner=0):
        if self.m_created:
            self.m_corner = aCorner
            self.m_graph_base.SetCorner(self.m_corner)
    def SetFontName(self, aFont='Windings'):
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
    def SetHidden(self, aValue=True):
        if self.m_created:
            self.m_hidden = aValue
            self.m_graph_base.SetHidden(self.m_hidden)
    def NameObj(self):
        return self.m_name
    def State(self):
        return self.m_graph_base.State()
    def XDistance(self):
        return self.m_xdist
    def YDistance(self):
        return self.m_ydist
    def PtrGraphBase(self):
        return self.m_graph_base

__all__ = ['CGButton']
