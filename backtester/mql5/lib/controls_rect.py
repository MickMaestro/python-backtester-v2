"""Rect.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class CPoint(MqlObject):
    _q_fields = ('x', 'y')
    def __init__(self, *args):
        self.x = 0
        self.y = 0

class CSize(MqlObject):
    _q_fields = ('cx', 'cy')
    def __init__(self, *args):
        self.cx = 0
        self.cy = 0

class CRect(MqlObject):
    _q_fields = ('left', 'top', 'right', 'bottom')
    def __init__(self, *args):
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0
    def LeftTop_0(self):
        point = CPoint()
        point.x = self.left
        point.y = self.top
        return _copy(point)
    def LeftTop_2(self, x, y):
        self.left = x
        self.top = y
    def LeftTop_1(self, point):
        self.left = point.x
        self.top = point.y
    def RightBottom_0(self):
        point = CPoint()
        point.x = self.right
        point.y = self.bottom
        return _copy(point)
    def RightBottom_2(self, x, y):
        self.right = x
        self.bottom = y
    def RightBottom_1(self, point):
        self.right = point.x
        self.bottom = point.y
    def CenterPoint(self):
        point = CPoint()
        point.x = self.left + _idiv(self.Width_0(), 2)
        point.y = self.top + _idiv(self.Height_0(), 2)
        return _copy(point)
    def Width_0(self):
        return self.right - self.left
    def Width_1(self, w):
        self.right = self.left + w
    def Height_0(self):
        return self.bottom - self.top
    def Height_1(self, h):
        self.bottom = self.top + h
    def Size_0(self):
        size = CSize()
        size.cx = self.right - self.left
        size.cy = self.bottom - self.top
        return _copy(size)
    def Size_2(self, cx, cy):
        self.right = self.left + cx
        self.bottom = self.top + cy
    def Size_1(self, size):
        self.right = self.left + size.cx
        self.bottom = self.top + size.cy
    def SetBound_4(self, l, t, r, b):
        self.left = l
        self.top = t
        self.right = r
        self.bottom = b
    def SetBound_1(self, rect):
        self.left = rect.left
        self.top = rect.top
        self.right = rect.right
        self.bottom = rect.bottom
    def SetBound_3(self, point, size):
        self.LeftTop_1(point)
        self.Size_1(size)
    def SetBound_4(self, left_top, right_bottom):
        self.LeftTop_1(left_top)
        self.RightBottom_1(right_bottom)
    def Move_2(self, x, y):
        self.right += x - self.left
        self.bottom += y - self.top
        self.left = x
        self.top = y
    def Move_1(self, point):
        self.right += point.x - self.left
        self.bottom += point.y - self.top
        self.left = point.x
        self.top = point.y
    def Shift_2(self, dx, dy):
        self.left += dx
        self.top += dy
        self.right += dx
        self.bottom += dy
    def Shift_2(self, point):
        self.left += point.x
        self.top += point.y
        self.right += point.x
        self.bottom += point.y
    def Shift_3(self, size):
        self.left += size.cx
        self.top += size.cy
        self.right += size.cx
        self.bottom += size.cy
    def Contains_2(self, x, y):
        return ((x >= self.left and x <= self.right) and y >= self.top) and y <= self.bottom
    def Contains_1(self, point):
        return ((point.x >= self.left and point.x <= self.right) and point.y >= self.top) and point.y <= self.bottom
    def Normalize(self):
        if self.left > self.right:
            tmp1 = self.left
            self.left = self.right
            self.right = tmp1
        if self.top > self.bottom:
            tmp2 = self.top
            self.top = self.bottom
            self.bottom = tmp2

__all__ = ['CPoint', 'CSize', 'CRect']
