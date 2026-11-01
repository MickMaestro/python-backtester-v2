"""SingleBarValues — converted from MQL5: MQL5 Indicators/Utility to view the statistics for a Single Bar of any time frame/SingleBarValues.mq5

Display Single Bar Values.
Copyright: LukeB; Link: https://www.mql5.com/en/users/lukeb; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'LukeB', 'link': 'https://www.mql5.com/en/users/lukeb', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Display Single Bar Values.'], 'name': 'SingleBarValues', 'source': 'MQL5 Indicators/Utility to view the statistics for a Single Bar of any time frame/SingleBarValues.mq5', 'folder': 'Utility to view the statistics for a Single Bar of any time frame', 'inputs': [{'mql': 'Uniquifier', 'py': 'Uniquifier', 'param': 'Uniquifier', 'type': 'int', 'default': 3, 'label': 'Display Offset and Unique Instance Number', 'sinput': False}, {'mql': 'DirectClick', 'py': 'DirectClick', 'param': 'DirectClick', 'type': 'int', 'default': 1, 'label': 'select bars with a mouse click', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ANCHOR_POINTS
ANCHOR_POINT_ZERO = 0
ANCHOR_POINT_ONE = 1
_enum('ANCHOR_POINTS', {0: 'ANCHOR_POINT_ZERO', 1: 'ANCHOR_POINT_ONE'})

# enum BAR_INFO_MECH
COPY_FUNCS = 0
RATES = 1
DIRECT = 2
_enum('BAR_INFO_MECH', {0: 'COPY_FUNCS', 1: 'RATES', 2: 'DIRECT'})

# enum PERIOD_PARTS
PART_ONE = 0
PART_TWO = 1
_enum('PERIOD_PARTS', {0: 'PART_ONE', 1: 'PART_TWO'})

# enum ENUM_ON_OFF
OFF = 0
ON = 1
_enum('ENUM_ON_OFF', {0: 'OFF', 1: 'ON'})

# enum ENUM_CTRL_IDX
BAR_UP = 0
BAR_DN = 1
PERIOD_START = 2
PERIOD_END = 3
INFO_MECH = 4
endObjIdx = 5
_enum('ENUM_CTRL_IDX', {0: 'BAR_UP', 1: 'BAR_DN', 2: 'PERIOD_START', 3: 'PERIOD_END', 4: 'INFO_MECH', 5: 'endObjIdx'})

# enum INF_DISP_IDX
INFO_HDR = 0
INFO_OPEN = 1
INFO_HIGH = 2
INFO_LOW = 3
INFO_CLOSE = 4
INFO_TIME = 5
endInfoIdx = 6
_enum('INF_DISP_IDX', {0: 'INFO_HDR', 1: 'INFO_OPEN', 2: 'INFO_HIGH', 3: 'INFO_LOW', 4: 'INFO_CLOSE', 5: 'INFO_TIME', 6: 'endInfoIdx'})

# ---- inputs and global variables
shortName = 'SingleBarValues'
CHARTEVENT_MAKECHART = 37
WINDOW_ZERO = 0
CHARTWINDOW = 0
NOSHIFT = 0
COPYONEELEMENT = 1
workingTF = 0
workingMaMethod = 0
workingMechanism = 0
Uniquifier = _input('Uniquifier', 3)  # Display Offset and Unique Instance Number
DirectClick = _input('DirectClick', ON)  # select bars with a mouse click
ctrlObjName = Arr.of(['BAR_UP', 'BAR_DN', 'PERIOD_START', 'PERIOD_END', 'INFO_MECH'], fill="")
objXPos = Arr.of([10, 60, 170, 220, 270], fill=0)
objYPos = Arr.of([0, 0, 0, 0, 0], fill=0)
objClr = Arr.of([clrLimeGreen, clrLimeGreen, clrLimeGreen, clrLimeGreen, clrLimeGreen, clrLimeGreen], fill=0)
infObjName = Arr.of(['INFO_HDR', 'INFO_OPEN', 'INFO_HIGH', 'INFO_LOW', 'INFO_CLOSE', 'INFO_TIME'], fill="")
infXPos = Arr.of([10, 10, 10, 10, 10, 10], fill=0)
infYPos = Arr.of([0, 0, 0, 0, 0, 0], fill=0)
infClr = Arr.of([clrYellowGreen, clrYellowGreen, clrYellowGreen, clrYellowGreen, clrYellowGreen, clrYellowGreen], fill=0)

class BoxStruct(MqlObject):
    _q_fields = ('editBoxName', 'displayValue', 'xPos', 'yPos')
    def __init__(self, *args):
        self.editBoxName = ""
        self.displayValue = 0
        self.xPos = 0
        self.yPos = 0

class RectStruct(MqlObject):
    _q_fields = ('rectName', 'lineStyle', 'lineWidth', 'fillClr', 'topPrice', 'bottomPrice', 'startTime', 'endTime')
    def __init__(self, *args):
        self.rectName = ""
        self.lineStyle = 0
        self.lineWidth = 0
        self.fillClr = 0
        self.topPrice = 0.0
        self.bottomPrice = 0.0
        self.startTime = 0
        self.endTime = 0

def OnInit():
    global shortName, workingMaMethod, workingMechanism, workingTF
    succeeded = INIT_SUCCEEDED
    shortName += IntegerToString(Uniquifier)
    IndicatorSetString(INDICATOR_SHORTNAME, shortName)
    workingTF = getPeriodCurrent()
    workingMaMethod = MODE_SMA
    workingMechanism = RATES
    for i in range(0, endObjIdx):
        objYPos[i] = 10 * Uniquifier
        ctrlObjName[i] += IntegerToString(Uniquifier)
    for i in range(0, endInfoIdx):
        infYPos[i] = (16 * Uniquifier) + (i * 18)
        infObjName[i] += IntegerToString(Uniquifier)
    barNumBox.editBoxName += IntegerToString(Uniquifier)
    barRectangle.rectName += IntegerToString(Uniquifier)
    runDisplay()
    return succeeded

def OnDeinit(reason):
    chartID = ChartID()
    for i in range(0, endObjIdx):
        ObjectDelete(chartID, ctrlObjName[i])
    for i in range(0, endInfoIdx):
        ObjectDelete(chartID, infObjName[i])
    ObjectDelete(chartID, barNumBox.editBoxName)
    ObjectDelete(chartID, barRectangle.rectName)

def OnChartEvent(id_, lparam, dparam, sparam):
    global workingMechanism, workingTF
    display = False
    if id_ == CHARTEVENT_OBJECT_ENDEDIT and sparam == barNumBox.editBoxName:
        boxValue = _int(StringToInteger(ObjectGetString(WINDOW_ZERO, barNumBox.editBoxName, OBJPROP_TEXT, 0)))
        bars = iBars(Symbol(), workingTF)
        if not (boxValue > -1 and boxValue < bars):
            barNumBox.displayValue = 1
        else:
            barNumBox.displayValue = boxValue
        display = True
    elif id_ == CHARTEVENT_OBJECT_CLICK:
        if sparam == ctrlObjName[BAR_UP]:
            bars = iBars(Symbol(), workingTF)
            if (barNumBox.displayValue + 1) < bars:
                barNumBox.displayValue += 1
            else:
                barNumBox.displayValue = 0
            display = True
        if sparam == ctrlObjName[BAR_DN]:
            bars = iBars(Symbol(), workingTF)
            if (barNumBox.displayValue - 1) >= 0:
                barNumBox.displayValue -= 1
            else:
                barNumBox.displayValue = bars - 1
            display = True
        if sparam == ctrlObjName[PERIOD_START]:
            set_ = False
            while not set_:
                workingTF = getNextTF(workingTF)
                bars = iBars(Symbol(), workingTF)
                if barNumBox.displayValue < bars:
                    set_ = True
            display = True
        if sparam == ctrlObjName[PERIOD_END]:
            set_ = False
            while not set_:
                workingTF = getPreviousTF(workingTF)
                bars = iBars(Symbol(), workingTF)
                if barNumBox.displayValue < bars:
                    set_ = True
            display = True
        if sparam == ctrlObjName[INFO_MECH]:
            workingMechanism = getNextMec(workingMechanism)
            display = True
    elif id_ == CHARTEVENT_CLICK and DirectClick == ON:
        chartClickTime = Box(0)
        chartClickPrice = Box(0.0)
        windowNumber = Box(0)
        if ChartXYToTimePrice(ChartID(), _int(lparam), _int(dparam), windowNumber, chartClickTime, chartClickPrice):
            barNum = iBarShift(Symbol(), workingTF, chartClickTime.v, False)
            if barNum > -1:
                barNumBox.displayValue = barNum
                display = True
            else:
                errCode = GetLastError()
                Print('OnChartEvent', ' at ', TimeToString(chartClickTime.v, TIME_DATE | TIME_MINUTES), ' iBarShift generated error: ', IntegerToString(errCode))
        else:
            errCode = GetLastError()
            Print('OnChartEvent', ' ChartXYToTimePrice generated error: ', IntegerToString(errCode))
    elif id_ == (CHARTEVENT_CUSTOM + CHARTEVENT_MAKECHART):
        if lparam == Uniquifier:
            runDisplay()
    if display == True:
        EventChartCustom(ChartID(), CHARTEVENT_MAKECHART, Uniquifier, None, None)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (rates_total - prev_calculated) > 0:
        EventChartCustom(ChartID(), CHARTEVENT_MAKECHART, Uniquifier, None, None)
    elif barNumBox.displayValue < 1:
        EventChartCustom(ChartID(), CHARTEVENT_MAKECHART, Uniquifier, None, None)
    return rates_total

def displayControls():
    displayABox(barNumBox)
    for i in range(0, endObjIdx):
        dispText = getPromptTxt(i)
        manageALabel(ctrlObjName[i], dispText, objXPos[i], objYPos[i], objClr[i], 10)

def runDisplay():
    global _s_runDisplay_barClose, _s_runDisplay_barHigh, _s_runDisplay_barLow, _s_runDisplay_barOpen, _s_runDisplay_callCount
    _s_runDisplay_callCount += 1
    barNum = barNumBox.displayValue
    catlen = 0
    barStr = IntegerToString(barNum)
    theTime = 0
    barTime = Arr(1, 0, dyn=False)
    hdrString = Box("")
    closeString = Box("")
    openString = Box("")
    highString = Box("")
    lowString = Box("")
    timeString = Box("")
    displayControls()
    ResetLastError()
    _sw1 = workingMechanism
    if _sw1 == COPY_FUNCS:
        if CopyClose(Symbol(), workingTF, barNum, COPYONEELEMENT, _s_runDisplay_price) > -1:
            _s_runDisplay_barClose = _s_runDisplay_price[0]
        else:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('CopyClose', barNum, workingTF, errCode, _s_runDisplay_callCount)
        if CopyHigh(Symbol(), workingTF, barNum, COPYONEELEMENT, _s_runDisplay_price) > -1:
            _s_runDisplay_barHigh = _s_runDisplay_price[0]
        else:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('CopyHigh', barNum, workingTF, errCode, _s_runDisplay_callCount)
        if CopyLow(Symbol(), workingTF, barNum, COPYONEELEMENT, _s_runDisplay_price) > -1:
            _s_runDisplay_barLow = _s_runDisplay_price[0]
        else:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('CopyLow', barNum, workingTF, errCode, _s_runDisplay_callCount)
        if CopyOpen(Symbol(), workingTF, barNum, COPYONEELEMENT, _s_runDisplay_price) > -1:
            _s_runDisplay_barOpen = _s_runDisplay_price[0]
        else:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('CopyOpen', barNum, workingTF, errCode, _s_runDisplay_callCount)
        if CopyTime(Symbol(), workingTF, barNum, COPYONEELEMENT, barTime) > -1:
            theTime = barTime[0]
        else:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('CopyTime', barNum, workingTF, errCode, _s_runDisplay_callCount)
        catlen = StringConcatenate(hdrString, 'Bar: ', IntegerToString(barNum), '; Range: ', DoubleToString(_s_runDisplay_barHigh - _s_runDisplay_barLow, Digits()))
        catlen = StringConcatenate(closeString, 'CopyClose = ', DoubleToString(_s_runDisplay_barClose, Digits()))
        catlen = StringConcatenate(openString, 'CopyOpen = ', DoubleToString(_s_runDisplay_barOpen, Digits()))
        catlen = StringConcatenate(highString, 'CopyHigh = ', DoubleToString(_s_runDisplay_barHigh, Digits()))
        catlen = StringConcatenate(lowString, 'CopyLow = ', DoubleToString(_s_runDisplay_barLow, Digits()))
        catlen = StringConcatenate(timeString, 'CopyTime = ', TimeToString(theTime, TIME_DATE | TIME_MINUTES))
    elif _sw1 == DIRECT:
        _s_runDisplay_barClose = iClose(Symbol(), workingTF, barNum)
        if _s_runDisplay_barClose == 0:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('iClose', barNum, workingTF, errCode, _s_runDisplay_callCount)
        _s_runDisplay_barHigh = iHigh(Symbol(), workingTF, barNum)
        if _s_runDisplay_barHigh == 0:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('iHigh', barNum, workingTF, errCode, _s_runDisplay_callCount)
        _s_runDisplay_barLow = iLow(Symbol(), workingTF, barNum)
        if _s_runDisplay_barLow == 0:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('iLow', barNum, workingTF, errCode, _s_runDisplay_callCount)
        _s_runDisplay_barOpen = iOpen(Symbol(), workingTF, barNum)
        if _s_runDisplay_barOpen == 0:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('iOpen', barNum, workingTF, errCode, _s_runDisplay_callCount)
        theTime = iTime(Symbol(), workingTF, barNum)
        if theTime == 0:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('iTime', barNum, workingTF, errCode, _s_runDisplay_callCount)
        catlen = StringConcatenate(hdrString, 'Bar: ', IntegerToString(barNum), '; Range: ', DoubleToString(_s_runDisplay_barHigh - _s_runDisplay_barLow, Digits()))
        catlen = StringConcatenate(closeString, 'iClose = ', DoubleToString(_s_runDisplay_barClose, Digits()))
        catlen = StringConcatenate(openString, 'iOpen = ', DoubleToString(_s_runDisplay_barOpen, Digits()))
        catlen = StringConcatenate(highString, 'iHigh = ', DoubleToString(_s_runDisplay_barHigh, Digits()))
        catlen = StringConcatenate(lowString, 'iLow = ', DoubleToString(_s_runDisplay_barLow, Digits()))
        catlen = StringConcatenate(timeString, 'iTime = ', TimeToString(theTime, TIME_DATE | TIME_MINUTES))
    else:
        if CopyRates(Symbol(), workingTF, barNum, COPYONEELEMENT, _s_runDisplay_rates) < 0:
            errCode = GetLastError()
            ResetLastError()
            PostTerminalError('CopyRates', barNum, workingTF, errCode, _s_runDisplay_callCount)
        _s_runDisplay_barClose = _s_runDisplay_rates[0].close
        _s_runDisplay_barHigh = _s_runDisplay_rates[0].high
        _s_runDisplay_barLow = _s_runDisplay_rates[0].low
        _s_runDisplay_barOpen = _s_runDisplay_rates[0].open
        theTime = _s_runDisplay_rates[0].time
        catlen = StringConcatenate(hdrString, 'Bar: ', IntegerToString(barNum), '; Range: ', DoubleToString(_s_runDisplay_barHigh - _s_runDisplay_barLow, Digits()))
        catlen = StringConcatenate(closeString, 'rates[].close = ', DoubleToString(_s_runDisplay_barClose, Digits()))
        catlen = StringConcatenate(openString, 'rates[].open  = ', DoubleToString(_s_runDisplay_barOpen, Digits()))
        catlen = StringConcatenate(highString, 'rates[].high  = ', DoubleToString(_s_runDisplay_barHigh, Digits()))
        catlen = StringConcatenate(lowString, 'rates[].low   = ', DoubleToString(_s_runDisplay_barLow, Digits()))
        catlen = StringConcatenate(timeString, 'rates[].time  = ', TimeToString(theTime, TIME_DATE | TIME_MINUTES))
    manageALabel(infObjName[INFO_HDR], hdrString.v, infXPos[INFO_HDR], infYPos[INFO_HDR], infClr[INFO_HDR], 11)
    manageALabel(infObjName[INFO_CLOSE], closeString.v, infXPos[INFO_CLOSE], infYPos[INFO_CLOSE], infClr[INFO_CLOSE], 11)
    manageALabel(infObjName[INFO_OPEN], openString.v, infXPos[INFO_OPEN], infYPos[INFO_OPEN], infClr[INFO_OPEN], 11)
    manageALabel(infObjName[INFO_HIGH], highString.v, infXPos[INFO_HIGH], infYPos[INFO_HIGH], infClr[INFO_HIGH], 11)
    manageALabel(infObjName[INFO_LOW], lowString.v, infXPos[INFO_LOW], infYPos[INFO_LOW], infClr[INFO_LOW], 11)
    manageALabel(infObjName[INFO_TIME], timeString.v, infXPos[INFO_TIME], infYPos[INFO_TIME], infClr[INFO_TIME], 11)
    barRectangle.topPrice = _s_runDisplay_barHigh
    barRectangle.bottomPrice = _s_runDisplay_barLow
    barRectangle.startTime = theTime
    if CopyTime(Symbol(), Period(), NOSHIFT, COPYONEELEMENT, barTime) > -1:
        if barTime[0] < (theTime + PeriodSeconds(workingTF)):
            barRectangle.endTime = barTime[0] + PeriodSeconds(PERIOD_CURRENT)
        else:
            barRectangle.endTime = theTime + PeriodSeconds(workingTF)
    else:
        errCode = GetLastError()
        ResetLastError()
        zeroBar = 0
        PostTerminalError('CopyTime', zeroBar, workingTF, errCode, _s_runDisplay_callCount)
        barRectangle.endTime = TimeCurrent()
    makeARectangle(barRectangle)

def PostTerminalError(operation, barNum, tf, errCode, callCount):
    Print('Call: ', IntegerToString(callCount), ' for ', operation, ' for bar: ', IntegerToString(barNum), ' of Time Frame: ', getPeriodText(tf, PART_TWO), ' posted error: ' + IntegerToString(errCode))

def displayABox(displayBox):
    global _s_displayABox_chartID
    if _s_displayABox_chartID is _UNSET:
        _s_displayABox_chartID = ChartID()
    objName = displayBox.editBoxName
    displayStr = IntegerToString(displayBox.displayValue)
    dispWindow = ObjectFind(_s_displayABox_chartID, objName)
    if dispWindow < 0:
        ObjectCreate(_s_displayABox_chartID, objName, OBJ_EDIT, WINDOW_ZERO, 0, 0)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_FONTSIZE, 10)
        ObjectSetString(_s_displayABox_chartID, objName, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_COLOR, clrCornflowerBlue)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_BORDER_COLOR, clrBlack)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_BGCOLOR, clrLightGray)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_XSIZE, 50)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_YSIZE, 20)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_ALIGN, ALIGN_CENTER)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_READONLY, False)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_BACK, False)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_SELECTED, False)
        ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_HIDDEN, True)
    ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_XDISTANCE, displayBox.xPos)
    ObjectSetInteger(_s_displayABox_chartID, objName, OBJPROP_YDISTANCE, displayBox.yPos)
    ObjectSetString(_s_displayABox_chartID, objName, OBJPROP_TEXT, displayStr)

def manageALabel(objName, dispStr, xPos, yPos, dispClr, fontSize=12):
    global _s_manageALabel_chartID
    if _s_manageALabel_chartID is _UNSET:
        _s_manageALabel_chartID = ChartID()
    if ObjectFind(_s_manageALabel_chartID, objName) < 0:
        ObjectCreate(_s_manageALabel_chartID, objName, OBJ_LABEL, WINDOW_ZERO, 0, 0)
        ObjectSetInteger(_s_manageALabel_chartID, objName, OBJPROP_FONTSIZE, fontSize)
        ObjectSetString(_s_manageALabel_chartID, objName, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(_s_manageALabel_chartID, objName, OBJPROP_COLOR, dispClr)
        ObjectSetInteger(_s_manageALabel_chartID, objName, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(_s_manageALabel_chartID, objName, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
        ObjectSetInteger(_s_manageALabel_chartID, objName, OBJPROP_BACK, True)
        ObjectSetInteger(_s_manageALabel_chartID, objName, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(_s_manageALabel_chartID, objName, OBJPROP_SELECTED, False)
        ObjectSetInteger(_s_manageALabel_chartID, objName, OBJPROP_HIDDEN, True)
    ObjectSetInteger(_s_manageALabel_chartID, objName, OBJPROP_XDISTANCE, xPos)
    ObjectSetInteger(_s_manageALabel_chartID, objName, OBJPROP_YDISTANCE, yPos)
    ObjectSetString(_s_manageALabel_chartID, objName, OBJPROP_TEXT, dispStr)

def makeARectangle(displayRect):
    global _s_makeARectangle_chartID
    if _s_makeARectangle_chartID is _UNSET:
        _s_makeARectangle_chartID = ChartID()
    windowIndex = ObjectFind(_s_makeARectangle_chartID, displayRect.rectName)
    if windowIndex < 0:
        if ObjectCreate(_s_makeARectangle_chartID, displayRect.rectName, OBJ_RECTANGLE, CHARTWINDOW, displayRect.startTime, displayRect.topPrice, displayRect.endTime, displayRect.bottomPrice):
            ObjectSetInteger(_s_makeARectangle_chartID, displayRect.rectName, OBJPROP_COLOR, displayRect.fillClr)
            ObjectSetInteger(_s_makeARectangle_chartID, displayRect.rectName, OBJPROP_STYLE, displayRect.lineStyle)
            ObjectSetInteger(_s_makeARectangle_chartID, displayRect.rectName, OBJPROP_WIDTH, displayRect.lineWidth)
            ObjectSetInteger(_s_makeARectangle_chartID, displayRect.rectName, OBJPROP_BACK, True)
            ObjectSetInteger(_s_makeARectangle_chartID, displayRect.rectName, OBJPROP_SELECTABLE, False)
            ObjectSetInteger(_s_makeARectangle_chartID, displayRect.rectName, OBJPROP_SELECTED, False)
            ObjectSetInteger(_s_makeARectangle_chartID, displayRect.rectName, OBJPROP_HIDDEN, True)
        else:
            errCode = GetLastError()
            errString = Box("")
            catLen = StringConcatenate(errString, 'makeARectangle', ' Failed to create object ', displayRect.rectName, ', Error: ', IntegerToString(errCode))
            Print(errString.v)
            Comment(errString.v)
    else:
        ObjectMove(_s_makeARectangle_chartID, displayRect.rectName, ANCHOR_POINT_ZERO, displayRect.startTime, displayRect.topPrice)
        ObjectMove(_s_makeARectangle_chartID, displayRect.rectName, ANCHOR_POINT_ONE, displayRect.endTime, displayRect.bottomPrice)

def getInfoMecDescription(mechanism):
    dispString = ""
    _sw2 = mechanism
    if _sw2 == COPY_FUNCS:
        dispString = 'COPY_FUNCS'
    elif _sw2 == RATES:
        dispString = 'RATES'
    elif _sw2 == DIRECT:
        dispString = 'DIRECT'
    else:
        dispString = 'Unknown ' + IntegerToString(mechanism)
    return dispString

def getNextMec(mechanism):
    nextMech = 0
    _sw3 = mechanism
    if _sw3 == RATES:
        nextMech = COPY_FUNCS
    elif _sw3 == COPY_FUNCS:
        nextMech = DIRECT
    elif _sw3 == DIRECT:
        nextMech = RATES
    else:
        nextMech = RATES
    return nextMech

def getPromptTxt(idx):
    dispString = ""
    _sw4 = idx
    if _sw4 == BAR_UP:
        dispString = 'Bar Up'
    elif _sw4 == BAR_DN:
        dispString = 'Bar Dn'
    elif _sw4 == PERIOD_START:
        dispString = getPeriodText(workingTF, PART_ONE)
    elif _sw4 == PERIOD_END:
        dispString = getPeriodText(workingTF, PART_TWO)
    elif _sw4 == INFO_MECH:
        dispString = getInfoMecDescription(workingMechanism)
    else:
        dispString = 'Unknown ' + IntegerToString(idx)
    return dispString

def getPeriodText(tf, partOneTwo):
    returnString = ""
    _sw5 = tf
    if _sw5 == PERIOD_M1:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M1')
    elif _sw5 == PERIOD_M2:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M2')
    elif _sw5 == PERIOD_M3:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M3')
    elif _sw5 == PERIOD_M4:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M4')
    elif _sw5 == PERIOD_M5:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M5')
    elif _sw5 == PERIOD_M6:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M6')
    elif _sw5 == PERIOD_M10:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M10')
    elif _sw5 == PERIOD_M12:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M12')
    elif _sw5 == PERIOD_M15:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M15')
    elif _sw5 == PERIOD_M20:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M20')
    elif _sw5 == PERIOD_M30:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_M30')
    elif _sw5 == PERIOD_H1:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_H1')
    elif _sw5 == PERIOD_H2:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_H2')
    elif _sw5 == PERIOD_H3:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_H3')
    elif _sw5 == PERIOD_H4:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_H4')
    elif _sw5 == PERIOD_H6:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_H6')
    elif _sw5 == PERIOD_H8:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_H8')
    elif _sw5 == PERIOD_H12:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_H12')
    elif _sw5 == PERIOD_D1:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_D1')
    elif _sw5 == PERIOD_W1:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_W1')
    elif _sw5 == PERIOD_MN1:
        returnString = ('PERIOD' if (partOneTwo == PART_ONE) else '_MN1')
    else:
        returnString = 'Unknown: ' + IntegerToString(tf)
    return returnString

def getNextTF(tf):
    returnTF = 0
    _sw6 = tf
    if _sw6 == PERIOD_M1:
        returnTF = PERIOD_M2
    elif _sw6 == PERIOD_M2:
        returnTF = PERIOD_M3
    elif _sw6 == PERIOD_M3:
        returnTF = PERIOD_M4
    elif _sw6 == PERIOD_M4:
        returnTF = PERIOD_M5
    elif _sw6 == PERIOD_M5:
        returnTF = PERIOD_M6
    elif _sw6 == PERIOD_M6:
        returnTF = PERIOD_M10
    elif _sw6 == PERIOD_M10:
        returnTF = PERIOD_M12
    elif _sw6 == PERIOD_M12:
        returnTF = PERIOD_M15
    elif _sw6 == PERIOD_M15:
        returnTF = PERIOD_M20
    elif _sw6 == PERIOD_M20:
        returnTF = PERIOD_M30
    elif _sw6 == PERIOD_M30:
        returnTF = PERIOD_H1
    elif _sw6 == PERIOD_H1:
        returnTF = PERIOD_H2
    elif _sw6 == PERIOD_H2:
        returnTF = PERIOD_H3
    elif _sw6 == PERIOD_H3:
        returnTF = PERIOD_H4
    elif _sw6 == PERIOD_H4:
        returnTF = PERIOD_H6
    elif _sw6 == PERIOD_H6:
        returnTF = PERIOD_H8
    elif _sw6 == PERIOD_H8:
        returnTF = PERIOD_H12
    elif _sw6 == PERIOD_H12:
        returnTF = PERIOD_D1
    elif _sw6 == PERIOD_D1:
        returnTF = PERIOD_W1
    elif _sw6 == PERIOD_W1:
        returnTF = PERIOD_MN1
    elif _sw6 == PERIOD_MN1:
        returnTF = PERIOD_M1
    else:
        returnTF = PERIOD_CURRENT
    return returnTF

def getPreviousTF(tf):
    returnTF = 0
    _sw7 = tf
    if _sw7 == PERIOD_M1:
        returnTF = PERIOD_MN1
    elif _sw7 == PERIOD_M2:
        returnTF = PERIOD_M1
    elif _sw7 == PERIOD_M3:
        returnTF = PERIOD_M2
    elif _sw7 == PERIOD_M4:
        returnTF = PERIOD_M3
    elif _sw7 == PERIOD_M5:
        returnTF = PERIOD_M4
    elif _sw7 == PERIOD_M6:
        returnTF = PERIOD_M5
    elif _sw7 == PERIOD_M10:
        returnTF = PERIOD_M6
    elif _sw7 == PERIOD_M12:
        returnTF = PERIOD_M10
    elif _sw7 == PERIOD_M15:
        returnTF = PERIOD_M12
    elif _sw7 == PERIOD_M20:
        returnTF = PERIOD_M15
    elif _sw7 == PERIOD_M30:
        returnTF = PERIOD_M20
    elif _sw7 == PERIOD_H1:
        returnTF = PERIOD_M30
    elif _sw7 == PERIOD_H2:
        returnTF = PERIOD_H1
    elif _sw7 == PERIOD_H3:
        returnTF = PERIOD_H2
    elif _sw7 == PERIOD_H4:
        returnTF = PERIOD_H3
    elif _sw7 == PERIOD_H6:
        returnTF = PERIOD_H4
    elif _sw7 == PERIOD_H8:
        returnTF = PERIOD_H6
    elif _sw7 == PERIOD_H12:
        returnTF = PERIOD_H8
    elif _sw7 == PERIOD_D1:
        returnTF = PERIOD_H12
    elif _sw7 == PERIOD_W1:
        returnTF = PERIOD_D1
    elif _sw7 == PERIOD_MN1:
        returnTF = PERIOD_W1
    else:
        returnTF = getPeriodCurrent()
    return returnTF

def getPeriodCurrent():
    returnTF = Period()
    return returnTF

# ---- global variables initialised from expressions
barNumBox = _struct_init(BoxStruct(), ['BarNumBox', 1, 110, 30])
barRectangle = _struct_init(RectStruct(), ['BarRectangle', STYLE_DASHDOT, 1, clrOldLace, 0, 0, 0, 0])

# ---- static local variables
_s_runDisplay_callCount = 0
_s_runDisplay_barClose = 0.0
_s_runDisplay_barHigh = 0.0
_s_runDisplay_barLow = 0.0
_s_runDisplay_barOpen = 0.0
_s_runDisplay_price = Arr(1, 0.0, dyn=False)
_s_runDisplay_rates = Arr(1, 0, dyn=False, factory=MqlRates)
_s_displayABox_chartID = _UNSET
_s_manageALabel_chartID = _UNSET
_s_makeARectangle_chartID = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SingleBarValues(_MQL5Indicator):
    name = 'SingleBarValues'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Uniquifier': 3,  # Display Offset and Unique Instance Number
        'DirectClick': _Choice({0: 'OFF', 1: 'ON'}, default=1),  # select bars with a mouse click
    }

