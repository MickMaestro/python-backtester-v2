"""Object.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh


class CObject(MqlObject):
    _q_fields = ('m_prev', 'm_next')
    _q_ptrs = ('m_prev', 'm_next',)
    def __init__(self):
        self.m_prev = None
        self.m_next = None
        self.m_prev = None
        self.m_next = None
    def _q_dtor(self):
        pass
    def Prev_0(self):
        return self.m_prev
    def Prev_1(self, node):
        self.m_prev = node
    def Next_0(self):
        return self.m_next
    def Next_1(self, node):
        self.m_next = node
    def Save(self, file_handle):
        return True
    def Load(self, file_handle):
        return True
    def Type(self):
        return 0
    def Compare(self, node, mode=0):
        return 0

__all__ = ['CObject']
