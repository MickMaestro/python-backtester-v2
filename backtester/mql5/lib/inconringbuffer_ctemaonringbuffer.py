"""ctemaonringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_cdemaonringbuffer import *  # cdemaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CTEMAOnRingBuffer(CArrayRing):
    _q_fields = ('dema', 'm_dema_err', 'm_name', 'm_as_series', 'm_bars_required', 'm_begin1', 'm_begin2', 'm_start', 'm_index')
    def __init__(self):
        CArrayRing.__init__(self)
        self.dema = CDEMAOnRingBuffer()
        self.m_dema_err = CMAOnRingBuffer()
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin1 = 0
        self.m_begin2 = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        pass
    def Init(self, period=12, method=MODE_EMA, size_buffer=256, as_series=False):
        sizebuffer = 2
        if size_buffer < sizebuffer:
            printf('Input parameter size_buffer has incorrect value (%d). Indicator will use value %d for calculations.', size_buffer, sizebuffer)
        else:
            sizebuffer = size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.dema.Init(period, method, sizebuffer):
            return False
        if not self.m_dema_err.Init(period, method, sizebuffer):
            return False
        self.m_name = 'TEMA(' + IntegerToString(self.Period()) + ',' + self.Method() + ')'
        self.m_as_series = as_series
        self.m_bars_required = self.dema.BarsRequired() + self.m_dema_err.BarsRequired()
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
            self.m_begin1 = MathMax(i, rates_total - self.Size() - self.m_bars_required)
            self.m_start = self.m_begin1
            self.m_begin2 = self.m_begin1 + self.dema.BarsRequired()
        else:
            self.m_start = prev_calculated - 1
        demavalue = self.dema.MainOnValue(rates_total, prev_calculated, self.m_begin1, array[self.m_start], self.m_start)
        dema_err = self.m_dema_err.MainOnValue(rates_total, prev_calculated, self.m_begin2, array[self.m_start] - demavalue, self.m_start)
        if demavalue == EMPTY_VALUE or dema_err == EMPTY_VALUE:
            self.Last_1(EMPTY_VALUE)
        else:
            self.Last_1(demavalue + dema_err)
        for i in range(self.m_start + 1, rates_total):
            demavalue = self.dema.MainOnValue(rates_total, prev_calculated, self.m_begin1, array[i], i)
            dema_err = self.m_dema_err.MainOnValue(rates_total, prev_calculated, self.m_begin2, array[i] - demavalue, i)
            if demavalue == EMPTY_VALUE or dema_err == EMPTY_VALUE:
                self.Add(EMPTY_VALUE)
            else:
                self.Add(demavalue + dema_err)
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
            self.m_begin1 = begin
            self.m_begin2 = begin + self.dema.BarsRequired()
        demavalue = self.dema.MainOnValue(rates_total, prev_calculated, self.m_begin1, value, self.m_index)
        dema_err = self.m_dema_err.MainOnValue(rates_total, prev_calculated, self.m_begin2, value - demavalue, self.m_index)
        if (prev_calculated - 1) == self.m_index:
            if demavalue == EMPTY_VALUE or dema_err == EMPTY_VALUE:
                self.Last_1(EMPTY_VALUE)
            else:
                self.Last_1(demavalue + dema_err)
        else:
            if demavalue == EMPTY_VALUE or dema_err == EMPTY_VALUE:
                self.Add(EMPTY_VALUE)
            else:
                self.Add(demavalue + dema_err)
        return self.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def Period(self):
        return self.dema.Period()
    def Method(self):
        return self.dema.Method()
    def MA(self, index):
        return self.dema.ma.At(index)
    def DEMA(self, index):
        return self.dema.At(index)
    def __getitem__(self, index):
        return self.At(index)

__all__ = ['CTEMAOnRingBuffer']
