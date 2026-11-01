"""vwap — converted from MQL5: MQL5 Indicators/VWAP - Volume Weighted Average Price/vwap.mq5

Copyright: Copyright 2015, SOL Digital Consultoria LTDA; Link: http://www.soldigitalconsultoria.com.br; Version: 1.47

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, SOL Digital Consultoria LTDA', 'link': 'http://www.soldigitalconsultoria.com.br', 'version': '1.47', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [255], 2: [16711680], 3: [32768], 4: [8421504], 5: [65535], 6: [32768], 7: [0], 8: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2}, 'styles': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'labels': {1: 'VWAP Daily', 2: 'VWAP Weekly', 3: 'VWAP Monthly', 4: 'VWAP Level 01', 5: 'VWAP Level 02', 6: 'VWAP Level 03', 7: 'VWAP Level 04', 8: 'VWAP Level 05'}, 'levels': [], 'description': [], 'name': 'vwap', 'source': 'MQL5 Indicators/VWAP - Volume Weighted Average Price/vwap.mq5', 'folder': 'VWAP - Volume Weighted Average Price', 'inputs': [{'mql': 'Indicator_Name', 'py': 'Indicator_Name', 'param': None, 'type': 'string', 'default': 'Volume Weighted Average Price (VWAP)', 'label': '', 'sinput': True}, {'mql': 'Price_Type', 'py': 'Price_Type', 'param': 'Price_Type', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'Enable_Daily', 'py': 'Enable_Daily', 'param': 'Enable_Daily', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Enable_Weekly', 'py': 'Enable_Weekly', 'param': 'Enable_Weekly', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Enable_Monthly', 'py': 'Enable_Monthly', 'param': 'Enable_Monthly', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Enable_Level_01', 'py': 'Enable_Level_01', 'param': 'Enable_Level_01', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'VWAP_Level_01_Period', 'py': 'VWAP_Level_01_Period', 'param': 'VWAP_Level_01_Period', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Enable_Level_02', 'py': 'Enable_Level_02', 'param': 'Enable_Level_02', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'VWAP_Level_02_Period', 'py': 'VWAP_Level_02_Period', 'param': 'VWAP_Level_02_Period', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'Enable_Level_03', 'py': 'Enable_Level_03', 'param': 'Enable_Level_03', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'VWAP_Level_03_Period', 'py': 'VWAP_Level_03_Period', 'param': 'VWAP_Level_03_Period', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'Enable_Level_04', 'py': 'Enable_Level_04', 'param': 'Enable_Level_04', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'VWAP_Level_04_Period', 'py': 'VWAP_Level_04_Period', 'param': 'VWAP_Level_04_Period', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'Enable_Level_05', 'py': 'Enable_Level_05', 'param': 'Enable_Level_05', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'VWAP_Level_05_Period', 'py': 'VWAP_Level_05_Period', 'param': 'VWAP_Level_05_Period', 'type': 'int', 'default': 40, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 255  # #property indicator_color1
indicator_color2 = 16711680  # #property indicator_color2
indicator_color3 = 32768  # #property indicator_color3
indicator_color4 = 8421504  # #property indicator_color4
indicator_color5 = 65535  # #property indicator_color5
indicator_color6 = 32768  # #property indicator_color6
indicator_color7 = 0  # #property indicator_color7
indicator_color8 = 16711680  # #property indicator_color8

# enum DATE_TYPE
DAILY = 0
WEEKLY = 1
MONTHLY = 2
_enum('DATE_TYPE', {0: 'DAILY', 1: 'WEEKLY', 2: 'MONTHLY'})

# enum PRICE_TYPE
OPEN = 0
CLOSE = 1
HIGH = 2
LOW = 3
OPEN_CLOSE = 4
HIGH_LOW = 5
CLOSE_HIGH_LOW = 6
OPEN_CLOSE_HIGH_LOW = 7
_enum('PRICE_TYPE', {0: 'OPEN', 1: 'CLOSE', 2: 'HIGH', 3: 'LOW', 4: 'OPEN_CLOSE', 5: 'HIGH_LOW', 6: 'CLOSE_HIGH_LOW', 7: 'OPEN_CLOSE_HIGH_LOW'})

# ---- inputs and global variables
Indicator_Name = _input('Indicator_Name', 'Volume Weighted Average Price (VWAP)')
Price_Type = _input('Price_Type', CLOSE_HIGH_LOW)
Enable_Daily = _input('Enable_Daily', True)
Enable_Weekly = _input('Enable_Weekly', True)
Enable_Monthly = _input('Enable_Monthly', True)
Enable_Level_01 = _input('Enable_Level_01', False)
VWAP_Level_01_Period = _input('VWAP_Level_01_Period', 5)
Enable_Level_02 = _input('Enable_Level_02', False)
VWAP_Level_02_Period = _input('VWAP_Level_02_Period', 13)
Enable_Level_03 = _input('Enable_Level_03', False)
VWAP_Level_03_Period = _input('VWAP_Level_03_Period', 20)
Enable_Level_04 = _input('Enable_Level_04', False)
VWAP_Level_04_Period = _input('VWAP_Level_04_Period', 30)
Enable_Level_05 = _input('Enable_Level_05', False)
VWAP_Level_05_Period = _input('VWAP_Level_05_Period', 40)
Show_Daily_Value = True
Show_Weekly_Value = True
Show_Monthly_Value = True
VWAP_Buffer_Daily = Arr(0, 0.0)
VWAP_Buffer_Weekly = Arr(0, 0.0)
VWAP_Buffer_Monthly = Arr(0, 0.0)
VWAP_Buffer_01 = Arr(0, 0.0)
VWAP_Buffer_02 = Arr(0, 0.0)
VWAP_Buffer_03 = Arr(0, 0.0)
VWAP_Buffer_04 = Arr(0, 0.0)
VWAP_Buffer_05 = Arr(0, 0.0)
nPriceArr = Arr(0, 0.0)
nTotalTPV = Arr(0, 0.0)
nTotalVol = Arr(0, 0.0)
nSumDailyTPV = 0.0
nSumWeeklyTPV = 0.0
nSumMonthlyTPV = 0.0
nSumDailyVol = 0.0
nSumWeeklyVol = 0.0
nSumMonthlyVol = 0.0
nIdxDaily = 0
nIdxWeekly = 0
nIdxMonthly = 0
nIdx = 0
bIsFirstRun = True
LastTimePeriod = PERIOD_MN1
sDailyStr = ''
sWeeklyStr = ''
sMonthlyStr = ''
sLevel01Str = ''
sLevel02Str = ''
sLevel03Str = ''
sLevel04Str = ''
sLevel05Str = ''

def CreateDateTime(nReturnType=DAILY, dtDay=946684800, pHour=0, pMinute=0, pSecond=0):
    dtReturnDate = 0
    timeStruct = MqlDateTime()
    TimeToStruct(dtDay, timeStruct)
    timeStruct.hour = pHour
    timeStruct.min = pMinute
    timeStruct.sec = pSecond
    dtReturnDate = StructToTime(timeStruct)
    if nReturnType == WEEKLY:
        while timeStruct.day_of_week != 0:
            dtReturnDate = dtReturnDate - 86400
            TimeToStruct(dtReturnDate, timeStruct)
    if nReturnType == MONTHLY:
        timeStruct.day = 1
        dtReturnDate = StructToTime(timeStruct)
    return dtReturnDate

def OnInit():
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, VWAP_Buffer_Daily, INDICATOR_DATA)
    SetIndexBuffer(1, VWAP_Buffer_Weekly, INDICATOR_DATA)
    SetIndexBuffer(2, VWAP_Buffer_Monthly, INDICATOR_DATA)
    SetIndexBuffer(3, VWAP_Buffer_01, INDICATOR_DATA)
    SetIndexBuffer(4, VWAP_Buffer_02, INDICATOR_DATA)
    SetIndexBuffer(5, VWAP_Buffer_03, INDICATOR_DATA)
    SetIndexBuffer(6, VWAP_Buffer_04, INDICATOR_DATA)
    SetIndexBuffer(7, VWAP_Buffer_05, INDICATOR_DATA)
    ObjectCreate(0, 'VWAP_Daily', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'VWAP_Daily', OBJPROP_CORNER, 3)
    ObjectSetInteger(0, 'VWAP_Daily', OBJPROP_XDISTANCE, 180)
    ObjectSetInteger(0, 'VWAP_Daily', OBJPROP_YDISTANCE, 40)
    ObjectSetInteger(0, 'VWAP_Daily', OBJPROP_COLOR, indicator_color1)
    ObjectSetInteger(0, 'VWAP_Daily', OBJPROP_FONTSIZE, 7)
    ObjectSetString(0, 'VWAP_Daily', OBJPROP_FONT, 'Verdana')
    ObjectSetString(0, 'VWAP_Daily', OBJPROP_TEXT, ' ')
    ObjectCreate(0, 'VWAP_Weekly', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'VWAP_Weekly', OBJPROP_CORNER, 3)
    ObjectSetInteger(0, 'VWAP_Weekly', OBJPROP_XDISTANCE, 180)
    ObjectSetInteger(0, 'VWAP_Weekly', OBJPROP_YDISTANCE, 60)
    ObjectSetInteger(0, 'VWAP_Weekly', OBJPROP_COLOR, indicator_color2)
    ObjectSetInteger(0, 'VWAP_Weekly', OBJPROP_FONTSIZE, 7)
    ObjectSetString(0, 'VWAP_Weekly', OBJPROP_FONT, 'Verdana')
    ObjectSetString(0, 'VWAP_Weekly', OBJPROP_TEXT, ' ')
    ObjectCreate(0, 'VWAP_Monthly', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'VWAP_Monthly', OBJPROP_CORNER, 3)
    ObjectSetInteger(0, 'VWAP_Monthly', OBJPROP_XDISTANCE, 180)
    ObjectSetInteger(0, 'VWAP_Monthly', OBJPROP_YDISTANCE, 80)
    ObjectSetInteger(0, 'VWAP_Monthly', OBJPROP_COLOR, indicator_color3)
    ObjectSetInteger(0, 'VWAP_Monthly', OBJPROP_FONTSIZE, 7)
    ObjectSetString(0, 'VWAP_Monthly', OBJPROP_FONT, 'Verdana')
    ObjectSetString(0, 'VWAP_Monthly', OBJPROP_TEXT, ' ')
    ObjectCreate(0, 'VWAP_Level_01', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'VWAP_Level_01', OBJPROP_CORNER, 3)
    ObjectSetInteger(0, 'VWAP_Level_01', OBJPROP_XDISTANCE, 180)
    ObjectSetInteger(0, 'VWAP_Level_01', OBJPROP_YDISTANCE, 100)
    ObjectSetInteger(0, 'VWAP_Level_01', OBJPROP_COLOR, indicator_color4)
    ObjectSetInteger(0, 'VWAP_Level_01', OBJPROP_FONTSIZE, 7)
    ObjectSetString(0, 'VWAP_Level_01', OBJPROP_FONT, 'Verdana')
    ObjectSetString(0, 'VWAP_Level_01', OBJPROP_TEXT, ' ')
    ObjectCreate(0, 'VWAP_Level_02', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'VWAP_Level_02', OBJPROP_CORNER, 3)
    ObjectSetInteger(0, 'VWAP_Level_02', OBJPROP_XDISTANCE, 180)
    ObjectSetInteger(0, 'VWAP_Level_02', OBJPROP_YDISTANCE, 120)
    ObjectSetInteger(0, 'VWAP_Level_02', OBJPROP_COLOR, indicator_color5)
    ObjectSetInteger(0, 'VWAP_Level_02', OBJPROP_FONTSIZE, 7)
    ObjectSetString(0, 'VWAP_Level_02', OBJPROP_FONT, 'Verdana')
    ObjectSetString(0, 'VWAP_Level_02', OBJPROP_TEXT, ' ')
    ObjectCreate(0, 'VWAP_Level_03', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'VWAP_Level_03', OBJPROP_CORNER, 3)
    ObjectSetInteger(0, 'VWAP_Level_03', OBJPROP_XDISTANCE, 180)
    ObjectSetInteger(0, 'VWAP_Level_03', OBJPROP_YDISTANCE, 140)
    ObjectSetInteger(0, 'VWAP_Level_03', OBJPROP_COLOR, indicator_color6)
    ObjectSetInteger(0, 'VWAP_Level_03', OBJPROP_FONTSIZE, 7)
    ObjectSetString(0, 'VWAP_Level_03', OBJPROP_FONT, 'Verdana')
    ObjectSetString(0, 'VWAP_Level_03', OBJPROP_TEXT, ' ')
    ObjectCreate(0, 'VWAP_Level_04', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'VWAP_Level_04', OBJPROP_CORNER, 3)
    ObjectSetInteger(0, 'VWAP_Level_04', OBJPROP_XDISTANCE, 180)
    ObjectSetInteger(0, 'VWAP_Level_04', OBJPROP_YDISTANCE, 160)
    ObjectSetInteger(0, 'VWAP_Level_04', OBJPROP_COLOR, indicator_color7)
    ObjectSetInteger(0, 'VWAP_Level_04', OBJPROP_FONTSIZE, 7)
    ObjectSetString(0, 'VWAP_Level_04', OBJPROP_FONT, 'Verdana')
    ObjectSetString(0, 'VWAP_Level_04', OBJPROP_TEXT, ' ')
    ObjectCreate(0, 'VWAP_Level_05', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'VWAP_Level_05', OBJPROP_CORNER, 3)
    ObjectSetInteger(0, 'VWAP_Level_05', OBJPROP_XDISTANCE, 180)
    ObjectSetInteger(0, 'VWAP_Level_05', OBJPROP_YDISTANCE, 180)
    ObjectSetInteger(0, 'VWAP_Level_05', OBJPROP_COLOR, indicator_color8)
    ObjectSetInteger(0, 'VWAP_Level_05', OBJPROP_FONTSIZE, 7)
    ObjectSetString(0, 'VWAP_Level_05', OBJPROP_FONT, 'Verdana')
    ObjectSetString(0, 'VWAP_Level_05', OBJPROP_TEXT, ' ')
    return INIT_SUCCEEDED

def OnDeinit(pReason):
    ObjectDelete(0, 'VWAP_Daily')
    ObjectDelete(0, 'VWAP_Weekly')
    ObjectDelete(0, 'VWAP_Monthly')
    ObjectDelete(0, 'VWAP_Level_01')
    ObjectDelete(0, 'VWAP_Level_02')
    ObjectDelete(0, 'VWAP_Level_03')
    ObjectDelete(0, 'VWAP_Level_04')
    ObjectDelete(0, 'VWAP_Level_05')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LastTimePeriod, bIsFirstRun, dtLastDay, dtLastMonth, dtLastWeek, nIdx, nIdxDaily, nIdxMonthly, nIdxWeekly, nSumDailyTPV, nSumDailyVol, nSumMonthlyTPV, nSumMonthlyVol, nSumWeeklyTPV, nSumWeeklyVol, sDailyStr, sLevel01Str, sLevel02Str, sLevel03Str, sLevel04Str, sLevel05Str, sMonthlyStr, sWeeklyStr
    if PERIOD_CURRENT != LastTimePeriod:
        bIsFirstRun = True
        LastTimePeriod = PERIOD_CURRENT
    if rates_total > prev_calculated or bIsFirstRun:
        ArrayResize(nPriceArr, rates_total)
        ArrayResize(nTotalTPV, rates_total)
        ArrayResize(nTotalVol, rates_total)
        if Enable_Daily:
            nIdx = nIdxDaily
            nSumDailyTPV = 0.0
            nSumDailyVol = 0.0
        if Enable_Weekly:
            nIdx = nIdxWeekly
            nSumWeeklyTPV = 0.0
            nSumWeeklyVol = 0.0
        if Enable_Monthly:
            nIdx = nIdxMonthly
            nSumMonthlyTPV = 0.0
            nSumMonthlyVol = 0.0
        while nIdx < rates_total:
            if CreateDateTime(DAILY, time[nIdx]) != dtLastDay:
                nIdxDaily = nIdx
                nSumDailyTPV = 0.0
                nSumDailyVol = 0.0
            if CreateDateTime(WEEKLY, time[nIdx]) != dtLastWeek:
                nIdxWeekly = nIdx
                nSumWeeklyTPV = 0.0
                nSumWeeklyVol = 0.0
            if CreateDateTime(MONTHLY, time[nIdx]) != dtLastMonth:
                nIdxMonthly = nIdx
                nSumMonthlyTPV = 0.0
                nSumMonthlyVol = 0.0
            nPriceArr[nIdx] = 0.0
            nTotalTPV[nIdx] = 0.0
            nTotalVol[nIdx] = 0.0
            _sw1 = Price_Type
            if _sw1 == OPEN:
                nPriceArr[nIdx] = open[nIdx]
            elif _sw1 == CLOSE:
                nPriceArr[nIdx] = close[nIdx]
            elif _sw1 == HIGH:
                nPriceArr[nIdx] = high[nIdx]
            elif _sw1 == LOW:
                nPriceArr[nIdx] = low[nIdx]
            elif _sw1 == HIGH_LOW:
                nPriceArr[nIdx] = (high[nIdx] + low[nIdx]) / 2
            elif _sw1 == OPEN_CLOSE:
                nPriceArr[nIdx] = (open[nIdx] + close[nIdx]) / 2
            elif _sw1 == CLOSE_HIGH_LOW:
                nPriceArr[nIdx] = (close[nIdx] + high[nIdx] + low[nIdx]) / 3
            elif _sw1 == OPEN_CLOSE_HIGH_LOW:
                nPriceArr[nIdx] = (open[nIdx] + close[nIdx] + high[nIdx] + low[nIdx]) / 4
            else:
                nPriceArr[nIdx] = (close[nIdx] + high[nIdx] + low[nIdx]) / 3
            if tick_volume[nIdx]:
                nTotalTPV[nIdx] = nPriceArr[nIdx] * tick_volume[nIdx]
                nTotalVol[nIdx] = float(tick_volume[nIdx])
            elif volume[nIdx]:
                nTotalTPV[nIdx] = nPriceArr[nIdx] * volume[nIdx]
                nTotalVol[nIdx] = float(volume[nIdx])
            if Enable_Daily and nIdx >= nIdxDaily:
                nSumDailyTPV += nTotalTPV[nIdx]
                nSumDailyVol += nTotalVol[nIdx]
                if nSumDailyVol:
                    VWAP_Buffer_Daily[nIdx] = _fdiv(nSumDailyTPV, nSumDailyVol)
                if sDailyStr != ('VWAP Daily: ' + _str(NormalizeDouble(VWAP_Buffer_Daily[nIdx], Digits()))) and Show_Daily_Value:
                    sDailyStr = 'VWAP Daily: ' + _str(NormalizeDouble(VWAP_Buffer_Daily[nIdx], Digits()))
                    ObjectSetString(0, 'VWAP_Daily', OBJPROP_TEXT, sDailyStr)
            if Enable_Weekly and nIdx >= nIdxWeekly:
                nSumWeeklyTPV += nTotalTPV[nIdx]
                nSumWeeklyVol += nTotalVol[nIdx]
                if nSumWeeklyVol:
                    VWAP_Buffer_Weekly[nIdx] = _fdiv(nSumWeeklyTPV, nSumWeeklyVol)
                if sWeeklyStr != ('VWAP Weekly: ' + _str(NormalizeDouble(VWAP_Buffer_Weekly[nIdx], Digits()))) and Show_Weekly_Value:
                    sWeeklyStr = 'VWAP Weekly: ' + _str(NormalizeDouble(VWAP_Buffer_Weekly[nIdx], Digits()))
                    ObjectSetString(0, 'VWAP_Weekly', OBJPROP_TEXT, sWeeklyStr)
            if Enable_Monthly and nIdx >= nIdxMonthly:
                nSumMonthlyTPV += nTotalTPV[nIdx]
                nSumMonthlyVol += nTotalVol[nIdx]
                if nSumMonthlyVol:
                    VWAP_Buffer_Monthly[nIdx] = _fdiv(nSumMonthlyTPV, nSumMonthlyVol)
                if sMonthlyStr != ('VWAP Monthly: ' + _str(NormalizeDouble(VWAP_Buffer_Monthly[nIdx], Digits()))) and Show_Monthly_Value:
                    sMonthlyStr = 'VWAP Monthly: ' + _str(NormalizeDouble(VWAP_Buffer_Monthly[nIdx], Digits()))
                    ObjectSetString(0, 'VWAP_Monthly', OBJPROP_TEXT, sMonthlyStr)
            dtLastDay = CreateDateTime(DAILY, time[nIdx])
            dtLastWeek = CreateDateTime(WEEKLY, time[nIdx])
            dtLastMonth = CreateDateTime(MONTHLY, time[nIdx])
            nIdx += 1
        if Enable_Level_01:
            nStartPos = ((prev_calculated - VWAP_Level_01_Period) if (prev_calculated > VWAP_Level_01_Period) else VWAP_Level_01_Period)
            nIdx = nStartPos
            while nIdx < rates_total:
                nSumTotalTPV = 0.0
                nSumTotalVol = 0.0
                VWAP_Buffer_01[nIdx] = EMPTY_VALUE
                for nSubIdx in range(1, VWAP_Level_01_Period):
                    nSumTotalTPV += nTotalTPV[nIdx - nSubIdx]
                    nSumTotalVol += nTotalVol[nIdx - nSubIdx]
                if nSumTotalVol:
                    VWAP_Buffer_01[nIdx] = _fdiv(nSumTotalTPV, nSumTotalVol)
                else:
                    VWAP_Buffer_01[nIdx] = 0.0
                if sLevel01Str != ('VWAP Level 01 (' + _str(VWAP_Level_01_Period) + '): ' + _str(NormalizeDouble(VWAP_Buffer_01[nIdx], Digits()))):
                    sLevel01Str = 'VWAP Level 01 (' + _str(VWAP_Level_01_Period) + '): ' + _str(NormalizeDouble(VWAP_Buffer_01[nIdx], Digits()))
                    ObjectSetString(0, 'VWAP_Level_01', OBJPROP_TEXT, sLevel01Str)
                nIdx += 1
        if Enable_Level_02:
            nStartPos = ((prev_calculated - VWAP_Level_02_Period) if (prev_calculated > VWAP_Level_02_Period) else VWAP_Level_02_Period)
            nIdx = nStartPos
            while nIdx < rates_total:
                nSumTotalTPV = 0.0
                nSumTotalVol = 0.0
                VWAP_Buffer_02[nIdx] = EMPTY_VALUE
                for nSubIdx in range(1, VWAP_Level_02_Period):
                    nSumTotalTPV += nTotalTPV[nIdx - nSubIdx]
                    nSumTotalVol += nTotalVol[nIdx - nSubIdx]
                if nSumTotalVol:
                    VWAP_Buffer_02[nIdx] = _fdiv(nSumTotalTPV, nSumTotalVol)
                else:
                    VWAP_Buffer_02[nIdx] = 0.0
                if sLevel02Str != ('VWAP Level 02 (' + _str(VWAP_Level_02_Period) + '): ' + _str(NormalizeDouble(VWAP_Buffer_02[nIdx], Digits()))):
                    sLevel02Str = 'VWAP Level 02 (' + _str(VWAP_Level_02_Period) + '): ' + _str(NormalizeDouble(VWAP_Buffer_02[nIdx], Digits()))
                    ObjectSetString(0, 'VWAP_Level_02', OBJPROP_TEXT, sLevel02Str)
                nIdx += 1
        if Enable_Level_03:
            nStartPos = ((prev_calculated - VWAP_Level_03_Period) if (prev_calculated > VWAP_Level_03_Period) else VWAP_Level_03_Period)
            nIdx = nStartPos
            while nIdx < rates_total:
                nSumTotalTPV = 0.0
                nSumTotalVol = 0.0
                VWAP_Buffer_03[nIdx] = EMPTY_VALUE
                for nSubIdx in range(1, VWAP_Level_03_Period):
                    nSumTotalTPV += nTotalTPV[nIdx - nSubIdx]
                    nSumTotalVol += nTotalVol[nIdx - nSubIdx]
                if nSumTotalVol:
                    VWAP_Buffer_03[nIdx] = _fdiv(nSumTotalTPV, nSumTotalVol)
                else:
                    VWAP_Buffer_03[nIdx] = 0.0
                if sLevel03Str != ('VWAP Level 03 (' + _str(VWAP_Level_03_Period) + '): ' + _str(NormalizeDouble(VWAP_Buffer_03[nIdx], Digits()))):
                    sLevel03Str = 'VWAP Level 03 (' + _str(VWAP_Level_03_Period) + '): ' + _str(NormalizeDouble(VWAP_Buffer_03[nIdx], Digits()))
                    ObjectSetString(0, 'VWAP_Level_03', OBJPROP_TEXT, sLevel03Str)
                nIdx += 1
        if Enable_Level_04:
            nStartPos = ((prev_calculated - VWAP_Level_04_Period) if (prev_calculated > VWAP_Level_04_Period) else VWAP_Level_04_Period)
            nIdx = nStartPos
            while nIdx < rates_total:
                nSumTotalTPV = 0.0
                nSumTotalVol = 0.0
                VWAP_Buffer_04[nIdx] = EMPTY_VALUE
                for nSubIdx in range(1, VWAP_Level_04_Period):
                    nSumTotalTPV += nTotalTPV[nIdx - nSubIdx]
                    nSumTotalVol += nTotalVol[nIdx - nSubIdx]
                if nSumTotalVol:
                    VWAP_Buffer_04[nIdx] = _fdiv(nSumTotalTPV, nSumTotalVol)
                else:
                    VWAP_Buffer_04[nIdx] = 0.0
                if sLevel04Str != ('VWAP Level 04 (' + _str(VWAP_Level_04_Period) + '): ' + _str(NormalizeDouble(VWAP_Buffer_04[nIdx], Digits()))):
                    sLevel04Str = 'VWAP Level 04 (' + _str(VWAP_Level_04_Period) + '): ' + _str(NormalizeDouble(VWAP_Buffer_04[nIdx], Digits()))
                    ObjectSetString(0, 'VWAP_Level_04', OBJPROP_TEXT, sLevel04Str)
                nIdx += 1
        if Enable_Level_05:
            nStartPos = ((prev_calculated - VWAP_Level_05_Period) if (prev_calculated > VWAP_Level_05_Period) else VWAP_Level_05_Period)
            nIdx = nStartPos
            while nIdx < rates_total:
                nSumTotalTPV = 0.0
                nSumTotalVol = 0.0
                VWAP_Buffer_05[nIdx] = EMPTY_VALUE
                for nSubIdx in range(1, VWAP_Level_05_Period):
                    nSumTotalTPV += nTotalTPV[nIdx - nSubIdx]
                    nSumTotalVol += nTotalVol[nIdx - nSubIdx]
                if nSumTotalVol:
                    VWAP_Buffer_05[nIdx] = _fdiv(nSumTotalTPV, nSumTotalVol)
                else:
                    VWAP_Buffer_05[nIdx] = 0.0
                if sLevel05Str != ('VWAP Level 05 (' + _str(VWAP_Level_05_Period) + '): ' + _str(NormalizeDouble(VWAP_Buffer_05[nIdx], Digits()))):
                    sLevel05Str = 'VWAP Level 05 (' + _str(VWAP_Level_05_Period) + '): ' + _str(NormalizeDouble(VWAP_Buffer_05[nIdx], Digits()))
                    ObjectSetString(0, 'VWAP_Level_05', OBJPROP_TEXT, sLevel05Str)
                nIdx += 1
        bIsFirstRun = False
    return rates_total

# ---- global variables initialised from expressions
dtLastDay = CreateDateTime(DAILY)
dtLastWeek = CreateDateTime(WEEKLY)
dtLastMonth = CreateDateTime(MONTHLY)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vwap(_MQL5Indicator):
    name = 'vwap'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price_Type': _Choice({0: 'OPEN', 1: 'CLOSE', 2: 'HIGH', 3: 'LOW', 4: 'OPEN_CLOSE', 5: 'HIGH_LOW', 6: 'CLOSE_HIGH_LOW', 7: 'OPEN_CLOSE_HIGH_LOW'}, default=6),
        'Enable_Daily': True,
        'Enable_Weekly': True,
        'Enable_Monthly': True,
        'Enable_Level_01': False,
        'VWAP_Level_01_Period': 5,
        'Enable_Level_02': False,
        'VWAP_Level_02_Period': 13,
        'Enable_Level_03': False,
        'VWAP_Level_03_Period': 20,
        'Enable_Level_04': False,
        'VWAP_Level_04_Period': 30,
        'Enable_Level_05': False,
        'VWAP_Level_05_Period': 40,
    }

