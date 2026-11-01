"""Wnd.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.controls_rect import *  # Rect.mqh
from backtester.mql5.lib.controls_defines import *  # Defines.mqh
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh


class CWnd(CObject):
    _q_fields = ('m_chart_id', 'm_subwin', 'm_name', 'm_rect', 'm_id', 'm_state_flags', 'm_prop_flags', 'm_align_flags', 'm_align_left', 'm_align_top', 'm_align_right', 'm_align_bottom', 'm_mouse_x', 'm_mouse_y', 'm_mouse_flags', 'm_last_click', 'm_drag_object')
    _q_ptrs = ('m_drag_object',)
    def __init__(self):
        CObject.__init__(self)
        self.m_chart_id = 0
        self.m_subwin = 0
        self.m_name = ""
        self.m_rect = CRect()
        self.m_id = 0
        self.m_state_flags = 0
        self.m_prop_flags = 0
        self.m_align_flags = 0
        self.m_align_left = 0
        self.m_align_top = 0
        self.m_align_right = 0
        self.m_align_bottom = 0
        self.m_mouse_x = 0
        self.m_mouse_y = 0
        self.m_mouse_flags = 0
        self.m_last_click = 0
        self.m_drag_object = None
        self.m_chart_id = -1
        self.m_subwin = -1
        self.m_name = ""
        self.m_id = -1
        self.m_state_flags = WND_STATE_FLAG_ENABLE + WND_STATE_FLAG_VISIBLE
        self.m_prop_flags = 0
        self.m_align_flags = WND_ALIGN_NONE
        self.m_align_left = 0
        self.m_align_top = 0
        self.m_align_right = 0
        self.m_align_bottom = 0
        self.m_mouse_x = 0
        self.m_mouse_y = 0
        self.m_mouse_flags = MOUSE_INVALID_FLAGS
        self.m_last_click = 0
        self.m_drag_object = None
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        self.m_chart_id = chart
        self.m_name = name
        self.m_subwin = subwin
        self.Left_1(x1)
        self.Top_1(y1)
        self.Right_1(x2)
        self.Bottom_1(y2)
        return True
    def Destroy(self, reason=0):
        if self.OnDestroy():
            self.m_name = ''
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ != CHARTEVENT_MOUSE_MOVE:
            return False
        if not ((self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0):
            return False
        x = _int(lparam)
        y = _int(dparam)
        flags = _int(StringToInteger(sparam))
        if self.m_drag_object is not None:
            return self.m_drag_object.OnMouseEvent(x, y, flags)
        return self.OnMouseEvent(x, y, flags)
    def OnMouseEvent(self, x, y, flags):
        if not self.Contains_2(x, y):
            if (self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0:
                self.m_mouse_x = 0
                self.m_mouse_y = 0
                self.m_mouse_flags = MOUSE_INVALID_FLAGS
                self.Deactivate()
            return False
        if (flags & MOUSE_LEFT) != 0:
            if self.m_mouse_flags == MOUSE_INVALID_FLAGS:
                if not ((self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0):
                    EventChartCustom(-1, 9, self.m_id, 0.0, self.m_name)
                    return self.Activate()
                return True
            if (self.m_mouse_flags & MOUSE_LEFT) != 0:
                if (self.m_prop_flags & WND_PROP_FLAG_CAN_DRAG) != 0:
                    return self.OnDragProcess(x, y)
                if (self.m_prop_flags & WND_PROP_FLAG_CLICKS_BY_PRESS) != 0:
                    EventChartCustom(-1, 0, self.m_id, 0.0, self.m_name)
                    return True
            else:
                self.m_mouse_flags = flags
                self.m_mouse_x = x
                self.m_mouse_y = y
                return self.OnMouseDown()
        else:
            if self.m_mouse_flags == MOUSE_INVALID_FLAGS:
                self.m_mouse_flags = flags
                EventChartCustom(-1, 9, self.m_id, 0.0, self.m_name)
                return self.Activate()
            if (self.m_mouse_flags & MOUSE_LEFT) != 0:
                self.m_mouse_flags = flags
                self.m_mouse_x = x
                self.m_mouse_y = y
                return self.OnMouseUp()
        return True
    def Name(self):
        return self.m_name
    def ControlsTotal(self):
        return 0
    def Control(self, ind):
        return None
    def ControlFind(self, id_):
        result = None
        if id_ == self.m_id:
            result = self
        return result
    def Rect(self):
        return _copy(self.m_rect)
    def Left_0(self):
        return self.m_rect.left
    def Left_1(self, x):
        self.m_rect.left = x
    def Top_0(self):
        return self.m_rect.top
    def Top_1(self, y):
        self.m_rect.top = y
    def Right_0(self):
        return self.m_rect.right
    def Right_1(self, x):
        self.m_rect.right = x
    def Bottom_0(self):
        return self.m_rect.bottom
    def Bottom_1(self, y):
        self.m_rect.bottom = y
    def Width_0(self):
        return self.m_rect.Width_0()
    def Width_1(self, w):
        self.m_rect.Width_1(w)
        return self.OnResize()
    def Height_0(self):
        return self.m_rect.Height_0()
    def Height_1(self, h):
        self.m_rect.Height_1(h)
        return self.OnResize()
    def Size_0(self):
        return self.m_rect.Size_0()
    def Size_2(self, w, h):
        self.m_rect.Size_2(w, h)
        return self.OnResize()
    def Size_1(self, size):
        self.m_rect.Size_1(size)
        return self.OnResize()
    def Move_2(self, x, y):
        self.m_rect.Move_2(x, y)
        return self.OnMove()
    def Move_1(self, point):
        self.m_rect.Move_1(point)
        return self.OnMove()
    def Shift(self, dx, dy):
        self.m_rect.Shift_2(dx, dy)
        return self.OnMove()
    def Contains_2(self, x, y):
        return self.m_rect.Contains_2(x, y)
    def Contains_1(self, control):
        if control is None:
            return False
        return self.Contains_2(control.Left_0(), control.Top_0()) and self.Contains_2(control.Right_0(), control.Bottom_0())
    def Alignment(self, flags, left, top, right, bottom):
        self.m_align_flags = flags
        self.m_align_left = left
        self.m_align_top = top
        self.m_align_right = right
        self.m_align_bottom = bottom
    def Align(self, rect):
        new_value = 0
        if self.m_align_flags == WND_ALIGN_NONE:
            return True
        if (self.m_align_flags & WND_ALIGN_RIGHT) != 0:
            if (self.m_align_flags & WND_ALIGN_LEFT) != 0:
                new_value = rect.Width_0() - self.m_align_left - self.m_align_right
                if not self.Size_2(new_value, self.Height_0()):
                    return False
            else:
                new_value = rect.right - self.Width_0() - self.m_align_right
                if not self.Move_2(new_value, self.Top_0()):
                    return False
        if (self.m_align_flags & WND_ALIGN_BOTTOM) != 0:
            if (self.m_align_flags & WND_ALIGN_TOP) != 0:
                new_value = rect.Height_0() - self.m_align_top - self.m_align_bottom
                if not self.Size_2(self.Width_0(), new_value):
                    return False
            else:
                new_value = rect.bottom - self.Height_0() - self.m_align_bottom
                if not self.Move_2(self.Left_0(), new_value):
                    return False
        return True
    def Id_1(self, id_):
        self.m_id = id_
        return 1
    def Id_0(self):
        return self.m_id
    def IsEnabled(self):
        return (self.m_state_flags & WND_STATE_FLAG_ENABLE) != 0
    def Enable(self):
        if (self.m_state_flags & WND_STATE_FLAG_ENABLE) != 0:
            return True
        self.StateFlagsSet(WND_STATE_FLAG_ENABLE)
        return self.OnEnable()
    def Disable(self):
        if not ((self.m_state_flags & WND_STATE_FLAG_ENABLE) != 0):
            return True
        self.StateFlagsReset(WND_STATE_FLAG_ENABLE)
        return self.OnDisable()
    def IsVisible(self):
        return (self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0
    def Visible(self, flag):
        if ((self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0) == flag:
            return True
        return (self.Show() if flag else self.Hide())
    def Show(self):
        self.StateFlagsSet(WND_STATE_FLAG_VISIBLE)
        return self.OnShow()
    def Hide(self):
        self.StateFlagsReset(WND_STATE_FLAG_VISIBLE)
        return self.OnHide()
    def IsActive(self):
        return (self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0
    def Activate(self):
        if (self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0:
            return True
        self.StateFlagsSet(WND_STATE_FLAG_ACTIVE)
        return self.OnActivate()
    def Deactivate(self):
        if not ((self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0):
            return True
        self.StateFlagsReset(WND_STATE_FLAG_ACTIVE)
        return self.OnDeactivate()
    def StateFlags_0(self):
        return self.m_state_flags
    def StateFlags_1(self, flags):
        self.m_state_flags = flags
    def StateFlagsSet(self, flags):
        self.m_state_flags |= flags
    def StateFlagsReset(self, flags):
        self.m_state_flags &= ~flags
    def PropFlags_0(self):
        return self.m_prop_flags
    def PropFlags_1(self, flags):
        self.m_prop_flags = flags
    def PropFlagsSet(self, flags):
        self.m_prop_flags |= flags
    def PropFlagsReset(self, flags):
        self.m_prop_flags &= ~flags
    def MouseX_0(self):
        return self.m_mouse_x
    def MouseX_1(self, value):
        self.m_mouse_x = value
    def MouseY_0(self):
        return self.m_mouse_y
    def MouseY_1(self, value):
        self.m_mouse_y = value
    def MouseFlags_0(self):
        return self.m_mouse_flags
    def MouseFlags_1(self, value):
        self.m_mouse_flags = value
    def MouseFocusKill(self, id_=-1):
        if id_ == self.m_id:
            return False
        self.Deactivate()
        self.m_mouse_x = 0
        self.m_mouse_y = 0
        self.m_mouse_flags = MOUSE_INVALID_FLAGS
        return self.OnDeactivate()
    def BringToTop(self):
        EventChartCustom(-1, 14, self.m_id, 0.0, self.m_name)
        return True
    def OnCreate(self):
        return True
    def OnDestroy(self):
        return True
    def OnMove(self):
        return True
    def OnResize(self):
        return True
    def OnEnable(self):
        return True
    def OnDisable(self):
        return True
    def OnShow(self):
        return True
    def OnHide(self):
        return True
    def OnActivate(self):
        return True
    def OnDeactivate(self):
        return True
    def OnClick(self):
        EventChartCustom(-1, 0, self.m_id, 0.0, self.m_name)
        return True
    def OnDblClick(self):
        EventChartCustom(-1, 1, self.m_id, 0.0, self.m_name)
        return True
    def OnChange(self):
        return True
    def OnMouseDown(self):
        if (self.m_prop_flags & WND_PROP_FLAG_CAN_DRAG) != 0:
            return self.OnDragStart()
        if (self.m_prop_flags & WND_PROP_FLAG_CLICKS_BY_PRESS) != 0:
            return self.OnClick()
        return True
    def OnMouseUp(self):
        if (self.m_prop_flags & WND_PROP_FLAG_CAN_DBL_CLICK) != 0:
            last_time = GetTickCount()
            if self.m_last_click == 0 or (last_time - self.m_last_click) > 100:
                self.m_last_click = (1 if (last_time == 0) else last_time)
            else:
                self.m_last_click = 0
                return self.OnDblClick()
        if (self.m_prop_flags & WND_PROP_FLAG_CAN_DRAG) != 0:
            return self.OnDragEnd()
        if not ((self.m_prop_flags & WND_PROP_FLAG_CLICKS_BY_PRESS) != 0):
            return self.OnClick()
        return True
    def OnDragStart(self):
        if not ((self.m_prop_flags & WND_PROP_FLAG_CAN_DRAG) != 0):
            return True
        ChartSetInteger(self.m_chart_id, CHART_MOUSE_SCROLL, False)
        EventChartCustom(-1, 11, self.m_id, 0.0, self.m_name)
        return True
    def OnDragProcess(self, x, y):
        self.Shift(x - self.m_mouse_x, y - self.m_mouse_y)
        self.m_mouse_x = x
        self.m_mouse_y = y
        return True
    def OnDragEnd(self):
        if not ((self.m_prop_flags & WND_PROP_FLAG_CAN_DRAG) != 0):
            return True
        ChartSetInteger(self.m_chart_id, CHART_MOUSE_SCROLL, True)
        EventChartCustom(-1, 13, self.m_id, 0.0, self.m_name)
        return True
    def DragObjectCreate(self):
        return False
    def DragObjectDestroy(self):
        if self.m_drag_object is not None:
            _delete(self.m_drag_object)
            self.m_drag_object = None
        return True

class CDragWnd(CWnd):
    _q_fields = ('m_limit_left', 'm_limit_top', 'm_limit_right', 'm_limit_bottom')
    def __init__(self):
        CWnd.__init__(self)
        self.m_limit_left = 0
        self.m_limit_top = 0
        self.m_limit_right = 0
        self.m_limit_bottom = 0
    def _q_dtor(self):
        pass
    def Limits(self, l, t, r, b):
        self.m_limit_left = l
        self.m_limit_top = t
        self.m_limit_right = r
        self.m_limit_bottom = b
    def OnDragProcess(self, x, y):
        dx = x - self.m_mouse_x
        dy = y - self.m_mouse_y
        if (self.Right_0() + dx) > self.m_limit_right:
            dx = self.m_limit_right - self.Right_0()
        if (self.Left_0() + dx) < self.m_limit_left:
            dx = self.m_limit_left - self.Left_0()
        if (self.Bottom_0() + dy) > self.m_limit_bottom:
            dy = self.m_limit_bottom - self.Bottom_0()
        if (self.Top_0() + dy) < self.m_limit_top:
            dy = self.m_limit_top - self.Top_0()
        self.Shift(dx, dy)
        self.m_mouse_x = x
        self.m_mouse_y = y
        EventChartCustom(-1, 12, self.m_id, 0.0, self.m_name)
        return True

__all__ = ['CWnd', 'CDragWnd']
