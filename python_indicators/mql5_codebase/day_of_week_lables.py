"""Day_Of_Week_Lables — converted from MQL5: MQL5 Indicators/Day_Of_Week_Lables/Day_Of_Week_Lables.mq5

Day of week indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Day of week indicator'], 'name': 'Day_Of_Week_Lables', 'source': 'MQL5 Indicators/Day_Of_Week_Lables/Day_Of_Week_Lables.mq5', 'folder': 'Day_Of_Week_Lables', 'inputs': [{'mql': 'InpHoursOffset', 'py': 'InpHoursOffset', 'param': 'InpHoursOffset', 'type': 'uint', 'default': 0, 'label': 'Hours offset', 'sinput': False}, {'mql': 'InpShowDaysDate', 'py': 'InpShowDaysDate', 'param': 'InpShowDaysDate', 'type': 'int', 'default': 1, 'label': 'Show days numbers', 'sinput': False}, {'mql': 'InpDayLabelColor', 'py': 'InpDayLabelColor', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Day label color', 'sinput': False}, {'mql': 'InpDayLabelSize', 'py': 'InpDayLabelSize', 'param': 'InpDayLabelSize', 'type': 'uchar', 'default': 8, 'label': 'Day label font size', 'sinput': False}, {'mql': 'InpDayLabelFont', 'py': 'InpDayLabelFont', 'param': None, 'type': 'string', 'default': 'Calibri', 'label': 'Day label font name', 'sinput': False}, {'mql': 'InpDaySepColor', 'py': 'InpDaySepColor', 'param': None, 'type': 'color', 'default': 11119017, 'label': 'Day dividing lines color', 'sinput': False}, {'mql': 'InpDaySepStyle', 'py': 'InpDaySepStyle', 'param': 'InpDaySepStyle', 'type': 'int', 'default': 2, 'label': 'Day dividing lines style', 'sinput': False}, {'mql': 'InpDaySepWidth', 'py': 'InpDaySepWidth', 'param': 'InpDaySepWidth', 'type': 'uchar', 'default': 1, 'label': 'Day dividing lines width', 'sinput': False}, {'mql': 'InpDaySepDate', 'py': 'InpDaySepDate', 'param': 'InpDaySepDate', 'type': 'int', 'default': 0, 'label': 'Show day dividing lines date field', 'sinput': False}, {'mql': 'InpMonthLabelColor', 'py': 'InpMonthLabelColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Month label color', 'sinput': False}, {'mql': 'InpMonthLabelSize', 'py': 'InpMonthLabelSize', 'param': 'InpMonthLabelSize', 'type': 'uchar', 'default': 10, 'label': 'Month label font size', 'sinput': False}, {'mql': 'InpMonthLabelFont', 'py': 'InpMonthLabelFont', 'param': None, 'type': 'string', 'default': 'Calibri', 'label': 'Month label font name', 'sinput': False}, {'mql': 'InpMonthSepColor', 'py': 'InpMonthSepColor', 'param': None, 'type': 'color', 'default': 36095, 'label': 'Month dividing lines color', 'sinput': False}, {'mql': 'InpMonthSepStyle', 'py': 'InpMonthSepStyle', 'param': 'InpMonthSepStyle', 'type': 'int', 'default': 0, 'label': 'Month dividing lines style', 'sinput': False}, {'mql': 'InpMonthSepWidth', 'py': 'InpMonthSepWidth', 'param': 'InpMonthSepWidth', 'type': 'uchar', 'default': 2, 'label': 'Month dividing lines width', 'sinput': False}, {'mql': 'InpMonthSepDate', 'py': 'InpMonthSepDate', 'param': 'InpMonthSepDate', 'type': 'int', 'default': 1, 'label': 'Show month dividing lines date field', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpHoursOffset = _input('InpHoursOffset', 0)  # Hours offset
InpShowDaysDate = _input('InpShowDaysDate', INPUT_YES)  # Show days numbers
InpDayLabelColor = _input('InpDayLabelColor', clrGreen)  # Day label color
InpDayLabelSize = _input('InpDayLabelSize', 8)  # Day label font size
InpDayLabelFont = _input('InpDayLabelFont', 'Calibri')  # Day label font name
InpDaySepColor = _input('InpDaySepColor', clrDarkGray)  # Day dividing lines color
InpDaySepStyle = _input('InpDaySepStyle', STYLE_DOT)  # Day dividing lines style
InpDaySepWidth = _input('InpDaySepWidth', 1)  # Day dividing lines width
InpDaySepDate = _input('InpDaySepDate', INPUT_NO)  # Show day dividing lines date field
InpMonthLabelColor = _input('InpMonthLabelColor', clrRed)  # Month label color
InpMonthLabelSize = _input('InpMonthLabelSize', 10)  # Month label font size
InpMonthLabelFont = _input('InpMonthLabelFont', 'Calibri')  # Month label font name
InpMonthSepColor = _input('InpMonthSepColor', clrDarkOrange)  # Month dividing lines color
InpMonthSepStyle = _input('InpMonthSepStyle', STYLE_SOLID)  # Month dividing lines style
InpMonthSepWidth = _input('InpMonthSepWidth', 2)  # Month dividing lines width
InpMonthSepDate = _input('InpMonthSepDate', INPUT_YES)  # Show month dividing lines date field
prefix = ""
days = Arr(7, "", dyn=False)
month = Arr(12, "", dyn=False)
day_date = ""
hour_offset = 0

def OnInit():
    global hour_offset, prefix
    EventSetTimer(90)
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    hour_offset = (23 if (InpHoursOffset > 23) else InpHoursOffset)
    days[0] = TextByLanguage('Воскресение', 'Sunday')
    days[1] = TextByLanguage('Понедельник', 'Monday')
    days[2] = TextByLanguage('Вторник', 'Tuesday')
    days[3] = TextByLanguage('Среда', 'Wednesday')
    days[4] = TextByLanguage('Четверг', 'Thursday')
    days[5] = TextByLanguage('Пятница', 'Friday')
    days[6] = TextByLanguage('Суббота', 'Saturday')
    month[0] = TextByLanguage('Январь', 'January')
    month[1] = TextByLanguage('Февраль', 'February')
    month[2] = TextByLanguage('Март', 'March')
    month[3] = TextByLanguage('Апрель', 'April')
    month[4] = TextByLanguage('Май', 'May')
    month[5] = TextByLanguage('Июнь', 'June')
    month[6] = TextByLanguage('Июль', 'July')
    month[7] = TextByLanguage('Август', 'August')
    month[8] = TextByLanguage('Сентябрь', 'September')
    month[9] = TextByLanguage('Октябрь', 'October')
    month[10] = TextByLanguage('Ноябрь', 'November')
    month[11] = TextByLanguage('Декабрь', 'December')
    IndicatorSetString(INDICATOR_SHORTNAME, 'Day of week')
    iTime(None, PERIOD_D1, 1)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)
    ChartRedraw()

def OnTimer():
    iTime(None, PERIOD_D1, 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_month, day_date
    ArraySetAsSeries(time, True)
    if rates_total < 4 or (not IsTimeframeDataReady(PERIOD_D1)):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
    day_date = ''
    for i in range(limit, 0 - 1, -1):
        if TimeHour_u(time[i]) == hour_offset:
            day_date = (IntegerToString(TimeDay_u(time[i]), 2, 48) if InpShowDaysDate else '')
            Separator(prefix + 'day_sep_' + _str(i), time[i], InpDaySepColor, InpDaySepWidth, InpDaySepStyle, (InpDaySepDate != 0))
            ObjectMakeText(prefix + 'day_' + _str(i), time[i] + _idiv(PeriodSeconds(PERIOD_D1), 2), iHigh(None, PERIOD_D1, iBarShift(None, PERIOD_D1, time[i])) + (20 * Point()), days[TimeDayOfWeek_u(time[i])] + ' ' + day_date, InpDayLabelColor, InpDayLabelFont, InpDayLabelSize)
            cur_month = TimeMonth_u(time[i])
            if cur_month != _s_OnCalculate_last_month:
                Separator(prefix + 'month_sep' + _str(i), time[i], InpMonthSepColor, InpMonthSepWidth, InpMonthSepStyle, (InpMonthSepDate != 0))
                ObjectMakeText(prefix + 'month_' + _str(i), time[i] + _idiv(PeriodSeconds(PERIOD_D1), 2), iLow(None, PERIOD_D1, iBarShift(None, PERIOD_D1, time[i])) + (30 * Point()), month[TimeMonth_u(time[i]) - 1], InpMonthLabelColor, InpMonthLabelFont, InpMonthLabelSize)
                _s_OnCalculate_last_month = cur_month
    return rates_total

def Separator(name, time, clr, width, style, date=False):
    if ObjectFind(0, name) < 1:
        ObjectCreate(0, name, OBJ_VLINE, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, name, OBJPROP_STYLE, style)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(0, name, OBJPROP_RAY, date)

def ObjectMakeText(name, time, price, text, clr, font='Calibri', size=8):
    if ObjectFind(0, name) < 1:
        ObjectCreate(0, name, OBJ_TEXT, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_CENTER)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetString(0, name, OBJPROP_FONT, font)
    return

def TimeDay_u(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    return tm.day

def TimeDayOfWeek_u(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    return tm.day_of_week

def TimeMonth_u(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    return tm.mon

def TimeHour_u(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    return tm.hour

def TextByLanguage(text_ru, text_en):
    return (text_ru if (TerminalInfoString(TERMINAL_LANGUAGE) == 'Russian') else text_en)

def IsTimeframeDataReady(timeframe):
    ResetLastError()
    iTime(None, timeframe, 1)
    return GetLastError() == ERR_SUCCESS

# ---- static local variables
_s_OnCalculate_last_month = WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DayOfWeekLables(_MQL5Indicator):
    name = 'Day_Of_Week_Lables'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpHoursOffset': 0,  # Hours offset
        'InpShowDaysDate': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show days numbers
        'InpDayLabelSize': 8,  # Day label font size
        'InpDaySepStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Day dividing lines style
        'InpDaySepWidth': 1,  # Day dividing lines width
        'InpDaySepDate': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show day dividing lines date field
        'InpMonthLabelSize': 10,  # Month label font size
        'InpMonthSepStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Month dividing lines style
        'InpMonthSepWidth': 2,  # Month dividing lines width
        'InpMonthSepDate': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show month dividing lines date field
    }

