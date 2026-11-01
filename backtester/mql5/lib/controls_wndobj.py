"""WndObj.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.controls_wnd import *  # Wnd.mqh
from backtester.mql5.lib.controls_rect import *  # Rect.mqh
from backtester.mql5.lib.controls_defines import *  # Defines.mqh
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh


class CWndObj(CWnd):
    _q_fields = ('m_undeletable', 'm_unchangeable', 'm_unmoveable', 'm_text', 'm_color', 'm_color_background', 'm_color_border', 'm_font', 'm_font_size', 'm_zorder')
    def __init__(self):
        CWnd.__init__(self)
        self.m_undeletable = False
        self.m_unchangeable = False
        self.m_unmoveable = False
        self.m_text = ""
        self.m_color = 0
        self.m_color_background = 0
        self.m_color_border = 0
        self.m_font = ""
        self.m_font_size = 0
        self.m_zorder = 0
        self.m_color = clrNONE
        self.m_color_background = clrNONE
        self.m_color_border = clrNONE
        self.m_font = 'Trebuchet MS'
        self.m_font_size = 10
        self.m_zorder = 0
        self.m_undeletable = True
        self.m_unchangeable = True
        self.m_unmoveable = True
    def _q_dtor(self):
        pass
    def OnEvent(self, id_, lparam, dparam, sparam):
        if self.m_name == sparam:
            _sw1 = id_
            if _sw1 == CHARTEVENT_OBJECT_CREATE:
                return self.OnObjectCreate()
            elif _sw1 == CHARTEVENT_OBJECT_CHANGE:
                return self.OnObjectChange()
            elif _sw1 == CHARTEVENT_OBJECT_DELETE:
                return self.OnObjectDelete()
            elif _sw1 == CHARTEVENT_OBJECT_DRAG:
                return self.OnObjectDrag()
        return CWnd.OnEvent(self, id_, lparam, dparam, sparam)
    def Text_0(self):
        return self.m_text
    def Text_1(self, value):
        self.m_text = value
        return self.OnSetText()
    def Color_0(self):
        return self.m_color
    def Color_1(self, value):
        self.m_color = value
        return self.OnSetColor()
    def ColorBackground_0(self):
        return self.m_color_background
    def ColorBackground_1(self, value):
        self.m_color_background = value
        return self.OnSetColorBackground()
    def ColorBorder_0(self):
        return self.m_color_border
    def ColorBorder_1(self, value):
        self.m_color_border = value
        return self.OnSetColorBorder()
    def Font_0(self):
        return self.m_font
    def Font_1(self, value):
        self.m_font = value
        return self.OnSetFont()
    def FontSize_0(self):
        return self.m_font_size
    def FontSize_1(self, value):
        self.m_font_size = value
        return self.OnSetFontSize()
    def ZOrder_0(self):
        return self.m_zorder
    def ZOrder_1(self, value):
        self.m_zorder = value
        return self.OnSetZOrder()
    def OnObjectCreate(self):
        return True
    def OnObjectChange(self):
        if self.m_unchangeable:
            if not self.OnMove():
                return False
            if not self.OnResize():
                return False
            if not self.OnChange():
                return False
        return True
    def OnObjectDelete(self):
        if self.m_undeletable:
            if not self.OnCreate():
                return False
            if not self.OnChange():
                return False
            return (self.OnShow() if ((self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0) else self.OnHide())
        return True
    def OnObjectDrag(self):
        if self.m_unmoveable:
            return self.OnMove()
        return True
    def OnSetText(self):
        return True
    def OnSetColor(self):
        return True
    def OnSetColorBackground(self):
        return True
    def OnSetColorBorder(self):
        return True
    def OnSetFont(self):
        return True
    def OnSetFontSize(self):
        return True
    def OnSetZOrder(self):
        return True
    def OnDestroy(self):
        return ObjectDelete(self.m_chart_id, self.m_name)
    def OnChange(self):
        if not self.OnSetText():
            return False
        if not self.OnSetFont():
            return False
        if not self.OnSetFontSize():
            return False
        if not self.OnSetColor():
            return False
        if not self.OnSetColorBackground():
            return False
        if not self.OnSetColorBorder():
            return False
        return True

__all__ = ['CWndObj']
