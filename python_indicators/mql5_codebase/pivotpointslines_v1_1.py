"""PivotPointsLines_v1.1 — converted from MQL5: MQL5 Indicators/PivotPointsLines _v1.1/PivotPointsLines_v1.1.mq5

Copyright: Copyright 2020, NickBixy; Link: https://www.forexfactory.com/showthread.php?t=904734

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, NickBixy', 'link': 'https://www.forexfactory.com/showthread.php?t=904734', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'PivotPointsLines_v1.1', 'source': 'MQL5 Indicators/PivotPointsLines _v1.1/PivotPointsLines_v1.1.mq5', 'folder': 'PivotPointsLines _v1.1', 'inputs': [{'mql': 'Header', 'py': 'Header', 'param': None, 'type': 'string', 'default': '----------------- Pivot Point Settings------------------------------------------', 'label': '----- Pivot Point Settings', 'sinput': False}, {'mql': 'pivotSelection', 'py': 'pivotSelection', 'param': 'pivotSelection', 'type': 'int', 'default': 0, 'label': 'Pivot Point Formula', 'sinput': False}, {'mql': 'drawFloorMidPP', 'py': 'drawFloorMidPP', 'param': 'drawFloorMidPP', 'type': 'int', 'default': 0, 'label': 'Draw Floor Mid Pivot Points?', 'sinput': False}, {'mql': 'showPriceLabel', 'py': 'showPriceLabel', 'param': 'showPriceLabel', 'type': 'int', 'default': 0, 'label': 'Show Price In Label?', 'sinput': False}, {'mql': 'timeFrame', 'py': 'timeFrame', 'param': 'timeFrame', 'type': 'int', 'default': 16408, 'label': 'TimeFrame', 'sinput': False}, {'mql': 'Header2', 'py': 'Header2', 'param': None, 'type': 'string', 'default': '----------------- Pivot Point Line/Label Customize Settings------------------------------------------', 'label': '----- Pivot Point Line/Label Customize Settings', 'sinput': False}, {'mql': 'customMSG', 'py': 'customMSG', 'param': None, 'type': 'string', 'default': '', 'label': 'Custom Message Before Pivot Name', 'sinput': False}, {'mql': 'useShortLines', 'py': 'useShortLines', 'param': 'useShortLines', 'type': 'int', 'default': 1, 'label': 'Draw Short Lines', 'sinput': False}, {'mql': 'Line_Length', 'py': 'Line_Length', 'param': 'Line_Length', 'type': 'int', 'default': 15, 'label': 'Length of Short Line', 'sinput': False}, {'mql': 'lineStyle', 'py': 'lineStyle', 'param': 'lineStyle', 'type': 'int', 'default': 0, 'label': 'Line Style', 'sinput': False}, {'mql': 'lineWidth', 'py': 'lineWidth', 'param': 'lineWidth', 'type': 'int', 'default': 1, 'label': 'Line Width', 'sinput': False}, {'mql': 'Font', 'py': 'Font', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'Label Font', 'sinput': False}, {'mql': 'labelFontSize', 'py': 'labelFontSize', 'param': 'labelFontSize', 'type': 'int', 'default': 8, 'label': 'Label Font Size', 'sinput': False}, {'mql': 'ShiftLabel', 'py': 'ShiftLabel', 'param': 'ShiftLabel', 'type': 'int', 'default': 10, 'label': 'Label Shift +move right -move left', 'sinput': False}, {'mql': 'useSameColorLabelChoice', 'py': 'useSameColorLabelChoice', 'param': 'useSameColorLabelChoice', 'type': 'int', 'default': 0, 'label': 'Label use Same Color?', 'sinput': False}, {'mql': 'useSameColorLabelColor', 'py': 'useSameColorLabelColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'Label Color for Label use Same Color', 'sinput': False}, {'mql': 'resistantColor', 'py': 'resistantColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Resistant Line/Label Color', 'sinput': False}, {'mql': 'pivotColor', 'py': 'pivotColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Pivot Line/Label Color', 'sinput': False}, {'mql': 'supportColor', 'py': 'supportColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Support Line/Label PP Color', 'sinput': False}, {'mql': 'midColor', 'py': 'midColor', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Mid PP Line/Label Color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

SYMBOL_SWAP_MODE = 0  # MQL5 constant unknown to the converter

# enum pivotTypes
Standard = 0
Fibonacci = 1
Camarilla = 2
Woodie = 3
_enum('pivotTypes', {0: 'Standard', 1: 'Fibonacci', 2: 'Camarilla', 3: 'Woodie'})

# enum yesnoChoiceToggle
No = 0
Yes = 1
_enum('yesnoChoiceToggle', {0: 'No', 1: 'Yes'})

# ---- inputs and global variables
Header = _input('Header', '----------------- Pivot Point Settings------------------------------------------')  # ----- Pivot Point Settings
pivotSelection = _input('pivotSelection', Standard)  # Pivot Point Formula
drawFloorMidPP = _input('drawFloorMidPP', No)  # Draw Floor Mid Pivot Points?
showPriceLabel = _input('showPriceLabel', No)  # Show Price In Label?
timeFrame = _input('timeFrame', PERIOD_D1)  # TimeFrame
Header2 = _input('Header2', '----------------- Pivot Point Line/Label Customize Settings------------------------------------------')  # ----- Pivot Point Line/Label Customize Settings
customMSG = _input('customMSG', '')  # Custom Message Before Pivot Name
useShortLines = _input('useShortLines', Yes)  # Draw Short Lines
Line_Length = _input('Line_Length', 15)  # Length of Short Line
lineStyle = _input('lineStyle', STYLE_SOLID)  # Line Style
lineWidth = _input('lineWidth', 1)  # Line Width
Font = _input('Font', 'Arial')  # Label Font
labelFontSize = _input('labelFontSize', 8)  # Label Font Size
ShiftLabel = _input('ShiftLabel', 10)  # Label Shift +move right -move left
useSameColorLabelChoice = _input('useSameColorLabelChoice', No)  # Label use Same Color?
useSameColorLabelColor = _input('useSameColorLabelColor', clrWhite)  # Label Color for Label use Same Color
resistantColor = _input('resistantColor', clrDodgerBlue)  # Resistant Line/Label Color
pivotColor = _input('pivotColor', clrMagenta)  # Pivot Line/Label Color
supportColor = _input('supportColor', clrRed)  # Support Line/Label PP Color
midColor = _input('midColor', clrGreen)  # Mid PP Line/Label Color
camarillaPivotNames = Arr.of(['PP', 'S1', 'S2', 'S3', 'S4', 'R1', 'R2', 'R3', 'R4', 'R5', 'S5'], fill="")
camarillaValueArray = Arr(11, 0.0, dyn=False)
standardPivotNames = Arr.of(['PP', 'S1', 'S2', 'S3', 'R1', 'R2', 'R3', 'R4', 'S4', 'MR4', 'MR3', 'MR2', 'MR1', 'MS1', 'MS2', 'MS3', 'MS4'], fill="")
standardValueArray = Arr(17, 0.0, dyn=False)
woodiePivotNames = Arr.of(['PP', 'S1', 'S2', 'R1', 'R2', 'S3', 'S4', 'R3', 'R4'], fill="")
woodieValueArray = Arr(9, 0.0, dyn=False)
fibonacciPivotNames = Arr.of(['PP', 'R38', 'R61', 'R78', 'R100', 'R138', 'R161', 'R200', 'S38', 'S61', 'S78', 'S100', 'S138', 'S161', 'S200'], fill="")
fibonacciValueArray = Arr(15, 0.0, dyn=False)

def OnInit():
    ObjectsDeleteAll(0, indiName, 0, OBJ_TREND)
    ObjectsDeleteAll(0, indiName, 0, OBJ_TEXT)
    return INIT_SUCCEEDED

def deinit():
    ObjectsDeleteAll(0, indiName, 0, OBJ_TREND)
    ObjectsDeleteAll(0, indiName, 0, OBJ_TEXT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if pivotSelection == Camarilla:
        camarillaPivotPoint(camarillaValueArray)
        i = 0
        while i < ArraySize(camarillaValueArray):
            DrawPivotLines(camarillaValueArray[i], camarillaPivotNames[i])
            i += 1
    if pivotSelection == Standard:
        if drawFloorMidPP == Yes:
            standardPivotPoint(standardValueArray)
            for i in range(0, 17):
                DrawPivotLines(standardValueArray[i], standardPivotNames[i])
        else:
            standardPivotPoint(standardValueArray)
            for i in range(0, 9):
                DrawPivotLines(standardValueArray[i], standardPivotNames[i])
    if pivotSelection == Fibonacci:
        fibonacciPivotPoint(fibonacciValueArray)
        i = 0
        while i < ArraySize(fibonacciValueArray):
            DrawPivotLines(fibonacciValueArray[i], fibonacciPivotNames[i])
            i += 1
    if pivotSelection == Woodie:
        woodiePivotPoint(woodieValueArray)
        i = 0
        while i < ArraySize(woodieValueArray):
            DrawPivotLines(woodieValueArray[i], woodiePivotNames[i])
            i += 1
    return 0

def DrawPivotLines(value, pivotName):
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
    Time = Arr(0, 0)
    count = 2
    ArraySetAsSeries(Time, True)
    CopyTime(Symbol(), Period(), 0, count, Time)
    lineLabelColor = clrNONE
    message = 'Poop'
    if showPriceLabel == Yes:
        message = customMSG + pivotName + ': ' + DoubleToString(value, Digits())
    else:
        message = customMSG + pivotName
    if 82 == StringGetCharacter(pivotName, 0):
        lineLabelColor = resistantColor
    elif 80 == StringGetCharacter(pivotName, 0):
        lineLabelColor = pivotColor
    elif 83 == StringGetCharacter(pivotName, 0):
        lineLabelColor = supportColor
    elif 77 == StringGetCharacter(pivotName, 0):
        lineLabelColor = midColor
    nameLine = indiName + ' ' + EnumToString(pivotSelection, 'pivotTypes') + EnumToString(timeFrame, 'ENUM_TIMEFRAMES') + pivotName + ' Line'
    nameLabel = indiName + ' ' + EnumToString(pivotSelection, 'pivotTypes') + EnumToString(timeFrame, 'ENUM_TIMEFRAMES') + pivotName + ' Label'
    if ObjectFindMQL4(nameLine) != 0:
        if useShortLines == Yes:
            ObjectCreateMQL4(nameLine, OBJ_TREND, 0, Time[1] + (timeframeValue * 60), value, Time[0] + (timeframeValue * 60 * Line_Length), value)
            ObjectSetMQL4(nameLine, 310, False)
        else:
            ObjectCreateMQL4(nameLine, OBJ_TREND, 0, iTime(None, timeFrame, 0), value, Time[0] + (timeframeValue * 60), value)
            ObjectSetMQL4(nameLine, 310, True)
        ObjectSetMQL4(nameLine, OBJPROP_COLOR, lineLabelColor)
        ObjectSetMQL4(nameLine, OBJPROP_STYLE, lineStyle)
        ObjectSetMQL4(nameLine, OBJPROP_WIDTH, lineWidth)
        ObjectSetMQL4(nameLine, OBJPROP_BACK, True)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTED, False)
        ObjectSetMQL4(nameLine, OBJPROP_SELECTABLE, False)
    else:
        if useShortLines == Yes:
            ObjectSetMQL4(nameLine, 310, False)
            ObjectMoveMQL4(nameLine, 0, Time[1] + (timeframeValue * 60), value)
            ObjectMoveMQL4(nameLine, 1, Time[0] + (timeframeValue * 60 * Line_Length), value)
        else:
            ObjectSetMQL4(nameLine, 310, True)
            ObjectMoveMQL4(nameLine, 0, iTime(None, timeFrame, 0), value)
            ObjectMoveMQL4(nameLine, 1, Time[0] + (timeframeValue * 60), value)
    if ObjectFindMQL4(nameLabel) != 0:
        ObjectCreateMQL4(nameLabel, OBJ_TEXT, 0, Time[0] + (timeframeValue * 60 * ShiftLabel), value)
        if useSameColorLabelChoice == Yes:
            ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, useSameColorLabelColor)
        else:
            ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, lineLabelColor)
        ObjectSetMQL4(nameLabel, OBJPROP_BACK, True)
        ObjectSetMQL4(nameLabel, OBJPROP_SELECTED, False)
        ObjectSetMQL4(nameLabel, OBJPROP_SELECTABLE, False)
    else:
        ObjectMoveMQL4(nameLabel, 0, Time[0] + (timeframeValue * 60 * ShiftLabel), value)
        if useSameColorLabelChoice == Yes:
            ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, useSameColorLabelColor)
        else:
            ObjectSetTextMQL4(nameLabel, message, labelFontSize, Font, lineLabelColor)
    ChartRedraw(0)

def camarillaPivotPoint(ppArrayRef):
    shift = 1
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    camRange = iHigh(None, timeFrame, shift) - iLow(None, timeFrame, shift)
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    symbolDigits = _int(MarketInfoMQL4("", 12))
    R1 = ((1.1 / 12) * camRange) + prevClose
    R2 = ((1.1 / 6) * camRange) + prevClose
    R3 = ((1.1 / 4) * camRange) + prevClose
    R4 = ((1.1 / 2) * camRange) + prevClose
    S1 = prevClose - ((1.1 / 12) * camRange)
    S2 = prevClose - ((1.1 / 6) * camRange)
    S3 = prevClose - ((1.1 / 4) * camRange)
    S4 = prevClose - ((1.1 / 2) * camRange)
    PP = (R4 + S4) / 2
    R5 = _fdiv(prevHigh, prevLow) * prevClose
    S5 = prevClose - (R5 - prevClose)
    ppArrayRef[0] = PP
    ppArrayRef[1] = S1
    ppArrayRef[2] = S2
    ppArrayRef[3] = S3
    ppArrayRef[4] = S4
    ppArrayRef[5] = R1
    ppArrayRef[6] = R2
    ppArrayRef[7] = R3
    ppArrayRef[8] = R4
    ppArrayRef[9] = R5
    ppArrayRef[10] = S5

def standardPivotPoint(ppArrayRef):
    shift = 1
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    PP = (prevHigh + prevLow + prevClose) / 3
    R1 = (PP * 2) - prevLow
    S1 = (PP * 2) - prevHigh
    R2 = PP + prevHigh - prevLow
    S2 = PP - prevHigh + prevLow
    R3 = R1 + (prevHigh - prevLow)
    S3 = prevLow - (2 * (prevHigh - PP))
    R4 = R3 + (R2 - R1)
    S4 = S3 - (S1 - S2)
    ppArrayRef[0] = PP
    ppArrayRef[1] = S1
    ppArrayRef[2] = S2
    ppArrayRef[3] = S3
    ppArrayRef[4] = R1
    ppArrayRef[5] = R2
    ppArrayRef[6] = R3
    ppArrayRef[7] = R4
    ppArrayRef[8] = S4
    if drawFloorMidPP == Yes:
        ppArrayRef[9] = (R3 + R4) / 2
        ppArrayRef[10] = (R2 + R3) / 2
        ppArrayRef[11] = (R1 + R2) / 2
        ppArrayRef[12] = (PP + R1) / 2
        ppArrayRef[13] = (PP + S1) / 2
        ppArrayRef[14] = (S1 + S2) / 2
        ppArrayRef[15] = (S2 + S3) / 2
        ppArrayRef[16] = (S3 + S4) / 2

def woodiePivotPoint(ppArrayRef):
    shift = 1
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    prevRange = iHigh(None, timeFrame, shift) - iLow(None, timeFrame, shift)
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    todayOpen = iOpen(None, timeFrame, shift - 1)
    PP = (prevHigh + prevLow + (todayOpen * 2)) / 4
    R1 = (PP * 2) - prevLow
    R2 = PP + prevRange
    S1 = (PP * 2) - prevHigh
    S2 = PP - prevRange
    S3 = prevLow - (2 * (prevHigh - PP))
    S4 = S3 - prevRange
    R3 = prevHigh + (2 * (PP - prevLow))
    R4 = R3 + prevRange
    ppArrayRef[0] = PP
    ppArrayRef[1] = S1
    ppArrayRef[2] = S2
    ppArrayRef[3] = R1
    ppArrayRef[4] = R2
    ppArrayRef[5] = S3
    ppArrayRef[6] = S4
    ppArrayRef[7] = R3
    ppArrayRef[8] = R4

def fibonacciPivotPoint(ppArrayRef):
    shift = 1
    if timeFrame == PERIOD_D1:
        dayCheck1 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck1) == 0:
            shift += 1
        dayCheck2 = iTime(None, PERIOD_D1, shift)
        if TimeDayOfWeekMQL4(dayCheck2) == 6:
            shift += 1
    prevRange = iHigh(None, timeFrame, shift) - iLow(None, timeFrame, shift)
    prevHigh = iHigh(None, timeFrame, shift)
    prevLow = iLow(None, timeFrame, shift)
    prevClose = iClose(None, timeFrame, shift)
    Pivot = (prevHigh + prevLow + prevClose) / 3
    R38 = Pivot + (prevRange * 0.382)
    R61 = Pivot + (prevRange * 0.618)
    R78 = Pivot + (prevRange * 0.786)
    R100 = Pivot + (prevRange * 1.0)
    R138 = Pivot + (prevRange * 1.382)
    R161 = Pivot + (prevRange * 1.618)
    R200 = Pivot + (prevRange * 2.0)
    S38 = Pivot - (prevRange * 0.382)
    S61 = Pivot - (prevRange * 0.618)
    S78 = Pivot - (prevRange * 0.786)
    S100 = Pivot - (prevRange * 1.0)
    S138 = Pivot - (prevRange * 1.382)
    S161 = Pivot - (prevRange * 1.618)
    S200 = Pivot - (prevRange * 2.0)
    ppArrayRef[0] = Pivot
    ppArrayRef[1] = R38
    ppArrayRef[2] = R61
    ppArrayRef[3] = R78
    ppArrayRef[4] = R100
    ppArrayRef[5] = R138
    ppArrayRef[6] = R161
    ppArrayRef[7] = R200
    ppArrayRef[8] = S38
    ppArrayRef[9] = S61
    ppArrayRef[10] = S78
    ppArrayRef[11] = S100
    ppArrayRef[12] = S138
    ppArrayRef[13] = S161
    ppArrayRef[14] = S200

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
    elif _sw2 == 310:
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

def TimeDayOfWeekMQL4(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day_of_week

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

# ---- global variables initialised from expressions
indiName = 'PPL' + ' ' + EnumToString(pivotSelection, 'pivotTypes') + ' ' + EnumToString(timeFrame, 'ENUM_TIMEFRAMES')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PivotPointsLinesV11(_MQL5Indicator):
    name = 'PivotPointsLines_v1.1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'pivotSelection': _Choice({0: 'Standard(Floor) Pivot Formula', 1: 'Fibonacci Pivot Formula', 2: 'Camarilla Pivot Formula', 3: 'Woodie Pivot Formula'}, default=0),  # Pivot Point Formula
        'drawFloorMidPP': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Draw Floor Mid Pivot Points?
        'showPriceLabel': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Show Price In Label?
        'timeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # TimeFrame
        'useShortLines': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Draw Short Lines
        'Line_Length': 15,  # Length of Short Line
        'lineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Line Style
        'lineWidth': 1,  # Line Width
        'labelFontSize': 8,  # Label Font Size
        'ShiftLabel': 10,  # Label Shift +move right -move left
        'useSameColorLabelChoice': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Label use Same Color?
    }

