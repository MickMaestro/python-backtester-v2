"""crsionringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CRSIOnRingBuffer(CArrayRing):
    _q_fields = ('m_pma', 'm_nma', 'm_name', 'm_prev_value', 'm_cur_value', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index')
    def __init__(self):
        CArrayRing.__init__(self)
        self.m_pma = CMAOnRingBuffer()
        self.m_nma = CMAOnRingBuffer()
        self.m_name = ""
        self.m_prev_value = 0.0
        self.m_cur_value = 0.0
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        pass
    def Init(self, period=14, method=MODE_SMMA, size_buffer=256, as_series=False):
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
        self.m_name = 'RSI(' + IntegerToString(self.Period()) + ',' + self.Method() + ')'
        self.m_as_series = as_series
        self.m_bars_required = self.m_pma.BarsRequired() + 1
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
            self.m_begin = MathMax(i, rates_total - self.Size() - self.m_bars_required) + 1
            self.m_start = self.m_begin
        else:
            self.m_start = prev_calculated - 1
        diff = array[self.m_start] - array[self.m_start - 1]
        positive = (diff if (diff > 0) else 0)
        negative = ((-diff) if (diff < 0) else 0)
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
            diff = array[i] - array[i - 1]
            positive = (diff if (diff > 0) else 0)
            negative = ((-diff) if (diff < 0) else 0)
            pma = self.m_pma.MainOnValue(rates_total, prev_calculated, self.m_begin, positive, i)
            nma = self.m_nma.MainOnValue(rates_total, prev_calculated, self.m_begin, negative, i)
            if pma == EMPTY_VALUE or nma == EMPTY_VALUE:
                self.Add(EMPTY_VALUE)
            elif nma != 0.0:
                self.Add(100.0 - _fdiv(100.0, 1 + _fdiv(pma, nma)))
            elif pma != 0.0:
                self.Add(100.0)
            else:
                self.Add(50.0)
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
        if self.m_index == begin:
            self.m_prev_value = value
            self.m_cur_value = value
            return EMPTY_VALUE
        if (prev_calculated - 1) != self.m_index:
            self.m_prev_value = self.m_cur_value
        self.m_cur_value = value
        diff = value - self.m_prev_value
        positive = (diff if (diff > 0) else 0)
        negative = ((-diff) if (diff < 0) else 0)
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
    def __getitem__(self, index):
        return self.At(index)

__all__ = ['CRSIOnRingBuffer']
