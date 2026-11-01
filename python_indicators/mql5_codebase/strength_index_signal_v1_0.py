"""Strength Index Signal v1.0 — converted from MQL5: MQL5 Indicators/Strength Index Signal/Strength Index Signal v1.0.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: FileReadLong, FileWriteLong
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 2}, 'types': {}, 'colors': {1: [16711680], 2: [255], 3: [42495], 4: [13688896], 5: [65280], 6: [2763429], 7: [8421504], 8: [65535]}, 'widths': {}, 'styles': {}, 'labels': {1: 'EUR', 2: 'GBP', 3: 'AUD', 4: 'NZD', 5: 'USD', 6: 'CAD', 7: 'CHF', 8: 'JPY'}, 'levels': [0.0], 'description': [], 'name': 'Strength Index Signal v1.0', 'source': 'MQL5 Indicators/Strength Index Signal/Strength Index Signal v1.0.mq5', 'folder': 'Strength Index Signal', 'inputs': [{'mql': 'inp_ma_period', 'py': 'inp_ma_period', 'param': 'inp_ma_period', 'type': 'int', 'default': 50, 'label': 'strenght accumulation period', 'sinput': False}, {'mql': 'inp_ma_delta', 'py': 'inp_ma_delta', 'param': 'inp_ma_delta', 'type': 'int', 'default': 1, 'label': 'delta', 'sinput': False}, {'mql': 'inp_atr_period', 'py': 'inp_atr_period', 'param': 'inp_atr_period', 'type': 'int', 'default': 20, 'label': 'atr period', 'sinput': False}, {'mql': 'inp_atr_coefficient', 'py': 'inp_atr_coefficient', 'param': 'inp_atr_coefficient', 'type': 'double', 'default': 1.0, 'label': 'atr delta', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter
OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
inp_ma_period = _input('inp_ma_period', 50)  # strenght accumulation period
inp_ma_delta = _input('inp_ma_delta', 1)  # delta
inp_atr_period = _input('inp_atr_period', 20)  # atr period
inp_atr_coefficient = _input('inp_atr_coefficient', 1.0)  # atr delta
ShowEUR = False
ShowGBP = False
ShowAUD = False
ShowNZD = False
ShowUSD = False
ShowCAD = False
ShowCHF = False
ShowJPY = False
EURx = Arr(0, 0.0)  # indexes
GBPx = Arr(0, 0.0)
AUDx = Arr(0, 0.0)
NZDx = Arr(0, 0.0)
USDx = Arr(0, 0.0)
CADx = Arr(0, 0.0)
CHFx = Arr(0, 0.0)
JPYx = Arr(0, 0.0)
ext_arrow_up = Arr(0, 0.0)
ext_arrow_dn = Arr(0, 0.0)
ext_trend = Arr(0, 0.0)
EUR = 0.0
GBP = 0.0
AUD = 0.0
NZD = 0.0
USD = 0.0
CAD = 0.0
CHF = 0.0
JPY = 0.0
A1 = 0.0
A2 = 0.0
A3 = 0.0
A4 = 0.0
A5 = 0.0
A6 = 0.0
A7 = 0.0
Currencies = Arr.of(['EUR', 'GBP', 'AUD', 'NZD', 'USD', 'CAD', 'CHF', 'JPY'], fill="")
symbols = Arr.of(['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY'], fill="", dyn=False, size=28)
chart_currency_index = Arr(2, 0, dyn=False)
handle_atr = 0
init_status = True

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

class CiADX(CIndicator):
    _q_fields = ('m_ma_period',)
    def __init__(self):
        CIndicator.__init__(self)
        self.m_ma_period = 0
        self.m_ma_period = -1
    def _q_dtor(self):
        pass
    def MaPeriod(self):
        return self.m_ma_period
    def Create(self, symbol, period, ma_period):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iADX(symbol, period, ma_period)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_3(symbol, period, ma_period):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Main(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Plus(self, index):
        buffer = self.At(1)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Minus(self, index):
        buffer = self.At(2)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_ADX
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_3(symbol, period, _int(params[0].integer_value))
    def Initialize_3(self, symbol, period, ma_period):
        if self.CreateBuffers(symbol, period, 3):
            self.m_name = 'ADX'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(ma_period) + ') H=' + IntegerToString(self.m_handle)
            self.m_ma_period = ma_period
            self.At(0).Name_1('MAIN_LINE')
            self.At(1).Name_1('PLUS_LINE')
            self.At(2).Name_1('MINUS_LINE')
            return True
        return False

class CiADXWilder(CIndicator):
    _q_fields = ('m_ma_period',)
    def __init__(self):
        CIndicator.__init__(self)
        self.m_ma_period = 0
        self.m_ma_period = -1
    def _q_dtor(self):
        pass
    def MaPeriod(self):
        return self.m_ma_period
    def Create(self, symbol, period, ma_period):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iADXWilder(symbol, period, ma_period)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_3(symbol, period, ma_period):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Main(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Plus(self, index):
        buffer = self.At(1)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Minus(self, index):
        buffer = self.At(2)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_ADXW
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_3(symbol, period, _int(params[0].integer_value))
    def Initialize_3(self, symbol, period, ma_period):
        if self.CreateBuffers(symbol, period, 3):
            self.m_name = 'ADXWilder'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(ma_period) + ') H=' + IntegerToString(self.m_handle)
            self.m_ma_period = ma_period
            self.At(0).Name_1('MAIN_LINE')
            self.At(1).Name_1('PLUS_LINE')
            self.At(2).Name_1('MINUS_LINE')
            return True
        return False

class CiBands(CIndicator):
    _q_fields = ('m_ma_period', 'm_ma_shift', 'm_deviation', 'm_applied')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_ma_period = 0
        self.m_ma_shift = 0
        self.m_deviation = 0.0
        self.m_applied = 0
        self.m_ma_period = -1
        self.m_ma_shift = -1
        self.m_deviation = EMPTY_VALUE
        self.m_applied = -1
    def _q_dtor(self):
        pass
    def MaPeriod(self):
        return self.m_ma_period
    def MaShift(self):
        return self.m_ma_shift
    def Deviation(self):
        return self.m_deviation
    def Applied(self):
        return self.m_applied
    def Create(self, symbol, period, ma_period, ma_shift, deviation, applied):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iBands(symbol, period, ma_period, ma_shift, deviation, applied)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_6(symbol, period, ma_period, ma_shift, deviation, applied):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Base(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Upper(self, index):
        buffer = self.At(1)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Lower(self, index):
        buffer = self.At(2)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_BANDS
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_6(symbol, period, _int(params[0].integer_value), _int(params[1].integer_value), params[2].double_value, _int(params[3].integer_value))
    def Initialize_6(self, symbol, period, ma_period, ma_shift, deviation, applied):
        if self.CreateBuffers(symbol, period, 3):
            self.m_name = 'Bands'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(ma_period) + ',' + IntegerToString(ma_shift) + ',' + DoubleToString(deviation) + ',' + CIndicator.PriceDescription(applied) + ') H=' + IntegerToString(self.m_handle)
            self.m_ma_period = ma_period
            self.m_ma_shift = ma_shift
            self.m_deviation = deviation
            self.m_applied = applied
            self.At(0).Name_1('BASE_LINE')
            self.At(0).Offset_1(ma_shift)
            self.At(1).Name_1('UPPER_BAND')
            self.At(1).Offset_1(ma_shift)
            self.At(2).Name_1('LOWER_BAND')
            self.At(2).Offset_1(ma_shift)
            return True
        return False

class CiEnvelopes(CIndicator):
    _q_fields = ('m_ma_period', 'm_ma_shift', 'm_ma_method', 'm_applied', 'm_deviation')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_ma_period = 0
        self.m_ma_shift = 0
        self.m_ma_method = 0
        self.m_applied = 0
        self.m_deviation = 0.0
        self.m_ma_period = -1
        self.m_ma_shift = -1
        self.m_ma_method = WRONG_VALUE
        self.m_applied = -1
        self.m_deviation = EMPTY_VALUE
    def _q_dtor(self):
        pass
    def MaPeriod(self):
        return self.m_ma_period
    def MaShift(self):
        return self.m_ma_shift
    def MaMethod(self):
        return self.m_ma_method
    def Applied(self):
        return self.m_applied
    def Deviation(self):
        return self.m_deviation
    def Create(self, symbol, period, ma_period, ma_shift, ma_method, applied, deviation):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iEnvelopes(symbol, period, ma_period, ma_shift, ma_method, applied, deviation)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_7(symbol, period, ma_period, ma_shift, ma_method, applied, deviation):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Upper(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Lower(self, index):
        buffer = self.At(1)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_ENVELOPES
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_7(symbol, period, _int(params[0].integer_value), _int(params[1].integer_value), params[2].integer_value, _int(params[3].integer_value), _int(params[4].double_value))
    def Initialize_7(self, symbol, period, ma_period, ma_shift, ma_method, applied, deviation):
        if self.CreateBuffers(symbol, period, 2):
            self.m_name = 'Envelopes'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(ma_period) + ',' + IntegerToString(ma_shift) + ',' + CIndicator.MethodDescription(ma_method) + ',' + CIndicator.PriceDescription(applied) + ',' + DoubleToString(deviation) + ') H=' + IntegerToString(self.m_handle)
            self.m_ma_period = ma_period
            self.m_ma_shift = ma_shift
            self.m_ma_method = ma_method
            self.m_applied = applied
            self.m_deviation = deviation
            self.At(0).Name_1('UPPER_LINE')
            self.At(0).Offset_1(ma_shift)
            self.At(1).Name_1('LOWER_LINE')
            self.At(1).Offset_1(ma_shift)
            return True
        return False

class CiIchimoku(CIndicator):
    _q_fields = ('m_tenkan_sen', 'm_kijun_sen', 'm_senkou_span_b')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_tenkan_sen = 0
        self.m_kijun_sen = 0
        self.m_senkou_span_b = 0
        self.m_tenkan_sen = -1
        self.m_kijun_sen = -1
        self.m_senkou_span_b = -1
    def _q_dtor(self):
        pass
    def TenkanSenPeriod(self):
        return self.m_tenkan_sen
    def KijunSenPeriod(self):
        return self.m_kijun_sen
    def SenkouSpanBPeriod(self):
        return self.m_senkou_span_b
    def Create(self, symbol, period, tenkan_sen, kijun_sen, senkou_span_b):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iIchimoku(symbol, period, tenkan_sen, kijun_sen, senkou_span_b)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_5(symbol, period, tenkan_sen, kijun_sen, senkou_span_b):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def TenkanSen(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def KijunSen(self, index):
        buffer = self.At(1)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def SenkouSpanA(self, index):
        buffer = self.At(2)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def SenkouSpanB(self, index):
        buffer = self.At(3)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def ChinkouSpan(self, index):
        buffer = self.At(4)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_ICHIMOKU
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_5(symbol, period, _int(params[0].integer_value), _int(params[1].integer_value), _int(params[2].integer_value))
    def Initialize_5(self, symbol, period, tenkan_sen, kijun_sen, senkou_span_b):
        if self.CreateBuffers(symbol, period, 5):
            self.m_name = 'Ichimoku'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(tenkan_sen) + ',' + IntegerToString(kijun_sen) + ',' + IntegerToString(senkou_span_b) + ') H=' + IntegerToString(self.m_handle)
            self.m_tenkan_sen = tenkan_sen
            self.m_kijun_sen = kijun_sen
            self.m_senkou_span_b = senkou_span_b
            self.At(0).Name_1('TENKANSEN_LINE')
            self.At(1).Name_1('KIJUNSEN_LINE')
            self.At(2).Name_1('SENKOUSPANA_LINE')
            self.At(2).Offset_1(kijun_sen)
            self.At(3).Name_1('SENKOUSPANB_LINE')
            self.At(3).Offset_1(kijun_sen)
            self.At(4).Name_1('CHIKOUSPAN_LINE')
            self.At(4).Offset_1(-kijun_sen)
            return True
        return False

class CiMA(CIndicator):
    _q_fields = ('m_ma_period', 'm_ma_shift', 'm_ma_method', 'm_applied')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_ma_period = 0
        self.m_ma_shift = 0
        self.m_ma_method = 0
        self.m_applied = 0
        self.m_ma_period = -1
        self.m_ma_shift = -1
        self.m_ma_method = WRONG_VALUE
        self.m_applied = -1
    def _q_dtor(self):
        pass
    def MaPeriod(self):
        return self.m_ma_period
    def MaShift(self):
        return self.m_ma_shift
    def MaMethod(self):
        return self.m_ma_method
    def Applied(self):
        return self.m_applied
    def Create(self, symbol, period, ma_period, ma_shift, ma_method, applied):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iMA(symbol, period, ma_period, ma_shift, ma_method, applied)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_6(symbol, period, ma_period, ma_shift, ma_method, applied):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Main(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_MA
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_6(symbol, period, _int(params[0].integer_value), _int(params[1].integer_value), params[2].integer_value, _int(params[3].integer_value))
    def Initialize_6(self, symbol, period, ma_period, ma_shift, ma_method, applied):
        if self.CreateBuffers(symbol, period, 1):
            self.m_name = 'MA'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(ma_period) + ',' + IntegerToString(ma_shift) + ',' + CIndicator.MethodDescription(ma_method) + ',' + CIndicator.PriceDescription(applied) + ') H=' + IntegerToString(self.m_handle)
            self.m_ma_period = ma_period
            self.m_ma_shift = ma_shift
            self.m_ma_method = ma_method
            self.m_applied = applied
            self.At(0).Name_1('MAIN_LINE')
            self.At(0).Offset_1(ma_shift)
            return True
        return False

class CiSAR(CIndicator):
    _q_fields = ('m_step', 'm_maximum')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_step = 0.0
        self.m_maximum = 0.0
        self.m_step = EMPTY_VALUE
        self.m_maximum = EMPTY_VALUE
    def _q_dtor(self):
        pass
    def SarStep(self):
        return self.m_step
    def Maximum(self):
        return self.m_maximum
    def Create(self, symbol, period, step, maximum):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iSAR(symbol, period, step, maximum)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_2(symbol, period, step, maximum):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Main(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_SAR
    def Initialize_1(self, symbol, period, num_params, params):
        return self.Initialize_2(symbol, period, params[0].double_value, params[1].double_value)
    def Initialize_2(self, symbol, period, step, maximum):
        if self.CreateBuffers(symbol, period, 1):
            self.m_name = 'SAR'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + DoubleToString(step, 4) + ',' + DoubleToString(maximum, 4) + ',' + ') H=' + IntegerToString(self.m_handle)
            self.m_step = step
            self.m_maximum = maximum
            self.At(0).Name_1('MAIN_LINE')
            return True
        return False

class CiStdDev(CIndicator):
    _q_fields = ('m_ma_period', 'm_ma_shift', 'm_ma_method', 'm_applied')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_ma_period = 0
        self.m_ma_shift = 0
        self.m_ma_method = 0
        self.m_applied = 0
        self.m_ma_period = -1
        self.m_ma_shift = -1
        self.m_ma_method = WRONG_VALUE
        self.m_applied = -1
    def _q_dtor(self):
        pass
    def MaPeriod(self):
        return self.m_ma_period
    def MaShift(self):
        return self.m_ma_shift
    def MaMethod(self):
        return self.m_ma_method
    def Applied(self):
        return self.m_applied
    def Create(self, symbol, period, ma_period, ma_shift, ma_method, applied):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iStdDev(symbol, period, ma_period, ma_shift, ma_method, applied)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_6(symbol, period, ma_period, ma_shift, ma_method, applied):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Main(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_STDDEV
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_6(symbol, period, _int(params[0].integer_value), _int(params[1].integer_value), params[2].integer_value, _int(params[3].integer_value))
    def Initialize_6(self, symbol, period, ma_period, ma_shift, ma_method, applied):
        if self.CreateBuffers(symbol, period, 1):
            self.m_name = 'StdDev'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(ma_period) + ',' + IntegerToString(ma_shift) + ',' + CIndicator.MethodDescription(ma_method) + ') H=' + IntegerToString(self.m_handle)
            self.m_ma_period = ma_period
            self.m_ma_shift = ma_shift
            self.m_ma_method = ma_method
            self.m_applied = applied
            self.At(0).Name_1('MAIN_LINE')
            self.At(0).Offset_1(ma_shift)
            return True
        return False

class CiDEMA(CIndicator):
    _q_fields = ('m_ma_period', 'm_ind_shift', 'm_applied')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_ma_period = 0
        self.m_ind_shift = 0
        self.m_applied = 0
        self.m_ma_period = -1
        self.m_ind_shift = -1
        self.m_applied = -1
    def _q_dtor(self):
        pass
    def MaPeriod(self):
        return self.m_ma_period
    def IndShift(self):
        return self.m_ind_shift
    def Applied(self):
        return self.m_applied
    def Create(self, symbol, period, ma_period, ind_shift, applied):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iDEMA(symbol, period, ma_period, ind_shift, applied)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_5(symbol, period, ma_period, ind_shift, applied):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Main(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_DEMA
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_5(symbol, period, _int(params[0].integer_value), _int(params[1].integer_value), _int(params[2].integer_value))
    def Initialize_5(self, symbol, period, ma_period, ind_shift, applied):
        if self.CreateBuffers(symbol, period, 1):
            self.m_name = 'DEMA'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(ma_period) + ',' + IntegerToString(ind_shift) + ',' + CIndicator.PriceDescription(applied) + ') H=' + IntegerToString(self.m_handle)
            self.m_ma_period = ma_period
            self.m_ind_shift = ind_shift
            self.m_applied = applied
            self.At(0).Name_1('MAIN_LINE')
            self.At(0).Offset_1(ind_shift)
            return True
        return False

class CiTEMA(CIndicator):
    _q_fields = ('m_ma_period', 'm_ind_shift', 'm_applied')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_ma_period = 0
        self.m_ind_shift = 0
        self.m_applied = 0
        self.m_ma_period = -1
        self.m_ind_shift = -1
        self.m_applied = -1
    def _q_dtor(self):
        pass
    def MaPeriod(self):
        return self.m_ma_period
    def IndShift(self):
        return self.m_ind_shift
    def Applied(self):
        return self.m_applied
    def Create(self, symbol, period, ma_period, ind_shift, applied):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iTEMA(symbol, period, ma_period, ind_shift, applied)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_5(symbol, period, ma_period, ind_shift, applied):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Main(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_TEMA
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_5(symbol, period, _int(params[0].integer_value), _int(params[1].integer_value), _int(params[2].integer_value))
    def Initialize_5(self, symbol, period, ma_period, ind_shift, applied):
        if self.CreateBuffers(symbol, period, 1):
            self.m_name = 'TEMA'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(ma_period) + ',' + IntegerToString(ind_shift) + ',' + CIndicator.PriceDescription(applied) + ') H=' + IntegerToString(self.m_handle)
            self.m_ma_period = ma_period
            self.m_ind_shift = ind_shift
            self.m_applied = applied
            self.At(0).Name_1('MAIN_LINE')
            self.At(0).Offset_1(ind_shift)
            return True
        return False

class CiFrAMA(CIndicator):
    _q_fields = ('m_ma_period', 'm_ind_shift', 'm_applied')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_ma_period = 0
        self.m_ind_shift = 0
        self.m_applied = 0
        self.m_ma_period = -1
        self.m_ind_shift = -1
        self.m_applied = -1
    def _q_dtor(self):
        pass
    def MaPeriod(self):
        return self.m_ma_period
    def IndShift(self):
        return self.m_ind_shift
    def Applied(self):
        return self.m_applied
    def Create(self, symbol, period, ma_period, ind_shift, applied):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iFrAMA(symbol, period, ma_period, ind_shift, applied)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_5(symbol, period, ma_period, ind_shift, applied):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Main(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_FRAMA
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_5(symbol, period, _int(params[0].integer_value), _int(params[1].integer_value), _int(params[2].integer_value))
    def Initialize_5(self, symbol, period, ma_period, ind_shift, applied):
        if self.CreateBuffers(symbol, period, 1):
            self.m_name = 'FrAMA'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(ma_period) + ',' + IntegerToString(ind_shift) + ',' + CIndicator.PriceDescription(applied) + ') H=' + IntegerToString(self.m_handle)
            self.m_ma_period = ma_period
            self.m_applied = applied
            self.At(0).Name_1('MAIN_LINE')
            self.At(0).Offset_1(ind_shift)
            return True
        return False

class CiAMA(CIndicator):
    _q_fields = ('m_ma_period', 'm_fast_ema_period', 'm_slow_ema_period', 'm_ind_shift', 'm_applied')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_ma_period = 0
        self.m_fast_ema_period = 0
        self.m_slow_ema_period = 0
        self.m_ind_shift = 0
        self.m_applied = 0
        self.m_ma_period = -1
        self.m_fast_ema_period = -1
        self.m_slow_ema_period = -1
        self.m_ind_shift = -1
        self.m_applied = -1
    def _q_dtor(self):
        pass
    def MaPeriod(self):
        return self.m_ma_period
    def FastEmaPeriod(self):
        return self.m_fast_ema_period
    def SlowEmaPeriod(self):
        return self.m_slow_ema_period
    def IndShift(self):
        return self.m_ind_shift
    def Applied(self):
        return self.m_applied
    def Create(self, symbol, period, ma_period, fast_ema_period, slow_ema_period, ind_shift, applied):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iAMA(symbol, period, ma_period, fast_ema_period, slow_ema_period, ind_shift, applied)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_7(symbol, period, ma_period, fast_ema_period, slow_ema_period, ind_shift, applied):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Main(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_AMA
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_7(symbol, period, _int(params[0].integer_value), _int(params[1].integer_value), _int(params[2].integer_value), _int(params[3].integer_value), _int(params[4].integer_value))
    def Initialize_7(self, symbol, period, ma_period, fast_ema_period, slow_ema_period, ind_shift, applied):
        if self.CreateBuffers(symbol, period, 1):
            self.m_name = 'AMA'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(ma_period) + ',' + IntegerToString(fast_ema_period) + ',' + IntegerToString(slow_ema_period) + ',' + IntegerToString(ind_shift) + ',' + CIndicator.PriceDescription(applied) + ') H=' + IntegerToString(self.m_handle)
            self.m_ma_period = ma_period
            self.m_fast_ema_period = fast_ema_period
            self.m_slow_ema_period = slow_ema_period
            self.m_ind_shift = ind_shift
            self.m_applied = applied
            self.At(0).Name_1('MAIN_LINE')
            self.At(0).Offset_1(ind_shift)
            return True
        return False

class CiVIDyA(CIndicator):
    _q_fields = ('m_cmo_period', 'm_ema_period', 'm_ind_shift', 'm_applied')
    def __init__(self):
        CIndicator.__init__(self)
        self.m_cmo_period = 0
        self.m_ema_period = 0
        self.m_ind_shift = 0
        self.m_applied = 0
        self.m_cmo_period = -1
        self.m_ema_period = -1
        self.m_ind_shift = -1
        self.m_applied = -1
    def _q_dtor(self):
        pass
    def CmoPeriod(self):
        return self.m_cmo_period
    def EmaPeriod(self):
        return self.m_ema_period
    def IndShift(self):
        return self.m_ind_shift
    def Applied(self):
        return self.m_applied
    def Create(self, symbol, period, cmo_period, ema_period, ind_shift, applied):
        if not self.SetSymbolPeriod(symbol, period):
            return False
        self.m_handle = iVIDyA(symbol, period, cmo_period, ema_period, ind_shift, applied)
        if self.m_handle == INVALID_HANDLE:
            return False
        if not self.Initialize_6(symbol, period, cmo_period, ema_period, ind_shift, applied):
            IndicatorRelease(self.m_handle)
            self.m_handle = INVALID_HANDLE
            return False
        return True
    def Main(self, index):
        buffer = self.At(0)
        if buffer is None:
            return EMPTY_VALUE
        return buffer.At(index)
    def Type(self):
        return IND_VIDYA
    def Initialize_4(self, symbol, period, num_params, params):
        return self.Initialize_6(symbol, period, _int(params[0].integer_value), _int(params[1].integer_value), _int(params[2].integer_value), _int(params[3].integer_value))
    def Initialize_6(self, symbol, period, cmo_period, ema_period, ind_shift, applied):
        if self.CreateBuffers(symbol, period, 1):
            self.m_name = 'VIDyA'
            self.m_status = '(' + symbol + ',' + self.PeriodDescription() + ',' + IntegerToString(cmo_period) + ',' + IntegerToString(ema_period) + ',' + IntegerToString(ind_shift) + ',' + CIndicator.PriceDescription(applied) + ') H=' + IntegerToString(self.m_handle)
            self.m_cmo_period = cmo_period
            self.m_ema_period = ema_period
            self.m_ind_shift = ind_shift
            self.m_applied = applied
            self.At(0).Name_1('MAIN_LINE')
            self.At(0).Offset_1(ind_shift)
            return True
        return False

def OnInit():
    global ShowAUD, ShowCAD, ShowCHF, ShowEUR, ShowGBP, ShowJPY, ShowNZD, ShowUSD, handle_atr, init_status
    ArrayInitialize(chart_currency_index, -1)
    symbol_name_clean = StringSubstr(Symbol(), 0, 6)
    symbol_name_part = Arr(2, "", dyn=False)
    symbol_name_part[0] = StringSubstr(symbol_name_clean, 0, 3)
    symbol_name_part[1] = StringSubstr(symbol_name_clean, 3, 3)
    for c in range(0, ArraySize(Currencies)):
        for p in range(0, 2):
            if Currencies[c] != symbol_name_part[p]:
                continue
            chart_currency_index[p] = c
            _sw4 = c
            if _sw4 == 0:
                ShowEUR = True
            elif _sw4 == 1:
                ShowGBP = True
            elif _sw4 == 2:
                ShowAUD = True
            elif _sw4 == 3:
                ShowNZD = True
            elif _sw4 == 4:
                ShowUSD = True
            elif _sw4 == 5:
                ShowCAD = True
            elif _sw4 == 6:
                ShowCHF = True
            elif _sw4 == 7:
                ShowJPY = True
    if chart_currency_index[0] < 0 or chart_currency_index[1] < 0:
        Print('OnInit', ' wrong symbol')
        init_status = False
    handle_atr = iATR(None, PERIOD_CURRENT, inp_atr_period)
    if handle_atr == INVALID_HANDLE:
        Alert("Can't get atr handle")
        return INIT_FAILED
    ShortName = 'Currency Strength Index CSI(' + _str(inp_ma_period) + '/' + _str(inp_ma_delta) + ') >>'
    IndicatorSetString(INDICATOR_SHORTNAME, ShortName)
    SetIndexBuffer(0, ext_arrow_up, INDICATOR_DATA)
    SetIndexBuffer(1, ext_arrow_dn, INDICATOR_DATA)
    SetIndexBuffer(2, ext_trend, INDICATOR_DATA)
    SetIndexBuffer(3, EURx, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, GBPx, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, AUDx, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, NZDx, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, USDx, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, CADx, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, CHFx, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, JPYx, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'Arrow up')
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetString(1, PLOT_LABEL, 'Arrow down')
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    ArraySetAsSeries(EURx, True)
    ArraySetAsSeries(GBPx, True)
    ArraySetAsSeries(AUDx, True)
    ArraySetAsSeries(NZDx, True)
    ArraySetAsSeries(USDx, True)
    ArraySetAsSeries(CADx, True)
    ArraySetAsSeries(CHFx, True)
    ArraySetAsSeries(JPYx, True)
    ArraySetAsSeries(ext_arrow_up, True)
    ArraySetAsSeries(ext_arrow_dn, True)
    ArraySetAsSeries(ext_trend, True)
    if not CreateHandles():
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'obj_csi_')

def CreateHandles():
    SymbolSuffix = StringSubstr(Symbol(), 6, StringLen(Symbol()) - 6)
    i = 0
    while i < ArraySize(symbols):
        symbol = symbols[i] + SymbolSuffix
        if not CheckMarketWatch(symbol):
            return False
        if not ma[i].Create(symbol, PERIOD_CURRENT, inp_ma_period, 0, MODE_LWMA, PRICE_CLOSE):
            Print('CreateHandles', ': failed to create handle of iMA indicator for symbol ', symbol)
            return False
        i += 1
    return True

def CheckMarketWatch(symbol):
    if not SymbolInfoInteger(symbol, SYMBOL_SELECT):
        if GetLastError() == ERR_MARKET_UNKNOWN_SYMBOL:
            printf('CheckMarketWatch' + ": Unknown symbol '%s'", symbol)
            return False
        if not SymbolSelect(symbol, True):
            printf('CheckMarketWatch' + ': Error adding symbol %d', GetLastError())
            return False
    return True

def CheckLoadHistory(symbol, period, size):
    if Bars(symbol, period) < size:
        times = Arr(1, 0, dyn=False)
        CopyTime(symbol, period, size - 1, 1, times)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global A1, A2, A3, A4, A5, A6, A7, AUD, CAD, CHF, EUR, GBP, JPY, NZD, USD
    if not init_status:
        return rates_total
    limit = rates_total
    i = 0
    while i < ArraySize(ma):
        if ma[i].BarsCalculated() < 0:
            Print('OnCalculate' + ': ', symbols[i], ' not ready.')
            CheckLoadHistory(symbols[i], PERIOD_CURRENT, 100)
            return 0
        ma[i].Refresh()
        limit = MathMin(limit, ma[i].BarsCalculated())
        i += 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = limit - inp_ma_delta
    else:
        limit = rates_total - prev_calculated + 1
    for i in range(0, limit):
        if ShowEUR:
            A1 = _fdiv(ma[11].Main(i), ma[11].Main(i + inp_ma_delta))
            A2 = _fdiv(ma[8].Main(i), ma[8].Main(i + inp_ma_delta))
            A3 = _fdiv(ma[13].Main(i), ma[13].Main(i + inp_ma_delta))
            A4 = _fdiv(ma[14].Main(i), ma[14].Main(i + inp_ma_delta))
            A5 = _fdiv(ma[9].Main(i), ma[9].Main(i + inp_ma_delta))
            A6 = _fdiv(ma[10].Main(i), ma[10].Main(i + inp_ma_delta))
            A7 = _fdiv(ma[12].Main(i), ma[12].Main(i + inp_ma_delta))
            EUR = (A1 * A2 * A3 * A4 * A5 * A6 * A7) - 1
            EURx[i] = EUR
        if ShowGBP:
            A1 = _fdiv(ma[11].Main(i), ma[11].Main(i + inp_ma_delta))
            A2 = _fdiv(ma[15].Main(i), ma[15].Main(i + inp_ma_delta))
            A3 = _fdiv(ma[19].Main(i), ma[19].Main(i + inp_ma_delta))
            A4 = _fdiv(ma[20].Main(i), ma[20].Main(i + inp_ma_delta))
            A5 = _fdiv(ma[16].Main(i), ma[16].Main(i + inp_ma_delta))
            A6 = _fdiv(ma[17].Main(i), ma[17].Main(i + inp_ma_delta))
            A7 = _fdiv(ma[18].Main(i), ma[18].Main(i + inp_ma_delta))
            GBP = (_fdiv(1, A1) * A2 * A3 * A4 * A5 * A6 * A7) - 1
            GBPx[i] = GBP
        if ShowAUD:
            A1 = _fdiv(ma[8].Main(i), ma[8].Main(i + inp_ma_delta))
            A2 = _fdiv(ma[15].Main(i), ma[15].Main(i + inp_ma_delta))
            A3 = _fdiv(ma[3].Main(i), ma[3].Main(i + inp_ma_delta))
            A4 = _fdiv(ma[4].Main(i), ma[4].Main(i + inp_ma_delta))
            A5 = _fdiv(ma[0].Main(i), ma[0].Main(i + inp_ma_delta))
            A6 = _fdiv(ma[1].Main(i), ma[1].Main(i + inp_ma_delta))
            A7 = _fdiv(ma[2].Main(i), ma[2].Main(i + inp_ma_delta))
            AUD = (_fdiv(_fdiv(1, A1) * 1, A2) * A3 * A4 * A5 * A6 * A7) - 1
            AUDx[i] = AUD
        if ShowNZD:
            A1 = _fdiv(ma[13].Main(i), ma[13].Main(i + inp_ma_delta))
            A2 = _fdiv(ma[19].Main(i), ma[19].Main(i + inp_ma_delta))
            A3 = _fdiv(ma[3].Main(i), ma[3].Main(i + inp_ma_delta))
            A4 = _fdiv(ma[24].Main(i), ma[24].Main(i + inp_ma_delta))
            A5 = _fdiv(ma[21].Main(i), ma[21].Main(i + inp_ma_delta))
            A6 = _fdiv(ma[22].Main(i), ma[22].Main(i + inp_ma_delta))
            A7 = _fdiv(ma[23].Main(i), ma[23].Main(i + inp_ma_delta))
            NZD = (_fdiv(_fdiv(_fdiv(1, A1) * 1, A2) * 1, A3) * A4 * A5 * A6 * A7) - 1
            NZDx[i] = NZD
        if ShowUSD:
            A1 = _fdiv(ma[14].Main(i), ma[14].Main(i + inp_ma_delta))
            A2 = _fdiv(ma[20].Main(i), ma[20].Main(i + inp_ma_delta))
            A3 = _fdiv(ma[4].Main(i), ma[4].Main(i + inp_ma_delta))
            A4 = _fdiv(ma[24].Main(i), ma[24].Main(i + inp_ma_delta))
            A5 = _fdiv(ma[26].Main(i), ma[26].Main(i + inp_ma_delta))
            A6 = _fdiv(ma[26].Main(i), ma[26].Main(i + inp_ma_delta))
            A7 = _fdiv(ma[27].Main(i), ma[27].Main(i + inp_ma_delta))
            USD = (_fdiv(_fdiv(_fdiv(_fdiv(1, A1) * 1, A2) * 1, A3) * 1, A4) * A5 * A6 * A7) - 1
            USDx[i] = USD
        if ShowCAD:
            A1 = _fdiv(ma[9].Main(i), ma[9].Main(i + inp_ma_delta))
            A2 = _fdiv(ma[16].Main(i), ma[16].Main(i + inp_ma_delta))
            A3 = _fdiv(ma[0].Main(i), ma[0].Main(i + inp_ma_delta))
            A4 = _fdiv(ma[21].Main(i), ma[21].Main(i + inp_ma_delta))
            A5 = _fdiv(ma[26].Main(i), ma[26].Main(i + inp_ma_delta))
            A6 = _fdiv(ma[5].Main(i), ma[5].Main(i + inp_ma_delta))
            A7 = _fdiv(ma[6].Main(i), ma[6].Main(i + inp_ma_delta))
            CAD = (_fdiv(_fdiv(_fdiv(_fdiv(_fdiv(1, A1) * 1, A2) * 1, A3) * 1, A4) * 1, A5) * A6 * A7) - 1
            CADx[i] = CAD
        if ShowCHF:
            A1 = _fdiv(ma[10].Main(i), ma[10].Main(i + inp_ma_delta))
            A2 = _fdiv(ma[17].Main(i), ma[17].Main(i + inp_ma_delta))
            A3 = _fdiv(ma[1].Main(i), ma[1].Main(i + inp_ma_delta))
            A4 = _fdiv(ma[22].Main(i), ma[22].Main(i + inp_ma_delta))
            A5 = _fdiv(ma[26].Main(i), ma[26].Main(i + inp_ma_delta))
            A6 = _fdiv(ma[5].Main(i), ma[5].Main(i + inp_ma_delta))
            A7 = _fdiv(ma[7].Main(i), ma[7].Main(i + inp_ma_delta))
            CHF = (_fdiv(_fdiv(_fdiv(_fdiv(_fdiv(_fdiv(1, A1) * 1, A2) * 1, A3) * 1, A4) * 1, A5) * 1, A6) * A7) - 1
            CHFx[i] = CHF
        if ShowJPY:
            A1 = _fdiv(ma[12].Main(i), ma[12].Main(i + inp_ma_delta))
            A2 = _fdiv(ma[18].Main(i), ma[18].Main(i + inp_ma_delta))
            A3 = _fdiv(ma[2].Main(i), ma[2].Main(i + inp_ma_delta))
            A4 = _fdiv(ma[23].Main(i), ma[23].Main(i + inp_ma_delta))
            A5 = _fdiv(ma[27].Main(i), ma[27].Main(i + inp_ma_delta))
            A6 = _fdiv(ma[6].Main(i), ma[6].Main(i + inp_ma_delta))
            A7 = _fdiv(ma[7].Main(i), ma[7].Main(i + inp_ma_delta))
            JPY = _fdiv(_fdiv(_fdiv(_fdiv(_fdiv(_fdiv(_fdiv(1, A1) * 1, A2) * 1, A3) * 1, A4) * 1, A5) * 1, A6) * 1, A7) - 1
            JPYx[i] = JPY
    for i in range(limit, 0, -1):
        value_line = Arr(2, 0.0, dyn=False, dims=(2,))
        for c in range(0, 2):
            _sw5 = chart_currency_index[c]
            if _sw5 == 0:
                value_line[c][0] = EURx[i + 0]
                value_line[c][1] = EURx[i + 1]
            elif _sw5 == 1:
                value_line[c][0] = GBPx[i + 0]
                value_line[c][1] = GBPx[i + 1]
            elif _sw5 == 2:
                value_line[c][0] = AUDx[i + 0]
                value_line[c][1] = AUDx[i + 1]
            elif _sw5 == 3:
                value_line[c][0] = NZDx[i + 0]
                value_line[c][1] = NZDx[i + 1]
            elif _sw5 == 4:
                value_line[c][0] = USDx[i + 0]
                value_line[c][1] = USDx[i + 1]
            elif _sw5 == 5:
                value_line[c][0] = CADx[i + 0]
                value_line[c][1] = CADx[i + 1]
            elif _sw5 == 6:
                value_line[c][0] = CHFx[i + 0]
                value_line[c][1] = CHFx[i + 1]
            elif _sw5 == 7:
                value_line[c][0] = JPYx[i + 0]
                value_line[c][1] = JPYx[i + 1]
        atr_value = Arr(0, 0.0)
        CopyBuffer(handle_atr, 0, i, 1, atr_value)
        line_shift = atr_value[0] * inp_atr_coefficient
        ext_trend[i] = ext_trend[i + 1]
        if ((value_line[0][0] - value_line[1][0]) > line_shift and (value_line[0][1] - value_line[1][1]) <= line_shift) and ext_trend[i] != 1:
            ext_arrow_up[i] = iLow(None, PERIOD_CURRENT, i) - (atr_value[0] / 3)
            ext_trend[i] = 1.0
        else:
            ext_arrow_up[i] = 0.0
        if ((value_line[0][0] - value_line[1][0]) < (-line_shift) and (value_line[0][1] - value_line[1][1]) >= (-line_shift)) and ext_trend[i] != -1:
            ext_arrow_dn[i] = iHigh(None, PERIOD_CURRENT, i) + (atr_value[0] / 3)
            ext_trend[i] = -1.0
        else:
            ext_arrow_dn[i] = 0.0
    return rates_total

# ---- global variables initialised from expressions
ma = Arr(28, 0, dyn=False, factory=CiMA)

# ---- static local variables
_s_CSeries_PeriodDescription__p_str = Arr.of(['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M10', 'M12', 'M15', 'M20', 'M30', 'H1', 'H2', 'H3', 'H4', 'H6', 'H8', 'H12', 'D1', 'W1', 'MN', 'UNKNOWN'], fill="")
_s_CSeries_PeriodDescription__p_int = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_s_CSeries_PeriodToTimeframeFlag__p_int = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StrengthIndexSignalV10(_MQL5Indicator):
    name = 'Strength Index Signal v1.0'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inp_ma_period': 50,  # strenght accumulation period
        'inp_ma_delta': 1,  # delta
        'inp_atr_period': 20,  # atr period
        'inp_atr_coefficient': 1.0,  # atr delta
    }

