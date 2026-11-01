"""FractalsTrendLines — converted from MQL5: MQL5 Indicators/FractalsTrendLines/FractalsTrendLines.mq5

Индикатор чертит бычью и медвежью линии тренда, на основании инд. iFractals. От ближайшего экстремума до последнего не пробитого фрактала. При пробитии данного фрактала линия закрепляется до появления нового экстремума.\\n
Трактовать можно следующим образом:
1) Пересечение линий \\"Проходной Крест\\"
2) Закрытие выше обоих линий: \\"Тренд бычий\\"
3) Закрытие ниже обоих линий: \\"Тренд медвежий\\"
4) Закрытие между линий, и \\"П.К.\\" слева: \\"Флет\\"
5) Закрытие между линий, и \\"П.К.\\" справа: \\"Треугольник неопределенности\\"
Copyright: Copyright 2014, Svds75; Link: https://login.mql5.com/ru/users/svds75/; Version: 1.00

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

MQL5_META = {'props': {'copyright': 'Copyright 2014, Svds75', 'link': 'https://login.mql5.com/ru/users/svds75/', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор чертит бычью и медвежью линии тренда, на основании инд. iFractals. От ближайшего экстремума до последнего не пробитого фрактала. При пробитии данного фрактала линия закрепляется до появления нового экстремума.\\n', 'Трактовать можно следующим образом:', '1) Пересечение линий \\"Проходной Крест\\"', '2) Закрытие выше обоих линий: \\"Тренд бычий\\"', '3) Закрытие ниже обоих линий: \\"Тренд медвежий\\"', '4) Закрытие между линий, и \\"П.К.\\" слева: \\"Флет\\"', '5) Закрытие между линий, и \\"П.К.\\" справа: \\"Треугольник неопределенности\\"'], 'name': 'FractalsTrendLines', 'source': 'MQL5 Indicators/FractalsTrendLines/FractalsTrendLines.mq5', 'folder': 'FractalsTrendLines', 'inputs': [{'mql': 'inpClrBull', 'py': 'inpClrBull', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Цвет бычьей линии тренда', 'sinput': True}, {'mql': 'inpClrBear', 'py': 'inpClrBear', 'param': None, 'type': 'color', 'default': 255, 'label': 'Цвет медвежьей линии тренда', 'sinput': True}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

CHAR_VALUE = 0  # MQL5 constant unknown to the converter
INT_VALUE = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
inpClrBull = _input('inpClrBull', clrGreen)  # Цвет бычьей линии тренда
inpClrBear = _input('inpClrBear', clrRed)  # Цвет медвежьей линии тренда
handle = 0  # Будет хранить хэндл индикатора iFractals

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

def OnInit():
    global handle
    handle = iFractals(Symbol(), Period())
    if handle == INVALID_HANDLE:
        handle = IndicatorCreate(Symbol(), Period(), IND_FRACTALS)
    if handle == INVALID_HANDLE:
        PrintFormat('Error create Fractals indicator handle %s/%s, code %d', Symbol(), EnumToString(Period(), 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat(MQLInfoString(MQL_PROGRAM_NAME) + '(%s/%s)', Symbol(), EnumToString(Period(), 'ENUM_TIMEFRAMES')))
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    if not createTrendLine(0, time):
        return 0
    if not createTrendLine(1, time):
        return 0
    return rates_total

def OnDeinit(reason):
    IndicatorRelease(handle)

def createTrendLine(t, TM):
    count = 500
    if t == 0:
        a = Arr(0, 0.0)
        ArraySetAsSeries(a, True)
        if CopyBuffer(handle, 0, 0, count, a) < 0:
            PrintFormat('Не удалось скопировать данные из индикатора iFractals, код ошибки %d', GetLastError())
            return False
        b1 = 0
        b2 = 0
        p1 = 0.0
        p2 = 0.0
        t1 = 0
        t2 = 0
        for b in range(3, count):
            if a[b] != EMPTY_VALUE:
                if p2 == 0:
                    p2 = a[b]
                    t2 = TM[b]
                    b2 = b
                elif p1 == 0:
                    p1 = a[b]
                    t1 = TM[b]
                    b1 = b
                elif a[b] < p1 and p1 > p2:
                    break
                else:
                    p2 = p1
                    t2 = t1
                    b2 = b1
                    p1 = a[b]
                    t1 = TM[b]
                    b1 = b
        for b in range(b2 - 1, 2, -1):
            if a[b] != EMPTY_VALUE:
                if p2 > a[b]:
                    p2 = a[b]
                    t2 = TM[b]
                    b2 = b
                else:
                    break
        if upLine.Name_0() != (MQLInfoString(MQL_PROGRAM_NAME) + '_Bear_Trend'):
            upLine.Create(0, MQLInfoString(MQL_PROGRAM_NAME) + '_Bear_Trend', 0, t1, p1, t2, p2)
            upLine.RayRight_1(True)
            upLine.Style_1(STYLE_DOT)
            upLine.Color_1(inpClrBear)
        else:
            upLine.Time_2(0, t1)
            upLine.Price_2(0, p1)
            upLine.Time_2(1, t2)
            upLine.Price_2(1, p2)
        return True
    if t == 1:
        a = Arr(0, 0.0)
        ArraySetAsSeries(a, True)
        if CopyBuffer(handle, 1, 0, count, a) < 0:
            PrintFormat('Не удалось скопировать данные из индикатора iFractals, код ошибки %d', GetLastError())
            return False
        b1 = 0
        b2 = 0
        p1 = 0.0
        p2 = 0.0
        t1 = 0
        t2 = 0
        for b in range(3, count):
            if a[b] != EMPTY_VALUE:
                if p2 == 0:
                    p2 = a[b]
                    t2 = TM[b]
                    b2 = b
                elif p1 == 0:
                    p1 = a[b]
                    t1 = TM[b]
                    b1 = b
                elif a[b] > p1 and p1 < p2:
                    break
                else:
                    p2 = p1
                    t2 = t1
                    b2 = b1
                    p1 = a[b]
                    t1 = TM[b]
                    b1 = b
        for b in range(b2 - 1, 2, -1):
            if a[b] != EMPTY_VALUE:
                if p2 < a[b]:
                    p2 = a[b]
                    t2 = TM[b]
                    b2 = b
                else:
                    break
        if dnLine.Name_0() != (MQLInfoString(MQL_PROGRAM_NAME) + '_Bull_Trend'):
            dnLine.Create(0, MQLInfoString(MQL_PROGRAM_NAME) + '_Bull_Trend', 0, t1, p1, t2, p2)
            dnLine.RayRight_1(True)
            dnLine.Style_1(STYLE_DOT)
            dnLine.Color_1(inpClrBull)
        else:
            dnLine.Time_2(0, t1)
            dnLine.Price_2(0, p1)
            dnLine.Time_2(1, t2)
            dnLine.Price_2(1, p2)
        return True
    return False

# ---- global variables initialised from expressions
upLine = _alloc(CChartObjectTrend)  # Объект верхней линии тренда (медвежей)
upLine.__init__()
dnLine = _alloc(CChartObjectTrend)  # Объект нижней линии тренда (бычей)
dnLine.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalsTrendLines(_MQL5Indicator):
    name = 'FractalsTrendLines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

