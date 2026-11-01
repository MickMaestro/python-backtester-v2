"""cmomentumonringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CMomentumOnRingBuffer(CArrayRing):
    _q_fields = ('m_value_in', 'm_name', 'm_period', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index')
    def __init__(self):
        CArrayRing.__init__(self)
        self.m_value_in = CArrayRing()
        self.m_name = ""
        self.m_period = 0
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        pass
    def Init(self, period=14, size_buffer=256, as_series=False):
        if period < 0:
            self.m_period = 14
            Print('Input parameter Period has wrong value. Indicator will use value ', self.m_period)
        else:
            self.m_period = period
        sizebuffer = period
        if size_buffer < sizebuffer:
            printf('Input parameter size_buffer has incorrect value (%d). Indicator will use value %d for calculations.', size_buffer, sizebuffer)
        else:
            sizebuffer = size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_value_in.Init(self.m_period + 1):
            return False
        self.m_as_series = as_series
        self.m_bars_required = self.m_period + 1
        self.m_name = 'Momentum(' + IntegerToString(self.m_period) + ')'
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
        else:
            self.m_start = prev_calculated - 1
        if array[self.m_start - self.m_period] != 0:
            self.Last_1(_fdiv(array[self.m_start] * 100.0, array[self.m_start - self.m_period]))
        else:
            self.Last_1(EMPTY_VALUE)
        i = self.m_start + 1
        j = self.m_start + 1 - self.m_period
        while i < rates_total:
            if array[j] != 0:
                self.Add(_fdiv(array[i] * 100.0, array[j]))
            else:
                self.Add(EMPTY_VALUE)
            i += 1
            j += 1
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
            self.m_value_in.Last_1(value)
        else:
            self.m_value_in.Add(value)
        if self.m_index < (begin + self.m_period):
            return EMPTY_VALUE
        if (prev_calculated - 1) == self.m_index:
            if self.m_value_in[self.m_period] != 0:
                self.Last_1(_fdiv(value * 100.0, self.m_value_in[self.m_period]))
            else:
                self.Last_1(EMPTY_VALUE)
        else:
            if self.m_value_in[self.m_period] != 0:
                self.Add(_fdiv(value * 100.0, self.m_value_in[self.m_period]))
            else:
                self.Add(EMPTY_VALUE)
        return self.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def Period(self):
        return self.m_period
    def __getitem__(self, index):
        return self.At(index)

__all__ = ['CMomentumOnRingBuffer']
