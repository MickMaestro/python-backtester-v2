"""clearview_periodseparator — converted from MQL5: MQL5 Indicators/ClearView - PricePointer, RoundNumberMarker, PeriodSeparator plus template/clearview_periodseparator.mq5

ClearView PeriodSeparator, period separator to mark days, weeks, months and custom session start/end
 
This is indicator is best used together with: ClearView_PricePointer and ClearView_RoundNumberMarker
 
See the source file for instructions on usage
Copyright: 2010, traderak20@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, traderak20@gmail.com', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['ClearView PeriodSeparator, period separator to mark days, weeks, months and custom session start/end', ' ', 'This is indicator is best used together with: ClearView_PricePointer and ClearView_RoundNumberMarker', ' ', 'See the source file for instructions on usage'], 'name': 'clearview_periodseparator', 'source': 'MQL5 Indicators/ClearView - PricePointer, RoundNumberMarker, PeriodSeparator plus template/clearview_periodseparator.mq5', 'folder': 'ClearView - PricePointer, RoundNumberMarker, PeriodSeparator plus template', 'inputs': [{'mql': 'InpMaxBars', 'py': 'InpMaxBars', 'param': 'InpMaxBars', 'type': 'int', 'default': 2500, 'label': 'Show separators for # bars (0=ALL)', 'sinput': False}, {'mql': 'InpUseBrightColors', 'py': 'InpUseBrightColors', 'param': 'InpUseBrightColors', 'type': 'bool', 'default': True, 'label': 'Use bright colors', 'sinput': False}, {'mql': 'InpDrawAsBackground', 'py': 'InpDrawAsBackground', 'param': 'InpDrawAsBackground', 'type': 'bool', 'default': True, 'label': 'Draw lines as background', 'sinput': False}, {'mql': 'InpShowSessionSeparator', 'py': 'InpShowSessionSeparator', 'param': 'InpShowSessionSeparator', 'type': 'bool', 'default': True, 'label': 'Show separator for session start/end', 'sinput': False}, {'mql': 'InpMaxTF_Session', 'py': 'InpMaxTF_Session', 'param': 'InpMaxTF_Session', 'type': 'int', 'default': 30, 'label': 'Show session separator up to timeframe', 'sinput': False}, {'mql': 'InpSessionStartTime', 'py': 'InpSessionStartTime', 'param': 'InpSessionStartTime', 'type': 'int', 'default': 9, 'label': 'Start hour of session (0-23)', 'sinput': False}, {'mql': 'InpShiftStartMins', 'py': 'InpShiftStartMins', 'param': 'InpShiftStartMins', 'type': 'int', 'default': 0, 'label': 'Shift start by minutes', 'sinput': False}, {'mql': 'InpSessionEndTime', 'py': 'InpSessionEndTime', 'param': 'InpSessionEndTime', 'type': 'int', 'default': 18, 'label': 'End hour of session (0-23)', 'sinput': False}, {'mql': 'InpShiftEndMins', 'py': 'InpShiftEndMins', 'param': 'InpShiftEndMins', 'type': 'int', 'default': 0, 'label': 'Shift end by minutes', 'sinput': False}, {'mql': 'InpSessionStartColor', 'py': 'InpSessionStartColor', 'param': None, 'type': 'color', 'default': 668170, 'label': 'Start of session', 'sinput': False}, {'mql': 'InpSessionStartColorBright', 'py': 'InpSessionStartColorBright', 'param': None, 'type': 'color', 'default': 1336340, 'label': 'Start of session bright', 'sinput': False}, {'mql': 'InpSessionEndColor', 'py': 'InpSessionEndColor', 'param': None, 'type': 'color', 'default': 657970, 'label': 'End of session', 'sinput': False}, {'mql': 'InpSessionEndColorBright', 'py': 'InpSessionEndColorBright', 'param': None, 'type': 'color', 'default': 1315940, 'label': 'End of session bright', 'sinput': False}, {'mql': 'InpShowDailySeparator', 'py': 'InpShowDailySeparator', 'param': 'InpShowDailySeparator', 'type': 'bool', 'default': True, 'label': 'Show separator between days', 'sinput': False}, {'mql': 'InpMaxTF_Daily', 'py': 'InpMaxTF_Daily', 'param': 'InpMaxTF_Daily', 'type': 'int', 'default': 16388, 'label': 'Show day separator up to timeframe', 'sinput': False}, {'mql': 'InpDailyColor', 'py': 'InpDailyColor', 'param': None, 'type': 'color', 'default': 4333824, 'label': 'New day', 'sinput': False}, {'mql': 'InpDailyColorBright', 'py': 'InpDailyColorBright', 'param': None, 'type': 'color', 'default': 8667648, 'label': 'New day bright', 'sinput': False}, {'mql': 'InpShowWeeklySeparator', 'py': 'InpShowWeeklySeparator', 'param': 'InpShowWeeklySeparator', 'type': 'bool', 'default': True, 'label': 'Show separator between weeks', 'sinput': False}, {'mql': 'InpMaxTF_Weekly', 'py': 'InpMaxTF_Weekly', 'param': 'InpMaxTF_Weekly', 'type': 'int', 'default': 16396, 'label': 'Show week separator up to timeframe', 'sinput': False}, {'mql': 'InpWeeklyColor', 'py': 'InpWeeklyColor', 'param': None, 'type': 'color', 'default': 4325442, 'label': 'New week', 'sinput': False}, {'mql': 'InpWeeklyColorBright', 'py': 'InpWeeklyColorBright', 'param': None, 'type': 'color', 'default': 8650884, 'label': 'New week bright', 'sinput': False}, {'mql': 'InpShowMonthlySeparator', 'py': 'InpShowMonthlySeparator', 'param': 'InpShowMonthlySeparator', 'type': 'bool', 'default': True, 'label': 'Show separator between months', 'sinput': False}, {'mql': 'InpMaxTF_Monthly', 'py': 'InpMaxTF_Monthly', 'param': 'InpMaxTF_Monthly', 'type': 'int', 'default': 16408, 'label': 'Show month separator up to timeframe', 'sinput': False}, {'mql': 'InpMonthlyColor', 'py': 'InpMonthlyColor', 'param': None, 'type': 'color', 'default': 16962, 'label': 'New month', 'sinput': False}, {'mql': 'InpMonthlyColorBright', 'py': 'InpMonthlyColorBright', 'param': None, 'type': 'color', 'default': 33924, 'label': 'New month bright', 'sinput': False}, {'mql': 'InpShowYearlySeparator', 'py': 'InpShowYearlySeparator', 'param': 'InpShowYearlySeparator', 'type': 'bool', 'default': True, 'label': 'Show separator between years', 'sinput': False}, {'mql': 'InpYearlyColor', 'py': 'InpYearlyColor', 'param': None, 'type': 'color', 'default': 8514, 'label': 'New year', 'sinput': False}, {'mql': 'InpYearlyColorBright', 'py': 'InpYearlyColorBright', 'param': None, 'type': 'color', 'default': 17028, 'label': 'New year bright', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMaxBars = _input('InpMaxBars', 2500)  # Show separators for # bars (0=ALL)
InpUseBrightColors = _input('InpUseBrightColors', True)  # Use bright colors
InpDrawAsBackground = _input('InpDrawAsBackground', True)  # Draw lines as background
InpShowSessionSeparator = _input('InpShowSessionSeparator', True)  # Show separator for session start/end
InpMaxTF_Session = _input('InpMaxTF_Session', PERIOD_M30)  # Show session separator up to timeframe
InpSessionStartTime = _input('InpSessionStartTime', 9)  # Start hour of session (0-23)
InpShiftStartMins = _input('InpShiftStartMins', 0)  # Shift start by minutes
InpSessionEndTime = _input('InpSessionEndTime', 18)  # End hour of session (0-23)
InpShiftEndMins = _input('InpShiftEndMins', 0)  # Shift end by minutes
InpSessionStartColor = _input('InpSessionStartColor', 0x0A320A)  # Start of session
InpSessionStartColorBright = _input('InpSessionStartColorBright', 0x146414)  # Start of session bright
InpSessionEndColor = _input('InpSessionEndColor', 0x0A0A32)  # End of session
InpSessionEndColorBright = _input('InpSessionEndColorBright', 0x141464)  # End of session bright
InpShowDailySeparator = _input('InpShowDailySeparator', True)  # Show separator between days
InpMaxTF_Daily = _input('InpMaxTF_Daily', PERIOD_H4)  # Show day separator up to timeframe
InpDailyColor = _input('InpDailyColor', 0x422100)  # New day
InpDailyColorBright = _input('InpDailyColorBright', 0x844200)  # New day bright
InpShowWeeklySeparator = _input('InpShowWeeklySeparator', True)  # Show separator between weeks
InpMaxTF_Weekly = _input('InpMaxTF_Weekly', PERIOD_H12)  # Show week separator up to timeframe
InpWeeklyColor = _input('InpWeeklyColor', 0x420042)  # New week
InpWeeklyColorBright = _input('InpWeeklyColorBright', 0x840084)  # New week bright
InpShowMonthlySeparator = _input('InpShowMonthlySeparator', True)  # Show separator between months
InpMaxTF_Monthly = _input('InpMaxTF_Monthly', PERIOD_D1)  # Show month separator up to timeframe
InpMonthlyColor = _input('InpMonthlyColor', 0x004242)  # New month
InpMonthlyColorBright = _input('InpMonthlyColorBright', 0x008484)  # New month bright
InpShowYearlySeparator = _input('InpShowYearlySeparator', True)  # Show separator between years
InpYearlyColor = _input('InpYearlyColor', 0x002142)  # New year
InpYearlyColorBright = _input('InpYearlyColorBright', 0x004284)  # New year bright
sessionStartTime = 0  # start/end of session
sessionEndTime = 0  # start/end of session
extendedSessionStartTime = 0  # datetime for extended start of session separator
extendedSessionEndTime = 0  # datetime for extended end of session separator
extendedNewDayTime = 0  # datetime for extended new day separator
sessionStartCol = 0  # colors for session start/end
sessionEndCol = 0  # colors for session start/end
dailyCol = 0  # color for daily/weekly separator
weeklyCol = 0  # color for daily/weekly separator
monthlyCol = 0  # colors for monthly/yearly separator
yearlyCol = 0  # colors for monthly/yearly separator
oneDay = 86400  # seconds in a day: 60*60*24
drawingStyle = 0  # drawing style for daily/weekly/monthly/yearly separators

def DeleteObjects():
    f_TotalObjects = ObjectsTotal(0, 0, OBJ_VLINE)
    for i in range(f_TotalObjects - 1, 0 - 1, -1):
        f_ObjName = ObjectName(0, i, 0, OBJ_VLINE)
        if ((((StringFind(f_ObjName, 'objNewDay_', 0) >= 0 or StringFind(f_ObjName, 'objNewWeek_', 0) >= 0) or StringFind(f_ObjName, 'objNewMonth_', 0) >= 0) or StringFind(f_ObjName, 'objNewYear_', 0) >= 0) or StringFind(f_ObjName, 'objSessionStart_', 0) >= 0) or StringFind(f_ObjName, 'objSessionEnd_', 0) >= 0:
            ObjectDelete(0, f_ObjName)
    ChartRedraw(0)

def CreateSeparatorObj(f_ObjName, f_Time, f_ObjColor, f_LineStyle, f_LineWidth):
    ObjectDelete(0, f_ObjName)
    ObjectCreate(0, f_ObjName, OBJ_VLINE, 0, f_Time, 0)
    ObjectSetInteger(0, f_ObjName, OBJPROP_BACK, InpDrawAsBackground)
    ObjectSetInteger(0, f_ObjName, OBJPROP_COLOR, f_ObjColor)
    ObjectSetInteger(0, f_ObjName, OBJPROP_STYLE, f_LineStyle)
    ObjectSetInteger(0, f_ObjName, OBJPROP_WIDTH, f_LineWidth)

def DayOfWeekString(f_dayofweek):
    _sw1 = f_dayofweek
    if _sw1 == 0:
        return 'SUN'
    elif _sw1 == 1:
        return 'MON'
    elif _sw1 == 2:
        return 'TUE'
    elif _sw1 == 3:
        return 'WED'
    elif _sw1 == 4:
        return 'THU'
    elif _sw1 == 5:
        return 'FRI'
    elif _sw1 == 6:
        return 'SAT'
    else:
        return ''

def OnInit():
    global dailyCol, drawingStyle, extendedNewDayTime, extendedSessionEndTime, extendedSessionStartTime, monthlyCol, sessionEndCol, sessionEndTime, sessionStartCol, sessionStartTime, weeklyCol, yearlyCol
    IndicatorSetString(INDICATOR_SHORTNAME, 'Period Separator')
    sessionStartTime = InpSessionStartTime
    if InpSessionStartTime < 0:
        sessionStartTime = 1
    if InpSessionStartTime > 23:
        sessionStartTime = 23
    sessionEndTime = InpSessionEndTime
    if InpSessionEndTime < 0:
        sessionEndTime = 1
    if InpSessionEndTime > 23:
        sessionEndTime = 23
    extendedSessionStartTime = 0
    extendedSessionEndTime = 0
    extendedNewDayTime = 0
    if InpUseBrightColors == False:
        sessionStartCol = InpSessionStartColor
        sessionEndCol = InpSessionEndColor
        dailyCol = InpDailyColor
        weeklyCol = InpWeeklyColor
        monthlyCol = InpMonthlyColor
        yearlyCol = InpYearlyColor
    else:
        sessionStartCol = InpSessionStartColorBright
        sessionEndCol = InpSessionEndColorBright
        dailyCol = InpDailyColorBright
        weeklyCol = InpWeeklyColorBright
        monthlyCol = InpMonthlyColorBright
        yearlyCol = InpYearlyColorBright
    if Period() <= InpMaxTF_Session and InpShowSessionSeparator == True:
        drawingStyle = STYLE_DASH
    else:
        drawingStyle = STYLE_DOT

def OnDeinit(reason):
    DeleteObjects()

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global extendedNewDayTime, extendedSessionEndTime, extendedSessionStartTime
    ArraySetAsSeries(Time, True)
    if rates_total < 100:
        return 0
    maxBars = InpMaxBars
    if maxBars >= rates_total or maxBars < 0:
        maxBars = rates_total - 2
    limit = 0
    if (prev_calculated == 0 or prev_calculated < 0) or prev_calculated > rates_total:
        if maxBars == 0:
            limit = rates_total - 2
        if maxBars > 0:
            limit = maxBars
    else:
        limit = rates_total - prev_calculated
    for i in range(limit, 0 - 1, -1):
        timeStruct = MqlDateTime()
        timeStruct_prev = MqlDateTime()
        TimeToStruct(Time[i], timeStruct)
        TimeToStruct(Time[i + 1], timeStruct_prev)
        today_int = timeStruct.day_of_week
        today_str = DayOfWeekString(today_int)
        curdate_str = TimeToString(Time[i], TIME_DATE)
        curdate_datetime = StringToTime(curdate_str)
        if InpShowSessionSeparator == True and Period() <= InpMaxTF_Session:
            if timeStruct.hour == sessionStartTime and timeStruct_prev.hour != sessionStartTime:
                CreateSeparatorObj('objSessionStart_' + _str(rates_total - i), Time[i] + (InpShiftStartMins * 60), sessionStartCol, STYLE_DOT, 0)
            if i == 0 and Time[i] >= extendedSessionStartTime:
                extendedSessionStartTime = curdate_datetime + (sessionStartTime * 3600) + (InpShiftStartMins * 60)
                if timeStruct.hour >= sessionStartTime:
                    extendedSessionStartTime += oneDay
                CreateSeparatorObj('objSessionStart_Extended', extendedSessionStartTime, sessionStartCol, STYLE_DOT, 0)
        if InpShowSessionSeparator == True and Period() <= InpMaxTF_Session:
            if timeStruct.hour == sessionEndTime and timeStruct_prev.hour != sessionEndTime:
                CreateSeparatorObj('objSessionEnd_' + _str(rates_total - i), Time[i] + (InpShiftEndMins * 60), sessionEndCol, STYLE_DOT, 0)
            if i == 0 and Time[i] >= extendedSessionEndTime:
                extendedSessionEndTime = curdate_datetime + (sessionEndTime * 3600) + (InpShiftEndMins * 60)
                if timeStruct.hour >= sessionEndTime:
                    extendedSessionEndTime += oneDay
                CreateSeparatorObj('objSessionEnd_Extended', extendedSessionEndTime, sessionEndCol, STYLE_DOT, 0)
        if InpShowYearlySeparator == True and timeStruct.year != timeStruct_prev.year:
            CreateSeparatorObj('objNewYear_' + today_str + '_' + _str(rates_total - i), Time[i], yearlyCol, drawingStyle, 0)
            continue
        if (InpShowMonthlySeparator == True and Period() <= InpMaxTF_Monthly) and timeStruct.mon != timeStruct_prev.mon:
            CreateSeparatorObj('objNewMonth_' + today_str + '_' + _str(rates_total - i), Time[i], monthlyCol, drawingStyle, 0)
            continue
        if ((InpShowWeeklySeparator == True and Period() <= InpMaxTF_Weekly) and timeStruct.day_of_week != 5) and timeStruct_prev.day_of_week == 5:
            CreateSeparatorObj('objNewWeek_' + today_str + '_' + _str(rates_total - i), Time[i], weeklyCol, drawingStyle, 0)
            continue
        if InpShowDailySeparator == True and Period() <= InpMaxTF_Daily:
            if timeStruct.day_of_year != timeStruct_prev.day_of_year:
                CreateSeparatorObj('objNewDay_' + today_str + '_' + _str(rates_total - i), Time[i], dailyCol, drawingStyle, 0)
            if i == 0 and Time[i] >= extendedNewDayTime:
                extendedNewDayTime = curdate_datetime + oneDay
                CreateSeparatorObj('objNewDay_Extended', extendedNewDayTime, dailyCol, drawingStyle, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ClearviewPeriodseparator(_MQL5Indicator):
    name = 'clearview_periodseparator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMaxBars': 2500,  # Show separators for # bars (0=ALL)
        'InpUseBrightColors': True,  # Use bright colors
        'InpDrawAsBackground': True,  # Draw lines as background
        'InpShowSessionSeparator': True,  # Show separator for session start/end
        'InpMaxTF_Session': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # Show session separator up to timeframe
        'InpSessionStartTime': 9,  # Start hour of session (0-23)
        'InpShiftStartMins': 0,  # Shift start by minutes
        'InpSessionEndTime': 18,  # End hour of session (0-23)
        'InpShiftEndMins': 0,  # Shift end by minutes
        'InpShowDailySeparator': True,  # Show separator between days
        'InpMaxTF_Daily': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Show day separator up to timeframe
        'InpShowWeeklySeparator': True,  # Show separator between weeks
        'InpMaxTF_Weekly': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # Show week separator up to timeframe
        'InpShowMonthlySeparator': True,  # Show separator between months
        'InpMaxTF_Monthly': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Show month separator up to timeframe
        'InpShowYearlySeparator': True,  # Show separator between years
    }

