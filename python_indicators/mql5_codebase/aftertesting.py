"""aftertesting — converted from MQL5: MQL5 Indicators/After Testing - Analysis of Operations/aftertesting.mq5

Copyright: Copyright 2015, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

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

MQL5_META = {'props': {'copyright': 'Copyright 2015, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'aftertesting', 'source': 'MQL5 Indicators/After Testing - Analysis of Operations/aftertesting.mq5', 'folder': 'After Testing - Analysis of Operations', 'inputs': [{'mql': 'DrawArrow', 'py': 'DrawArrow', 'param': 'DrawArrow', 'type': 'bool', 'default': True, 'label': 'Рисовать стрелки', 'sinput': False}, {'mql': 'BuyLineColor', 'py': 'BuyLineColor', 'param': None, 'type': 'color', 'default': 11296515, 'label': 'Цвет покупки', 'sinput': False}, {'mql': 'BuyWidth', 'py': 'BuyWidth', 'param': 'BuyWidth', 'type': 'int', 'default': 2, 'label': 'Толщина линии', 'sinput': False}, {'mql': 'SellLineColor', 'py': 'SellLineColor', 'param': None, 'type': 'color', 'default': 1918177, 'label': 'Цвет продажи', 'sinput': False}, {'mql': 'SellWidth', 'py': 'SellWidth', 'param': 'SellWidth', 'type': 'int', 'default': 2, 'label': 'Толщина линии', 'sinput': False}, {'mql': 'ClrStartPos', 'py': 'ClrStartPos', 'param': None, 'type': 'color', 'default': 65535, 'label': '', 'sinput': False}, {'mql': 'ClrEndPos', 'py': 'ClrEndPos', 'param': None, 'type': 'color', 'default': 13749760, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
DrawArrow = _input('DrawArrow', True)  # Рисовать стрелки
BuyLineColor = _input('BuyLineColor', 0xAC5F03)  # Цвет покупки
BuyWidth = _input('BuyWidth', 2)  # Толщина линии
SellLineColor = _input('SellLineColor', 0x1D44E1)  # Цвет продажи
SellWidth = _input('SellWidth', 2)  # Толщина линии
ClrStartPos = _input('ClrStartPos', clrYellow)
ClrEndPos = _input('ClrEndPos', clrDarkTurquoise)
historyList = None
clrBuy = 0xAC5F03
clrSell = 0x1D44E1
btn_background_color = 0xA67626  # Цвет кнопки при наведении курсора
btn_std_color = clrGray  # стандартный цвет кнопок
btnIdShowBuy = 'ShowBuy'
btnIdShowSell = 'ShowSell'
btnIdShowWinners = 'ShowWinners'
btnIdShowLosses = 'ShowLosses'
btnIdStartPoint = 'StartPoint'
btnIdEndPoint = 'EndPoint'
buttonsArr = Arr.of(['ShowBuy', 'ShowSell', 'ShowWinners', 'ShowLosses', 'StartPoint', 'EndPoint'], fill="")
btnStateShowBuy = True
btnStateShowSell = True
btnStateShowWinners = False
btnStateShowLosses = False
btnStateStartPoint = False
btnStateEndPoint = False

class CList(CObject):
    _q_fields = ('m_first_node', 'm_last_node', 'm_curr_node', 'm_curr_idx', 'm_data_total', 'm_free_mode', 'm_data_sort', 'm_sort_mode')
    _q_ptrs = ('m_first_node', 'm_last_node', 'm_curr_node',)
    def __init__(self):
        CObject.__init__(self)
        self.m_first_node = None
        self.m_last_node = None
        self.m_curr_node = None
        self.m_curr_idx = 0
        self.m_data_total = 0
        self.m_free_mode = False
        self.m_data_sort = False
        self.m_sort_mode = 0
        self.m_first_node = None
        self.m_last_node = None
        self.m_curr_node = None
        self.m_curr_idx = -1
        self.m_data_total = 0
        self.m_free_mode = True
        self.m_data_sort = False
        self.m_sort_mode = 0
    def _q_dtor(self):
        self.Clear()
    def FreeMode_0(self):
        return self.m_free_mode
    def FreeMode_1(self, mode):
        self.m_free_mode = mode
    def Total(self):
        return self.m_data_total
    def IsSorted(self):
        return self.m_data_sort
    def SortMode(self):
        return self.m_sort_mode
    def Type(self):
        return 0x7779
    def Save(self, file_handle):
        node = None
        result = True
        if (not CheckPointer(self.m_curr_node)) or file_handle == INVALID_HANDLE:
            return False
        if _missing('FileWriteLong')(file_handle, -1) != 8:
            return False
        if FileWriteInteger(file_handle, self.Type(), INT_VALUE) != INT_VALUE:
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        node = self.m_first_node
        while node is not None:
            result &= node.Save(file_handle)
            node = node.Next_0()
        return result
    def Load(self, file_handle):
        i = 0
        num = 0
        node = None
        result = True
        if file_handle == INVALID_HANDLE:
            return False
        if _missing('FileReadLong')(file_handle) != -1:
            return False
        if FileReadInteger(file_handle, INT_VALUE) != self.Type():
            return False
        num = FileReadInteger(file_handle, INT_VALUE)
        self.Clear()
        i = 0
        for i in range(i, num):
            node = self.CreateElement()
            if node is None:
                return False
            self.Add(node)
            result &= node.Load(file_handle)
        else:
            i = _range_end(i, num, 1)
        return result
    def CreateElement(self):
        return None
    def Add(self, new_node):
        if not CheckPointer(new_node):
            return -1
        if self.m_first_node is None:
            self.m_first_node = new_node
        else:
            self.m_last_node.Next_1(new_node)
            new_node.Prev_1(self.m_last_node)
        self.m_curr_node = new_node
        self.m_curr_idx = self.m_data_total
        self.m_last_node = new_node
        self.m_data_sort = False
        return _incattr(self, 'm_data_total', 1, True)
    def Insert(self, new_node, index):
        tmp_node = None
        if not CheckPointer(new_node):
            return -1
        if index > self.m_data_total or index < 0:
            return -1
        if index == -1:
            if self.m_curr_node is None:
                return self.Add(new_node)
        else:
            if self.GetNodeAtIndex(index) is None:
                return self.Add(new_node)
        tmp_node = self.m_curr_node.Prev_0()
        new_node.Prev_1(tmp_node)
        if tmp_node is not None:
            tmp_node.Next_1(new_node)
        else:
            self.m_first_node = new_node
        new_node.Next_1(self.m_curr_node)
        self.m_curr_node.Prev_1(new_node)
        self.m_data_total += 1
        self.m_data_sort = False
        self.m_curr_node = new_node
        return index
    def IndexOf(self, node):
        if (not CheckPointer(node)) or (not CheckPointer(self.m_curr_node)):
            return -1
        if node == self.m_curr_node:
            return self.m_curr_idx
        if self.GetFirstNode() == node:
            return 0
        i = 1
        while i < self.m_data_total:
            if self.GetNextNode() == node:
                return i
            i += 1
        return -1
    def GetNodeAtIndex(self, index):
        i = 0
        revers = False
        result = None
        if index >= self.m_data_total:
            return None
        if index == self.m_curr_idx:
            return self.m_curr_node
        if index < self.m_curr_idx:
            if (self.m_curr_idx - index) < index:
                i = self.m_curr_idx
                revers = True
                result = self.m_curr_node
            else:
                i = 0
                revers = False
                result = self.m_first_node
        else:
            if (index - self.m_curr_idx) < (self.m_data_total - index - 1):
                i = self.m_curr_idx
                revers = False
                result = self.m_curr_node
            else:
                i = self.m_data_total - 1
                revers = True
                result = self.m_last_node
        if not CheckPointer(result):
            return None
        if revers:
            while i > index:
                result = result.Prev_0()
                if result is None:
                    return None
                i -= 1
        else:
            while i < index:
                result = result.Next_0()
                if result is None:
                    return None
                i += 1
        self.m_curr_idx = index
        return _setattr(self, 'm_curr_node', result)
    def GetFirstNode(self):
        if not CheckPointer(self.m_first_node):
            return None
        self.m_curr_idx = 0
        return _setattr(self, 'm_curr_node', self.m_first_node)
    def GetPrevNode(self):
        if (not CheckPointer(self.m_curr_node)) or self.m_curr_node.Prev_0() is None:
            return None
        self.m_curr_idx -= 1
        return _setattr(self, 'm_curr_node', self.m_curr_node.Prev_0())
    def GetCurrentNode(self):
        return self.m_curr_node
    def GetNextNode(self):
        if (not CheckPointer(self.m_curr_node)) or self.m_curr_node.Next_0() is None:
            return None
        self.m_curr_idx += 1
        return _setattr(self, 'm_curr_node', self.m_curr_node.Next_0())
    def GetLastNode(self):
        if not CheckPointer(self.m_last_node):
            return None
        self.m_curr_idx = self.m_data_total - 1
        return _setattr(self, 'm_curr_node', self.m_last_node)
    def DetachCurrent(self):
        tmp_node = None
        result = None
        if not CheckPointer(self.m_curr_node):
            return result
        result = self.m_curr_node
        self.m_curr_node = None
        if (tmp_node := result.Next_0()) is not None:
            tmp_node.Prev_1(result.Prev_0())
            self.m_curr_node = tmp_node
        if (tmp_node := result.Prev_0()) is not None:
            tmp_node.Next_1(result.Next_0())
            if self.m_curr_node is None:
                self.m_curr_node = tmp_node
                self.m_curr_idx = self.m_data_total - 2
        self.m_data_total -= 1
        if self.m_first_node == result:
            self.m_first_node = result.Next_0()
        if self.m_last_node == result:
            self.m_last_node = result.Prev_0()
        result.Prev_1(None)
        result.Next_1(None)
        return result
    def DeleteCurrent(self):
        result = self.DetachCurrent()
        if result is None:
            return False
        if self.m_free_mode:
            if CheckPointer(result) == POINTER_DYNAMIC:
                _delete(result)
        return True
    def Delete(self, index):
        if self.GetNodeAtIndex(index) is None:
            return False
        return self.DeleteCurrent()
    def Clear(self):
        self.GetFirstNode()
        while self.m_data_total != 0:
            if not self.DeleteCurrent():
                break
    def CompareList(self, List):
        node = None
        lnode = None
        if not CheckPointer(List):
            return False
        if (node := self.GetFirstNode()) is None:
            return False
        if (lnode := List.GetFirstNode()) is None:
            return False
        if node.Compare(lnode) != 0:
            return False
        while (node := self.GetNextNode()) is not None:
            if (lnode := List.GetNextNode()) is None:
                return False
            if node.Compare(lnode) != 0:
                return False
        return True
    def Sort(self, mode):
        if self.m_data_total == 0:
            return
        if self.m_data_sort and self.m_sort_mode == mode:
            return
        self.QuickSort(0, self.m_data_total - 1, mode)
        self.m_sort_mode = mode
        self.m_data_sort = True
    def MoveToIndex(self, index):
        if index >= self.m_data_total or (not CheckPointer(self.m_curr_node)):
            return False
        if self.m_curr_idx == index:
            return True
        if self.m_curr_idx < index:
            index -= 1
        self.Insert(self.DetachCurrent(), index)
        return True
    def Exchange(self, node1, node2):
        tmp_node = None
        node = None
        if (not CheckPointer(node1)) or (not CheckPointer(node2)):
            return False
        tmp_node = node1.Prev_0()
        node1.Prev_1(node2.Prev_0())
        if node1.Prev_0() is not None:
            node = node1.Prev_0()
            node.Next_1(node1)
        else:
            self.m_first_node = node1
        node2.Prev_1(tmp_node)
        if node2.Prev_0() is not None:
            node = node2.Prev_0()
            node.Next_1(node2)
        else:
            self.m_first_node = node2
        tmp_node = node1.Next_0()
        node1.Next_1(node2.Next_0())
        if node1.Next_0() is not None:
            node = node1.Next_0()
            node.Prev_1(node1)
        else:
            self.m_last_node = node1
        node2.Next_1(tmp_node)
        if node2.Next_0() is not None:
            node = node2.Next_0()
            node.Prev_1(node2)
        else:
            self.m_last_node = node2
        self.m_curr_idx = 0
        self.m_curr_node = self.m_first_node
        self.m_data_sort = False
        return True
    def Search(self, element):
        result = None
        if (not CheckPointer(element)) or (not self.m_data_sort):
            return None
        result = self.QuickSearch(element)
        return result
    def QuickSort(self, beg, end, mode):
        i = 0
        j = 0
        k = 0
        i_ptr = None
        j_ptr = None
        k_ptr = None
        i_ptr = self.GetNodeAtIndex((i := beg))
        j_ptr = self.GetNodeAtIndex((j := end))
        while i < end:
            k_ptr = self.GetNodeAtIndex((k := (beg + end) >> 1))
            while i < j:
                while i_ptr.Compare(k_ptr, mode) < 0:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                    i_ptr = i_ptr.Next_0()
                while j_ptr.Compare(k_ptr, mode) > 0:
                    if j == 0:
                        break
                    j -= 1
                    j_ptr = j_ptr.Prev_0()
                if i <= j:
                    self.Exchange(i_ptr, j_ptr)
                    i += 1
                    i_ptr = self.GetNodeAtIndex(i)
                    if j == 0:
                        break
                    else:
                        j -= 1
                        j_ptr = self.GetNodeAtIndex(j)
            if beg < j:
                self.QuickSort(beg, j, mode)
            beg = i
            i_ptr = self.GetNodeAtIndex((i := beg))
            j_ptr = self.GetNodeAtIndex((j := end))
    def QuickSearch(self, element):
        i = 0
        j = 0
        m = 0
        t_node = None
        if self.m_data_total == 0:
            return None
        i = 0
        j = self.m_data_total
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m >= self.m_data_total:
                break
            t_node = self.GetNodeAtIndex(m)
            if t_node.Compare(element, self.m_sort_mode) == 0:
                break
            if t_node.Compare(element, self.m_sort_mode) > 0:
                j = m - 1
            else:
                i = m + 1
            t_node = None
        return t_node

class COperation(CObject):
    _q_fields = ('m_Name', 'm_IsBuy', 'm_IsWinner', 'm_StartPosName', 'm_EndPosName', 'm_StartPosPrice', 'm_EndPosPrice', 'm_StartPosDt', 'm_EndPosDt')
    def __init__(self, *args):
        CObject.__init__(self)
        self.m_Name = ""
        self.m_IsBuy = False
        self.m_IsWinner = False
        self.m_StartPosName = ""
        self.m_EndPosName = ""
        self.m_StartPosPrice = 0.0
        self.m_EndPosPrice = 0.0
        self.m_StartPosDt = 0
        self.m_EndPosDt = 0

def OnInit():
    ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, True)
    CreateButtons()
    if not GetOperationsHistory():
        return INIT_FAILED
    OnButtonStateChanged()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0)
    Comment('')
    ChartSetInteger(0, CHART_MOUSE_SCROLL, True)
    ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, False)
    SetDefaultLines()
    if historyList is not None:
        _delete(historyList)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global btnStateEndPoint, btnStateShowBuy, btnStateShowLosses, btnStateShowSell, btnStateShowWinners, btnStateStartPoint
    if id_ == CHARTEVENT_OBJECT_CLICK:
        if sparam == btnIdShowBuy:
            btnStateShowBuy = (ObjectGetInteger(0, btnIdShowBuy, OBJPROP_STATE) != 0)
            OnButtonStateChanged()
        if sparam == btnIdShowSell:
            btnStateShowSell = (ObjectGetInteger(0, btnIdShowSell, OBJPROP_STATE) != 0)
            OnButtonStateChanged()
        if sparam == btnIdShowWinners:
            btnStateShowWinners = (ObjectGetInteger(0, btnIdShowWinners, OBJPROP_STATE) != 0)
            OnButtonStateChanged()
        if sparam == btnIdShowLosses:
            btnStateShowLosses = (ObjectGetInteger(0, btnIdShowLosses, OBJPROP_STATE) != 0)
            OnButtonStateChanged()
        if sparam == btnIdStartPoint:
            btnStateStartPoint = (ObjectGetInteger(0, btnIdStartPoint, OBJPROP_STATE) != 0)
            OnButtonStateChanged()
        if sparam == btnIdEndPoint:
            btnStateEndPoint = (ObjectGetInteger(0, btnIdEndPoint, OBJPROP_STATE) != 0)
            OnButtonStateChanged()
        ChartRedraw()
        return
    if id_ == CHARTEVENT_MOUSE_MOVE:
        name = Box('')
        if ButtonMouseMoveFocus(lparam, dparam, name):
            ChartSetInteger(0, CHART_MOUSE_SCROLL, False)
            ObjectSetInteger(0, name.v, OBJPROP_BGCOLOR, btn_background_color)
        else:
            SetButtonColorToDefalult()
            ChartSetInteger(0, CHART_MOUSE_SCROLL, True)
        ChartRedraw()
        return

def CreateButtons():
    ObjectCreate(0, btnIdShowBuy, OBJ_BUTTON, 0, 100, 100)
    ObjectSetInteger(0, btnIdShowBuy, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(0, btnIdShowBuy, OBJPROP_BGCOLOR, btn_std_color)
    ObjectSetInteger(0, btnIdShowBuy, OBJPROP_XDISTANCE, 200)
    ObjectSetInteger(0, btnIdShowBuy, OBJPROP_YDISTANCE, 0)
    ObjectSetInteger(0, btnIdShowBuy, OBJPROP_XSIZE, 100)
    ObjectSetInteger(0, btnIdShowBuy, OBJPROP_YSIZE, 15)
    ObjectSetString(0, btnIdShowBuy, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, btnIdShowBuy, OBJPROP_TEXT, 'Show buy')
    ObjectSetInteger(0, btnIdShowBuy, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, btnIdShowBuy, OBJPROP_SELECTABLE, 0)
    ObjectSetInteger(0, btnIdShowBuy, OBJPROP_STATE, btnStateShowBuy)
    ObjectCreate(0, btnIdShowSell, OBJ_BUTTON, 0, 100, 100)
    ObjectSetInteger(0, btnIdShowSell, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(0, btnIdShowSell, OBJPROP_BGCOLOR, btn_std_color)
    ObjectSetInteger(0, btnIdShowSell, OBJPROP_XDISTANCE, 200)
    ObjectSetInteger(0, btnIdShowSell, OBJPROP_YDISTANCE, 16)
    ObjectSetInteger(0, btnIdShowSell, OBJPROP_XSIZE, 100)
    ObjectSetInteger(0, btnIdShowSell, OBJPROP_YSIZE, 15)
    ObjectSetString(0, btnIdShowSell, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, btnIdShowSell, OBJPROP_TEXT, 'Show sell')
    ObjectSetInteger(0, btnIdShowSell, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, btnIdShowSell, OBJPROP_SELECTABLE, 0)
    ObjectSetInteger(0, btnIdShowSell, OBJPROP_STATE, btnStateShowSell)
    ObjectCreate(0, btnIdShowWinners, OBJ_BUTTON, 0, 100, 100)
    ObjectSetInteger(0, btnIdShowWinners, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(0, btnIdShowWinners, OBJPROP_BGCOLOR, btn_std_color)
    ObjectSetInteger(0, btnIdShowWinners, OBJPROP_XDISTANCE, 200)
    ObjectSetInteger(0, btnIdShowWinners, OBJPROP_YDISTANCE, 31)
    ObjectSetInteger(0, btnIdShowWinners, OBJPROP_XSIZE, 100)
    ObjectSetInteger(0, btnIdShowWinners, OBJPROP_YSIZE, 15)
    ObjectSetString(0, btnIdShowWinners, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, btnIdShowWinners, OBJPROP_TEXT, 'Show winners')
    ObjectSetInteger(0, btnIdShowWinners, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, btnIdShowWinners, OBJPROP_SELECTABLE, 0)
    ObjectSetInteger(0, btnIdShowWinners, OBJPROP_STATE, btnStateShowWinners)
    ObjectCreate(0, btnIdShowLosses, OBJ_BUTTON, 0, 100, 100)
    ObjectSetInteger(0, btnIdShowLosses, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(0, btnIdShowLosses, OBJPROP_BGCOLOR, btn_std_color)
    ObjectSetInteger(0, btnIdShowLosses, OBJPROP_XDISTANCE, 200)
    ObjectSetInteger(0, btnIdShowLosses, OBJPROP_YDISTANCE, 46)
    ObjectSetInteger(0, btnIdShowLosses, OBJPROP_XSIZE, 100)
    ObjectSetInteger(0, btnIdShowLosses, OBJPROP_YSIZE, 15)
    ObjectSetString(0, btnIdShowLosses, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, btnIdShowLosses, OBJPROP_TEXT, 'Show losses')
    ObjectSetInteger(0, btnIdShowLosses, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, btnIdShowLosses, OBJPROP_SELECTABLE, 0)
    ObjectSetInteger(0, btnIdShowLosses, OBJPROP_STATE, btnStateShowLosses)
    ObjectCreate(0, btnIdStartPoint, OBJ_BUTTON, 0, 100, 100)
    ObjectSetInteger(0, btnIdStartPoint, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(0, btnIdStartPoint, OBJPROP_BGCOLOR, btn_std_color)
    ObjectSetInteger(0, btnIdStartPoint, OBJPROP_XDISTANCE, 305)
    ObjectSetInteger(0, btnIdStartPoint, OBJPROP_YDISTANCE, 16)
    ObjectSetInteger(0, btnIdStartPoint, OBJPROP_XSIZE, 100)
    ObjectSetInteger(0, btnIdStartPoint, OBJPROP_YSIZE, 15)
    ObjectSetString(0, btnIdStartPoint, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, btnIdStartPoint, OBJPROP_TEXT, 'Start point')
    ObjectSetInteger(0, btnIdStartPoint, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, btnIdStartPoint, OBJPROP_SELECTABLE, 0)
    ObjectSetInteger(0, btnIdStartPoint, OBJPROP_STATE, btnStateStartPoint)
    ObjectCreate(0, btnIdEndPoint, OBJ_BUTTON, 0, 100, 100)
    ObjectSetInteger(0, btnIdEndPoint, OBJPROP_COLOR, clrWhite)
    ObjectSetInteger(0, btnIdEndPoint, OBJPROP_BGCOLOR, btn_std_color)
    ObjectSetInteger(0, btnIdEndPoint, OBJPROP_XDISTANCE, 305)
    ObjectSetInteger(0, btnIdEndPoint, OBJPROP_YDISTANCE, 31)
    ObjectSetInteger(0, btnIdEndPoint, OBJPROP_XSIZE, 100)
    ObjectSetInteger(0, btnIdEndPoint, OBJPROP_YSIZE, 15)
    ObjectSetString(0, btnIdEndPoint, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, btnIdEndPoint, OBJPROP_TEXT, 'End point')
    ObjectSetInteger(0, btnIdEndPoint, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, btnIdEndPoint, OBJPROP_SELECTABLE, 0)
    ObjectSetInteger(0, btnIdEndPoint, OBJPROP_STATE, btnStateEndPoint)

def GetOperationsHistory():
    global historyList
    Line1 = 0.0
    Line2 = 0.0
    Time1 = 0
    Time2 = 0
    getcolor = 0
    objName = ""
    objectall = ObjectsTotal(0, 0, -1)
    if objectall == 0:
        Comment('No object to work. Нет объектов для работы')
        return False
    historyList = CList()
    for i in range(0, objectall):
        objName = ''
        objName = ObjectName(0, i, 0, OBJ_TREND)
        if objName != '':
            Line1 = NormalizeDouble(ObjectGetDouble(0, objName, OBJPROP_PRICE, 0), Digits())
            Line2 = NormalizeDouble(ObjectGetDouble(0, objName, OBJPROP_PRICE, 1), Digits())
            Time1 = ObjectGetInteger(0, objName, OBJPROP_TIME, 0)
            Time2 = ObjectGetInteger(0, objName, OBJPROP_TIME, 1)
            getcolor = _uint(ObjectGetInteger(0, objName, OBJPROP_COLOR))
            item = COperation()
            item.m_Name = objName
            item.m_StartPosPrice = Line1
            item.m_EndPosPrice = Line2
            item.m_StartPosDt = Time1
            item.m_EndPosDt = Time2
            if getcolor == clrBuy:
                item.m_IsBuy = True
            if getcolor == clrSell:
                item.m_IsBuy = False
            item.m_IsWinner = IsWiner(item)
            historyList.Add(item)
    GetOperationsArrows(objectall)
    operations = historyList.Total()
    if operations == 0:
        return False
    else:
        Comment('loaded ' + _str(operations) + ' operations')
    return True

def GetOperationsArrows(objectall):
    objName = ""
    arrowType = 0
    Line1 = 0.0
    Time1 = 0
    for i in range(0, objectall):
        objName = ''
        arrowType = 0
        objName = ObjectName(0, i)
        type_ = ObjectGetInteger(0, objName, OBJPROP_TYPE)
        if type_ == OBJ_ARROW_BUY:
            Line1 = NormalizeDouble(ObjectGetDouble(0, objName, OBJPROP_PRICE, 0), Digits())
            Time1 = ObjectGetInteger(0, objName, OBJPROP_TIME, 0)
            node = historyList.GetFirstNode()
            while node is not None:
                if node.m_StartPosPrice == Line1 and node.m_StartPosDt == Time1:
                    node.m_StartPosName = objName
                if node.m_EndPosPrice == Line1 and node.m_EndPosDt == Time1:
                    node.m_EndPosName = objName
                node = node.Next_0()
        if type_ == OBJ_ARROW_SELL:
            Line1 = NormalizeDouble(ObjectGetDouble(0, objName, OBJPROP_PRICE, 0), Digits())
            Time1 = ObjectGetInteger(0, objName, OBJPROP_TIME, 0)
            node = historyList.GetFirstNode()
            while node is not None:
                if node.m_StartPosPrice == Line1 and node.m_StartPosDt == Time1:
                    node.m_StartPosName = objName
                if node.m_EndPosPrice == Line1 and node.m_EndPosDt == Time1:
                    node.m_EndPosName = objName
                node = node.Next_0()

def IsWiner(item):
    if item.m_IsBuy and item.m_StartPosPrice < item.m_EndPosPrice:
        return True
    if (not item.m_IsBuy) and item.m_StartPosPrice > item.m_EndPosPrice:
        return True
    return False

def OnButtonStateChanged():
    ObjectsDeleteAll(0)
    CreateButtons()
    node = historyList.GetFirstNode()
    while node is not None:
        if node.m_IsBuy and btnStateShowBuy:
            DrawLinesCondition(node, BuyLineColor, BuyWidth)
        if (not node.m_IsBuy) and btnStateShowSell:
            DrawLinesCondition(node, SellLineColor, SellWidth)
        node = node.Next_0()

def DrawLinesCondition(node, clr, lineWidth):
    if btnStateShowWinners and node.m_IsWinner:
        ObjectCreate(0, node.m_Name, OBJ_TREND, 0, node.m_StartPosDt, node.m_StartPosPrice, node.m_EndPosDt, node.m_EndPosPrice)
        ObjectSetInteger(0, node.m_Name, OBJPROP_COLOR, clr)
        ObjectSetInteger(0, node.m_Name, OBJPROP_WIDTH, lineWidth)
        DrawArrows(node, DrawArrow)
        DrawVerticalLinePosition(node.m_Name, node.m_StartPosDt, node.m_EndPosDt)
    if btnStateShowLosses and (not node.m_IsWinner):
        ObjectCreate(0, node.m_Name, OBJ_TREND, 0, node.m_StartPosDt, node.m_StartPosPrice, node.m_EndPosDt, node.m_EndPosPrice)
        ObjectSetInteger(0, node.m_Name, OBJPROP_COLOR, clr)
        ObjectSetInteger(0, node.m_Name, OBJPROP_WIDTH, lineWidth)
        DrawArrows(node, DrawArrow)
        DrawVerticalLinePosition(node.m_Name, node.m_StartPosDt, node.m_EndPosDt)
    if (not btnStateShowWinners) and (not btnStateShowLosses):
        ObjectCreate(0, node.m_Name, OBJ_TREND, 0, node.m_StartPosDt, node.m_StartPosPrice, node.m_EndPosDt, node.m_EndPosPrice)
        ObjectSetInteger(0, node.m_Name, OBJPROP_COLOR, clr)
        ObjectSetInteger(0, node.m_Name, OBJPROP_WIDTH, lineWidth)
        DrawArrows(node, DrawArrow)
        DrawVerticalLinePosition(node.m_Name, node.m_StartPosDt, node.m_EndPosDt)

def DrawArrows(node, canDrawArrow=True):
    if canDrawArrow:
        if node.m_IsBuy:
            ObjectCreate(0, node.m_StartPosName, OBJ_ARROW_BUY, 0, node.m_StartPosDt, node.m_StartPosPrice)
            ObjectCreate(0, node.m_EndPosName, OBJ_ARROW_SELL, 0, node.m_EndPosDt, node.m_EndPosPrice)
        else:
            ObjectCreate(0, node.m_StartPosName, OBJ_ARROW_SELL, 0, node.m_StartPosDt, node.m_StartPosPrice)
            ObjectCreate(0, node.m_EndPosName, OBJ_ARROW_BUY, 0, node.m_EndPosDt, node.m_EndPosPrice)

def DrawVerticalLinePosition(name, Sdate, Edate):
    if btnStateStartPoint:
        objName = name + 'VlineS'
        ObjectCreate(0, objName, OBJ_VLINE, 0, Sdate, 0)
        ObjectSetInteger(0, objName, OBJPROP_COLOR, ClrStartPos)
    if btnStateEndPoint:
        objName = name + 'VlineE'
        ObjectCreate(0, objName, OBJ_VLINE, 0, Edate, 0)
        ObjectSetInteger(0, objName, OBJPROP_COLOR, ClrEndPos)

def ButtonMouseMoveFocus(x, y, name):
    sizeX = 0
    sizeY = 0
    distX = 0
    distY = 0
    for i in range(ArraySize(buttonsArr) - 1, 0 - 1, -1):
        sizeX = _int(ObjectGetInteger(0, buttonsArr[i], OBJPROP_XSIZE))
        sizeY = _int(ObjectGetInteger(0, buttonsArr[i], OBJPROP_YSIZE))
        distX = _int(ObjectGetInteger(0, buttonsArr[i], OBJPROP_XDISTANCE))
        distY = _int(ObjectGetInteger(0, buttonsArr[i], OBJPROP_YDISTANCE))
        endPointX = distX + sizeX
        endPointY = distY + sizeY
        if ((x > distX and x < endPointX) and y > distY) and y < endPointY:
            name.v = buttonsArr[i]
            return True
    return False

def SetButtonColorToDefalult():
    for i in range(ArraySize(buttonsArr) - 1, 0 - 1, -1):
        ObjectSetInteger(0, buttonsArr[i], OBJPROP_BGCOLOR, btn_std_color)

def SetDefaultLines():
    node = historyList.GetFirstNode()
    while node is not None:
        ObjectCreate(0, node.m_Name, OBJ_TREND, 0, node.m_StartPosDt, node.m_StartPosPrice, node.m_EndPosDt, node.m_EndPosPrice)
        ObjectSetInteger(0, node.m_Name, OBJPROP_STYLE, STYLE_DOT)
        ObjectSetInteger(0, node.m_Name, OBJPROP_WIDTH, 1)
        if node.m_IsBuy:
            ObjectSetInteger(0, node.m_Name, OBJPROP_COLOR, clrBuy)
        else:
            ObjectSetInteger(0, node.m_Name, OBJPROP_COLOR, clrSell)
        DrawArrows(node)
        node = node.Next_0()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Aftertesting(_MQL5Indicator):
    name = 'aftertesting'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DrawArrow': True,  # Рисовать стрелки
        'BuyWidth': 2,  # Толщина линии
        'SellWidth': 2,  # Толщина линии
    }

