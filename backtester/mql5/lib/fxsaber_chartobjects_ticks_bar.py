"""Bar.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.fxsaber_chartobjects_ticks_tick import *  # Tick.mqh


class BAR(MqlObject):
    _q_fields = ('Ticks', 'Amount', 'time')
    def __init__(self, dTime):
        self.Ticks = Arr(0, 0, factory=TICK)
        self.Amount = 0
        self.time = 0
        self.time = dTime
        self.Amount = 0
    def Add(self, Tick):
        _assign(self.Ticks[self.Amount], Tick)
        self.Amount += 1
        return
    def AddData(self, TmpTick, Source, Pos, iAmount):
        Size = (ArrayResize(self.Ticks, iAmount + 1) if (self.Amount == 0) else ArrayResize(self.Ticks, iAmount + self.Amount))
        if (self.Amount == 0 and Size > 0) and TmpTick > 0:
            if iAmount > 0 and Source[Pos].time_msc > (self.time * 1000):
                TmpTick.time = self.time * 1000
                self.Add(TmpTick)
        i = 0
        while i < iAmount and self.Amount < Size:
            Tick = _copy(Source[Pos])
            if Tick.bid != 0 or Tick.ask != 0:
                NewTmpTick = TICK((TmpTick.bid if (Tick.bid == 0) else Tick.bid), (TmpTick.ask if (Tick.ask == 0) else Tick.ask))
                if NewTmpTick != TmpTick and NewTmpTick > 0:
                    _assign(TmpTick, NewTmpTick)
                    TmpTick.time = Tick.time_msc
                    self.Add(TmpTick)
            Pos += 1
            i += 1
        self.Amount = ArrayResize(self.Ticks, self.Amount)
    def __getitem__(self, Pos):
        return _copy(self.Ticks[Pos])
    def GetAmount(self):
        return self.Amount
    def GetMax(self):
        Res = DBL_MIN
        i = 0
        while i < self.Amount:
            Tick = _copy(self.Ticks[i])
            if Tick.ask > Res:
                Res = Tick.ask
            if Tick.bid > Res:
                Res = Tick.bid
            i += 1
        return Res
    def GetMin(self):
        Res = DBL_MAX
        i = 0
        while i < self.Amount:
            Tick = _copy(self.Ticks[i])
            if Tick.bid < Res:
                Res = Tick.bid
            if Tick.ask < Res:
                Res = Tick.ask
            i += 1
        return Res
    def ToString(self):
        Str = _str(self.time)
        i = 0
        while i < self.Amount:
            Str += '\n' + self.Ticks[i].ToString()
            i += 1
        return Str

__all__ = ['BAR']
