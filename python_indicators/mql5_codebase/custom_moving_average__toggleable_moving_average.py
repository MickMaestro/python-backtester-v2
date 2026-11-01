"""Custom Moving Average — converted from MQL5: MQL5 Indicators/Toggleable Moving Average/Custom Moving Average.mq5

The indicator demonstrates how to obtain data
of indicator buffers for the iMA technical indicator.
A symbol and timeframe used for calculation of the indicator,
are set by the symbol and period parameters.
The method of creation of the handle1 is set through the 'type' parameter (function type).
All other parameters like in the standard Moving Average.
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Functions not available here: FileReadLong, FileWriteLong
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.controls_wndobj import *  # #include WndObj.mqh
from backtester.mql5.lib.controls_wnd import *  # #include Wnd.mqh
from backtester.mql5.lib.controls_rect import *  # #include Rect.mqh
from backtester.mql5.lib.controls_defines import *  # #include Defines.mqh
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {1: 'iMA'}, 'levels': [], 'description': ['The indicator demonstrates how to obtain data', 'of indicator buffers for the iMA technical indicator.', 'A symbol and timeframe used for calculation of the indicator,', 'are set by the symbol and period parameters.', "The method of creation of the handle1 is set through the 'type' parameter (function type).", 'All other parameters like in the standard Moving Average.'], 'name': 'Custom Moving Average', 'source': 'MQL5 Indicators/Toggleable Moving Average/Custom Moving Average.mq5', 'folder': 'Toggleable Moving Average', 'inputs': [{'mql': 'ma1_period', 'py': 'ma1_period', 'param': 'ma1_period', 'type': 'int', 'default': 20, 'label': 'Period of Short MA', 'sinput': False}, {'mql': 'ma1_method', 'py': 'ma1_method', 'param': 'ma1_method', 'type': 'int', 'default': 0, 'label': 'Type of Short MA', 'sinput': False}, {'mql': 'ma1_shift', 'py': 'ma1_shift', 'param': 'ma1_shift', 'type': 'int', 'default': 0, 'label': 'Shift of Short MA', 'sinput': False}, {'mql': 'indicator_color1', 'py': 'indicator_color1', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color of Short MA', 'sinput': False}, {'mql': 'indicator_width1', 'py': 'indicator_width1', 'param': 'indicator_width1', 'type': 'int', 'default': 2, 'label': 'Width of Short MA', 'sinput': False}, {'mql': 'indicator_style1', 'py': 'indicator_style1', 'param': 'indicator_style1', 'type': 'int', 'default': 0, 'label': 'Style of Short MA', 'sinput': False}, {'mql': 'applied1_price', 'py': 'applied1_price', 'param': 'applied1_price', 'type': 'int', 'default': 1, 'label': 'Applied Price of Short MA', 'sinput': False}, {'mql': 'button1_text', 'py': 'button1_text', 'param': None, 'type': 'string', 'default': 'MA20', 'label': 'Button Test of Short MA', 'sinput': False}, {'mql': 'ma2_period', 'py': 'ma2_period', 'param': 'ma2_period', 'type': 'int', 'default': 50, 'label': 'Period of Medium MA', 'sinput': False}, {'mql': 'ma2_method', 'py': 'ma2_method', 'param': 'ma2_method', 'type': 'int', 'default': 0, 'label': 'Type of Medium MA', 'sinput': False}, {'mql': 'ma2_shift', 'py': 'ma2_shift', 'param': 'ma2_shift', 'type': 'int', 'default': 0, 'label': 'Shift of Medium MA', 'sinput': False}, {'mql': 'indicator_color2', 'py': 'indicator_color2', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Color of Medium MA', 'sinput': False}, {'mql': 'indicator_width2', 'py': 'indicator_width2', 'param': 'indicator_width2', 'type': 'int', 'default': 2, 'label': 'Width of Medium MA', 'sinput': False}, {'mql': 'indicator_style2', 'py': 'indicator_style2', 'param': 'indicator_style2', 'type': 'int', 'default': 0, 'label': 'Style of Medium MA', 'sinput': False}, {'mql': 'applied2_price', 'py': 'applied2_price', 'param': 'applied2_price', 'type': 'int', 'default': 1, 'label': 'Applied Medium of Short MA', 'sinput': False}, {'mql': 'button2_text', 'py': 'button2_text', 'param': None, 'type': 'string', 'default': 'MA50', 'label': 'Button Test of Short MA', 'sinput': False}, {'mql': 'ma3_period', 'py': 'ma3_period', 'param': 'ma3_period', 'type': 'int', 'default': 200, 'label': 'Period of Long MA', 'sinput': False}, {'mql': 'ma3_method', 'py': 'ma3_method', 'param': 'ma3_method', 'type': 'int', 'default': 0, 'label': 'Type of Long MA', 'sinput': False}, {'mql': 'ma3_shift', 'py': 'ma3_shift', 'param': 'ma3_shift', 'type': 'int', 'default': 0, 'label': 'Shift of Long MA', 'sinput': False}, {'mql': 'indicator_color3', 'py': 'indicator_color3', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Color of Long MA', 'sinput': False}, {'mql': 'indicator_width3', 'py': 'indicator_width3', 'param': 'indicator_width3', 'type': 'int', 'default': 2, 'label': 'Width of Long MA', 'sinput': False}, {'mql': 'indicator_style3', 'py': 'indicator_style3', 'param': 'indicator_style3', 'type': 'int', 'default': 0, 'label': 'Style of Long MA', 'sinput': False}, {'mql': 'applied3_price', 'py': 'applied3_price', 'param': 'applied3_price', 'type': 'int', 'default': 1, 'label': 'Applied Price of Long MA', 'sinput': False}, {'mql': 'button3_text', 'py': 'button3_text', 'param': None, 'type': 'string', 'default': 'MA200', 'label': 'Button Test of Short MA', 'sinput': False}, {'mql': 'symbol', 'py': 'symbol', 'param': None, 'type': 'string', 'default': ' ', 'label': 'symbol', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 0, 'label': 'timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['WndObj.mqh', 'Wnd.mqh', 'Rect.mqh', 'Defines.mqh', 'Object.mqh', 'StdLibErr.mqh']}

CHAR_VALUE = 0  # MQL5 constant unknown to the converter
INT_VALUE = 0  # MQL5 constant unknown to the converter
OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter
OBJ_NO_PERIODS = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
ma1_period = _input('ma1_period', 20)  # Period of Short MA
ma1_method = _input('ma1_method', MODE_SMA)  # Type of Short MA
ma1_shift = _input('ma1_shift', 0)  # Shift of Short MA
indicator_color1 = _input('indicator_color1', clrRed)  # Color of Short MA
indicator_width1 = _input('indicator_width1', 2)  # Width of Short MA
indicator_style1 = _input('indicator_style1', STYLE_SOLID)  # Style of Short MA
applied1_price = _input('applied1_price', PRICE_CLOSE)  # Applied Price of Short MA
button1_text = _input('button1_text', 'MA20')  # Button Test of Short MA
iMA1Buffer = Arr(0, 0.0)
MA1_Ind = False
ma2_period = _input('ma2_period', 50)  # Period of Medium MA
ma2_method = _input('ma2_method', MODE_SMA)  # Type of Medium MA
ma2_shift = _input('ma2_shift', 0)  # Shift of Medium MA
indicator_color2 = _input('indicator_color2', clrBlue)  # Color of Medium MA
indicator_width2 = _input('indicator_width2', 2)  # Width of Medium MA
indicator_style2 = _input('indicator_style2', STYLE_SOLID)  # Style of Medium MA
applied2_price = _input('applied2_price', PRICE_CLOSE)  # Applied Medium of Short MA
button2_text = _input('button2_text', 'MA50')  # Button Test of Short MA
iMA2Buffer = Arr(0, 0.0)
MA2_Ind = False
ma3_period = _input('ma3_period', 200)  # Period of Long MA
ma3_method = _input('ma3_method', MODE_SMA)  # Type of Long MA
ma3_shift = _input('ma3_shift', 0)  # Shift of Long MA
indicator_color3 = _input('indicator_color3', clrGreen)  # Color of Long MA
indicator_width3 = _input('indicator_width3', 2)  # Width of Long MA
indicator_style3 = _input('indicator_style3', STYLE_SOLID)  # Style of Long MA
applied3_price = _input('applied3_price', PRICE_CLOSE)  # Applied Price of Long MA
button3_text = _input('button3_text', 'MA200')  # Button Test of Short MA
iMA3Buffer = Arr(0, 0.0)
MA3_Ind = False
symbol = _input('symbol', ' ')  # symbol
period = _input('period', PERIOD_CURRENT)  # timeframe
handle1 = 0
handle2 = 0
handle3 = 0
short_name = ""
bars_calculated = 0
bars_number = 0

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
    def Name_1(self, name_):
        if self.m_chart_id == -1:
            return False
        if ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_NAME, name_):
            self.m_name = name_
            return True
        return False
    def NumPoints(self):
        return self.m_num_points
    def Attach(self, chart_id, name_, window, points):
        if ObjectFind(chart_id, name_) < 0:
            return False
        if chart_id == 0:
            chart_id = ChartID()
        self.m_chart_id = chart_id
        self.m_window = window
        self.m_name = name_
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
    def Create(self, chart_id, name_, window, time, price):
        if not ObjectCreate(chart_id, name_, OBJ_TEXT, window, time, price):
            return False
        if not self.Attach(chart_id, name_, window, 1):
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
    def Create(self, chart_id, name_, window, X, Y):
        if not ObjectCreate(chart_id, name_, OBJ_LABEL, window, 0, 0.0):
            return False
        if not self.Attach(chart_id, name_, window, 1):
            return False
        if not self.Description_1(name_):
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
    def Create(self, chart_id, name_, window, X, Y, sizeX, sizeY):
        if not ObjectCreate(chart_id, name_, self.Type(), window, 0, 0, 0):
            return False
        if not self.Attach(chart_id, name_, window, 1):
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
    def Create(self, chart_id, name_, window, X, Y, sizeX, sizeY):
        if not ObjectCreate(chart_id, name_, self.Type(), window, 0, 0, 0):
            return False
        if not self.Attach(chart_id, name_, window, 1):
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

class CButton(CWndObj):
    _q_fields = ('m_button',)
    def __init__(self):
        CWndObj.__init__(self)
        self.m_button = CChartObjectButton()
        self.m_color = 0x28293B
        self.m_color_background = 0xEBE2DD
        self.m_color_border = 0xCFC3B2
    def _q_dtor(self):
        pass
    def Create(self, chart, name_, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name_, subwin, x1, y1, x2, y2):
            return False
        if not self.m_button.Create(chart, name_, subwin, x1, y1, self.Width_0(), self.Height_0()):
            return False
        return self.OnChange()
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
    def OnSetText(self):
        return self.m_button.Description_1(self.m_text)
    def OnSetColor(self):
        return self.m_button.Color_1(self.m_color)
    def OnSetColorBackground(self):
        return self.m_button.BackColor_1(self.m_color_background)
    def OnSetColorBorder(self):
        return self.m_button.BorderColor_1(self.m_color_border)
    def OnSetFont(self):
        return self.m_button.Font_1(self.m_font)
    def OnSetFontSize(self):
        return self.m_button.FontSize_1(self.m_font_size)
    def OnCreate(self):
        return self.m_button.Create(self.m_chart_id, self.m_name, self.m_subwin, self.m_rect.left, self.m_rect.top, self.m_rect.Width_0(), self.m_rect.Height_0())
    def OnShow(self):
        return self.m_button.Timeframes_1(_int(OBJ_ALL_PERIODS))
    def OnHide(self):
        return self.m_button.Timeframes_1(_int(OBJ_NO_PERIODS))
    def OnMove(self):
        return self.m_button.X_Distance_1(self.m_rect.left) and self.m_button.Y_Distance_1(self.m_rect.top)
    def OnResize(self):
        return self.m_button.X_Size_1(self.m_rect.Width_0()) and self.m_button.Y_Size_1(self.m_rect.Height_0())
    def OnMouseDown(self):
        if not ((self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0):
            self.Pressed_1(not self.Pressed_0())
        return CWnd.OnMouseDown(self)
    def OnMouseUp(self):
        if self.m_button.State_0() and (not ((self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0)):
            self.m_button.State_1(False)
        return CWnd.OnMouseUp(self)

def OnInit():
    global handle1, handle2, handle3, name, short_name
    ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, True)
    x1 = 25
    y1 = 100
    x2 = x1 + 70
    y2 = y1 + 30
    MA1Button.Create(0, button1_text, 0, x1, y1, x2, y2)
    MA1Button.Text_1(button1_text)
    x1 = x1 + 85
    x2 = x2 + 85
    MA2Button.Create(0, button2_text, 0, x1, y1, x2, y2)
    MA2Button.Text_1(button2_text)
    x1 = x1 + 85
    x2 = x2 + 85
    MA3Button.Create(0, button3_text, 0, x1, y1, x2, y2)
    MA3Button.Text_1(button3_text)
    SetIndexBuffer(0, iMA1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, iMA2Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, iMA3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, ma1_shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, ma2_shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, ma3_shift)
    name = symbol
    StringTrimRight(_GlobRef(globals(), 'name'))
    StringTrimLeft(_GlobRef(globals(), 'name'))
    if StringLen(name) == 0:
        name = Symbol()
    bars_number == Bars(name, period)
    handle1 = iMA(name, period, ma1_period, ma1_shift, ma1_method, applied1_price)
    handle2 = iMA(name, period, ma2_period, ma2_shift, ma2_method, applied2_price)
    handle3 = iMA(name, period, ma3_period, ma3_shift, ma3_method, applied3_price)
    if handle1 == INVALID_HANDLE:
        PrintFormat('Failed to create handle for Short MA of the iMA indicator for the symbol %s/%s, error code %d', name, EnumToString(period, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    if handle2 == INVALID_HANDLE:
        PrintFormat('Failed to create handle for Medium MA of the iMA indicator for the symbol %s/%s, error code %d', name, EnumToString(period, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    if handle3 == INVALID_HANDLE:
        PrintFormat('Failed to create handle for Long MA of the iMA indicator for the symbol %s/%s, error code %d', name, EnumToString(period, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    short_name = 'Custom Toggelable Moving Average'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated = BarsCalculated(handle1)
    if calculated <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(iMA1Buffer, ma1_shift, handle1, values_to_copy):
        Print('Error in MA1')
    if not FillArrayFromBuffer(iMA2Buffer, ma2_shift, handle2, values_to_copy):
        Print('Error in MA2')
    if not FillArrayFromBuffer(iMA3Buffer, ma3_shift, handle3, values_to_copy):
        Print('Error in MA3')
    comm = StringFormat('%s ==>  Updated value in the indicator %s: %d', TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS), short_name, values_to_copy)
    Comment(comm)
    bars_calculated = calculated
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle1, amount):
    ResetLastError()
    if CopyBuffer(ind_handle1, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def OnChartEvent(id_, lparam, dparam, sparam):
    global MA1_Ind, MA2_Ind, MA3_Ind
    if MA1Button.Contains_2(lparam, _int(dparam)):
        MA1Button.Pressed_1(True)
    else:
        MA1Button.Pressed_1(False)
    if id_ == CHARTEVENT_OBJECT_CLICK and sparam == button1_text:
        Print('Button 1 Pressed')
        Print('MA1_Ind Before:' + _str(MA1_Ind))
        if MA1_Ind == False:
            MA1_Ind = True
        else:
            MA1_Ind = False
        Print('MA1_Ind After:' + _str(MA1_Ind))
        _sw1 = MA1_Ind
        if _sw1 == True:
            PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
            PlotIndexSetInteger(0, PLOT_LINE_STYLE, indicator_style1)
            PlotIndexSetInteger(0, PLOT_LINE_COLOR, indicator_color1)
            PlotIndexSetInteger(0, PLOT_LINE_WIDTH, indicator_width1)
        elif _sw1 == False:
            PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
            PlotIndexSetInteger(0, PLOT_LINE_STYLE, STYLE_SOLID)
            PlotIndexSetInteger(0, PLOT_LINE_COLOR, clrNONE)
    if MA2Button.Contains_2(lparam, _int(dparam)):
        MA2Button.Pressed_1(True)
    else:
        MA2Button.Pressed_1(False)
    if id_ == CHARTEVENT_OBJECT_CLICK and sparam == button2_text:
        Print('Button 2 Pressed')
        Print('MA2_Ind:' + _str(MA2_Ind))
        if MA2_Ind == False:
            MA2_Ind = True
        else:
            MA2_Ind = False
        _sw2 = MA2_Ind
        if _sw2 == True:
            PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
            PlotIndexSetInteger(1, PLOT_LINE_STYLE, indicator_style2)
            PlotIndexSetInteger(1, PLOT_LINE_COLOR, indicator_color2)
            PlotIndexSetInteger(1, PLOT_LINE_WIDTH, indicator_width2)
        elif _sw2 == False:
            PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
            PlotIndexSetInteger(1, PLOT_LINE_STYLE, STYLE_SOLID)
            PlotIndexSetInteger(1, PLOT_LINE_COLOR, clrNONE)
    if MA3Button.Contains_2(lparam, _int(dparam)):
        MA3Button.Pressed_1(True)
    else:
        MA3Button.Pressed_1(False)
    if id_ == CHARTEVENT_OBJECT_CLICK and sparam == button3_text:
        Print('Button 3 Pressed')
        Print('MA3_Ind:' + _str(MA3_Ind))
        if MA3_Ind == False:
            MA3_Ind = True
        else:
            MA3_Ind = False
        _sw3 = MA3_Ind
        if _sw3 == True:
            PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_LINE)
            PlotIndexSetInteger(2, PLOT_LINE_STYLE, indicator_style3)
            PlotIndexSetInteger(2, PLOT_LINE_COLOR, indicator_color3)
            PlotIndexSetInteger(2, PLOT_LINE_WIDTH, indicator_width3)
        elif _sw3 == False:
            PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_NONE)
            PlotIndexSetInteger(2, PLOT_LINE_STYLE, STYLE_SOLID)
            PlotIndexSetInteger(2, PLOT_LINE_COLOR, clrNONE)
    ChartRedraw()

def OnDeinit(reason):
    if handle1 != INVALID_HANDLE:
        IndicatorRelease(handle1)
    Comment('')

# ---- global variables initialised from expressions
MA1Button = _alloc(CButton)
MA1Button.__init__()
MA2Button = _alloc(CButton)
MA2Button.__init__()
MA3Button = _alloc(CButton)
MA3Button.__init__()
name = symbol


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomMovingAverage(_MQL5Indicator):
    name = 'Custom Moving Average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ma1_period': 20,  # Period of Short MA
        'ma1_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Type of Short MA
        'ma1_shift': 0,  # Shift of Short MA
        'indicator_width1': 2,  # Width of Short MA
        'indicator_style1': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Style of Short MA
        'applied1_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied Price of Short MA
        'ma2_period': 50,  # Period of Medium MA
        'ma2_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Type of Medium MA
        'ma2_shift': 0,  # Shift of Medium MA
        'indicator_width2': 2,  # Width of Medium MA
        'indicator_style2': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Style of Medium MA
        'applied2_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied Medium of Short MA
        'ma3_period': 200,  # Period of Long MA
        'ma3_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Type of Long MA
        'ma3_shift': 0,  # Shift of Long MA
        'indicator_width3': 2,  # Width of Long MA
        'indicator_style3': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Style of Long MA
        'applied3_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied Price of Long MA
        'period': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # timeframe
    }

