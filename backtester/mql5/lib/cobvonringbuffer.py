"""cobvonringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class COBVOnRingBuffer(CArrayRing):
    _q_fields = ('m_dOBV', 'm_name', 'm_period', 'm_dobv', 'm_prev_price', 'm_cur_price', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index')
    def __init__(self):
        CArrayRing.__init__(self)
        self.m_dOBV = CArrayRing()
        self.m_name = ""
        self.m_period = 0
        self.m_dobv = 0
        self.m_prev_price = 0.0
        self.m_cur_price = 0.0
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        pass
    def Init(self, period=0, size_buffer=256, as_series=False):
        if period < 0:
            self.m_period = 0
            printf('Input parameter Period has incorrect value (%d). Indicator will use value %d for calculations.', period, self.m_period)
        else:
            self.m_period = period
        sizebuffer = 2
        if size_buffer < sizebuffer:
            printf('Input parameter size_buffer has incorrect value (%d). Indicator will use value %d for calculations.', size_buffer, sizebuffer)
        else:
            sizebuffer = size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_dOBV.Init(self.m_period + 1):
            return False
        self.m_bars_required = 0
        self.m_name = 'OBV'
        if self.m_period > 0:
            self.m_bars_required = self.m_period
            self.m_name += '(' + IntegerToString(self.m_period) + ')'
        self.m_as_series = as_series
        return True
    def MainOnArray(self, rates_total, prev_calculated, price, volume):
        as_series_price = ArrayGetAsSeries(price)
        as_series_vol = ArrayGetAsSeries(volume)
        if as_series_price:
            ArraySetAsSeries(price, False)
        if as_series_vol:
            ArraySetAsSeries(volume, False)
        if prev_calculated == 0:
            i = -1
            while (i := i + 1) < rates_total:
                if price[i] != 0 and price[i] != EMPTY_VALUE:
                    break
            if self.m_period > 0:
                self.m_start = i + self.m_period
                self.Update(0.0, 1)
                while (i := i + 1) <= self.m_start:
                    if price[i] > price[i - 1]:
                        self.m_dobv = volume[i]
                    elif price[i] < price[i - 1]:
                        self.m_dobv = -volume[i]
                    else:
                        self.m_dobv = 0
                    self.m_dOBV.Add(self.m_dobv)
                    self.Update(self.At(1) + self.m_dobv, 1)
                self.m_dOBV.Add(self.m_dobv)
            else:
                self.m_start = i
                self.Update(volume[i], 1)
            self.m_start = self.m_start + 1
        else:
            self.m_start = prev_calculated - 1
        if price[self.m_start] > price[self.m_start - 1]:
            self.m_dobv = volume[self.m_start]
        elif price[self.m_start] < price[self.m_start - 1]:
            self.m_dobv = -volume[self.m_start]
        else:
            self.m_dobv = 0
        self.Last_1(self.At(1) + self.m_dobv)
        if self.m_period > 0:
            self.m_dOBV.Last_1(self.m_dobv)
            self.Last_1(self.Last_0() - self.m_dOBV[self.m_period])
            for i in range(self.m_start + 1, rates_total):
                if price[i] > price[i - 1]:
                    self.m_dobv = volume[i]
                elif price[i] < price[i - 1]:
                    self.m_dobv = -volume[i]
                else:
                    self.m_dobv = 0
                self.m_dOBV.Add(self.m_dobv)
                self.Add(self.Last_0() + self.m_dobv - self.m_dOBV.At(self.m_period))
        else:
            for i in range(self.m_start + 1, rates_total):
                if price[i] > price[i - 1]:
                    self.m_dobv = volume[i]
                elif price[i] < price[i - 1]:
                    self.m_dobv = -volume[i]
                else:
                    self.m_dobv = 0
                self.Add(self.Last_0() + self.m_dobv)
        if as_series_price:
            ArraySetAsSeries(price, True)
        if as_series_vol:
            ArraySetAsSeries(volume, True)
        return rates_total
    def MainOnValue(self, rates_total, prev_calculated, begin, price, volume, index):
        if self.m_as_series:
            self.m_begin = rates_total - 1 - begin
            self.m_index = rates_total - 1 - index
        else:
            self.m_begin = begin
            self.m_index = index
        if self.m_index < self.m_begin:
            return EMPTY_VALUE
        if self.m_index == self.m_begin:
            self.m_cur_price = price
            self.m_prev_price = self.m_cur_price
            if self.m_period > 0:
                self.Last_1(0.0)
                return 0.0
            else:
                self.Update(volume, 1)
                self.Update(volume, 0)
                return float(volume)
        if (prev_calculated - 1) != self.m_index:
            self.m_prev_price = self.m_cur_price
        self.m_cur_price = price
        if price > self.m_prev_price:
            self.m_dobv = volume
        elif price < self.m_prev_price:
            self.m_dobv = -volume
        else:
            self.m_dobv = 0
        if self.m_period > 0:
            if self.m_index <= (self.m_begin + self.m_period):
                self.m_dOBV.Add(self.m_dobv)
                self.Last_1(self.Last_0() + self.m_dobv)
                if self.m_index == (self.m_begin + self.m_period):
                    self.Update(self.Last_0(), 1)
                return 0.0
        if (prev_calculated - 1) == self.m_index:
            self.m_dOBV.Last_1(self.m_dobv)
            self.Last_1(self.At(1) + self.m_dobv)
        else:
            self.m_dOBV.Add(self.m_dobv)
            self.Add(self.Last_0() + self.m_dobv)
        if self.m_period > 0:
            self.Last_1(self.Last_0() - self.m_dOBV[self.m_period])
        return self.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def Period(self):
        return self.m_period
    def __getitem__(self, index):
        return self.At(index)

__all__ = ['COBVOnRingBuffer']
