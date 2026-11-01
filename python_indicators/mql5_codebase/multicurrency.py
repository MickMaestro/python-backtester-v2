"""multicurrency — converted from MQL5: MQL5 Indicators/MultiCurrency/multicurrency.mq5

Copyright: 2012,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: ChartPriceOnDropped, ChartTimeOnDropped, ChartWindowOnDropped, ChartXOnDropped, ChartYOnDropped, FileReadLong, FileWriteLong
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': '2012,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'multicurrency', 'source': 'MQL5 Indicators/MultiCurrency/multicurrency.mq5', 'folder': 'MultiCurrency', 'inputs': [{'mql': 'ShowIndicator1', 'py': 'ShowIndicator1', 'param': 'ShowIndicator1', 'type': 'bool', 'default': True, 'label': 'permission to display the indicator', 'sinput': False}, {'mql': 'Symbol1', 'py': 'Symbol1', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'currency', 'sinput': False}, {'mql': 'Direct1', 'py': 'Direct1', 'param': 'Direct1', 'type': 'bool', 'default': True, 'label': 'no chart inversion', 'sinput': False}, {'mql': 'ShowIndicator2', 'py': 'ShowIndicator2', 'param': 'ShowIndicator2', 'type': 'bool', 'default': True, 'label': 'permission to display the indicator', 'sinput': False}, {'mql': 'Symbol2', 'py': 'Symbol2', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'currency', 'sinput': False}, {'mql': 'Direct2', 'py': 'Direct2', 'param': 'Direct2', 'type': 'bool', 'default': True, 'label': 'no chart inversion', 'sinput': False}, {'mql': 'ShowIndicator3', 'py': 'ShowIndicator3', 'param': 'ShowIndicator3', 'type': 'bool', 'default': True, 'label': 'permission to display the indicator', 'sinput': False}, {'mql': 'Symbol3', 'py': 'Symbol3', 'param': None, 'type': 'string', 'default': 'AUDUSD', 'label': 'currency', 'sinput': False}, {'mql': 'Direct3', 'py': 'Direct3', 'param': 'Direct3', 'type': 'bool', 'default': True, 'label': 'no chart inversion', 'sinput': False}, {'mql': 'ShowIndicator4', 'py': 'ShowIndicator4', 'param': 'ShowIndicator4', 'type': 'bool', 'default': True, 'label': 'permission to display the indicator', 'sinput': False}, {'mql': 'Symbol4', 'py': 'Symbol4', 'param': None, 'type': 'string', 'default': 'NZDUSD', 'label': 'currency', 'sinput': False}, {'mql': 'Direct4', 'py': 'Direct4', 'param': 'Direct4', 'type': 'bool', 'default': True, 'label': 'no chart inversion', 'sinput': False}, {'mql': 'ShowIndicator5', 'py': 'ShowIndicator5', 'param': 'ShowIndicator5', 'type': 'bool', 'default': True, 'label': 'permission to display the indicator', 'sinput': False}, {'mql': 'Symbol5', 'py': 'Symbol5', 'param': None, 'type': 'string', 'default': 'USDCHF', 'label': 'currency', 'sinput': False}, {'mql': 'Direct5', 'py': 'Direct5', 'param': 'Direct5', 'type': 'bool', 'default': False, 'label': 'no chart inversion', 'sinput': False}, {'mql': 'ShowIndicator6', 'py': 'ShowIndicator6', 'param': 'ShowIndicator6', 'type': 'bool', 'default': True, 'label': 'permission to display the indicator', 'sinput': False}, {'mql': 'Symbol6', 'py': 'Symbol6', 'param': None, 'type': 'string', 'default': 'USDJPY', 'label': 'currency', 'sinput': False}, {'mql': 'Direct6', 'py': 'Direct6', 'param': 'Direct6', 'type': 'bool', 'default': False, 'label': 'no chart inversion', 'sinput': False}, {'mql': 'ShowIndicator7', 'py': 'ShowIndicator7', 'param': 'ShowIndicator7', 'type': 'bool', 'default': True, 'label': 'permission to display the indicator', 'sinput': False}, {'mql': 'Symbol7', 'py': 'Symbol7', 'param': None, 'type': 'string', 'default': 'USDCAD', 'label': 'currency', 'sinput': False}, {'mql': 'Direct7', 'py': 'Direct7', 'param': 'Direct7', 'type': 'bool', 'default': False, 'label': 'no chart inversion', 'sinput': False}, {'mql': 'ShowIndicator8', 'py': 'ShowIndicator8', 'param': 'ShowIndicator8', 'type': 'bool', 'default': True, 'label': 'permission to display the indicator', 'sinput': False}, {'mql': 'Symbol8', 'py': 'Symbol8', 'param': None, 'type': 'string', 'default': 'XAUUSD', 'label': 'currency', 'sinput': False}, {'mql': 'Direct8', 'py': 'Direct8', 'param': 'Direct8', 'type': 'bool', 'default': True, 'label': 'no chart inversion', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

CHAR_VALUE = 0  # MQL5 constant unknown to the converter
INT_VALUE = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
ShowIndicator1 = _input('ShowIndicator1', True)  # permission to display the indicator
Symbol1 = _input('Symbol1', 'EURUSD')  # currency
Direct1 = _input('Direct1', True)  # no chart inversion
ShowIndicator2 = _input('ShowIndicator2', True)  # permission to display the indicator
Symbol2 = _input('Symbol2', 'GBPUSD')  # currency
Direct2 = _input('Direct2', True)  # no chart inversion
ShowIndicator3 = _input('ShowIndicator3', True)  # permission to display the indicator
Symbol3 = _input('Symbol3', 'AUDUSD')  # currency
Direct3 = _input('Direct3', True)  # no chart inversion
ShowIndicator4 = _input('ShowIndicator4', True)  # permission to display the indicator
Symbol4 = _input('Symbol4', 'NZDUSD')  # currency
Direct4 = _input('Direct4', True)  # no chart inversion
ShowIndicator5 = _input('ShowIndicator5', True)  # permission to display the indicator
Symbol5 = _input('Symbol5', 'USDCHF')  # currency
Direct5 = _input('Direct5', False)  # no chart inversion
ShowIndicator6 = _input('ShowIndicator6', True)  # permission to display the indicator
Symbol6 = _input('Symbol6', 'USDJPY')  # currency
Direct6 = _input('Direct6', False)  # no chart inversion
ShowIndicator7 = _input('ShowIndicator7', True)  # permission to display the indicator
Symbol7 = _input('Symbol7', 'USDCAD')  # currency
Direct7 = _input('Direct7', False)  # no chart inversion
ShowIndicator8 = _input('ShowIndicator8', True)  # permission to display the indicator
Symbol8 = _input('Symbol8', 'XAUUSD')  # currency
Direct8 = _input('Direct8', True)  # no chart inversion

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

def OnInit():
    digit = 0
    InpInd_Handle = 0
    count = 0
    if ShowIndicator1:
        digit = _int(SymbolInfoInteger(Symbol1, SYMBOL_DIGITS))
        InpInd_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'CrossIndex', Symbol1, clrRed, STYLE_SOLID, PRICE_CLOSE, digit, Direct1)
        if InpInd_Handle == INVALID_HANDLE:
            Print(' Failed to get the CrossIndex indicator handle by ', Symbol1)
    cchart[count].Attach_1(0)
    ResetLastError()
    if not cchart[count].IndicatorAdd(count + 1, InpInd_Handle):
        Print(' Failed to add the CrossIndex indicator by ', Symbol1)
    if ShowIndicator2:
        digit = _int(SymbolInfoInteger(Symbol2, SYMBOL_DIGITS))
        InpInd_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'CrossIndex', Symbol2, clrRed, STYLE_SOLID, PRICE_CLOSE, digit, Direct2)
        if InpInd_Handle == INVALID_HANDLE:
            Print(' Failed to get the CrossIndex indicator handle by ', Symbol2)
    count += 1
    cchart[count].Attach_1(0)
    ResetLastError()
    if not cchart[count].IndicatorAdd(count + 1, InpInd_Handle):
        Print(' Failed to add the CrossIndex indicator by ', Symbol2)
    if ShowIndicator3:
        digit = _int(SymbolInfoInteger(Symbol3, SYMBOL_DIGITS))
        InpInd_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'CrossIndex', Symbol3, clrRed, STYLE_SOLID, PRICE_CLOSE, digit, Direct3)
        if InpInd_Handle == INVALID_HANDLE:
            Print(' Failed to get the CrossIndex indicator handle by ', Symbol3)
    count += 1
    cchart[count].Attach_1(0)
    ResetLastError()
    if not cchart[count].IndicatorAdd(count + 1, InpInd_Handle):
        Print(' Failed to add the CrossIndex indicator by ', Symbol3)
    if ShowIndicator4:
        digit = _int(SymbolInfoInteger(Symbol4, SYMBOL_DIGITS))
        InpInd_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'CrossIndex', Symbol4, clrRed, STYLE_SOLID, PRICE_CLOSE, digit, Direct4)
        if InpInd_Handle == INVALID_HANDLE:
            Print(' Failed to get the CrossIndex indicator handle by ', Symbol4)
    count += 1
    cchart[count].Attach_1(0)
    ResetLastError()
    if not cchart[count].IndicatorAdd(count + 1, InpInd_Handle):
        Print(' Failed to add the CrossIndex indicator by ', Symbol4)
    if ShowIndicator5:
        digit = _int(SymbolInfoInteger(Symbol5, SYMBOL_DIGITS))
        InpInd_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'CrossIndex', Symbol5, clrRed, STYLE_SOLID, PRICE_CLOSE, digit, Direct5)
        if InpInd_Handle == INVALID_HANDLE:
            Print(' Failed to get the CrossIndex indicator handle by ', Symbol5)
    count += 1
    cchart[count].Attach_1(0)
    ResetLastError()
    if not cchart[count].IndicatorAdd(count + 1, InpInd_Handle):
        Print(' Failed to add the CrossIndex indicator by ', Symbol5)
    if ShowIndicator6:
        digit = _int(SymbolInfoInteger(Symbol6, SYMBOL_DIGITS))
        InpInd_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'CrossIndex', Symbol6, clrRed, STYLE_SOLID, PRICE_CLOSE, digit, Direct6)
        if InpInd_Handle == INVALID_HANDLE:
            Print(' Failed to get the CrossIndex indicator handle by ', Symbol6)
    count += 1
    cchart[count].Attach_1(0)
    ResetLastError()
    if not cchart[count].IndicatorAdd(count + 1, InpInd_Handle):
        Print(' Failed to add the CrossIndex indicator by ', Symbol6)
    if ShowIndicator7:
        digit = _int(SymbolInfoInteger(Symbol7, SYMBOL_DIGITS))
        InpInd_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'CrossIndex', Symbol7, clrRed, STYLE_SOLID, PRICE_CLOSE, digit, Direct7)
        if InpInd_Handle == INVALID_HANDLE:
            Print(' Failed to get the CrossIndex indicator handle by ', Symbol7)
    count += 1
    cchart[count].Attach_1(0)
    ResetLastError()
    if not cchart[count].IndicatorAdd(count + 1, InpInd_Handle):
        Print(' Failed to add the CrossIndex indicator by ', Symbol7)
    if ShowIndicator8:
        digit = _int(SymbolInfoInteger(Symbol8, SYMBOL_DIGITS))
        InpInd_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'CrossIndex', Symbol8, clrRed, STYLE_SOLID, PRICE_CLOSE, digit, Direct8)
        if InpInd_Handle == INVALID_HANDLE:
            Print(' Failed to get the CrossIndex indicator handle by ', Symbol8)
    count += 1
    cchart[count].Attach_1(0)
    ResetLastError()
    if not cchart[count].IndicatorAdd(count + 1, InpInd_Handle):
        Print(' Failed to add the CrossIndex indicator by ', Symbol8)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

# ---- global variables initialised from expressions
cchart = Arr(8, 0, dyn=False, factory=CChart)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Multicurrency(_MQL5Indicator):
    name = 'multicurrency'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ShowIndicator1': True,  # permission to display the indicator
        'Direct1': True,  # no chart inversion
        'ShowIndicator2': True,  # permission to display the indicator
        'Direct2': True,  # no chart inversion
        'ShowIndicator3': True,  # permission to display the indicator
        'Direct3': True,  # no chart inversion
        'ShowIndicator4': True,  # permission to display the indicator
        'Direct4': True,  # no chart inversion
        'ShowIndicator5': True,  # permission to display the indicator
        'Direct5': False,  # no chart inversion
        'ShowIndicator6': True,  # permission to display the indicator
        'Direct6': False,  # no chart inversion
        'ShowIndicator7': True,  # permission to display the indicator
        'Direct7': False,  # no chart inversion
        'ShowIndicator8': True,  # permission to display the indicator
        'Direct8': True,  # no chart inversion
    }

