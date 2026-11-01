"""CGraphBase.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class CGraphBase(MqlObject):
    _q_fields = ('m_name', 'm_id', 'm_subwin', 'm_delete')
    def __init__(self, aName='', aID=0, aSubWin=0, a_delete=True):
        self.m_name = ""
        self.m_id = 0
        self.m_subwin = 0
        self.m_delete = False
        self.m_name = aName
        self.m_id = aID
        self.m_subwin = aSubWin
        self.m_delete = a_delete
    def _q_dtor(self):
        if self.m_delete:
            self.Deinit()
    def Deinit(self):
        if not self.Delete():
            Print('CGraphBase::Deinit', ': ATTENTION! CAN NOT DELETE ', self.m_name)
    def CreateLabel(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_LABEL, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateLabel', ': OBJ_LABEL. Error Code = ', GetLastError())
            return False
        return True
    def CreateBitmap_0(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_BITMAP, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateBitmap', ': OBJ_BITMAP. Error Code = ', GetLastError())
            return False
        return True
    def CreateBitmap_2(self, aTime=0, aPrice=0.0):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_BITMAP, self.m_subwin, aTime, aPrice):
            Print('CGraphBase::CreateBitmap', ': OBJ_BITMAP. Error Code = ', GetLastError())
            return False
        return True
    def CreateBitmapLabel(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_BITMAP_LABEL, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateBitmapLabel', ': OBJ_BITMAP_LABEL. Error Code = ', GetLastError())
            return False
        return True
    def CreateText(self, aTime=0, aPrice=0.0):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_TEXT, self.m_subwin, aTime, aPrice):
            Print('CGraphBase::CreateText', ': OBJ_TEXT. Error Code = ', GetLastError())
            return False
        return True
    def CreateButton(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_BUTTON, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateButton', ': OBJ_BUTTON. Error Code = ', GetLastError())
            return False
        return True
    def CreateEdit(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_EDIT, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateEdit', ': OBJ_EDIT. Error Code = ', GetLastError())
            return False
        return True
    def CreateVLine(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_VLINE, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateVLine', ': OBJ_VLINE. Error Code = ', GetLastError())
            return False
        return True
    def CreateHLine(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_HLINE, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateHLine', ': OBJ_HLINE. Error Code = ', GetLastError())
            return False
        return True
    def CreateTrend(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_TREND, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateTrend', ': OBJ_TREND. Error Code = ', GetLastError())
            return False
        return True
    def CreateTrendByAngle(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_TRENDBYANGLE, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateTrendByAngle', ': OBJ_TRENDBYANGLE. Error Code = ', GetLastError())
            return False
        return True
    def CreateEvent(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_EVENT, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateEvent', ': OBJ_EVENT. Error Code = ', GetLastError())
            return False
        return True
    def CreateRectangle_0(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_RECTANGLE, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateRectangle', ': OBJ_RECTANGLE(void). Error Code = ', GetLastError())
            return False
        return True
    def CreateRectangle_4(self, aTime1=0, aPrice1=0.0, aTime2=0, aPrice2=0.0):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_RECTANGLE, self.m_subwin, aTime1, aPrice1, aTime2, aPrice2):
            Print('CGraphBase::CreateRectangle', ': OBJ_RECTANGLE(times&prices). Error Code = ', GetLastError())
            return False
        return True
    def CreateRectangleLabel(self):
        ResetLastError()
        if not ObjectCreate(self.m_id, self.m_name, OBJ_RECTANGLE_LABEL, self.m_subwin, 0, 0):
            Print('CGraphBase::CreateRectangleLabel', ': OBJ_RECTANGLE_LABEL. Error Code = ', GetLastError())
            return False
        return True
    def Name(self):
        return self.m_name
    def Chart_ID(self):
        self.m_id = ChartID()
        return self.m_id
    def SubWindow(self):
        return self.m_subwin
    def SetText(self, aValue):
        ResetLastError()
        if not ObjectSetString(self.m_id, self.m_name, OBJPROP_TEXT, aValue):
            Print('CGraphBase::SetText', ': . Error Code = ', GetLastError())
            return False
        return True
    def SetFont(self, aValue):
        ResetLastError()
        if not ObjectSetString(self.m_id, self.m_name, OBJPROP_FONT, aValue):
            Print('CGraphBase::SetFont', ': OBJPROP_TEXT. Error Code = ', GetLastError())
            return False
        return True
    def SetCorner(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_CORNER, aValue):
            Print('CGraphBase::SetCorner', ': OBJPROP_CORNER. Error Code = ', GetLastError())
            return False
        return True
    def SetFontSize(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_FONTSIZE, aValue):
            Print('CGraphBase::SetFontSize', ': OBJPROP_FONTSIZE. Error Code = ', GetLastError())
            return False
        return True
    def SetColor(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_COLOR, aValue):
            Print('CGraphBase::SetColor', ': OBJPROP_COLOR. Error Code = ', GetLastError())
            return False
        return True
    def SetBgColor(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_BGCOLOR, aValue):
            Print('CGraphBase::SetBgColor', ': OBJPROP_BGCOLOR. Error Code = ', GetLastError())
            return False
        return True
    def SetBorderColor(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_BORDER_COLOR, aValue):
            Print('CGraphBase::SetBorderColor', ': OBJPROP_BORDER_COLOR. Error Code = ', GetLastError())
            return False
        return True
    def SetXSize(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_XSIZE, aValue):
            Print('CGraphBase::SetXSize', ': OBJPROP_XSIZE. Error Code = ', GetLastError())
            return False
        return True
    def SetYSize(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_YSIZE, aValue):
            Print('CGraphBase::SetYSize', ': OBJPROP_YSIZE. Error Code = ', GetLastError())
            return False
        return True
    def SetXDistance(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_XDISTANCE, aValue):
            Print('CGraphBase::SetXDistance', ': OBJPROP_XDISTANCE. Error Code = ', GetLastError())
            return False
        return True
    def SetYDistance(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_YDISTANCE, aValue):
            Print('CGraphBase::SetYDistance', ': OBJPROP_YDISTANCE. Error Code = ', GetLastError())
            return False
        return True
    def SetSelected(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_SELECTED, aValue):
            Print('CGraphBase::SetSelected', ': OBJPROP_SELECTED. Error Code = ', GetLastError())
            return False
        return True
    def SetSelectable(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_SELECTABLE, aValue):
            Print('CGraphBase::SetSelectable', ': OBJPROP_SELECTABLE. Error Code = ', GetLastError())
            return False
        return True
    def SetZOrder(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_ZORDER, aValue):
            Print('CGraphBase::SetZOrder', ': OBJPROP_ZORDER. Error Code = ', GetLastError())
            return False
        return True
    def SetReadOnly(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_READONLY, aValue):
            Print('CGraphBase::SetReadOnly', ': OBJPROP_READONLY. Error Code = ', GetLastError())
            return False
        return True
    def SetAligh(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_ALIGN, aValue):
            Print('CGraphBase::SetAligh', ': OBJPROP_ALIGN. Error Code = ', GetLastError())
            return False
        return True
    def SetNoTip(self, aValue):
        ResetLastError()
        if not ObjectSetString(self.m_id, self.m_name, OBJPROP_TOOLTIP, aValue):
            Print('CGraphBase::SetNoTip', ': OBJPROP_TOOLTIP. Error Code = ', GetLastError())
            return False
        return True
    def SetTimeFrames(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_TIMEFRAMES, aValue):
            Print('CGraphBase::SetTimeFrames', ': OBJPROP_TIMEFRAMES. Error Code = ', GetLastError())
            return False
        return True
    def SetStyle(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_STYLE, aValue):
            Print('CGraphBase::SetStyle', ': OBJPROP_STYLE. Error Code = ', GetLastError())
            return False
        return True
    def SetWidth(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_WIDTH, aValue):
            Print('CGraphBase::SetWidth', ': OBJPROP_WIDTH. Error Code = ', GetLastError())
            return False
        return True
    def SetAnchor(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_ANCHOR, aValue):
            Print('CGraphBase::SetAnchor', ': OBJPROP_ANCHOR. Error Code = ', GetLastError())
            return False
        return True
    def SetBorderType(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_BORDER_TYPE, aValue):
            Print('CGraphBase::SetBorderType', ': OBJPROP_BORDER_TYPE. Error Code = ', GetLastError())
            return False
        return True
    def SetBack(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_BACK, aValue):
            Print('CGraphBase::SetBack', ': OBJPROP_BACK. Error Code = ', GetLastError())
            return False
        return True
    def SetState(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_STATE, aValue):
            Print('CGraphBase::SetState', ': OBJPROP_STATE. Error Code = ', GetLastError())
            return False
        return True
    def SetFill(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_FILL, aValue):
            Print('CGraphBase::SetFill', ': OBJPROP_FILL. Error Code = ', GetLastError())
            return False
        return True
    def SetTime(self, aIndex, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_TIME, aIndex, aValue):
            Print('CGraphBase::SetTime', ': OBJPROP_TIME. Error Code = ', GetLastError())
            return False
        return True
    def SetLevels(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_LEVELS, aValue):
            Print('CGraphBase::SetLevels', ': OBJPROP_LEVELS. Error Code = ', GetLastError())
            return False
        return True
    def SetLevelColor(self, aIndex, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_LEVELCOLOR, aIndex, aValue):
            Print('CGraphBase::SetLevelColor', ': OBJPROP_LEVELCOLOR. Error Code = ', GetLastError())
            return False
        return True
    def SetLevelStyle(self, aIndex, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_LEVELSTYLE, aIndex, aValue):
            Print('CGraphBase::SetLevelStyle', ': OBJPROP_LEVELSTYLE. Error Code = ', GetLastError())
            return False
        return True
    def SetLevelWidth(self, aIndex, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_LEVELWIDTH, aIndex, aValue):
            Print('CGraphBase::SetLevelWidth', ': OBJPROP_LEVELWIDTH. Error Code = ', GetLastError())
            return False
        return True
    def SetRayRight(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_RAY_RIGHT, aValue):
            Print('CGraphBase::SetRayRight', ': OBJPROP_RAY_RIGHT. Error Code = ', GetLastError())
            return False
        return True
    def SetRay(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_RAY, aValue):
            Print('CGraphBase::SetRay', ': OBJPROP_RAY. Error Code = ', GetLastError())
            return False
        return True
    def SetEllipse(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_ELLIPSE, aValue):
            Print('CGraphBase::SetEllipse', ': OBJPROP_ELLIPSE. Error Code = ', GetLastError())
            return False
        return True
    def SetArrowCode(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_ARROWCODE, aValue):
            Print('CGraphBase::SetArrowCode', ': OBJPROP_ARROWCODE. Error Code = ', GetLastError())
            return False
        return True
    def SetDirection(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_DIRECTION, aValue):
            Print('CGraphBase::SetDirection', ': OBJPROP_DIRECTION. Error Code = ', GetLastError())
            return False
        return True
    def SetDrawLines(self, aValue):
        pass
    def SetXOffset(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_XOFFSET, aValue):
            Print('CGraphBase::SetXOffset', ': OBJPROP_XOFFSET. Error Code = ', GetLastError())
            return False
        return True
    def SetYOffset(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_YOFFSET, aValue):
            Print('CGraphBase::SetYOffset', ': OBJPROP_YOFFSET. Error Code = ', GetLastError())
            return False
        return True
    def SetPeriod(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_PERIOD, aValue):
            Print('CGraphBase::SetPeriod', ': OBJPROP_PERIOD. Error Code = ', GetLastError())
            return False
        return True
    def SetDateScale(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_DATE_SCALE, aValue):
            Print('CGraphBase::SetDateScale', ': OBJPROP_DATE_SCALE. Error Code = ', GetLastError())
            return False
        return True
    def SetPriceScale(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_PRICE_SCALE, aValue):
            Print('CGraphBase::SetPriceScale', ': OBJPROP_PRICE_SCALE. Error Code = ', GetLastError())
            return False
        return True
    def SetChartScale(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_CHART_SCALE, aValue):
            Print('CGraphBase::SetChartScale', ': OBJPROP_CHART_SCALE. Error Code = ', GetLastError())
            return False
        return True
    def SetPrice(self, aIndex, aValue):
        ResetLastError()
        if not ObjectSetDouble(self.m_id, self.m_name, OBJPROP_PRICE, aIndex, aValue):
            Print('CGraphBase::SetPrice', ': OBJPROP_PRICE. Error Code = ', GetLastError())
            return False
        return True
    def SetLevelValue(self, aIndex, aValue):
        ResetLastError()
        if not ObjectSetDouble(self.m_id, self.m_name, OBJPROP_LEVELVALUE, aIndex, aValue):
            Print('CGraphBase::SetLevelValue', ': OBJPROP_LEVELVALUE. Error Code = ', GetLastError())
            return False
        return True
    def SetScale(self, aValue):
        ResetLastError()
        if not ObjectSetDouble(self.m_id, self.m_name, OBJPROP_SCALE, aValue):
            Print('CGraphBase::SetScale', ': OBJPROP_SCALE. Error Code = ', GetLastError())
            return False
        return True
    def SetAngle(self, aValue):
        ResetLastError()
        if not ObjectSetDouble(self.m_id, self.m_name, OBJPROP_ANGLE, aValue):
            Print('CGraphBase::SetAngle', ': OBJPROP_ANGLE. Error Code = ', GetLastError())
            return False
        return True
    def SetDeviation(self, aValue):
        ResetLastError()
        if not ObjectSetDouble(self.m_id, self.m_name, OBJPROP_DEVIATION, aValue):
            Print('CGraphBase::SetDeviation', ': OBJPROP_DEVIATION. Error Code = ', GetLastError())
            return False
        return True
    def SetToolTip(self, aValue):
        ResetLastError()
        if not ObjectSetString(self.m_id, self.m_name, OBJPROP_TOOLTIP, aValue):
            Print('CGraphBase::SetToolTip', ': OBJPROP_TOOLTIP. Error Code = ', GetLastError())
            return False
        return True
    def SetLevelText(self, aIndex, aValue):
        ResetLastError()
        if not ObjectSetString(self.m_id, self.m_name, OBJPROP_LEVELTEXT, aIndex, aValue):
            Print('CGraphBase::SetLevelText', ': OBJPROP_LEVELTEXT. Error Code = ', GetLastError())
            return False
        return True
    def SetBmpFile(self, aValue):
        ResetLastError()
        if not ObjectSetString(self.m_id, self.m_name, OBJPROP_BMPFILE, aValue):
            Print('CGraphBase::SetBmpFile', ': OBJPROP_BMPFILE. Error Code = ', GetLastError())
            return False
        return True
    def SetBmpFileOn(self, aValue):
        ResetLastError()
        if not ObjectSetString(self.m_id, self.m_name, OBJPROP_BMPFILE, 0, aValue):
            Print('CGraphBase::SetBmpFileOn', ': OBJPROP_BMPFILE. Error Code = ', GetLastError())
            return False
        return True
    def SetBmpFileOff(self, aValue):
        ResetLastError()
        if not ObjectSetString(self.m_id, self.m_name, OBJPROP_BMPFILE, 1, aValue):
            Print('CGraphBase::SetBmpFileOff', ': OBJPROP_BMPFILE. Error Code = ', GetLastError())
            return False
        return True
    def SetSymbol(self, aValue):
        ResetLastError()
        if not ObjectSetString(self.m_id, self.m_name, OBJPROP_SYMBOL, aValue):
            Print('CGraphBase::SetSymbol', ': OBJPROP_SYMBOL. Error Code = ', GetLastError())
            return False
        return True
    def SetHidden(self, aValue):
        ResetLastError()
        if not ObjectSetInteger(self.m_id, self.m_name, OBJPROP_HIDDEN, aValue):
            Print('CGraphBase::SetHidden', ': OBJPROP_HIDDEN. Error Code = ', GetLastError())
            return False
        return True
    def SetTimePrice(self, aIndex, aTime, aPrice):
        ResetLastError()
        if not ObjectMove(self.m_id, self.m_name, aIndex, aTime, aPrice):
            Print('CGraphBase::SetTimePrice', ': ObjectMove. Error Code = ', GetLastError())
            return False
        return True
    def Color(self):
        return _uint(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_COLOR))
    def Style(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_STYLE)
    def Width(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_WIDTH))
    def Back(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_BACK))
    def Fill(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_FILL))
    def Selected(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_SELECTED))
    def ReadOnly(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_READONLY))
    def Type(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_TYPE)
    def Time(self, aIndex):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_TIME, aIndex)
    def Selectable(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_SELECTABLE))
    def CreateTime(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_CREATETIME)
    def Levels(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_LEVELS))
    def LevelColor(self, aIndex):
        return _uint(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_LEVELCOLOR, aIndex))
    def LevelStyle(self, aIndex):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_LEVELSTYLE, aIndex)
    def LevelWidth(self, aIndex):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_LEVELWIDTH, aIndex))
    def FontSize(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_FONTSIZE))
    def RayLeft(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_RAY_LEFT))
    def RayRight(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_RAY_RIGHT))
    def Ray(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_RAY))
    def Ellipse(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_ELLIPSE))
    def ArrowCode(self):
        return _char(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_ARROWCODE))
    def TimeFrames(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_TIMEFRAMES)
    def Anchor(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_ANCHOR)
    def XDistance(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_XDISTANCE))
    def YDistance(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_YDISTANCE))
    def Direction(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_DIRECTION)
    def State(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_STATE))
    def ChartChartID(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_CHART_ID))
    def XSize(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_XSIZE))
    def YSize(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_YSIZE))
    def XOffset(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_XOFFSET))
    def YOffset(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_YOFFSET))
    def Period(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_PERIOD)
    def DateScale(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_DATE_SCALE))
    def PriceScale(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_PRICE_SCALE))
    def ChartScale(self):
        return _int(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_CHART_SCALE))
    def BgColor(self):
        return _uint(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_BGCOLOR))
    def Corner(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_CORNER)
    def BorderType(self):
        return ObjectGetInteger(self.m_id, self.m_name, OBJPROP_BORDER_TYPE)
    def Price(self, aIndex):
        return ObjectGetDouble(self.m_id, self.m_name, OBJPROP_PRICE, aIndex)
    def LevelValue(self, aIndex):
        return ObjectGetDouble(self.m_id, self.m_name, OBJPROP_LEVELVALUE, aIndex)
    def Scale(self):
        return ObjectGetDouble(self.m_id, self.m_name, OBJPROP_SCALE)
    def Angle(self):
        return ObjectGetDouble(self.m_id, self.m_name, OBJPROP_ANGLE)
    def Deviation(self):
        return ObjectGetDouble(self.m_id, self.m_name, OBJPROP_DEVIATION)
    def Text(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_TEXT)
    def ToolTip(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_TOOLTIP)
    def LevelText(self, aIndex):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_LEVELTEXT, aIndex)
    def Font(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_FONT)
    def BmpFile(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_BMPFILE)
    def BmpFileOn(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_BMPFILE, 0)
    def BmpFileOff(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_BMPFILE, 1)
    def GraphSymbol(self):
        return ObjectGetString(self.m_id, self.m_name, OBJPROP_SYMBOL)
    def Hidden(self):
        return _bool(ObjectGetInteger(self.m_id, self.m_name, OBJPROP_HIDDEN))
    def ChartWidth(self):
        return _int(ChartGetInteger(self.m_id, CHART_WIDTH_IN_PIXELS, self.m_subwin))
    def ChartHeight(self):
        return _int(ChartGetInteger(self.m_id, CHART_HEIGHT_IN_PIXELS, self.m_subwin))
    def ChartWidthWithError(self):
        result = Box(-1)
        ResetLastError()
        if not ChartGetInteger(self.m_id, CHART_WIDTH_IN_PIXELS, self.m_subwin, result):
            Alert('CGraphBase::ChartWidthWithError' + ', Error Code = ', GetLastError())
        return _int(result.v)
    def ChartHeightWithError(self):
        result = Box(-1)
        ResetLastError()
        if not ChartGetInteger(self.m_id, CHART_HEIGHT_IN_PIXELS, self.m_subwin, result):
            Print('CGraphBase::ChartHeightWithError', ': CHART_HEIGHT_IN_PIXELS. Error Code = ', GetLastError())
        return _int(result.v)
    def Delete(self):
        ResetLastError()
        if not ObjectDelete(self.m_id, self.m_name):
            Print('CGraphBase::Delete', ': Object Delete Error Code = ', GetLastError())
            return False
        return True
    def Redraw(self):
        ChartRedraw(self.m_id)

__all__ = ['CGraphBase']
