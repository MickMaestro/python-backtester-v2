"""vgridline_weekly — converted from MQL5: MQL5 Indicators/VGridLine Weekly/vgridline_weekly.mq5

Time grid mesh. Grid step - 1 week
The indicator works at all timeframes less than a week.
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'indicator_buffers': 1, 'indicator_plots': 1, 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Time grid mesh. Grid step - 1 week', 'The indicator works at all timeframes less than a week.'], 'name': 'vgridline_weekly', 'source': 'MQL5 Indicators/VGridLine Weekly/vgridline_weekly.mq5', 'folder': 'VGridLine Weekly', 'inputs': [{'mql': 'LinesSirname', 'py': 'LinesSirname', 'param': None, 'type': 'string', 'default': 'VLine_Grid_Weekly_', 'label': 'Line name', 'sinput': False}, {'mql': 'Line_Color', 'py': 'Line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Line color', 'sinput': False}, {'mql': 'Line_Style', 'py': 'Line_Style', 'param': 'Line_Style', 'type': 'int', 'default': 0, 'label': 'Line display style', 'sinput': False}, {'mql': 'Line_Width', 'py': 'Line_Width', 'param': 'Line_Width', 'type': 'int', 'default': 1, 'label': 'Line width', 'sinput': False}, {'mql': 'SetBackground', 'py': 'SetBackground', 'param': 'SetBackground', 'type': 'bool', 'default': True, 'label': 'Lines background display', 'sinput': False}, {'mql': 'LinesTotal', 'py': 'LinesTotal', 'param': 'LinesTotal', 'type': 'uint', 'default': 10, 'label': 'Number of lines in history', 'sinput': False}, {'mql': 'FutureTotal', 'py': 'FutureTotal', 'param': 'FutureTotal', 'type': 'uint', 'default': 1, 'label': 'Number of lines in future empty history', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Aqua = 0xFFFF00  # MQL4 colour name

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
LinesSirname = _input('LinesSirname', 'VLine_Grid_Weekly_')  # Line name
Line_Style = _input('Line_Style', SOLID_)  # Line display style
Line_Width = _input('Line_Width', w_1)  # Line width
SetBackground = _input('SetBackground', True)  # Lines background display
LinesTotal = _input('LinesTotal', 10)  # Number of lines in history
FutureTotal = _input('FutureTotal', 1)  # Number of lines in future empty history
Count = Arr(0, 0)
VLineTime = Arr(0, 0)
LinesTotal_ = 0

def CheckVLinePoint(bar, bartime):
    tm = MqlDateTime()
    TimeToStruct(bartime, tm)
    if tm.day_of_week == 0 or tm.day_of_week == 6:
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
    if Period() > PERIOD_D1:
        return
    Deinit()
    LinesTotal_ = LinesTotal + FutureTotal
    ArrayResize(Count, LinesTotal_)
    ArrayResize(VLineTime, LinesTotal_)
    shortname = Box("")
    StringConcatenate(shortname, 'VGridLine_Weekly(', LinesSirname, ', ', LinesTotal, ')')
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
    global _s_OnCalculate_LastTime
    if Period() > PERIOD_D1:
        return 0
    if rates_total < 2:
        return 0
    if prev_calculated == rates_total:
        return rates_total
    Name = ""
    Time = 0
    limit = 0
    bar = 0
    ArraySetAsSeries(time, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        VLineCount = 0
        bar = 0
        for bar in range(bar, limit + 1):
            if CheckVLinePoint(bar, _idiv(time[bar] + time[bar + 1], 2)):
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
        if CheckVLinePoint(bar, _idiv(time[bar] + time[bar + 1], 2)):
            Name = LinesSirname + TimeToString(time[bar])
            RenameVline(0, LinesSirname + TimeToString(VLineTime[Count[FutureTotal]]), Name)
            SetVline(0, Name, 0, time[bar], Line_Color, Line_Style, Line_Width, SetBackground, 'week bar')
            VLineTime[Count[FutureTotal]] = time[bar]
            if bar > 0:
                Recount_ArrayZeroPos(Count, LinesTotal_)
            _s_OnCalculate_LastTime = time[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    for numb in range(_int(FutureTotal) - 1, 0 - 1, -1):
        Time = _s_OnCalculate_LastTime + (604800 * (FutureTotal - numb))
        Name = LinesSirname + TimeToString(Time)
        RenameVline(0, LinesSirname + TimeToString(VLineTime[Count[numb]]), Name)
        SetVline(0, Name, 0, Time, Line_Color, Line_Style, Line_Width, SetBackground, 'week bar')
        VLineTime[Count[numb]] = Time
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Line_Color = _input('Line_Color', _uint(Aqua))  # Line color

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_LastTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VgridlineWeekly(_MQL5Indicator):
    name = 'vgridline_weekly'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Line_Style': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Line display style
        'Line_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Line width
        'SetBackground': True,  # Lines background display
        'LinesTotal': 10,  # Number of lines in history
        'FutureTotal': 1,  # Number of lines in future empty history
    }

