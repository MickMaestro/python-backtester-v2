"""AverageRangeLines_v1.6 — converted from MQL5: MQL5 Indicators/AverageRangeLines_v1.6/AverageRangeLines_v1.6.mq5

Copyright: Copyright 2020, NickBixy; Link: https://www.forexfactory.com/showthread.php?t=904734

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, NickBixy', 'link': 'https://www.forexfactory.com/showthread.php?t=904734', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'AverageRangeLines_v1.6', 'source': 'MQL5 Indicators/AverageRangeLines_v1.6/AverageRangeLines_v1.6.mq5', 'folder': 'AverageRangeLines_v1.6', 'inputs': [{'mql': 'adrHeader', 'py': 'adrHeader', 'param': None, 'type': 'string', 'default': '-----------------Average Range Settings------------------------------------------', 'label': '----- Average Range Settings', 'sinput': False}, {'mql': 'timeFrame', 'py': 'timeFrame', 'param': 'timeFrame', 'type': 'int', 'default': 16408, 'label': 'TimeFrame', 'sinput': False}, {'mql': 'useShortLines', 'py': 'useShortLines', 'param': 'useShortLines', 'type': 'int', 'default': 1, 'label': 'Draw Short Lines', 'sinput': False}, {'mql': 'Line_Length', 'py': 'Line_Length', 'param': 'Line_Length', 'type': 'int', 'default': 15, 'label': 'Length of Short Line', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'lineLabelHeader', 'py': 'lineLabelHeader', 'param': None, 'type': 'string', 'default': '-----------------Line/Label Customize  Settings------------------------------------------', 'label': '----- Line/Label Customize  Settings', 'sinput': False}, {'mql': 'Font', 'py': 'Font', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'Font', 'sinput': False}, {'mql': 'labelFontSize', 'py': 'labelFontSize', 'param': 'labelFontSize', 'type': 'int', 'default': 8, 'label': 'Font Size', 'sinput': False}, {'mql': 'ShiftLabel', 'py': 'ShiftLabel', 'param': 'ShiftLabel', 'type': 'int', 'default': 10, 'label': 'Label Shift +move right -move left', 'sinput': False}, {'mql': 'highHeader', 'py': 'highHeader', 'param': None, 'type': 'string', 'default': 'High Line/Label Customize--------------------------------------------', 'label': '----- High Line/Label Customize', 'sinput': False}, {'mql': 'customHighMSG', 'py': 'customHighMSG', 'param': None, 'type': 'string', 'default': 'ADR High', 'label': 'High Label custom MSG', 'sinput': False}, {'mql': 'highLineStyle', 'py': 'highLineStyle', 'param': 'highLineStyle', 'type': 'int', 'default': 2, 'label': 'High Line Style', 'sinput': False}, {'mql': 'highLineWidth', 'py': 'highLineWidth', 'param': 'highLineWidth', 'type': 'int', 'default': 1, 'label': 'High Line Width', 'sinput': False}, {'mql': 'highLineClr', 'py': 'highLineClr', 'param': None, 'type': 'color', 'default': 42495, 'label': 'High Line Color', 'sinput': False}, {'mql': 'highLabelClr', 'py': 'highLabelClr', 'param': None, 'type': 'color', 'default': 42495, 'label': 'High Label Color', 'sinput': False}, {'mql': 'lowHeader', 'py': 'lowHeader', 'param': None, 'type': 'string', 'default': 'Low Line/Label Customize--------------------------------------------', 'label': '----- Low Line/Label Customize', 'sinput': False}, {'mql': 'customLowMSG', 'py': 'customLowMSG', 'param': None, 'type': 'string', 'default': 'ADR Low', 'label': 'Low Label custom MSG', 'sinput': False}, {'mql': 'lowLineStyle', 'py': 'lowLineStyle', 'param': 'lowLineStyle', 'type': 'int', 'default': 2, 'label': 'Low Line Style', 'sinput': False}, {'mql': 'lowLineWidth', 'py': 'lowLineWidth', 'param': 'lowLineWidth', 'type': 'int', 'default': 1, 'label': 'Low Line Width', 'sinput': False}, {'mql': 'lowLineClr', 'py': 'lowLineClr', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Low Line Color', 'sinput': False}, {'mql': 'lowLabelClr', 'py': 'lowLabelClr', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Low Label Color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

SYMBOL_SWAP_MODE = 0  # MQL5 constant unknown to the converter

# enum pipPointChoice
Pips = 0
Points = 1
_enum('pipPointChoice', {0: 'Pips', 1: 'Points'})

# enum yesnoChoiceToggle
No = 0
Yes = 1
_enum('yesnoChoiceToggle', {0: 'No', 1: 'Yes'})

# ---- inputs and global variables
adrHeader = _input('adrHeader', '-----------------Average Range Settings------------------------------------------')  # ----- Average Range Settings
timeFrame = _input('timeFrame', PERIOD_D1)  # TimeFrame
useShortLines = _input('useShortLines', Yes)  # Draw Short Lines
Line_Length = _input('Line_Length', 15)  # Length of Short Line
period = _input('period', 14)  # Period
lineLabelHeader = _input('lineLabelHeader', '-----------------Line/Label Customize  Settings------------------------------------------')  # ----- Line/Label Customize  Settings
Font = _input('Font', 'Arial')  # Font
labelFontSize = _input('labelFontSize', 8)  # Font Size
ShiftLabel = _input('ShiftLabel', 10)  # Label Shift +move right -move left
highHeader = _input('highHeader', 'High Line/Label Customize--------------------------------------------')  # ----- High Line/Label Customize
customHighMSG = _input('customHighMSG', 'ADR High')  # High Label custom MSG
highLineStyle = _input('highLineStyle', STYLE_DOT)  # High Line Style
highLineWidth = _input('highLineWidth', 1)  # High Line Width
highLineClr = _input('highLineClr', clrOrange)  # High Line Color
highLabelClr = _input('highLabelClr', clrOrange)  # High Label Color
lowHeader = _input('lowHeader', 'Low Line/Label Customize--------------------------------------------')  # ----- Low Line/Label Customize
customLowMSG = _input('customLowMSG', 'ADR Low')  # Low Label custom MSG
lowLineStyle = _input('lowLineStyle', STYLE_DOT)  # Low Line Style
lowLineWidth = _input('lowLineWidth', 1)  # Low Line Width
lowLineClr = _input('lowLineClr', clrOrange)  # Low Line Color
lowLabelClr = _input('lowLabelClr', clrOrange)  # Low Label Color

def OnInit():
    global indiName
    if period < 1:
        Alert("Period can't be less than 1")
    ObjectsDeleteAll(0, indiName, 0, OBJ_TREND)
    ObjectsDeleteAll(0, indiName, 0, OBJ_TEXT)
    indiName = 'ARL' + ' ' + EnumToString(timeFrame, 'ENUM_TIMEFRAMES') + ' ' + _str(period)
    return INIT_SUCCEEDED

def deinit():
    ObjectsDeleteAll(0, indiName, 0, OBJ_TREND)
    ObjectsDeleteAll(0, indiName, 0, OBJ_TEXT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    DrawRangeLines()
    return 0

def DrawRangeLines():
    timeframeValue = 0
    _sw1 = Period()
    if _sw1 == PERIOD_M1:
        timeframeValue = 1
    elif _sw1 == PERIOD_M2:
        timeframeValue = 2
    elif _sw1 == PERIOD_M3:
        timeframeValue = 3
    elif _sw1 == PERIOD_M4:
        timeframeValue = 4
    elif _sw1 == PERIOD_M5:
        timeframeValue = 5
    elif _sw1 == PERIOD_M6:
        timeframeValue = 6
    elif _sw1 == PERIOD_M10:
        timeframeValue = 10
    elif _sw1 == PERIOD_M12:
        timeframeValue = 12
    elif _sw1 == PERIOD_M15:
        timeframeValue = 15
    elif _sw1 == PERIOD_M20:
        timeframeValue = 20
    elif _sw1 == PERIOD_M30:
        timeframeValue = 30
    elif _sw1 == PERIOD_H1:
        timeframeValue = 60
    elif _sw1 == PERIOD_H2:
        timeframeValue = 240
    elif _sw1 == PERIOD_H3:
        timeframeValue = 180
    elif _sw1 == PERIOD_H4:
        timeframeValue = 240
    elif _sw1 == PERIOD_H6:
        timeframeValue = 360
    elif _sw1 == PERIOD_H8:
        timeframeValue = 480
    elif _sw1 == PERIOD_H12:
        timeframeValue = 720
    elif _sw1 == PERIOD_D1:
        timeframeValue = 1440
    elif _sw1 == PERIOD_W1:
        timeframeValue = 10080
    elif _sw1 == PERIOD_MN1:
        timeframeValue = 43200
    highMSG = ''
    lowMSG = ''
    highMSG = customHighMSG
    lowMSG = customLowMSG
    Time = Arr(0, 0)
    count = 2
    ArraySetAsSeries(Time, True)
    CopyTime(Symbol(), Period(), 0, count, Time)
    highLine = indiName + ' High'
    if ObjectFindMQL4(highLine) != 0:
        if useShortLines == Yes:
            ObjectCreateMQL4(highLine, OBJ_TREND, 0, Time[1] + (timeframeValue * 60), GetAverageRangeHigh(), Time[0] + (timeframeValue * 60 * Line_Length), GetAverageRangeHigh())
            ObjectSetMQL4(highLine, OBJPROP_RAY, False)
        else:
            ObjectCreateMQL4(highLine, OBJ_TREND, 0, iTime(None, timeFrame, 0), GetAverageRangeHigh(), Time[0] + (timeframeValue * 60), GetAverageRangeHigh())
            ObjectSetMQL4(highLine, OBJPROP_RAY, True)
        ObjectSetMQL4(highLine, OBJPROP_COLOR, highLineClr)
        ObjectSetMQL4(highLine, OBJPROP_STYLE, highLineStyle)
        ObjectSetMQL4(highLine, OBJPROP_WIDTH, highLineWidth)
        ObjectSetMQL4(highLine, OBJPROP_BACK, True)
        ObjectSetMQL4(highLine, OBJPROP_SELECTED, False)
        ObjectSetMQL4(highLine, OBJPROP_SELECTABLE, False)
    else:
        if useShortLines == Yes:
            ObjectSetMQL4(highLine, OBJPROP_RAY, False)
            ObjectMoveMQL4(highLine, 0, Time[1] + (timeframeValue * 60), GetAverageRangeHigh())
            ObjectMoveMQL4(highLine, 1, Time[0] + (timeframeValue * 60 * Line_Length), GetAverageRangeHigh())
        else:
            ObjectSetMQL4(highLine, OBJPROP_RAY, True)
            ObjectMoveMQL4(highLine, 0, iTime(None, timeFrame, 0), GetAverageRangeHigh())
            ObjectMoveMQL4(highLine, 1, Time[0] + (timeframeValue * 60), GetAverageRangeHigh())
    lowLine = indiName + ' LOW'
    if ObjectFindMQL4(lowLine) != 0:
        if useShortLines == Yes:
            ObjectCreateMQL4(lowLine, OBJ_TREND, 0, Time[1] + (timeframeValue * 60), GetAverageRangeLow(), Time[0] + (timeframeValue * 60 * Line_Length), GetAverageRangeLow())
            ObjectSetMQL4(lowLine, OBJPROP_RAY, False)
        else:
            ObjectCreateMQL4(lowLine, OBJ_TREND, 0, iTime(None, timeFrame, 0), GetAverageRangeLow(), Time[0] + (timeframeValue * 60), GetAverageRangeLow())
            ObjectSetMQL4(lowLine, OBJPROP_RAY, True)
        ObjectSetMQL4(lowLine, OBJPROP_COLOR, lowLineClr)
        ObjectSetMQL4(lowLine, OBJPROP_STYLE, lowLineStyle)
        ObjectSetMQL4(lowLine, OBJPROP_WIDTH, lowLineWidth)
        ObjectSetMQL4(lowLine, OBJPROP_BACK, True)
        ObjectSetMQL4(lowLine, OBJPROP_SELECTED, False)
        ObjectSetMQL4(lowLine, OBJPROP_SELECTABLE, False)
    else:
        if useShortLines == Yes:
            ObjectSetMQL4(lowLine, OBJPROP_RAY, False)
            ObjectMoveMQL4(lowLine, 0, Time[1] + (timeframeValue * 60), GetAverageRangeLow())
            ObjectMoveMQL4(lowLine, 1, Time[0] + (timeframeValue * 60 * Line_Length), GetAverageRangeLow())
        else:
            ObjectSetMQL4(lowLine, OBJPROP_RAY, True)
            ObjectMoveMQL4(lowLine, 0, iTime(None, timeFrame, 0), GetAverageRangeLow())
            ObjectMoveMQL4(lowLine, 1, Time[0] + (timeframeValue * 60), GetAverageRangeLow())
    highLabel = indiName + ' HighLabel'
    if ObjectFindMQL4(highLabel) != 0:
        ObjectCreateMQL4(highLabel, OBJ_TEXT, 0, Time[0] + (timeframeValue * 60 * ShiftLabel), GetAverageRangeHigh())
        ObjectSetTextMQL4(highLabel, highMSG, labelFontSize, Font, highLabelClr)
        ObjectSetMQL4(highLabel, OBJPROP_BACK, True)
        ObjectSetMQL4(highLabel, OBJPROP_SELECTED, False)
        ObjectSetMQL4(highLabel, OBJPROP_SELECTABLE, False)
    else:
        ObjectMoveMQL4(highLabel, 0, Time[0] + (timeframeValue * 60 * ShiftLabel), GetAverageRangeHigh())
        ObjectSetTextMQL4(highLabel, highMSG, labelFontSize, Font, highLabelClr)
    lowLabel = indiName + ' LowLabel'
    if ObjectFindMQL4(lowLabel) != 0:
        ObjectCreateMQL4(lowLabel, OBJ_TEXT, 0, Time[0] + (timeframeValue * 60 * ShiftLabel), GetAverageRangeLow())
        ObjectSetTextMQL4(lowLabel, lowMSG, labelFontSize, Font, lowLabelClr)
        ObjectSetMQL4(lowLabel, OBJPROP_BACK, True)
        ObjectSetMQL4(lowLabel, OBJPROP_SELECTED, False)
        ObjectSetMQL4(lowLabel, OBJPROP_SELECTABLE, False)
    else:
        ObjectMoveMQL4(lowLabel, 0, Time[0] + (timeframeValue * 60 * ShiftLabel), GetAverageRangeLow())
        ObjectSetTextMQL4(lowLabel, lowMSG, labelFontSize, Font, lowLabelClr)
    ChartRedraw(0)

def GetBidAverageRangeDistancePipsPoints(rangeValue):
    value = 0.0
    bid = MarketInfoMQL4("", 9)
    points = MarketInfoMQL4("", 11)
    if ((rangeValue != 0 and rangeValue != 0) and bid != 0) and bid != 0:
        value = _fdiv(rangeValue - bid, points)
    return value

def GetAverageRangeRatioPipsPoints():
    value = 0.0
    todayRange = GetTodayRangePipsPoints()
    averageRangeNumPeriods = GetAverageRangeNumPeriodsPipsPoints()
    if (todayRange != 0 and todayRange != 0) and (averageRangeNumPeriods != 0 and averageRangeNumPeriods != 0):
        value = _fdiv(todayRange, averageRangeNumPeriods) * 100
    return value

def PipsToPointFactor():
    point = 1
    if Digits() == 5 or Digits() == 3:
        point = 10
    elif Digits() == 4 or Digits() == 2:
        point = 1
    elif Digits() == 1:
        point = 1
    return point

def GetAverageRangeNumPeriodsPipsPoints():
    value = GetAverageRangeNumPeriods()
    points = MarketInfoMQL4("", 11)
    if ((value != 0 and value != 0) and points != 0) and points != 0:
        value = _fdiv(value, points)
    return value

def GetTodayRangePipsPoints():
    value = 0.0
    points = MarketInfoMQL4("", 11)
    high = iHigh(None, timeFrame, 0)
    low = iLow(None, timeFrame, 0)
    value = MathAbs(high - low)
    if ((value != 0 and value != 0) and points != 0) and points != 0:
        value = _fdiv(value, points)
    return value

def GetAverageRangeNumPeriods():
    result = 0.0
    averageRange = 0.0
    for i in range(1, period + 1):
        if timeFrame == PERIOD_D1:
            dayCheck1 = iTime(None, PERIOD_D1, i)
            if TimeDayOfWeekMQL4(dayCheck1) == 0:
                continue
            dayCheck2 = iTime(None, PERIOD_D1, i)
            if TimeDayOfWeekMQL4(dayCheck2) == 6:
                continue
        high = iHigh(None, timeFrame, i)
        low = iLow(None, timeFrame, i)
        averageRange += high - low
    return (result := averageRange / period)

def GetTimeFrameHighestHigh():
    return iHigh(None, timeFrame, 0)

def GetTimeFrameLowestLow():
    return iLow(None, timeFrame, 0)

def GetAverageRangeHigh():
    todayHigh = iHigh(None, timeFrame, 0)
    todayLow = iLow(None, timeFrame, 0)
    rangeHigh = GetTimeFrameLowestLow() + GetAverageRangeNumPeriods()
    averageRange = GetAverageRangeNumPeriods()
    if (todayHigh - todayLow) > averageRange:
        if MarketInfoMQL4("", 9) >= (todayHigh - ((todayHigh - todayLow) / 2)):
            rangeHigh = todayLow + averageRange
        else:
            rangeHigh = todayHigh
    return rangeHigh

def GetAverageRangeLow():
    todayHigh = iHigh(None, timeFrame, 0)
    todayLow = iLow(None, timeFrame, 0)
    rangeLow = GetTimeFrameHighestHigh() - GetAverageRangeNumPeriods()
    averageRange = GetAverageRangeNumPeriods()
    if (todayHigh - todayLow) > averageRange:
        if MarketInfoMQL4("", 9) >= (todayHigh - ((todayHigh - todayLow) / 2)):
            rangeLow = todayLow
        else:
            rangeLow = todayHigh - averageRange
    return rangeLow

def ObjectFindMQL4(name):
    return ObjectFind(0, name)

def ObjectSetMQL4(name, index, value):
    _sw2 = index
    if _sw2 == 300:
        ObjectSetInteger(0, name, OBJPROP_TIME, _int(value))
        return True
    elif _sw2 == 301:
        ObjectSetDouble(0, name, OBJPROP_PRICE, value)
        return True
    elif _sw2 == 302:
        ObjectSetInteger(0, name, OBJPROP_TIME, 1, _int(value))
        return True
    elif _sw2 == 303:
        ObjectSetDouble(0, name, OBJPROP_PRICE, 1, value)
        return True
    elif _sw2 == 304:
        ObjectSetInteger(0, name, OBJPROP_TIME, 2, _int(value))
        return True
    elif _sw2 == 305:
        ObjectSetDouble(0, name, OBJPROP_PRICE, 2, value)
        return True
    elif _sw2 == OBJPROP_COLOR:
        ObjectSetInteger(0, name, OBJPROP_COLOR, _int(value))
        return True
    elif _sw2 == OBJPROP_STYLE:
        ObjectSetInteger(0, name, OBJPROP_STYLE, _int(value))
        return True
    elif _sw2 == OBJPROP_WIDTH:
        ObjectSetInteger(0, name, OBJPROP_WIDTH, _int(value))
        return True
    elif _sw2 == OBJPROP_BACK:
        ObjectSetInteger(0, name, OBJPROP_BACK, _int(value))
        return True
    elif _sw2 == OBJPROP_RAY:
        ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, _int(value))
        return True
    elif _sw2 == OBJPROP_ELLIPSE:
        ObjectSetInteger(0, name, OBJPROP_ELLIPSE, _int(value))
        return True
    elif _sw2 == OBJPROP_SCALE:
        ObjectSetDouble(0, name, OBJPROP_SCALE, value)
        return True
    elif _sw2 == OBJPROP_ANGLE:
        ObjectSetDouble(0, name, OBJPROP_ANGLE, value)
        return True
    elif _sw2 == OBJPROP_ARROWCODE:
        ObjectSetInteger(0, name, OBJPROP_ARROWCODE, _int(value))
        return True
    elif _sw2 == OBJPROP_TIMEFRAMES:
        ObjectSetInteger(0, name, OBJPROP_TIMEFRAMES, _int(value))
        return True
    elif _sw2 == OBJPROP_DEVIATION:
        ObjectSetDouble(0, name, OBJPROP_DEVIATION, value)
        return True
    elif _sw2 == OBJPROP_FONTSIZE:
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, _int(value))
        return True
    elif _sw2 == OBJPROP_CORNER:
        ObjectSetInteger(0, name, OBJPROP_CORNER, _int(value))
        return True
    elif _sw2 == OBJPROP_XDISTANCE:
        ObjectSetInteger(0, name, OBJPROP_XDISTANCE, _int(value))
        return True
    elif _sw2 == OBJPROP_YDISTANCE:
        ObjectSetInteger(0, name, OBJPROP_YDISTANCE, _int(value))
        return True
    elif _sw2 == 200:
        ObjectSetInteger(0, name, OBJPROP_LEVELS, _int(value))
        return True
    elif _sw2 == OBJPROP_LEVELCOLOR:
        ObjectSetInteger(0, name, OBJPROP_LEVELCOLOR, _int(value))
        return True
    elif _sw2 == OBJPROP_LEVELSTYLE:
        ObjectSetInteger(0, name, OBJPROP_LEVELSTYLE, _int(value))
        return True
    elif _sw2 == OBJPROP_LEVELWIDTH:
        ObjectSetInteger(0, name, OBJPROP_LEVELWIDTH, _int(value))
        return True
    else:
        return False
    return False

def ObjectMoveMQL4(name, point, time1, price1):
    return ObjectMove(0, name, point, time1, price1)

def ObjectCreateMQL4(name, type_, window, time1, price1, time2=0, price2=0.0, time3=0, price3=0.0):
    return ObjectCreate(0, name, type_, window, time1, price1, time2, price2, time3, price3)

def ObjectSetTextMQL4(name, text, font_size, font='', text_color=CLR_NONE):
    tmpObjType = _int(ObjectGetInteger(0, name, OBJPROP_TYPE))
    if tmpObjType != OBJ_LABEL and tmpObjType != OBJ_TEXT:
        return False
    if StringLen(text) > 0 and font_size > 0:
        if ObjectSetString(0, name, OBJPROP_TEXT, text) == True and ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size) == True:
            if StringLen(font) > 0 and ObjectSetString(0, name, OBJPROP_FONT, font) == False:
                return False
            if text_color > -1 and ObjectSetInteger(0, name, OBJPROP_COLOR, text_color) == False:
                return False
            return True
        return False
    return False

def MarketInfoMQL4(symbol, type_):
    _sw3 = type_
    if _sw3 == 1:
        return SymbolInfoDouble(symbol, SYMBOL_LASTLOW)
    elif _sw3 == 2:
        return SymbolInfoDouble(symbol, SYMBOL_LASTHIGH)
    elif _sw3 == 5:
        return SymbolInfoInteger(symbol, SYMBOL_TIME)
    elif _sw3 == 11:
        return SymbolInfoDouble(symbol, SYMBOL_POINT)
    elif _sw3 == 12:
        return SymbolInfoInteger(symbol, SYMBOL_DIGITS)
    elif _sw3 == 13:
        return SymbolInfoInteger(symbol, SYMBOL_SPREAD)
    elif _sw3 == 14:
        return SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL)
    elif _sw3 == 15:
        return SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE)
    elif _sw3 == 16:
        return SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)
    elif _sw3 == 17:
        return SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)
    elif _sw3 == 18:
        return SymbolInfoDouble(symbol, SYMBOL_SWAP_LONG)
    elif _sw3 == 19:
        return SymbolInfoDouble(symbol, SYMBOL_SWAP_SHORT)
    elif _sw3 == 20:
        return 0.0
    elif _sw3 == 21:
        return 0.0
    elif _sw3 == 22:
        return 0.0
    elif _sw3 == 23:
        return SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN)
    elif _sw3 == 24:
        return SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP)
    elif _sw3 == 25:
        return SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX)
    elif _sw3 == 26:
        return SymbolInfoInteger(symbol, SYMBOL_SWAP_MODE)
    elif _sw3 == 27:
        return SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE)
    elif _sw3 == 28:
        return 0.0
    elif _sw3 == 29:
        return 0.0
    elif _sw3 == 30:
        return 0.0
    elif _sw3 == 31:
        return 0.0
    elif _sw3 == 32:
        return 0.0
    elif _sw3 == 33:
        return SymbolInfoInteger(symbol, SYMBOL_TRADE_FREEZE_LEVEL)
    else:
        return 0.0
    return 0.0

def TimeDayOfWeekMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day_of_week

# ---- global variables initialised from expressions
indiName = 'ARL' + ' ' + EnumToString(timeFrame, 'ENUM_TIMEFRAMES') + ' ' + _str(period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AverageRangeLinesV16(_MQL5Indicator):
    name = 'AverageRangeLines_v1.6'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'timeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # TimeFrame
        'useShortLines': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Draw Short Lines
        'Line_Length': 15,  # Length of Short Line
        'period': 14,  # Period
        'labelFontSize': 8,  # Font Size
        'ShiftLabel': 10,  # Label Shift +move right -move left
        'highLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # High Line Style
        'highLineWidth': 1,  # High Line Width
        'lowLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Low Line Style
        'lowLineWidth': 1,  # Low Line Width
    }

