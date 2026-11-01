"""Pips Percentage — converted from MQL5: MQL5 Indicators/Price Percentage and Times on cursor crosshair/Pips Percentage.mq5

Copyright: Ludovico Mattiuzzo; Link: no-one; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Ludovico Mattiuzzo', 'link': 'no-one', 'version': '1.01', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Pips Percentage', 'source': 'MQL5 Indicators/Price Percentage and Times on cursor crosshair/Pips Percentage.mq5', 'folder': 'Price Percentage and Times on cursor crosshair', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


class PipsPercentage(MqlObject):
    _q_fields = ('MY_TEXT', 'MY_TEXT_BKG', 'CrossHairVisible', 'BeginDrag', 'startPrice', 'startTime', 'chartWidth')
    def __init__(self):
        self.MY_TEXT = ""
        self.MY_TEXT_BKG = ""
        self.CrossHairVisible = False
        self.BeginDrag = False
        self.startPrice = 0.0
        self.startTime = 0
        self.chartWidth = 0
        self.MY_TEXT = 'CROSS_PIPS_PCT'
        self.MY_TEXT_BKG = 'CROSS_PIPS_PCT_RECT'
        self.startPrice = -1.0
        ObjectDelete(0, self.MY_TEXT)
        ObjectDelete(0, self.MY_TEXT_BKG)
    def handleMouseEvent(self, id_, lparam, dparam, sparam):
        if id_ == CHARTEVENT_MOUSE_MOVE:
            subWindow = Box(0)
            if sparam == '16':
                self.CrossHairVisible = True
            if sparam == '1' and self.CrossHairVisible:
                if self.startPrice < 0:
                    ChartXYToTimePrice(0, _int(lparam), _int(dparam), subWindow, _AttrRef(self, 'startTime'), _AttrRef(self, 'startPrice'))
                self.BeginDrag = True
            if sparam != '1' and self.BeginDrag:
                self.BeginDrag = False
                self.CrossHairVisible = False
                self.hideLabel()
                self.startPrice = -1.0
            if self.CrossHairVisible and self.BeginDrag:
                currentPrice = Box(0.0)
                currentTime = Box(0)
                ChartXYToTimePrice(0, _int(lparam), _int(dparam), subWindow, currentTime, currentPrice)
                pct = ''
                if currentPrice.v > self.startPrice:
                    pct = DoubleToString((_fdiv(currentPrice.v, self.startPrice) - 1) * 100, 2) + '%'
                else:
                    pct = DoubleToString((1 - _fdiv(self.startPrice, currentPrice.v)) * 100, 2) + '%'
                timeSpan = MathAbs(currentTime.v - self.startTime)
                timeSpanStr = ""
                if _idiv(timeSpan, 60) < 60:
                    timeSpanStr = IntegerToString(_idiv(timeSpan, 60)) + ' min'
                elif _idiv(timeSpan, 3600) < 24:
                    timeSpanStr = IntegerToString(_idiv(timeSpan, 3600)) + ' hours'
                elif (_idiv(timeSpan, 3600) / 24.0) < 100:
                    timeSpanStr = DoubleToString(_idiv(timeSpan, 3600) / 24.0, 1) + ' days'
                elif _fdiv(_idiv(timeSpan, 3600), 30 * 24.0) < 19:
                    timeSpanStr = DoubleToString(_fdiv(_idiv(timeSpan, 3600), 30 * 24.0), 1) + ' months'
                else:
                    timeSpanStr = DoubleToString(_fdiv(_idiv(timeSpan, 3600), 365 * 24.0), 1) + ' years'
                self.showLabel(StringFormat('%s / %s', pct, timeSpanStr), MathMin(self.chartWidth - 80, _int(lparam) + 5), _int(dparam) - 15)
        elif id_ == CHARTEVENT_CHART_CHANGE:
            self.setChartWidth()
    def setChartWidth(self):
        self.chartWidth = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0)
    def showLabel(self, text, x, y):
        if ObjectFind(0, self.MY_TEXT) < 0:
            foregroundColor = Box(clrNONE)
            backgroundColor = Box(clrNONE)
            ChartGetInteger(0, CHART_COLOR_FOREGROUND, 0, foregroundColor)
            ChartGetInteger(0, CHART_COLOR_BACKGROUND, 0, backgroundColor)
            self.RectLabelCreate(0, self.MY_TEXT_BKG, 0, x - 2, y, 80, 18, backgroundColor.v, BORDER_FLAT, CORNER_LEFT_UPPER)
            ObjectCreate(0, self.MY_TEXT, OBJ_LABEL, 0, 0, 0)
            ObjectSetInteger(0, self.MY_TEXT, OBJPROP_XDISTANCE, x)
            ObjectSetInteger(0, self.MY_TEXT, OBJPROP_YDISTANCE, y)
            ObjectSetString(0, self.MY_TEXT, OBJPROP_TEXT, text)
            ObjectSetInteger(0, self.MY_TEXT, OBJPROP_CORNER, CORNER_LEFT_UPPER)
            ObjectSetInteger(0, self.MY_TEXT, OBJPROP_COLOR, _uint(foregroundColor.v))
            ObjectSetInteger(0, self.MY_TEXT, OBJPROP_FONTSIZE, 7)
            ObjectSetInteger(0, self.MY_TEXT, OBJPROP_SELECTABLE, False)
            ObjectSetInteger(0, self.MY_TEXT, OBJPROP_HIDDEN, True)
            ObjectSetInteger(0, self.MY_TEXT, OBJPROP_BACK, False)
        else:
            ObjectSetString(0, self.MY_TEXT, OBJPROP_TEXT, text)
            ObjectSetInteger(0, self.MY_TEXT, OBJPROP_XDISTANCE, x)
            ObjectSetInteger(0, self.MY_TEXT, OBJPROP_YDISTANCE, y)
            ObjectSetInteger(0, self.MY_TEXT_BKG, OBJPROP_XDISTANCE, x)
            ObjectSetInteger(0, self.MY_TEXT_BKG, OBJPROP_YDISTANCE, y)
    def hideLabel(self):
        if ObjectFind(0, self.MY_TEXT) >= 0:
            ObjectDelete(0, self.MY_TEXT)
        if ObjectFind(0, self.MY_TEXT_BKG) >= 0:
            ObjectDelete(0, self.MY_TEXT_BKG)
        ChartRedraw()
    def RectLabelCreate(self, chart_ID=0, name='RectLabel', sub_window=0, x=0, y=0, width=50, height=18, back_clr=0xD8E9EC, border=BORDER_SUNKEN, corner=CORNER_LEFT_UPPER, clr=clrRed, style=STYLE_SOLID, line_width=0, back=False, selection=False, hidden=True, z_order=255):
        ResetLastError()
        if not ObjectCreate(chart_ID, name, OBJ_RECTANGLE_LABEL, sub_window, 0, 0):
            Print('PipsPercentage::RectLabelCreate', ': failed to create a rectangle label! Error code = ', GetLastError())
            return False
        ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
        ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
        ObjectSetInteger(chart_ID, name, OBJPROP_XSIZE, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_YSIZE, height)
        ObjectSetInteger(chart_ID, name, OBJPROP_BGCOLOR, back_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BORDER_TYPE, border)
        ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
        ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, line_width)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        return True

def OnInit():
    ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, 0, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    pipsPercentage.handleMouseEvent(id_, lparam, dparam, sparam)

# ---- global variables initialised from expressions
pipsPercentage = _alloc(PipsPercentage)
pipsPercentage.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PipsPercentageIndicator(_MQL5Indicator):
    name = 'Pips Percentage'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

