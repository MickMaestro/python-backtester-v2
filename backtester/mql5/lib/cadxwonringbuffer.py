"""cadxwonringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CADXWOnRingBuffer(MqlObject):
    _q_fields = ('pdi', 'ndi', 'm_adxw', 'm_pds', 'm_nds', 'm_atr', 'm_name', 'm_as_series', 'm_bars_required', 'm_begin', 'm_start', 'm_index', 'm_high', 'm_low', 'm_close', 'm_phigh', 'm_plow', 'm_pclose', 'm_PD', 'm_ND')
    def __init__(self):
        self.pdi = CArrayRing()
        self.ndi = CArrayRing()
        self.m_adxw = CMAOnRingBuffer()
        self.m_pds = CMAOnRingBuffer()
        self.m_nds = CMAOnRingBuffer()
        self.m_atr = CMAOnRingBuffer()
        self.m_name = ""
        self.m_as_series = False
        self.m_bars_required = 0
        self.m_begin = 0
        self.m_start = 0
        self.m_index = 0
        self.m_high = 0.0
        self.m_low = 0.0
        self.m_close = 0.0
        self.m_phigh = 0.0
        self.m_plow = 0.0
        self.m_pclose = 0.0
        self.m_PD = 0.0
        self.m_ND = 0.0
    def _q_dtor(self):
        pass
    def Init(self, ma_period=14, ma_method=MODE_SMMA, size_buffer=256, as_series=False):
        if not self.pdi.Init(size_buffer):
            return False
        if not self.ndi.Init(size_buffer):
            return False
        if not self.m_atr.Init(ma_period, ma_method, size_buffer):
            return False
        if not self.m_pds.Init(ma_period, ma_method, size_buffer):
            return False
        if not self.m_nds.Init(ma_period, ma_method, size_buffer):
            return False
        if not self.m_adxw.Init(ma_period, ma_method, size_buffer):
            return False
        self.m_name = '(' + IntegerToString(ma_period) + ',' + self.MAMethod() + ')'
        self.m_as_series = as_series
        self.m_bars_required = self.m_adxw.BarsRequired() + 1
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
        self.m_index = self.m_start
        while self.m_index < rates_total:
            self.m_phigh = high[self.m_index - 1]
            self.m_plow = low[self.m_index - 1]
            self.m_pclose = close[self.m_index - 1]
            self.m_high = high[self.m_index]
            self.m_low = low[self.m_index]
            self.ADXW(rates_total, prev_calculated)
            self.m_index += 1
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
            self.m_high = high
            self.m_low = low
            self.m_close = close
            self.m_begin = begin + 1
            return EMPTY_VALUE
        if (prev_calculated - 1) != self.m_index:
            self.m_phigh = self.m_high
            self.m_plow = self.m_low
            self.m_pclose = self.m_close
        self.m_high = high
        self.m_low = low
        self.m_close = close
        self.ADXW(rates_total, prev_calculated)
        return self.m_adxw.Last_0()
    def BarsRequired(self):
        return self.m_bars_required
    def NameADXW(self):
        return 'ADX Wilder' + self.m_name
    def NameNDI(self):
        return '-DI' + self.m_name
    def NamePDI(self):
        return '+DI' + self.m_name
    def MAMethod(self):
        return self.m_adxw.MAMethod()
    def MAPeriod(self):
        return self.m_adxw.MAPeriod()
    def Size(self):
        return self.m_adxw.Size()
    def __getitem__(self, index):
        return self.m_adxw.At(index)
    def ADXW(self, rates_total, prev_calculated):
        dTmpP = self.m_high - self.m_phigh
        dTmpN = self.m_plow - self.m_low
        if dTmpP < 0.0:
            dTmpP = 0.0
        if dTmpN < 0.0:
            dTmpN = 0.0
        if dTmpP > dTmpN:
            dTmpN = 0.0
        else:
            if dTmpP < dTmpN:
                dTmpP = 0.0
            else:
                dTmpP = 0.0
                dTmpN = 0.0
        tr = MathMax(MathMax(MathAbs(self.m_high - self.m_low), MathAbs(self.m_high - self.m_pclose)), MathAbs(self.m_low - self.m_pclose))
        tr = self.m_atr.MainOnValue(rates_total, prev_calculated, self.m_begin, tr, self.m_index)
        dTmpP = self.m_pds.MainOnValue(rates_total, prev_calculated, self.m_begin, dTmpP, self.m_index)
        dTmpN = self.m_nds.MainOnValue(rates_total, prev_calculated, self.m_begin, dTmpN, self.m_index)
        if tr == EMPTY_VALUE:
            tr = 0.0
        if dTmpP == EMPTY_VALUE:
            dTmpP = 0.0
        if dTmpN == EMPTY_VALUE:
            dTmpN = 0.0
        if self.m_index == (prev_calculated - 1):
            if tr != 0.0 or tr != EMPTY_VALUE:
                self.pdi.Last_1(_fdiv(100.0 * dTmpP, tr))
                self.ndi.Last_1(_setattr(self, 'm_ND', _fdiv(100.0 * dTmpN, tr)))
            else:
                self.pdi.Last_1(0.0)
                self.ndi.Last_1(0.0)
        else:
            if tr != 0.0:
                self.pdi.Add(_fdiv(100.0 * dTmpP, tr))
                self.ndi.Add(_setattr(self, 'm_ND', _fdiv(100.0 * dTmpN, tr)))
            else:
                self.pdi.Add(0.0)
                self.ndi.Add(0.0)
        dTmp = self.pdi.Last_0() + self.ndi.Last_0()
        if dTmp != 0.0:
            dTmp = 100.0 * MathAbs(_fdiv(self.pdi.Last_0() - self.ndi.Last_0(), dTmp))
        else:
            dTmp = 0.0
        self.m_adxw.MainOnValue(rates_total, prev_calculated, self.m_begin, dTmp, self.m_index)

__all__ = ['CADXWOnRingBuffer']
