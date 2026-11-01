"""xMASumAvg — converted from MQL5: MQL5 Indicators/xMASumAvg/xMASumAvg.mq5

X MA Sum Average indicator
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

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'XMA Average'}, 'levels': [], 'description': ['X MA Sum Average indicator'], 'name': 'xMASumAvg', 'source': 'MQL5 Indicators/xMASumAvg/xMASumAvg.mq5', 'folder': 'xMASumAvg', 'inputs': [{'mql': 'InpPeriodBeg', 'py': 'InpPeriodBeg', 'param': 'InpPeriodBeg', 'type': 'uint', 'default': 20, 'label': 'Initial period', 'sinput': False}, {'mql': 'InpPeriodEnd', 'py': 'InpPeriodEnd', 'param': 'InpPeriodEnd', 'type': 'uint', 'default': 100, 'label': 'End period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
InpPeriodBeg = _input('InpPeriodBeg', 20)  # Initial period
InpPeriodEnd = _input('InpPeriodEnd', 100)  # End period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferXMA = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
cnt = 0
period_beg = 0
period_end = 0

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

class CArrayObj(CArray):
    _q_fields = ('m_data', 'm_free_mode')
    _q_ptrs = ('m_data',)
    def __init__(self):
        CArray.__init__(self)
        self.m_data = Arr(0, None)
        self.m_free_mode = False
        self.m_free_mode = True
        self.m_data_max = ArraySize(self.m_data)
    def _q_dtor(self):
        if self.m_data_max != 0:
            self.Shutdown()
    def FreeMode_0(self):
        return self.m_free_mode
    def FreeMode_1(self, mode):
        self.m_free_mode = mode
    def Type(self):
        return 0x7778
    def Save(self, file_handle):
        i = 0
        if not CArray.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        while i < self.m_data_total:
            if self.m_data[i].Save(file_handle) != True:
                break
            i += 1
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
                if not self.CreateElement(i):
                    break
                if self.m_data[i].Load(file_handle) != True:
                    break
                self.m_data_total += 1
            else:
                i = _range_end(i, num, 1)
        self.m_sort_mode = -1
        return self.m_data_total == num
    def CreateElement(self, index):
        return False
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
            for i in range(self.m_data_total, self.m_data_max):
                self.m_data[i] = None
        return self.Available() >= size
    def Resize(self, size):
        new_size = 0
        if size < 0:
            return False
        new_size = self.m_step_resize * (1 + _idiv(size, self.m_step_resize))
        if self.m_data_total > size:
            if self.m_free_mode:
                for i in range(size, self.m_data_total):
                    if CheckPointer(self.m_data[i]) == POINTER_DYNAMIC:
                        _delete(self.m_data[i])
            self.m_data_total = size
        if self.m_data_max != new_size:
            if _setattr(self, 'm_data_max', ArrayResize(self.m_data, new_size)) == -1:
                self.m_data_max = ArraySize(self.m_data)
                return False
        return self.m_data_max == new_size
    def Shutdown(self):
        if self.m_data_max == 0:
            return True
        self.Clear()
        if ArrayResize(self.m_data, 0) == -1:
            return False
        self.m_data_max = 0
        return True
    def Add(self, element):
        if not CheckPointer(element):
            return False
        if not self.Reserve(1):
            return False
        self.m_data[_incattr(self, 'm_data_total', 1, True)] = element
        self.m_sort_mode = -1
        return True
    def AddArray(self, src):
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
        if pos < 0 or (not CheckPointer(element)):
            return False
        if not self.Reserve(1):
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
    def InsertArray(self, src, pos):
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
    def AssignArray(self, src):
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
            return None
        return self.m_data[index]
    def Update(self, index, element):
        if (index < 0 or (not CheckPointer(element))) or index >= self.m_data_total:
            return False
        if self.m_free_mode and CheckPointer(self.m_data[index]) == POINTER_DYNAMIC:
            _delete(self.m_data[index])
        self.m_data[index] = element
        self.m_sort_mode = -1
        return True
    def Shift(self, index, shift):
        tmp_node = None
        if (index < 0 or (index + shift) < 0) or (index + shift) >= self.m_data_total:
            return False
        if shift == 0:
            return True
        tmp_node = self.m_data[index]
        self.m_data[index] = None
        if shift > 0:
            if self.MemMove(index, index + 1, shift) < 0:
                return False
        else:
            if self.MemMove(index + shift + 1, index + shift, -shift) < 0:
                return False
        self.m_data[index + shift] = tmp_node
        self.m_sort_mode = -1
        return True
    def Detach(self, index):
        result = None
        if index >= self.m_data_total:
            return None
        result = self.m_data[index]
        self.m_data[index] = None
        if index < (self.m_data_total - 1) and self.MemMove(index, index + 1, self.m_data_total - index - 1) < 0:
            return None
        self.m_data_total -= 1
        return result
    def Delete(self, index):
        if index >= self.m_data_total:
            return False
        if index < (self.m_data_total - 1):
            if index >= 0 and self.MemMove(index, index + 1, self.m_data_total - index - 1) < 0:
                return False
        elif self.m_free_mode and CheckPointer(self.m_data[index]) == POINTER_DYNAMIC:
            _delete(self.m_data[index])
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
        i = to - from_ + 1
        while i > 0:
            if self.m_free_mode and CheckPointer(self.m_data[self.m_data_total - 1]) == POINTER_DYNAMIC:
                _delete(self.m_data[self.m_data_total - 1])
            i -= 1
            self.m_data_total -= 1
        return True
    def Clear(self):
        if self.m_free_mode:
            for i in range(0, self.m_data_total):
                if CheckPointer(self.m_data[i]) == POINTER_DYNAMIC:
                    _delete(self.m_data[i])
                self.m_data[i] = None
        self.m_data_total = 0
    def CompareArray(self, array):
        if not CheckPointer(array):
            return False
        if self.m_data_total != array.m_data_total:
            return False
        i = 0
        while i < self.m_data_total:
            if self.m_data[i].Compare(array.m_data[i], 0) != 0:
                return False
            i += 1
        return True
    def InsertSort(self, element):
        pos = 0
        if (not CheckPointer(element)) or self.m_sort_mode == -1:
            return False
        if not self.Reserve(1):
            return False
        if self.m_data_total == 0:
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = element
            return True
        mode = self.m_sort_mode
        pos = self.QuickSearch(element)
        if self.m_data[pos].Compare(element, self.m_sort_mode) > 0:
            self.Insert(element, pos)
        else:
            self.Insert(element, pos + 1)
        self.m_sort_mode = mode
        return True
    def Search(self, element):
        pos = 0
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos].Compare(element, self.m_sort_mode) == 0:
            return pos
        return -1
    def SearchGreat(self, element):
        pos = 0
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos].Compare(element, self.m_sort_mode) <= 0:
            if (pos := pos + 1) == self.m_data_total:
                return -1
        return pos
    def SearchLess(self, element):
        pos = 0
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos].Compare(element, self.m_sort_mode) >= 0:
            if ((pos := pos - 1) + 1) == 0:
                return -1
        return pos
    def SearchGreatOrEqual(self, element):
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        while pos < self.m_data_total:
            if self.m_data[pos].Compare(element, self.m_sort_mode) >= 0:
                return pos
            pos += 1
        return -1
    def SearchLessOrEqual(self, element):
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        for pos in range(self.QuickSearch(element), 0 - 1, -1):
            if self.m_data[pos].Compare(element, self.m_sort_mode) <= 0:
                return pos
        return -1
    def SearchFirst(self, element):
        pos = 0
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos].Compare(element, self.m_sort_mode) == 0:
            while self.m_data[pos].Compare(element, self.m_sort_mode) == 0:
                if ((pos := pos - 1) + 1) == 0:
                    break
            return pos + 1
        return -1
    def SearchLast(self, element):
        pos = 0
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos].Compare(element, self.m_sort_mode) == 0:
            while self.m_data[pos].Compare(element, self.m_sort_mode) == 0:
                if (pos := pos + 1) == self.m_data_total:
                    break
            return pos - 1
        return -1
    def QuickSort(self, beg, end, mode):
        i = 0
        j = 0
        p_node = None
        t_node = None
        i = beg
        j = end
        while i < end:
            p_node = self.m_data[(beg + end) >> 1]
            while i < j:
                while self.m_data[i].Compare(p_node, mode) < 0:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                while self.m_data[j].Compare(p_node, mode) > 0:
                    if j == 0:
                        break
                    j -= 1
                if i <= j:
                    t_node = self.m_data[i]
                    self.m_data[((i := i + 1) - 1)] = self.m_data[j]
                    self.m_data[j] = t_node
                    if j == 0:
                        break
                    j -= 1
            if beg < j:
                self.QuickSort(beg, j, mode)
            beg = i
            j = end
    def QuickSearch(self, element):
        i = 0
        j = 0
        m = -1
        t_node = None
        i = 0
        j = self.m_data_total - 1
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m == (self.m_data_total - 1):
                break
            t_node = self.m_data[m]
            if t_node.Compare(element, self.m_sort_mode) == 0:
                break
            if t_node.Compare(element, self.m_sort_mode) > 0:
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
                if self.m_free_mode and CheckPointer(self.m_data[dest + i]) == POINTER_DYNAMIC:
                    _delete(self.m_data[dest + i])
                self.m_data[dest + i] = self.m_data[src + i]
                self.m_data[src + i] = None
            else:
                i = _range_end(i, count, 1)
        else:
            i = count - 1
            for i in range(i, 0 - 1, -1):
                if self.m_free_mode and CheckPointer(self.m_data[dest + i]) == POINTER_DYNAMIC:
                    _delete(self.m_data[dest + i])
                self.m_data[dest + i] = self.m_data[src + i]
                self.m_data[src + i] = None
            else:
                i = _range_end(i, 0 - 1, -1)
        return dest

class CAvg(CObject):
    _q_fields = ('m_timeframe', 'm_symbol', 'm_period', 'm_method', 'm_price', 'm_rates_total', 'm_prev_value')
    def _q_ctor1(self, rates_total, symbol_name, timeframe, period):
        CObject.__init__(self)
        self.m_timeframe = 0
        self.m_symbol = ""
        self.m_period = 0
        self.m_method = 0
        self.m_price = 0
        self.m_rates_total = 0
        self.m_prev_value = 0.0
        self.m_prev_value = 0.0
        self.m_symbol = symbol_name
        self.m_timeframe = timeframe
        self.m_period = period
        self.m_rates_total = rates_total
    def _q_ctor2(self):
        CObject.__init__(self)
        self.m_timeframe = 0
        self.m_symbol = ""
        self.m_period = 0
        self.m_method = 0
        self.m_price = 0
        self.m_rates_total = 0
        self.m_prev_value = 0.0
        self.m_prev_value = 0.0
    def __init__(self, *args):
        if 4 <= len(args) <= 4 and (len(args) == 0 or (isinstance(args[0], int) and not isinstance(args[0], bool))):
            self._q_ctor1(*args)
            return
        if 0 <= len(args) <= 0:
            self._q_ctor2(*args)
            return
        self._q_ctor1(*args)
    def _q_dtor(self):
        pass
    def CheckPosition(self, rates_total, period, index):
        return period >= 1 and index <= (rates_total - period - 1)
    def Open(self, symbol_name, timeframe, index):
        array = Arr(0, 0.0)
        return (array[0] if (CopyOpen(symbol_name, timeframe, index, 1, array) == 1) else 0)
    def High(self, symbol_name, timeframe, index):
        array = Arr(0, 0.0)
        return (array[0] if (CopyHigh(symbol_name, timeframe, index, 1, array) == 1) else 0)
    def Low(self, symbol_name, timeframe, index):
        array = Arr(0, 0.0)
        return (array[0] if (CopyLow(symbol_name, timeframe, index, 1, array) == 1) else 0)
    def Close(self, symbol_name, timeframe, index):
        array = Arr(0, 0.0)
        return (array[0] if (CopyClose(symbol_name, timeframe, index, 1, array) == 1) else 0)
    def Median(self, symbol_name, timeframe, index):
        array = Arr(0, 0.0)
        high = self.High(symbol_name, timeframe, index)
        low = self.Low(symbol_name, timeframe, index)
        return (((high + low) / 2.0) if (high > 0 and low > 0) else 0)
    def Typical(self, symbol_name, timeframe, index):
        array = Arr(0, 0.0)
        high = self.High(symbol_name, timeframe, index)
        low = self.Low(symbol_name, timeframe, index)
        close = self.Close(symbol_name, timeframe, index)
        return (((high + low + close) / 3.0) if ((high > 0 and low > 0) and close > 0) else 0)
    def Weighted(self, symbol_name, timeframe, index):
        array = Arr(0, 0.0)
        high = self.High(symbol_name, timeframe, index)
        low = self.Low(symbol_name, timeframe, index)
        close = self.Close(symbol_name, timeframe, index)
        return (((high + low + close + close) / 4.0) if ((high > 0 and low > 0) and close > 0) else 0)
    def Timeframe_1(self, timeframe):
        self.m_timeframe = timeframe
    def Timeframe_0(self):
        return self.m_timeframe
    def Method_1(self, method):
        self.m_method = method
    def Method_0(self):
        return self.m_method
    def AppliedPrice_1(self, price):
        self.m_price = price
    def AppliedPrice_0(self):
        return self.m_price
    def AppliedPrice_4(self, applied_price, symbol_name, timeframe, index):
        _sw1 = applied_price
        if _sw1 == PRICE_OPEN:
            return self.Open(symbol_name, timeframe, index)
        elif _sw1 == PRICE_HIGH:
            return self.High(symbol_name, timeframe, index)
        elif _sw1 == PRICE_LOW:
            return self.Low(symbol_name, timeframe, index)
        elif _sw1 == PRICE_CLOSE:
            return self.Close(symbol_name, timeframe, index)
        elif _sw1 == PRICE_MEDIAN:
            return self.Median(symbol_name, timeframe, index)
        elif _sw1 == PRICE_TYPICAL:
            return self.Typical(symbol_name, timeframe, index)
        else:
            return self.Weighted(symbol_name, timeframe, index)
    def AppliedPrice_4(self, index):
        _sw2 = self.m_price
        if _sw2 == PRICE_OPEN:
            return self.Open(self.m_symbol, self.m_timeframe, index)
        elif _sw2 == PRICE_HIGH:
            return self.High(self.m_symbol, self.m_timeframe, index)
        elif _sw2 == PRICE_LOW:
            return self.Low(self.m_symbol, self.m_timeframe, index)
        elif _sw2 == PRICE_CLOSE:
            return self.Close(self.m_symbol, self.m_timeframe, index)
        elif _sw2 == PRICE_MEDIAN:
            return self.Median(self.m_symbol, self.m_timeframe, index)
        elif _sw2 == PRICE_TYPICAL:
            return self.Typical(self.m_symbol, self.m_timeframe, index)
        else:
            return self.Weighted(self.m_symbol, self.m_timeframe, index)
    def Symbol_1(self, symbol_name):
        self.m_symbol = symbol_name
    def Symbol_0(self):
        return self.m_symbol
    def Period_1(self, period):
        self.m_period = period
    def Period_0(self):
        return self.m_period
    def RatesTotal(self):
        return self.m_rates_total
    def SMA(self, rates_total, period, index, price):
        result = 0.0
        if not self.CheckPosition(rates_total, period, index):
            return 0.0
        for i in range(0, period):
            result = result + price[index + i]
        result = _fdiv(result, period)
        return result
    def EMA(self, rates_total, period, index, price):
        result = 0.0
        if not self.CheckPosition(rates_total, period, index):
            return 0.0
        pr = _fdiv(2.0, period + 1.0)
        if index == (rates_total - period - 1) or self.m_prev_value == 0:
            result = self.SMA(rates_total, period, index, price)
            self.m_prev_value = result
        else:
            result = self.m_prev_value + (pr * (price[index] - self.m_prev_value))
            if index != 0:
                self.m_prev_value = result
        return result
    def SMMA(self, rates_total, period, index, price):
        result = 0.0
        if not self.CheckPosition(rates_total, period, index):
            return 0.0
        if index == (rates_total - period - 1) or self.m_prev_value == 0:
            result = self.SMA(rates_total, period, index, price)
            self.m_prev_value = result
        else:
            result = _fdiv((self.m_prev_value * (period - 1)) + price[index], period)
            if index != 0:
                self.m_prev_value = result
        return result
    def LWMA(self, rates_total, period, index, price):
        result = 0.0
        count = 0.0
        total = 0.0
        k = 0.0
        if not self.CheckPosition(rates_total, period, index):
            return 0.0
        for j in range(index + period - 1, index - 1, -1):
            count += 1
            k += count
            total += price[j] * count
        result = _fdiv(total, k)
        return result
    def GetMA_5(self, rates_total, method, period, index, price):
        _sw3 = method
        if _sw3 == MODE_EMA:
            return self.EMA(rates_total, period, index, price)
        elif _sw3 == MODE_SMMA:
            return self.SMMA(rates_total, period, index, price)
        elif _sw3 == MODE_LWMA:
            return self.LWMA(rates_total, period, index, price)
        else:
            return self.SMA(rates_total, period, index, price)
    def GetMA_3(self, rates_total, index, price):
        self.m_rates_total = rates_total
        _sw4 = self.m_method
        if _sw4 == MODE_EMA:
            return self.EMA(self.m_rates_total, self.m_period, index, price)
        elif _sw4 == MODE_SMMA:
            return self.SMMA(self.m_rates_total, self.m_period, index, price)
        elif _sw4 == MODE_LWMA:
            return self.LWMA(self.m_rates_total, self.m_period, index, price)
        else:
            return self.SMA(self.m_rates_total, self.m_period, index, price)
    def MethodToString_1(self, method):
        return StringSubstr(EnumToString(method, 'ENUM_MA_METHOD'), 5)
    def MethodToString_0(self):
        return StringSubstr(EnumToString(self.m_method, 'ENUM_MA_METHOD'), 5)
    def PriceToString_1(self, price):
        return StringSubstr(EnumToString(price, 'ENUM_APPLIED_PRICE'), 6)
    def PriceToString_0(self):
        return StringSubstr(EnumToString(self.m_price, 'ENUM_APPLIED_PRICE'), 6)

def OnInit():
    global cnt, period_beg, period_end
    period_beg = (1 if (InpPeriodBeg < 1) else InpPeriodBeg)
    period_end = ((period_beg + 1) if (_int(InpPeriodEnd) <= period_beg) else InpPeriodEnd)
    cnt = period_end - period_beg + 1
    SetIndexBuffer(0, BufferXMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPrice, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'The sum of ' + _str(cnt) + ' ' + MethodToString(InpMethod) + ' (Periods from ' + _str(period_beg) + ' to ' + _str(period_end) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_end)
    PlotIndexSetString(0, PLOT_LABEL, 'Sum ' + _str(cnt) + ' ' + MethodToString(InpMethod))
    ArraySetAsSeries(BufferXMA, True)
    ArraySetAsSeries(BufferPrice, True)
    i = 0
    while i < cnt:
        period_cnt = period_beg + i
        avg = CAvg()
        if avg is None:
            i += 1
            continue
        avg.Period_1(period_cnt)
        avg.AppliedPrice_1(InpAppliedPrice)
        avg.Method_1(InpMethod)
        avg.Symbol_1(Symbol())
        avg.Timeframe_1(Period())
        array_ma.Add(avg)
        i += 1
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferXMA, EMPTY_VALUE)
        ArrayInitialize(BufferPrice, 0)
    for i in range(limit, 0 - 1, -1):
        sum_ = 0.0
        total = array_ma.Total()
        for j in range(0, total):
            avg = array_ma.At(j)
            if avg is None:
                continue
            BufferPrice[i] = avg.AppliedPrice_4(i)
            ma = avg.GetMA_3(rates_total, i, BufferPrice)
            sum_ += ma
        BufferXMA[i] = _fdiv(sum_, cnt)
    return rates_total

def MethodToString(method):
    return StringSubstr(EnumToString(method, 'ENUM_MA_METHOD'), 5)

# ---- global variables initialised from expressions
array_ma = _alloc(CArrayObj)
array_ma.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XMASumAvg(_MQL5Indicator):
    name = 'xMASumAvg'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodBeg': 20,  # Initial period
        'InpPeriodEnd': 100,  # End period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

