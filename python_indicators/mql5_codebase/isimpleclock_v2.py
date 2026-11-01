"""isimpleclock_v2 — converted from MQL5: MQL5 Indicators/iSimpleClock_v2/isimpleclock_v2.mq5

Copyright: Integer; Link: https://login.mql5.com/ru/users/Integer; Version: 4.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'https://login.mql5.com/ru/users/Integer', 'version': '4.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'isimpleclock_v2', 'source': 'MQL5 Indicators/iSimpleClock_v2/isimpleclock_v2.mq5', 'folder': 'iSimpleClock_v2', 'inputs': [{'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'FontColor', 'py': 'FontColor', 'param': None, 'type': 'color', 'default': 9234160, 'label': '', 'sinput': False}, {'mql': 'Corner', 'py': 'Corner', 'param': 'Corner', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'PosX', 'py': 'PosX', 'param': 'PosX', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'PosY', 'py': 'PosY', 'param': 'PosY', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
FontSize = _input('FontSize', 8)
FontColor = _input('FontColor', clrKhaki)
Corner = _input('Corner', CORNER_RIGHT_LOWER)
PosX = _input('PosX', 0)
PosY = _input('PosY', 0)
BarTime = 0
ObjName = 'Clock'

class CGraphicObjectShell(MqlObject):
    _q_fields = ('m_name', 'm_id')
    def __init__(self, *args):
        self.m_name = ""
        self.m_id = 0
    def Attach(self, aName, aChartID=0):
        self.m_name = aName
        self.m_id = aChartID
    def Name(self):
        return self.m_name
    def ChartID(self):
        return self.m_id
    def CreateVLine(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_VLINE, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateHLine(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_HLINE, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateTrend(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_TREND, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateTrendByAngle(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_TRENDBYANGLE, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateChannel(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_CHANNEL, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateStdDevChannel(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_STDDEVCHANNEL, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateRegresion(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_REGRESSION, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreatePitchFork(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_PITCHFORK, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateGannLine(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_GANNLINE, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateGannFan(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_GANNFAN, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateGannGrid(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_GANNGRID, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateFibo(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_FIBO, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateFiboTimes(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_FIBOTIMES, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateFiboFan(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_FIBOFAN, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateFiboArc(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_FIBOARC, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateFiboChannel(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_FIBOCHANNEL, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateExpansion(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_EXPANSION, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateElliotWave5(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ELLIOTWAVE5, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateElliotWave3(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ELLIOTWAVE3, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateRectangle(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_RECTANGLE, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateTriangle(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_TRIANGLE, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateEllipse(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ELLIPSE, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateCycles(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_CYCLES, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateThumbUp(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW_THUMB_UP, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateTumbDn(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW_THUMB_DOWN, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateArrowUp(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW_UP, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateArrowDn(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW_DOWN, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateArrowStop(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW_STOP, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateArrowCheck(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW_CHECK, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateArrowLeftPrice(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW_LEFT_PRICE, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateArrowRightPrice(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW_RIGHT_PRICE, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateArrowBuy(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW_BUY, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateArrowSell(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW_SELL, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateArrow(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROW, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateText(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_TEXT, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateLabel(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_LABEL, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateButton(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_BUTTON, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateChart(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_CHART, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateBitmap(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_BITMAP, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreatePitmapLabel(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_BITMAP_LABEL, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateEdit(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_EDIT, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateArrowedLine(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_ARROWED_LINE, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateEvent(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_EVENT, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def CreateRectangleLabel(self, aName, aSubWindow=0, aChartID=0):
        ObjectCreate(aChartID, aName, OBJ_RECTANGLE_LABEL, aSubWindow, 0, 0)
        self.Attach(aName, aChartID)
    def Color_0(self):
        return _uint(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_COLOR))
    def Color_1(self, aName):
        return _uint(ObjectGetInteger(0, aName, OBJPROP_COLOR))
    def Color_2(self, aChartID, aName):
        return _uint(ObjectGetInteger(aChartID, aName, OBJPROP_COLOR))
    def Style_0(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_STYLE)
    def Style_1(self, aName):
        return ObjectGetInteger(0, aName, OBJPROP_STYLE)
    def Style_2(self, aChartID, aName):
        return ObjectGetInteger(aChartID, aName, OBJPROP_STYLE)
    def Width_0(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_WIDTH))
    def Width_1(self, aName):
        return _int(ObjectGetInteger(0, aName, OBJPROP_WIDTH))
    def Width_2(self, aChartID, aName):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_WIDTH))
    def Back_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_BACK))
    def Back_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_BACK))
    def Back_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_BACK))
    def Fill_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_FILL))
    def Fill_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_FILL))
    def Fill_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_FILL))
    def Selected_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_SELECTED))
    def Selected_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_SELECTED))
    def Selected_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_SELECTED))
    def ReadOnly_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_READONLY))
    def ReadOnly_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_READONLY))
    def ReadOnly_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_READONLY))
    def Type_0(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_TYPE)
    def Type_1(self, aName):
        return ObjectGetInteger(0, aName, OBJPROP_TYPE)
    def Type_2(self, aChartID, aName):
        return ObjectGetInteger(aChartID, aName, OBJPROP_TYPE)
    def Time_1(self, aIndex):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_TIME, aIndex)
    def Time_2(self, aName, aIndex):
        return ObjectGetInteger(0, aName, OBJPROP_TIME, aIndex)
    def Time_3(self, aChartID, aName, aIndex):
        return ObjectGetInteger(aChartID, aName, OBJPROP_TIME, aIndex)
    def Selectable_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_SELECTABLE))
    def Selectable_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_SELECTABLE))
    def Selectable_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_SELECTABLE))
    def CreateTime_0(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_CREATETIME)
    def CreateTime_1(self, aName):
        return ObjectGetInteger(0, aName, OBJPROP_CREATETIME)
    def CreateTime_2(self, aChartID, aName):
        return ObjectGetInteger(aChartID, aName, OBJPROP_CREATETIME)
    def Levels_0(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_LEVELS))
    def Levels_1(self, aName):
        return _int(ObjectGetInteger(0, aName, OBJPROP_LEVELS))
    def Levels_2(self, aChartID, aName):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_LEVELS))
    def LevelColor_1(self, aIndex):
        return _uint(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_LEVELCOLOR, aIndex))
    def LevelColor_2(self, aName, aIndex):
        return _uint(ObjectGetInteger(0, aName, OBJPROP_LEVELCOLOR, aIndex))
    def LevelColor_3(self, aChartID, aName, aIndex):
        return _uint(ObjectGetInteger(aChartID, aName, OBJPROP_LEVELCOLOR, aIndex))
    def LevelStyle_1(self, aIndex):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_LEVELSTYLE, aIndex)
    def LevelStyle_2(self, aName, aIndex):
        return ObjectGetInteger(0, aName, OBJPROP_LEVELSTYLE, aIndex)
    def LevelStyle_3(self, aChartID, aName, aIndex):
        return ObjectGetInteger(aChartID, aName, OBJPROP_LEVELSTYLE, aIndex)
    def LevelWidth_1(self, aIndex):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_LEVELWIDTH, aIndex))
    def LevelWidth_2(self, aName, aIndex):
        return _int(ObjectGetInteger(0, aName, OBJPROP_LEVELWIDTH, aIndex))
    def LevelWidth_3(self, aChartID, aName, aIndex):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_LEVELWIDTH, aIndex))
    def FontSize_0(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_FONTSIZE))
    def FontSize_1(self, aName):
        return _int(ObjectGetInteger(0, aName, OBJPROP_FONTSIZE))
    def FontSize_2(self, aChartID, aName):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_FONTSIZE))
    def RayLeft_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_RAY_LEFT))
    def RayLeft_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_RAY_LEFT))
    def RayLeft_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_RAY_LEFT))
    def RayRight_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_RAY_RIGHT))
    def RayRight_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_RAY_RIGHT))
    def RayRight_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_RAY_RIGHT))
    def Ray_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_RAY))
    def Ray_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_RAY))
    def Ray_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_RAY))
    def Ellipse_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_ELLIPSE))
    def Ellipse_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_ELLIPSE))
    def Ellipse_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_ELLIPSE))
    def ArrowCode_0(self):
        return _char(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_ARROWCODE))
    def ArrowCode_1(self, aName):
        return _char(ObjectGetInteger(0, aName, OBJPROP_ARROWCODE))
    def ArrowCode_2(self, aChartID, aName):
        return _char(ObjectGetInteger(aChartID, aName, OBJPROP_ARROWCODE))
    def TimeFrames_0(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_TIMEFRAMES)
    def TimeFrames_1(self, aName):
        return ObjectGetInteger(0, aName, OBJPROP_TIMEFRAMES)
    def TimeFrames_2(self, aChartID, aName):
        return ObjectGetInteger(aChartID, aName, OBJPROP_TIMEFRAMES)
    def Anchor_0(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_ANCHOR)
    def Anchor_1(self, aName):
        return ObjectGetInteger(0, aName, OBJPROP_ANCHOR)
    def Anchor_2(self, aChartID, aName):
        return ObjectGetInteger(aChartID, aName, OBJPROP_ANCHOR)
    def XDistance_0(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_XDISTANCE))
    def XDistance_1(self, aName):
        return _int(ObjectGetInteger(0, aName, OBJPROP_XDISTANCE))
    def XDistance_2(self, aChartID, aName):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_XDISTANCE))
    def YDistance_0(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_YDISTANCE))
    def YDistance_1(self, aName):
        return _int(ObjectGetInteger(0, aName, OBJPROP_YDISTANCE))
    def YDistance_2(self, aChartID, aName):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_YDISTANCE))
    def Direction_0(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_DIRECTION)
    def Direction_1(self, aName):
        return ObjectGetInteger(0, aName, OBJPROP_DIRECTION)
    def Direction_2(self, aChartID, aName):
        return ObjectGetInteger(aChartID, aName, OBJPROP_DIRECTION)
    def Degree_0(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_DEGREE)
    def Degree_1(self, aName):
        return ObjectGetInteger(0, aName, OBJPROP_DEGREE)
    def Degree_2(self, aChartID, aName):
        return ObjectGetInteger(aChartID, aName, OBJPROP_DEGREE)
    def DrawLines_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_DRAWLINES))
    def DrawLines_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_DRAWLINES))
    def DrawLines_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_DRAWLINES))
    def State_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_STATE))
    def State_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_STATE))
    def State_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_STATE))
    def ChartChartID_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_CHART_ID))
    def ChartChartID_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_CHART_ID))
    def ChartChartID_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_CHART_ID))
    def XSize_0(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_XSIZE))
    def XSize_1(self, aName):
        return _int(ObjectGetInteger(0, aName, OBJPROP_XSIZE))
    def XSize_2(self, aChartID, aName):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_XSIZE))
    def YSize_0(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_YSIZE))
    def YSize_1(self, aName):
        return _int(ObjectGetInteger(0, aName, OBJPROP_YSIZE))
    def YSize_2(self, aChartID, aName):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_YSIZE))
    def XOffset_0(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_XOFFSET))
    def XOffset_1(self, aName):
        return _int(ObjectGetInteger(0, aName, OBJPROP_XOFFSET))
    def XOffset_2(self, aChartID, aName):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_XOFFSET))
    def YOffset_0(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_YOFFSET))
    def YOffset_1(self, aName):
        return _int(ObjectGetInteger(0, aName, OBJPROP_YOFFSET))
    def YOffset_2(self, aChartID, aName):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_YOFFSET))
    def Period_0(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_PERIOD)
    def Period_1(self, aName):
        return ObjectGetInteger(0, aName, OBJPROP_PERIOD)
    def Period_2(self, aChartID, aName):
        return ObjectGetInteger(aChartID, aName, OBJPROP_PERIOD)
    def DateScale_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_DATE_SCALE))
    def DateScale_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_DATE_SCALE))
    def DateScale_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_DATE_SCALE))
    def PriceScale_0(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_PRICE_SCALE))
    def PriceScale_1(self, aName):
        return _bool(ObjectGetInteger(0, aName, OBJPROP_PRICE_SCALE))
    def PriceScale_2(self, aChartID, aName):
        return _bool(ObjectGetInteger(aChartID, aName, OBJPROP_PRICE_SCALE))
    def ChartScale_0(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_CHART_SCALE))
    def ChartScale_1(self, aName):
        return _int(ObjectGetInteger(0, aName, OBJPROP_CHART_SCALE))
    def ChartScale_2(self, aChartID, aName):
        return _int(ObjectGetInteger(aChartID, aName, OBJPROP_CHART_SCALE))
    def BgColor_0(self):
        return _uint(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_BGCOLOR))
    def BgColor_1(self, aName):
        return _uint(ObjectGetInteger(0, aName, OBJPROP_BGCOLOR))
    def BgColor_2(self, aChartID, aName):
        return _uint(ObjectGetInteger(aChartID, aName, OBJPROP_BGCOLOR))
    def Corner_0(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_CORNER)
    def Corner_1(self, aName):
        return ObjectGetInteger(0, aName, OBJPROP_CORNER)
    def Corner_2(self, aChartID, aName):
        return ObjectGetInteger(aChartID, aName, OBJPROP_CORNER)
    def BorderType_0(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_BORDER_TYPE)
    def BorderType_1(self, aName):
        return ObjectGetInteger(0, aName, OBJPROP_BORDER_TYPE)
    def BorderType_2(self, aChartID, aName):
        return ObjectGetInteger(aChartID, aName, OBJPROP_BORDER_TYPE)
    def Price_1(self, aIndex):
        return ObjectGetDouble(self.m_id, self.m_name, OBJPROP_PRICE, aIndex)
    def Price_2(self, aName, aIndex):
        return ObjectGetDouble(0, aName, OBJPROP_PRICE, aIndex)
    def Price_3(self, aChartID, aName, aIndex):
        return ObjectGetDouble(aChartID, aName, OBJPROP_PRICE, aIndex)
    def LevelValue_1(self, aIndex):
        return ObjectGetDouble(self.m_id, self.m_name, OBJPROP_LEVELVALUE, aIndex)
    def LevelValue_2(self, aName, aIndex):
        return ObjectGetDouble(0, aName, OBJPROP_LEVELVALUE, aIndex)
    def LevelValue_3(self, aChartID, aName, aIndex):
        return ObjectGetDouble(aChartID, aName, OBJPROP_LEVELVALUE, aIndex)
    def Scale_0(self):
        return ObjectGetDouble(self.m_id, self.m_name, OBJPROP_SCALE)
    def Scale_1(self, aName):
        return ObjectGetDouble(0, aName, OBJPROP_SCALE)
    def Scale_2(self, aChartID, aName):
        return ObjectGetDouble(aChartID, aName, OBJPROP_SCALE)
    def Angle_0(self):
        return ObjectGetDouble(self.m_id, self.m_name, OBJPROP_ANGLE)
    def Angle_1(self, aName):
        return ObjectGetDouble(0, aName, OBJPROP_ANGLE)
    def Angle_2(self, aChartID, aName):
        return ObjectGetDouble(aChartID, aName, OBJPROP_ANGLE)
    def Deviation_0(self):
        return ObjectGetDouble(self.m_id, self.m_name, OBJPROP_DEVIATION)
    def Deviation_1(self, aName):
        return ObjectGetDouble(0, aName, OBJPROP_DEVIATION)
    def Deviation_2(self, aChartID, aName):
        return ObjectGetDouble(aChartID, aName, OBJPROP_DEVIATION)
    def Text_0(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_TEXT)
    def Text_1(self, aName):
        return ObjectGetString(0, aName, OBJPROP_TEXT)
    def Text_2(self, aChartID, aName):
        return ObjectGetString(aChartID, aName, OBJPROP_TEXT)
    def ToolTip_0(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_TOOLTIP)
    def ToolTip_1(self, aName):
        return ObjectGetString(0, aName, OBJPROP_TOOLTIP)
    def ToolTip_2(self, aChartID, aName):
        return ObjectGetString(aChartID, aName, OBJPROP_TOOLTIP)
    def LevelText_1(self, aIndex):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_LEVELTEXT, aIndex)
    def LevelText_2(self, aName, aIndex):
        return ObjectGetString(0, aName, OBJPROP_LEVELTEXT, aIndex)
    def LevelText_3(self, aChartID, aName, aIndex):
        return ObjectGetString(aChartID, aName, OBJPROP_LEVELTEXT, aIndex)
    def Font_0(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_FONT)
    def Font_1(self, aName):
        return ObjectGetString(0, aName, OBJPROP_FONT)
    def Font_2(self, aChartID, aName):
        return ObjectGetString(aChartID, aName, OBJPROP_FONT)
    def BmpFileOn_0(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_BMPFILE, 0)
    def BmpFileOn_1(self, aName):
        return ObjectGetString(0, aName, OBJPROP_BMPFILE, 0)
    def BmpFileOn_2(self, aChartID, aName):
        return ObjectGetString(aChartID, aName, OBJPROP_BMPFILE, 0)
    def BmpFileOff_0(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_BMPFILE, 1)
    def BmpFileOff_1(self, aName):
        return ObjectGetString(0, aName, OBJPROP_BMPFILE, 1)
    def BmpFileOff_2(self, aChartID, aName):
        return ObjectGetString(aChartID, aName, OBJPROP_BMPFILE, 1)
    def Symbol_0(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_SYMBOL)
    def Symbol_1(self, aName):
        return ObjectGetString(0, aName, OBJPROP_SYMBOL)
    def Symbol_2(self, aChartID, aName):
        return ObjectGetString(aChartID, aName, OBJPROP_SYMBOL)
    def SetColor_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_COLOR, aValue)
    def SetColor_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_COLOR, aValue)
    def SetColor_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_COLOR, aValue)
    def SetStyle_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_STYLE, aValue)
    def SetStyle_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_STYLE, aValue)
    def SetStyle_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_STYLE, aValue)
    def SetWidth_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_WIDTH, aValue)
    def SetWidth_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_WIDTH, aValue)
    def SetWidth_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_WIDTH, aValue)
    def SetBack_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_BACK, aValue)
    def SetBack_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_BACK, aValue)
    def SetBack_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_BACK, aValue)
    def SetFill_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_FILL, aValue)
    def SetFill_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_FILL, aValue)
    def SetFill_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_FILL, aValue)
    def SetSelected_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_SELECTED, aValue)
    def SetSelected_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_SELECTED, aValue)
    def SetSelected_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_SELECTED, aValue)
    def SetReadOnly_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_READONLY, aValue)
    def SetReadOnly_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_READONLY, aValue)
    def SetReadOnly_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_READONLY, aValue)
    def SetTime_2(self, aIndex, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_TIME, aIndex, aValue)
    def SetTime_3(self, aName, aIndex, aValue):
        ObjectSetInteger(0, aName, OBJPROP_TIME, aIndex, aValue)
    def SetTime_4(self, aChartID, aName, aIndex, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_TIME, aIndex, aValue)
    def SetSelectable_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_SELECTABLE, aValue)
    def SetSelectable_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_SELECTABLE, aValue)
    def SetSelectable_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_SELECTABLE, aValue)
    def SetLevels_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_LEVELS, aValue)
    def SetLevels_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_LEVELS, aValue)
    def SetLevels_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_LEVELS, aValue)
    def SetLevelColor_2(self, aIndex, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_LEVELCOLOR, aIndex, aValue)
    def SetLevelColor_3(self, aName, aIndex, aValue):
        ObjectSetInteger(0, aName, OBJPROP_LEVELCOLOR, aIndex, aValue)
    def SetLevelColor_4(self, aChartID, aName, aIndex, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_LEVELCOLOR, aIndex, aValue)
    def SetLevelStyle_2(self, aIndex, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_LEVELSTYLE, aIndex, aValue)
    def SetLevelStyle_3(self, aName, aIndex, aValue):
        ObjectSetInteger(0, aName, OBJPROP_LEVELSTYLE, aIndex, aValue)
    def SetLevelStyle_4(self, aChartID, aName, aIndex, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_LEVELSTYLE, aIndex, aValue)
    def SetLevelWidth_2(self, aIndex, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_LEVELWIDTH, aIndex, aValue)
    def SetLevelWidth_3(self, aName, aIndex, aValue):
        ObjectSetInteger(0, aName, OBJPROP_LEVELWIDTH, aIndex, aValue)
    def SetLevelWidth_4(self, aChartID, aName, aIndex, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_LEVELWIDTH, aIndex, aValue)
    def SetFontSize_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_FONTSIZE, aValue)
    def SetFontSize_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_FONTSIZE, aValue)
    def SetFontSize_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_FONTSIZE, aValue)
    def SetRayLeft_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_RAY_LEFT, aValue)
    def SetRayLeft_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_RAY_LEFT, aValue)
    def SetRayLeft_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_RAY_LEFT, aValue)
    def SetRayRight_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_RAY_RIGHT, aValue)
    def SetRayRight_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_RAY_RIGHT, aValue)
    def SetRayRight_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_RAY_RIGHT, aValue)
    def SetRay_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_RAY, aValue)
    def SetRay_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_RAY, aValue)
    def SetRay_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_RAY, aValue)
    def SetEllipse_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_ELLIPSE, aValue)
    def SetEllipse_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_ELLIPSE, aValue)
    def SetEllipse_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_ELLIPSE, aValue)
    def SetArrowCode_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_ARROWCODE, aValue)
    def SetArrowCode_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_ARROWCODE, aValue)
    def SetArrowCode_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_ARROWCODE, aValue)
    def SetTimeFrames_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_TIMEFRAMES, aValue)
    def SetTimeFrames_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_TIMEFRAMES, aValue)
    def SetTimeFrames_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_TIMEFRAMES, aValue)
    def SetAnchor_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_ANCHOR, aValue)
    def SetAnchor_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_ANCHOR, aValue)
    def SetAnchor_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_ANCHOR, aValue)
    def SetXDistance_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_XDISTANCE, aValue)
    def SetXDistance_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_XDISTANCE, aValue)
    def SetXDistance_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_XDISTANCE, aValue)
    def SetYDistance_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_YDISTANCE, aValue)
    def SetYDistance_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_YDISTANCE, aValue)
    def SetYDistance_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_YDISTANCE, aValue)
    def SetDirection_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_DIRECTION, aValue)
    def SetDirection_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_DIRECTION, aValue)
    def SetDirection_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_DIRECTION, aValue)
    def SetDegree_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_DEGREE, aValue)
    def SetDegree_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_DEGREE, aValue)
    def SetDegree_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_DEGREE, aValue)
    def SetDrawLines_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_DRAWLINES, aValue)
    def SetDrawLines_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_DRAWLINES, aValue)
    def SetDrawLines_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_DRAWLINES, aValue)
    def SetState_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_STATE, aValue)
    def SetState_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_STATE, aValue)
    def SetState_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_STATE, aValue)
    def SetXSize_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_XSIZE, aValue)
    def SetXSize_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_XSIZE, aValue)
    def SetXSize_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_XSIZE, aValue)
    def SetYSize_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_YSIZE, aValue)
    def SetYSize_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_YSIZE, aValue)
    def SetYSize_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_YSIZE, aValue)
    def SetXOffset_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_XOFFSET, aValue)
    def SetXOffset_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_XOFFSET, aValue)
    def SetXOffset_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_XOFFSET, aValue)
    def SetYOffset_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_YOFFSET, aValue)
    def SetYOffset_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_YOFFSET, aValue)
    def SetYOffset_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_YOFFSET, aValue)
    def SetPeriod_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_PERIOD, aValue)
    def SetPeriod_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_PERIOD, aValue)
    def SetPeriod_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_PERIOD, aValue)
    def SetDateScale_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_DATE_SCALE, aValue)
    def SetDateScale_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_DATE_SCALE, aValue)
    def SetDateScale_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_DATE_SCALE, aValue)
    def SetPriceScale_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_PRICE_SCALE, aValue)
    def SetPriceScale_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_PRICE_SCALE, aValue)
    def SetPriceScale_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_PRICE_SCALE, aValue)
    def SetChartScale_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_CHART_SCALE, aValue)
    def SetChartScale_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_CHART_SCALE, aValue)
    def SetChartScale_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_CHART_SCALE, aValue)
    def SetBgColor_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_BGCOLOR, aValue)
    def SetBgColor_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_BGCOLOR, aValue)
    def SetBgColor_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_BGCOLOR, aValue)
    def SetCorner_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_CORNER, aValue)
    def SetCorner_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_CORNER, aValue)
    def SetCorner_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_CORNER, aValue)
    def SetBorderType_1(self, aValue):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_BORDER_TYPE, aValue)
    def SetBorderType_2(self, aName, aValue):
        ObjectSetInteger(0, aName, OBJPROP_BORDER_TYPE, aValue)
    def SetBorderType_3(self, aChartID, aName, aValue):
        ObjectSetInteger(aChartID, aName, OBJPROP_BORDER_TYPE, aValue)
    def SetPrice_2(self, aIndex, aValue):
        ObjectSetDouble(self.m_id, self.m_name, OBJPROP_PRICE, aIndex, aValue)
    def SetPrice_3(self, aName, aIndex, aValue):
        ObjectSetDouble(0, aName, OBJPROP_PRICE, aIndex, aValue)
    def SetPrice_4(self, aChartID, aName, aIndex, aValue):
        ObjectSetDouble(aChartID, aName, OBJPROP_PRICE, aIndex, aValue)
    def SetLevelValue_2(self, aIndex, aValue):
        ObjectSetDouble(self.m_id, self.m_name, OBJPROP_LEVELVALUE, aIndex, aValue)
    def SetLevelValue_3(self, aName, aIndex, aValue):
        ObjectSetDouble(0, aName, OBJPROP_LEVELVALUE, aIndex, aValue)
    def SetLevelValue_4(self, aChartID, aName, aIndex, aValue):
        ObjectSetDouble(aChartID, aName, OBJPROP_LEVELVALUE, aIndex, aValue)
    def SetScale_1(self, aValue):
        ObjectSetDouble(self.m_id, self.m_name, OBJPROP_SCALE, aValue)
    def SetScale_2(self, aName, aValue):
        ObjectSetDouble(0, aName, OBJPROP_SCALE, aValue)
    def SetScale_3(self, aChartID, aName, aValue):
        ObjectSetDouble(aChartID, aName, OBJPROP_SCALE, aValue)
    def SetAngle_1(self, aValue):
        ObjectSetDouble(self.m_id, self.m_name, OBJPROP_ANGLE, aValue)
    def SetAngle_2(self, aName, aValue):
        ObjectSetDouble(0, aName, OBJPROP_ANGLE, aValue)
    def SetAngle_3(self, aChartID, aName, aValue):
        ObjectSetDouble(aChartID, aName, OBJPROP_ANGLE, aValue)
    def SetDeviation_1(self, aValue):
        ObjectSetDouble(self.m_id, self.m_name, OBJPROP_DEVIATION, aValue)
    def SetDeviation_2(self, aName, aValue):
        ObjectSetDouble(0, aName, OBJPROP_DEVIATION, aValue)
    def SetDeviation_3(self, aChartID, aName, aValue):
        ObjectSetDouble(aChartID, aName, OBJPROP_DEVIATION, aValue)
    def SetText_1(self, aValue):
        ObjectSetString(self.m_id, self.m_name, OBJPROP_TEXT, aValue)
    def SetText_2(self, aName, aValue):
        ObjectSetString(0, aName, OBJPROP_TEXT, aValue)
    def SetText_3(self, aChartID, aName, aValue):
        ObjectSetString(aChartID, aName, OBJPROP_TEXT, aValue)
    def SetToolTip_1(self, aValue):
        ObjectSetString(self.m_id, self.m_name, OBJPROP_TOOLTIP, aValue)
    def SetToolTip_2(self, aName, aValue):
        ObjectSetString(0, aName, OBJPROP_TOOLTIP, aValue)
    def SetToolTip_3(self, aChartID, aName, aValue):
        ObjectSetString(aChartID, aName, OBJPROP_TOOLTIP, aValue)
    def SetLevelText_2(self, aIndex, aValue):
        ObjectSetString(self.m_id, self.m_name, OBJPROP_LEVELTEXT, aIndex, aValue)
    def SetLevelText_3(self, aName, aIndex, aValue):
        ObjectSetString(0, aName, OBJPROP_LEVELTEXT, aIndex, aValue)
    def SetLevelText_4(self, aChartID, aName, aIndex, aValue):
        ObjectSetString(aChartID, aName, OBJPROP_LEVELTEXT, aIndex, aValue)
    def SetFont_1(self, aValue):
        ObjectSetString(self.m_id, self.m_name, OBJPROP_FONT, aValue)
    def SetFont_2(self, aName, aValue):
        ObjectSetString(0, aName, OBJPROP_FONT, aValue)
    def SetFont_3(self, aChartID, aName, aValue):
        ObjectSetString(aChartID, aName, OBJPROP_FONT, aValue)
    def SetBmpFileOn_1(self, aValue):
        ObjectSetString(self.m_id, self.m_name, OBJPROP_BMPFILE, 0, aValue)
    def SetBmpFileOn_2(self, aName, aValue):
        ObjectSetString(0, aName, OBJPROP_BMPFILE, 0, aValue)
    def SetBmpFileOn_3(self, aChartID, aName, aValue):
        ObjectSetString(aChartID, aName, OBJPROP_BMPFILE, 0, aValue)
    def SetBmpFileOff_1(self, aValue):
        ObjectSetString(self.m_id, self.m_name, OBJPROP_BMPFILE, 1, aValue)
    def SetBmpFileOff_2(self, aName, aValue):
        ObjectSetString(0, aName, OBJPROP_BMPFILE, 1, aValue)
    def SetBmpFileOff_3(self, aChartID, aName, aValue):
        ObjectSetString(aChartID, aName, OBJPROP_BMPFILE, 1, aValue)
    def SetSymbol_1(self, aValue):
        ObjectSetString(self.m_id, self.m_name, OBJPROP_SYMBOL, aValue)
    def SetSymbol_2(self, aName, aValue):
        ObjectSetString(0, aName, OBJPROP_SYMBOL, aValue)
    def SetSymbol_3(self, aChartID, aName, aValue):
        ObjectSetString(aChartID, aName, OBJPROP_SYMBOL, aValue)
    def Delete_0(self):
        ObjectDelete(self.m_id, self.m_name)
    def Delete_1(self, aName):
        ObjectDelete(0, aName)
    def Delete_2(self, aChartID, aName):
        ObjectDelete(aChartID, aName)
    def Move_3(self, aIndex, aTime, aPrice):
        ObjectMove(self.m_id, self.m_name, aIndex, aTime, aPrice)
    def Move_4(self, aName, aIndex, aTime, aPrice):
        ObjectMove(0, aName, aIndex, aTime, aPrice)
    def Move_5(self, aChartID, aName, aIndex, aTime, aPrice):
        ObjectMove(aChartID, aName, aIndex, aTime, aPrice)
    def Find_0(self):
        return ObjectFind(self.m_id, self.m_name)
    def Find_1(self, aName):
        return ObjectFind(0, aName)
    def Find_2(self, aChartID, aName):
        return ObjectFind(aChartID, aName)
    def GetTimeByValue_2(self, aValue, aLineID=0):
        return _long(ObjectGetTimeByValue(self.m_id, self.m_name, aValue, aLineID))
    def GetTimeByValue_3(self, aName, aValue, aLineID=0):
        return _long(ObjectGetTimeByValue(0, aName, aValue, aLineID))
    def GetTimeByValue_4(self, aChartID, aName, aValue, aLineID=0):
        return _long(ObjectGetTimeByValue(aChartID, aName, aValue, aLineID))
    def GetValueByTime_2(self, aTime, aLineID=0):
        return ObjectGetValueByTime(self.m_id, self.m_name, aTime, aLineID)
    def GetValueByTime_3(self, aName, aTime, aLineID=0):
        return ObjectGetValueByTime(0, aName, aTime, aLineID)
    def GetValueByTime_4(self, aChartID, aName, aTime, aLineID=0):
        return ObjectGetValueByTime(aChartID, aName, aTime, aLineID)
    def Total(self, aChartID=0, aSubWindow=-1, aType=-1):
        return ObjectsTotal(aChartID, aSubWindow, aType)
    def Redraw_0(self):
        ChartRedraw(self.m_id)
    def Redraw_1(self, aChartID):
        ChartRedraw(aChartID)
    def SetXYDistance_2(self, aValueX, aValueY):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_XDISTANCE, aValueX)
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_YDISTANCE, aValueY)
    def SetXYDistance_3(self, aName, aValueX, aValueY):
        ObjectSetInteger(0, aName, OBJPROP_XDISTANCE, aValueX)
        ObjectSetInteger(0, aName, OBJPROP_YDISTANCE, aValueY)
    def SetXYDistance_4(self, aChartID, aName, aValueX, aValueY):
        ObjectSetInteger(aChartID, aName, OBJPROP_XDISTANCE, aValueX)
        ObjectSetInteger(aChartID, aName, OBJPROP_YDISTANCE, aValueY)
    def SetXYSize_2(self, aValueX, aValueY):
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_XSIZE, aValueX)
        ObjectSetInteger(self.m_id, self.m_name, OBJPROP_YSIZE, aValueY)
    def SetXYSize_3(self, aName, aValueX, aValueY):
        ObjectSetInteger(0, aName, OBJPROP_XSIZE, aValueX)
        ObjectSetInteger(0, aName, OBJPROP_YSIZE, aValueY)
    def SetXYSize_4(self, aChartID, aName, aValueX, aValueY):
        ObjectSetInteger(aChartID, aName, OBJPROP_XSIZE, aValueX)
        ObjectSetInteger(aChartID, aName, OBJPROP_YSIZE, aValueY)

class CWorkPiece(MqlObject):
    _q_fields = ()
    def __init__(self, *args):
        pass
    def Canvas(self, aName='Canvas', aSubWindow=0, aLeft=100, aTop=100, aWidth=300, aHeight=150, aColorBg=clrIvory, aColorBorder=clrDimGray):
        g.CreateRectangleLabel(aName, aSubWindow)
        g.SetXDistance_1(aLeft)
        g.SetYDistance_1(aTop)
        g.SetXSize_1(aWidth)
        g.SetYSize_1(aHeight)
        g.SetBgColor_1(aColorBg)
        g.SetColor_1(aColorBorder)
        g.SetCorner_1(CORNER_LEFT_UPPER)
        g.SetBorderType_1(BORDER_FLAT)
        g.SetTimeFrames_1(_long(OBJ_ALL_PERIODS))
        g.SetSelected_1(False)
        g.SetSelectable_1(False)
        g.SetWidth_1(1)
        g.SetStyle_1(STYLE_SOLID)
    def Label(self, aName='Label', aSubWindow=0, aLeft=100, aTop=100, aText='Label', aColor=clrDimGray, aFontSize=8, aFont='Arial'):
        g.CreateLabel(aName, aSubWindow)
        g.SetXDistance_1(aLeft)
        g.SetYDistance_1(aTop)
        g.SetText_1(aText)
        g.SetColor_1(aColor)
        g.SetFontSize_1(aFontSize)
        g.SetFont_1(aFont)
        g.SetCorner_1(CORNER_LEFT_UPPER)
        g.SetAnchor_1(ANCHOR_LEFT_UPPER)
        g.SetSelected_1(False)
        g.SetSelectable_1(False)
    def Button(self, aName='Button', aSubWindow=0, aLeft=100, aTop=100, aWidth=40, aHeight=15, aText='Button', aColorBg=clrSilver, aColorText=clrBlack, aFontSize=7, aFont='Arial'):
        g.CreateButton(aName, aSubWindow)
        g.SetXDistance_1(aLeft)
        g.SetYDistance_1(aTop)
        g.SetXSize_1(aWidth)
        g.SetYSize_1(aHeight)
        g.SetText_1(aText)
        g.SetColor_1(aColorText)
        g.SetBgColor_1(aColorBg)
        g.SetFontSize_1(aFontSize)
        g.SetFont_1(aFont)
        g.SetCorner_1(CORNER_LEFT_UPPER)
        g.SetSelected_1(False)
        g.SetSelectable_1(False)
    def Edit(self, aName='Edit', aSubWindow=0, aLeft=100, aTop=100, aWidth=40, aHeight=15, aText='Edit', aColorBg=clrSnow, aColorText=clrDimGray, aFontSize=7, aFont='Arial'):
        g.CreateEdit(aName, aSubWindow)
        g.SetXDistance_1(aLeft)
        g.SetYDistance_1(aTop)
        g.SetXSize_1(aWidth)
        g.SetYSize_1(aHeight)
        g.SetText_1(aText)
        g.SetColor_1(aColorText)
        g.SetBgColor_1(aColorBg)
        g.SetFontSize_1(aFontSize)
        g.SetFont_1(aFont)
        g.SetCorner_1(CORNER_LEFT_UPPER)
        g.SetSelected_1(False)
        g.SetSelectable_1(False)
        g.SetReadOnly_1(False)
    def Frame(self, aName='Frame', aSubWindow=0, aLeft=100, aTop=100, aWidth=50, aHeight=50, aCaption='Frame', aCaptionWidth=31, aColorBg=clrIvory, aColorBorder=clrDimGray, aColorCaption=clrDimGray):
        self.Canvas(aName + '_Frame', aSubWindow, aLeft, aTop, aWidth, aHeight, aColorBg, aColorBorder)
        if aCaption != '':
            self.Canvas(aName + '_FrameC', aSubWindow, aLeft + 4, aTop, aCaptionWidth, 1, aColorBg, aColorBg)
            self.Label(aName + '_FrameL', aSubWindow, aLeft + 6, aTop - 5, aCaption, aColorCaption, 7, 'Arial')
    def FrameDelete(self, aName='Frame'):
        ObjectDelete(0, aName + '_Frame')
        ObjectDelete(0, aName + '_FrameC')
        ObjectDelete(0, aName + '_FrameL')
    def Delete(self, aName):
        ObjectDelete(0, aName)
    def Redraw(self):
        ChartRedraw(0)

class CColorSchemes(MqlObject):
    _q_fields = ('m_ShemeIndex',)
    def __init__(self, *args):
        self.m_ShemeIndex = 0
    def SetScheme(self, aShemeIndex):
        self.m_ShemeIndex = aShemeIndex
    def Color(self, aColorIndex):
        m_Color = Arr(7, 0, dyn=False, dims=(55,))
        m_Color[0][0] = clrSnow
        m_Color[0][1] = clrDimGray
        m_Color[0][2] = clrDimGray
        m_Color[0][3] = clrPink
        m_Color[0][4] = clrSilver
        m_Color[0][5] = clrLightGray
        m_Color[0][6] = clrDimGray
        m_Color[0][7] = clrLightGray
        m_Color[0][8] = clrSilver
        m_Color[0][9] = clrPink
        m_Color[0][10] = clrDimGray
        m_Color[0][11] = clrSnow
        m_Color[0][12] = clrLightGray
        m_Color[0][13] = clrGainsboro
        m_Color[0][14] = clrPaleTurquoise
        m_Color[0][15] = clrWhiteSmoke
        m_Color[0][16] = clrGainsboro
        m_Color[0][17] = clrRed
        m_Color[0][18] = clrLightGray
        m_Color[0][19] = clrDimGray
        m_Color[0][20] = clrLightSkyBlue
        m_Color[0][21] = clrDimGray
        m_Color[0][22] = clrLightGray
        m_Color[0][23] = clrDimGray
        m_Color[0][24] = clrWhiteSmoke
        m_Color[0][25] = clrDimGray
        m_Color[0][26] = clrMistyRose
        m_Color[0][27] = clrPaleGreen
        m_Color[0][28] = clrPaleTurquoise
        m_Color[0][29] = clrSnow
        m_Color[0][30] = clrDimGray
        m_Color[0][31] = clrPink
        m_Color[0][32] = clrWhiteSmoke
        m_Color[0][33] = clrDimGray
        m_Color[0][34] = clrSilver
        m_Color[0][35] = clrBlack
        m_Color[0][36] = 0xA93F1B
        m_Color[0][37] = clrGray
        m_Color[0][38] = clrYellow
        m_Color[0][39] = clrWhiteSmoke
        m_Color[0][40] = clrDimGray
        m_Color[0][41] = clrDimGray
        m_Color[0][42] = clrSilver
        m_Color[0][43] = 0x464646
        m_Color[0][44] = clrDimGray
        m_Color[0][45] = clrWhiteSmoke
        m_Color[0][46] = clrDimGray
        m_Color[0][47] = clrSilver
        m_Color[0][48] = clrDimGray
        m_Color[0][49] = clrDimGray
        m_Color[0][50] = clrLightBlue
        m_Color[0][51] = clrSnow
        m_Color[0][52] = clrGainsboro
        m_Color[0][53] = clrPink
        m_Color[0][54] = clrRed
        m_Color[1][0] = clrLightYellow
        m_Color[1][1] = clrBrown
        m_Color[1][2] = clrBrown
        m_Color[1][3] = clrLightPink
        m_Color[1][4] = clrBurlyWood
        m_Color[1][5] = clrNavajoWhite
        m_Color[1][6] = clrBrown
        m_Color[1][7] = clrNavajoWhite
        m_Color[1][8] = clrBurlyWood
        m_Color[1][9] = clrPink
        m_Color[1][10] = clrBrown
        m_Color[1][11] = clrLightYellow
        m_Color[1][12] = clrLightYellow
        m_Color[1][13] = clrLightYellow
        m_Color[1][14] = clrBisque
        m_Color[1][15] = clrLightYellow
        m_Color[1][16] = clrNavajoWhite
        m_Color[1][17] = clrRed
        m_Color[1][18] = clrNavajoWhite
        m_Color[1][19] = clrBrown
        m_Color[1][20] = clrOrange
        m_Color[1][21] = clrBrown
        m_Color[1][22] = clrBurlyWood
        m_Color[1][23] = clrBrown
        m_Color[1][24] = clrBisque
        m_Color[1][25] = clrBrown
        m_Color[1][26] = clrLightPink
        m_Color[1][27] = clrLightGreen
        m_Color[1][28] = clrPaleTurquoise
        m_Color[1][29] = clrLightYellow
        m_Color[1][30] = clrBrown
        m_Color[1][31] = clrPink
        m_Color[1][32] = 0xCDF5FF
        m_Color[1][33] = clrSienna
        m_Color[1][34] = 0x97D6F0
        m_Color[1][35] = 0x213C74
        m_Color[1][36] = 0x213C74
        m_Color[1][37] = 0x213C74
        m_Color[1][38] = 0xDCF1FA
        m_Color[1][39] = 0xCDF5FF
        m_Color[1][40] = clrBrown
        m_Color[1][41] = clrBrown
        m_Color[1][42] = clrBurlyWood
        m_Color[1][43] = clrMaroon
        m_Color[1][44] = clrBrown
        m_Color[1][45] = clrLightYellow
        m_Color[1][46] = clrBrown
        m_Color[1][47] = clrBurlyWood
        m_Color[1][48] = clrBrown
        m_Color[1][49] = clrBrown
        m_Color[1][50] = clrGold
        m_Color[1][51] = 0xF0FFFF
        m_Color[1][52] = 0x96DCDC
        m_Color[1][53] = clrPink
        m_Color[1][54] = clrRed
        m_Color[2][0] = clrAliceBlue
        m_Color[2][1] = clrNavy
        m_Color[2][2] = clrNavy
        m_Color[2][3] = clrLightPink
        m_Color[2][4] = clrLightSteelBlue
        m_Color[2][5] = clrAliceBlue
        m_Color[2][6] = clrNavy
        m_Color[2][7] = clrLightBlue
        m_Color[2][8] = clrLightSteelBlue
        m_Color[2][9] = clrLightPink
        m_Color[2][10] = clrNavy
        m_Color[2][11] = clrAliceBlue
        m_Color[2][12] = clrAliceBlue
        m_Color[2][13] = clrAliceBlue
        m_Color[2][14] = clrPaleTurquoise
        m_Color[2][15] = clrAliceBlue
        m_Color[2][16] = clrLightBlue
        m_Color[2][17] = clrRed
        m_Color[2][18] = clrLightBlue
        m_Color[2][19] = clrNavy
        m_Color[2][20] = clrDodgerBlue
        m_Color[2][21] = clrNavy
        m_Color[2][22] = clrLightSteelBlue
        m_Color[2][23] = clrNavy
        m_Color[2][24] = clrLightBlue
        m_Color[2][25] = clrNavy
        m_Color[2][26] = clrLightPink
        m_Color[2][27] = clrLightGreen
        m_Color[2][28] = clrPaleTurquoise
        m_Color[2][29] = clrAliceBlue
        m_Color[2][30] = clrNavy
        m_Color[2][31] = clrPink
        m_Color[2][32] = 0xF4EFDD
        m_Color[2][33] = clrSteelBlue
        m_Color[2][34] = 0xEECA86
        m_Color[2][35] = clrNavy
        m_Color[2][36] = clrNavy
        m_Color[2][37] = clrNavy
        m_Color[2][38] = 0xF7E3BF
        m_Color[2][39] = 0xF4EFDD
        m_Color[2][40] = clrNavy
        m_Color[2][41] = clrNavy
        m_Color[2][42] = clrLightSteelBlue
        m_Color[2][43] = clrNavy
        m_Color[2][44] = clrNavy
        m_Color[2][45] = clrAliceBlue
        m_Color[2][46] = clrNavy
        m_Color[2][47] = clrLightSteelBlue
        m_Color[2][48] = clrNavy
        m_Color[2][49] = clrNavy
        m_Color[2][50] = 0xE6E664
        m_Color[2][51] = 0xFFFFF5
        m_Color[2][52] = 0xE6E6C8
        m_Color[2][53] = clrPink
        m_Color[2][54] = clrRed
        m_Color[3][0] = clrHoneydew
        m_Color[3][1] = clrDarkSlateGray
        m_Color[3][2] = clrDarkSlateGray
        m_Color[3][3] = clrLightPink
        m_Color[3][4] = clrDarkSeaGreen
        m_Color[3][5] = clrHoneydew
        m_Color[3][6] = clrDarkSlateGray
        m_Color[3][7] = 0x9EC7A2
        m_Color[3][8] = clrDarkSeaGreen
        m_Color[3][9] = clrLightPink
        m_Color[3][10] = clrDarkSlateGray
        m_Color[3][11] = 0xCCE1CE
        m_Color[3][12] = 0xBAD8BC
        m_Color[3][13] = 0xBAD8BC
        m_Color[3][14] = clrPaleTurquoise
        m_Color[3][15] = clrHoneydew
        m_Color[3][16] = 0xC7DEC9
        m_Color[3][17] = clrRed
        m_Color[3][18] = 0xC7DEC9
        m_Color[3][19] = clrDarkSlateGray
        m_Color[3][20] = clrYellowGreen
        m_Color[3][21] = clrDarkSlateGray
        m_Color[3][22] = 0xA3C9A6
        m_Color[3][23] = clrDarkSlateGray
        m_Color[3][24] = 0xC7DEC9
        m_Color[3][25] = clrDarkSlateGray
        m_Color[3][26] = clrLightPink
        m_Color[3][27] = clrLightGreen
        m_Color[3][28] = clrPaleTurquoise
        m_Color[3][29] = clrHoneydew
        m_Color[3][30] = clrDarkSlateGray
        m_Color[3][31] = clrPink
        m_Color[3][32] = 0xE1FAE1
        m_Color[3][33] = 0x757546
        m_Color[3][34] = 0x9BD78C
        m_Color[3][35] = clrDarkGreen
        m_Color[3][36] = clrDarkGreen
        m_Color[3][37] = clrDarkGreen
        m_Color[3][38] = 0xB4FFB4
        m_Color[3][39] = 0xE1FAE1
        m_Color[3][40] = clrDarkSlateGray
        m_Color[3][41] = clrDarkSlateGray
        m_Color[3][42] = 0xA8D1AC
        m_Color[3][43] = 0x3E3E24
        m_Color[3][44] = clrDarkSlateGray
        m_Color[3][45] = clrHoneydew
        m_Color[3][46] = clrDarkSlateGray
        m_Color[3][47] = clrDarkSeaGreen
        m_Color[3][48] = clrDarkSlateGray
        m_Color[3][49] = clrDimGray
        m_Color[3][50] = clrSpringGreen
        m_Color[3][51] = 0xF0FFF0
        m_Color[3][52] = 0xC8F0C8
        m_Color[3][53] = clrPink
        m_Color[3][54] = clrRed
        m_Color[4][0] = clrBlack
        m_Color[4][1] = clrYellow
        m_Color[4][2] = clrYellow
        m_Color[4][3] = clrRed
        m_Color[4][4] = clrBlack
        m_Color[4][5] = clrSilver
        m_Color[4][6] = clrYellow
        m_Color[4][7] = clrDimGray
        m_Color[4][8] = clrBlack
        m_Color[4][9] = clrRed
        m_Color[4][10] = clrYellow
        m_Color[4][11] = clrDarkKhaki
        m_Color[4][12] = clrGray
        m_Color[4][13] = clrGray
        m_Color[4][14] = clrNavy
        m_Color[4][15] = clrDimGray
        m_Color[4][16] = clrBlack
        m_Color[4][17] = clrYellow
        m_Color[4][18] = clrDimGray
        m_Color[4][19] = clrYellow
        m_Color[4][20] = clrChocolate
        m_Color[4][21] = clrYellow
        m_Color[4][22] = clrDimGray
        m_Color[4][23] = clrYellow
        m_Color[4][24] = clrBlack
        m_Color[4][25] = clrYellow
        m_Color[4][26] = clrBrown
        m_Color[4][27] = clrGreen
        m_Color[4][28] = clrNavy
        m_Color[4][29] = clrBlack
        m_Color[4][30] = clrYellow
        m_Color[4][31] = clrRed
        m_Color[4][32] = 0x002D2D
        m_Color[4][33] = clrYellow
        m_Color[4][34] = clrKhaki
        m_Color[4][35] = 0x002D2D
        m_Color[4][36] = 0x005A5A
        m_Color[4][37] = 0x005A5A
        m_Color[4][38] = clrYellow
        m_Color[4][39] = 0x002D2D
        m_Color[4][40] = clrYellow
        m_Color[4][41] = clrYellow
        m_Color[4][42] = 0x507878
        m_Color[4][43] = clrYellow
        m_Color[4][44] = clrYellow
        m_Color[4][45] = clrBlack
        m_Color[4][46] = clrYellow
        m_Color[4][47] = 0x507878
        m_Color[4][48] = clrYellow
        m_Color[4][49] = clrYellow
        m_Color[4][50] = clrDarkSlateGray
        m_Color[4][51] = 0x507878
        m_Color[4][52] = 0x788C8C
        m_Color[4][53] = clrGreen
        m_Color[4][54] = clrLime
        m_Color[5][0] = clrBlack
        m_Color[5][1] = clrLime
        m_Color[5][2] = clrLime
        m_Color[5][3] = clrRed
        m_Color[5][4] = clrBlack
        m_Color[5][5] = clrSilver
        m_Color[5][6] = clrLime
        m_Color[5][7] = clrDimGray
        m_Color[5][8] = clrBlack
        m_Color[5][9] = clrRed
        m_Color[5][10] = clrLime
        m_Color[5][11] = clrGreen
        m_Color[5][12] = clrGray
        m_Color[5][13] = clrGray
        m_Color[5][14] = clrNavy
        m_Color[5][15] = clrDimGray
        m_Color[5][16] = clrBlack
        m_Color[5][17] = clrLime
        m_Color[5][18] = clrDimGray
        m_Color[5][19] = clrLime
        m_Color[5][20] = clrForestGreen
        m_Color[5][21] = clrLime
        m_Color[5][22] = clrDimGray
        m_Color[5][23] = clrLime
        m_Color[5][24] = clrBlack
        m_Color[5][25] = clrLime
        m_Color[5][26] = clrBrown
        m_Color[5][27] = clrGreen
        m_Color[5][28] = clrNavy
        m_Color[5][29] = clrBlack
        m_Color[5][30] = clrLime
        m_Color[5][31] = clrRed
        m_Color[5][32] = 0x002D00
        m_Color[5][33] = clrLime
        m_Color[5][34] = clrPaleGreen
        m_Color[5][35] = 0x002D00
        m_Color[5][36] = clrDarkSlateGray
        m_Color[5][37] = clrDarkSlateGray
        m_Color[5][38] = clrLime
        m_Color[5][39] = 0x002D00
        m_Color[5][40] = clrLime
        m_Color[5][41] = clrLime
        m_Color[5][42] = 0x507850
        m_Color[5][43] = clrLime
        m_Color[5][44] = clrLime
        m_Color[5][45] = clrBlack
        m_Color[5][46] = clrLime
        m_Color[5][47] = 0x507850
        m_Color[5][48] = clrLime
        m_Color[5][49] = clrLime
        m_Color[5][50] = 0x507878
        m_Color[5][51] = 0x507850
        m_Color[5][52] = 0x788C78
        m_Color[5][53] = 0xFF6432
        m_Color[5][54] = clrYellow
        m_Color[6][0] = clrBlack
        m_Color[6][1] = clrAqua
        m_Color[6][2] = clrAqua
        m_Color[6][3] = clrRed
        m_Color[6][4] = clrBlack
        m_Color[6][5] = clrSilver
        m_Color[6][6] = clrAqua
        m_Color[6][7] = clrDimGray
        m_Color[6][8] = clrBlack
        m_Color[6][9] = clrRed
        m_Color[6][10] = clrAqua
        m_Color[6][11] = clrLightSeaGreen
        m_Color[6][12] = clrGray
        m_Color[6][13] = clrGray
        m_Color[6][14] = clrNavy
        m_Color[6][15] = clrDimGray
        m_Color[6][16] = clrBlack
        m_Color[6][17] = clrAqua
        m_Color[6][18] = clrDimGray
        m_Color[6][19] = clrAqua
        m_Color[6][20] = clrLightSeaGreen
        m_Color[6][21] = clrAqua
        m_Color[6][22] = clrDimGray
        m_Color[6][23] = clrAqua
        m_Color[6][24] = clrBlack
        m_Color[6][25] = clrAqua
        m_Color[6][26] = clrBrown
        m_Color[6][27] = clrGreen
        m_Color[6][28] = clrNavy
        m_Color[6][29] = clrBlack
        m_Color[6][30] = clrAqua
        m_Color[6][31] = clrRed
        m_Color[6][32] = 0x2D2D00
        m_Color[6][33] = clrAqua
        m_Color[6][34] = clrMediumTurquoise
        m_Color[6][35] = 0x2D2D00
        m_Color[6][36] = clrSlateGray
        m_Color[6][37] = clrSlateGray
        m_Color[6][38] = clrAqua
        m_Color[6][39] = 0x2D2D00
        m_Color[6][40] = clrAqua
        m_Color[6][41] = clrAqua
        m_Color[6][42] = 0x787850
        m_Color[6][43] = clrAqua
        m_Color[6][44] = clrAqua
        m_Color[6][45] = clrBlack
        m_Color[6][46] = clrAqua
        m_Color[6][47] = 0x787850
        m_Color[6][48] = clrAqua
        m_Color[6][49] = clrAqua
        m_Color[6][50] = clrDarkSlateGray
        m_Color[6][51] = 0x787850
        m_Color[6][52] = 0x8C8C78
        m_Color[6][53] = clrBrown
        m_Color[6][54] = clrYellow
        return m_Color[self.m_ShemeIndex][aColorIndex]
    def Show(self):
        m_sc = 7
        m_cc = 45
        m_bcolor = self.Color(1)
        m_RemScheme = self.m_ShemeIndex
        for s in range(0, m_sc):
            w.Label('ColorSchemes_' + IntegerToString(s), 0, 10, 20 + (s * 20), IntegerToString(s), m_bcolor)
        for s in range(0, m_sc):
            self.m_ShemeIndex = s
            for c in range(0, m_cc):
                w.Canvas('ColorSchemes_' + IntegerToString(s) + '_' + IntegerToString(c), 0, 10 + (c * 20) + 15, 20 + (s * 20), 19, 19, self.Color(c), m_bcolor)
        ChartRedraw(0)
        self.m_ShemeIndex = m_RemScheme
    def Hide(self):
        m_sc = 7
        m_cc = 45
        for s in range(0, m_sc):
            ObjectDelete(0, 'ColorSchemes_' + IntegerToString(s))
            for c in range(0, m_cc):
                ObjectDelete(0, 'ColorSchemes_' + IntegerToString(s) + '_' + IntegerToString(c))
        ChartRedraw(0)

class CInputBox(MqlObject):
    _q_fields = ('m_NameEdit', 'm_NameLabel', 'm_Left', 'm_Top', 'm_Width', 'm_Height', 'm_Visible', 'm_Digits', 'm_Caption', 'm_Value', 'm_ValueMin', 'm_ValueMax', 'm_BgColor', 'm_TxtColor', 'm_LblColor', 'm_WarningColor', 'm_Warning', 'm_SubWindow', 'm_Tag', 'm_ReadOnly')
    def __init__(self, *args):
        self.m_NameEdit = ""
        self.m_NameLabel = ""
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_Visible = False
        self.m_Digits = 0
        self.m_Caption = ""
        self.m_Value = ""
        self.m_ValueMin = 0.0
        self.m_ValueMax = 0.0
        self.m_BgColor = 0
        self.m_TxtColor = 0
        self.m_LblColor = 0
        self.m_WarningColor = 0
        self.m_Warning = False
        self.m_SubWindow = 0
        self.m_Tag = ""
        self.m_ReadOnly = False
    def Create(self):
        m_ctmp = self.m_BgColor
        if self.m_Warning:
            m_ctmp = self.m_WarningColor
        w.Edit(self.m_NameEdit, self.m_SubWindow, self.m_Left, self.m_Top, self.m_Width, self.m_Height, self.m_Value, m_ctmp, self.m_TxtColor, 7, 'Arial')
        g.SetReadOnly_2(self.m_NameEdit, self.m_ReadOnly)
        if self.m_Caption != '':
            w.Label(self.m_NameLabel, self.m_SubWindow, self.m_Left + self.m_Width + 1, self.m_Top + 2, self.m_Caption, self.m_LblColor, 7, 'Arial')
    def Delete(self):
        ObjectDelete(0, self.m_NameEdit)
        ObjectDelete(0, self.m_NameLabel)
    def Init(self, aName='CInputBox', aWidth=50, aDigits=-1, aCaption='CInputBox'):
        self.m_NameEdit = aName + '_E'
        self.m_NameLabel = aName + '_L'
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = aWidth
        self.m_Height = 15
        self.m_Visible = False
        self.m_Digits = aDigits
        self.m_Caption = aCaption
        self.m_Value = ''
        if aDigits >= 0:
            self.m_Value = DoubleToString(0, self.m_Digits)
        self.m_ValueMin = -DBL_MAX
        self.m_ValueMax = DBL_MAX
        self.m_BgColor = ClrScheme.Color(0)
        self.m_TxtColor = ClrScheme.Color(1)
        self.m_LblColor = ClrScheme.Color(2)
        self.m_WarningColor = ClrScheme.Color(3)
        self.m_Warning = False
        self.m_SubWindow = 0
        self.m_Tag = ''
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def SetWidth(self, aWidth):
        self.m_Width = aWidth
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        ChartRedraw()
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.Create()
            ChartRedraw()
    def SetValue_1(self, aValue):
        self.m_Value = aValue
        if self.m_Visible:
            g.Attach(self.m_NameEdit)
            g.SetText_1(self.m_Value)
            ChartRedraw()
    def SetValue_2(self, aValue):
        if self.m_Digits >= 0:
            aValue = NormalizeDouble(aValue, self.m_Digits)
            aValue = MathMax(aValue, self.m_ValueMin)
            aValue = MathMin(aValue, self.m_ValueMax)
            self.SetValue_1(DoubleToString(aValue, self.m_Digits))
        else:
            self.SetValue_1(_str(aValue))
    def Event(self, id_, lparam, dparam, sparam):
        m_event = (0 != 0)
        if id_ == CHARTEVENT_OBJECT_ENDEDIT:
            if sparam == self.m_NameEdit:
                if self.m_Digits < 0:
                    g.Attach(self.m_NameEdit)
                    if g.Text_0() != self.m_Value:
                        self.m_Value = g.Text_0()
                        m_event = (1 != 0)
                else:
                    m_OldValue = self.m_Value
                    g.Attach(self.m_NameEdit)
                    m_stmp = Box(g.Text_0())
                    StringReplace(m_stmp, ',', '.')
                    m_dtmp = StringToDouble(m_stmp.v)
                    self.SetValue_2(m_dtmp)
                    if StringToDouble(self.m_Value) != StringToDouble(m_OldValue):
                        m_event = (1 != 0)
        return m_event
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def ValueString(self):
        return self.m_Value
    def ValueDouble(self):
        return StringToDouble(self.m_Value)
    def SetWarning(self, aValue):
        if self.m_Visible:
            if aValue:
                if not self.m_Warning:
                    g.Attach(self.m_NameEdit)
                    g.SetBgColor_1(self.m_WarningColor)
            else:
                if self.m_Warning:
                    g.Attach(self.m_NameEdit)
                    g.SetBgColor_1(self.m_BgColor)
        self.m_Warning = aValue
    def Warning(self):
        return self.m_Warning
    def SetMaxValue(self, aValue):
        self.m_ValueMax = aValue
        if self.m_Digits >= 0:
            if StringToDouble(self.m_Value) > self.m_ValueMax:
                self.SetValue_2(self.m_ValueMax)
    def SetMinValue(self, aValue):
        self.m_ValueMin = aValue
        if self.m_Digits >= 0:
            if StringToDouble(self.m_Value) < self.m_ValueMin:
                self.SetValue_2(self.m_ValueMin)
    def MaxValue(self):
        return self.m_ValueMax
    def MinValue(self):
        return self.m_ValueMin
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag
    def SetDigits(self, aValue):
        self.m_Digits = aValue
        if self.m_Digits >= 0:
            self.SetValue_2(self.ValueDouble())
    def Digits(self):
        return self.m_Digits
    def Visible(self):
        return self.m_Visible
    def SetReadOnly(self, aValue):
        self.m_ReadOnly = aValue
        if self.m_Visible:
            g.SetReadOnly_2(self.m_NameEdit, self.m_ReadOnly)
    def ReadOnly(self):
        return self.m_ReadOnly

class CSpinInputBox(MqlObject):
    _q_fields = ('m_ib', 'm_NameSU', 'm_NameSD', 'm_NameLabel', 'm_Left', 'm_Top', 'm_Width', 'm_Height', 'm_Caption', 'm_SubWindow', 'm_LblColor', 'm_SpBgColor', 'm_SpTxtColor', 'm_FlashColor', 'm_WrongColor', 'm_Visible', 'm_Change', 'm_Digits')
    def __init__(self, *args):
        self.m_ib = CInputBox()
        self.m_NameSU = ""
        self.m_NameSD = ""
        self.m_NameLabel = ""
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_Caption = ""
        self.m_SubWindow = 0
        self.m_LblColor = 0
        self.m_SpBgColor = 0
        self.m_SpTxtColor = 0
        self.m_FlashColor = 0
        self.m_WrongColor = 0
        self.m_Visible = False
        self.m_Change = 0.0
        self.m_Digits = 0
    def DefineDigits(self, aValue):
        m_Digits = 0
        for i in range(8, 0 - 1, -1):
            if aValue >= NormalizeDouble(_fdiv(1.0, MathPow(10, i)), 8):
                m_Digits = i
        return m_Digits
    def Create(self):
        w.Edit(self.m_NameSD, self.m_SubWindow, self.m_Left + self.m_Width - 13, self.m_Top + 7, 13, 8, ' -', self.m_SpBgColor, self.m_SpTxtColor, 6, 'Arial')
        w.Edit(self.m_NameSU, self.m_SubWindow, self.m_Left + self.m_Width - 13, self.m_Top, 13, 8, ' +', self.m_SpBgColor, self.m_SpTxtColor, 5, 'Arial')
        g.SetReadOnly_2(self.m_NameSU, True)
        g.SetReadOnly_2(self.m_NameSD, True)
        if self.m_Caption != '':
            w.Label(self.m_NameLabel, self.m_SubWindow, self.m_Left + self.m_Width + 1, self.m_Top + 2, self.m_Caption, self.m_LblColor, 7, 'Arial')
    def Delete(self):
        ObjectDelete(0, self.m_NameSU)
        ObjectDelete(0, self.m_NameSD)
        ObjectDelete(0, self.m_NameLabel)
    def Flash(self, aName, aFlash, aNormal):
        g.SetBgColor_2(aName, aFlash)
        g.Redraw_0()
        Sleep(100)
        g.SetBgColor_2(aName, aNormal)
        g.Redraw_0()
    def Init(self, aName='CSpinInputBox', aWidth=50, aChange=0.1, aCaption='CSpinInputBox'):
        self.m_NameSU = aName + '_U'
        self.m_NameSD = aName + '_D'
        self.m_NameLabel = aName + '_L'
        self.m_SubWindow = 0
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = aWidth
        self.m_Height = 15
        self.m_Caption = aCaption
        self.m_SpTxtColor = ClrScheme.Color(1)
        self.m_LblColor = ClrScheme.Color(2)
        self.m_WrongColor = ClrScheme.Color(3)
        self.m_SpBgColor = ClrScheme.Color(4)
        self.m_FlashColor = ClrScheme.Color(5)
        self.m_Visible = False
        self.m_Change = aChange
        self.m_Digits = self.DefineDigits(self.m_Change)
        self.m_ib.Init(aName + '_IB', self.m_Width - 12, self.m_Digits, '')
        self.m_ib.SetReadOnly(True)
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.m_ib.SetPos(self.m_Left, self.m_Top)
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
        self.m_ib.SetPosLeft(self.m_Left)
    def SetPosTop(self, aTop):
        self.m_Top = aTop
        self.m_ib.SetPosTop(self.m_Top)
    def SetWidth(self, aWidth):
        self.m_Width = aWidth
        self.m_ib.SetWidth(self.m_Width - 12)
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        self.m_ib.Show_0()
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        self.m_ib.Hide()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.Create()
            self.m_ib.Refresh()
    def Event(self, id_, lparam, dparam, sparam):
        m_event = self.m_ib.Event(id_, lparam, dparam, sparam)
        if m_event == 0:
            m_OldValue = 0.0
            if id_ == CHARTEVENT_OBJECT_CLICK:
                if sparam == self.m_NameSU:
                    m_OldValue = self.m_ib.ValueDouble()
                    self.m_ib.SetValue_2(m_OldValue + self.m_Change)
                    if m_OldValue != self.m_ib.ValueDouble():
                        self.Flash(self.m_NameSU, self.m_FlashColor, self.m_SpBgColor)
                        m_event = 2
                    else:
                        self.Flash(self.m_NameSU, self.m_WrongColor, self.m_SpBgColor)
                if sparam == self.m_NameSD:
                    m_OldValue = self.m_ib.ValueDouble()
                    self.m_ib.SetValue_2(m_OldValue - self.m_Change)
                    if m_OldValue != self.m_ib.ValueDouble():
                        self.Flash(self.m_NameSD, self.m_FlashColor, self.m_SpBgColor)
                        m_event = 2
                    else:
                        self.Flash(self.m_NameSD, self.m_WrongColor, self.m_SpBgColor)
        return m_event
    def SetMaxValue(self, aValue):
        self.m_ib.SetMaxValue(aValue)
    def SetMinValue(self, aValue):
        self.m_ib.SetMinValue(aValue)
    def MaxValue(self):
        return self.m_ib.MaxValue()
    def MinValue(self):
        return self.m_ib.MinValue()
    def SetTag(self, aValue):
        self.m_ib.SetTag(aValue)
    def Tag(self):
        return self.m_ib.Tag()
    def SetValue(self, aValue):
        self.m_ib.SetValue_2(aValue)
    def Value(self):
        return self.m_ib.ValueDouble()
    def SetChange(self, aValue):
        self.m_Change = aValue
        self.m_Digits = self.DefineDigits(self.m_Change)
        self.m_ib.SetDigits(self.m_Digits)
    def Change(self):
        return self.m_Change
    def Digits(self):
        return self.m_Digits
    def SetWarning(self, aValue):
        self.m_ib.SetWarning(aValue)
    def Warning(self):
        return self.m_ib.Warning()
    def SetReadOnly(self, aValue):
        self.m_ib.SetReadOnly(aValue)
    def ReadOnly(self):
        return self.m_ib.ReadOnly()
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.m_ib.SetSubWindow_1(self.m_SubWindow)
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))

class CCheckBox(MqlObject):
    _q_fields = ('m_BgColor', 'm_CheckColor', 'm_LabelColor', 'm_Caption', 'm_NameBox', 'm_NameChecked', 'm_NameLabel', 'm_Left', 'm_Top', 'm_Width', 'm_Height', 'm_Value', 'm_Visible', 'm_SubWindow', 'm_Tag')
    def __init__(self, *args):
        self.m_BgColor = 0
        self.m_CheckColor = 0
        self.m_LabelColor = 0
        self.m_Caption = ""
        self.m_NameBox = ""
        self.m_NameChecked = ""
        self.m_NameLabel = ""
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_Value = False
        self.m_Visible = False
        self.m_SubWindow = 0
        self.m_Tag = ""
    def Create(self):
        w.Canvas(self.m_NameBox, self.m_SubWindow, self.m_Left, self.m_Top, self.m_Width, self.m_Height, self.m_BgColor, self.m_CheckColor)
        m_str = ' '
        if self.m_Value:
            m_str = CharToString(252)
        w.Label(self.m_NameChecked, self.m_SubWindow, self.m_Left + 1, self.m_Top + 1, m_str, self.m_CheckColor, 12, 'Wingdings')
        w.Label(self.m_NameLabel, self.m_SubWindow, self.m_Left + self.m_Width + 1, self.m_Top + 2, self.m_Caption, self.m_LabelColor, 7)
    def Delete(self):
        ObjectDelete(0, self.m_NameBox)
        ObjectDelete(0, self.m_NameChecked)
        ObjectDelete(0, self.m_NameLabel)
    def Init(self, aName='CCheckBox', aCaption='CCheckBox'):
        self.m_NameBox = aName + '_B'
        self.m_NameChecked = aName + '_C'
        self.m_NameLabel = aName + '_L'
        self.m_Caption = aCaption
        self.m_BgColor = ClrScheme.Color(0)
        self.m_CheckColor = ClrScheme.Color(1)
        self.m_LabelColor = ClrScheme.Color(2)
        self.m_Value = False
        self.m_Visible = False
        self.m_Width = 15
        self.m_Height = 15
        self.m_SubWindow = 0
        self.m_Tag = ''
    def Show_2(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.Show_0()
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        ChartRedraw(0)
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        ChartRedraw(0)
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.Create()
            ChartRedraw(0)
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def SetValue(self, aValue):
        self.m_Value = aValue
        if self.m_Visible:
            m_str = ' '
            if self.m_Value:
                m_str = CharToString(252)
            g.SetText_2(self.m_NameChecked, m_str)
            g.Redraw_0()
    def Value(self):
        return self.m_Value
    def Event(self, id_, lparam, dparam, sparam):
        m_event = 0
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if (sparam == self.m_NameBox or sparam == self.m_NameChecked) or sparam == self.m_NameLabel:
                if self.m_Value:
                    self.SetValue(False)
                else:
                    self.SetValue(True)
                m_event = 1
        return m_event
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag

class CRadioGroup(MqlObject):
    _q_fields = ('m_Button', 'm_Left', 'm_Top', 'm_Value', 'm_Visible', 'm_RoundColor', 'm_DotColor', 'm_LabelColor', 'm_Name', 'm_SubWindow', 'm_Width', 'm_Height', 'm_Tag')
    def __init__(self, *args):
        self.m_Button = Arr(0, 0, factory=sRBut)
        self.m_Left = 0
        self.m_Top = 0
        self.m_Value = 0
        self.m_Visible = False
        self.m_RoundColor = 0
        self.m_DotColor = 0
        self.m_LabelColor = 0
        self.m_Name = ""
        self.m_SubWindow = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_Tag = ""
    def Create(self):
        i = 0
        while i < ArraySize(self.m_Button):
            w.Label(self.m_Button[i].NameRound, self.m_SubWindow, self.m_Left + self.m_Button[i].Left, self.m_Top + self.m_Button[i].Top, CharToString(108), self.m_RoundColor, 12, 'Wingdings')
            w.Label(self.m_Button[i].NameDot, self.m_SubWindow, self.m_Left + self.m_Button[i].Left, self.m_Top + self.m_Button[i].Top, CharToString(161), self.m_DotColor, 12, 'Wingdings')
            if self.m_Button[i].Caption != '':
                w.Label(self.m_Button[i].NameLabel, self.m_SubWindow, self.m_Left + self.m_Button[i].Left + 13, self.m_Top + self.m_Button[i].Top + 3, self.m_Button[i].Caption, self.m_LabelColor, 7, 'Arial')
            if self.m_Value > -1:
                g.SetText_2(self.m_Button[self.m_Value].NameDot, CharToString(164))
            i += 1
    def Delete(self):
        for i in range(0, ArraySize(self.m_Button)):
            ObjectDelete(0, self.m_Button[i].NameRound)
            ObjectDelete(0, self.m_Button[i].NameDot)
            ObjectDelete(0, self.m_Button[i].NameLabel)
    def Init(self, aName='CRadioGroup'):
        self.m_RoundColor = ClrScheme.Color(0)
        self.m_DotColor = ClrScheme.Color(1)
        self.m_LabelColor = ClrScheme.Color(2)
        self.m_Name = aName
        ArrayResize(self.m_Button, 0)
        self.m_Value = -1
        self.m_Visible = False
        self.m_SubWindow = 0
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Height = 0
        m_Tag = ''
    def AddButton(self, aCaption='Radio', aLeft=0, aTop=0):
        m_LastIndex = ArraySize(self.m_Button)
        ArrayResize(self.m_Button, m_LastIndex + 1)
        self.m_Button[m_LastIndex].NameRound = self.m_Name + '_B(' + IntegerToString(m_LastIndex) + ')'
        self.m_Button[m_LastIndex].NameDot = self.m_Name + '_D(' + IntegerToString(m_LastIndex) + ')'
        self.m_Button[m_LastIndex].NameLabel = self.m_Name + '_L(' + IntegerToString(m_LastIndex) + ')'
        self.m_Button[m_LastIndex].Caption = aCaption
        self.m_Button[m_LastIndex].Left = aLeft
        self.m_Button[m_LastIndex].Top = aTop
        self.m_Width = MathMax(self.m_Width, aLeft + 14)
        self.m_Height = MathMax(self.m_Height, aTop + 14)
    def Show_2(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.Show_0()
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        ChartRedraw(0)
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        ChartRedraw(0)
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.Create()
            ChartRedraw(0)
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def SetValue(self, aValue):
        if self.m_Value > -1 and self.m_Visible:
            g.SetText_2(self.m_Button[self.m_Value].NameDot, CharToString(161))
            g.Redraw_0()
        self.m_Value = aValue
        self.m_Value = MathMin(self.m_Value, ArraySize(self.m_Button) - 1)
        if self.m_Value > -1 and self.m_Visible:
            g.SetText_2(self.m_Button[self.m_Value].NameDot, CharToString(164))
            g.Redraw_0()
    def Value(self):
        return self.m_Value
    def Event(self, id_, lparam, dparam, sparam):
        m_event = 0
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if StringFind(sparam, self.m_Name, 0) == 0:
                m_pos1 = StringFind(sparam, '(', 0)
                m_pos2 = StringFind(sparam, ')', 0)
                m_Index = _int(StringToInteger(StringSubstr(sparam, m_pos1 + 1, m_pos2 - m_pos1 - 1)))
                if m_Index != self.m_Value:
                    self.SetValue(m_Index)
                    m_event = 1
        return m_event
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag

class sRBut(MqlObject):
    _q_fields = ('NameRound', 'NameDot', 'NameLabel', 'Caption', 'Left', 'Top')
    def __init__(self, *args):
        self.NameRound = ""
        self.NameDot = ""
        self.NameLabel = ""
        self.Caption = ""
        self.Left = 0
        self.Top = 0

class CVScrollBar(MqlObject):
    _q_fields = ('m_NameUpperButton', 'm_NameLowerButton', 'm_NameUpperField', 'm_NameLowerField', 'm_NameSlider', 'm_Left', 'm_Top', 'm_Height', 'm_Width', 'm_Min', 'm_Max', 'm_SmallChange', 'm_LageChange', 'm_Value', 'm_SliderSelected', 'm_SliderHeight', 'm_Range', 'm_A', 'm_D', 'm_L', 'm_G', 'm_T', 'm_E', 'm_K', 'm_N', 'm_BorderColor', 'm_BarColor', 'm_ButtonColor', 'm_WarningColor', 'm_TxtColor', 'm_SliderSelectedColor', 'm_ButtonFlashColor', 'm_BarFlashColor', 'm_FontSize', 'm_Visible', 'm_SubWindow', 'm_Tag')
    def __init__(self, *args):
        self.m_NameUpperButton = ""
        self.m_NameLowerButton = ""
        self.m_NameUpperField = ""
        self.m_NameLowerField = ""
        self.m_NameSlider = ""
        self.m_Left = 0
        self.m_Top = 0
        self.m_Height = 0
        self.m_Width = 0
        self.m_Min = 0
        self.m_Max = 0
        self.m_SmallChange = 0
        self.m_LageChange = 0
        self.m_Value = 0
        self.m_SliderSelected = False
        self.m_SliderHeight = 0
        self.m_Range = 0
        self.m_A = 0
        self.m_D = 0
        self.m_L = 0
        self.m_G = 0
        self.m_T = 0
        self.m_E = 0
        self.m_K = 0
        self.m_N = 0
        self.m_BorderColor = 0
        self.m_BarColor = 0
        self.m_ButtonColor = 0
        self.m_WarningColor = 0
        self.m_TxtColor = 0
        self.m_SliderSelectedColor = 0
        self.m_ButtonFlashColor = 0
        self.m_BarFlashColor = 0
        self.m_FontSize = 0
        self.m_Visible = False
        self.m_SubWindow = 0
        self.m_Tag = ""
    def SetWidthAndFontSize(self, aValue):
        _sw1 = aValue
        if _sw1 == 1:
            self.m_Width = 13
            self.m_FontSize = 6
        elif _sw1 == 2:
            self.m_Width = 19
            self.m_FontSize = 8
        elif _sw1 == 3:
            self.m_Width = 24
            self.m_FontSize = 10
        elif _sw1 == 4:
            self.m_Width = 30
            self.m_FontSize = 14
    def SolveMainPositions(self):
        if self.m_Max < self.m_Min:
            m_tmp = self.m_Max
            self.m_Max = self.m_Min
            self.m_Min = m_tmp
        if self.m_Max == self.m_Min:
            self.m_Max = self.m_Min + 1
        self.m_Range = self.m_Max - self.m_Min
        self.m_LageChange = MathMin(self.m_LageChange, self.m_Range)
        self.m_SmallChange = MathMin(self.m_SmallChange, self.m_LageChange)
        self.m_LageChange = MathMax(self.m_LageChange, 1)
        self.m_SmallChange = MathMax(self.m_SmallChange, 1)
        self.m_D = self.m_Height - (2 * self.m_Width)
        self.m_SliderHeight = _idiv(self.m_D, _idiv(self.m_Range, self.m_LageChange) + 1)
        self.m_SliderHeight = MathMax(self.m_SliderHeight, 3)
        self.m_L = self.m_D - self.m_SliderHeight
        self.m_G = self.m_Top - self.m_Width + self.m_Height
        self.m_E = self.m_Top + self.m_Width
        self.m_T = self.m_E + self.m_SliderHeight
        self.m_K = self.m_D - self.m_SliderHeight
        self.m_N = self.m_Top + self.m_Width + _idiv(self.m_SliderHeight, 2)
    def SetObjectsPos(self):
        self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
        self.m_A = _idiv(self.m_K * (self.m_Value - self.m_Min), self.m_Range)
        g.Attach(self.m_NameUpperField)
        g.SetXYDistance_2(self.m_Left, self.m_E - 1)
        g.SetXYSize_2(self.m_Width, self.m_A + 2)
        g.Attach(self.m_NameLowerField)
        g.SetXYDistance_2(self.m_Left, self.m_T + self.m_A - 1)
        g.SetXYSize_2(self.m_Width, self.m_L - self.m_A + 2)
        g.Attach(self.m_NameSlider)
        g.SetXYDistance_2(self.m_Left, self.m_E + self.m_A - 1)
        g.SetXYSize_2(self.m_Width, self.m_SliderHeight + 2)
        g.Attach(self.m_NameSlider)
        g.SetBgColor_1(self.m_ButtonColor)
        g.Attach(self.m_NameLowerButton)
        g.SetXYDistance_2(self.m_Left, self.m_Top)
        g.SetXYSize_2(self.m_Width, self.m_Width)
        g.Attach(self.m_NameUpperButton)
        g.SetXYDistance_2(self.m_Left, self.m_G)
        g.SetXYSize_2(self.m_Width, self.m_Width)
        ChartRedraw(0)
    def Create(self):
        self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
        self.m_A = _idiv(self.m_K * (self.m_Value - self.m_Min), self.m_Range)
        w.Edit(self.m_NameUpperField, self.m_SubWindow, self.m_Left, self.m_E - 1, self.m_Width, self.m_A + 2, '', self.m_BarColor, self.m_BorderColor)
        g.SetReadOnly_2(self.m_NameUpperField, True)
        w.Edit(self.m_NameLowerField, self.m_SubWindow, self.m_Left, self.m_T + self.m_A - 1, self.m_Width, self.m_L - self.m_A + 2, '', self.m_BarColor, self.m_BorderColor)
        g.SetReadOnly_2(self.m_NameLowerField, True)
        w.Edit(self.m_NameSlider, self.m_SubWindow, self.m_Left, self.m_E + self.m_A - 1, self.m_Width, self.m_SliderHeight + 2, '', self.m_ButtonColor, self.m_BorderColor)
        g.SetReadOnly_2(self.m_NameSlider, True)
        w.Edit(self.m_NameLowerButton, self.m_SubWindow, self.m_Left, self.m_Top, self.m_Width, self.m_Width, ' /\\', self.m_ButtonColor, self.m_BorderColor, self.m_FontSize, 'Arial')
        g.SetReadOnly_2(self.m_NameLowerButton, True)
        w.Edit(self.m_NameUpperButton, self.m_SubWindow, self.m_Left, self.m_G, self.m_Width, self.m_Width, ' \\/', self.m_ButtonColor, self.m_BorderColor, self.m_FontSize, 'Arial')
        g.SetReadOnly_2(self.m_NameUpperButton, True)
    def Delete(self):
        ObjectDelete(0, self.m_NameUpperButton)
        ObjectDelete(0, self.m_NameLowerButton)
        ObjectDelete(0, self.m_NameUpperField)
        ObjectDelete(0, self.m_NameLowerField)
        ObjectDelete(0, self.m_NameSlider)
    def ChartClickY(self, aDparam, aY):
        hs = 0
        ps = 0
        i = 0
        while i < ChartGetInteger(0, CHART_WINDOWS_TOTAL):
            hs += 3 + ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, i)
            if hs >= aDparam:
                aY.v = _int(aDparam - ps - 3)
                break
            ps = hs
            i += 1
    def RePose(self):
        if self.m_Visible:
            self.SolveMainPositions()
            self.SetObjectsPos()
            ChartRedraw()
    def Flash(self, aName, aFlash, aNormal):
        g.SetBgColor_2(aName, aFlash)
        g.Redraw_0()
        Sleep(100)
        g.SetBgColor_2(aName, aNormal)
        g.Redraw_0()
    def Init(self, aName='CVScrollBar', aHeight=100, aSizeType=1):
        self.m_Visible = False
        self.m_NameUpperButton = aName + '_UB'
        self.m_NameLowerButton = aName + '_LB'
        self.m_NameUpperField = aName + '_UF'
        self.m_NameLowerField = aName + '_LF'
        self.m_NameSlider = aName + '_S'
        self.m_BorderColor = ClrScheme.Color(6)
        self.m_BarColor = ClrScheme.Color(7)
        self.m_ButtonColor = ClrScheme.Color(8)
        self.m_WarningColor = ClrScheme.Color(9)
        self.m_TxtColor = ClrScheme.Color(10)
        self.m_SliderSelectedColor = ClrScheme.Color(11)
        self.m_ButtonFlashColor = ClrScheme.Color(12)
        self.m_BarFlashColor = ClrScheme.Color(13)
        self.m_Min = 0
        self.m_Max = 100
        self.m_SmallChange = 1
        self.m_LageChange = 10
        self.m_Value = 0
        self.m_Height = aHeight
        self.m_SubWindow = 0
        self.SetWidthAndFontSize(aSizeType)
        m_Tag = ''
    def Show_0(self):
        self.m_Visible = True
        self.SolveMainPositions()
        self.Create()
        ChartRedraw()
    def Show_2(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.SolveMainPositions()
            self.Create()
            ChartRedraw()
    def Visible(self):
        return self.m_Visible
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def SetSizeType(self, aValue):
        self.SetWidthAndFontSize(aValue)
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def SetHeight(self, aValue):
        self.m_Height = aValue
    def Height(self):
        return self.m_Height
    def Width(self):
        return self.m_Width
    def SetMin(self, aValue):
        self.m_Min = aValue
    def SetMax(self, aValue):
        self.m_Max = aValue
    def SetSmallChange(self, aValue):
        self.m_SmallChange = aValue
    def SetLageChange(self, aValue):
        self.m_LageChange = aValue
    def SetValue(self, aValue):
        self.m_Value = aValue
        self.RePose()
    def Min(self):
        return self.m_Min
    def Max(self):
        return self.m_Max
    def SmallChange(self):
        return self.m_SmallChange
    def LageChange(self):
        return self.m_LageChange
    def Value(self):
        return self.m_Value
    def Event(self, id_, lparam, dparam, sparam):
        m_old = self.m_Value
        if id_ == CHARTEVENT_OBJECT_CLICK:
            m_Y = Box(0)
            self.ChartClickY(dparam, m_Y)
            if sparam == self.m_NameLowerButton:
                if self.m_Value > self.m_Min:
                    self.Flash(self.m_NameLowerButton, self.m_ButtonFlashColor, self.m_ButtonColor)
                else:
                    self.Flash(self.m_NameLowerButton, self.m_WarningColor, self.m_ButtonColor)
                if self.m_SliderSelected:
                    self.m_Value = self.m_Min
                    self.m_SliderSelected = False
                else:
                    self.m_Value -= self.m_SmallChange
                    self.m_Value = MathMax(self.m_Value, self.m_Min)
                self.RePose()
            if sparam == self.m_NameUpperButton:
                if self.m_Value < self.m_Max:
                    self.Flash(self.m_NameUpperButton, self.m_ButtonFlashColor, self.m_ButtonColor)
                else:
                    self.Flash(self.m_NameUpperButton, self.m_WarningColor, self.m_ButtonColor)
                if self.m_SliderSelected:
                    self.m_Value = self.m_Max
                    self.m_SliderSelected = False
                else:
                    self.m_Value += self.m_SmallChange
                    self.m_Value = MathMin(self.m_Value, self.m_Max)
                self.RePose()
            if sparam == self.m_NameUpperField:
                self.Flash(self.m_NameUpperField, self.m_BarFlashColor, self.m_BarColor)
                if self.m_SliderSelected:
                    self.m_Value = self.m_Min + _idiv(self.m_Range * (m_Y.v - self.m_N), self.m_L)
                    self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
                    self.m_SliderSelected = False
                else:
                    self.m_Value -= self.m_LageChange
                    self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
                self.RePose()
            if sparam == self.m_NameLowerField:
                self.Flash(self.m_NameLowerField, self.m_BarFlashColor, self.m_BarColor)
                if self.m_SliderSelected:
                    self.m_Value = self.m_Min + _idiv(self.m_Range * (m_Y.v - self.m_N), self.m_L)
                    self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
                    self.m_SliderSelected = False
                else:
                    self.m_Value += self.m_LageChange
                    self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
                self.RePose()
            if sparam == self.m_NameSlider:
                if self.m_SliderSelected:
                    g.Attach(self.m_NameSlider)
                    self.m_SliderSelected = False
                    g.SetBgColor_1(self.m_ButtonColor)
                    g.Redraw_0()
                else:
                    self.m_SliderSelected = True
                    g.Attach(self.m_NameSlider)
                    g.SetBgColor_1(self.m_SliderSelectedColor)
                    g.Redraw_0()
        if m_old != self.m_Value:
            return 1
        return 0
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag

class CHScrollBar(MqlObject):
    _q_fields = ('m_NameUpperButton', 'm_NameLowerButton', 'm_NameUpperField', 'm_NameLowerField', 'm_NameSlider', 'm_Left', 'm_Top', 'm_Height', 'm_Width', 'm_Min', 'm_Max', 'm_SmallChange', 'm_LageChange', 'm_Value', 'm_SliderSelected', 'm_SliderWidth', 'm_Range', 'm_A', 'm_D', 'm_L', 'm_G', 'm_T', 'm_E', 'm_K', 'm_N', 'm_BorderColor', 'm_BarColor', 'm_ButtonColor', 'm_WarningColor', 'm_TxtColor', 'm_SliderSelectedColor', 'm_ButtonFlashColor', 'm_BarFlashColor', 'm_FontSize', 'm_Visible', 'm_SubWindow', 'm_Tag')
    def __init__(self, *args):
        self.m_NameUpperButton = ""
        self.m_NameLowerButton = ""
        self.m_NameUpperField = ""
        self.m_NameLowerField = ""
        self.m_NameSlider = ""
        self.m_Left = 0
        self.m_Top = 0
        self.m_Height = 0
        self.m_Width = 0
        self.m_Min = 0
        self.m_Max = 0
        self.m_SmallChange = 0
        self.m_LageChange = 0
        self.m_Value = 0
        self.m_SliderSelected = False
        self.m_SliderWidth = 0
        self.m_Range = 0
        self.m_A = 0
        self.m_D = 0
        self.m_L = 0
        self.m_G = 0
        self.m_T = 0
        self.m_E = 0
        self.m_K = 0
        self.m_N = 0
        self.m_BorderColor = 0
        self.m_BarColor = 0
        self.m_ButtonColor = 0
        self.m_WarningColor = 0
        self.m_TxtColor = 0
        self.m_SliderSelectedColor = 0
        self.m_ButtonFlashColor = 0
        self.m_BarFlashColor = 0
        self.m_FontSize = 0
        self.m_Visible = False
        self.m_SubWindow = 0
        self.m_Tag = ""
    def SetWidthAndFontSize(self, aValue):
        _sw2 = aValue
        if _sw2 == 1:
            self.m_Height = 13
            self.m_FontSize = 8
        elif _sw2 == 2:
            self.m_Height = 19
            self.m_FontSize = 11
        elif _sw2 == 3:
            self.m_Height = 24
            self.m_FontSize = 15
        elif _sw2 == 4:
            self.m_Height = 30
            self.m_FontSize = 19
    def SolveMainPositions(self):
        if self.m_Max < self.m_Min:
            m_tmp = self.m_Max
            self.m_Max = self.m_Min
            self.m_Min = m_tmp
        if self.m_Max == self.m_Min:
            self.m_Max = self.m_Min + 1
        self.m_Range = self.m_Max - self.m_Min
        self.m_LageChange = MathMin(self.m_LageChange, self.m_Range)
        self.m_SmallChange = MathMin(self.m_SmallChange, self.m_LageChange)
        self.m_LageChange = MathMax(self.m_LageChange, 1)
        self.m_SmallChange = MathMax(self.m_SmallChange, 1)
        self.m_D = self.m_Width - (2 * self.m_Height)
        self.m_SliderWidth = _idiv(self.m_D, _idiv(self.m_Range, self.m_LageChange) + 1)
        self.m_SliderWidth = MathMax(self.m_SliderWidth, 3)
        self.m_L = self.m_D - self.m_SliderWidth
        self.m_G = self.m_Left - self.m_Height + self.m_Width
        self.m_E = self.m_Left + self.m_Height
        self.m_T = self.m_E + self.m_SliderWidth
        self.m_K = self.m_D - self.m_SliderWidth
        self.m_N = self.m_Left + self.m_Height + _idiv(self.m_SliderWidth, 2)
    def SetObjectsPos(self):
        self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
        self.m_A = _idiv(self.m_K * (self.m_Value - self.m_Min), self.m_Range)
        g.Attach(self.m_NameUpperField)
        g.SetXYDistance_2(self.m_E - 1, self.m_Top)
        g.SetXYSize_2(self.m_A + 2, self.m_Height)
        g.Attach(self.m_NameLowerField)
        g.SetXYDistance_2(self.m_T + self.m_A - 1, self.m_Top)
        g.SetXYSize_2(self.m_L - self.m_A + 2, self.m_Height)
        g.Attach(self.m_NameSlider)
        g.SetXYDistance_2(self.m_E + self.m_A - 1, self.m_Top)
        g.SetXYSize_2(self.m_SliderWidth + 2, self.m_Height)
        g.Attach(self.m_NameSlider)
        g.SetBgColor_1(self.m_ButtonColor)
        g.Attach(self.m_NameLowerButton)
        g.SetXYDistance_2(self.m_Left, self.m_Top)
        g.SetXYSize_2(self.m_Height, self.m_Height)
        g.Attach(self.m_NameUpperButton)
        g.SetXYDistance_2(self.m_G, self.m_Top)
        g.SetXYSize_2(self.m_Height, self.m_Height)
        ChartRedraw(0)
    def Create(self):
        self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
        self.m_A = _idiv(self.m_K * (self.m_Value - self.m_Min), self.m_Range)
        w.Edit(self.m_NameUpperField, self.m_SubWindow, self.m_E - 1, self.m_Top, self.m_A + 2, self.m_Height, '', self.m_BarColor, self.m_BorderColor)
        g.SetReadOnly_2(self.m_NameUpperField, True)
        w.Edit(self.m_NameLowerField, self.m_SubWindow, self.m_T + self.m_A - 1, self.m_Top, self.m_L - self.m_A + 2, self.m_Height, '', self.m_BarColor, self.m_BorderColor)
        g.SetReadOnly_2(self.m_NameLowerField, True)
        w.Edit(self.m_NameSlider, self.m_SubWindow, self.m_E + self.m_A - 1, self.m_Top, self.m_SliderWidth + 2, self.m_Height, '', self.m_ButtonColor, self.m_BorderColor)
        g.SetReadOnly_2(self.m_NameSlider, True)
        w.Edit(self.m_NameLowerButton, self.m_SubWindow, self.m_Left, self.m_Top, self.m_Height, self.m_Height, '<', self.m_ButtonColor, self.m_BorderColor, self.m_FontSize, 'Arial')
        g.SetReadOnly_2(self.m_NameLowerButton, True)
        w.Edit(self.m_NameUpperButton, self.m_SubWindow, self.m_G, self.m_Top, self.m_Height, self.m_Height, '>', self.m_ButtonColor, self.m_BorderColor, self.m_FontSize, 'Arial')
        g.SetReadOnly_2(self.m_NameUpperButton, True)
    def Delete(self):
        ObjectDelete(0, self.m_NameUpperButton)
        ObjectDelete(0, self.m_NameLowerButton)
        ObjectDelete(0, self.m_NameUpperField)
        ObjectDelete(0, self.m_NameLowerField)
        ObjectDelete(0, self.m_NameSlider)
    def RePose(self):
        if self.m_Visible:
            self.SolveMainPositions()
            self.SetObjectsPos()
            ChartRedraw()
    def Flash(self, aName, aFlash, aNormal):
        g.SetBgColor_2(aName, aFlash)
        g.Redraw_0()
        Sleep(100)
        g.SetBgColor_2(aName, aNormal)
        g.Redraw_0()
    def Init(self, aName='CHScrollBar', aWidth=100, aSizeType=1):
        self.m_Visible = False
        self.m_NameUpperButton = aName + '_UB'
        self.m_NameLowerButton = aName + '_LB'
        self.m_NameUpperField = aName + '_UF'
        self.m_NameLowerField = aName + '_LF'
        self.m_NameSlider = aName + '_S'
        self.m_BorderColor = ClrScheme.Color(6)
        self.m_BarColor = ClrScheme.Color(7)
        self.m_ButtonColor = ClrScheme.Color(8)
        self.m_WarningColor = ClrScheme.Color(9)
        self.m_TxtColor = ClrScheme.Color(10)
        self.m_SliderSelectedColor = ClrScheme.Color(11)
        self.m_ButtonFlashColor = ClrScheme.Color(12)
        self.m_BarFlashColor = ClrScheme.Color(13)
        self.m_Min = 0
        self.m_Max = 100
        self.m_SmallChange = 1
        self.m_LageChange = 10
        self.m_Value = 0
        self.m_Width = aWidth
        self.m_SubWindow = 0
        self.SetWidthAndFontSize(aSizeType)
        self.m_Tag = ''
    def Show_0(self):
        self.m_Visible = True
        self.SolveMainPositions()
        self.Create()
        ChartRedraw()
    def Show_2(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.SolveMainPositions()
            self.Create()
            ChartRedraw()
    def Visible(self):
        return self.m_Visible
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def SetSizeType(self, aValue):
        self.SetWidthAndFontSize(aValue)
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def SetWidth(self, aValue):
        self.m_Width = aValue
    def Height(self):
        return self.m_Height
    def Width(self):
        return self.m_Width
    def SetMin(self, aValue):
        self.m_Min = aValue
    def SetMax(self, aValue):
        self.m_Max = aValue
    def SetSmallChange(self, aValue):
        self.m_SmallChange = aValue
    def SetLageChange(self, aValue):
        self.m_LageChange = aValue
    def SetValue(self, aValue):
        self.m_Value = aValue
        self.RePose()
    def Min(self):
        return self.m_Min
    def Max(self):
        return self.m_Max
    def SmallChange(self):
        return self.m_SmallChange
    def LageChange(self):
        return self.m_LageChange
    def Value(self):
        return self.m_Value
    def Event(self, id_, lparam, dparam, sparam):
        m_old = self.m_Value
        if id_ == CHARTEVENT_OBJECT_CLICK:
            m_Y = _int(lparam) - 2
            if sparam == self.m_NameLowerButton:
                if self.m_Value > self.m_Min:
                    self.Flash(self.m_NameLowerButton, self.m_ButtonFlashColor, self.m_ButtonColor)
                else:
                    self.Flash(self.m_NameLowerButton, self.m_WarningColor, self.m_ButtonColor)
                if self.m_SliderSelected:
                    self.m_Value = self.m_Min
                    self.m_SliderSelected = False
                else:
                    self.m_Value -= self.m_SmallChange
                    self.m_Value = MathMax(self.m_Value, self.m_Min)
                self.RePose()
            if sparam == self.m_NameUpperButton:
                if self.m_Value < self.m_Max:
                    self.Flash(self.m_NameUpperButton, self.m_ButtonFlashColor, self.m_ButtonColor)
                else:
                    self.Flash(self.m_NameUpperButton, self.m_WarningColor, self.m_ButtonColor)
                if self.m_SliderSelected:
                    self.m_Value = self.m_Max
                    self.m_SliderSelected = False
                else:
                    self.m_Value += self.m_SmallChange
                    self.m_Value = MathMin(self.m_Value, self.m_Max)
                self.RePose()
            if sparam == self.m_NameUpperField:
                self.Flash(self.m_NameUpperField, self.m_BarFlashColor, self.m_BarColor)
                if self.m_SliderSelected:
                    self.m_Value = self.m_Min + _idiv(self.m_Range * (m_Y - self.m_N), self.m_L)
                    self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
                    self.m_SliderSelected = False
                else:
                    self.m_Value -= self.m_LageChange
                    self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
                self.RePose()
            if sparam == self.m_NameLowerField:
                self.Flash(self.m_NameLowerField, self.m_BarFlashColor, self.m_BarColor)
                if self.m_SliderSelected:
                    self.m_Value = self.m_Min + _idiv(self.m_Range * (m_Y - self.m_N), self.m_L)
                    self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
                    self.m_SliderSelected = False
                else:
                    self.m_Value += self.m_LageChange
                    self.m_Value = MathMin(MathMax(self.m_Value, self.m_Min), self.m_Max)
                self.RePose()
            if sparam == self.m_NameSlider:
                if self.m_SliderSelected:
                    g.Attach(self.m_NameSlider)
                    self.m_SliderSelected = False
                    g.SetBgColor_1(self.m_ButtonColor)
                    g.Redraw_0()
                else:
                    self.m_SliderSelected = True
                    g.Attach(self.m_NameSlider)
                    g.SetBgColor_1(self.m_SliderSelectedColor)
                    g.Redraw_0()
        if m_old != self.m_Value:
            return 1
        return 0
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag

class CList(MqlObject):
    _q_fields = ('m_Name', 'm_Left', 'm_Top', 'm_Width', 'm_HeightInItems', 'm_Height', 'm_ItemText', 'm_SubWindow', 'm_sb', 'm_Visible', 'm_Selected', 'm_BgColor', 'm_TxtColor', 'm_SelColor', 'm_LastSelected', 'm_SbVisible', 'm_FieldsCount', 'm_AllowDeselect')
    def __init__(self, *args):
        self.m_Name = ""
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_HeightInItems = 0
        self.m_Height = 0
        self.m_ItemText = Arr(0, "")
        self.m_SubWindow = 0
        self.m_sb = CVScrollBar()
        self.m_Visible = False
        self.m_Selected = 0
        self.m_BgColor = 0
        self.m_TxtColor = 0
        self.m_SelColor = 0
        self.m_LastSelected = 0
        self.m_SbVisible = False
        self.m_FieldsCount = 0
        self.m_AllowDeselect = False
    def Create(self):
        m_w = self.m_Width
        if ArraySize(self.m_ItemText) > self.m_HeightInItems:
            self.m_SbVisible = True
            m_w -= self.m_sb.Width()
            self.m_sb.SetPos(self.m_Left + m_w, self.m_Top)
            self.m_sb.SetHeight(self.m_Height)
            self.m_sb.SetMax(ArraySize(self.m_ItemText) - self.m_HeightInItems)
            self.m_sb.SetLageChange(self.m_HeightInItems)
            self.m_sb.SetSubWindow_1(self.m_SubWindow)
            if self.m_sb.Value() > (ArraySize(self.m_ItemText) - self.m_HeightInItems):
                self.m_sb.SetValue(ArraySize(self.m_ItemText) - self.m_HeightInItems)
            m_w += 1
        else:
            self.m_SbVisible = False
            self.m_sb.SetValue(0)
        s = self.m_sb.Value()
        e = MathMin(s + self.m_HeightInItems, ArraySize(self.m_ItemText))
        i = 0
        m_ItemName = ""
        while s < e:
            m_ItemName = self.m_Name + '_IT(' + IntegerToString(i) + ')'
            w.Edit(m_ItemName, self.m_SubWindow, self.m_Left, self.m_Top + (i * 14), m_w, 15, self.m_ItemText[s], self.m_BgColor, self.m_TxtColor)
            g.SetReadOnly_2(m_ItemName, True)
            s += 1
            i += 1
        while i < self.m_HeightInItems:
            m_ItemName = self.m_Name + '_IT(' + IntegerToString(i) + ')'
            w.Edit(m_ItemName, self.m_SubWindow, self.m_Left, self.m_Top + (i * 14), m_w, 15, '', self.m_BgColor, self.m_TxtColor)
            g.SetReadOnly_2(m_ItemName, True)
            i += 1
        self.m_FieldsCount = self.m_HeightInItems
        self.SelectedON()
    def SelectedON(self):
        if self.m_Selected >= 0:
            self.m_LastSelected = -1
            m_Index = self.m_Selected - self.m_sb.Value()
            if m_Index >= 0 and m_Index < self.m_HeightInItems:
                self.m_LastSelected = m_Index
                g.SetBgColor_2(self.m_Name + '_IT(' + IntegerToString(m_Index) + ')', self.m_SelColor)
    def SelectedOFF(self):
        if self.m_LastSelected >= 0:
            g.SetBgColor_2(self.m_Name + '_IT(' + IntegerToString(self.m_LastSelected) + ')', self.m_BgColor)
            self.m_LastSelected = -1
    def Delete(self):
        for i in range(0, self.m_FieldsCount):
            m_ItemName = self.m_Name + '_IT(' + IntegerToString(i) + ')'
            ObjectDelete(0, m_ItemName)
    def PutValues(self):
        s = self.m_sb.Value()
        e = MathMin(s + self.m_HeightInItems, ArraySize(self.m_ItemText))
        i = 0
        m_ItemName = ""
        while s < e:
            m_ItemName = self.m_Name + '_IT(' + IntegerToString(i) + ')'
            g.SetText_2(m_ItemName, self.m_ItemText[s])
            s += 1
            i += 1
        while i < self.m_HeightInItems:
            m_ItemName = self.m_Name + '_IT(' + IntegerToString(i) + ')'
            g.SetText_2(m_ItemName, ' ')
            i += 1
    def Init(self, aName='CList', aWidth=100, aHeightInItems=8):
        self.m_Visible = False
        self.m_Name = aName
        self.m_Width = aWidth
        self.m_HeightInItems = aHeightInItems
        self.m_Left = 0
        self.m_Top = 0
        ArrayResize(self.m_ItemText, 0)
        self.m_BgColor = ClrScheme.Color(0)
        self.m_TxtColor = ClrScheme.Color(1)
        self.m_SelColor = ClrScheme.Color(14)
        self.m_Height = (self.m_HeightInItems * 14) + 1
        self.m_sb.Init(aName + '_SB', self.m_Height, 1)
        self.m_sb.SetMin(0)
        self.m_sb.SetValue(0)
        self.m_sb.SetSmallChange(1)
        self.m_sb.SetLageChange(aHeightInItems)
        self.m_Selected = -1
        self.m_LastSelected = -1
        self.m_SbVisible = False
        self.m_AllowDeselect = True
    def SetAllowDeselect(self, aValue):
        self.m_AllowDeselect = aValue
    def AllowDeselect(self):
        return self.m_AllowDeselect
    def AddItem(self, aText):
        ArrayResize(self.m_ItemText, ArraySize(self.m_ItemText) + 1)
        self.m_ItemText[ArraySize(self.m_ItemText) - 1] = aText
    def DeleteItem(self, aIndex):
        if aIndex < ArraySize(self.m_ItemText):
            for i in range(aIndex, ArraySize(self.m_ItemText) - 1):
                self.m_ItemText[i] = self.m_ItemText[i + 1]
            ArrayResize(self.m_ItemText, ArraySize(self.m_ItemText) - 1)
            if aIndex < self.m_Selected:
                self.m_Selected -= 1
            elif aIndex == self.m_Selected:
                self.m_Selected = -1
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        if self.m_SbVisible:
            self.m_sb.Show_0()
        else:
            ChartRedraw(0)
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        if self.m_SbVisible:
            self.m_sb.Hide()
            self.m_SbVisible = False
        else:
            ChartRedraw(0)
    def Visible(self):
        return self.m_Visible
    def Refresh(self):
        if self.m_Visible:
            self.Hide()
            self.Show_0()
            ChartRedraw(0)
    def Count(self):
        return ArraySize(self.m_ItemText)
    def SelectedIndex(self):
        return self.m_Selected
    def SelectedText(self):
        if self.m_Selected < 0:
            return ''
        return self.m_ItemText[self.m_Selected]
    def Text(self, aIndex):
        return self.m_ItemText[aIndex]
    def SetSelectedIndex(self, aIndex):
        if aIndex >= -1 and aIndex < ArraySize(self.m_ItemText):
            self.m_Selected = aIndex
            if self.m_Visible:
                self.SelectedOFF()
                self.SelectedON()
                ChartRedraw()
    def SetText(self, aIndex, aText):
        self.m_ItemText[aIndex] = aText
        if self.m_Visible:
            if aIndex >= self.m_sb.Value() and aIndex < (self.m_sb.Value() + self.m_HeightInItems):
                g.SetText_2(self.m_Name + '_IT(' + IntegerToString(aIndex - self.m_sb.Value()) + ')', aText)
                ChartRedraw()
    def SetWidth(self, aValue):
        self.m_Width = aValue
    def SetHeightInItems(self, aValue):
        self.m_HeightInItems = aValue
        self.m_Height = (self.m_HeightInItems * 14) + 1
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Event(self, id_, lparam, dparam, sparam):
        m_event = 0
        if self.m_sb.Event(id_, lparam, dparam, sparam) == 1:
            self.SelectedOFF()
            self.PutValues()
            self.SelectedON()
            ChartRedraw()
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if StringFind(sparam, self.m_Name + '_IT(', 0) == 0:
                m_Pos1 = StringFind(sparam, '_IT(', 0)
                m_Pos2 = StringFind(sparam, ')', m_Pos1)
                m_Index = self.m_sb.Value() + _int(StringToInteger(StringSubstr(sparam, m_Pos1 + 4, m_Pos2 - m_Pos1 - 4)))
                if m_Index < ArraySize(self.m_ItemText):
                    if m_Index == self.m_Selected:
                        if self.m_AllowDeselect:
                            self.SetSelectedIndex(-1)
                            m_event = 1
                    else:
                        self.SetSelectedIndex(m_Index)
                        m_event = 2
        return m_event
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def ScrollTo(self, aValue):
        if ArraySize(self.m_ItemText) > self.m_HeightInItems:
            aValue = MathMin(ArraySize(self.m_ItemText) - self.m_HeightInItems, MathMax(0, aValue))
            self.m_sb.SetValue(aValue)
            if self.m_Visible:
                self.SelectedOFF()
                self.PutValues()
                self.SelectedON()
                ChartRedraw()
    def FirstIndex(self):
        return self.m_sb.Value()
    def Clear(self):
        ArrayResize(self.m_ItemText, 0)
        self.m_Selected = -1
        self.m_LastSelected = -1
    def SetTag(self, aValue):
        self.m_sb.SetTag(aValue)
    def Tag(self):
        return self.m_sb.Tag()

class CListMS(MqlObject):
    _q_fields = ('m_Name', 'm_Left', 'm_Top', 'm_Width', 'm_HeightInItems', 'm_Height', 'm_ItemText', 'm_Itemselected', 'm_SubWindow', 'm_sb', 'm_Visible', 'm_BgColor', 'm_TxtColor', 'm_SelColor', 'm_SbVisible', 'm_FieldsCount', 'm_LastChanged', 'm_SearchFrom')
    def __init__(self, *args):
        self.m_Name = ""
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_HeightInItems = 0
        self.m_Height = 0
        self.m_ItemText = Arr(0, "")
        self.m_Itemselected = Arr(0, False)
        self.m_SubWindow = 0
        self.m_sb = CVScrollBar()
        self.m_Visible = False
        self.m_BgColor = 0
        self.m_TxtColor = 0
        self.m_SelColor = 0
        self.m_SbVisible = False
        self.m_FieldsCount = 0
        self.m_LastChanged = 0
        self.m_SearchFrom = 0
    def Create(self):
        m_w = self.m_Width
        if ArraySize(self.m_ItemText) > self.m_HeightInItems:
            self.m_SbVisible = True
            m_w -= self.m_sb.Width()
            self.m_sb.SetPos(self.m_Left + m_w, self.m_Top)
            self.m_sb.SetHeight(self.m_Height)
            self.m_sb.SetMax(ArraySize(self.m_ItemText) - self.m_HeightInItems)
            self.m_sb.SetLageChange(self.m_HeightInItems)
            self.m_sb.SetSubWindow_1(self.m_SubWindow)
            if self.m_sb.Value() > (ArraySize(self.m_ItemText) - self.m_HeightInItems):
                self.m_sb.SetValue(ArraySize(self.m_ItemText) - self.m_HeightInItems)
            m_w += 1
        else:
            self.m_SbVisible = False
            self.m_sb.SetValue(0)
        s = self.m_sb.Value()
        e = MathMin(s + self.m_HeightInItems, ArraySize(self.m_ItemText))
        i = 0
        m_ItemName = ""
        while s < e:
            m_ItemName = self.m_Name + '_IT(' + IntegerToString(i) + ')'
            m_Clr = self.m_BgColor
            if self.m_Itemselected[s]:
                m_Clr = self.m_SelColor
            w.Edit(m_ItemName, self.m_SubWindow, self.m_Left, self.m_Top + (i * 14), m_w, 15, self.m_ItemText[s], m_Clr, self.m_TxtColor)
            g.SetReadOnly_2(m_ItemName, True)
            s += 1
            i += 1
        while i < self.m_HeightInItems:
            m_ItemName = self.m_Name + '_IT(' + IntegerToString(i) + ')'
            w.Edit(m_ItemName, self.m_SubWindow, self.m_Left, self.m_Top + (i * 14), m_w, 15, '', self.m_BgColor, self.m_TxtColor)
            g.SetReadOnly_2(m_ItemName, True)
            i += 1
        self.m_FieldsCount = self.m_HeightInItems
    def Delete(self):
        for i in range(0, self.m_FieldsCount):
            m_ItemName = self.m_Name + '_IT(' + IntegerToString(i) + ')'
            ObjectDelete(0, m_ItemName)
    def PutValues(self):
        s = self.m_sb.Value()
        e = MathMin(s + self.m_HeightInItems, ArraySize(self.m_ItemText))
        i = 0
        m_ItemName = ""
        while s < e:
            m_ItemName = self.m_Name + '_IT(' + IntegerToString(i) + ')'
            g.SetText_2(m_ItemName, self.m_ItemText[s])
            m_Clr = self.m_BgColor
            if self.m_Itemselected[s]:
                m_Clr = self.m_SelColor
            g.SetBgColor_2(m_ItemName, m_Clr)
            s += 1
            i += 1
        while i < self.m_HeightInItems:
            m_ItemName = self.m_Name + '_IT(' + IntegerToString(i) + ')'
            g.SetText_2(m_ItemName, ' ')
            i += 1
    def Init(self, aName='CListMS', aWidth=100, aHeightInItems=8):
        self.m_Visible = False
        self.m_Name = aName
        self.m_Width = aWidth
        self.m_HeightInItems = aHeightInItems
        self.m_Left = 0
        self.m_Top = 0
        ArrayResize(self.m_ItemText, 0)
        ArrayResize(self.m_Itemselected, 0)
        self.m_BgColor = ClrScheme.Color(0)
        self.m_TxtColor = ClrScheme.Color(1)
        self.m_SelColor = ClrScheme.Color(14)
        self.m_Height = (self.m_HeightInItems * 14) + 1
        self.m_sb.Init(aName + '_SB', self.m_Height, 1)
        self.m_sb.SetMin(0)
        self.m_sb.SetValue(0)
        self.m_sb.SetSmallChange(1)
        self.m_sb.SetLageChange(aHeightInItems)
        self.m_SbVisible = False
        self.m_LastChanged = -1
        self.m_SearchFrom = 0
    def AddItem(self, aText):
        ArrayResize(self.m_ItemText, ArraySize(self.m_ItemText) + 1)
        self.m_ItemText[ArraySize(self.m_ItemText) - 1] = aText
        ArrayResize(self.m_Itemselected, ArraySize(self.m_Itemselected) + 1)
        self.m_Itemselected[ArraySize(self.m_Itemselected) - 1] = False
    def DeleteItem(self, aIndex):
        if aIndex < ArraySize(self.m_ItemText):
            for i in range(aIndex, ArraySize(self.m_ItemText) - 1):
                self.m_ItemText[i] = self.m_ItemText[i + 1]
                self.m_Itemselected[i] = self.m_Itemselected[i + 1]
            ArrayResize(self.m_ItemText, ArraySize(self.m_ItemText) - 1)
            ArrayResize(self.m_Itemselected, ArraySize(self.m_Itemselected) - 1)
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        if self.m_SbVisible:
            self.m_sb.Show_0()
        else:
            ChartRedraw(0)
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        if self.m_SbVisible:
            self.m_sb.Hide()
            self.m_SbVisible = False
        else:
            ChartRedraw(0)
    def Visible(self):
        return self.m_Visible
    def Refresh(self):
        if self.m_Visible:
            self.Hide()
            self.Show_0()
            ChartRedraw(0)
    def Count(self):
        return ArraySize(self.m_ItemText)
    def SetWidth(self, aValue):
        self.m_Width = aValue
    def SetHeightInItems(self, aValue):
        self.m_HeightInItems = aValue
        self.m_Height = (self.m_HeightInItems * 14) + 1
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Event(self, id_, lparam, dparam, sparam):
        m_event = 0
        if self.m_sb.Event(id_, lparam, dparam, sparam) == 1:
            self.PutValues()
            ChartRedraw()
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if StringFind(sparam, self.m_Name + '_IT(', 0) == 0:
                m_Pos1 = StringFind(sparam, '_IT(', 0)
                m_Pos2 = StringFind(sparam, ')', m_Pos1)
                m_Index = self.m_sb.Value() + _int(StringToInteger(StringSubstr(sparam, m_Pos1 + 4, m_Pos2 - m_Pos1 - 4)))
                self.SetSelected(m_Index, not self.Selected(m_Index))
                if self.Selected(m_Index):
                    m_event = 2
                else:
                    m_event = 1
        return m_event
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def ScrollTo(self, aValue):
        if ArraySize(self.m_ItemText) > self.m_HeightInItems:
            aValue = MathMin(ArraySize(self.m_ItemText) - self.m_HeightInItems, MathMax(0, aValue))
            self.m_sb.SetValue(aValue)
            if self.m_Visible:
                self.PutValues()
                ChartRedraw()
    def FirstIndex(self):
        return self.m_sb.Value()
    def Clear(self):
        ArrayResize(self.m_ItemText, 0)
        ArrayResize(self.m_Itemselected, 0)
    def SetTag(self, aValue):
        self.m_sb.SetTag(aValue)
    def Tag(self):
        return self.m_sb.Tag()
    def SetText(self, aIndex, aText):
        self.m_ItemText[aIndex] = aText
        if self.m_Visible:
            if aIndex >= self.m_sb.Value() and aIndex < (self.m_sb.Value() + self.m_HeightInItems):
                g.SetText_2(self.m_Name + '_IT(' + IntegerToString(aIndex - self.m_sb.Value()) + ')', aText)
                ChartRedraw()
    def Text(self, aIndex):
        return self.m_ItemText[aIndex]
    def SetSelected(self, aIndex, aSelected):
        if aIndex < 0 or aIndex >= ArraySize(self.m_Itemselected):
            return
        self.m_Itemselected[aIndex] = aSelected
        self.m_LastChanged = aIndex
        if self.m_Visible:
            if aIndex >= self.m_sb.Value() and aIndex < (self.m_sb.Value() + self.m_HeightInItems):
                m_Clr = self.m_BgColor
                if aSelected:
                    m_Clr = self.m_SelColor
                g.SetBgColor_2(self.m_Name + '_IT(' + IntegerToString(aIndex - self.m_sb.Value()) + ')', m_Clr)
                ChartRedraw()
    def Selected(self, aIndex):
        if aIndex >= 0 and aIndex < ArraySize(self.m_Itemselected):
            return self.m_Itemselected[aIndex]
        return False
    def LastChanged(self):
        return self.m_LastChanged
    def FirstSelected(self):
        self.m_SearchFrom = 0
        return self.NextSelected()
    def NextSelected(self):
        for i in range(self.m_SearchFrom, ArraySize(self.m_ItemText)):
            if self.m_Itemselected[i]:
                self.m_SearchFrom = i + 1
                return i
        return -1

class CComBox(MqlObject):
    _q_fields = ('m_Left', 'm_Top', 'm_Width', 'm_Visible', 'm_Value', 'm_SubWindow', 'm_NpCnt', 'm_ReadOnly', 'm_Name', 'm_NameEdit', 'm_NameButton', 'm_NameList', 'm_ExName', 'm_lst', 'm_BgColor', 'm_TxtColor', 'm_ButTxtColor', 'm_ButBgColor', 'm_FlashColor', 'm_WarningColor', 'm_Warning', 'm_NameLbl', 'm_Caption', 'm_LblColor')
    def __init__(self, *args):
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Visible = False
        self.m_Value = ""
        self.m_SubWindow = 0
        self.m_NpCnt = 0
        self.m_ReadOnly = False
        self.m_Name = ""
        self.m_NameEdit = ""
        self.m_NameButton = ""
        self.m_NameList = ""
        self.m_ExName = Arr(6, "", dyn=False)
        self.m_lst = CList()
        self.m_BgColor = 0
        self.m_TxtColor = 0
        self.m_ButTxtColor = 0
        self.m_ButBgColor = 0
        self.m_FlashColor = 0
        self.m_WarningColor = 0
        self.m_Warning = False
        self.m_NameLbl = ""
        self.m_Caption = ""
        self.m_LblColor = 0
    def Flash(self, aName, aFlash, aNormal):
        g.SetBgColor_2(aName, aFlash)
        g.Redraw_0()
        Sleep(100)
        g.SetBgColor_2(aName, aNormal)
        g.Redraw_0()
    def Create(self):
        m_tcol = self.m_BgColor
        if self.m_Warning:
            m_tcol = self.m_WarningColor
        w.Edit(self.m_NameEdit, self.m_SubWindow, self.m_Left, self.m_Top, self.m_Width - 12, 15, self.m_Value, m_tcol, self.m_TxtColor)
        g.Attach(self.m_NameEdit)
        g.SetReadOnly_1(self.m_ReadOnly)
        w.Edit(self.m_NameButton, self.m_SubWindow, self.m_Left + self.m_Width - 13, self.m_Top, 13, 15, ' /', self.m_ButBgColor, self.m_ButTxtColor, 6)
        g.SetReadOnly_2(self.m_NameButton, True)
        self.m_lst.SetSubWindow_1(self.m_SubWindow)
        m_center = _idiv(_int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, self.m_SubWindow)), 2)
        if (self.m_Top - 7) > m_center:
            self.m_lst.SetPos(self.m_Left, self.m_Top - self.m_lst.Height() + 1)
        else:
            self.m_lst.SetPos(self.m_Left, self.m_Top + 14)
        if self.m_Caption != '':
            w.Label(self.m_NameLbl, self.m_SubWindow, self.m_Left + self.m_Width + 1, self.m_Top + 2, self.m_Caption, self.m_LblColor, 7, 'Arial')
    def Delete(self):
        ObjectDelete(0, self.m_NameEdit)
        ObjectDelete(0, self.m_NameButton)
        ObjectDelete(0, self.m_NameLbl)
    def Init(self, aName='CComBox', aWidth=100, aCaption='CComBox'):
        self.m_Visible = False
        self.m_Width = aWidth
        self.m_Name = aName
        self.m_ReadOnly = True
        self.m_SubWindow = 0
        self.m_NpCnt = 0
        self.m_Warning = False
        self.m_NameEdit = self.m_Name + '_E'
        self.m_NameButton = self.m_Name + '_B'
        self.m_NameList = aName + '_Lst'
        self.m_NameLbl = aName + '_L'
        self.m_ExName[0] = self.m_Name + '_Lst_SB_LB'
        self.m_ExName[1] = self.m_Name + '_Lst_SB_UB'
        self.m_ExName[2] = self.m_Name + '_Lst_SB_S'
        self.m_ExName[3] = self.m_Name + '_Lst_SB_LF'
        self.m_ExName[4] = self.m_Name + '_Lst_SB_UF'
        self.m_ExName[5] = self.m_Name + '_B'
        self.m_Caption = aCaption
        self.m_lst.Init(self.m_NameList, aWidth, 1)
        self.m_lst.SetAllowDeselect(False)
        self.m_BgColor = ClrScheme.Color(0)
        self.m_TxtColor = ClrScheme.Color(1)
        self.m_ButTxtColor = ClrScheme.Color(1)
        self.m_ButBgColor = ClrScheme.Color(4)
        self.m_FlashColor = ClrScheme.Color(5)
        self.m_WarningColor = ClrScheme.Color(3)
        self.m_LblColor = ClrScheme.Color(2)
    def Clear(self):
        self.m_lst.Clear()
        self.m_lst.SetHeightInItems(1)
        self.m_Value = ''
    def AddItem(self, aItem):
        self.m_lst.AddItem(aItem)
        self.m_lst.SetHeightInItems(MathMin(8, self.m_lst.Count()))
    def DeleteItem(self, aIndex):
        self.m_lst.DeleteItem(aIndex)
        self.m_lst.SetHeightInItems(MathMin(8, self.m_lst.Count()))
    def Count(self):
        return self.m_lst.Count()
    def SetSelectedIndex(self, aIndex):
        self.m_lst.SetSelectedIndex(aIndex)
        self.m_lst.ScrollTo(aIndex)
        self.m_Value = self.m_lst.SelectedText()
        if self.m_Visible:
            g.SetText_2(self.m_NameEdit, self.m_Value)
            g.Redraw_0()
    def SetValue(self, aValue):
        i = 0
        while i < self.m_lst.Count():
            if aValue == self.m_lst.Text(i):
                self.SetSelectedIndex(i)
                return
            i += 1
        self.m_lst.SetSelectedIndex(-1)
        self.m_lst.ScrollTo(0)
        self.m_Value = aValue
        if self.m_Visible:
            g.SetText_2(self.m_NameEdit, self.m_Value)
            g.Redraw_0()
    def SetText(self, aIndex, aText):
        self.m_lst.SetText(aIndex, aText)
        if aIndex == self.m_lst.SelectedIndex():
            self.m_Value = aText
            if self.m_Visible:
                g.SetText_2(self.m_NameEdit, self.m_Value)
                g.Redraw_0()
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        ChartRedraw()
    def Show_2(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.Show_0()
    def Visible(self):
        return self.m_Visible
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        if self.m_lst.Visible():
            self.m_lst.Hide()
        else:
            ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.Create()
            self.m_lst.Hide()
            ChartRedraw()
    def SetReadOnly(self, aValue):
        self.m_ReadOnly = aValue
        if self.m_Visible:
            g.Attach(self.m_NameEdit)
            g.SetReadOnly_1(self.m_ReadOnly)
            g.Redraw_0()
    def ReadOnly(self):
        return self.m_ReadOnly
    def SelectedIndex(self):
        return self.m_lst.SelectedIndex()
    def SelectedText(self):
        return self.m_lst.SelectedText()
    def Value(self):
        return self.m_Value
    def Width(self):
        return self.m_Width
    def Height(self):
        return 15
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Event(self, id_, lparam, dparam, sparam):
        m_event = 0
        if sparam == '':
            self.m_NpCnt += 1
            if self.m_NpCnt > 1:
                self.m_lst.Hide()
        else:
            self.m_NpCnt = 0
            if self.m_lst.Event(id_, lparam, dparam, sparam) == 2:
                g.Attach(self.m_NameEdit)
                if self.m_lst.SelectedText() != g.Text_0():
                    m_event = 1
                    g.SetText_1(self.m_lst.SelectedText())
                    self.m_Value = g.Text_0()
                    g.Redraw_0()
                    Sleep(100)
            if id_ == CHARTEVENT_OBJECT_ENDEDIT:
                if sparam == self.m_NameEdit:
                    g.Attach(self.m_NameEdit)
                    if self.m_Value != g.Text_0():
                        m_event = 1
                        self.m_Value = g.Text_0()
                        self.m_lst.SetSelectedIndex(-1)
                        i = 0
                        while i < self.m_lst.Count():
                            if self.m_Value == self.m_lst.Text(i):
                                self.m_lst.SetSelectedIndex(i)
                                self.m_lst.ScrollTo(i)
                                break
                            i += 1
            if id_ == CHARTEVENT_OBJECT_CLICK:
                if sparam == self.m_NameButton:
                    self.Flash(self.m_NameButton, self.m_FlashColor, self.m_ButBgColor)
                    if self.m_lst.Visible():
                        self.m_lst.Hide()
                    else:
                        self.m_lst.Show_0()
            if not (((((sparam == self.m_ExName[0] or sparam == self.m_ExName[1]) or sparam == self.m_ExName[2]) or sparam == self.m_ExName[3]) or sparam == self.m_ExName[4]) or sparam == self.m_ExName[5]):
                if self.m_lst.Visible():
                    self.m_lst.Hide()
        return m_event
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_lst.SetTag(aValue)
    def Tag(self):
        return self.m_lst.Tag()
    def SetWarning(self, aValue):
        if self.m_Visible:
            if aValue:
                if not self.m_Warning:
                    g.Attach(self.m_NameEdit)
                    g.SetBgColor_1(self.m_WarningColor)
            else:
                if self.m_Warning:
                    g.Attach(self.m_NameEdit)
                    g.SetBgColor_1(self.m_BgColor)
        self.m_Warning = aValue
    def Warning(self):
        return self.m_Warning

class CHMenu(MqlObject):
    _q_fields = ('m_Visible', 'm_Name', 'm_Left', 'm_Top', 'm_Width', 'm_VisItems', 'm_DefVisItems', 'm_Start', 'm_Items', 'm_Checked', 'm_SubWindow', 'm_NameLBB', 'm_NameLBS', 'm_NameRBB', 'm_NameRBS', 'm_Tag', 'm_BgColorOn', 'm_BgColorOf', 'm_BgColor', 'm_TxtColor', 'm_ButTxtColor', 'm_ButBgColor', 'm_ButFlashColor', 'm_ItemFlashColor', 'm_WarningColor', 'm_CheckColor', 'm_CheckCnt', 'm_LastClickedX', 'm_LastClickedY', 'm_LastClickedQuarter', 'm_LastClickedW', 'm_LastClickedName1', 'm_LastClickedName2')
    def __init__(self, *args):
        self.m_Visible = False
        self.m_Name = ""
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_VisItems = 0
        self.m_DefVisItems = 0
        self.m_Start = 0
        self.m_Items = Arr(0, "")
        self.m_Checked = Arr(0, False)
        self.m_SubWindow = 0
        self.m_NameLBB = ""
        self.m_NameLBS = ""
        self.m_NameRBB = ""
        self.m_NameRBS = ""
        self.m_Tag = ""
        self.m_BgColorOn = 0
        self.m_BgColorOf = 0
        self.m_BgColor = 0
        self.m_TxtColor = 0
        self.m_ButTxtColor = 0
        self.m_ButBgColor = 0
        self.m_ButFlashColor = 0
        self.m_ItemFlashColor = 0
        self.m_WarningColor = 0
        self.m_CheckColor = 0
        self.m_CheckCnt = 0
        self.m_LastClickedX = 0
        self.m_LastClickedY = 0
        self.m_LastClickedQuarter = 0
        self.m_LastClickedW = 0
        self.m_LastClickedName1 = ""
        self.m_LastClickedName2 = ""
    def ScrollTo(self):
        if self.m_Visible:
            if ArraySize(self.m_Items) > 0:
                m_stri = ""
                i = 0
                while i < self.m_VisItems:
                    m_stri = IntegerToString(i)
                    g.Attach(self.m_Name + '_IT(' + m_stri + ')')
                    j = i + self.m_Start
                    if j < ArraySize(self.m_Items):
                        g.SetText_1('    ' + self.m_Items[j])
                    else:
                        g.SetText_1('')
                    g.Attach(self.m_Name + '_IC(' + m_stri + ')')
                    if self.m_Checked[j]:
                        g.SetText_1(CharToString(252))
                    else:
                        g.SetText_1(' ')
                    i += 1
    def Delete(self):
        m_stri = ""
        for i in range(0, self.m_VisItems):
            m_stri = IntegerToString(i)
            ObjectDelete(0, self.m_Name + '_IT(' + m_stri + ')')
            ObjectDelete(0, self.m_Name + '_IC(' + m_stri + ')')
        ObjectDelete(0, self.m_NameLBB)
        ObjectDelete(0, self.m_NameLBS)
        ObjectDelete(0, self.m_NameRBS)
        ObjectDelete(0, self.m_NameRBB)
    def DefineBgColor(self):
        if self.m_CheckCnt > 0:
            self.m_BgColor = self.m_BgColorOn
            self.m_ItemFlashColor = self.m_BgColorOf
        else:
            self.m_BgColor = self.m_BgColorOf
            self.m_ItemFlashColor = self.m_BgColorOn
    def SetBgColor(self):
        self.DefineBgColor()
        i = 0
        while i < self.m_VisItems:
            m_stri = IntegerToString(i)
            g.SetBgColor_2(self.m_Name + '_IT(' + m_stri + ')', self.m_BgColor)
            i += 1
    def Create(self):
        self.DefineBgColor()
        w.Edit(self.m_NameLBB, self.m_SubWindow, self.m_Left, self.m_Top, 9, 15, 'I', self.m_ButBgColor, self.m_ButTxtColor, 7, 'Arial')
        g.SetReadOnly_2(self.m_NameLBB, True)
        w.Edit(self.m_NameLBS, self.m_SubWindow, self.m_Left + 8, self.m_Top, 11, 15, '<', self.m_ButBgColor, self.m_ButTxtColor, 7, 'Arial')
        g.SetReadOnly_2(self.m_NameLBS, True)
        w.Edit(self.m_NameRBS, self.m_SubWindow, self.m_Left + self.m_Width - 19, self.m_Top, 11, 15, '>', self.m_ButBgColor, self.m_ButTxtColor, 7, 'Arial')
        g.SetReadOnly_2(self.m_NameRBS, True)
        w.Edit(self.m_NameRBB, self.m_SubWindow, self.m_Left + self.m_Width - 9, self.m_Top, 9, 15, 'I', self.m_ButBgColor, self.m_ButTxtColor, 7, 'Arial')
        g.SetReadOnly_2(self.m_NameRBB, True)
        m_tw = _idiv(self.m_Width - 40, self.m_VisItems)
        m_stri = ""
        m_z3 = 0
        i = 0
        while i < self.m_VisItems:
            m_z1 = _idiv(i * (self.m_Width - 40 + 2), self.m_VisItems)
            m_z2 = _idiv((i + 1) * (self.m_Width - 40 + 2), self.m_VisItems)
            m_stri = IntegerToString(i)
            m_z3 = self.m_Left + 18 + m_z1
            w.Edit(self.m_Name + '_IT(' + m_stri + ')', self.m_SubWindow, m_z3, self.m_Top, m_z2 - m_z1 + 1, 15, '', self.m_BgColor, self.m_TxtColor)
            g.SetReadOnly_2(self.m_Name + '_IT(' + m_stri + ')', True)
            w.Label(self.m_Name + '_IC(' + m_stri + ')', self.m_SubWindow, self.m_Left + 18 + m_z1 + 3, self.m_Top + 2, ' ', self.m_CheckColor, 9, 'Wingdings')
            i += 1
        if self.m_VisItems > 0:
            m_stri = IntegerToString(self.m_VisItems - 1)
            g.Attach(self.m_Name + '_IT(' + m_stri + ')')
            g.SetXSize_1(self.m_Left + self.m_Width - 18 - m_z3)
    def Flash(self, aName, aFlash, aNormal):
        g.SetBgColor_2(aName, aFlash)
        g.Redraw_0()
        Sleep(100)
        g.SetBgColor_2(aName, aNormal)
        g.Redraw_0()
    def Init(self, aName='CHMenu', aWidth=300, aVisibleItems=3):
        self.m_BgColorOn = ClrScheme.Color(15)
        self.m_BgColorOf = ClrScheme.Color(16)
        self.m_TxtColor = ClrScheme.Color(1)
        self.m_ButTxtColor = ClrScheme.Color(1)
        self.m_ButBgColor = ClrScheme.Color(4)
        self.m_ButFlashColor = ClrScheme.Color(5)
        self.m_WarningColor = ClrScheme.Color(3)
        self.m_CheckColor = ClrScheme.Color(17)
        self.m_BgColor = self.m_BgColorOf
        self.m_ItemFlashColor = self.m_BgColorOn
        self.m_SubWindow = 0
        self.m_Visible = False
        self.m_Name = aName
        self.m_NameLBB = self.m_Name + '_LBB'
        self.m_NameLBS = self.m_Name + '_LBS'
        self.m_NameRBB = self.m_Name + '_RBB'
        self.m_NameRBS = self.m_Name + '_RBS'
        self.m_Width = aWidth
        self.m_VisItems = aVisibleItems
        self.m_DefVisItems = aVisibleItems
        self.m_Start = 0
        ArrayResize(self.m_Items, 0)
        ArrayResize(self.m_Checked, 0)
        self.m_Tag = ''
        self.m_CheckCnt = 0
        self.m_LastClickedX = -1
        self.m_LastClickedY = -1
        self.m_LastClickedQuarter = -1
        self.m_LastClickedW = -1
        self.m_LastClickedName1 = ''
        self.m_LastClickedName2 = ''
    def AddItem(self, aItem, aChecked=False):
        ArrayResize(self.m_Items, ArraySize(self.m_Items) + 1)
        self.m_Items[ArraySize(self.m_Items) - 1] = aItem
        self.m_VisItems = MathMin(self.m_DefVisItems, ArraySize(self.m_Items))
        ArrayResize(self.m_Checked, ArraySize(self.m_Checked) + 1)
        self.m_Checked[ArraySize(self.m_Checked) - 1] = aChecked
        if aChecked:
            self.m_CheckCnt += 1
    def Show_2(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.Show_0()
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        self.ScrollTo()
        ChartRedraw()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.Show_0()
    def Visible(self):
        return self.m_Visible
    def SetChecked(self, aIndex, aValue):
        if self.m_Checked[aIndex] and (not aValue):
            self.m_CheckCnt -= 1
        if (not self.m_Checked[aIndex]) and aValue:
            self.m_CheckCnt += 1
        self.m_Checked[aIndex] = aValue
        if self.m_Visible:
            self.SetBgColor()
            m_n = aIndex - self.m_Start
            if m_n >= 0 and m_n < self.m_VisItems:
                g.Attach(self.m_Name + '_IC(' + IntegerToString(m_n) + ')')
                if aValue:
                    g.SetText_1(CharToString(252))
                else:
                    g.SetText_1(' ')
            ChartRedraw()
    def Checked(self, aIndex):
        return self.m_Checked[aIndex]
    def CheckedExist(self):
        return self.m_CheckCnt > 0
    def Text(self, aIndex):
        return self.m_Items[aIndex]
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Width(self):
        return self.m_Width
    def Height(self):
        return 15
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Event(self, id_, lparam, dparam, sparam):
        m_rv = -1
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if sparam == self.m_NameLBB:
                if self.m_Start > 0:
                    self.Flash(self.m_NameLBB, self.m_ButFlashColor, self.m_ButBgColor)
                    self.m_Start = 0
                    self.ScrollTo()
                    ChartRedraw()
                else:
                    self.Flash(self.m_NameLBB, self.m_WarningColor, self.m_ButBgColor)
            if sparam == self.m_NameLBS:
                if self.m_Start > 0:
                    self.Flash(self.m_NameLBS, self.m_ButFlashColor, self.m_ButBgColor)
                    self.m_Start -= self.m_VisItems
                    if self.m_Start < 0:
                        self.m_Start = 0
                    self.ScrollTo()
                    ChartRedraw()
                else:
                    self.Flash(self.m_NameLBS, self.m_WarningColor, self.m_ButBgColor)
            if sparam == self.m_NameRBB:
                if self.m_Start < (ArraySize(self.m_Items) - self.m_VisItems):
                    self.Flash(self.m_NameRBB, self.m_ButFlashColor, self.m_ButBgColor)
                    self.m_Start = ArraySize(self.m_Items) - self.m_VisItems
                    self.ScrollTo()
                    ChartRedraw()
                else:
                    self.Flash(self.m_NameRBB, self.m_WarningColor, self.m_ButBgColor)
            if sparam == self.m_NameRBS:
                if self.m_Start < (ArraySize(self.m_Items) - self.m_VisItems):
                    self.Flash(self.m_NameRBS, self.m_ButFlashColor, self.m_ButBgColor)
                    self.m_Start += self.m_VisItems
                    self.m_Start = MathMin(self.m_Start, ArraySize(self.m_Items) - self.m_VisItems)
                    self.ScrollTo()
                    ChartRedraw()
                else:
                    self.Flash(self.m_NameRBS, self.m_WarningColor, self.m_ButBgColor)
            if StringFind(sparam, self.m_Name + '_I', 0) == 0:
                m_pos = StringFind(sparam, '(', 0)
                m_oi = StringSubstr(sparam, m_pos + 1, StringLen(sparam) - m_pos - 2)
                self.m_LastClickedName1 = self.m_Name + '_IT(' + m_oi + ')'
                self.m_LastClickedName2 = self.m_Name + '_IC(' + m_oi + ')'
                m_index = self.m_Start + _int(StringToInteger(m_oi))
                g.Attach(self.m_LastClickedName1)
                self.m_LastClickedX = g.XDistance_0()
                self.m_LastClickedY = g.YDistance_0()
                self.m_LastClickedW = g.XSize_0()
                m_ocx = g.XDistance_0() + _idiv(g.XSize_0(), 2)
                m_ocy = g.YDistance_0() + _idiv(g.YSize_0(), 2)
                m_ccx = _idiv(_int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, self.m_SubWindow)), 2)
                m_ccy = _idiv(_int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, self.m_SubWindow)), 2)
                if m_ocy < m_ccy:
                    if m_ocx < m_ccx:
                        self.m_LastClickedQuarter = 1
                    else:
                        self.m_LastClickedQuarter = 2
                else:
                    if m_ocx < m_ccx:
                        self.m_LastClickedQuarter = 3
                    else:
                        self.m_LastClickedQuarter = 4
                self.Flash(self.m_LastClickedName1, self.m_ItemFlashColor, self.m_BgColor)
                return m_index
        return m_rv
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag
    def LastClickedX(self):
        return self.m_LastClickedX
    def LastClickedY(self):
        return self.m_LastClickedY
    def LastClickedQuarter(self):
        return self.m_LastClickedQuarter
    def LastClickedW(self):
        return self.m_LastClickedW
    def LastClickedName1(self):
        return self.m_LastClickedName1
    def LastClickedName2(self):
        return self.m_LastClickedName2
    def SolvePosLeft(self, aWidth):
        if self.m_LastClickedQuarter == 2 or self.m_LastClickedQuarter == 4:
            return self.m_LastClickedX + self.m_LastClickedW - aWidth
        return self.m_LastClickedX
    def SolvePosTop(self, aHeight):
        if self.m_LastClickedQuarter == 3 or self.m_LastClickedQuarter == 4:
            return self.m_LastClickedY - aHeight + 1
        return self.m_LastClickedY + self.Height() - 1

class CVMenu(MqlObject):
    _q_fields = ('m_ItemText', 'm_Checked', 'm_Name', 'm_Left', 'm_Top', 'm_Width', 'm_HeightInItems', 'm_DefHeightInItems', 'm_Start', 'm_sb', 'm_Visible', 'm_BgColorOn', 'm_BgColorOf', 'm_BgColor', 'm_TxtColor', 'm_ButTxtColor', 'm_ButBgColor', 'm_ButFlashColor', 'm_ItemFlashColor', 'm_WarningColor', 'm_CheckColor', 'm_SubWindow', 'm_CheckCnt', 'm_Tag', 'm_LastClickedX', 'm_LastClickedY', 'm_LastClickedQuarter', 'm_NpCnt', 'm_ExName', 'm_LastClickedName1', 'm_LastClickedName2')
    def __init__(self, *args):
        self.m_ItemText = Arr(0, "")
        self.m_Checked = Arr(0, False)
        self.m_Name = ""
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_HeightInItems = 0
        self.m_DefHeightInItems = 0
        self.m_Start = 0
        self.m_sb = CVScrollBar()
        self.m_Visible = False
        self.m_BgColorOn = 0
        self.m_BgColorOf = 0
        self.m_BgColor = 0
        self.m_TxtColor = 0
        self.m_ButTxtColor = 0
        self.m_ButBgColor = 0
        self.m_ButFlashColor = 0
        self.m_ItemFlashColor = 0
        self.m_WarningColor = 0
        self.m_CheckColor = 0
        self.m_SubWindow = 0
        self.m_CheckCnt = 0
        self.m_Tag = ""
        self.m_LastClickedX = 0
        self.m_LastClickedY = 0
        self.m_LastClickedQuarter = 0
        self.m_NpCnt = 0
        self.m_ExName = Arr(0, "")
        self.m_LastClickedName1 = ""
        self.m_LastClickedName2 = ""
    def ScrollTo(self):
        i = 0
        while i < self.m_HeightInItems:
            j = self.m_Start + i
            if j < ArraySize(self.m_ItemText):
                g.Attach(self.m_Name + '_IT(' + IntegerToString(i) + ')')
                g.SetText_1('    ' + self.m_ItemText[j])
                m_chtxt = ' '
                if self.m_Checked[j]:
                    m_chtxt = CharToString(252)
                g.Attach(self.m_Name + '_IC(' + IntegerToString(i) + ')')
                g.SetText_1(m_chtxt)
            else:
                g.Attach(self.m_Name + '_IT(' + IntegerToString(i) + ')')
                g.SetText_1(' ')
                g.Attach(self.m_Name + '_IC(' + IntegerToString(i) + ')')
                g.SetText_1(' ')
            i += 1
    def DefineBgColor(self):
        if self.m_CheckCnt > 0:
            self.m_BgColor = self.m_BgColorOn
            self.m_ItemFlashColor = self.m_BgColorOf
        else:
            self.m_BgColor = self.m_BgColorOf
            self.m_ItemFlashColor = self.m_BgColorOn
    def SetBgColor(self):
        self.DefineBgColor()
        i = 0
        while i < self.m_HeightInItems:
            m_stri = IntegerToString(i)
            g.SetBgColor_2(self.m_Name + '_IT(' + m_stri + ')', self.m_BgColor)
            i += 1
    def Create(self):
        self.m_NpCnt = 0
        self.DefineBgColor()
        m_w = self.m_Width
        if ArraySize(self.m_ItemText) > self.m_HeightInItems:
            m_w = self.m_Width - self.m_sb.Width()
            self.m_sb.Show_2(self.m_Left + m_w, self.m_Top)
            m_w += 1
        i = 0
        while i < self.m_HeightInItems:
            w.Edit(self.m_Name + '_IT(' + IntegerToString(i) + ')', self.m_SubWindow, self.m_Left, self.m_Top + (i * 14), m_w, 15, ' ', self.m_BgColor, self.m_TxtColor, 7, 'Arial')
            g.SetReadOnly_2(self.m_Name + '_IT(' + IntegerToString(i) + ')', True)
            w.Label(self.m_Name + '_IC(' + IntegerToString(i) + ')', self.m_SubWindow, self.m_Left + 3, self.m_Top + (i * 14) + 2, ' ', self.m_CheckColor, 9, 'Wingdings')
            i += 1
        self.m_sb.SetSubWindow_1(self.m_SubWindow)
    def Delete(self):
        for i in range(0, self.m_HeightInItems):
            ObjectDelete(0, self.m_Name + '_IT(' + IntegerToString(i) + ')')
            ObjectDelete(0, self.m_Name + '_IC(' + IntegerToString(i) + ')')
    def Flash(self, aName, aFlash, aNormal):
        g.SetBgColor_2(aName, aFlash)
        g.Redraw_0()
        Sleep(100)
        g.SetBgColor_2(aName, aNormal)
        g.Redraw_0()
    def Init(self, aName='CVMenu', aWidth=100, aVisibleItems=10):
        self.m_BgColorOn = ClrScheme.Color(15)
        self.m_BgColorOf = ClrScheme.Color(16)
        self.m_TxtColor = ClrScheme.Color(1)
        self.m_ButTxtColor = ClrScheme.Color(1)
        self.m_ButBgColor = ClrScheme.Color(4)
        self.m_ButFlashColor = ClrScheme.Color(5)
        self.m_WarningColor = ClrScheme.Color(3)
        self.m_CheckColor = ClrScheme.Color(17)
        self.m_SubWindow = 0
        self.m_CheckCnt = 0
        self.m_Visible = False
        self.m_Name = aName
        self.m_Width = aWidth
        self.m_HeightInItems = aVisibleItems
        self.m_DefHeightInItems = aVisibleItems
        self.m_Left = 0
        self.m_Top = 0
        self.m_Start = 0
        ArrayResize(self.m_ItemText, 0)
        ArrayResize(self.m_Checked, 0)
        self.m_sb.Init(aName + '_SB', (aVisibleItems * 14) + 1, 1)
        self.m_sb.SetMin(0)
        self.m_sb.SetValue(0)
        self.m_sb.SetSmallChange(1)
        self.m_sb.SetLageChange(aVisibleItems)
        self.m_Tag = ''
        self.m_LastClickedX = -1
        self.m_LastClickedY = -1
        self.m_LastClickedQuarter = -1
        self.m_NpCnt = 0
        ArrayResize(self.m_ExName, 0)
        self.m_LastClickedName1 = ''
        self.m_LastClickedName2 = ''
    def ToggleNameAdd(self, aValue):
        ArrayResize(self.m_ExName, ArraySize(self.m_ExName) + 1)
        self.m_ExName[ArraySize(self.m_ExName) - 1] = aValue
    def ToggleNamesClear(self):
        ArrayResize(self.m_ExName, 0)
    def AddItem(self, aText, aChecked=False):
        ArrayResize(self.m_ItemText, ArraySize(self.m_ItemText) + 1)
        self.m_ItemText[ArraySize(self.m_ItemText) - 1] = aText
        ArrayResize(self.m_Checked, ArraySize(self.m_Checked) + 1)
        self.m_Checked[ArraySize(self.m_Checked) - 1] = aChecked
        self.m_HeightInItems = MathMin(self.m_DefHeightInItems, ArraySize(self.m_ItemText))
        if ArraySize(self.m_ItemText) > self.m_HeightInItems:
            self.m_sb.SetMax(ArraySize(self.m_ItemText) - self.m_HeightInItems)
        if aChecked:
            self.m_CheckCnt += 1
    def Show_2(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.Show_0()
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        self.ScrollTo()
        ChartRedraw(0)
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        if self.m_sb.Visible():
            self.m_sb.Hide()
        else:
            ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            if self.m_sb.Visible():
                self.m_sb.Hide()
            self.Show_0()
    def Visible(self):
        return self.m_Visible
    def SetChecked(self, aIndex, aValue):
        if self.m_Checked[aIndex] and (not aValue):
            self.m_CheckCnt -= 1
        if (not self.m_Checked[aIndex]) and aValue:
            self.m_CheckCnt += 1
        self.m_Checked[aIndex] = aValue
        if self.m_Visible:
            self.SetBgColor()
            m_n = aIndex - self.m_Start
            if m_n >= 0 and m_n < self.m_HeightInItems:
                g.Attach(self.m_Name + '_IC(' + IntegerToString(m_n) + ')')
                if aValue:
                    g.SetText_1(CharToString(252))
                else:
                    g.SetText_1(' ')
            ChartRedraw()
    def Checked(self, aIndex):
        return self.m_Checked[aIndex]
    def CheckedExist(self):
        return self.m_CheckCnt > 0
    def Text(self, aIndex):
        return self.m_ItemText[aIndex]
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Width(self):
        return self.m_Width
    def Height(self):
        return (self.m_HeightInItems * 14) + 1
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Event(self, id_, lparam, dparam, sparam):
        if self.m_sb.Event(id_, lparam, dparam, sparam) == 1:
            self.m_Start = self.m_sb.Value()
            self.ScrollTo()
            ChartRedraw()
            self.m_NpCnt = 0
            return -1
        if (((sparam == (self.m_Name + '_SB_LB') or sparam == (self.m_Name + '_SB_UB')) or sparam == (self.m_Name + '_SB_S')) or sparam == (self.m_Name + '_SB_LF')) or sparam == (self.m_Name + '_SB_UF'):
            self.m_NpCnt = 0
            return -1
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if StringFind(sparam, self.m_Name + '_I', 0) == 0:
                self.m_NpCnt = 0
                m_pos = StringFind(sparam, '(', 0)
                m_oi = StringSubstr(sparam, m_pos + 1, StringLen(sparam) - m_pos - 2)
                m_index = self.m_Start + _int(StringToInteger(m_oi))
                self.m_LastClickedName1 = self.m_Name + '_IT(' + m_oi + ')'
                self.m_LastClickedName2 = self.m_Name + '_IC(' + m_oi + ')'
                g.Attach(self.m_LastClickedName1)
                self.m_LastClickedX = g.XDistance_0()
                self.m_LastClickedY = g.YDistance_0()
                m_ocx = g.XDistance_0() + _idiv(g.XSize_0(), 2)
                m_ocy = g.YDistance_0() + _idiv(g.YSize_0(), 2)
                m_ccx = _idiv(_int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, self.m_SubWindow)), 2)
                m_ccy = _idiv(_int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, self.m_SubWindow)), 2)
                if m_ocy < m_ccy:
                    if m_ocx < m_ccx:
                        self.m_LastClickedQuarter = 1
                    else:
                        self.m_LastClickedQuarter = 2
                else:
                    if m_ocx < m_ccx:
                        self.m_LastClickedQuarter = 3
                    else:
                        self.m_LastClickedQuarter = 4
                self.Flash(self.m_LastClickedName1, self.m_ItemFlashColor, self.m_BgColor)
                return m_index
        self.m_NpCnt += 1
        if ArraySize(self.m_ExName) == 0:
            self.m_NpCnt = 0
        else:
            for i in range(0, ArraySize(self.m_ExName)):
                if sparam == self.m_ExName[i]:
                    self.m_NpCnt = 0
                    break
        if self.m_NpCnt > 1:
            self.m_NpCnt = 0
            self.Hide()
        return -1
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.m_sb.SetSubWindow_1(self.m_SubWindow)
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag
    def LastClickedX(self):
        return self.m_LastClickedX
    def LastClickedY(self):
        return self.m_LastClickedY
    def LastClickedQuarter(self):
        return self.m_LastClickedQuarter
    def LastClickedName1(self):
        return self.m_LastClickedName1
    def LastClickedName2(self):
        return self.m_LastClickedName2
    def ItemHeight(self):
        return 15
    def SolvePosLeft(self, aWidth):
        if self.m_LastClickedQuarter == 2 or self.m_LastClickedQuarter == 4:
            return self.m_LastClickedX - aWidth + 1
        return self.m_LastClickedX + self.Width() - 1
    def SolvePosTop(self, aHeight):
        if self.m_LastClickedQuarter == 3 or self.m_LastClickedQuarter == 4:
            return self.m_LastClickedY + self.ItemHeight() - aHeight
        return self.m_LastClickedY

class CHProgress(MqlObject):
    _q_fields = ('m_Started', 'm_Name', 'm_NameC1', 'm_NameC2', 'm_NameL1', 'm_NameL2', 'm_Left', 'm_Top', 'm_Width', 'm_Height', 'm_Min', 'm_Max', 'm_Value', 'm_Digits', 'm_Visible', 'm_Len', 'm_St', 'm_Add', 'm_RefreshInterval', 'm_LastTime', 'm_BgColor', 'm_BorderColor', 'm_ProgrColor', 'm_TxtColor', 'm_SubWindow', 'm_Tag')
    def __init__(self, *args):
        self.m_Started = False
        self.m_Name = ""
        self.m_NameC1 = ""
        self.m_NameC2 = ""
        self.m_NameL1 = ""
        self.m_NameL2 = ""
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_Min = 0.0
        self.m_Max = 0.0
        self.m_Value = 0.0
        self.m_Digits = 0
        self.m_Visible = False
        self.m_Len = 0
        self.m_St = 0
        self.m_Add = 0
        self.m_RefreshInterval = 0
        self.m_LastTime = 0
        self.m_BgColor = 0
        self.m_BorderColor = 0
        self.m_ProgrColor = 0
        self.m_TxtColor = 0
        self.m_SubWindow = 0
        self.m_Tag = ""
    def FormatSec(self, aSec):
        m_rs = ''
        m_h = _idiv(aSec, 3600)
        aSec -= m_h * 3600
        m_m = _idiv(aSec, 60)
        aSec -= m_m * 60
        if m_h > 0:
            if m_h < 10:
                m_rs = '0' + IntegerToString(m_h) + ':'
            else:
                m_rs = IntegerToString(m_h) + ':'
        if m_m < 10:
            m_rs = m_rs + '0' + IntegerToString(m_m) + ':'
        else:
            m_rs = m_rs + IntegerToString(m_m) + ':'
        if aSec < 10:
            m_rs = m_rs + '0' + IntegerToString(aSec)
        else:
            m_rs = m_rs + IntegerToString(aSec)
        return m_rs
    def Labels(self):
        m_done = _fdiv(self.m_Value - self.m_Min, self.m_Max - self.m_Min)
        self.m_Len = _int(MathRound(m_done * (self.m_Width - 2)))
        g.Attach(self.m_NameC2)
        g.SetXSize_1(self.m_Len)
        g.Attach(self.m_NameL1)
        g.SetText_1(DoubleToString(m_done * 100.0, 2) + '%')
        if self.m_Started:
            m_tcn = GetTickCount()
            m_tms = 0
            if m_tcn < self.m_St:
                self.m_Add = ULONG_MAX - self.m_St
                self.m_St = 0
            m_tms = self.m_Add + (m_tcn - self.m_St)
            m_lt = 0
            if m_done > 0:
                m_lt = _int(MathRound(1.0 + _fdiv(0.001 * m_tms * (1.0 - m_done), m_done)))
            g.Attach(self.m_NameL2)
            g.SetText_1(self.FormatSec(m_lt))
    def Create(self):
        w.Edit(self.m_NameC1, self.m_SubWindow, self.m_Left, self.m_Top, self.m_Width, self.m_Height, ' ', self.m_BgColor, self.m_BorderColor)
        g.SetReadOnly_2(self.m_NameC1, True)
        w.Edit(self.m_NameC2, self.m_SubWindow, self.m_Left + 1, self.m_Top + 1, self.m_Len, self.m_Height - 2, ' ', self.m_ProgrColor, self.m_ProgrColor)
        g.SetReadOnly_2(self.m_NameC2, True)
        w.Label(self.m_NameL1, self.m_SubWindow, self.m_Left + 4, self.m_Top + 2, ' ', self.m_TxtColor, 7)
        w.Label(self.m_NameL2, self.m_SubWindow, self.m_Left + self.m_Width - 4, self.m_Top + 2, ' ', self.m_TxtColor, 7)
        g.SetAnchor_2(self.m_NameL2, ANCHOR_RIGHT_UPPER)
    def Delete(self):
        g.Delete_1(self.m_NameC1)
        g.Delete_1(self.m_NameC2)
        g.Delete_1(self.m_NameL1)
        g.Delete_1(self.m_NameL2)
    def Init(self, aName='CHProgress', aWidth=200):
        self.m_Name = aName
        self.m_NameC1 = self.m_Name + '_C1'
        self.m_NameC2 = self.m_Name + '_C2'
        self.m_NameL1 = self.m_Name + '_L1'
        self.m_NameL2 = self.m_Name + '_L2'
        self.m_Visible = False
        self.m_Name = aName
        self.m_Min = 0.0
        self.m_Max = 100.0
        self.m_Width = aWidth
        self.m_Height = 15
        self.m_Value = 0.0
        self.m_Len = 0
        self.m_RefreshInterval = 0
        self.m_BgColor = ClrScheme.Color(18)
        self.m_BorderColor = ClrScheme.Color(19)
        self.m_ProgrColor = ClrScheme.Color(20)
        self.m_TxtColor = ClrScheme.Color(21)
        self.m_SubWindow = 0
        self.m_Tag = ''
    def SetRefreshInterval(self, aSeconds):
        self.m_RefreshInterval = aSeconds
    def SetWidth(self, aWidth):
        self.m_Width = aWidth
    def Refersh(self):
        if self.m_Visible:
            self.Hide()
            self.Show_0()
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Width(self):
        return self.m_Width
    def Height(self):
        return 15
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Show_2(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.Show_0()
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        ChartRedraw()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.Show_0()
    def Begin(self, aMin=0.0, aMax=100.0):
        self.Reset()
        self.m_Started = True
        self.m_Min = aMin
        self.m_Max = aMax
        self.m_St = GetTickCount()
        self.m_Add = 0
        self.m_Value = self.m_Min
    def Reset(self):
        self.m_Started = False
        self.m_Value = self.m_Min
        if self.m_Visible:
            g.SetXSize_2(self.m_NameC2, 0)
            g.SetText_2(self.m_NameL1, ' ')
            g.SetText_2(self.m_NameL2, ' ')
            g.Redraw_0()
    def SetValue(self, aValue):
        self.m_Value = aValue
        if TimeLocal() < (self.m_LastTime + self.m_RefreshInterval):
            return
        self.m_LastTime = TimeLocal()
        if self.m_Visible:
            self.Labels()
            ChartRedraw()
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag

class CDialer(MqlObject):
    _q_fields = ('m_NameFrame', 'm_Name1', 'm_Name2', 'm_Name3', 'm_Name4', 'm_Name5', 'm_Name6', 'm_Name7', 'm_Name8', 'm_Name9', 'm_Name0', 'm_NameD', 'm_NameX', 'm_NameC', 'm_NameE', 'm_NameT', 'm_NameM', 'm_ButtonSize', 'm_TextSize', 'm_Left', 'm_Top', 'm_BGColor', 'm_BorderColor', 'm_ButDigTxColor', 'm_ButDigBgColor', 'm_ButDigCtrlBgColor', 'm_ButDigOkBgColor', 'm_ButDigClColor', 'm_TxBgColor', 'm_TxTxColor', 'm_WrongFlashColor', 'm_Visible', 'm_Width', 'm_Height', 'm_Value', 'm_Tag', 'm_SubWindow')
    def __init__(self, *args):
        self.m_NameFrame = ""
        self.m_Name1 = ""
        self.m_Name2 = ""
        self.m_Name3 = ""
        self.m_Name4 = ""
        self.m_Name5 = ""
        self.m_Name6 = ""
        self.m_Name7 = ""
        self.m_Name8 = ""
        self.m_Name9 = ""
        self.m_Name0 = ""
        self.m_NameD = ""
        self.m_NameX = ""
        self.m_NameC = ""
        self.m_NameE = ""
        self.m_NameT = ""
        self.m_NameM = ""
        self.m_ButtonSize = 0
        self.m_TextSize = 0
        self.m_Left = 0
        self.m_Top = 0
        self.m_BGColor = 0
        self.m_BorderColor = 0
        self.m_ButDigTxColor = 0
        self.m_ButDigBgColor = 0
        self.m_ButDigCtrlBgColor = 0
        self.m_ButDigOkBgColor = 0
        self.m_ButDigClColor = 0
        self.m_TxBgColor = 0
        self.m_TxTxColor = 0
        self.m_WrongFlashColor = 0
        self.m_Visible = False
        self.m_Width = 0
        self.m_Height = 0
        self.m_Value = 0.0
        self.m_Tag = ""
        self.m_SubWindow = 0
    def Flash(self, aName, aColor):
        g.Attach(aName)
        restc = g.BgColor_0()
        g.SetBgColor_1(aColor)
        g.Redraw_0()
        Sleep(100)
        g.SetBgColor_1(restc)
        g.Redraw_0()
    def Push(self, aName):
        g.Attach(aName)
        m_x = g.XDistance_0()
        m_y = g.YDistance_0()
        g.SetXDistance_1(m_x + 1)
        g.SetYDistance_1(m_y + 1)
        g.Redraw_0()
        Sleep(100)
        g.SetXDistance_1(m_x)
        g.SetYDistance_1(m_y)
        g.Redraw_0()
    def Create(self):
        w.Edit(self.m_NameFrame, self.m_SubWindow, self.m_Left, self.m_Top, self.m_Width, self.m_Height, ' ', self.m_BGColor, self.m_BorderColor)
        w.Edit(self.m_Name7, self.m_SubWindow, self.m_Left + 2, self.m_Top + 2, self.m_ButtonSize, self.m_ButtonSize, ' 7', self.m_ButDigBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_Name8, self.m_SubWindow, self.m_Left + self.m_ButtonSize + 4, self.m_Top + 2, self.m_ButtonSize, self.m_ButtonSize, ' 8', self.m_ButDigBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_Name9, self.m_SubWindow, self.m_Left + 6 + (self.m_ButtonSize * 2), self.m_Top + 2, self.m_ButtonSize, self.m_ButtonSize, ' 9', self.m_ButDigBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_Name4, self.m_SubWindow, self.m_Left + 2, self.m_Top + 4 + self.m_ButtonSize, self.m_ButtonSize, self.m_ButtonSize, ' 4', self.m_ButDigBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_Name5, self.m_SubWindow, self.m_Left + 4 + self.m_ButtonSize, self.m_Top + 4 + self.m_ButtonSize, self.m_ButtonSize, self.m_ButtonSize, ' 5', self.m_ButDigBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_Name6, self.m_SubWindow, self.m_Left + 6 + (2 * self.m_ButtonSize), self.m_Top + 4 + self.m_ButtonSize, self.m_ButtonSize, self.m_ButtonSize, ' 6', self.m_ButDigBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_Name1, self.m_SubWindow, self.m_Left + 2, self.m_Top + 6 + (2 * self.m_ButtonSize), self.m_ButtonSize, self.m_ButtonSize, ' 1', self.m_ButDigBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_Name2, self.m_SubWindow, self.m_Left + 4 + self.m_ButtonSize, self.m_Top + 6 + (2 * self.m_ButtonSize), self.m_ButtonSize, self.m_ButtonSize, ' 2', self.m_ButDigBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_Name3, self.m_SubWindow, self.m_Left + 6 + (2 * self.m_ButtonSize), self.m_Top + 6 + (2 * self.m_ButtonSize), self.m_ButtonSize, self.m_ButtonSize, ' 3', self.m_ButDigBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_Name0, self.m_SubWindow, self.m_Left + 2, self.m_Top + 8 + (3 * self.m_ButtonSize), (2 * self.m_ButtonSize) + 2, self.m_ButtonSize, ' 0', self.m_ButDigBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_NameD, self.m_SubWindow, self.m_Left + 6 + (2 * self.m_ButtonSize), self.m_Top + 8 + (3 * self.m_ButtonSize), self.m_ButtonSize, self.m_ButtonSize, "    '", self.m_ButDigBgColor, self.m_ButDigTxColor, 5)
        w.Edit(self.m_NameX, self.m_SubWindow, self.m_Left + 8 + (3 * self.m_ButtonSize), self.m_Top + 2, self.m_ButtonSize, self.m_ButtonSize, ' X', self.m_ButDigClColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_NameC, self.m_SubWindow, self.m_Left + 8 + (3 * self.m_ButtonSize), self.m_Top + 4 + self.m_ButtonSize, self.m_ButtonSize, self.m_ButtonSize, ' C', self.m_ButDigCtrlBgColor, self.m_ButDigTxColor, 8)
        w.Edit(self.m_NameM, self.m_SubWindow, self.m_Left + 8 + (3 * self.m_ButtonSize), self.m_Top + 6 + (2 * self.m_ButtonSize), self.m_ButtonSize, self.m_ButtonSize, ' -', self.m_ButDigBgColor, self.m_ButDigTxColor, 10)
        w.Edit(self.m_NameE, self.m_SubWindow, self.m_Left + 8 + (3 * self.m_ButtonSize), self.m_Top + 8 + (3 * self.m_ButtonSize), self.m_ButtonSize, self.m_ButtonSize, 'OK', self.m_ButDigOkBgColor, self.m_ButDigTxColor, 7)
        w.Edit(self.m_NameT, self.m_SubWindow, self.m_Left + 2, self.m_Top + 10 + (4 * self.m_ButtonSize), (4 * self.m_ButtonSize) + 6, self.m_TextSize, '', self.m_TxBgColor, self.m_TxTxColor, 7)
        g.SetReadOnly_2(self.m_NameFrame, True)
        g.SetReadOnly_2(self.m_Name7, True)
        g.SetReadOnly_2(self.m_Name8, True)
        g.SetReadOnly_2(self.m_Name9, True)
        g.SetReadOnly_2(self.m_Name4, True)
        g.SetReadOnly_2(self.m_Name5, True)
        g.SetReadOnly_2(self.m_Name6, True)
        g.SetReadOnly_2(self.m_Name1, True)
        g.SetReadOnly_2(self.m_Name2, True)
        g.SetReadOnly_2(self.m_Name3, True)
        g.SetReadOnly_2(self.m_Name0, True)
        g.SetReadOnly_2(self.m_NameD, True)
        g.SetReadOnly_2(self.m_NameX, True)
        g.SetReadOnly_2(self.m_NameC, True)
        g.SetReadOnly_2(self.m_NameM, True)
        g.SetReadOnly_2(self.m_NameE, True)
        g.SetReadOnly_2(self.m_NameT, True)
    def Delete(self):
        g.Delete_1(self.m_NameFrame)
        g.Delete_1(self.m_Name1)
        g.Delete_1(self.m_Name2)
        g.Delete_1(self.m_Name3)
        g.Delete_1(self.m_Name4)
        g.Delete_1(self.m_Name5)
        g.Delete_1(self.m_Name6)
        g.Delete_1(self.m_Name7)
        g.Delete_1(self.m_Name8)
        g.Delete_1(self.m_Name9)
        g.Delete_1(self.m_Name0)
        g.Delete_1(self.m_NameD)
        g.Delete_1(self.m_NameX)
        g.Delete_1(self.m_NameC)
        g.Delete_1(self.m_NameE)
        g.Delete_1(self.m_NameT)
        g.Delete_1(self.m_NameM)
    def Init(self, aName='CDialer'):
        self.m_NameFrame = aName + '_Frame'
        self.m_Name1 = aName + '_B1'
        self.m_Name2 = aName + '_B2'
        self.m_Name3 = aName + '_B3'
        self.m_Name4 = aName + '_B4'
        self.m_Name5 = aName + '_B5'
        self.m_Name6 = aName + '_B6'
        self.m_Name7 = aName + '_B7'
        self.m_Name8 = aName + '_B8'
        self.m_Name9 = aName + '_B9'
        self.m_Name0 = aName + '_B0'
        self.m_NameD = aName + '_BD'
        self.m_NameX = aName + '_BX'
        self.m_NameC = aName + '_BC'
        self.m_NameE = aName + '_BE'
        self.m_NameT = aName + '_T'
        self.m_NameM = aName + '_M'
        self.m_ButtonSize = 20
        self.m_TextSize = 15
        self.m_BGColor = ClrScheme.Color(22)
        self.m_BorderColor = ClrScheme.Color(23)
        self.m_ButDigBgColor = ClrScheme.Color(24)
        self.m_ButDigTxColor = ClrScheme.Color(25)
        self.m_ButDigCtrlBgColor = ClrScheme.Color(26)
        self.m_ButDigOkBgColor = ClrScheme.Color(27)
        self.m_ButDigClColor = ClrScheme.Color(28)
        self.m_TxBgColor = ClrScheme.Color(29)
        self.m_TxTxColor = ClrScheme.Color(30)
        self.m_WrongFlashColor = ClrScheme.Color(31)
        self.m_Width = (4 * self.m_ButtonSize) + 10
        self.m_Height = (4 * self.m_ButtonSize) + 12 + self.m_TextSize
        self.m_Visible = False
        self.m_SubWindow = 0
    def SetTag(self, aTag):
        self.m_Tag = aTag
    def Tag(self):
        return self.m_Tag
    def Show_2(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.Show_0()
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        ChartRedraw()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.Show_0()
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Visible(self):
        return self.m_Visible
    def Value(self):
        return self.m_Value
    def Event(self, id_, lparam, dparam, sparam):
        m_rv = 0
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if sparam == self.m_Name1:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1(g.Text_0() + '1')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_Name2:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1(g.Text_0() + '2')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_Name3:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1(g.Text_0() + '3')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_Name4:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1(g.Text_0() + '4')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_Name5:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1(g.Text_0() + '5')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_Name6:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1(g.Text_0() + '6')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_Name7:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1(g.Text_0() + '7')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_Name8:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1(g.Text_0() + '8')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_Name9:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1(g.Text_0() + '9')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_Name0:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1(g.Text_0() + '0')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_NameD:
                g.Attach(self.m_NameT)
                if StringFind(g.Text_0(), '.', 0) == -1:
                    self.Push(sparam)
                    g.Attach(self.m_NameT)
                    if g.Text_0() == '' or g.Text_0() == '-':
                        g.SetText_1(g.Text_0() + '0')
                    g.SetText_1(g.Text_0() + '.')
                    g.Redraw_0()
                else:
                    self.Flash(sparam, self.m_WrongFlashColor)
                m_rv = 2
            if sparam == self.m_NameX:
                self.Push(sparam)
                self.Hide()
                m_rv = 2
            if sparam == self.m_NameC:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                g.SetText_1('')
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_NameE:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                sVal = g.Text_0()
                self.m_Value = StringToDouble(sVal)
                self.Hide()
                m_rv = 1
            if sparam == self.m_NameM:
                self.Push(sparam)
                g.Attach(self.m_NameT)
                if StringSubstr(g.Text_0(), 0, 1) == '-':
                    g.SetText_1(StringSubstr(g.Text_0(), 1, StringLen(g.Text_0()) - 1))
                else:
                    g.SetText_1('-' + g.Text_0())
                g.Redraw_0()
                m_rv = 2
            if sparam == self.m_NameFrame:
                m_rv = 2
            if sparam == self.m_NameT:
                m_rv = 2
        return m_rv
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))

class CDialerInputBox(MqlObject):
    _q_fields = ('m_SubWindow', 'm_Left', 'm_Top', 'm_Width', 'm_Height', 'm_DName', 'm_IName', 'm_BName', 'm_LName', 'm_Caption', 'm_d', 'm_ib', 'm_ColDBg', 'm_ColDTx', 'm_ColL', 'm_cc', 'm_Visible', 'm_Tag')
    def __init__(self, *args):
        self.m_SubWindow = 0
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_DName = ""
        self.m_IName = ""
        self.m_BName = ""
        self.m_LName = ""
        self.m_Caption = ""
        self.m_d = CDialer()
        self.m_ib = CInputBox()
        self.m_ColDBg = 0
        self.m_ColDTx = 0
        self.m_ColL = 0
        self.m_cc = 0
        self.m_Visible = False
        self.m_Tag = ""
    def Create(self):
        w.Edit(self.m_BName, self.m_SubWindow, self.m_Left + self.m_Width - 13, self.m_Top, 13, self.m_Height, 'd', self.m_ColDBg, self.m_ColDTx, 7, 'Arial')
        g.SetReadOnly_2(self.m_BName, True)
        if self.m_Caption != '':
            w.Label(self.m_LName, self.m_SubWindow, self.m_Left + self.m_Width + 1, self.m_Top + 2, self.m_Caption, self.m_ColL, 7, 'Arial')
    def Delete(self):
        ObjectDelete(0, self.m_BName)
        ObjectDelete(0, self.m_LName)
    def Init(self, aName='CDialerInputBox', aWidth=50, aDigits=4, aCaption='CDialerInputBox'):
        self.m_ColDBg = ClrScheme.Color(4)
        self.m_ColDTx = ClrScheme.Color(1)
        self.m_ColL = ClrScheme.Color(2)
        self.m_Visible = False
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = aWidth
        self.m_Height = 15
        self.m_Caption = aCaption
        self.m_DName = aName + '_D'
        self.m_IName = aName + '_I'
        self.m_BName = aName + '_B'
        self.m_LName = aName + '_L'
        self.m_ib.Init(self.m_IName, self.m_Width - 12, aDigits, '')
        self.m_ib.SetReadOnly(True)
        self.m_d.Init(self.m_DName)
        self.m_cc = 0
        self.m_Tag = ''
    def SetReadOnly(self, aValue):
        self.m_ib.SetReadOnly(aValue)
    def ReadOnly(self):
        return self.m_ib.ReadOnly()
    def SetDigits(self, aValue):
        self.m_ib.SetDigits(aValue)
    def Digits(self):
        return self.m_ib.Digits()
    def SetMinValue(self, aValue):
        self.m_ib.SetMinValue(aValue)
    def MinValue(self):
        return self.m_ib.MinValue()
    def SetMaxValue(self, aValue):
        self.m_ib.SetMaxValue(aValue)
    def MaxValue(self):
        return self.m_ib.MaxValue()
    def SetWidth(self, aValue):
        self.m_Width = aValue
        self.m_ib.SetWidth(self.m_Width - 12)
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.m_d.Hide()
            self.m_ib.Hide()
            self.Show_0()
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.m_ib.SetPos(self.m_Left, self.m_Top)
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
        self.m_ib.SetPosLeft(self.m_Left)
    def SetPosTop(self, aTop):
        self.m_Top = aTop
        self.m_ib.SetPosTop(self.m_Top)
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        self.m_ib.Show_0()
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        self.m_d.Hide()
        self.m_ib.Hide()
    def Value(self):
        return self.m_ib.ValueDouble()
    def SetValue(self, aValue):
        self.m_ib.SetValue_2(aValue)
    def Event(self, id_, lparam, dparam, sparam):
        m_event = 0
        if sparam == '':
            if id_ == CHARTEVENT_CLICK:
                self.m_cc += 1
                if self.m_cc >= 2:
                    if self.m_d.Visible():
                        self.m_d.Hide()
        else:
            self.m_cc = 0
            if self.m_ib.Event(id_, lparam, dparam, sparam) == 1:
                m_event = 1
            m_dev = self.m_d.Event(id_, lparam, dparam, sparam)
            if m_dev == 1:
                m_oldvalue = self.m_ib.ValueDouble()
                self.m_ib.SetValue_2(self.m_d.Value())
                if m_oldvalue != self.m_d.Value():
                    m_event = 1
                ChartRedraw()
            if id_ == CHARTEVENT_OBJECT_CLICK:
                if sparam == self.m_BName:
                    if self.m_d.Visible():
                        self.m_d.Hide()
                    else:
                        m_w = _idiv(_int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, self.m_SubWindow)), 2)
                        m_h = _idiv(_int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, self.m_SubWindow)), 2)
                        m_x = self.m_Left + _idiv(self.m_Width, 2)
                        m_y = self.m_Top + _idiv(self.m_Height, 2)
                        m_cx = 0
                        m_cy = 0
                        if m_x < m_w:
                            m_cx = self.m_Left
                        else:
                            m_cx = self.m_Left - self.m_d.Width() + self.m_Width
                        if m_y < m_h:
                            m_cy = self.m_Top + self.m_ib.Height() - 1
                        else:
                            m_cy = self.m_Top - self.m_d.Height() + 1
                        self.m_d.Show_2(m_cx, m_cy)
                else:
                    if m_dev != 2:
                        if self.m_d.Visible():
                            self.m_d.Hide()
        return m_event
    def SetTag(self, aTag):
        self.m_Tag = aTag
    def Tag(self):
        return self.m_Tag
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.m_ib.SetSubWindow_1(self.m_SubWindow)
            self.m_d.SetSubWindow_1(self.m_SubWindow)
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def Warning(self):
        return self.m_ib.Warning()
    def SetWarning(self, aValue):
        self.m_ib.SetWarning(aValue)

class CTable(MqlObject):
    _q_fields = ('m_row', 'm__vsb', 'm__hsb', 'm_Name', 'm_CollsCount', 'm_CollWidth', 'm_RowsCount', 'm_Width', 'm_Height', 'm_left', 'm_Top', 'm_Visible', 'm_tWidth', 'm_tHeight', 'm_vsb', 'm_hsb', 'm_DefBgColor', 'm_DefTxColor', 'm_DefFontFace', 'm_DefFontSize', 'm_SubWindow', 'm_mrc', 'm_mcc', 'm_FlashColor', 'm_PreSelectedR', 'm_PreSelectedC', 'm_PreNorm', 'm_Tag', 'm_LastClickedRow', 'm_LastClickedColl', 'm_AllowSelection')
    def __init__(self, *args):
        self.m_row = Arr(0, 0, factory=sRow)
        self.m__vsb = CVScrollBar()
        self.m__hsb = CHScrollBar()
        self.m_Name = ""
        self.m_CollsCount = 0
        self.m_CollWidth = Arr(0, 0)
        self.m_RowsCount = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_left = 0
        self.m_Top = 0
        self.m_Visible = False
        self.m_tWidth = 0
        self.m_tHeight = 0
        self.m_vsb = False
        self.m_hsb = False
        self.m_DefBgColor = 0
        self.m_DefTxColor = 0
        self.m_DefFontFace = ""
        self.m_DefFontSize = 0
        self.m_SubWindow = 0
        self.m_mrc = 0
        self.m_mcc = 0
        self.m_FlashColor = 0
        self.m_PreSelectedR = 0
        self.m_PreSelectedC = 0
        self.m_PreNorm = False
        self.m_Tag = ""
        self.m_LastClickedRow = 0
        self.m_LastClickedColl = 0
        self.m_AllowSelection = False
    def SB(self):
        self.CountTWidth()
        self.CountTHeight()
        self.m_hsb = False
        self.m_vsb = False
        m_bheight = self.m_Height
        m_bwidth = self.m_Width
        m_tth = self.m_tHeight
        m_ttw = self.m_tWidth
        if self.m_tWidth > m_bwidth:
            self.m_tWidth = m_bwidth
            self.m_hsb = True
            m_bheight -= self.m__hsb.Height()
        if self.m_tHeight > m_bheight:
            self.m_tHeight = m_bheight
            self.m_vsb = True
            m_bwidth -= self.m__vsb.Width()
        if self.m_tWidth > m_bwidth:
            self.m_tWidth = m_bwidth
            if not self.m_hsb:
                self.m_hsb = True
                m_bheight -= self.m__hsb.Height()
        if self.m_tHeight > m_bheight:
            self.m_tHeight = m_bheight
            if not self.m_vsb:
                self.m_vsb = True
                m_bwidth -= self.m__vsb.Width()
        if self.m_vsb:
            self.m__vsb.SetMax(m_tth - m_bheight)
            self.m__vsb.SetSmallChange(MathMax(MathMin(25, m_bheight), 1))
            self.m__vsb.SetLageChange(MathMax(m_bheight, 1))
        else:
            self.m__vsb.SetValue(0)
        if self.m_hsb:
            self.m__hsb.SetMax(m_ttw - m_bwidth)
            self.m__hsb.SetSmallChange(MathMax(MathMin(25, m_bwidth), 1))
            self.m__hsb.SetLageChange(MathMax(m_bwidth, 1))
        else:
            self.m__hsb.SetValue(0)
    def CountTWidth(self):
        self.m_tWidth = 0
        for i in range(0, self.m_CollsCount):
            self.m_tWidth += self.m_CollWidth[i]
    def CountTHeight(self):
        self.m_tHeight = 0
        for i in range(0, self.m_RowsCount):
            self.m_tHeight += self.m_row[i].RowHeight
    def iif(self, aBool, aIfTrue, aIfFalse):
        if aBool:
            return aIfTrue
        return aIfFalse
    def its(self, aValue):
        return IntegerToString(aValue)
    def GetRGB(self, aColor, aR, aG, aB):
        aR.v = aColor
        aB.v = _idiv(aR.v, 65536)
        aR.v -= aB.v * 65536
        aG.v = _idiv(aR.v, 256)
        aR.v -= aG.v * 256
    def WEBColor(self, aColor):
        ttr = Box(0)
        ttg = Box(0)
        ttb = Box(0)
        self.GetRGB(aColor, ttr, ttg, ttb)
        return '#' + StringFormat('%02x', ttr.v) + StringFormat('%02x', ttg.v) + StringFormat('%02x', ttb.v)
    def Create(self):
        self.m_PreSelectedR = -1
        self.m_PreSelectedC = -1
        self.m_PreNorm = False
        self.SB()
        self.m_mrc = MathMax(self.m_mrc, self.m_RowsCount)
        self.m_mcc = MathMax(self.m_mcc, self.m_CollsCount)
        m_xpos = 0
        m_ypos = 0
        if self.m_vsb:
            self.m__vsb.SetHeight(self.m_tHeight)
            self.m__vsb.Show_2(self.m_left + self.m_tWidth, self.m_Top)
        else:
            self.m__vsb.Hide()
        if self.m_hsb:
            self.m__hsb.SetWidth(self.m_tWidth)
            self.m__hsb.Show_2(self.m_left, self.m_Top + self.m_tHeight)
        else:
            self.m__hsb.Hide()
        m_xs = self.m__hsb.Value()
        m_ys = self.m__vsb.Value()
        m_ypos = -m_ys
        i = 0
        while i < self.m_RowsCount:
            m_xpos = -m_xs
            m_br = False
            j = 0
            while j < self.m_CollsCount:
                if self.m_row[i].CellExist[j]:
                    m_w = self.m_CollWidth[j]
                    m_h = self.m_row[i].RowHeight
                    if self.m_row[i].CellCollSpan[j] > 1 or self.m_row[i].CellRowSpan[j] > 1:
                        if self.m_row[i].CellCollSpan[j] > 1:
                            for k in range(j + 1, self.m_CollsCount):
                                if self.m_row[i].CellExist[k]:
                                    break
                                m_w += self.m_CollWidth[k]
                        if self.m_row[i].CellRowSpan[j] > 1:
                            for k in range(i + 1, self.m_RowsCount):
                                if self.m_row[k].CellExist[j]:
                                    break
                                m_h += self.m_row[k].RowHeight
                    if m_xpos > self.m_tWidth:
                        while j < self.m_CollsCount:
                            ObjectDelete(0, self.m_Name + '_Cell_R(' + IntegerToString(i) + ')_C(' + IntegerToString(j) + ')')
                            j += 1
                        break
                    if m_ypos > self.m_tHeight:
                        while j < self.m_CollsCount:
                            ObjectDelete(0, self.m_Name + '_Cell_R(' + IntegerToString(i) + ')_C(' + IntegerToString(j) + ')')
                            j += 1
                        break
                    if (self.m_left + m_xpos + m_w) > (self.m_left + self.m_tWidth):
                        m_w = self.m_tWidth - m_xpos
                        m_br = True
                    if (m_ypos + m_h) > self.m_tHeight:
                        m_h = self.m_tHeight - m_ypos
                    m_l2 = self.m_left + m_xpos
                    m_t2 = self.m_Top + m_ypos
                    if (m_xpos + m_w) > 0 and (m_ypos + m_h) > 0:
                        if m_xpos < 0:
                            m_l2 = self.m_left
                            m_w = m_xpos + m_w
                        if m_ypos < 0:
                            m_t2 = self.m_Top
                            m_h = m_ypos + m_h
                        w.Edit(self.m_Name + '_Cell_R(' + IntegerToString(i) + ')_C(' + IntegerToString(j) + ')', self.m_SubWindow, m_l2, m_t2, m_w, m_h, self.m_row[i].CellText[j], self.m_row[i].CellBGColor[j], self.m_row[i].CellTxtColor[j], self.m_row[i].CellFontSize[j], self.m_row[i].CellFont[j])
                        g.SetReadOnly_2(self.m_Name + '_Cell_R(' + IntegerToString(i) + ')_C(' + IntegerToString(j) + ')', True)
                    else:
                        ObjectDelete(0, self.m_Name + '_Cell_R(' + IntegerToString(i) + ')_C(' + IntegerToString(j) + ')')
                    if m_br:
                        j += 1
                        while j < self.m_CollsCount:
                            ObjectDelete(0, self.m_Name + '_Cell_R(' + IntegerToString(i) + ')_C(' + IntegerToString(j) + ')')
                            j += 1
                        break
                m_xpos += self.m_CollWidth[j]
                j += 1
            m_ypos += self.m_row[i].RowHeight
            i += 1
    def Delete(self):
        for i in range(0, self.m_mrc):
            for j in range(0, self.m_mcc):
                ObjectDelete(0, self.m_Name + '_Cell_R(' + IntegerToString(i) + ')_C(' + IntegerToString(j) + ')')
        self.m_mrc = 0
        self.m_mcc = 0
    def SetCrossColor(self, aR, aC, aNormal):
        if aNormal:
            i = 0
            while i < self.m_RowsCount:
                m_tn = self.m_Name + '_Cell_R(' + IntegerToString(i) + ')_C(' + IntegerToString(aC) + ')'
                if ObjectFind(0, m_tn) == self.m_SubWindow:
                    g.Attach(m_tn)
                    g.SetBgColor_1(self.m_row[i].CellBGColor[aC])
                i += 1
            i = 0
            while i < self.m_CollsCount:
                m_tn = self.m_Name + '_Cell_R(' + IntegerToString(aR) + ')_C(' + IntegerToString(i) + ')'
                if ObjectFind(0, m_tn) == self.m_SubWindow:
                    g.Attach(m_tn)
                    g.SetBgColor_1(self.m_row[aR].CellBGColor[i])
                i += 1
        else:
            i = 0
            while i < self.m_RowsCount:
                m_tn = self.m_Name + '_Cell_R(' + IntegerToString(i) + ')_C(' + IntegerToString(aC) + ')'
                if ObjectFind(0, m_tn) == self.m_SubWindow:
                    g.Attach(m_tn)
                    g.SetBgColor_1(self.m_FlashColor)
                i += 1
            i = 0
            while i < self.m_CollsCount:
                m_tn = self.m_Name + '_Cell_R(' + IntegerToString(aR) + ')_C(' + IntegerToString(i) + ')'
                if ObjectFind(0, m_tn) == self.m_SubWindow:
                    g.Attach(m_tn)
                    g.SetBgColor_1(self.m_FlashColor)
                i += 1
    def Init(self, aName='CTable', aWidth=200, aHeight=200):
        self.m_SubWindow = 0
        self.m_Visible = False
        self.m_Name = aName
        self.m_CollsCount = 0
        self.m_RowsCount = 0
        ArrayResize(self.m_CollWidth, 0)
        ArrayResize(self.m_row, 0)
        self.m_Width = aWidth
        self.m_Height = aHeight
        self.m_left = 0
        self.m_Top = 0
        self.m_tWidth = 0
        self.m_tHeight = 0
        self.m_DefBgColor = ClrScheme.Color(0)
        self.m_DefTxColor = ClrScheme.Color(1)
        self.m_FlashColor = ClrScheme.Color(14)
        self.m_DefFontFace = 'Arial'
        self.m_DefFontSize = 7
        self.m_PreSelectedR = -1
        self.m_PreSelectedC = -1
        self.m_PreNorm = True
        self.m_Tag = ''
        self.m__vsb.Init(self.m_Name + '_VSB', self.m_Height)
        self.m__hsb.Init(self.m_Name + '_HSB', self.m_Width)
        self.m_LastClickedRow = -1
        self.m_LastClickedColl = -1
        self.m_AllowSelection = True
    def AddRow(self):
        ArrayResize(self.m_row, self.m_RowsCount + 1)
        ArrayResize(self.m_row[self.m_RowsCount].CellBGColor, self.m_CollsCount)
        ArrayResize(self.m_row[self.m_RowsCount].CellText, self.m_CollsCount)
        ArrayResize(self.m_row[self.m_RowsCount].CellTxtColor, self.m_CollsCount)
        ArrayResize(self.m_row[self.m_RowsCount].CellFont, self.m_CollsCount)
        ArrayResize(self.m_row[self.m_RowsCount].CellFontSize, self.m_CollsCount)
        ArrayResize(self.m_row[self.m_RowsCount].CellCollSpan, self.m_CollsCount)
        ArrayResize(self.m_row[self.m_RowsCount].CellRowSpan, self.m_CollsCount)
        ArrayResize(self.m_row[self.m_RowsCount].CellExist, self.m_CollsCount)
        self.m_row[self.m_RowsCount].RowHeight = 15
        for i in range(0, self.m_CollsCount):
            self.m_row[self.m_RowsCount].CellBGColor[i] = self.m_DefBgColor
            self.m_row[self.m_RowsCount].CellText[i] = ''
            self.m_row[self.m_RowsCount].CellTxtColor[i] = self.m_DefTxColor
            self.m_row[self.m_RowsCount].CellFont[i] = self.m_DefFontFace
            self.m_row[self.m_RowsCount].CellFontSize[i] = self.m_DefFontSize
            self.m_row[self.m_RowsCount].CellCollSpan[i] = 1
            self.m_row[self.m_RowsCount].CellRowSpan[i] = 1
            self.m_row[self.m_RowsCount].CellExist[i] = True
        self.m_RowsCount += 1
        self.CountTHeight()
    def DeleteRow(self, aIndex):
        if self.m_RowsCount > 0:
            for i in range(aIndex, self.m_RowsCount - 1):
                ArrayResize(self.m_row[i].CellBGColor, ArraySize(self.m_row[i + 1].CellBGColor))
                ArrayCopy(self.m_row[i].CellBGColor, self.m_row[i + 1].CellBGColor)
                ArrayResize(self.m_row[i].CellCollSpan, ArraySize(self.m_row[i + 1].CellCollSpan))
                ArrayCopy(self.m_row[i].CellCollSpan, self.m_row[i + 1].CellCollSpan)
                ArrayResize(self.m_row[i].CellExist, ArraySize(self.m_row[i + 1].CellExist))
                ArrayCopy(self.m_row[i].CellExist, self.m_row[i + 1].CellExist)
                ArrayResize(self.m_row[i].CellFont, ArraySize(self.m_row[i + 1].CellFont))
                ArrayCopy(self.m_row[i].CellFont, self.m_row[i + 1].CellFont)
                ArrayResize(self.m_row[i].CellFontSize, ArraySize(self.m_row[i + 1].CellFontSize))
                ArrayCopy(self.m_row[i].CellFontSize, self.m_row[i + 1].CellFontSize)
                ArrayResize(self.m_row[i].CellMergeHeight, ArraySize(self.m_row[i + 1].CellMergeHeight))
                ArrayCopy(self.m_row[i].CellMergeHeight, self.m_row[i + 1].CellMergeHeight)
                ArrayResize(self.m_row[i].CellMergeWidth, ArraySize(self.m_row[i + 1].CellMergeWidth))
                ArrayCopy(self.m_row[i].CellMergeWidth, self.m_row[i + 1].CellMergeWidth)
                ArrayResize(self.m_row[i].CellRowSpan, ArraySize(self.m_row[i + 1].CellRowSpan))
                ArrayCopy(self.m_row[i].CellRowSpan, self.m_row[i + 1].CellRowSpan)
                ArrayResize(self.m_row[i].CellText, ArraySize(self.m_row[i + 1].CellText))
                ArrayCopy(self.m_row[i].CellText, self.m_row[i + 1].CellText)
                ArrayResize(self.m_row[i].CellTxtColor, ArraySize(self.m_row[i + 1].CellTxtColor))
                ArrayCopy(self.m_row[i].CellTxtColor, self.m_row[i + 1].CellTxtColor)
                self.m_row[i].RowHeight = self.m_row[i + 1].RowHeight
            self.m_RowsCount -= 1
            ArrayResize(self.m_row, self.m_RowsCount)
    def Show_2(self, aLeft, aTop):
        self.m_left = aLeft
        self.m_Top = aTop
        self.Show_0()
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        ChartRedraw()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        if self.m__vsb.Visible() or self.m__hsb.Visible():
            self.m__vsb.Hide()
            self.m__hsb.Hide()
        ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
        if self.m__hsb.Visible():
            self.m__hsb.Hide()
        if self.m__vsb.Visible():
            self.m__vsb.Hide()
        if self.m_Visible:
            self.Show_0()
    def SetPos(self, aLeft, aTop):
        self.m_left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Left(self):
        return self.m_left
    def Top(self):
        return self.m_Top
    def SetWidth(self, aWidth):
        self.m_Width = aWidth
    def SetHeight(self, aHeight):
        self.m_Height = aHeight
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def SetCollsCount(self, aCount):
        m_tmp = self.m_CollsCount
        self.m_CollsCount = aCount
        ArrayResize(self.m_CollWidth, self.m_CollsCount)
        for j in range(m_tmp, self.m_CollsCount):
            self.m_CollWidth[j] = 30
        for i in range(0, self.m_RowsCount):
            ArrayResize(self.m_row[i].CellBGColor, self.m_CollsCount)
            ArrayResize(self.m_row[i].CellText, self.m_CollsCount)
            ArrayResize(self.m_row[i].CellTxtColor, self.m_CollsCount)
            ArrayResize(self.m_row[i].CellFont, self.m_CollsCount)
            ArrayResize(self.m_row[i].CellFontSize, self.m_CollsCount)
            ArrayResize(self.m_row[i].CellCollSpan, self.m_CollsCount)
            ArrayResize(self.m_row[i].CellRowSpan, self.m_CollsCount)
            ArrayResize(self.m_row[i].CellExist, self.m_CollsCount)
            for j in range(m_tmp, self.m_CollsCount):
                self.m_row[i].CellBGColor[j] = self.m_DefBgColor
                self.m_row[i].CellText[j] = ''
                self.m_row[i].CellTxtColor[j] = self.m_DefTxColor
                self.m_row[i].CellFont[j] = self.m_DefFontFace
                self.m_row[i].CellFontSize[j] = self.m_DefFontSize
                self.m_row[i].CellCollSpan[j] = 1
                self.m_row[i].CellRowSpan[j] = 1
                self.m_row[i].CellExist[j] = True
        self.CountTWidth()
    def SetCollWidth(self, aCollIndex, aWidth):
        self.m_CollWidth[aCollIndex] = aWidth
        self.CountTWidth()
    def SetRowsCount(self, aRowsCount):
        if aRowsCount < self.m_RowsCount:
            self.m_RowsCount = aRowsCount
            ArrayResize(self.m_row, self.m_RowsCount)
            self.CountTHeight()
        else:
            for i in range(self.m_RowsCount, aRowsCount):
                self.AddRow()
    def Clear(self):
        ArrayResize(self.m_row, 0)
        ArrayResize(self.m_CollWidth, 0)
        self.m_CollsCount = 0
        self.m_RowsCount = 0
        self.m__hsb.SetValue(0)
        self.m__vsb.SetValue(0)
    def SetRowHeight(self, aRowIndex, aHeight):
        self.m_row[aRowIndex].RowHeight = aHeight
        self.CountTHeight()
    def SetCellText(self, aRowIndex, aCollIndex, aText):
        self.m_row[aRowIndex].CellText[aCollIndex] = aText
    def SetCellBGColor(self, aRowIndex, aCollIndex, aBGColor):
        self.m_row[aRowIndex].CellBGColor[aCollIndex] = aBGColor
    def SetCellTxtColor(self, aRowIndex, aCollIndex, aTxtColor):
        self.m_row[aRowIndex].CellTxtColor[aCollIndex] = aTxtColor
    def SetCellFont(self, aRowIndex, aCollIndex, aFont='Arial'):
        self.m_row[aRowIndex].CellFont[aCollIndex] = aFont
    def SetCellFontSize(self, aRowIndex, aCollIndex, aFontSize):
        self.m_row[aRowIndex].CellFontSize[aCollIndex] = aFontSize
    def SetCellsMerge(self, aRowIndex, aCollIndex, aRowSpan, aCollSpan):
        aRowSpan = MathMax(aRowSpan, 1)
        aCollSpan = MathMax(aCollSpan, 1)
        if self.m_row[aRowIndex].CellExist[aCollIndex]:
            m_rs = self.m_row[aRowIndex].CellRowSpan[aCollIndex]
            m_cs = self.m_row[aRowIndex].CellCollSpan[aCollIndex]
            for i in range(aRowIndex, MathMin(self.m_RowsCount, aRowIndex + m_rs)):
                for j in range(aCollIndex, MathMin(self.m_CollsCount, aCollIndex + m_cs)):
                    self.m_row[i].CellExist[j] = True
            m_rs = aRowSpan
            m_cs = aCollSpan
            for i in range(aRowIndex, MathMin(self.m_RowsCount, aRowIndex + m_rs)):
                for j in range(aCollIndex, MathMin(self.m_CollsCount, aCollIndex + m_cs)):
                    self.m_row[i].CellExist[j] = False
            self.m_row[aRowIndex].CellRowSpan[aCollIndex] = aRowSpan
            self.m_row[aRowIndex].CellCollSpan[aCollIndex] = aCollSpan
            m_cs = self.m_row[aRowIndex].CellCollSpan[aCollIndex]
            self.m_row[aRowIndex].CellExist[aCollIndex] = True
    def CollsCount(self):
        return self.m_CollsCount
    def CollWidth(self, aCollIndex):
        return self.m_CollWidth[aCollIndex]
    def RowsCount(self):
        return self.m_RowsCount
    def RowHeight(self, aRowIndex):
        return self.m_row[aRowIndex].RowHeight
    def CellText(self, aRowIndex, aCollIndex):
        return self.m_row[aRowIndex].CellText[aCollIndex]
    def CellBGColor(self, aRowIndex, aCollIndex):
        return self.m_row[aRowIndex].CellBGColor[aCollIndex]
    def CellTxtColor(self, aRowIndex, aCollIndex):
        return self.m_row[aRowIndex].CellTxtColor[aCollIndex]
    def CellFont(self, aRowIndex, aCollIndex):
        return self.m_row[aRowIndex].CellFont[aCollIndex]
    def CellFontSize(self, aRowIndex, aCollIndex):
        return self.m_row[aRowIndex].CellFontSize[aCollIndex]
    def Event(self, id_, lparam, dparam, sparam):
        m_rv = 0
        if self.m__hsb.Event(id_, lparam, dparam, sparam) or self.m__vsb.Event(id_, lparam, dparam, sparam):
            self.Show_0()
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if StringFind(sparam, self.m_Name + '_Cell', 0) == 0:
                m_p1 = StringFind(sparam, 'R(', 0) + 2
                m_p2 = StringFind(sparam, ')', 0)
                self.m_LastClickedRow = _int(StringToInteger(StringSubstr(sparam, m_p1, m_p2 - m_p1)))
                m_p1 = StringFind(sparam, 'C(', 0) + 2
                m_p2 = StringFind(sparam, ')', 0)
                self.m_LastClickedColl = _int(StringToInteger(StringSubstr(sparam, m_p1, m_p2 - m_p1)))
                m_rv = 1
                if self.m_AllowSelection:
                    if self.m_LastClickedRow == self.m_PreSelectedR and self.m_LastClickedColl == self.m_PreSelectedC:
                        if not self.m_PreNorm:
                            self.SetCrossColor(self.m_PreSelectedR, self.m_PreSelectedC, True)
                            self.m_PreNorm = True
                        else:
                            self.SetCrossColor(self.m_PreSelectedR, self.m_PreSelectedC, False)
                            self.m_PreNorm = False
                    else:
                        if self.m_PreSelectedR != -1:
                            self.SetCrossColor(self.m_PreSelectedR, self.m_PreSelectedC, True)
                        self.SetCrossColor(self.m_LastClickedRow, self.m_LastClickedColl, False)
                        self.m_PreNorm = False
                    self.m_PreSelectedR = self.m_LastClickedRow
                    self.m_PreSelectedC = self.m_LastClickedColl
                ChartRedraw(0)
        return m_rv
    def HTML(self):
        m_ms = 'style="' + 'border: 1px solid ' + self.WEBColor(self.m_DefTxColor) + ';' + 'border-spacing: 0;' + 'font-family: ' + self.m_DefFontFace + ';' + 'font-size: ' + self.its(self.m_DefFontSize) + 'pt;' + 'color: ' + self.WEBColor(self.m_DefTxColor) + ';' + 'background-color: ' + self.WEBColor(self.m_DefBgColor) + ';' + '"'
        m_str = '<table ' + m_ms + ' cellspacing=0>\n'
        i = 0
        while i < ArraySize(self.m_row):
            m_str = m_str + '<tr>\n'
            j = 0
            while j < self.m_CollsCount:
                if self.m_row[i].CellExist[j]:
                    m_t1 = self.iif(self.m_row[i].CellCollSpan[j] > 1, ' colspan=' + IntegerToString(self.m_row[i].CellCollSpan[j]), '')
                    m_t2 = self.iif(self.m_row[i].CellRowSpan[j] > 1, ' rowspan=' + IntegerToString(self.m_row[i].CellRowSpan[j]), '')
                    m_t3 = 'style="'
                    m_t3 = m_t3 + 'border: 1px solid ' + self.WEBColor(self.m_row[i].CellTxtColor[j]) + ';'
                    if self.m_row[i].CellBGColor[j] != self.m_DefBgColor:
                        m_t3 = m_t3 + 'background-color: ' + self.WEBColor(self.m_row[i].CellBGColor[j]) + ';'
                    if self.m_row[i].CellFont[j] != self.m_DefFontFace:
                        m_t3 = m_t3 + 'font-family: ' + self.m_row[i].CellFont[j] + ';'
                    if self.m_row[i].CellFontSize[j] != self.m_DefFontSize:
                        m_t3 = m_t3 + 'font-size: ' + self.its(self.m_row[i].CellFontSize[j]) + 'pt;'
                    if self.m_row[i].CellTxtColor[j] != self.m_DefTxColor:
                        m_t3 = m_t3 + 'color: ' + self.WEBColor(self.m_row[i].CellTxtColor[j]) + ';'
                    m_t3 = m_t3 + '"'
                    m_w = 0
                    k = j
                    while k < (j + self.m_row[i].CellCollSpan[j]):
                        if k < self.m_CollsCount:
                            m_w += self.m_CollWidth[j]
                        k += 1
                    m_h = 0
                    k = i
                    while k < (i + self.m_row[i].CellRowSpan[j]):
                        if k < ArraySize(self.m_row):
                            m_h += self.m_row[k].RowHeight
                        k += 1
                    m_h -= 2
                    m_str = m_str + '<td ' + m_t3 + ' width=' + self.its(m_w) + ' height=' + self.its(m_h) + m_t1 + m_t2 + '>' + self.m_row[i].CellText[j] + '</td>\n'
                j += 1
            m_str = m_str + '</tr>\n'
            i += 1
        m_str = m_str + '</table>\n'
        return m_str
    def SetTag(self, aTag):
        self.m_Tag = aTag
    def Tag(self):
        return self.m_Tag
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.m__hsb.SetSubWindow_1(self.m_SubWindow)
            self.m__vsb.SetSubWindow_1(self.m_SubWindow)
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def LastClickedRaw(self):
        return self.m_LastClickedRow
    def LastClickedColl(self):
        return self.m_LastClickedColl
    def SetAllowSelection(self, aValue):
        self.m_AllowSelection = aValue
    def AllowSelection(self):
        return self.m_AllowSelection

class sRow(MqlObject):
    _q_fields = ('RowHeight', 'CellText', 'CellBGColor', 'CellTxtColor', 'CellFont', 'CellFontSize', 'CellCollSpan', 'CellRowSpan', 'CellExist', 'CellMergeWidth', 'CellMergeHeight')
    def __init__(self, *args):
        self.RowHeight = 0
        self.CellText = Arr(0, "")
        self.CellBGColor = Arr(0, 0)
        self.CellTxtColor = Arr(0, 0)
        self.CellFont = Arr(0, "")
        self.CellFontSize = Arr(0, 0)
        self.CellCollSpan = Arr(0, 0)
        self.CellRowSpan = Arr(0, 0)
        self.CellExist = Arr(0, 0)
        self.CellMergeWidth = Arr(0, 0)
        self.CellMergeHeight = Arr(0, 0)

class CFrame(MqlObject):
    _q_fields = ('m_Left', 'm_Top', 'm_Width', 'm_Height', 'm_CaptionWidth', 'm_Name', 'm_Caption', 'm_SubWindow', 'm_Visible', 'm_BgColor', 'm_BorderColor', 'm_CaptionColor', 'm_Tag')
    def __init__(self, *args):
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_CaptionWidth = 0
        self.m_Name = ""
        self.m_Caption = ""
        self.m_SubWindow = 0
        self.m_Visible = False
        self.m_BgColor = 0
        self.m_BorderColor = 0
        self.m_CaptionColor = 0
        self.m_Tag = ""
    def Init(self, aName='CFrame', aWidth=50, aHeight=50, aCaption='CFrame', aCaptionWidth=37):
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = aWidth
        self.m_Height = aHeight
        self.m_CaptionWidth = aCaptionWidth
        self.m_Name = aName
        self.m_Caption = aCaption
        self.m_SubWindow = 0
        self.m_Visible = False
        self.m_BgColor = ClrScheme.Color(39)
        self.m_BorderColor = ClrScheme.Color(40)
        self.m_CaptionColor = ClrScheme.Color(41)
        self.m_Tag = ''
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Show_0(self):
        self.m_Visible = True
        w.Frame(self.m_Name, self.m_SubWindow, self.m_Left, self.m_Top, self.m_Width, self.m_Height, self.m_Caption, self.m_CaptionWidth, self.m_BgColor, self.m_BorderColor, self.m_CaptionColor)
        w.Redraw()
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        w.FrameDelete(self.m_Name)
        w.Redraw()
    def Refresh(self):
        if self.m_Visible:
            w.FrameDelete(self.m_Name)
            self.Show_0()
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def SetWidth(self, aWidth):
        self.m_Width = aWidth
    def SetHeight(self, aHeight):
        self.m_Height = aHeight
    def CaptionWidth(self):
        return self.m_CaptionWidth
    def SetCaptionWidth(self, aCaptionWidth):
        self.m_CaptionWidth = aCaptionWidth
    def Caption(self):
        return self.m_Caption
    def SetCaption(self, aCaption):
        self.m_Caption = aCaption
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag

class CButton(MqlObject):
    _q_fields = ('m_Left', 'm_Top', 'm_Width', 'm_Height', 'm_CaptionWidth', 'm_Name', 'm_Caption', 'm_SubWindow', 'm_Visible', 'm_BgColor', 'm_CaptionColor', 'm_Tag')
    def __init__(self, *args):
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_CaptionWidth = 0
        self.m_Name = ""
        self.m_Caption = ""
        self.m_SubWindow = 0
        self.m_Visible = False
        self.m_BgColor = 0
        self.m_CaptionColor = 0
        self.m_Tag = ""
    def Init(self, aName='CButton', aWidth=80, aHeight=30, aCaption='CButton'):
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = aWidth
        self.m_Height = aHeight
        self.m_Name = aName
        self.m_Caption = aCaption
        self.m_SubWindow = 0
        self.m_Visible = False
        self.m_BgColor = ClrScheme.Color(42)
        self.m_CaptionColor = ClrScheme.Color(43)
        self.m_Tag = ''
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Show_0(self):
        self.m_Visible = True
        w.Button(self.m_Name, self.m_SubWindow, self.m_Left, self.m_Top, self.m_Width, self.m_Height, self.m_Caption, self.m_BgColor, self.m_CaptionColor)
        w.Redraw()
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        w.Delete(self.m_Name)
        w.Redraw()
    def Refresh(self):
        if self.m_Visible:
            w.Delete(self.m_Name)
            self.Show_0()
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def SetWidth(self, aWidth):
        self.m_Width = aWidth
    def SetHeight(self, aHeight):
        self.m_Height = aHeight
    def Caption(self):
        return self.m_Caption
    def SetCaption(self, aCaption):
        self.m_Caption = aCaption
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag
    def Event(self, id_, lparam, dparam, sparam):
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if sparam == self.m_Name:
                if g.State_1(self.m_Name):
                    Sleep(100)
                    g.SetState_2(self.m_Name, False)
                    g.Redraw_0()
                    return 1
        return 0

class CLabel(MqlObject):
    _q_fields = ('m_Left', 'm_Top', 'm_Width', 'm_Height', 'm_Name', 'm_Text', 'm_TextArray', 'm_SubWindow', 'm_Visible', 'm_Color', 'm_FontSize', 'm_Font', 'm_Tag')
    def __init__(self, *args):
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_Name = ""
        self.m_Text = ""
        self.m_TextArray = Arr(0, "")
        self.m_SubWindow = 0
        self.m_Visible = False
        self.m_Color = 0
        self.m_FontSize = 0
        self.m_Font = ""
        self.m_Tag = ""
    def Create(self):
        i = 0
        while i < ArraySize(self.m_TextArray):
            w.Label(self.m_Name + '_Lbl(' + IntegerToString(i) + ')', self.m_SubWindow, self.m_Left, self.m_Top + _int(i * self.m_FontSize * 1.4), self.m_TextArray[i], self.m_Color, self.m_FontSize, self.m_Font)
            i += 1
    def Delete(self):
        i = 0
        while i < ArraySize(self.m_TextArray):
            g.Delete_1(self.m_Name + '_Lbl(' + IntegerToString(i) + ')')
            i += 1
    def Init(self, aName='CLabel', aText='CLabel'):
        self.m_Left = 0
        self.m_Top = 0
        self.m_Name = aName
        self.m_Text = aText
        self.m_SubWindow = 0
        self.m_Visible = False
        self.m_Color = ClrScheme.Color(44)
        self.m_FontSize = 8
        self.m_Font = 'Arial'
        self.m_Tag = ''
        StringSplit(self.m_Text, 10, self.m_TextArray)
        self.m_Visible = False
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        ChartRedraw()
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.Show_0()
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Text(self):
        return self.m_Text
    def SetText(self, aText=''):
        if self.m_Visible:
            self.Delete()
        self.m_Text = aText
        StringSplit(self.m_Text, 10, self.m_TextArray)
        if self.m_Visible:
            self.Create()
            ChartRedraw()
    def Font(self):
        return self.m_Font
    def SetFont(self, aFont='Arial'):
        self.m_Font = aFont
        self.Refresh()
    def FontSize(self):
        return self.m_FontSize
    def SetFontSize(self, aFontSize=8):
        self.m_FontSize = aFontSize
        self.Refresh()
    def SetColor(self, aColor=16777216):
        if aColor == 16777216:
            aColor = ClrScheme.Color(44)
        self.m_Color = aColor
        self.Refresh()
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aValue):
        self.m_Tag = aValue
    def Tag(self):
        return self.m_Tag

class CCalendar(MqlObject):
    _q_fields = ('m_SubWindow', 'm_Left', 'm_Top', 'm_Name', 'm_Visible', 'm_cb', 'm_sb', 'm_cb1', 'm_cb2', 'm_cb3', 'm_TimeValue', 'm_TimeStr', 'm_BgColor', 'm_BorderColor', 'm_ButBgColor', 'm_ButTxtColor', 'm_TxtColor', 'm_HeaderBgColor', 'm_DayBgColor', 'm_OtherMonthDayBgColor', 'm_DayColor', 'm_ToDayColor', 'm_RdBgColor', 'm_ToDay', 'm_ToDayStr', 'm_Cell', 'm_Date', 'm_Time', 'm_Sec', 'm_Line', 'm_TimeMode', 'm_Tag', 'm_NowText', 'm_ToDayText', 'm_LineText', 'm_wdn')
    def __init__(self, *args):
        self.m_SubWindow = 0
        self.m_Left = 0
        self.m_Top = 0
        self.m_Name = ""
        self.m_Visible = False
        self.m_cb = CComBox()
        self.m_sb = CSpinInputBox()
        self.m_cb1 = CComBox()
        self.m_cb2 = CComBox()
        self.m_cb3 = CComBox()
        self.m_TimeValue = 0
        self.m_TimeStr = MqlDateTime()
        self.m_BgColor = 0
        self.m_BorderColor = 0
        self.m_ButBgColor = 0
        self.m_ButTxtColor = 0
        self.m_TxtColor = 0
        self.m_HeaderBgColor = 0
        self.m_DayBgColor = 0
        self.m_OtherMonthDayBgColor = 0
        self.m_DayColor = 0
        self.m_ToDayColor = 0
        self.m_RdBgColor = 0
        self.m_ToDay = 0
        self.m_ToDayStr = MqlDateTime()
        self.m_Cell = Arr(7, 0, dyn=False, factory=m_SCellInfo, dims=(6,))
        self.m_Date = False
        self.m_Time = False
        self.m_Sec = False
        self.m_Line = False
        self.m_TimeMode = 0
        self.m_Tag = ""
        self.m_NowText = ""
        self.m_ToDayText = ""
        self.m_LineText = ""
        self.m_wdn = Arr(0, "")
    def F2(self, aA):
        if aA < 10:
            return '0' + IntegerToString(aA)
        return IntegerToString(aA)
    def ModeTime(self):
        if self.m_TimeMode == 1:
            return TimeLocal()
        else:
            return TimeCurrent()
    def Create(self):
        w.Canvas(self.m_Name + '_Canvas', self.m_SubWindow, self.m_Left, self.m_Top, 140, 55, self.m_BgColor, self.m_BorderColor)
        m_AddY = 0
        if self.m_Date:
            m_AddY = 117
            w.Button(self.m_Name + '_Left', self.m_SubWindow, self.m_Left + 3, self.m_Top + 2, 15, 15, '<', self.m_ButBgColor, self.m_ButTxtColor)
            self.m_cb.Show_2(self.m_Left + 20, self.m_Top + 2)
            self.m_sb.Show_2(self.m_Left + 81, self.m_Top + 2)
            w.Button(self.m_Name + '_Right', self.m_SubWindow, self.m_Left + 122, self.m_Top + 2, 15, 15, '>', self.m_ButBgColor, self.m_ButTxtColor)
            m_tn = ""
            for i in range(0, 7):
                m_tn = self.m_Name + '_WDN_' + IntegerToString(i)
                w.Edit(m_tn, self.m_SubWindow, self.m_Left + 3 + (i * 19), self.m_Top + 18, 20, 13, self.m_wdn[i], self.m_HeaderBgColor, self.m_TxtColor)
                g.SetReadOnly_2(m_tn, True)
            for j in range(0, 6):
                for i in range(0, 7):
                    m_tn = self.m_Name + '_D_' + IntegerToString(i) + '_' + IntegerToString(j)
                    w.Edit(self.m_Name + '_D_' + IntegerToString(i) + '_' + IntegerToString(j), self.m_SubWindow, self.m_Left + 3 + (i * 19), self.m_Top + 18 + 12 + (j * 12), 20, 13, 'zz', self.m_DayBgColor, self.m_TxtColor)
                    g.SetReadOnly_2(m_tn, True)
            self.m_ToDay = self.ModeTime()
            TimeToStruct(self.m_ToDay, self.m_ToDayStr)
            w.Canvas(self.m_Name + '_CDM', self.m_SubWindow, self.m_Left + 3, self.m_Top + 104, 20, 12, self.m_BgColor, self.m_ToDayColor)
            w.Button(self.m_Name + '_CDMB', self.m_SubWindow, self.m_Left + 4, self.m_Top + 105, 18, 10, ' ', self.m_ButBgColor, self.m_ButTxtColor)
            w.Label(self.m_Name + '_CD', self.m_SubWindow, self.m_Left + 29, self.m_Top + 105, '', self.m_TxtColor, 7)
            w.Canvas(self.m_Name + '_HL1', self.m_SubWindow, self.m_Left, self.m_Top + 117, 140, 1, self.m_BorderColor, self.m_BorderColor)
            g.SetYSize_2(self.m_Name + '_Canvas', m_AddY + 19)
        if self.m_Time:
            m_xad = 0
            m_xad1 = 0
            if self.m_Sec:
                self.m_cb3.Show_2(self.m_Left + 90 + 3, self.m_Top + 2 + m_AddY)
            else:
                m_xad = 20
                m_xad1 = 5
            self.m_cb1.Show_2(self.m_Left + 13 + m_xad, self.m_Top + 2 + m_AddY)
            self.m_cb2.Show_2(self.m_Left + 53 + m_xad, self.m_Top + 2 + m_AddY)
            w.Canvas(self.m_Name + '_CTM', self.m_SubWindow, self.m_Left + 3, self.m_Top + 18 + m_AddY, 20, 12, self.m_BgColor, self.m_ToDayColor)
            w.Button(self.m_Name + '_CTMB', self.m_SubWindow, self.m_Left + 4, self.m_Top + 19 + m_AddY, 18, 10, ' ', self.m_ButBgColor, self.m_ButTxtColor)
            w.Label(self.m_Name + '_CT', self.m_SubWindow, self.m_Left + 33 + m_xad1, self.m_Top + 19 + m_AddY, '', self.m_TxtColor, 7)
            w.Canvas(self.m_Name + '_HL2', self.m_SubWindow, self.m_Left, self.m_Top + 31 + m_AddY, 140, 1, self.m_BorderColor, self.m_BorderColor)
            m_AddY += 31
            g.SetYSize_2(self.m_Name + '_Canvas', m_AddY + 19)
        if self.m_Line:
            w.Button(self.m_Name + '_Line', self.m_SubWindow, self.m_Left + 50, self.m_Top + m_AddY + 2, 40, 15, self.m_LineText, self.m_ButBgColor, self.m_ButTxtColor)
        w.Button(self.m_Name + '_Cancel', self.m_SubWindow, self.m_Left + 3, self.m_Top + m_AddY + 2, 25, 15, ' x', self.m_ButBgColor, self.m_ButTxtColor)
        w.Button(self.m_Name + '_Ok', self.m_SubWindow, self.m_Left + 112, self.m_Top + m_AddY + 2, 25, 15, 'ok', self.m_ButBgColor, self.m_ButTxtColor)
        g.SetYSize_2(self.m_Name + '_Canvas', m_AddY + 19)
    def Delete(self):
        ObjectDelete(0, self.m_Name + '_Canvas')
        ObjectDelete(0, self.m_Name + '_Left')
        ObjectDelete(0, self.m_Name + '_Right')
        for i in range(0, 7):
            ObjectDelete(0, self.m_Name + '_WDN_' + IntegerToString(i))
        for j in range(0, 6):
            for i in range(0, 7):
                ObjectDelete(0, self.m_Name + '_D_' + IntegerToString(i) + '_' + IntegerToString(j))
        ObjectDelete(0, self.m_Name + '_CDM')
        ObjectDelete(0, self.m_Name + '_CD')
        ObjectDelete(0, self.m_Name + '_CDMB')
        ObjectDelete(0, self.m_Name + '_HL1')
        ObjectDelete(0, self.m_Name + '_CTM')
        ObjectDelete(0, self.m_Name + '_CT')
        ObjectDelete(0, self.m_Name + '_CTMB')
        ObjectDelete(0, self.m_Name + '_HL2')
        ObjectDelete(0, self.m_Name + '_Cancel')
        ObjectDelete(0, self.m_Name + '_Ok')
        ObjectDelete(0, self.m_Name + '_Line')
        ObjectDelete(0, self.m_Name + '_VLine')
        self.m_cb.Hide()
        self.m_sb.Hide()
        self.m_cb1.Hide()
        self.m_cb2.Hide()
        self.m_cb3.Hide()
    def MonthStartDayOfWeek(self, aMonth, aYear):
        m_sdate = IntegerToString(aYear) + '.' + IntegerToString(aMonth) + '.1'
        m_ddate = StringToTime(m_sdate)
        m_tstr = MqlDateTime()
        TimeToStruct(m_ddate, m_tstr)
        return m_tstr.day_of_week
    def DaysInMonth(self, aMonth, aYear):
        m_dim = Arr.of([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], fill=0)
        m_rv = m_dim[aMonth]
        if aMonth == 2 and _imod(aYear, 4) == 1:
            m_rv += 1
        return m_rv
    def SetCalendar(self):
        m_tn = ""
        i = 0
        j = 0
        j = 0
        for j in range(j, 6):
            i = 0
            for i in range(i, 7):
                m_tn = self.m_Name + '_D_' + IntegerToString(i) + '_' + IntegerToString(j)
                g.SetText_2(m_tn, '')
                g.SetColor_2(m_tn, self.m_TxtColor)
            else:
                i = _range_end(i, 7, 1)
        else:
            j = _range_end(j, 6, 1)
        m_m = self.m_cb.SelectedIndex() + 1
        m_y = _int(self.m_sb.Value())
        if m_y < 1970:
            return
        m_mswd = self.MonthStartDayOfWeek(m_m, m_y)
        if m_mswd == 1:
            j = 1
        else:
            j = 0
        i = m_mswd - 1
        if i < 0:
            i = 6
        m_NextDay = 0
        m_pm = m_m
        m_py = m_y
        m_pm -= 1
        if m_pm <= 0:
            m_pm = 12
            m_py -= 1
        m_NextDay = self.DaysInMonth(m_pm, m_py)
        m_bc = self.m_OtherMonthDayBgColor
        k = i - 1
        if k < 0:
            k = 6
        while k >= 0:
            m_tn = self.m_Name + '_D_' + IntegerToString(k) + '_' + IntegerToString(0)
            g.SetText_2(m_tn, IntegerToString(m_NextDay))
            self.m_Cell[k][0].Day = m_NextDay
            self.m_Cell[k][0].Month = m_pm
            self.m_Cell[k][0].Year = m_py
            g.SetBgColor_2(m_tn, m_bc)
            m_NextDay -= 1
            k -= 1
        m_ditm = self.DaysInMonth(m_m, m_y)
        m_bc = self.m_DayBgColor
        m_NextDay = 1
        m_NextMonth = False
        while j < 6:
            while i < 7:
                m_tn = self.m_Name + '_D_' + IntegerToString(i) + '_' + IntegerToString(j)
                g.SetText_2(m_tn, IntegerToString(m_NextDay))
                self.m_Cell[i][j].Day = m_NextDay
                self.m_Cell[i][j].Month = m_m + m_NextMonth
                self.m_Cell[i][j].Year = m_y
                g.SetBgColor_2(m_tn, m_bc)
                if m_NextDay == self.m_TimeStr.day:
                    if not m_NextMonth:
                        g.SetBgColor_2(m_tn, self.m_DayColor)
                if m_NextDay == m_ditm:
                    m_NextMonth = True
                    m_NextDay = 0
                    m_bc = self.m_OtherMonthDayBgColor
                m_NextDay += 1
                i += 1
            i = 0
            j += 1
        j = 0
        for j in range(j, 6):
            i = 0
            for i in range(i, 7):
                if (self.m_Cell[i][j].Day == self.m_ToDayStr.day and self.m_Cell[i][j].Month == self.m_ToDayStr.mon) and self.m_Cell[i][j].Year == self.m_ToDayStr.year:
                    m_tn = self.m_Name + '_D_' + IntegerToString(i) + '_' + IntegerToString(j)
                    g.Attach(m_tn)
                    m_t1 = g.BgColor_0()
                    m_t3 = g.XDistance_0()
                    m_t4 = g.YDistance_0()
                    m_t5 = g.Text_0()
                    m_t6 = g.XSize_0()
                    m_t7 = g.YSize_0()
                    g.Delete_0()
                    w.Edit(m_tn, self.m_SubWindow, m_t3, m_t4, m_t6, m_t7, m_t5, m_t1, self.m_ToDayColor)
                    g.SetReadOnly_2(m_tn, True)
            else:
                i = _range_end(i, 7, 1)
        else:
            j = _range_end(j, 6, 1)
    def SolveTime(self, aY, aM, aD, ah, am, as_):
        m_tstr = MqlDateTime()
        m_tstr.year = aY
        m_tstr.mon = aM
        m_tstr.day = aD
        m_tstr.hour = ah
        m_tstr.min = am
        m_tstr.sec = as_
        return StructToTime(m_tstr)
    def Init(self, aName='CCalendar', aDate=True, aTime=True, aSeconds=True, aLine=True, aTimeMode=0):
        self.m_TimeMode = aTimeMode
        self.m_Visible = False
        self.m_Date = aDate
        self.m_Time = aTime
        self.m_Sec = aSeconds
        self.m_Line = aLine
        self.m_Name = aName
        self.m_SubWindow = 0
        self.m_Left = 0
        self.m_Top = 0
        self.m_BgColor = ClrScheme.Color(45)
        self.m_BorderColor = ClrScheme.Color(46)
        self.m_ButBgColor = ClrScheme.Color(47)
        self.m_ButTxtColor = ClrScheme.Color(48)
        self.m_TxtColor = ClrScheme.Color(49)
        self.m_HeaderBgColor = ClrScheme.Color(50)
        self.m_DayBgColor = ClrScheme.Color(51)
        self.m_OtherMonthDayBgColor = ClrScheme.Color(52)
        self.m_DayColor = ClrScheme.Color(53)
        self.m_ToDayColor = ClrScheme.Color(54)
        self.m_cb.Init(aName + '_Month', 59, '')
        m_Month = Arr(0, "")
        if TerminalInfoString(TERMINAL_LANGUAGE) == 'Russian':
            StringSplit('Январь,Февраль,Maрт,Апрель,Май,Июнь,Июль,Август,Сентябрь,Октябрь,Ноябрь,Декабрь', 44, m_Month)
            self.m_NowText = 'Сейчас'
            self.m_ToDayText = 'Сегодня'
            self.m_LineText = 'Линия'
            StringSplit('Пн,Вт,Ср,Чт,Пт,Сб,Вс', 44, self.m_wdn)
        else:
            StringSplit('January,February,Mart,April,May,June,July,August,Septemb.,October,Novemb.,Decemb.', 44, m_Month)
            self.m_NowText = 'Now'
            self.m_ToDayText = 'Today'
            self.m_LineText = 'Line'
            StringSplit('Mo,Tu,We,Th,Fr,Sa,Su', 44, self.m_wdn)
        i = 0
        while i < ArraySize(m_Month):
            self.m_cb.AddItem(m_Month[i])
            i += 1
        self.m_sb.Init(aName + '_Year', 39, 1.0, '')
        self.m_sb.SetReadOnly(False)
        self.m_sb.SetMinValue(1970.0)
        self.m_cb1.Init(aName + '_Hour', 30, 'Ч')
        self.m_cb2.Init(aName + '_Min', 30, 'М')
        self.m_cb3.Init(aName + '_Sec', 30, 'С')
        self.m_cb1.SetReadOnly(False)
        self.m_cb2.SetReadOnly(False)
        self.m_cb3.SetReadOnly(False)
        for i in range(0, 24):
            self.m_cb1.AddItem(self.F2(i))
        for i in range(0, 60):
            self.m_cb2.AddItem(self.F2(i))
            self.m_cb3.AddItem(self.F2(i))
        self.SetValueDateTime(self.ModeTime())
        self.m_Tag = ''
    def TimeNowRefresh(self):
        if self.m_Visible:
            self.m_ToDay = self.ModeTime()
            TimeToStruct(self.m_ToDay, self.m_ToDayStr)
            if self.m_Time:
                m_fl = TIME_MINUTES
                if self.m_Sec:
                    m_fl = TIME_SECONDS
                g.SetText_2(self.m_Name + '_CT', self.m_NowText + ': ' + TimeToString(self.m_ToDay, m_fl))
            if self.m_Date:
                g.SetText_2(self.m_Name + '_CD', self.m_ToDayText + ': ' + TimeToString(self.m_ToDay, TIME_DATE))
            g.Redraw_0()
    def SetValueDateTime(self, aTime):
        self.m_TimeValue = aTime
        TimeToStruct(self.m_TimeValue, self.m_TimeStr)
        if not self.m_Date:
            self.m_TimeStr.day = 1
            self.m_TimeStr.year = 1970
            self.m_TimeStr.mon = 1
            self.m_TimeValue = StructToTime(self.m_TimeStr)
        if not self.m_Time:
            self.m_TimeStr.hour = 0
            self.m_TimeStr.min = 0
            self.m_TimeStr.sec = 0
            self.m_TimeValue = StructToTime(self.m_TimeStr)
        else:
            if not self.m_Sec:
                self.m_TimeStr.sec = 0
                self.m_TimeValue = StructToTime(self.m_TimeStr)
        if self.m_cb.SelectedIndex() != (self.m_TimeStr.mon - 1):
            self.m_cb.SetSelectedIndex(self.m_TimeStr.mon - 1)
        if self.m_sb.Value() != self.m_TimeStr.year:
            self.m_sb.SetValue(self.m_TimeStr.year)
        if self.m_cb1.SelectedIndex() != self.m_TimeStr.hour:
            self.m_cb1.SetSelectedIndex(self.m_TimeStr.hour)
        if self.m_cb2.SelectedIndex() != self.m_TimeStr.min:
            self.m_cb2.SetSelectedIndex(self.m_TimeStr.min)
        if self.m_cb3.SelectedIndex() != self.m_TimeStr.sec:
            self.m_cb3.SetSelectedIndex(self.m_TimeStr.sec)
        if self.m_Visible:
            self.SetCalendar()
            ChartRedraw(0)
    def DateTimeValue(self):
        return self.m_TimeValue
    def DateTimeString(self):
        m_ret = ''
        if self.m_Date:
            if self.m_Time:
                m_ret = TimeToString(self.m_TimeValue, TIME_DATE) + ' '
                if self.m_Sec:
                    m_ret += TimeToString(self.m_TimeValue, TIME_SECONDS)
                else:
                    m_ret += TimeToString(self.m_TimeValue, TIME_MINUTES)
            else:
                m_ret = TimeToString(self.m_TimeValue, TIME_DATE)
        else:
            if self.m_Time:
                if self.m_Sec:
                    m_ret = TimeToString(self.m_TimeValue, TIME_SECONDS)
                else:
                    m_ret = TimeToString(self.m_TimeValue, TIME_MINUTES)
            else:
                m_ret = ''
        return m_ret
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
    def SetPosTop(self, aTop):
        self.m_Top = aTop
    def Left(self, aLeft):
        return self.m_Left
    def Top(self, aTop):
        return self.m_Top
    def Width(self):
        return 140
    def Height(self):
        m_rv = 0
        if self.m_Date:
            m_rv = 117
        if self.m_Time:
            m_rv += 31
        m_rv += 19
        return m_rv
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        self.SetCalendar()
        self.TimeNowRefresh()
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        ChartRedraw()
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.Show_0()
    def Event(self, id_, lparam, dparam, sparam):
        m_NewTime = 0
        m_lineoff = False
        if self.m_cb1.Event(id_, lparam, dparam, sparam) == 1:
            self.m_cb1.SetSelectedIndex(MathMax(0, _int(MathMin(StringToInteger(self.m_cb1.Value()), 23))))
            m_NewTime = self.SolveTime(self.m_TimeStr.year, self.m_TimeStr.mon, self.m_TimeStr.day, self.m_cb1.SelectedIndex(), self.m_TimeStr.min, self.m_TimeStr.sec)
            self.SetValueDateTime(m_NewTime)
            m_lineoff = True
        if self.m_cb2.Event(id_, lparam, dparam, sparam) == 1:
            self.m_cb2.SetSelectedIndex(MathMax(0, _int(MathMin(StringToInteger(self.m_cb2.Value()), 59))))
            m_NewTime = self.SolveTime(self.m_TimeStr.year, self.m_TimeStr.mon, self.m_TimeStr.day, self.m_TimeStr.hour, self.m_cb2.SelectedIndex(), self.m_TimeStr.sec)
            self.SetValueDateTime(m_NewTime)
            m_lineoff = True
        if self.m_cb3.Event(id_, lparam, dparam, sparam) == 1:
            self.m_cb3.SetSelectedIndex(MathMax(0, _int(MathMin(StringToInteger(self.m_cb3.Value()), 59))))
            m_NewTime = self.SolveTime(self.m_TimeStr.year, self.m_TimeStr.mon, self.m_TimeStr.day, self.m_TimeStr.hour, self.m_TimeStr.min, self.m_cb3.SelectedIndex())
            self.SetValueDateTime(m_NewTime)
            m_lineoff = True
        if self.m_cb.Event(id_, lparam, dparam, sparam) == 1:
            m_NewTime = self.SolveTime(self.m_TimeStr.year, self.m_cb.SelectedIndex() + 1, self.m_TimeStr.day, self.m_TimeStr.hour, self.m_TimeStr.min, self.m_TimeStr.sec)
            self.SetValueDateTime(m_NewTime)
            m_lineoff = True
        if self.m_sb.Event(id_, lparam, dparam, sparam):
            m_NewTime = self.SolveTime(_int(self.m_sb.Value()), self.m_TimeStr.mon, self.m_TimeStr.day, self.m_TimeStr.hour, self.m_TimeStr.min, self.m_TimeStr.sec)
            self.SetValueDateTime(m_NewTime)
            m_lineoff = True
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if sparam == (self.m_Name + '_Ok'):
                Sleep(100)
                g.SetState_2(sparam, False)
                g.Redraw_0()
                Sleep(100)
                self.Hide()
                return 1
            if sparam == (self.m_Name + '_Cancel'):
                Sleep(100)
                g.SetState_2(sparam, False)
                g.Redraw_0()
                Sleep(100)
                self.Hide()
            if sparam == (self.m_Name + '_Left'):
                if g.State_1(sparam):
                    Sleep(50)
                    g.SetState_2(sparam, False)
                    if self.m_cb.SelectedIndex() > 0:
                        self.m_cb.SetSelectedIndex(self.m_cb.SelectedIndex() - 1)
                        m_NewTime = self.SolveTime(_int(self.m_sb.Value()), self.m_cb.SelectedIndex() + 1, self.m_TimeStr.day, self.m_TimeStr.hour, self.m_TimeStr.min, self.m_TimeStr.sec)
                        self.SetValueDateTime(m_NewTime)
                        m_lineoff = True
                    else:
                        if self.m_sb.Value() > 1970:
                            self.m_cb.SetSelectedIndex(11)
                            self.m_sb.SetValue(self.m_sb.Value() - 1)
                            m_NewTime = self.SolveTime(_int(self.m_sb.Value()), self.m_cb.SelectedIndex() + 1, self.m_TimeStr.day, self.m_TimeStr.hour, self.m_TimeStr.min, self.m_TimeStr.sec)
                            self.SetValueDateTime(m_NewTime)
                            m_lineoff = True
                    g.Redraw_0()
            if sparam == (self.m_Name + '_Right'):
                if g.State_1(sparam):
                    Sleep(50)
                    g.SetState_2(sparam, False)
                    if self.m_cb.SelectedIndex() < 11:
                        self.m_cb.SetSelectedIndex(self.m_cb.SelectedIndex() + 1)
                        m_NewTime = self.SolveTime(_int(self.m_sb.Value()), self.m_cb.SelectedIndex() + 1, self.m_TimeStr.day, self.m_TimeStr.hour, self.m_TimeStr.min, self.m_TimeStr.sec)
                        self.SetValueDateTime(m_NewTime)
                        m_lineoff = True
                    else:
                        self.m_cb.SetSelectedIndex(0)
                        self.m_sb.SetValue(self.m_sb.Value() + 1)
                        m_NewTime = self.SolveTime(_int(self.m_sb.Value()), self.m_cb.SelectedIndex() + 1, self.m_TimeStr.day, self.m_TimeStr.hour, self.m_TimeStr.min, self.m_TimeStr.sec)
                        self.SetValueDateTime(m_NewTime)
                        m_lineoff = True
                    g.Redraw_0()
            if StringFind(sparam, self.m_Name + '_D_', 0) == 0:
                m_prelen = StringLen(self.m_Name + '_D_')
                m_p1 = StringFind(sparam, '_', m_prelen)
                m_i = _int(StringToInteger(StringSubstr(sparam, m_prelen, m_p1 - m_prelen)))
                m_j = _int(StringToInteger(StringSubstr(sparam, m_p1 + 1, StringLen(sparam) - m_p1 - 1)))
                if self.m_Cell[m_i][m_j].Year >= 1970:
                    m_NewTime = self.SolveTime(self.m_Cell[m_i][m_j].Year, self.m_Cell[m_i][m_j].Month, self.m_Cell[m_i][m_j].Day, self.m_TimeStr.hour, self.m_TimeStr.min, self.m_TimeStr.sec)
                    if m_NewTime != self.m_TimeValue:
                        self.SetValueDateTime(m_NewTime)
                        m_lineoff = True
            if sparam == (self.m_Name + '_CDMB'):
                g.Attach(sparam)
                if g.State_0():
                    Sleep(50)
                    g.SetState_1(False)
                    m_NewTime = self.SolveTime(self.m_ToDayStr.year, self.m_ToDayStr.mon, self.m_ToDayStr.day, self.m_TimeStr.hour, self.m_TimeStr.min, self.m_TimeStr.sec)
                    if m_NewTime != self.m_TimeValue:
                        self.SetValueDateTime(m_NewTime)
                        m_lineoff = True
                    else:
                        ChartRedraw()
            if sparam == (self.m_Name + '_CTMB'):
                g.Attach(sparam)
                if g.State_0():
                    Sleep(50)
                    g.SetState_1(False)
                    m_NewTime = self.SolveTime(self.m_TimeStr.year, self.m_TimeStr.mon, self.m_TimeStr.day, self.m_ToDayStr.hour, self.m_ToDayStr.min, self.m_ToDayStr.sec)
                    if m_NewTime != self.m_TimeValue:
                        self.SetValueDateTime(m_NewTime)
                        m_lineoff = True
                    else:
                        ChartRedraw()
            if sparam == (self.m_Name + '_Line'):
                if g.State_1(sparam):
                    m_dta = Arr(1, 0, dyn=False)
                    m_bn = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR)) - _idiv(_int(ChartGetInteger(0, CHART_WIDTH_IN_BARS)), 2)
                    m_bn = MathMax(m_bn, 0)
                    if CopyTime(Symbol(), Period(), m_bn, 1, m_dta) == -1:
                        g.SetState_2(sparam, False)
                    else:
                        g.CreateVLine(self.m_Name + '_VLine')
                        g.SetColor_1(_uint(Red))
                        g.SetWidth_1(1)
                        g.SetStyle_1(STYLE_SOLID)
                        g.SetSelectable_1(True)
                        g.SetSelected_1(True)
                        g.SetRay_1(True)
                        g.SetBack_1(True)
                        g.SetTime_2(0, m_dta[0])
                        ChartRedraw()
                        self.SetValueDateTime(g.Time_1(0))
                else:
                    m_lineoff = True
            if m_lineoff:
                if g.State_1(self.m_Name + '_Line') or g.Find_1(self.m_Name + '_VLine') >= 0:
                    g.SetState_2(self.m_Name + '_Line', False)
                    g.Delete_1(self.m_Name + '_VLine')
                    g.Redraw_0()
        if id_ == CHARTEVENT_OBJECT_DRAG:
            if sparam == (self.m_Name + '_VLine'):
                self.SetValueDateTime(g.Time_2(sparam, 0))
                ChartRedraw()
        return 0
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.m_cb.SetSubWindow_1(self.m_SubWindow)
            self.m_sb.SetSubWindow_1(self.m_SubWindow)
            self.m_cb1.SetSubWindow_1(self.m_SubWindow)
            self.m_cb2.SetSubWindow_1(self.m_SubWindow)
            self.m_cb3.SetSubWindow_1(self.m_SubWindow)
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def SetTag(self, aTag):
        self.m_Tag = aTag
    def Tag(self, aTag):
        return self.m_Tag
    def Visible(self):
        return self.m_Visible

class m_SCellInfo(MqlObject):
    _q_fields = ('Year', 'Month', 'Day')
    def __init__(self, *args):
        self.Year = 0
        self.Month = 0
        self.Day = 0

class CCalendarInputBox(MqlObject):
    _q_fields = ('m_SubWindow', 'm_Left', 'm_Top', 'm_Width', 'm_Height', 'm_Name', 'm_DName', 'm_IName', 'm_BName', 'm_LName', 'm_Caption', 'm_d', 'm_ib', 'm_ColDBg', 'm_ColDTx', 'm_ColL', 'm_cc', 'm_Visible', 'm_Tag')
    def __init__(self, *args):
        self.m_SubWindow = 0
        self.m_Left = 0
        self.m_Top = 0
        self.m_Width = 0
        self.m_Height = 0
        self.m_Name = ""
        self.m_DName = ""
        self.m_IName = ""
        self.m_BName = ""
        self.m_LName = ""
        self.m_Caption = ""
        self.m_d = CCalendar()
        self.m_ib = CInputBox()
        self.m_ColDBg = 0
        self.m_ColDTx = 0
        self.m_ColL = 0
        self.m_cc = 0
        self.m_Visible = False
        self.m_Tag = ""
    def Create(self):
        w.Edit(self.m_BName, self.m_SubWindow, self.m_Left + self.m_Width - 13, self.m_Top, 13, self.m_Height, 'd', self.m_ColDBg, self.m_ColDTx, 7, 'Arial')
        g.SetReadOnly_2(self.m_BName, True)
        if self.m_Caption != '':
            w.Label(self.m_LName, self.m_SubWindow, self.m_Left + self.m_Width + 1, self.m_Top + 2, self.m_Caption, self.m_ColL, 7, 'Arial')
    def Delete(self):
        ObjectDelete(0, self.m_BName)
        ObjectDelete(0, self.m_LName)
    def Init(self, aName='CCalendarInput', aDate=True, aTime=True, aSeconds=True, aLine=True, aTimeMode=0, aCaption='CCalendarInput'):
        self.m_Name = aName
        self.m_ColDBg = ClrScheme.Color(4)
        self.m_ColDTx = ClrScheme.Color(1)
        self.m_ColL = ClrScheme.Color(2)
        if aDate:
            if aTime:
                if aSeconds:
                    self.m_Width = 105
                else:
                    self.m_Width = 90
            else:
                self.m_Width = 65
        else:
            if aTime:
                if aSeconds:
                    self.m_Width = 55
                else:
                    self.m_Width = 45
            else:
                self.m_Width = 105
        self.m_Visible = False
        self.m_Left = 0
        self.m_Top = 0
        self.m_Height = 15
        self.m_Caption = aCaption
        self.m_DName = aName + '_D'
        self.m_IName = aName + '_I'
        self.m_BName = aName + '_B'
        self.m_LName = aName + '_L'
        self.m_cc = 0
        self.m_Tag = ''
        self.m_ib.Init(self.m_IName, self.m_Width - 12, -1, '')
        self.m_ib.SetReadOnly(True)
        self.m_d.Init(self.m_DName, aDate, aTime, aSeconds, aLine, aTimeMode)
        self.m_ib.SetValue_1(self.m_d.DateTimeString())
    def SetReadOnly(self, aValue):
        self.m_ib.SetReadOnly(aValue)
    def ReadOnly(self):
        return self.m_ib.ReadOnly()
    def SetWidth(self, aValue):
        self.m_Width = aValue
        self.m_ib.SetWidth(self.m_Width - 12)
    def Width(self):
        return self.m_Width
    def Height(self):
        return self.m_Height
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def Refresh(self):
        if self.m_Visible:
            self.Delete()
            self.m_d.Hide()
            self.m_ib.Hide()
            self.Show_0()
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.m_ib.SetPos(self.m_Left, self.m_Top)
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
        self.m_ib.SetPosLeft(self.m_Left)
    def SetPosTop(self, aTop):
        self.m_Top = aTop
        self.m_ib.SetPosTop(self.m_Top)
    def Show_0(self):
        self.m_Visible = True
        self.Create()
        self.m_ib.Show_0()
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.Delete()
        self.m_d.Hide()
        self.m_ib.Hide()
    def ValueDateTime(self):
        return self.m_d.DateTimeValue()
    def ValueString(self):
        return self.m_d.DateTimeString()
    def SetValueDateTime(self, aDateTime):
        self.m_d.SetValueDateTime(aDateTime)
        self.m_ib.SetValue_1(self.m_d.DateTimeString())
    def Event(self, id_, lparam, dparam, sparam):
        m_event = 0
        if sparam == '':
            if id_ == CHARTEVENT_CLICK:
                self.m_cc += 1
                if self.m_cc >= 2:
                    if self.m_d.Visible():
                        self.m_d.Hide()
        else:
            self.m_cc = 0
            if self.m_ib.Event(id_, lparam, dparam, sparam) == 1:
                m_event = 1
            m_dev = self.m_d.Event(id_, lparam, dparam, sparam)
            if m_dev == 1:
                m_oldvalue = self.m_ib.ValueString()
                self.m_ib.SetValue_1(self.m_d.DateTimeString())
                if m_oldvalue != self.m_d.DateTimeString():
                    m_event = 1
                ChartRedraw()
            if id_ == CHARTEVENT_OBJECT_CLICK:
                if sparam == self.m_BName:
                    if self.m_d.Visible():
                        self.m_d.Hide()
                    else:
                        m_w = _idiv(_int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, self.m_SubWindow)), 2)
                        m_h = _idiv(_int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, self.m_SubWindow)), 2)
                        m_x = self.m_Left + _idiv(self.m_Width, 2)
                        m_y = self.m_Top + _idiv(self.m_Height, 2)
                        m_cx = 0
                        m_cy = 0
                        if m_x < m_w:
                            m_cx = self.m_Left
                        else:
                            m_cx = self.m_Left - self.m_d.Width() + self.m_Width
                        if m_y < m_h:
                            m_cy = self.m_Top + self.m_ib.Height() - 1
                        else:
                            m_cy = self.m_Top - self.m_d.Height() + 1
                        self.m_d.Show_2(m_cx, m_cy)
                else:
                    if m_dev != 2:
                        if self.m_d.Visible():
                            if StringFind(sparam, self.m_Name, 0) != 0:
                                self.m_d.Hide()
        return m_event
    def SetTag(self, aTag):
        self.m_Tag = aTag
    def Tag(self):
        return self.m_Tag
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.m_ib.SetSubWindow_1(self.m_SubWindow)
            self.m_d.SetSubWindow_1(self.m_SubWindow)
            self.Refresh()
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def Warning(self):
        return self.m_ib.Warning()
    def SetWarning(self, aValue):
        self.m_ib.SetWarning(aValue)
    def TimeNowRefresh(self):
        self.m_d.TimeNowRefresh()

class CFormBase(MqlObject):
    _q_fields = ('m_MainColor', 'm_BorderColor', 'm_TxtColor', 'm_UpperColor', 'm_LowerColor', 'm_UpperTxtColor', 'm_ButColor', 'm_Type', 'm_SubWindow', 'm_Name', 'm_Width', 'm_Height', 'm_Left', 'm_Top', 'm_Caption', 'm_MoveMode', 'm_Tc', 'm_State', 'm_Tag', 'm_Movable', 'm_Resizable', 'm_CloseButton', 'm_SpaceLeft', 'm_SpaceTop', 'm_Visible')
    def __init__(self, *args):
        self.m_MainColor = 0
        self.m_BorderColor = 0
        self.m_TxtColor = 0
        self.m_UpperColor = 0
        self.m_LowerColor = 0
        self.m_UpperTxtColor = 0
        self.m_ButColor = 0
        self.m_Type = 0
        self.m_SubWindow = 0
        self.m_Name = ""
        self.m_Width = 0
        self.m_Height = 0
        self.m_Left = 0
        self.m_Top = 0
        self.m_Caption = ""
        self.m_MoveMode = False
        self.m_Tc = 0
        self.m_State = 0
        self.m_Tag = ""
        self.m_Movable = False
        self.m_Resizable = False
        self.m_CloseButton = False
        self.m_SpaceLeft = 0
        self.m_SpaceTop = 0
        self.m_Visible = False
    def OnShowEvent(self, aLeft, aTop):
        pass
    def OnHideEvent(self):
        pass
    def EventsHandler(self, id_, lparam, dparam, sparam):
        pass
    def OnCancelEvent(self):
        return True
    def OnApplyEvent(self):
        return True
    def MainProperties(self):
        pass
    def OnInitEvent(self):
        pass
    def OnWindowChangeEvent(self, aSubWindow):
        pass
    def PosCorrection(self):
        m_chw = _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, self.m_SubWindow))
        m_chh = _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, self.m_SubWindow))
        if m_chw <= 0 or m_chh <= 0:
            return False
        m_mxleft = m_chw - self.Width()
        m_mxtop = m_chh - self.Height()
        m_oldleft = self.m_Left
        m_oldtop = self.m_Top
        self.m_Left = MathMin(self.m_Left, m_mxleft)
        self.m_Left = MathMax(self.m_Left, 0)
        self.m_Top = MathMin(self.m_Top, m_mxtop)
        self.m_Top = MathMax(self.m_Top, 0)
        self.m_SpaceLeft = self.m_Left
        self.m_SpaceTop = self.m_Top + 16
        return m_oldleft != self.m_Left or m_oldtop != self.m_Top
    def CreateForm(self):
        if self.m_State == 0:
            return
        self.PosCorrection()
        if self.m_State != 2:
            w.Canvas(self.m_Name + '_Form', self.m_SubWindow, self.m_Left, self.m_Top, self.m_Width, self.m_Height, self.m_MainColor, self.m_BorderColor)
        w.Canvas(self.m_Name + '_Upper', self.m_SubWindow, self.m_Left, self.m_Top, self.m_Width, 17, self.m_UpperColor, self.m_BorderColor)
        m_xshift = 15
        if self.m_CloseButton:
            w.Button(self.m_Name + '_Close', self.m_SubWindow, self.m_Left + self.m_Width - 15, self.m_Top + 2, 13, 13, CharToString(251), self.m_ButColor, self.m_TxtColor, 10, 'Wingdings')
            m_xshift = 29
        if self.m_Resizable:
            w.Button(self.m_Name + '_Min', self.m_SubWindow, self.m_Left + self.m_Width - m_xshift, self.m_Top + 2, 13, 13, CharToString(168), self.m_ButColor, self.m_TxtColor, 7, 'Wingdings')
        m_xshift = 4
        if self.m_Movable:
            w.Button(self.m_Name + '_Move', self.m_SubWindow, self.m_Left + 2, self.m_Top + 2, 13, 13, CharToString(73), self.m_ButColor, self.m_TxtColor, 8, 'Wingdings')
            m_xshift = 16
        w.Label(self.m_Name + '_Caption', self.m_SubWindow, self.m_Left + m_xshift, self.m_Top + 2, self.m_Caption, self.m_UpperTxtColor)
        if self.m_State != 2:
            _sw3 = self.m_Type
            if _sw3 == 1:
                w.Canvas(self.m_Name + '_Lower', self.m_SubWindow, self.m_Left, self.m_Top + self.m_Height - 18, self.m_Width, 18, self.m_LowerColor, self.m_BorderColor)
                w.Button(self.m_Name + '_Apply', self.m_SubWindow, self.m_Left + self.m_Width - 42, self.m_Top + self.m_Height - 16, 40, 14, 'Apply', self.m_ButColor, self.m_TxtColor)
                w.Button(self.m_Name + '_Cancel', self.m_SubWindow, self.m_Left + 2, self.m_Top + self.m_Height - 16, 40, 14, 'Cancel', self.m_ButColor, self.m_TxtColor)
            elif _sw3 == 2:
                w.Canvas(self.m_Name + '_Lower', self.m_SubWindow, self.m_Left, self.m_Top + self.m_Height - 18, self.m_Width, 18, self.m_LowerColor, self.m_BorderColor)
                w.Button(self.m_Name + '_Cancel', self.m_SubWindow, self.m_Left + _idiv(self.m_Width, 2) - 20, self.m_Top + self.m_Height - 16, 40, 14, 'Close', self.m_ButColor, self.m_TxtColor)
            self.OnShowEvent(self.m_SpaceLeft, self.m_SpaceTop)
    def DeleteForm(self):
        self.OnHideEvent()
        ObjectDelete(0, self.m_Name + '_Form')
        ObjectDelete(0, self.m_Name + '_Upper')
        ObjectDelete(0, self.m_Name + '_Close')
        ObjectDelete(0, self.m_Name + '_Min')
        ObjectDelete(0, self.m_Name + '_Move')
        ObjectDelete(0, self.m_Name + '_Caption')
        ObjectDelete(0, self.m_Name + '_Lower')
        ObjectDelete(0, self.m_Name + '_Apply')
        ObjectDelete(0, self.m_Name + '_Cancel')
    def ChartClickY(self, aDparam, aY):
        hs = 0
        ps = 0
        i = 0
        while i < ChartGetInteger(0, CHART_WINDOWS_TOTAL):
            hs += 3 + ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, i)
            if hs >= aDparam:
                aY.v = _int(aDparam - ps - 3)
                break
            ps = hs
            i += 1
    def WhenChartResize(self):
        if self.m_State != 0:
            if self.PosCorrection():
                self.Refresh()
    def Init(self, aState=1):
        self.m_Visible = False
        self.m_SubWindow = 0
        self.m_MainColor = ClrScheme.Color(32)
        self.m_BorderColor = ClrScheme.Color(33)
        self.m_ButColor = ClrScheme.Color(34)
        self.m_TxtColor = ClrScheme.Color(35)
        self.m_UpperColor = ClrScheme.Color(36)
        self.m_LowerColor = ClrScheme.Color(37)
        self.m_UpperTxtColor = ClrScheme.Color(38)
        self.m_Tag = ''
        self.m_MoveMode = False
        self.m_State = aState
        self.m_SpaceLeft = 0
        self.m_SpaceTop = 16
        self.MainProperties()
        self.OnInitEvent()
    def SetPos(self, aLeft, aTop):
        self.m_Left = aLeft
        self.m_Top = aTop
        self.m_SpaceLeft = self.m_Left
        self.m_SpaceTop = self.m_Top + 16
    def SetPosLeft(self, aLeft):
        self.m_Left = aLeft
        self.m_SpaceLeft = self.m_Left
    def SetPosTop(self, aTop):
        self.m_Top = aTop
        self.m_SpaceTop = self.m_Top + 16
    def Show_0(self):
        self.m_Visible = True
        self.CreateForm()
        ChartRedraw()
    def Show_2(self, aLeft, aTop):
        self.SetPos(aLeft, aTop)
        self.Show_0()
    def Hide(self):
        self.m_Visible = False
        self.DeleteForm()
        ChartRedraw(0)
    def Refresh(self):
        if self.m_State != 0:
            self.DeleteForm()
            self.CreateForm()
            ChartRedraw()
    def Width(self):
        return self.m_Width
    def Height(self):
        _sw4 = self.m_State
        if _sw4 == 1:
            return self.HeightMax()
        elif _sw4 == 2:
            return self.HeightMin()
        return 0
    def HeightMax(self):
        return self.m_Height
    def HeightMin(self):
        return 17
    def Left(self):
        return self.m_Left
    def Top(self):
        return self.m_Top
    def SetState(self, aState=1):
        if aState >= 1 and aState <= 2:
            self.m_State = aState
            if self.m_Visible:
                self.Refresh()
    def State(self):
        return self.m_State
    def Name(self):
        return self.m_Name
    def Caption(self):
        return self.m_Caption
    def SetTag(self, aTag):
        self.m_Tag = aTag
    def Tag(self, aTag):
        return self.m_Tag
    def SetSubWindow_1(self, aNumber):
        m_itmp = MathMax(aNumber, 0)
        if m_itmp != self.m_SubWindow:
            self.m_SubWindow = m_itmp
            self.m_MoveMode = False
            if self.m_Visible:
                self.Hide()
                self.OnWindowChangeEvent(m_itmp)
                self.Show_0()
            else:
                self.OnWindowChangeEvent(m_itmp)
    def SetSubWindow_2(self, aName):
        self.SetSubWindow_1(ChartWindowFind(0, aName))
    def Event(self, id_, lparam, dparam, sparam):
        m_rv = 0
        if not self.m_MoveMode:
            self.EventsHandler(id_, lparam, dparam, sparam)
            if id_ == CHARTEVENT_OBJECT_CLICK:
                if sparam == (self.m_Name + '_Form'):
                    m_rv = 4
                if sparam == (self.m_Name + '_Close'):
                    Sleep(150)
                    g.Attach(self.m_Name + '_Close')
                    g.SetState_1(False)
                    g.Redraw_0()
                    Sleep(150)
                    if self.OnCancelEvent():
                        self.Hide()
                        m_rv = 1
                if sparam == (self.m_Name + '_Cancel'):
                    Sleep(150)
                    g.Attach(self.m_Name + '_Cancel')
                    g.SetState_1(False)
                    g.Redraw_0()
                    Sleep(150)
                    if self.OnCancelEvent():
                        self.Hide()
                        m_rv = 1
                if sparam == (self.m_Name + '_Apply'):
                    Sleep(150)
                    g.Attach(self.m_Name + '_Apply')
                    g.SetState_1(False)
                    g.Redraw_0()
                    Sleep(150)
                    if self.OnApplyEvent():
                        self.Hide()
                        m_rv = 2
                if sparam == (self.m_Name + '_Min'):
                    Sleep(150)
                    g.Attach(self.m_Name + '_Min')
                    g.SetState_1(False)
                    g.Redraw_0()
                    Sleep(150)
                    if self.m_State == 1:
                        self.SetState(2)
                    elif self.m_State == 2:
                        self.SetState(1)
                    m_rv = 3
        if sparam == (self.m_Name + '_Move'):
            g.Attach(self.m_Name + '_Move')
            self.m_MoveMode = g.State_0()
            self.m_Tc = GetTickCount()
        if id_ == CHARTEVENT_CLICK:
            if self.m_MoveMode:
                if GetTickCount() > (self.m_Tc + 300):
                    self.m_MoveMode = False
                    m_Y = Box(0)
                    self.ChartClickY(dparam, m_Y)
                    self.SetPos(_int(lparam) - 3, m_Y.v)
                    self.Refresh()
        if CHARTEVENT_CHART_CHANGE:
            self.WhenChartResize()
        return m_rv

class CFormTemplate(CFormBase):
    _q_fields = ()
    def __init__(self, *args):
        CFormBase.__init__(self)
    def MainProperties(self):
        self.m_Name = 'Form'
        self.m_Width = 200
        self.m_Height = 150
        self.m_Type = 1
        self.m_Caption = 'FormCaption'
        self.m_Movable = True
        self.m_Resizable = True
        self.m_CloseButton = True
    def OnInitEvent(self):
        pass
    def OnShowEvent(self, aLeft, aTop):
        pass
    def OnHideEvent(self):
        pass
    def OnWindowChangeEvent(self, aSubWindow):
        pass
    def EventsHandler(self, id_, lparam, dparam, sparam):
        pass
    def OnApplyEvent(self):
        return True
    def OnCancelEvent(self):
        return True

def OnInit():
    g.CreateLabel(ObjName, 0, 0)
    g.SetColor_2(ObjName, FontColor)
    g.SetFontSize_2(ObjName, FontSize)
    g.SetCorner_2(ObjName, Corner)
    g.SetXYDistance_3(ObjName, PosX, PosY)
    if Corner == CORNER_LEFT_UPPER:
        g.SetAnchor_2(ObjName, ANCHOR_LEFT_UPPER)
    if Corner == CORNER_LEFT_LOWER:
        g.SetAnchor_2(ObjName, ANCHOR_LEFT_LOWER)
    if Corner == CORNER_RIGHT_UPPER:
        g.SetAnchor_2(ObjName, ANCHOR_RIGHT_UPPER)
    if Corner == CORNER_RIGHT_LOWER:
        g.SetAnchor_2(ObjName, ANCHOR_RIGHT_LOWER)
    EventSetTimer(1)
    return 0

def OnDeinit(reason):
    g.Delete_1(ObjName)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global BarTime
    BarTime = time[rates_total - 1]
    OnTimer()
    return rates_total

def OnTimer():
    if Period() == PERIOD_W1 or Period() == PERIOD_MN1:
        return
    if BarTime == 0:
        g.SetText_2(ObjName, 'Waiting for price change...')
        return
    tc = TimeCurrent()
    tf = tc - BarTime
    tt = PeriodSeconds(Period()) - tf
    if tt < 0:
        g.SetText_2(ObjName, 'Waiting for a new bar opening...')
        return
    g.SetText_2(ObjName, TimeToString(tc, TIME_SECONDS) + ' - ' + TimeToString(tf, TIME_SECONDS) + ' - ' + TimeToString(tt, TIME_SECONDS))

# ---- global variables initialised from expressions
g = _alloc(CGraphicObjectShell)
g.__init__()
w = _alloc(CWorkPiece)
w.__init__()
ClrScheme = _alloc(CColorSchemes)
ClrScheme.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IsimpleclockV2(_MQL5Indicator):
    name = 'isimpleclock_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FontSize': 8,
        'Corner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=2),
        'PosX': 0,
        'PosY': 0,
    }

