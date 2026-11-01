"""Generic_Index — converted from MQL5: MQL5 Indicators/Generic_Index/Generic_Index.mq5

Generic Index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Functions not available here: FileReadLong, FileWriteLong
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13434880]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'GIndex'}, 'levels': [], 'description': ['Generic Index'], 'name': 'Generic_Index', 'source': 'MQL5 Indicators/Generic_Index/Generic_Index.mq5', 'folder': 'Generic_Index', 'inputs': [{'mql': 'InpIndex', 'py': 'InpIndex', 'param': None, 'type': 'string', 'default': 'USD', 'label': 'Index', 'sinput': False}, {'mql': 'InpInverse', 'py': 'InpInverse', 'param': 'InpInverse', 'type': 'int', 'default': 0, 'label': 'Inverse', 'sinput': False}, {'mql': 'InpInstrument1', 'py': 'InpInstrument1', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'Instrument 1', 'sinput': False}, {'mql': 'InpUseInstrument1', 'py': 'InpUseInstrument1', 'param': 'InpUseInstrument1', 'type': 'int', 'default': 1, 'label': 'Use instrument 1', 'sinput': False}, {'mql': 'InpInstrument2', 'py': 'InpInstrument2', 'param': None, 'type': 'string', 'default': 'USDJPY', 'label': 'Instrument 2', 'sinput': False}, {'mql': 'InpUseInstrument2', 'py': 'InpUseInstrument2', 'param': 'InpUseInstrument2', 'type': 'int', 'default': 1, 'label': 'Use instrument 2', 'sinput': False}, {'mql': 'InpInstrument3', 'py': 'InpInstrument3', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Instrument 3', 'sinput': False}, {'mql': 'InpUseInstrument3', 'py': 'InpUseInstrument3', 'param': 'InpUseInstrument3', 'type': 'int', 'default': 1, 'label': 'Use instrument 3', 'sinput': False}, {'mql': 'InpInstrument4', 'py': 'InpInstrument4', 'param': None, 'type': 'string', 'default': 'USDCHF', 'label': 'Instrument 4', 'sinput': False}, {'mql': 'InpUseInstrument4', 'py': 'InpUseInstrument4', 'param': 'InpUseInstrument4', 'type': 'int', 'default': 1, 'label': 'Use instrument 4', 'sinput': False}, {'mql': 'InpInstrument5', 'py': 'InpInstrument5', 'param': None, 'type': 'string', 'default': 'USDCAD', 'label': 'Instrument 5', 'sinput': False}, {'mql': 'InpUseInstrument5', 'py': 'InpUseInstrument5', 'param': 'InpUseInstrument5', 'type': 'int', 'default': 1, 'label': 'Use instrument 5', 'sinput': False}, {'mql': 'InpInstrument6', 'py': 'InpInstrument6', 'param': None, 'type': 'string', 'default': 'NZDUSD', 'label': 'Instrument 6', 'sinput': False}, {'mql': 'InpUseInstrument6', 'py': 'InpUseInstrument6', 'param': 'InpUseInstrument6', 'type': 'int', 'default': 1, 'label': 'Use instrument 6', 'sinput': False}, {'mql': 'InpInstrument7', 'py': 'InpInstrument7', 'param': None, 'type': 'string', 'default': 'AUDUSD', 'label': 'Instrument 7', 'sinput': False}, {'mql': 'InpUseInstrument7', 'py': 'InpUseInstrument7', 'param': 'InpUseInstrument7', 'type': 'int', 'default': 1, 'label': 'Use instrument 7', 'sinput': False}, {'mql': 'InpInstrument8', 'py': 'InpInstrument8', 'param': None, 'type': 'string', 'default': 'USDSEK', 'label': 'Instrument 8', 'sinput': False}, {'mql': 'InpUseInstrument8', 'py': 'InpUseInstrument8', 'param': 'InpUseInstrument8', 'type': 'int', 'default': 1, 'label': 'Use instrument 8', 'sinput': False}, {'mql': 'InpInstrument9', 'py': 'InpInstrument9', 'param': None, 'type': 'string', 'default': 'USDRUB', 'label': 'Instrument 9', 'sinput': False}, {'mql': 'InpUseInstrument9', 'py': 'InpUseInstrument9', 'param': 'InpUseInstrument9', 'type': 'int', 'default': 1, 'label': 'Use instrument 9', 'sinput': False}, {'mql': 'InpInstrument10', 'py': 'InpInstrument10', 'param': None, 'type': 'string', 'default': 'XAUUSD', 'label': 'Instrument 10', 'sinput': False}, {'mql': 'InpUseInstrument10', 'py': 'InpUseInstrument10', 'param': 'InpUseInstrument10', 'type': 'int', 'default': 1, 'label': 'Use instrument 10', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpIndex = _input('InpIndex', 'USD')  # Index
InpInverse = _input('InpInverse', INPUT_NO)  # Inverse
InpInstrument1 = _input('InpInstrument1', 'EURUSD')  # Instrument 1
InpUseInstrument1 = _input('InpUseInstrument1', INPUT_YES)  # Use instrument 1
InpInstrument2 = _input('InpInstrument2', 'USDJPY')  # Instrument 2
InpUseInstrument2 = _input('InpUseInstrument2', INPUT_YES)  # Use instrument 2
InpInstrument3 = _input('InpInstrument3', 'GBPUSD')  # Instrument 3
InpUseInstrument3 = _input('InpUseInstrument3', INPUT_YES)  # Use instrument 3
InpInstrument4 = _input('InpInstrument4', 'USDCHF')  # Instrument 4
InpUseInstrument4 = _input('InpUseInstrument4', INPUT_YES)  # Use instrument 4
InpInstrument5 = _input('InpInstrument5', 'USDCAD')  # Instrument 5
InpUseInstrument5 = _input('InpUseInstrument5', INPUT_YES)  # Use instrument 5
InpInstrument6 = _input('InpInstrument6', 'NZDUSD')  # Instrument 6
InpUseInstrument6 = _input('InpUseInstrument6', INPUT_YES)  # Use instrument 6
InpInstrument7 = _input('InpInstrument7', 'AUDUSD')  # Instrument 7
InpUseInstrument7 = _input('InpUseInstrument7', INPUT_YES)  # Use instrument 7
InpInstrument8 = _input('InpInstrument8', 'USDSEK')  # Instrument 8
InpUseInstrument8 = _input('InpUseInstrument8', INPUT_YES)  # Use instrument 8
InpInstrument9 = _input('InpInstrument9', 'USDRUB')  # Instrument 9
InpUseInstrument9 = _input('InpUseInstrument9', INPUT_YES)  # Use instrument 9
InpInstrument10 = _input('InpInstrument10', 'XAUUSD')  # Instrument 10
InpUseInstrument10 = _input('InpUseInstrument10', INPUT_YES)  # Use instrument 10
BufferGI = Arr(0, 0.0)
scale_factor = 0.0

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

class CInstrument(CObject):
    _q_fields = ('m_symbol_main', 'm_symbol_name', 'm_weight', 'm_bars')
    def __init__(self, main_symbol, symbol_name):
        CObject.__init__(self)
        self.m_symbol_main = ""
        self.m_symbol_name = ""
        self.m_weight = 0.0
        self.m_bars = 0
        self.m_weight = 0.0
        self.m_bars = 0
        self.m_symbol_main = main_symbol
        self.m_symbol_name = symbol_name
    def _q_dtor(self):
        pass
    def Symbol(self):
        return self.m_symbol_name
    def SetSignOfWeight(self):
        first = StringSubstr(self.m_symbol_name, 0, 3)
        second = StringSubstr(self.m_symbol_name, 3, 3)
        self.m_weight = (1 if (self.m_symbol_main == first) else -1)
    def GetSignOfWeight(self):
        return self.m_weight
    def Bars_1(self, bars):
        self.m_bars = bars
    def Bars_0(self):
        return self.m_bars
    def Refresh(self):
        array = Arr(0, 0)
        return CopyTime(self.m_symbol_name, PERIOD_CURRENT, 0, 1, array) == 1

def OnInit():
    global scale_factor
    EventSetTimer(90)
    list_instruments.Sort()
    scale_factor = InitInstruments()
    SetIndexBuffer(0, BufferGI, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Generic Index ' + InpIndex)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferGI, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    min_bars = 4
    if rates_total < min_bars or (not CheckBars(rates_total, min_bars)):
        return 0
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferGI, EMPTY_VALUE)
    limit_min = fmin(rates_total, MinBars()) - 1
    total = (limit if (limit == 0) else limit_min)
    count = list_instruments.Total()
    for i in range(total, 0 - 1, -1):
        X = 1.0
        for j in range(0, count):
            instr = list_instruments.At(j)
            if instr is None:
                continue
            symbol = instr.Symbol()
            IndexBar = BarShift(symbol, 0, time[i])
            index_bars = (limit_min if (limit_min < instr.Bars_0()) else instr.Bars_0())
            IndexBar0 = BarShift(symbol, 0, time[index_bars - 1])
            if IndexBar == WRONG_VALUE or IndexBar0 == WRONG_VALUE:
                continue
            Close1 = Close(symbol, IndexBar)
            Close0 = Close(symbol, IndexBar0)
            X = X * pow(_fdiv(Close1, (Close0 if (Close0 > 0) else DBL_MIN)), instr.GetSignOfWeight())
        BufferGI[i] = X * scale_factor
    return rates_total

def OnTimer():
    total = list_instruments.Total()
    for i in range(0, total):
        instr = list_instruments.At(i)
        if instr is None:
            continue
        instr.Refresh()
    ChartRedraw()

def SymbolCheck(symbol_name):
    select = Box(0)
    ResetLastError()
    if not SymbolInfoInteger(symbol_name, SYMBOL_SELECT, select):
        err = GetLastError()
        Print('Error: ', err, ' Symbol ', symbol_name, ' does not exist')
        return False
    else:
        if select.v:
            return True
        ResetLastError()
        if not SymbolSelect(symbol_name, True):
            err = GetLastError()
            Print('Error selected ', symbol_name, ': ', err)
    return False

def CheckBars(rates_total, min_bars):
    res = True
    total = list_instruments.Total()
    for i in range(0, total):
        instr = list_instruments.At(i)
        if instr is None:
            continue
        symbol = instr.Symbol()
        instr.Bars_1((rates_total if (symbol == Symbol()) else Bars(symbol, PERIOD_CURRENT)))
        instr.Refresh()
        if instr.Bars_0() < min_bars:
            res = False
    return res

def MinBars():
    total = list_instruments.Total()
    min_bars = INT_MAX
    for i in range(0, total):
        instr = list_instruments.At(i)
        if instr is None:
            continue
        if instr.Bars_0() < min_bars:
            min_bars = instr.Bars_0()
    return (WRONG_VALUE if (min_bars == INT_MAX) else min_bars)

def InitInstruments():
    array_names = Arr(10, "", dyn=False, dims=(2,))
    array_names[0][0] = InpInstrument1
    array_names[0][1] = ('u' if InpUseInstrument1 else None)
    array_names[1][0] = InpInstrument2
    array_names[1][1] = ('u' if InpUseInstrument2 else None)
    array_names[2][0] = InpInstrument3
    array_names[2][1] = ('u' if InpUseInstrument3 else None)
    array_names[3][0] = InpInstrument4
    array_names[3][1] = ('u' if InpUseInstrument4 else None)
    array_names[4][0] = InpInstrument5
    array_names[4][1] = ('u' if InpUseInstrument5 else None)
    array_names[5][0] = InpInstrument6
    array_names[5][1] = ('u' if InpUseInstrument6 else None)
    array_names[6][0] = InpInstrument7
    array_names[6][1] = ('u' if InpUseInstrument7 else None)
    array_names[7][0] = InpInstrument8
    array_names[7][1] = ('u' if InpUseInstrument8 else None)
    array_names[8][0] = InpInstrument9
    array_names[8][1] = ('u' if InpUseInstrument9 else None)
    array_names[9][0] = InpInstrument10
    array_names[9][1] = ('u' if InpUseInstrument10 else None)
    x = 1.0
    total = 10
    for i in range(0, total):
        if array_names[i][1] == "":
            continue
        name = array_names[i][0]
        if not SymbolCheck(name):
            continue
        instr = CInstrument(InpIndex, name)
        if instr is None:
            continue
        list_instruments.Add(instr)
        instr.SetSignOfWeight()
        instr.Refresh()
    return CalcWeights()

def CalcWeights():
    total = list_instruments.Total()
    x = 1.0
    for i in range(0, total):
        instr = list_instruments.At(i)
        if instr is None:
            continue
        wt = instr.GetSignOfWeight()
        wt = _fdiv(wt, total * (-1.0 if InpInverse else 1.0))
        x = x * pow(total, wt)
    return _fdiv(100.0, x)

def Close(symbol_name, shift):
    array = Arr(0, 0.0)
    if CopyClose(symbol_name, PERIOD_CURRENT, shift, 1, array) == 1:
        return array[0]
    return 0.0

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res

# ---- global variables initialised from expressions
list_instruments = _alloc(CArrayObj)
list_instruments.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GenericIndex(_MQL5Indicator):
    name = 'Generic_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpInverse': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Inverse
        'InpUseInstrument1': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use instrument 1
        'InpUseInstrument2': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use instrument 2
        'InpUseInstrument3': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use instrument 3
        'InpUseInstrument4': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use instrument 4
        'InpUseInstrument5': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use instrument 5
        'InpUseInstrument6': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use instrument 6
        'InpUseInstrument7': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use instrument 7
        'InpUseInstrument8': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use instrument 8
        'InpUseInstrument9': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use instrument 9
        'InpUseInstrument10': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use instrument 10
    }

