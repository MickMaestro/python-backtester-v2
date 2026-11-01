"""SeriesIntegerInfo_and_MqlRates_TF_Status — converted from MQL5: MQL5 Indicators/SeriesIntegerInfo and Rates Bar Information Utility, displays how many bars there are in all timefra/SeriesIntegerInfo_and_MqlRates_TF_Status.mq5

View TF Bar Count retreives with SeriesIntegerInfo and Mqlrates (CopyRates) data availablity
for all the TimeFrames of a Market Symbol
Copyright: LukeB; Link: https://www.mql5.com/en/users/lukeb; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'LukeB', 'link': 'https://www.mql5.com/en/users/lukeb', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['View TF Bar Count retreives with SeriesIntegerInfo and Mqlrates (CopyRates) data availablity', 'for all the TimeFrames of a Market Symbol'], 'name': 'SeriesIntegerInfo_and_MqlRates_TF_Status', 'source': 'MQL5 Indicators/SeriesIntegerInfo and Rates Bar Information Utility, displays how many bars there are in all timefra/SeriesIntegerInfo_and_MqlRates_TF_Status.mq5', 'folder': 'SeriesIntegerInfo and Rates Bar Information Utility, displays how many bars there are in all timefra', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_YES_NO
YES = 0
NO = 1
_enum('ENUM_YES_NO', {0: 'YES', 1: 'NO'})

# enum ENUM_ON_OFF
ON = 0
OFF = 1
_enum('ENUM_ON_OFF', {0: 'ON', 1: 'OFF'})

# enum ENUM_DISP_OBJ_IDX
INFO_HDR_IDX = 0
BAR_ENTRY_IDX = 1
SYMB_HDR_IDX = 2
SYMB_ENTRY_IDX = 3
SERIES_INFO_IDX = 4
RATES_INFO_IDX = 5
END_DIP_OBJ_IDX = 6
_enum('ENUM_DISP_OBJ_IDX', {0: 'INFO_HDR_IDX', 1: 'BAR_ENTRY_IDX', 2: 'SYMB_HDR_IDX', 3: 'SYMB_ENTRY_IDX', 4: 'SERIES_INFO_IDX', 5: 'RATES_INFO_IDX', 6: 'END_DIP_OBJ_IDX'})

# ---- inputs and global variables
shortName = 'MQLRatesAndSeriesIntegerInfo'
uniquifier = 37503  # a number to identify custom events from this indicator and make objects unique
CHARTEVENT_RUNINDI = 37500
COPYONEELEMENT = 1
WINDOW_ZERO = 0
NOMODIFIER = 0
outputLogs = 0
TFPeriods = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
useSuggetedBar = NO
suggestedBar = 0
panelDisplay = ON
statisticsSymbol = ""
disp_obj_type = Arr.of([OBJ_LABEL, OBJ_EDIT, OBJ_LABEL, OBJ_EDIT, OBJ_LABEL, OBJ_LABEL], fill=0)
disp_obj_name = Arr.of(['INFO_HDR', 'BAR_ENTRY', 'SYMB_HDR', 'SYMB_ENTRY', 'SERIES_INFO', 'RATES_INFO'], fill="")
disp_obj_txt = Arr.of(['Bar/Rates OF', 'BAR:', 'Symbol:', '', 'SERIES', 'RATES'], fill="")
disp_obj_clr = Arr.of([clrLime, clrDarkBlue, clrLime, clrDarkBlue, clrLime, clrLime], fill=0)
disp_obj_size = Arr.of([12, 10, 12, 9, 10, 10], fill=0)
disp_X_pos = Arr.of([10, 0, 0, 0, 0, 0], fill=0)
disp_Y_pos = Arr.of([20, 0, 0, 0, 0, 0], fill=0)
msg = ""

class tfRatesSruct(MqlObject):
    _q_fields = ('disp', 'barNum', 'errCode', 'mqlRates')
    def __init__(self, *args):
        self.disp = ""
        self.barNum = 0
        self.errCode = 0
        self.mqlRates = Arr(1, 0, dyn=False, factory=MqlRates)

class SeriesInfoStruc(MqlObject):
    _q_fields = ('m_barsCount', 'm_firstBarDate', 'm_firstBarNum', 'm_isSyncronized', 'm_barErrCode', 'm_barDateErrCode', 'm_syncErrCode')
    def __init__(self, *args):
        self.m_barsCount = 0
        self.m_firstBarDate = 0
        self.m_firstBarNum = 0
        self.m_isSyncronized = False
        self.m_barErrCode = 0
        self.m_barDateErrCode = 0
        self.m_syncErrCode = 0
    def SeriesInfoStruc(self):
        self.setInitialValues()
    def setInitialValues(self):
        self.m_barErrCode = 0
        self.m_barDateErrCode = 0
        self.m_syncErrCode = 0
        self.m_barsCount = INT_MIN
        self.m_firstBarDate = 0
        self.m_firstBarNum = INT_MIN
        self.m_isSyncronized = False
    def setBarTimeAndNum(self, firstBarTime, symbol, tf):
        self.m_firstBarDate = firstBarTime
        self.m_firstBarNum = iBarShift(symbol, tf, firstBarTime, False)
        if self.m_firstBarNum < 0:
            errCode = GetLastError()
            ResetLastError()
            Print('SeriesInfoStruc::setBarTimeAndNum', ', iBarShift for ', GetPeriodText(tf), ' produced error ' + IntegerToString(errCode))

def SetObjXYPositions():
    disp_X_pos[BAR_ENTRY_IDX] = disp_X_pos[INFO_HDR_IDX] + 110
    disp_Y_pos[BAR_ENTRY_IDX] = disp_Y_pos[INFO_HDR_IDX]
    disp_X_pos[SYMB_HDR_IDX] = disp_X_pos[INFO_HDR_IDX] + 180
    disp_Y_pos[SYMB_HDR_IDX] = disp_Y_pos[INFO_HDR_IDX]
    disp_X_pos[SYMB_ENTRY_IDX] = disp_X_pos[INFO_HDR_IDX] + 240
    disp_Y_pos[SYMB_ENTRY_IDX] = disp_Y_pos[INFO_HDR_IDX]

def OnInit():
    global msg, outputLogs, shortName, statisticsSymbol
    initCode = INIT_SUCCEEDED
    shortName += IntegerToString(uniquifier)
    IndicatorSetString(INDICATOR_SHORTNAME, shortName)
    SetObjXYPositions()
    for idx in range(0, ArrayRange(disp_obj_name, 0)):
        disp_obj_name[idx] = IntegerToString(uniquifier) + disp_obj_name[idx]
    if ArrayResize(struc_tfRates, ArrayRange(TFPeriods, 0)) != ArrayRange(TFPeriods, 0):
        errCode = GetLastError()
        ResetLastError()
        msg = 'OnInit' + ' Array Resize Faild for struc_tfRates[], error: ' + IntegerToString(errCode)
        Print(msg)
        initCode = INIT_FAILED
    elif ArrayResize(struc_seriesInfo, ArrayRange(TFPeriods, 0)) != ArrayRange(TFPeriods, 0):
        errCode = GetLastError()
        ResetLastError()
        msg = 'OnInit' + ' Array Resize Faild for struc_seriesInfo[], error: ' + IntegerToString(errCode)
        Print(msg)
        initCode = INIT_FAILED
    else:
        statisticsSymbol = Symbol()
        callerCount = 1
        outputLogs = ON
        RunTheIndicator('OnInit', callerCount, statisticsSymbol, TFPeriods, struc_tfRates, struc_seriesInfo, suggestedBar, useSuggetedBar)
    return initCode

def OnDeinit(reason):
    global msg
    if StringLen(msg) > 0:
        msg = ''
        Comment(msg)
    for i in range(ObjectsTotal(ChartID()) - 1, 0 - 1, -1):
        objName = ObjectName(ChartID(), i)
        objSubStr = StringSubstr(objName, 0, StringLen(IntegerToString(uniquifier)))
        if objSubStr == IntegerToString(uniquifier):
            ObjectDelete(ChartID(), objName)
    ChartRedraw(ChartID())

def OnChartEvent(id_, lparam, dparam, sparam):
    global _s_OnChartEvent_clickCount, _s_OnChartEvent_editCount, outputLogs, statisticsSymbol, suggestedBar, useSuggetedBar
    if id_ == (CHARTEVENT_CUSTOM + CHARTEVENT_RUNINDI):
        if lparam == uniquifier:
            callerCount = _int(dparam)
            RunTheIndicator(sparam, callerCount, statisticsSymbol, TFPeriods, struc_tfRates, struc_seriesInfo, suggestedBar, useSuggetedBar)
    elif id_ == CHARTEVENT_OBJECT_CLICK:
        _s_OnChartEvent_clickCount += 1
        if sparam == disp_obj_name[SYMB_HDR_IDX]:
            useSuggetedBar = (NO if (useSuggetedBar == YES) else YES)
            RunTheIndicator('OnChartEvent', _s_OnChartEvent_clickCount, statisticsSymbol, TFPeriods, struc_tfRates, struc_seriesInfo, suggestedBar, useSuggetedBar)
            ChartRedraw(ChartID())
        elif sparam == (IntegerToString(uniquifier) + 'ROW20|5'):
            outputLogs = (ON if (outputLogs == OFF) else OFF)
            DisplayThePanel(struc_tfRates, struc_seriesInfo, TFPeriods, statisticsSymbol)
            ChartRedraw(ChartID())
    elif id_ == CHARTEVENT_OBJECT_DRAG:
        if sparam == disp_obj_name[INFO_HDR_IDX]:
            disp_X_pos[INFO_HDR_IDX] = _uint(ObjectGetInteger(ChartID(), sparam, OBJPROP_XDISTANCE, NOMODIFIER))
            disp_Y_pos[INFO_HDR_IDX] = _uint(ObjectGetInteger(ChartID(), sparam, OBJPROP_YDISTANCE, NOMODIFIER))
            SetObjXYPositions()
            DisplayThePanel(struc_tfRates, struc_seriesInfo, TFPeriods, statisticsSymbol)
            ChartRedraw(ChartID())
    elif id_ == CHARTEVENT_OBJECT_ENDEDIT:
        _s_OnChartEvent_editCount += 1
        if sparam == disp_obj_name[BAR_ENTRY_IDX]:
            enteredBar = _int(StringToInteger(ObjectGetString(WINDOW_ZERO, disp_obj_name[BAR_ENTRY_IDX], OBJPROP_TEXT, 0)))
            if enteredBar < 0:
                enteredBar = 0
            maxBarNum = GetMaxBarCount(struc_seriesInfo)
            if enteredBar > _int(maxBarNum):
                enteredBar = _int(maxBarNum)
            suggestedBar = enteredBar
            useSuggetedBar = YES
            RunTheIndicator('OnChartEvent', _s_OnChartEvent_editCount, statisticsSymbol, TFPeriods, struc_tfRates, struc_seriesInfo, suggestedBar, useSuggetedBar)
            ChartRedraw(ChartID())
        elif sparam == disp_obj_name[SYMB_ENTRY_IDX]:
            enteredText = Box(ObjectGetString(WINDOW_ZERO, disp_obj_name[SYMB_ENTRY_IDX], OBJPROP_TEXT, 0))
            StringToUpper(enteredText)
            if GetMarketSymbol(enteredText):
                statisticsSymbol = enteredText.v
            RunTheIndicator('OnChartEvent', _s_OnChartEvent_editCount, statisticsSymbol, TFPeriods, struc_tfRates, struc_seriesInfo, suggestedBar, useSuggetedBar)
            ChartRedraw(ChartID())

def GetMarketSymbol(enteredText):
    global msg
    found = False
    msg = ''
    i = 0
    while i < SymbolsTotal(True):
        symbol = SymbolName(i, True)
        if StringSubstr(symbol, 0, StringLen(enteredText.v)) == enteredText.v:
            enteredText.v = symbol
            found = True
            break
        i += 1
    Print(msg)
    return found

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_callCount, outputLogs
    _s_OnCalculate_callCount += 1
    if prev_calculated < 1:
        outputLogs = OFF
    EventChartCustom(ChartID(), CHARTEVENT_RUNINDI, uniquifier, _s_OnCalculate_callCount, 'OnCalculate')
    return rates_total

def RunTheIndicator(caller, callerCount, statsSymbol, tfPeriods, tfRatesStruc_ary, seriesInfo_ary, requestedBar, useRequestedBar):
    SetSeriesInfoAryVals(caller, statsSymbol, tfPeriods, seriesInfo_ary, callerCount)
    SetRatesBarNum(tfRatesStruc_ary, seriesInfo_ary, suggestedBar, useSuggetedBar)
    SetCopyRatesAryVals(caller, statsSymbol, tfPeriods, struc_tfRates, callerCount)
    DisplayThePanel(tfRatesStruc_ary, seriesInfo_ary, tfPeriods, statsSymbol)

def SetSeriesInfoAryVals(caller, statSymbol, periods_ary, seriesInfo_ary, callerCount):
    global msg
    succeeded = True
    i = 0
    while i < ArrayRange(seriesInfo_ary, 0):
        if SetSeriesInfoForTf(caller, statSymbol, periods_ary[i], seriesInfo_ary[i], callerCount):
            if outputLogs == ON:
                msg = 'SetSeriesInfoAryVals' + ' Called by ' + caller + ' on callerCount ' + IntegerToString(callerCount) + ' "SeriesInfoInteger" succeeded for ' + Symbol() + ' in time frame ' + GetPeriodText(periods_ary[i]) + ' for symbol ' + statSymbol
                Print(msg)
        else:
            succeeded = False
        i += 1
    return succeeded

def SetSeriesInfoForTf(caller, statSymbol, tf, seriesInfoStruc, callerCount):
    global msg
    succeeded = True
    seriesLongInfo = Box(0)
    if SeriesInfoInteger(statSymbol, tf, SERIES_BARS_COUNT, seriesLongInfo) == False:
        seriesInfoStruc.m_barErrCode = GetLastError()
        ResetLastError()
        if outputLogs == ON:
            msg = 'SetSeriesInfoForTf' + ' Caller: ' + caller + ', caller count' + IntegerToString(callerCount) + ' "SeriesInfoInteger" call for bars of Time Frame: ' + GetPeriodText(tf) + ' posted error: ' + IntegerToString(seriesInfoStruc.m_barErrCode)
            Print(msg)
        seriesInfoStruc.m_barsCount = 1
        succeeded = False
    else:
        seriesInfoStruc.m_barsCount = _int(seriesLongInfo.v)
        seriesInfoStruc.m_barErrCode = 0
    if SeriesInfoInteger(statSymbol, tf, SERIES_FIRSTDATE, seriesLongInfo) == False:
        seriesInfoStruc.m_barDateErrCode = GetLastError()
        ResetLastError()
        if outputLogs == ON:
            msg = 'SetSeriesInfoForTf' + ' Caller: ' + caller + ', caller count' + IntegerToString(callerCount) + ' "SeriesInfoInteger" call for First Date of Time Frame: ' + GetPeriodText(tf) + ' posted error: ' + IntegerToString(seriesInfoStruc.m_barDateErrCode)
            Print(msg)
        timeCurrent = TimeCurrent()
        seriesInfoStruc.setBarTimeAndNum(timeCurrent, statSymbol, tf)
        succeeded = False
    else:
        seriesInfoStruc.setBarTimeAndNum(seriesLongInfo.v, statSymbol, tf)
        seriesInfoStruc.m_barDateErrCode = 0
    if SeriesInfoInteger(statSymbol, tf, SERIES_SYNCHRONIZED, seriesLongInfo) == False:
        seriesInfoStruc.m_syncErrCode = GetLastError()
        ResetLastError()
        if outputLogs == ON:
            msg = 'SetSeriesInfoForTf' + ' Caller: ' + caller + ', caller count' + IntegerToString(callerCount) + ' "SeriesInfoInteger" call for Synchronization of Time Frame: ' + GetPeriodText(tf) + ' posted error: ' + IntegerToString(seriesInfoStruc.m_syncErrCode)
            Print(msg)
        seriesInfoStruc.m_isSyncronized = False
        succeeded = False
    else:
        seriesInfoStruc.m_isSyncronized = _bool(seriesLongInfo.v)
        seriesInfoStruc.m_syncErrCode = 0
    return succeeded

def SetRatesBarNum(tfRates_ary, seriesInfo_ary, requestedBar, useRequestedBar):
    if ArrayRange(tfRates_ary, 0) == ArrayRange(seriesInfo_ary, 0):
        for idx in range(0, ArrayRange(seriesInfo_ary, 0)):
            if useRequestedBar == YES:
                if seriesInfo_ary[idx].m_barsCount > requestedBar:
                    tfRates_ary[idx].barNum = requestedBar
                else:
                    tfRates_ary[idx].barNum = seriesInfo_ary[idx].m_firstBarNum
            else:
                tfRates_ary[idx].barNum = seriesInfo_ary[idx].m_firstBarNum

def SetCopyRatesAryVals(caller, statsSymbol, periods_ary, tfRates_ary, callerCount):
    global msg
    succeeded = True
    i = 0
    while i < ArrayRange(periods_ary, 0):
        if SetRatesForBar(caller, statsSymbol, periods_ary[i], tfRates_ary[i], callerCount):
            if outputLogs == ON:
                msg = 'SetCopyRatesAryVals' + ' Called by ' + caller + ' on callerCount ' + IntegerToString(callerCount) + ' "CopyRates" succeeded for ' + Symbol() + ' in time frame ' + GetPeriodText(periods_ary[i]) + ' for bar ' + IntegerToString(tfRates_ary[i].barNum)
                Print(msg)
            tfRates_ary[i].disp = 'Bar ' + IntegerToString(tfRates_ary[i].barNum) + ', ' + TimeToString(tfRates_ary[i].mqlRates[0].time, TIME_DATE | TIME_MINUTES)
        else:
            tfRates_ary[i].disp = 'Bar ' + IntegerToString(tfRates_ary[i].barNum) + ', ER: ' + IntegerToString(tfRates_ary[i].errCode)
            tfRates_ary[i].errCode = 0
            succeeded = False
        i += 1
    return succeeded

def SetRatesForBar(caller, statsSymbol, barTF, ratesStruc, callerCount):
    global msg
    succeeded = True
    if CopyRates(statsSymbol, barTF, ratesStruc.barNum, COPYONEELEMENT, ratesStruc.mqlRates) < 0:
        ratesStruc.errCode = GetLastError()
        ResetLastError()
        if outputLogs == ON:
            msg = 'SetRatesForBar' + ' Caller: ' + caller + ', caller count' + IntegerToString(callerCount) + ' CopyRates Call for bar: ' + IntegerToString(ratesStruc.barNum) + ' of Time Frame: ' + GetPeriodText(barTF) + ' posted error: ' + IntegerToString(ratesStruc.errCode)
            Print(msg)
        succeeded = False
    return succeeded

def DisplayThePanel(tfRatesStruc_ary, seriesInfoStruc, tf_ary, statsSymbol):
    tfIdx = 0
    for objIdx in range(0, SERIES_INFO_IDX):
        SetDisplayText(objIdx, tf_ary[tfIdx], statsSymbol, tfRatesStruc_ary[tfIdx], seriesInfoStruc[tfIdx])
        _sw1 = disp_obj_type[objIdx]
        if _sw1 == OBJ_LABEL:
            ManageALabel(objIdx)
        elif _sw1 == OBJ_EDIT:
            DisplayABox(objIdx)
    tfIdx = 0
    while tfIdx < ArrayRange(TFPeriods, 0):
        objIdx = SERIES_INFO_IDX
        itrCount = 0
        while objIdx < END_DIP_OBJ_IDX:
            disp_Y_pos[objIdx] = disp_Y_pos[SYMB_HDR_IDX] + (20 + (15 * tfIdx))
            disp_X_pos[objIdx] = disp_X_pos[INFO_HDR_IDX] + (itrCount * 330)
            disp_obj_name[objIdx] = IntegerToString(uniquifier) + 'ROW' + IntegerToString(tfIdx) + '|' + IntegerToString(objIdx)
            SetDisplayText(objIdx, tf_ary[tfIdx], statsSymbol, tfRatesStruc_ary[tfIdx], seriesInfoStruc[tfIdx])
            _sw2 = disp_obj_type[objIdx]
            if _sw2 == OBJ_LABEL:
                ManageALabel(objIdx)
            elif _sw2 == OBJ_EDIT:
                DisplayABox(objIdx)
            objIdx += 1
            itrCount += 1
        tfIdx += 1

def SetDisplayText(objIdx, tf, statsSymbol, srucTfRates, seriesInfoStruc):
    global msg
    _sw3 = objIdx
    if _sw3 == INFO_HDR_IDX:
        if panelDisplay == ON:
            disp_obj_txt[INFO_HDR_IDX] = 'Rates and Bar:'
        else:
            disp_obj_txt[INFO_HDR_IDX] = 'Rates and Bars OFF'
    elif _sw3 == BAR_ENTRY_IDX:
        if useSuggetedBar == NO:
            disp_obj_txt[BAR_ENTRY_IDX] = 'Oldest'
        else:
            disp_obj_txt[BAR_ENTRY_IDX] = IntegerToString(suggestedBar)
    elif _sw3 == SYMB_HDR_IDX:
        disp_obj_txt[SYMB_HDR_IDX] = 'Symbol:'
    elif _sw3 == SYMB_ENTRY_IDX:
        disp_obj_txt[SYMB_ENTRY_IDX] = statsSymbol
    elif _sw3 == SERIES_INFO_IDX:
        disp_obj_txt[SERIES_INFO_IDX] = GetPeriodText(tf) + ' ' + ('SYNC' if (seriesInfoStruc.m_isSyncronized == True) else 'UN_SYNCH') + ', Bars: ' + IntegerToString(seriesInfoStruc.m_barsCount) + ', Time: ' + TimeToString(seriesInfoStruc.m_firstBarDate, TIME_DATE | TIME_MINUTES)
    elif _sw3 == RATES_INFO_IDX:
        disp_obj_txt[RATES_INFO_IDX] = srucTfRates.disp
    else:
        if objIdx < END_DIP_OBJ_IDX:
            disp_obj_txt[objIdx] = 'What the Heck ' + IntegerToString(objIdx)
        msg = 'SetDisplayText' + ' called with invalid value: ' + IntegerToString(objIdx)
        Print(msg)

def DisplayABox(objIdx):
    global _s_DisplayABox_chartID
    if _s_DisplayABox_chartID is _UNSET:
        _s_DisplayABox_chartID = ChartID()
    objName = disp_obj_name[objIdx]
    dispWindow = ObjectFind(_s_DisplayABox_chartID, objName)
    if dispWindow < 0:
        ObjectCreate(_s_DisplayABox_chartID, objName, OBJ_EDIT, WINDOW_ZERO, 0, 0)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_FONTSIZE, disp_obj_size[objIdx])
        ObjectSetString(_s_DisplayABox_chartID, objName, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_BORDER_COLOR, clrBlack)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_BGCOLOR, clrLightGray)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_XSIZE, 60)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_YSIZE, 20)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_ALIGN, ALIGN_CENTER)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_READONLY, False)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_BACK, False)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_SELECTED, False)
        ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_HIDDEN, True)
    ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_COLOR, disp_obj_clr[objIdx])
    ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_XDISTANCE, disp_X_pos[objIdx])
    ObjectSetInteger(_s_DisplayABox_chartID, objName, OBJPROP_YDISTANCE, disp_Y_pos[objIdx])
    ObjectSetString(_s_DisplayABox_chartID, objName, OBJPROP_TEXT, disp_obj_txt[objIdx])

def ManageALabel(objIdx):
    global _s_ManageALabel_chartID
    objColor = 0
    objName = disp_obj_name[objIdx]
    if outputLogs == ON and objName == (IntegerToString(uniquifier) + 'ROW20|5'):
        objColor = clrYellowGreen
    else:
        objColor = disp_obj_clr[objIdx]
    selectable = False
    if objIdx == INFO_HDR_IDX:
        selectable = True
    if _s_ManageALabel_chartID is _UNSET:
        _s_ManageALabel_chartID = ChartID()
    if ObjectFind(_s_ManageALabel_chartID, objName) < 0:
        ObjectCreate(_s_ManageALabel_chartID, objName, OBJ_LABEL, WINDOW_ZERO, 0, 0)
        ObjectSetInteger(_s_ManageALabel_chartID, objName, OBJPROP_FONTSIZE, disp_obj_size[objIdx])
        ObjectSetString(_s_ManageALabel_chartID, objName, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(_s_ManageALabel_chartID, objName, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(_s_ManageALabel_chartID, objName, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
        ObjectSetInteger(_s_ManageALabel_chartID, objName, OBJPROP_BACK, True)
        ObjectSetInteger(_s_ManageALabel_chartID, objName, OBJPROP_SELECTABLE, selectable)
        ObjectSetInteger(_s_ManageALabel_chartID, objName, OBJPROP_SELECTED, False)
        ObjectSetInteger(_s_ManageALabel_chartID, objName, OBJPROP_HIDDEN, True)
    ObjectSetInteger(_s_ManageALabel_chartID, objName, OBJPROP_COLOR, objColor)
    ObjectSetInteger(_s_ManageALabel_chartID, objName, OBJPROP_XDISTANCE, disp_X_pos[objIdx])
    ObjectSetInteger(_s_ManageALabel_chartID, objName, OBJPROP_YDISTANCE, disp_Y_pos[objIdx])
    ObjectSetString(_s_ManageALabel_chartID, objName, OBJPROP_TEXT, disp_obj_txt[objIdx])

def GetPeriodText(tf):
    returnString = ""
    workingTF = tf
    if tf == PERIOD_CURRENT:
        workingTF = Period()
    _sw4 = workingTF
    if _sw4 == PERIOD_M1:
        returnString = 'M1'
    elif _sw4 == PERIOD_M2:
        returnString = 'M2'
    elif _sw4 == PERIOD_M3:
        returnString = 'M3'
    elif _sw4 == PERIOD_M4:
        returnString = 'M4'
    elif _sw4 == PERIOD_M5:
        returnString = 'M5'
    elif _sw4 == PERIOD_M6:
        returnString = 'M6'
    elif _sw4 == PERIOD_M10:
        returnString = 'M10'
    elif _sw4 == PERIOD_M12:
        returnString = 'M12'
    elif _sw4 == PERIOD_M15:
        returnString = 'M15'
    elif _sw4 == PERIOD_M20:
        returnString = 'M20'
    elif _sw4 == PERIOD_M30:
        returnString = 'M30'
    elif _sw4 == PERIOD_H1:
        returnString = 'H1'
    elif _sw4 == PERIOD_H2:
        returnString = 'H2'
    elif _sw4 == PERIOD_H3:
        returnString = 'H3'
    elif _sw4 == PERIOD_H4:
        returnString = 'H4'
    elif _sw4 == PERIOD_H6:
        returnString = 'H6'
    elif _sw4 == PERIOD_H8:
        returnString = 'H8'
    elif _sw4 == PERIOD_H12:
        returnString = 'H12'
    elif _sw4 == PERIOD_D1:
        returnString = 'D1'
    elif _sw4 == PERIOD_W1:
        returnString = 'W1'
    elif _sw4 == PERIOD_MN1:
        returnString = 'MN1'
    else:
        returnString = 'Unknown: ' + IntegerToString(tf)
    return returnString

def GetMaxBarCount(seriesInfoStruc):
    maxCount = 0
    for i in range(0, ArrayRange(seriesInfoStruc, 0)):
        if seriesInfoStruc[i].m_barsCount > maxCount:
            maxCount = seriesInfoStruc[i].m_barsCount
    return maxCount

# ---- global variables initialised from expressions
struc_tfRates = Arr(0, 0, factory=tfRatesSruct)  # hold the Rates values for each timeframe
struc_seriesInfo = Arr(0, 0, factory=SeriesInfoStruc)  # hold the Rates values for each timeframe

# ---- static local variables
_s_OnChartEvent_clickCount = 0
_s_OnChartEvent_editCount = 0
_s_OnCalculate_callCount = 0
_s_DisplayABox_chartID = _UNSET
_s_ManageALabel_chartID = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SeriesIntegerInfoAndMqlRatesTFStatus(_MQL5Indicator):
    name = 'SeriesIntegerInfo_and_MqlRates_TF_Status'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

