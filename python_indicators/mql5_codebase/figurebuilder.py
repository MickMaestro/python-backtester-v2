"""FigureBuilder — converted from MQL5: MQL5 Indicators/FigureBuilder/FigureBuilder.mq5

Copyright: 2017, Progid.; Link: https://www.mql5.com/en/users/progid/; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.0', 'copyright': '2017, Progid.', 'link': 'https://www.mql5.com/en/users/progid/', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'FigureBuilder', 'source': 'MQL5 Indicators/FigureBuilder/FigureBuilder.mq5', 'folder': 'FigureBuilder', 'inputs': [{'mql': 'Prefix_', 'py': 'Prefix_', 'param': None, 'type': 'string', 'default': 'Figure', 'label': 'Objects prefix name', 'sinput': False}, {'mql': '_dots_', 'py': '_dots_', 'param': None, 'type': 'string', 'default': '------- Dot -------', 'label': ':', 'sinput': False}, {'mql': 'DotsMax_', 'py': 'DotsMax_', 'param': 'DotsMax_', 'type': 'uint', 'default': 5, 'label': '[2...]Dots Max Number', 'sinput': False}, {'mql': 'DotEmptyArowCode_', 'py': 'DotEmptyArowCode_', 'param': 'DotEmptyArowCode_', 'type': 'uchar', 'default': 161, 'label': 'Empty Dot Code', 'sinput': False}, {'mql': 'DotEmptySize_', 'py': 'DotEmptySize_', 'param': 'DotEmptySize_', 'type': 'uint', 'default': 4, 'label': 'Empty Dot Width', 'sinput': False}, {'mql': 'DotFillArowCode_', 'py': 'DotFillArowCode_', 'param': 'DotFillArowCode_', 'type': 'uchar', 'default': 108, 'label': 'Filled Dot Code', 'sinput': False}, {'mql': 'DotFillSize_', 'py': 'DotFillSize_', 'param': 'DotFillSize_', 'type': 'uint', 'default': 2, 'label': 'Filled Dot Width', 'sinput': False}, {'mql': '_line_', 'py': '_line_', 'param': None, 'type': 'string', 'default': '------- Line -------', 'label': ':', 'sinput': False}, {'mql': 'LineLeftRay_', 'py': 'LineLeftRay_', 'param': 'LineLeftRay_', 'type': 'bool', 'default': False, 'label': 'First Dot Line Left Ray', 'sinput': False}, {'mql': 'LineRightRay_', 'py': 'LineRightRay_', 'param': 'LineRightRay_', 'type': 'bool', 'default': False, 'label': 'Last Dot Line Right Ray', 'sinput': False}, {'mql': 'LineColor_', 'py': 'LineColor_', 'param': None, 'type': 'color', 'default': 255, 'label': 'Lines color', 'sinput': False}, {'mql': 'LineStyle_', 'py': 'LineStyle_', 'param': 'LineStyle_', 'type': 'int', 'default': 0, 'label': 'Lines Style', 'sinput': False}, {'mql': 'LineWidth_', 'py': 'LineWidth_', 'param': 'LineWidth_', 'type': 'uchar', 'default': 1, 'label': 'Lines Width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Prefix_ = _input('Prefix_', 'Figure')  # Objects prefix name
_dots_ = _input('_dots_', '------- Dot -------')  # :
DotsMax_ = _input('DotsMax_', 5)  # [2...]Dots Max Number
DotEmptyArowCode_ = _input('DotEmptyArowCode_', 161)  # Empty Dot Code
DotEmptySize_ = _input('DotEmptySize_', 4)  # Empty Dot Width
DotFillArowCode_ = _input('DotFillArowCode_', 108)  # Filled Dot Code
DotFillSize_ = _input('DotFillSize_', 2)  # Filled Dot Width
_line_ = _input('_line_', '------- Line -------')  # :
LineLeftRay_ = _input('LineLeftRay_', False)  # First Dot Line Left Ray
LineRightRay_ = _input('LineRightRay_', False)  # Last Dot Line Right Ray
LineColor_ = _input('LineColor_', clrRed)  # Lines color
LineStyle_ = _input('LineStyle_', STYLE_SOLID)  # Lines Style
LineWidth_ = _input('LineWidth_', 1)  # Lines Width
_Prefix = ""

class sDot(MqlObject):
    _q_fields = ('_ObjName', '_Number', '_Time', '_Price')
    def __init__(self, *args):
        self._ObjName = ""
        self._Number = 0
        self._Time = 0
        self._Price = 0.0
    def _q_assign(self, source):
        self._ObjName = source._ObjName
        self._Number = source._Number
        self._Time = source._Time
        self._Price = source._Price

class cFigureBuilder(MqlObject):
    _q_fields = ('_LastFigureID', '_DotsMax', '_LastDotsCount', '_ChronologyBuf', '_ChronologyBufRS', '_ChronologySize')
    def __init__(self, *args):
        self._LastFigureID = 0
        self._DotsMax = 0
        self._LastDotsCount = 0
        self._ChronologyBuf = Arr(0, 0, factory=sDot)
        self._ChronologyBufRS = 0
        self._ChronologySize = 0
    def Init(self, dots_max):
        self._LastFigureID = GetTickCount()
        self._DotsMax = fmax(dots_max, 2)
        self._LastDotsCount = 0
        self._ChronologySize = 0
        self._ChronologyBufRS = 1
        if ArrayResize(self._ChronologyBuf, self._ChronologySize, self._ChronologyBufRS) != 0:
            Print('Error: ', '', ' line: ' + _str(85) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::Init' + '; GetLastError: ' + _str(GetLastError()))
            return False
        return True
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == CHARTEVENT_CLICK:
            CtrlKeyState = TerminalInfoInteger(TERMINAL_KEYSTATE_CONTROL)
            if CtrlKeyState == -128 or CtrlKeyState == -127:
                X = _int(lparam)
                Y = _int(dparam)
                self.AddDot(X, Y)
        elif id_ == CHARTEVENT_KEYDOWN:
            if lparam == 8:
                CtrlKeyState = TerminalInfoInteger(TERMINAL_KEYSTATE_CONTROL)
                if CtrlKeyState == -128 or CtrlKeyState == -127:
                    if not self.DeleteLastDot():
                        Print('Error: ', '', ' line: ' + _str(121) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::OnEvent' + '; GetLastError: ' + _str(GetLastError()))
                    ChartRedraw()
            elif lparam == 46:
                CtrlKeyState = TerminalInfoInteger(TERMINAL_KEYSTATE_CONTROL)
                if CtrlKeyState == -128 or CtrlKeyState == -127:
                    ObjectsDeleteAll(0, _Prefix, 0)
                    ChartRedraw()
    def AddDot(self, x, y):
        AxtSubW = Box(0)
        ActTime = Box(0)
        ActPrice = Box(0.0)
        if not ChartXYToTimePrice(0, x, y, AxtSubW, ActTime, ActPrice):
            Print('Error: ', 'x:' + _str(x) + ' y:' + _str(y), ' line: ' + _str(151) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::AddDot' + '; GetLastError: ' + _str(GetLastError()))
            return False
        if AxtSubW.v != 0:
            return False
        ActTime.v = ActTime.v + _idiv(PeriodSeconds(Period()), 2)
        TimeBuf = Arr(0, 0)
        if CopyTime(Symbol(), Period(), _DT(ActTime.v), 1, TimeBuf) != 1:
            Print('Error: ', 'CopyTime', ' line: ' + _str(162) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::AddDot' + '; GetLastError: ' + _str(GetLastError()))
            return False
        ActTime.v = TimeBuf[0]
        for c in range(0, self._LastDotsCount):
            if (self._ChronologySize - c - 1) < 0:
                break
            if self._ChronologyBuf[self._ChronologySize - c - 1]._Time == ActTime.v:
                Print('Warning: this bar has a dot!')
                return False
        ObjName = _Prefix + 'fig[' + _str(self._LastFigureID + 1) + ']:dot[' + _str(self._LastDotsCount) + ']'
        NewDot = sDot()
        NewDot._ObjName = ObjName
        NewDot._Number = self._LastDotsCount
        NewDot._Time = ActTime.v
        NewDot._Price = ActPrice.v
        if not self.AddToChronology_1(NewDot):
            Print('Error: ', '', ' line: ' + _str(188) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::AddDot' + '; GetLastError: ' + _str(GetLastError()))
            return False
        ObjectDelete(0, ObjName)
        PixelSize = self.GetPixelSize()
        if not ObjectCreate(0, ObjName, OBJ_ARROW, 0, ActTime.v, ActPrice.v + (4 * PixelSize) + (DotEmptySize_ * 3 * PixelSize)):
            Print('Error: ', '', ' line: ' + _str(194) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::AddDot' + '; GetLastError: ' + _str(GetLastError()))
            return False
        if not ObjectSetInteger(0, ObjName, OBJPROP_ARROWCODE, DotEmptyArowCode_):
            Print('Error: ', '', ' line: ' + _str(196) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::AddDot' + '; GetLastError: ' + _str(GetLastError()))
        if not ObjectSetInteger(0, ObjName, OBJPROP_WIDTH, DotEmptySize_):
            Print('Error: ', '', ' line: ' + _str(197) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::AddDot' + '; GetLastError: ' + _str(GetLastError()))
        ChartRedraw()
        self._LastDotsCount += 1
        self._LastFigureID += 1
        if self._LastDotsCount >= self._DotsMax:
            if not self.FigureBuild():
                Print('Error: ', '', ' line: ' + _str(208) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::AddDot' + '; GetLastError: ' + _str(GetLastError()))
                return False
        return True
    def FigureBuild(self):
        PixelSize = self.GetPixelSize()
        LinesNames = Arr(0, "")
        ArrayResize(LinesNames, self._LastDotsCount - 1)
        c = 0
        while c < (self._LastDotsCount - 1):
            Dot1 = _copy(self._ChronologyBuf[self._ChronologySize - self._LastDotsCount + c])
            Dot2 = _copy(self._ChronologyBuf[self._ChronologySize - self._LastDotsCount + c + 1])
            ObjName = _Prefix + 'fig[' + _str(self._LastFigureID) + ']:line[' + _str(c - 1) + ']'
            LinesNames[c] = ObjName
            if not ObjectCreate(0, ObjName, OBJ_TREND, 0, Dot1._Time, Dot1._Price, Dot2._Time, Dot2._Price):
                Print('Error: ', '', ' line: ' + _str(235) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
                self._LastDotsCount = 0
                return False
            if not ObjectSetInteger(0, ObjName, OBJPROP_RAY_LEFT, (LineLeftRay_ if (c == 0) else False)):
                Print('Error: ', '', ' line: ' + _str(238) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            if not ObjectSetInteger(0, ObjName, OBJPROP_RAY_RIGHT, (LineRightRay_ if (c == (self._LastDotsCount - 2)) else False)):
                Print('Error: ', '', ' line: ' + _str(239) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            if not ObjectSetInteger(0, ObjName, OBJPROP_COLOR, LineColor_):
                Print('Error: ', '', ' line: ' + _str(240) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            if not ObjectSetInteger(0, ObjName, OBJPROP_STYLE, LineStyle_):
                Print('Error: ', '', ' line: ' + _str(241) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            if not ObjectSetInteger(0, ObjName, OBJPROP_WIDTH, LineWidth_):
                Print('Error: ', '', ' line: ' + _str(242) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            if not ObjectSetInteger(0, Dot1._ObjName, OBJPROP_ARROWCODE, DotFillArowCode_):
                Print('Error: ', '', ' line: ' + _str(245) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            if not ObjectSetInteger(0, Dot1._ObjName, OBJPROP_WIDTH, DotFillSize_):
                Print('Error: ', '', ' line: ' + _str(246) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            if not ObjectSetDouble(0, Dot1._ObjName, OBJPROP_PRICE, Dot1._Price + (4 * PixelSize) + (DotFillSize_ * 3 * PixelSize)):
                Print('Error: ', '', ' line: ' + _str(247) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            if not ObjectSetInteger(0, Dot2._ObjName, OBJPROP_ARROWCODE, DotFillArowCode_):
                Print('Error: ', '', ' line: ' + _str(249) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            if not ObjectSetInteger(0, Dot2._ObjName, OBJPROP_WIDTH, DotFillSize_):
                Print('Error: ', '', ' line: ' + _str(250) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            if not ObjectSetDouble(0, Dot2._ObjName, OBJPROP_PRICE, Dot2._Price + (4 * PixelSize) + (DotFillSize_ * 3 * PixelSize)):
                Print('Error: ', '', ' line: ' + _str(251) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            ChartRedraw()
            c += 1
        c = 0
        while c < (self._LastDotsCount - 1):
            if not self.AddToChronology_2(LinesNames[c]):
                Print('Error: ', '', ' line: ' + _str(261) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::FigureBuild' + '; GetLastError: ' + _str(GetLastError()))
            c += 1
        self._LastDotsCount = 0
        return True
    def AddToChronology_1(self, dot):
        if self._ChronologyBufRS <= (self._ChronologySize + 1):
            self._ChronologyBufRS = _int(ceil((self._ChronologySize + 1) * 1.3))
        if ArrayResize(self._ChronologyBuf, self._ChronologySize + 1, self._ChronologyBufRS) != (self._ChronologySize + 1):
            Print('Error: ', '', ' line: ' + _str(277) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::AddToChronology' + '; GetLastError: ' + _str(GetLastError()))
            return False
        _assign(self._ChronologyBuf[self._ChronologySize], dot)
        self._ChronologySize += 1
        return True
    def AddToChronology_2(self, obj_name):
        if self._ChronologyBufRS <= (self._ChronologySize + 1):
            self._ChronologyBufRS = _int(ceil((self._ChronologySize + 1) * 1.3))
        if ArrayResize(self._ChronologyBuf, self._ChronologySize + 1, self._ChronologyBufRS) != (self._ChronologySize + 1):
            Print('Error: ', '', ' line: ' + _str(292) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::AddToChronology' + '; GetLastError: ' + _str(GetLastError()))
            return False
        self._ChronologyBuf[self._ChronologySize]._ObjName = obj_name
        self._ChronologyBuf[self._ChronologySize]._Number = 0
        self._ChronologyBuf[self._ChronologySize]._Time = 0
        self._ChronologyBuf[self._ChronologySize]._Price = 0.0
        self._ChronologySize += 1
        return True
    def DeleteLastDot(self):
        PixelSize = self.GetPixelSize()
        for i in range(self._ChronologySize - 1, 0 - 1, -1):
            IsLine = False
            DotNumber = -1
            if self._ChronologySize > 0:
                IsLine = self._ChronologyBuf[self._ChronologySize - 1]._Time == 0
                DotNumber = self._ChronologyBuf[self._ChronologySize - 1]._Number
                ObjName = self._ChronologyBuf[self._ChronologySize - 1]._ObjName
                if ObjectDelete(0, ObjName):
                    ChartRedraw()
                    self._ChronologySize -= 1
                    if ArrayResize(self._ChronologyBuf, self._ChronologySize, self._ChronologyBufRS) != self._ChronologySize:
                        Print('Error: ', 'ArrayResize', ' line: ' + _str(328) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::DeleteLastDot' + '; GetLastError: ' + _str(GetLastError()))
                        return False
                else:
                    Print('Error: ', '!ObjectDelete(' + ObjName + ')', ' line: ' + _str(330) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::DeleteLastDot' + '; GetLastError: ' + _str(GetLastError()))
                    return False
            if not IsLine:
                if self._LastDotsCount > 0:
                    self._LastDotsCount -= 1
                elif self._ChronologySize > 0:
                    self._LastDotsCount = self._DotsMax - 1
                    i1 = self._ChronologySize - 1
                    c = 0
                    while i1 >= 0 and c < self._LastDotsCount:
                        if self._ChronologyBuf[self._ChronologySize - 1]._Time == 0:
                            Print('Error: ', '', ' line: ' + _str(345) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::DeleteLastDot' + '; GetLastError: ' + _str(GetLastError()))
                            return False
                            break
                        if not ObjectSetInteger(0, self._ChronologyBuf[i1]._ObjName, OBJPROP_ARROWCODE, DotEmptyArowCode_):
                            Print('Error: ', '', ' line: ' + _str(349) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::DeleteLastDot' + '; GetLastError: ' + _str(GetLastError()))
                        if not ObjectSetInteger(0, self._ChronologyBuf[i1]._ObjName, OBJPROP_WIDTH, DotEmptySize_):
                            Print('Error: ', '', ' line: ' + _str(350) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::DeleteLastDot' + '; GetLastError: ' + _str(GetLastError()))
                        if not ObjectSetDouble(0, self._ChronologyBuf[i1]._ObjName, OBJPROP_PRICE, self._ChronologyBuf[i1]._Price + (4 * PixelSize) + (DotEmptySize_ * 3 * PixelSize)):
                            Print('Error: ', '', ' line: ' + _str(351) + ' file: ' + 'cFigureBuilder.mqh' + ' function: ' + 'cFigureBuilder::DeleteLastDot' + '; GetLastError: ' + _str(GetLastError()))
                        i1 -= 1
                        c += 1
                break
        return True
    def GetPixelSize(self):
        ActChartHeightPx = _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS))
        ActChartHeightPr = ChartGetDouble(0, CHART_PRICE_MAX) - ChartGetDouble(0, CHART_PRICE_MIN)
        return _fdiv(ActChartHeightPr, fmax(ActChartHeightPx, 1))

def OnInit():
    global _Prefix
    _Prefix = (Prefix_ if (Prefix_ != '') else 'Figure') + ':'
    if not _Builder.Init(DotsMax_):
        Print('Error: ', '', ' line: ' + _str(85) + ' file: ' + 'FigureBuilder.mq5' + ' function: ' + 'OnInit' + '; GetLastError: ' + _str(GetLastError()))
        return INIT_FAILED
    Print('Monitoring Started.')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Print('Monitoring Completed.')

def OnChartEvent(id_, lparam, dparam, sparam):
    _Builder.OnEvent(id_, lparam, dparam, sparam)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return 0

# ---- global variables initialised from expressions
_Builder = _alloc(cFigureBuilder)
_Builder.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FigureBuilder(_MQL5Indicator):
    name = 'FigureBuilder'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DotsMax_': 5,  # [2...]Dots Max Number
        'DotEmptyArowCode_': 161,  # Empty Dot Code
        'DotEmptySize_': 4,  # Empty Dot Width
        'DotFillArowCode_': 108,  # Filled Dot Code
        'DotFillSize_': 2,  # Filled Dot Width
        'LineLeftRay_': False,  # First Dot Line Left Ray
        'LineRightRay_': False,  # Last Dot Line Right Ray
        'LineStyle_': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Lines Style
        'LineWidth_': 1,  # Lines Width
    }

