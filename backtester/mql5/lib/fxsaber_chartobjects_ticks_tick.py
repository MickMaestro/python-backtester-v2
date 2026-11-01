"""Tick.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class TICK(MqlObject):
    _q_fields = ('bid', 'ask', 'time')
    def __init__(self, dBid=0.0, dAsk=0.0):
        self.bid = 0.0
        self.ask = 0.0
        self.time = 0
        self.bid = dBid
        self.ask = dAsk
        self.time = 0
    def GetMin(self):
        return MathMin(self.bid, self.ask)
    def GetMax(self):
        return MathMax(self.bid, self.ask)
    def __gt__(self, Price):
        return self.bid > Price and self.ask > Price
    def __ne__(self, Tick):
        return self.bid != Tick.bid or self.ask != Tick.ask
    def ToString(self):
        return TimeToString(_idiv(self.time, 1000), TIME_DATE | TIME_SECONDS) + '.' + IntegerToString(_imod(self.time, 1000), 3, 48) + ' bid = ' + _str(self.bid) + ' ask = ' + _str(self.ask)

__all__ = ['TICK']
