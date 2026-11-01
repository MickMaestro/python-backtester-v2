"""attention_level — converted from MQL5: MQL5 Indicators/Attention Level/attention_level.mq5

Индикатор размещает на графике горизонтальный не торговый уровень, помогающий внутредневным трейдерам оценить изменение дневной тенденции в поведении цены.
Indicator places in the chart do not trade horizontal level, which helps intraday traders to estimate the change in the daily trend in the behavior of prices.
Copyright: Pavel Trofimov; Link: https://vk.com/trofimovpp; Version: 1.00

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

MQL5_META = {'props': {'copyright': 'Pavel Trofimov', 'link': 'https://vk.com/trofimovpp', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 0}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {1: 'A_L'}, 'levels': [], 'description': ['Индикатор размещает на графике горизонтальный не торговый уровень, помогающий внутредневным трейдерам оценить изменение дневной тенденции в поведении цены.', 'Indicator places in the chart do not trade horizontal level, which helps intraday traders to estimate the change in the daily trend in the behavior of prices.'], 'name': 'attention_level', 'source': 'MQL5 Indicators/Attention Level/attention_level.mq5', 'folder': 'Attention Level', 'inputs': [{'mql': 'ATR_maPeriod', 'py': 'ATR_maPeriod', 'param': 'ATR_maPeriod', 'type': 'int', 'default': 10, 'label': 'ATR averaging period \\ Период усреднения ATR', 'sinput': False}, {'mql': 'LevelColor', 'py': 'LevelColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color line level \\ Цвет линии уровня', 'sinput': False}, {'mql': 'LevelStyle', 'py': 'LevelStyle', 'param': 'LevelStyle', 'type': 'int', 'default': 0, 'label': 'Style line level \\ Стиль линии уровня', 'sinput': False}, {'mql': 'LevelWidth', 'py': 'LevelWidth', 'param': 'LevelWidth', 'type': 'int', 'default': 1, 'label': 'Width line level \\ Толщина линии уровня', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

CHAR_VALUE = 0  # MQL5 constant unknown to the converter
INT_VALUE = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
ATR_maPeriod = _input('ATR_maPeriod', 10)  # ATR averaging period \ Период усреднения ATR
LevelColor = _input('LevelColor', clrRed)  # Color line level \ Цвет линии уровня
LevelStyle = _input('LevelStyle', STYLE_SOLID)  # Style line level \ Стиль линии уровня
LevelWidth = _input('LevelWidth', 1)  # Width line level \ Толщина линии уровня
A_LBuffer = Arr(0, 0.0)
ATR_values = Arr(0, 0.0)  # массив значение индикатора ATR;
handle = 0  # хендл индикатора
symbol = ""  # символ инструмента
m_HLine = None  # переменная для графических объектов Hline
obj_name = 'Attention_level'  # имя объекта
DayCount = 0  # счетчик дневных баров

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

class CChartObjectVLine(CChartObject):
    _q_fields = ()
    def __init__(self):
        CChartObject.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, time):
        if not ObjectCreate(chart_id, name, OBJ_VLINE, window, time, 0.0):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        return True
    def Type(self):
        return OBJ_VLINE

class CChartObjectHLine(CChartObject):
    _q_fields = ()
    def __init__(self):
        CChartObject.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, price):
        if not ObjectCreate(chart_id, name, OBJ_HLINE, window, 0, price):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        return True
    def Type(self):
        return OBJ_HLINE

class CChartObjectTrend(CChartObject):
    _q_fields = ()
    def __init__(self):
        CChartObject.__init__(self)
    def _q_dtor(self):
        pass
    def RayLeft_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_RAY_LEFT))
    def RayLeft_1(self, new_ray):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_RAY_LEFT, new_ray)
    def RayRight_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_RAY_RIGHT))
    def RayRight_1(self, new_ray):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_RAY_RIGHT, new_ray)
    def Create(self, chart_id, name, window, time1, price1, time2, price2):
        if not ObjectCreate(chart_id, name, OBJ_TREND, window, time1, price1, time2, price2):
            return False
        if not self.Attach(chart_id, name, window, 2):
            return False
        return True
    def Type(self):
        return OBJ_TREND
    def Save(self, file_handle):
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_RAY_LEFT)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_RAY_RIGHT)), CHAR_VALUE) != 1:
            return False
        return True
    def Load(self, file_handle):
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_RAY_LEFT, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_RAY_RIGHT, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        return True

class CChartObjectTrendByAngle(CChartObjectTrend):
    _q_fields = ()
    def __init__(self):
        CChartObjectTrend.__init__(self)
    def _q_dtor(self):
        pass
    def Angle_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_ANGLE)
    def Angle_1(self, angle):
        if self.m_chart_id == -1:
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_ANGLE, angle)
    def Create(self, chart_id, name, window, time1, price1, time2, price2):
        if not ObjectCreate(chart_id, name, OBJ_TRENDBYANGLE, window, time1, price1, time2, price2):
            return False
        if not self.Attach(chart_id, name, window, 2):
            return False
        return True
    def Type(self):
        return OBJ_TRENDBYANGLE

class CChartObjectCycles(CChartObject):
    _q_fields = ()
    def __init__(self):
        CChartObject.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, time1, price1, time2, price2):
        if not ObjectCreate(chart_id, name, OBJ_CYCLES, window, time1, price1, time2, price2):
            return False
        if not self.Attach(chart_id, name, window, 2):
            return False
        return True
    def Type(self):
        return OBJ_CYCLES

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

def OnInit():
    global symbol
    ArraySetAsSeries(A_LBuffer, True)
    SetIndexBuffer(0, A_LBuffer, INDICATOR_CALCULATIONS)
    symbol = Symbol()
    ArraySetAsSeries(rates_array, True)
    ArraySetAsSeries(ATR_values, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global DayCount
    iCod = 0
    DayCount = Bars(symbol, PERIOD_D1)
    if DayCount == -1:
        return 0
    if prev_calculated == 0:
        if ATR_Calculation() == -1:
            return 0
        ArrayInitialize(A_LBuffer, 0)
        iCod = CopyRates(symbol, PERIOD_D1, 0, DayCount, rates_array)
        Level_Calculation(rates_array)
    if DayCount > iCod:
        if ATR_Calculation() == -1:
            return rates_total
        ArrayInitialize(A_LBuffer, 0)
        iCod = CopyRates(symbol, PERIOD_D1, 0, DayCount, rates_array)
        Level_Calculation(rates_array)
    return rates_total

def Level_Calculation(rates):
    global m_HLine
    d_open = 0.0
    d_close = 0.0
    d_high = 0.0
    d_low = 0.0
    end_flag = False
    k = 1
    while k < DayCount and (not end_flag):
        d_open = rates_array[k].open
        d_close = rates_array[k].close
        d_high = rates_array[k].high
        d_low = rates_array[k].low
        if d_close < d_open:
            A_LBuffer[0] = d_low + ATR_values[k]
            end_flag = True
        if d_open < d_close:
            A_LBuffer[0] = d_high - ATR_values[k]
            end_flag = True
        if d_open == d_close:
            end_flag = False
            k += 1
        if end_flag:
            Comment('Attention level: ' + DoubleToString(A_LBuffer[0]))
            m_HLine = CChartObjectHLine()
            m_HLine.Create(0, obj_name, 0, A_LBuffer[0])
            m_HLine.Color_1(LevelColor)
            m_HLine.Style_1(LevelStyle)
            m_HLine.Width_1(LevelWidth)
            m_List_line.Add(m_HLine)

def ATR_Calculation():
    global handle
    ResetLastError()
    handle = iATR(symbol, PERIOD_D1, ATR_maPeriod)
    BufSize = CopyBuffer(handle, 0, 0, ATR_maPeriod, ATR_values)
    if BufSize == -1:
        Print('Error ATR calculation. No day data available. Check the connection to the server')
        return -1
    if DayCount < (ATR_maPeriod + 1):
        Print('Error ATR calculation. Too few historical data uploaded! Try reduce ATR_maPeriod.')
        return -1
    return BufSize

def OnDeinit(reason):
    m_List_line.Clear()
    if ObjectFind(0, obj_name) > 0:
        ObjectDelete(0, obj_name)
    Comment('')

# ---- global variables initialised from expressions
rates_array = Arr(0, 0, factory=MqlRates)  # массив с дневными котировками символа
m_List_line = _alloc(CList)  # член класса CList для хранения графических объектов индикатора
m_List_line.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AttentionLevel(_MQL5Indicator):
    name = 'attention_level'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ATR_maPeriod': 10,  # ATR averaging period \ Период усреднения ATR
        'LevelStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Style line level \ Стиль линии уровня
        'LevelWidth': 1,  # Width line level \ Толщина линии уровня
    }

