"""ceronringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CEROnRingBuffer(CArrayRing):
    _q_fields = ('m_array_in', 'm_dnoise', 'm_period', 'm_noise', 'm_name', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index')
    def __init__(self):
        CArrayRing.__init__(self)
        self.m_array_in = CArrayRing()
        self.m_dnoise = CArrayRing()
        self.m_period = 0
        self.m_noise = 0.0
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        pass
    def Init(self, period=34, size_buffer=256, as_series=False):
        if period <= 0:
            self.m_period = 34
            printf('Input parameter Period has incorrect value (%d). Indicator will use value %d for calculations.', period, self.m_period)
        else:
            self.m_period = period
        sizebuffer = size_buffer
        if size_buffer < (period + 1):
            sizebuffer = self.m_period + 1
            printf('Input parameter size_buffer has incorrect value (%d). Indicator will use value %d for calculations.', size_buffer, sizebuffer)
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_dnoise.Init(self.m_period + 1):
            return False
        if not self.m_array_in.Init(self.m_period + 1):
            return False
        self.m_name = 'ER(' + IntegerToString(self.m_period) + ')'
        self.m_as_series = as_series
        self.m_bars_required = self.m_period + 1
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
            self.m_start = MathMax(i, rates_total - self.Size() - self.m_bars_required) + self.m_period
            self.m_noise = 0.0
            i = self.m_start - self.m_period + 1
            while i <= self.m_start:
                self.m_dnoise.Add(fabs(array[i] - array[i - 1]))
                self.m_noise += self.m_dnoise.Last_0()
                i += 1
        else:
            self.m_start = prev_calculated - 1
        self.m_noise -= self.m_dnoise.Last_0()
        self.m_dnoise.Last_1(fabs(array[self.m_start] - array[self.m_start - 1]))
        self.m_noise += self.m_dnoise.Last_0()
        if self.m_noise == 0:
            self.Last_1(0.0)
        else:
            self.Last_1(_fdiv(fabs(array[self.m_start] - array[self.m_start - self.m_period]), self.m_noise))
        for i in range(self.m_start + 1, rates_total):
            self.m_dnoise.Add(fabs(array[i] - array[i - 1]))
            self.m_noise += self.m_dnoise.Last_0() - self.m_dnoise[self.m_period]
            if self.m_noise == 0:
                self.Add(0.0)
            else:
                self.Add(_fdiv(fabs(array[i] - array[i - self.m_period]), self.m_noise))
        if as_series:
            ArraySetAsSeries(array, True)
        return rates_total
    def MainOnValue(self, rates_total, prev_calculated, begin, value, index):
        if self.m_as_series:
            self.m_index = rates_total - 1 - index
        else:
            self.m_index = index
        if self.m_index < begin:
            return EMPTY_VALUE
        if (prev_calculated - 1) == self.m_index:
            self.m_array_in.Last_1(value)
        else:
            self.m_array_in.Add(value)
        self.m_begin = begin + self.m_period
        if self.m_index < self.m_begin:
            return EMPTY_VALUE
        if self.m_index == self.m_begin:
            self.m_noise = 0.0
            for i in range(self.m_period - 1, 0 - 1, -1):
                self.m_dnoise.Add(fabs(self.m_array_in[i] - self.m_array_in[i + 1]))
                self.m_noise += self.m_dnoise.Last_0()
            if self.m_noise == 0:
                self.Add(0.0)
            else:
                self.Add(_fdiv(fabs(value - self.m_array_in[self.m_period]), self.m_noise))
            return self.Last_0()
        if (prev_calculated - 1) == self.m_index:
            self.m_noise -= self.m_dnoise.Last_0()
            self.m_dnoise.Last_1(fabs(value - self.m_array_in[1]))
            self.m_noise += self.m_dnoise.Last_0()
            if self.m_noise == 0:
                self.Last_1(0.0)
            else:
                self.Last_1(_fdiv(fabs(value - self.m_array_in[self.m_period]), self.m_noise))
        else:
            self.m_dnoise.Add(fabs(value - self.m_array_in[1]))
            self.m_noise += self.m_dnoise.Last_0() - self.m_dnoise[self.m_period]
            if self.m_noise == 0:
                self.Add(0.0)
            else:
                self.Add(_fdiv(fabs(value - self.m_array_in[self.m_period]), self.m_noise))
        return self.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def Period(self):
        return self.m_period
    def __getitem__(self, index):
        return self.At(index)

__all__ = ['CEROnRingBuffer']
