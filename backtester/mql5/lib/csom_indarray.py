"""IndArray.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class IndicatorGetter(MqlObject):
    _q_fields = ('owner', 'cursor')
    _q_ptrs = ('owner',)
    def __init__(self, o):
        self.owner = None
        self.cursor = 0
        self.owner = o
    def __getitem__(self, b):
        return self.owner[_uint(b)]

class Indicator(MqlObject):
    _q_fields = ('buffer', 'cursor', 'instance')
    _q_ptrs = ('instance',)
    def __init__(self, i):
        self.buffer = Arr(0, 0.0)
        self.cursor = 0
        self.instance = None
        SetIndexBuffer(i, self.buffer)
        ArraySetAsSeries(self.buffer, True)
        ArrayInitialize(self.buffer, EMPTY_VALUE)
        self.instance = IndicatorGetter(self)
    def _q_dtor(self):
        _delete(self.instance)
    def __getitem__(self, b):
        return self.buffer[b]
    def __getitem__(self, b):
        self.cursor = b
        return self
    def _q_assign(self, x):
        self.buffer[self.cursor] = x
        return x
    def edit(self):
        return self.instance
    def __add__(self, x):
        return self.buffer[self.cursor] + x
    def __sub__(self, x):
        return self.buffer[self.cursor] - x
    def __mul__(self, x):
        return self.buffer[self.cursor] * x
    def __truediv__(self, x):
        return _fdiv(self.buffer[self.cursor], x)
    def __iadd__(self, x):
        self.buffer[self.cursor] += x
        return self.buffer[self.cursor]
    def __isub__(self, x):
        self.buffer[self.cursor] -= x
        return self.buffer[self.cursor]
    def __imul__(self, x):
        self.buffer[self.cursor] *= x
        return self.buffer[self.cursor]
    def __itruediv__(self, x):
        self.buffer[self.cursor] = _fdiv(self.buffer[self.cursor], x)
        return self.buffer[self.cursor]

class IndicatorArray(MqlObject):
    _q_fields = ('array',)
    _q_ptrs = ('array',)
    def __init__(self, n):
        self.array = Arr(0, None)
        ArrayResize(self.array, n)
        for i in range(0, n):
            self.array[i] = Indicator(i)
    def _q_dtor(self):
        n = ArraySize(self.array)
        for i in range(0, n):
            if CheckPointer(self.array[i]) == POINTER_DYNAMIC:
                _delete(self.array[i])
        ArrayResize(self.array, 0)
    def __getitem__(self, n):
        return self.array[n]
    def size(self):
        return ArraySize(self.array)

class IndicatorArrayGetter(MqlObject):
    _q_fields = ('array',)
    _q_ptrs = ('array',)
    def _q_ctor1(self):
        self.array = Arr(0, None)
    def _q_ctor2(self, a):
        self.array = Arr(0, None)
        self.bind(a)
    def __init__(self, *args):
        if 0 <= len(args) <= 0:
            self._q_ctor1(*args)
            return
        if 1 <= len(args) <= 1 and (len(args) == 0 or isinstance(args[0], MqlObject)):
            self._q_ctor2(*args)
            return
        self._q_ctor1(*args)
    def _q_dtor(self):
        ArrayResize(self.array, 0)
    def bind(self, a):
        n = a.size()
        ArrayResize(self.array, n)
        for i in range(0, n):
            self.array[i] = a[i].edit()
    def __getitem__(self, n):
        return self.array[n]

__all__ = ['IndicatorGetter', 'Indicator', 'IndicatorArray', 'IndicatorArrayGetter']
