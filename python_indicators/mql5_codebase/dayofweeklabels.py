"""DayOfWeekLabels — converted from MQL5: MQL5 Indicators/DayOfWeekLabels/DayOfWeekLabels.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'DayOfWeekLabels', 'source': 'MQL5 Indicators/DayOfWeekLabels/DayOfWeekLabels.mq5', 'folder': 'DayOfWeekLabels', 'inputs': [{'mql': 'InpShowDay', 'py': 'InpShowDay', 'param': 'InpShowDay', 'type': 'int', 'default': 1, 'label': 'Show days', 'sinput': False}, {'mql': 'InpShowMon', 'py': 'InpShowMon', 'param': 'InpShowMon', 'type': 'int', 'default': 1, 'label': 'Show months', 'sinput': False}, {'mql': 'InpShowYear', 'py': 'InpShowYear', 'param': 'InpShowYear', 'type': 'int', 'default': 1, 'label': 'Show years', 'sinput': False}, {'mql': 'InpNameMon', 'py': 'InpNameMon', 'param': None, 'type': 'string', 'default': 'Monday', 'label': 'Name of Monday label', 'sinput': False}, {'mql': 'InpNameTue', 'py': 'InpNameTue', 'param': None, 'type': 'string', 'default': 'Tuesday', 'label': 'Name of Tuesday label', 'sinput': False}, {'mql': 'InpNameWed', 'py': 'InpNameWed', 'param': None, 'type': 'string', 'default': 'Wednesday', 'label': 'Name of Wednesday label', 'sinput': False}, {'mql': 'InpNameThu', 'py': 'InpNameThu', 'param': None, 'type': 'string', 'default': 'Thursday', 'label': 'Name of Thursday label', 'sinput': False}, {'mql': 'InpNameFri', 'py': 'InpNameFri', 'param': None, 'type': 'string', 'default': 'Friday', 'label': 'Name of Friday label', 'sinput': False}, {'mql': 'InpNameSat', 'py': 'InpNameSat', 'param': None, 'type': 'string', 'default': 'Saturday', 'label': 'Name of Saturday label', 'sinput': False}, {'mql': 'InpNameSun', 'py': 'InpNameSun', 'param': None, 'type': 'string', 'default': 'Sunday', 'label': 'Name of Sunday label', 'sinput': False}, {'mql': 'InpNameJan', 'py': 'InpNameJan', 'param': None, 'type': 'string', 'default': 'January', 'label': 'Name of January label', 'sinput': False}, {'mql': 'InpNameFeb', 'py': 'InpNameFeb', 'param': None, 'type': 'string', 'default': 'February', 'label': 'Name of February label', 'sinput': False}, {'mql': 'InpNameMar', 'py': 'InpNameMar', 'param': None, 'type': 'string', 'default': 'March', 'label': 'Name of March label', 'sinput': False}, {'mql': 'InpNameApr', 'py': 'InpNameApr', 'param': None, 'type': 'string', 'default': 'April', 'label': 'Name of April label', 'sinput': False}, {'mql': 'InpNameMay', 'py': 'InpNameMay', 'param': None, 'type': 'string', 'default': 'May', 'label': 'Name of May label', 'sinput': False}, {'mql': 'InpNameJun', 'py': 'InpNameJun', 'param': None, 'type': 'string', 'default': 'June', 'label': 'Name of June label', 'sinput': False}, {'mql': 'InpNameJul', 'py': 'InpNameJul', 'param': None, 'type': 'string', 'default': 'July', 'label': 'Name of July label', 'sinput': False}, {'mql': 'InpNameAug', 'py': 'InpNameAug', 'param': None, 'type': 'string', 'default': 'August', 'label': 'Name of August label', 'sinput': False}, {'mql': 'InpNameSep', 'py': 'InpNameSep', 'param': None, 'type': 'string', 'default': 'September', 'label': 'Name of September label', 'sinput': False}, {'mql': 'InpNameOct', 'py': 'InpNameOct', 'param': None, 'type': 'string', 'default': 'October', 'label': 'Name of October label', 'sinput': False}, {'mql': 'InpNameNov', 'py': 'InpNameNov', 'param': None, 'type': 'string', 'default': 'November', 'label': 'Name of November label', 'sinput': False}, {'mql': 'InpNameDec', 'py': 'InpNameDec', 'param': None, 'type': 'string', 'default': 'December', 'label': 'Name of December label', 'sinput': False}, {'mql': 'InpColorDayLine', 'py': 'InpColorDayLine', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Day line color', 'sinput': False}, {'mql': 'InpWidthDay', 'py': 'InpWidthDay', 'param': 'InpWidthDay', 'type': 'uint', 'default': 2, 'label': 'Day line width', 'sinput': False}, {'mql': 'InpColorDayLabel', 'py': 'InpColorDayLabel', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Day label color', 'sinput': False}, {'mql': 'InpFontSizeDay', 'py': 'InpFontSizeDay', 'param': 'InpFontSizeDay', 'type': 'uint', 'default': 8, 'label': 'Day label size', 'sinput': False}, {'mql': 'InpColorMonLine', 'py': 'InpColorMonLine', 'param': None, 'type': 'color', 'default': 3937500, 'label': 'Month line color', 'sinput': False}, {'mql': 'InpWidthMon', 'py': 'InpWidthMon', 'param': 'InpWidthMon', 'type': 'uint', 'default': 3, 'label': 'Month line width', 'sinput': False}, {'mql': 'InpColorMonLabel', 'py': 'InpColorMonLabel', 'param': None, 'type': 'color', 'default': 3937500, 'label': 'Month label color', 'sinput': False}, {'mql': 'InpFontSizeMon', 'py': 'InpFontSizeMon', 'param': 'InpFontSizeMon', 'type': 'uint', 'default': 10, 'label': 'Month label size', 'sinput': False}, {'mql': 'InpFontName', 'py': 'InpFontName', 'param': None, 'type': 'string', 'default': 'Calibri', 'label': 'Font name', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpShowDay = _input('InpShowDay', INPUT_YES)  # Show days
InpShowMon = _input('InpShowMon', INPUT_YES)  # Show months
InpShowYear = _input('InpShowYear', INPUT_YES)  # Show years
InpNameMon = _input('InpNameMon', 'Monday')  # Name of Monday label
InpNameTue = _input('InpNameTue', 'Tuesday')  # Name of Tuesday label
InpNameWed = _input('InpNameWed', 'Wednesday')  # Name of Wednesday label
InpNameThu = _input('InpNameThu', 'Thursday')  # Name of Thursday label
InpNameFri = _input('InpNameFri', 'Friday')  # Name of Friday label
InpNameSat = _input('InpNameSat', 'Saturday')  # Name of Saturday label
InpNameSun = _input('InpNameSun', 'Sunday')  # Name of Sunday label
InpNameJan = _input('InpNameJan', 'January')  # Name of January label
InpNameFeb = _input('InpNameFeb', 'February')  # Name of February label
InpNameMar = _input('InpNameMar', 'March')  # Name of March label
InpNameApr = _input('InpNameApr', 'April')  # Name of April label
InpNameMay = _input('InpNameMay', 'May')  # Name of May label
InpNameJun = _input('InpNameJun', 'June')  # Name of June label
InpNameJul = _input('InpNameJul', 'July')  # Name of July label
InpNameAug = _input('InpNameAug', 'August')  # Name of August label
InpNameSep = _input('InpNameSep', 'September')  # Name of September label
InpNameOct = _input('InpNameOct', 'October')  # Name of October label
InpNameNov = _input('InpNameNov', 'November')  # Name of November label
InpNameDec = _input('InpNameDec', 'December')  # Name of December label
InpColorDayLine = _input('InpColorDayLine', clrGreen)  # Day line color
InpWidthDay = _input('InpWidthDay', 2)  # Day line width
InpColorDayLabel = _input('InpColorDayLabel', clrGreen)  # Day label color
InpFontSizeDay = _input('InpFontSizeDay', 8)  # Day label size
InpColorMonLine = _input('InpColorMonLine', clrCrimson)  # Month line color
InpWidthMon = _input('InpWidthMon', 3)  # Month line width
InpColorMonLabel = _input('InpColorMonLabel', clrCrimson)  # Month label color
InpFontSizeMon = _input('InpFontSizeMon', 10)  # Month label size
InpFontName = _input('InpFontName', 'Calibri')  # Font name
BeginMinutes = 0
MondayNameH = ""
TuesdayNameH = ""
WednesdayNameH = ""
ThursdayNameH = ""
FridayNameH = ""
SaturdayNameH = ""
SundayNameH = ""
JanuaryNameH = ""
FebruaryNameH = ""
MarchNameH = ""
AprilNameH = ""
MayNameH = ""
JuneNameH = ""
JulyNameH = ""
AugustNameH = ""
SeptemberNameH = ""
OctoberNameH = ""
NovemberNameH = ""
DecemberNameH = ""
prefix = ""

def OnInit():
    global AprilNameH, AugustNameH, DecemberNameH, FebruaryNameH, FridayNameH, JanuaryNameH, JulyNameH, JuneNameH, MarchNameH, MayNameH, MondayNameH, NovemberNameH, OctoberNameH, SaturdayNameH, SeptemberNameH, SundayNameH, ThursdayNameH, TuesdayNameH, WednesdayNameH, prefix
    prefix = 'DayOW_'
    MondayNameH = GetName(InpNameMon)
    TuesdayNameH = GetName(InpNameTue)
    WednesdayNameH = GetName(InpNameWed)
    ThursdayNameH = GetName(InpNameThu)
    FridayNameH = GetName(InpNameFri)
    SaturdayNameH = GetName(InpNameSat)
    SundayNameH = GetName(InpNameSun)
    JanuaryNameH = GetName(InpNameJan)
    FebruaryNameH = GetName(InpNameFeb)
    MarchNameH = GetName(InpNameMar)
    AprilNameH = GetName(InpNameApr)
    MayNameH = GetName(InpNameMay)
    JuneNameH = GetName(InpNameJun)
    JulyNameH = GetName(InpNameJul)
    AugustNameH = GetName(InpNameAug)
    SeptemberNameH = GetName(InpNameSep)
    OctoberNameH = GetName(InpNameOct)
    NovemberNameH = GetName(InpNameNov)
    DecemberNameH = GetName(InpNameDec)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
    tm = MqlDateTime()
    tm_prev = MqlDateTime()
    name = ''
    tooltip = '\n'
    nm_dw = ''
    nm_dm = ''
    for i in range(limit, 0 - 1, -1):
        if not TimeToStruct(time[i], tm):
            continue
        if InpShowDay:
            day = tm.day
            day_prev = DayNumber(time[i + 1])
            if day != day_prev:
                name = prefix + TimeToString(time[i]) + 'L'
                nm_dw = NameDayOfWeek(tm.day_of_week)
                tooltip = TimeToString(time[i], TIME_DATE) + '\n' + nm_dw
                if CreateObject(name, OBJ_VLINE, InpColorDayLine):
                    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time[i])
                    ObjectSetInteger(0, name, OBJPROP_WIDTH, InpWidthDay)
                    ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip)
                name = prefix + TimeToString(time[i]) + 'T'
                if CreateObject(name, OBJ_TEXT, InpColorDayLabel):
                    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time[i])
                    ObjectSetDouble(0, name, OBJPROP_PRICE, high[i])
                    ObjectSetDouble(0, name, OBJPROP_ANGLE, 90)
                    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, InpFontSizeDay)
                    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
                    ObjectSetString(0, name, OBJPROP_FONT, InpFontName)
                    ObjectSetString(0, name, OBJPROP_TEXT, NameDayOfWeek(tm.day_of_week, True))
                    ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip)
        if InpShowMon:
            month = tm.mon
            month_prev = MonthNumber(time[i + 1])
            year = tm.year
            if month != month_prev:
                name = prefix + TimeToString(time[i]) + 'LM'
                nm_dm = NameOfMonth(month, year)
                tooltip = TimeToString(time[i], TIME_DATE) + '\n' + nm_dw + '\n' + nm_dm
                if CreateObject(name, OBJ_VLINE, InpColorMonLine):
                    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time[i])
                    ObjectSetInteger(0, name, OBJPROP_WIDTH, InpWidthMon)
                    ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip)
                name = prefix + TimeToString(time[i]) + 'TM'
                if CreateObject(name, OBJ_TEXT, InpColorMonLabel):
                    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time[i])
                    ObjectSetDouble(0, name, OBJPROP_PRICE, high[i])
                    ObjectSetDouble(0, name, OBJPROP_ANGLE, 90)
                    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, InpFontSizeMon)
                    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
                    ObjectSetString(0, name, OBJPROP_FONT, InpFontName)
                    ObjectSetString(0, name, OBJPROP_TEXT, nm_dm)
                    ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip)
    return rates_total

def CreateObject(name, object_type, object_color):
    if ObjectCreate(0, name, object_type, 0, 0, 0):
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, name, OBJPROP_COLOR, object_color)
        return True
    return False

def GetName(name):
    return name + GetHole(StringLen(name))

def GetHole(length):
    hole = ''
    for i in range(1, 2 * length + 1):
        hole += ' '
    return hole

def DayNumber(time):
    tm = MqlDateTime()
    day_number = WRONG_VALUE
    if TimeToStruct(time, tm):
        day_number = tm.day
    return day_number

def MonthNumber(time):
    tm = MqlDateTime()
    month_number = WRONG_VALUE
    if TimeToStruct(time, tm):
        month_number = tm.mon
    return month_number

def NameDayOfWeek(day_number, hole=False):
    return ((SundayNameH if hole else InpNameSun) if (day_number == 0) else (MondayNameH if hole else InpNameMon) if (day_number == 1) else (TuesdayNameH if hole else InpNameTue) if (day_number == 2) else (WednesdayNameH if hole else InpNameWed) if (day_number == 3) else (ThursdayNameH if hole else InpNameThu) if (day_number == 4) else (FridayNameH if hole else InpNameFri) if (day_number == 5) else SaturdayNameH)

def NameOfMonth(month_number, year_number):
    month_name = (JanuaryNameH if (month_number == 1) else FebruaryNameH if (month_number == 2) else MarchNameH if (month_number == 3) else AprilNameH if (month_number == 4) else MayNameH if (month_number == 5) else JuneNameH if (month_number == 6) else JulyNameH if (month_number == 7) else AugustNameH if (month_number == 8) else SeptemberNameH if (month_number == 9) else OctoberNameH if (month_number == 10) else NovemberNameH if (month_number == 11) else DecemberNameH)
    return ((_str(year_number) + ' ' + month_name) if InpShowYear else month_name)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DayOfWeekLabels(_MQL5Indicator):
    name = 'DayOfWeekLabels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpShowDay': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show days
        'InpShowMon': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show months
        'InpShowYear': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show years
        'InpWidthDay': 2,  # Day line width
        'InpFontSizeDay': 8,  # Day label size
        'InpWidthMon': 3,  # Month line width
        'InpFontSizeMon': 10,  # Month label size
    }

