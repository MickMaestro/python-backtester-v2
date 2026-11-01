"""vgridline_annual — converted from MQL5: MQL5 Indicators/VGridLine_Annual/vgridline_annual.mq5

Time grid mesh. Grid step - 1 year
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Time grid mesh. Grid step - 1 year'], 'name': 'vgridline_annual', 'source': 'MQL5 Indicators/VGridLine_Annual/vgridline_annual.mq5', 'folder': 'VGridLine_Annual', 'inputs': [{'mql': 'LinesSirname', 'py': 'LinesSirname', 'param': None, 'type': 'string', 'default': 'VLine_Grid_Annual_', 'label': 'Line name', 'sinput': False}, {'mql': 'Line_Color', 'py': 'Line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Line color', 'sinput': False}, {'mql': 'Line_Style', 'py': 'Line_Style', 'param': 'Line_Style', 'type': 'int', 'default': 0, 'label': 'Line display style', 'sinput': False}, {'mql': 'Line_Width', 'py': 'Line_Width', 'param': 'Line_Width', 'type': 'int', 'default': 1, 'label': 'Line width', 'sinput': False}, {'mql': 'SetBackground', 'py': 'SetBackground', 'param': 'SetBackground', 'type': 'bool', 'default': True, 'label': 'Lines background display', 'sinput': False}, {'mql': 'LinesTotal', 'py': 'LinesTotal', 'param': 'LinesTotal', 'type': 'uint', 'default': 10, 'label': 'Number of lines in history', 'sinput': False}, {'mql': 'FutureTotal', 'py': 'FutureTotal', 'param': 'FutureTotal', 'type': 'uint', 'default': 1, 'label': 'Number of lines in future empty history', 'sinput': False}, {'mql': 'Position', 'py': 'Position', 'param': 'Position', 'type': 'bool', 'default': True, 'label': 'Lines position (true - true position, false - matching with bars)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Orange = 0x00A5FF  # MQL4 colour name

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

# ---- inputs and global variables
LinesSirname = _input('LinesSirname', 'VLine_Grid_Annual_')  # Line name
Line_Style = _input('Line_Style', SOLID_)  # Line display style
Line_Width = _input('Line_Width', w_1)  # Line width
SetBackground = _input('SetBackground', True)  # Lines background display
LinesTotal = _input('LinesTotal', 10)  # Number of lines in history
FutureTotal = _input('FutureTotal', 1)  # Number of lines in future empty history
Position = _input('Position', True)  # Lines position (true - true position, false - matching with bars)
Count = Arr(0, 0)
VLineTime = Arr(0, 0)
LinesTotal_ = 0

def CheckVLinePoint(bar, lastyear, bartime):
    tm = MqlDateTime()
    TimeToStruct(bartime, tm)
    if tm.year != lastyear.v:
        lastyear.v = tm.year
        return True
    if Period() == PERIOD_W1:
        if bar > 0:
            TimeToStruct(bartime + PeriodSeconds() - 2, tm)
        else:
            TimeToStruct(TimeCurrent(), tm)
        if tm.year != lastyear.v:
            lastyear.v = tm.year
            return True
    return False

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

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

def SetVline(chart_id, name, nwin, time1, Color, style, width, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateVline(chart_id, name, nwin, time1, Color, style, width, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, 999999999)

def OnInit():
    global LinesTotal_
    Deinit()
    LinesTotal_ = LinesTotal + FutureTotal
    ArrayResize(Count, LinesTotal_)
    ArrayResize(VLineTime, LinesTotal_)
    shortname = Box("")
    StringConcatenate(shortname, 'VGridLine_Annual(', LinesSirname, ', ', LinesTotal, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

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

def OnDeinit(reason):
    Deinit()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastYear
    if rates_total < 2:
        return 0
    if prev_calculated == rates_total:
        return rates_total
    Name = ""
    Time = 0
    limit = 0
    bar = 0
    year = 0
    tm = MqlDateTime()
    TimeToStruct(TimeCurrent(), tm)
    if _s_OnCalculate_LastYear == tm.year:
        return rates_total
    ArraySetAsSeries(time, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        TimeToStruct(time[0], tm)
        _s_OnCalculate_LastYear = tm.year
        lastyear = Box(0)
        VLineCount = 0
        bar = 1
        for bar in range(bar, limit + 1):
            if CheckVLinePoint(bar, lastyear, time[bar]):
                VLineCount += 1
                if VLineCount >= LinesTotal:
                    break
        else:
            bar = _range_end(bar, limit + 1, 1)
        if bar < limit:
            limit = bar
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if CheckVLinePoint(bar, _GlobRef(globals(), '_s_OnCalculate_LastYear'), time[bar]):
            if Position:
                Time = StringToTime(_str(_s_OnCalculate_LastYear) + '.01.01 00:00')
            else:
                Time = time[bar]
            Name = LinesSirname + TimeToString(Time)
            RenameVline(0, LinesSirname + TimeToString(VLineTime[Count[FutureTotal]]), Name)
            SetVline(0, Name, 0, Time, Line_Color, Line_Style, Line_Width, SetBackground, 'годовой бар')
            VLineTime[Count[FutureTotal]] = Time
            if bar > 0:
                Recount_ArrayZeroPos(Count, LinesTotal_)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    for numb in range(_int(FutureTotal) - 1, 0 - 1, -1):
        year = _int(_s_OnCalculate_LastYear + FutureTotal - numb)
        Time = StringToTime(_str(year) + '.01.01 00:00')
        Name = LinesSirname + TimeToString(Time)
        RenameVline(0, LinesSirname + TimeToString(VLineTime[Count[numb]]), Name)
        SetVline(0, Name, 0, Time, Line_Color, Line_Style, Line_Width, SetBackground, 'годовой бар')
        VLineTime[Count[numb]] = Time
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Line_Color = _input('Line_Color', _uint(Orange))  # Line color

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_LastYear = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VgridlineAnnual(_MQL5Indicator):
    name = 'vgridline_annual'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Line_Style': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Line display style
        'Line_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width
        'SetBackground': True,  # Lines background display
        'LinesTotal': 10,  # Number of lines in history
        'FutureTotal': 1,  # Number of lines in future empty history
        'Position': True,  # Lines position (true - true position, false - matching with bars)
    }

