"""cmacdonringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CMACDOnRingBuffer(CArrayRing):
    _q_fields = ('signal', 'm_fast', 'm_slow', 'm_name', 'm_name_main', 'm_name_signal', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index')
    def __init__(self):
        CArrayRing.__init__(self)
        self.signal = CMAOnRingBuffer()
        self.m_fast = CMAOnRingBuffer()
        self.m_slow = CMAOnRingBuffer()
        self.m_name = ""
        self.m_name_main = ""
        self.m_name_signal = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        pass
    def Init(self, fast_period=12, slow_period=26, signal_period=9, fast_method=MODE_EMA, slow_method=MODE_EMA, signal_method=MODE_SMA, size_buffer=256, as_series=False):
        fastperiod = fast_period
        slowperiod = slow_period
        signalperiod = signal_period
        sizebuffer = size_buffer
        if fast_period <= 0:
            fastperiod = 12
            printf('Input parameter Fast Period has incorrect value (%d). Indicator will use value %d for calculations.', fast_period, fastperiod)
        if slow_period <= 0:
            slowperiod = 26
            printf('Input parameter Slow Period has incorrect value (%d). Indicator will use value %d for calculations.', slow_period, slowperiod)
        if signal_period <= 0:
            signalperiod = 9
            printf('Input parameter Signal Period has incorrect value (%d). Indicator will use value %d for calculations.', signal_period, signalperiod)
        sizebuffer = MathMax(fastperiod, MathMax(slowperiod, signalperiod))
        if size_buffer < sizebuffer:
            printf('Input parameter size_buffer has incorrect value (%d). Indicator will use value %d for calculations.', size_buffer, sizebuffer)
        else:
            sizebuffer = size_buffer
        if not CArrayRing.Init(self, sizebuffer):
            return False
        if not self.m_fast.Init(fastperiod, fast_method, sizebuffer):
            return False
        if not self.m_slow.Init(slowperiod, slow_method, sizebuffer):
            return False
        if not self.signal.Init(signalperiod, signal_method, sizebuffer):
            return False
        self.m_name = 'MACD(' + self.m_fast.Name() + ',' + self.m_slow.Name() + ',' + self.signal.Name() + ')'
        self.m_name_main = 'Main(' + self.m_fast.Name() + ',' + self.m_slow.Name() + ')'
        self.m_name_signal = 'Signal(' + self.signal.Name() + ')'
        self.m_as_series = as_series
        self.m_bars_required = MathMax(self.m_fast.BarsRequired(), self.m_slow.BarsRequired()) + self.signal.BarsRequired() - 1
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
            self.m_start = self.m_begin
        else:
            self.m_start = prev_calculated - 1
        self.m_fast.MainOnValue(rates_total, prev_calculated, self.m_begin, array[self.m_start], self.m_start)
        self.m_slow.MainOnValue(rates_total, prev_calculated, self.m_begin, array[self.m_start], self.m_start)
        self.Last_1(self.m_fast.Last_0() - self.m_slow.Last_0())
        self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.Last_0(), self.m_start)
        for i in range(self.m_start + 1, rates_total):
            self.m_fast.MainOnValue(rates_total, prev_calculated, self.m_begin, array[i], i)
            self.m_slow.MainOnValue(rates_total, prev_calculated, self.m_begin, array[i], i)
            self.Add(self.m_fast.Last_0() - self.m_slow.Last_0())
            self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.Last_0(), i)
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
        self.m_fast.MainOnValue(rates_total, prev_calculated, self.m_begin, value, self.m_index)
        self.m_slow.MainOnValue(rates_total, prev_calculated, self.m_begin, value, self.m_index)
        if (prev_calculated - 1) == self.m_index:
            self.Last_1(self.m_fast.Last_0() - self.m_slow.Last_0())
        else:
            self.Add(self.m_fast.Last_0() - self.m_slow.Last_0())
        self.signal.MainOnValue(rates_total, prev_calculated, self.m_begin, self.Last_0(), self.m_index)
        return self.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def NameMain(self):
        return self.m_name_main
    def NameSignal(self):
        return self.m_name_signal
    def FastMethod(self):
        return self.m_fast.MAMethod()
    def SlowMethod(self):
        return self.m_slow.MAMethod()
    def SignalMethod(self):
        return self.signal.MAMethod()
    def FastPeriod(self):
        return self.m_fast.MAPeriod()
    def SlowPeriod(self):
        return self.m_slow.MAPeriod()
    def SignalPeriod(self):
        return self.signal.MAPeriod()
    def __getitem__(self, index):
        return self.At(index)

__all__ = ['CMACDOnRingBuffer']
