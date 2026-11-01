"""cmfionringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CMFIOnRingBuffer(CArrayRing):
    _q_fields = ('m_pma', 'm_nma', 'm_name', 'm_prev_price', 'm_cur_price', 'm_applied_price', 'm_applied_volume', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index')
    def __init__(self):
        CArrayRing.__init__(self)
        self.m_pma = CMAOnRingBuffer()
        self.m_nma = CMAOnRingBuffer()
        self.m_name = ""
        self.m_prev_price = 0.0
        self.m_cur_price = 0.0
        self.m_applied_price = 0
        self.m_applied_volume = 0
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        pass
    def Init(self, period=14, method=MODE_SMA, applied_price=PRICE_TYPICAL, applied_volume=VOLUME_TICK, size_buffer=256, as_series=False):
        sizebuffer = period
        if size_buffer < sizebuffer:
            printf('Input parameter size_buffer has incorrect value (%d). Indicator will use value %d for calculations.', size_buffer, sizebuffer)
        else:
            sizebuffer = size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_pma.Init(period, method, sizebuffer):
            return False
        if not self.m_nma.Init(period, method, sizebuffer):
            return False
        self.m_name = 'MFI(' + IntegerToString(self.Period()) + ',' + self.Method() + ')'
        self.m_applied_price = applied_price
        self.m_applied_volume = applied_volume
        self.m_as_series = as_series
        self.m_bars_required = self.m_pma.BarsRequired() + 1
        return True
    def MainOnArray(self, rates_total, prev_calculated, open, high, low, close, tick_volume, volume):
        as_series_open = ArrayGetAsSeries(open)
        as_series_high = ArrayGetAsSeries(high)
        as_series_low = ArrayGetAsSeries(low)
        as_series_close = ArrayGetAsSeries(close)
        as_series_tvol = ArrayGetAsSeries(tick_volume)
        as_series_rvol = ArrayGetAsSeries(volume)
        if as_series_open:
            ArraySetAsSeries(open, False)
        if as_series_high:
            ArraySetAsSeries(high, False)
        if as_series_low:
            ArraySetAsSeries(low, False)
        if as_series_close:
            ArraySetAsSeries(close, False)
        if as_series_tvol:
            ArraySetAsSeries(tick_volume, False)
        if as_series_rvol:
            ArraySetAsSeries(volume, False)
        if prev_calculated == 0:
            i = -1
            while (i := i + 1) < rates_total:
                if ((((((open[i] != 0 and open[i] != EMPTY_VALUE) and high[i] != 0) and high[i] != EMPTY_VALUE) and low[i] != 0) and low[i] != EMPTY_VALUE) and close[i] != 0) and close[i] != EMPTY_VALUE:
                    break
            self.m_start = MathMax(i, rates_total - self.Size() - self.m_bars_required)
            self.m_cur_price = self.Price_4(open[self.m_start], high[self.m_start], low[self.m_start], close[self.m_start])
            self.m_prev_price = self.m_cur_price
            self.m_begin = self.m_start + 1
            self.m_start = self.m_begin
        else:
            self.m_start = prev_calculated - 1
        if (prev_calculated - 1) != self.m_start:
            self.m_prev_price = self.m_cur_price
        self.m_cur_price = self.Price_4(open[self.m_start], high[self.m_start], low[self.m_start], close[self.m_start])
        positive = ((self.m_cur_price * self.Volume_2(tick_volume[self.m_start], volume[self.m_start])) if (self.m_cur_price > self.m_prev_price) else 0)
        negative = ((self.m_cur_price * self.Volume_2(tick_volume[self.m_start], volume[self.m_start])) if (self.m_cur_price < self.m_prev_price) else 0)
        pma = self.m_pma.MainOnValue(rates_total, prev_calculated, self.m_begin, positive, self.m_start)
        nma = self.m_nma.MainOnValue(rates_total, prev_calculated, self.m_begin, negative, self.m_start)
        if pma == EMPTY_VALUE or nma == EMPTY_VALUE:
            self.Last_1(EMPTY_VALUE)
        elif nma != 0:
            self.Last_1(100.0 - _fdiv(100.0, 1 + _fdiv(pma, nma)))
        elif pma != 0.0:
            self.Last_1(100.0)
        else:
            self.Last_1(50.0)
        for i in range(self.m_start + 1, rates_total):
            self.m_prev_price = self.m_cur_price
            self.m_cur_price = self.Price_4(open[i], high[i], low[i], close[i])
            positive = ((self.m_cur_price * self.Volume_2(tick_volume[i], volume[i])) if (self.m_cur_price > self.m_prev_price) else 0)
            negative = ((self.m_cur_price * self.Volume_2(tick_volume[i], volume[i])) if (self.m_cur_price < self.m_prev_price) else 0)
            pma = self.m_pma.MainOnValue(rates_total, prev_calculated, self.m_begin, positive, i)
            nma = self.m_nma.MainOnValue(rates_total, prev_calculated, self.m_begin, negative, i)
            if pma == EMPTY_VALUE or nma == EMPTY_VALUE:
                self.Add(EMPTY_VALUE)
            elif nma != 0:
                self.Add(100.0 - _fdiv(100.0, 1 + _fdiv(pma, nma)))
            elif pma != 0.0:
                self.Add(100.0)
            else:
                self.Add(50.0)
        if as_series_open:
            ArraySetAsSeries(open, True)
        if as_series_high:
            ArraySetAsSeries(high, True)
        if as_series_low:
            ArraySetAsSeries(low, True)
        if as_series_close:
            ArraySetAsSeries(close, True)
        if as_series_tvol:
            ArraySetAsSeries(tick_volume, True)
        if as_series_rvol:
            ArraySetAsSeries(volume, True)
        return rates_total
    def MainOnValue(self, rates_total, prev_calculated, begin, open, high, low, close, tick_volume, volume, index):
        if self.m_as_series:
            self.m_index = rates_total - 1 - index
        else:
            self.m_index = index
        if self.m_index < begin:
            return EMPTY_VALUE
        if self.m_index == begin:
            self.m_cur_price = self.Price_4(open, high, low, close)
            self.m_prev_price = self.m_cur_price
            return EMPTY_VALUE
        if (prev_calculated - 1) != self.m_index:
            self.m_prev_price = self.m_cur_price
        self.m_cur_price = self.Price_4(open, high, low, close)
        positive = ((self.m_cur_price * self.Volume_2(tick_volume, volume)) if (self.m_cur_price > self.m_prev_price) else 0)
        negative = ((self.m_cur_price * self.Volume_2(tick_volume, volume)) if (self.m_cur_price < self.m_prev_price) else 0)
        pma = self.m_pma.MainOnValue(rates_total, prev_calculated, begin + 1, positive, self.m_index)
        nma = self.m_nma.MainOnValue(rates_total, prev_calculated, begin + 1, negative, self.m_index)
        if (prev_calculated - 1) == self.m_index:
            if pma == EMPTY_VALUE or nma == EMPTY_VALUE:
                self.Last_1(EMPTY_VALUE)
            elif nma != 0.0:
                self.Last_1(100.0 - _fdiv(100.0, 1 + _fdiv(pma, nma)))
            elif pma != 0.0:
                self.Last_1(100.0)
            else:
                self.Last_1(50.0)
        else:
            if pma == EMPTY_VALUE or nma == EMPTY_VALUE:
                self.Add(EMPTY_VALUE)
            elif nma != 0.0:
                self.Add(100.0 - _fdiv(100.0, 1 + _fdiv(pma, nma)))
            elif pma != 0.0:
                self.Add(100.0)
            else:
                self.Add(50.0)
        return self.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def Period(self):
        return self.m_pma.MAPeriod()
    def Method(self):
        return self.m_pma.MAMethod()
    def Price_0(self):
        return self.m_applied_price
    def Price_4(self, open, high, low, close):
        _sw1 = self.m_applied_price
        if _sw1 == PRICE_OPEN:
            return open
        elif _sw1 == PRICE_CLOSE:
            return close
        elif _sw1 == PRICE_HIGH:
            return high
        elif _sw1 == PRICE_LOW:
            return low
        elif _sw1 == PRICE_MEDIAN:
            return (high + low) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            return (high + low + close) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            return (high + low + close + close) / 4.0
        return EMPTY_VALUE
    def Volume_0(self):
        return self.m_applied_volume
    def Volume_2(self, tick_volume, volume):
        _sw2 = self.m_applied_volume
        if _sw2 == VOLUME_TICK:
            return float(tick_volume)
        elif _sw2 == VOLUME_REAL:
            return float(volume)
        return EMPTY_VALUE
    def __getitem__(self, index):
        return self.At(index)

__all__ = ['CMFIOnRingBuffer']
