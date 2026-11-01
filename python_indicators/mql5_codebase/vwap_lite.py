"""vwap_lite — converted from MQL5: MQL5 Indicators/VWAP Lite - Volume Weighted Average Price/vwap_lite.mq5

Copyright: Copyright 2016, SOL Digital Consultoria LTDA; Link: http://www.soldigitalconsultoria.com.br; Version: 1.49

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, SOL Digital Consultoria LTDA', 'link': 'http://www.soldigitalconsultoria.com.br', 'version': '1.49', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [32768]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 1, 2: 1, 3: 1}, 'labels': {1: 'VWAP Daily', 2: 'VWAP Weekly', 3: 'VWAP Monthly'}, 'levels': [], 'description': [], 'name': 'vwap_lite', 'source': 'MQL5 Indicators/VWAP Lite - Volume Weighted Average Price/vwap_lite.mq5', 'folder': 'VWAP Lite - Volume Weighted Average Price', 'inputs': [{'mql': 'Indicator_Name', 'py': 'Indicator_Name', 'param': None, 'type': 'string', 'default': 'Volume Weighted Average Price (VWAP)', 'label': '', 'sinput': True}, {'mql': 'Price_Type', 'py': 'Price_Type', 'param': 'Price_Type', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'Calc_Every_Tick', 'py': 'Calc_Every_Tick', 'param': 'Calc_Every_Tick', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Enable_Daily', 'py': 'Enable_Daily', 'param': 'Enable_Daily', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_Daily_Value', 'py': 'Show_Daily_Value', 'param': 'Show_Daily_Value', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Enable_Weekly', 'py': 'Enable_Weekly', 'param': 'Enable_Weekly', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Show_Weekly_Value', 'py': 'Show_Weekly_Value', 'param': 'Show_Weekly_Value', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Enable_Monthly', 'py': 'Enable_Monthly', 'param': 'Enable_Monthly', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Show_Monthly_Value', 'py': 'Show_Monthly_Value', 'param': 'Show_Monthly_Value', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 255  # #property indicator_color1
indicator_color2 = 16711680  # #property indicator_color2
indicator_color3 = 32768  # #property indicator_color3

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
Calc_Every_Tick = _input('Calc_Every_Tick', False)
Enable_Daily = _input('Enable_Daily', True)
Show_Daily_Value = _input('Show_Daily_Value', True)
Enable_Weekly = _input('Enable_Weekly', False)
Show_Weekly_Value = _input('Show_Weekly_Value', False)
Enable_Monthly = _input('Enable_Monthly', False)
Show_Monthly_Value = _input('Show_Monthly_Value', False)
VWAP_Buffer_Daily = Arr(0, 0.0)
VWAP_Buffer_Weekly = Arr(0, 0.0)
VWAP_Buffer_Monthly = Arr(0, 0.0)
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
sDailyStr = ''
sWeeklyStr = ''
sMonthlyStr = ''
LastTimePeriod = PERIOD_MN1
nStringYDistance = 40

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
    global nStringYDistance
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, VWAP_Buffer_Daily, INDICATOR_DATA)
    SetIndexBuffer(1, VWAP_Buffer_Weekly, INDICATOR_DATA)
    SetIndexBuffer(2, VWAP_Buffer_Monthly, INDICATOR_DATA)
    if Show_Daily_Value:
        ObjectCreate(0, 'VWAP_Daily', OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, 'VWAP_Daily', OBJPROP_CORNER, 3)
        ObjectSetInteger(0, 'VWAP_Daily', OBJPROP_XDISTANCE, 180)
        ObjectSetInteger(0, 'VWAP_Daily', OBJPROP_YDISTANCE, nStringYDistance)
        ObjectSetInteger(0, 'VWAP_Daily', OBJPROP_COLOR, indicator_color1)
        ObjectSetInteger(0, 'VWAP_Daily', OBJPROP_FONTSIZE, 7)
        ObjectSetString(0, 'VWAP_Daily', OBJPROP_FONT, 'Verdana')
        ObjectSetString(0, 'VWAP_Daily', OBJPROP_TEXT, ' ')
        nStringYDistance = nStringYDistance + 20
    if Show_Weekly_Value:
        ObjectCreate(0, 'VWAP_Weekly', OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, 'VWAP_Weekly', OBJPROP_CORNER, 3)
        ObjectSetInteger(0, 'VWAP_Weekly', OBJPROP_XDISTANCE, 180)
        ObjectSetInteger(0, 'VWAP_Weekly', OBJPROP_YDISTANCE, nStringYDistance)
        ObjectSetInteger(0, 'VWAP_Weekly', OBJPROP_COLOR, indicator_color2)
        ObjectSetInteger(0, 'VWAP_Weekly', OBJPROP_FONTSIZE, 7)
        ObjectSetString(0, 'VWAP_Weekly', OBJPROP_FONT, 'Verdana')
        ObjectSetString(0, 'VWAP_Weekly', OBJPROP_TEXT, ' ')
        nStringYDistance = nStringYDistance + 20
    if Show_Monthly_Value:
        ObjectCreate(0, 'VWAP_Monthly', OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, 'VWAP_Monthly', OBJPROP_CORNER, 3)
        ObjectSetInteger(0, 'VWAP_Monthly', OBJPROP_XDISTANCE, 180)
        ObjectSetInteger(0, 'VWAP_Monthly', OBJPROP_YDISTANCE, nStringYDistance)
        ObjectSetInteger(0, 'VWAP_Monthly', OBJPROP_COLOR, indicator_color3)
        ObjectSetInteger(0, 'VWAP_Monthly', OBJPROP_FONTSIZE, 7)
        ObjectSetString(0, 'VWAP_Monthly', OBJPROP_FONT, 'Verdana')
        ObjectSetString(0, 'VWAP_Monthly', OBJPROP_TEXT, ' ')
    return INIT_SUCCEEDED

def OnDeinit(pReason):
    if Show_Daily_Value:
        ObjectDelete(0, 'VWAP_Daily')
    if Show_Weekly_Value:
        ObjectDelete(0, 'VWAP_Weekly')
    if Show_Monthly_Value:
        ObjectDelete(0, 'VWAP_Monthly')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LastTimePeriod, bIsFirstRun, dtLastDay, dtLastMonth, dtLastWeek, nIdx, nIdxDaily, nIdxMonthly, nIdxWeekly, nSumDailyTPV, nSumDailyVol, nSumMonthlyTPV, nSumMonthlyVol, nSumWeeklyTPV, nSumWeeklyVol, sDailyStr, sMonthlyStr, sWeeklyStr
    if PERIOD_CURRENT != LastTimePeriod:
        bIsFirstRun = True
        LastTimePeriod = PERIOD_CURRENT
    if (rates_total > prev_calculated or bIsFirstRun) or Calc_Every_Tick:
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
            VWAP_Buffer_Daily[nIdx] = EMPTY_VALUE
            VWAP_Buffer_Weekly[nIdx] = EMPTY_VALUE
            VWAP_Buffer_Monthly[nIdx] = EMPTY_VALUE
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
        bIsFirstRun = False
    return rates_total

# ---- global variables initialised from expressions
dtLastDay = CreateDateTime(DAILY)
dtLastWeek = CreateDateTime(WEEKLY)
dtLastMonth = CreateDateTime(MONTHLY)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VwapLite(_MQL5Indicator):
    name = 'vwap_lite'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price_Type': _Choice({0: 'OPEN', 1: 'CLOSE', 2: 'HIGH', 3: 'LOW', 4: 'OPEN_CLOSE', 5: 'HIGH_LOW', 6: 'CLOSE_HIGH_LOW', 7: 'OPEN_CLOSE_HIGH_LOW'}, default=6),
        'Calc_Every_Tick': False,
        'Enable_Daily': True,
        'Show_Daily_Value': True,
        'Enable_Weekly': False,
        'Show_Weekly_Value': False,
        'Enable_Monthly': False,
        'Show_Monthly_Value': False,
    }

