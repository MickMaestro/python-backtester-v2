"""stocksbg — converted from MQL5: MQL5 Indicators/StocksBG/stocksbg.mq5

Project Stocks
Project Stocks
Project Stocks
Project Stocks
Project Stocks
Project Stocks
Project Stocks
Project Stocks
Project Stocks
Copyright: Copyright 2014, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Functions not available here: FileReadLong, FileWriteLong
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh
from backtester.mql5.lib.cgostocksbg import *  # #include CGOStocksBG.mqh
from backtester.mql5.lib.cgstockasbg import *  # #include CGStockAsBG.mqh
from backtester.mql5.lib.cstock import *  # #include CStock.mqh
from backtester.mql5.lib.stockstruct import *  # #include StockStruct.mqh
from backtester.mql5.lib.cstockstyles import *  # #include CStockStyles.mqh
from backtester.mql5.lib.cgcanvas import *  # #include CGCanvas.mqh
from backtester.mql5.lib.cgraphbase import *  # #include CGraphBase.mqh
from backtester.mql5.lib.cglabel import *  # #include CGLabel.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2014, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Project Stocks', 'Project Stocks', 'Project Stocks', 'Project Stocks', 'Project Stocks', 'Project Stocks', 'Project Stocks', 'Project Stocks', 'Project Stocks'], 'name': 'stocksbg', 'source': 'MQL5 Indicators/StocksBG/stocksbg.mq5', 'folder': 'StocksBG', 'inputs': [{'mql': 'ipt_top', 'py': 'ipt_top', 'param': 'ipt_top', 'type': 'int', 'default': 0, 'label': 'Top indent', 'sinput': False}, {'mql': 'ipt_down', 'py': 'ipt_down', 'param': 'ipt_down', 'type': 'int', 'default': 20, 'label': 'Bottom indent', 'sinput': False}, {'mql': 'ipt_scheme', 'py': 'ipt_scheme', 'param': 'ipt_scheme', 'type': 'int', 'default': 0, 'label': 'Color scheme', 'sinput': False}, {'mql': 'ipt_total', 'py': 'ipt_total', 'param': 'ipt_total', 'type': 'int', 'default': 4, 'label': 'Number of days to show', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh', 'CGOStocksBG.mqh', 'CGStockAsBG.mqh', 'CStock.mqh', 'StockStruct.mqh', 'CStockStyles.mqh', 'CGCanvas.mqh', 'CGraphBase.mqh', 'CGLabel.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
ipt_top = _input('ipt_top', 0)  # Top indent
ipt_down = _input('ipt_down', 20)  # Bottom indent
ipt_scheme = _input('ipt_scheme', 0)  # Color scheme
ipt_total = _input('ipt_total', 4)  # Number of days to show
m_daily_stocks = None
DTime = Arr(0, 0)
debug = ''
stop_running = False

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

class CGOStocksContainer(MqlObject):
    _q_fields = ('m_id', 'm_subwin', 'm_scheme', 'm_created', 'm_caption', 'm_dt_start', 'm_prefix', 'm_suffix', 'm_total', 'm_current', 'm_top_indent', 'm_bottom_indent', 'm_container_stock')
    _q_ptrs = ('m_container_stock',)
    def __init__(self, aDTime, aTop=0, aDown=20, aScheme=0, aPrefix='ST_', aTotal=1, aCaption=False, aID=0, aSubwin=0):
        self.m_id = 0
        self.m_subwin = 0
        self.m_scheme = 0
        self.m_created = False
        self.m_caption = False
        self.m_dt_start = Arr(0, 0)
        self.m_prefix = ""
        self.m_suffix = Arr(0, "")
        self.m_total = 0
        self.m_current = 0
        self.m_top_indent = 0
        self.m_bottom_indent = 0
        self.m_container_stock = None
        self.m_id = aID
        self.m_subwin = aSubwin
        self.m_scheme = aScheme
        self.m_top_indent = aTop
        self.m_bottom_indent = aDown
        self.m_caption = aCaption
        self.m_total = aTotal
        self.m_prefix = aPrefix
        ArrayResize(self.m_dt_start, self.m_total)
        ArrayResize(self.m_suffix, self.m_total)
        for i in range(0, self.m_total):
            self.m_dt_start[i] = aDTime[i]
            self.m_suffix[i] = IntegerToString(i, 3, 48)
        self.m_container_stock = CArrayObj()
    def _q_dtor(self):
        self.m_container_stock.DeleteRange(0, self.m_total - 1)
        _delete(self.m_container_stock)
    def GetStocks(self):
        return self.m_container_stock
    def GetPtrToStocks(self):
        return self.m_container_stock.At(self.m_current)
    def GetTotal(self):
        return self.m_total
    def SetCurrentIndex(self, aIndex):
        self.m_current = aIndex
    def SetAllStocks(self):
        i = 0
        while i < self.m_total:
            stocks_bg = CGOStocksBG(self.m_dt_start[i], self.m_top_indent, self.m_bottom_indent, self.m_scheme, self.m_prefix, self.m_suffix[i], self.m_caption, self.m_id, self.m_subwin)
            stocks_bg.SetPositionsDefaults()
            self.m_container_stock.Add(stocks_bg)
            i += 1
        self.ReDraw()
    def ProcessingAllStocks(self, aDTime):
        ptr_stocks_bg = None
        ptr_stocks_bg = self.GetPtrToStocks()
        i = 0
        while i < self.m_total:
            self.SetCurrentIndex(i)
            ptr_stocks_bg = self.GetPtrToStocks()
            self.m_dt_start[i] = aDTime[i]
            ptr_stocks_bg.ProcessingStocks(self.m_dt_start[i])
            i += 1
    def DeInit(self):
        ptr_stocks_bg = None
        i = 0
        while i < self.m_total:
            self.SetCurrentIndex(i)
            ptr_stocks_bg = self.GetPtrToStocks()
            ptr_stocks_bg.DeInit()
            i += 1
        self.m_container_stock.DeleteRange(0, self.m_total - 1)
        _delete(self.m_container_stock)
    def ReDraw(self):
        ChartRedraw(self.m_id)
    def DeleteByPrefix(self, aPrefix):
        obj_name = ""
        obj_total = ObjectsTotal(0, 0, -1)
        for i in range(obj_total - 1, 0 - 1, -1):
            obj_name = ObjectName(0, i, 0, -1)
            if StringFind(obj_name, aPrefix, 0) == 0:
                ObjectDelete(0, obj_name)

def SetPrefix():
    prefix = ''
    period_current = Period()
    _sw1 = period_current
    if _sw1 == PERIOD_M15:
        prefix = 'StocksM15_' + Symbol() + '_'
    elif _sw1 == PERIOD_M12:
        prefix = 'StocksM12_' + Symbol() + '_'
    elif _sw1 == PERIOD_M10:
        prefix = 'StocksM10_' + Symbol() + '_'
    elif _sw1 == PERIOD_M6:
        prefix = 'StocksM6_' + Symbol() + '_'
    elif _sw1 == PERIOD_M5:
        prefix = 'StocksM5_' + Symbol() + '_'
    elif _sw1 == PERIOD_M4:
        prefix = 'StocksM15_' + Symbol() + '_'
    elif _sw1 == PERIOD_M3:
        prefix = 'StocksM3_' + Symbol() + '_'
    elif _sw1 == PERIOD_M2:
        prefix = 'StocksM2_' + Symbol() + '_'
    elif _sw1 == PERIOD_M1:
        prefix = 'StocksM1_' + Symbol() + '_'
    return prefix

def GetMultipier():
    period_current = Period()
    divisor = 1
    _sw2 = period_current
    if _sw2 == PERIOD_M15:
        divisor = 15
    elif _sw2 == PERIOD_M12:
        divisor = 12
    elif _sw2 == PERIOD_M10:
        divisor = 10
    elif _sw2 == PERIOD_M6:
        divisor = 6
    elif _sw2 == PERIOD_M5:
        divisor = 5
    elif _sw2 == PERIOD_M4:
        divisor = 4
    elif _sw2 == PERIOD_M3:
        divisor = 3
    elif _sw2 == PERIOD_M2:
        divisor = 2
    elif _sw2 == PERIOD_M1:
        divisor = 1
    return _idiv(60, divisor)

def OnInit():
    global m_daily_stocks, stop_running
    if Period() > PERIOD_M15:
        stop_running = True
        return INIT_SUCCEEDED
    ArraySetAsSeries(DTime, True)
    ArrayResize(DTime, ipt_total)
    aPrefix = SetPrefix()
    for i in range(0, ipt_total):
        DTime[i] = TimeCurrent()
    m_daily_stocks = CGOStocksContainer(DTime, ipt_top, ipt_down, ipt_scheme, aPrefix, ipt_total)
    m_daily_stocks.SetAllStocks()
    m_daily_stocks.ReDraw()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if stop_running:
        return
    aPrefix = SetPrefix()
    m_daily_stocks.DeleteByPrefix(aPrefix)
    _delete(m_daily_stocks)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_currentBarTimeOpen
    if stop_running:
        return rates_total
    ArraySetAsSeries(time, True)
    xdist = 0
    ydist = 0
    win_height = Box(-1)
    ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, 0, win_height)
    if _s_OnCalculate_currentBarTimeOpen != time[0]:
        for i in range(0, ipt_total):
            _s_OnCalculate_currentBarTimeOpen = time[0]
            DTime[i] = time[i * (24 * GetMultipier())]
        m_daily_stocks.ProcessingAllStocks(DTime)
        m_daily_stocks.ReDraw()
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if stop_running:
        Alert(' Period must be equal or less than 15 minutes.')
        return
    m_daily_stocks.ProcessingAllStocks(DTime)
    m_daily_stocks.ReDraw()

# ---- static local variables
_s_OnCalculate_currentBarTimeOpen = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stocksbg(_MQL5Indicator):
    name = 'stocksbg'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ipt_top': 0,  # Top indent
        'ipt_down': 20,  # Bottom indent
        'ipt_scheme': 0,  # Color scheme
        'ipt_total': 4,  # Number of days to show
    }

