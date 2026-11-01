"""timezones — converted from MQL5: MQL5 Indicators/TimeZones/timezones.mq5

Copyright: Copyright © 2005. Alejandro Galindo; Link: http://elCactus.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005. Alejandro Galindo', 'link': 'http://elCactus.com', 'version': '1.00', 'indicator_buffers': 0, 'indicator_plots': 0, 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [''], 'name': 'timezones', 'source': 'MQL5 Indicators/TimeZones/timezones.mq5', 'folder': 'TimeZones', 'inputs': [{'mql': 'LinesSirname', 'py': 'LinesSirname', 'param': None, 'type': 'string', 'default': 'TimeZones', 'label': 'Line name', 'sinput': False}, {'mql': 'WeeklyTotal', 'py': 'WeeklyTotal', 'param': 'WeeklyTotal', 'type': 'uint', 'default': 4, 'label': 'Number of weeks in the history for indexing', 'sinput': False}, {'mql': 'FutureTotal', 'py': 'FutureTotal', 'param': 'FutureTotal', 'type': 'uint', 'default': 1, 'label': 'Number of lines in future for indexing', 'sinput': False}, {'mql': 'Line_Color_D', 'py': 'Line_Color_D', 'param': None, 'type': 'color', 'default': 255, 'label': 'Day line color', 'sinput': False}, {'mql': 'Line_Style_D', 'py': 'Line_Style_D', 'param': 'Line_Style_D', 'type': 'int', 'default': 0, 'label': 'Day line display style', 'sinput': False}, {'mql': 'Line_Width_D', 'py': 'Line_Width_D', 'param': 'Line_Width_D', 'type': 'int', 'default': 3, 'label': 'Day line width', 'sinput': False}, {'mql': 'SetBackground_D', 'py': 'SetBackground_D', 'param': 'SetBackground_D', 'type': 'bool', 'default': True, 'label': 'Background display of day lines', 'sinput': False}, {'mql': 'GMT', 'py': 'GMT', 'param': 'GMT', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'Line_Color_D1', 'py': 'Line_Color_D1', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'GMT line color', 'sinput': False}, {'mql': 'Line_Style_D1', 'py': 'Line_Style_D1', 'param': 'Line_Style_D1', 'type': 'int', 'default': 0, 'label': 'GMT line style', 'sinput': False}, {'mql': 'Line_Width_D1', 'py': 'Line_Width_D1', 'param': 'Line_Width_D1', 'type': 'int', 'default': 2, 'label': 'GMT line width', 'sinput': False}, {'mql': 'SetBackground_D1', 'py': 'SetBackground_D1', 'param': 'SetBackground_D1', 'type': 'bool', 'default': True, 'label': 'Background display of the GMT line', 'sinput': False}, {'mql': 'MST', 'py': 'MST', 'param': 'MST', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'Line_Color_D2', 'py': 'Line_Color_D2', 'param': None, 'type': 'color', 'default': 65280, 'label': 'MST line color', 'sinput': False}, {'mql': 'Line_Style_D2', 'py': 'Line_Style_D2', 'param': 'Line_Style_D2', 'type': 'int', 'default': 0, 'label': 'MST line style', 'sinput': False}, {'mql': 'Line_Width_D2', 'py': 'Line_Width_D2', 'param': 'Line_Width_D2', 'type': 'int', 'default': 2, 'label': 'MST line width', 'sinput': False}, {'mql': 'SetBackground_D2', 'py': 'SetBackground_D2', 'param': 'SetBackground_D2', 'type': 'bool', 'default': True, 'label': 'Background display of the MST line', 'sinput': False}, {'mql': 'EST', 'py': 'EST', 'param': 'EST', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'Line_Color_D3', 'py': 'Line_Color_D3', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'EST line color', 'sinput': False}, {'mql': 'Line_Style_D3', 'py': 'Line_Style_D3', 'param': 'Line_Style_D3', 'type': 'int', 'default': 0, 'label': 'EST line style', 'sinput': False}, {'mql': 'Line_Width_D3', 'py': 'Line_Width_D3', 'param': 'Line_Width_D3', 'type': 'int', 'default': 2, 'label': 'EST line width', 'sinput': False}, {'mql': 'SetBackground_D3', 'py': 'SetBackground_D3', 'param': 'SetBackground_D3', 'type': 'bool', 'default': True, 'label': 'Background display of the EST line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# enum Hour
H00 = 0
H01 = 1
H02 = 2
H03 = 3
H04 = 4
H05 = 5
H06 = 6
H07 = 7
H08 = 8
H09 = 9
H10 = 10
H11 = 11
H12 = 12
H13 = 13
H14 = 14
H15 = 15
H16 = 16
H17 = 17
H18 = 18
H19 = 19
H20 = 20
H21 = 21
H22 = 22
H23 = 23
_enum('Hour', {0: 'H00', 1: 'H01', 2: 'H02', 3: 'H03', 4: 'H04', 5: 'H05', 6: 'H06', 7: 'H07', 8: 'H08', 9: 'H09', 10: 'H10', 11: 'H11', 12: 'H12', 13: 'H13', 14: 'H14', 15: 'H15', 16: 'H16', 17: 'H17', 18: 'H18', 19: 'H19', 20: 'H20', 21: 'H21', 22: 'H22', 23: 'H23'})

# ---- inputs and global variables
LinesSirname = _input('LinesSirname', 'TimeZones')  # Line name
WeeklyTotal = _input('WeeklyTotal', 4)  # Number of weeks in the history for indexing
FutureTotal = _input('FutureTotal', 1)  # Number of lines in future for indexing
Line_Color_D = _input('Line_Color_D', clrRed)  # Day line color
Line_Style_D = _input('Line_Style_D', SOLID_)  # Day line display style
Line_Width_D = _input('Line_Width_D', w_3)  # Day line width
SetBackground_D = _input('SetBackground_D', True)  # Background display of day lines
GMT = _input('GMT', H02)
Line_Color_D1 = _input('Line_Color_D1', clrDodgerBlue)  # GMT line color
Line_Style_D1 = _input('Line_Style_D1', SOLID_)  # GMT line style
Line_Width_D1 = _input('Line_Width_D1', w_2)  # GMT line width
SetBackground_D1 = _input('SetBackground_D1', True)  # Background display of the GMT line
MST = _input('MST', H06)
Line_Color_D2 = _input('Line_Color_D2', clrLime)  # MST line color
Line_Style_D2 = _input('Line_Style_D2', SOLID_)  # MST line style
Line_Width_D2 = _input('Line_Width_D2', w_2)  # MST line width
SetBackground_D2 = _input('SetBackground_D2', True)  # Background display of the MST line
EST = _input('EST', H07)
Line_Color_D3 = _input('Line_Color_D3', clrDarkOrchid)  # EST line color
Line_Style_D3 = _input('Line_Style_D3', SOLID_)  # EST line style
Line_Width_D3 = _input('Line_Width_D3', w_2)  # EST line width
SetBackground_D3 = _input('SetBackground_D3', True)  # Background display of the EST line
Count_W = Arr(0, 0)
Count_D0 = Arr(0, 0)
Count_D1 = Arr(0, 0)
Count_D2 = Arr(0, 0)
Count_D3 = Arr(0, 0)
VLineTime_W = Arr(0, 0)
VLineTime_D0 = Arr(0, 0)
VLineTime_D1 = Arr(0, 0)
VLineTime_D2 = Arr(0, 0)
VLineTime_D3 = Arr(0, 0)
WeeklyTotal_ = 0
LinesTotal_D_ = 0
LinesTotal_D = 0
FutureTotal_D = 0
Sirname_W = ""
Sirname_D = Arr(4, "", dyn=False)

class CRecount_ArrayZeroPos(MqlObject):
    _q_fields = ('m_count',)
    def __init__(self):
        self.m_count = 0
        self.m_count = 1
    def Recount_ArrayZeroPos(self, CoArr, Size):
        numb = 0
        Max1 = 0
        Max2 = 0
        Max2 = Size
        Max1 = Max2 - 1
        self.m_count -= 1
        if self.m_count < 0:
            self.m_count = Max1
        for iii in range(0, Max2):
            numb = iii + self.m_count
            if numb > Max1:
                numb -= Max2
            CoArr[iii] = numb

def CheckVLinePoint_D(bartime1, bartime0):
    tm0 = MqlDateTime()
    tm1 = MqlDateTime()
    TimeToStruct(bartime0, tm0)
    TimeToStruct(bartime1, tm1)
    if tm0.day_of_year != tm1.day_of_year:
        return True
    return False

def CheckVLinePoint_DN(bartime1, bartime0, hour):
    tm0 = MqlDateTime()
    tm1 = MqlDateTime()
    TimeToStruct(bartime0, tm0)
    TimeToStruct(bartime1, tm1)
    if tm1.hour != hour and tm0.hour == hour:
        return True
    if tm0.day_of_year != tm1.day_of_year and tm0.hour == hour:
        return True
    return False

def CheckVLinePoint_W(bar, bartime):
    tm = MqlDateTime()
    TimeToStruct(bartime, tm)
    if tm.day_of_week == 0 or tm.day_of_week == 6:
        return True
    return False

def RenameVline(chart_id, oldname, newname):
    if ObjectFind(chart_id, oldname) > 0:
        ObjectSetString(chart_id, oldname, OBJPROP_NAME, newname)
        return True
    return False

def CreateVline(chart_id, name, nwin, time1, Color, style, width, background, text):
    ObjectCreate(chart_id, name, OBJ_VLINE, nwin, time1, 999999999)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, background)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetVline(chart_id, name, nwin, time1, Color, style, width, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateVline(chart_id, name, nwin, time1, Color, style, width, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, 999999999)

def Deinit():
    total = ObjectsTotal(0, 0, -1) - 1
    name = ""
    sirname = ""
    for numb in range(total, 0 - 1, -1):
        name = ObjectName(0, numb, 0, -1)
        sirname = StringSubstr(name, 0, StringLen(LinesSirname))
        if sirname == LinesSirname:
            ObjectDelete(0, name)
    ChartRedraw(0)

def OnInit():
    global FutureTotal_D, LinesTotal_D, LinesTotal_D_, Sirname_W, WeeklyTotal_
    if Period() > PERIOD_H1:
        return
    Deinit()
    WeeklyTotal_ = WeeklyTotal + 1
    LinesTotal_D = WeeklyTotal_ * 4
    FutureTotal_D = FutureTotal
    LinesTotal_D_ = LinesTotal_D + FutureTotal_D
    Sirname_W = LinesSirname + '_W_'
    Sirname_D[0] = LinesSirname + '_D0_'
    Sirname_D[1] = LinesSirname + '_D1_'
    Sirname_D[2] = LinesSirname + '_D2_'
    Sirname_D[3] = LinesSirname + '_D3_'
    ArrayResize(Count_D0, LinesTotal_D_)
    ArrayResize(VLineTime_D0, LinesTotal_D_)
    ArrayResize(Count_D1, LinesTotal_D_)
    ArrayResize(VLineTime_D1, LinesTotal_D_)
    ArrayResize(Count_D2, LinesTotal_D_)
    ArrayResize(VLineTime_D2, LinesTotal_D_)
    ArrayResize(Count_D3, LinesTotal_D_)
    ArrayResize(VLineTime_D3, LinesTotal_D_)
    shortname = Box("")
    StringConcatenate(shortname, 'TimeZones(', LinesSirname, ', ', WeeklyTotal, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnDeinit(reason):
    Deinit()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Period() > PERIOD_H1:
        return 0
    if rates_total < 2:
        return 0
    if prev_calculated == rates_total:
        return rates_total
    Name = ""
    Time = 0
    TimeCur = 0
    limit = 0
    bar = 0
    ArrayInitialize(_s_OnCalculate_LastTime_D, 0)
    ArraySetAsSeries(time, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        VLineCount_W = 0
        bar = 0
        for bar in range(bar, limit + 1):
            if CheckVLinePoint_W(bar, _idiv(time[bar] + time[bar + 1], 2)):
                VLineCount_W += 1
                if VLineCount_W >= WeeklyTotal:
                    break
        else:
            bar = _range_end(bar, limit + 1, 1)
        if bar < limit:
            limit = bar
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if CheckVLinePoint_DN(time[bar + 1], time[bar], GMT):
            Name = Sirname_D[1] + TimeToString(time[bar])
            Time = VLineTime_D1[Count_D1[FutureTotal_D]]
            RenameVline(0, Sirname_D[1] + TimeToString(Time), Name)
            SetVline(0, Name, 0, time[bar], Line_Color_D1, Line_Style_D1, Line_Width_D1, SetBackground_D1, 'intraday GMT bar')
            VLineTime_D1[Count_D1[FutureTotal_D]] = time[bar]
            if bar > 0:
                _s_OnCalculate_D1.Recount_ArrayZeroPos(Count_D1, LinesTotal_D_)
            _s_OnCalculate_LastTime_D[1] = time[bar]
        if CheckVLinePoint_DN(time[bar + 1], time[bar], MST):
            Name = Sirname_D[2] + TimeToString(time[bar])
            Time = VLineTime_D2[Count_D2[FutureTotal_D]]
            RenameVline(0, Sirname_D[2] + TimeToString(Time), Name)
            SetVline(0, Name, 0, time[bar], Line_Color_D2, Line_Style_D2, Line_Width_D2, SetBackground_D2, 'intraday MST bar')
            VLineTime_D2[Count_D2[FutureTotal_D]] = time[bar]
            if bar > 0:
                _s_OnCalculate_D2.Recount_ArrayZeroPos(Count_D2, LinesTotal_D_)
            _s_OnCalculate_LastTime_D[2] = time[bar]
        if CheckVLinePoint_DN(time[bar + 1], time[bar], EST):
            Name = Sirname_D[3] + TimeToString(time[bar])
            Time = VLineTime_D3[Count_D3[FutureTotal_D]]
            RenameVline(0, Sirname_D[3] + TimeToString(Time), Name)
            SetVline(0, Name, 0, time[bar], Line_Color_D3, Line_Style_D3, Line_Width_D3, SetBackground_D3, 'intraday EST bar')
            VLineTime_D3[Count_D3[FutureTotal_D]] = time[bar]
            if bar > 0:
                _s_OnCalculate_D3.Recount_ArrayZeroPos(Count_D3, LinesTotal_D_)
            _s_OnCalculate_LastTime_D[3] = time[bar]
        if CheckVLinePoint_D(time[bar + 1], time[bar]):
            Name = Sirname_D[0] + TimeToString(time[bar])
            Time = VLineTime_D0[Count_D0[FutureTotal_D]]
            RenameVline(0, Sirname_D[0] + TimeToString(Time), Name)
            SetVline(0, Name, 0, time[bar], Line_Color_D, Line_Style_D, Line_Width_D, SetBackground_D, 'day bar')
            VLineTime_D0[Count_D0[FutureTotal_D]] = time[bar]
            if bar > 0:
                _s_OnCalculate_D0.Recount_ArrayZeroPos(Count_D0, LinesTotal_D_)
            _s_OnCalculate_LastTime_D[0] = time[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    TimeCur = TimeCurrent()
    for numb in range(_int(FutureTotal_D) - 1, 0 - 1, -1):
        Time = _s_OnCalculate_LastTime_D[1] + (86400 * (FutureTotal_D - numb))
        if TimeCur >= Time:
            Time += 86400
        if TimeCur >= Time:
            Time += 86400
        Name = Sirname_D[1] + TimeToString(Time)
        RenameVline(0, Sirname_D[1] + TimeToString(VLineTime_D1[Count_D1[numb]]), Name)
        SetVline(0, Name, 0, Time, Line_Color_D1, Line_Style_D1, Line_Width_D1, SetBackground_D1, 'intraday GMT bar')
        VLineTime_D1[Count_D1[numb]] = Time
        Time = _s_OnCalculate_LastTime_D[2] + (86400 * (FutureTotal_D - numb))
        if TimeCur >= Time:
            Time += 86400
        if TimeCur >= Time:
            Time += 86400
        Name = Sirname_D[2] + TimeToString(Time)
        RenameVline(0, Sirname_D[2] + TimeToString(VLineTime_D2[Count_D2[numb]]), Name)
        SetVline(0, Name, 0, Time, Line_Color_D2, Line_Style_D2, Line_Width_D2, SetBackground_D2, 'внутридневный бар MST')
        VLineTime_D2[Count_D2[numb]] = Time
        Time = _s_OnCalculate_LastTime_D[3] + (86400 * (FutureTotal_D - numb))
        if TimeCur >= Time:
            Time += 86400
        if TimeCur >= Time:
            Time += 86400
        Name = Sirname_D[3] + TimeToString(Time)
        RenameVline(0, Sirname_D[3] + TimeToString(VLineTime_D3[Count_D3[numb]]), Name)
        SetVline(0, Name, 0, Time, Line_Color_D3, Line_Style_D3, Line_Width_D3, SetBackground_D3, 'внутридневный бар EST')
        VLineTime_D3[Count_D2[numb]] = Time
        Time = _s_OnCalculate_LastTime_D[0] + (86400 * (FutureTotal_D - numb))
        if TimeCur >= Time:
            Time += 86400
        if TimeCur >= Time:
            Time += 86400
        Name = Sirname_D[0] + TimeToString(Time)
        RenameVline(0, Sirname_D[0] + TimeToString(VLineTime_D0[Count_D0[numb]]), Name)
        SetVline(0, Name, 0, Time, Line_Color_D, Line_Style_D, Line_Width_D, SetBackground_D, 'day bar')
        VLineTime_D0[Count_D0[numb]] = Time
    ChartRedraw(0)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastTime_D = Arr(4, 0, dyn=False)
_s_OnCalculate_D0 = CRecount_ArrayZeroPos()
_s_OnCalculate_D1 = CRecount_ArrayZeroPos()
_s_OnCalculate_D2 = CRecount_ArrayZeroPos()
_s_OnCalculate_D3 = CRecount_ArrayZeroPos()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Timezones(_MQL5Indicator):
    name = 'timezones'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WeeklyTotal': 4,  # Number of weeks in the history for indexing
        'FutureTotal': 1,  # Number of lines in future for indexing
        'Line_Style_D': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Day line display style
        'Line_Width_D': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Day line width
        'SetBackground_D': True,  # Background display of day lines
        'GMT': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=2),
        'Line_Style_D1': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # GMT line style
        'Line_Width_D1': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # GMT line width
        'SetBackground_D1': True,  # Background display of the GMT line
        'MST': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=6),
        'Line_Style_D2': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # MST line style
        'Line_Width_D2': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # MST line width
        'SetBackground_D2': True,  # Background display of the MST line
        'EST': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=7),
        'Line_Style_D3': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # EST line style
        'Line_Width_D3': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # EST line width
        'SetBackground_D3': True,  # Background display of the EST line
    }

