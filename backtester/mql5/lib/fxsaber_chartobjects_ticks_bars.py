"""Bars.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.fxsaber_chartobjects_ticks_bar import *  # Bar.mqh
from backtester.mql5.lib.fxsaber_chartobjects_ticks_tick import *  # Tick.mqh
from backtester.mql5.lib.fxsaber_pointer import *  # Pointer.mqh


class BARS(MqlObject):
    _q_fields = ('bars', 'Amount', 'Symb')
    _q_ptrs = ('bars',)
    def __init__(self, Chart_ID=0):
        self.bars = Arr(0, None)
        self.Amount = 0
        self.Symb = ""
        self.Symb = ChartSymbol(Chart_ID)
        self.Amount = _int(ChartGetInteger(Chart_ID, CHART_VISIBLE_BARS))
        FirstBar = _int(ChartGetInteger(Chart_ID, CHART_FIRST_VISIBLE_BAR)) - self.Amount
        if FirstBar < 0:
            FirstBar = 0
        else:
            self.Amount += 1
        period = ChartPeriod(Chart_ID)
        Times = Arr(0, 0)
        PrevAmount = self.Amount
        self.Amount = CopyTime(self.Symb, period, FirstBar, self.Amount, Times)
        if self.Amount > 0:
            Ticks = Arr(0, 0, factory=MqlTick)
            AmountTicks = Box(1)
            ArrayResize(Ticks, AmountTicks.v)
            Ticks[0].time_msc = (Times[0] * 1000) - 1
            self.GetNextTicks(Ticks, AmountTicks)
            if AmountTicks.v > 0:
                self.Amount = ArrayResize(self.bars, self.Amount)
            else:
                self.Amount = 0
            PeriodSec = PeriodSeconds(period)
            Pos = Box(0)
            TmpTick = TICK()
            i = 0
            while i < self.Amount:
                self.SkipTicks(Ticks, AmountTicks, Pos, TmpTick, Times[i], _ElemRef(self.bars, i), False)
                self.SkipTicks(Ticks, AmountTicks, Pos, TmpTick, Times[i] + PeriodSec, _ElemRef(self.bars, i), True)
                if AmountTicks.v <= 0:
                    self.Amount = ArrayResize(self.bars, i + 1)
                    break
                i += 1
    def _q_dtor(self):
        POINTER.DeleteObject_2(self.bars)
    def GetNextTicks(self, Ticks, AmountTicks):
        if AmountTicks.v > 0:
            AmountTicks.v = CopyTicks(self.Symb, Ticks, COPY_TICKS_INFO, Ticks[AmountTicks.v - 1].time_msc + 1)
        return
    def SkipTicks(self, Ticks, AmountTicks, Pos, TmpTick, EndTime, Bar, SaveFlag=False):
        Count = 0
        NewTmpTick = _copy(TmpTick)
        while Pos.v < AmountTicks.v:
            Tick = _copy(Ticks[Pos.v])
            if Tick.time >= EndTime:
                if SaveFlag:
                    Bar.v.AddData(TmpTick, Ticks, Pos.v - Count, Count)
                else:
                    Bar.v = BAR(EndTime)
                break
            if Tick.bid != 0:
                NewTmpTick.bid = Tick.bid
            if Tick.ask != 0:
                NewTmpTick.ask = Tick.ask
            Count += 1
            Pos.v += 1
            if Pos.v == AmountTicks.v:
                if SaveFlag:
                    Bar.v.AddData(TmpTick, Ticks, Pos.v - Count, Count)
                self.GetNextTicks(Ticks, AmountTicks)
                Pos.v = 0
                Count = 0
        _assign(TmpTick, NewTmpTick)
        return
    def GetAmount(self):
        return self.Amount
    def __getitem__(self, Pos):
        return self.bars[Pos]
    def __getitem__(self, time):
        Res = None
        if self.Amount > 0:
            i = 0
            i = 0
            while i < self.Amount:
                if self.bars[i].time >= time:
                    break
                i += 1
            Res = (self.bars[i - 1] if (i == self.Amount) else self.bars[i])
        return Res
    def GetMax(self):
        Res = DBL_MIN
        i = 0
        while i < self.Amount:
            Tmp = self.bars[i].GetMax()
            if Tmp > Res:
                Res = Tmp
            i += 1
        return Res
    def GetMin(self):
        Res = DBL_MAX
        i = 0
        while i < self.Amount:
            Tmp = self.bars[i].GetMin()
            if Tmp < Res:
                Res = Tmp
            i += 1
        return Res
    def GetAmountTicks(self):
        Sum = 0
        i = 0
        while i < self.Amount:
            Sum += self.bars[i].GetAmount()
            i += 1
        return Sum

__all__ = ['BARS']
