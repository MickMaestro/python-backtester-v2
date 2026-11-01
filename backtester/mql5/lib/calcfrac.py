"""calcfrac.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class CalcFrac(MqlObject):
    _q_fields = ('before_period', 'after_period', 'values')
    def __init__(self, *args):
        self.before_period = 0
        self.after_period = 0
        self.values = Arr(0, 0.0)
    def is_lower_fr(self, bar):
        i = 1
        while i <= self.CountMax():
            if i <= self.after_period and self.values[bar] > self.values[bar + i]:
                return False
            if i <= self.before_period and self.values[bar] > self.values[bar - i]:
                return False
            i += 1
        return True
    def is_upper_fr(self, bar):
        i = 1
        while i <= self.CountMax():
            if i <= self.after_period and self.values[bar] < self.values[bar + i]:
                return False
            if i <= self.before_period and self.values[bar] < self.values[bar - i]:
                return False
            i += 1
        return True
    def CountMax(self):
        return MathMax(self.before_period, self.after_period)

__all__ = ['CalcFrac']
