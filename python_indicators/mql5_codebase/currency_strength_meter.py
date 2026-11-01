"""Currency Strength Meter — converted from MQL5: MQL5 Indicators/Currency Strength Meter MT5/Currency Strength Meter.mq5

Copyright: Copyright 2021, aligroup™; Link: https://www.aligroup.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Functions not available here: FileReadLong, FileWriteLong
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2021, aligroup™', 'link': 'https://www.aligroup.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Currency Strength Meter', 'source': 'MQL5 Indicators/Currency Strength Meter MT5/Currency Strength Meter.mq5', 'folder': 'Currency Strength Meter MT5', 'inputs': [{'mql': 'RefreshRate', 'py': 'RefreshRate', 'param': 'RefreshRate', 'type': 'int', 'default': 100, 'label': 'Refresh Rate (Milliseconds)', 'sinput': False}, {'mql': 'SHOW_CURRENCIES', 'py': 'SHOW_CURRENCIES', 'param': 'SHOW_CURRENCIES', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'SHOW_CHART_PAIR', 'py': 'SHOW_CHART_PAIR', 'param': 'SHOW_CHART_PAIR', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'SHOW_COMMENT', 'py': 'SHOW_COMMENT', 'param': 'SHOW_COMMENT', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'timeframe', 'py': 'timeframe', 'param': 'timeframe', 'type': 'int', 'default': 16408, 'label': 'Strength Timeframe', 'sinput': False}, {'mql': 'CurrencyPairs', 'py': 'CurrencyPairs', 'param': None, 'type': 'string', 'default': 'AUDCAD,AUDCHF,AUDJPY,AUDNZD,AUDUSD,CADCHF,CADJPY,CHFJPY,EURAUD,EURCAD,EURCHF,EURGBP,EURJPY,EURNZD,EURUSD,GBPAUD,GBPCAD,GBPCHF,GBPJPY,GBPNZD,GBPUSD,NZDCAD,NZDCHF,NZDJPY,NZDUSD,USDCAD,USDCHF,USDJPY', 'label': '28 pairs', 'sinput': False}, {'mql': 'FontName', 'py': 'FontName', 'param': None, 'type': 'string', 'default': 'Calibri', 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'HorizPos', 'py': 'HorizPos', 'param': 'HorizPos', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'VertPos', 'py': 'VertPos', 'param': 'VertPos', 'type': 'int', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'VertSpacing', 'py': 'VertSpacing', 'param': 'VertSpacing', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'Color1', 'py': 'Color1', 'param': None, 'type': 'color', 'default': 8721863, 'label': '', 'sinput': False}, {'mql': 'Level1', 'py': 'Level1', 'param': 'Level1', 'type': 'double', 'default': 7.0, 'label': '', 'sinput': False}, {'mql': 'Color2', 'py': 'Color2', 'param': None, 'type': 'color', 'default': 25600, 'label': '', 'sinput': False}, {'mql': 'Level2', 'py': 'Level2', 'param': 'Level2', 'type': 'double', 'default': 5.0, 'label': '', 'sinput': False}, {'mql': 'Color3', 'py': 'Color3', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'Level3', 'py': 'Level3', 'param': 'Level3', 'type': 'double', 'default': 2.9, 'label': '', 'sinput': False}, {'mql': 'Color4', 'py': 'Color4', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'Level4', 'py': 'Level4', 'param': 'Level4', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'ShowNoOfPairs', 'py': 'ShowNoOfPairs', 'param': 'ShowNoOfPairs', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SortDescending', 'py': 'SortDescending', 'param': 'SortDescending', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
RefreshRate = _input('RefreshRate', 100)  # Refresh Rate (Milliseconds)
SHOW_CURRENCIES = _input('SHOW_CURRENCIES', True)
SHOW_CHART_PAIR = _input('SHOW_CHART_PAIR', True)
SHOW_COMMENT = _input('SHOW_COMMENT', False)
timeframe = _input('timeframe', PERIOD_D1)  # Strength Timeframe
CurrencyPairs = _input('CurrencyPairs', 'AUDCAD,AUDCHF,AUDJPY,AUDNZD,AUDUSD,CADCHF,CADJPY,CHFJPY,EURAUD,EURCAD,EURCHF,EURGBP,EURJPY,EURNZD,EURUSD,GBPAUD,GBPCAD,GBPCHF,GBPJPY,GBPNZD,GBPUSD,NZDCAD,NZDCHF,NZDJPY,NZDUSD,USDCAD,USDCHF,USDJPY')  # 28 pairs
FontName = _input('FontName', 'Calibri')
FontSize = _input('FontSize', 12)
HorizPos = _input('HorizPos', 5)
VertPos = _input('VertPos', 200)
VertSpacing = _input('VertSpacing', 20)
Color1 = _input('Color1', clrMediumVioletRed)
Level1 = _input('Level1', 7.0)
Color2 = _input('Color2', clrDarkGreen)
Level2 = _input('Level2', 5.0)
Color3 = _input('Color3', clrBlue)
Level3 = _input('Level3', 2.9)
Color4 = _input('Color4', clrRed)
Level4 = _input('Level4', 0.0)
ShowNoOfPairs = _input('ShowNoOfPairs', False)
SortDescending = _input('SortDescending', True)
busy = False
ccy_count = Arr(8, 0, dyn=False)
myCorner = CORNER_RIGHT_UPPER
BaseVal = 0.0
QuoteVal = 0.0
PairVal = 0.0
ccy_strength = Arr(8, 0.0, dyn=False)
BaseCur = ""
QuoteCur = ""
tMessage = ""

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

def OnInit():
    global BaseCur, QuoteCur
    SymbolGroups.Add('AUD')
    SymbolGroups.Add('CAD')
    SymbolGroups.Add('CHF')
    SymbolGroups.Add('EUR')
    SymbolGroups.Add('GBP')
    SymbolGroups.Add('JPY')
    SymbolGroups.Add('NZD')
    SymbolGroups.Add('USD')
    if CurrencyPairs == '':
        Symbols.Clear()
        Symbols.Add(Symbol())
    else:
        Symbols.Clear()
        ArraySplitResult = Arr(0, "")
        tradesResult = StringSplit(CurrencyPairs, StringGetCharacter(',', 0), ArraySplitResult)
        for i in range(0, tradesResult):
            symbol = ArraySplitResult[i]
            if StringLen(symbol) == 6 and Symbols.SearchFirst(symbol) == -1:
                if AddSymbolToMarketWatch(symbol):
                    Symbols.Add(symbol)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Currecy Strength Meter')
    BaseCur = StringSubstr(Symbol(), 0, 3)
    QuoteCur = StringSubstr(Symbol(), 3, 3)
    Refresh_CS_Data()
    EventSetMillisecondTimer(RefreshRate)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    EventKillTimer()
    ObjectsDeleteAll(0, obj_name_prefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnTimer():
    global _s_OnTimer_LastTime, busy
    if not busy:
        busy = True
        isTicking = False
        CurrentTime = TimeCurrent()
        _s_OnTimer_LastTime = (CurrentTime if (isTicking := CurrentTime > _s_OnTimer_LastTime) else _s_OnTimer_LastTime)
        if isTicking:
            Refresh_CS_Data()
        busy = False

def Refresh_CS_Data():
    global BaseVal, PairVal, QuoteVal, tMessage
    ArrayInitialize(ccy_strength, 0.0)
    ArrayInitialize(ccy_count, 0)
    i = 0
    while i < Symbols.Total():
        ind_strength = 0.0
        symbol = _str(Symbols[i])
        day_high = iHigh(symbol, timeframe, 0)
        day_low = iLow(symbol, timeframe, 0)
        bid_ratio = 100.0 * DivZero(SymbolInfoDouble(symbol, SYMBOL_BID) - day_low, day_high - day_low)
        if bid_ratio > 3.0:
            ind_strength = 1.0
        if bid_ratio > 10.0:
            ind_strength = 2.0
        if bid_ratio > 25.0:
            ind_strength = 3.0
        if bid_ratio > 40.0:
            ind_strength = 4.0
        if bid_ratio > 50.0:
            ind_strength = 5.0
        if bid_ratio > 60.0:
            ind_strength = 6.0
        if bid_ratio > 75.0:
            ind_strength = 7.0
        if bid_ratio > 90.0:
            ind_strength = 8.0
        if bid_ratio > 97.0:
            ind_strength = 9.0
        j = 0
        while j < SymbolGroups.Total():
            if SymbolGroups[j] == StringSubstr(symbol, 0, 3):
                ccy_strength[j] += ind_strength
                ccy_count[j] += 1
                break
            j += 1
        j = 0
        while j < SymbolGroups.Total():
            if SymbolGroups[j] == StringSubstr(symbol, 3, 3):
                ccy_strength[j] += SymbolGroups.Total() + 1 - ind_strength
                ccy_count[j] += 1
                break
            j += 1
        i += 1
    length = 0
    average_strength = 0.0
    array_to_sort = Arr(8, "", dyn=False)
    display_txt = ""
    j = 0
    while j < SymbolGroups.Total():
        array_to_sort[j] = ''
        average_strength = DivZero(ccy_strength[j], ccy_count[j])
        if SymbolGroups[j] == BaseCur:
            BaseVal = average_strength
            basej = j
        if SymbolGroups[j] == QuoteCur:
            QuoteVal = average_strength
            quotej = j
        display_txt = DoubleToString(average_strength, 1) + _str(SymbolGroups[j])
        length = StringLen(DoubleToString(average_strength, 1))
        if ShowNoOfPairs:
            display_txt = display_txt + DoubleToString(ccy_count[j], 0)
        array_to_sort[j] = display_txt
        j += 1
    xp = HorizPos
    yp = VertPos
    ShellsortStringArray(array_to_sort, SortDescending)
    j = 0
    while j < SymbolGroups.Total():
        FontColor = clrWhite
        average_strength = StringToDouble(StringSubstr(array_to_sort[j], 0, length))
        display_txt = StringSubstr(array_to_sort[j], length, 3) + '    ' + DoubleToString(average_strength, 1)
        if ShowNoOfPairs:
            display_txt = display_txt + ' (' + StringSubstr(array_to_sort[j], length + 3) + ')'
        if SHOW_CURRENCIES:
            if average_strength >= Level4:
                FontColor = Color4
            if average_strength > Level3:
                FontColor = Color3
            if average_strength > Level2:
                FontColor = Color2
            if average_strength > Level1:
                FontColor = Color1
            display_txt = StringRightPad(display_txt, 16, ' ')
            CreateTextLabel(obj_name_prefix, _str(j), display_txt, xp, yp, FontColor, FontSize, myCorner)
            yp += VertSpacing
        j += 1
    FontColor = clrWhite
    PairVal = BaseVal - QuoteVal
    _sw1 = (1 if (PairVal > 0.0) else -1 if (PairVal < 0.0) else 0)
    if _sw1 == 1:
        FontColor = clrGreen
        tMessage = 'BUY   '
    elif _sw1 == -1:
        FontColor = clrRed
        tMessage = 'SELL  '
    else:
        FontColor = clrDimGray
        tMessage = 'WAIT  '
    if SHOW_CHART_PAIR:
        display_txt = GetTimeFrame(timeframe) + ': ' + Symbol() + ' ' + DoubleToString(PairVal, 1) + ' ' + tMessage
        CreateTextLabel(obj_name_prefix, 'active_chart', display_txt, xp, yp, FontColor, FontSize, myCorner)
        yp += VertSpacing
    if SHOW_COMMENT:
        Comment(BaseCur + ' ' + DoubleToString(BaseVal, Digits()), '\n', QuoteCur + ' ' + DoubleToString(QuoteVal, Digits()), '\n', Symbol() + ' ' + DoubleToString(PairVal, Digits()) + ' ' + tMessage, '\n', '')

def StringRightPad(str_, n=1, str2=' '):
    return str_ + StringRepeat(str2, n - StringLen(str_))

def StringRepeat(str_, n=1):
    outstr = ''
    for i in range(0, n):
        outstr = outstr + str_
    return outstr

def DivZero(n, d):
    return (0 if (d == 0) else _fdiv(1.0 * n, d))

def ShellsortStringArray(array, desc=False):
    mid = ""
    n = ArraySize(array)
    j = 0
    i = 0
    m = 0
    m = _idiv(n, 2)
    while m > 0:
        j = m
        for j in range(j, n):
            i = j - m
            while i >= 0:
                if desc:
                    if array[i + m] <= array[i]:
                        break
                    else:
                        mid = array[i]
                        array[i] = array[i + m]
                        array[i + m] = mid
                else:
                    if array[i + m] >= array[i]:
                        break
                    else:
                        mid = array[i]
                        array[i] = array[i + m]
                        array[i + m] = mid
                i -= m
        else:
            j = _range_end(j, n, 1)
        m = _idiv(m, 2)

def CreateTextLabel(obj_prefix, obj_label, obj_text, x_dist, y_dist, text_color, font_size, obj_corner):
    obj_label = obj_prefix + obj_label
    if ObjectFind(0, obj_label) >= 0:
        ObjectSetString(0, obj_label, OBJPROP_TEXT, obj_text)
        ObjectSetInteger(0, obj_label, OBJPROP_COLOR, text_color)
    else:
        if ObjectCreate(0, obj_label, OBJ_LABEL, 0, 0, 0):
            _sw2 = obj_corner
            if _sw2 == CORNER_LEFT_UPPER:
                ObjectSetInteger(0, obj_label, OBJPROP_ALIGN, ALIGN_LEFT)
                ObjectSetInteger(0, obj_label, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
            elif _sw2 == CORNER_RIGHT_UPPER:
                ObjectSetInteger(0, obj_label, OBJPROP_ALIGN, ALIGN_RIGHT)
                ObjectSetInteger(0, obj_label, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
            elif _sw2 == CORNER_LEFT_LOWER:
                ObjectSetInteger(0, obj_label, OBJPROP_ALIGN, ALIGN_LEFT)
                ObjectSetInteger(0, obj_label, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
            elif _sw2 == CORNER_RIGHT_LOWER:
                ObjectSetInteger(0, obj_label, OBJPROP_ALIGN, ALIGN_RIGHT)
                ObjectSetInteger(0, obj_label, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
            ObjectSetInteger(0, obj_label, OBJPROP_CORNER, obj_corner)
            ObjectSetString(0, obj_label, OBJPROP_TEXT, obj_text)
            ObjectSetInteger(0, obj_label, OBJPROP_COLOR, text_color)
            ObjectSetInteger(0, obj_label, OBJPROP_FONTSIZE, font_size)
            ObjectSetInteger(0, obj_label, OBJPROP_XDISTANCE, x_dist)
            ObjectSetInteger(0, obj_label, OBJPROP_YDISTANCE, y_dist)
        else:
            Print('CreateTextLabel', ': failed to create text label! Error code: ', GetLastError())

def AddSymbolToMarketWatch(symbol):
    i = 0
    while i < SymbolsTotal(False):
        name = SymbolName(i, False)
        if name == symbol:
            return SymbolSelect(name, True)
        i += 1
    return False

def GetTimeFrame(tf):
    tf = (Period() if (tf == PERIOD_CURRENT) else tf)
    period_xxx = EnumToString(tf, 'ENUM_TIMEFRAMES')
    return StringSubstr(period_xxx, 7)

# ---- global variables initialised from expressions
SymbolGroups = _alloc(CArrayString)
SymbolGroups.__init__()
Symbols = _alloc(CArrayString)
Symbols.__init__()
obj_name_prefix = '_CurrencyStrength_' + _str(timeframe)

# ---- static local variables
_s_OnTimer_LastTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CurrencyStrengthMeter(_MQL5Indicator):
    name = 'Currency Strength Meter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RefreshRate': 100,  # Refresh Rate (Milliseconds)
        'SHOW_CURRENCIES': True,
        'SHOW_CHART_PAIR': True,
        'SHOW_COMMENT': False,
        'timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Strength Timeframe
        'FontSize': 12,
        'HorizPos': 5,
        'VertPos': 200,
        'VertSpacing': 20,
        'Level1': 7.0,
        'Level2': 5.0,
        'Level3': 2.9,
        'Level4': 0.0,
        'ShowNoOfPairs': False,
        'SortDescending': True,
    }

