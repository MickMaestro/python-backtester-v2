"""USDX_Candle — converted from MQL5: MQL5 Indicators/USDX_Candle/USDX_Candle.mq5

USD Index Candle
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

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 29, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [7451452, 42495, 8421504]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['USD Index Candle'], 'name': 'USDX_Candle', 'source': 'MQL5 Indicators/USDX_Candle/USDX_Candle.mq5', 'folder': 'USDX_Candle', 'inputs': [{'mql': 'InpReverse', 'py': 'InpReverse', 'param': 'InpReverse', 'type': 'int', 'default': 0, 'label': 'Reverse', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpReverse = _input('InpReverse', INPUT_NO)  # Reverse
BufferUSDX_O = Arr(0, 0.0)
BufferUSDX_H = Arr(0, 0.0)
BufferUSDX_L = Arr(0, 0.0)
BufferUSDX_C = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
scale_factor = 0.0
symbols = Arr.of(['EURUSD', 'USDJPY', 'GBPUSD', 'USDCAD', 'USDSEK', 'USDCHF'], fill="")
weights = Arr.of([-0.576, 0.136, -0.119, 0.091, 0.042, 0.036], fill=0.0)
timeframes = Arr.of([PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)

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
    _q_fields = ('m_symbol_name', 'm_weight', 'm_bars', 'm_handle_o', 'm_handle_h', 'm_handle_l', 'm_handle_c', 'm_buffer_o', 'm_buffer_h', 'm_buffer_l', 'm_buffer_c')
    def __init__(self, symbol_name):
        CObject.__init__(self)
        self.m_symbol_name = ""
        self.m_weight = 0.0
        self.m_bars = 0
        self.m_handle_o = 0
        self.m_handle_h = 0
        self.m_handle_l = 0
        self.m_handle_c = 0
        self.m_buffer_o = Arr(0, 0.0)
        self.m_buffer_h = Arr(0, 0.0)
        self.m_buffer_l = Arr(0, 0.0)
        self.m_buffer_c = Arr(0, 0.0)
        self.m_weight = 0.0
        self.m_bars = 0
        self.m_symbol_name = symbol_name
    def _q_dtor(self):
        pass
    def HandleO_1(self, handle):
        self.m_handle_o = handle
    def HandleO_0(self):
        return self.m_handle_o
    def HandleH_1(self, handle):
        self.m_handle_h = handle
    def HandleH_0(self):
        return self.m_handle_h
    def HandleL_1(self, handle):
        self.m_handle_l = handle
    def HandleL_0(self):
        return self.m_handle_l
    def HandleC_1(self, handle):
        self.m_handle_c = handle
    def HandleC_0(self):
        return self.m_handle_c
    def Symbol_1(self, symbol):
        self.m_symbol_name = symbol
    def Symbol_0(self):
        return self.m_symbol_name
    def Weight_1(self, weight):
        self.m_weight = weight
    def Weight_0(self):
        return self.m_weight
    def Bars_1(self, bars):
        self.m_bars = bars
    def Bars_0(self):
        return self.m_bars
    def Refresh_0(self):
        array = Arr(0, 0)
        return CopyTime(self.m_symbol_name, PERIOD_CURRENT, 0, 1, array) == 1
    def Refresh_1(self, timeframe):
        array = Arr(0, 0)
        CopyTime(self.m_symbol_name, timeframe, 0, 1, array)

def OnInit():
    SetIndexBuffer(0, BufferUSDX_O, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUSDX_H, INDICATOR_DATA)
    SetIndexBuffer(2, BufferUSDX_L, INDICATOR_DATA)
    SetIndexBuffer(3, BufferUSDX_C, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    EventSetTimer(90)
    total = ArraySize(symbols)
    list_instruments.Clear()
    index_buffer = 1
    for i in range(0, total):
        symbol = symbols[i]
        if not SymbolCheck(symbol):
            continue
        instr = CInstrument(symbol)
        if instr is None:
            continue
        instr.Weight_1(weights[i])
        ResetLastError()
        handle_o = iMA(symbol, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_OPEN)
        if handle_o == INVALID_HANDLE:
            Print('The ', symbol, ' iMA(1) by PRICE_OPEN object was not created: Error ', GetLastError())
            continue
        handle_h = iMA(symbol, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_HIGH)
        if handle_h == INVALID_HANDLE:
            Print('The ', symbol, ' iMA(1) by PRICE_HIGH object was not created: Error ', GetLastError())
            continue
        handle_l = iMA(symbol, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_LOW)
        if handle_l == INVALID_HANDLE:
            Print('The ', symbol, ' iMA(1) by PRICE_LOW object was not created: Error ', GetLastError())
            continue
        handle_c = iMA(symbol, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_CLOSE)
        if handle_c == INVALID_HANDLE:
            Print('The ', symbol, ' iMA(1) by PRICE_CLOSE object was not created: Error ', GetLastError())
            continue
        instr.HandleO_1(handle_o)
        instr.HandleH_1(handle_h)
        instr.HandleL_1(handle_l)
        instr.HandleC_1(handle_c)
        index_buffer += 4
        SetIndexBuffer(index_buffer, instr.m_buffer_o, INDICATOR_CALCULATIONS)
        SetIndexBuffer(index_buffer + 1, instr.m_buffer_h, INDICATOR_CALCULATIONS)
        SetIndexBuffer(index_buffer + 2, instr.m_buffer_l, INDICATOR_CALCULATIONS)
        SetIndexBuffer(index_buffer + 3, instr.m_buffer_c, INDICATOR_CALCULATIONS)
        ArraySetAsSeries(instr.m_buffer_o, True)
        ArraySetAsSeries(instr.m_buffer_h, True)
        ArraySetAsSeries(instr.m_buffer_l, True)
        ArraySetAsSeries(instr.m_buffer_c, True)
        list_instruments.Add(instr)
    IndicatorSetString(INDICATOR_SHORTNAME, 'USD Index Candle')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUSDX_O, True)
    ArraySetAsSeries(BufferUSDX_H, True)
    ArraySetAsSeries(BufferUSDX_L, True)
    ArraySetAsSeries(BufferUSDX_C, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(time, True)
    total = list_instruments.Total()
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferUSDX_O, EMPTY_VALUE)
        ArrayInitialize(BufferUSDX_H, EMPTY_VALUE)
        ArrayInitialize(BufferUSDX_L, EMPTY_VALUE)
        ArrayInitialize(BufferUSDX_C, EMPTY_VALUE)
        for j in range(0, total):
            instr = list_instruments.At(j)
            if instr is None:
                continue
            ArrayInitialize(instr.m_buffer_o, 0)
            ArrayInitialize(instr.m_buffer_h, 0)
            ArrayInitialize(instr.m_buffer_l, 0)
            ArrayInitialize(instr.m_buffer_c, 0)
            bars = (rates_total if (instr.Symbol_0() == Symbol()) else Bars(instr.Symbol_0(), PERIOD_CURRENT))
            instr.Bars_1(bars)
    min_bars = rates_total
    for j in range(0, total):
        instr = list_instruments.At(j)
        if instr is None:
            continue
        instr.Refresh_0()
        bars = (rates_total if (instr.Symbol_0() == Symbol()) else Bars(instr.Symbol_0(), PERIOD_CURRENT))
        if bars < min_bars:
            min_bars = bars
        copied = 0
        count = (1 if (limit == 0) else rates_total if (instr.Symbol_0() == Symbol()) else instr.Bars_0())
        copied = CopyBuffer(instr.HandleO_0(), 0, 0, count, instr.m_buffer_o)
        if copied <= 0:
            return 0
        copied = CopyBuffer(instr.HandleH_0(), 0, 0, count, instr.m_buffer_h)
        if copied <= 0:
            return 0
        copied = CopyBuffer(instr.HandleL_0(), 0, 0, count, instr.m_buffer_l)
        if copied <= 0:
            return 0
        copied = CopyBuffer(instr.HandleC_0(), 0, 0, count, instr.m_buffer_c)
        if copied <= 0:
            return 0
    limit1 = ((min_bars - 1) if (limit > 1) else 0)
    for i in range(limit1, 0 - 1, -1):
        xO = 50.14348112
        xH = 50.14348112
        xL = 50.14348112
        xC = 50.14348112
        for j in range(0, total):
            instr = list_instruments.At(j)
            if instr is None:
                continue
            symbol = instr.Symbol_0()
            bar = BarShift(symbol, PERIOD_CURRENT, Time(symbol, i))
            if bar == WRONG_VALUE or bar > (instr.Bars_0() - 1):
                continue
            power = instr.Weight_0()
            price_ma_o = instr.m_buffer_o[bar]
            coeff_o = pow(price_ma_o, power)
            xO *= coeff_o
            price_ma_h = instr.m_buffer_h[bar]
            coeff_h = pow(price_ma_h, power)
            xH *= coeff_h
            price_ma_l = instr.m_buffer_l[bar]
            coeff_l = pow(price_ma_l, power)
            xL *= coeff_l
            price_ma_c = instr.m_buffer_c[bar]
            coeff_c = pow(price_ma_c, power)
            xC *= coeff_c
        BufferUSDX_O[i] = (_fdiv(1, xO) if InpReverse else xO)
        BufferUSDX_H[i] = (_fdiv(1, xH) if InpReverse else xH)
        BufferUSDX_L[i] = (_fdiv(1, xL) if InpReverse else xL)
        BufferUSDX_C[i] = (_fdiv(1, xC) if InpReverse else xC)
        BufferColors[i] = (0 if (BufferUSDX_O[i] < BufferUSDX_C[i]) else 1 if (BufferUSDX_O[i] > BufferUSDX_C[i]) else 2)
    return rates_total

def OnTimer():
    total = list_instruments.Total()
    for i in range(0, total):
        instr = list_instruments.At(i)
        if instr is None:
            continue
        count = 9
        for j in range(0, count):
            timeframe = timeframes[j]
            instr.Refresh_1(timeframe)

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

def Time(symbol_name, shift):
    array = Arr(0, 0)
    if CopyTime(symbol_name, PERIOD_CURRENT, shift, 1, array) == 1:
        return array[0]
    return 0

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


class USDXCandle(_MQL5Indicator):
    name = 'USDX_Candle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpReverse': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Reverse
    }

