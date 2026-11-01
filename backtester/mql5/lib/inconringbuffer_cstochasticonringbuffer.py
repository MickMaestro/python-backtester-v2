"""cstochasticonringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CStochasticOnRingBuffer(MqlObject):
    _q_fields = ('signal', 'm_main', 'm_max', 'm_min', 'm_close', 'm_high', 'm_low', 'm_period_k', 'm_period_d', 'm_period_s', 'm_sumlow', 'm_sumhigh', 'm_name', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index')
    def __init__(self):
        self.signal = CMAOnRingBuffer()
        self.m_main = CArrayRing()
        self.m_max = CArrayRing()
        self.m_min = CArrayRing()
        self.m_close = CArrayRing()
        self.m_high = CArrayRing()
        self.m_low = CArrayRing()
        self.m_period_k = 0
        self.m_period_d = 0
        self.m_period_s = 0
        self.m_sumlow = 0.0
        self.m_sumhigh = 0.0
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        pass
    def Init(self, period_k=5, period_d=3, period_s=3, method_d=MODE_SMA, size_buffer=256, as_series=False):
        if period_k <= 0:
            self.m_period_k = 5
            printf('Input parameter period_k has incorrect value (%d). Indicator will use value %d for calculations.', period_k, self.m_period_k)
        else:
            self.m_period_k = period_k
        if period_d <= 0:
            self.m_period_d = 3
            printf('Input parameter period_d has incorrect value (%d). Indicator will use value %d for calculations.', period_d, self.m_period_d)
        else:
            self.m_period_d = period_d
        if period_s <= 0:
            self.m_period_s = 3
            printf('Input parameter period_s has incorrect value (%d). Indicator will use value %d for calculations.', period_s, self.m_period_s)
        else:
            self.m_period_s = period_s
        sizebuffer = MathMax(self.m_period_k, MathMax(self.m_period_d, self.m_period_s))
        if size_buffer < sizebuffer:
            printf('Input parameter size_buffer has incorrect value (%d). Indicator will use value %d for calculations.', size_buffer, sizebuffer)
        else:
            sizebuffer = size_buffer
        if not self.m_max.Init(self.m_period_s + 1):
            return False
        if not self.m_min.Init(self.m_period_s + 1):
            return False
        if not self.m_close.Init(self.m_period_k + 1):
            return False
        if not self.m_high.Init(self.m_period_k + 1):
            return False
        if not self.m_low.Init(self.m_period_k + 1):
            return False
        if not self.m_main.Init(sizebuffer):
            return False
        if not self.signal.Init(self.m_period_d, method_d, sizebuffer):
            return False
        self.m_name = 'Stoch(' + IntegerToString(self.m_period_k) + ',' + self.signal.Name() + ',' + IntegerToString(self.m_period_s) + ')'
        self.m_as_series = as_series
        self.m_bars_required = self.signal.BarsRequired() + self.m_period_k + self.m_period_s - 2
        return True
    def MainOnArray(self, rates_total, prev_calculated, high, low, close):
        as_series_high = ArrayGetAsSeries(high)
        as_series_low = ArrayGetAsSeries(low)
        as_series_close = ArrayGetAsSeries(close)
        if as_series_high:
            ArraySetAsSeries(high, False)
        if as_series_low:
            ArraySetAsSeries(low, False)
        if as_series_close:
            ArraySetAsSeries(close, False)
        if prev_calculated == 0:
            for i in range(0, rates_total):
                if ((((high[i] != 0 and high[i] != EMPTY_VALUE) and low[i] != 0) and low[i] != EMPTY_VALUE) and close[i] != 0) and close[i] != EMPTY_VALUE:
                    self.m_start = MathMax(i + 1, rates_total - self.Size() - self.m_bars_required)
                    break
            self.m_sumlow = 0.0
            self.m_sumhigh = 0.0
            self.m_start += self.m_period_k - 1
            i = self.m_start
            while i < (self.m_start + self.m_period_s):
                self.m_max.Add(high[ArrayMaximum(high, i - self.m_period_k + 1, self.m_period_k)])
                self.m_min.Add(low[ArrayMinimum(low, i - self.m_period_k + 1, self.m_period_k)])
                self.m_close.Add(close[i])
                self.m_sumlow += close[i] - self.m_min.Last_0()
                self.m_sumhigh += self.m_max.Last_0() - self.m_min.Last_0()
                i += 1
            self.m_begin = self.m_start + self.m_period_s - 1
            self.m_start = self.m_begin
        else:
            self.m_start = prev_calculated - 1
        self.m_sumlow -= self.m_close.Last_0() - self.m_min.Last_0()
        self.m_sumhigh -= self.m_max.Last_0() - self.m_min.Last_0()
        self.m_max.Last_1(high[ArrayMaximum(high, self.m_start - self.m_period_k + 1, self.m_period_k)])
        self.m_min.Last_1(low[ArrayMinimum(low, self.m_start - self.m_period_k + 1, self.m_period_k)])
        self.m_close.Last_1(close[self.m_start])
        self.m_sumlow += close[self.m_start] - self.m_min.Last_0()
        self.m_sumhigh += self.m_max.Last_0() - self.m_min.Last_0()
        if self.m_sumhigh == 0.0:
            self.m_main.Last_1(100.0)
        else:
            self.m_main.Last_1(_fdiv(self.m_sumlow, self.m_sumhigh) * 100.0)
        self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.m_main.Last_0(), self.m_start)
        self.m_index = self.m_start + 1
        while self.m_index < rates_total:
            self.m_max.Add(high[ArrayMaximum(high, self.m_index - self.m_period_k + 1, self.m_period_k)])
            self.m_min.Add(low[ArrayMinimum(low, self.m_index - self.m_period_k + 1, self.m_period_k)])
            self.m_close.Add(close[self.m_index])
            self.m_sumlow += close[self.m_index] - self.m_min.Last_0() - close[self.m_index - self.m_period_s] + self.m_min[self.m_period_s]
            self.m_sumhigh += self.m_max.Last_0() - self.m_min.Last_0() - self.m_max[self.m_period_s] + self.m_min[self.m_period_s]
            if self.m_sumhigh == 0.0:
                self.m_main.Add(100.0)
            else:
                self.m_main.Add(_fdiv(self.m_sumlow, self.m_sumhigh) * 100.0)
            self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.m_main.Last_0(), self.m_index)
            self.m_index += 1
        if as_series_high:
            ArraySetAsSeries(high, True)
        if as_series_low:
            ArraySetAsSeries(low, True)
        if as_series_close:
            ArraySetAsSeries(close, True)
        return rates_total
    def MainOnValue(self, rates_total, prev_calculated, begin, high, low, close, index):
        if self.m_as_series:
            self.m_index = rates_total - 1 - index
        else:
            self.m_index = index
        if self.m_index < begin:
            return EMPTY_VALUE
        self.m_begin = begin + self.m_period_k - 1
        if self.m_index < self.m_begin:
            self.m_high.Add(high)
            self.m_low.Add(low)
            self.m_close.Add(close)
            return EMPTY_VALUE
        if self.m_index == self.m_begin:
            self.m_sumlow = 0.0
            self.m_sumhigh = 0.0
        self.m_begin += self.m_period_s
        if self.m_index < self.m_begin:
            self.m_high.Add(high)
            self.m_low.Add(low)
            self.m_close.Add(close)
            self.m_max.Add(self.Max())
            self.m_min.Add(self.Min())
            self.m_sumlow += close - self.m_min.Last_0()
            self.m_sumhigh += self.m_max.Last_0() - self.m_min.Last_0()
            return EMPTY_VALUE
        if (prev_calculated - 1) == self.m_index:
            self.m_sumlow -= self.m_close.Last_0() - self.m_min.Last_0()
            self.m_sumhigh -= self.m_max.Last_0() - self.m_min.Last_0()
            self.m_high.Last_1(high)
            self.m_low.Last_1(low)
            self.m_close.Last_1(close)
            self.m_max.Last_1(self.Max())
            self.m_min.Last_1(self.Min())
            self.m_sumlow += close - self.m_min.Last_0()
            self.m_sumhigh += self.m_max.Last_0() - self.m_min.Last_0()
            if self.m_sumhigh == 0.0:
                self.m_main.Last_1(100.0)
            else:
                self.m_main.Last_1(_fdiv(self.m_sumlow, self.m_sumhigh) * 100.0)
        else:
            self.m_high.Add(high)
            self.m_low.Add(low)
            self.m_close.Add(close)
            self.m_max.Add(self.Max())
            self.m_min.Add(self.Min())
            self.m_sumlow += close - self.m_min.Last_0() - self.m_close[self.m_period_s] + self.m_min[self.m_period_s]
            self.m_sumhigh += self.m_max.Last_0() - self.m_min.Last_0() - self.m_max[self.m_period_s] + self.m_min[self.m_period_s]
            if self.m_sumhigh == 0.0:
                self.m_main.Add(100.0)
            else:
                self.m_main.Add(_fdiv(self.m_sumlow, self.m_sumhigh) * 100.0)
        self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.m_main.Last_0(), self.m_index)
        return self.m_main.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return 'Main' + self.m_name
    def NameSignal(self):
        return 'Signal' + self.m_name
    def Method(self):
        return self.signal.MAMethod()
    def PeriodK(self):
        return self.m_period_k
    def PeriodS(self):
        return self.m_period_s
    def PeriodD(self):
        return self.m_period_d
    def Size(self):
        return self.m_main.Size()
    def __getitem__(self, index):
        return self.m_main.At(index)
    def Max(self):
        max_ = -DBL_MAX
        for i in range(0, self.m_period_k):
            max_ = MathMax(max_, self.m_high[i])
        return max_
    def Min(self):
        min_ = DBL_MAX
        for i in range(0, self.m_period_k):
            min_ = MathMin(min_, self.m_low[i])
        return min_

__all__ = ['CStochasticOnRingBuffer']
