"""VGridLine_Custom — converted from MQL5: MQL5 Indicators/VGridLine_Custom/VGridLine_Custom.mq5

Временная координатная сетка. Шаг сетки - 1 день.
Индикатор работает на всех таймфреймах меньше дневного.
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.10', 'indicator_buffers': 0, 'indicator_plots': 0, 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Временная координатная сетка. Шаг сетки - 1 день.', 'Индикатор работает на всех таймфреймах меньше дневного.'], 'name': 'VGridLine_Custom', 'source': 'MQL5 Indicators/VGridLine_Custom/VGridLine_Custom.mq5', 'folder': 'VGridLine_Custom', 'inputs': [{'mql': 'LinesSirname', 'py': 'LinesSirname', 'param': None, 'type': 'string', 'default': 'VLine_Grid_Custom_', 'label': 'название линии', 'sinput': False}, {'mql': 'LineHours', 'py': 'LineHours', 'param': 'LineHours', 'type': 'int', 'default': 0, 'label': 'Время установки линии (Часы)', 'sinput': False}, {'mql': 'LineMinuts', 'py': 'LineMinuts', 'param': 'LineMinuts', 'type': 'int', 'default': 0, 'label': 'Время установки линии (Минуты)', 'sinput': False}, {'mql': 'Line_Color', 'py': 'Line_Color', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет линии', 'sinput': False}, {'mql': 'Line_Style', 'py': 'Line_Style', 'param': 'Line_Style', 'type': 'int', 'default': 4, 'label': 'стиль изображения линии', 'sinput': False}, {'mql': 'Line_Width', 'py': 'Line_Width', 'param': 'Line_Width', 'type': 'int', 'default': 1, 'label': 'толщина линии', 'sinput': False}, {'mql': 'SetBackground', 'py': 'SetBackground', 'param': 'SetBackground', 'type': 'bool', 'default': True, 'label': 'фоновое отображение линий', 'sinput': False}, {'mql': 'LinesTotal', 'py': 'LinesTotal', 'param': 'LinesTotal', 'type': 'uint', 'default': 10, 'label': 'количество линий на истории', 'sinput': False}, {'mql': 'FutureTotal', 'py': 'FutureTotal', 'param': 'FutureTotal', 'type': 'uint', 'default': 1, 'label': 'количество линий на пустой истории будущего', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum HOURS
ENUM_HOUR_0 = 0
ENUM_HOUR_1 = 1
ENUM_HOUR_2 = 2
ENUM_HOUR_3 = 3
ENUM_HOUR_4 = 4
ENUM_HOUR_5 = 5
ENUM_HOUR_6 = 6
ENUM_HOUR_7 = 7
ENUM_HOUR_8 = 8
ENUM_HOUR_9 = 9
ENUM_HOUR_10 = 10
ENUM_HOUR_11 = 11
ENUM_HOUR_12 = 12
ENUM_HOUR_13 = 13
ENUM_HOUR_14 = 14
ENUM_HOUR_15 = 15
ENUM_HOUR_16 = 16
ENUM_HOUR_17 = 17
ENUM_HOUR_18 = 18
ENUM_HOUR_19 = 19
ENUM_HOUR_20 = 20
ENUM_HOUR_21 = 21
ENUM_HOUR_22 = 22
ENUM_HOUR_23 = 23
_enum('HOURS', {0: 'ENUM_HOUR_0', 1: 'ENUM_HOUR_1', 2: 'ENUM_HOUR_2', 3: 'ENUM_HOUR_3', 4: 'ENUM_HOUR_4', 5: 'ENUM_HOUR_5', 6: 'ENUM_HOUR_6', 7: 'ENUM_HOUR_7', 8: 'ENUM_HOUR_8', 9: 'ENUM_HOUR_9', 10: 'ENUM_HOUR_10', 11: 'ENUM_HOUR_11', 12: 'ENUM_HOUR_12', 13: 'ENUM_HOUR_13', 14: 'ENUM_HOUR_14', 15: 'ENUM_HOUR_15', 16: 'ENUM_HOUR_16', 17: 'ENUM_HOUR_17', 18: 'ENUM_HOUR_18', 19: 'ENUM_HOUR_19', 20: 'ENUM_HOUR_20', 21: 'ENUM_HOUR_21', 22: 'ENUM_HOUR_22', 23: 'ENUM_HOUR_23'})

# enum MINUTS
ENUM_MINUT_0 = 0
ENUM_MINUT_1 = 1
ENUM_MINUT_2 = 2
ENUM_MINUT_3 = 3
ENUM_MINUT_4 = 4
ENUM_MINUT_5 = 5
ENUM_MINUT_6 = 6
ENUM_MINUT_7 = 7
ENUM_MINUT_8 = 8
ENUM_MINUT_9 = 9
ENUM_MINUT_10 = 10
ENUM_MINUT_11 = 11
ENUM_MINUT_12 = 12
ENUM_MINUT_13 = 13
ENUM_MINUT_14 = 14
ENUM_MINUT_15 = 15
ENUM_MINUT_16 = 16
ENUM_MINUT_17 = 17
ENUM_MINUT_18 = 18
ENUM_MINUT_19 = 19
ENUM_MINUT_20 = 20
ENUM_MINUT_21 = 21
ENUM_MINUT_22 = 22
ENUM_MINUT_23 = 23
ENUM_MINUT_24 = 24
ENUM_MINUT_25 = 25
ENUM_MINUT_26 = 26
ENUM_MINUT_27 = 27
ENUM_MINUT_28 = 28
ENUM_MINUT_29 = 29
ENUM_MINUT_30 = 30
ENUM_MINUT_31 = 31
ENUM_MINUT_32 = 32
ENUM_MINUT_33 = 33
ENUM_MINUT_34 = 34
ENUM_MINUT_35 = 35
ENUM_MINUT_36 = 36
ENUM_MINUT_37 = 37
ENUM_MINUT_38 = 38
ENUM_MINUT_39 = 39
ENUM_MINUT_40 = 40
ENUM_MINUT_41 = 41
ENUM_MINUT_42 = 42
ENUM_MINUT_43 = 43
ENUM_MINUT_44 = 44
ENUM_MINUT_45 = 45
ENUM_MINUT_46 = 46
ENUM_MINUT_47 = 47
ENUM_MINUT_48 = 48
ENUM_MINUT_49 = 49
ENUM_MINUT_50 = 50
ENUM_MINUT_51 = 51
ENUM_MINUT_52 = 52
ENUM_MINUT_53 = 53
ENUM_MINUT_54 = 54
ENUM_MINUT_55 = 55
ENUM_MINUT_56 = 56
ENUM_MINUT_57 = 57
ENUM_MINUT_58 = 58
ENUM_MINUT_59 = 59
_enum('MINUTS', {0: 'ENUM_MINUT_0', 1: 'ENUM_MINUT_1', 2: 'ENUM_MINUT_2', 3: 'ENUM_MINUT_3', 4: 'ENUM_MINUT_4', 5: 'ENUM_MINUT_5', 6: 'ENUM_MINUT_6', 7: 'ENUM_MINUT_7', 8: 'ENUM_MINUT_8', 9: 'ENUM_MINUT_9', 10: 'ENUM_MINUT_10', 11: 'ENUM_MINUT_11', 12: 'ENUM_MINUT_12', 13: 'ENUM_MINUT_13', 14: 'ENUM_MINUT_14', 15: 'ENUM_MINUT_15', 16: 'ENUM_MINUT_16', 17: 'ENUM_MINUT_17', 18: 'ENUM_MINUT_18', 19: 'ENUM_MINUT_19', 20: 'ENUM_MINUT_20', 21: 'ENUM_MINUT_21', 22: 'ENUM_MINUT_22', 23: 'ENUM_MINUT_23', 24: 'ENUM_MINUT_24', 25: 'ENUM_MINUT_25', 26: 'ENUM_MINUT_26', 27: 'ENUM_MINUT_27', 28: 'ENUM_MINUT_28', 29: 'ENUM_MINUT_29', 30: 'ENUM_MINUT_30', 31: 'ENUM_MINUT_31', 32: 'ENUM_MINUT_32', 33: 'ENUM_MINUT_33', 34: 'ENUM_MINUT_34', 35: 'ENUM_MINUT_35', 36: 'ENUM_MINUT_36', 37: 'ENUM_MINUT_37', 38: 'ENUM_MINUT_38', 39: 'ENUM_MINUT_39', 40: 'ENUM_MINUT_40', 41: 'ENUM_MINUT_41', 42: 'ENUM_MINUT_42', 43: 'ENUM_MINUT_43', 44: 'ENUM_MINUT_44', 45: 'ENUM_MINUT_45', 46: 'ENUM_MINUT_46', 47: 'ENUM_MINUT_47', 48: 'ENUM_MINUT_48', 49: 'ENUM_MINUT_49', 50: 'ENUM_MINUT_50', 51: 'ENUM_MINUT_51', 52: 'ENUM_MINUT_52', 53: 'ENUM_MINUT_53', 54: 'ENUM_MINUT_54', 55: 'ENUM_MINUT_55', 56: 'ENUM_MINUT_56', 57: 'ENUM_MINUT_57', 58: 'ENUM_MINUT_58', 59: 'ENUM_MINUT_59'})

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
LinesSirname = _input('LinesSirname', 'VLine_Grid_Custom_')  # название линии
LineHours = _input('LineHours', ENUM_HOUR_0)  # Время установки линии (Часы)
LineMinuts = _input('LineMinuts', ENUM_MINUT_0)  # Время установки линии (Минуты)
Line_Color = _input('Line_Color', clrMagenta)  # цвет линии
Line_Style = _input('Line_Style', STYLE_DASHDOTDOT)  # стиль изображения линии
Line_Width = _input('Line_Width', w_1)  # толщина линии
SetBackground = _input('SetBackground', True)  # фоновое отображение линий
LinesTotal = _input('LinesTotal', 10)  # количество линий на истории
FutureTotal = _input('FutureTotal', 1)  # количество линий на пустой истории будущего
Count = Arr(0, 0)
VLineTime = Arr(0, 0)
LinesTotal_ = 0

def CheckVLinePoint(bartime1, bartime0):
    tm0 = MqlDateTime()
    tm1 = MqlDateTime()
    TimeToStruct(bartime0, tm0)
    TimeToStruct(bartime1, tm1)
    if tm0.hour == LineHours and tm0.min == LineMinuts:
        return True
    if not LineMinuts:
        if tm0.day_of_year == tm1.day_of_year:
            if tm1.hour < LineHours and tm0.hour > LineHours:
                return True
        if tm0.day_of_year != tm1.day_of_year:
            if tm0.hour >= LineHours:
                return True
    if LineMinuts:
        if (tm0.hour == LineHours and tm1.min < LineMinuts) and tm0.min >= LineMinuts:
            return True
        if (tm0.day_of_year == tm1.day_of_year and tm1.hour < LineHours) and tm0.hour > LineHours:
            return True
        if tm0.day_of_year != tm1.day_of_year:
            if tm0.hour > LineHours:
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
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetVline(chart_id, name, nwin, time1, Color, style, width, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateVline(chart_id, name, nwin, time1, Color, style, width, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, 999999999)

def OnInit():
    global LinesTotal_
    if Period() > PERIOD_H12:
        return
    Deinit()
    LinesTotal_ = LinesTotal + FutureTotal
    ArrayResize(Count, LinesTotal_)
    ArrayResize(VLineTime, LinesTotal_)
    shortname = Box("")
    StringConcatenate(shortname, 'VLine_Grid_Custom(', LinesSirname, ', ', LinesTotal, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def Deinit():
    ObjectsDeleteAll(0, LinesSirname, -1, OBJ_VLINE)
    ChartRedraw(0)

def OnDeinit(reason):
    Deinit()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastTime
    if Period() > PERIOD_H12:
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
        ArrayInitialize(Count, None)
        bar = 0
        for bar in range(bar, limit + 1):
            if CheckVLinePoint(time[bar + 1], time[bar]):
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
        if CheckVLinePoint(time[bar + 1], time[bar]):
            Name = LinesSirname + TimeToString(time[bar])
            RenameVline(0, LinesSirname + TimeToString(VLineTime[Count[FutureTotal]]), Name)
            SetVline(0, Name, 0, time[bar], Line_Color, Line_Style, Line_Width, SetBackground, 'дневной бар')
            VLineTime[Count[FutureTotal]] = time[bar]
            if bar > 0:
                Recount_ArrayZeroPos(Count, LinesTotal_)
            _s_OnCalculate_LastTime = time[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    for numb in range(_int(FutureTotal) - 1, 0 - 1, -1):
        Time = _s_OnCalculate_LastTime + (86400 * (FutureTotal - numb))
        Name = LinesSirname + TimeToString(Time)
        RenameVline(0, LinesSirname + TimeToString(VLineTime[Count[numb]]), Name)
        SetVline(0, Name, 0, Time, Line_Color, Line_Style, Line_Width, SetBackground, 'дневной бар')
        VLineTime[Count[numb]] = Time
    ChartRedraw(0)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_LastTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VGridLineCustom(_MQL5Indicator):
    name = 'VGridLine_Custom'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LineHours': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=0),  # Время установки линии (Часы)
        'LineMinuts': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=0),  # Время установки линии (Минуты)
        'Line_Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # стиль изображения линии
        'Line_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина линии
        'SetBackground': True,  # фоновое отображение линий
        'LinesTotal': 10,  # количество линий на истории
        'FutureTotal': 1,  # количество линий на пустой истории будущего
    }

