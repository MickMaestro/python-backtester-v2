"""Pointer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class POINTER(MqlObject):
    _q_fields = ()
    def __init__(self, *args):
        pass
    @staticmethod
    def DeleteObject_1(Pointer):
        if CheckPointer(Pointer) == POINTER_DYNAMIC:
            _delete(Pointer)
        return
    @staticmethod
    def DeleteObject_2(Pointer):
        Size = ArraySize(Pointer)
        for i in range(0, Size):
            POINTER.DeleteObject_1(Pointer[i])
        return
    @staticmethod
    def Swap(Pointer1, Pointer2):
        Tmp = Pointer1
        Pointer1 = Pointer2
        Pointer2 = Tmp
        return

__all__ = ['POINTER']
