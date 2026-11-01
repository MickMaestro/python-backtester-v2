"""clearview_pricepointer — converted from MQL5: MQL5 Indicators/ClearView - PricePointer, RoundNumberMarker, PeriodSeparator plus template/clearview_pricepointer.mq5

ClearView PricePointer, bid/ask pointer with color-coded alerts every 500/1000 pips, daily high/low, high/low on the chart, historical high/low, shows last bid/ask/spread/tick-time
 
This is indicator is best used together with: ClearView_RoundNumberMarker and ClearView_PeriodSeparator
 
See the source file for instructions on usage
Copyright: 2010, traderak20@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, traderak20@gmail.com', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['ClearView PricePointer, bid/ask pointer with color-coded alerts every 500/1000 pips, daily high/low, high/low on the chart, historical high/low, shows last bid/ask/spread/tick-time', ' ', 'This is indicator is best used together with: ClearView_RoundNumberMarker and ClearView_PeriodSeparator', ' ', 'See the source file for instructions on usage'], 'name': 'clearview_pricepointer', 'source': 'MQL5 Indicators/ClearView - PricePointer, RoundNumberMarker, PeriodSeparator plus template/clearview_pricepointer.mq5', 'folder': 'ClearView - PricePointer, RoundNumberMarker, PeriodSeparator plus template', 'inputs': [{'mql': 'InpPrintHighLow', 'py': 'InpPrintHighLow', 'param': 'InpPrintHighLow', 'type': 'bool', 'default': False, 'label': 'Print high/low information when indicator loads', 'sinput': False}, {'mql': 'InpManualAbsHigh', 'py': 'InpManualAbsHigh', 'param': 'InpManualAbsHigh', 'type': 'double', 'default': 0.0, 'label': 'Set historical high (0=use monthly chart)', 'sinput': False}, {'mql': 'InpManualAbsLow', 'py': 'InpManualAbsLow', 'param': 'InpManualAbsLow', 'type': 'double', 'default': 0.0, 'label': 'Set historical low (0=use monthly chart)', 'sinput': False}, {'mql': 'InpShowBidLine', 'py': 'InpShowBidLine', 'param': 'InpShowBidLine', 'type': 'bool', 'default': True, 'label': 'Show Bid line', 'sinput': False}, {'mql': 'InpShowAskLine', 'py': 'InpShowAskLine', 'param': 'InpShowAskLine', 'type': 'bool', 'default': True, 'label': 'Show Ask line', 'sinput': False}, {'mql': 'InpShowRayLeft', 'py': 'InpShowRayLeft', 'param': 'InpShowRayLeft', 'type': 'bool', 'default': False, 'label': 'Extend price pointer to the left', 'sinput': False}, {'mql': 'InpPriceLineColor', 'py': 'InpPriceLineColor', 'param': None, 'type': 'color', 'default': 8603662, 'label': 'Bid/Ask line default color', 'sinput': False}, {'mql': 'InpProximity_500_1000', 'py': 'InpProximity_500_1000', 'param': 'InpProximity_500_1000', 'type': 'int', 'default': 55, 'label': 'Alert # of pips around 500/1000 markers', 'sinput': False}, {'mql': 'InpMarker_500_1000', 'py': 'InpMarker_500_1000', 'param': None, 'type': 'color', 'default': 9114251, 'label': '500/1000 pips markers', 'sinput': False}, {'mql': 'InpProximity_DailyHighLow', 'py': 'InpProximity_DailyHighLow', 'param': 'InpProximity_DailyHighLow', 'type': 'int', 'default': 10, 'label': 'Alert # of pips before high/low for the day', 'sinput': False}, {'mql': 'InpMarker_DailyHighLow', 'py': 'InpMarker_DailyHighLow', 'param': None, 'type': 'color', 'default': 0, 'label': 'High/low for the day', 'sinput': False}, {'mql': 'InpProximity_ChartHighLow', 'py': 'InpProximity_ChartHighLow', 'param': 'InpProximity_ChartHighLow', 'type': 'int', 'default': 55, 'label': 'Alert # of pips before high/low on the chart', 'sinput': False}, {'mql': 'InpMarker_ChartHighLow', 'py': 'InpMarker_ChartHighLow', 'param': None, 'type': 'color', 'default': 0, 'label': 'High/low on the chart', 'sinput': False}, {'mql': 'InpProximity_AbsHighLow', 'py': 'InpProximity_AbsHighLow', 'param': 'InpProximity_AbsHighLow', 'type': 'int', 'default': 55, 'label': 'Alert # of pips before historical high/low', 'sinput': False}, {'mql': 'InpMarker_AbsHighLow', 'py': 'InpMarker_AbsHighLow', 'param': None, 'type': 'color', 'default': 0, 'label': 'Historical high/low', 'sinput': False}, {'mql': 'InpShowBidAsk', 'py': 'InpShowBidAsk', 'param': 'InpShowBidAsk', 'type': 'bool', 'default': True, 'label': 'Show Bid/Ask prices', 'sinput': False}, {'mql': 'InpBidAskColor', 'py': 'InpBidAskColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Bid/Ask prices', 'sinput': False}, {'mql': 'InpLastDigitkColor', 'py': 'InpLastDigitkColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Last digit default color', 'sinput': False}, {'mql': 'InpChangeLastDigitColor', 'py': 'InpChangeLastDigitColor', 'param': 'InpChangeLastDigitColor', 'type': 'bool', 'default': False, 'label': 'Change color of last digit with Bid/Ask', 'sinput': False}, {'mql': 'InpBidAskSeparator', 'py': 'InpBidAskSeparator', 'param': None, 'type': 'string', 'default': '/', 'label': 'Bid/Ask separator', 'sinput': False}, {'mql': 'InpSeparatorColor', 'py': 'InpSeparatorColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Bid/Ask separator', 'sinput': False}, {'mql': 'InpShowClock', 'py': 'InpShowClock', 'param': 'InpShowClock', 'type': 'bool', 'default': True, 'label': 'Show most recent tick time', 'sinput': False}, {'mql': 'InpTimeColor', 'py': 'InpTimeColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Most recent tick time', 'sinput': False}, {'mql': 'InpBaseCorner', 'py': 'InpBaseCorner', 'param': 'InpBaseCorner', 'type': 'int', 'default': 3, 'label': 'Corner for Bid/Ask & time', 'sinput': False}, {'mql': 'InpDrawAsBackground', 'py': 'InpDrawAsBackground', 'param': 'InpDrawAsBackground', 'type': 'bool', 'default': False, 'label': 'Draw objects as background', 'sinput': False}, {'mql': 'InpWindowIdx', 'py': 'InpWindowIdx', 'param': 'InpWindowIdx', 'type': 'int', 'default': 0, 'label': 'Sub-window for Bid/Ask & clock (0=main)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DimGray = 0x696969  # MQL4 colour name
DodgerBlue = 0xFF901E  # MQL4 colour name
Gold = 0x00D7FF  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name

# ---- inputs and global variables
InpPrintHighLow = _input('InpPrintHighLow', False)  # Print high/low information when indicator loads
InpManualAbsHigh = _input('InpManualAbsHigh', 0.0)  # Set historical high (0=use monthly chart)
InpManualAbsLow = _input('InpManualAbsLow', 0.0)  # Set historical low (0=use monthly chart)
InpShowBidLine = _input('InpShowBidLine', True)  # Show Bid line
InpShowAskLine = _input('InpShowAskLine', True)  # Show Ask line
InpShowRayLeft = _input('InpShowRayLeft', False)  # Extend price pointer to the left
InpPriceLineColor = _input('InpPriceLineColor', 0x83480E)  # Bid/Ask line default color
InpProximity_500_1000 = _input('InpProximity_500_1000', 55)  # Alert # of pips around 500/1000 markers
InpMarker_500_1000 = _input('InpMarker_500_1000', 0x8B128B)  # 500/1000 pips markers
InpProximity_DailyHighLow = _input('InpProximity_DailyHighLow', 10)  # Alert # of pips before high/low for the day
InpProximity_ChartHighLow = _input('InpProximity_ChartHighLow', 55)  # Alert # of pips before high/low on the chart
InpProximity_AbsHighLow = _input('InpProximity_AbsHighLow', 55)  # Alert # of pips before historical high/low
InpShowBidAsk = _input('InpShowBidAsk', True)  # Show Bid/Ask prices
InpChangeLastDigitColor = _input('InpChangeLastDigitColor', False)  # Change color of last digit with Bid/Ask
InpBidAskSeparator = _input('InpBidAskSeparator', '/')  # Bid/Ask separator
InpShowClock = _input('InpShowClock', True)  # Show most recent tick time
InpBaseCorner = _input('InpBaseCorner', CORNER_RIGHT_UPPER)  # Corner for Bid/Ask & time
InpDrawAsBackground = _input('InpDrawAsBackground', False)  # Draw objects as background
InpWindowIdx = _input('InpWindowIdx', 0)  # Sub-window for Bid/Ask & clock (0=main)
X_Distance = 6  # X distance in pixels from binding corner for clock and Bid/Ask
Y_Distance1 = 18  # Y distance in pixels from binding corner for clock or Bid/Ask
Y_Distance2 = 38  # Y distance in pixels from binding corner for clock or Bid/Ask
Y_DistanceBidAsk = 0  # Y distance in pixels from binding corner for Bid/Ask
Y_DistanceClock = 0  # Y distance in pixels from binding corner for clock
lineExtender = 2678400  # seconds in a month: 60*60*24*31
objAnchor = 0  # anchor for clock and Bid/Ask price
dailyHighInt = INT_MIN  # highest high for the day in points
dailyLowInt = INT_MAX  # lowest low for the day in points
chartHighInt = INT_MIN  # highest high on the chart in points
chartLowInt = INT_MAX  # lowest low on the chart in points
absHighInt = INT_MIN  # highest high on the monthly chart in points
absLowInt = INT_MAX  # lowest low on the monthly chart in points
bidAskFont = 'Courier'  # font for Bid/Ask prices, has to be a fixed width font
bidAskFontSize = 14  # fontsize for Bid/Ask prices
clockFont = 'Arial'  # font for clock
clockFontSize = 10  # fontsize for clock
prox_500_1000 = 0  # number of pips around the 500 & 1000 pips markers
prox_DailyHighLow = 0  # number of pips before high and low for the day
prox_ChartHighLow = 0  # number of pips before high and low on the chart
prox_AbsHighLow = 0  # number of pips before high and low on the monthly chart

def SetSpacerLength(f_CurString, f_PrevString):
    f_StrLenTotal = StringLen(f_PrevString)
    f_StrSpacer = Box("")
    StringInit(f_StrSpacer, f_StrLenTotal, 32)
    if InpBaseCorner == CORNER_RIGHT_UPPER or InpBaseCorner == CORNER_RIGHT_LOWER:
        StringAdd(f_CurString, f_StrSpacer.v)
    if InpBaseCorner == CORNER_LEFT_UPPER or InpBaseCorner == CORNER_LEFT_LOWER:
        StringAdd(f_StrSpacer, f_CurString.v)
        f_CurString.v = f_StrSpacer.v

def CreateLabelObj(f_ObjName, f_Y_Distance, f_ObjLabel, f_ObjFont, f_ObjFontSize, f_ObjColor):
    ObjectCreate(0, f_ObjName, OBJ_LABEL, InpWindowIdx, 0, 0)
    ObjectSetInteger(0, f_ObjName, OBJPROP_ANCHOR, objAnchor)
    ObjectSetInteger(0, f_ObjName, OBJPROP_CORNER, InpBaseCorner)
    ObjectSetInteger(0, f_ObjName, OBJPROP_XDISTANCE, X_Distance)
    ObjectSetInteger(0, f_ObjName, OBJPROP_YDISTANCE, f_Y_Distance)
    ObjectSetString(0, f_ObjName, OBJPROP_TEXT, f_ObjLabel)
    ObjectSetString(0, f_ObjName, OBJPROP_FONT, f_ObjFont)
    ObjectSetInteger(0, f_ObjName, OBJPROP_FONTSIZE, f_ObjFontSize)
    ObjectSetInteger(0, f_ObjName, OBJPROP_COLOR, f_ObjColor)
    ObjectSetInteger(0, f_ObjName, OBJPROP_BACK, InpDrawAsBackground)

def OnInit():
    global Y_DistanceBidAsk, Y_DistanceClock, objAnchor, prox_500_1000, prox_AbsHighLow, prox_ChartHighLow, prox_DailyHighLow
    IndicatorSetString(INDICATOR_SHORTNAME, 'Price Pointer')
    prox_500_1000 = InpProximity_500_1000 * 10
    prox_DailyHighLow = InpProximity_DailyHighLow * 10
    prox_ChartHighLow = InpProximity_ChartHighLow * 10
    prox_AbsHighLow = InpProximity_AbsHighLow * 10
    Y_DistanceBidAsk = Y_Distance2
    if (InpShowClock == False or InpBaseCorner == CORNER_RIGHT_LOWER) or InpBaseCorner == CORNER_LEFT_LOWER:
        Y_DistanceBidAsk = Y_Distance1
    Y_DistanceClock = Y_Distance1
    if InpBaseCorner == CORNER_RIGHT_LOWER or InpBaseCorner == CORNER_LEFT_LOWER:
        Y_DistanceClock = Y_Distance2
    _sw1 = InpBaseCorner
    if _sw1 == CORNER_LEFT_UPPER:
        objAnchor = ANCHOR_LEFT_UPPER
    elif _sw1 == CORNER_LEFT_LOWER:
        objAnchor = ANCHOR_LEFT_LOWER
    elif _sw1 == CORNER_RIGHT_LOWER:
        objAnchor = ANCHOR_RIGHT_LOWER
    elif _sw1 == CORNER_RIGHT_UPPER:
        objAnchor = ANCHOR_RIGHT_UPPER
    else:
        objAnchor = ANCHOR_RIGHT_UPPER

def OnDeinit(reason):
    ObjectDelete(0, 'objAskPointer')
    ObjectDelete(0, 'objBidPointer')
    ObjectDelete(0, 'objBidText')
    ObjectDelete(0, 'objBidLastDigitText')
    ObjectDelete(0, 'objAskText')
    ObjectDelete(0, 'objAskLastDigitText')
    ObjectDelete(0, 'objSpreadText')
    ObjectDelete(0, 'objSpreadLastDigitText')
    ObjectDelete(0, 'objSeparator1')
    ObjectDelete(0, 'objSeparator2')
    ObjectDelete(0, 'objTime')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global absHighInt, absLowInt, chartHighInt, chartLowInt, dailyHighInt, dailyLowInt
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    curBidVal = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    curBidPips = _int(_fdiv(curBidVal, Point()))
    curAskVal = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
    curAskPips = _int(_fdiv(curAskVal, Point()))
    curSpreadVal = 0
    if InpShowBidAsk == True:
        curSpreadVal = _int(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD))
    if curBidPips > dailyHighInt:
        dailyHighInt = _int(_fdiv(SymbolInfoDouble(Symbol(), SYMBOL_BIDHIGH), Point()))
    if curBidPips < dailyLowInt:
        dailyLowInt = _int(_fdiv(SymbolInfoDouble(Symbol(), SYMBOL_BIDLOW), Point()))
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
        chartHighIdx = ArrayMaximum(High, 0, WHOLE_ARRAY)
        chartHighInt = _int(_fdiv(High[chartHighIdx], Point()))
        chartLowIdx = ArrayMinimum(Low, 0, WHOLE_ARRAY)
        chartLowInt = _int(_fdiv(Low[chartLowIdx], Point()))
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
    if curBidPips > chartHighInt:
        chartHighInt = curBidPips
    if curBidPips < chartLowInt:
        chartLowInt = curBidPips
    if curBidPips > absHighInt:
        absHighInt = curBidPips
    if curBidPips < absLowInt:
        absLowInt = curBidPips
    bidAskColor = InpBidAskColor
    bidAskLineColor = InpPriceLineColor
    LastDigitColor = InpLastDigitkColor
    update_bidAskLineColor = False
    if curAskPips >= (dailyHighInt - prox_DailyHighLow) or curBidPips <= (dailyLowInt + prox_DailyHighLow):
        bidAskColor = InpMarker_DailyHighLow
        update_bidAskLineColor = True
    if ((MathMod(curAskPips, 10000) >= (10000 - prox_500_1000) or MathMod(curBidPips, 10000) <= prox_500_1000) or MathMod(curAskPips, 5000) >= (5000 - prox_500_1000)) or MathMod(curBidPips, 5000) <= prox_500_1000:
        bidAskColor = InpMarker_500_1000
        update_bidAskLineColor = True
    if curAskPips >= (chartHighInt - prox_ChartHighLow) or curBidPips <= (chartLowInt + prox_ChartHighLow):
        bidAskColor = InpMarker_ChartHighLow
        update_bidAskLineColor = True
    if curAskPips >= (absHighInt - prox_AbsHighLow) or curBidPips <= (absLowInt + prox_AbsHighLow):
        bidAskColor = InpMarker_AbsHighLow
        update_bidAskLineColor = True
    if update_bidAskLineColor == True:
        bidAskLineColor = bidAskColor
    if InpChangeLastDigitColor == True:
        LastDigitColor = bidAskColor
    if InpShowBidAsk == True:
        tempSpreadStr = IntegerToString(curSpreadVal)
        curSpreadLastDigit = Box(StringSubstr(tempSpreadStr, StringLen(tempSpreadStr) - 1, 1))
        curSpreadStr = Box(StringSubstr(tempSpreadStr, 0, StringLen(tempSpreadStr) - 1))
        if curSpreadStr.v == '':
            curSpreadStr.v = '0'
        separator_1 = Box(InpBidAskSeparator)
        tempAskStr = DoubleToString(curAskVal, Digits())
        curAskLastDigit = Box(StringSubstr(tempAskStr, StringLen(tempAskStr) - 1, 1))
        curAskStr = Box(StringSubstr(tempAskStr, StringLen(tempAskStr) - 3, 2))
        separator_2 = Box(InpBidAskSeparator)
        tempBidStr = DoubleToString(curBidVal, Digits())
        curBidLastDigit = Box(StringSubstr(tempBidStr, StringLen(tempBidStr) - 1, 1))
        curBidStr = Box(StringSubstr(tempBidStr, 0, StringLen(tempBidStr) - 1))
        if InpBaseCorner == CORNER_RIGHT_UPPER or InpBaseCorner == CORNER_RIGHT_LOWER:
            SetSpacerLength(curSpreadStr, curSpreadLastDigit.v)
            SetSpacerLength(separator_1, curSpreadStr.v)
            SetSpacerLength(curAskLastDigit, separator_1.v)
            SetSpacerLength(curAskStr, curAskLastDigit.v)
            SetSpacerLength(separator_2, curAskStr.v)
            SetSpacerLength(curBidLastDigit, separator_2.v)
            SetSpacerLength(curBidStr, curBidLastDigit.v)
        if InpBaseCorner == CORNER_LEFT_UPPER or InpBaseCorner == CORNER_LEFT_LOWER:
            SetSpacerLength(curBidLastDigit, curBidStr.v)
            SetSpacerLength(separator_2, curBidLastDigit.v)
            SetSpacerLength(curAskStr, separator_2.v)
            SetSpacerLength(curAskLastDigit, curAskStr.v)
            SetSpacerLength(separator_1, curAskLastDigit.v)
            SetSpacerLength(curSpreadStr, separator_1.v)
            SetSpacerLength(curSpreadLastDigit, curSpreadStr.v)
        if ObjectFind(0, 'objSpreadLastDigitText') == InpWindowIdx:
            ObjectSetString(0, 'objSpreadLastDigitText', OBJPROP_TEXT, curSpreadLastDigit.v)
        else:
            CreateLabelObj('objSpreadLastDigitText', Y_DistanceBidAsk, curSpreadLastDigit.v, bidAskFont, bidAskFontSize, LastDigitColor)
        if ObjectFind(0, 'objSpreadText') == InpWindowIdx:
            ObjectSetString(0, 'objSpreadText', OBJPROP_TEXT, curSpreadStr.v)
            ObjectSetInteger(0, 'objSpreadText', OBJPROP_COLOR, bidAskColor)
        else:
            CreateLabelObj('objSpreadText', Y_DistanceBidAsk, curSpreadStr.v, bidAskFont, bidAskFontSize, bidAskColor)
        if ObjectFind(0, 'objSeparator1') == InpWindowIdx:
            ObjectSetString(0, 'objSeparator1', OBJPROP_TEXT, separator_1.v)
        else:
            CreateLabelObj('objSeparator1', Y_DistanceBidAsk, separator_1.v, bidAskFont, bidAskFontSize, InpSeparatorColor)
        if ObjectFind(0, 'objAskLastDigitText') == InpWindowIdx:
            ObjectSetString(0, 'objAskLastDigitText', OBJPROP_TEXT, curAskLastDigit.v)
        else:
            CreateLabelObj('objAskLastDigitText', Y_DistanceBidAsk, curAskLastDigit.v, bidAskFont, bidAskFontSize, LastDigitColor)
        if ObjectFind(0, 'objAskText') == InpWindowIdx:
            ObjectSetString(0, 'objAskText', OBJPROP_TEXT, curAskStr.v)
            ObjectSetInteger(0, 'objAskText', OBJPROP_COLOR, bidAskColor)
        else:
            CreateLabelObj('objAskText', Y_DistanceBidAsk, curAskStr.v, bidAskFont, bidAskFontSize, bidAskColor)
        if ObjectFind(0, 'objSeparator2') == InpWindowIdx:
            ObjectSetString(0, 'objSeparator2', OBJPROP_TEXT, separator_2.v)
        else:
            CreateLabelObj('objSeparator2', Y_DistanceBidAsk, separator_2.v, bidAskFont, bidAskFontSize, InpSeparatorColor)
        if ObjectFind(0, 'objBidLastDigitText') == InpWindowIdx:
            ObjectSetString(0, 'objBidLastDigitText', OBJPROP_TEXT, curBidLastDigit.v)
        else:
            CreateLabelObj('objBidLastDigitText', Y_DistanceBidAsk, curBidLastDigit.v, bidAskFont, bidAskFontSize, LastDigitColor)
        if ObjectFind(0, 'objBidText') == InpWindowIdx:
            ObjectSetString(0, 'objBidText', OBJPROP_TEXT, curBidStr.v)
            ObjectSetInteger(0, 'objBidText', OBJPROP_COLOR, bidAskColor)
        else:
            CreateLabelObj('objBidText', Y_DistanceBidAsk, curBidStr.v, bidAskFont, bidAskFontSize, bidAskColor)
    if InpShowBidLine == True:
        if ObjectFind(0, 'objBidPointer') == 0:
            ObjectMove(0, 'objBidPointer', 0, Time[0], curBidVal)
            ObjectMove(0, 'objBidPointer', 1, Time[0] + lineExtender, curBidVal)
            ObjectSetInteger(0, 'objBidPointer', OBJPROP_COLOR, bidAskLineColor)
        else:
            ObjectCreate(0, 'objBidPointer', OBJ_TREND, 0, Time[0], curBidVal, Time[0] + lineExtender, curBidVal)
            ObjectSetInteger(0, 'objBidPointer', OBJPROP_STYLE, STYLE_SOLID)
            ObjectSetInteger(0, 'objBidPointer', OBJPROP_RAY_RIGHT, True)
            ObjectSetInteger(0, 'objBidPointer', OBJPROP_RAY_LEFT, InpShowRayLeft)
            ObjectSetInteger(0, 'objBidPointer', OBJPROP_COLOR, bidAskLineColor)
            ObjectSetInteger(0, 'objBidPointer', OBJPROP_BACK, InpDrawAsBackground)
    if InpShowAskLine == True:
        if ObjectFind(0, 'objAskPointer') == 0:
            ObjectMove(0, 'objAskPointer', 0, Time[0], curAskVal)
            ObjectMove(0, 'objAskPointer', 1, Time[0] + lineExtender, curAskVal)
            ObjectSetInteger(0, 'objAskPointer', OBJPROP_COLOR, bidAskLineColor)
        else:
            ObjectCreate(0, 'objAskPointer', OBJ_TREND, 0, Time[0], curAskVal, Time[0] + lineExtender, curAskVal)
            ObjectSetInteger(0, 'objAskPointer', OBJPROP_STYLE, STYLE_DOT)
            ObjectSetInteger(0, 'objAskPointer', OBJPROP_RAY_RIGHT, True)
            ObjectSetInteger(0, 'objAskPointer', OBJPROP_RAY_LEFT, InpShowRayLeft)
            ObjectSetInteger(0, 'objAskPointer', OBJPROP_COLOR, bidAskLineColor)
            ObjectSetInteger(0, 'objAskPointer', OBJPROP_BACK, InpDrawAsBackground)
    if InpShowClock == True:
        if ObjectFind(0, 'objTime') == InpWindowIdx:
            ObjectSetString(0, 'objTime', OBJPROP_TEXT, TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS))
        else:
            CreateLabelObj('objTime', Y_DistanceClock, TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS), clockFont, clockFontSize, InpTimeColor)
    return rates_total

# ---- global variables initialised from expressions
InpMarker_DailyHighLow = _input('InpMarker_DailyHighLow', _uint(DodgerBlue))  # High/low for the day
InpMarker_ChartHighLow = _input('InpMarker_ChartHighLow', _uint(Gold))  # High/low on the chart
InpMarker_AbsHighLow = _input('InpMarker_AbsHighLow', _uint(White))  # Historical high/low
InpBidAskColor = _input('InpBidAskColor', _uint(DodgerBlue))  # Bid/Ask prices
InpLastDigitkColor = _input('InpLastDigitkColor', _uint(DimGray))  # Last digit default color
InpSeparatorColor = _input('InpSeparatorColor', _uint(DimGray))  # Bid/Ask separator
InpTimeColor = _input('InpTimeColor', _uint(DimGray))  # Most recent tick time


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ClearviewPricepointer(_MQL5Indicator):
    name = 'clearview_pricepointer'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPrintHighLow': False,  # Print high/low information when indicator loads
        'InpManualAbsHigh': 0.0,  # Set historical high (0=use monthly chart)
        'InpManualAbsLow': 0.0,  # Set historical low (0=use monthly chart)
        'InpShowBidLine': True,  # Show Bid line
        'InpShowAskLine': True,  # Show Ask line
        'InpShowRayLeft': False,  # Extend price pointer to the left
        'InpProximity_500_1000': 55,  # Alert # of pips around 500/1000 markers
        'InpProximity_DailyHighLow': 10,  # Alert # of pips before high/low for the day
        'InpProximity_ChartHighLow': 55,  # Alert # of pips before high/low on the chart
        'InpProximity_AbsHighLow': 55,  # Alert # of pips before historical high/low
        'InpShowBidAsk': True,  # Show Bid/Ask prices
        'InpChangeLastDigitColor': False,  # Change color of last digit with Bid/Ask
        'InpShowClock': True,  # Show most recent tick time
        'InpBaseCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Corner for Bid/Ask & time
        'InpDrawAsBackground': False,  # Draw objects as background
        'InpWindowIdx': 0,  # Sub-window for Bid/Ask & clock (0=main)
    }

