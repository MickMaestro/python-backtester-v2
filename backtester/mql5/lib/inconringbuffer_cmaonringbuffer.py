"""cmaonringbuffer.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.inconringbuffer_carrayring import *  # carrayring.mqh


class CMAOnRingBuffer(CArrayRing):
    _q_fields = ('m_array_in', 'm_ma_period', 'm_ma_method', 'm_as_series', 'm_k1', 'm_k2', 'm_LK', 'm_name', 'm_bars_required', 'm_start', 'm_index')
    _q_ptrs = ('m_array_in',)
    def __init__(self):
        CArrayRing.__init__(self)
        self.m_array_in = None
        self.m_ma_period = 0
        self.m_ma_method = 0
        self.m_as_series = False
        self.m_k1 = 0.0
        self.m_k2 = 0.0
        self.m_LK = Arr(0, 0.0)
        self.m_name = ""
        self.m_bars_required = 0
        self.m_start = 0
        self.m_index = 0
    def _q_dtor(self):
        if CheckPointer(self.m_array_in) != POINTER_INVALID:
            _delete(self.m_array_in)
    def Init(self, ma_period=14, ma_method=MODE_SMA, size_buffer=256, as_series=False):
        if ma_period <= 0:
            self.m_ma_period = 14
            printf('Input parameter ma_period has incorrect value (%d). Indicator will use value %d for calculations.', ma_period, self.m_ma_period)
        else:
            self.m_ma_period = ma_period
        if size_buffer <= self.m_ma_period:
            printf('Input parameter size_buffer has incorrect value (%d). Indicator will use value %d for calculations.', size_buffer, self.m_ma_period)
            size_buffer = self.m_ma_period
        if not CArrayRing.Init(self, size_buffer):
            return False
        coeff_required = 10
        self.m_as_series = as_series
        self.m_ma_method = ma_method
        _sw1 = self.m_ma_method
        if _sw1 == MODE_SMA:
            self.m_bars_required = self.m_ma_period
        elif _sw1 == MODE_EMA:
            self.m_k1 = _fdiv(2.0, self.m_ma_period + 1.0)
            self.m_k2 = 1.0 - self.m_k1
            self.m_bars_required = self.m_ma_period * coeff_required
        elif _sw1 == MODE_SMMA:
            self.m_k1 = _fdiv(1.0, self.m_ma_period)
            self.m_k2 = 1.0 - self.m_k1
            self.m_bars_required = self.m_ma_period * coeff_required
        elif _sw1 == MODE_LWMA:
            ArrayResize(self.m_LK, self.m_ma_period)
            sum_ = 0.0
            for j in range(0, self.m_ma_period):
                sum_ += _setitem(self.m_LK, j, self.m_ma_period - j)
            for j in range(0, self.m_ma_period):
                self.m_LK[j] = _fdiv(self.m_LK[j], sum_)
            sum_ = 0.0
            for j in range(0, self.m_ma_period):
                sum_ += self.m_LK[j]
            self.m_bars_required = self.m_ma_period
        else:
            pass
        self.m_name = self.MethodToString(self.m_ma_method) + '(' + IntegerToString(self.m_ma_period) + ')'
        return True
    def MainOnArray(self, rates_total, prev_calculated, array):
        as_series = ArrayGetAsSeries(array)
        if as_series:
            ArraySetAsSeries(array, False)
        _sw2 = self.m_ma_method
        if _sw2 == MODE_SMA:
            self.SMAOnArray(rates_total, prev_calculated, array)
        elif _sw2 in (MODE_EMA, MODE_SMMA):
            self.EMAOnArray(rates_total, prev_calculated, array)
        elif _sw2 == MODE_LWMA:
            self.LWMAOnArray(rates_total, prev_calculated, array)
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
        _sw3 = self.m_ma_method
        if _sw3 == MODE_SMA:
            return self.SMAOnValue(prev_calculated, begin, value, index)
        elif _sw3 in (MODE_EMA, MODE_SMMA):
            return self.EMAOnValue(prev_calculated, begin, value, index)
        elif _sw3 == MODE_LWMA:
            return self.LWMAOnValue(prev_calculated, begin, value, index)
        return EMPTY_VALUE
    def BarsRequired(self):
        return self.m_bars_required
    def Name(self):
        return self.m_name
    def MAMethod(self):
        return self.MethodToString(self.m_ma_method)
    def MAPeriod(self):
        return self.m_ma_period
    def __getitem__(self, index):
        return self.At(index)
    def SMAOnArray(self, rates_total, prev_calculated, array):
        if prev_calculated == 0:
            self.m_start = self.Begin(rates_total, array) + self.m_ma_period - 1
            sum_ = 0.0
            for i in range(self.m_start, self.m_start - self.m_ma_period, -1):
                sum_ += array[i]
            self.Last_1(_fdiv(sum_, self.m_ma_period))
        else:
            self.m_start = prev_calculated - 1
            self.Last_1(self.At(1) - _fdiv(array[self.m_start - self.m_ma_period] - array[self.m_start], self.m_ma_period))
        for i in range(self.m_start + 1, rates_total):
            self.Add(self.Last_0() - _fdiv(array[i - self.m_ma_period] - array[i], self.m_ma_period))
    def EMAOnArray(self, rates_total, prev_calculated, array):
        if prev_calculated == 0:
            self.m_start = self.Begin(rates_total, array)
            self.Last_1(array[self.m_start])
        else:
            self.m_start = prev_calculated - 1
            self.Last_1((self.m_k1 * array[self.m_start]) + (self.m_k2 * self.At(1)))
        for i in range(self.m_start + 1, rates_total):
            self.Add((self.m_k1 * array[i]) + (self.m_k2 * self.Last_0()))
    def LWMAOnArray(self, rates_total, prev_calculated, array):
        if prev_calculated == 0:
            self.m_start = self.Begin(rates_total, array) + self.m_ma_period - 1
        else:
            self.m_start = prev_calculated - 1
        volue = 0.0
        for j in range(0, self.m_ma_period):
            volue += array[self.m_start - j] * self.m_LK[j]
        self.Last_1(volue)
        for i in range(self.m_start + 1, rates_total):
            volue = 0.0
            for j in range(0, self.m_ma_period):
                volue += array[i - j] * self.m_LK[j]
            self.Add(volue)
    def SMAOnValue(self, prev_calculated, begin, value, index):
        if not self.FillArrayIn(prev_calculated, value):
            return EMPTY_VALUE
        self.m_start = begin + self.m_ma_period - 1
        if self.m_index < self.m_start:
            return EMPTY_VALUE
        elif self.m_index == self.m_start:
            sum_ = 0.0
            for i in range(0, self.m_ma_period):
                sum_ += self.m_array_in[i]
            self.Last_1(_fdiv(sum_, self.m_ma_period))
            return self.Last_0()
        if (prev_calculated - 1) == self.m_index:
            self.Last_1(self.At(1) - _fdiv(self.m_array_in[self.m_ma_period] - value, self.m_ma_period))
        else:
            self.Add(self.Last_0() - _fdiv(self.m_array_in[self.m_ma_period] - value, self.m_ma_period))
        return self.Last_0()
    def EMAOnValue(self, prev_calculated, begin, value, index):
        if self.m_index == begin:
            self.Last_1(value)
            return value
        if (prev_calculated - 1) == self.m_index:
            self.Last_1((self.m_k1 * value) + (self.m_k2 * self.At(1)))
        else:
            self.Add((self.m_k1 * value) + (self.m_k2 * self.Last_0()))
        return self.Last_0()
    def LWMAOnValue(self, prev_calculated, begin, value, index):
        if not self.FillArrayIn(prev_calculated, value):
            return EMPTY_VALUE
        if self.m_index < (begin + self.m_ma_period - 1):
            return EMPTY_VALUE
        volue = 0.0
        for j in range(0, self.m_ma_period):
            volue += self.m_array_in[j] * self.m_LK[j]
        if (prev_calculated - 1) == self.m_index:
            self.Last_1(volue)
        else:
            self.Add(volue)
        return self.Last_0()
    def Begin(self, rates_total, array):
        i = -1
        while (i := i + 1) < rates_total:
            if array[i] != 0 and array[i] != EMPTY_VALUE:
                break
        return MathMax(i, rates_total - self.Size() - self.m_bars_required)
    def FillArrayIn(self, prev_calculated, value):
        if CheckPointer(self.m_array_in) == POINTER_INVALID:
            if _setattr(self, 'm_array_in', CArrayRing()) is None:
                return False
            if not self.m_array_in.Init(self.Size()):
                return False
        if (prev_calculated - 1) == self.m_index:
            self.m_array_in.Last_1(value)
        else:
            self.m_array_in.Add(value)
        return True
    def MethodToString(self, method):
        _sw4 = method
        if _sw4 == MODE_SMA:
            return 'SMA'
        elif _sw4 == MODE_EMA:
            return 'EMA'
        elif _sw4 == MODE_LWMA:
            return 'LWMA'
        elif _sw4 == MODE_SMMA:
            return 'SMMA'
        return EnumToString(method, 'ENUM_MA_METHOD')

__all__ = ['CMAOnRingBuffer']
