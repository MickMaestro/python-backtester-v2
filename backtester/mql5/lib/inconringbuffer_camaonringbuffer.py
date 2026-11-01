"""camaonringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_ceronringbuffer import *  # ceronringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CAMAOnRingBuffer(CArrayRing):
    _q_fields = ('m_er', 'm_period', 'm_fast_period', 'm_slow_period', 'm_name', 'm_fc', 'm_sc', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index')
    def __init__(self):
        CArrayRing.__init__(self)
        self.m_er = CEROnRingBuffer()
        self.m_period = 0
        self.m_fast_period = 0
        self.m_slow_period = 0
        self.m_name = ""
        self.m_fc = 0.0
        self.m_sc = 0.0
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        pass
    def Init(self, period=10, fast_period=2, slow_period=30, size_buffer=256, as_series=False):
        if period <= 0:
            self.m_period = 10
            printf('Input parameter Period has incorrect value (%d). Indicator will use value %d for calculations.', period, self.m_period)
        else:
            self.m_period = period
        if fast_period <= 0:
            self.m_fast_period = 2
            printf('Input parameter Fast Period has incorrect value (%d). Indicator will use value %d for calculations.', self.m_fast_period, fast_period)
        else:
            self.m_fast_period = fast_period
        if slow_period <= 0:
            self.m_slow_period = 30
            printf('Input parameter Slow Period has incorrect value (%d). Indicator will use value %d for calculations.', self.m_slow_period, slow_period)
        else:
            self.m_slow_period = slow_period
        sizebuffer = self.m_period
        if size_buffer < sizebuffer:
            printf('Input parameter size_buffer has incorrect value (%d). Indicator will use value %d for calculations.', size_buffer, sizebuffer)
        else:
            sizebuffer = size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_er.Init(self.m_period, self.m_period + 1):
            return False
        self.m_name = 'AMA(' + IntegerToString(self.m_period) + ',' + IntegerToString(self.m_fast_period) + ',' + IntegerToString(self.m_slow_period) + ')'
        self.m_fc = _fdiv(2.0, self.m_fast_period + 1.0)
        self.m_sc = _fdiv(2.0, self.m_slow_period + 1.0)
        self.m_as_series = as_series
        m = 10
        self.m_bars_required = (m * MathMax(self.m_fast_period, self.m_slow_period)) + self.m_period - 1
        return True
    def MainOnArray(self, rates_total, prev_calculated, array):
        as_series = ArrayGetAsSeries(array)
        if as_series:
            ArraySetAsSeries(array, False)
        if prev_calculated == 0:
            i = -1
            while (i := i + 1) < rates_total:
                if array[i] != 0 and array[i] != EMPTY_VALUE:
                    break
            self.m_begin = MathMax(i, rates_total - self.Size() - self.m_bars_required)
            self.m_start = self.m_begin + self.m_period
            i = self.m_begin
            while i < self.m_start:
                self.m_er.MainOnValue(rates_total, prev_calculated, self.m_begin, array[i], i)
                i += 1
            self.Update(array[self.m_start - 1], 1)
        else:
            self.m_start = prev_calculated - 1
        self.m_er.MainOnValue(rates_total, prev_calculated, self.m_begin, array[self.m_start], self.m_start)
        dCurrentSSC = (self.m_er.Last_0() * (self.m_fc - self.m_sc)) + self.m_sc
        dPrevAMA = self.At(1)
        self.Last_1((pow(dCurrentSSC, 2) * (array[self.m_start] - dPrevAMA)) + dPrevAMA)
        for i in range(self.m_start + 1, rates_total):
            self.m_er.MainOnValue(rates_total, prev_calculated, self.m_begin, array[i], i)
            dCurrentSSC = (self.m_er.Last_0() * (self.m_fc - self.m_sc)) + self.m_sc
            dPrevAMA = self.Last_0()
            self.Add((pow(dCurrentSSC, 2) * (array[i] - dPrevAMA)) + dPrevAMA)
        if as_series:
            ArraySetAsSeries(array, True)
        return rates_total
    def MainOnValue(self, rates_total, prev_calculated, begin, value, index):
        if self.m_as_series:
            self.m_index = rates_total - 1 - index
        else:
            self.m_index = index
        self.m_er.MainOnValue(rates_total, prev_calculated, begin, value, self.m_index)
        self.m_begin = begin + self.m_er.BarsRequired()
        if self.m_index < self.m_begin:
            return EMPTY_VALUE
        if self.m_index == self.m_begin:
            self.Update(self.m_er.m_array_in[1], 1)
            self.Update(self.m_er.m_array_in[0], 0)
        dCurrentSSC = (self.m_er.Last_0() * (self.m_fc - self.m_sc)) + self.m_sc
        if (prev_calculated - 1) == self.m_index:
            self.Last_1((pow(dCurrentSSC, 2) * (value - self.At(1))) + self.At(1))
        else:
            self.Add((pow(dCurrentSSC, 2) * (value - self.Last_0())) + self.Last_0())
        return self.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def Period(self):
        return self.m_period
    def FastPeriod(self):
        return self.m_fast_period
    def SlowPeriod(self):
        return self.m_slow_period
    def __getitem__(self, index):
        return self.At(index)

__all__ = ['CAMAOnRingBuffer']
