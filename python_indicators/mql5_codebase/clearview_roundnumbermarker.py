"""clearview_roundnumbermarker — converted from MQL5: MQL5 Indicators/ClearView - PricePointer, RoundNumberMarker, PeriodSeparator plus template/clearview_roundnumbermarker.mq5

ClearView RoundNumberMarker, draws markers for every 50/100/500/1000 pips, high/low on the chart, historical high/low
 
This is indicator is best used together with: ClearView_PricePointer and ClearView_PeriodSeparator
 
See the source file for instructions on usage
Copyright: 2010, traderak20@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, traderak20@gmail.com', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['ClearView RoundNumberMarker, draws markers for every 50/100/500/1000 pips, high/low on the chart, historical high/low', ' ', 'This is indicator is best used together with: ClearView_PricePointer and ClearView_PeriodSeparator', ' ', 'See the source file for instructions on usage'], 'name': 'clearview_roundnumbermarker', 'source': 'MQL5 Indicators/ClearView - PricePointer, RoundNumberMarker, PeriodSeparator plus template/clearview_roundnumbermarker.mq5', 'folder': 'ClearView - PricePointer, RoundNumberMarker, PeriodSeparator plus template', 'inputs': [{'mql': 'InpPrintHighLow', 'py': 'InpPrintHighLow', 'param': 'InpPrintHighLow', 'type': 'bool', 'default': False, 'label': 'Print high/low information when indicator loads', 'sinput': False}, {'mql': 'InpManualAbsHigh', 'py': 'InpManualAbsHigh', 'param': 'InpManualAbsHigh', 'type': 'double', 'default': 0.0, 'label': 'Set historical high (0=use monthly chart)', 'sinput': False}, {'mql': 'InpManualAbsLow', 'py': 'InpManualAbsLow', 'param': 'InpManualAbsLow', 'type': 'double', 'default': 0.0, 'label': 'Set historical low (0=use monthly chart)', 'sinput': False}, {'mql': 'InpResetDelayTime', 'py': 'InpResetDelayTime', 'param': 'InpResetDelayTime', 'type': 'int', 'default': 16408, 'label': 'Delay to reset previous high/low marker', 'sinput': False}, {'mql': 'InpUseBrightColors', 'py': 'InpUseBrightColors', 'param': 'InpUseBrightColors', 'type': 'bool', 'default': True, 'label': 'Use bright colors', 'sinput': False}, {'mql': 'InpDrawAsBackground', 'py': 'InpDrawAsBackground', 'param': 'InpDrawAsBackground', 'type': 'bool', 'default': True, 'label': 'Draw lines as background', 'sinput': False}, {'mql': 'InpMaxTF_1000', 'py': 'InpMaxTF_1000', 'param': 'InpMaxTF_1000', 'type': 'int', 'default': 49153, 'label': 'Show 1000 pips marker up to timeframe', 'sinput': False}, {'mql': 'InpMarker_1000', 'py': 'InpMarker_1000', 'param': None, 'type': 'color', 'default': 4590150, 'label': '1000 pips marker', 'sinput': False}, {'mql': 'InpMarker_1000_Brt', 'py': 'InpMarker_1000_Brt', 'param': None, 'type': 'color', 'default': 9180300, 'label': '1000 pips marker bright', 'sinput': False}, {'mql': 'InpMaxTF_500', 'py': 'InpMaxTF_500', 'param': 'InpMaxTF_500', 'type': 'int', 'default': 16408, 'label': 'Show 500 pips marker up to timeframe', 'sinput': False}, {'mql': 'InpMarker_500', 'py': 'InpMarker_500', 'param': None, 'type': 'color', 'default': 4590150, 'label': '500 pips marker', 'sinput': False}, {'mql': 'InpMarker_500_Brt', 'py': 'InpMarker_500_Brt', 'param': None, 'type': 'color', 'default': 9180300, 'label': '500 pips marker bright', 'sinput': False}, {'mql': 'InpMaxTF_100', 'py': 'InpMaxTF_100', 'param': 'InpMaxTF_100', 'type': 'int', 'default': 16388, 'label': 'Show 100 pips marker up to timeframe', 'sinput': False}, {'mql': 'InpMarker_100', 'py': 'InpMarker_100', 'param': None, 'type': 'color', 'default': 535816, 'label': '100 pips marker', 'sinput': False}, {'mql': 'InpMarker_100_Brt', 'py': 'InpMarker_100_Brt', 'param': None, 'type': 'color', 'default': 1071632, 'label': '100 pips marker bright', 'sinput': False}, {'mql': 'InpMaxTF_50', 'py': 'InpMaxTF_50', 'param': 'InpMaxTF_50', 'type': 'int', 'default': 16385, 'label': 'Show 50 pips marker up to timeframe', 'sinput': False}, {'mql': 'InpMarker_50', 'py': 'InpMarker_50', 'param': None, 'type': 'color', 'default': 3283200, 'label': '50 pips marker', 'sinput': False}, {'mql': 'InpMarker_50_Brt', 'py': 'InpMarker_50_Brt', 'param': None, 'type': 'color', 'default': 6566400, 'label': '50 pips marker bright', 'sinput': False}, {'mql': 'InpMarker_ChartHigh', 'py': 'InpMarker_ChartHigh', 'param': None, 'type': 'color', 'default': 27005, 'label': 'Highest high on the chart', 'sinput': False}, {'mql': 'InpMarker_ChartHigh_Brt', 'py': 'InpMarker_ChartHigh_Brt', 'param': None, 'type': 'color', 'default': 54010, 'label': 'Highest high on the chart bright', 'sinput': False}, {'mql': 'InpMarker_ChartLow', 'py': 'InpMarker_ChartLow', 'param': None, 'type': 'color', 'default': 27005, 'label': 'Lowest low on the chart', 'sinput': False}, {'mql': 'InpMarker_ChartLow_Brt', 'py': 'InpMarker_ChartLow_Brt', 'param': None, 'type': 'color', 'default': 54010, 'label': 'Lowest low on the chart bright', 'sinput': False}, {'mql': 'InpMarker_AbsHigh', 'py': 'InpMarker_AbsHigh', 'param': None, 'type': 'color', 'default': 8355711, 'label': 'Historical high', 'sinput': False}, {'mql': 'InpMarker_AbsHigh_Brt', 'py': 'InpMarker_AbsHigh_Brt', 'param': None, 'type': 'color', 'default': 0, 'label': 'Historical high bright', 'sinput': False}, {'mql': 'InpMarker_AbsLow', 'py': 'InpMarker_AbsLow', 'param': None, 'type': 'color', 'default': 8355711, 'label': 'Historical low', 'sinput': False}, {'mql': 'InpMarker_AbsLow_Brt', 'py': 'InpMarker_AbsLow_Brt', 'param': None, 'type': 'color', 'default': 0, 'label': 'Historical low bright', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

White = 0xFFFFFF  # MQL4 colour name

# ---- inputs and global variables
InpPrintHighLow = _input('InpPrintHighLow', False)  # Print high/low information when indicator loads
InpManualAbsHigh = _input('InpManualAbsHigh', 0.0)  # Set historical high (0=use monthly chart)
InpManualAbsLow = _input('InpManualAbsLow', 0.0)  # Set historical low (0=use monthly chart)
InpResetDelayTime = _input('InpResetDelayTime', PERIOD_D1)  # Delay to reset previous high/low marker
InpUseBrightColors = _input('InpUseBrightColors', True)  # Use bright colors
InpDrawAsBackground = _input('InpDrawAsBackground', True)  # Draw lines as background
InpMaxTF_1000 = _input('InpMaxTF_1000', PERIOD_MN1)  # Show 1000 pips marker up to timeframe
InpMarker_1000 = _input('InpMarker_1000', 0x460A46)  # 1000 pips marker
InpMarker_1000_Brt = _input('InpMarker_1000_Brt', 0x8C148C)  # 1000 pips marker bright
InpMaxTF_500 = _input('InpMaxTF_500', PERIOD_D1)  # Show 500 pips marker up to timeframe
InpMarker_500 = _input('InpMarker_500', 0x460A46)  # 500 pips marker
InpMarker_500_Brt = _input('InpMarker_500_Brt', 0x8C148C)  # 500 pips marker bright
InpMaxTF_100 = _input('InpMaxTF_100', PERIOD_H4)  # Show 100 pips marker up to timeframe
InpMarker_100 = _input('InpMarker_100', 0x082D08)  # 100 pips marker
InpMarker_100_Brt = _input('InpMarker_100_Brt', 0x105A10)  # 100 pips marker bright
InpMaxTF_50 = _input('InpMaxTF_50', PERIOD_H1)  # Show 50 pips marker up to timeframe
InpMarker_50 = _input('InpMarker_50', 0x321900)  # 50 pips marker
InpMarker_50_Brt = _input('InpMarker_50_Brt', 0x643200)  # 50 pips marker bright
InpMarker_ChartHigh = _input('InpMarker_ChartHigh', 0x00697D)  # Highest high on the chart
InpMarker_ChartHigh_Brt = _input('InpMarker_ChartHigh_Brt', 0x00D2FA)  # Highest high on the chart bright
InpMarker_ChartLow = _input('InpMarker_ChartLow', 0x00697D)  # Lowest low on the chart
InpMarker_ChartLow_Brt = _input('InpMarker_ChartLow_Brt', 0x00D2FA)  # Lowest low on the chart bright
InpMarker_AbsHigh = _input('InpMarker_AbsHigh', 0x7F7F7F)  # Historical high
InpMarker_AbsLow = _input('InpMarker_AbsLow', 0x7F7F7F)  # Historical low
highestExtended = 0  # Limits between which to draw markers
lowestExtended = 0  # Limits between which to draw markers
absHighInt = 0  # value of highest high and lowest low for PERIOD_MN1
absLowInt = 0  # value of highest high and lowest low for PERIOD_MN1
prevAbsHighInt = 0  # value of previous highest high and lowest low for PERIOD_MN1
prevAbsLowInt = 0  # value of previous highest high and lowest low for PERIOD_MN1
newAbsHighDate = 0  # date of new highest high and lowest low for PERIOD_MN1
newAbsLowDate = 0  # date of new highest high and lowest low for PERIOD_MN1
newAbsHigh = False  # flag to show a new highest high or lowest low has been made for PERIOD_MN1
newAbsLow = False  # flag to show a new highest high or lowest low has been made for PERIOD_MN1
chartHighInt = 0  # value of highest high and lowest low on chart
chartLowInt = 0  # value of highest high and lowest low on chart
prevChartHighInt = 0  # value of previous highest high and lowest low on chart
prevChartLowInt = 0  # value of previous highest high and lowest low on chart
newChartHighDate = 0  # date of new highest high and lowest low on the chart
newChartLowDate = 0  # date of new highest high and lowest low on the chart
newChartHigh = False  # flag to show a new highest high or lowest low has been made on the chart
newChartLow = False  # flag to show a new highest high or lowest low has been made on the chart
marker_1000_Clr = 0  # colors for 1000 & 500 pips markers
marker_500_Clr = 0  # colors for 1000 & 500 pips markers
marker_100_Clr = 0  # colors for 100 & 50 pips markers
marker_50_Clr = 0  # colors for 100 & 50 pips markers
marker_ChartHigh_Clr = 0  # colors for highest high & lowest low markers
marker_ChartLow_Clr = 0  # colors for highest high & lowest low markers
marker_AbsHigh_Clr = 0  # colors for absolute highest high & absolute lowest low markers
marker_AbsLow_Clr = 0  # colors for absolute highest high & absolute lowest low markers
resetDelay = 0  # delay before marker for previous high/low is reset

def DeleteObjects():
    ObjectDelete(0, 'objMarker_HISTORICAL_HIGH')
    ObjectDelete(0, 'objMarker_PREV_HISTORICAL_HIGH')
    ObjectDelete(0, 'objMarker_HISTORICAL_LOW')
    ObjectDelete(0, 'objMarker_PREV_HISTORICAL_LOW')
    ObjectDelete(0, 'objMarker_CHART_HIGH')
    ObjectDelete(0, 'objMarker_PREV_CHART_HIGH')
    ObjectDelete(0, 'objMarker_CHART_LOW')
    ObjectDelete(0, 'objMarker_PREV_CHART_LOW')
    i = highestExtended
    while i >= lowestExtended:
        if MathMod(i, 10000) == 0:
            ObjectDelete(0, 'objMarker_1000_' + _str(i))
        if MathMod(i, 5000) == 0:
            ObjectDelete(0, 'objMarker_500_' + _str(i))
        if MathMod(i, 1000) == 0:
            ObjectDelete(0, 'objMarker_100_' + _str(i))
        if MathMod(i, 500) == 0:
            ObjectDelete(0, 'objMarker_50_' + _str(i))
        i -= 500
    ChartRedraw(0)

def DeleteObject(f_ObjName):
    ObjectDelete(0, f_ObjName)

def CreateMarkerObj(f_ObjName, f_Price, f_ObjColor, f_ObjLineStyle, f_ObjWidth):
    ObjectDelete(0, f_ObjName)
    ObjectCreate(0, f_ObjName, OBJ_HLINE, 0, 0, f_Price * Point())
    ObjectSetInteger(0, f_ObjName, OBJPROP_BACK, InpDrawAsBackground)
    ObjectSetInteger(0, f_ObjName, OBJPROP_COLOR, f_ObjColor)
    ObjectSetInteger(0, f_ObjName, OBJPROP_STYLE, f_ObjLineStyle)
    ObjectSetInteger(0, f_ObjName, OBJPROP_WIDTH, f_ObjWidth)

def OnInit():
    global marker_1000_Clr, marker_100_Clr, marker_500_Clr, marker_50_Clr, marker_AbsHigh_Clr, marker_AbsLow_Clr, marker_ChartHigh_Clr, marker_ChartLow_Clr, newAbsHigh, newAbsLow, newChartHigh, newChartLow, resetDelay
    IndicatorSetString(INDICATOR_SHORTNAME, 'Round Number Marker')
    resetDelay = PeriodSeconds(InpResetDelayTime)
    newAbsHigh = False
    newAbsLow = False
    newChartHigh = False
    newChartLow = False
    if InpUseBrightColors == False:
        marker_1000_Clr = InpMarker_1000
        marker_500_Clr = InpMarker_500
        marker_100_Clr = InpMarker_100
        marker_50_Clr = InpMarker_50
        marker_ChartHigh_Clr = InpMarker_ChartHigh
        marker_ChartLow_Clr = InpMarker_ChartLow
        marker_AbsHigh_Clr = InpMarker_AbsHigh
        marker_AbsLow_Clr = InpMarker_AbsLow
    else:
        marker_1000_Clr = InpMarker_1000_Brt
        marker_500_Clr = InpMarker_500_Brt
        marker_100_Clr = InpMarker_100_Brt
        marker_50_Clr = InpMarker_50_Brt
        marker_ChartHigh_Clr = InpMarker_ChartHigh_Brt
        marker_ChartLow_Clr = InpMarker_ChartLow_Brt
        marker_AbsHigh_Clr = InpMarker_AbsHigh_Brt
        marker_AbsLow_Clr = InpMarker_AbsLow_Brt

def OnDeinit(reason):
    DeleteObjects()

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global absHighInt, absLowInt, chartHighInt, chartLowInt, highestExtended, lowestExtended, newAbsHigh, newAbsHighDate, newAbsLow, newAbsLowDate, newChartHigh, newChartHighDate, newChartLow, newChartLowDate, prevAbsHighInt, prevAbsLowInt, prevChartHighInt, prevChartLowInt
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Time, True)
    drawAbsHighMarker = False
    drawPrevAbsHighMarker = False
    drawAbsLowMarker = False
    drawPrevAbsLowMarker = False
    drawChartHighMarker = False
    drawPrevChartHighMarker = False
    drawChartLowMarker = False
    drawPrevChartLowMarker = False
    drawRoundNumberMarkers = False
    if prev_calculated <= 0 or prev_calculated > rates_total:
        monthlyRates = Arr(0, 0, factory=MqlRates)
        absHighIdx = INT_MIN
        absLowIdx = INT_MAX
        if InpManualAbsHigh == 0 or InpManualAbsLow == 0:
            ArraySetAsSeries(monthlyRates, True)
            if CopyRates(None, PERIOD_MN1, 0, Bars(None, 0), monthlyRates) <= 0:
                return 0
            if InpManualAbsHigh == 0:
                monthlyRatesHigh = Arr(0, 0.0)
                ArraySetAsSeries(monthlyRatesHigh, True)
                ArrayInitialize(monthlyRatesHigh, EMPTY_VALUE)
                ArrayResize(monthlyRatesHigh, Bars(None, PERIOD_MN1))
                for i in range(0, Bars(None, PERIOD_MN1)):
                    monthlyRatesHigh[i] = monthlyRates[i].high
                absHighIdx = ArrayMaximum(monthlyRatesHigh, 0, WHOLE_ARRAY)
                absHighInt = _int(_fdiv(monthlyRatesHigh[absHighIdx], Point()))
            if InpManualAbsLow == 0:
                monthlyRatesLow = Arr(0, 0.0)
                ArraySetAsSeries(monthlyRatesLow, True)
                ArrayInitialize(monthlyRatesLow, EMPTY_VALUE)
                ArrayResize(monthlyRatesLow, Bars(None, PERIOD_MN1))
                for i in range(0, Bars(None, PERIOD_MN1)):
                    monthlyRatesLow[i] = monthlyRates[i].low
                absLowIdx = ArrayMinimum(monthlyRatesLow, 0, WHOLE_ARRAY)
                absLowInt = _int(_fdiv(monthlyRatesLow[absLowIdx], Point()))
        if InpManualAbsHigh != 0:
            absHighInt = _int(_fdiv(InpManualAbsHigh, Point()))
        if InpManualAbsLow != 0:
            absLowInt = _int(_fdiv(InpManualAbsLow, Point()))
        prevAbsHighInt = absHighInt
        prevAbsLowInt = absLowInt
        chartHighIdx = ArrayMaximum(High, 0, WHOLE_ARRAY)
        chartHighInt = _int(_fdiv(High[chartHighIdx], Point()))
        prevChartHighInt = chartHighInt
        highestExtended = chartHighInt - _int(MathMod(chartHighInt, 500)) + 500 + 10000
        chartLowIdx = ArrayMinimum(Low, 0, WHOLE_ARRAY)
        chartLowInt = _int(_fdiv(Low[chartLowIdx], Point()))
        prevChartLowInt = chartLowInt
        lowestExtended = chartLowInt - _int(MathMod(chartLowInt, 500)) - 10000
        if InpPrintHighLow == True:
            if InpManualAbsHigh == 0:
                absHighMonth = TimeToString(monthlyRates[absHighIdx].time, TIME_DATE)
                absHighMonth = StringSubstr(absHighMonth, 0, StringLen(absHighMonth) - 3)
                Print(Symbol(), ' [', absHighMonth, '] - Historical high on monthly chart: ', absHighInt * Point())
            if InpManualAbsHigh != 0:
                Print(Symbol(), ' - Historical high (set manually): ', absHighInt * Point())
            if InpManualAbsLow == 0:
                absLowMonth = TimeToString(monthlyRates[absLowIdx].time, TIME_DATE)
                absLowMonth = StringSubstr(absLowMonth, 0, StringLen(absLowMonth) - 3)
                Print(Symbol(), ' [', absLowMonth, '] - Historical low on monthly chart: ', absLowInt * Point())
            if InpManualAbsLow != 0:
                Print(Symbol(), ' - Historical low (set manually): ', absLowInt * Point())
            chartHighDateTime = TimeToString(Time[chartHighIdx], TIME_DATE | TIME_MINUTES)
            Print(Symbol(), ' [', chartHighDateTime, '] - Highest high on current chart: ', chartHighInt * Point())
            chartLowDateTime = TimeToString(Time[chartLowIdx], TIME_DATE | TIME_MINUTES)
            Print(Symbol(), ' [', chartLowDateTime, '] - Lowest low on current chart: ', chartLowInt * Point())
        drawAbsHighMarker = True
        drawAbsLowMarker = True
        drawChartHighMarker = True
        drawChartLowMarker = True
        drawRoundNumberMarkers = True
    curBid = 0
    curBid = _int(_fdiv(SymbolInfoDouble(Symbol(), SYMBOL_BID), Point()))
    if curBid > absHighInt:
        if newAbsHigh == False:
            drawPrevAbsHighMarker = True
            newAbsHighDate = TimeCurrent()
            newAbsHigh = True
        absHighInt = curBid
        drawAbsHighMarker = True
    if newAbsHigh == True and TimeCurrent() >= (newAbsHighDate + resetDelay):
        prevAbsHighInt = absHighInt
        DeleteObject('objMarker_PREVABSHIGH')
        newAbsHigh = False
    if curBid < absLowInt:
        if newAbsLow == False:
            drawPrevAbsLowMarker = True
            newAbsLowDate = TimeCurrent()
            newAbsLow = True
        absLowInt = curBid
        drawAbsLowMarker = True
    if newAbsLow == True and TimeCurrent() >= (newAbsLowDate + resetDelay):
        prevAbsLowInt = absLowInt
        DeleteObject('objMarker_PREVABSLOW')
        newAbsLow = False
    if curBid > chartHighInt:
        if newChartHigh == False:
            if prevChartHighInt != prevAbsHighInt:
                drawPrevChartHighMarker = True
            newChartHighDate = TimeCurrent()
            newChartHigh = True
        chartHighInt = curBid
        if chartHighInt != absHighInt:
            drawChartHighMarker = True
        if chartHighInt == absHighInt:
            DeleteObject('objMarker_CHARTHIGH')
    if newChartHigh == True and TimeCurrent() >= (newChartHighDate + resetDelay):
        prevChartHighInt = chartHighInt
        DeleteObject('objMarker_PREVCHARTHIGH')
        newChartHigh = False
    if curBid < chartLowInt:
        if newChartLow == False:
            if prevChartLowInt != prevAbsLowInt:
                drawPrevChartLowMarker = True
            newChartLowDate = TimeCurrent()
            newChartLow = True
        chartLowInt = curBid
        if chartLowInt != absLowInt:
            drawChartLowMarker = True
        if chartLowInt == absLowInt:
            DeleteObject('objMarker_CHARTLOW')
    if newChartLow == True and TimeCurrent() >= (newChartLowDate + resetDelay):
        prevChartLowInt = chartLowInt
        DeleteObject('objMarker_PREVCHARTLOW')
        newChartLow = False
    if curBid <= (lowestExtended + 2000) or curBid >= (highestExtended - 2000):
        if curBid >= (highestExtended - 2000):
            highestExtended += 5000
        if curBid <= (lowestExtended + 2000):
            lowestExtended -= 5000
        drawRoundNumberMarkers = True
    if drawRoundNumberMarkers == True:
        i = highestExtended
        while i >= lowestExtended:
            if MathMod(i, 10000) == 0 and Period() <= InpMaxTF_1000:
                CreateMarkerObj('objMarker_1000_' + _str(i), i, marker_1000_Clr, STYLE_DASHDOT, 1)
                i -= 500
                continue
            if MathMod(i, 5000) == 0 and Period() <= InpMaxTF_500:
                CreateMarkerObj('objMarker_500_' + _str(i), i, marker_500_Clr, STYLE_DASHDOT, 1)
                i -= 500
                continue
            if MathMod(i, 1000) == 0 and Period() <= InpMaxTF_100:
                CreateMarkerObj('objMarker_100_' + _str(i), i, marker_100_Clr, STYLE_DASHDOT, 1)
                i -= 500
                continue
            if MathMod(i, 500) == 0 and Period() <= InpMaxTF_50:
                CreateMarkerObj('objMarker_50_' + _str(i), i, marker_50_Clr, STYLE_DASHDOT, 1)
            i -= 500
    if drawChartHighMarker == True:
        CreateMarkerObj('objMarker_CHART_HIGH', chartHighInt, marker_ChartHigh_Clr, STYLE_DASHDOT, 1)
    if drawPrevChartHighMarker == True:
        CreateMarkerObj('objMarker_PREV_CHART_HIGH', prevChartHighInt, marker_ChartHigh_Clr, STYLE_DOT, 1)
    if drawChartLowMarker == True and chartLowInt != absLowInt:
        CreateMarkerObj('objMarker_CHART_LOW', chartLowInt, marker_ChartLow_Clr, STYLE_DASHDOT, 1)
    if drawPrevChartLowMarker == True:
        CreateMarkerObj('objMarker_PREV_CHART_LOW', prevChartLowInt, marker_ChartLow_Clr, STYLE_DOT, 1)
    if drawAbsHighMarker == True:
        CreateMarkerObj('objMarker_HISTORICAL_HIGH', absHighInt, marker_AbsHigh_Clr, STYLE_DASH, 1)
    if drawPrevAbsHighMarker == True:
        CreateMarkerObj('objMarker_PREV_HISTORICAL_HIGH', prevAbsHighInt, marker_AbsHigh_Clr, STYLE_DOT, 1)
    if drawAbsLowMarker == True:
        CreateMarkerObj('objMarker_HISTORICAL_LOW', absLowInt, marker_AbsLow_Clr, STYLE_DASH, 1)
    if drawPrevAbsLowMarker == True:
        CreateMarkerObj('objMarker_PREV_HISTORICAL_LOW', prevAbsLowInt, marker_AbsLow_Clr, STYLE_DOT, 1)
    return rates_total

# ---- global variables initialised from expressions
InpMarker_AbsHigh_Brt = _input('InpMarker_AbsHigh_Brt', _uint(White))  # Historical high bright
InpMarker_AbsLow_Brt = _input('InpMarker_AbsLow_Brt', _uint(White))  # Historical low bright


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ClearviewRoundnumbermarker(_MQL5Indicator):
    name = 'clearview_roundnumbermarker'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPrintHighLow': False,  # Print high/low information when indicator loads
        'InpManualAbsHigh': 0.0,  # Set historical high (0=use monthly chart)
        'InpManualAbsLow': 0.0,  # Set historical low (0=use monthly chart)
        'InpResetDelayTime': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Delay to reset previous high/low marker
        'InpUseBrightColors': True,  # Use bright colors
        'InpDrawAsBackground': True,  # Draw lines as background
        'InpMaxTF_1000': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=49153),  # Show 1000 pips marker up to timeframe
        'InpMaxTF_500': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Show 500 pips marker up to timeframe
        'InpMaxTF_100': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Show 100 pips marker up to timeframe
        'InpMaxTF_50': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Show 50 pips marker up to timeframe
    }

