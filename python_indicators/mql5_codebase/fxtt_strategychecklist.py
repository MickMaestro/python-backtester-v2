"""FXTT_StrategyChecklist — converted from MQL5: MQL5 Indicators/Strategy Checklist/FXTT_StrategyChecklist.mq5

Copyright: Copyright 2016, Carlos Oliveira; Link: https://www.forextradingtools.eu/; Version: 2.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Functions not available here: ChartPriceOnDropped, ChartTimeOnDropped, ChartWindowOnDropped, ChartXOnDropped, ChartYOnDropped, FileReadLong, FileReadStruct, FileWriteLong, FileWriteStruct
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.controls_wnd import *  # #include Wnd.mqh
from backtester.mql5.lib.controls_rect import *  # #include Rect.mqh
from backtester.mql5.lib.controls_defines import *  # #include Defines.mqh
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh
from backtester.mql5.lib.controls_wndobj import *  # #include WndObj.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2016, Carlos Oliveira', 'link': 'https://www.forextradingtools.eu/', 'version': '2.0', 'window': 'chart', 'indicator_plots': 0, 'indicator_buffers': 0, 'indicator_minimum': 0.0, 'indicator_maximum': 0.0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'FXTT_StrategyChecklist', 'source': 'MQL5 Indicators/Strategy Checklist/FXTT_StrategyChecklist.mq5', 'folder': 'Strategy Checklist', 'inputs': [{'mql': 'TAG', 'py': 'TAG', 'param': None, 'type': 'string', 'default': 'FxTT_SC20_', 'label': '', 'sinput': False}, {'mql': 'Location', 'py': 'Location', 'param': 'Location', 'type': 'int', 'default': 2, 'label': 'Window Location', 'sinput': False}, {'mql': 'Check01', 'py': 'Check01', 'param': None, 'type': 'string', 'default': '>------- Example 1 -------<', 'label': '', 'sinput': False}, {'mql': 'Check02', 'py': 'Check02', 'param': None, 'type': 'string', 'default': 'Example 2', 'label': '', 'sinput': False}, {'mql': 'Check03', 'py': 'Check03', 'param': None, 'type': 'string', 'default': 'Example 3', 'label': '', 'sinput': False}, {'mql': 'Check04', 'py': 'Check04', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check05', 'py': 'Check05', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check06', 'py': 'Check06', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check07', 'py': 'Check07', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check08', 'py': 'Check08', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check09', 'py': 'Check09', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check10', 'py': 'Check10', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check11', 'py': 'Check11', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check12', 'py': 'Check12', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check13', 'py': 'Check13', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check14', 'py': 'Check14', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check15', 'py': 'Check15', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check16', 'py': 'Check16', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check17', 'py': 'Check17', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check18', 'py': 'Check18', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check19', 'py': 'Check19', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Check20', 'py': 'Check20', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Wnd.mqh', 'Rect.mqh', 'Defines.mqh', 'Object.mqh', 'StdLibErr.mqh', 'WndObj.mqh']}

CHAR_VALUE = 0  # MQL5 constant unknown to the converter
INT_VALUE = 0  # MQL5 constant unknown to the converter
OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter
OBJ_NO_PERIODS = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
TAG = _input('TAG', 'FxTT_SC20_')
Location = _input('Location', CORNER_RIGHT_LOWER)  # Window Location
Check01 = _input('Check01', '>------- Example 1 -------<')
Check02 = _input('Check02', 'Example 2')
Check03 = _input('Check03', 'Example 3')
Check04 = _input('Check04', '')
Check05 = _input('Check05', '')
Check06 = _input('Check06', '')
Check07 = _input('Check07', '')
Check08 = _input('Check08', '')
Check09 = _input('Check09', '')
Check10 = _input('Check10', '')
Check11 = _input('Check11', '')
Check12 = _input('Check12', '')
Check13 = _input('Check13', '')
Check14 = _input('Check14', '')
Check15 = _input('Check15', '')
Check16 = _input('Check16', '')
Check17 = _input('Check17', '')
Check18 = _input('Check18', '')
Check19 = _input('Check19', '')
Check20 = _input('Check20', '')
DataFileName = 'data.bin'  # File name
DataDirectoryName = 'SChecklist'  # Folder name

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

class CWndContainer(CWnd):
    _q_fields = ('m_controls',)
    def __init__(self):
        CWnd.__init__(self)
        self.m_controls = CArrayObj()
    def _q_dtor(self):
        pass
    def Destroy(self, reason=0):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(0)
            if control is None:
                continue
            control.Destroy()
            self.m_controls.Delete(0)
    def OnEvent(self, id_, lparam, dparam, sparam):
        if self.m_drag_object is not None and self.m_drag_object.OnEvent(id_, lparam, dparam, sparam):
            return True
        total = self.m_controls.Total()
        for i in range(total - 1, 0 - 1, -1):
            control = self.Control(i)
            if control is None:
                continue
            if control.OnEvent(id_, lparam, dparam, sparam):
                return True
        return False
    def OnMouseEvent(self, x, y, flags):
        if not ((self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0):
            return False
        if self.m_drag_object is not None and self.m_drag_object.OnMouseEvent(x, y, flags):
            return True
        total = self.m_controls.Total()
        for i in range(total - 1, 0 - 1, -1):
            control = self.Control(i)
            if control is None:
                continue
            if control.OnMouseEvent(x, y, flags):
                return True
        return CWnd.OnMouseEvent(self, x, y, flags)
    def ControlsTotal(self):
        return self.m_controls.Total()
    def Control(self, ind):
        return self.m_controls.At(ind)
    def ControlFind(self, id_):
        result = CWnd.ControlFind(self, id_)
        if result is not None:
            return result
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            result = control.ControlFind(id_)
            if result is not None:
                break
        return result
    def MouseFocusKill(self, id_=-1):
        if not ((self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0):
            return False
        self.Deactivate()
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.MouseFocusKill()
        return True
    def Add_1(self, control):
        if control is None:
            return False
        control.Shift(self.Left_0(), self.Top_0())
        if (self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0 and control.IsVisible():
            control.Visible(self.Contains_1(control))
        else:
            control.Hide()
        if (self.m_state_flags & WND_STATE_FLAG_ENABLE) != 0:
            control.Enable()
        else:
            control.Disable()
        return self.m_controls.Add(control)
    def Add_2(self, control):
        return self.Add_1(control)
    def Delete_1(self, control):
        if control is None:
            return False
        total = self.m_controls.Total()
        for i in range(0, total):
            pointer = self.Control(i)
            if pointer is None:
                continue
            if pointer == control:
                return self.m_controls.Delete(i)
        return False
    def Delete_2(self, control):
        return self.Delete_1(control)
    def Move_2(self, x, y):
        return self.Shift(x - self.Left_0(), y - self.Top_0())
    def Move_1(self, point):
        return self.Shift(point.x - self.Left_0(), point.y - self.Top_0())
    def Shift(self, dx, dy):
        if not CWnd.Shift(self, dx, dy):
            return False
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Shift(dx, dy)
        return True
    def Id_1(self, id_):
        id_used = 1
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            id_used += control.Id_1(id_ + id_used)
        self.m_id = id_
        return id_used
    def Id_0(self):
        return CWnd.Id_0(self)
    def Enable(self):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Enable()
        return CWnd.Enable(self)
    def Disable(self):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Disable()
        return CWnd.Disable(self)
    def Show(self):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Show()
        return CWnd.Show(self)
    def Hide(self):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Hide()
        return CWnd.Hide(self)
    def Save(self, file_handle):
        result = True
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            result &= control.Save(file_handle)
        return result
    def Load(self, file_handle):
        result = True
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            result &= control.Load(file_handle)
        return result
    def OnResize(self):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            if not control.Align(self.Rect()):
                return False
        return True
    def OnActivate(self):
        if (self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0:
            return False
        self.Activate()
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Activate()
        return True
    def OnDeactivate(self):
        if not ((self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0):
            return False
        self.Deactivate()
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Deactivate()
        return True

class CChartObject(CObject):
    _q_fields = ('m_chart_id', 'm_window', 'm_name', 'm_num_points')
    def __init__(self):
        CObject.__init__(self)
        self.m_chart_id = 0
        self.m_window = 0
        self.m_name = ""
        self.m_num_points = 0
        self.Detach()
    def _q_dtor(self):
        if self.m_chart_id != -1:
            ObjectDelete(self.m_chart_id, self.m_name)
    def Type(self):
        return 0x8888
    def ChartId(self):
        return self.m_chart_id
    def Window(self):
        return self.m_window
    def Name_0(self):
        return self.m_name
    def Name_1(self, name):
        if self.m_chart_id == -1:
            return False
        if ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_NAME, name):
            self.m_name = name
            return True
        return False
    def NumPoints(self):
        return self.m_num_points
    def Attach(self, chart_id, name, window, points):
        if ObjectFind(chart_id, name) < 0:
            return False
        if chart_id == 0:
            chart_id = ChartID()
        self.m_chart_id = chart_id
        self.m_window = window
        self.m_name = name
        self.m_num_points = points
        return True
    def SetPoint(self, point, time, price):
        if self.m_chart_id == -1:
            return False
        if point >= self.m_num_points:
            return False
        return ObjectMove(self.m_chart_id, self.m_name, point, time, price)
    def Delete(self):
        if self.m_chart_id == -1:
            return False
        result = ObjectDelete(self.m_chart_id, self.m_name)
        self.Detach()
        return result
    def Detach(self):
        self.m_chart_id = -1
        self.m_window = -1
        self.m_name = ""
        self.m_num_points = 0
    def Time_1(self, point):
        if self.m_chart_id == -1:
            return 0
        if point >= self.m_num_points:
            return 0
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_TIME, point)
    def Time_2(self, point, time):
        if self.m_chart_id == -1:
            return False
        if point >= self.m_num_points:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_TIME, point, time)
    def Price_1(self, point):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        if point >= self.m_num_points:
            return EMPTY_VALUE
        return ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_PRICE, point)
    def Price_2(self, point, price):
        if self.m_chart_id == -1:
            return False
        if point >= self.m_num_points:
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_PRICE, point, price)
    def Color_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_COLOR))
    def Color_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_COLOR, new_color)
    def Style_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STYLE)
    def Style_1(self, new_style):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STYLE, new_style)
    def Width_0(self):
        if self.m_chart_id == -1:
            return -1
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_WIDTH))
    def Width_1(self, new_width):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_WIDTH, new_width)
    def Background_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BACK))
    def Background_1(self, new_back):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BACK, new_back)
    def Fill_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_FILL))
    def Fill_1(self, new_fill):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_FILL, new_fill)
    def Z_Order_0(self):
        if self.m_chart_id == -1:
            return 0
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_ZORDER)
    def Z_Order_1(self, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_ZORDER, value)
    def Selected_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTED))
    def Selected_1(self, new_sel):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTED, new_sel)
    def Selectable_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTABLE))
    def Selectable_1(self, new_sel):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTABLE, new_sel)
    def Description_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_TEXT)
    def Description_1(self, new_text):
        if self.m_chart_id == -1:
            return False
        if new_text == '':
            return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_TEXT, ' ')
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_TEXT, new_text)
    def Tooltip_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_TOOLTIP)
    def Tooltip_1(self, new_text):
        if self.m_chart_id == -1:
            return False
        if new_text == '':
            return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_TOOLTIP, ' ')
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_TOOLTIP, new_text)
    def Timeframes_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_TIMEFRAMES))
    def Timeframes_1(self, timeframes):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_TIMEFRAMES, timeframes)
    def CreateTime(self):
        if self.m_chart_id == -1:
            return 0
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_CREATETIME)
    def LevelsCount_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELS))
    def LevelsCount_1(self, new_count):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELS, new_count)
    def LevelColor_1(self, level):
        if self.m_chart_id == -1:
            return clrNONE
        if level >= self.LevelsCount_0():
            return clrNONE
        return _uint(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELCOLOR, level))
    def LevelColor_2(self, level, new_color):
        if self.m_chart_id == -1:
            return False
        if level >= self.LevelsCount_0():
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELCOLOR, level, new_color)
    def LevelStyle_1(self, level):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        if level >= self.LevelsCount_0():
            return WRONG_VALUE
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELSTYLE, level)
    def LevelStyle_2(self, level, new_style):
        if self.m_chart_id == -1:
            return False
        if level >= self.LevelsCount_0():
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELSTYLE, level, new_style)
    def LevelWidth_1(self, level):
        if self.m_chart_id == -1:
            return -1
        if level >= self.LevelsCount_0():
            return -1
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELWIDTH, level))
    def LevelWidth_2(self, level, new_width):
        if self.m_chart_id == -1:
            return False
        if level >= self.LevelsCount_0():
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELWIDTH, level, new_width)
    def LevelValue_1(self, level):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        if level >= self.LevelsCount_0():
            return EMPTY_VALUE
        return ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_LEVELVALUE, level)
    def LevelValue_2(self, level, new_value):
        if self.m_chart_id == -1:
            return False
        if level >= self.LevelsCount_0():
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_LEVELVALUE, level, new_value)
    def LevelDescription_1(self, level):
        if self.m_chart_id == -1:
            return ''
        if level >= self.LevelsCount_0():
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_LEVELTEXT, level)
    def LevelDescription_2(self, level, new_text):
        if self.m_chart_id == -1:
            return False
        if level >= self.LevelsCount_0():
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_LEVELTEXT, level, new_text)
    def GetInteger_2(self, prop_id, modifier=-1):
        if self.m_chart_id == -1:
            return 0
        if modifier == -1:
            return ObjectGetInteger(self.m_chart_id, self.m_name, prop_id)
        return ObjectGetInteger(self.m_chart_id, self.m_name, prop_id, modifier)
    def GetInteger_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return (ObjectGetInteger(self.m_chart_id, self.m_name, prop_id, modifier, value) != 0)
    def SetInteger_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, prop_id, modifier, value)
    def SetInteger_2(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, prop_id, value)
    def GetDouble_2(self, prop_id, modifier=-1):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        if modifier == -1:
            return ObjectGetDouble(self.m_chart_id, self.m_name, prop_id)
        return ObjectGetDouble(self.m_chart_id, self.m_name, prop_id, modifier)
    def GetDouble_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return (ObjectGetDouble(self.m_chart_id, self.m_name, prop_id, modifier, value) != 0)
    def SetDouble_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, prop_id, modifier, value)
    def SetDouble_2(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, prop_id, value)
    def GetString_2(self, prop_id, modifier=-1):
        if self.m_chart_id == -1:
            return ''
        if modifier == -1:
            return ObjectGetString(self.m_chart_id, self.m_name, prop_id)
        return ObjectGetString(self.m_chart_id, self.m_name, prop_id, modifier)
    def GetString_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetString(self.m_chart_id, self.m_name, prop_id, modifier, value))
    def SetString_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, prop_id, modifier, value)
    def SetString_2(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, prop_id, value)
    def ShiftObject(self, d_time, d_price):
        result = True
        i = 0
        if self.m_chart_id == -1:
            return False
        i = 0
        while i < self.m_num_points:
            result &= self.ShiftPoint(i, d_time, d_price)
            i += 1
        return result
    def ShiftPoint(self, point, d_time, d_price):
        if self.m_chart_id == -1:
            return False
        if point >= self.m_num_points:
            return False
        time = ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_TIME, point)
        price = ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_PRICE, point)
        return ObjectMove(self.m_chart_id, self.m_name, point, time + d_time, price + d_price)
    def Save(self, file_handle):
        i = 0
        len_ = 0
        levels = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if _missing('FileWriteLong')(file_handle, -1) != 8:
            return False
        if FileWriteInteger(file_handle, self.Type(), INT_VALUE) != INT_VALUE:
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_NAME)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0:
            if FileWriteString(file_handle, str_, len_) != len_:
                return False
        if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_COLOR)) != 8:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STYLE))) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_WIDTH))) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BACK)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTABLE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_TIMEFRAMES)), INT_VALUE) != 4:
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_TEXT)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0:
            if FileWriteString(file_handle, str_, len_) != len_:
                return False
        if FileWriteInteger(file_handle, self.m_num_points, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, self.m_num_points):
            if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_TIME, i)) != 8:
                return False
            if FileWriteDouble(file_handle, ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_PRICE, i)) != 8:
                return False
        else:
            i = _range_end(i, self.m_num_points, 1)
        levels = _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELS))
        if FileWriteInteger(file_handle, levels, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, levels):
            if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELCOLOR, i)) != 8:
                return False
            if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELSTYLE, i))) != 4:
                return False
            if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELWIDTH, i))) != 4:
                return False
            if FileWriteDouble(file_handle, ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_LEVELVALUE, i)) != 8:
                return False
            str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_LEVELTEXT, i)
            len_ = StringLen(str_)
            if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
                return False
            if len_ != 0:
                if FileWriteString(file_handle, str_, len_) != len_:
                    return False
        else:
            i = _range_end(i, levels, 1)
        return True
    def Load(self, file_handle):
        i = 0
        len_ = 0
        num = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if _missing('FileReadLong')(file_handle) != -1:
            return False
        if FileReadInteger(file_handle, INT_VALUE) != self.Type():
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_NAME, str_):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_COLOR, _missing('FileReadLong')(file_handle)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STYLE, FileReadInteger(file_handle)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_WIDTH, FileReadInteger(file_handle)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BACK, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTABLE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_TIMEFRAMES, FileReadInteger(file_handle, INT_VALUE)):
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_TEXT, str_):
            return False
        num = FileReadInteger(file_handle, INT_VALUE)
        if num != 0:
            i = 0
            for i in range(i, num):
                if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_TIME, i, _missing('FileReadLong')(file_handle)):
                    return False
                if not ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_PRICE, i, FileReadDouble(file_handle)):
                    return False
            else:
                i = _range_end(i, num, 1)
        num = FileReadInteger(file_handle, INT_VALUE)
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELS, 0, num):
            return False
        if num != 0:
            i = 0
            for i in range(i, num):
                if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELCOLOR, i, _missing('FileReadLong')(file_handle)):
                    return False
                if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELSTYLE, i, FileReadInteger(file_handle)):
                    return False
                if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELWIDTH, i, FileReadInteger(file_handle)):
                    return False
                if not ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_LEVELVALUE, i, FileReadDouble(file_handle)):
                    return False
                len_ = FileReadInteger(file_handle, INT_VALUE)
                str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
                if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_LEVELTEXT, i, str_):
                    return False
            else:
                i = _range_end(i, num, 1)
        return True

class CChartObjectText(CChartObject):
    _q_fields = ()
    def __init__(self):
        CChartObject.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, time, price):
        if not ObjectCreate(chart_id, name, OBJ_TEXT, window, time, price):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        return True
    def Type(self):
        return OBJ_TEXT
    def Angle_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_ANGLE)
    def Angle_1(self, angle):
        if self.m_chart_id == -1:
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_ANGLE, angle)
    def Font_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_FONT)
    def Font_1(self, font):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_FONT, font)
    def FontSize_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_FONTSIZE))
    def FontSize_1(self, size):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_FONTSIZE, size)
    def Anchor_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_ANCHOR)
    def Anchor_1(self, anchor):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_ANCHOR, anchor)
    def Save(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Save(self, file_handle):
            return False
        if FileWriteDouble(file_handle, ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_ANGLE)) != 8:
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_FONT)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0 and FileWriteString(file_handle, str_, len_) != len_:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_FONTSIZE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_ANCHOR)), INT_VALUE) != 4:
            return False
        return True
    def Load(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Load(self, file_handle):
            return False
        if not ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_ANGLE, 0, FileReadDouble(file_handle)):
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_FONT, str_):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_FONTSIZE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_ANCHOR, FileReadInteger(file_handle, INT_VALUE)):
            return False
        return True

class CChartObjectLabel(CChartObjectText):
    _q_fields = ()
    def __init__(self):
        CChartObjectText.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, X, Y):
        if not ObjectCreate(chart_id, name, OBJ_LABEL, window, 0, 0.0):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        if not self.Description_1(name):
            return False
        if (not self.X_Distance_1(X)) or (not self.Y_Distance_1(Y)):
            return False
        return True
    def Type(self):
        return OBJ_LABEL
    def X_Distance_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE))
    def X_Distance_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE, X)
    def Y_Distance_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE))
    def Y_Distance_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE, Y)
    def X_Size(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE))
    def Y_Size(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE))
    def Corner_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER)
    def Corner_1(self, corner):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER, corner)
    def Time_1(self, point):
        return CChartObject.Time_1(self, point)
    def Time_2(self, point, time):
        return False
    def Price_1(self, point):
        return CChartObject.Price_1(self, point)
    def Price_2(self, point, price):
        return False
    def Save(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectText.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER)), INT_VALUE) != 4:
            return False
        return True
    def Load(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectText.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER, FileReadInteger(file_handle, INT_VALUE)):
            return False
        return True

class CChartObjectEdit(CChartObjectLabel):
    _q_fields = ()
    def __init__(self):
        CChartObjectLabel.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, X, Y, sizeX, sizeY):
        if not ObjectCreate(chart_id, name, self.Type(), window, 0, 0, 0):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        if (not self.X_Distance_1(X)) or (not self.Y_Distance_1(Y)):
            return False
        if (not self.X_Size_1(sizeX)) or (not self.Y_Size_1(sizeY)):
            return False
        return True
    def Type(self):
        return OBJ_EDIT
    def X_Size_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE, X)
    def X_Size_0(self):
        return CChartObjectLabel.X_Size(self)
    def Y_Size_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE, Y)
    def Y_Size_0(self):
        return CChartObjectLabel.Y_Size(self)
    def BackColor_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR))
    def BackColor_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR, new_color)
    def BorderColor_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_COLOR))
    def BorderColor_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_COLOR, new_color)
    def ReadOnly_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_READONLY))
    def ReadOnly_1(self, flag):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_READONLY, flag)
    def TextAlign_0(self):
        if self.m_chart_id == -1:
            return False
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_ALIGN)
    def TextAlign_1(self, align):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_ALIGN, align)
    def Angle_1(self, angle):
        return False
    def Angle_0(self):
        return CChartObjectText.Angle_0(self)
    def Save(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectLabel.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE)), INT_VALUE) != 4:
            return False
        if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR)) != 8:
            return False
        return True
    def Load(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectLabel.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR, _missing('FileReadLong')(file_handle)):
            return False
        return True

class CChartObjectButton(CChartObjectEdit):
    _q_fields = ()
    def __init__(self):
        CChartObjectEdit.__init__(self)
    def _q_dtor(self):
        pass
    def Type(self):
        return OBJ_BUTTON
    def State_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE))
    def State_1(self, state):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE, state)
    def Save(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectEdit.Save(self, file_handle):
            return False
        if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE)) != 8:
            return False
        return True
    def Load(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectEdit.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE, _missing('FileReadLong')(file_handle)):
            return False
        return True

class CChartObjectRectLabel(CChartObjectLabel):
    _q_fields = ()
    def __init__(self):
        CChartObjectLabel.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, X, Y, sizeX, sizeY):
        if not ObjectCreate(chart_id, name, self.Type(), window, 0, 0, 0):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        if (not self.X_Distance_1(X)) or (not self.Y_Distance_1(Y)):
            return False
        if (not self.X_Size_1(sizeX)) or (not self.Y_Size_1(sizeY)):
            return False
        return True
    def Type(self):
        return OBJ_RECTANGLE_LABEL
    def X_Size_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE, X)
    def X_Size_0(self):
        return CChartObjectLabel.X_Size(self)
    def Y_Size_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE, Y)
    def Y_Size_0(self):
        return CChartObjectLabel.Y_Size(self)
    def BackColor_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR))
    def BackColor_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR, new_color)
    def BorderType_0(self):
        if self.m_chart_id == -1:
            return False
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_TYPE)
    def BorderType_1(self, type_):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_TYPE, type_)
    def Angle_1(self, angle):
        return False
    def Angle_0(self):
        return CChartObjectText.Angle_0(self)
    def Save(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectLabel.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE)), INT_VALUE) != 4:
            return False
        if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR)) != 8:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_TYPE)), INT_VALUE) != 4:
            return False
        return True
    def Load(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectLabel.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR, _missing('FileReadLong')(file_handle)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_TYPE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        return True

class CPanel(CWndObj):
    _q_fields = ('m_rectangle', 'm_border')
    def __init__(self):
        CWndObj.__init__(self)
        self.m_rectangle = CChartObjectRectLabel()
        self.m_border = 0
        self.m_border = BORDER_FLAT
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.m_rectangle.Create(chart, name, subwin, x1, y1, self.Width_0(), self.Height_0()):
            return False
        return self.OnChange()
    def BorderType_0(self):
        return self.m_border
    def BorderType_1(self, type_):
        self.m_border = type_
        return self.m_rectangle.BorderType_1(type_)
    def OnSetText(self):
        return self.m_rectangle.Description_1(self.m_text)
    def OnSetColorBackground(self):
        return self.m_rectangle.BackColor_1(self.m_color_background)
    def OnSetColorBorder(self):
        return self.m_rectangle.Color_1(self.m_color_border)
    def OnCreate(self):
        return self.m_rectangle.Create(self.m_chart_id, self.m_name, self.m_subwin, self.m_rect.left, self.m_rect.top, self.m_rect.Width_0(), self.m_rect.Height_0())
    def OnShow(self):
        return self.m_rectangle.Timeframes_1(_int(OBJ_ALL_PERIODS))
    def OnHide(self):
        return self.m_rectangle.Timeframes_1(_int(OBJ_NO_PERIODS))
    def OnMove(self):
        return self.m_rectangle.X_Distance_1(self.m_rect.left) and self.m_rectangle.Y_Distance_1(self.m_rect.top)
    def OnResize(self):
        return self.m_rectangle.X_Size_1(self.m_rect.Width_0()) and self.m_rectangle.Y_Size_1(self.m_rect.Height_0())
    def OnChange(self):
        return CWndObj.OnChange(self) and self.m_rectangle.BorderType_1(self.m_border)

class CChartObjectBitmap(CChartObject):
    _q_fields = ()
    def __init__(self):
        CChartObject.__init__(self)
    def _q_dtor(self):
        pass
    def BmpFile_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE)
    def BmpFile_1(self, name):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, name)
    def X_Offset_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XOFFSET))
    def X_Offset_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XOFFSET, X)
    def Y_Offset_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YOFFSET))
    def Y_Offset_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YOFFSET, Y)
    def Create(self, chart_id, name, window, time, price):
        if not ObjectCreate(chart_id, name, OBJ_BITMAP, window, time, price):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        return True
    def Type(self):
        return OBJ_BITMAP
    def Save(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Save(self, file_handle):
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0 and FileWriteString(file_handle, str_, len_) != len_:
            return False
        return True
    def Load(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Load(self, file_handle):
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, str_):
            return False
        return True

class CChartObjectBmpLabel(CChartObject):
    _q_fields = ()
    def __init__(self):
        CChartObject.__init__(self)
    def _q_dtor(self):
        pass
    def X_Distance_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE))
    def X_Distance_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE, X)
    def Y_Distance_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE))
    def Y_Distance_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE, Y)
    def X_Size(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE))
    def Y_Size(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE))
    def Corner_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER)
    def Corner_1(self, corner):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER, corner)
    def BmpFileOn_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 0)
    def BmpFileOn_1(self, name):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 0, name)
    def BmpFileOff_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 1)
    def BmpFileOff_1(self, name):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 1, name)
    def State_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE))
    def State_1(self, state):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE, state)
    def X_Offset_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XOFFSET))
    def X_Offset_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XOFFSET, X)
    def Y_Offset_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YOFFSET))
    def Y_Offset_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YOFFSET, Y)
    def Time(self, time):
        return False
    def Price(self, price):
        return False
    def Create(self, chart_id, name, window, X, Y):
        if not ObjectCreate(chart_id, name, OBJ_BITMAP_LABEL, window, 0, 0.0):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        if (not self.X_Distance_1(X)) or (not self.Y_Distance_1(Y)):
            return False
        return True
    def Type(self):
        return OBJ_BITMAP_LABEL
    def Save(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER)), INT_VALUE) != 4:
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 0)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0 and FileWriteString(file_handle, str_, len_) != len_:
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 1)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0 and FileWriteString(file_handle, str_, len_) != len_:
            return False
        if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE)) != 8:
            return False
        return True
    def Load(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER, FileReadInteger(file_handle, INT_VALUE)):
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 0, str_):
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 1, str_):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE, _missing('FileReadLong')(file_handle)):
            return False
        return True

class CBmpButton(CWndObj):
    _q_fields = ('m_button', 'm_border', 'm_bmp_off_name', 'm_bmp_on_name', 'm_bmp_passive_name', 'm_bmp_active_name')
    def __init__(self):
        CWndObj.__init__(self)
        self.m_button = CChartObjectBmpLabel()
        self.m_border = 0
        self.m_bmp_off_name = ""
        self.m_bmp_on_name = ""
        self.m_bmp_passive_name = ""
        self.m_bmp_active_name = ""
        self.m_border = 0
        self.m_bmp_off_name = ""
        self.m_bmp_on_name = ""
        self.m_bmp_passive_name = ""
        self.m_bmp_active_name = ""
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.m_button.Create(chart, name, subwin, x1, y1):
            return False
        return self.OnChange()
    def Border_0(self):
        return self.m_border
    def Border_1(self, value):
        self.m_border = value
        return self.m_button.Width_1(value)
    def BmpNames(self, off='', on=''):
        self.m_bmp_off_name = off
        self.m_bmp_on_name = on
        if not self.m_button.BmpFileOff_1(off):
            return False
        if not self.m_button.BmpFileOn_1(on):
            return False
        return True
    def BmpOffName_0(self):
        return self.m_bmp_off_name
    def BmpOffName_1(self, name):
        self.m_bmp_off_name = name
        if not self.m_button.BmpFileOff_1(name):
            return False
        self.Width_1(self.m_button.X_Size())
        self.Height_1(self.m_button.Y_Size())
        return True
    def BmpOnName_0(self):
        return self.m_bmp_on_name
    def BmpOnName_1(self, name):
        self.m_bmp_on_name = name
        if not self.m_button.BmpFileOn_1(name):
            return False
        self.Width_1(self.m_button.X_Size())
        self.Height_1(self.m_button.Y_Size())
        return True
    def BmpPassiveName_0(self):
        return self.m_bmp_passive_name
    def BmpPassiveName_1(self, name):
        self.m_bmp_passive_name = name
        if not ((self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0):
            return self.BmpOffName_1(name)
        return True
    def BmpActiveName_0(self):
        return self.m_bmp_active_name
    def BmpActiveName_1(self, name):
        self.m_bmp_active_name = name
        if (self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0:
            return self.BmpOffName_1(name)
        return True
    def Pressed_0(self):
        return self.m_button.State_0()
    def Pressed_1(self, pressed):
        return self.m_button.State_1(pressed)
    def Locking_0(self):
        return (self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0
    def Locking_1(self, flag):
        if flag:
            self.PropFlagsSet(WND_PROP_FLAG_CAN_LOCK)
        else:
            self.PropFlagsReset(WND_PROP_FLAG_CAN_LOCK)
    def OnSetZOrder(self):
        return self.m_button.Z_Order_1(self.m_zorder)
    def OnCreate(self):
        return self.m_button.Create(self.m_chart_id, self.m_name, self.m_subwin, self.m_rect.left, self.m_rect.top)
    def OnShow(self):
        return self.m_button.Timeframes_1(_int(OBJ_ALL_PERIODS))
    def OnHide(self):
        return self.m_button.Timeframes_1(_int(OBJ_NO_PERIODS))
    def OnMove(self):
        return self.m_button.X_Distance_1(self.m_rect.left) and self.m_button.Y_Distance_1(self.m_rect.top)
    def OnChange(self):
        return (self.m_button.Width_1(self.m_border) and self.m_button.BmpFileOff_1(self.m_bmp_off_name)) and self.m_button.BmpFileOn_1(self.m_bmp_on_name)
    def OnActivate(self):
        if self.m_bmp_active_name != "":
            self.BmpOffName_1(self.m_bmp_active_name)
        return True
    def OnDeactivate(self):
        if self.m_bmp_passive_name != "":
            self.BmpOffName_1(self.m_bmp_passive_name)
        if not ((self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0):
            self.Pressed_1(False)
        return True
    def OnMouseDown(self):
        if not ((self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0):
            self.Pressed_1(not self.Pressed_0())
        return CWnd.OnMouseDown(self)
    def OnMouseUp(self):
        if self.m_button.State_0() and (not ((self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0)):
            self.m_button.State_1(False)
        return CWnd.OnMouseUp(self)

class CScroll(CWndContainer):
    _q_fields = ('m_back', 'm_inc', 'm_dec', 'm_thumb', 'm_min_pos', 'm_max_pos', 'm_curr_pos')
    def __init__(self):
        CWndContainer.__init__(self)
        self.m_back = CPanel()
        self.m_inc = CBmpButton()
        self.m_dec = CBmpButton()
        self.m_thumb = CBmpButton()
        self.m_min_pos = 0
        self.m_max_pos = 0
        self.m_curr_pos = 0
        self.m_curr_pos = 0
        self.m_min_pos = 0
        self.m_max_pos = 0
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.CreateBack():
            return False
        if not self.CreateInc():
            return False
        if not self.CreateDec():
            return False
        if not self.CreateThumb():
            return False
        return True
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_inc.Id_0():
            self.OnClickInc()
            return True
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_dec.Id_0():
            self.OnClickDec()
            return True
        if id_ == (11 + CHARTEVENT_CUSTOM) and lparam == self.m_thumb.Id_0():
            self.OnThumbDragStart()
            return True
        if (self.m_drag_object is not None and id_ == (12 + CHARTEVENT_CUSTOM)) and lparam == self.m_drag_object.Id_0():
            self.OnThumbDragProcess()
            return True
        if (self.m_drag_object is not None and id_ == (13 + CHARTEVENT_CUSTOM)) and lparam == self.m_drag_object.Id_0():
            self.OnThumbDragEnd()
            return True
        return CWndContainer.OnEvent(self, id_, lparam, dparam, sparam)
    def MinPos_0(self):
        return self.m_min_pos
    def MinPos_1(self, value):
        if self.m_min_pos != value:
            self.m_min_pos = value
            self.CurrPos_1(self.m_curr_pos)
    def MaxPos_0(self):
        return self.m_max_pos
    def MaxPos_1(self, value):
        if self.m_max_pos != value:
            self.m_max_pos = value
            self.CurrPos_1(self.m_curr_pos)
    def CurrPos_0(self):
        return self.m_curr_pos
    def CurrPos_1(self, value):
        if value < self.m_min_pos:
            value = self.m_min_pos
        if value > self.m_max_pos:
            value = self.m_max_pos
        if self.m_curr_pos != value:
            self.m_curr_pos = value
            return self.OnChangePos()
        return False
    def CreateBack(self):
        if not self.m_back.Create(self.m_chart_id, self.m_name + 'Back', self.m_subwin, 0, 0, self.Width_0(), self.Height_0()):
            return False
        if not self.m_back.ColorBackground_1(0xECECEC):
            return False
        if not self.m_back.ColorBorder_1(0xD3D3D3):
            return False
        if not self.Add_1(self.m_back):
            return False
        return True
    def CreateInc(self):
        return True
    def CreateDec(self):
        return True
    def CreateThumb(self):
        return True
    def OnClickInc(self):
        if not self.CurrPos_1(self.m_curr_pos + 1):
            return True
        EventChartCustom(-1, 7, self.m_id, 0.0, self.m_name)
        return True
    def OnClickDec(self):
        if not self.CurrPos_1(self.m_curr_pos - 1):
            return True
        EventChartCustom(-1, 8, self.m_id, 0.0, self.m_name)
        return True
    def OnShow(self):
        if self.m_id == -1:
            return True
        EventChartCustom(-1, 2, self.m_id, 0.0, self.m_name)
        return True
    def OnHide(self):
        if self.m_id == -1:
            return True
        EventChartCustom(-1, 3, self.m_id, 0.0, self.m_name)
        return True
    def OnChangePos(self):
        return True
    def OnThumbDragStart(self):
        return True
    def OnThumbDragProcess(self):
        return True
    def OnThumbDragEnd(self):
        return True
    def CalcPos(self, coord):
        return 0

class CScrollV(CScroll):
    _q_fields = ()
    def __init__(self):
        CScroll.__init__(self)
    def _q_dtor(self):
        pass
    def CreateInc(self):
        x1 = 1
        y1 = self.Height_0() - 18 + 1
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_inc.Create(self.m_chart_id, self.m_name + 'Inc', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_inc.BmpNames('::res\\Down.bmp'):
            return False
        if not self.Add_1(self.m_inc):
            return False
        self.m_inc.PropFlags_1(WND_PROP_FLAG_CLICKS_BY_PRESS)
        return True
    def CreateDec(self):
        x1 = 1
        y1 = 1
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_dec.Create(self.m_chart_id, self.m_name + 'Dec', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_dec.BmpNames('::res\\Up.bmp'):
            return False
        if not self.Add_1(self.m_dec):
            return False
        self.m_dec.PropFlags_1(WND_PROP_FLAG_CLICKS_BY_PRESS)
        return True
    def CreateThumb(self):
        x1 = 1
        y1 = 18 - 1
        x2 = x1 + 16
        y2 = y1 + 22
        if not self.m_thumb.Create(self.m_chart_id, self.m_name + 'Thumb', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_thumb.BmpNames('::res\\ThumbVert.bmp'):
            return False
        if not self.Add_1(self.m_thumb):
            return False
        self.m_thumb.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        return True
    def OnResize(self):
        if self.Width_0() != 18:
            self.m_rect.Width_1(18)
        if not self.m_back.Size_1(self.Size_0()):
            return False
        if not self.m_inc.Move_2(self.m_inc.Left_0(), self.Bottom_0() - 18):
            return False
        return self.OnChangePos()
    def OnChangePos(self):
        if (self.m_max_pos - self.m_min_pos) <= 0:
            return self.Visible(False)
        elif not self.Visible(True):
            return False
        steps = self.m_max_pos - self.m_min_pos
        min_coord = self.m_dec.Bottom_0()
        max_coord = self.m_inc.Top_0() - self.m_thumb.Height_0()
        new_coord = min_coord + _idiv((max_coord - min_coord) * self.m_curr_pos, steps)
        return self.m_thumb.Move_2(self.m_thumb.Left_0(), new_coord)
    def OnThumbDragStart(self):
        if self.m_drag_object is None:
            self.m_drag_object = CDragWnd()
            if self.m_drag_object is None:
                return False
        x1 = self.m_thumb.Left_0() - 50
        y1 = self.m_thumb.Top_0() - 50
        x2 = self.m_thumb.Right_0() + 50
        y2 = self.m_thumb.Bottom_0() + 50
        self.m_drag_object.Create(self.m_chart_id, '', self.m_subwin, x1, y1, x2, y2)
        self.m_drag_object.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        self.m_drag_object.Limits(x1, self.m_dec.Bottom_0() - 50, x2, self.m_inc.Top_0() + 50)
        self.m_drag_object.MouseX_1(self.m_thumb.MouseX_0())
        self.m_drag_object.MouseY_1(self.m_thumb.MouseY_0())
        self.m_drag_object.MouseFlags_1(self.m_thumb.MouseFlags_0())
        return True
    def OnThumbDragProcess(self):
        if self.m_drag_object is None:
            return False
        x = self.m_drag_object.Left_0() + 50
        y = self.m_drag_object.Top_0() + 50
        new_pos = self.CalcPos(y)
        if new_pos != self.m_curr_pos:
            event_id = (7 if (self.m_curr_pos < new_pos) else 8)
            self.m_curr_pos = new_pos
            EventChartCustom(-1, event_id, self.m_id, 0.0, self.m_name)
        self.m_thumb.Move_2(x, y)
        return True
    def OnThumbDragEnd(self):
        if self.m_drag_object is not None:
            self.m_thumb.MouseFlags_1(self.m_drag_object.MouseFlags_0())
            _delete(self.m_drag_object)
            self.m_drag_object = None
        return self.m_thumb.Pressed_1(False)
    def CalcPos(self, coord):
        steps = self.m_max_pos - self.m_min_pos
        min_coord = self.m_dec.Bottom_0()
        max_coord = self.m_inc.Top_0() - self.m_thumb.Height_0()
        if max_coord == min_coord:
            return 0
        if coord < min_coord or coord > max_coord:
            return self.m_curr_pos
        new_pos = _int(MathRound(_fdiv(float(coord - min_coord), max_coord - min_coord) * steps))
        return new_pos

class CScrollH(CScroll):
    _q_fields = ()
    def __init__(self):
        CScroll.__init__(self)
    def _q_dtor(self):
        pass
    def CreateInc(self):
        x1 = self.Width_0() - 18 + 1
        y1 = 1
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_inc.Create(self.m_chart_id, self.m_name + 'Inc', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_inc.BmpNames('::res\\Right.bmp'):
            return False
        if not self.Add_1(self.m_inc):
            return False
        self.m_inc.PropFlags_1(WND_PROP_FLAG_CLICKS_BY_PRESS)
        return True
    def CreateDec(self):
        x1 = 1
        y1 = 1
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_dec.Create(self.m_chart_id, self.m_name + 'Dec', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_dec.BmpNames('::res\\Left.bmp'):
            return False
        if not self.Add_1(self.m_dec):
            return False
        self.m_dec.PropFlags_1(WND_PROP_FLAG_CLICKS_BY_PRESS)
        return True
    def CreateThumb(self):
        x1 = 18 - 1
        y1 = 1
        x2 = x1 + 22
        y2 = y1 + 16
        if not self.m_thumb.Create(self.m_chart_id, self.m_name + 'Thumb', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_thumb.BmpNames('::res\\ThumbHor.bmp'):
            return False
        if not self.Add_1(self.m_thumb):
            return False
        self.m_thumb.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        return True
    def OnResize(self):
        if self.Height_0() != 18:
            self.m_rect.Height_1(18)
        if not self.m_back.Size_1(self.Size_0()):
            return False
        if not self.m_inc.Move_2(self.Right_0() - 18, self.m_inc.Top_0()):
            return False
        return self.OnChangePos()
    def OnChangePos(self):
        if (self.m_max_pos - self.m_min_pos) <= 0:
            return self.Visible(False)
        elif not self.Visible(True):
            return False
        steps = self.m_max_pos - self.m_min_pos
        min_coord = self.m_dec.Right_0()
        max_coord = self.m_inc.Left_0() - self.m_thumb.Width_0()
        new_coord = min_coord + _idiv((max_coord - min_coord) * self.m_curr_pos, steps)
        return self.m_thumb.Move_2(new_coord, self.m_thumb.Top_0())
    def OnThumbDragStart(self):
        if self.m_drag_object is None:
            self.m_drag_object = CDragWnd()
            if self.m_drag_object is None:
                return False
        x1 = self.m_thumb.Left_0() - 50
        y1 = self.m_thumb.Top_0() - 50
        x2 = self.m_thumb.Right_0() + 50
        y2 = self.m_thumb.Bottom_0() + 50
        self.m_drag_object.Create(self.m_chart_id, '', self.m_subwin, x1, y1, x2, y2)
        self.m_drag_object.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        self.m_drag_object.Limits(self.m_dec.Right_0() - 50, y1, self.m_inc.Left_0() + 50, y2)
        self.m_drag_object.MouseX_1(self.m_thumb.MouseX_0())
        self.m_drag_object.MouseY_1(self.m_thumb.MouseY_0())
        self.m_drag_object.MouseFlags_1(self.m_thumb.MouseFlags_0())
        return True
    def OnThumbDragProcess(self):
        if self.m_drag_object is None:
            return False
        x = self.m_drag_object.Left_0() + 50
        y = self.m_drag_object.Top_0() + 50
        new_pos = self.CalcPos(x)
        if new_pos != self.m_curr_pos:
            event_id = (7 if (self.m_curr_pos < new_pos) else 8)
            self.m_curr_pos = new_pos
            EventChartCustom(-1, event_id, self.m_id, 0.0, self.m_name)
        self.m_thumb.Move_2(x, y)
        return True
    def OnThumbDragEnd(self):
        if self.m_drag_object is not None:
            self.m_thumb.MouseFlags_1(self.m_drag_object.MouseFlags_0())
            _delete(self.m_drag_object)
            self.m_drag_object = None
        return self.m_thumb.Pressed_1(False)
    def CalcPos(self, coord):
        steps = self.m_max_pos - self.m_min_pos
        min_coord = self.m_dec.Right_0()
        max_coord = self.m_inc.Left_0() - self.m_thumb.Width_0()
        if max_coord == min_coord:
            return 0
        if coord < min_coord or coord > max_coord:
            return self.m_curr_pos
        new_pos = _int(MathRound(_fdiv(float(coord - min_coord), max_coord - min_coord) * steps))
        return new_pos

class CWndClient(CWndContainer):
    _q_fields = ('m_v_scrolled', 'm_h_scrolled', 'm_background', 'm_scroll_v', 'm_scroll_h')
    def __init__(self):
        CWndContainer.__init__(self)
        self.m_v_scrolled = False
        self.m_h_scrolled = False
        self.m_background = CPanel()
        self.m_scroll_v = CScrollV()
        self.m_scroll_h = CScrollH()
        self.m_v_scrolled = False
        self.m_h_scrolled = False
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.CreateBack():
            return False
        if self.m_v_scrolled and (not self.CreateScrollV()):
            return False
        if self.m_h_scrolled and (not self.CreateScrollH()):
            return False
        return True
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == (2 + CHARTEVENT_CUSTOM) and sparam == self.m_scroll_v.Name():
            self.OnVScrollShow()
            return True
        if id_ == (3 + CHARTEVENT_CUSTOM) and sparam == self.m_scroll_v.Name():
            self.OnVScrollHide()
            return True
        if id_ == (8 + CHARTEVENT_CUSTOM) and lparam == self.m_scroll_v.Id_0():
            self.OnScrollLineUp()
            return True
        if id_ == (7 + CHARTEVENT_CUSTOM) and lparam == self.m_scroll_v.Id_0():
            self.OnScrollLineDown()
            return True
        if id_ == (2 + CHARTEVENT_CUSTOM) and sparam == self.m_scroll_h.Name():
            self.OnHScrollShow()
            return True
        if id_ == (3 + CHARTEVENT_CUSTOM) and sparam == self.m_scroll_h.Name():
            self.OnHScrollHide()
            return True
        if id_ == (8 + CHARTEVENT_CUSTOM) and lparam == self.m_scroll_h.Id_0():
            self.OnScrollLineLeft()
            return True
        if id_ == (7 + CHARTEVENT_CUSTOM) and lparam == self.m_scroll_h.Id_0():
            self.OnScrollLineRight()
            return True
        return CWndContainer.OnEvent(self, id_, lparam, dparam, sparam)
    def ColorBackground(self, value):
        return self.m_background.ColorBackground_1(value)
    def ColorBorder(self, value):
        return self.m_background.ColorBorder_1(value)
    def BorderType(self, flag):
        return self.m_background.BorderType_1(flag)
    def VScrolled_0(self):
        return self.m_v_scrolled
    def VScrolled_1(self, flag):
        if self.m_v_scrolled == flag:
            return True
        d_size = 0
        if flag:
            if not self.CreateScrollV():
                return False
            d_size = -18
        else:
            self.m_scroll_v.Destroy()
            if not self.Delete_1(self.m_scroll_v):
                return False
            d_size = 18
        self.m_v_scrolled = flag
        if self.m_h_scrolled:
            if not self.m_scroll_h.Width_1(self.m_scroll_h.Width_0() + d_size):
                return False
        return True
    def HScrolled_0(self):
        return self.m_h_scrolled
    def HScrolled_1(self, flag):
        if self.m_h_scrolled == flag:
            return True
        d_size = 0
        if flag:
            if not self.CreateScrollH():
                return False
            d_size = -18
        else:
            self.m_scroll_h.Destroy()
            if not self.Delete_1(self.m_scroll_h):
                return False
            d_size = 18
        self.m_h_scrolled = flag
        if self.m_v_scrolled:
            if not self.m_scroll_v.Height_1(self.m_scroll_v.Height_0() + d_size):
                return False
        return True
    def Id_1(self, id_):
        id_used = CWndContainer.Id_1(self, id_)
        if not self.m_v_scrolled:
            id_used += self.m_scroll_v.Id_1(id_ + id_used)
        if not self.m_h_scrolled:
            id_used += self.m_scroll_h.Id_1(id_ + id_used)
        return id_used
    def Id_0(self):
        return CWnd.Id_0(self)
    def Show(self):
        CWndContainer.Show(self)
        if not self.m_v_scrolled:
            self.m_scroll_v.Hide()
        if not self.m_h_scrolled:
            self.m_scroll_h.Hide()
        return True
    def CreateBack(self):
        if not self.m_background.Create(self.m_chart_id, self.m_name + 'Back', self.m_subwin, 0, 0, self.Width_0(), self.Height_0()):
            return False
        if not self.m_background.ColorBorder_1(0x2C2C2C):
            return False
        if not self.m_background.ColorBackground_1(0xDEDEDE):
            return False
        if not self.Add_1(self.m_background):
            return False
        return True
    def CreateScrollV(self):
        x1 = self.Width_0() - 18 - 1
        y1 = 1
        x2 = self.Width_0() - 1
        y2 = self.Height_0() - 1
        if self.m_h_scrolled:
            y2 -= 18
        if not self.m_scroll_v.Create(self.m_chart_id, self.m_name + 'VScroll', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.Add_1(self.m_scroll_v):
            return False
        return True
    def CreateScrollH(self):
        x1 = 1
        y1 = self.Height_0() - 18 - 1
        x2 = self.Width_0() - 1
        y2 = self.Height_0() - 1
        if self.m_v_scrolled:
            x2 -= 18
        if not self.m_scroll_h.Create(self.m_chart_id, self.m_name + 'HScroll', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.Add_1(self.m_scroll_h):
            return False
        return True
    def OnResize(self):
        if not CWndContainer.OnResize(self):
            return False
        d_size = 0
        self.m_background.Width_1(self.Width_0())
        self.m_background.Height_1(self.Height_0())
        if self.m_v_scrolled:
            self.m_scroll_v.Move_2(self.Right_0() - 18, self.Top_0())
            d_size = (18 if self.m_h_scrolled else 0)
            self.m_scroll_v.Height_1(self.Height_0() - d_size)
        if self.m_h_scrolled:
            self.m_scroll_h.Move_2(self.Left_0(), self.Bottom_0() - 18)
            d_size = (18 if self.m_v_scrolled else 0)
            self.m_scroll_h.Width_1(self.Width_0() - d_size)
        return True
    def OnVScrollShow(self):
        return True
    def OnVScrollHide(self):
        return True
    def OnHScrollShow(self):
        return True
    def OnHScrollHide(self):
        return True
    def OnScrollLineDown(self):
        return True
    def OnScrollLineUp(self):
        return True
    def OnScrollLineLeft(self):
        return True
    def OnScrollLineRight(self):
        return True
    def Rebound(self, rect):
        self.m_rect.SetBound_1(rect)
        return self.OnResize()

class CEdit(CWndObj):
    _q_fields = ('m_edit', 'm_read_only', 'm_align_mode')
    def __init__(self):
        CWndObj.__init__(self)
        self.m_edit = CChartObjectEdit()
        self.m_read_only = False
        self.m_align_mode = 0
        self.m_read_only = False
        self.m_align_mode = ALIGN_LEFT
        self.m_color = 0x28293B
        self.m_color_background = clrWhite
        self.m_color_border = 0xCFC3B2
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.m_edit.Create(chart, name, subwin, x1, y1, self.Width_0(), self.Height_0()):
            return False
        return self.OnChange()
    def OnEvent(self, id_, lparam, dparam, sparam):
        if self.m_name == sparam and id_ == CHARTEVENT_OBJECT_ENDEDIT:
            return self.OnObjectEndEdit()
        return CWndObj.OnEvent(self, id_, lparam, dparam, sparam)
    def ReadOnly_0(self):
        return self.m_read_only
    def ReadOnly_1(self, flag):
        self.m_read_only = flag
        return self.m_edit.ReadOnly_1(flag)
    def TextAlign_0(self):
        return self.m_align_mode
    def TextAlign_1(self, align):
        self.m_align_mode = align
        return self.m_edit.TextAlign_1(align)
    def Text_0(self):
        return self.m_edit.Description_0()
    def Text_1(self, value):
        return CWndObj.Text_1(self, value)
    def OnObjectEndEdit(self):
        EventChartCustom(-1, 6, self.m_id, 0.0, self.m_name)
        return True
    def OnSetText(self):
        return self.m_edit.Description_1(self.m_text)
    def OnSetColor(self):
        return self.m_edit.Color_1(self.m_color)
    def OnSetColorBackground(self):
        return self.m_edit.BackColor_1(self.m_color_background)
    def OnSetColorBorder(self):
        return self.m_edit.BorderColor_1(self.m_color_border)
    def OnSetFont(self):
        return self.m_edit.Font_1(self.m_font)
    def OnSetFontSize(self):
        return self.m_edit.FontSize_1(self.m_font_size)
    def OnSetZOrder(self):
        return self.m_edit.Z_Order_1(self.m_zorder)
    def OnCreate(self):
        return self.m_edit.Create(self.m_chart_id, self.m_name, self.m_subwin, self.m_rect.left, self.m_rect.top, self.m_rect.Width_0(), self.m_rect.Height_0())
    def OnShow(self):
        return self.m_edit.Timeframes_1(_int(OBJ_ALL_PERIODS))
    def OnHide(self):
        return self.m_edit.Timeframes_1(_int(OBJ_NO_PERIODS))
    def OnMove(self):
        return self.m_edit.X_Distance_1(self.m_rect.left) and self.m_edit.Y_Distance_1(self.m_rect.top)
    def OnResize(self):
        return self.m_edit.X_Size_1(self.m_rect.Width_0()) and self.m_edit.Y_Size_1(self.m_rect.Height_0())
    def OnChange(self):
        return (CWndObj.OnChange(self) and self.ReadOnly_1(self.m_read_only)) and self.TextAlign_1(self.m_align_mode)
    def OnClick(self):
        if not self.m_read_only:
            EventChartCustom(-1, 5, self.m_id, 0.0, self.m_name)
            return True
        return CWnd.OnClick(self)

class CChart(CObject):
    _q_fields = ('m_chart_id',)
    def __init__(self):
        CObject.__init__(self)
        self.m_chart_id = 0
        self.m_chart_id = -1
    def _q_dtor(self):
        if self.m_chart_id != -1:
            self.Close()
    def ChartId(self):
        return self.m_chart_id
    def Type(self):
        return 0x1111
    def Mode_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ChartGetInteger(self.m_chart_id, CHART_MODE)
    def Mode_1(self, mode):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_MODE, mode)
    def Foreground_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_FOREGROUND))
    def Foreground_1(self, foreground):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_FOREGROUND, foreground)
    def Shift_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHIFT))
    def Shift_1(self, shift):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHIFT, shift)
    def ShiftSize_0(self):
        if self.m_chart_id == -1:
            return DBL_MAX
        return ChartGetDouble(self.m_chart_id, CHART_SHIFT_SIZE)
    def ShiftSize_1(self, shift):
        if self.m_chart_id == -1:
            return False
        if shift < 10:
            shift = 10.0
        if shift > 50:
            shift = 50.0
        return ChartSetDouble(self.m_chart_id, CHART_SHIFT_SIZE, shift)
    def AutoScroll_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_AUTOSCROLL))
    def AutoScroll_1(self, auto_scroll):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_AUTOSCROLL, auto_scroll)
    def Scale_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_SCALE))
    def Scale_1(self, shift):
        if self.m_chart_id == -1:
            return False
        if shift < 0:
            shift = 0
        if shift > 32:
            shift = 32
        return ChartSetInteger(self.m_chart_id, CHART_SCALE, shift)
    def ScaleFix_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX))
    def ScaleFix_1(self, scale_fix):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SCALEFIX, scale_fix)
    def ScaleFix_11_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX_11))
    def ScaleFix_11_1(self, scale_fix_11):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SCALEFIX_11, scale_fix_11)
    def FixedMax_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_FIXED_MAX)
    def FixedMax_1(self, fixed_max):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, CHART_FIXED_MAX, fixed_max)
    def FixedMin_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_FIXED_MIN)
    def FixedMin_1(self, fixed_min):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, CHART_FIXED_MIN, fixed_min)
    def ScalePPB_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR))
    def ScalePPB_1(self, scale_ppb):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR, scale_ppb)
    def PointsPerBar_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_POINTS_PER_BAR)
    def PointsPerBar_1(self, points_per_bar):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, CHART_POINTS_PER_BAR, points_per_bar)
    def ShowOHLC_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_OHLC))
    def ShowOHLC_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_OHLC, show)
    def ShowLineBid_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_BID_LINE))
    def ShowLineBid_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_BID_LINE, show)
    def ShowLineAsk_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE))
    def ShowLineAsk_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE, show)
    def ShowLastLine_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE))
    def ShowLastLine_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE, show)
    def ShowPeriodSep_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP))
    def ShowPeriodSep_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP, show)
    def ShowGrid_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_GRID))
    def ShowGrid_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_GRID, show)
    def ShowVolumes_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ChartGetInteger(self.m_chart_id, CHART_SHOW_VOLUMES)
    def ShowVolumes_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_VOLUMES, show)
    def ShowObjectDescr_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR))
    def ShowObjectDescr_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR, show)
    def ShowDateScale(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_DATE_SCALE, show)
    def ShowPriceScale(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_PRICE_SCALE, show)
    def ColorBackground_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_BACKGROUND))
    def ColorBackground_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_BACKGROUND, new_color)
    def ColorForeground_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_FOREGROUND))
    def ColorForeground_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_FOREGROUND, new_color)
    def ColorGrid_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_GRID))
    def ColorGrid_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_GRID, new_color)
    def ColorBarUp_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CHART_UP))
    def ColorBarUp_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CHART_UP, new_color)
    def ColorBarDown_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CHART_DOWN))
    def ColorBarDown_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CHART_DOWN, new_color)
    def ColorCandleBull_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BULL))
    def ColorCandleBull_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BULL, new_color)
    def ColorCandleBear_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BEAR))
    def ColorCandleBear_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BEAR, new_color)
    def ColorChartLine_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CHART_LINE))
    def ColorChartLine_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CHART_LINE, new_color)
    def ColorVolumes_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_VOLUME))
    def ColorVolumes_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_VOLUME, new_color)
    def ColorLineBid_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_BID))
    def ColorLineBid_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_BID, new_color)
    def ColorLineAsk_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_ASK))
    def ColorLineAsk_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_ASK, new_color)
    def ColorLineLast_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_LAST))
    def ColorLineLast_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_LAST, new_color)
    def ColorStopLevels_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_STOP_LEVEL))
    def ColorStopLevels_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_STOP_LEVEL, new_color)
    def BringToTop(self):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_BRING_TO_TOP, True)
    def EventObjectCreate(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_EVENT_OBJECT_CREATE, flag)
    def EventObjectDelete(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_EVENT_OBJECT_DELETE, flag)
    def EventMouseMove(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_EVENT_MOUSE_MOVE, flag)
    def MouseScroll(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_MOUSE_SCROLL, flag)
    def VisibleBars(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WIDTH_IN_BARS))
    def WindowsTotal(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WINDOWS_TOTAL))
    def WindowIsVisible(self, num):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_WINDOW_IS_VISIBLE, num))
    def WindowHandle(self):
        if self.m_chart_id == -1:
            return INVALID_HANDLE
        return _int(ChartGetInteger(self.m_chart_id, CHART_WINDOW_HANDLE))
    def FirstVisibleBar(self):
        if self.m_chart_id == -1:
            return -1
        return _int(ChartGetInteger(self.m_chart_id, CHART_FIRST_VISIBLE_BAR))
    def WidthInBars(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WIDTH_IN_BARS))
    def WidthInPixels(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WIDTH_IN_PIXELS))
    def HeightInPixels(self, num):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_HEIGHT_IN_PIXELS, num))
    def SubwindowY(self, num):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WINDOW_YDISTANCE, num))
    def PriceMin(self, num):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_PRICE_MIN, num)
    def PriceMax(self, num):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_PRICE_MAX, num)
    def IsObject(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_IS_OBJECT))
    def Attach_0(self):
        self.m_chart_id = ChartID()
    def Attach_1(self, chart):
        self.m_chart_id = chart
    def FirstChart(self):
        self.m_chart_id = ChartFirst()
    def NextChart(self):
        self.m_chart_id = ChartNext(self.m_chart_id)
    def Open(self, symbol_name, timeframe):
        self.m_chart_id = ChartOpen(symbol_name, timeframe)
        if self.m_chart_id == 0:
            self.m_chart_id = -1
        return self.m_chart_id
    def Detach(self):
        self.m_chart_id = -1
    def Close(self):
        if self.m_chart_id != -1:
            ChartClose(self.m_chart_id)
            self.m_chart_id = -1
    def Navigate(self, position, shift=0):
        if self.m_chart_id == -1:
            return False
        return ChartNavigate(self.m_chart_id, position, shift)
    def Symbol(self):
        return ChartSymbol(self.m_chart_id)
    def Period(self):
        return ChartPeriod(self.m_chart_id)
    def Redraw(self):
        ChartRedraw(self.m_chart_id)
    def GetInteger_2(self, prop_id, subwindow=0):
        if self.m_chart_id == -1:
            return 0
        return ChartGetInteger(self.m_chart_id, prop_id, subwindow)
    def GetInteger_3(self, prop_id, subwindow, value):
        if self.m_chart_id == -1:
            return False
        return (ChartGetInteger(self.m_chart_id, prop_id, subwindow, value) != 0)
    def SetInteger(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, prop_id, value)
    def GetDouble_2(self, prop_id, subwindow=0):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, prop_id, subwindow)
    def GetDouble_3(self, prop_id, subwindow, value):
        if self.m_chart_id == -1:
            return False
        return (ChartGetDouble(self.m_chart_id, prop_id, subwindow, value) != 0)
    def SetDouble(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, prop_id, value)
    def GetString_1(self, prop_id):
        if self.m_chart_id == -1:
            return ''
        return ChartGetString(self.m_chart_id, prop_id)
    def GetString_2(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetString(self.m_chart_id, prop_id, value))
    def SetString(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ChartSetString(self.m_chart_id, prop_id, value)
    def SetSymbolPeriod(self, symbol, period):
        if self.m_chart_id == -1:
            return False
        return ChartSetSymbolPeriod(self.m_chart_id, symbol, period)
    def ApplyTemplate(self, filename):
        if self.m_chart_id == -1:
            return False
        return ChartApplyTemplate(self.m_chart_id, filename)
    def ScreenShot(self, filename, width, height, align_mode=ALIGN_RIGHT):
        if self.m_chart_id == -1:
            return False
        return ChartScreenShot(self.m_chart_id, filename, width, height, align_mode)
    def WindowOnDropped(self):
        if self.m_chart_id == -1:
            return 0
        return _missing('ChartWindowOnDropped')()
    def PriceOnDropped(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return _missing('ChartPriceOnDropped')()
    def TimeOnDropped(self):
        if self.m_chart_id == -1:
            return False
        return _long(_missing('ChartTimeOnDropped')())
    def XOnDropped(self):
        if self.m_chart_id == -1:
            return 0
        return _int(_missing('ChartXOnDropped')())
    def YOnDropped(self):
        if self.m_chart_id == -1:
            return 0
        return _int(_missing('ChartYOnDropped')())
    def IndicatorAdd(self, subwin, handle):
        if self.m_chart_id == -1:
            return False
        return ChartIndicatorAdd(self.m_chart_id, subwin, handle)
    def IndicatorDelete(self, subwin, name):
        if self.m_chart_id == -1:
            return False
        return ChartIndicatorDelete(self.m_chart_id, subwin, name)
    def IndicatorsTotal(self, subwin):
        if self.m_chart_id == -1:
            return 0
        return ChartIndicatorsTotal(self.m_chart_id, subwin)
    def IndicatorName(self, subwin, index):
        if self.m_chart_id == -1:
            return ''
        return ChartIndicatorName(self.m_chart_id, subwin, index)
    def Save(self, file_handle):
        work_str = ""
        work_int = 0
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if _missing('FileWriteLong')(file_handle, -1) != 8:
            return False
        if FileWriteInteger(file_handle, self.Type(), INT_VALUE) != INT_VALUE:
            return False
        work_str = self.Symbol()
        work_int = StringLen(work_str)
        if FileWriteInteger(file_handle, work_int, INT_VALUE) != INT_VALUE:
            return False
        if work_int != 0:
            if FileWriteString(file_handle, work_str, work_int) != work_int:
                return False
        if FileWriteInteger(file_handle, self.Period(), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_MODE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_FOREGROUND)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHIFT)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHIFT)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_AUTOSCROLL)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX_11)), CHAR_VALUE) != 1:
            return False
        if FileWriteDouble(file_handle, ChartGetDouble(self.m_chart_id, CHART_FIXED_MAX)) != 8:
            return False
        if FileWriteDouble(file_handle, ChartGetDouble(self.m_chart_id, CHART_FIXED_MIN)) != 8:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR)), CHAR_VALUE) != 1:
            return False
        if FileWriteDouble(file_handle, ChartGetDouble(self.m_chart_id, CHART_POINTS_PER_BAR)) != 8:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_OHLC)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_BID_LINE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_GRID)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_VOLUMES)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR)), CHAR_VALUE) != 1:
            return False
        return True
    def Load(self, file_handle):
        resutl = True
        work_str = ""
        work_int = 0
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if _missing('FileReadLong')(file_handle) != -1:
            return False
        if FileReadInteger(file_handle, INT_VALUE) != self.Type():
            return False
        work_int = FileReadInteger(file_handle)
        if work_int != 0:
            work_str = FileReadString(file_handle, work_int)
        else:
            work_str = ''
        work_int = FileReadInteger(file_handle)
        self.SetSymbolPeriod(work_str, work_int)
        if not ChartSetInteger(self.m_chart_id, CHART_MODE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_FOREGROUND, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHIFT, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHIFT, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_AUTOSCROLL, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALEFIX, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALEFIX_11, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetDouble(self.m_chart_id, CHART_FIXED_MAX, FileReadDatetime(file_handle)):
            return False
        if not ChartSetDouble(self.m_chart_id, CHART_FIXED_MIN, FileReadDatetime(file_handle)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetDouble(self.m_chart_id, CHART_POINTS_PER_BAR, FileReadDatetime(file_handle)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_OHLC, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_BID_LINE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_GRID, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_VOLUMES, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        return resutl

class CDialog(CWndContainer):
    _q_fields = ('m_white_border', 'm_background', 'm_caption', 'm_button_close', 'm_client_area', 'm_panel_flag', 'm_minimized', 'm_min_rect', 'm_norm_rect')
    def __init__(self):
        CWndContainer.__init__(self)
        self.m_white_border = CPanel()
        self.m_background = CPanel()
        self.m_caption = CEdit()
        self.m_button_close = CBmpButton()
        self.m_client_area = CWndClient()
        self.m_panel_flag = False
        self.m_minimized = False
        self.m_min_rect = CRect()
        self.m_norm_rect = CRect()
        self.m_panel_flag = False
        self.m_minimized = False
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if (not self.m_panel_flag) and (not self.CreateWhiteBorder()):
            return False
        if not self.CreateBackground():
            return False
        if not self.CreateCaption():
            return False
        if not self.CreateButtonClose():
            return False
        if not self.CreateClientArea():
            return False
        self.m_norm_rect.SetBound_1(self.m_rect)
        return True
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_button_close.Id_0():
            self.OnClickButtonClose()
            return True
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_caption.Id_0():
            self.OnClickCaption()
            return True
        if id_ == (11 + CHARTEVENT_CUSTOM) and lparam == self.m_caption.Id_0():
            self.OnDialogDragStart()
            return True
        if (self.m_drag_object is not None and id_ == (12 + CHARTEVENT_CUSTOM)) and lparam == self.m_drag_object.Id_0():
            self.OnDialogDragProcess()
            return True
        if (self.m_drag_object is not None and id_ == (13 + CHARTEVENT_CUSTOM)) and lparam == self.m_drag_object.Id_0():
            self.OnDialogDragEnd()
            return True
        return CWndContainer.OnEvent(self, id_, lparam, dparam, sparam)
    def Caption_0(self):
        return self.m_caption.Text_0()
    def Caption_1(self, text):
        return self.m_caption.Text_1(text)
    def Add_1(self, control):
        return self.m_client_area.Add_1(control)
    def Add_2(self, control):
        return self.m_client_area.Add_2(control)
    def Save(self, file_handle):
        if file_handle == INVALID_HANDLE:
            return False
        _missing('FileWriteStruct')(file_handle, self.m_norm_rect)
        FileWriteInteger(file_handle, self.m_min_rect.left)
        FileWriteInteger(file_handle, self.m_min_rect.top)
        FileWriteInteger(file_handle, self.m_minimized)
        return CWndContainer.Save(self, file_handle)
    def Load(self, file_handle):
        if file_handle == INVALID_HANDLE:
            return False
        if not FileIsEnding(file_handle):
            _missing('FileReadStruct')(file_handle, self.m_norm_rect)
            left = FileReadInteger(file_handle)
            top = FileReadInteger(file_handle)
            self.m_min_rect.Move_2(left, top)
            self.m_minimized = (FileReadInteger(file_handle) != 0)
        return CWndContainer.Load(self, file_handle)
    def CreateWhiteBorder(self):
        x1 = 0
        y1 = 0
        x2 = self.Width_0()
        y2 = self.Height_0()
        if not self.m_white_border.Create(self.m_chart_id, self.m_name + 'Border', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_white_border.ColorBackground_1(0xF0F0F0):
            return False
        if not self.m_white_border.ColorBorder_1(clrWhite):
            return False
        if not CWndContainer.Add_1(self, self.m_white_border):
            return False
        self.m_white_border.Alignment(WND_ALIGN_CLIENT, 0, 0, 0, 0)
        return True
    def CreateBackground(self):
        off = (0 if self.m_panel_flag else 1)
        x1 = off
        y1 = off
        x2 = self.Width_0() - off
        y2 = self.Height_0() - off
        if not self.m_background.Create(self.m_chart_id, self.m_name + 'Back', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_background.ColorBackground_1(0xF0F0F0):
            return False
        border = (0xF0F0F0 if self.m_panel_flag else 0xB6B6B6)
        if not self.m_background.ColorBorder_1(border):
            return False
        if not CWndContainer.Add_1(self, self.m_background):
            return False
        self.m_background.Alignment(WND_ALIGN_CLIENT, off, off, off, off)
        return True
    def CreateCaption(self):
        off = (0 if self.m_panel_flag else (2 * 1))
        x1 = off
        y1 = off
        x2 = self.Width_0() - off
        y2 = y1 + 22
        if not self.m_caption.Create(self.m_chart_id, self.m_name + 'Caption', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_caption.Color_1(0x3B2928):
            return False
        if not self.m_caption.ColorBackground_1(0xF0F0F0):
            return False
        if not self.m_caption.ColorBorder_1(0xF0F0F0):
            return False
        if not self.m_caption.ReadOnly_1(True):
            return False
        if not self.m_caption.Text_1(self.m_name):
            return False
        if not CWndContainer.Add_1(self, self.m_caption):
            return False
        self.m_caption.Alignment(WND_ALIGN_WIDTH, off, 0, off, 0)
        if not self.m_panel_flag:
            self.m_caption.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        return True
    def CreateButtonClose(self):
        off = (0 if self.m_panel_flag else (2 * 1))
        x1 = self.Width_0() - off - (16 + 3)
        y1 = off + 3
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_button_close.Create(self.m_chart_id, self.m_name + 'Close', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_button_close.BmpNames('::res\\Close.bmp'):
            return False
        if not CWndContainer.Add_1(self, self.m_button_close):
            return False
        self.m_button_close.Alignment(WND_ALIGN_RIGHT, 0, 0, off + 3, 0)
        self.CaptionAlignment(WND_ALIGN_WIDTH, off, 0, off + (16 + 3), 0)
        return True
    def CreateClientArea(self):
        off = (0 if self.m_panel_flag else (2 * 1))
        x1 = off + 2
        y1 = off + 22
        x2 = self.Width_0() - (off + 2)
        y2 = self.Height_0() - (off + 2)
        if not self.m_client_area.Create(self.m_chart_id, self.m_name + 'Client', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_client_area.ColorBackground(0xF7F7F7):
            return False
        if not self.m_client_area.ColorBorder(0xC8C8C8):
            return False
        CWndContainer.Add_1(self, self.m_client_area)
        self.m_client_area.Alignment(WND_ALIGN_CLIENT, x1, y1, x1, x1)
        return True
    def OnClickCaption(self):
        pass
    def OnClickButtonClose(self):
        self.Visible(False)
    def CaptionAlignment(self, flags, left, top, right, bottom):
        self.m_caption.Alignment(flags, left, top, right, bottom)
    def ClientAreaVisible(self, visible):
        return self.m_client_area.Visible(visible)
    def ClientAreaLeft(self):
        return self.m_client_area.Left_0()
    def ClientAreaTop(self):
        return self.m_client_area.Top_0()
    def ClientAreaRight(self):
        return self.m_client_area.Right_0()
    def ClientAreaBottom(self):
        return self.m_client_area.Bottom_0()
    def ClientAreaWidth(self):
        return self.m_client_area.Width_0()
    def ClientAreaHeight(self):
        return self.m_client_area.Height_0()
    def OnDialogDragStart(self):
        if self.m_drag_object is None:
            self.m_drag_object = CDragWnd()
            if self.m_drag_object is None:
                return False
        x1 = self.Left_0() - 50
        y1 = self.Top_0() - 50
        x2 = self.Right_0() + 50
        y2 = self.Bottom_0() + 50
        self.m_drag_object.Create(self.m_chart_id, '', self.m_subwin, x1, y1, x2, y2)
        self.m_drag_object.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        chart = CChart()
        chart.Attach_1(self.m_chart_id)
        self.m_drag_object.Limits(-50, -50, chart.WidthInPixels() + 50, chart.HeightInPixels(self.m_subwin) + 50)
        chart.Detach()
        self.m_drag_object.MouseX_1(self.m_caption.MouseX_0())
        self.m_drag_object.MouseY_1(self.m_caption.MouseY_0())
        self.m_drag_object.MouseFlags_1(self.m_caption.MouseFlags_0())
        return True
    def OnDialogDragProcess(self):
        if self.m_drag_object is None:
            return False
        x = self.m_drag_object.Left_0() + 50
        y = self.m_drag_object.Top_0() + 50
        self.Move_2(x, y)
        return True
    def OnDialogDragEnd(self):
        if self.m_drag_object is not None:
            self.m_caption.MouseFlags_1(self.m_drag_object.MouseFlags_0())
            _delete(self.m_drag_object)
            self.m_drag_object = None
        if self.m_minimized:
            self.m_min_rect.SetBound_1(self.m_rect)
        else:
            self.m_norm_rect.SetBound_1(self.m_rect)
        return True

class CAppDialog(CDialog):
    _q_fields = ('m_button_minmax', 'm_program_name', 'm_instance_id', 'm_program_type', 'm_indicator_name', 'm_deinit_reason', 'm_subwin_Yoff', 'm_focused_wnd', 'm_top_wnd', 'm_chart')
    _q_ptrs = ('m_focused_wnd', 'm_top_wnd',)
    def __init__(self):
        CDialog.__init__(self)
        self.m_button_minmax = CBmpButton()
        self.m_program_name = ""
        self.m_instance_id = ""
        self.m_program_type = 0
        self.m_indicator_name = ""
        self.m_deinit_reason = 0
        self.m_subwin_Yoff = 0
        self.m_focused_wnd = None
        self.m_top_wnd = None
        self.m_chart = CChart()
        self.m_program_type = WRONG_VALUE
        self.m_deinit_reason = WRONG_VALUE
        self.m_subwin_Yoff = 0
        self.m_focused_wnd = None
        self.m_top_wnd = None
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not self.CreateCommon(chart, name, subwin):
            return False
        _sw1 = self.m_program_type
        if _sw1 == PROGRAM_EXPERT:
            if not self.CreateExpert(x1, y1, x2, y2):
                return False
        elif _sw1 == PROGRAM_INDICATOR:
            if not self.CreateIndicator(x1, y1, x2, y2):
                return False
        else:
            Print('CAppDialog: invalid program type')
            return False
        if not self.Caption_1(self.m_program_name):
            return False
        if not self.CreateButtonMinMax():
            return False
        self.SubwinOff()
        if self.m_minimized:
            self.Minimize()
        else:
            self.Maximize()
        return True
    def Destroy(self, reason=REASON_PROGRAM):
        if self.m_deinit_reason != WRONG_VALUE:
            return
        self.m_deinit_reason = reason
        self.IniFileSave()
        self.m_chart.Detach()
        CWndContainer.Destroy(self)
        if reason == REASON_PROGRAM:
            if self.m_program_type == PROGRAM_EXPERT:
                ExpertRemove()
            if self.m_program_type == PROGRAM_INDICATOR:
                ChartIndicatorDelete(self.m_chart_id, self.m_subwin, self.m_indicator_name)
        EventChartCustom(-1, 100, self.m_subwin, 0.0, self.m_program_name)
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_button_minmax.Id_0():
            self.OnClickButtonMinMax()
            return True
        if id_ == (100 + CHARTEVENT_CUSTOM):
            self.OnAnotherApplicationClose(lparam, dparam, sparam)
            return True
        return CDialog.OnEvent(self, id_, lparam, dparam, sparam)
    def Run(self):
        self.m_chart.Redraw()
        if self.Id_1(self.m_subwin * 10000) > 10000:
            Print('CAppDialog: too many objects')
            return False
        return True
    def ChartEvent(self, id_, lparam, dparam, sparam):
        mouse_x = _int(lparam)
        mouse_y = _int(dparam) - self.m_subwin_Yoff
        _sw2 = id_
        if _sw2 == CHARTEVENT_CHART_CHANGE:
            pass
        elif _sw2 == CHARTEVENT_OBJECT_CLICK:
            return
        elif _sw2 == CHARTEVENT_CUSTOM + 9:
            if CheckPointer(self.m_focused_wnd) != POINTER_INVALID:
                if not self.m_focused_wnd.MouseFocusKill(lparam):
                    return
            self.m_focused_wnd = self.ControlFind(lparam)
            return
        elif _sw2 == CHARTEVENT_CUSTOM + 14:
            self.m_top_wnd = self.ControlFind(lparam)
            return
        elif _sw2 == CHARTEVENT_MOUSE_MOVE:
            if CheckPointer(self.m_top_wnd) != POINTER_INVALID:
                if self.m_top_wnd.OnMouseEvent(mouse_x, mouse_y, _int(StringToInteger(sparam))):
                    self.m_chart.Redraw()
                    return
            if self.OnMouseEvent(mouse_x, mouse_y, _int(StringToInteger(sparam))):
                self.m_chart.Redraw()
            return
        else:
            if self.OnEvent(id_, lparam, dparam, sparam):
                self.m_chart.Redraw()
            return
        if id_ == CHARTEVENT_CHART_CHANGE:
            if self.m_subwin != 0 and self.m_subwin != ChartWindowFind():
                fiction = 1
                self.OnAnotherApplicationClose(fiction, dparam, sparam)
            if self.m_chart.HeightInPixels(self.m_subwin) < (self.Height_0() + 1):
                self.m_button_minmax.Pressed_1(True)
                self.Minimize()
                self.m_chart.Redraw()
            if self.m_chart.WidthInPixels() != self.Width_0() and self.m_subwin != 0:
                self.Width_1(self.m_chart.WidthInPixels())
                self.m_chart.Redraw()
            self.SubwinOff()
    def Minimized(self, flag):
        self.m_minimized = flag
    def IniFileSave(self):
        filename = self.IniFileName() + self.IniFileExt()
        handle = FileOpen(filename, (FILE_WRITE | FILE_BIN) | FILE_ANSI)
        if handle != INVALID_HANDLE:
            self.Save(handle)
            FileClose(handle)
    def IniFileLoad(self):
        filename = self.IniFileName() + self.IniFileExt()
        handle = FileOpen(filename, (FILE_READ | FILE_BIN) | FILE_ANSI)
        if handle != INVALID_HANDLE:
            self.Load(handle)
            FileClose(handle)
    def IniFileName(self):
        name = ""
        name = (self.m_indicator_name if (self.m_indicator_name != "") else self.m_program_name)
        name += '_' + Symbol()
        name += '_Ini'
        return name
    def IniFileExt(self):
        return '.dat'
    def Load(self, file_handle):
        if CDialog.Load(self, file_handle):
            if self.m_minimized:
                self.m_button_minmax.Pressed_1(True)
                self.Minimize()
            else:
                self.m_button_minmax.Pressed_1(False)
                self.Maximize()
            prev_deinit_reason = FileReadInteger(file_handle)
            if prev_deinit_reason == REASON_CHARTCLOSE or prev_deinit_reason == REASON_CLOSE:
                prev_instance_id = IntegerToString(FileReadInteger(file_handle), 5, 48)
                if prev_instance_id != self.m_instance_id:
                    chart_id = self.m_chart.ChartId()
                    total = ObjectsTotal(chart_id, self.m_subwin)
                    for i in range(total - 1, 0 - 1, -1):
                        obj_name = ObjectName(chart_id, i, self.m_subwin)
                        if StringFind(obj_name, prev_instance_id) == 0:
                            ObjectDelete(chart_id, obj_name)
            return True
        return False
    def Save(self, file_handle):
        if CDialog.Save(self, file_handle):
            FileWriteInteger(file_handle, self.m_deinit_reason)
            FileWriteInteger(file_handle, _int(StringToInteger(self.m_instance_id)))
            return True
        return False
    def CreateCommon(self, chart, name, subwin):
        self.m_chart_id = chart
        self.m_name = name
        self.m_subwin = subwin
        self.m_program_name = name
        self.m_deinit_reason = WRONG_VALUE
        self.m_instance_id = self.CreateInstanceId()
        self.m_chart.Attach_1(chart)
        self.m_program_type = MQLInfoInteger(MQL_PROGRAM_TYPE)
        if ((not self.m_chart.EventObjectCreate()) or (not self.m_chart.EventObjectDelete())) or (not self.m_chart.EventMouseMove()):
            Print('CAppDialog: object events specify error')
            self.m_chart.Detach()
            return False
        return True
    def CreateExpert(self, x1, y1, x2, y2):
        self.m_subwin = 0
        self.m_min_rect.SetBound_4(10, 10, 10 + 100, 10 + ((4 * 1) + 22))
        if not CDialog.Create(self, self.m_chart.ChartId(), self.m_instance_id, self.m_subwin, x1, y1, x2, y2):
            Print('CAppDialog: expert dialog create error')
            self.m_chart.Detach()
            return False
        return True
    def CreateIndicator(self, x1, y1, x2, y2):
        width = self.m_chart.WidthInPixels()
        self.m_min_rect.LeftTop_2(0, 0)
        self.m_min_rect.Width_1(width)
        self.m_min_rect.Height_1((4 * 1) + 22 - (2 * 1))
        self.m_subwin = ChartWindowFind()
        if self.m_subwin == -1:
            Print('CAppDialog: find subwindow error')
            self.m_chart.Detach()
            return False
        total = ChartIndicatorsTotal(self.m_chart.ChartId(), self.m_subwin)
        self.m_indicator_name = ChartIndicatorName(self.m_chart.ChartId(), self.m_subwin, total - 1)
        if self.m_subwin == 0:
            return self.CreateExpert(x1, y1, x2, y2)
        if total != 1:
            Print('CAppDialog: subwindow busy')
            ChartIndicatorDelete(self.m_chart.ChartId(), self.m_subwin, ChartIndicatorName(self.m_chart.ChartId(), self.m_subwin, total - 1))
            self.m_chart.Detach()
            return False
        if not IndicatorSetInteger(INDICATOR_HEIGHT, y2 - y1 + 1):
            Print('CAppDialog: subwindow resize error')
            ChartIndicatorDelete(self.m_chart.ChartId(), self.m_subwin, ChartIndicatorName(self.m_chart.ChartId(), self.m_subwin, total - 1))
            self.m_chart.Detach()
            return False
        self.m_indicator_name = self.m_program_name + IntegerToString(self.m_subwin)
        if not IndicatorSetString(INDICATOR_SHORTNAME, self.m_indicator_name):
            Print('CAppDialog: shortname error')
            ChartIndicatorDelete(self.m_chart.ChartId(), self.m_subwin, ChartIndicatorName(self.m_chart.ChartId(), self.m_subwin, total - 1))
            self.m_chart.Detach()
            return False
        self.m_panel_flag = True
        if not CDialog.Create(self, self.m_chart.ChartId(), self.m_instance_id, self.m_subwin, 0, 0, width, y2 - y1):
            Print('CAppDialog: indicator dialog create error')
            ChartIndicatorDelete(self.m_chart.ChartId(), self.m_subwin, ChartIndicatorName(self.m_chart.ChartId(), self.m_subwin, total - 1))
            self.m_chart.Detach()
            return False
        return True
    def CreateButtonMinMax(self):
        off = (0 if self.m_panel_flag else (2 * 1))
        x1 = self.Width_0() - off - (2 * (16 + 3))
        y1 = off + 3
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_button_minmax.Create(self.m_chart_id, self.m_name + 'MinMax', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_button_minmax.BmpNames('::res\\Turn.bmp', '::res\\Restore.bmp'):
            return False
        if not CWndContainer.Add_1(self, self.m_button_minmax):
            return False
        self.m_button_minmax.Locking_1(True)
        self.m_button_minmax.Alignment(WND_ALIGN_RIGHT, 0, 0, off + 16 + (2 * 3), 0)
        self.CaptionAlignment(WND_ALIGN_WIDTH, off, 0, off + (2 * (16 + 3)), 0)
        return True
    def OnClickButtonClose(self):
        self.Destroy()
    def OnClickButtonMinMax(self):
        if self.m_button_minmax.Pressed_0():
            self.Minimize()
        else:
            self.Maximize()
        self.SubwinOff()
    def OnAnotherApplicationClose(self, lparam, dparam, sparam):
        if self.m_subwin == 0:
            return
        if lparam == 0:
            return
        self.SubwinOff()
        if lparam >= self.m_subwin:
            return
        self.m_subwin = ChartWindowFind()
        self.m_indicator_name = self.m_program_name + IntegerToString(self.m_subwin)
        IndicatorSetString(INDICATOR_SHORTNAME, self.m_indicator_name)
        self.Caption_1(self.m_program_name)
        self.Run()
    def Rebound(self, rect):
        if not self.Move_1(rect.LeftTop_0()):
            return False
        if not self.Size_1(rect.Size_0()):
            return False
        if self.m_program_type == PROGRAM_INDICATOR and (not IndicatorSetInteger(INDICATOR_HEIGHT, rect.Height_0() + 1)):
            Print('CAppDialog: subwindow resize error')
            return False
        return True
    def Minimize(self):
        self.m_minimized = True
        self.Rebound(self.m_min_rect)
        self.ClientAreaVisible(False)
    def Maximize(self):
        self.m_minimized = False
        self.Rebound(self.m_norm_rect)
        self.ClientAreaVisible(True)
    def CreateInstanceId(self):
        return IntegerToString(rand(), 5, 48)
    def ProgramName(self):
        return self.m_program_name
    def SubwinOff(self):
        self.m_subwin_Yoff = self.m_chart.SubwindowY(self.m_subwin)

class CCheckBox(CWndContainer):
    _q_fields = ('m_button', 'm_label', 'm_value')
    def __init__(self):
        CWndContainer.__init__(self)
        self.m_button = CBmpButton()
        self.m_label = CEdit()
        self.m_value = 0
        self.m_value = 0
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.CreateButton():
            return False
        if not self.CreateLabel():
            return False
        return True
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_button.Id_0():
            self.OnClickButton()
            return True
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_label.Id_0():
            self.OnClickLabel()
            return True
        return CWndContainer.OnEvent(self, id_, lparam, dparam, sparam)
    def Text_0(self):
        return self.m_label.Text_0()
    def Text_1(self, value):
        return self.m_label.Text_1(value)
    def Color_0(self):
        return self.m_label.Color_0()
    def Color_1(self, value):
        return self.m_label.Color_1(value)
    def Checked_0(self):
        return self.m_button.Pressed_0()
    def Checked_1(self, flag):
        return self.m_button.Pressed_1(flag)
    def Value_0(self):
        return self.m_value
    def Value_1(self, value):
        self.m_value = value
    def Save(self, file_handle):
        if file_handle == INVALID_HANDLE:
            return False
        FileWriteInteger(file_handle, self.Checked_0())
        return True
    def Load(self, file_handle):
        if file_handle == INVALID_HANDLE:
            return False
        if not FileIsEnding(file_handle):
            self.Checked_1((FileReadInteger(file_handle) != 0))
        return True
    def CreateButton(self):
        x1 = 3
        y1 = 3
        x2 = x1 + 16
        y2 = y1 + 16 - 1
        if not self.m_button.Create(self.m_chart_id, self.m_name + 'Button', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_button.BmpNames('::res\\CheckBoxOff.bmp', '::res\\CheckBoxOn.bmp'):
            return False
        if not self.Add_1(self.m_button):
            return False
        self.m_button.Locking_1(True)
        return True
    def CreateLabel(self):
        x1 = 20
        y1 = 0
        x2 = self.Width_0()
        y2 = self.Height_0()
        if not self.m_label.Create(self.m_chart_id, self.m_name + 'Label', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_label.Text_1(self.m_name):
            return False
        if not self.Add_1(self.m_label):
            return False
        self.m_label.ReadOnly_1(True)
        self.m_label.ColorBackground_1(0xF7F7F7)
        self.m_label.ColorBorder_1(0xF7F7F7)
        return True
    def OnClickButton(self):
        EventChartCustom(-1, 4, self.m_id, 0.0, self.m_name)
        return True
    def OnClickLabel(self):
        self.m_button.Pressed_1(not self.m_button.Pressed_0())
        return self.OnClickButton()

class CArrayString(CArray):
    _q_fields = ('m_data',)
    def __init__(self):
        CArray.__init__(self)
        self.m_data = Arr(0, "")
        self.m_data_max = ArraySize(self.m_data)
    def _q_dtor(self):
        if self.m_data_max != 0:
            self.Shutdown()
    def Type(self):
        return TYPE_STRING
    def Save(self, file_handle):
        i = 0
        len_ = 0
        if not CArray.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, self.m_data_total):
            len_ = StringLen(self.m_data[i])
            if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
                return False
            if len_ != 0:
                if FileWriteString(file_handle, self.m_data[i], len_) != len_:
                    break
        else:
            i = _range_end(i, self.m_data_total, 1)
        return i == self.m_data_total
    def Load(self, file_handle):
        i = 0
        num = 0
        len_ = 0
        if not CArray.Load(self, file_handle):
            return False
        num = FileReadInteger(file_handle, INT_VALUE)
        self.Clear()
        if num != 0:
            if not self.Reserve(num):
                return False
            i = 0
            for i in range(i, num):
                len_ = FileReadInteger(file_handle, INT_VALUE)
                if len_ != 0:
                    self.m_data[i] = FileReadString(file_handle, len_)
                else:
                    self.m_data[i] = ''
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
            return ''
        return self.m_data[index]
    def __getitem__(self, index):
        return self.At(index)
    def Update(self, index, element):
        if index < 0 or index >= self.m_data_total:
            return False
        self.m_data[index] = element
        self.m_sort_mode = -1
        return True
    def Shift(self, index, shift):
        tmp_string = ""
        if (index < 0 or (index + shift) < 0) or (index + shift) >= self.m_data_total:
            return False
        if shift == 0:
            return True
        tmp_string = self.m_data[index]
        if shift > 0:
            if self.MemMove(index, index + 1, shift) < 0:
                return False
        else:
            if self.MemMove(index + shift + 1, index + shift, -shift) < 0:
                return False
        self.m_data[index + shift] = tmp_string
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
        p_string = ""
        t_string = ""
        if beg < 0 or end < 0:
            return
        i = beg
        j = end
        while i < end:
            p_string = self.m_data[(beg + end) >> 1]
            while i < j:
                while self.m_data[i] < p_string:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                while self.m_data[j] > p_string:
                    if j == 0:
                        break
                    j -= 1
                if i <= j:
                    t_string = self.m_data[i]
                    self.m_data[((i := i + 1) - 1)] = self.m_data[j]
                    self.m_data[j] = t_string
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
        t_string = ""
        i = 0
        j = self.m_data_total - 1
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m >= self.m_data_total:
                break
            t_string = self.m_data[m]
            if t_string == element:
                break
            if t_string > element:
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

class CArrayLong(CArray):
    _q_fields = ('m_data',)
    def __init__(self):
        CArray.__init__(self)
        self.m_data = Arr(0, 0)
        self.m_data_max = ArraySize(self.m_data)
    def _q_dtor(self):
        if self.m_data_max != 0:
            self.Shutdown()
    def Type(self):
        return TYPE_LONG
    def Save(self, file_handle):
        i = 0
        if not CArray.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, self.m_data_total):
            if _missing('FileWriteLong')(file_handle, self.m_data[i]) != 8:
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
                self.m_data[i] = _long(_missing('FileReadLong')(file_handle))
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
            return LONG_MAX
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
        tmp_long = 0
        if (index < 0 or (index + shift) < 0) or (index + shift) >= self.m_data_total:
            return False
        if shift == 0:
            return True
        tmp_long = self.m_data[index]
        if shift > 0:
            if self.MemMove(index, index + 1, shift) < 0:
                return False
        else:
            if self.MemMove(index + shift + 1, index + shift, -shift) < 0:
                return False
        self.m_data[index + shift] = tmp_long
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
        p_long = 0
        t_long = 0
        if beg < 0 or end < 0:
            return
        i = beg
        j = end
        while i < end:
            p_long = self.m_data[(beg + end) >> 1]
            while i < j:
                while self.m_data[i] < p_long:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                while self.m_data[j] > p_long:
                    if j == 0:
                        break
                    j -= 1
                if i <= j:
                    t_long = self.m_data[i]
                    self.m_data[((i := i + 1) - 1)] = self.m_data[j]
                    self.m_data[j] = t_long
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
        t_long = 0
        i = 0
        j = self.m_data_total - 1
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m >= self.m_data_total:
                break
            t_long = self.m_data[m]
            if t_long == element:
                break
            if t_long > element:
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

class CArrayUChar(CArray):
    _q_fields = ('m_data',)
    def __init__(self):
        CArray.__init__(self)
        self.m_data = Arr(0, 0)
        self.m_data_max = ArraySize(self.m_data)
    def _q_dtor(self):
        if self.m_data_max != 0:
            self.Shutdown()
    def Type(self):
        return TYPE_UCHAR
    def Save(self, file_handle):
        i = 0
        if not CArray.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, self.m_data_total):
            if FileWriteInteger(file_handle, self.m_data[i], CHAR_VALUE) != CHAR_VALUE:
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
                self.m_data[i] = _uchar(FileReadInteger(file_handle, CHAR_VALUE))
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
            return CHAR_MAX
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
        tmp_char = 0
        if (index < 0 or (index + shift) < 0) or (index + shift) >= self.m_data_total:
            return False
        if shift == 0:
            return True
        tmp_char = self.m_data[index]
        if shift > 0:
            if self.MemMove(index, index + 1, shift) < 0:
                return False
        else:
            if self.MemMove(index + shift + 1, index + shift, -shift) < 0:
                return False
        self.m_data[index + shift] = tmp_char
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
        p_char = 0
        t_char = 0
        if beg < 0 or end < 0:
            return
        i = beg
        j = end
        while i < end:
            p_char = self.m_data[(beg + end) >> 1]
            while i < j:
                while self.m_data[i] < p_char:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                while self.m_data[j] > p_char:
                    if j == 0:
                        break
                    j -= 1
                if i <= j:
                    t_char = self.m_data[i]
                    self.m_data[((i := i + 1) - 1)] = self.m_data[j]
                    self.m_data[j] = t_char
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
        t_char = 0
        i = 0
        j = self.m_data_total - 1
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m >= self.m_data_total:
                break
            t_char = self.m_data[m]
            if t_char == element:
                break
            if t_char > element:
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

class CCheckGroup(CWndClient):
    _q_fields = ('m_rows', 'm_offset', 'm_total_view', 'm_item_height', 'm_strings', 'm_values', 'm_states', 'm_value', 'm_current')
    def __init__(self):
        CWndClient.__init__(self)
        self.m_rows = Arr(0, 0, factory=CCheckBox)
        self.m_offset = 0
        self.m_total_view = 0
        self.m_item_height = 0
        self.m_strings = CArrayString()
        self.m_values = CArrayLong()
        self.m_states = CArrayUChar()
        self.m_value = 0
        self.m_current = 0
        self.m_offset = 0
        self.m_total_view = 0
        self.m_item_height = 18
        self.m_current = -1
        self.m_value = 0
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        self.m_total_view = _idiv(y2 - y1, self.m_item_height)
        if self.m_total_view < 1:
            return False
        if not CWndClient.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.m_background.ColorBackground_1(0xF7F7F7):
            return False
        if not self.m_background.ColorBorder_1(0xCFC3B2):
            return False
        ArrayResize(self.m_rows, self.m_total_view)
        i = 0
        while i < self.m_total_view:
            if not self.CreateButton(i):
                return False
            i += 1
        return True
    def Destroy(self, reason=0):
        CWndContainer.Destroy(self, reason)
        self.m_strings.Clear()
        self.m_values.Clear()
        self.m_states.Clear()
    def OnEvent(self, id_, lparam, dparam, sparam):
        total = ArraySize(self.m_rows)
        for i in range(0, total):
            if id_ == (4 + CHARTEVENT_CUSTOM) and lparam == self.m_rows[i].Id_0():
                return self.OnChangeItem(i)
        return CWndClient.OnEvent(self, id_, lparam, dparam, sparam)
    def AddItem(self, item, value=0):
        if not self.m_strings.Add(item):
            return False
        if not self.m_values.Add(value):
            return False
        if not self.m_states.Add(0):
            return False
        total = self.m_strings.Total()
        if total < (self.m_total_view + 1):
            if (self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0 and total != 0:
                self.m_rows[total - 1].Show()
            return self.Redraw()
        if total == (self.m_total_view + 1):
            if not self.VScrolled_1(True):
                return False
            if not ((self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0):
                self.m_scroll_v.Visible(False)
        self.m_scroll_v.MaxPos_1(self.m_strings.Total() - self.m_total_view)
        return self.Redraw()
    def Value_0(self):
        return self.m_value
    def Value_1(self, value):
        self.m_value = value
        return self.Redraw()
    def Check_1(self, idx):
        if idx >= self.m_values.Total():
            return False
        return self.m_states[idx] != 0
    def Check_2(self, idx, value):
        if idx >= self.m_values.Total():
            return False
        state = (0 if (value == 0) else 1)
        res = self.m_states.Update(idx, state) and self.Redraw()
        self.m_value |= value
        return res
    def Show(self):
        if not CWndClient.Show(self):
            return False
        total = self.m_values.Total()
        i = total
        while i < self.m_total_view:
            self.m_rows[i].Hide()
            i += 1
        return True
    def Save(self, file_handle):
        if file_handle == INVALID_HANDLE:
            return False
        _missing('FileWriteLong')(file_handle, self.m_value)
        return True
    def Load(self, file_handle):
        if file_handle == INVALID_HANDLE:
            return False
        if not FileIsEnding(file_handle):
            self.m_value = _long(_missing('FileReadLong')(file_handle))
        return True
    def CreateButton(self, index):
        x1 = 1
        y1 = 1 + (self.m_item_height * index)
        x2 = self.Width_0() - 1
        y2 = y1 + self.m_item_height
        if not self.m_rows[index].Create(self.m_chart_id, self.m_name + 'Item' + IntegerToString(index), self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_rows[index].Text_1(''):
            return False
        if not self.Add_1(self.m_rows[index]):
            return False
        self.m_rows[index].Hide()
        return True
    def OnVScrollShow(self):
        i = 0
        while i < self.m_total_view:
            self.m_rows[i].Width_1(self.Width_0() - (18 + 1))
            i += 1
        if not ((self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0):
            self.m_scroll_v.Visible(False)
            return True
        return True
    def OnVScrollHide(self):
        if not ((self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0):
            return True
        i = 0
        while i < self.m_total_view:
            self.m_rows[i].Width_1(self.Width_0() - 1)
            i += 1
        return True
    def OnScrollLineDown(self):
        self.m_offset = self.m_scroll_v.CurrPos_0()
        return self.Redraw()
    def OnScrollLineUp(self):
        self.m_offset = self.m_scroll_v.CurrPos_0()
        return self.Redraw()
    def OnChangeItem(self, row_index):
        self.m_states.Update(row_index + self.m_offset, self.m_rows[row_index].Checked_0())
        if (row_index + self.m_offset) < 64:
            value = self.m_values.At(row_index + self.m_offset)
            if self.m_rows[row_index].Checked_0():
                self.m_value |= value
            else:
                self.m_value &= ~value
        EventChartCustom(-1, 4, self.m_id, 0.0, self.m_name)
        return True
    def Redraw(self):
        i = 0
        while i < self.m_total_view:
            if not self.m_rows[i].Text_1(_str(self.m_strings[i + self.m_offset])):
                return False
            if not self.RowState(i, self.m_states[i + self.m_offset] != 0):
                return False
            i += 1
        return True
    def RowState(self, index, select):
        if index < 0 or index >= ArraySize(self.m_rows):
            return True
        return self.m_rows[index].Checked_1(select)

class Dimension(MqlObject):
    _q_fields = ('width', 'height')
    def __init__(self, *args):
        self.width = 0
        self.height = 0

class Position(MqlObject):
    _q_fields = ('x', 'y')
    def __init__(self, *args):
        self.x = 0
        self.y = 0

class CPanelDialog(CAppDialog):
    _q_fields = ('m_check_group', 'm_checks_array')
    def __init__(self):
        CAppDialog.__init__(self)
        self.m_check_group = CCheckGroup()
        self.m_checks_array = Arr(20, False, dyn=False)
    def _q_dtor(self):
        self.SaveChecklistState()
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CAppDialog.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.InitializeCheckGroupControls():
            return False
        self.LoadChecklistState()
        return True
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == (4 + CHARTEVENT_CUSTOM) and lparam == self.m_check_group.Id_0():
            self.OnChangeCheckGroup()
            return True
        return CAppDialog.OnEvent(self, id_, lparam, dparam, sparam)
    def OnChangeCheckGroup(self):
        for i in range(0, 20):
            self.m_checks_array[i] = self.m_check_group.Check_1(i)
    def InitializeCheckGroupControls(self):
        x1 = 10
        y1 = 10
        x2 = 320
        y2 = CalculateWindowHeight(CountNonEmptyChecklistItems())
        if not self.m_check_group.Create(self.m_chart_id, TAG + self.m_name + 'CheckGroup', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.Add_1(self.m_check_group):
            return False
        if not self.InitCheckGroupItems():
            return False
        return True
    def InitCheckGroupItems(self):
        checks = Arr(20, "", dyn=False)
        GetChecklistStrings(checks)
        for i in range(0, 20):
            if StringLen(checks[i]) > 0:
                id_ = _int(1 << i)
                if not self.m_check_group.AddItem(checks[i], id_):
                    return False
        return True
    def SaveChecklistState(self):
        path = DataDirectoryName + '//' + Symbol() + DataFileName
        ResetLastError()
        handle = FileOpen(path, (FILE_READ | FILE_WRITE) | FILE_BIN)
        if handle == INVALID_HANDLE:
            Print('Failed to open the file, error: ' + _str(GetLastError()))
        else:
            if not FileWriteArray(handle, self.m_checks_array):
                Print('Failed to write to the file, error: ' + _str(GetLastError()))
            FileClose(handle)
    def LoadChecklistState(self):
        path = DataDirectoryName + '//' + Symbol() + DataFileName
        ResetLastError()
        file_handle = FileOpen(path, FILE_READ | FILE_BIN)
        if file_handle == INVALID_HANDLE:
            Print('File open failed, error: ' + _str(GetLastError()))
        else:
            if not FileReadArray(file_handle, self.m_checks_array):
                Print('Failed to read from the file, error: ' + _str(GetLastError()))
            FileClose(file_handle)
            for i in range(0, 20):
                self.m_check_group.Check_2(i, self.m_checks_array[i])

def OnInit():
    dialogDim = InitDialogDimensions()
    chartDim = GetChartDimensions()
    if not CreateAndRunDialog(dialogDim, chartDim):
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), TAG)
    ExtDialog.Destroy(reason)

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    ExtDialog.ChartEvent(id_, lparam, dparam, sparam)

def InitDialogDimensions():
    dim = _struct_init(Dimension(), [340, CalculateWindowHeight(CountNonEmptyChecklistItems()) + 40])
    return _copy(dim)

def GetChartDimensions():
    dim = _struct_init(Dimension(), [_int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0)), _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, 0))])
    return _copy(dim)

def CreateAndRunDialog(dialogDim, chartDim):
    dialogPos = CalculateDialogPosition(dialogDim, chartDim)
    dialogEndPos = _struct_init(Position(), [dialogPos.x + dialogDim.width, dialogPos.y + dialogDim.height])
    return ExtDialog.Create(0, TAG + '-Strategy Checklist', 0, dialogPos.x, dialogPos.y, dialogEndPos.x, dialogEndPos.y) and ExtDialog.Run()

def CountNonEmptyChecklistItems():
    checks = Arr(20, "", dyn=False)
    GetChecklistStrings(checks)
    count = 0
    for i in range(0, 20):
        if StringLen(checks[i]) > 0:
            count += 1
    return count

def GetChecklistStrings(arr):
    checks = Arr.of([Check01, Check02, Check03, Check04, Check05, Check06, Check07, Check08, Check09, Check10, Check11, Check12, Check13, Check14, Check15, Check16, Check17, Check18, Check19, Check20], fill="", dyn=False, size=20)
    for i in range(0, 20):
        arr[i] = checks[i]

def CalculateWindowHeight(numberOfCheckboxes):
    checkboxHeight = 19
    padding = 3
    topAndBottomMargin = 10
    windowHeight = (numberOfCheckboxes * checkboxHeight) + topAndBottomMargin
    return windowHeight

def CalculateDialogPosition(dialogDim, chartDim):
    margin = 20
    dialogPos = _struct_init(Position(), [margin, margin])
    _sw3 = Location
    if _sw3 == CORNER_RIGHT_UPPER:
        dialogPos.x = chartDim.width - dialogDim.width - margin
    elif _sw3 == CORNER_LEFT_LOWER:
        dialogPos.y = chartDim.height - dialogDim.height - margin
    elif _sw3 == CORNER_RIGHT_LOWER:
        dialogPos.x = chartDim.width - dialogDim.width - margin
        dialogPos.y = chartDim.height - dialogDim.height - margin
    return _copy(dialogPos)

# ---- global variables initialised from expressions
ExtDialog = _alloc(CPanelDialog)
ExtDialog.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FXTTStrategyChecklist(_MQL5Indicator):
    name = 'FXTT_StrategyChecklist'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Location': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=2),  # Window Location
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (0.0, 0.0)

