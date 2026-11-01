"""HPFMatchProcessor.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class PATTERN_MATCH(MqlObject):
    _q_fields = ('bullish', 'XIndex', 'AIndex', 'BIndex', 'CIndex', 'DIndex', 'X', 'A', 'B', 'C', 'nearD', 'farD')
    def _q_ctor1(self):
        self.bullish = False
        self.XIndex = 0
        self.AIndex = 0
        self.BIndex = 0
        self.CIndex = 0
        self.DIndex = 0
        self.X = 0.0
        self.A = 0.0
        self.B = 0.0
        self.C = 0.0
        self.nearD = 0.0
        self.farD = 0.0
    def _q_ctor2(self, other):
        self.bullish = False
        self.XIndex = 0
        self.AIndex = 0
        self.BIndex = 0
        self.CIndex = 0
        self.DIndex = 0
        self.X = 0.0
        self.A = 0.0
        self.B = 0.0
        self.C = 0.0
        self.nearD = 0.0
        self.farD = 0.0
        self.bullish = other.bullish
        self.XIndex = other.XIndex
        self.AIndex = other.AIndex
        self.BIndex = other.BIndex
        self.CIndex = other.CIndex
        self.DIndex = other.DIndex
        self.X = other.X
        self.A = other.A
        self.B = other.B
        self.C = other.C
        self.nearD = other.nearD
        self.farD = other.farD
    def __init__(self, *args):
        if 0 <= len(args) <= 0:
            self._q_ctor1(*args)
            return
        if 1 <= len(args) <= 1 and (len(args) == 0 or isinstance(args[0], MqlObject)):
            self._q_ctor2(*args)
            return
        self._q_ctor1(*args)

class CHPFMatchProcessor(MqlObject):
    _q_fields = ()
    def __init__(self, *args):
        pass
    def PatternUndershot(self, match):
        pass
    def PatternMatched(self, match):
        pass
    def PatternOvershot(self, match):
        pass

__all__ = ['PATTERN_MATCH', 'CHPFMatchProcessor']
