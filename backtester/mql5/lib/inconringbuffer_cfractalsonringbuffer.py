"""cfractalsonringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CFractalsOnRingBuffer(MqlObject):
    _q_fields = ('upper', 'lower', 'm_high_in', 'm_low_in', 'm_name', 'm_bars_right', 'm_bars_left', 'm_bars_total', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index')
    def __init__(self):
        self.upper = CArrayRing()
        self.lower = CArrayRing()
        self.m_high_in = CArrayRing()
        self.m_low_in = CArrayRing()
        self.m_name = ""
        self.m_bars_right = 0
        self.m_bars_left = 0
        self.m_bars_total = 0
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        pass
    def Init(self, bars_right=2, bars_left=2, size_buffer=256, as_series=False):
        if bars_right < 1:
            self.m_bars_right = 1
            printf('Input parameter bars_right has incorrect value (%d). Indicator will use value %d for calculations.', bars_right, self.m_bars_right)
        else:
            self.m_bars_right = bars_right
        if bars_left < 1:
            self.m_bars_left = 1
            printf('Input parameter bars_left has incorrect value (%d). Indicator will use value %d for calculations.', bars_left, self.m_bars_left)
        else:
            self.m_bars_left = bars_left
        self.m_bars_total = self.m_bars_right + self.m_bars_left + 1
        sizebuffer = self.m_bars_total + 1
        if size_buffer < sizebuffer:
            printf('Input parameter size_buffer has incorrect value (%d). Indicator will use value %d for calculations.', size_buffer, sizebuffer)
        else:
            sizebuffer = size_buffer
        if not self.upper.Init(sizebuffer):
            return False
        if not self.lower.Init(sizebuffer):
            return False
        if not self.m_high_in.Init(sizebuffer):
            return False
        if not self.m_low_in.Init(sizebuffer):
            return False
        self.m_name = 'Fractals(' + IntegerToString(self.m_bars_left) + ',' + IntegerToString(self.m_bars_right) + ')'
        self.m_as_series = as_series
        self.m_bars_required = self.m_bars_total
        return True
    def MainOnArray(self, rates_total, prev_calculated, high, low):
        as_series_high = ArrayGetAsSeries(high)
        as_series_low = ArrayGetAsSeries(low)
        if not as_series_high:
            ArraySetAsSeries(high, True)
        if not as_series_low:
            ArraySetAsSeries(low, True)
        if prev_calculated == 0:
            i = rates_total
            while (i := i - 1) >= 0:
                if ((high[i] != 0 and high[i] != EMPTY_VALUE) and low[i] != 0) and low[i] != EMPTY_VALUE:
                    break
            self.m_start = MathMin(i, self.upper.Size() + self.m_bars_required)
            self.m_start -= self.m_bars_total
        else:
            self.m_start = rates_total - (prev_calculated - 1)
        self.m_index = self.m_start + self.m_bars_right
        if ArrayMaximum(high, self.m_start, self.m_bars_total) == self.m_index:
            self.upper.Update(high[self.m_index], self.m_bars_right)
        else:
            self.upper.Update(EMPTY_VALUE, self.m_bars_right)
        if ArrayMinimum(low, self.m_start, self.m_bars_total) == self.m_index:
            self.lower.Update(low[self.m_index], self.m_bars_right)
        else:
            self.lower.Update(EMPTY_VALUE, self.m_bars_right)
        for i in range(self.m_start - 1, 0 - 1, -1):
            self.m_index -= 1
            self.upper.Add(EMPTY_VALUE)
            if ArrayMaximum(high, i, self.m_bars_total) == self.m_index:
                self.upper.Update(high[self.m_index], self.m_bars_right)
            else:
                self.upper.Update(EMPTY_VALUE, self.m_bars_right)
            self.lower.Add(EMPTY_VALUE)
            if ArrayMinimum(low, i, self.m_bars_total) == self.m_index:
                self.lower.Update(low[self.m_index], self.m_bars_right)
            else:
                self.lower.Update(EMPTY_VALUE, self.m_bars_right)
        if not as_series_high:
            ArraySetAsSeries(high, False)
        if not as_series_low:
            ArraySetAsSeries(low, False)
        return rates_total
    def MainOnHigh(self, rates_total, prev_calculated, begin, high, index):
        if self.m_as_series:
            self.m_begin = rates_total - 1 - begin
            self.m_index = rates_total - 1 - index
        else:
            self.m_begin = begin
            self.m_index = index
        if self.m_index < self.m_begin:
            return EMPTY_VALUE
        if (prev_calculated - 1) == self.m_index:
            self.m_high_in.Last_1(high)
        else:
            self.m_high_in.Add(high)
        if self.m_index < (self.m_begin + self.m_bars_required):
            return EMPTY_VALUE
        if (prev_calculated - 1) != self.m_index:
            self.upper.Add(EMPTY_VALUE)
        index_max = 0
        for i in range(1, self.m_bars_total):
            if self.m_high_in[index_max] < self.m_high_in[i]:
                index_max = i
        if index_max == self.m_bars_right:
            self.upper.Update(self.m_high_in[index_max], self.m_bars_right)
        else:
            self.upper.Update(EMPTY_VALUE, self.m_bars_right)
        return self.upper.At(self.m_bars_right)
    def MainOnLow(self, rates_total, prev_calculated, begin, low, index):
        if self.m_as_series:
            self.m_begin = rates_total - 1 - begin
            self.m_index = rates_total - 1 - index
        else:
            self.m_begin = begin
            self.m_index = index
        if self.m_index < self.m_begin:
            return EMPTY_VALUE
        if (prev_calculated - 1) == self.m_index:
            self.m_low_in.Last_1(low)
        else:
            self.m_low_in.Add(low)
        if self.m_index < (self.m_begin + self.m_bars_required):
            return EMPTY_VALUE
        if (prev_calculated - 1) != self.m_index:
            self.lower.Add(EMPTY_VALUE)
        index_min = 0
        for i in range(1, self.m_bars_total):
            if self.m_low_in[index_min] > self.m_low_in[i]:
                index_min = i
        if index_min == self.m_bars_right:
            self.lower.Update(self.m_low_in[index_min], self.m_bars_right)
        else:
            self.lower.Update(EMPTY_VALUE, self.m_bars_right)
        return self.lower.At(self.m_bars_right)
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def NameUpper(self):
        return 'Upper ' + self.m_name
    def NameLower(self):
        return 'Lower ' + self.m_name
    def BarsRight(self):
        return self.m_bars_right
    def BarsLeft(self):
        return self.m_bars_left
    def Size(self):
        return self.upper.Size()

__all__ = ['CFractalsOnRingBuffer']
