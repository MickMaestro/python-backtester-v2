"""Correlate — converted from MQL5: MQL5 Indicators/Currency Correlation II/Correlate.mq5

Copyright: Copyright 2020, ernst.; Link: https://www.mql5.com/en/users/pippod; Version: 1.77

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Functions not available here: FileReadLong, FileWriteLong
- Unresolved names: indicator_label1, indicator_label2, indicator_label3, indicator_label4, indicator_label5, indicator_label6, indicator_label7, indicator_label8, indicator_label9
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2020, ernst.', 'link': 'https://www.mql5.com/en/users/pippod', 'version': '1.77', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 9}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'colors': {1: [36095], 2: [16776960], 3: [2237106], 4: [14772545], 5: [12632256], 6: [1262987], 7: [13828244], 8: [55295], 9: [3329330]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'labels': {1: 'AUD', 2: 'CAD', 3: 'CHF', 4: 'EUR', 5: 'GBP', 6: 'JPY', 7: 'NZD', 8: 'XAU', 9: 'USD'}, 'levels': [], 'description': [], 'name': 'Correlate', 'source': 'MQL5 Indicators/Currency Correlation II/Correlate.mq5', 'folder': 'Currency Correlation II', 'inputs': [{'mql': 'Indicator', 'py': 'Indicator', 'param': 'Indicator', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'BarsToCount', 'py': 'BarsToCount', 'param': 'BarsToCount', 'type': 'int', 'default': 500, 'label': 'Bars to count', 'sinput': False}, {'mql': 'Sfix', 'py': 'Sfix', 'param': None, 'type': 'string', 'default': '', 'label': 'Symbol Suffix', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'ushort', 'default': 14, 'label': 'MA Period', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 0, 'label': 'MA Method', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'MA Price', 'sinput': False}, {'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'ushort', 'default': 12, 'label': 'Fast EMA Period', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'ushort', 'default': 26, 'label': 'Slow EMA Period', 'sinput': False}, {'mql': 'MACDPrice', 'py': 'MACDPrice', 'param': 'MACDPrice', 'type': 'int', 'default': 1, 'label': 'MACD Price', 'sinput': False}, {'mql': 'Kperiod', 'py': 'Kperiod', 'param': 'Kperiod', 'type': 'ushort', 'default': 7, 'label': 'K Period', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'ushort', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'PriceField', 'py': 'PriceField', 'param': 'PriceField', 'type': 'int', 'default': 0, 'label': 'Price Field', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'ushort', 'default': 14, 'label': 'RSI Period', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'RSI Price', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'ushort', 'default': 14, 'label': 'CCI Period', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 1, 'label': 'CCI Price', 'sinput': False}, {'mql': 'RVIPeriod', 'py': 'RVIPeriod', 'param': 'RVIPeriod', 'type': 'ushort', 'default': 14, 'label': 'RVI Period', 'sinput': False}, {'mql': 'DeMarkerPeriod', 'py': 'DeMarkerPeriod', 'param': 'DeMarkerPeriod', 'type': 'ushort', 'default': 14, 'label': 'DeMarker Period', 'sinput': False}, {'mql': 'MomentumPeriod', 'py': 'MomentumPeriod', 'param': 'MomentumPeriod', 'type': 'ushort', 'default': 14, 'label': 'Momentum Period', 'sinput': False}, {'mql': 'MomentumPrice', 'py': 'MomentumPrice', 'param': 'MomentumPrice', 'type': 'int', 'default': 1, 'label': 'Momentum Price', 'sinput': False}, {'mql': 'TrixPeriod', 'py': 'TrixPeriod', 'param': 'TrixPeriod', 'type': 'ushort', 'default': 14, 'label': 'TriX Period', 'sinput': False}, {'mql': 'TrixPrice', 'py': 'TrixPrice', 'param': 'TrixPrice', 'type': 'int', 'default': 1, 'label': 'TriX Price', 'sinput': False}, {'mql': 'MFIPeriod', 'py': 'MFIPeriod', 'param': 'MFIPeriod', 'type': 'ushort', 'default': 14, 'label': 'MFI Period', 'sinput': False}, {'mql': 'MFIVolume', 'py': 'MFIVolume', 'param': 'MFIVolume', 'type': 'int', 'default': 0, 'label': 'MFI Volume', 'sinput': False}, {'mql': 'Auto', 'py': 'Auto', 'param': 'Auto', 'type': 'bool', 'default': False, 'label': 'Display chart currencies', 'sinput': False}, {'mql': 'bAUD', 'py': 'bAUD', 'param': 'bAUD', 'type': 'bool', 'default': True, 'label': 'Display Aussie', 'sinput': False}, {'mql': 'bCAD', 'py': 'bCAD', 'param': 'bCAD', 'type': 'bool', 'default': True, 'label': 'Display Loonie', 'sinput': False}, {'mql': 'bCHF', 'py': 'bCHF', 'param': 'bCHF', 'type': 'bool', 'default': True, 'label': 'Display Swissy', 'sinput': False}, {'mql': 'bEUR', 'py': 'bEUR', 'param': 'bEUR', 'type': 'bool', 'default': True, 'label': 'Display Fiber', 'sinput': False}, {'mql': 'bGBP', 'py': 'bGBP', 'param': 'bGBP', 'type': 'bool', 'default': True, 'label': 'Display Sterling', 'sinput': False}, {'mql': 'bJPY', 'py': 'bJPY', 'param': 'bJPY', 'type': 'bool', 'default': True, 'label': 'Display Yen', 'sinput': False}, {'mql': 'bNZD', 'py': 'bNZD', 'param': 'bNZD', 'type': 'bool', 'default': True, 'label': 'Display Kiwi', 'sinput': False}, {'mql': 'bXAU', 'py': 'bXAU', 'param': 'bXAU', 'type': 'bool', 'default': True, 'label': 'Display Gold', 'sinput': False}, {'mql': 'bUSD', 'py': 'bUSD', 'param': 'bUSD', 'type': 'bool', 'default': True, 'label': 'Display Greenback', 'sinput': False}, {'mql': '__', 'py': '__', 'param': None, 'type': 'string', 'default': '', 'label': '---', 'sinput': False}, {'mql': 'Pips', 'py': 'Pips', 'param': 'Pips', 'type': 'bool', 'default': True, 'label': 'Ticks on pip change only', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

CHAR_VALUE = 0  # MQL5 constant unknown to the converter
INT_VALUE = 0  # MQL5 constant unknown to the converter
indicator_buffers = 9  # #property indicator_buffers
indicator_color1 = 36095  # #property indicator_color1
indicator_color2 = 16776960  # #property indicator_color2
indicator_color3 = 2237106  # #property indicator_color3
indicator_color4 = 14772545  # #property indicator_color4
indicator_color5 = 12632256  # #property indicator_color5
indicator_color6 = 1262987  # #property indicator_color6
indicator_color7 = 13828244  # #property indicator_color7
indicator_color8 = 55295  # #property indicator_color8
indicator_color9 = 3329330  # #property indicator_color9
indicator_plots = 9  # #property indicator_plots

# enum indicators
INDICATOR_MA = 0
INDICATOR_MACD = 1
INDICATOR_STOCHASTIC = 2
INDICATOR_RSI = 3
INDICATOR_CCI = 4
INDICATOR_RVI = 5
INDICATOR_DEMARKER = 6
INDICATOR_MOMENTUM = 7
INDICATOR_TRIX = 8
INDICATOR_MFI = 9
_enum('indicators', {0: 'INDICATOR_MA', 1: 'INDICATOR_MACD', 2: 'INDICATOR_STOCHASTIC', 3: 'INDICATOR_RSI', 4: 'INDICATOR_CCI', 5: 'INDICATOR_RVI', 6: 'INDICATOR_DEMARKER', 7: 'INDICATOR_MOMENTUM', 8: 'INDICATOR_TRIX', 9: 'INDICATOR_MFI'})

# ---- inputs and global variables
indicator_level1 = 0.0
indicator_level2 = 0.2
indicator_level3 = 20.0
indicator_level4 = 30.0
indicator_level5 = 100.0
indicator = Arr(8, None, dyn=False)
ind = None
currency = Arr(indicator_buffers, None, dyn=False)
cur = None
Indicator = _input('Indicator', INDICATOR_RSI)
BarsToCount = _input('BarsToCount', 500)  # Bars to count
Sfix = _input('Sfix', '')  # Symbol Suffix
MAPeriod = _input('MAPeriod', 14)  # MA Period
MAMethod = _input('MAMethod', MODE_SMA)  # MA Method
MAPrice = _input('MAPrice', PRICE_CLOSE)  # MA Price
FastEMA = _input('FastEMA', 12)  # Fast EMA Period
SlowEMA = _input('SlowEMA', 26)  # Slow EMA Period
MACDPrice = _input('MACDPrice', PRICE_CLOSE)  # MACD Price
Kperiod = _input('Kperiod', 7)  # K Period
Slowing = _input('Slowing', 3)
PriceField = _input('PriceField', STO_LOWHIGH)  # Price Field
RSIPeriod = _input('RSIPeriod', 14)  # RSI Period
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # RSI Price
CCIPeriod = _input('CCIPeriod', 14)  # CCI Period
CCIPrice = _input('CCIPrice', PRICE_CLOSE)  # CCI Price
RVIPeriod = _input('RVIPeriod', 14)  # RVI Period
DeMarkerPeriod = _input('DeMarkerPeriod', 14)  # DeMarker Period
MomentumPeriod = _input('MomentumPeriod', 14)  # Momentum Period
MomentumPrice = _input('MomentumPrice', PRICE_CLOSE)  # Momentum Price
TrixPeriod = _input('TrixPeriod', 14)  # TriX Period
TrixPrice = _input('TrixPrice', PRICE_CLOSE)  # TriX Price
MFIPeriod = _input('MFIPeriod', 14)  # MFI Period
MFIVolume = _input('MFIVolume', VOLUME_TICK)  # MFI Volume
Auto = _input('Auto', False)  # Display chart currencies
bAUD = _input('bAUD', True)  # Display Aussie
bCAD = _input('bCAD', True)  # Display Loonie
bCHF = _input('bCHF', True)  # Display Swissy
bEUR = _input('bEUR', True)  # Display Fiber
bGBP = _input('bGBP', True)  # Display Sterling
bJPY = _input('bJPY', True)  # Display Yen
bNZD = _input('bNZD', True)  # Display Kiwi
bXAU = _input('bXAU', True)  # Display Gold
bUSD = _input('bUSD', True)  # Display Greenback
__ = _input('__', "")  # ---
Pips = _input('Pips', True)  # Ticks on pip change only
chartID = 0
windowNo = 0
Symbols = Arr.of(['AUDUSD', 'USDCAD', 'USDCHF', 'EURUSD', 'GBPUSD', 'USDJPY', 'NZDUSD', 'XAUUSD'], fill="", dyn=False, size=8)
Currency = Arr(indicator_buffers, "", dyn=False)
IsVisible = Arr(indicator_buffers, False, dyn=False)
lbl = None

class CSymbol(MqlObject):
    _q_fields = ('m_symbol', 'm_handle', 'm_tick', 'm_size', 'm_buffer', 'Bars')
    def __init__(self, symbol):
        self.m_symbol = ""
        self.m_handle = 0
        self.m_tick = 0
        self.m_size = 0
        self.m_buffer = Arr(0, 0.0)
        self.Bars = 0
        self.m_symbol = symbol
        self.m_handle = INVALID_HANDLE
        self.m_tick = INVALID_HANDLE
        self.ArraySetAsSeries(True)
    def _q_dtor(self):
        self.IndicatorRelease()
    def Handle(self, handle, index):
        return _setattr(self, 'm_handle', handle) != INVALID_HANDLE and _setattr(self, 'm_tick', iCustom(self.m_symbol, Period(), '::Indicators\\OnTick.ex5', ChartID(), index, Pips)) != INVALID_HANDLE
    def __getitem__(self, index):
        return (self.m_buffer[index] if (index >= 0 and index < self.m_size) else 0.0)
    def CopyBuffer(self, start, count):
        return _setattr(self, 'm_size', CopyBuffer(self.m_handle, 0, start, count, self.m_buffer))
    def BarsCalculated(self):
        return BarsCalculated(self.m_handle) >= _setattr(self, 'Bars', iBars(self.m_symbol, Period()))
    def IndicatorRelease(self):
        return IndicatorRelease(self.m_handle) and IndicatorRelease(self.m_tick)
    def ArraySetAsSeries(self, flag):
        return self.ArraySetAsSeries(_bool(self.m_buffer), flag)

class CBuffer(MqlObject):
    _q_fields = ('m_size', 'm_buffer', 'close')
    def __init__(self):
        self.m_size = 0
        self.m_buffer = Arr(0, 0.0)
        self.close = 0.0
        self.ArraySetAsSeries(True)
    def _q_dtor(self):
        pass
    def SetIndexBuffer(self, index, buffer_mode=INDICATOR_DATA):
        return SetIndexBuffer(index, self.m_buffer, buffer_mode)
    def ArraySetAsSeries(self, flag):
        return self.ArraySetAsSeries(_bool(self.m_buffer), flag)
    def ArrayInitialize(self, value):
        return ArrayInitialize(self.m_buffer, value)
    def ArrayFree(self):
        self.ArrayFree(self.m_buffer)
        return
    def Close(self, index, value):
        return _setitem(self.m_buffer, index, value)

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

def OnInit():
    global chartID, lbl, windowNo
    Symbol_ = Arr(8, "", dyn=False)
    chartID = ChartID()
    for i in range(0, 8):
        Symbol_[i] = Symbols[i] + Sfix
        if not SymbolSelect(Symbol_[i], True):
            Alert(Symbol_[i], ' not available in Market Watch.\nInitialization Failed.')
            return INIT_FAILED
    shortName = ""
    _sw1 = Indicator
    if _sw1 == INDICATOR_MA:
        for i in range(0, 8):
            if (not CheckPointer(_setitem(indicator, i, CSymbol(Symbol_[i])))) or (not indicator[i].Handle(iMA(Symbol_[i], 0, MAPeriod, PERIOD_CURRENT, MAMethod, MAPrice), i)):
                return INIT_FAILED
        shortName = StringFormat('Correl8 %s(%d)', StringSubstr(EnumToString(MAMethod, 'ENUM_MA_METHOD'), 5), MAPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 5)
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
    elif _sw1 == INDICATOR_MACD:
        for i in range(0, 8):
            if (not CheckPointer(_setitem(indicator, i, CSymbol(Symbol_[i])))) or (not indicator[i].Handle(iMACD(Symbol_[i], PERIOD_CURRENT, FastEMA, SlowEMA, 9, MACDPrice), i)):
                return INIT_FAILED
        shortName = StringFormat('Correl8 MACD(%d,%d)', FastEMA, SlowEMA)
        IndicatorSetInteger(INDICATOR_DIGITS, 5)
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
    elif _sw1 == INDICATOR_STOCHASTIC:
        for i in range(0, 8):
            if (not CheckPointer(_setitem(indicator, i, CSymbol(Symbol_[i])))) or (not indicator[i].Handle(iStochastic(Symbol_[i], PERIOD_CURRENT, Kperiod, 2, Slowing, MODE_SMA, PriceField), i)):
                return INIT_FAILED
        shortName = StringFormat('Correl8 Stochastic(%d,%d)', Kperiod, Slowing)
        IndicatorSetInteger(INDICATOR_DIGITS, 1)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level4)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level4)
    elif _sw1 == INDICATOR_RSI:
        for i in range(0, 8):
            if (not CheckPointer(_setitem(indicator, i, CSymbol(Symbol_[i])))) or (not indicator[i].Handle(iRSI(Symbol_[i], PERIOD_CURRENT, RSIPeriod, RSIPrice), i)):
                return INIT_FAILED
        shortName = StringFormat('Correl8 RSI(%d)', RSIPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 1)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level3)
    elif _sw1 == INDICATOR_CCI:
        for i in range(0, 8):
            if (not CheckPointer(_setitem(indicator, i, CSymbol(Symbol_[i])))) or (not indicator[i].Handle(iCCI(Symbol_[i], PERIOD_CURRENT, CCIPeriod, CCIPrice), i)):
                return INIT_FAILED
        shortName = StringFormat('Correl8 CCI(%d)', CCIPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 0)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level5)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level5)
    elif _sw1 == INDICATOR_RVI:
        for i in range(0, 8):
            if (not CheckPointer(_setitem(indicator, i, CSymbol(Symbol_[i])))) or (not indicator[i].Handle(iRVI(Symbol_[i], PERIOD_CURRENT, RVIPeriod), i)):
                return INIT_FAILED
        shortName = StringFormat('Correl8 RVI(%d)', RVIPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 3)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level2)
    elif _sw1 == INDICATOR_DEMARKER:
        for i in range(0, 8):
            if (not CheckPointer(_setitem(indicator, i, CSymbol(Symbol_[i])))) or (not indicator[i].Handle(iDeMarker(Symbol_[i], PERIOD_CURRENT, DeMarkerPeriod), i)):
                return INIT_FAILED
        shortName = StringFormat('Correl8 DeMarker(%d)', DeMarkerPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 3)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level2)
    elif _sw1 == INDICATOR_MOMENTUM:
        for i in range(0, 8):
            if (not CheckPointer(_setitem(indicator, i, CSymbol(Symbol_[i])))) or (not indicator[i].Handle(iMomentum(Symbol_[i], PERIOD_CURRENT, MomentumPeriod, MomentumPrice), i)):
                return INIT_FAILED
        shortName = StringFormat('Correl8 Momentum(%d)', MomentumPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 3)
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
    elif _sw1 == INDICATOR_TRIX:
        for i in range(0, 8):
            if (not CheckPointer(_setitem(indicator, i, CSymbol(Symbol_[i])))) or (not indicator[i].Handle(iTriX(Symbol_[i], PERIOD_CURRENT, TrixPeriod, TrixPrice), i)):
                return INIT_FAILED
        shortName = StringFormat('Correl8 TriX(%d)', TrixPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 5)
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
    elif _sw1 == INDICATOR_MFI:
        for i in range(0, 8):
            if (not CheckPointer(_setitem(indicator, i, CSymbol(Symbol_[i])))) or (not indicator[i].Handle(iMFI(Symbol_[i], PERIOD_CURRENT, MFIPeriod, MFIVolume), i)):
                return INIT_FAILED
        shortName = StringFormat('Correl8 MFI(%d)', MFIPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 1)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -indicator_level3)
    IndicatorSetString(INDICATOR_SHORTNAME, shortName)
    windowNo = ChartWindowFind()
    i = 0
    while i < indicator_buffers:
        if _setitem(currency, i, CBuffer()) is None:
            return INIT_FAILED
        currency[i].SetIndexBuffer(i, INDICATOR_DATA)
        currency[i].ArraySetAsSeries(True)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        i += 1
    label = ""
    label = _str(indicator_label1)
    Currency[0] = label
    label = _str(indicator_label2)
    Currency[1] = label
    label = _str(indicator_label3)
    Currency[2] = label
    label = _str(indicator_label4)
    Currency[3] = label
    label = _str(indicator_label5)
    Currency[4] = label
    label = _str(indicator_label6)
    Currency[5] = label
    label = _str(indicator_label7)
    Currency[6] = label
    label = _str(indicator_label8)
    Currency[7] = label
    label = _str(indicator_label9)
    Currency[8] = label
    IsVisible[0] = bAUD
    IsVisible[1] = bCAD
    IsVisible[2] = bCHF
    IsVisible[3] = bEUR
    IsVisible[4] = bGBP
    IsVisible[5] = bJPY
    IsVisible[6] = bNZD
    IsVisible[7] = bXAU
    IsVisible[8] = bUSD
    if Auto:
        i = 0
        while i < indicator_plots:
            IsVisible[i] = False
            if StringFind(Symbol(), Currency[i]) != -1:
                IsVisible[i] = True
            i += 1
    if not CheckPointer((lbl := CChartObjectLabel())):
        return INIT_FAILED
    CreateLabels()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    global ind
    toCount = ((rates_total - prev_calculated) if (rates_total != prev_calculated) else 1)
    if not prev_calculated:
        barsTotal = MathMin(BarsToCount, rates_total)
        result = 0
        for i in range(0, 8):
            if (not CheckPointer((ind := indicator[i]))) or (not ind.BarsCalculated()):
                result += 1
            if barsTotal > ind.Bars:
                barsTotal = ind.Bars
        if barsTotal < 100 or result > 0:
            return 0
        i = 0
        while i < indicator_buffers:
            if CheckPointer(currency[i]):
                currency[i].ArrayInitialize(EMPTY_VALUE)
            i += 1
        toCount = barsTotal - 1
    if OnTick(toCount) != toCount:
        return 0
    return rates_total

def OnDeinit(reason):
    ObjectsDeleteAll(chartID, windowNo, OBJ_LABEL)
    if CheckPointer(lbl):
        _delete(lbl)
    for i in range(0, 8):
        if CheckPointer(indicator[i]):
            _delete(indicator[i])
    i = 0
    while i < indicator_buffers:
        if CheckPointer(currency[i]):
            _delete(currency[i])
        i += 1
    return

def OnTick(to_count):
    global cur, ind
    for i in range(0, 8):
        if (not CheckPointer((ind := indicator[i]))) or ind.CopyBuffer(0, to_count + 1) != (to_count + 1):
            printf('CopyBuffer for %s failed', Symbols[i])
            return 0
    usd = currency[8]
    i = to_count - 1
    h = 0
    while i >= 0:
        usd.close = 0.0
        h = 0
        for h in range(h, 8):
            cur = currency[h]
            _sw2 = Indicator
            if _sw2 == INDICATOR_MA:
                curClose = indicator[h][i]
                preClose = indicator[h][i + 1]
                if h == 5:
                    usd.close += _setattr(cur, 'close', (((preClose - curClose) / 100) if (curClose and preClose) else 0.0))
                elif h == 7:
                    usd.close += _setattr(cur, 'close', ((_fdiv(1000, preClose) - _fdiv(1000, curClose)) if (curClose and preClose) else 0.0))
                elif h == 1 or h == 2:
                    usd.close += _setattr(cur, 'close', ((preClose - curClose) if (curClose and preClose) else 0.0))
                else:
                    usd.close += _setattr(cur, 'close', ((_fdiv(1, preClose) - _fdiv(1, curClose)) if (curClose and preClose) else 0.0))
            elif _sw2 == INDICATOR_MACD:
                if h == 5:
                    usd.close += _setattr(cur, 'close', (-indicator[h][i]) / 100)
                elif h == 7:
                    usd.close += _setattr(cur, 'close', indicator[h][i] / 10000)
                elif h == 1 or h == 2:
                    usd.close += _setattr(cur, 'close', -indicator[h][i])
                else:
                    usd.close += _setattr(cur, 'close', indicator[h][i])
            elif _sw2 in (INDICATOR_STOCHASTIC, INDICATOR_RSI, INDICATOR_MFI):
                if (h == 1 or h == 2) or h == 5:
                    usd.close += _setattr(cur, 'close', -(indicator[h][i] - 50))
                else:
                    usd.close += _setattr(cur, 'close', indicator[h][i] - 50)
            elif _sw2 in (INDICATOR_CCI, INDICATOR_RVI):
                if (h == 1 or h == 2) or h == 5:
                    usd.close += _setattr(cur, 'close', -indicator[h][i])
                else:
                    usd.close += _setattr(cur, 'close', indicator[h][i])
            elif _sw2 == INDICATOR_DEMARKER:
                if (h == 1 or h == 2) or h == 5:
                    usd.close += _setattr(cur, 'close', -(indicator[h][i] - 0.5))
                else:
                    usd.close += _setattr(cur, 'close', indicator[h][i] - 0.5)
            elif _sw2 == INDICATOR_MOMENTUM:
                if (h == 1 or h == 2) or h == 5:
                    usd.close += _setattr(cur, 'close', -(indicator[h][i] - 100))
                else:
                    usd.close += _setattr(cur, 'close', indicator[h][i] - 100)
            elif _sw2 == INDICATOR_TRIX:
                if (h == 1 or h == 2) or h == 5:
                    usd.close += _setattr(cur, 'close', (-indicator[h][i]) * 100)
                else:
                    usd.close += _setattr(cur, 'close', indicator[h][i] * 100)
        else:
            h = _range_end(h, 8, 1)
        h = 0
        for h in range(h, 8):
            cur = currency[h]
            cur.close += (usd.close - cur.close) / (-(8 - 1))
        else:
            h = _range_end(h, 8, 1)
        usd.close = usd.close / -8
        h = 0
        while h < indicator_buffers:
            cur = currency[h]
            cur.Close(i, (cur.close if IsVisible[h] else EMPTY_VALUE))
            h += 1
        i -= 1
    return to_count

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ >= CHARTEVENT_CUSTOM:
        OnTick(_int(lparam + 1))
        if lbl is not None:
            lbl.SetString_2(_int(OBJPROP_TEXT), sparam)
        ChartRedraw(chartID)

def CreateLabels():
    Color = Arr.of([_uint(indicator_color1), _uint(indicator_color2), _uint(indicator_color3), _uint(indicator_color4), _uint(indicator_color5), _uint(indicator_color6), _uint(indicator_color7), _uint(indicator_color8), _uint(indicator_color9)], fill=0, dyn=False, size=indicator_buffers)
    xStart = 4
    xIncrement = 24
    yStart = 16
    yIncrement = 0
    i = 0
    while i < indicator_buffers:
        if not IsVisible[i]:
            PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
            i += 1
            continue
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, True)
        ObjectCreate_u(Currency[i], xStart, yStart, Color[i])
        xStart += xIncrement
        yStart += yIncrement
        i += 1
    lbl.Create(chartID, 'Symbol', windowNo, 5, 20)
    lbl.Corner_1(CORNER_LEFT_LOWER)
    lbl.Color_1(clrWhite)
    lbl.SetString_2(_int(OBJPROP_TEXT), ' ')
    lbl.Font_1('Arial Bold')
    lbl.FontSize_1(10)

def ObjectCreate_u(label, x, y, clr):
    name = label + _str(windowNo)
    ObjectDelete(chartID, name)
    ObjectCreate(chartID, name, OBJ_LABEL, windowNo, 0, 0)
    ObjectSetString(chartID, name, OBJPROP_TEXT, label)
    ObjectSetString(chartID, name, OBJPROP_FONT, 'Arial Bold')
    ObjectSetInteger(chartID, name, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(chartID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chartID, name, OBJPROP_YDISTANCE, y)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Correlate(_MQL5Indicator):
    name = 'Correlate'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Indicator': _Choice({0: 'Moving Average', 1: 'Moving Average Convergence/Divergence', 2: 'Stochastic Oscillator', 3: 'Relative Strength Index', 4: 'Commodity Channel Index', 5: 'Relative Vigour Index', 6: 'DeMarker Oscillator', 7: 'Momentum Oscillator', 8: 'Triple Exponential Average', 9: 'Money Flow Index'}, default=3),
        'BarsToCount': 500,  # Bars to count
        'MAPeriod': 14,  # MA Period
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Method
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Price
        'FastEMA': 12,  # Fast EMA Period
        'SlowEMA': 26,  # Slow EMA Period
        'MACDPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MACD Price
        'Kperiod': 7,  # K Period
        'Slowing': 3,
        'PriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Price Field
        'RSIPeriod': 14,  # RSI Period
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI Price
        'CCIPeriod': 14,  # CCI Period
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # CCI Price
        'RVIPeriod': 14,  # RVI Period
        'DeMarkerPeriod': 14,  # DeMarker Period
        'MomentumPeriod': 14,  # Momentum Period
        'MomentumPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Momentum Price
        'TrixPeriod': 14,  # TriX Period
        'TrixPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # TriX Price
        'MFIPeriod': 14,  # MFI Period
        'MFIVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # MFI Volume
        'Auto': False,  # Display chart currencies
        'bAUD': True,  # Display Aussie
        'bCAD': True,  # Display Loonie
        'bCHF': True,  # Display Swissy
        'bEUR': True,  # Display Fiber
        'bGBP': True,  # Display Sterling
        'bJPY': True,  # Display Yen
        'bNZD': True,  # Display Kiwi
        'bXAU': True,  # Display Gold
        'bUSD': True,  # Display Greenback
        'Pips': True,  # Ticks on pip change only
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

