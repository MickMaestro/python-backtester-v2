"""Pip Chart — converted from MQL5: MQL5 Indicators/Pip Chart/Pip Chart.mq5

Copyright: Copyright 2019, ernst; Link: https://www.mql5.com/en/users/pippod; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Functions not available here: ChartPriceOnDropped, ChartTimeOnDropped, ChartWindowOnDropped, ChartXOnDropped, ChartYOnDropped, FileReadLong, FileWriteLong
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2019, ernst', 'link': 'https://www.mql5.com/en/users/pippod', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {}, 'colors': {1: [14772545, 2237106, 65535]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Pip Chart', 'source': 'MQL5 Indicators/Pip Chart/Pip Chart.mq5', 'folder': 'Pip Chart', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 1, 'label': 'Chart mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

CHAR_VALUE = 0  # MQL5 constant unknown to the converter
INT_VALUE = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
Mode = _input('Mode', CHART_CANDLES)  # Chart mode
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
muldiv = 0
open = 0.0
close = 0.0
line = None

class CChart(CObject):
    _q_fields = ('m_chart_id',)
    def __init__(self):
        CObject.__init__(self)
        self.m_chart_id = 0
        self.m_chart_id = -1
    def _q_dtor(self):
        if self.m_chart_id != -1:
            self.Close()
    def ChartId(self):
        return self.m_chart_id
    def Type(self):
        return 0x1111
    def Mode_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ChartGetInteger(self.m_chart_id, CHART_MODE)
    def Mode_1(self, mode):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_MODE, mode)
    def Foreground_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_FOREGROUND))
    def Foreground_1(self, foreground):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_FOREGROUND, foreground)
    def Shift_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHIFT))
    def Shift_1(self, shift):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHIFT, shift)
    def ShiftSize_0(self):
        if self.m_chart_id == -1:
            return DBL_MAX
        return ChartGetDouble(self.m_chart_id, CHART_SHIFT_SIZE)
    def ShiftSize_1(self, shift):
        if self.m_chart_id == -1:
            return False
        if shift < 10:
            shift = 10.0
        if shift > 50:
            shift = 50.0
        return ChartSetDouble(self.m_chart_id, CHART_SHIFT_SIZE, shift)
    def AutoScroll_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_AUTOSCROLL))
    def AutoScroll_1(self, auto_scroll):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_AUTOSCROLL, auto_scroll)
    def Scale_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_SCALE))
    def Scale_1(self, shift):
        if self.m_chart_id == -1:
            return False
        if shift < 0:
            shift = 0
        if shift > 32:
            shift = 32
        return ChartSetInteger(self.m_chart_id, CHART_SCALE, shift)
    def ScaleFix_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX))
    def ScaleFix_1(self, scale_fix):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SCALEFIX, scale_fix)
    def ScaleFix_11_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX_11))
    def ScaleFix_11_1(self, scale_fix_11):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SCALEFIX_11, scale_fix_11)
    def FixedMax_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_FIXED_MAX)
    def FixedMax_1(self, fixed_max):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, CHART_FIXED_MAX, fixed_max)
    def FixedMin_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_FIXED_MIN)
    def FixedMin_1(self, fixed_min):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, CHART_FIXED_MIN, fixed_min)
    def ScalePPB_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR))
    def ScalePPB_1(self, scale_ppb):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR, scale_ppb)
    def PointsPerBar_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_POINTS_PER_BAR)
    def PointsPerBar_1(self, points_per_bar):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, CHART_POINTS_PER_BAR, points_per_bar)
    def ShowOHLC_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_OHLC))
    def ShowOHLC_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_OHLC, show)
    def ShowLineBid_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_BID_LINE))
    def ShowLineBid_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_BID_LINE, show)
    def ShowLineAsk_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE))
    def ShowLineAsk_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE, show)
    def ShowLastLine_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE))
    def ShowLastLine_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE, show)
    def ShowPeriodSep_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP))
    def ShowPeriodSep_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP, show)
    def ShowGrid_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_GRID))
    def ShowGrid_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_GRID, show)
    def ShowVolumes_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ChartGetInteger(self.m_chart_id, CHART_SHOW_VOLUMES)
    def ShowVolumes_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_VOLUMES, show)
    def ShowObjectDescr_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR))
    def ShowObjectDescr_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR, show)
    def ShowDateScale(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_DATE_SCALE, show)
    def ShowPriceScale(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_PRICE_SCALE, show)
    def ColorBackground_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_BACKGROUND))
    def ColorBackground_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_BACKGROUND, new_color)
    def ColorForeground_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_FOREGROUND))
    def ColorForeground_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_FOREGROUND, new_color)
    def ColorGrid_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_GRID))
    def ColorGrid_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_GRID, new_color)
    def ColorBarUp_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CHART_UP))
    def ColorBarUp_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CHART_UP, new_color)
    def ColorBarDown_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CHART_DOWN))
    def ColorBarDown_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CHART_DOWN, new_color)
    def ColorCandleBull_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BULL))
    def ColorCandleBull_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BULL, new_color)
    def ColorCandleBear_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BEAR))
    def ColorCandleBear_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BEAR, new_color)
    def ColorChartLine_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CHART_LINE))
    def ColorChartLine_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CHART_LINE, new_color)
    def ColorVolumes_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_VOLUME))
    def ColorVolumes_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_VOLUME, new_color)
    def ColorLineBid_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_BID))
    def ColorLineBid_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_BID, new_color)
    def ColorLineAsk_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_ASK))
    def ColorLineAsk_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_ASK, new_color)
    def ColorLineLast_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_LAST))
    def ColorLineLast_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_LAST, new_color)
    def ColorStopLevels_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_STOP_LEVEL))
    def ColorStopLevels_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_STOP_LEVEL, new_color)
    def BringToTop(self):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_BRING_TO_TOP, True)
    def EventObjectCreate(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_EVENT_OBJECT_CREATE, flag)
    def EventObjectDelete(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_EVENT_OBJECT_DELETE, flag)
    def EventMouseMove(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_EVENT_MOUSE_MOVE, flag)
    def MouseScroll(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_MOUSE_SCROLL, flag)
    def VisibleBars(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WIDTH_IN_BARS))
    def WindowsTotal(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WINDOWS_TOTAL))
    def WindowIsVisible(self, num):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_WINDOW_IS_VISIBLE, num))
    def WindowHandle(self):
        if self.m_chart_id == -1:
            return INVALID_HANDLE
        return _int(ChartGetInteger(self.m_chart_id, CHART_WINDOW_HANDLE))
    def FirstVisibleBar(self):
        if self.m_chart_id == -1:
            return -1
        return _int(ChartGetInteger(self.m_chart_id, CHART_FIRST_VISIBLE_BAR))
    def WidthInBars(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WIDTH_IN_BARS))
    def WidthInPixels(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WIDTH_IN_PIXELS))
    def HeightInPixels(self, num):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_HEIGHT_IN_PIXELS, num))
    def SubwindowY(self, num):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WINDOW_YDISTANCE, num))
    def PriceMin(self, num):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_PRICE_MIN, num)
    def PriceMax(self, num):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_PRICE_MAX, num)
    def IsObject(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_IS_OBJECT))
    def Attach_0(self):
        self.m_chart_id = ChartID()
    def Attach_1(self, chart):
        self.m_chart_id = chart
    def FirstChart(self):
        self.m_chart_id = ChartFirst()
    def NextChart(self):
        self.m_chart_id = ChartNext(self.m_chart_id)
    def Open(self, symbol_name, timeframe):
        self.m_chart_id = ChartOpen(symbol_name, timeframe)
        if self.m_chart_id == 0:
            self.m_chart_id = -1
        return self.m_chart_id
    def Detach(self):
        self.m_chart_id = -1
    def Close(self):
        if self.m_chart_id != -1:
            ChartClose(self.m_chart_id)
            self.m_chart_id = -1
    def Navigate(self, position, shift=0):
        if self.m_chart_id == -1:
            return False
        return ChartNavigate(self.m_chart_id, position, shift)
    def Symbol(self):
        return ChartSymbol(self.m_chart_id)
    def Period(self):
        return ChartPeriod(self.m_chart_id)
    def Redraw(self):
        ChartRedraw(self.m_chart_id)
    def GetInteger_2(self, prop_id, subwindow=0):
        if self.m_chart_id == -1:
            return 0
        return ChartGetInteger(self.m_chart_id, prop_id, subwindow)
    def GetInteger_3(self, prop_id, subwindow, value):
        if self.m_chart_id == -1:
            return False
        return (ChartGetInteger(self.m_chart_id, prop_id, subwindow, value) != 0)
    def SetInteger(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, prop_id, value)
    def GetDouble_2(self, prop_id, subwindow=0):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, prop_id, subwindow)
    def GetDouble_3(self, prop_id, subwindow, value):
        if self.m_chart_id == -1:
            return False
        return (ChartGetDouble(self.m_chart_id, prop_id, subwindow, value) != 0)
    def SetDouble(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, prop_id, value)
    def GetString_1(self, prop_id):
        if self.m_chart_id == -1:
            return ''
        return ChartGetString(self.m_chart_id, prop_id)
    def GetString_2(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetString(self.m_chart_id, prop_id, value))
    def SetString(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ChartSetString(self.m_chart_id, prop_id, value)
    def SetSymbolPeriod(self, symbol, period):
        if self.m_chart_id == -1:
            return False
        return ChartSetSymbolPeriod(self.m_chart_id, symbol, period)
    def ApplyTemplate(self, filename):
        if self.m_chart_id == -1:
            return False
        return ChartApplyTemplate(self.m_chart_id, filename)
    def ScreenShot(self, filename, width, height, align_mode=ALIGN_RIGHT):
        if self.m_chart_id == -1:
            return False
        return ChartScreenShot(self.m_chart_id, filename, width, height, align_mode)
    def WindowOnDropped(self):
        if self.m_chart_id == -1:
            return 0
        return _missing('ChartWindowOnDropped')()
    def PriceOnDropped(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return _missing('ChartPriceOnDropped')()
    def TimeOnDropped(self):
        if self.m_chart_id == -1:
            return False
        return _long(_missing('ChartTimeOnDropped')())
    def XOnDropped(self):
        if self.m_chart_id == -1:
            return 0
        return _int(_missing('ChartXOnDropped')())
    def YOnDropped(self):
        if self.m_chart_id == -1:
            return 0
        return _int(_missing('ChartYOnDropped')())
    def IndicatorAdd(self, subwin, handle):
        if self.m_chart_id == -1:
            return False
        return ChartIndicatorAdd(self.m_chart_id, subwin, handle)
    def IndicatorDelete(self, subwin, name):
        if self.m_chart_id == -1:
            return False
        return ChartIndicatorDelete(self.m_chart_id, subwin, name)
    def IndicatorsTotal(self, subwin):
        if self.m_chart_id == -1:
            return 0
        return ChartIndicatorsTotal(self.m_chart_id, subwin)
    def IndicatorName(self, subwin, index):
        if self.m_chart_id == -1:
            return ''
        return ChartIndicatorName(self.m_chart_id, subwin, index)
    def Save(self, file_handle):
        work_str = ""
        work_int = 0
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if _missing('FileWriteLong')(file_handle, -1) != 8:
            return False
        if FileWriteInteger(file_handle, self.Type(), INT_VALUE) != INT_VALUE:
            return False
        work_str = self.Symbol()
        work_int = StringLen(work_str)
        if FileWriteInteger(file_handle, work_int, INT_VALUE) != INT_VALUE:
            return False
        if work_int != 0:
            if FileWriteString(file_handle, work_str, work_int) != work_int:
                return False
        if FileWriteInteger(file_handle, self.Period(), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_MODE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_FOREGROUND)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHIFT)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHIFT)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_AUTOSCROLL)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX_11)), CHAR_VALUE) != 1:
            return False
        if FileWriteDouble(file_handle, ChartGetDouble(self.m_chart_id, CHART_FIXED_MAX)) != 8:
            return False
        if FileWriteDouble(file_handle, ChartGetDouble(self.m_chart_id, CHART_FIXED_MIN)) != 8:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR)), CHAR_VALUE) != 1:
            return False
        if FileWriteDouble(file_handle, ChartGetDouble(self.m_chart_id, CHART_POINTS_PER_BAR)) != 8:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_OHLC)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_BID_LINE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_GRID)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_VOLUMES)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR)), CHAR_VALUE) != 1:
            return False
        return True
    def Load(self, file_handle):
        resutl = True
        work_str = ""
        work_int = 0
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if _missing('FileReadLong')(file_handle) != -1:
            return False
        if FileReadInteger(file_handle, INT_VALUE) != self.Type():
            return False
        work_int = FileReadInteger(file_handle)
        if work_int != 0:
            work_str = FileReadString(file_handle, work_int)
        else:
            work_str = ''
        work_int = FileReadInteger(file_handle)
        self.SetSymbolPeriod(work_str, work_int)
        if not ChartSetInteger(self.m_chart_id, CHART_MODE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_FOREGROUND, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHIFT, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHIFT, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_AUTOSCROLL, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALEFIX, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALEFIX_11, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetDouble(self.m_chart_id, CHART_FIXED_MAX, FileReadDatetime(file_handle)):
            return False
        if not ChartSetDouble(self.m_chart_id, CHART_FIXED_MIN, FileReadDatetime(file_handle)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetDouble(self.m_chart_id, CHART_POINTS_PER_BAR, FileReadDatetime(file_handle)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_OHLC, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_BID_LINE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_GRID, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_VOLUMES, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        return resutl

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
    global line, muldiv
    digits = Digits() - 1
    IndicatorSetInteger(INDICATOR_DIGITS, digits)
    chrt.Attach_0()
    chrt.Mode_1(Mode)
    chrt.ShowLineBid_1(False)
    chrt.ColorBarUp_1(clrNONE)
    chrt.ColorBarDown_1(clrNONE)
    chrt.ColorCandleBull_1(clrNONE)
    chrt.ColorCandleBear_1(clrNONE)
    chrt.ColorChartLine_1(clrNONE)
    _sw1 = Mode
    if _sw1 == CHART_BARS:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_BARS)
        PlotIndexSetString(0, PLOT_LABEL, 'Open;High;Low;Close')
        Width()
        SetIndexBuffer(0, OpenBuffer, INDICATOR_DATA)
        SetIndexBuffer(1, HighBuffer, INDICATOR_DATA)
        SetIndexBuffer(2, LowBuffer, INDICATOR_DATA)
        SetIndexBuffer(3, CloseBuffer, INDICATOR_DATA)
        SetIndexBuffer(4, ColorBuffer, INDICATOR_COLOR_INDEX)
    elif _sw1 == CHART_CANDLES:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_CANDLES)
        PlotIndexSetString(0, PLOT_LABEL, 'Open;High;Low;Close')
        SetIndexBuffer(0, OpenBuffer, INDICATOR_DATA)
        SetIndexBuffer(1, HighBuffer, INDICATOR_DATA)
        SetIndexBuffer(2, LowBuffer, INDICATOR_DATA)
        SetIndexBuffer(3, CloseBuffer, INDICATOR_DATA)
        SetIndexBuffer(4, ColorBuffer, INDICATOR_COLOR_INDEX)
    elif _sw1 == CHART_LINE:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_LINE)
        PlotIndexSetString(0, PLOT_LABEL, 'Close')
        Width()
        SetIndexBuffer(0, CloseBuffer, INDICATOR_DATA)
        SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
        SetIndexBuffer(2, OpenBuffer, INDICATOR_CALCULATIONS)
        SetIndexBuffer(3, HighBuffer, INDICATOR_CALCULATIONS)
        SetIndexBuffer(4, LowBuffer, INDICATOR_CALCULATIONS)
    muldiv = _int(MathPow(10, digits))
    if not CheckPointer((line := CChartObjectHLine())):
        return INIT_FAILED
    line.Create(ChartID(), 'bidLine', 0, 0.0)
    line.SetInteger_2(OBJPROP_COLOR, clrLightSlateGray)
    line.SetInteger_2(OBJPROP_SELECTABLE, False)
    line.SetString_2(_int(OBJPROP_TOOLTIP), '\n')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_volume, Volume, Spread):
    global close, open
    begin = (prev_calculated if (rates_total != prev_calculated) else (prev_calculated - 1))
    if not prev_calculated:
        CloseBuffer[0] = (_fdiv(MathFloor(Close[0] * muldiv), muldiv) if (Close[0] > Open[0]) else _fdiv(MathCeil(Close[0] * muldiv), muldiv))
        LowBuffer[0] = CloseBuffer[0]
        HighBuffer[0] = LowBuffer[0]
        OpenBuffer[((begin := begin + 1) - 1)] = HighBuffer[0]
    for i in range(begin, rates_total):
        if rates_total != prev_calculated:
            open = (_fdiv(MathFloor(Open[i] * muldiv), muldiv) if (Open[i] > CloseBuffer[i - 1]) else _fdiv(MathCeil(Open[i] * muldiv), muldiv))
            OpenBuffer[i] = open
        close = (_fdiv(MathFloor(Close[i] * muldiv), muldiv) if (Close[i] > open) else _fdiv(MathCeil(Close[i] * muldiv), muldiv))
        CloseBuffer[i] = close
        HighBuffer[i] = MathMax(open, MathMax(close, _fdiv(MathFloor(High[i] * muldiv), muldiv)))
        LowBuffer[i] = MathMin(open, MathMin(close, _fdiv(MathCeil(Low[i] * muldiv), muldiv)))
        if Mode == CHART_LINE:
            ColorBuffer[i] = (0 if (close > CloseBuffer[i - 1]) else 1 if (close < CloseBuffer[i - 1]) else 2)
        else:
            ColorBuffer[i] = (0 if (close > open) else 1 if (close < open) else 2)
    if line is not None:
        line.SetDouble_2(OBJPROP_PRICE, CloseBuffer[rates_total - 1])
    return rates_total

def OnDeinit(reason):
    if CheckPointer(line):
        line.Delete()
        _delete(line)
    chrt.ShowLineBid_1(True)
    chrt.ColorBarUp_1(clrLime)
    chrt.ColorBarDown_1(clrLime)
    chrt.ColorCandleBull_1(clrBlack)
    chrt.ColorCandleBear_1(clrWhite)
    chrt.ColorChartLine_1(clrLime)
    chrt.Detach()

def OnChartEvent(id_, lparam, dparam, sparam):
    global _s_OnChartEvent_scale
    if id_ == CHARTEVENT_CHART_CHANGE:
        if _s_OnChartEvent_scale != chrt.Scale_0() and (Mode == CHART_LINE or Mode == CHART_BARS):
            Width()
            chrt.Redraw()
            _s_OnChartEvent_scale = chrt.Scale_0()

def Width():
    _sw2 = chrt.Scale_0()
    if _sw2 in (0, 1):
        return PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 1)
    elif _sw2 == 2:
        return PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2)
    elif _sw2 == 3:
        return PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 3)
    elif _sw2 == 4:
        return PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 4)
    elif _sw2 == 5:
        return PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 5)
    return False

# ---- global variables initialised from expressions
chrt = _alloc(CChart)
chrt.__init__()

# ---- static local variables
_s_OnChartEvent_scale = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PipChart(_MQL5Indicator):
    name = 'Pip Chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Mode': _Choice({0: 'CHART_BARS', 1: 'CHART_CANDLES', 2: 'CHART_LINE'}, default=1),  # Chart mode
    }

