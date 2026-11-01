"""mamc — converted from MQL5: MQL5 Indicators/MA mass cloud/mamc.mq5

MA Mass Cloud\\n
Clouds formed by the masses of moving averages of different periods
Changes color when perfect order is
Copyright: Copyright 2011, kur.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Functions not available here: FileReadLong, FileWriteLong
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2011, kur.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16443110], 2: [16443110], 3: [16443110]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ma_cloud', 2: 'aim_u', 3: 'aim_l'}, 'levels': [], 'description': ['MA Mass Cloud\\n', 'Clouds formed by the masses of moving averages of different periods', 'Changes color when perfect order is'], 'name': 'mamc', 'source': 'MQL5 Indicators/MA mass cloud/mamc.mq5', 'folder': 'MA mass cloud', 'inputs': [{'mql': 'METHOD', 'py': 'METHOD', 'param': 'METHOD', 'type': 'int', 'default': 1, 'label': 'MA Method', 'sinput': False}, {'mql': 'APPLIED', 'py': 'APPLIED', 'param': 'APPLIED', 'type': 'int', 'default': 2, 'label': 'MA Applied Price', 'sinput': False}, {'mql': 'Weight', 'py': 'Weight', 'param': 'Weight', 'type': 'int', 'default': 64, 'label': 'MA Period STEP', 'sinput': False}, {'mql': 'Depth', 'py': 'Depth', 'param': 'Depth', 'type': 'int', 'default': 10, 'label': 'Number of MA', 'sinput': False}, {'mql': 'Default', 'py': 'Default', 'param': None, 'type': 'color', 'default': 16443110, 'label': '', 'sinput': False}, {'mql': 'Bullish', 'py': 'Bullish', 'param': None, 'type': 'color', 'default': 15658671, 'label': '', 'sinput': False}, {'mql': 'Bearish', 'py': 'Bearish', 'param': None, 'type': 'color', 'default': 13353215, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter
OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
Upper = Arr(0, 0.0)  # buffers
Lower = Arr(0, 0.0)  # buffers
Aim_u = Arr(0, 0.0)  # buffers
Aim_l = Arr(0, 0.0)  # buffers
METHOD = _input('METHOD', MODE_EMA)  # MA Method
APPLIED = _input('APPLIED', PRICE_OPEN)  # MA Applied Price
Weight = _input('Weight', 64)  # MA Period STEP
Depth = _input('Depth', 10)  # Number of MA
Default = _input('Default', clrLavender)
Bullish = _input('Bullish', clrPaleTurquoise)
Bearish = _input('Bearish', clrPink)
H = 0  # MA handle
L = 0  # End position of the bar  //hasi no ba- no iti
R = 0  # End position of the bar  //hasi no ba- no iti
I = False  # The first access or new bar

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

class CArrayDouble(CArray):
    _q_fields = ('m_data', 'm_delta')
    def __init__(self):
        CArray.__init__(self)
        self.m_data = Arr(0, 0.0)
        self.m_delta = 0.0
        self.m_delta = 0.0
        self.m_data_max = ArraySize(self.m_data)
    def _q_dtor(self):
        if self.m_data_max != 0:
            self.Shutdown()
    def Delta(self, delta):
        self.m_delta = MathAbs(delta)
    def Type(self):
        return TYPE_DOUBLE
    def Save(self, file_handle):
        i = 0
        if not CArray.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, self.m_data_total):
            if FileWriteDouble(file_handle, self.m_data[i]) != 8:
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
                self.m_data[i] = FileReadDouble(file_handle)
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
            return DBL_MAX
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
        tmp_double = 0.0
        if (index < 0 or (index + shift) < 0) or (index + shift) >= self.m_data_total:
            return False
        if shift == 0:
            return True
        tmp_double = self.m_data[index]
        if shift > 0:
            if self.MemMove(index, index + 1, shift) < 0:
                return False
        else:
            if self.MemMove(index + shift + 1, index + shift, -shift) < 0:
                return False
        self.m_data[index + shift] = tmp_double
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
        if MathAbs(self.m_data[pos] - element) <= self.m_delta:
            return pos
        return -1
    def SearchGreat(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos] <= (element + self.m_delta):
            if (pos := pos + 1) == self.m_data_total:
                return -1
        return pos
    def SearchLess(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos] >= (element - self.m_delta):
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
            while MathAbs(self.m_data[pos] - element) <= self.m_delta:
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
            while MathAbs(self.m_data[pos] - element) <= self.m_delta:
                if (pos := pos + 1) == self.m_data_total:
                    break
            return pos - 1
        return -1
    def SearchLinear(self, element):
        if self.m_data_total == 0:
            return -1
        for i in range(0, self.m_data_total):
            if MathAbs(self.m_data[i] - element) <= self.m_delta:
                return i
        return -1
    def QuickSort(self, beg, end, mode=0):
        i = 0
        j = 0
        p_double = 0.0
        t_double = 0.0
        if beg < 0 or end < 0:
            return
        i = beg
        j = end
        while i < end:
            p_double = self.m_data[(beg + end) >> 1]
            while i < j:
                while self.m_data[i] < p_double:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                while self.m_data[j] > p_double:
                    if j == 0:
                        break
                    j -= 1
                if i <= j:
                    t_double = self.m_data[i]
                    self.m_data[((i := i + 1) - 1)] = self.m_data[j]
                    self.m_data[j] = t_double
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
        t_double = 0.0
        i = 0
        j = self.m_data_total - 1
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m >= self.m_data_total:
                break
            t_double = self.m_data[m]
            if MathAbs(t_double - element) <= self.m_delta:
                break
            if t_double > element:
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

class CSeries(CArrayObj):
    _q_fields = ('m_name', 'm_buffers_total', 'm_buffer_size', 'm_timeframe_flags', 'm_symbol', 'm_period', 'm_refresh_current', 'm_first_date')
    def __init__(self):
        CArrayObj.__init__(self)
        self.m_name = ""
        self.m_buffers_total = 0
        self.m_buffer_size = 0
        self.m_timeframe_flags = 0
        self.m_symbol = ""
        self.m_period = 0
        self.m_refresh_current = False
        self.m_first_date = 0
        self.m_name = ''
        self.m_timeframe_flags = 0
        self.m_buffers_total = 0
        self.m_buffer_size = 0
        self.m_symbol = ''
        self.m_period = WRONG_VALUE
        self.m_refresh_current = True
    def _q_dtor(self):
        pass
    def Name(self):
        return self.m_name
    def BuffersTotal(self):
        return self.m_buffers_total
    def BufferSize(self):
        return self.m_buffer_size
    def Timeframe(self):
        return self.m_timeframe_flags
    def Symbol(self):
        return self.m_symbol
    def Period(self):
        return self.m_period
    def PeriodDescription(self, val=0):
        i = 0
        frame = 0
        frame = (self.m_period if (val == 0) else val)
        if frame == WRONG_VALUE:
            return 'WRONG_VALUE'
        i = 0
        for i in range(i, ArraySize(_s_CSeries_PeriodDescription__p_int)):
            if frame == _s_CSeries_PeriodDescription__p_int[i]:
                break
        else:
            i = _range_end(i, ArraySize(_s_CSeries_PeriodDescription__p_int), 1)
        return _s_CSeries_PeriodDescription__p_str[i]
    def RefreshCurrent(self, flag):
        self.m_refresh_current = flag
    def BufferResize(self, size):
        if not self.CheckLoadHistory(size):
            printf('failed to get %d bars for %s,%s', size, self.m_symbol, EnumToString(self.m_period, 'ENUM_TIMEFRAMES'))
            return False
        self.m_buffer_size = size
        return True
    def Refresh(self, flags):
        pass
    def SetSymbolPeriod(self, symbol, period):
        self.m_symbol = (ChartSymbol() if (symbol == "") else symbol)
        self.m_period = (ChartPeriod() if (period == 0) else period)
        self.PeriodToTimeframeFlag(self.m_period)
        return True
    def PeriodToTimeframeFlag(self, period):
        for i in range(0, ArraySize(_s_CSeries_PeriodToTimeframeFlag__p_int)):
            if period == _s_CSeries_PeriodToTimeframeFlag__p_int[i]:
                self.m_timeframe_flags = _int(1 << i)
                return
    def CheckLoadHistory(self, size):
        if (MQLInfoInteger(MQL_PROGRAM_TYPE) == PROGRAM_INDICATOR and self.Period() == self.m_period) and self.Symbol() == self.m_symbol:
            return True
        if size > TerminalInfoInteger(TERMINAL_MAXBARS):
            printf('CSeries::CheckLoadHistory' + ': requested too much data (%d)', size)
            return False
        self.m_first_date = 0
        if self.CheckTerminalHistory(size):
            return True
        if self.CheckServerHistory(size):
            return True
        return False
    def CheckTerminalHistory(self, size):
        times = Arr(1, 0, dyn=False)
        bars = Box(0)
        if Bars(self.m_symbol, self.m_period) >= size:
            return True
        if SeriesInfoInteger(self.m_symbol, PERIOD_M1, SERIES_BARS_COUNT, bars):
            if bars.v > _idiv(size * PeriodSeconds(self.m_period), 60):
                CopyTime(self.m_symbol, self.m_period, size - 1, 1, times)
                if SeriesInfoInteger(self.m_symbol, self.m_period, SERIES_BARS_COUNT, bars):
                    if bars.v > size:
                        return True
        return False
    def CheckServerHistory(self, size):
        first_server_date = Box(0)
        while not SeriesInfoInteger(self.m_symbol, PERIOD_M1, SERIES_SERVER_FIRSTDATE, first_server_date):
            Sleep(5)
        if first_server_date.v > (TimeCurrent() - (size * PeriodSeconds(self.m_period))):
            return False
        fail_cnt = 0
        times = Arr(1, 0, dyn=False)
        while True:
            while not SeriesInfoInteger(self.m_symbol, self.m_period, SERIES_SYNCHRONIZED):
                Sleep(5)
            bars = Bars(self.m_symbol, self.m_period)
            if bars > size:
                return True
            if CopyTime(self.m_symbol, self.m_period, size - 1, 1, times) == 1:
                return True
            if (fail_cnt := fail_cnt + 1) >= 100:
                return False
            Sleep(10)
        return False

class CDoubleBuffer(CArrayDouble):
    _q_fields = ('m_symbol', 'm_period', 'm_size')
    def __init__(self):
        CArrayDouble.__init__(self)
        self.m_symbol = ""
        self.m_period = 0
        self.m_size = 0
        self.m_symbol = ''
        self.m_period = WRONG_VALUE
        self.m_size = 1024
        ArraySetAsSeries(self.m_data, True)
    def _q_dtor(self):
        pass
    def Size(self, size):
        self.m_size = size
    def At(self, index):
        if index >= self.m_data_total:
            return EMPTY_VALUE
        d = CArrayDouble.At(self, index)
        return d
    def Refresh(self):
        return True
    def RefreshCurrent(self):
        return True
    def SetSymbolPeriod(self, symbol, period):
        self.m_symbol = (ChartSymbol() if (symbol == "") else symbol)
        self.m_period = (ChartPeriod() if (period == 0) else period)

class CIndicatorBuffer(CDoubleBuffer):
    _q_fields = ('m_offset', 'm_name')
    def __init__(self):
        CDoubleBuffer.__init__(self)
        self.m_offset = 0
        self.m_name = ""
        self.m_offset = 0
        self.m_name = ''
    def _q_dtor(self):
        pass
    def Offset_0(self):
        return self.m_offset
    def Offset_1(self, offset):
        self.m_offset = offset
    def Name_0(self):
        return self.m_name
    def Name_1(self, name):
        self.m_name = name
    def At(self, index):
        return CDoubleBuffer.At(self, index + self.m_offset)
    def Refresh_2(self, handle, num):
        if handle == INVALID_HANDLE:
            SetUserError(1)
            return False
        self.m_data_total = CopyBuffer(handle, num, -self.m_offset, self.m_size, self.m_data)
        return self.m_data_total > 0
    def Refresh_0(self):
        return CDoubleBuffer.Refresh(self)
    def RefreshCurrent_2(self, handle, num):
        array = Arr(1, 0.0, dyn=False)
        if handle == INVALID_HANDLE:
            SetUserError(1)
            return False
        if CopyBuffer(handle, num, -self.m_offset, 1, array) > 0 and self.m_data_total > 0:
            self.m_data[0] = array[0]
            return True
        return False
    def RefreshCurrent_0(self):
        return CDoubleBuffer.RefreshCurrent(self)

class CIndicator(CSeries):
    _q_fields = ('m_handle', 'm_status', 'm_full_release', 'm_redrawer')
    def __init__(self):
        CSeries.__init__(self)
        self.m_handle = 0
        self.m_status = ""
        self.m_full_release = False
        self.m_redrawer = False
        self.m_handle = INVALID_HANDLE
        self.m_status = ''
        self.m_full_release = False
        self.m_redrawer = False
    def _q_dtor(self):
        if self.m_full_release and self.m_handle != INVALID_HANDLE:
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
    def Handle(self):
        return self.m_handle
    def Status(self):
        return self.m_status
    def FullRelease(self, flag=True):
        self.m_full_release = flag
    def Redrawer(self, flag=True):
        self.m_redrawer = flag
    def Create(self, symbol, period, type_, num_params, params):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = IndicatorCreate(symbol, period, type_, num_params, params)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize(symbol, period, num_params, params):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def BufferResize(self, size):
        if size > self.m_buffer_size and (not CSeries.BufferResize(self, size)):
            return False
        total = self.Total()
        for i in range(0, total):
            buff = self.At(i)
            if buff is None:
                return False
            buff.Size(size)
        return True
    def BarsCalculated(self):
        if self.m_handle == INVALID_HANDLE:
            return -1
        return BarsCalculated(self.m_handle)
    def GetData_2(self, buffer_num, index):
        buffer = self.At(buffer_num)
        if buffer is None:
            Print('CIndicator::GetData', ': invalid buffer')
            return EMPTY_VALUE
        return buffer.At(index)
    def GetData_2(self, start_pos, count, buffer_num, buffer):
        if self.m_handle == INVALID_HANDLE:
            SetUserError(1)
            return -1
        if buffer_num >= self.m_buffers_total:
            SetUserError(2)
            return -1
        return CopyBuffer(self.m_handle, buffer_num, start_pos, count, buffer)
    def GetData_3(self, start_time, count, buffer_num, buffer):
        if self.m_handle == INVALID_HANDLE:
            SetUserError(1)
            return -1
        if buffer_num >= self.m_buffers_total:
            SetUserError(2)
            return -1
        return CopyBuffer(self.m_handle, buffer_num, _DT(start_time), count, buffer)
    def GetData_4(self, start_time, stop_time, buffer_num, buffer):
        if self.m_handle == INVALID_HANDLE:
            SetUserError(1)
            return -1
        if buffer_num >= self.m_buffers_total:
            SetUserError(2)
            return -1
        return CopyBuffer(self.m_handle, buffer_num, _DT(start_time), _DT(stop_time), buffer)
    def Minimum(self, buffer_num, start, count):
        if self.m_handle == INVALID_HANDLE:
            SetUserError(1)
            return -1
        if buffer_num >= self.m_buffers_total:
            SetUserError(2)
            return -1
        buffer = self.At(buffer_num)
        if buffer is None:
            return -1
        return buffer.Minimum(start, count)
    def MinValue(self, buffer_num, start, count, index):
        idx = self.Minimum(buffer_num, start, count)
        res = EMPTY_VALUE
        if idx != -1:
            buffer = self.At(buffer_num)
            res = buffer.At(idx)
            index.v = idx
        return res
    def Maximum(self, buffer_num, start, count):
        if self.m_handle == INVALID_HANDLE:
            SetUserError(1)
            return -1
        if buffer_num >= self.m_buffers_total:
            SetUserError(2)
            return -1
        buffer = self.At(buffer_num)
        if buffer is None:
            return -1
        return buffer.Maximum(start, count)
    def MaxValue(self, buffer_num, start, count, index):
        idx = self.Maximum(buffer_num, start, count)
        res = EMPTY_VALUE
        if idx != -1:
            buffer = self.At(buffer_num)
            res = buffer.At(idx)
            index.v = idx
        return res
    def Refresh(self, flags=_int(OBJ_ALL_PERIODS)):
        i = 0
        buff = None
        i = 0
        while i < self.Total():
            buff = self.At(i)
            if self.m_redrawer:
                buff.Refresh_2(self.m_handle, i)
                i += 1
                continue
            if not (flags & self.m_timeframe_flags):
                if self.m_refresh_current:
                    buff.RefreshCurrent_2(self.m_handle, i)
            else:
                buff.Refresh_2(self.m_handle, i)
            i += 1
    def AddToChart(self, chart, subwin):
        if ChartIndicatorAdd(chart, subwin, self.m_handle):
            self.m_name = ChartIndicatorName(chart, subwin, ChartIndicatorsTotal(chart, subwin) - 1)
            return True
        return False
    def DeleteFromChart(self, chart, subwin):
        return ChartIndicatorDelete(chart, subwin, self.m_name)
    @staticmethod
    def MethodDescription(val):
        _sw1 = val
        if _sw1 == MODE_SMA:
            return 'SMA'
        elif _sw1 == MODE_EMA:
            return 'EMA'
        elif _sw1 == MODE_SMMA:
            return 'SMMA'
        elif _sw1 == MODE_LWMA:
            return 'LWMA'
        return 'MethodUnknown=' + IntegerToString(val)
    @staticmethod
    def PriceDescription(val):
        _sw2 = val
        if _sw2 == PRICE_CLOSE:
            return 'Close'
        elif _sw2 == PRICE_OPEN:
            return 'Open'
        elif _sw2 == PRICE_HIGH:
            return 'High'
        elif _sw2 == PRICE_LOW:
            return 'Low'
        elif _sw2 == PRICE_MEDIAN:
            return 'Median'
        elif _sw2 == PRICE_TYPICAL:
            return 'Typical'
        elif _sw2 == PRICE_WEIGHTED:
            return 'Weighted'
        else:
            if val >= 10:
                return 'AppliedHandle=' + IntegerToString(val)
        return 'PriceUnknown=' + IntegerToString(val)
    @staticmethod
    def VolumeDescription(val):
        _sw3 = val
        if _sw3 == VOLUME_TICK:
            return 'Tick'
        elif _sw3 == VOLUME_REAL:
            return 'Real'
        return 'VolumeUnknown=' + IntegerToString(val)
    def CreateBuffers(self, symbol, period, buffers):
        result = True
        if self.m_handle == INVALID_HANDLE:
            SetUserError(1)
            return False
        if buffers == 0:
            return False
        if not self.Reserve(buffers):
            return False
        for i in range(0, buffers):
            result &= self.Add(CIndicatorBuffer())
        if result:
            self.m_buffers_total = buffers
        return result
    def Initialize(self, symbol, period, num_params, params):
        return False

def OnInit():
    global H, I, L, R
    if Weight < 1 or Depth < 1:
        return -1
    app = Box(EnumToString(APPLIED, 'ENUM_APPLIED_PRICE'))
    app.v = StringSubstr(app.v, 6, 1)
    StringToLower(app)
    met = EnumToString(METHOD, 'ENUM_MA_METHOD')
    met = StringSubstr(met, 5, StringLen(met) - 5)
    PlotIndexSetString(0, PLOT_LABEL, _str(Weight) + ',' + _str(Depth) + ',' + app.v + ',' + met)
    SetIndexBuffer(0, Upper, INDICATOR_DATA)
    ArraySetAsSeries(Upper, True)
    SetIndexBuffer(1, Lower, INDICATOR_DATA)
    ArraySetAsSeries(Lower, True)
    SetIndexBuffer(2, Aim_u, INDICATOR_DATA)
    ArraySetAsSeries(Aim_u, True)
    SetIndexBuffer(3, Aim_l, INDICATOR_DATA)
    ArraySetAsSeries(Aim_l, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    I = True
    R = 0
    L = R
    H = INVALID_HANDLE
    return 0

def OnDeinit(r):
    global H
    if H != INVALID_HANDLE:
        if not IndicatorRelease(H):
            Print(GetLastError())
        else:
            H = INVALID_HANDLE

def OnChartEvent(id_, lparam, dparam, sparam):
    Run()

def OnCalculate(zen, zumi, begin, price):
    global I
    if zen < zumi or zen > zumi:
        I = True
    Run()
    return zen

def Run():
    global I, L, R
    l = 0
    r = Box(0)
    l = Bar(r)
    if ((not I) and L == l) and R == r.v:
        return
    else:
        L = l
        R = r.v
    for bar in range(l, r.v - 1, -1):
        Upper[bar] = EMPTY_VALUE
        Lower[bar] = EMPTY_VALUE
        Aim_u[bar] = EMPTY_VALUE
        Aim_l[bar] = EMPTY_VALUE
        err = False
        asc = True
        des = True
        min_ = DBL_MAX
        max_ = 0.0
        i = 0
        per = Weight
        while i < Depth:
            w = Ima(per, bar)
            if w == 0 or (not MathIsValidNumber(w)):
                err = True
                break
            if w < min_:
                min_ = w
            else:
                des = False
            if w > max_:
                max_ = w
            else:
                asc = False
            i += 1
            per += Weight
        if not err:
            Upper[bar] = max_
            Lower[bar] = min_
            Aim_u[bar] = max_ + max_ - min_
            Aim_l[bar] = min_ - max_ + min_
            I = False
            if bar == r.v:
                if des:
                    LineColor(Bullish)
                elif asc:
                    LineColor(Bearish)
                else:
                    LineColor(Default)

def Ima(ma_period, pos):
    global H
    H = iMA(Symbol(), Period(), ma_period, 0, METHOD, APPLIED)
    if H == INVALID_HANDLE:
        return 0.0
    return Iat(H, 0, pos)

def Iat(handle, bufnum, index):
    iat.Size(index + 1)
    ret = (iat.At(index) if iat.Refresh_2(handle, bufnum) else None)
    return ret

def Bar(right):
    left = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
    bars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
    right.v = fmax(left - bars, 0)
    return left

def LineColor(col):
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, col)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, col)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, col)

# ---- global variables initialised from expressions
iat = _alloc(CIndicatorBuffer)
iat.__init__()

# ---- static local variables
_s_CSeries_PeriodDescription__p_str = Arr.of(['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M10', 'M12', 'M15', 'M20', 'M30', 'H1', 'H2', 'H3', 'H4', 'H6', 'H8', 'H12', 'D1', 'W1', 'MN', 'UNKNOWN'], fill="")
_s_CSeries_PeriodDescription__p_int = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_s_CSeries_PeriodToTimeframeFlag__p_int = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Mamc(_MQL5Indicator):
    name = 'mamc'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'METHOD': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA Method
        'APPLIED': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=2),  # MA Applied Price
        'Weight': 64,  # MA Period STEP
        'Depth': 10,  # Number of MA
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

