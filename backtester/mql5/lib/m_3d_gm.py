"""GM.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class CGM(MqlObject):
    _q_fields = ('m_name',)
    def __init__(self):
        self.m_name = ""
    def _q_dtor(self):
        pass
    def Create(self, name):
        self.m_name = name
    def R_OBJPROP_PRICE(self, prop_modifier=0):
        return ObjectGetDouble(0, self.m_name, OBJPROP_PRICE, prop_modifier)
    def R_OBJPROP_TIME(self, prop_modifier=0):
        return ObjectGetInteger(0, self.m_name, OBJPROP_TIME, prop_modifier)
    def R_OBJPROP_ANGLE(self):
        return ObjectGetDouble(0, self.m_name, OBJPROP_ANGLE)
    def R_OBJPROP_TEXT(self):
        return ObjectGetString(0, self.m_name, OBJPROP_TEXT)
    def R_ValueByTime(self, time):
        return ObjectGetValueByTime(0, self.m_name, time)
    def W_OBJPROP_TEXT(self, text):
        ObjectSetString(0, self.m_name, OBJPROP_TEXT, text)

__all__ = ['CGM']
