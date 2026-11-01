"""DailyPercentageChange — converted from MQL5: MQL5 Indicators/Daily Percentage Change MT5/DailyPercentageChange.mq5

Shows daily percentage change value (yesterday's close to current bid).
You can set hourly shift for day start.
Can also show weekly and monthly price changes.
Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ["Shows daily percentage change value (yesterday's close to current bid).", 'You can set hourly shift for day start.', 'Can also show weekly and monthly price changes.'], 'name': 'DailyPercentageChange', 'source': 'MQL5 Indicators/Daily Percentage Change MT5/DailyPercentageChange.mq5', 'folder': 'Daily Percentage Change MT5', 'inputs': [{'mql': 'Time_Shift', 'py': 'Time_Shift', 'param': 'Time_Shift', 'type': 'int', 'default': 0, 'label': 'Time shift for day start (-12 to +12 hours)', 'sinput': False}, {'mql': 'Show_Weekly', 'py': 'Show_Weekly', 'param': 'Show_Weekly', 'type': 'bool', 'default': True, 'label': 'Show weekly change?', 'sinput': False}, {'mql': 'Show_Monthly', 'py': 'Show_Monthly', 'param': 'Show_Monthly', 'type': 'bool', 'default': True, 'label': 'Show monthly change?', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'int', 'default': 8, 'label': 'Font size', 'sinput': False}, {'mql': 'Arrow_Size', 'py': 'Arrow_Size', 'param': 'Arrow_Size', 'type': 'int', 'default': 10, 'label': 'Arrow size', 'sinput': False}, {'mql': 'Up_Color', 'py': 'Up_Color', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Up color', 'sinput': False}, {'mql': 'Up_Arrow', 'py': 'Up_Arrow', 'param': None, 'type': 'string', 'default': 'p', 'label': 'Up arrow Windings code', 'sinput': False}, {'mql': 'Down_Color', 'py': 'Down_Color', 'param': None, 'type': 'color', 'default': 255, 'label': 'Down color', 'sinput': False}, {'mql': 'Down_Arrow', 'py': 'Down_Arrow', 'param': None, 'type': 'string', 'default': 'q', 'label': 'Up arrow Windings code', 'sinput': False}, {'mql': 'No_Mvt_Color', 'py': 'No_Mvt_Color', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'No change color', 'sinput': False}, {'mql': 'X_Position_Text', 'py': 'X_Position_Text', 'param': 'X_Position_Text', 'type': 'int', 'default': 21, 'label': 'X distance for text', 'sinput': False}, {'mql': 'Y_Position_Text', 'py': 'Y_Position_Text', 'param': 'Y_Position_Text', 'type': 'int', 'default': 20, 'label': 'Y distance for text', 'sinput': False}, {'mql': 'Corner_Position_Text', 'py': 'Corner_Position_Text', 'param': 'Corner_Position_Text', 'type': 'int', 'default': 1, 'label': 'Text corner', 'sinput': False}, {'mql': 'X_Position_Arrow', 'py': 'X_Position_Arrow', 'param': 'X_Position_Arrow', 'type': 'int', 'default': 5, 'label': 'X distance for arrow', 'sinput': False}, {'mql': 'Y_Position_Arrow', 'py': 'Y_Position_Arrow', 'param': 'Y_Position_Arrow', 'type': 'int', 'default': 20, 'label': 'Y distance for arrow', 'sinput': False}, {'mql': 'Corner_Position_Arrow', 'py': 'Corner_Position_Arrow', 'param': 'Corner_Position_Arrow', 'type': 'int', 'default': 1, 'label': 'Arrow corner', 'sinput': False}, {'mql': 'X_Position_Text_W', 'py': 'X_Position_Text_W', 'param': 'X_Position_Text_W', 'type': 'int', 'default': 21, 'label': 'X distance for weekly text', 'sinput': False}, {'mql': 'Y_Position_Text_W', 'py': 'Y_Position_Text_W', 'param': 'Y_Position_Text_W', 'type': 'int', 'default': 35, 'label': 'Y distance for weekly text', 'sinput': False}, {'mql': 'Corner_Position_Text_W', 'py': 'Corner_Position_Text_W', 'param': 'Corner_Position_Text_W', 'type': 'int', 'default': 1, 'label': 'Weekly text corner', 'sinput': False}, {'mql': 'X_Position_Arrow_W', 'py': 'X_Position_Arrow_W', 'param': 'X_Position_Arrow_W', 'type': 'int', 'default': 5, 'label': 'X distance for weekly arrow', 'sinput': False}, {'mql': 'Y_Position_Arrow_W', 'py': 'Y_Position_Arrow_W', 'param': 'Y_Position_Arrow_W', 'type': 'int', 'default': 35, 'label': 'Y distance for weekly arrow', 'sinput': False}, {'mql': 'Corner_Position_Arrow_W', 'py': 'Corner_Position_Arrow_W', 'param': 'Corner_Position_Arrow_W', 'type': 'int', 'default': 1, 'label': 'Weekly arrow corner', 'sinput': False}, {'mql': 'X_Position_Text_M', 'py': 'X_Position_Text_M', 'param': 'X_Position_Text_M', 'type': 'int', 'default': 21, 'label': 'X distance for monthly text', 'sinput': False}, {'mql': 'Y_Position_Text_M', 'py': 'Y_Position_Text_M', 'param': 'Y_Position_Text_M', 'type': 'int', 'default': 50, 'label': 'Y distance for monthly text', 'sinput': False}, {'mql': 'Corner_Position_Text_M', 'py': 'Corner_Position_Text_M', 'param': 'Corner_Position_Text_M', 'type': 'int', 'default': 1, 'label': 'Monthly text corner', 'sinput': False}, {'mql': 'X_Position_Arrow_M', 'py': 'X_Position_Arrow_M', 'param': 'X_Position_Arrow_M', 'type': 'int', 'default': 5, 'label': 'X distance for monthly arrow', 'sinput': False}, {'mql': 'Y_Position_Arrow_M', 'py': 'Y_Position_Arrow_M', 'param': 'Y_Position_Arrow_M', 'type': 'int', 'default': 50, 'label': 'Y distance for monthly arrow', 'sinput': False}, {'mql': 'Corner_Position_Arrow_M', 'py': 'Corner_Position_Arrow_M', 'param': 'Corner_Position_Arrow_M', 'type': 'int', 'default': 1, 'label': 'Monthly arrow corner', 'sinput': False}, {'mql': 'Text_Object', 'py': 'Text_Object', 'param': None, 'type': 'string', 'default': 'DailyChange', 'label': 'Text object name', 'sinput': False}, {'mql': 'Arrow_Object', 'py': 'Arrow_Object', 'param': None, 'type': 'string', 'default': 'ArrowChange', 'label': 'Arrow object name', 'sinput': False}, {'mql': 'Text_Object_W', 'py': 'Text_Object_W', 'param': None, 'type': 'string', 'default': 'WeeklyChange', 'label': 'Weekly text object name', 'sinput': False}, {'mql': 'Arrow_Object_W', 'py': 'Arrow_Object_W', 'param': None, 'type': 'string', 'default': 'ArrowChange_W', 'label': 'Weekly arrow object name', 'sinput': False}, {'mql': 'Text_Object_M', 'py': 'Text_Object_M', 'param': None, 'type': 'string', 'default': 'MonthlyChange', 'label': 'Monthly text object name', 'sinput': False}, {'mql': 'Arrow_Object_M', 'py': 'Arrow_Object_M', 'param': None, 'type': 'string', 'default': 'ArrowChange_M', 'label': 'Monthly arrow object name', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Time_Shift = _input('Time_Shift', 0)  # Time shift for day start (-12 to +12 hours)
Show_Weekly = _input('Show_Weekly', True)  # Show weekly change?
Show_Monthly = _input('Show_Monthly', True)  # Show monthly change?
Font_Size = _input('Font_Size', 8)  # Font size
Arrow_Size = _input('Arrow_Size', 10)  # Arrow size
Up_Color = _input('Up_Color', clrGreen)  # Up color
Up_Arrow = _input('Up_Arrow', 'p')  # Up arrow Windings code
Down_Color = _input('Down_Color', clrRed)  # Down color
Down_Arrow = _input('Down_Arrow', 'q')  # Up arrow Windings code
No_Mvt_Color = _input('No_Mvt_Color', clrBlue)  # No change color
X_Position_Text = _input('X_Position_Text', 21)  # X distance for text
Y_Position_Text = _input('Y_Position_Text', 20)  # Y distance for text
Corner_Position_Text = _input('Corner_Position_Text', CORNER_LEFT_LOWER)  # Text corner
X_Position_Arrow = _input('X_Position_Arrow', 5)  # X distance for arrow
Y_Position_Arrow = _input('Y_Position_Arrow', 20)  # Y distance for arrow
Corner_Position_Arrow = _input('Corner_Position_Arrow', CORNER_LEFT_LOWER)  # Arrow corner
X_Position_Text_W = _input('X_Position_Text_W', 21)  # X distance for weekly text
Y_Position_Text_W = _input('Y_Position_Text_W', 35)  # Y distance for weekly text
Corner_Position_Text_W = _input('Corner_Position_Text_W', CORNER_LEFT_LOWER)  # Weekly text corner
X_Position_Arrow_W = _input('X_Position_Arrow_W', 5)  # X distance for weekly arrow
Y_Position_Arrow_W = _input('Y_Position_Arrow_W', 35)  # Y distance for weekly arrow
Corner_Position_Arrow_W = _input('Corner_Position_Arrow_W', CORNER_LEFT_LOWER)  # Weekly arrow corner
X_Position_Text_M = _input('X_Position_Text_M', 21)  # X distance for monthly text
Y_Position_Text_M = _input('Y_Position_Text_M', 50)  # Y distance for monthly text
Corner_Position_Text_M = _input('Corner_Position_Text_M', CORNER_LEFT_LOWER)  # Monthly text corner
X_Position_Arrow_M = _input('X_Position_Arrow_M', 5)  # X distance for monthly arrow
Y_Position_Arrow_M = _input('Y_Position_Arrow_M', 50)  # Y distance for monthly arrow
Corner_Position_Arrow_M = _input('Corner_Position_Arrow_M', CORNER_LEFT_LOWER)  # Monthly arrow corner
Text_Object = _input('Text_Object', 'DailyChange')  # Text object name
Arrow_Object = _input('Arrow_Object', 'ArrowChange')  # Arrow object name
Text_Object_W = _input('Text_Object_W', 'WeeklyChange')  # Weekly text object name
Arrow_Object_W = _input('Arrow_Object_W', 'ArrowChange_W')  # Weekly arrow object name
Text_Object_M = _input('Text_Object_M', 'MonthlyChange')  # Monthly text object name
Arrow_Object_M = _input('Arrow_Object_M', 'ArrowChange_M')  # Monthly arrow object name

def OnInit():
    if Time_Shift > 12 or Time_Shift < -12:
        Alert('Time shift should be between -12 and 12.')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, Text_Object)
    ObjectDelete(0, Arrow_Object)
    ObjectDelete(0, Text_Object_W)
    ObjectDelete(0, Arrow_Object_W)
    ObjectDelete(0, Text_Object_M)
    ObjectDelete(0, Arrow_Object_M)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    PercChange = 0.0
    DailyClose = -1.0
    PerChg = ""
    if Time_Shift == 0:
        CloseDaily = Arr(0, 0.0)
        if CopyClose(Symbol(), PERIOD_D1, 1, 1, CloseDaily) != 1:
            return 0
        DailyClose = CloseDaily[0]
    else:
        CloseHourly = Arr(0, 0.0)
        TimeHourly = Arr(0, 0)
        datetime_str = MqlDateTime()
        if CopyClose(Symbol(), PERIOD_H1, 0, 25, CloseHourly) != 25:
            return 0
        if CopyTime(Symbol(), PERIOD_H1, 0, 25, TimeHourly) != 25:
            return 0
        TimeToStruct(TimeHourly[24] + (Time_Shift * 3600), datetime_str)
        current_img_day = datetime_str.day_of_year
        for i in range(23, 0 - 1, -1):
            TimeToStruct(TimeHourly[i] + (Time_Shift * 3600), datetime_str)
            if datetime_str.day_of_year != current_img_day:
                DailyClose = CloseHourly[i]
                break
    PercChange = _fdiv(SymbolInfoDouble(Symbol(), SYMBOL_BID) - DailyClose, DailyClose) * 100
    PerChg = 'Daily Change: ' + DoubleToString(PercChange, 2) + '%'
    ShowObjects(PercChange, PerChg, Text_Object, Arrow_Object, Corner_Position_Text, X_Position_Text, Y_Position_Text, Corner_Position_Arrow, X_Position_Arrow, Y_Position_Arrow)
    if Show_Weekly:
        CloseWeekly = Arr(0, 0.0)
        if CopyClose(Symbol(), PERIOD_W1, 1, 1, CloseWeekly) != 1:
            return 0
        WeeklyClose = CloseWeekly[0]
        PercChange = _fdiv(SymbolInfoDouble(Symbol(), SYMBOL_BID) - WeeklyClose, WeeklyClose) * 100
        PerChg = 'Weekly Change: ' + DoubleToString(PercChange, 2) + '%'
        ShowObjects(PercChange, PerChg, Text_Object_W, Arrow_Object_W, Corner_Position_Text_W, X_Position_Text_W, Y_Position_Text_W, Corner_Position_Arrow_W, X_Position_Arrow_W, Y_Position_Arrow_W)
    if Show_Monthly:
        MonthlyClose = -1.0
        if Time_Shift == 0:
            CloseMonthly = Arr(0, 0.0)
            if CopyClose(Symbol(), PERIOD_MN1, 1, 1, CloseMonthly) != 1:
                return 0
            MonthlyClose = CloseMonthly[0]
        else:
            CloseHourly = Arr(0, 0.0)
            TimeHourly = Arr(0, 0)
            datetime_str = MqlDateTime()
            if CopyClose(Symbol(), PERIOD_H1, 0, (31 * 24) + 1, CloseHourly) != ((31 * 24) + 1):
                return 0
            if CopyTime(Symbol(), PERIOD_H1, 0, (31 * 24) + 1, TimeHourly) != ((31 * 24) + 1):
                return 0
            TimeToStruct(TimeHourly[31 * 24] + (Time_Shift * 3600), datetime_str)
            current_img_month = datetime_str.mon
            for i in range(31 * 24, 0 - 1, -1):
                TimeToStruct(TimeHourly[i] + (Time_Shift * 3600), datetime_str)
                if datetime_str.mon != current_img_month:
                    MonthlyClose = CloseHourly[i]
                    break
        PercChange = _fdiv(SymbolInfoDouble(Symbol(), SYMBOL_BID) - MonthlyClose, MonthlyClose) * 100
        PerChg = 'Monthly Change: ' + DoubleToString(PercChange, 2) + '%'
        ShowObjects(PercChange, PerChg, Text_Object_M, Arrow_Object_M, Corner_Position_Text_M, X_Position_Text_M, Y_Position_Text_M, Corner_Position_Arrow_M, X_Position_Arrow_M, Y_Position_Arrow_M)
    return rates_total

def ShowObjects(PercChange, PerChg, text_obj, arrow_obj, corner_pos_text, x_pos_text, y_pos_text, corner_pos_arrow, x_pos_arrow, y_pos_arrow):
    Arrow = ''
    Obj_Color = No_Mvt_Color
    if PercChange > 0:
        Arrow = Up_Arrow
        Obj_Color = Up_Color
    elif PercChange < 0:
        Arrow = Down_Arrow
        Obj_Color = Down_Color
    if ObjectFind(0, text_obj) < 0:
        ObjectCreate(0, text_obj, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, text_obj, OBJPROP_CORNER, corner_pos_text)
        ObjectSetInteger(0, text_obj, OBJPROP_XDISTANCE, x_pos_text)
        ObjectSetInteger(0, text_obj, OBJPROP_YDISTANCE, y_pos_text)
        ObjectSetInteger(0, text_obj, OBJPROP_FONTSIZE, Font_Size)
        ObjectSetString(0, text_obj, OBJPROP_FONT, 'Verdana')
    ObjectSetInteger(0, text_obj, OBJPROP_COLOR, Obj_Color)
    ObjectSetString(0, text_obj, OBJPROP_TEXT, PerChg)
    if ObjectFind(0, arrow_obj) < 0:
        ObjectCreate(0, arrow_obj, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, arrow_obj, OBJPROP_CORNER, corner_pos_arrow)
        ObjectSetInteger(0, arrow_obj, OBJPROP_XDISTANCE, x_pos_arrow)
        ObjectSetInteger(0, arrow_obj, OBJPROP_YDISTANCE, y_pos_arrow)
        ObjectSetInteger(0, arrow_obj, OBJPROP_FONTSIZE, Font_Size)
        ObjectSetString(0, arrow_obj, OBJPROP_FONT, 'Wingdings 3')
    ObjectSetInteger(0, arrow_obj, OBJPROP_COLOR, Obj_Color)
    ObjectSetString(0, arrow_obj, OBJPROP_TEXT, Arrow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyPercentageChange(_MQL5Indicator):
    name = 'DailyPercentageChange'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Time_Shift': 0,  # Time shift for day start (-12 to +12 hours)
        'Show_Weekly': True,  # Show weekly change?
        'Show_Monthly': True,  # Show monthly change?
        'Font_Size': 8,  # Font size
        'Arrow_Size': 10,  # Arrow size
        'X_Position_Text': 21,  # X distance for text
        'Y_Position_Text': 20,  # Y distance for text
        'Corner_Position_Text': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Text corner
        'X_Position_Arrow': 5,  # X distance for arrow
        'Y_Position_Arrow': 20,  # Y distance for arrow
        'Corner_Position_Arrow': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Arrow corner
        'X_Position_Text_W': 21,  # X distance for weekly text
        'Y_Position_Text_W': 35,  # Y distance for weekly text
        'Corner_Position_Text_W': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Weekly text corner
        'X_Position_Arrow_W': 5,  # X distance for weekly arrow
        'Y_Position_Arrow_W': 35,  # Y distance for weekly arrow
        'Corner_Position_Arrow_W': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Weekly arrow corner
        'X_Position_Text_M': 21,  # X distance for monthly text
        'Y_Position_Text_M': 50,  # Y distance for monthly text
        'Corner_Position_Text_M': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Monthly text corner
        'X_Position_Arrow_M': 5,  # X distance for monthly arrow
        'Y_Position_Arrow_M': 50,  # Y distance for monthly arrow
        'Corner_Position_Arrow_M': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Monthly arrow corner
    }

