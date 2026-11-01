"""carrayring.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class CArrayRing(MqlObject):
    _q_fields = ('m_data', 'm_size', 'm_last_pos', 'm_filling')
    def __init__(self):
        self.m_data = Arr(0, 0.0)
        self.m_size = 0
        self.m_last_pos = 0
        self.m_filling = 0.0
        self.m_last_pos = 0
        self.m_filling = EMPTY_VALUE
        self.m_size = ArraySize(self.m_data)
    def _q_dtor(self):
        ArrayFree(self.m_data)
    def Init(self, size, volue=EMPTY_VALUE):
        self.m_last_pos = 0
        self.m_filling = volue
        self.m_size = ArraySize(self.m_data)
        result = self.Resize(size)
        ArrayFill(self.m_data, 0, self.m_size, self.m_filling)
        return result
    def Size(self):
        return self.m_size - 1
    def Resize(self, new_size):
        if new_size < 0:
            return False
        if new_size > self.m_size:
            set_size = ArrayResize(self.m_data, new_size)
            if set_size < 0:
                return False
            if set_size > self.m_size:
                i = self.m_size - 1
                j = set_size - 1
                while i > self.m_last_pos:
                    self.m_data[j] = self.m_data[i]
                    self.m_data[i] = self.m_filling
                    i -= 1
                    j -= 1
            self.m_size = set_size
            return True
        if new_size > (self.m_last_pos + 1):
            i = self.m_size - 1
            j = new_size - 1
            while j > self.m_last_pos:
                self.m_data[j] = self.m_data[i]
                i -= 1
                j -= 1
        else:
            i = self.m_last_pos + 1 - new_size
            j = 0
            while i <= self.m_last_pos:
                self.m_data[j] = self.m_data[i]
                i += 1
                j += 1
            self.m_last_pos = new_size - 1
        self.m_size = new_size
        ArrayResize(self.m_data, new_size)
        return True
    def Add(self, element):
        self.m_last_pos = _imod(_incattr(self, 'm_last_pos', 1, False), self.m_size)
        self.m_data[self.m_last_pos] = element
    def At(self, index):
        if _idiv(index, self.m_size) == 0:
            return self.m_data[_imod(self.m_size + self.m_last_pos - index, self.m_size)]
        return DBL_MAX
    def __getitem__(self, index):
        return self.At(index)
    def Last_0(self):
        return self.m_data[self.m_last_pos]
    def Last_1(self, element):
        self.m_data[self.m_last_pos] = element
    def Update(self, element, index=0):
        if _idiv(index, self.m_size) == 0:
            self.m_data[_imod(self.m_size + self.m_last_pos - index, self.m_size)] = element
            return True
        return False

__all__ = ['CArrayRing']
