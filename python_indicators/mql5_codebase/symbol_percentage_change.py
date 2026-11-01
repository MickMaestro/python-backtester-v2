"""Symbol_Percentage_Change — converted from MQL5: MQL5 Indicators/Symbol Percentage Change & Time/Symbol_Percentage_Change.mq5

Showing the Symbol Name, Last closing price and percentage change at the chart
Copyright: Copyright © 2021, Dark Ryd3r; Link: http://www.darkryd3r.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2021, Dark Ryd3r', 'link': 'http://www.darkryd3r.com', 'version': '1.0', 'indicator_buffers': 1, 'indicator_plots': 1, 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Showing the Symbol Name, Last closing price and percentage change at the chart'], 'name': 'Symbol_Percentage_Change', 'source': 'MQL5 Indicators/Symbol Percentage Change & Time/Symbol_Percentage_Change.mq5', 'folder': 'Symbol Percentage Change & Time', 'inputs': [{'mql': 'CurrentTime', 'py': 'CurrentTime', 'param': 'CurrentTime', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'inpTextColorPositive', 'py': 'inpTextColorPositive', 'param': None, 'type': 'color', 'default': 10408790, 'label': 'Positive Color', 'sinput': False}, {'mql': 'inpTextColorNegative', 'py': 'inpTextColorNegative', 'param': None, 'type': 'color', 'default': 9639167, 'label': 'Negative Color', 'sinput': False}, {'mql': 'inpFontType', 'py': 'inpFontType', 'param': 'inpFontType', 'type': 'int', 'default': 1, 'label': 'Font Type', 'sinput': False}, {'mql': 'inpWindowPosition', 'py': 'inpWindowPosition', 'param': 'inpWindowPosition', 'type': 'int', 'default': 2, 'label': 'Symbol position', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ML_WINPOSITION
ML_WINPOSITION_UPPER_LEFT = 0
ML_WINPOSITION_UPPER_CENTER = 1
ML_WINPOSITION_UPPER_RIGHT = 2
ML_WINPOSITION_LOWER_LEFT = 3
ML_WINPOSITION_LOWER_CENTER = 4
ML_WINPOSITION_LOWER_RIGHT = 5
_enum('ML_WINPOSITION', {0: 'ML_WINPOSITION_UPPER_LEFT', 1: 'ML_WINPOSITION_UPPER_CENTER', 2: 'ML_WINPOSITION_UPPER_RIGHT', 3: 'ML_WINPOSITION_LOWER_LEFT', 4: 'ML_WINPOSITION_LOWER_CENTER', 5: 'ML_WINPOSITION_LOWER_RIGHT'})

# enum ML_FONTTYPE
ML_FONTTYPE_ARIAL = 0
ML_FONTTYPE_ARIALBLACK = 1
ML_FONTTYPE_VERDANA = 2
ML_FONTTYPE_TAHOMA = 3
ML_FONTTYPE_COURIERNEW = 4
ML_FONTTYPE_LUCIDACONSOLE = 5
_enum('ML_FONTTYPE', {0: 'ML_FONTTYPE_ARIAL', 1: 'ML_FONTTYPE_ARIALBLACK', 2: 'ML_FONTTYPE_VERDANA', 3: 'ML_FONTTYPE_TAHOMA', 4: 'ML_FONTTYPE_COURIERNEW', 5: 'ML_FONTTYPE_LUCIDACONSOLE'})

# enum TimeSelect
Current = 0
GMT = 1
Local = 2
_enum('TimeSelect', {0: 'Current', 1: 'GMT', 2: 'Local'})

# ---- inputs and global variables
DPCBuffer = Arr(0, 0.0)
C = 0.0
O = 0.0
leftTime = 0
sTime = ""
days = 0
sCurrentTime = ""
CurrentTime = _input('CurrentTime', GMT)
inpTextColorPositive = _input('inpTextColorPositive', 0x9ED356)  # Positive Color
inpTextColorNegative = _input('inpTextColorNegative', clrDeepPink)  # Negative Color
inpFontType = _input('inpFontType', 1)  # Font Type
inpFontSize = 14  # Symbol Font size
inpWindowPosition = _input('inpWindowPosition', ML_WINPOSITION_UPPER_RIGHT)  # Symbol position
inpXOffSet = -35  # Reposition Symbol Offset on X axis (+/-)
inpYOffSet = 10  # Reposition Symbol Offset on Y axis (+/-)
gmt = ""
_SymbolName = 'SymbolBackground'  # Namespacing the Symbol Background...
_CurWindowWidth = 0  # holds the current Chart width

def OnInit():
    SetIndexBuffer(0, DPCBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DPCBuffer, True)

def OnDeinit(reason):
    ObjectDelete(0, _SymbolName)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global C, O, gmt, leftTime, sCurrentTime
    if rates_total < _idiv(1440, Period()):
        return 0
    i = rates_total - 1
    if prev_calculated > 0:
        i = rates_total - prev_calculated - 1
    if i < 0:
        i = 0
    while i >= 0:
        date = iTime(None, 0, i)
        Hour = TimeHourMQL4(date)
        Minute = TimeMinuteMQL4(date)
        if Hour == 0 and Minute == 0:
            O = iOpen(None, 0, i)
        C = iClose(None, 0, i)
        if O == 0:
            DPCBuffer[i] = 0.0
        else:
            DPCBuffer[i] = NormalizeDouble(_fdiv(C - O, O) * 100, 2)
        BarData = Arr(1, 0, dyn=False, factory=MqlRates)
        CopyRates(Symbol(), Period(), 0, 1, BarData)
        Latest_Close_Price = BarData[0].close
        if CurrentTime == Current:
            tm = TimeCurrent()
            gmt = TimeToString(tm, TIME_SECONDS)
        if CurrentTime == GMT:
            tm = TimeGMT()
            gmt = TimeToString(tm, TIME_SECONDS)
        if CurrentTime == Local:
            tm = TimeLocal()
            gmt = TimeToString(tm, TIME_SECONDS)
        if DPCBuffer[i] > 0:
            ObjectCreate(0, _SymbolName, OBJ_LABEL, 0, 0, 0)
            ObjectSetString(0, _SymbolName, OBJPROP_TEXT, Symbol() + '\r ' + DoubleToString(Latest_Close_Price, Digits()) + ' \r+' + DoubleToString(DPCBuffer[i], 2) + '\r% ' + gmt)
            ObjectSetInteger(0, _SymbolName, OBJPROP_COLOR, inpTextColorPositive)
            ObjectSetInteger(0, _SymbolName, OBJPROP_FONTSIZE, inpFontSize)
            ObjectSetInteger(0, _SymbolName, OBJPROP_BACK, False)
        else:
            ObjectCreate(0, _SymbolName, OBJ_LABEL, 0, 0, 0)
            ObjectSetString(0, _SymbolName, OBJPROP_TEXT, Symbol() + '\r ' + DoubleToString(Latest_Close_Price, Digits()) + ' \r' + DoubleToString(DPCBuffer[i], 2) + '\r% ' + gmt)
            ObjectSetInteger(0, _SymbolName, OBJPROP_COLOR, inpTextColorNegative)
            ObjectSetInteger(0, _SymbolName, OBJPROP_FONTSIZE, inpFontSize)
            ObjectSetInteger(0, _SymbolName, OBJPROP_BACK, False)
        if inpFontType == ML_FONTTYPE_ARIAL:
            ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Arial')
        if inpFontType == ML_FONTTYPE_ARIALBLACK:
            ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Arial Black')
        if inpFontType == ML_FONTTYPE_VERDANA:
            ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Verdana')
        if inpFontType == ML_FONTTYPE_TAHOMA:
            ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Tahoma')
        if inpFontType == ML_FONTTYPE_COURIERNEW:
            ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Courier New')
        if inpFontType == ML_FONTTYPE_LUCIDACONSOLE:
            ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Lucida Console')
        updateXY()
        i -= 1
        sCurrentTime = TimeToString(TimeCurrent(), TIME_SECONDS)
        ArraySetAsSeries(time, True)
        leftTime = PeriodSeconds(Period()) - _int(TimeCurrent() - time[0])
    ChartRedraw(0)
    return rates_total

def TimeHourMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.hour

def TimeMinuteMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.min

def OnChartEvent(id_, lparam, dparam, sparam):
    global _CurWindowWidth
    newWindowsWidth = 0
    if id_ == CHARTEVENT_CHART_CHANGE:
        newWindowsWidth = _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0))
        if _CurWindowWidth != newWindowsWidth:
            updateXY()
            _CurWindowWidth = newWindowsWidth

def updateXY():
    if inpWindowPosition == ML_WINPOSITION_UPPER_LEFT:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet)
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    elif inpWindowPosition == ML_WINPOSITION_UPPER_RIGHT:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet)
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    elif inpWindowPosition == ML_WINPOSITION_UPPER_CENTER:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet + _idiv(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0), 2))
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    elif inpWindowPosition == ML_WINPOSITION_LOWER_LEFT:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_LEFT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet)
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    elif inpWindowPosition == ML_WINPOSITION_LOWER_RIGHT:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet)
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    elif inpWindowPosition == ML_WINPOSITION_LOWER_CENTER:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_LEFT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet + _idiv(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0), 2))
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SymbolPercentageChange(_MQL5Indicator):
    name = 'Symbol_Percentage_Change'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CurrentTime': _Choice({0: 'Current', 1: 'GMT', 2: 'Local'}, default=1),
        'inpFontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Verdana', 3: 'Tahoma', 4: 'Courier New', 5: 'Lucida Console'}, default=1),  # Font Type
        'inpWindowPosition': _Choice({0: 'Upper Left of the chart', 1: 'Upper Center of the chart', 2: 'Upper Right of the chart', 3: 'Lower Left of the chart', 4: 'Lower Center of the chart', 5: 'Lower Right of the chart'}, default=2),  # Symbol position
    }

