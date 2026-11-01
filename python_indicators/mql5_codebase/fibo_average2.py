"""Fibo_Average2 — converted from MQL5: MQL5 Indicators/Fibo_Average2/Fibo_Average2.mq5

Average given by the Fibonacci Sequence
And a MA based on that Line
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: FileReadLong, FileWriteLong
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [7451452], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fibo MA', 2: 'MA'}, 'levels': [], 'description': ['Average given by the Fibonacci Sequence', 'And a MA based on that Line'], 'name': 'Fibo_Average2', 'source': 'MQL5 Indicators/Fibo_Average2/Fibo_Average2.mq5', 'folder': 'Fibo_Average2', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 55, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'FiboMA applied price', 'sinput': False}, {'mql': 'InpCountFibo', 'py': 'InpCountFibo', 'param': 'InpCountFibo', 'type': 'uint', 'default': 11, 'label': 'Fibo count', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter

# enum ENUM_MA_MODE
METHOD_SMA = 0
METHOD_EMA = 1
METHOD_SMMA = 2
METHOD_LWMA = 3
METHOD_WILDER_EMA = 4
METHOD_SINE_WMA = 5
METHOD_TRI_MA = 6
METHOD_LSMA = 7
METHOD_HMA = 8
METHOD_ZL_EMA = 9
METHOD_ITREND_MA = 10
METHOD_MOVING_MEDIAN = 11
METHOD_GEO_MEAN = 12
METHOD_REMA = 13
METHOD_ILRS = 14
METHOD_IE_2 = 15
METHOD_TRI_MA_GEN = 16
METHOD_VWMA = 17
_enum('ENUM_MA_MODE', {0: 'METHOD_SMA', 1: 'METHOD_EMA', 2: 'METHOD_SMMA', 3: 'METHOD_LWMA', 4: 'METHOD_WILDER_EMA', 5: 'METHOD_SINE_WMA', 6: 'METHOD_TRI_MA', 7: 'METHOD_LSMA', 8: 'METHOD_HMA', 9: 'METHOD_ZL_EMA', 10: 'METHOD_ITREND_MA', 11: 'METHOD_MOVING_MEDIAN', 12: 'METHOD_GEO_MEAN', 13: 'METHOD_REMA', 14: 'METHOD_ILRS', 15: 'METHOD_IE_2', 16: 'METHOD_TRI_MA_GEN', 17: 'METHOD_VWMA'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 55)  # MA period
InpMethod = _input('InpMethod', METHOD_SMA)  # MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # FiboMA applied price
InpCountFibo = _input('InpCountFibo', 11)  # Fibo count
BufferFibo = Arr(0, 0.0)
BufferFiMA = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
period_ma = 0
weight_sum = 0
max_fibo_value = 0
handle_ma = 0

class CArray(CObject):
    _q_fields = ('m_step_resize', 'm_data_total', 'm_data_max', 'm_sort_mode')
    def __init__(self):
        CObject.__init__(self)
        self.m_step_resize = 0
        self.m_data_total = 0
        self.m_data_max = 0
        self.m_sort_mode = 0
        self.m_step_resize = 16
        self.m_data_total = 0
        self.m_data_max = 0
        self.m_sort_mode = -1
    def _q_dtor(self):
        pass
    def Step_0(self):
        return self.m_step_resize
    def Step_1(self, step):
        if step > 0:
            self.m_step_resize = step
            return True
        return False
    def Total(self):
        return self.m_data_total
    def Available(self):
        return self.m_data_max - self.m_data_total
    def Max(self):
        return self.m_data_max
    def IsSorted(self, mode=0):
        return self.m_sort_mode == mode
    def SortMode(self):
        return self.m_sort_mode
    def Clear(self):
        self.m_data_total = 0
    def Save(self, file_handle):
        if file_handle != INVALID_HANDLE:
            if _missing('FileWriteLong')(file_handle, -1) == 8:
                if FileWriteInteger(file_handle, self.Type(), INT_VALUE) == INT_VALUE:
                    return True
        return False
    def Load(self, file_handle):
        if file_handle != INVALID_HANDLE:
            if _missing('FileReadLong')(file_handle) == -1:
                if FileReadInteger(file_handle, INT_VALUE) == self.Type():
                    return True
        return False
    def Sort(self, mode=0):
        if self.IsSorted(mode):
            return
        self.m_sort_mode = mode
        if self.m_data_total <= 1:
            return
        self.QuickSort(0, self.m_data_total - 1, mode)
    def QuickSort(self, beg, end, mode=0):
        self.m_sort_mode = -1
    def Minimum(self, data, start, count):
        real_count = 0
        if self.m_data_total < 1:
            SetUserError(1000)
            return -1
        if start < 0 or start >= self.m_data_total:
            SetUserError(3)
            return -1
        real_count = ((self.m_data_total - start) if (count == WHOLE_ARRAY or (start + count) > self.m_data_total) else count)
        return ArrayMinimum(data, start, real_count)
    def Maximum(self, data, start, count):
        real_count = 0
        if self.m_data_total < 1:
            SetUserError(1000)
            return -1
        if start < 0 or start >= self.m_data_total:
            SetUserError(3)
            return -1
        real_count = ((self.m_data_total - start) if (count == WHOLE_ARRAY or (start + count) > self.m_data_total) else count)
        return ArrayMaximum(data, start, real_count)

class CArrayInt(CArray):
    _q_fields = ('m_data',)
    def __init__(self):
        CArray.__init__(self)
        self.m_data = Arr(0, 0)
        self.m_data_max = ArraySize(self.m_data)
    def _q_dtor(self):
        if self.m_data_max != 0:
            self.Shutdown()
    def Type(self):
        return TYPE_INT
    def Save(self, file_handle):
        i = 0
        if not CArray.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, self.m_data_total):
            if FileWriteInteger(file_handle, self.m_data[i], INT_VALUE) != INT_VALUE:
                break
        else:
            i = _range_end(i, self.m_data_total, 1)
        return i == self.m_data_total
    def Load(self, file_handle):
        i = 0
        num = 0
        if not CArray.Load(self, file_handle):
            return False
        num = FileReadInteger(file_handle, INT_VALUE)
        self.Clear()
        if num != 0:
            if not self.Reserve(num):
                return False
            i = 0
            for i in range(i, num):
                self.m_data[i] = FileReadInteger(file_handle, INT_VALUE)
                self.m_data_total += 1
                if FileIsEnding(file_handle):
                    break
            else:
                i = _range_end(i, num, 1)
        self.m_sort_mode = -1
        return self.m_data_total == num
    def Reserve(self, size):
        new_size = 0
        if size <= 0:
            return False
        if self.Available() < size:
            new_size = self.m_data_max + (self.m_step_resize * (1 + _idiv(size - self.Available(), self.m_step_resize)))
            if new_size < 0:
                return False
            if _setattr(self, 'm_data_max', ArrayResize(self.m_data, new_size)) == -1:
                self.m_data_max = ArraySize(self.m_data)
        return self.Available() >= size
    def Resize(self, size):
        new_size = 0
        if size < 0:
            return False
        new_size = self.m_step_resize * (1 + _idiv(size, self.m_step_resize))
        if self.m_data_max != new_size:
            if _setattr(self, 'm_data_max', ArrayResize(self.m_data, new_size)) == -1:
                self.m_data_max = ArraySize(self.m_data)
                return False
        if self.m_data_total > size:
            self.m_data_total = size
        return self.m_data_max == new_size
    def Shutdown(self):
        if self.m_data_max == 0:
            return True
        if ArrayResize(self.m_data, 0) == -1:
            return False
        self.m_data_total = 0
        self.m_data_max = 0
        return True
    def Add(self, element):
        if not self.Reserve(1):
            return False
        self.m_data[_incattr(self, 'm_data_total', 1, True)] = element
        self.m_sort_mode = -1
        return True
    def AddArray_1(self, src):
        num = ArraySize(src)
        if not self.Reserve(num):
            return False
        for i in range(0, num):
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = src[i]
        self.m_sort_mode = -1
        return True
    def AddArray_2(self, src):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.Total()
        if not self.Reserve(num):
            return False
        for i in range(0, num):
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = src.m_data[i]
        self.m_sort_mode = -1
        return True
    def Insert(self, element, pos):
        if pos < 0 or (not self.Reserve(1)):
            return False
        self.m_data_total += 1
        if pos < (self.m_data_total - 1):
            if self.MemMove(pos + 1, pos, self.m_data_total - pos - 1) < 0:
                return False
            self.m_data[pos] = element
        else:
            self.m_data[self.m_data_total - 1] = element
        self.m_sort_mode = -1
        return True
    def InsertArray_1(self, src, pos):
        num = ArraySize(src)
        if not self.Reserve(num):
            return False
        if self.MemMove(num + pos, pos, self.m_data_total - pos) < 0:
            return False
        for i in range(0, num):
            self.m_data[i + pos] = src[i]
        self.m_sort_mode = -1
        return True
    def InsertArray_2(self, src, pos):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.Total()
        if not self.Reserve(num):
            return False
        if self.MemMove(num + pos, pos, self.m_data_total - pos) < 0:
            return False
        for i in range(0, num):
            self.m_data[i + pos] = src.m_data[i]
        self.m_sort_mode = -1
        return True
    def AssignArray_1(self, src):
        num = ArraySize(src)
        self.Clear()
        if self.m_data_max < num:
            if not self.Reserve(num):
                return False
        else:
            self.Resize(num)
        for i in range(0, num):
            self.m_data[i] = src[i]
            self.m_data_total += 1
        self.m_sort_mode = -1
        return True
    def AssignArray_2(self, src):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.m_data_total
        self.Clear()
        if self.m_data_max < num:
            if not self.Reserve(num):
                return False
        else:
            self.Resize(num)
        for i in range(0, num):
            self.m_data[i] = src.m_data[i]
            self.m_data_total += 1
        self.m_sort_mode = src.SortMode()
        return True
    def At(self, index):
        if index < 0 or index >= self.m_data_total:
            return INT_MAX
        return self.m_data[index]
    def __getitem__(self, index):
        return self.At(index)
    def Minimum(self, start, count):
        return CArray.Minimum(self, self.m_data, start, count)
    def Maximum(self, start, count):
        return CArray.Maximum(self, self.m_data, start, count)
    def Update(self, index, element):
        if index < 0 or index >= self.m_data_total:
            return False
        self.m_data[index] = element
        self.m_sort_mode = -1
        return True
    def Shift(self, index, shift):
        tmp_int = 0
        if (index < 0 or (index + shift) < 0) or (index + shift) >= self.m_data_total:
            return False
        if shift == 0:
            return True
        tmp_int = self.m_data[index]
        if shift > 0:
            if self.MemMove(index, index + 1, shift) < 0:
                return False
        else:
            if self.MemMove(index + shift + 1, index + shift, -shift) < 0:
                return False
        self.m_data[index + shift] = tmp_int
        self.m_sort_mode = -1
        return True
    def Delete(self, index):
        if index < 0 or index >= self.m_data_total:
            return False
        if index < (self.m_data_total - 1) and self.MemMove(index, index + 1, self.m_data_total - index - 1) < 0:
            return False
        self.m_data_total -= 1
        return True
    def DeleteRange(self, from_, to):
        if from_ < 0 or to < 0:
            return False
        if from_ > to or from_ >= self.m_data_total:
            return False
        if to >= (self.m_data_total - 1):
            to = self.m_data_total - 1
        if self.MemMove(from_, to + 1, self.m_data_total - to - 1) < 0:
            return False
        self.m_data_total -= to - from_ + 1
        return True
    def CompareArray_1(self, array):
        if self.m_data_total != ArraySize(array):
            return False
        for i in range(0, self.m_data_total):
            if self.m_data[i] != array[i]:
                return False
        return True
    def CompareArray_2(self, array):
        if not CheckPointer(array):
            return False
        if self.m_data_total != array.m_data_total:
            return False
        for i in range(0, self.m_data_total):
            if self.m_data[i] != array.m_data[i]:
                return False
        return True
    def InsertSort(self, element):
        pos = 0
        if not self.IsSorted():
            return False
        if not self.Reserve(1):
            return False
        if self.m_data_total == 0:
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = element
            return True
        pos = self.QuickSearch(element)
        if self.m_data[pos] > element:
            self.Insert(element, pos)
        else:
            self.Insert(element, pos + 1)
        self.m_sort_mode = 0
        return True
    def Search(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos] == element:
            return pos
        return -1
    def SearchGreat(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos] <= element:
            if (pos := pos + 1) == self.m_data_total:
                return -1
        return pos
    def SearchLess(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos] >= element:
            if ((pos := pos - 1) + 1) == 0:
                return -1
        return pos
    def SearchGreatOrEqual(self, element):
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        for pos in range(self.QuickSearch(element), self.m_data_total):
            if self.m_data[pos] >= element:
                return pos
        return -1
    def SearchLessOrEqual(self, element):
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        for pos in range(self.QuickSearch(element), 0 - 1, -1):
            if self.m_data[pos] <= element:
                return pos
        return -1
    def SearchFirst(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos] == element:
            while self.m_data[pos] == element:
                if ((pos := pos - 1) + 1) == 0:
                    break
            return pos + 1
        return -1
    def SearchLast(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos] == element:
            while self.m_data[pos] == element:
                if (pos := pos + 1) == self.m_data_total:
                    break
            return pos - 1
        return -1
    def SearchLinear(self, element):
        if self.m_data_total == 0:
            return -1
        for i in range(0, self.m_data_total):
            if self.m_data[i] == element:
                return i
        return -1
    def QuickSort(self, beg, end, mode=0):
        i = 0
        j = 0
        p_int = 0
        t_int = 0
        if beg < 0 or end < 0:
            return
        i = beg
        j = end
        while i < end:
            p_int = self.m_data[(beg + end) >> 1]
            while i < j:
                while self.m_data[i] < p_int:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                while self.m_data[j] > p_int:
                    if j == 0:
                        break
                    j -= 1
                if i <= j:
                    t_int = self.m_data[i]
                    self.m_data[((i := i + 1) - 1)] = self.m_data[j]
                    self.m_data[j] = t_int
                    if j == 0:
                        break
                    j -= 1
            if beg < j:
                self.QuickSort(beg, j)
            beg = i
            j = end
    def QuickSearch(self, element):
        i = 0
        j = 0
        m = -1
        t_int = 0
        i = 0
        j = self.m_data_total - 1
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m >= self.m_data_total:
                break
            t_int = self.m_data[m]
            if t_int == element:
                break
            if t_int > element:
                j = m - 1
            else:
                i = m + 1
        return m
    def MemMove(self, dest, src, count):
        i = 0
        if (dest < 0 or src < 0) or count < 0:
            return -1
        if (src + count) > self.m_data_total:
            count = self.m_data_total - src
        if count < 0:
            return -1
        if dest == src or count == 0:
            return dest
        if (dest + count) > self.m_data_total:
            if self.m_data_max < (dest + count):
                return -1
            self.m_data_total = dest + count
        if dest < src:
            i = 0
            for i in range(i, count):
                self.m_data[dest + i] = self.m_data[src + i]
            else:
                i = _range_end(i, count, 1)
        else:
            i = count - 1
            for i in range(i, 0 - 1, -1):
                self.m_data[dest + i] = self.m_data[src + i]
            else:
                i = _range_end(i, 0 - 1, -1)
        return dest

def OnInit():
    global handle_ma, max_fibo_value, period_ma
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    count_fibo = (2 if (InpCountFibo < 2) else InpCountFibo)
    array_fibo_numbers.Sort()
    array_fibo_numbers.Clear()
    array_fibo_numbers.Insert(0, 0)
    array_fibo_numbers.Insert(1, 1)
    if count_fibo > 2:
        for i in range(2, count_fibo - 1 + 1):
            value = array_fibo_numbers.At(i - 2) + array_fibo_numbers.At(i - 1)
            array_fibo_numbers.Insert(value, i)
    max_fibo_value = array_fibo_numbers.At(array_fibo_numbers.Total() - 1)
    total = array_fibo_numbers.Total()
    SetIndexBuffer(0, BufferFibo, INDICATOR_DATA)
    SetIndexBuffer(1, BufferFiMA, INDICATOR_DATA)
    SetIndexBuffer(2, BufferPrice, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fibo averages2 (period: ' + _str(period_ma) + ', levels: ' + _str(array_fibo_numbers.Total()) + ' --> bars: ' + _str(max_fibo_value) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, max_fibo_value)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, max_fibo_value + period_ma - 1)
    PlotIndexSetString(0, PLOT_LABEL, 'Fibo MA(' + _str(array_fibo_numbers.Total()) + ')')
    PlotIndexSetString(1, PLOT_LABEL, MethodToString(InpMethod) + '(' + _str(period_ma) + ')')
    ArraySetAsSeries(BufferFibo, True)
    ArraySetAsSeries(BufferFiMA, True)
    ArraySetAsSeries(BufferPrice, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(max_fibo_value, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - max_fibo_value - 1
        ArrayInitialize(BufferFibo, 0)
        ArrayInitialize(BufferFiMA, 0)
        ArrayInitialize(BufferPrice, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferPrice)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        sum_ = 0.0
        total = array_fibo_numbers.Total() - 1
        for j in range(1, total + 1):
            sum_ += BufferPrice[i + array_fibo_numbers.At(j)]
        BufferFibo[i] = _fdiv(sum_, total)
    for i in range(limit, 0 - 1, -1):
        _sw1 = InpMethod
        if _sw1 == METHOD_EMA:
            BufferFiMA[i] = EMA(rates_total, BufferFibo[i], BufferFiMA[i + 1], period_ma, i)
        elif _sw1 == METHOD_SMMA:
            BufferFiMA[i] = SMMA(rates_total, BufferFibo, BufferFiMA[i + 1], period_ma, i)
        elif _sw1 == METHOD_LWMA:
            BufferFiMA[i] = LWMA(rates_total, BufferFibo, period_ma, i)
        elif _sw1 == METHOD_WILDER_EMA:
            BufferFiMA[i] = Wilder(rates_total, BufferFibo[i], BufferFiMA[i + 1], period_ma, i)
        elif _sw1 == METHOD_SINE_WMA:
            BufferFiMA[i] = SineWMA(rates_total, BufferFibo, period_ma, i)
        elif _sw1 == METHOD_TRI_MA:
            BufferFiMA[i] = TriMA(rates_total, BufferFibo, period_ma, i)
        elif _sw1 == METHOD_LSMA:
            BufferFiMA[i] = LSMA(rates_total, BufferFibo, period_ma, i)
        elif _sw1 == METHOD_HMA:
            BufferFiMA[i] = HMA(rates_total, BufferFibo, period_ma, i)
        elif _sw1 == METHOD_ZL_EMA:
            BufferFiMA[i] = ZeroLagEMA(rates_total, BufferFibo, BufferFiMA[i + 1], period_ma, i)
        elif _sw1 == METHOD_ITREND_MA:
            BufferFiMA[i] = ITrend(rates_total, BufferFibo, BufferFiMA, period_ma, i)
        elif _sw1 == METHOD_MOVING_MEDIAN:
            BufferFiMA[i] = Median(rates_total, BufferFibo, period_ma, i)
        elif _sw1 == METHOD_GEO_MEAN:
            BufferFiMA[i] = GeoMean(rates_total, BufferFibo, period_ma, i)
        elif _sw1 == METHOD_REMA:
            BufferFiMA[i] = REMA(rates_total, BufferFibo[i], BufferFiMA, period_ma, 0.5, i)
        elif _sw1 == METHOD_ILRS:
            BufferFiMA[i] = ILRS(rates_total, BufferFibo, period_ma, i)
        elif _sw1 == METHOD_IE_2:
            BufferFiMA[i] = IE2(rates_total, BufferFibo, period_ma, i)
        elif _sw1 == METHOD_TRI_MA_GEN:
            BufferFiMA[i] = TriMA_gen(rates_total, BufferFibo, period_ma, i)
        elif _sw1 == METHOD_VWMA:
            BufferFiMA[i] = VWMA(rates_total, BufferFibo, tick_volume, period_ma, i)
        else:
            BufferFiMA[i] = SMA(rates_total, BufferFibo, period_ma, i)
    return rates_total

def SMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return array_src[shift]
    sum_ = 0.0
    for i in range(0, period):
        sum_ += array_src[shift + i]
    return _fdiv(sum_, period)

def EMA(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + (_fdiv(2.0, 1 + period) * (price - prev))))

def Wilder(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + _fdiv(price - prev, period)))

def LWMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += period - i
        sum_ += array_src[shift + i] * (period - i)
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def SineWMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += sin(_fdiv(M_PI * (i + 1), period + 1))
        sum_ += array_src[shift + i] * sin(_fdiv(M_PI * (i + 1), period + 1))
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def TriMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sma = 0.0
    len_ = _int(ceil((period + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len_):
        sma = SMA(rates_total, array_src, len_, shift + i)
        sum_ += sma
    trima = _fdiv(sum_, len_)
    return trima

def LSMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    for i in range(period, 1 - 1, -1):
        sum_ += (i - ((period + 1) / 3.0)) * array_src[shift + period - i]
    lsma = _fdiv(sum_ * 6.0, period * (period + 1))
    return lsma

def SMMA(rates_total, array_src, prev, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    smma = 0.0
    if shift == (rates_total - period - 1):
        smma = SMA(rates_total, array_src, period, shift)
    elif shift < (rates_total - period - 1):
        sum_ = 0.0
        for i in range(0, period):
            sum_ += array_src[shift + i + 1]
        smma = _fdiv(sum_ - prev + array_src[shift], period)
    return smma

def HMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    tmp1 = Arr(0, 0.0)
    hma = 0.0
    len_ = _int(sqrt(period))
    ArrayResize(tmp1, len_)
    if shift == (rates_total - period - 1):
        hma = array_src[shift]
    elif shift < (rates_total - period - 1):
        for i in range(0, len_):
            tmp1[i] = (2.0 * LWMA(rates_total, array_src, _idiv(period, 2), shift + i)) - LWMA(rates_total, array_src, period, shift + i)
        hma = LWMA(rates_total, tmp1, len_, 0)
    return hma

def ZeroLagEMA(rates_total, array_src, prev, period, shift):
    alfa = _fdiv(2.0, 1 + period)
    lag = _int(0.5 * (period - 1))
    return (array_src[shift] if (shift >= (rates_total - lag)) else ((alfa * ((2.0 * array_src[shift]) - array_src[shift + lag])) + ((1 - alfa) * prev)))

def ITrend(rates_total, array_src, array, period, shift):
    alfa = _fdiv(2.0, period + 1)
    return ((((alfa - (0.25 * alfa * alfa)) * array_src[shift]) + (0.5 * alfa * alfa * array_src[shift + 1]) - ((alfa - (0.75 * alfa * alfa)) * array_src[shift + 2]) + (2 * (1 - alfa) * array[shift + 1]) - ((1 - alfa) * (1 - alfa) * array[shift + 2])) if (shift < (rates_total - 7)) else ((array_src[shift] + (2 * array_src[shift + 1]) + array_src[shift + 2]) / 4.0))

def Median(rates_total, array_src, period, shift):
    if period < 2 or shift > (rates_total - period - 1):
        return 0.0
    array = Arr(0, 0.0)
    ArrayResize(array, period)
    for i in range(0, period):
        array[i] = array_src[shift + i]
    ArraySort(array)
    num = _int(round(_idiv(period - 1, 2)))
    return (array_src[num] if (fmod(period, 2) > 0) else (0.5 * (array_src[num] + array[num + 1])))

def GeoMean(rates_total, array_src, period, shift):
    gmean = 0.0
    if shift < (rates_total - period):
        gmean = pow(array_src[shift], _fdiv(1.0, period))
        for i in range(1, period):
            gmean *= pow(array_src[shift + i], _fdiv(1.0, period))
    return gmean

def REMA(rates_total, price, array, period, lambda_, shift):
    alpha = _fdiv(2.0, period + 1)
    return (price if (shift >= (rates_total - 3)) else _fdiv((array[shift + 1] * (1 + (2 * lambda_))) + (alpha * (price - array[shift + 1])) - (lambda_ * array[shift + 2]), 1 + lambda_))

def ILRS(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = period * (period - 1) * 0.5
    sum2 = ((period - 1) * period * ((2 * period) - 1)) / 6.0
    sum1 = 0.0
    sumy = 0.0
    for i in range(0, period):
        sum1 += i * array_src[shift + i]
        sumy += array_src[shift + i]
    num1 = (period * sum1) - (sum_ * sumy)
    num2 = (sum_ * sum_) - (period * sum2)
    slope = (_fdiv(num1, num2) if (num2 != 0) else 0)
    return slope + SMA(rates_total, array_src, period, shift)

def IE2(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    return 0.5 * (ILRS(rates_total, array_src, period, shift) + LSMA(rates_total, array_src, period, shift))

def TriMA_gen(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    len1 = _int(floor((period + 1) * 0.5))
    len2 = _int(ceil((period + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len2):
        sum_ += SMA(rates_total, array_src, len1, shift + i)
    return _fdiv(sum_, len2)

def VWMA(rates_total, array_src, volume, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += float(volume[shift + i])
        sum_ += array_src[shift + i] * volume[shift + i]
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def MethodToString(method):
    return StringSubstr(EnumToString(method, 'ENUM_MA_MODE'), 7)

# ---- global variables initialised from expressions
array_fibo_numbers = _alloc(CArrayInt)
array_fibo_numbers.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FiboAverage2(_MQL5Indicator):
    name = 'Fibo_Average2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 55,  # MA period
        'InpMethod': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=0),  # MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # FiboMA applied price
        'InpCountFibo': 11,  # Fibo count
    }

