"""catronringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CATROnRingBuffer(MqlObject):
    _q_fields = ('m_ma', 'm_tr', 'm_atr', 'm_name', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index', 'm_close', 'm_prev_close')
    def __init__(self):
        self.m_ma = CMAOnRingBuffer()
        self.m_tr = 0.0
        self.m_atr = 0.0
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
        self.m_close = 0.0
        self.m_prev_close = 0.0
    def _q_dtor(self):
        pass
    def Init(self, ma_period=14, ma_method=MODE_SMA, size_buffer=256, as_series=False):
        if not self.m_ma.Init(ma_period, ma_method, size_buffer):
            return False
        self.m_as_series = as_series
        self.m_bars_required = self.m_ma.BarsRequired() + 1
        self.m_name = 'ATR(' + IntegerToString(ma_period) + ',' + self.MAMethod() + ')'
        return True
    def MainOnArray(self, rates_total, prev_calculated, high, low, close):
        as_series_high = ArrayGetAsSeries(high)
        as_series_low = ArrayGetAsSeries(low)
        as_series_close = ArrayGetAsSeries(close)
        if as_series_high:
            ArraySetAsSeries(high, False)
        if as_series_low:
            ArraySetAsSeries(low, False)
        if as_series_close:
            ArraySetAsSeries(close, False)
        if prev_calculated == 0:
            for i in range(0, rates_total):
                if ((((high[i] != 0 and high[i] != EMPTY_VALUE) and low[i] != 0) and low[i] != EMPTY_VALUE) and close[i] != 0) and close[i] != EMPTY_VALUE:
                    self.m_start = MathMax(i + 1, rates_total - self.Size() - self.m_bars_required)
                    break
            self.m_begin = self.m_start
        else:
            self.m_start = prev_calculated - 1
        for i in range(self.m_start, rates_total):
            self.m_tr = MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])
            self.m_ma.MainOnValue(rates_total, prev_calculated, self.m_begin, self.m_tr, i)
        if as_series_high:
            ArraySetAsSeries(high, True)
        if as_series_low:
            ArraySetAsSeries(low, True)
        if as_series_close:
            ArraySetAsSeries(close, True)
        return rates_total
    def MainOnValue(self, rates_total, prev_calculated, begin, high, low, close, index):
        if self.m_as_series:
            self.m_index = rates_total - 1 - index
        else:
            self.m_index = index
        if self.m_index < begin:
            return EMPTY_VALUE
        if self.m_index == begin:
            self.m_close = close
            return EMPTY_VALUE
        if (prev_calculated - 1) != self.m_index:
            self.m_prev_close = close
        self.m_close = close
        self.m_tr = MathMax(high, self.m_prev_close) - MathMin(low, self.m_prev_close)
        self.m_ma.MainOnValue(rates_total, prev_calculated, begin + 1, self.m_tr, self.m_index)
        return self.m_ma.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def MAMethod(self):
        return self.m_ma.MAMethod()
    def MAPeriod(self):
        return self.m_ma.MAPeriod()
    def Size(self):
        return self.m_ma.Size()
    def __getitem__(self, index):
        return self.m_ma.At(index)

__all__ = ['CATROnRingBuffer']
