"""cosmaonringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_cmacdonringbuffer import *  # cmacdonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class COsMAOnRingBuffer(CArrayRing):
    _q_fields = ('m_macd', 'm_name', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index')
    def __init__(self):
        CArrayRing.__init__(self)
        self.m_macd = CMACDOnRingBuffer()
        self.m_name = ""
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
        if not self.m_macd.Init(fastperiod, slowperiod, signal_period, fast_method, slow_method, signal_method, sizebuffer):
            return False
        self.m_name = 'OsMA(' + self.m_macd.Name() + ')'
        self.m_as_series = as_series
        self.m_bars_required = self.m_macd.BarsRequired()
        return True
    def MainOnArray(self, rates_total, prev_calculated, array):
        self.m_macd.MainOnArray(rates_total, prev_calculated, array)
        if prev_calculated == 0:
            i = self.Size()
            while (i := i - 1) > 0:
                if self.m_macd[i] != 0 and self.m_macd[i] != EMPTY_VALUE:
                    break
            self.m_start = i
        else:
            self.m_start = rates_total - prev_calculated
        self.Last_1(self.m_macd[self.m_start] - self.m_macd.signal[self.m_start])
        for i in range(self.m_start - 1, 0 - 1, -1):
            self.Add(self.m_macd[i] - self.m_macd.signal[i])
        return rates_total
    def MainOnValue(self, rates_total, prev_calculated, begin, value, index):
        self.m_macd.MainOnValue(rates_total, prev_calculated, begin, value, index)
        if self.m_as_series:
            self.m_index = rates_total - 1 - index
        else:
            self.m_index = index
        if self.m_index < begin:
            return EMPTY_VALUE
        if (prev_calculated - 1) == self.m_index:
            self.Last_1(self.m_macd.Last_0() - self.m_macd.signal.Last_0())
        else:
            self.Add(self.m_macd.Last_0() - self.m_macd.signal.Last_0())
        return self.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def FastMethod(self):
        return self.m_macd.FastMethod()
    def SlowMethod(self):
        return self.m_macd.SlowMethod()
    def SignalMethod(self):
        return self.m_macd.SignalMethod()
    def FastPeriod(self):
        return self.m_macd.FastPeriod()
    def SlowPeriod(self):
        return self.m_macd.SlowPeriod()
    def SignalPeriod(self):
        return self.m_macd.SignalPeriod()
    def __getitem__(self, index):
        return self.At(index)

__all__ = ['COsMAOnRingBuffer']
