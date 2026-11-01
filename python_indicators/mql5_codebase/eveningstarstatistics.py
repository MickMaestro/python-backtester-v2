"""EveningStarStatistics — converted from MQL5: MQL5 Indicators/EveningStarStatistics/EveningStarStatistics.mq5

Panel indicator: \\"Evening Star\\" pattern 
search results for different periods
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: FileReadFloat, FileReadLong, FileReadStruct, FileWriteFloat, FileWriteLong, FileWriteStruct, FolderClean, FolderDelete
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh
from backtester.mql5.lib.controls_rect import *  # #include Rect.mqh
from backtester.mql5.lib.graphics_axis import *  # #include Axis.mqh
from backtester.mql5.lib.graphics_colorgenerator import *  # #include ColorGenerator.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Panel indicator: \\"Evening Star\\" pattern ', 'search results for different periods'], 'name': 'EveningStarStatistics', 'source': 'MQL5 Indicators/EveningStarStatistics/EveningStarStatistics.mq5', 'folder': 'EveningStarStatistics', 'inputs': [{'mql': 'InpWidth', 'py': 'InpWidth', 'param': 'InpWidth', 'type': 'ushort', 'default': 900, 'label': 'Width', 'sinput': False}, {'mql': 'InpHeight', 'py': 'InpHeight', 'param': 'InpHeight', 'type': 'ushort', 'default': 400, 'label': 'Height', 'sinput': False}, {'mql': 'InpStartTime', 'py': 'InpStartTime', 'param': None, 'type': 'datetime', 'default': 1668464000, 'label': 'Start time', 'sinput': False}, {'mql': 'InpEndTime', 'py': 'InpEndTime', 'param': None, 'type': 'datetime', 'default': 1700000000, 'label': 'End time', 'sinput': False}, {'mql': 'InpGap', 'py': 'InpGap', 'param': 'InpGap', 'type': 'bool', 'default': True, 'label': 'Gap. true -> gap is taken into account', 'sinput': False}, {'mql': 'InpCandle2Type', 'py': 'InpCandle2Type', 'param': 'InpCandle2Type', 'type': 'bool', 'default': True, 'label': 'Candle 2 type. true -> type of candle 2 is taken into account', 'sinput': False}, {'mql': 'InpCandleSizes', 'py': 'InpCandleSizes', 'param': 'InpCandleSizes', 'type': 'bool', 'default': True, 'label': 'Candle sizes. true -> candle sizes is taken into account', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh', 'Rect.mqh', 'Axis.mqh', 'ColorGenerator.mqh']}

FW_MEDIUM = 0  # MQL5 constant unknown to the converter
INT_VALUE = 0  # MQL5 constant unknown to the converter

# enum ENUM_LINE_END
LINE_END_ROUND = 0
LINE_END_BUTT = 1
LINE_END_SQUARE = 2
_enum('ENUM_LINE_END', {0: 'LINE_END_ROUND', 1: 'LINE_END_BUTT', 2: 'LINE_END_SQUARE'})

# enum ENUM_CURVE_TYPE
CURVE_POINTS = 0
CURVE_LINES = 1
CURVE_POINTS_AND_LINES = 2
CURVE_STEPS = 3
CURVE_HISTOGRAM = 4
CURVE_CUSTOM = 5
CURVE_NONE = 6
_enum('ENUM_CURVE_TYPE', {0: 'CURVE_POINTS', 1: 'CURVE_LINES', 2: 'CURVE_POINTS_AND_LINES', 3: 'CURVE_STEPS', 4: 'CURVE_HISTOGRAM', 5: 'CURVE_CUSTOM', 6: 'CURVE_NONE'})

# enum ENUM_POINT_TYPE
POINT_CIRCLE = 0
POINT_SQUARE = 1
POINT_DIAMOND = 2
POINT_TRIANGLE = 3
POINT_TRIANGLE_DOWN = 4
POINT_X_CROSS = 5
POINT_PLUS = 6
POINT_STAR = 7
POINT_HORIZONTAL_DASH = 8
POINT_VERTICAL_DASH = 9
_enum('ENUM_POINT_TYPE', {0: 'POINT_CIRCLE', 1: 'POINT_SQUARE', 2: 'POINT_DIAMOND', 3: 'POINT_TRIANGLE', 4: 'POINT_TRIANGLE_DOWN', 5: 'POINT_X_CROSS', 6: 'POINT_PLUS', 7: 'POINT_STAR', 8: 'POINT_HORIZONTAL_DASH', 9: 'POINT_VERTICAL_DASH'})

# enum ENUM_MARK_POSITION
MARK_EXTERNAL = 0
MARK_INTERNAL = 1
MARK_MIDDLE = 2
_enum('ENUM_MARK_POSITION', {0: 'MARK_EXTERNAL', 1: 'MARK_INTERNAL', 2: 'MARK_MIDDLE'})

# ---- inputs and global variables
InpWidth = _input('InpWidth', 900)  # Width
InpHeight = _input('InpHeight', 400)  # Height
InpStartTime = _input('InpStartTime', 1700000000 - (365 * 24 * 60 * 60))  # Start time
InpEndTime = _input('InpEndTime', 1700000000)  # End time
InpGap = _input('InpGap', True)  # Gap. true -> gap is taken into account
InpCandle2Type = _input('InpCandle2Type', True)  # Candle 2 type. true -> type of candle 2 is taken into account
InpCandleSizes = _input('InpCandleSizes', True)  # Candle sizes. true -> candle sizes is taken into account
ExtDistance = 0.0  # minimum size of gap
m_adjusted_point = 0.0  # point value adjusted for 3 or 5 points
m_first_start = False

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

class CFile(CObject):
    _q_fields = ('m_handle', 'm_name', 'm_flags')
    def __init__(self):
        CObject.__init__(self)
        self.m_handle = 0
        self.m_name = ""
        self.m_flags = 0
        self.m_handle = INVALID_HANDLE
        self.m_name = ''
        self.m_flags = FILE_ANSI
    def _q_dtor(self):
        if self.m_handle != INVALID_HANDLE:
            self.Close()
    def Handle(self):
        return self.m_handle
    def FileName(self):
        return self.m_name
    def Flags(self):
        return self.m_flags
    def SetUnicode(self, unicode):
        if self.m_handle == INVALID_HANDLE:
            if unicode:
                self.m_flags |= FILE_UNICODE
            else:
                self.m_flags &= ~FILE_UNICODE
    def SetCommon(self, common):
        if self.m_handle == INVALID_HANDLE:
            if common:
                self.m_flags |= FILE_COMMON
            else:
                self.m_flags &= ~FILE_COMMON
    def Open(self, file_name, open_flags, delimiter=9):
        if self.m_handle != INVALID_HANDLE:
            self.Close()
        if (open_flags & (FILE_BIN | FILE_CSV)) == 0:
            open_flags |= FILE_TXT
        self.m_handle = FileOpen(file_name, open_flags | self.m_flags, delimiter)
        if self.m_handle != INVALID_HANDLE:
            self.m_flags |= open_flags
            self.m_name = file_name
        return self.m_handle
    def Close(self):
        if self.m_handle != INVALID_HANDLE:
            FileClose(self.m_handle)
            self.m_handle = INVALID_HANDLE
            self.m_name = ''
            self.m_flags &= FILE_ANSI | FILE_UNICODE
    def Delete_0(self):
        if self.m_handle != INVALID_HANDLE:
            file_name = self.m_name
            common_flag = self.m_flags & FILE_COMMON
            self.Close()
            FileDelete(file_name, common_flag)
    def Delete_2(self, file_name, common_flag=0):
        if file_name == self.m_name:
            flag = self.m_flags & FILE_COMMON
            if flag == common_flag:
                self.Close()
        FileDelete(file_name, common_flag)
    def Size(self):
        if self.m_handle != INVALID_HANDLE:
            return FileSize(self.m_handle)
        return 0
    def Tell(self):
        if self.m_handle != INVALID_HANDLE:
            return FileTell(self.m_handle)
        return 0
    def Seek(self, offset, origin):
        if self.m_handle != INVALID_HANDLE:
            FileSeek(self.m_handle, offset, origin)
    def Flush(self):
        if self.m_handle != INVALID_HANDLE:
            FileFlush(self.m_handle)
    def IsEnding(self):
        if self.m_handle != INVALID_HANDLE:
            return FileIsEnding(self.m_handle)
        return False
    def IsLineEnding(self):
        if self.m_handle != INVALID_HANDLE:
            if (self.m_flags & FILE_BIN) == 0:
                return FileIsLineEnding(self.m_handle)
        return False
    def IsExist(self, file_name, common_flag=0):
        return FileIsExist(file_name, common_flag)
    def Copy(self, src_name, common_flag, dst_name, mode_flags):
        return _bool(FileCopy(src_name, common_flag, dst_name, mode_flags))
    def Move(self, src_name, common_flag, dst_name, mode_flags):
        return _bool(FileMove(src_name, common_flag, dst_name, mode_flags))
    def FolderCreate(self, folder_name):
        return FolderCreate(folder_name, self.m_flags)
    def FolderDelete(self, folder_name):
        return _bool(_missing('FolderDelete')(folder_name, self.m_flags))
    def FolderClean(self, folder_name):
        return _bool(_missing('FolderClean')(folder_name, self.m_flags))
    def FileFindFirst(self, file_filter, returned_filename):
        return FileFindFirst(file_filter, returned_filename.v, self.m_flags)
    def FileFindNext(self, search_handle, returned_filename):
        return FileFindNext(search_handle, returned_filename.v)
    def FileFindClose(self, search_handle):
        FileFindClose(search_handle)

class CFileBin(CFile):
    _q_fields = ()
    def __init__(self):
        CFile.__init__(self)
    def _q_dtor(self):
        pass
    def Open(self, file_name, open_flags):
        return CFile.Open(self, file_name, open_flags | FILE_BIN)
    def WriteChar(self, value):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteInteger(self.m_handle, value, 1)
        return 0
    def WriteShort(self, value):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteInteger(self.m_handle, value, 2)
        return 0
    def WriteInteger(self, value):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteInteger(self.m_handle, value, 4)
        return 0
    def WriteLong(self, value):
        if self.m_handle != INVALID_HANDLE:
            return _uint(_missing('FileWriteLong')(self.m_handle, value))
        return 0
    def WriteFloat(self, value):
        if self.m_handle != INVALID_HANDLE:
            return _uint(_missing('FileWriteFloat')(self.m_handle, value))
        return 0
    def WriteDouble(self, value):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteDouble(self.m_handle, value)
        return 0
    def WriteString_1(self, value):
        if self.m_handle != INVALID_HANDLE:
            size = StringLen(value)
            if FileWriteInteger(self.m_handle, size) == 4:
                return FileWriteString(self.m_handle, value, size)
        return 0
    def WriteString_2(self, value, size):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteString(self.m_handle, value, size)
        return 0
    def WriteCharArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteShortArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteIntegerArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteLongArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteFloatArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteDoubleArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteStruct(self, data):
        if self.m_handle != INVALID_HANDLE:
            return _uint(_missing('FileWriteStruct')(self.m_handle, data.v))
        return 0
    def WriteObject(self, object_):
        if self.m_handle != INVALID_HANDLE:
            if CheckPointer(object_):
                return object_.Save(self.m_handle)
        return False
    def WriteEnum(self, value):
        return self.WriteInteger(_int(value))
    def ReadChar(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = _char(FileReadInteger(self.m_handle, 1))
            return GetLastError() == 0
        return False
    def ReadShort(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = _short(FileReadInteger(self.m_handle, 2))
            return GetLastError() == 0
        return False
    def ReadInteger(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = FileReadInteger(self.m_handle, 4)
            return GetLastError() == 0
        return False
    def ReadLong(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = _long(_missing('FileReadLong')(self.m_handle))
            return GetLastError() == 0
        return False
    def ReadFloat(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = _missing('FileReadFloat')(self.m_handle)
            return GetLastError() == 0
        return False
    def ReadDouble(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = FileReadDouble(self.m_handle)
            return GetLastError() == 0
        return False
    def ReadString_1(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            size = FileReadInteger(self.m_handle)
            if GetLastError() == 0:
                value.v = FileReadString(self.m_handle, size)
                return size == StringLen(value.v)
        return False
    def ReadString_2(self, value, size):
        if self.m_handle != INVALID_HANDLE:
            value.v = FileReadString(self.m_handle, size)
            return size == StringLen(value.v)
        return False
    def ReadCharArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadShortArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadIntegerArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadLongArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadFloatArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadDoubleArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadStruct(self, data):
        if self.m_handle != INVALID_HANDLE:
            return _uint(_missing('FileReadStruct')(self.m_handle, data.v))
        return 0
    def ReadObject(self, object_):
        if self.m_handle != INVALID_HANDLE:
            if CheckPointer(object_):
                return object_.Load(self.m_handle)
        return False
    def ReadEnum(self, value):
        val = Box(0)
        if not self.ReadInteger(val):
            return False
        value.v = val.v
        return True

class CCanvas(MqlObject):
    _q_fields = ('m_style', 'm_style_idx', 'm_chart_id', 'm_objname', 'm_objtype', 'm_rcname', 'm_width', 'm_height', 'm_format', 'm_fontname', 'm_fontsize', 'm_fontflags', 'm_fontangle', 'm_pixels')
    m_default_colors = None
    def __init__(self):
        self.m_style = 0
        self.m_style_idx = 0
        self.m_chart_id = 0
        self.m_objname = ""
        self.m_objtype = 0
        self.m_rcname = ""
        self.m_width = 0
        self.m_height = 0
        self.m_format = 0
        self.m_fontname = ""
        self.m_fontsize = 0
        self.m_fontflags = 0
        self.m_fontangle = 0
        self.m_pixels = Arr(0, 0)
        self.m_chart_id = 0
        self.m_objname = ""
        self.m_objtype = WRONG_VALUE
        self.m_rcname = ""
        self.m_width = 0
        self.m_height = 0
        self.m_format = COLOR_FORMAT_XRGB_NOALPHA
        self.m_fontname = 'arial'
        self.m_fontsize = -120
        self.m_fontflags = 0
        self.m_fontangle = 0
        self.m_style = UINT_MAX
        self.m_style_idx = 0
    def _q_dtor(self):
        pass
    def Create(self, name, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        self.Destroy()
        if (width > 0 and height > 0) and ArrayResize(self.m_pixels, width * height) > 0:
            uniq = _str(ChartID()) + _str(GetTickCount()) + '.' + _str(GetMicrosecondCount() & 0x3FF)
            self.m_rcname = '::' + StringSubstr(name, 0, 63 - StringLen(uniq)) + uniq
            ArrayInitialize(self.m_pixels, 0)
            if ResourceCreate(self.m_rcname, self.m_pixels, width, height, 0, 0, 0, clrfmt):
                self.m_width = width
                self.m_height = height
                self.m_format = clrfmt
                return True
        self.Destroy()
        return False
    def CreateBitmap_6(self, name, time, price, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        return self.CreateBitmap_8(0, 0, name, time, price, width, height, clrfmt)
    def CreateBitmap_8(self, chart_id, subwin, name, time, price, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        if self.Create(name, width, height, clrfmt):
            if ObjectCreate(chart_id, name, OBJ_BITMAP, subwin, time, price):
                if ObjectSetString(chart_id, name, OBJPROP_BMPFILE, self.m_rcname):
                    self.m_chart_id = chart_id
                    self.m_objname = name
                    self.m_objtype = OBJ_BITMAP
                    return True
        return False
    def CreateBitmapLabel_6(self, name, x, y, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        return self.CreateBitmapLabel_8(0, 0, name, x, y, width, height, clrfmt)
    def CreateBitmapLabel_8(self, chart_id, subwin, name, x, y, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        if self.Create(name, width, height, clrfmt):
            if ObjectCreate(chart_id, name, OBJ_BITMAP_LABEL, subwin, 0, 0):
                if (ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x) and ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y)) and ObjectSetString(chart_id, name, OBJPROP_BMPFILE, self.m_rcname):
                    self.m_chart_id = chart_id
                    self.m_objname = name
                    self.m_objtype = OBJ_BITMAP_LABEL
                    return True
        return False
    def Attach_3(self, chart_id, objname, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        if OBJ_BITMAP_LABEL == ObjectGetInteger(chart_id, objname, OBJPROP_TYPE):
            rcname = ObjectGetString(chart_id, objname, OBJPROP_BMPFILE)
            rcname = StringSubstr(rcname, StringFind(rcname, '::'))
            if ResourceReadImage(rcname, self.m_pixels, _uint(self.m_width), _uint(self.m_height)):
                self.m_chart_id = chart_id
                self.m_objname = objname
                self.m_rcname = rcname
                self.m_format = clrfmt
                self.m_objtype = OBJ_BITMAP_LABEL
                return True
        return False
    def Attach_5(self, chart_id, objname, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        if OBJ_BITMAP_LABEL == ObjectGetInteger(chart_id, objname, OBJPROP_TYPE):
            rcname = ObjectGetString(chart_id, objname, OBJPROP_BMPFILE)
            if ((StringLen(rcname) == 0 and width > 0) and height > 0) and ArrayResize(self.m_pixels, width * height) > 0:
                ZeroMemory(self.m_pixels)
                if ResourceCreate('::' + objname, self.m_pixels, width, height, 0, 0, 0, clrfmt) and ObjectSetString(chart_id, objname, OBJPROP_BMPFILE, '::' + objname):
                    self.m_chart_id = chart_id
                    self.m_width = width
                    self.m_height = height
                    self.m_objname = objname
                    self.m_rcname = '::' + objname
                    self.m_format = clrfmt
                    self.m_objtype = OBJ_BITMAP_LABEL
                    return True
        return False
    def Destroy(self):
        if self.m_objname != "":
            ObjectDelete(self.m_chart_id, self.m_objname)
            self.m_chart_id = 0
            self.m_objname = ""
            self.m_objtype = WRONG_VALUE
        ArrayFree(self.m_pixels)
        if self.m_rcname != "":
            ResourceFree(self.m_rcname)
            self.m_rcname = ""
        self.m_width = 0
        self.m_height = 0
    def ChartObjectName(self):
        return self.m_objname
    def ResourceName(self):
        return self.m_rcname
    def Width(self):
        return self.m_width
    def Height(self):
        return self.m_height
    def Update(self, redraw=True):
        if self.m_rcname == "":
            return
        if ResourceCreate(self.m_rcname, self.m_pixels, self.m_width, self.m_height, 0, 0, 0, self.m_format) and redraw:
            ChartRedraw(self.m_chart_id)
    def Resize(self, width, height):
        if (self.m_rcname != "" and width > 0) and height > 0:
            if ArrayResize(self.m_pixels, width * height) > 0:
                self.m_width = width
                self.m_height = height
                ArrayInitialize(self.m_pixels, 0)
                if ResourceCreate(self.m_rcname, self.m_pixels, self.m_width, self.m_height, 0, 0, 0, self.m_format):
                    if self.m_objname != "" and ObjectSetString(self.m_chart_id, self.m_objname, OBJPROP_BMPFILE, self.m_rcname):
                        return True
        return False
    def Erase(self, clr=0):
        ArrayInitialize(self.m_pixels, clr)
    def PixelGet(self, x, y):
        if ((x >= 0 and x < self.m_width) and y >= 0) and y < self.m_height:
            return self.m_pixels[(y * self.m_width) + x]
        return 0
    def PixelSet(self, x, y, clr):
        if ((x >= 0 and x < self.m_width) and y >= 0) and y < self.m_height:
            self.m_pixels[(y * self.m_width) + x] = clr
    def LineVertical(self, x, y1, y2, clr):
        tmp = 0
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        if ((y2 < 0 or y1 >= self.m_height) or x < 0) or x >= self.m_width:
            return
        if y1 < 0:
            y1 = 0
        if y2 >= self.m_height:
            y2 = self.m_height - 1
        index = (y1 * self.m_width) + x
        i = y1
        while i <= y2:
            self.m_pixels[index] = clr
            i += 1
            index += self.m_width
    def LineHorizontal(self, x1, x2, y, clr):
        tmp = 0
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if ((x2 < 0 or x1 >= self.m_width) or y < 0) or y >= self.m_height:
            return
        if x1 < 0:
            x1 = 0
        if x2 >= self.m_width:
            x2 = self.m_width - 1
        ArrayFill(self.m_pixels, (y * self.m_width) + x1, x2 - x1 + 1, clr)
    def Line(self, x1, y1, x2, y2, clr):
        if (x1 < 0 and x2 < 0) or (y1 < 0 and y2 < 0):
            return
        if x1 >= self.m_width and x2 >= self.m_width:
            return
        if y1 >= self.m_height and y2 >= self.m_height:
            return
        dx = ((x2 - x1) if (x2 > x1) else (x1 - x2))
        dy = ((y2 - y1) if (y2 > y1) else (y1 - y2))
        if dx == 0:
            self.LineVertical(x1, y1, y2, clr)
            return
        if dy == 0:
            self.LineHorizontal(x1, x2, y1, clr)
            return
        sx = (1 if (x1 < x2) else -1)
        sy = (1 if (y1 < y2) else -1)
        er = dx - dy
        draw = False
        while x1 != x2 or y1 != y2:
            if ((x1 < 0 or x1 >= self.m_width) or y1 < 0) or y1 >= self.m_height:
                if draw:
                    return
            else:
                self.m_pixels[(y1 * self.m_width) + x1] = clr
                draw = True
            er2 = _int(er << 1)
            if er2 > (-dy):
                er -= dy
                x1 += sx
            if er2 < dx:
                er += dx
                y1 += sy
        self.PixelSet(x2, y2, clr)
    def Polyline(self, x, y, clr):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        total -= 1
        for i in range(0, total):
            self.Line(x[i], y[i], x[i + 1], y[i + 1], clr)
    def Polygon(self, x, y, clr):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        total -= 1
        for i in range(0, total):
            self.Line(x[i], y[i], x[i + 1], y[i + 1], clr)
        self.Line(x[total], y[total], x[0], y[0], clr)
    def Rectangle(self, x1, y1, x2, y2, clr):
        self.LineHorizontal(x1, x2, y1, clr)
        self.LineVertical(x2, y1, y2, clr)
        self.LineHorizontal(x2, x1, y2, clr)
        self.LineVertical(x1, y2, y1, clr)
    def Triangle(self, x1, y1, x2, y2, x3, y3, clr):
        self.Line(x1, y1, x2, y2, clr)
        self.Line(x2, y2, x3, y3, clr)
        self.Line(x3, y3, x1, y1, clr)
    def Circle(self, x, y, r, clr):
        f = 1 - r
        dd_x = 1
        dd_y = -2 * r
        dx = 0
        dy = r
        xx = 0
        yy = 0
        while dy >= dx:
            xx = x + dx
            if xx >= 0 and xx < self.m_width:
                yy = y + dy
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
                yy = y - dy
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
            xx = x - dx
            if xx >= 0 and xx < self.m_width:
                yy = y + dy
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
                yy = y - dy
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
            xx = x + dy
            if xx >= 0 and xx < self.m_width:
                yy = y + dx
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
                yy = y - dx
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
            xx = x - dy
            if xx >= 0 and xx < self.m_width:
                yy = y + dx
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
                yy = y - dx
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
            if f >= 0:
                dy -= 1
                dd_y += 2
                f += dd_y
            dx += 1
            dd_x += 2
            f += dd_x
    def Ellipse(self, x1, y1, x2, y2, clr):
        x = 0
        y = 0
        rx = 0
        ry = 0
        dx = 0
        dy = 0
        xx = 0
        yy = 0
        rx_sq = 0
        ry_sq = 0
        f = 0
        tmp = 0
        if x1 == x2:
            if y1 == y2:
                self.PixelSet(x1, y1, clr)
            else:
                self.LineVertical(x1, y1, y2, clr)
            return
        if y1 == y2:
            self.LineHorizontal(x1, x2, y1, clr)
            return
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        x = (x2 + x1) >> 1
        y = (y2 + y1) >> 1
        rx = (x2 - x1) >> 1
        ry = (y2 - y1) >> 1
        dx = 0
        dy = ry
        rx_sq = rx * rx
        ry_sq = ry * ry
        f = (_int(rx_sq << 1) * ((dy - 1) * dy)) + rx_sq + (_int(ry_sq << 1) * (1 - rx_sq))
        while (rx_sq * dy) > (ry_sq * dx):
            yy = y + dy
            if yy >= 0 and yy < self.m_height:
                yy *= self.m_width
                xx = x + dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
                xx = x - dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
            yy = y - dy
            if yy >= 0 and yy < self.m_height:
                yy *= self.m_width
                xx = x + dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
                xx = x - dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
            if f >= 0:
                dy -= 1
                f -= _int(rx_sq << 2) * dy
            f += _int(ry_sq << 1) * (3 + _int(dx << 1))
            dx += 1
        f = (_int(ry_sq << 1) * (dx + 1) * dx) + (_int(rx_sq << 1) * ((dy * (dy - 2)) + 1)) + ((1 - _int(rx_sq << 1)) * ry_sq)
        while dy >= 0:
            yy = y + dy
            if yy >= 0 and yy < self.m_height:
                yy *= self.m_width
                xx = x + dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
                xx = x - dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
            yy = y - dy
            if yy >= 0 and yy < self.m_height:
                yy *= self.m_width
                xx = x + dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
                xx = x - dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
            if f <= 0:
                dx += 1
                f += _int(ry_sq << 2) * dx
            dy -= 1
            f += _int(rx_sq << 1) * (3 - _int(dy << 1))
    def Arc_9(self, x1, y1, x2, y2, x3, y3, x4, y4, clr):
        tmp = 0
        x = 0
        y = 0
        fi3 = 0.0
        fi4 = 0.0
        if x1 == x2 or y1 == y2:
            return
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        x = (x2 + x1) >> 1
        y = (y2 + y1) >> 1
        if x3 == x and y3 == y:
            return
        if x4 == x and y4 == y:
            return
        fi3 = self.AngleCalc(x, y, x3, y3)
        fi4 = self.AngleCalc(x, y, x4, y4)
        self.Arc_7(x, y, x2 - x, y2 - y, fi3, fi4, clr)
    def Arc_7(self, x, y, rx, ry, fi3, fi4, clr):
        x3 = Box(0)
        y3 = Box(0)
        x4 = Box(0)
        y4 = Box(0)
        if rx < 10 or ry < 10:
            return
        if rx < 0:
            rx = -rx
        if ry < 0:
            ry = -ry
        if fi3 == fi4:
            return
        if fi4 < fi3:
            fi4 += 2 * M_PI
        self.Arc_11(x, y, rx, ry, fi3, fi4, x3, y3, x4, y4, clr)
    def Arc_11(self, x, y, rx, ry, fi3, fi4, x3, y3, x4, y4, clr):
        if rx < 10 or ry < 10:
            return
        dx = 0
        dy = 0
        xx = 0
        yy = 0
        rx_sq = 0
        ry_sq = 0
        f = 0
        fi = 0.0
        ray3 = False
        ray4 = False
        ckw = False
        xx_c = 0
        yy_c = 0
        fi_c = 0.0
        ackw = False
        xx_a = 0
        yy_a = 0
        fi_a = 0.0
        rx_sq = rx * rx
        ry_sq = ry * ry
        fi = MathMod(fi4, 2 * M_PI)
        if ((fi3 < M_PI and fi3 > 0) or (fi < M_PI and fi > 0)) or (fi4 - fi3) >= M_PI:
            dx = 0
            dy = ry
            f = (_int(rx_sq << 1) * ((dy - 1) * dy)) + rx_sq + (_int(ry_sq << 1) * (1 - rx_sq))
            while (rx_sq * dy) >= (ry_sq * dx):
                yy = y - dy
                if dx == 0:
                    fi = self.AngleCalc(0, 0, 0, -dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(x, yy, clr)
                        ackw = True
                        ckw = ackw
                    else:
                        ackw = False
                        ckw = ackw
                    xx_c = x
                    yy_c = yy
                    fi_c = fi
                    xx_a = x
                    yy_a = yy
                    fi_a = fi
                else:
                    xx = x + dx
                    fi = self.AngleCalc(0, 0, dx, -dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ckw:
                            ckw = True
                            if not ray4:
                                if MathAbs(fi_c - MathMod(fi4, 2 * M_PI)) < MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                    self.PixelSet(_box_set(x4, xx_c), _box_set(y4, yy_c), clr)
                                else:
                                    x4.v = xx
                                    y4.v = yy
                                ray4 = True
                    else:
                        if ckw and (not ray3):
                            if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                                self.PixelSet(_box_set(x3, xx), _box_set(y3, yy), clr)
                            else:
                                x3.v = xx_c
                                y3.v = yy_c
                            ray3 = True
                        ckw = False
                    xx_c = xx
                    yy_c = yy
                    fi_c = fi
                    xx = x - dx
                    fi = self.AngleCalc(0, 0, -dx, -dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ackw:
                            ackw = True
                            if not ray3:
                                if MathAbs(fi_a - fi3) < MathAbs(fi - fi3):
                                    self.PixelSet(_box_set(x3, xx_a), _box_set(y3, yy_a), clr)
                                else:
                                    x3.v = xx
                                    y3.v = yy
                                ray3 = True
                    else:
                        if ackw and (not ray4):
                            if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                self.PixelSet(_box_set(x4, xx), _box_set(y4, yy), clr)
                            else:
                                x4.v = xx_a
                                y4.v = yy_a
                            ray4 = True
                        ackw = False
                    xx_a = xx
                    yy_a = yy
                    fi_a = fi
                if f >= 0:
                    dy -= 1
                    f -= _int(rx_sq << 2) * dy
                f += _int(ry_sq << 1) * (3 + _int(dx << 1))
                dx += 1
            if ckw and (not ray3):
                fi = self.AngleCalc(0, 0, dx, -dy)
                if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                    self.PixelSet(_box_set(x3, x + dx), _box_set(y3, y - dy), clr)
                else:
                    x3.v = xx_c
                    y3.v = yy_c
            if ackw and (not ray4):
                fi = self.AngleCalc(0, 0, -dx, -dy)
                if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                    self.PixelSet(_box_set(x4, x - dx), _box_set(y4, y - dy), clr)
                else:
                    x4.v = xx_a
                    y4.v = yy_a
        fi = MathMod(fi4, 2 * M_PI)
        if ((fi3 > M_PI_2 and fi3 < (3 * M_PI_2)) or (fi > M_PI_2 and fi < (3 * M_PI_2))) or (fi4 - fi3) >= M_PI:
            dx = rx
            dy = 0
            f = (_int(ry_sq << 1) * ((dx - 1) * dx)) + ry_sq + (_int(rx_sq << 1) * (1 - ry_sq))
            while (ry_sq * dx) >= (rx_sq * dy):
                xx = x - dx
                if dy == 0:
                    fi = self.AngleCalc(0, 0, -dx, 0)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, y, clr)
                        ackw = True
                        ckw = ackw
                    else:
                        ackw = False
                        ckw = ackw
                    xx_c = xx
                    yy_c = y
                    fi_c = fi
                    xx_a = xx
                    yy_a = y
                    fi_a = fi
                else:
                    yy = y - dy
                    fi = self.AngleCalc(0, 0, -dx, -dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ckw:
                            ckw = True
                            if not ray4:
                                if MathAbs(fi_c - MathMod(fi4, 2 * M_PI)) < MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                    self.PixelSet(_box_set(x4, xx_c), _box_set(y4, yy_c), clr)
                                else:
                                    x4.v = xx
                                    y4.v = yy
                                ray4 = True
                    else:
                        if ckw and (not ray3):
                            if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                                self.PixelSet(_box_set(x3, xx), _box_set(y3, yy), clr)
                            else:
                                x3.v = xx_c
                                y3.v = yy_c
                            ray3 = True
                        ckw = False
                    xx_c = xx
                    yy_c = yy
                    fi_c = fi
                    yy = y + dy
                    fi = self.AngleCalc(0, 0, -dx, dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ackw:
                            ackw = True
                            if not ray3:
                                if MathAbs(fi_a - fi3) < MathAbs(fi - fi3):
                                    self.PixelSet(_box_set(x3, xx_a), _box_set(y3, yy_a), clr)
                                else:
                                    x3.v = xx
                                    y3.v = yy
                                ray3 = True
                    else:
                        if ackw and (not ray4):
                            if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                self.PixelSet(_box_set(x4, xx), _box_set(y4, yy), clr)
                            else:
                                x4.v = xx_a
                                y4.v = yy_a
                            ray4 = True
                        ackw = False
                    xx_a = xx
                    yy_a = yy
                    fi_a = fi
                if f >= 0:
                    dx -= 1
                    f -= _int(ry_sq << 2) * dx
                f += _int(rx_sq << 1) * (3 + _int(dy << 1))
                dy += 1
            if ckw and (not ray3):
                fi = self.AngleCalc(0, 0, -dx, -dy)
                if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                    self.PixelSet(_box_set(x3, x - dx), _box_set(y3, y - dy), clr)
                else:
                    x3.v = xx_c
                    y3.v = yy_c
            if ackw and (not ray4):
                fi = self.AngleCalc(0, 0, -dx, dy)
                if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                    self.PixelSet(_box_set(x4, x - dx), _box_set(y4, y + dy), clr)
                else:
                    x4.v = xx_a
                    y4.v = yy_a
        fi = MathMod(fi4, 2 * M_PI)
        if ((fi3 > M_PI and fi3 < (2 * M_PI)) or (fi > M_PI and fi < (2 * M_PI))) or (fi4 - fi3) >= M_PI:
            dx = 0
            dy = ry
            f = (_int(rx_sq << 1) * ((dy - 1) * dy)) + rx_sq + (_int(ry_sq << 1) * (1 - rx_sq))
            while (rx_sq * dy) >= (ry_sq * dx):
                yy = y + dy
                if dx == 0:
                    fi = self.AngleCalc(0, 0, 0, dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(x, yy, clr)
                        ackw = True
                        ckw = ackw
                    else:
                        ackw = False
                        ckw = ackw
                    xx_c = x
                    yy_c = yy
                    fi_c = fi
                    xx_a = x
                    yy_a = yy
                    fi_a = fi
                else:
                    xx = x - dx
                    fi = self.AngleCalc(0, 0, -dx, dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ckw:
                            ckw = True
                            if not ray4:
                                if MathAbs(fi_c - MathMod(fi4, 2 * M_PI)) < MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                    self.PixelSet(_box_set(x4, xx_c), _box_set(y4, yy_c), clr)
                                else:
                                    x4.v = xx
                                    y4.v = yy
                                ray4 = True
                    else:
                        if ckw and (not ray3):
                            if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                                self.PixelSet(_box_set(x3, xx), _box_set(y3, yy), clr)
                            else:
                                x3.v = xx_c
                                y3.v = yy_c
                            ray3 = True
                        ckw = False
                    xx_c = xx
                    yy_c = yy
                    fi_c = fi
                    xx = x + dx
                    fi = self.AngleCalc(0, 0, dx, dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ackw:
                            ackw = True
                            if not ray3:
                                if MathAbs(fi_a - fi3) < MathAbs(fi - fi3):
                                    self.PixelSet(_box_set(x3, xx_a), _box_set(y3, yy_a), clr)
                                else:
                                    x3.v = xx
                                    y3.v = yy
                                ray3 = True
                    else:
                        if ackw and (not ray4):
                            if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                self.PixelSet(_box_set(x4, xx), _box_set(y4, yy), clr)
                            else:
                                x4.v = xx_a
                                y4.v = yy_a
                            ray4 = True
                        ackw = False
                    xx_a = xx
                    yy_a = yy
                    fi_a = fi
                if f >= 0:
                    dy -= 1
                    f -= _int(rx_sq << 2) * dy
                f += _int(ry_sq << 1) * (3 + _int(dx << 1))
                dx += 1
            if ckw and (not ray3):
                fi = self.AngleCalc(0, 0, -dx, dy)
                if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                    self.PixelSet(_box_set(x3, x - dx), _box_set(y3, y + dy), clr)
                else:
                    x3.v = xx_c
                    y3.v = yy_c
            if ackw and (not ray4):
                fi = self.AngleCalc(0, 0, dx, dy)
                if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                    self.PixelSet(_box_set(x4, x + dx), _box_set(y4, y + dy), clr)
                else:
                    x4.v = xx_a
                    y4.v = yy_a
        fi = MathMod(fi4, 2 * M_PI)
        if ((fi3 < M_PI_2 or fi3 > (3 * M_PI_2)) or (fi < M_PI_2 or fi > (3 * M_PI_2))) or (fi4 - fi3) >= M_PI:
            dx = rx
            dy = 0
            f = (_int(ry_sq << 1) * ((dx - 1) * dx)) + ry_sq + (_int(rx_sq << 1) * (1 - ry_sq))
            while (ry_sq * dx) >= (rx_sq * dy):
                xx = x + dx
                if dy == 0:
                    fi = self.AngleCalc(0, 0, dx, 0)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, y, clr)
                        ackw = True
                        ckw = ackw
                    else:
                        ackw = False
                        ckw = ackw
                    xx_c = xx
                    yy_c = y
                    fi_c = fi
                    xx_a = xx
                    yy_a = y
                    fi_a = fi
                else:
                    yy = y + dy
                    fi = self.AngleCalc(0, 0, dx, dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ckw:
                            ckw = True
                            if not ray4:
                                if MathAbs(fi_c - MathMod(fi4, 2 * M_PI)) < MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                    self.PixelSet(_box_set(x4, xx_c), _box_set(y4, yy_c), clr)
                                else:
                                    x4.v = xx
                                    y4.v = yy
                                ray4 = True
                    else:
                        if ckw and (not ray3):
                            if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                                self.PixelSet(_box_set(x3, xx), _box_set(y3, yy), clr)
                            else:
                                x3.v = xx_c
                                y3.v = yy_c
                            ray3 = True
                        ckw = False
                    xx_c = xx
                    yy_c = yy
                    fi_c = fi
                    yy = y - dy
                    fi = self.AngleCalc(0, 0, dx, -dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ackw:
                            ackw = True
                            if not ray3:
                                if MathAbs(MathMod(fi_a, 2 * M_PI) - fi3) < MathAbs(fi - fi3):
                                    self.PixelSet(_box_set(x3, xx_a), _box_set(y3, yy_a), clr)
                                else:
                                    x3.v = xx
                                    y3.v = yy
                                ray3 = True
                    else:
                        if ackw and (not ray4):
                            if MathAbs(MathMod(fi_a, 2 * M_PI) - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                self.PixelSet(_box_set(x4, xx), _box_set(y4, yy), clr)
                            else:
                                x4.v = xx_a
                                y4.v = yy_a
                            ray4 = True
                        ackw = False
                    xx_a = xx
                    yy_a = yy
                    fi_a = fi
                if f >= 0:
                    dx -= 1
                    f -= _int(ry_sq << 2) * dx
                f += _int(rx_sq << 1) * (3 + _int(dy << 1))
                dy += 1
            if ckw and (not ray3):
                fi = self.AngleCalc(0, 0, dx, dy)
                if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                    self.PixelSet(_box_set(x3, x + dx), _box_set(y3, y + dy), clr)
                else:
                    x3.v = xx_c
                    y3.v = yy_c
            if ackw and (not ray4):
                fi = self.AngleCalc(0, 0, dx, -dy)
                if MathAbs(MathMod(fi_a, 2 * M_PI) - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                    self.PixelSet(_box_set(x4, x + dx), _box_set(y4, y - dy), clr)
                else:
                    x4.v = xx_a
                    y4.v = yy_a
    def Pie_10(self, x1, y1, x2, y2, x3, y3, x4, y4, clr, fill_clr):
        tmp = 0
        x = 0
        y = 0
        fi3 = 0.0
        fi4 = 0.0
        if x1 == x2 or y1 == y2:
            return
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        x = (x2 + x1) >> 1
        y = (y2 + y1) >> 1
        if x3 == x and y3 == y:
            return
        if x4 == x and y4 == y:
            return
        fi3 = self.AngleCalc(x, y, x3, y3)
        fi4 = self.AngleCalc(x, y, x4, y4)
        self.Pie_8(x, y, x2 - x, y2 - y, fi3, fi4, clr, fill_clr)
    def Pie_8(self, x, y, rx, ry, fi3, fi4, clr, fill_clr):
        x3 = Box(x)
        y3 = Box(y)
        x4 = Box(x)
        y4 = Box(y)
        if rx == 0 or ry == 0:
            return
        if rx < 0:
            rx = -rx
        if ry < 0:
            ry = -ry
        if fi3 == fi4:
            return
        if fi4 < fi3:
            fi4 += 2 * M_PI
        self.Arc_11(x, y, rx, ry, fi3, fi4, x3, y3, x4, y4, clr)
        if (x == x3.v and y == y3.v) or (x == x4.v and y == y4.v):
            return
        self.Line(x, y, x3.v, y3.v, clr)
        self.Line(x, y, x4.v, y4.v, clr)
        if rx > ry:
            rx = ry
        fi = (fi3 + fi4) / 2
        xf = x + _int(0.9 * rx * cos(fi))
        yf = y - _int(0.9 * rx * sin(fi))
        self.Fill_3(xf, yf, fill_clr)
    def FillRectangle(self, x1, y1, x2, y2, clr):
        tmp = 0
        if x2 < x1:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y2 < y1:
            tmp = y1
            y1 = y2
            y2 = tmp
        if ((x2 < 0 or y2 < 0) or x1 >= self.m_width) or y1 >= self.m_height:
            return
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x2 >= self.m_width:
            x2 = self.m_width - 1
        if y2 >= self.m_height:
            y2 = self.m_height - 1
        len_ = x2 - x1 + 1
        while y1 <= y2:
            ArrayFill(self.m_pixels, (y1 * self.m_width) + x1, len_, clr)
            y1 += 1
    def FillTriangle(self, x1, y1, x2, y2, x3, y3, clr):
        xx1 = 0
        xx2 = 0
        tmp = 0
        k1 = 0.0
        k2 = 0.0
        xd1 = 0.0
        xd2 = 0.0
        if y1 > y2:
            tmp = y2
            y2 = y1
            y1 = tmp
            tmp = x2
            x2 = x1
            x1 = tmp
        if y1 > y3:
            tmp = y1
            y1 = y3
            y3 = tmp
            tmp = x1
            x1 = x3
            x3 = tmp
        if y2 > y3:
            tmp = y2
            y2 = y3
            y3 = tmp
            tmp = x2
            x2 = x3
            x3 = tmp
        if y3 < 0 or y1 > self.m_height:
            return
        if (x1 < 0 and x2 < 0) and x3 < 0:
            return
        if (x1 > self.m_width and x2 > self.m_width) and x3 > self.m_width:
            return
        if (tmp := y1 - y2) != 0:
            k1 = _fdiv(x1 - x2, float(tmp))
        if (tmp := y1 - y3) != 0:
            k2 = _fdiv(x1 - x3, float(tmp))
        xd1 = x1
        xd2 = x1
        for i in range(y1, y3 + 1):
            if i == y2:
                if (tmp := y2 - y3) != 0:
                    k1 = _fdiv(x2 - x3, float(tmp))
                xd1 = x2
            xx1 = _int(xd1)
            xd1 += k1
            xx2 = _int(xd2)
            xd2 += k2
            if i < 0 or i >= self.m_height:
                continue
            if xx1 > xx2:
                tmp = xx1
                xx1 = xx2
                xx2 = tmp
            if xx2 < 0 or xx1 >= self.m_width:
                continue
            if xx1 < 0:
                xx1 = 0
            if xx2 >= self.m_width:
                xx2 = self.m_width - 1
            ArrayFill(self.m_pixels, (i * self.m_width) + xx1, xx2 - xx1, clr)
    def FillPolygon(self, x, y, clr):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 3:
            return
        ArrayResize(_s_CCanvas_FillPolygon_p, total)
        imin = 0
        xmin = x[0]
        ymin = y[0]
        for i in range(1, total):
            if y[i] > ymin:
                continue
            if y[i] == ymin:
                if x[i] < xmin:
                    xmin = x[i]
                    imin = i
                continue
            xmin = x[i]
            ymin = y[i]
            imin = i
        i = 0
        while i < total:
            _s_CCanvas_FillPolygon_p[i].x = x[_imod(imin, total)]
            _s_CCanvas_FillPolygon_p[i].y = y[_imod(imin, total)]
            i += 1
            imin += 1
        self.PolygonFill(_s_CCanvas_FillPolygon_p, clr)
        ArrayFree(_s_CCanvas_FillPolygon_p)
    def FillCircle(self, x, y, r, clr):
        f = 1 - r
        dd_x = 1
        dd_y = -2 * r
        dx = 0
        dy = r
        while dy >= dx:
            self.LineHorizontal(x - dy, x + dy, y - dx, clr)
            self.LineHorizontal(x - dy, x + dy, y + dx, clr)
            if f >= 0:
                self.LineHorizontal(x - dx, x + dx, y - dy, clr)
                self.LineHorizontal(x - dx, x + dx, y + dy, clr)
                dy -= 1
                dd_y += 2
                f += dd_y
            dx += 1
            dd_x += 2
            f += dd_x
    def FillEllipse(self, x1, y1, x2, y2, clr):
        x = 0
        y = 0
        rx = 0
        ry = 0
        dx = 0
        dy = 0
        rx_sq = 0
        ry_sq = 0
        f = 0
        tmp = 0
        if x1 == x2:
            if y1 == y2:
                self.PixelSet(x1, y1, clr)
            else:
                self.LineVertical(x1, y1, y2, clr)
            return
        if y1 == y2:
            self.LineHorizontal(x1, x2, y1, clr)
            return
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        x = (x2 + x1) >> 1
        y = (y2 + y1) >> 1
        rx = (x2 - x1) >> 1
        ry = (y2 - y1) >> 1
        dx = 0
        dy = ry
        rx_sq = rx * rx
        ry_sq = ry * ry
        f = (_int(rx_sq << 1) * ((dy - 1) * dy)) + rx_sq + (_int(ry_sq << 1) * (1 - rx_sq))
        while (rx_sq * dy) > (ry_sq * dx):
            self.LineHorizontal(x - dx, x + dx, y + dy, clr)
            self.LineHorizontal(x - dx, x + dx, y - dy, clr)
            if f >= 0:
                dy -= 1
                f -= _int(rx_sq << 2) * dy
            f += _int(ry_sq << 1) * (3 + _int(dx << 1))
            dx += 1
        f = (_int(ry_sq << 1) * (dx + 1) * dx) + (_int(rx_sq << 1) * ((dy * (dy - 2)) + 1)) + ((1 - _int(rx_sq << 1)) * ry_sq)
        while dy >= 0:
            self.LineHorizontal(x - dx, x + dx, y + dy, clr)
            self.LineHorizontal(x - dx, x + dx, y - dy, clr)
            if f <= 0:
                dx += 1
                f += _int(ry_sq << 2) * dx
            dy -= 1
            f += _int(rx_sq << 1) * (3 - _int(dy << 1))
    def Fill_3(self, x, y, clr):
        if ((x < 0 or x >= self.m_width) or y < 0) or y >= self.m_height:
            return
        index = (y * self.m_width) + x
        old_clr = self.m_pixels[index]
        if old_clr == clr:
            return
        stack = Arr(0, 0)
        count = 1
        idx = 0
        total = ArraySize(self.m_pixels)
        if ArrayResize(stack, total) == -1:
            return
        stack[0] = index
        self.m_pixels[index] = clr
        i = 0
        while i < count:
            index = stack[i]
            x = _imod(index, self.m_width)
            idx = index - 1
            if x > 0 and self.m_pixels[idx] == old_clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index - self.m_width
            if idx >= 0 and self.m_pixels[idx] == old_clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index + 1
            if x < (self.m_width - 1) and self.m_pixels[idx] == old_clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index + self.m_width
            if idx < total and self.m_pixels[idx] == old_clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            i += 1
        ArrayFree(stack)
    def Fill_4(self, x, y, clr, threshould):
        if threshould == 0.0:
            self.Fill_3(x, y, clr)
            return
        if (((x < 0 or x >= self.m_width) or y < 0) or y >= self.m_height) or threshould > 255:
            return
        index = (y * self.m_width) + x
        old_clr = self.m_pixels[index]
        if old_clr == clr:
            return
        stack = Arr(0, 0)
        count = 1
        idx = 0
        total = ArraySize(self.m_pixels)
        if ArrayResize(stack, total) == -1:
            return
        stack[0] = index
        self.m_pixels[index] = clr
        i = 0
        while i < count:
            index = stack[i]
            x = _imod(index, self.m_width)
            idx = index - 1
            if (x > 0 and self.PixelsSimilar(self.m_pixels[idx], old_clr, threshould)) and self.m_pixels[idx] != clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index - self.m_width
            if (idx >= 0 and self.PixelsSimilar(self.m_pixels[idx], old_clr, threshould)) and self.m_pixels[idx] != clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index + 1
            if (x < (self.m_width - 1) and self.PixelsSimilar(self.m_pixels[idx], old_clr, threshould)) and self.m_pixels[idx] != clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index + self.m_width
            if (idx < total and self.PixelsSimilar(self.m_pixels[idx], old_clr, threshould)) and self.m_pixels[idx] != clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            i += 1
        ArrayFree(stack)
    def PixelSetAA(self, x, y, clr):
        ix = _int(MathRound(x))
        iy = _int(MathRound(y))
        rrr = 0.0
        k = 0.0
        dx = x - ix
        dy = y - iy
        a = 0
        r = 0
        g = 0
        b = 0
        c = 0
        if dx == 0.0 and dy == 0.0:
            self.PixelSet(ix, iy, clr)
            return
        _s_CCanvas_PixelSetAA_xx[2] = ix
        _s_CCanvas_PixelSetAA_xx[0] = _s_CCanvas_PixelSetAA_xx[2]
        _s_CCanvas_PixelSetAA_yy[1] = iy
        _s_CCanvas_PixelSetAA_yy[0] = _s_CCanvas_PixelSetAA_yy[1]
        if dx < 0.0:
            _s_CCanvas_PixelSetAA_xx[3] = ix - 1
            _s_CCanvas_PixelSetAA_xx[1] = _s_CCanvas_PixelSetAA_xx[3]
        if dx == 0.0:
            _s_CCanvas_PixelSetAA_xx[3] = ix
            _s_CCanvas_PixelSetAA_xx[1] = _s_CCanvas_PixelSetAA_xx[3]
        if dx > 0.0:
            _s_CCanvas_PixelSetAA_xx[3] = ix + 1
            _s_CCanvas_PixelSetAA_xx[1] = _s_CCanvas_PixelSetAA_xx[3]
        if dy < 0.0:
            _s_CCanvas_PixelSetAA_yy[3] = iy - 1
            _s_CCanvas_PixelSetAA_yy[2] = _s_CCanvas_PixelSetAA_yy[3]
        if dy == 0.0:
            _s_CCanvas_PixelSetAA_yy[3] = iy
            _s_CCanvas_PixelSetAA_yy[2] = _s_CCanvas_PixelSetAA_yy[3]
        if dy > 0.0:
            _s_CCanvas_PixelSetAA_yy[3] = iy + 1
            _s_CCanvas_PixelSetAA_yy[2] = _s_CCanvas_PixelSetAA_yy[3]
        for i in range(0, 4):
            dx = _s_CCanvas_PixelSetAA_xx[i] - x
            dy = _s_CCanvas_PixelSetAA_yy[i] - y
            _s_CCanvas_PixelSetAA_rr[i] = _fdiv(1, (dx * dx) + (dy * dy))
            rrr += _s_CCanvas_PixelSetAA_rr[i]
        for i in range(0, 4):
            k = _fdiv(_s_CCanvas_PixelSetAA_rr[i], rrr)
            c = self.PixelGet(_s_CCanvas_PixelSetAA_xx[i], _s_CCanvas_PixelSetAA_yy[i])
            a = _uchar((k * _uchar(clr >> 24)) + ((1 - k) * _uchar(c >> 24)))
            r = _uchar((k * _uchar(clr >> 16)) + ((1 - k) * _uchar(c >> 16)))
            g = _uchar((k * _uchar(clr >> 8)) + ((1 - k) * _uchar(c >> 8)))
            b = _uchar((k * _uchar(clr)) + ((1 - k) * _uchar(c)))
            self.PixelSet(_s_CCanvas_PixelSetAA_xx[i], _s_CCanvas_PixelSetAA_yy[i], (((_uchar(a) << 24) | (_uchar(r) << 16)) | (_uchar(g) << 8)) | _uchar(b))
    def LineAA(self, x1, y1, x2, y2, clr, style=UINT_MAX):
        if (x1 < 0 and x2 < 0) or (y1 < 0 and y2 < 0):
            return
        if x1 >= self.m_width and x2 >= self.m_width:
            return
        if y1 >= self.m_height and y2 >= self.m_height:
            return
        if x1 == x2 and y1 == y2:
            self.PixelSet(x1, y1, clr)
            return
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        dx = x2 - x1
        dy = y2 - y1
        xy = sqrt((dx * dx) + (dy * dy))
        xx = x1
        yy = y1
        mask = _int(1 << self.m_style_idx)
        dx = _fdiv(dx, xy)
        dy = _fdiv(dy, xy)
        while True:
            if (self.m_style & mask) == mask:
                self.PixelSetAA(xx, yy, clr)
            xx += dx
            yy += dy
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            if not (fabs(x2 - xx) >= fabs(dx) and fabs(y2 - yy) >= fabs(dy)):
                break
        if (self.m_style & mask) == mask:
            self.PixelSetAA(x2, y2, clr)
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolylineAA(self, x, y, clr, style=UINT_MAX):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        total -= 1
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for i in range(0, total):
            x1 = x[i]
            y1 = y[i]
            x2 = x[i + 1]
            y2 = y[i + 1]
            if (x1 < 0 and x2 < 0) or (y1 < 0 and y2 < 0):
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if x1 >= self.m_width and x2 >= self.m_width:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if y1 >= self.m_height and y2 >= self.m_height:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if x1 == x2 and y1 == y2:
                self.PixelSet(x1, y1, clr)
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            dx = x2 - x1
            dy = y2 - y1
            xy = sqrt((dx * dx) + (dy * dy))
            xx = x1
            yy = y1
            dx = _fdiv(dx, xy)
            dy = _fdiv(dy, xy)
            while True:
                if (self.m_style & mask) == mask:
                    self.PixelSetAA(xx, yy, clr)
                xx += dx
                yy += dy
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                if not (fabs(x2 - xx) >= fabs(dx) and fabs(y2 - yy) >= fabs(dy)):
                    break
            if (self.m_style & mask) == mask:
                self.PixelSetAA(x2, y2, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolygonAA(self, x, y, clr, style=UINT_MAX):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for i in range(0, total):
            x1 = x[i]
            y1 = y[i]
            x2 = (x[i + 1] if ((i + 1) != total) else x[0])
            y2 = (y[i + 1] if ((i + 1) != total) else y[0])
            if (x1 < 0 and x2 < 0) or (y1 < 0 and y2 < 0):
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if x1 >= self.m_width and x2 >= self.m_width:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if y1 >= self.m_height and y2 >= self.m_height:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if x1 == x2 and y1 == y2:
                self.PixelSet(x1, y1, clr)
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            dx = x2 - x1
            dy = y2 - y1
            xy = sqrt((dx * dx) + (dy * dy))
            xx = x1
            yy = y1
            dx = _fdiv(dx, xy)
            dy = _fdiv(dy, xy)
            while True:
                if (self.m_style & mask) == mask:
                    self.PixelSetAA(xx, yy, clr)
                xx += dx
                yy += dy
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                if not (fabs(x2 - xx) >= fabs(dx) and fabs(y2 - yy) >= fabs(dy)):
                    break
            if (self.m_style & mask) == mask:
                self.PixelSetAA(x2, y2, clr)
        if style != UINT_MAX:
            self.m_style = prev_style
    def TriangleAA(self, x1, y1, x2, y2, x3, y3, clr, style=UINT_MAX):
        x = Arr(3, 0, dyn=False)
        y = Arr(3, 0, dyn=False)
        x[0] = x1
        x[1] = x2
        x[2] = x3
        y[0] = y1
        y[1] = y2
        y[2] = y3
        self.PolygonAA(x, y, clr, style)
    def CircleAA(self, x, y, r, clr, style=UINT_MAX):
        if r <= 0:
            return
        xx = x + r
        yy = y
        fi = 0.0
        df = _fdiv(M_PI_2, MathCeil(r))
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        if r > M_PI:
            df = df / 2
        while True:
            xx = x + (r * cos(fi))
            yy = y - (r * sin(fi))
            if (self.m_style & mask) == mask:
                self.PixelSetAA(xx, yy, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            fi += df
            if not (fabs((2 * M_PI) - fi) >= (df / 2)):
                break
        if style != UINT_MAX:
            self.m_style = prev_style
    def EllipseAA(self, x1, y1, x2, y2, clr, style=UINT_MAX):
        rx = (x2 - x1) / 2
        ry = (y2 - y1) / 2
        x = ((x1 + rx) if (x2 > x1) else (x2 + rx))
        y = ((y1 + ry) if (y2 > y1) else (y2 + ry))
        rx2 = rx * rx
        ry2 = ry * ry
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        quarter = round(_fdiv(rx2, sqrt(rx2 + ry2)))
        dx = 0.0
        while dx <= quarter:
            dy = ry * sqrt(1 - _fdiv(dx * dx, rx2))
            if (self.m_style & mask) == mask:
                self.PixelSet4AA(x, y, dx, dy, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            dx += 1
        quarter = round(_fdiv(ry2, sqrt(rx2 + ry2)))
        dy = 0.0
        while dy <= quarter:
            dx = rx * sqrt(1 - _fdiv(dy * dy, ry2))
            if (self.m_style & mask) == mask:
                self.PixelSet4AA(x, y, dx, dy, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            dy += 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def LineWu(self, x1, y1, x2, y2, clr, style=UINT_MAX):
        dx = ((x2 - x1) if (x2 > x1) else (x1 - x2))
        dy = ((y2 - y1) if (y2 > y1) else (y1 - y2))
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        tmp = 0
        if dx == 0:
            if y1 > y2:
                tmp = y1
                y1 = y2
                y2 = tmp
            if ((y2 < 0 or y1 >= self.m_height) or x1 < 0) or x1 >= self.m_width:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if y1 < 0:
                y1 = 0
            if y2 >= (self.m_height - 1):
                y2 = self.m_height - 1
            index = (y1 * self.m_width) + x1
            i = y1
            while i <= y2:
                if (self.m_style & mask) == mask:
                    self.m_pixels[index] = clr
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                i += 1
                index += self.m_width
            if style != UINT_MAX:
                self.m_style = prev_style
            return
        if dy == 0:
            if x1 > x2:
                tmp = x1
                x1 = x2
                x2 = tmp
            if ((x2 < 0 or x1 >= self.m_width) or y1 < 0) or y1 >= self.m_height:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if x1 < 0:
                x1 = 0
            if x2 >= self.m_width:
                x2 = self.m_width - 1
            i = 0
            index = (y1 * self.m_width) + x1
            while i < (x2 - x1):
                if (self.m_style & mask) == mask:
                    self.m_pixels[index] = clr
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                i += 1
                index += 1
            if style != UINT_MAX:
                self.m_style = prev_style
            return
        if dx == 0 and dy == 0:
            self.PixelSet(x1, y1, clr)
            if style != UINT_MAX:
                self.m_style = prev_style
            return
        if dy < dx:
            if x2 < x1:
                x2 += x1
                x1 = x2 - x1
                x2 -= x1
                y2 += y1
                y1 = y2 - y1
                y2 -= y1
            if y2 < y1:
                dy *= -1
            grad = _fdiv(float(dy), dx)
            intery = y1 + grad
            if (self.m_style & mask) == mask:
                self.PixelSet(x1, y1, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            for x in range(x1 + 1, x2):
                alpha1 = 1 - (intery - _int(intery))
                alpha2 = intery - _int(intery)
                if (self.m_style & mask) == mask:
                    self.PixelTransform(x, _int(intery), clr, alpha1)
                    self.PixelTransform(x, _int(intery) + 1, clr, alpha2)
                intery += grad
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
            if (self.m_style & mask) == mask:
                self.PixelSet(x2, y2, clr)
        else:
            if y2 < y1:
                x2 += x1
                x1 = x2 - x1
                x2 -= x1
                y2 += y1
                y1 = y2 - y1
                y2 -= y1
            if x2 < x1:
                dx *= -1
            grad = _fdiv(float(dx), dy)
            interx = x1 + grad
            if (self.m_style & mask) == mask:
                self.PixelSet(x1, y1, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            for y in range(y1 + 1, y2):
                alpha1 = 1 - (interx - _int(interx))
                alpha2 = interx - _int(interx)
                if (self.m_style & mask) == mask:
                    self.PixelTransform(_int(interx), y, clr, alpha1)
                    self.PixelTransform(_int(interx) + 1, y, clr, alpha2)
                interx += grad
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
            if (self.m_style & mask) == mask:
                self.PixelSet(x2, y2, clr)
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolylineWu(self, x, y, clr, style=UINT_MAX):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        total -= 1
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for i in range(0, total):
            x1 = x[i]
            x2 = x[i + 1]
            y1 = y[i]
            y2 = y[i + 1]
            dx = ((x2 - x1) if (x2 > x1) else (x1 - x2))
            dy = ((y2 - y1) if (y2 > y1) else (y1 - y2))
            tmp = 0
            if dx == 0:
                if y1 > y2:
                    tmp = y1
                    y1 = y2
                    y2 = tmp
                if ((y2 < 0 or y1 >= self.m_height) or x1 < 0) or x1 >= self.m_width:
                    continue
                if y1 < 0:
                    y1 = 0
                if y2 >= (self.m_height - 1):
                    y2 = self.m_height - 1
                index = (y1 * self.m_width) + x1
                j = y1
                while j <= y2:
                    if (self.m_style & mask) == mask:
                        self.m_pixels[index] = clr
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                    j += 1
                    index += self.m_width
                continue
            if dy == 0:
                if x1 > x2:
                    tmp = x1
                    x1 = x2
                    x2 = tmp
                if ((x2 < 0 or x1 >= self.m_width) or y1 < 0) or y1 >= self.m_height:
                    continue
                if x1 < 0:
                    x1 = 0
                if x2 >= self.m_width:
                    x2 = self.m_width - 1
                j = 0
                index = (y1 * self.m_width) + x1
                while j < (x2 - x1):
                    if (self.m_style & mask) == mask:
                        self.m_pixels[index] = clr
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                    j += 1
                    index += 1
                continue
            if dx == 0 and dy == 0:
                self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                continue
            if dy < dx:
                if x2 < x1:
                    x2 += x1
                    x1 = x2 - x1
                    x2 -= x1
                    y2 += y1
                    y1 = y2 - y1
                    y2 -= y1
                if y2 < y1:
                    dy *= -1
                grad = _fdiv(float(dy), dx)
                intery = y1 + grad
                if (self.m_style & mask) == mask:
                    self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                for xc in range(x1 + 1, x2):
                    alpha1 = 1 - (intery - _int(intery))
                    alpha2 = intery - _int(intery)
                    if (self.m_style & mask) == mask:
                        self.PixelTransform(xc, _int(intery), clr, alpha1)
                        self.PixelTransform(xc, _int(intery) + 1, clr, alpha2)
                    intery += grad
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if (self.m_style & mask) == mask:
                    self.PixelSet(x2, y2, clr)
            else:
                if y2 < y1:
                    x2 += x1
                    x1 = x2 - x1
                    x2 -= x1
                    y2 += y1
                    y1 = y2 - y1
                    y2 -= y1
                if x2 < x1:
                    dx *= -1
                grad = _fdiv(float(dx), dy)
                interx = x1 + grad
                if (self.m_style & mask) == mask:
                    self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                for yc in range(y1 + 1, y2):
                    alpha1 = 1 - (interx - _int(interx))
                    alpha2 = interx - _int(interx)
                    if (self.m_style & mask) == mask:
                        self.PixelTransform(_int(interx), yc, clr, alpha1)
                        self.PixelTransform(_int(interx) + 1, yc, clr, alpha2)
                    interx += grad
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if (self.m_style & mask) == mask:
                    self.PixelSet(x2, y2, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolygonWu(self, x, y, clr, style=UINT_MAX):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for i in range(0, total):
            x1 = x[i]
            y1 = y[i]
            x2 = (x[i + 1] if ((i + 1) != total) else x[0])
            y2 = (y[i + 1] if ((i + 1) != total) else y[0])
            dx = ((x2 - x1) if (x2 > x1) else (x1 - x2))
            dy = ((y2 - y1) if (y2 > y1) else (y1 - y2))
            tmp = 0
            if dx == 0:
                if y1 > y2:
                    tmp = y1
                    y1 = y2
                    y2 = tmp
                if ((y2 < 0 or y1 >= self.m_height) or x1 < 0) or x1 >= self.m_width:
                    continue
                if y1 < 0:
                    y1 = 0
                if y2 >= (self.m_height - 1):
                    y2 = self.m_height - 1
                index = (y1 * self.m_width) + x1
                j = y1
                while j <= y2:
                    if (self.m_style & mask) == mask:
                        self.m_pixels[index] = clr
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                    j += 1
                    index += self.m_width
                continue
            if dy == 0:
                if x1 > x2:
                    tmp = x1
                    x1 = x2
                    x2 = tmp
                if ((x2 < 0 or x1 >= self.m_width) or y1 < 0) or y1 >= self.m_height:
                    continue
                if x1 < 0:
                    x1 = 0
                if x2 >= self.m_width:
                    x2 = self.m_width - 1
                j = 0
                index = (y1 * self.m_width) + x1
                while j < (x2 - x1):
                    if (self.m_style & mask) == mask:
                        self.m_pixels[index] = clr
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                    j += 1
                    index += 1
                continue
            if dx == 0 and dy == 0:
                self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                continue
            if dy < dx:
                if x2 < x1:
                    x2 += x1
                    x1 = x2 - x1
                    x2 -= x1
                    y2 += y1
                    y1 = y2 - y1
                    y2 -= y1
                if y2 < y1:
                    dy *= -1
                grad = _fdiv(float(dy), dx)
                intery = y1 + grad
                if (self.m_style & mask) == mask:
                    self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                for xc in range(x1 + 1, x2):
                    alpha1 = 1 - (intery - _int(intery))
                    alpha2 = intery - _int(intery)
                    if (self.m_style & mask) == mask:
                        self.PixelTransform(xc, _int(intery), clr, alpha1)
                        self.PixelTransform(xc, _int(intery) + 1, clr, alpha2)
                    intery += grad
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if (self.m_style & mask) == mask:
                    self.PixelSet(x2, y2, clr)
            else:
                if y2 < y1:
                    x2 += x1
                    x1 = x2 - x1
                    x2 -= x1
                    y2 += y1
                    y1 = y2 - y1
                    y2 -= y1
                if x2 < x1:
                    dx *= -1
                grad = _fdiv(float(dx), dy)
                interx = x1 + grad
                if (self.m_style & mask) == mask:
                    self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                for yc in range(y1 + 1, y2):
                    alpha1 = 1 - (interx - _int(interx))
                    alpha2 = interx - _int(interx)
                    if (self.m_style & mask) == mask:
                        self.PixelTransform(_int(interx), yc, clr, alpha1)
                        self.PixelTransform(_int(interx) + 1, yc, clr, alpha2)
                    interx += grad
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if (self.m_style & mask) == mask:
                    self.PixelSet(x2, y2, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def TriangleWu(self, x1, y1, x2, y2, x3, y3, clr, style=UINT_MAX):
        x = Arr(3, 0, dyn=False)
        y = Arr(3, 0, dyn=False)
        x[0] = x1
        x[1] = x2
        x[2] = x3
        y[0] = y1
        y[1] = y2
        y[2] = y3
        self.PolygonWu(x, y, clr, style)
    def CircleWu(self, x, y, r, clr, style=UINT_MAX):
        if r <= 0:
            return
        r2 = r * r
        quarter = round(_fdiv(r, sqrt(2.0)))
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        d1 = 0
        while d1 <= quarter:
            d2 = sqrt(r2 - (d1 * d1))
            alpha1 = d2 - floor(d2)
            alpha2 = 1 - alpha1
            if (self.m_style & mask) == mask:
                self.PixelTransform4(x, y, _int(d2) + 1, d1, clr, alpha1)
                self.PixelTransform4(x, y, d1, _int(d2) + 1, clr, alpha1)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            if (self.m_style & mask) == mask:
                self.PixelTransform4(x, y, d1, _int(d2), clr, alpha2)
                self.PixelTransform4(x, y, _int(d2), d1, clr, alpha2)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            d1 += 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def EllipseWu(self, x1, y1, x2, y2, clr, style=UINT_MAX):
        rx = _idiv(x2 - x1, 2)
        ry = _idiv(y2 - y1, 2)
        x = ((x1 + rx) if (x2 > x1) else (x2 + rx))
        y = ((y1 + ry) if (y2 > y1) else (y2 + ry))
        if rx <= 0 or ry <= 0:
            return
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        rx2 = rx * rx
        ry2 = ry * ry
        quarter = round(_fdiv(rx2, sqrt(rx2 + ry2)))
        dx = 0
        while dx <= quarter:
            dy = ry * sqrt(1 - _fdiv(dx * dx, rx2))
            alpha1 = dy - floor(dy)
            alpha2 = 1 - alpha1
            if (self.m_style & mask) == mask:
                self.PixelTransform4(x, y, dx, _int(dy) + 1, clr, alpha1)
                self.PixelTransform4(x, y, dx, _int(dy), clr, alpha2)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            dx += 1
        quarter = round(_fdiv(ry2, sqrt(rx2 + ry2)))
        dy = 0
        while dy <= quarter:
            dx = rx * sqrt(1 - _fdiv(dy * dy, ry2))
            alpha1 = dx - floor(dx)
            alpha2 = 1 - alpha1
            if (self.m_style & mask) == mask:
                self.PixelTransform4(x, y, _int(dx) + 1, dy, clr, alpha1)
                self.PixelTransform4(x, y, _int(dx), dy, clr, alpha2)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            dy += 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def LineThickVertical(self, x, y1, y2, clr, size, style, end_style):
        if size <= 2:
            if size > 0:
                self.LineWu(x, y1, x, y2, clr, style)
            return
        r = size / 2.0
        dy = MathAbs(y2 - y1)
        sign = (1 if (y1 < y2) else -1)
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        if style == STYLE_SOLID:
            self.SegmentVertical(x, y1, y2, sign, r, clr, end_style)
        else:
            ys = 0
            ye = 0
            steps = _int(MathRound(_fdiv(dy, r)))
            segment = False
            for i in range(0, steps + 1):
                if (self.m_style & mask) == mask and (not segment):
                    ys = y1 + (sign * _int(i * r))
                    segment = True
                elif (self.m_style & mask) != mask and segment:
                    ye = y1 + (sign * _int(i * r))
                    self.SegmentVertical(x, ys, ye, sign, r, clr, end_style)
                    segment = False
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
            if segment:
                self.SegmentVertical(x, ys, y2, sign, r, clr, end_style)
        if style != UINT_MAX:
            self.m_style = prev_style
    def LineThickHorizontal(self, x1, x2, y, clr, size, style, end_style):
        if size <= 2:
            if size > 0:
                self.LineWu(x1, y, x2, y, clr, style)
            return
        r = size / 2.0
        dx = MathAbs(x2 - x1)
        sign = (1 if (x1 < x2) else -1)
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        if style == STYLE_SOLID:
            self.SegmentHorizontal(x1, x2, y, sign, r, clr, end_style)
        else:
            xs = 0
            xe = 0
            steps = _int(MathRound(_fdiv(dx, r)))
            segment = False
            for i in range(0, steps + 1):
                if (self.m_style & mask) == mask and (not segment):
                    xs = x1 + (sign * _int(i * r))
                    segment = True
                elif (self.m_style & mask) != mask and segment:
                    xe = x1 + (sign * _int(i * r))
                    self.SegmentHorizontal(xs, xe, y, sign, r, clr, end_style)
                    segment = False
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
            if segment:
                self.SegmentHorizontal(xs, x2, y, sign, r, clr, end_style)
        if style != UINT_MAX:
            self.m_style = prev_style
    def LineThick(self, x1, y1, x2, y2, clr, size, style, end_style):
        if size <= 2:
            if size > 0:
                self.LineWu(x1, y1, x2, y2, clr, style)
            return
        r = size / 2.0
        dx = MathAbs(x2 - x1)
        dy = MathAbs(y2 - y1)
        if dx == 0:
            self.LineThickVertical(x1, y1, y2, clr, size, style, end_style)
            return
        if dy == 0:
            self.LineThickHorizontal(x1, x2, y1, clr, size, style, end_style)
            return
        k = MathArctan(_fdiv(dx, dy))
        rcos_k = r * cos(k)
        rsin_k = r * sin(k)
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        xsign = (1 if (x1 < x2) else -1)
        ysign = (1 if (y1 < y2) else -1)
        kp0 = (-xsign) * ysign * _fdiv(dx, dy)
        kp1 = _fdiv(-1, kp0)
        if style == STYLE_SOLID:
            self.Segment(x1, y1, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
        else:
            xs = 0
            ys = 0
            xe = 0
            ye = 0
            length = MathSqrt((dx * dx) + (dy * dy))
            steps = _int(MathRound(_fdiv(length, r)))
            segment = False
            for i in range(0, steps + 1):
                if (self.m_style & mask) == mask and (not segment):
                    xs = x1 + (xsign * _int(i * rsin_k))
                    ys = y1 + (ysign * _int(i * rcos_k))
                    segment = True
                elif (self.m_style & mask) != mask and segment:
                    xe = x1 + (xsign * _int(i * rsin_k))
                    ye = y1 + (ysign * _int(i * rcos_k))
                    self.Segment(xs, ys, xe, ye, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
                    segment = False
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
            if segment:
                self.Segment(xs, ys, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolylineThick(self, x, y, clr, size, style, end_style):
        if size <= 2:
            if size > 0:
                self.PolylineWu(x, y, clr, style)
            return
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        total -= 1
        r = size / 2.0
        gap = 1.0
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for index in range(0, total):
            x1 = x[index]
            y1 = y[index]
            x2 = x[index + 1]
            y2 = y[index + 1]
            dx = MathAbs(x2 - x1)
            dy = MathAbs(y2 - y1)
            if dx == 0:
                sign = (1 if (y1 < y2) else -1)
                if style == STYLE_SOLID:
                    self.SegmentVertical(x1, y1, y2, sign, r, clr, end_style)
                else:
                    ys = y1
                    ye = 0
                    steps = _fdiv(dy, r)
                    isteps = _int(steps)
                    segment = False
                    for i in range(0, isteps):
                        if (self.m_style & mask) == mask and (not segment):
                            ys = y1 + (sign * _int(i * r))
                            segment = True
                        elif (self.m_style & mask) != mask and segment:
                            ye = y1 + (sign * _int(i * r))
                            self.SegmentVertical(x1, ys, ye, sign, r, clr, end_style)
                            segment = False
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                    if segment or (steps < 1 and (self.m_style & mask) == mask):
                        self.SegmentVertical(x1, ys, y2, sign, r, clr, end_style)
                    gap -= steps - isteps
                    if gap < 0:
                        gap += 1
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                continue
            if dy == 0:
                sign = (1 if (x1 < x2) else -1)
                if style == STYLE_SOLID:
                    self.SegmentHorizontal(x1, x2, y1, sign, r, clr, end_style)
                else:
                    xs = x1
                    xe = 0
                    steps = _fdiv(dx, r)
                    isteps = _int(steps)
                    segment = False
                    for i in range(0, isteps):
                        if (self.m_style & mask) == mask and (not segment):
                            xs = x1 + (sign * _int(i * r))
                            segment = True
                        elif (self.m_style & mask) != mask and segment:
                            xe = x1 + (sign * _int(i * r))
                            self.SegmentHorizontal(xs, xe, y1, sign, r, clr, end_style)
                            segment = False
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                    if segment or (steps < 1 and (self.m_style & mask) == mask):
                        self.SegmentHorizontal(xs, x2, y1, sign, r, clr, end_style)
                    gap -= steps - isteps
                    if gap < 0:
                        gap += 1
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                continue
            k = MathArctan(_fdiv(dx, dy))
            rcos_k = r * cos(k)
            rsin_k = r * sin(k)
            xsign = (1 if (x1 < x2) else -1)
            ysign = (1 if (y1 < y2) else -1)
            kp0 = (-xsign) * ysign * _fdiv(dx, dy)
            kp1 = _fdiv(-1, kp0)
            if style == STYLE_SOLID:
                self.Segment(x1, y1, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
            else:
                xs = x1
                ys = y1
                xe = 0
                ye = 0
                length = MathSqrt((dx * dx) + (dy * dy))
                steps = _fdiv(length, r)
                isteps = _int(steps)
                segment = False
                for i in range(0, isteps):
                    if (self.m_style & mask) == mask and (not segment):
                        xs = x1 + (xsign * _int(i * rsin_k))
                        ys = y1 + (ysign * _int(i * rcos_k))
                        segment = True
                    elif (self.m_style & mask) != mask and segment:
                        xe = x1 + (xsign * _int(i * rsin_k))
                        ye = y1 + (ysign * _int(i * rcos_k))
                        self.Segment(xs, ys, xe, ye, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
                        segment = False
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if segment or (steps < 1 and (self.m_style & mask) == mask):
                    self.Segment(xs, ys, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
                gap -= steps - isteps
                if gap < 0:
                    gap += 1
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolygonThick(self, x, y, clr, size, style, end_style):
        if size <= 2:
            if size > 0:
                self.PolylineWu(x, y, clr, style)
            return
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        r = size / 2.0
        gap = 1.0
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for index in range(0, total):
            x1 = x[index]
            y1 = y[index]
            x2 = (x[index + 1] if (index != (total - 1)) else x[0])
            y2 = (y[index + 1] if (index != (total - 1)) else y[0])
            dx = MathAbs(x2 - x1)
            dy = MathAbs(y2 - y1)
            if dx == 0:
                sign = (1 if (y1 < y2) else -1)
                if style == STYLE_SOLID:
                    self.SegmentVertical(x1, y1, y2, sign, r, clr, end_style)
                else:
                    ys = y1
                    ye = 0
                    steps = _fdiv(dy, r)
                    isteps = _int(steps)
                    segment = False
                    for i in range(0, isteps):
                        if (self.m_style & mask) == mask and (not segment):
                            ys = y1 + (sign * _int(i * r))
                            segment = True
                        elif (self.m_style & mask) != mask and segment:
                            ye = y1 + (sign * _int(i * r))
                            self.SegmentVertical(x1, ys, ye, sign, r, clr, end_style)
                            segment = False
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                    if segment or (steps < 1 and (self.m_style & mask) == mask):
                        self.SegmentVertical(x1, ys, y2, sign, r, clr, end_style)
                    gap -= steps - isteps
                    if gap < 0:
                        gap += 1
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                continue
            if dy == 0:
                sign = (1 if (x1 < x2) else -1)
                if style == STYLE_SOLID:
                    self.SegmentHorizontal(x1, x2, y1, sign, r, clr, end_style)
                else:
                    xs = x1
                    xe = 0
                    steps = _fdiv(dx, r)
                    isteps = _int(steps)
                    segment = False
                    for i in range(0, isteps):
                        if (self.m_style & mask) == mask and (not segment):
                            xs = x1 + (sign * _int(i * r))
                            segment = True
                        elif (self.m_style & mask) != mask and segment:
                            xe = x1 + (sign * _int(i * r))
                            self.SegmentHorizontal(xs, xe, y1, sign, r, clr, end_style)
                            segment = False
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                    if segment or (steps < 1 and (self.m_style & mask) == mask):
                        self.SegmentHorizontal(xs, x2, y1, sign, r, clr, end_style)
                    gap -= steps - isteps
                    if gap < 0:
                        gap += 1
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                continue
            k = MathArctan(_fdiv(dx, dy))
            rcos_k = r * cos(k)
            rsin_k = r * sin(k)
            xsign = (1 if (x1 < x2) else -1)
            ysign = (1 if (y1 < y2) else -1)
            kp0 = (-xsign) * ysign * _fdiv(dx, dy)
            kp1 = _fdiv(-1, kp0)
            if style == STYLE_SOLID:
                self.Segment(x1, y1, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
            else:
                xs = x1
                ys = y1
                xe = 0
                ye = 0
                length = MathSqrt((dx * dx) + (dy * dy))
                steps = _fdiv(length, r)
                isteps = _int(steps)
                segment = False
                for i in range(0, isteps):
                    if (self.m_style & mask) == mask and (not segment):
                        xs = x1 + (xsign * _int(i * rsin_k))
                        ys = y1 + (ysign * _int(i * rcos_k))
                        segment = True
                    elif (self.m_style & mask) != mask and segment:
                        xe = x1 + (xsign * _int(i * rsin_k))
                        ye = y1 + (ysign * _int(i * rcos_k))
                        self.Segment(xs, ys, xe, ye, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
                        segment = False
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if segment or (steps < 1 and (self.m_style & mask) == mask):
                    self.Segment(xs, ys, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
                gap -= steps - isteps
                if gap < 0:
                    gap += 1
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolylineSmooth(self, x, y, clr, size, style=STYLE_SOLID, end_style=LINE_END_ROUND, tension=0.5, step=10.0):
        arr_size = ArraySize(x)
        if arr_size != ArraySize(y):
            return
        x1 = Box(0.0)
        x2 = Box(0.0)
        y1 = Box(0.0)
        y2 = Box(0.0)
        tension *= 0.3
        xc = Arr(0, 0)
        yc = Arr(0, 0)
        ptX = Arr(0, 0.0)
        ptY = Arr(0, 0.0)
        size_pt = (arr_size * 3) - 2
        ArrayResize(ptX, size_pt)
        ArrayResize(ptY, size_pt)
        self.CalcCurveBezierEndp(x[0], y[0], x[1], y[1], tension, x1, y1)
        ptX[0] = x[0]
        ptY[0] = y[0]
        ptX[1] = x1.v
        ptY[1] = y1.v
        for i in range(0, arr_size - 2):
            self.CalcCurveBezier(x, y, i, tension, x1, y1, x2, y2)
            ptX[(3 * i) + 2] = x1.v
            ptY[(3 * i) + 2] = y1.v
            ptX[(3 * i) + 3] = x[i + 1]
            ptY[(3 * i) + 3] = y[i + 1]
            ptX[(3 * i) + 4] = x2.v
            ptY[(3 * i) + 4] = y2.v
        self.CalcCurveBezierEndp(x[arr_size - 1], y[arr_size - 1], x[arr_size - 2], y[arr_size - 2], tension, x1, y1)
        ptX[size_pt - 2] = x1.v
        ptY[size_pt - 2] = y1.v
        ptX[size_pt - 1] = x[arr_size - 1]
        ptY[size_pt - 1] = y[arr_size - 1]
        index = 0
        for i in range(0, arr_size - 1):
            distance = MathSqrt(((x[i + 1] - x[i]) * (x[i + 1] - x[i])) + ((y[i + 1] - y[i]) * (y[i + 1] - y[i])))
            size_i = (_int(_fdiv(distance, step)) if (step > 0.0) else 1)
            if size_i < 1:
                size_i = 2
            ArrayResize(xc, ArraySize(xc) + size_i, 1024)
            ArrayResize(yc, ArraySize(yc) + size_i, 1024)
            t = 0
            while t < size_i:
                xc[index] = _int(MathRound(self.CalcBezierX(_fdiv(float(t), size_i), ptX[3 * i], ptX[(3 * i) + 1], ptX[(3 * i) + 2], ptX[(3 * i) + 3])))
                yc[index] = _int(MathRound(self.CalcBezierY(_fdiv(float(t), size_i), ptY[3 * i], ptY[(3 * i) + 1], ptY[(3 * i) + 2], ptY[(3 * i) + 3])))
                t += 1
                index += 1
        self.PolylineThick(xc, yc, clr, size, style, LINE_END_ROUND)
    def PolygonSmooth(self, x, y, clr, size, style=STYLE_SOLID, end_style=LINE_END_ROUND, tension=0.5, step=10.0):
        size_arr = ArraySize(x)
        if size_arr != ArraySize(y):
            return
        x1 = Box(0.0)
        x2 = Box(0.0)
        y1 = Box(0.0)
        y2 = Box(0.0)
        tension *= 0.3
        xc = Arr(0, 0)
        yc = Arr(0, 0)
        ptX = Arr(0, 0.0)
        ptY = Arr(0, 0.0)
        size_pt = ((size_arr + 1) * 3) - 3
        ArrayResize(ptX, size_pt)
        ArrayResize(ptY, size_pt)
        xe = Arr(0, 0)
        ye = Arr(0, 0)
        ArrayResize(xe, size_arr + 2)
        ArrayResize(ye, size_arr + 2)
        xe[0] = x[size_arr - 1]
        ye[0] = y[size_arr - 1]
        xe[size_arr + 1] = x[0]
        ye[size_arr + 1] = y[0]
        ArrayCopy(xe, x, 1, 0, size_arr)
        ArrayCopy(ye, y, 1, 0, size_arr)
        for i in range(0, size_arr):
            self.CalcCurveBezier(xe, ye, i, tension, x1, y1, x2, y2)
            ptX[(3 * i) + 0] = x1.v
            ptY[(3 * i) + 0] = y1.v
            ptX[(3 * i) + 1] = xe[i + 1]
            ptY[(3 * i) + 1] = ye[i + 1]
            ptX[(3 * i) + 2] = x2.v
            ptY[(3 * i) + 2] = y2.v
        index = 0
        for i in range(0, size_arr - 1):
            distance = MathSqrt(((x[i] - x[i + 1]) * (x[i] - x[i + 1])) + ((y[i] - y[i + 1]) * (y[i] - y[i + 1])))
            size_i = (_int(_fdiv(distance, step)) if (step > 0.0) else 1)
            if size_i < 1:
                size_i = 2
            ArrayResize(xc, ArraySize(xc) + size_i, 1024)
            ArrayResize(yc, ArraySize(yc) + size_i, 1024)
            t = 0
            while t < size_i:
                xc[index] = _int(MathRound(self.CalcBezierX(_fdiv(float(t), size_i), ptX[1 + (i * 3)], ptX[2 + (i * 3)], ptX[3 + (i * 3)], ptX[4 + (i * 3)])))
                yc[index] = _int(MathRound(self.CalcBezierY(_fdiv(float(t), size_i), ptY[1 + (i * 3)], ptY[2 + (i * 3)], ptY[3 + (i * 3)], ptY[4 + (i * 3)])))
                t += 1
                index += 1
        distance = MathSqrt(((x[size_arr - 1] - x[0]) * (x[size_arr - 1] - x[0])) + ((y[size_arr - 1] - y[0]) * (y[size_arr - 1] - y[0])))
        size_i = (_int(_fdiv(distance, step)) if (step > 0.0) else 1)
        if size_i < 1:
            size_i = 2
        ArrayResize(xc, ArraySize(xc) + size_i, 1024)
        ArrayResize(yc, ArraySize(yc) + size_i, 1024)
        t = 0
        while t < size_i:
            xc[index] = _int(MathRound(self.CalcBezierX(_fdiv(float(t), size_i), ptX[size_pt - 2], ptX[size_pt - 1], ptX[0], ptX[1])))
            yc[index] = _int(MathRound(self.CalcBezierY(_fdiv(float(t), size_i), ptY[size_pt - 2], ptY[size_pt - 1], ptY[0], ptY[1])))
            t += 1
            index += 1
        self.PolygonThick(xc, yc, clr, size, style, LINE_END_ROUND)
    def BitBlt(self, dst_x, dst_y, src, src_width, src_height, src_x, src_y, src_dx, src_dy, mode=0):
        for y in range(0, src_dy):
            for x in range(0, src_dx):
                self.PixelSet(dst_x + x, dst_y + y, src[((src_y + y) * src_width) + src_x + x])
    def FontSet_4(self, name, size, flags=0, angle=0):
        if not TextSetFont(name, size, flags, angle):
            return False
        self.m_fontname = name
        self.m_fontsize = size
        self.m_fontflags = flags
        self.m_fontangle = angle
        return True
    def FontSet_0(self):
        return TextSetFont(self.m_fontname, self.m_fontsize, self.m_fontflags, self.m_fontangle)
    def FontNameSet(self, name):
        if not TextSetFont(name, self.m_fontsize, self.m_fontflags, self.m_fontangle):
            return False
        self.m_fontname = name
        return True
    def FontSizeSet(self, size):
        if not TextSetFont(self.m_fontname, size, self.m_fontflags, self.m_fontangle):
            return False
        self.m_fontsize = size
        return True
    def FontFlagsSet(self, flags):
        if not TextSetFont(self.m_fontname, self.m_fontsize, flags, self.m_fontangle):
            return False
        self.m_fontflags = flags
        return True
    def FontAngleSet(self, angle):
        if not TextSetFont(self.m_fontname, self.m_fontsize, self.m_fontflags, angle):
            return False
        self.m_fontangle = angle
        return True
    def FontGet(self, name, size, flags, angle):
        name.v = self.m_fontname
        size.v = self.m_fontsize
        flags.v = self.m_fontflags
        angle.v = self.m_fontangle
    def FontNameGet(self):
        return self.m_fontname
    def FontSizeGet(self):
        return self.m_fontsize
    def FontFlagsGet(self):
        return self.m_fontflags
    def FontAngleGet(self):
        return self.m_fontangle
    def TextOut(self, x, y, text, clr, alignment=0):
        if self.FontSet_0():
            TextOut(text, x, y, alignment, self.m_pixels, self.m_width, self.m_height, clr, self.m_format)
    def TextWidth(self, text):
        if not self.FontSet_0():
            return 0
        w = 0
        h = 0
        TextGetSize(text, _ValRef(w), _ValRef(h))
        return _int(w)
    def TextHeight(self, text):
        if not self.FontSet_0():
            return 0
        w = 0
        h = 0
        TextGetSize(text, _ValRef(w), _ValRef(h))
        return _int(h)
    def TextSize(self, text, width, height):
        if self.FontSet_0():
            TextGetSize(text, _ValRef(_uint(width.v)), _ValRef(_uint(height.v)))
    @staticmethod
    def GetDefaultColor(i):
        if i < 0:
            return 0
        if i < ArraySize(CCanvas.m_default_colors):
            return CCanvas.m_default_colors[i]
        return ((0xFF000000 | (_uchar((_imod(i, 3) * 60) + (i * 50)) << 16)) | (_uchar((_imod(i + 1, 3) * 60) + (i * 60)) << 8)) | _uchar((_imod(i + 2, 3) * 60) + (i * 50))
    def TransparentLevelSet(self, value):
        total = ArraySize(self.m_pixels)
        value24 = _uint(value << 24)
        for i in range(0, total):
            self.m_pixels[i] = value24 | (self.m_pixels[i] & 0xFFFFFF)
    def LoadFromFile(self, filename):
        if not CCanvas.LoadBitmap(filename, self.m_pixels, _AttrRef(self, 'm_width'), _AttrRef(self, 'm_height')):
            return False
        if self.m_format == COLOR_FORMAT_ARGB_RAW:
            a = 0
            r = 0
            g = 0
            b = 0
            img_size = self.m_width * self.m_height
            for i in range(0, img_size):
                _sw1 = (a := _uchar(self.m_pixels[i] >> 24))
                if _sw1 == 0xFF:
                    pass
                elif _sw1 == 0x00:
                    self.m_pixels[i] = 0
                else:
                    r = _idiv(_uchar(self.m_pixels[i] >> 16) * a, 255)
                    g = _idiv(_uchar(self.m_pixels[i] >> 8) * a, 255)
                    b = _idiv(_uchar(self.m_pixels[i]) * a, 255)
                    self.m_pixels[i] = (((_uchar(a) << 24) | (_uchar(r) << 16)) | (_uchar(g) << 8)) | _uchar(b)
        return True
    def LineStyleGet(self):
        _sw2 = self.m_style
        if _sw2 == 0xFFFFFF:
            return STYLE_SOLID
        elif _sw2 == 0x3FFFF:
            return STYLE_DASH
        elif _sw2 == 0x1C71C7:
            return STYLE_DOT
        elif _sw2 == 0x381FF:
            return STYLE_DASHDOT
        elif _sw2 == 0x1C71FF:
            return STYLE_DASHDOTDOT
        else:
            return self.m_style
    def LineStyleSet(self, style):
        _sw3 = style
        if _sw3 == STYLE_SOLID:
            self.m_style = 0xFFFFFF
        elif _sw3 == STYLE_DASH:
            self.m_style = 0x3FFFF
        elif _sw3 == STYLE_DOT:
            self.m_style = 0x1C71C7
        elif _sw3 == STYLE_DASHDOT:
            self.m_style = 0x381FF
        elif _sw3 == STYLE_DASHDOTDOT:
            self.m_style = 0x1C71FF
        else:
            if (style & 0x80000000) != 0:
                self.m_style = style
        self.m_style_idx = 0
    @staticmethod
    def LoadBitmap(filename, data, width, height):
        header = BitmapHeader()
        result = True
        file = CFileBin()
        img_size = 0
        no_alpha = False
        no_flip = False
        r = 0
        g = 0
        b = 0
        if file.Open(filename, FILE_READ) == INVALID_HANDLE:
            Print('File not found')
            return False
        if file.ReadStruct(_ValRef(header)) != 8:
            Print('Failed to read file header')
            file.Close()
            return False
        width.v = _int(header.imgWidth)
        height.v = _int(header.imgHeight)
        if height.v < 0:
            height.v = -height.v
            no_flip = True
        if header.imgBitCount == 32:
            no_alpha = True
            img_size = file.ReadArray(data)
            if not no_flip:
                for i in range(0, _idiv(height.v, 2)):
                    tmp = Arr(0, 0)
                    ArrayCopy(tmp, data, 0, width.v * i, width.v)
                    ArrayCopy(data, data, width.v * i, width.v * (height.v - i - 1), width.v)
                    ArrayCopy(data, tmp, width.v * (height.v - i - 1), 0, width.v)
            for i in range(0, img_size):
                if _uchar(data[i] >> 24) != 0:
                    no_alpha = False
                    break
            if no_alpha:
                for i in range(0, img_size):
                    data[i] |= 0xFF000000
        else:
            byte_width = 0
            if ArrayResize(data, width.v * height.v) != -1:
                byte_width = width.v * 3
                byte_width = (byte_width + 3) & (~3)
                tmp = Arr(0, 0)
                for i in range(0, height.v):
                    if file.ReadArray(tmp, 0, byte_width) != byte_width:
                        result = False
                        break
                    j = 0
                    k = 0
                    p = width.v * (height.v - i - 1)
                    while j < width.v:
                        r = tmp[k + 2]
                        g = tmp[k + 1]
                        b = tmp[k]
                        data[p] = ((0xFF000000 | (_uchar(r) << 16)) | (_uchar(g) << 8)) | _uchar(b)
                        j += 1
                        p += 1
                        k += 3
            else:
                result = False
        file.Close()
        return result
    def TextOutFast(self, x, y, text, clr, alignment=0):
        TextOut(text, x, y, alignment, self.m_pixels, self.m_width, self.m_height, clr, self.m_format)
    def PixelsSimilar(self, clr0, clr1, threshould):
        dr = MathAbs(((clr0 >> 16) & 0xff) - ((clr1 >> 16) & 0xff))
        dg = MathAbs(((clr0 >> 8) & 0xff) - ((clr1 >> 8) & 0xff))
        db = MathAbs(((clr0 >> 0) & 0xff) - ((clr1 >> 0) & 0xff))
        return (dr <= threshould or dg <= threshould) or db <= threshould
    def PixelTransform(self, x, y, clr, alpha):
        index = (y * self.m_width) + x
        if (((x < 0 or y < 0) or x > self.m_width) or y > self.m_height) or index >= ArraySize(self.m_pixels):
            return
        if alpha == 1:
            self.m_pixels[index] = clr
            return
        clr0 = self.m_pixels[index]
        r0 = ((clr0 >> 16) & 0xFF) * (1.0 - alpha)
        g0 = ((clr0 >> 8) & 0xFF) * (1.0 - alpha)
        b0 = ((clr0 >> 0) & 0xFF) * (1.0 - alpha)
        r1 = ((clr >> 16) & 0xFF) * alpha
        g1 = ((clr >> 8) & 0xFF) * alpha
        b1 = ((clr >> 0) & 0xFF) * alpha
        r = _int(r0 + r1)
        g = _int(g0 + g1)
        b = _int(b0 + b1)
        self.m_pixels[(y * self.m_width) + x] = ((_int(r << 16) | _int(g << 8)) | _int(b << 0)) | _int(255 << 24)
    def PixelTransform4(self, x, y, dx, dy, clr, alpha):
        self.PixelTransform(x + dx, y + dy, clr, alpha)
        self.PixelTransform(x - dx, y + dy, clr, alpha)
        self.PixelTransform(x + dx, y - dy, clr, alpha)
        self.PixelTransform(x - dx, y - dy, clr, alpha)
    def PixelSet4AA(self, x, y, dx, dy, clr):
        self.PixelSetAA(x + dx, y + dy, clr)
        self.PixelSetAA(x - dx, y + dy, clr)
        self.PixelSetAA(x + dx, y - dy, clr)
        self.PixelSetAA(x - dx, y - dy, clr)
    def SegmentVertical(self, x, y1, y2, ysign, r, clr, end_style):
        ye1 = 0
        ye2 = 0
        ys1 = 0
        ys2 = 0
        _sw4 = end_style
        if _sw4 == LINE_END_ROUND:
            ye1 = y1
            ye2 = y2
            ys1 = y1 - _int(ysign * r)
            ys2 = y2 + _int(ysign * r)
        elif _sw4 == LINE_END_BUTT:
            ye1 = y1
            ye2 = y2
            ys1 = y1
            ys2 = y2
        elif _sw4 == LINE_END_SQUARE:
            ye1 = y1 - _int(ysign * r)
            ye2 = y2 + _int(ysign * r)
            ys1 = ye1
            ys2 = ye2
        else:
            return
        for i in range(0, MathAbs(ys2 - ys1) + 1):
            yi = ys1 + (ysign * i)
            j = 0
            while j < (2 * r):
                xi = x - r + j
                dist = self.DistancePointSegment(xi, yi, x, ye1, x, ye2)
                val = MathAbs(_fdiv(dist, r))
                self.PixelTransform(_int(xi), _int(yi), clr, self.FilterFunction(val))
                j += 1
    def SegmentHorizontal(self, x1, x2, y, xsign, r, clr, end_style):
        xe1 = 0
        xe2 = 0
        xs1 = 0
        xs2 = 0
        _sw5 = end_style
        if _sw5 == LINE_END_ROUND:
            xe1 = x1
            xe2 = x2
            xs1 = x1 - _int(xsign * r)
            xs2 = x2 + _int(xsign * r)
        elif _sw5 == LINE_END_BUTT:
            xe1 = x1
            xe2 = x2
            xs1 = x1
            xs2 = x2
        elif _sw5 == LINE_END_SQUARE:
            xe1 = x1 - _int(xsign * r)
            xe2 = x2 + _int(xsign * r)
            xs1 = xe1
            xs2 = xe2
        else:
            return
        for i in range(0, MathAbs(xs2 - xs1) + 1):
            xi = xs1 + (xsign * i)
            j = 0
            while j < (2 * r):
                yi = y - r + j
                dist = self.DistancePointSegment(xi, yi, xe1, y, xe2, y)
                val = MathAbs(_fdiv(dist, r))
                self.PixelTransform(_int(xi), _int(yi), clr, self.FilterFunction(val))
                j += 1
    def Segment(self, x1, y1, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style):
        if x1 == x2 and y1 == y2:
            return
        if x1 == x2:
            self.SegmentVertical(x1, y1, y2, ysign, r, clr, end_style)
            return
        if y1 == y2:
            self.SegmentHorizontal(x1, x2, y1, xsign, r, clr, end_style)
            return
        xe1 = 0
        ye1 = 0
        xe2 = 0
        ye2 = 0
        xs1 = 0
        ys1 = 0
        xs2 = 0
        ys2 = 0
        _sw6 = end_style
        if _sw6 == LINE_END_ROUND:
            xe1 = x1
            ye1 = y1
            xe2 = x2
            ye2 = y2
            xs1 = x1 - (xsign * _int(rsin_k))
            ys1 = y1 - (ysign * _int(rcos_k))
            xs2 = x2 + (xsign * _int(rsin_k))
            ys2 = y2 + (ysign * _int(rcos_k))
        elif _sw6 == LINE_END_BUTT:
            xe1 = x1
            ye1 = y1
            xe2 = x2
            ye2 = y2
            xs1 = x1
            ys1 = y1
            xs2 = x2
            ys2 = y2
        elif _sw6 == LINE_END_SQUARE:
            xe1 = x1 - (xsign * _int(rsin_k))
            ye1 = y1 - (ysign * _int(rcos_k))
            xe2 = x2 + (xsign * _int(rsin_k))
            ye2 = y2 + (ysign * _int(rcos_k))
            xs1 = xe1
            ys1 = ye1
            xs2 = xe2
            ys2 = ye2
        else:
            return
        p0x = xs1 + (xsign * rcos_k)
        p0y = ys1 - (ysign * rsin_k)
        p1x = xs1 - (xsign * rcos_k)
        p1y = ys1 + (ysign * rsin_k)
        p2x = xs2 + (xsign * rcos_k)
        p2y = ys2 - (ysign * rsin_k)
        p3x = xs2 - (xsign * rcos_k)
        p3y = ys2 + (ysign * rsin_k)
        if MathAbs(kp0) >= 1:
            xi0 = 0.0
            xi1 = 0.0
            height = MathAbs(p3y - p0y)
            i = 0
            while i <= height:
                y = p0y + (ysign * i)
                xi00 = MathRound(p0x + _fdiv(y - p0y, kp0))
                xi01 = MathRound(p1x + _fdiv(y - p1y, kp1))
                xi02 = MathRound(p2x + _fdiv(y - p2y, kp1))
                xi03 = MathRound(p3x + _fdiv(y - p3y, kp0))
                if xsign == 1:
                    xi0 = MathMax(xi00, xi01)
                    xi1 = MathMin(xi02, xi03)
                else:
                    xi0 = MathMin(xi00, xi01)
                    xi1 = MathMax(xi02, xi03)
                width = MathAbs(MathRound(xi1 - xi0))
                j = 0
                while j <= width:
                    xi = xi0 + (xsign * j)
                    dist = self.DistancePointSegment(xi, y, xe1, ye1, xe2, ye2)
                    val = MathAbs(_fdiv(dist, r))
                    self.PixelTransform(_int(xi), _int(y), clr, self.FilterFunction(val))
                    j += 1
                i += 1
        else:
            yi0 = 0.0
            yi1 = 0.0
            width = MathAbs(p2x - p1x)
            i = 0
            while i <= width:
                x = p1x + (xsign * i)
                yi00 = MathRound(p0y + ((x - p0x) * kp0))
                yi01 = MathRound(p1y + ((x - p1x) * kp1))
                yi02 = MathRound(p2y + ((x - p2x) * kp1))
                yi03 = MathRound(p3y + ((x - p3x) * kp0))
                if ysign == 1:
                    yi0 = MathMax(yi00, yi02)
                    yi1 = MathMin(yi01, yi03)
                else:
                    yi0 = MathMin(yi00, yi02)
                    yi1 = MathMax(yi01, yi03)
                height = MathAbs(yi1 - yi0)
                j = 0
                while j <= height:
                    yi = yi0 + (ysign * j)
                    dist = self.DistancePointSegment(x, yi, xe1, ye1, xe2, ye2)
                    val = MathAbs(_fdiv(dist, r))
                    self.PixelTransform(_int(x), _int(yi), clr, self.FilterFunction(val))
                    j += 1
                i += 1
    def DistancePointSegment(self, px, py, x1, y1, x2, y2):
        a = ((px - x1) * (px - x1)) + ((py - y1) * (py - y1))
        b = ((px - x2) * (px - x2)) + ((py - y2) * (py - y2))
        c = ((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1))
        if a >= (b + c):
            return MathSqrt(b)
        if b >= (a + c):
            return MathSqrt(a)
        a = MathSqrt(a)
        b = MathSqrt(b)
        c = MathSqrt(c)
        p = (a + b + c) / 2
        s = MathSqrt((p - a) * (p - b) * (p - c) * p)
        if MathIsValidNumber(s):
            return _fdiv(s * 2.0, c)
        else:
            return 0.0
    def AngleCalc(self, x1, y1, x2, y2):
        fi = 0.0
        if x1 == x2:
            if y1 == y2:
                return EMPTY_VALUE
            fi = (M_PI_2 if (y2 < y1) else (3 * M_PI_2))
        else:
            fi = atan(_fdiv(float(y1 - y2), x2 - x1))
            if x2 < x1:
                fi += M_PI
            else:
                if fi < 0:
                    fi += 2 * M_PI
        return fi
    def PointClassify(self, p0, p1, p2):
        return ((p1.x - p0.x) * (p2.y - p0.y)) - ((p2.x - p0.x) * (p1.y - p0.y))
    def PolygonClassify(self, p):
        total = ArraySize(p)
        im = 0
        xm = p[0].x
        ym = p[0].y
        for i in range(1, total):
            if p[i].y > ym:
                continue
            if p[i].y == ym and p[i].x > xm:
                continue
            im = i
            xm = p[i].x
            ym = p[i].y
        return self.PointClassify(p[_imod(im - 1 + total, total)], p[im], p[_imod(im + 1, total)])
    def IsPolygonConvex(self, p):
        total = ArraySize(p)
        if total == 3:
            return True
        res = (-1 if (self.PointClassify(p[0], p[1], p[2]) < 0) else 1)
        for i in range(1, total):
            res1 = (-1 if (self.PointClassify(p[i], p[_imod(i + 1, total)], p[_imod(i + 2, total)]) < 0) else 1)
            if res != res1:
                return False
        return True
    def PolygonNormalize(self, p):
        total = ArraySize(p)
        imin = 0
        xmin = p[0].x
        ymin = p[0].y
        for i in range(1, total):
            if p[i].y > ymin:
                continue
            if p[i].y == ymin:
                if p[i].x < xmin:
                    xmin = p[i].x
                    imin = i
                continue
            xmin = p[i].x
            ymin = p[i].y
            imin = i
        if imin == 0:
            return
        for i in range(0, imin):
            tmp = _copy(p[0])
            ArrayCopy(p, p, 0, 1)
            _assign(p[total - 1], tmp)
    def PolygonIntersect(self, p, add):
        total = ArraySize(p)
        res = (-1 if (self.PolygonClassify(p) < 0) else 1)
        for i in range(0, total):
            rr = (-1 if (self.PointClassify(p[i], p[_imod(i + 1, total)], p[_imod(i + 2, total)]) < 0) else 1)
            rl = (-1 if (self.PointClassify(p[_imod(total - i - 2, total)], p[_imod(total - i - 1, total)], p[_imod(total - i, total)]) < 0) else 1)
            if rl != res or rr != res:
                res = total - i - 1 - (i + 1)
                if res < 0:
                    return
                if res < 2:
                    ArrayResize(add, total - i)
                    _assign(add[0], p[0])
                    ArrayCopy(add, p, 1, i + 1, total - i - 1)
                    ArrayResize(p, i + 2)
                else:
                    ArrayResize(add, res + 1)
                    ArrayCopy(add, p, 0, i + 1, res + 1)
                    ArrayCopy(p, p, i + 2, i + res + 1, total - res - i - 1)
                    ArrayResize(p, total - res + 1)
                break
    def PolygonFill(self, p, clr):
        il = 0
        ir = 0
        xl = 0.0
        xr = 0.0
        yy = 0
        dl = 0.0
        dr = 0.0
        total = ArraySize(p)
        if total < 3:
            return
        while not self.IsPolygonConvex(p):
            add = Arr(0, 0, factory=CPoint)
            self.PolygonIntersect(p, add)
            self.PolygonNormalize(add)
            self.PolygonFill(add, clr)
            ArrayFree(add)
        total = ArraySize(p)
        ir = 0
        il = ir
        xr = p[0].x
        xl = xr
        yy = p[0].y
        if yy == p[1].y:
            xr = p[(ir := 1)].x
        self.LineHorizontal(_int(MathCeil(xl)), _int(MathFloor(xr)), yy, clr)
        while True:
            while yy == p[il].y:
                il = _imod(il - 1 + total, total)
                if yy > p[il].y:
                    return
                if yy != p[il].y:
                    dl = _fdiv(p[il].x - xl, p[il].y - yy)
                    self.LineHorizontal(_int(MathCeil(xl + (dl / 2))), _int(MathFloor(xl)), yy, clr)
                    xl += dl / 2
                else:
                    self.LineHorizontal(_int(MathCeil(xl)), _int(MathFloor(p[il].x)), yy, clr)
            while yy == p[ir].y:
                ir = _imod(ir + 1, total)
                if yy > p[ir].y:
                    return
                if yy != p[ir].y:
                    dr = _fdiv(p[ir].x - xr, p[ir].y - yy)
                    self.LineHorizontal(_int(MathCeil(xr)), _int(MathFloor(xr + (dr / 2))), yy, clr)
                    xr += dr / 2
                else:
                    self.LineHorizontal(_int(MathCeil(p[ir].x)), _int(MathFloor(xr)), yy, clr)
            yy += 1
            if yy == p[il].y:
                xl = p[il].x
            else:
                xl += dl
            if yy == p[ir].y:
                xr = p[ir].x
            else:
                xr += dr
            self.LineHorizontal(_int(MathCeil(xl)), _int(MathFloor(xr)), yy, clr)
            if not (il >= ir and ir != 0):
                break
    def CalcCurveBezierEndp(self, xend, yend, xadj, yadj, tension, x, y):
        x.v = (tension * (xadj - xend)) + xend
        y.v = (tension * (yadj - yend)) + yend
    def CalcCurveBezier(self, x, y, i, tension, x1, y1, x2, y2):
        xdiff = 0.0
        ydiff = 0.0
        xdiff = x[i + 2] - x[i]
        ydiff = y[i + 2] - y[i]
        x1.v = x[i + 1] - (tension * xdiff)
        y1.v = y[i + 1] - (tension * ydiff)
        x2.v = x[i + 1] + (tension * xdiff)
        y2.v = y[i + 1] + (tension * ydiff)
    def CalcBezierX(self, t, x0, x1, x2, x3):
        return (x0 * ((1 - t) * (1 - t) * (1 - t))) + (x1 * 3 * t * ((1 - t) * (1 - t))) + (x2 * 3 * (t * t) * (1 - t)) + (x3 * (t * t * t))
    def CalcBezierY(self, t, y0, y1, y2, y3):
        return (y0 * ((1 - t) * (1 - t) * (1 - t))) + (y1 * 3 * t * ((1 - t) * (1 - t))) + (y2 * 3 * (t * t) * (1 - t)) + (y3 * (t * t * t))
    def FilterFunction(self, x):
        if x <= 0.8:
            return 1.0
        else:
            return MathExp((-(x - 0.8)) * (x - 0.8) * 50)
CCanvas.m_default_colors = Arr.of([((0xFF000000 | (_uchar(0) << 16)) | (_uchar(0) << 8)) | _uchar(255), ((0xFF000000 | (_uchar(255) << 16)) | (_uchar(0) << 8)) | _uchar(0), ((0xFF000000 | (_uchar(0) << 16)) | (_uchar(128) << 8)) | _uchar(0), ((0xFF000000 | (_uchar(255) << 16)) | (_uchar(242) << 8)) | _uchar(0), ((0xFF000000 | (_uchar(255) << 16)) | (_uchar(0) << 8)) | _uchar(128), ((0xFF000000 | (_uchar(0) << 16)) | (_uchar(255) << 8)) | _uchar(0), ((0xFF000000 | (_uchar(185) << 16)) | (_uchar(0) << 8)) | _uchar(61), ((0xFF000000 | (_uchar(0) << 16)) | (_uchar(183) << 8)) | _uchar(239), ((0xFF000000 | (_uchar(255) << 16)) | (_uchar(128) << 8)) | _uchar(0)], fill=0, dyn=False, size=9)

class CGraphic(MqlObject):
    _q_fields = ('m_arr_curves', 'm_canvas', 'm_height', 'm_width', 'm_left', 'm_right', 'm_up', 'm_down', 'm_left0', 'm_right0', 'm_up0', 'm_down0', 'm_mark_size', 'm_dx', 'm_dy', 'm_x', 'm_y', 'm_grid', 'm_background', 'm_history', 'm_generator', 'm_gap', 'm_xc', 'm_yc', 'm_xvalues', 'm_yvalues', 'm_xsize', 'm_ysize', 'm_xupdate', 'm_yupdate')
    def __init__(self):
        self.m_arr_curves = CArrayObj()
        self.m_canvas = CCanvas()
        self.m_height = 0
        self.m_width = 0
        self.m_left = 0
        self.m_right = 0
        self.m_up = 0
        self.m_down = 0
        self.m_left0 = 0
        self.m_right0 = 0
        self.m_up0 = 0
        self.m_down0 = 0
        self.m_mark_size = 0
        self.m_dx = 0.0
        self.m_dy = 0.0
        self.m_x = CAxis()
        self.m_y = CAxis()
        self.m_grid = CGrid()
        self.m_background = CBackground()
        self.m_history = CCurveHistory()
        self.m_generator = CColorGenerator()
        self.m_gap = 0
        self.m_xc = Arr(0, 0)
        self.m_yc = Arr(0, 0)
        self.m_xvalues = Arr(0, "")
        self.m_yvalues = Arr(0, "")
        self.m_xsize = 0
        self.m_ysize = 0
        self.m_xupdate = False
        self.m_yupdate = False
        self.m_height = _int(0.0)
        self.m_width = _int(0.0)
        self.SetDefaultParameters()
    def _q_dtor(self):
        pass
    def Width(self):
        return self.m_width
    def Height(self):
        return self.m_height
    def IndentUp_0(self):
        return self.m_up0
    def IndentUp_1(self, up):
        self.m_up0 = up
    def IndentDown_0(self):
        return self.m_down0
    def IndentDown_1(self, down):
        self.m_down0 = down
    def IndentLeft_0(self):
        return self.m_left0
    def IndentLeft_1(self, left):
        self.m_left0 = left
    def IndentRight_0(self):
        return self.m_right0
    def IndentRight_1(self, right):
        self.m_right0 = right
    def GapSize_0(self):
        return self.m_gap
    def GapSize_1(self, size):
        self.m_gap = size
    def MajorMarkSize_0(self):
        return self.m_mark_size
    def MajorMarkSize_1(self, size):
        self.m_mark_size = size
    def XAxis(self):
        return self.m_x
    def YAxis(self):
        return self.m_y
    def HistoryNameWidth_0(self):
        return self.m_history.name_width
    def HistoryNameWidth_1(self, width):
        self.m_history.name_width = width
    def HistoryNameSize_0(self):
        return self.m_history.name_size
    def HistoryNameSize_1(self, size):
        self.m_history.name_size = size
    def HistorySymbolSize_0(self):
        return self.m_history.symbol_size
    def HistorySymbolSize_1(self, size):
        self.m_history.symbol_size = size
    def HistoryColor_0(self):
        return self.m_history.clr
    def HistoryColor_1(self, clr):
        self.m_history.clr = clr
    def GridLineColor_0(self):
        return self.m_grid.clr_line
    def GridLineColor_1(self, clr):
        self.m_grid.clr_line = clr
    def GridAxisLineColor_0(self):
        return self.m_grid.clr_axis_line
    def GridAxisLineColor_1(self, clr):
        self.m_grid.clr_axis_line = clr
    def GridBackgroundColor_0(self):
        return self.m_grid.clr_background
    def GridBackgroundColor_1(self, clr):
        self.m_grid.clr_background = clr
    def GridCircleRadius_0(self):
        return self.m_grid.r_circle
    def GridCircleRadius_1(self, r):
        self.m_grid.r_circle = r
    def GridCircleColor_0(self):
        return self.m_grid.clr_circle
    def GridCircleColor_1(self, clr):
        self.m_grid.clr_circle = clr
    def GridHasCircle_0(self):
        return self.m_grid.has_circle
    def GridHasCircle_1(self, has):
        self.m_grid.has_circle = has
    def BackgroundColor_0(self):
        return self.m_background.clr
    def BackgroundColor_1(self, clr):
        self.m_background.clr = clr
    def BackgroundMainColor_0(self):
        return self.m_background.clr_main
    def BackgroundMainColor_1(self, clr):
        self.m_background.clr_main = clr
    def BackgroundSubColor_0(self):
        return self.m_background.clr_sub
    def BackgroundSubColor_1(self, clr):
        self.m_background.clr_sub = clr
    def BackgroundMain_0(self):
        return self.m_background.main
    def BackgroundMain_1(self, main):
        self.m_background.main = main
    def BackgroundSub_0(self):
        return self.m_background.sub
    def BackgroundSub_1(self, sub):
        self.m_background.sub = sub
    def BackgroundMainSize_0(self):
        return self.m_background.size_main
    def BackgroundMainSize_1(self, size):
        self.m_background.size_main = size
    def BackgroundSubSize_0(self):
        return self.m_background.size_sub
    def BackgroundSubSize_1(self, size):
        self.m_background.size_sub = size
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if ObjectFind(chart, name) >= 0:
            return False
        width = x2 - x1
        height = y2 - y1
        if width > 0 and height > 0:
            self.m_width = width
            self.m_height = height
            if not ObjectCreate(chart, name, OBJ_BITMAP_LABEL, subwin, 0, 0):
                return False
            if (not ObjectSetInteger(chart, name, OBJPROP_XDISTANCE, x1)) or (not ObjectSetInteger(chart, name, OBJPROP_YDISTANCE, y1)):
                ObjectDelete(chart, name)
                return False
            if not self.m_canvas.Attach_5(chart, name, width, height):
                ObjectDelete(chart, name)
                return False
        return True
    def Attach_2(self, chart_id, objname):
        if self.m_canvas.Attach_3(chart_id, objname):
            self.m_width = self.m_canvas.Width()
            self.m_height = self.m_canvas.Height()
            return True
        return False
    def Attach_4(self, chart_id, objname, width, height):
        if self.m_canvas.Attach_5(chart_id, objname, width, height):
            self.m_width = self.m_canvas.Width()
            self.m_height = self.m_canvas.Height()
            return True
        return False
    def Destroy(self):
        self.SetDefaultParameters()
        self.m_generator.Reset()
        self.m_canvas.Destroy()
    def ChartObjectName(self):
        return self.m_canvas.ChartObjectName()
    def ResourceName(self):
        return self.m_canvas.ResourceName()
    def Redraw(self, rescale=False):
        self.ResetParameters()
        self.CalculateBoundaries()
        if rescale:
            self.CalculateMaxMinValues()
        if self.m_xupdate:
            self.CalculateXAxis()
        if self.m_yupdate:
            self.CalculateYAxis()
        self.CreateWorkspace()
        self.CreateGrid()
        i = 0
        while i < self.m_arr_curves.Total():
            curve = self.m_arr_curves.At(i)
            if CheckPointer(curve) != POINTER_DYNAMIC:
                return False
            if not curve.Visible_0():
                i += 1
                continue
            _sw7 = curve.Type_0()
            if _sw7 == CURVE_CUSTOM:
                self.CustomPlot(curve)
            elif _sw7 == CURVE_POINTS:
                self.PointsPlot(curve)
            elif _sw7 == CURVE_LINES:
                self.LinesPlot(curve)
            elif _sw7 == CURVE_POINTS_AND_LINES:
                self.PointsAndLinesPlot(curve)
            elif _sw7 == CURVE_STEPS:
                self.StepsPlot(curve)
            elif _sw7 == CURVE_HISTOGRAM:
                self.HistogramPlot(curve)
            elif _sw7 == CURVE_NONE:
                pass
            if curve.TrendLineVisible_0():
                self.TrendLinePlot(curve)
            i += 1
        self.CreateBackground()
        self.CreateXName()
        self.CreateYName()
        self.CreateAxes()
        self.CreateHistory()
        return True
    def Update(self, redraw=True):
        self.m_canvas.Update(redraw)
    def CurveAdd_1(self, y, type_, name=None):
        return self.CurveAdd_6(y, self.m_generator.Next(), type_, name)
    def CurveAdd_2(self, x, y, type_, name=None):
        return self.CurveAdd_5(x, y, self.m_generator.Next(), type_, name)
    def CurveAdd_3(self, points, type_, name=None):
        return self.CurveAdd_7(points, self.m_generator.Next(), type_, name)
    def CurveAdd_6(self, function, from_, to, step, type_, name=None):
        return self.CurveAdd_7(function, from_, to, step, self.m_generator.Next(), type_, name)
    def CurveAdd_5(self, x, y, clr, type_, name=None):
        xSize = ArraySize(x)
        ySize = ArraySize(y)
        if xSize != ySize:
            return None
        curve = CCurve(x, y, clr, type_, name)
        if self.m_arr_curves.Total() == 0:
            if self.m_x.AutoScale_0():
                self.m_x.Max_1(curve.XMax())
                self.m_x.Min_1(curve.XMin())
            if self.m_y.AutoScale_0():
                self.m_y.Max_1(curve.YMax())
                self.m_y.Min_1(curve.YMin())
            self.m_xupdate = True
            self.m_yupdate = True
        else:
            if self.m_x.Max_0() < curve.XMax() and self.m_x.AutoScale_0():
                self.m_x.Max_1(curve.XMax())
                self.m_xupdate = True
            if self.m_x.Min_0() > curve.XMin() and self.m_x.AutoScale_0():
                self.m_x.Min_1(curve.XMin())
                self.m_xupdate = True
            if self.m_y.Max_0() < curve.YMax() and self.m_y.AutoScale_0():
                self.m_y.Max_1(curve.YMax())
                self.m_yupdate = True
            if self.m_y.Min_0() > curve.YMin() and self.m_y.AutoScale_0():
                self.m_y.Min_1(curve.YMin())
                self.m_yupdate = True
        self.m_arr_curves.Add(curve)
        return curve
    def CurveAdd_6(self, y, clr, type_, name=None):
        curve = CCurve(y, clr, type_, name)
        if self.m_arr_curves.Total() == 0:
            if self.m_x.AutoScale_0():
                self.m_x.Max_1(curve.XMax())
                self.m_x.Min_1(curve.XMin())
            if self.m_y.AutoScale_0():
                self.m_y.Max_1(curve.YMax())
                self.m_y.Min_1(curve.YMin())
            self.m_xupdate = True
            self.m_yupdate = True
        else:
            if self.m_x.Max_0() < curve.XMax() and self.m_x.AutoScale_0():
                self.m_x.Max_1(curve.XMax())
                self.m_xupdate = True
            if self.m_x.Min_0() > curve.XMin() and self.m_x.AutoScale_0():
                self.m_x.Min_1(curve.XMin())
                self.m_xupdate = True
            if self.m_y.Max_0() < curve.YMax() and self.m_y.AutoScale_0():
                self.m_y.Max_1(curve.YMax())
                self.m_yupdate = True
            if self.m_y.Min_0() > curve.YMin() and self.m_y.AutoScale_0():
                self.m_y.Min_1(curve.YMin())
                self.m_yupdate = True
        self.m_arr_curves.Add(curve)
        return curve
    def CurveAdd_7(self, points, clr, type_, name=None):
        curve = CCurve(points, clr, type_, name)
        if self.m_arr_curves.Total() == 0:
            if self.m_x.AutoScale_0():
                self.m_x.Max_1(curve.XMax())
                self.m_x.Min_1(curve.XMin())
            if self.m_y.AutoScale_0():
                self.m_y.Max_1(curve.YMax())
                self.m_y.Min_1(curve.YMin())
            self.m_xupdate = True
            self.m_yupdate = True
        else:
            if self.m_x.Max_0() < curve.XMax() and self.m_x.AutoScale_0():
                self.m_x.Max_1(curve.XMax())
                self.m_xupdate = True
            if self.m_x.Min_0() > curve.XMin() and self.m_x.AutoScale_0():
                self.m_x.Min_1(curve.XMin())
                self.m_xupdate = True
            if self.m_y.Max_0() < curve.YMax() and self.m_y.AutoScale_0():
                self.m_y.Max_1(curve.YMax())
                self.m_yupdate = True
            if self.m_y.Min_0() > curve.YMin() and self.m_y.AutoScale_0():
                self.m_y.Min_1(curve.YMin())
                self.m_yupdate = True
        self.m_arr_curves.Add(curve)
        return curve
    def CurveAdd_7(self, function, from_, to, step, clr, type_, name=None):
        if (from_ >= to or step <= 0) or step >= MathAbs(to - from_):
            return None
        curve = CCurve(function, from_, to, step, clr, type_, name)
        if self.m_arr_curves.Total() == 0:
            if self.m_x.AutoScale_0():
                self.m_x.Max_1(curve.XMax())
                self.m_x.Min_1(curve.XMin())
            if self.m_y.AutoScale_0():
                self.m_y.Max_1(curve.YMax())
                self.m_y.Min_1(curve.YMin())
            self.m_xupdate = True
            self.m_yupdate = True
        else:
            if self.m_x.Max_0() < curve.XMax() and self.m_x.AutoScale_0():
                self.m_x.Max_1(curve.XMax())
                self.m_xupdate = True
            if self.m_x.Min_0() > curve.XMin() and self.m_x.AutoScale_0():
                self.m_x.Min_1(curve.XMin())
                self.m_xupdate = True
            if self.m_y.Max_0() < curve.YMax() and self.m_y.AutoScale_0():
                self.m_y.Max_1(curve.YMax())
                self.m_yupdate = True
            if self.m_y.Min_0() > curve.YMin() and self.m_y.AutoScale_0():
                self.m_y.Min_1(curve.YMin())
                self.m_yupdate = True
        self.m_arr_curves.Add(curve)
        return curve
    def CurvePlotAll(self):
        self.ResetParameters()
        self.CalculateBoundaries()
        if self.m_xupdate:
            self.CalculateXAxis()
        if self.m_yupdate:
            self.CalculateYAxis()
        self.CreateWorkspace()
        self.CreateGrid()
        i = 0
        while i < self.m_arr_curves.Total():
            curve = self.m_arr_curves.At(i)
            if not CheckPointer(curve):
                return False
            curve.Visible_1(True)
            _sw8 = curve.Type_0()
            if _sw8 == CURVE_CUSTOM:
                self.CustomPlot(curve)
            elif _sw8 == CURVE_POINTS:
                self.PointsPlot(curve)
            elif _sw8 == CURVE_LINES:
                self.LinesPlot(curve)
            elif _sw8 == CURVE_POINTS_AND_LINES:
                self.PointsAndLinesPlot(curve)
            elif _sw8 == CURVE_STEPS:
                self.StepsPlot(curve)
            elif _sw8 == CURVE_HISTOGRAM:
                self.HistogramPlot(curve)
            elif _sw8 == CURVE_NONE:
                pass
            if curve.TrendLineVisible_0():
                self.TrendLinePlot(curve)
            i += 1
        self.CreateBackground()
        self.CreateXName()
        self.CreateYName()
        self.CreateAxes()
        self.CreateHistory()
        return True
    def CurvePlot(self, index):
        curve = self.m_arr_curves.At(index)
        if CheckPointer(curve) == POINTER_DYNAMIC:
            curve.Visible_1(True)
        else:
            return False
        self.ResetParameters()
        self.CalculateBoundaries()
        if self.m_xupdate:
            self.CalculateXAxis()
        if self.m_yupdate:
            self.CalculateYAxis()
        self.CreateWorkspace()
        self.CreateGrid()
        i = 0
        while i < self.m_arr_curves.Total():
            curve = self.m_arr_curves.At(i)
            if CheckPointer(curve) != POINTER_DYNAMIC:
                return False
            if not curve.Visible_0():
                i += 1
                continue
            _sw9 = curve.Type_0()
            if _sw9 == CURVE_CUSTOM:
                self.CustomPlot(curve)
            elif _sw9 == CURVE_POINTS:
                self.PointsPlot(curve)
            elif _sw9 == CURVE_LINES:
                self.LinesPlot(curve)
            elif _sw9 == CURVE_POINTS_AND_LINES:
                self.PointsAndLinesPlot(curve)
            elif _sw9 == CURVE_STEPS:
                self.StepsPlot(curve)
            elif _sw9 == CURVE_HISTOGRAM:
                self.HistogramPlot(curve)
            elif _sw9 == CURVE_NONE:
                pass
            if curve.TrendLineVisible_0():
                self.TrendLinePlot(curve)
            i += 1
        self.CreateBackground()
        self.CreateXName()
        self.CreateYName()
        self.CreateAxes()
        self.CreateHistory()
        return True
    def CurvesTotal(self):
        return self.m_arr_curves.Total()
    def CurveGetByIndex(self, index):
        return self.m_arr_curves.At(index)
    def CurveGetByName(self, name):
        i = 0
        while i < self.m_arr_curves.Total():
            curve = self.m_arr_curves.At(i)
            if curve.Name_0() == name:
                return curve
            i += 1
        return None
    def CurveRemoveByIndex(self, index):
        curve = self.m_arr_curves.Detach(index)
        if CheckPointer(curve) == POINTER_DYNAMIC:
            _delete(curve)
            return True
        else:
            return False
    def CurveRemoveByName(self, name):
        i = 0
        while i < self.m_arr_curves.Total():
            curve = self.m_arr_curves.At(i)
            if curve.Name_0() == name:
                if CheckPointer(curve) == POINTER_DYNAMIC:
                    _delete(self.m_arr_curves.Detach(i))
                    return True
                else:
                    return False
            i += 1
        return False
    def MarksToAxisAdd(self, marks, mark_size, position, dimension=0):
        originalX = self.m_left
        originalY = self.m_height - self.m_down
        if dimension == 0:
            y1 = self.m_height - self.m_down
            y2 = self.m_height - self.m_down
            _sw10 = position
            if _sw10 == MARK_INTERNAL:
                y1 -= mark_size
            elif _sw10 == MARK_EXTERNAL:
                y2 += mark_size
            elif _sw10 == MARK_MIDDLE:
                y1 -= _idiv(mark_size, 2)
                y2 += _idiv(mark_size, 2)
            i = 0
            while i < ArraySize(marks):
                x = originalX + _int((marks[i] - self.m_x.Min_0()) * self.m_dx)
                self.m_canvas.LineVertical(x, y1, y2, ColorToARGB(clrBlack))
                i += 1
        elif dimension == 1:
            x1 = self.m_left
            x2 = self.m_left
            _sw11 = position
            if _sw11 == MARK_INTERNAL:
                x2 += mark_size
            elif _sw11 == MARK_EXTERNAL:
                x1 -= mark_size
            elif _sw11 == MARK_MIDDLE:
                x2 += _idiv(mark_size, 2)
                x1 -= _idiv(mark_size, 2)
            i = 0
            while i < ArraySize(marks):
                y = originalY - _int((marks[i] - self.m_y.Min_0()) * self.m_dy)
                self.m_canvas.LineHorizontal(x1, x2, y, ColorToARGB(clrBlack))
                i += 1
        else:
            return False
        return True
    def TextAdd_5(self, x, y, text, clr, alignment=0):
        if StringLen(text) < 1:
            return
        self.m_canvas.TextOut(x, y, text, clr, alignment)
    def TextAdd_4(self, point, text, clr, alignment=0):
        if StringLen(text) < 1:
            return
        self.m_canvas.TextOut(point.x, point.y, text, clr, alignment)
    def LineAdd_6(self, x1, y1, x2, y2, clr, style):
        self.m_canvas.LineWu(x1, y1, x2, y2, clr, style)
    def LineAdd_4(self, point1, point2, clr, style):
        self.m_canvas.LineWu(point1.x, point1.y, point2.x, point2.y, clr, style)
    def FontSet(self, name, size, flags=0, angle=0):
        return self.m_canvas.FontSet_4(name, size, flags, angle)
    def FontGet(self, name, size, flags, angle):
        self.m_canvas.FontGet(name, size, flags, angle)
    def ScaleX(self, x):
        xc = self.m_left + _int((x - self.m_x.Min_0()) * self.m_dx)
        return xc
    def ScaleY(self, y):
        yc = self.m_height - self.m_down - _int((y - self.m_y.Min_0()) * self.m_dy)
        return yc
    def SetDefaultParameters(self):
        self.m_xupdate = False
        self.m_yupdate = False
        self.m_xsize = 0
        self.m_ysize = 0
        self.m_left0 = 0
        self.m_right0 = 5
        self.m_up0 = 5
        self.m_down0 = 0
        self.m_mark_size = 3
        self.m_gap = 4
        self.m_history.name_width = 60
        self.m_history.symbol_size = 12
        self.m_history.name_size = 12
        self.m_history.count_points = 0
        self.m_history.count_lines = 0
        self.m_history.count_histogram = 0
        self.m_history.count_custom = 0
        self.m_x.Name_1("")
        self.m_y.Name_1("")
        self.m_grid.clr_line = clrWhiteSmoke
        self.m_grid.clr_axis_line = clrSilver
        self.m_grid.clr_frame = clrBlack
        self.m_grid.clr_background = clrWhite
        self.m_grid.r_circle = 0
        self.m_grid.clr_circle = clrWhite
        self.m_grid.has_circle = False
        self.m_background.clr = clrWhite
        self.m_background.clr_main = clrBlack
        self.m_background.clr_sub = clrBlack
        self.m_background.main = ""
        self.m_background.sub = ""
        self.m_background.size_main = 0
        self.m_background.size_sub = 0
    def ResetParameters(self):
        self.m_left = self.m_left0
        self.m_right = self.m_right0
        self.m_up = self.m_up0
        self.m_down = self.m_down0
        self.m_history.count_total = 0
    def CalculateMaxMinValues(self):
        size = self.m_arr_curves.Total()
        xmax = 0.0
        xmin = 0.0
        ymax = 0.0
        ymin = 0.0
        if size > 0:
            valid = False
            for i in range(0, size):
                curve = self.m_arr_curves.At(i)
                if CheckPointer(curve) == POINTER_DYNAMIC:
                    if not valid:
                        xmax = curve.XMax()
                        xmin = curve.XMin()
                        ymax = curve.YMax()
                        ymin = curve.YMin()
                        valid = True
                    else:
                        if xmax < curve.XMax():
                            xmax = curve.XMax()
                        if xmin > curve.XMin():
                            xmin = curve.XMin()
                        if ymax < curve.YMax():
                            ymax = curve.YMax()
                        if ymin > curve.YMin():
                            ymin = curve.YMin()
        if self.m_x.AutoScale_0():
            self.m_x.Max_1(xmax)
            self.m_x.Min_1(xmin)
        if self.m_y.AutoScale_0():
            self.m_y.Max_1(ymax)
            self.m_y.Min_1(ymin)
        self.m_xupdate = True
        self.m_yupdate = True
    def CustomPlot(self, curve):
        size = curve.Size()
        x = Arr(0, 0.0)
        y = Arr(0, 0.0)
        curve.GetX(x)
        curve.GetY(y)
        if ArraySize(x) == 0 or ArraySize(y) == 0:
            return
        plot = curve.CustomPlotFunction_0()
        if plot is None:
            return
        graphic = self
        canvas = self.m_canvas
        cbdata = curve.CustomPlotCBData_0()
        plot(x, y, size, graphic, canvas, cbdata)
    def PointsPlot(self, curve):
        size = curve.Size()
        x = Arr(0, 0.0)
        y = Arr(0, 0.0)
        curve.GetX(x)
        curve.GetY(y)
        if ArraySize(x) == 0 or ArraySize(y) == 0:
            return
        if curve.PointsSize_0() == 0:
            return
        clr0 = curve.Color_0()
        clr1 = curve.PointsColor_0()
        for i in range(0, size):
            if (not MathIsValidNumber(x[i])) or (not MathIsValidNumber(y[i])):
                continue
            xc = self.ScaleX(x[i])
            yc = self.ScaleY(y[i])
            r = _idiv(curve.PointsSize_0(), 2)
            if r > 0:
                _sw12 = curve.PointsType_0()
                if _sw12 == POINT_CIRCLE:
                    if curve.PointsFill_0():
                        self.m_canvas.FillCircle(xc, yc, r, clr1)
                    self.m_canvas.CircleWu(xc, yc, r, clr0)
                elif _sw12 == POINT_SQUARE:
                    self.m_canvas.Rectangle(xc - r, yc - r, xc + r, yc + r, clr0)
                    if curve.PointsFill_0():
                        self.m_canvas.FillRectangle(xc - r + 1, yc - r + 1, xc + r - 1, yc + r - 1, clr1)
                elif _sw12 == POINT_DIAMOND:
                    xc1 = xc + 1 - r
                    yc1 = yc
                    xc2 = xc
                    yc2 = yc + 1 - r
                    self.m_canvas.Line(xc - r, yc, xc, yc - r, clr0)
                    self.m_canvas.Line(xc, yc - r, xc + r, yc, clr0)
                    self.m_canvas.Line(xc + r, yc, xc, yc + r, clr0)
                    self.m_canvas.Line(xc, yc + r, xc - r, yc, clr0)
                    if curve.PointsFill_0():
                        count = ((curve.PointsSize_0() - 1) if (_imod(curve.PointsSize_0(), 2) == 0) else (curve.PointsSize_0() - 2))
                        for j in range(0, count):
                            self.m_canvas.Line(xc1, yc1, xc2, yc2, clr1)
                            if _imod(j, 2) == 0:
                                yc2 += 1
                                xc1 += 1
                            else:
                                xc2 += 1
                                yc1 += 1
                elif _sw12 == POINT_TRIANGLE:
                    self.m_canvas.TriangleWu(xc, yc - r, xc - r, yc + r, xc + r, yc + r, clr0)
                    if curve.PointsFill_0():
                        dy = -r
                        dx = 0
                        count = ((curve.PointsSize_0() - 1) if (_imod(curve.PointsSize_0(), 2) == 0) else (curve.PointsSize_0() - 2))
                        j = 0
                        while j < count:
                            self.m_canvas.LineHorizontal(xc - dx + 1, xc + dx, yc + 1 + dy, clr1)
                            if _imod(j, 2) == 0:
                                dx += 1
                            j += 1
                            dy += 1
                elif _sw12 == POINT_TRIANGLE_DOWN:
                    self.m_canvas.TriangleWu(xc, yc + r, xc - r, yc - r, xc + r, yc - r, clr0)
                    if curve.PointsFill_0():
                        dy = r
                        dx = 0
                        count = ((curve.PointsSize_0() - 1) if (_imod(curve.PointsSize_0(), 2) == 0) else (curve.PointsSize_0() - 2))
                        j = 0
                        while j < count:
                            self.m_canvas.LineHorizontal(xc - dx + 1, xc + dx, yc - 1 + dy, clr1)
                            if _imod(j, 2) == 0:
                                dx += 1
                            j += 1
                            dy -= 1
                elif _sw12 == POINT_X_CROSS:
                    self.m_canvas.Line(xc + r, yc + r, xc - r, yc - r, clr0)
                    self.m_canvas.Line(xc - r, yc + r, xc + r, yc - r, clr0)
                elif _sw12 == POINT_PLUS:
                    self.m_canvas.LineHorizontal(xc + r + 1, xc - r, yc, clr0)
                    self.m_canvas.LineVertical(xc, yc + r, yc - r, clr0)
                elif _sw12 == POINT_STAR:
                    self.m_canvas.LineHorizontal(xc + r + 1, xc - r, yc, clr0)
                    self.m_canvas.LineVertical(xc, yc + r, yc - r, clr0)
                    self.m_canvas.Line(xc + r, yc + r, xc - r, yc - r, clr0)
                    self.m_canvas.Line(xc - r, yc + r, xc + r, yc - r, clr0)
                elif _sw12 == POINT_HORIZONTAL_DASH:
                    self.m_canvas.LineHorizontal(xc + r + 1, xc - r, yc, clr0)
                elif _sw12 == POINT_VERTICAL_DASH:
                    self.m_canvas.LineVertical(xc, yc + r, yc - r, clr0)
            else:
                self.m_canvas.PixelSet(xc, yc, clr0)
    def LinesPlot(self, curve):
        size = 0
        x = Arr(0, 0.0)
        y = Arr(0, 0.0)
        size = curve.Size()
        curve.GetX(x)
        curve.GetY(y)
        if ArraySize(x) == 0 or ArraySize(y) == 0:
            return
        xc = Arr(0, 0)
        yc = Arr(0, 0)
        discontinuity = Arr(0, 0)
        for i in range(0, size):
            if (not MathIsValidNumber(x[i])) or (not MathIsValidNumber(y[i])):
                ArrayResize(discontinuity, ArraySize(discontinuity) + 1, size)
                discontinuity[ArraySize(discontinuity) - 1] = i
        tension = curve.LinesSmoothTension_0()
        if ArraySize(discontinuity) == 0:
            ArrayResize(xc, size)
            ArrayResize(yc, size)
            for i in range(0, size):
                xc[i] = self.ScaleX(x[i])
                yc[i] = self.ScaleY(y[i])
            if ((curve.LinesSmooth_0() and size > 2) and tension > 0.0) and tension <= 1.0:
                self.m_canvas.PolylineSmooth(xc, yc, curve.Color_0(), curve.LinesWidth_0(), curve.LinesStyle_0(), curve.LinesEndStyle_0(), tension, curve.LinesSmoothStep_0())
            elif size > 1:
                self.m_canvas.PolylineThick(xc, yc, curve.Color_0(), curve.LinesWidth_0(), curve.LinesStyle_0(), curve.LinesEndStyle_0())
            elif size == 1:
                self.m_canvas.PixelSet(xc[0], yc[0], curve.Color_0())
        else:
            index = 0
            j = 0
            while j <= ArraySize(discontinuity):
                xj = Arr(0, 0.0)
                yj = Arr(0, 0.0)
                sizej = 0
                if j == 0:
                    sizej = discontinuity[0]
                    ArrayCopy(xj, x, 0, 0, sizej)
                    ArrayCopy(yj, y, 0, 0, sizej)
                elif j == ArraySize(discontinuity):
                    sizej = size - discontinuity[j - 1] - 1
                    ArrayCopy(xj, x, 0, discontinuity[j - 1] + 1, sizej)
                    ArrayCopy(yj, y, 0, discontinuity[j - 1] + 1, sizej)
                else:
                    sizej = discontinuity[j] - discontinuity[j - 1] - 1
                    ArrayCopy(xj, x, 0, discontinuity[j - 1] + 1, sizej)
                    ArrayCopy(yj, y, 0, discontinuity[j - 1] + 1, sizej)
                ArrayResize(xc, sizej, size)
                ArrayResize(yc, sizej, size)
                for i in range(0, sizej):
                    xc[i] = self.ScaleX(xj[i])
                    yc[i] = self.ScaleY(yj[i])
                    index += 1
                if ((curve.LinesSmooth_0() and size > 2) and tension > 0.0) and tension <= 1.0:
                    self.m_canvas.PolylineSmooth(xc, yc, curve.Color_0(), curve.LinesWidth_0(), curve.LinesStyle_0(), curve.LinesEndStyle_0(), tension, curve.LinesSmoothStep_0())
                elif sizej > 1:
                    self.m_canvas.PolylineThick(xc, yc, curve.Color_0(), curve.LinesWidth_0(), curve.LinesStyle_0(), curve.LinesEndStyle_0())
                elif sizej == 1:
                    self.m_canvas.PixelSet(xc[0], yc[0], curve.Color_0())
                j += 1
    def PointsAndLinesPlot(self, curve):
        self.LinesPlot(curve)
        self.PointsPlot(curve)
    def StepsPlot(self, curve):
        size = curve.Size()
        x = Arr(0, 0.0)
        y = Arr(0, 0.0)
        curve.GetX(x)
        curve.GetY(y)
        xc = Arr(0, 0)
        yc = Arr(0, 0)
        size = (size * 2) - 1
        ArrayResize(xc, size)
        ArrayResize(yc, size)
        index = 0
        if curve.StepsDimension_0() == 0:
            i = 0
            while i < (size - 1):
                xc[i] = self.ScaleX(x[index])
                xc[i + 1] = self.ScaleX(x[index + 1])
                yc[i] = self.ScaleY(y[index])
                yc[i + 1] = yc[i]
                i += 2
                index += 1
        elif curve.StepsDimension_0() == 1:
            i = 0
            while i < (size - 1):
                xc[i] = self.ScaleX(x[index])
                xc[i + 1] = xc[i]
                yc[i] = self.ScaleY(y[index])
                yc[i + 1] = self.ScaleY(y[index + 1])
                i += 2
                index += 1
        else:
            return
        xc[size - 1] = self.ScaleX(x[index])
        yc[size - 1] = self.ScaleY(y[index])
        self.m_canvas.PolylineWu(xc, yc, curve.Color_0(), curve.LinesStyle_0())
    def HistogramPlot(self, curve):
        size = curve.Size()
        x = Arr(0, 0.0)
        y = Arr(0, 0.0)
        histogram_width = curve.HistogramWidth_0()
        if histogram_width <= 0:
            return
        curve.GetX(x)
        curve.GetY(y)
        if ArraySize(x) == 0 or ArraySize(y) == 0:
            return
        originalY = self.m_height - self.m_down
        yc0 = self.ScaleY(0.0)
        clr = curve.Color_0()
        for i in range(0, size):
            if (not MathIsValidNumber(x[i])) or (not MathIsValidNumber(y[i])):
                continue
            xc = self.ScaleX(x[i])
            yc = self.ScaleY(y[i])
            xc1 = xc - _idiv(histogram_width, 2)
            xc2 = xc + _idiv(histogram_width, 2)
            yc1 = yc
            yc2 = (yc0 if (originalY > yc0 and yc0 > 0) else originalY)
            if yc1 > yc2:
                yc2 += 1
            else:
                yc2 -= 1
            self.m_canvas.FillRectangle(xc1, yc1, xc2, yc2, clr)
    def TrendLinePlot(self, curve):
        coeff = Arr(0, 0.0)
        curve.TrendLineCoefficients(coeff)
        x0 = curve.XMin()
        x1 = curve.XMax()
        y0 = (coeff[0] * x0) + coeff[1]
        y1 = (coeff[0] * x1) + coeff[1]
        xc0 = self.ScaleX(x0)
        xc1 = self.ScaleX(x1)
        yc0 = self.ScaleY(y0)
        yc1 = self.ScaleY(y1)
        clr = curve.Color_0()
        self.m_canvas.LineWu(xc0, yc0, xc1, yc1, curve.TrendLineColor_0())
    def CreateWorkspace(self):
        x1 = self.m_left
        y1 = self.m_up
        x2 = self.m_width - self.m_right
        y2 = self.m_height - self.m_down
        self.m_canvas.FillRectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, self.m_grid.clr_background)
    def CreateGrid(self):
        xc0 = _int(-1.0)
        yc0 = _int(-1.0)
        i = 1
        while i < (self.m_ysize - 1):
            if StringToDouble(self.m_yvalues[i]) == 0.0:
                yc0 = self.m_yc[i]
            else:
                self.m_canvas.LineHorizontal(self.m_left + 1, self.m_width - self.m_right, self.m_yc[i], self.m_grid.clr_line)
            j = 1
            while j < (self.m_xsize - 1):
                if i == 1:
                    if StringToDouble(self.m_xvalues[j]) == 0.0:
                        xc0 = self.m_xc[j]
                    else:
                        self.m_canvas.LineVertical(self.m_xc[j], self.m_height - self.m_down - 1, self.m_up + 1, self.m_grid.clr_line)
                if self.m_grid.has_circle:
                    self.m_canvas.FillCircle(self.m_xc[j], self.m_yc[i], self.m_grid.r_circle, self.m_grid.clr_circle)
                    self.m_canvas.CircleWu(self.m_xc[j], self.m_yc[i], self.m_grid.r_circle, self.m_grid.clr_circle)
                j += 1
            i += 1
        if yc0 > 0:
            self.m_canvas.LineHorizontal(self.m_left + 1, self.m_width - self.m_right, yc0, self.m_grid.clr_axis_line)
        if xc0 > 0:
            self.m_canvas.LineVertical(xc0, self.m_height - self.m_down - 1, self.m_up + 1, self.m_grid.clr_axis_line)
    def CreateBackground(self):
        x1 = 0
        y1 = 0
        x2 = self.m_width
        y2 = self.m_height
        self.m_canvas.FillRectangle(0, 0, self.m_width, self.m_up - 1, self.m_background.clr)
        self.m_canvas.FillRectangle(0, self.m_height - self.m_down + 1, self.m_width, self.m_height, self.m_background.clr)
        self.m_canvas.FillRectangle(0, self.m_up, self.m_left - 1, self.m_height - self.m_down, self.m_background.clr)
        self.m_canvas.FillRectangle(self.m_width - self.m_right + 1, self.m_up, self.m_width, self.m_height - self.m_down, self.m_background.clr)
        if self.m_background.main != "" and self.m_background.size_main != 0:
            self.m_canvas.FontSet_4('Arial', self.m_background.size_main, FW_HEAVY)
            xc = _int((x2 + x1 - self.m_canvas.TextWidth(self.m_background.main)) / 2.0)
            yc = self.m_up - self.m_background.size_main - self.m_gap
            self.m_canvas.TextOut(xc, yc, self.m_background.main, self.m_background.clr_main)
            self.m_canvas.FontFlagsSet(0)
        if self.m_background.sub != "" and self.m_background.size_sub != 0:
            self.m_canvas.FontSet_4('Arial', self.m_background.size_sub, _uint(FW_MEDIUM))
            xc = _int((x2 + x1 - self.m_canvas.TextWidth(self.m_background.sub)) / 2.0)
            yc = self.m_height - self.m_down + self.m_mark_size + self.m_y.ValuesSize_0() + self.m_y.NameSize_0() + (self.m_gap * 3)
            self.m_canvas.TextOut(xc, yc, self.m_background.sub, self.m_background.clr_sub)
            self.m_canvas.FontFlagsSet(0)
    def CreateXName(self):
        if self.m_x.NameSize_0() != 0 and self.m_x.Name_0() != "":
            self.m_canvas.FontSizeSet(self.m_x.NameSize_0())
            yc = self.m_height - self.m_down + self.m_mark_size + self.m_x.ValuesSize_0() + (self.m_gap * 2)
            self.m_canvas.TextOut(_int((self.m_width - self.m_canvas.TextWidth(self.m_x.Name_0())) / 2.0), yc, self.m_x.Name_0(), self.m_x.Color_0())
    def CreateYName(self):
        if self.m_y.NameSize_0() != 0 and self.m_y.Name_0() != "":
            self.m_canvas.FontSizeSet(self.m_y.NameSize_0())
            self.m_canvas.FontAngleSet(900)
            xc = self.m_left - self.m_y.NameSize_0() - self.m_mark_size - self.m_y.ValuesWidth_0() - (self.m_gap * 2)
            self.m_canvas.TextOut(xc, _int((self.m_height + self.m_canvas.TextWidth(self.m_y.Name_0())) / 2.0), self.m_y.Name_0(), self.m_y.Color_0())
            self.m_canvas.FontAngleSet(0)
    def CreateAxes(self):
        x1 = self.m_left
        x2 = self.m_left - self.m_mark_size
        y1 = self.m_height - self.m_down
        y2 = self.m_height - self.m_down + self.m_mark_size
        self.m_canvas.Rectangle(self.m_left, self.m_up, self.m_width - self.m_right, self.m_height - self.m_down, self.m_grid.clr_frame)
        self.m_canvas.FontSet_4(self.m_y.ValuesFontName_0(), self.m_y.ValuesSize_0(), self.m_y.ValuesFontFlags_0(), self.m_y.ValuesFontAngle_0())
        i = 0
        while i < self.m_ysize:
            yvalue = self.m_yvalues[i]
            yh = self.m_canvas.TextHeight(yvalue)
            if self.m_canvas.TextWidth(yvalue) > self.m_y.ValuesWidth_0():
                if self.m_canvas.TextWidth('...') > self.m_y.ValuesWidth_0():
                    yvalue = ""
                else:
                    while self.m_canvas.TextWidth(yvalue + '...') > self.m_y.ValuesWidth_0():
                        yvalue = StringSubstr(yvalue, 0, StringLen(yvalue) - 1)
                    yvalue += '...'
            yi_width = self.m_canvas.TextWidth(yvalue)
            self.m_canvas.TextOut(self.m_left - yi_width - self.m_mark_size - self.m_gap, self.m_yc[i] - _idiv(yh, 2), yvalue, self.m_y.Color_0(), TA_LEFT)
            if self.m_mark_size > 0.0:
                self.m_canvas.LineHorizontal(x1, x2, self.m_yc[i], self.m_y.Color_0())
            i += 1
        self.m_canvas.FontSet_4(self.m_x.ValuesFontName_0(), self.m_x.ValuesSize_0(), self.m_x.ValuesFontFlags_0(), self.m_x.ValuesFontAngle_0())
        i = 0
        while i < self.m_xsize:
            xvalue = self.m_xvalues[i]
            xw = self.m_canvas.TextWidth(xvalue)
            self.m_canvas.TextOut(self.m_xc[i] - _idiv(xw, 2), y2 + self.m_gap, xvalue, self.m_x.Color_0())
            if self.m_mark_size > 0.0:
                self.m_canvas.LineVertical(self.m_xc[i], y1, y2, self.m_x.Color_0())
            i += 1
    def CreateHistory(self):
        i = 0
        while i < self.m_arr_curves.Total():
            curve = self.m_arr_curves.At(i)
            if CheckPointer(curve) != POINTER_DYNAMIC:
                return
            if not curve.Visible_0():
                i += 1
                continue
            yc = self.m_up + _idiv(self.m_history.name_size, 2) + (self.m_history.name_size * self.m_history.count_total)
            name = curve.Name_0()
            _sw13 = curve.Type_0()
            _k14 = 0 if _sw13 == CURVE_STEPS else 0 if _sw13 == CURVE_POINTS_AND_LINES else 0 if _sw13 == CURVE_LINES else 1 if _sw13 == CURVE_POINTS else 2 if _sw13 == CURVE_HISTOGRAM else 3 if _sw13 == CURVE_CUSTOM else 4
            try:
                if _k14 <= 0:
                    xc1 = self.m_width - self.m_right + self.m_gap
                    xc2 = self.m_width - self.m_right + self.m_gap + self.m_history.symbol_size
                    if self.m_history.symbol_size > 0:
                        self.m_canvas.LineWu(xc1, yc, xc2, yc, curve.Color_0(), curve.LinesStyle_0())
                    if curve.Type_0() == CURVE_LINES:
                        if name == "":
                            name = 'Lines ' + IntegerToString(_incattr(self.m_history, 'count_lines', 1, True))
                            curve.Name_1(name)
                        raise _SwitchBreak
                    elif curve.Type_0() == CURVE_STEPS:
                        if name == "":
                            name = 'Steps ' + IntegerToString(_incattr(self.m_history, 'count_lines', 1, True))
                            curve.Name_1(name)
                        raise _SwitchBreak
                if _k14 <= 1:
                    xc = self.m_width - self.m_right + self.m_gap + _idiv(self.m_history.symbol_size, 2)
                    r = _idiv(self.m_history.symbol_size, 3)
                    if r > 0:
                        _sw15 = curve.PointsType_0()
                        if _sw15 == POINT_CIRCLE:
                            if curve.PointsFill_0():
                                self.m_canvas.FillCircle(xc, yc, r, curve.PointsColor_0())
                            self.m_canvas.CircleWu(xc, yc, r, curve.Color_0())
                        elif _sw15 == POINT_SQUARE:
                            self.m_canvas.Rectangle(xc - r, yc - r, xc + r, yc + r, curve.Color_0())
                            if curve.PointsFill_0():
                                self.m_canvas.FillRectangle(xc - r + 1, yc - r + 1, xc + r - 1, yc + r - 1, curve.PointsColor_0())
                        elif _sw15 == POINT_DIAMOND:
                            xc1 = xc + 1 - r
                            yc1 = yc
                            xc2 = xc
                            yc2 = yc + 1 - r
                            self.m_canvas.Line(xc - r, yc, xc, yc - r, curve.Color_0())
                            self.m_canvas.Line(xc, yc - r, xc + r, yc, curve.Color_0())
                            self.m_canvas.Line(xc + r, yc, xc, yc + r, curve.Color_0())
                            self.m_canvas.Line(xc, yc + r, xc - r, yc, curve.Color_0())
                            if curve.PointsFill_0():
                                count = (((r * 2) - 1) if (_imod(r * 2, 2) == 0) else ((r * 2) - 2))
                                for j in range(0, count):
                                    self.m_canvas.Line(xc1, yc1, xc2, yc2, curve.PointsColor_0())
                                    if _imod(j, 2) == 0:
                                        yc2 += 1
                                        xc1 += 1
                                    else:
                                        xc2 += 1
                                        yc1 += 1
                        elif _sw15 == POINT_TRIANGLE:
                            self.m_canvas.TriangleWu(xc, yc - r, xc - r, yc + r, xc + r, yc + r, curve.Color_0())
                            if curve.PointsFill_0():
                                dy = -r
                                dx = 0
                                count = (((r * 2) - 1) if (_imod(r * 2, 2) == 0) else ((r * 2) - 2))
                                j = 0
                                while j < count:
                                    self.m_canvas.LineHorizontal(xc - dx + 1, xc + dx, yc + 1 + dy, curve.PointsColor_0())
                                    if _imod(j, 2) == 0:
                                        dx += 1
                                    j += 1
                                    dy += 1
                        elif _sw15 == POINT_TRIANGLE_DOWN:
                            self.m_canvas.TriangleWu(xc, yc + r, xc - r, yc - r, xc + r, yc - r, curve.Color_0())
                            if curve.PointsFill_0():
                                dy = r
                                dx = 0
                                count = (((r * 2) - 1) if (_imod(r * 2, 2) == 0) else ((r * 2) - 2))
                                j = 0
                                while j < count:
                                    self.m_canvas.LineHorizontal(xc - dx + 1, xc + dx, yc - 1 + dy, curve.PointsColor_0())
                                    if _imod(j, 2) == 0:
                                        dx += 1
                                    j += 1
                                    dy -= 1
                        elif _sw15 == POINT_X_CROSS:
                            self.m_canvas.Line(xc + r, yc + r, xc - r, yc - r, curve.Color_0())
                            self.m_canvas.Line(xc - r, yc + r, xc + r, yc - r, curve.Color_0())
                        elif _sw15 == POINT_PLUS:
                            self.m_canvas.LineHorizontal(xc + r + 1, xc - r, yc, curve.Color_0())
                            self.m_canvas.LineVertical(xc, yc + r, yc - r, curve.Color_0())
                        elif _sw15 == POINT_STAR:
                            self.m_canvas.LineHorizontal(xc + r + 1, xc - r, yc, curve.Color_0())
                            self.m_canvas.LineVertical(xc, yc + r, yc - r, curve.Color_0())
                            self.m_canvas.Line(xc + r, yc + r, xc - r, yc - r, curve.Color_0())
                            self.m_canvas.Line(xc - r, yc + r, xc + r, yc - r, curve.Color_0())
                        elif _sw15 == POINT_HORIZONTAL_DASH:
                            self.m_canvas.LineHorizontal(xc + r + 1, xc - r, yc, curve.Color_0())
                        elif _sw15 == POINT_VERTICAL_DASH:
                            self.m_canvas.LineVertical(xc, yc + r, yc - r, curve.Color_0())
                    else:
                        if curve.PointsSize_0() > 0:
                            self.m_canvas.PixelSet(xc, yc, curve.Color_0())
                    if curve.Type_0() == CURVE_POINTS:
                        if name == "":
                            name = 'Points ' + IntegerToString(_incattr(self.m_history, 'count_points', 1, True))
                            curve.Name_1(name)
                    elif curve.Type_0() == CURVE_POINTS_AND_LINES:
                        if name == "":
                            name = 'Points and Lines ' + IntegerToString(_incattr(self.m_history, 'count_points', 1, True))
                            curve.Name_1(name)
                    raise _SwitchBreak
                if _k14 <= 2:
                    xc1 = self.m_width - self.m_right + self.m_gap + _idiv(self.m_history.symbol_size, 6)
                    yc1 = yc - _idiv(self.m_history.symbol_size * 1, 3)
                    xc2 = self.m_width - self.m_right + self.m_gap + _idiv(self.m_history.symbol_size * 5, 6)
                    yc2 = yc + _idiv(self.m_history.symbol_size * 1, 3)
                    if self.m_history.symbol_size > 0:
                        self.m_canvas.FillRectangle(xc1, yc1, xc2, yc2, curve.Color_0())
                    if name == "":
                        name = 'Histogram ' + IntegerToString(_incattr(self.m_history, 'count_histogram', 1, True))
                        curve.Name_1(name)
                    raise _SwitchBreak
                if _k14 <= 3:
                    if name == "":
                        name = 'Custom ' + IntegerToString(_incattr(self.m_history, 'count_custom', 1, True))
                        curve.Name_1(name)
                    raise _SwitchBreak
            except _SwitchBreak:
                pass
            self.m_canvas.FontSet_4('arial', self.m_history.name_size)
            if self.m_canvas.TextWidth(name) > self.m_history.name_width:
                if self.m_canvas.TextWidth('...') > self.m_history.name_width:
                    name = ""
                else:
                    while self.m_canvas.TextWidth(name + '...') > self.m_history.name_width:
                        name = StringSubstr(name, 0, StringLen(name) - 1)
                    name += '...'
            xct = self.m_width - self.m_right + (2 * self.m_gap) + self.m_history.symbol_size
            yct = yc - _idiv(self.m_history.name_size, 2)
            self.m_canvas.TextOut(xct, yct, name, self.m_history.clr)
            self.m_history.count_total += 1
            i += 1
    def CalculateBoundaries(self):
        if self.m_width > 0 and self.m_height > 0:
            self.m_right += self.m_history.symbol_size + self.m_history.name_width + (3 * self.m_gap)
            self.m_up += self.m_background.size_main + (2 * self.m_gap)
            self.m_down += self.m_background.size_sub + self.m_x.ValuesSize_0() + self.m_x.NameSize_0() + (4 * self.m_gap)
            self.m_left += self.m_y.NameSize_0() + self.m_mark_size + self.m_y.ValuesWidth_0() + (4 * self.m_gap)
        else:
            ZeroMemory(_AttrRef(self, 'm_right'))
            ZeroMemory(_AttrRef(self, 'm_up'))
            ZeroMemory(_AttrRef(self, 'm_down'))
            ZeroMemory(_AttrRef(self, 'm_left'))
    def CalculateXAxis(self):
        self.m_x.SelectAxisScale()
        max_ = self.m_x.Max_0()
        min_ = self.m_x.Min_0()
        step = self.m_x.Step()
        xtype = self.m_x.Type_0()
        xformat = ('%.7g' if (self.m_x.ValuesFormat_0() == "") else self.m_x.ValuesFormat_0())
        xmode = self.m_x.ValuesDateTimeMode_0()
        xfunc = self.m_x.ValuesFunctionFormat_0()
        xcbdata = self.m_x.ValuesFunctionFormatCBData_0()
        xf1 = self.m_left
        xf2 = self.m_width - self.m_right
        x_size = max_ - min_
        xf_size = xf2 - xf1
        self.m_dx = _fdiv(xf_size, x_size)
        self.m_xsize = _int(MathRound(_fdiv(max_ - min_, step))) + 1
        ArrayResize(self.m_xc, self.m_xsize)
        ArrayResize(self.m_xvalues, self.m_xsize)
        factor = CGraphic.AxisFactorPrecision(min_, max_, step)
        for i in range(0, self.m_xsize):
            x = min_ + (i * step)
            if factor != 1.0:
                x = MathRound(_fdiv(x, factor)) * factor
            if x > max_:
                x = max_
            if i == 0:
                self.m_xc[i] = self.m_left
            elif i == (self.m_xsize - 1):
                self.m_xc[i] = self.m_width - self.m_right
            else:
                self.m_xc[i] = self.m_left + _int((x - min_) * self.m_dx)
            _sw16 = xtype
            if _sw16 == AXIS_TYPE_DOUBLE:
                self.m_xvalues[i] = StringFormat(xformat, x)
            elif _sw16 == AXIS_TYPE_DATETIME:
                self.m_xvalues[i] = TimeToString(_long(x), xmode)
            elif _sw16 == AXIS_TYPE_CUSTOM:
                self.m_xvalues[i] = _str((None if (xfunc is None) else xfunc(x, xcbdata)))
        self.m_xupdate = False
    def CalculateYAxis(self):
        self.m_y.SelectAxisScale()
        max_ = self.m_y.Max_0()
        min_ = self.m_y.Min_0()
        step = self.m_y.Step()
        ytype = self.m_y.Type_0()
        yformat = ('%.7g' if (self.m_y.ValuesFormat_0() == "") else self.m_y.ValuesFormat_0())
        ymode = self.m_y.ValuesDateTimeMode_0()
        yfunc = self.m_y.ValuesFunctionFormat_0()
        ycbdata = self.m_y.ValuesFunctionFormatCBData_0()
        yf1 = self.m_up
        yf2 = self.m_height - self.m_down
        y_size = max_ - min_
        yf_size = yf2 - yf1
        self.m_dy = _fdiv(yf_size, y_size)
        self.m_ysize = _int(MathRound(_fdiv(max_ - min_, step))) + 1
        ArrayResize(self.m_yc, self.m_ysize)
        ArrayResize(self.m_yvalues, self.m_ysize)
        factor = CGraphic.AxisFactorPrecision(min_, max_, step)
        for i in range(0, self.m_ysize):
            y = min_ + (i * step)
            if factor != 1.0:
                y = MathRound(_fdiv(y, factor)) * factor
            if y > max_:
                y = max_
            if i == 0:
                self.m_yc[i] = self.m_height - self.m_down
            elif i == (self.m_ysize - 1):
                self.m_yc[i] = self.m_up
            else:
                self.m_yc[i] = self.m_height - self.m_down - _int((y - min_) * self.m_dy)
            _sw17 = ytype
            if _sw17 == AXIS_TYPE_DOUBLE:
                self.m_yvalues[i] = StringFormat(yformat, y)
                StringTrimLeft(_ElemRef(self.m_yvalues, i))
                StringTrimRight(_ElemRef(self.m_yvalues, i))
            elif _sw17 == AXIS_TYPE_DATETIME:
                self.m_yvalues[i] = TimeToString(_long(y), ymode)
            elif _sw17 == AXIS_TYPE_CUSTOM:
                self.m_yvalues[i] = _str((None if (yfunc is None) else yfunc(y, ycbdata)))
        self.m_yupdate = False
    @staticmethod
    def AxisFactorPrecision(min_, max_, step):
        big_min = _s_CGraphic_AxisFactorPrecision_big_value * min_
        big_max = _s_CGraphic_AxisFactorPrecision_big_value * max_
        big_step = _s_CGraphic_AxisFactorPrecision_big_value * step
        delta_min = big_min - min_
        delta_max = big_max - max_
        delta_step = big_step - step
        error_min = MathAbs(min_ - (big_min - delta_min))
        error_max = MathAbs(max_ - (big_max - delta_max))
        error_step = MathAbs(step - (big_step - delta_step))
        error = MathMax(MathMax(error_min, error_max), error_step)
        factor = 1.0
        if error != 0:
            log10_val = MathLog10(MathAbs(error))
            log10_val = (MathCeil(log10_val) if (log10_val > 0) else MathFloor(log10_val))
            if log10_val <= -308:
                factor = 1e-308
            elif log10_val >= 308:
                factor = 1e+308
            else:
                factor = MathPow(10, log10_val)
        return factor

class CPoint2D(MqlObject):
    _q_fields = ('x', 'y')
    def __init__(self, *args):
        self.x = 0.0
        self.y = 0.0

class CCurve(CObject):
    _q_fields = ('m_clr', 'm_x', 'm_y', 'm_xmin', 'm_xmax', 'm_ymin', 'm_ymax', 'm_size', 'm_type', 'm_name', 'm_lines_style', 'm_lines_end_style', 'm_lines_width', 'm_lines_smooth', 'm_lines_tension', 'm_lines_step', 'm_points_size', 'm_points_type', 'm_points_fill', 'm_points_clr', 'm_steps_dimension', 'm_hisogram_width', 'm_custom_plot_func', 'm_custom_plot_cbdata', 'm_visible', 'm_trend_clr', 'm_trend_visible', 'm_trend_calc', 'm_trend_coeff')
    def _q_ctor1(self, y, clr, type_, name):
        CObject.__init__(self)
        self.m_clr = 0
        self.m_x = Arr(0, 0.0)
        self.m_y = Arr(0, 0.0)
        self.m_xmin = 0.0
        self.m_xmax = 0.0
        self.m_ymin = 0.0
        self.m_ymax = 0.0
        self.m_size = 0
        self.m_type = 0
        self.m_name = ""
        self.m_lines_style = 0
        self.m_lines_end_style = 0
        self.m_lines_width = 0
        self.m_lines_smooth = False
        self.m_lines_tension = 0.0
        self.m_lines_step = 0.0
        self.m_points_size = 0
        self.m_points_type = 0
        self.m_points_fill = False
        self.m_points_clr = 0
        self.m_steps_dimension = 0
        self.m_hisogram_width = 0
        self.m_custom_plot_func = None
        self.m_custom_plot_cbdata = 0
        self.m_visible = False
        self.m_trend_clr = 0
        self.m_trend_visible = False
        self.m_trend_calc = False
        self.m_trend_coeff = Arr(0, 0.0)
        self.m_name = name
        self.m_clr = clr
        self.m_type = type_
        self.m_visible = False
        self.m_lines_style = STYLE_SOLID
        self.m_lines_end_style = LINE_END_ROUND
        self.m_lines_width = 1
        self.m_lines_smooth = False
        self.m_lines_tension = 0.5
        self.m_lines_step = 1.0
        self.m_points_size = 6
        self.m_points_type = POINT_CIRCLE
        self.m_points_fill = False
        self.m_points_clr = clr
        self.m_steps_dimension = 0
        self.m_hisogram_width = 1
        self.m_custom_plot_func = None
        self.m_custom_plot_cbdata = None
        self.m_trend_visible = False
        self.m_trend_clr = clr
        self.m_trend_calc = False
        self.m_size = ArraySize(y)
        ArrayResize(self.m_x, self.m_size)
        ArrayCopy(self.m_y, y)
        self.m_xmax = self.m_size - 1
        self.m_xmin = 0.0
        self.m_ymax = 0.0
        self.m_ymin = 0.0
        yvalid = False
        for i in range(0, self.m_size):
            self.m_x[i] = i
            if MathIsValidNumber(self.m_y[i]):
                if not yvalid:
                    self.m_ymax = self.m_y[i]
                    self.m_ymin = self.m_y[i]
                    yvalid = True
                else:
                    if self.m_ymax < y[i]:
                        self.m_ymax = y[i]
                    elif self.m_ymin > y[i]:
                        self.m_ymin = y[i]
    def _q_ctor2(self, x, y, clr, type_, name):
        CObject.__init__(self)
        self.m_clr = 0
        self.m_x = Arr(0, 0.0)
        self.m_y = Arr(0, 0.0)
        self.m_xmin = 0.0
        self.m_xmax = 0.0
        self.m_ymin = 0.0
        self.m_ymax = 0.0
        self.m_size = 0
        self.m_type = 0
        self.m_name = ""
        self.m_lines_style = 0
        self.m_lines_end_style = 0
        self.m_lines_width = 0
        self.m_lines_smooth = False
        self.m_lines_tension = 0.0
        self.m_lines_step = 0.0
        self.m_points_size = 0
        self.m_points_type = 0
        self.m_points_fill = False
        self.m_points_clr = 0
        self.m_steps_dimension = 0
        self.m_hisogram_width = 0
        self.m_custom_plot_func = None
        self.m_custom_plot_cbdata = 0
        self.m_visible = False
        self.m_trend_clr = 0
        self.m_trend_visible = False
        self.m_trend_calc = False
        self.m_trend_coeff = Arr(0, 0.0)
        self.m_name = name
        self.m_clr = clr
        self.m_type = type_
        self.m_visible = False
        self.m_lines_style = STYLE_SOLID
        self.m_lines_end_style = LINE_END_ROUND
        self.m_lines_width = 1
        self.m_lines_smooth = False
        self.m_lines_tension = 0.5
        self.m_lines_step = 1.0
        self.m_points_size = 6
        self.m_points_type = POINT_CIRCLE
        self.m_points_fill = False
        self.m_points_clr = clr
        self.m_steps_dimension = 0
        self.m_hisogram_width = 1
        self.m_custom_plot_func = None
        self.m_custom_plot_cbdata = None
        self.m_trend_visible = False
        self.m_trend_clr = clr
        self.m_trend_calc = False
        ArrayCopy(self.m_x, x)
        ArrayCopy(self.m_y, y)
        self.m_size = ArraySize(x)
        self.m_xmax = 0.0
        self.m_xmin = 0.0
        self.m_ymax = 0.0
        self.m_ymin = 0.0
        yvalid = False
        xvalid = False
        for i in range(0, self.m_size):
            if MathIsValidNumber(self.m_x[i]):
                if not xvalid:
                    self.m_xmax = x[i]
                    self.m_xmin = x[i]
                    xvalid = True
                else:
                    if self.m_xmax < x[i]:
                        self.m_xmax = x[i]
                    elif self.m_xmin > x[i]:
                        self.m_xmin = x[i]
            if MathIsValidNumber(self.m_y[i]):
                if not yvalid:
                    self.m_ymax = y[i]
                    self.m_ymin = y[i]
                    yvalid = True
                else:
                    if self.m_ymax < y[i]:
                        self.m_ymax = y[i]
                    elif self.m_ymin > y[i]:
                        self.m_ymin = y[i]
    def _q_ctor3(self, points, clr, type_, name):
        CObject.__init__(self)
        self.m_clr = 0
        self.m_x = Arr(0, 0.0)
        self.m_y = Arr(0, 0.0)
        self.m_xmin = 0.0
        self.m_xmax = 0.0
        self.m_ymin = 0.0
        self.m_ymax = 0.0
        self.m_size = 0
        self.m_type = 0
        self.m_name = ""
        self.m_lines_style = 0
        self.m_lines_end_style = 0
        self.m_lines_width = 0
        self.m_lines_smooth = False
        self.m_lines_tension = 0.0
        self.m_lines_step = 0.0
        self.m_points_size = 0
        self.m_points_type = 0
        self.m_points_fill = False
        self.m_points_clr = 0
        self.m_steps_dimension = 0
        self.m_hisogram_width = 0
        self.m_custom_plot_func = None
        self.m_custom_plot_cbdata = 0
        self.m_visible = False
        self.m_trend_clr = 0
        self.m_trend_visible = False
        self.m_trend_calc = False
        self.m_trend_coeff = Arr(0, 0.0)
        self.m_name = name
        self.m_clr = clr
        self.m_type = type_
        self.m_visible = False
        self.m_lines_style = STYLE_SOLID
        self.m_lines_end_style = LINE_END_ROUND
        self.m_lines_width = 1
        self.m_lines_smooth = False
        self.m_lines_tension = 0.5
        self.m_lines_step = 1.0
        self.m_points_size = 6
        self.m_points_type = POINT_CIRCLE
        self.m_points_fill = False
        self.m_points_clr = clr
        self.m_steps_dimension = 0
        self.m_hisogram_width = 1
        self.m_custom_plot_func = None
        self.m_custom_plot_cbdata = None
        self.m_trend_visible = False
        self.m_trend_clr = clr
        self.m_trend_calc = False
        self.m_size = ArraySize(points)
        ArrayResize(self.m_x, self.m_size)
        ArrayResize(self.m_y, self.m_size)
        self.m_xmax = 0.0
        self.m_xmin = 0.0
        self.m_ymax = 0.0
        self.m_ymin = 0.0
        xvalid = False
        yvalid = False
        for i in range(0, self.m_size):
            self.m_x[i] = points[i].x
            self.m_y[i] = points[i].y
            if MathIsValidNumber(self.m_x[i]):
                if not xvalid:
                    self.m_xmax = self.m_x[i]
                    self.m_xmin = self.m_x[i]
                    xvalid = True
                else:
                    if self.m_xmax < self.m_x[i]:
                        self.m_xmax = self.m_x[i]
                    elif self.m_xmin > self.m_x[i]:
                        self.m_xmin = self.m_x[i]
            if MathIsValidNumber(self.m_y[i]):
                if not yvalid:
                    self.m_ymax = self.m_y[i]
                    self.m_ymin = self.m_y[i]
                    yvalid = True
                else:
                    if self.m_ymax < self.m_y[i]:
                        self.m_ymax = self.m_y[i]
                    elif self.m_ymin > self.m_y[i]:
                        self.m_ymin = self.m_y[i]
    def _q_ctor4(self, function, from_, to, step, clr, type_, name):
        CObject.__init__(self)
        self.m_clr = 0
        self.m_x = Arr(0, 0.0)
        self.m_y = Arr(0, 0.0)
        self.m_xmin = 0.0
        self.m_xmax = 0.0
        self.m_ymin = 0.0
        self.m_ymax = 0.0
        self.m_size = 0
        self.m_type = 0
        self.m_name = ""
        self.m_lines_style = 0
        self.m_lines_end_style = 0
        self.m_lines_width = 0
        self.m_lines_smooth = False
        self.m_lines_tension = 0.0
        self.m_lines_step = 0.0
        self.m_points_size = 0
        self.m_points_type = 0
        self.m_points_fill = False
        self.m_points_clr = 0
        self.m_steps_dimension = 0
        self.m_hisogram_width = 0
        self.m_custom_plot_func = None
        self.m_custom_plot_cbdata = 0
        self.m_visible = False
        self.m_trend_clr = 0
        self.m_trend_visible = False
        self.m_trend_calc = False
        self.m_trend_coeff = Arr(0, 0.0)
        self.m_name = name
        self.m_clr = clr
        self.m_type = type_
        self.m_visible = False
        self.m_lines_style = STYLE_SOLID
        self.m_lines_end_style = LINE_END_ROUND
        self.m_lines_width = 1
        self.m_lines_smooth = False
        self.m_lines_tension = 0.5
        self.m_lines_step = 1.0
        self.m_points_size = 6
        self.m_points_type = POINT_CIRCLE
        self.m_points_fill = False
        self.m_points_clr = clr
        self.m_steps_dimension = 0
        self.m_hisogram_width = 1
        self.m_custom_plot_func = None
        self.m_custom_plot_cbdata = None
        self.m_trend_visible = False
        self.m_trend_clr = clr
        self.m_trend_calc = False
        self.m_size = _int(_fdiv(to - from_, step)) + 1
        ArrayResize(self.m_x, self.m_size)
        ArrayResize(self.m_y, self.m_size)
        self.m_xmax = to
        self.m_xmin = from_
        self.m_ymax = 0.0
        self.m_ymin = 0.0
        yvalid = False
        for i in range(0, self.m_size):
            self.m_x[i] = from_ + (i * step)
            self.m_y[i] = function(self.m_x[i])
            if MathIsValidNumber(self.m_y[i]):
                if not yvalid:
                    self.m_ymax = self.m_y[i]
                    self.m_ymin = self.m_y[i]
                    yvalid = True
                else:
                    if self.m_ymax < self.m_y[i]:
                        self.m_ymax = self.m_y[i]
                    elif self.m_ymin > self.m_y[i]:
                        self.m_ymin = self.m_y[i]
    def __init__(self, *args):
        if 4 <= len(args) <= 4 and (len(args) == 0 or isinstance(args[0], Arr)):
            self._q_ctor1(*args)
            return
        if 5 <= len(args) <= 5 and (len(args) == 0 or isinstance(args[0], Arr)):
            self._q_ctor2(*args)
            return
        if 4 <= len(args) <= 4 and (len(args) == 0 or isinstance(args[0], MqlObject)):
            self._q_ctor3(*args)
            return
        if 7 <= len(args) <= 7:
            self._q_ctor4(*args)
            return
        self._q_ctor1(*args)
    def _q_dtor(self):
        pass
    def GetX(self, x):
        ArrayCopy(x, self.m_x)
    def GetY(self, y):
        ArrayCopy(y, self.m_y)
    def XMax(self):
        return self.m_xmax
    def XMin(self):
        return self.m_xmin
    def YMax(self):
        return self.m_ymax
    def YMin(self):
        return self.m_ymin
    def Size(self):
        return self.m_size
    def Update_1(self, y):
        self.m_trend_calc = False
        ArrayFree(self.m_y)
        size = ArraySize(y)
        if self.m_size != size:
            self.m_size = size
            ArrayResize(self.m_x, self.m_size)
        ArrayCopy(self.m_y, y)
        self.m_xmax = self.m_size - 1
        self.m_xmin = 0.0
        self.m_ymax = 0.0
        self.m_ymin = 0.0
        yvalid = False
        for i in range(0, self.m_size):
            self.m_x[i] = i
            if MathIsValidNumber(self.m_y[i]):
                if not yvalid:
                    self.m_ymax = self.m_y[i]
                    self.m_ymin = self.m_y[i]
                    yvalid = True
                else:
                    if self.m_ymax < y[i]:
                        self.m_ymax = y[i]
                    elif self.m_ymin > y[i]:
                        self.m_ymin = y[i]
    def Update_2(self, x, y):
        self.m_trend_calc = False
        ArrayFree(self.m_x)
        ArrayFree(self.m_y)
        ArrayCopy(self.m_x, x)
        ArrayCopy(self.m_y, y)
        self.m_size = ArraySize(x)
        self.m_xmax = 0.0
        self.m_xmin = 0.0
        self.m_ymax = 0.0
        self.m_ymin = 0.0
        yvalid = False
        xvalid = False
        for i in range(0, self.m_size):
            if MathIsValidNumber(self.m_x[i]):
                if not xvalid:
                    self.m_xmax = x[i]
                    self.m_xmin = x[i]
                    xvalid = True
                else:
                    if self.m_xmax < x[i]:
                        self.m_xmax = x[i]
                    elif self.m_xmin > x[i]:
                        self.m_xmin = x[i]
            if MathIsValidNumber(self.m_y[i]):
                if not yvalid:
                    self.m_ymax = y[i]
                    self.m_ymin = y[i]
                    yvalid = True
                else:
                    if self.m_ymax < y[i]:
                        self.m_ymax = y[i]
                    elif self.m_ymin > y[i]:
                        self.m_ymin = y[i]
    def Update_3(self, points):
        self.m_trend_calc = False
        size = ArraySize(points)
        if size != self.m_size:
            self.m_size = size
            ArrayResize(self.m_x, self.m_size)
            ArrayResize(self.m_y, self.m_size)
        self.m_xmax = 0.0
        self.m_xmin = 0.0
        self.m_ymax = 0.0
        self.m_ymin = 0.0
        xvalid = False
        yvalid = False
        for i in range(0, self.m_size):
            self.m_x[i] = points[i].x
            self.m_y[i] = points[i].y
            if MathIsValidNumber(self.m_x[i]):
                if not xvalid:
                    self.m_xmax = self.m_x[i]
                    self.m_xmin = self.m_x[i]
                    xvalid = True
                else:
                    if self.m_xmax < self.m_x[i]:
                        self.m_xmax = self.m_x[i]
                    elif self.m_xmin > self.m_x[i]:
                        self.m_xmin = self.m_x[i]
            if MathIsValidNumber(self.m_y[i]):
                if not yvalid:
                    self.m_ymax = self.m_y[i]
                    self.m_ymin = self.m_y[i]
                    yvalid = True
                else:
                    if self.m_ymax < self.m_y[i]:
                        self.m_ymax = self.m_y[i]
                    elif self.m_ymin > self.m_y[i]:
                        self.m_ymin = self.m_y[i]
    def Update_4(self, function, from_, to, step):
        self.m_trend_calc = False
        size = _int(_fdiv(to - from_, step)) + 1
        if size != self.m_size:
            self.m_size = size
            ArrayResize(self.m_x, self.m_size)
            ArrayResize(self.m_y, self.m_size)
        self.m_xmax = to
        self.m_xmin = from_
        self.m_ymax = 0.0
        self.m_ymin = 0.0
        yvalid = False
        for i in range(0, self.m_size):
            self.m_x[i] = from_ + (i * step)
            self.m_y[i] = function(self.m_x[i])
            if MathIsValidNumber(self.m_y[i]):
                if not yvalid:
                    self.m_ymax = self.m_y[i]
                    self.m_ymin = self.m_y[i]
                    yvalid = True
                else:
                    if self.m_ymax < self.m_y[i]:
                        self.m_ymax = self.m_y[i]
                    elif self.m_ymin > self.m_y[i]:
                        self.m_ymin = self.m_y[i]
    def Color_0(self):
        return self.m_clr
    def Color_1(self, clr):
        self.m_clr = clr
    def Type_0(self):
        return self.m_type
    def Type_1(self, type_):
        self.m_type = type_
    def Name_0(self):
        return self.m_name
    def Name_1(self, name):
        self.m_name = name
    def Visible_0(self):
        return self.m_visible
    def Visible_1(self, visible):
        self.m_visible = visible
    def LinesStyle_0(self):
        return self.m_lines_style
    def LinesStyle_1(self, style):
        self.m_lines_style = style
    def LinesEndStyle_0(self):
        return self.m_lines_end_style
    def LinesEndStyle_1(self, end_style):
        self.m_lines_end_style = end_style
    def LinesWidth_0(self):
        return self.m_lines_width
    def LinesWidth_1(self, width):
        self.m_lines_width = width
    def LinesSmooth_0(self):
        return self.m_lines_smooth
    def LinesSmooth_1(self, smooth):
        self.m_lines_smooth = smooth
    def LinesSmoothTension_0(self):
        return self.m_lines_tension
    def LinesSmoothTension_1(self, tension):
        self.m_lines_tension = tension
    def LinesSmoothStep_0(self):
        return self.m_lines_step
    def LinesSmoothStep_1(self, step):
        self.m_lines_step = step
    def PointsSize_0(self):
        return self.m_points_size
    def PointsSize_1(self, size):
        self.m_points_size = size
    def PointsType_0(self):
        return self.m_points_type
    def PointsType_1(self, type_):
        self.m_points_type = type_
    def PointsFill_0(self):
        return self.m_points_fill
    def PointsFill_1(self, fill):
        self.m_points_fill = fill
    def PointsColor_0(self):
        return self.m_points_clr
    def PointsColor_1(self, clr):
        self.m_points_clr = clr
    def StepsDimension_0(self):
        return self.m_steps_dimension
    def StepsDimension_1(self, dimension):
        self.m_steps_dimension = dimension
    def HistogramWidth_0(self):
        return self.m_hisogram_width
    def HistogramWidth_1(self, width):
        self.m_hisogram_width = width
    def CustomPlotFunction_0(self):
        return self.m_custom_plot_func
    def CustomPlotFunction_1(self, func):
        self.m_custom_plot_func = func
    def CustomPlotCBData_0(self):
        return self.m_custom_plot_cbdata
    def CustomPlotCBData_1(self, cbdata):
        self.m_custom_plot_cbdata = cbdata
    def TrendLineVisible_0(self):
        return self.m_trend_visible
    def TrendLineVisible_1(self, visible):
        self.m_trend_visible = visible
    def TrendLineColor_0(self):
        return self.m_trend_clr
    def TrendLineColor_1(self, clr):
        self.m_trend_clr = clr
    def TrendLineCoefficients(self, coefficients):
        if not self.m_trend_calc:
            self.CalculateCoefficients()
            self.m_trend_calc = True
        ArrayCopy(coefficients, self.m_trend_coeff)
    def CalculateCoefficients(self):
        ArrayResize(self.m_trend_coeff, 2)
        xmean = 0.0
        ymean = 0.0
        sum_xy = 0.0
        sum_xx = 0.0
        for i in range(0, self.m_size):
            xmean += self.m_x[i]
            ymean += self.m_y[i]
            sum_xy += self.m_x[i] * self.m_y[i]
            sum_xx += self.m_x[i] * self.m_x[i]
        xmean = _fdiv(xmean, self.m_size)
        ymean = _fdiv(ymean, self.m_size)
        self.m_trend_coeff[0] = _fdiv(sum_xy - (self.m_size * xmean * ymean), sum_xx - (self.m_size * xmean * xmean))
        self.m_trend_coeff[1] = ymean - (self.m_trend_coeff[0] * xmean)

class CBackground(MqlObject):
    _q_fields = ('clr', 'clr_main', 'clr_sub', 'main', 'sub', 'size_main', 'size_sub')
    def __init__(self, *args):
        self.clr = 0
        self.clr_main = 0
        self.clr_sub = 0
        self.main = ""
        self.sub = ""
        self.size_main = 0
        self.size_sub = 0

class CCurveHistory(MqlObject):
    _q_fields = ('name_width', 'name_size', 'symbol_size', 'count_total', 'count_points', 'count_lines', 'count_histogram', 'count_custom', 'clr')
    def __init__(self, *args):
        self.name_width = 0
        self.name_size = 0
        self.symbol_size = 0
        self.count_total = 0
        self.count_points = 0
        self.count_lines = 0
        self.count_histogram = 0
        self.count_custom = 0
        self.clr = 0

class CGrid(MqlObject):
    _q_fields = ('clr_line', 'clr_background', 'clr_circle', 'clr_axis_line', 'clr_frame', 'r_circle', 'has_circle')
    def __init__(self, *args):
        self.clr_line = 0
        self.clr_background = 0
        self.clr_circle = 0
        self.clr_axis_line = 0
        self.clr_frame = 0
        self.r_circle = 0
        self.has_circle = False

class BitmapHeader(MqlObject):
    _q_fields = ('type', 'size', 'reserv', 'offbits', 'imgSSize', 'imgWidth', 'imgHeight', 'imgPlanes', 'imgBitCount', 'imgCompression', 'imgSizeImage', 'imgXPelsPerMeter', 'imgYPelsPerMeter', 'imgClrUsed', 'imgClrImportant')
    def __init__(self, *args):
        self.type = 0
        self.size = 0
        self.reserv = 0
        self.offbits = 0
        self.imgSSize = 0
        self.imgWidth = 0
        self.imgHeight = 0
        self.imgPlanes = 0
        self.imgBitCount = 0
        self.imgCompression = 0
        self.imgSizeImage = 0
        self.imgXPelsPerMeter = 0
        self.imgYPelsPerMeter = 0
        self.imgClrUsed = 0
        self.imgClrImportant = 0

def GraphPlot_1(y, type_=CURVE_POINTS, objname=None):
    graphic = CGraphic()
    width = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
    height = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    res = False
    objname = ('Graphic' if (objname == "") else objname)
    if ObjectFind(0, objname) >= 0:
        res = graphic.Attach_2(0, objname)
    else:
        res = graphic.Create(0, objname, 0, 65, 45, _int(0.6 * width), _int(0.65 * height))
    if not res:
        return ""
    graphic.CurveAdd_1(y, type_)
    graphic.CurvePlotAll()
    graphic.Update()
    return graphic.ChartObjectName()

def GraphPlot_2(x, y, type_=CURVE_POINTS, objname=None):
    graphic = CGraphic()
    width = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
    height = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    res = False
    objname = ('Graphic' if (objname == "") else objname)
    if ObjectFind(0, objname) >= 0:
        res = graphic.Attach_2(0, objname)
    else:
        res = graphic.Create(0, objname, 0, 65, 45, _int(0.6 * width), _int(0.65 * height))
    if not res:
        return ""
    graphic.CurveAdd_2(x, y, type_)
    graphic.CurvePlotAll()
    graphic.Update()
    return graphic.ChartObjectName()

def GraphPlot_3(x1, y1, x2, y2, type_=CURVE_POINTS, objname=None):
    graphic = CGraphic()
    width = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
    height = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    res = False
    objname = ('Graphic' if (objname == "") else objname)
    if ObjectFind(0, objname) >= 0:
        res = graphic.Attach_2(0, objname)
    else:
        res = graphic.Create(0, objname, 0, 65, 45, _int(0.6 * width), _int(0.65 * height))
    if not res:
        return ""
    graphic.CurveAdd_2(x1, y1, type_)
    graphic.CurveAdd_2(x2, y2, type_)
    graphic.CurvePlotAll()
    graphic.Update()
    return graphic.ChartObjectName()

def GraphPlot_4(x1, y1, x2, y2, x3, y3, type_=CURVE_POINTS, objname=None):
    graphic = CGraphic()
    width = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
    height = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    res = False
    objname = ('Graphic' if (objname == "") else objname)
    if ObjectFind(0, objname) >= 0:
        res = graphic.Attach_2(0, objname)
    else:
        res = graphic.Create(0, objname, 0, 65, 45, _int(0.6 * width), _int(0.65 * height))
    if not res:
        return ""
    graphic.CurveAdd_2(x1, y1, type_)
    graphic.CurveAdd_2(x2, y2, type_)
    graphic.CurveAdd_2(x3, y3, type_)
    graphic.CurvePlotAll()
    graphic.Update()
    return graphic.ChartObjectName()

def GraphPlot_5(points, type_=CURVE_POINTS, objname=None):
    graphic = CGraphic()
    width = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
    height = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    res = False
    objname = ('Graphic' if (objname == "") else objname)
    if ObjectFind(0, objname) >= 0:
        res = graphic.Attach_2(0, objname)
    else:
        res = graphic.Create(0, objname, 0, 65, 45, _int(0.6 * width), _int(0.65 * height))
    if not res:
        return ""
    graphic.CurveAdd_3(points, type_)
    graphic.CurvePlotAll()
    graphic.Update()
    return graphic.ChartObjectName()

def GraphPlot_6(points1, points2, type_=CURVE_POINTS, objname=None):
    graphic = CGraphic()
    width = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
    height = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    res = False
    objname = ('Graphic' if (objname == "") else objname)
    if ObjectFind(0, objname) >= 0:
        res = graphic.Attach_2(0, objname)
    else:
        res = graphic.Create(0, objname, 0, 65, 45, _int(0.6 * width), _int(0.65 * height))
    if not res:
        return ""
    graphic.CurveAdd_3(points1, type_)
    graphic.CurveAdd_3(points2, type_)
    graphic.CurvePlotAll()
    graphic.Update()
    return graphic.ChartObjectName()

def GraphPlot_7(points1, points2, points3, type_=CURVE_POINTS, objname=None):
    graphic = CGraphic()
    width = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
    height = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    res = False
    objname = ('Graphic' if (objname == "") else objname)
    if ObjectFind(0, objname) >= 0:
        res = graphic.Attach_2(0, objname)
    else:
        res = graphic.Create(0, objname, 0, 65, 45, _int(0.6 * width), _int(0.65 * height))
    if not res:
        return ""
    graphic.CurveAdd_3(points1, type_)
    graphic.CurveAdd_3(points2, type_)
    graphic.CurveAdd_3(points3, type_)
    graphic.CurvePlotAll()
    graphic.Update()
    return graphic.ChartObjectName()

def GraphPlot_8(function, from_, to, step, type_=CURVE_POINTS, objname=None):
    graphic = CGraphic()
    width = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
    height = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    res = False
    objname = ('Graphic' if (objname == "") else objname)
    if ObjectFind(0, objname) >= 0:
        res = graphic.Attach_2(0, objname)
    else:
        res = graphic.Create(0, objname, 0, 65, 45, _int(0.6 * width), _int(0.65 * height))
    if not res:
        return ""
    graphic.CurveAdd_6(function, from_, to, step, type_)
    graphic.CurvePlotAll()
    graphic.Update()
    return graphic.ChartObjectName()

def GraphPlot_9(function1, function2, from_, to, step, type_=CURVE_POINTS, objname=None):
    graphic = CGraphic()
    width = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
    height = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    res = False
    objname = ('Graphic' if (objname == "") else objname)
    if ObjectFind(0, objname) >= 0:
        res = graphic.Attach_2(0, objname)
    else:
        res = graphic.Create(0, objname, 0, 65, 45, _int(0.6 * width), _int(0.65 * height))
    if not res:
        return ""
    graphic.CurveAdd_6(function1, from_, to, step, type_)
    graphic.CurveAdd_6(function2, from_, to, step, type_)
    graphic.CurvePlotAll()
    graphic.Update()
    return graphic.ChartObjectName()

def GraphPlot_10(function1, function2, function3, from_, to, step, type_=CURVE_POINTS, objname=None):
    graphic = CGraphic()
    width = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)
    height = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    res = False
    objname = ('Graphic' if (objname == "") else objname)
    if ObjectFind(0, objname) >= 0:
        res = graphic.Attach_2(0, objname)
    else:
        res = graphic.Create(0, objname, 0, 65, 45, _int(0.6 * width), _int(0.65 * height))
    if not res:
        return ""
    graphic.CurveAdd_6(function1, from_, to, step, type_)
    graphic.CurveAdd_6(function2, from_, to, step, type_)
    graphic.CurveAdd_6(function3, from_, to, step, type_)
    graphic.CurvePlotAll()
    graphic.Update()
    return graphic.ChartObjectName()

def OnInit():
    global ExtDistance, m_adjusted_point, m_first_start
    digits_adjust = 1
    if Digits() == 3 or Digits() == 5:
        digits_adjust = 10
    m_adjusted_point = Point() * digits_adjust
    ExtDistance = 1 * m_adjusted_point
    my_graphic.Create(0, 'Evening Star Statistics', 0, 20, 20, 20 + InpWidth, 20 + InpHeight)
    m_first_start = False
    return INIT_SUCCEEDED

def OnDeinit(reason):
    my_graphic.Destroy()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global m_first_start
    if not m_first_start:
        ArraySetAsSeries(time, True)
        ArraySetAsSeries(open, True)
        ArraySetAsSeries(high, True)
        ArraySetAsSeries(low, True)
        ArraySetAsSeries(close, True)
        size = rates_total
        arrX = Arr(0, 0.0)
        arrY = Arr(0, 0.0)
        ArraySetAsSeries(arrX, True)
        ArraySetAsSeries(arrY, True)
        j = 0
        while j < size:
            if time[j] < InpStartTime:
                size = j
                break
            j += 1
        limit = size
        ArrayResize(arrX, limit)
        ArrayResize(arrY, limit)
        arrY[0] = 0.0
        arrY[limit - 3] = 0.0
        arrY[limit - 2] = 0.0
        arrY[limit - 1] = 0.0
        arrX[limit - 3] = float(time[limit - 3])
        arrX[limit - 2] = float(time[limit - 2])
        arrX[limit - 1] = float(time[limit - 1])
        for i in range(0, limit - 3):
            arrX[i] = float(time[i])
            if open[i + 0] > close[i + 0] and open[i + 2] < close[i + 2]:
                if InpCandleSizes:
                    if MathAbs(open[i + 0] - close[i + 0]) < MathAbs(open[i + 1] - close[i + 1]) or MathAbs(open[i + 2] - close[i + 2]) < MathAbs(open[i + 1] - close[i + 1]):
                        arrY[i + 1] = 0.0
                        continue
                if InpCandle2Type:
                    if open[i + 1] > close[i + 1]:
                        arrY[i + 1] = 0.0
                        continue
                else:
                    if close[i + 1] > open[i + 1]:
                        arrY[i + 1] = 0.0
                        continue
                if InpGap:
                    if open[i + 0] >= (close[i + 1] - ExtDistance) or open[i + 1] <= (close[i + 2] + ExtDistance):
                        arrY[i + 1] = 0.0
                        continue
                arrY[i + 1] = 1.0
        curve_b = my_graphic.CurveAdd_2(arrX, arrY, CURVE_POINTS, '')
        xAxis = my_graphic.XAxis()
        xAxis.Type_1(AXIS_TYPE_DATETIME)
        if Period() > PERIOD_M30:
            xAxis.ValuesDateTimeMode_1(TIME_DATE)
        else:
            xAxis.ValuesDateTimeMode_1(TIME_DATE | TIME_MINUTES)
        yAxis = my_graphic.YAxis()
        yAxis.ZeroLever_1(1.0)
        yAxis.Min_1(0.9)
        my_graphic.CurvePlotAll()
        text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1)
        text += ';'
        text += ('true' if InpGap else 'false')
        text += ';'
        text += ('true' if InpCandle2Type else 'false')
        text += ';'
        text += ('true' if InpCandleSizes else 'false')
        my_graphic.TextAdd_5(_idiv(20 + InpWidth, 3), _idiv(20 + InpHeight, 3), 'Evening Star (' + text + ')', ColorToARGB(clrBlue, 255))
        my_graphic.Update()
        m_first_start = True
    return rates_total

# ---- global variables initialised from expressions
my_graphic = _alloc(CGraphic)
my_graphic.__init__()

# ---- static local variables
_s_CCanvas_FillPolygon_p = Arr(0, 0, factory=CPoint)
_s_CCanvas_PixelSetAA_rr = Arr(4, 0.0, dyn=False)
_s_CCanvas_PixelSetAA_xx = Arr(4, 0, dyn=False)
_s_CCanvas_PixelSetAA_yy = Arr(4, 0, dyn=False)
_s_CGraphic_AxisFactorPrecision_big_value = 4097.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EveningStarStatistics(_MQL5Indicator):
    name = 'EveningStarStatistics'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpWidth': 900,  # Width
        'InpHeight': 400,  # Height
        'InpGap': True,  # Gap. true -> gap is taken into account
        'InpCandle2Type': True,  # Candle 2 type. true -> type of candle 2 is taken into account
        'InpCandleSizes': True,  # Candle sizes. true -> candle sizes is taken into account
    }

