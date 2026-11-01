"""timerclosingperiod — converted from MQL5: MQL5 Indicators/TimerClosingPeriod v.2/timerclosingperiod.mq5

Copyright: Dmitry Voronkov; Link: vdv_2001@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Functions not available here: FileReadLong, FileWriteLong
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'Dmitry Voronkov', 'link': 'vdv_2001@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_plots': 1, 'indicator_buffers': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'timerclosingperiod', 'source': 'MQL5 Indicators/TimerClosingPeriod v.2/timerclosingperiod.mq5', 'folder': 'TimerClosingPeriod v.2', 'inputs': [{'mql': 'InpPathFirstSound', 'py': 'InpPathFirstSound', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'First signal', 'sinput': False}, {'mql': 'InpPathSecondSound', 'py': 'InpPathSecondSound', 'param': None, 'type': 'string', 'default': 'news.wav', 'label': 'Second signal', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

CHAR_VALUE = 0  # MQL5 constant unknown to the converter
Green = 0x008000  # MQL4 colour name
INT_VALUE = 0  # MQL5 constant unknown to the converter
Red = 0x0000FF  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name

# ---- inputs and global variables
InpPathFirstSound = _input('InpPathFirstSound', 'alert.wav')  # First signal
InpPathSecondSound = _input('InpPathSecondSound', 'news.wav')  # Second signal

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

class CTimer(CObject):
    _q_fields = ('_TimePeriod', 'TimerText', 'TimerSubstrate', 'TimerSignalButton', '_Color', '_Substrate', '_Corner', 'InitTimer', 'SoundFlag', 'SignalName')
    _q_ptrs = ('TimerText', 'TimerSubstrate', 'TimerSignalButton',)
    def __init__(self):
        CObject.__init__(self)
        self._TimePeriod = 0
        self.TimerText = None
        self.TimerSubstrate = None
        self.TimerSignalButton = None
        self._Color = 0
        self._Substrate = 0
        self._Corner = 0
        self.InitTimer = False
        self.SoundFlag = False
        self.SignalName = ""
        self.TimerSubstrate = None
        self.TimerText = None
        self.TimerSignalButton = None
        self._TimePeriod = Period()
        self._Color = _uint(White)
        self._Substrate = _uint(Green)
        self._Corner = CORNER_RIGHT_LOWER
        self.InitTimer = False
        self.SoundFlag = False
        self.SignalName = ''
    def _q_dtor(self):
        self.InitTimer = False
        if self.TimerSubstrate is not None:
            _delete(self.TimerSubstrate)
        if self.TimerText is not None:
            _delete(self.TimerText)
        if self.TimerSignalButton is not None:
            _delete(self.TimerSignalButton)
    def Create(self, chart_id, name, window, X, Y):
        result = False
        if self._TimePeriod > PERIOD_D1:
            return False
        self.TimerSubstrate = CChartObjectLabel()
        if ObjectFind(0, 'Substrate' + name) == -1:
            result = self.TimerSubstrate.Create(0, 'Substrate' + name, 0, X, Y)
        else:
            result = self.TimerSubstrate.Attach(0, 'Substrate' + name, 0, 2)
            self.TimerSubstrate.X_Distance_1(X)
            self.TimerSubstrate.Y_Distance_1(Y)
        result &= self.TimerSubstrate.Anchor_1(ANCHOR_CENTER)
        result &= self.TimerSubstrate.Font_1('Webdings')
        result &= self.TimerSubstrate.FontSize_1(13)
        result &= self.TimerSubstrate.Color_1(self._Substrate)
        result &= self.TimerSubstrate.Corner_1(self._Corner)
        result &= self.TimerSubstrate.Description_1('gggg')
        result &= self.TimerSubstrate.Background_1(True)
        self.TimerText = CChartObjectLabel()
        if ObjectFind(0, name) == -1:
            result &= self.TimerText.Create(0, name, 0, X, Y)
        else:
            result &= self.TimerText.Attach(0, name, 0, 2)
            self.TimerText.X_Distance_1(X)
            self.TimerText.Y_Distance_1(Y)
        result &= self.TimerText.Anchor_1(ANCHOR_CENTER)
        result &= self.TimerText.Font_1('Arial Black')
        result &= self.TimerText.FontSize_1(10)
        result &= self.TimerText.Color_1(self._Color)
        result &= self.TimerText.Corner_1(self._Corner)
        result &= self.TimerText.Background_1(False)
        result &= self.TimerText.Description_1(TimeToString(self.TimeEndOfPeriod(), TIME_SECONDS))
        self.SignalOn()
        if result:
            self.InitTimer = True
        return result
    def Color_1(self, col):
        self._Color = col
        if self.TimerText is not None:
            return self.TimerText.Color_1(col)
        else:
            return False
    def Color_0(self):
        return self._Color
    def ColorBackground_1(self, col):
        self._Substrate = col
        if self.TimerSubstrate is not None:
            return self.TimerSubstrate.Color_1(col)
        else:
            return False
    def ColorBackground_0(self):
        return self._Substrate
    def Corner_1(self, corner):
        result = False
        self._Corner = corner
        result = self.TimerText.Corner_1(self._Corner)
        result &= self.TimerSubstrate.Corner_1(self._Corner)
        self.OnTimer()
        return result
    def Corner_0(self):
        pass
    def SignalFile_1(self, pach):
        self.SignalName = pach
        StringTrimLeft(_AttrRef(self, 'SignalName'))
        StringTrimRight(_AttrRef(self, 'SignalName'))
        self.SignalOn()
    def SignalFile_0(self):
        return self.SignalName
    def SignalOn(self):
        X = 0
        Y = 0
        name_obj = ""
        if self.TimerSubstrate is None:
            return False
        if self.SignalName == '':
            if self.TimerSignalButton is not None:
                _delete(self.TimerSignalButton)
                self.TimerSignalButton = None
            return False
        X = self.TimerSubstrate.X_Distance_0()
        Y = self.TimerSubstrate.Y_Distance_0()
        if self.TimerSignalButton is None:
            self.TimerSignalButton = CChartObjectButton()
            name_obj = self.TimerText.Name_0() + ' Signal'
            if ObjectFind(0, name_obj) == -1:
                self.TimerSignalButton.Create(0, name_obj, 0, X + 52, Y + 10, 18, 18)
            else:
                self.TimerSignalButton.Attach(0, name_obj, 0, 2)
                self.TimerSignalButton.X_Distance_1(X + 52)
                self.TimerSignalButton.Y_Distance_1(Y + 10)
            self.TimerSignalButton.State_1(False)
            self.TimerSignalButton.Font_1('Webdings')
            self.TimerSignalButton.FontSize_1(10)
            self.TimerSignalButton.Corner_1(self._Corner)
        self.TimerSignalButton.Color_1(self._Substrate)
        self.TimerSignalButton.Description_1('U')
        self.SoundFlag = True
        return True
    def SignalOff(self):
        name_obj = ""
        result = True
        if self.TimerSignalButton is None:
            return False
        if not self.TimerSignalButton.State_0():
            self.TimerSignalButton.State_1(True)
        self.TimerSignalButton.Color_1(_uint(Red))
        self.TimerSignalButton.Description_1('V')
        self.SoundFlag = False
        return result
    def OnTimer(self):
        global _s_CTimer_OnTimer_BlinkFlag
        if self.InitTimer:
            if self._TimePeriod > PERIOD_D1:
                return
            tmpTime = self.TimeEndOfPeriod()
            self.TimerText.Description_1(TimeToString(tmpTime, TIME_SECONDS))
            if tmpTime <= 10:
                if self.SoundFlag and tmpTime <= 1:
                    if not PlaySound(self.SignalName):
                        Print('Signal error ' + self.SignalName)
                if _s_CTimer_OnTimer_BlinkFlag:
                    self.TimerSubstrate.Color_1(_uint(Red))
                    _s_CTimer_OnTimer_BlinkFlag = False
                else:
                    self.TimerSubstrate.Color_1(self._Substrate)
                    _s_CTimer_OnTimer_BlinkFlag = True
            else:
                self.TimerSubstrate.Color_1(self._Substrate)
            ChartRedraw()
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if self.TimerSignalButton is not None:
                if self.TimerSignalButton.Name_0() == sparam:
                    if self.TimerSignalButton.State_0():
                        self.SignalOff()
                    else:
                        self.SignalOn()
    def TimePeriod_1(self, period):
        self._TimePeriod = period
        self.OnTimer()
    def TimePeriod_0(self):
        return self._TimePeriod
    def TimeEndOfPeriod(self):
        tmpDateTime = 0
        tmp = 0
        last_time = MqlDateTime()
        TimeToStruct(TimeTradeServer(), last_time)
        last_time.sec = 0
        if Period() <= PERIOD_H1:
            tmp = _idiv(PeriodSeconds(self._TimePeriod), PeriodSeconds(PERIOD_M1))
            tmp = _idiv(last_time.min, tmp)
            last_time.min = _idiv((tmp + 1) * PeriodSeconds(self._TimePeriod), PeriodSeconds(PERIOD_M1))
        elif Period() > PERIOD_H1 and Period() <= PERIOD_D1:
            tmp = _idiv(PeriodSeconds(self._TimePeriod), PeriodSeconds(PERIOD_H1))
            tmp = _idiv(last_time.hour, tmp)
            last_time.hour = _idiv((tmp + 1) * PeriodSeconds(self._TimePeriod), PeriodSeconds(PERIOD_H1))
            last_time.min = 0
        tmpDateTime = StructToTime(last_time)
        tmpDateTime = tmpDateTime - TimeTradeServer()
        return tmpDateTime

def OnInit():
    global Timer1, TimerH1
    Timer1 = CTimer()
    Timer1.Create(0, 'Current Timer ' + IntegerToString(Period()), 0, 50, 15)
    Timer1.SignalFile_1(InpPathFirstSound)
    if Period() < PERIOD_H1:
        Timer1.SignalOff()
        TimerH1 = CTimer()
        TimerH1.TimePeriod_1(PERIOD_H1)
        TimerH1.Create(0, 'H1 Timer ' + IntegerToString(Period()), 0, 50, 35)
        TimerH1.SignalFile_1(InpPathSecondSound)
    EventSetTimer(1)
    return 0

def OnDeinit(reason):
    global Timer1, TimerH1
    if Timer1 is not None:
        _delete(Timer1)
        Timer1 = None
    if TimerH1 is not None:
        _delete(TimerH1)
        TimerH1 = None
    EventKillTimer()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if Timer1 is not None:
        Timer1.OnEvent(id_, lparam, dparam, sparam)
    if TimerH1 is not None:
        TimerH1.OnEvent(id_, lparam, dparam, sparam)
    ChartRedraw()

def OnTimer():
    if Timer1 is not None:
        Timer1.OnTimer()
    if TimerH1 is not None:
        TimerH1.OnTimer()

# ---- global variables initialised from expressions
Timer1 = None
TimerH1 = None

# ---- static local variables
_s_CTimer_OnTimer_BlinkFlag = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Timerclosingperiod(_MQL5Indicator):
    name = 'timerclosingperiod'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

