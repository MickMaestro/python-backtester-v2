"""Dolly_Graphics_v11-GMTShift — converted from MQL5: MQL5 Indicators/Dolly_Graphics_v11-GMTShift/Dolly_Graphics_v11-GMTShift.mq5

Link:  Dolly Graphics cja

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '', 'link': ' Dolly Graphics cja', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Dolly_Graphics_v11-GMTShift', 'source': 'MQL5 Indicators/Dolly_Graphics_v11-GMTShift/Dolly_Graphics_v11-GMTShift.mq5', 'folder': 'Dolly_Graphics_v11-GMTShift', 'inputs': [{'mql': 'GMTshift', 'py': 'GMTshift', 'param': 'GMTshift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Using_OpenGraphics', 'py': 'Using_OpenGraphics', 'param': 'Using_OpenGraphics', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Dolly_GRAPHICS', 'py': 'Dolly_GRAPHICS', 'param': 'Dolly_GRAPHICS', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Alert_ON', 'py': 'Alert_ON', 'param': 'Alert_ON', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Auto_Signals', 'py': 'Auto_Signals', 'param': 'Auto_Signals', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_DollyCOMMENTS', 'py': 'Show_DollyCOMMENTS', 'param': 'Show_DollyCOMMENTS', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'BUY_Color_2', 'py': 'BUY_Color_2', 'param': None, 'type': 'color', 'default': 9830400, 'label': '', 'sinput': False}, {'mql': 'BUY_Color_1', 'py': 'BUY_Color_1', 'param': None, 'type': 'color', 'default': 6553600, 'label': '', 'sinput': False}, {'mql': 'SELL_Color_1', 'py': 'SELL_Color_1', 'param': None, 'type': 'color', 'default': 120, 'label': '', 'sinput': False}, {'mql': 'SELL_Color_2', 'py': 'SELL_Color_2', 'param': None, 'type': 'color', 'default': 180, 'label': '', 'sinput': False}, {'mql': 'BUY_Target_2', 'py': 'BUY_Target_2', 'param': 'BUY_Target_2', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'BUY_Target_1', 'py': 'BUY_Target_1', 'param': 'BUY_Target_1', 'type': 'int', 'default': 40, 'label': '', 'sinput': False}, {'mql': 'BUY_Area', 'py': 'BUY_Area', 'param': 'BUY_Area', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'SELL_Area', 'py': 'SELL_Area', 'param': 'SELL_Area', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'SELL_Target_1', 'py': 'SELL_Target_1', 'param': 'SELL_Target_1', 'type': 'int', 'default': 40, 'label': '', 'sinput': False}, {'mql': 'SELL_Target_2', 'py': 'SELL_Target_2', 'param': 'SELL_Target_2', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'SHIFT_DailyText', 'py': 'SHIFT_DailyText', 'param': 'SHIFT_DailyText', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Show_DailyAverageGRAPHICS', 'py': 'Show_DailyAverageGRAPHICS', 'param': 'Show_DailyAverageGRAPHICS', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Daily_AverageGRAPHICS', 'py': 'Daily_AverageGRAPHICS', 'param': 'Daily_AverageGRAPHICS', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'DAILY_Av_UP_Color_150', 'py': 'DAILY_Av_UP_Color_150', 'param': None, 'type': 'color', 'default': 16739840, 'label': '', 'sinput': False}, {'mql': 'DAILY_Av_UP_Color_125', 'py': 'DAILY_Av_UP_Color_125', 'param': None, 'type': 'color', 'default': 16729600, 'label': '', 'sinput': False}, {'mql': 'DAILY_Av_UP_Color_100', 'py': 'DAILY_Av_UP_Color_100', 'param': None, 'type': 'color', 'default': 16716820, 'label': '', 'sinput': False}, {'mql': 'DAILY_Av_UP_Color_75', 'py': 'DAILY_Av_UP_Color_75', 'param': None, 'type': 'color', 'default': 13762560, 'label': '', 'sinput': False}, {'mql': 'DAILY_Av_DN_Color_75', 'py': 'DAILY_Av_DN_Color_75', 'param': None, 'type': 'color', 'default': 220, 'label': '', 'sinput': False}, {'mql': 'DAILY_Av_DN_Color_100', 'py': 'DAILY_Av_DN_Color_100', 'param': None, 'type': 'color', 'default': 655615, 'label': '', 'sinput': False}, {'mql': 'DAILY_Av_DN_Color_125', 'py': 'DAILY_Av_DN_Color_125', 'param': None, 'type': 'color', 'default': 18175, 'label': '', 'sinput': False}, {'mql': 'DAILY_Av_DN_Color_150', 'py': 'DAILY_Av_DN_Color_150', 'param': None, 'type': 'color', 'default': 28415, 'label': '', 'sinput': False}, {'mql': 'SHIFT_DailyAverageText', 'py': 'SHIFT_DailyAverageText', 'param': 'SHIFT_DailyAverageText', 'type': 'int', 'default': 28, 'label': '', 'sinput': False}, {'mql': 'Show_PivotLines', 'py': 'Show_PivotLines', 'param': 'Show_PivotLines', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Show_M_PivotLines', 'py': 'Show_M_PivotLines', 'param': 'Show_M_PivotLines', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SHIFT_Pivot_PointText', 'py': 'SHIFT_Pivot_PointText', 'param': 'SHIFT_Pivot_PointText', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Pivot_Point_ExtendLINE', 'py': 'Pivot_Point_ExtendLINE', 'param': 'Pivot_Point_ExtendLINE', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Show_FibLines', 'py': 'Show_FibLines', 'param': 'Show_FibLines', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Show_EXTRAFibLines', 'py': 'Show_EXTRAFibLines', 'param': 'Show_EXTRAFibLines', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SHIFT_FibText', 'py': 'SHIFT_FibText', 'param': 'SHIFT_FibText', 'type': 'int', 'default': 65, 'label': '', 'sinput': False}, {'mql': 'FIB_ExtendDISPLAY', 'py': 'FIB_ExtendDISPLAY', 'param': 'FIB_ExtendDISPLAY', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Show_Daily_HI_LOW', 'py': 'Show_Daily_HI_LOW', 'param': 'Show_Daily_HI_LOW', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SHIFT_HI_LOW_TEXT', 'py': 'SHIFT_HI_LOW_TEXT', 'param': 'SHIFT_HI_LOW_TEXT', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'Show_Daily_OPEN', 'py': 'Show_Daily_OPEN', 'param': 'Show_Daily_OPEN', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SHIFT_Daily_OPEN_TEXT', 'py': 'SHIFT_Daily_OPEN_TEXT', 'param': 'SHIFT_Daily_OPEN_TEXT', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Black = 0x000000  # MQL4 colour name
CornflowerBlue = 0xED9564  # MQL4 colour name
DarkOrange = 0x008CFF  # MQL4 colour name
DarkSeaGreen = 0x8FBC8F  # MQL4 colour name
DeepSkyBlue = 0xFFBF00  # MQL4 colour name
DimGray = 0x696969  # MQL4 colour name
DodgerBlue = 0xFF901E  # MQL4 colour name
Gold = 0x00D7FF  # MQL4 colour name
Gray = 0x808080  # MQL4 colour name
Green = 0x008000  # MQL4 colour name
LightBlue = 0xE6D8AD  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Maroon = 0x000080  # MQL4 colour name
Orange = 0x00A5FF  # MQL4 colour name
OrangeRed = 0x0045FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
Silver = 0xC0C0C0  # MQL4 colour name
Turquoise = 0xD0E040  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name
YellowGreen = 0x32CD9A  # MQL4 colour name

# ---- inputs and global variables
GMTshift = _input('GMTshift', 0)
Using_OpenGraphics = _input('Using_OpenGraphics', True)
Dolly_GRAPHICS = _input('Dolly_GRAPHICS', True)
Alert_ON = _input('Alert_ON', False)
Auto_Signals = _input('Auto_Signals', True)
Show_DollyCOMMENTS = _input('Show_DollyCOMMENTS', True)
BUY_Color_2 = _input('BUY_Color_2', 0x960000)
BUY_Color_1 = _input('BUY_Color_1', 0x640000)
SELL_Color_1 = _input('SELL_Color_1', 0x000078)
SELL_Color_2 = _input('SELL_Color_2', 0x0000B4)
BUY_Target_2 = _input('BUY_Target_2', 50)
BUY_Target_1 = _input('BUY_Target_1', 40)
BUY_Area = _input('BUY_Area', 20)
SELL_Area = _input('SELL_Area', 20)
SELL_Target_1 = _input('SELL_Target_1', 40)
SELL_Target_2 = _input('SELL_Target_2', 50)
SHIFT_DailyText = _input('SHIFT_DailyText', 0)
Show_DailyAverageGRAPHICS = _input('Show_DailyAverageGRAPHICS', True)
Daily_AverageGRAPHICS = _input('Daily_AverageGRAPHICS', True)
DAILY_Av_UP_Color_150 = _input('DAILY_Av_UP_Color_150', 0xFF6E00)
DAILY_Av_UP_Color_125 = _input('DAILY_Av_UP_Color_125', 0xFF4600)
DAILY_Av_UP_Color_100 = _input('DAILY_Av_UP_Color_100', 0xFF1414)
DAILY_Av_UP_Color_75 = _input('DAILY_Av_UP_Color_75', 0xD20000)
DAILY_Av_DN_Color_75 = _input('DAILY_Av_DN_Color_75', 0x0000DC)
DAILY_Av_DN_Color_100 = _input('DAILY_Av_DN_Color_100', 0x0A00FF)
DAILY_Av_DN_Color_125 = _input('DAILY_Av_DN_Color_125', 0x0046FF)
DAILY_Av_DN_Color_150 = _input('DAILY_Av_DN_Color_150', 0x006EFF)
SHIFT_DailyAverageText = _input('SHIFT_DailyAverageText', 28)
Show_PivotLines = _input('Show_PivotLines', False)
Show_M_PivotLines = _input('Show_M_PivotLines', False)
SHIFT_Pivot_PointText = _input('SHIFT_Pivot_PointText', 0)
Pivot_Point_ExtendLINE = _input('Pivot_Point_ExtendLINE', 0)
Show_FibLines = _input('Show_FibLines', False)
Show_EXTRAFibLines = _input('Show_EXTRAFibLines', False)
SHIFT_FibText = _input('SHIFT_FibText', 65)
FIB_ExtendDISPLAY = _input('FIB_ExtendDISPLAY', 1)
Show_Daily_HI_LOW = _input('Show_Daily_HI_LOW', False)
SHIFT_HI_LOW_TEXT = _input('SHIFT_HI_LOW_TEXT', 50)
Show_Daily_OPEN = _input('Show_Daily_OPEN', False)
SHIFT_Daily_OPEN_TEXT = _input('SHIFT_Daily_OPEN_TEXT', 0)
Bid = 0.0
Ask = 0.0
day_high = 0.0
day_low = 0.0
yesterday_open = 0.0
today_open = 0.0
cur_day = 0.0
prev_day = 0.0
yesterday_high = 0.0
yesterday_low = 0.0
yesterday_close = 0.0

def OnDeinit(reason):
    ObjectsDeleteAll(0, -1, OBJ_TEXT)
    ObjectsDeleteAll(0, -1, OBJ_LABEL)
    ObjectsDeleteAll(0, -1, OBJ_RECTANGLE)
    ObjectsDeleteAll(0, -1, OBJ_TRENDBYANGLE)
    ObjectDelete(0, 'Pivot')
    ObjectDelete(0, 'Open')
    ObjectDelete(0, 'Dolly')
    ObjectDelete(0, 'Dolly1')
    ObjectDelete(0, 'Dolly2')
    ObjectDelete(0, 'Dolly3')
    ObjectDelete(0, 'Dolly4')
    ObjectDelete(0, 'Dolly5')
    ObjectDelete(0, 'Dolly6')
    ObjectDelete(0, 'Dolly7')
    ObjectDelete(0, 'Dolly8')
    ObjectDelete(0, 'Dolly9')
    ObjectDelete(0, 'Dolly10')
    ObjectDelete(0, 'Dolly11')
    ObjectDelete(0, 'Dolly12')
    ObjectDelete(0, 'Dolly13')
    ObjectDelete(0, 'Dolly14')
    ObjectDelete(0, 'Dolly15')
    ObjectDelete(0, 'Dolly16')
    ObjectDelete(0, 'Dolly17')
    ObjectDelete(0, 'Dolly18')
    ObjectDelete(0, 'Dolly19')
    ObjectDelete(0, 'Dolly20')
    ObjectDelete(0, 'Dolly21')
    ObjectDelete(0, 'Dolly22')
    ObjectDelete(0, 'Dolly23')
    ObjectDelete(0, 'Dolly24')
    ObjectDelete(0, 'Dolly25')
    ObjectDelete(0, 'Dolly26')
    ObjectDelete(0, 'Dolly27')
    ObjectDelete(0, 'Dolly28')
    ObjectDelete(0, 'Dolly29')
    ObjectDelete(0, 'Dolly30')
    ObjectDelete(0, 'Dolly31')
    ObjectDelete(0, 'Dolly32')
    ObjectDelete(0, 'Dolly33')
    ObjectDelete(0, 'Dolly34')
    ObjectDelete(0, 'Dolly35')
    ObjectDelete(0, 'Dolly36')
    ObjectDelete(0, 'Dolly37')
    ObjectDelete(0, 'Dolly38')
    ObjectDelete(0, 'Dolly39')
    ObjectDelete(0, 'Dolly40')
    ObjectDelete(0, 'Dolly41')
    ObjectDelete(0, 'Dolly42')
    ObjectDelete(0, 'Dolly43')
    ObjectDelete(0, 'Dolly44')
    ObjectDelete(0, 'Dolly45')
    ObjectDelete(0, 'Dolly46')
    ObjectDelete(0, 'Dolly47')
    ObjectDelete(0, 'Dolly48')
    ObjectDelete(0, 'Dolly49')
    ObjectDelete(0, 'Dolly50')
    ObjectDelete(0, 'Dolly51')

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dolly Graphics #11 GMT Shift')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Ask, Bid
    Bid = close[rates_total - 1]
    Ask = Bid + (Point() * spread[rates_total - 1])
    CreateP()
    ChartRedraw(0)
    return rates_total

def CreateP():
    ObjectsDeleteAll(0, -1, OBJ_TRENDBYANGLE)
    DeleteCreatePivots1()
    CreateDL()

def DeleteCreatePivots1():
    ObjectDelete(0, 'P1')
    ObjectDelete(0, 'DHI')
    ObjectDelete(0, 'DLO')
    ObjectDelete(0, 'DO')

def CreateDL():
    ObjectsDeleteAll(0, -1, OBJ_RECTANGLE)
    DeleteDollyGraphics()
    CreateAL()

def DeleteDollyGraphics():
    ObjectDelete(0, 'DollyBUY3')
    ObjectDelete(0, 'DollyBUY2')
    ObjectDelete(0, 'DollyBUY1')
    ObjectDelete(0, 'DollySELL1')
    ObjectDelete(0, 'DollySELL2')
    ObjectDelete(0, 'DollySELL3')

def CreateAL():
    ObjectsDeleteAll(0, -1, OBJ_RECTANGLE)
    DeleteAvGraphics()
    CreatePP()

def DeleteAvGraphics():
    ObjectDelete(0, 'AvBUY150')
    ObjectDelete(0, 'AvBUY125')
    ObjectDelete(0, 'AvBUY100')
    ObjectDelete(0, 'AvBUY75')
    ObjectDelete(0, 'AvSELL75')
    ObjectDelete(0, 'AvSELL100')
    ObjectDelete(0, 'AvSELL125')
    ObjectDelete(0, 'AvSELL150')

def CreatePP():
    ObjectsDeleteAll(0, -1, OBJ_TRENDBYANGLE)
    DeleteCreatePivots()
    CreateFIB()

def DeleteCreatePivots():
    ObjectDelete(0, 'PP1')
    ObjectDelete(0, 'RR3')
    ObjectDelete(0, 'RR2')
    ObjectDelete(0, 'RR1')
    ObjectDelete(0, 'SS1')
    ObjectDelete(0, 'SS2')
    ObjectDelete(0, 'SS3')
    ObjectDelete(0, 'P1')
    ObjectDelete(0, 'MM1')
    ObjectDelete(0, 'MM2')
    ObjectDelete(0, 'MM3')
    ObjectDelete(0, 'MM4')
    ObjectDelete(0, 'MM5')
    ObjectDelete(0, 'MM0')
    ObjectDelete(0, 'DDHI')
    ObjectDelete(0, 'DDLO')

def CreatePivots1(Pivots1, start, end, w, s, clr):
    ObjectCreate(0, Pivots1, OBJ_TRENDBYANGLE, 0, iTime(None, PERIOD_D1, 0) + (GMTshift * 3600), start, iTime(None, PERIOD_CURRENT, 0), w, s, end)
    ObjectSetInteger(0, Pivots1, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, Pivots1, OBJPROP_RAY, False)
    ObjectSetInteger(0, Pivots1, OBJPROP_BACK, True)
    ObjectSetInteger(0, Pivots1, OBJPROP_WIDTH, w)
    ObjectSetInteger(0, Pivots1, OBJPROP_STYLE, s)

def CreateDollyGraphics(Dolly_, start, end, clr):
    ObjectCreate(0, Dolly_, OBJ_RECTANGLE, 0, iTime(None, PERIOD_D1, 0) + (GMTshift * 3600), start, iTime(None, PERIOD_CURRENT, 0), end)
    ObjectSetInteger(0, Dolly_, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, Dolly_, OBJPROP_BACK, Dolly_GRAPHICS)
    ObjectSetInteger(0, Dolly_, OBJPROP_WIDTH, 2)
    ObjectSetInteger(0, Dolly_, OBJPROP_STYLE, 0)
    ObjectSetInteger(0, Dolly_, OBJPROP_FILL, True)

def CreateAvGraphics(DailyAv, start, end, clr):
    ObjectCreate(0, DailyAv, OBJ_RECTANGLE, 0, iTime(None, PERIOD_D1, 0) + (GMTshift * 3600), start, iTime(None, PERIOD_CURRENT, 0), end)
    ObjectSetInteger(0, DailyAv, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, DailyAv, OBJPROP_BACK, Daily_AverageGRAPHICS)
    ObjectSetInteger(0, DailyAv, OBJPROP_WIDTH, 0)
    ObjectSetInteger(0, DailyAv, OBJPROP_STYLE, 0)
    ObjectSetInteger(0, DailyAv, OBJPROP_FILL, True)

def CreatePivots(Pivots, start, end, w, s, clr):
    ObjectCreate(0, Pivots, OBJ_TRENDBYANGLE, 0, iTime(None, PERIOD_D1, Pivot_Point_ExtendLINE + 0), start, iTime(None, PERIOD_CURRENT, 0), w, s, end)
    ObjectSetInteger(0, Pivots, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, Pivots, OBJPROP_RAY, False)
    ObjectSetInteger(0, Pivots, OBJPROP_WIDTH, w)
    ObjectSetInteger(0, Pivots, OBJPROP_STYLE, s)

def CreateFibs(FibLevels, start, end, w, s, clr):
    ObjectCreate(0, FibLevels, OBJ_TRENDBYANGLE, 0, iTime(None, PERIOD_D1, FIB_ExtendDISPLAY), start, iTime(None, PERIOD_CURRENT, 0), w, s, end)
    ObjectSetInteger(0, FibLevels, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, FibLevels, OBJPROP_RAY, False)
    ObjectSetInteger(0, FibLevels, OBJPROP_WIDTH, w)
    ObjectSetInteger(0, FibLevels, OBJPROP_STYLE, s)

def DeleteCreateFibs():
    ObjectDelete(0, 'Fib100')
    ObjectDelete(0, 'Fib764')
    ObjectDelete(0, 'Fib618')
    ObjectDelete(0, 'Fib50')
    ObjectDelete(0, 'Fib236')
    ObjectDelete(0, 'Fib0')
    ObjectDelete(0, 'Fib382')
    ObjectDelete(0, 'FibP100')
    ObjectDelete(0, 'FibP618')
    ObjectDelete(0, 'FibP50')
    ObjectDelete(0, 'FibP382')
    ObjectDelete(0, 'FibM100')
    ObjectDelete(0, 'FibM618')
    ObjectDelete(0, 'FibM50')
    ObjectDelete(0, 'FibM382')
    ObjectDelete(0, 'FibP236')
    ObjectDelete(0, 'FibM236')
    ObjectDelete(0, 'FibP764')
    ObjectDelete(0, 'FibM764')
    ObjectDelete(0, 'FibP150')
    ObjectDelete(0, 'FibM150')
    ObjectDelete(0, 'FibP200')
    ObjectDelete(0, 'FibM200')
    ObjectDelete(0, 'FibP250')
    ObjectDelete(0, 'FibM250')
    ObjectDelete(0, 'FibP300')
    ObjectDelete(0, 'FibM300')

def CreateFIB():
    global cur_day, day_high, day_low, prev_day, today_open, yesterday_close, yesterday_high, yesterday_low, yesterday_open
    ObjectsDeleteAll(0, -1, OBJ_TRENDBYANGLE)
    DeleteCreateFibs()
    day_high = 0.0
    day_low = 0.0
    yesterday_open = 0.0
    today_open = 0.0
    cur_day = 0.0
    prev_day = 0.0
    cnt = 720
    while cnt != 0:
        tm = MqlDateTime()
        TimeToStruct(iTime(None, PERIOD_CURRENT, cnt), tm)
        if tm.day_of_week == 0:
            cur_day = prev_day
        else:
            tm1 = MqlDateTime()
            TimeToStruct(iTime(None, PERIOD_CURRENT, cnt) - (GMTshift * 3600), tm1)
            cur_day = tm1.day
        if prev_day != cur_day:
            yesterday_close = iClose(None, PERIOD_CURRENT, cnt + 1)
            today_open = iOpen(None, PERIOD_CURRENT, cnt)
            yesterday_high = day_high
            yesterday_low = day_low
            day_high = iHigh(None, PERIOD_CURRENT, cnt)
            day_low = iLow(None, PERIOD_CURRENT, cnt)
            prev_day = cur_day
        if iHigh(None, PERIOD_CURRENT, cnt) > day_high:
            day_high = iHigh(None, PERIOD_CURRENT, cnt)
        if iLow(None, PERIOD_CURRENT, cnt) < day_low:
            day_low = iLow(None, PERIOD_CURRENT, cnt)
        cnt -= 1
    P = (yesterday_high + yesterday_low + yesterday_close) / 3
    r3 = (2 * P) + (yesterday_high - (2 * yesterday_low))
    r2 = P + (yesterday_high - yesterday_low)
    r1 = (2 * P) - yesterday_low
    s1 = (2 * P) - yesterday_high
    s2 = P - (yesterday_high - yesterday_low)
    s3 = (2 * P) - ((2 * yesterday_high) - yesterday_low)
    m0 = (s2 + s3) / 2
    m1 = (s1 + s2) / 2
    m2 = (P + s1) / 2
    m3 = (P + r1) / 2
    m4 = (r1 + r2) / 2
    m5 = (r2 + r3) / 2
    OPEN = today_open
    HI2 = iHigh(None, PERIOD_D1, 0)
    LOW2 = iLow(None, PERIOD_D1, 0)
    HI3 = yesterday_high
    LOW3 = yesterday_low
    HI4 = iHigh(None, PERIOD_D1, 0)
    LOW4 = iLow(None, PERIOD_D1, 0)
    HI5 = iHigh(None, PERIOD_D1, 2)
    LOW5 = iLow(None, PERIOD_D1, 2)
    HI6 = iHigh(None, PERIOD_D1, 3)
    LOW6 = iLow(None, PERIOD_D1, 3)
    HI7 = iHigh(None, PERIOD_D1, 4)
    LOW7 = iLow(None, PERIOD_D1, 4)
    HI8 = iHigh(None, PERIOD_D1, 5)
    LOW8 = iLow(None, PERIOD_D1, 5)
    HI9 = iHigh(None, PERIOD_D1, 6)
    LOW9 = iLow(None, PERIOD_D1, 6)
    HI10 = iHigh(None, PERIOD_D1, 7)
    LOW10 = iLow(None, PERIOD_D1, 7)
    HI11 = iHigh(None, PERIOD_D1, 8)
    LOW11 = iLow(None, PERIOD_D1, 8)
    HI12 = iHigh(None, PERIOD_D1, 9)
    LOW12 = iLow(None, PERIOD_D1, 9)
    HI13 = iHigh(None, PERIOD_D1, 10)
    LOW13 = iLow(None, PERIOD_D1, 10)
    HI14 = iHigh(None, PERIOD_D1, 11)
    LOW14 = iLow(None, PERIOD_D1, 11)
    HI15 = iHigh(None, PERIOD_D1, 12)
    LOW15 = iLow(None, PERIOD_D1, 12)
    HI16 = iHigh(None, PERIOD_D1, 13)
    LOW16 = iLow(None, PERIOD_D1, 13)
    HI17 = iHigh(None, PERIOD_D1, 14)
    LOW17 = iLow(None, PERIOD_D1, 14)
    HI18 = iHigh(None, PERIOD_D1, 15)
    LOW18 = iLow(None, PERIOD_D1, 15)
    HI19 = iHigh(None, PERIOD_D1, 16)
    LOW19 = iLow(None, PERIOD_D1, 16)
    HI20 = iHigh(None, PERIOD_D1, 17)
    LOW20 = iLow(None, PERIOD_D1, 17)
    HI21 = iHigh(None, PERIOD_D1, 18)
    LOW21 = iLow(None, PERIOD_D1, 18)
    HI22 = iHigh(None, PERIOD_D1, 19)
    LOW22 = iLow(None, PERIOD_D1, 19)
    HI23 = iHigh(None, PERIOD_D1, 20)
    LOW23 = iLow(None, PERIOD_D1, 20)
    ONE = HI3 - LOW3
    FIVE = (HI3 - LOW3 + (HI5 - LOW5) + (HI6 - LOW6) + (HI7 - LOW7) + (HI8 - LOW8)) / 5
    TEN = (HI3 - LOW3 + (HI5 - LOW5) + (HI6 - LOW6) + (HI7 - LOW7) + (HI8 - LOW8) + (HI9 - LOW9) + (HI10 - LOW10) + (HI11 - LOW11) + (HI12 - LOW12) + (HI13 - LOW13)) / 10
    TWENTY = (HI3 - LOW3 + (HI5 - LOW5) + (HI6 - LOW6) + (HI7 - LOW7) + (HI8 - LOW8) + (HI9 - LOW9) + (HI10 - LOW10) + (HI11 - LOW11) + (HI12 - LOW12) + (HI13 - LOW13) + (HI14 - LOW14) + (HI15 - LOW15) + (HI16 - LOW16) + (HI17 - LOW17) + (HI18 - LOW18) + (HI19 - LOW19) + (HI20 - LOW20) + (HI21 - LOW21) + (HI22 - LOW22) + (HI23 - LOW23)) / 20
    AV = (ONE + FIVE + TEN + TWENTY) / 4
    DollyOpenGraphics = 0.0
    if Using_OpenGraphics == True:
        DollyOpenGraphics = OPEN
    else:
        DollyOpenGraphics = P
    AvDN150 = DollyOpenGraphics - ((AV / 2) * 3)
    AvUP150 = DollyOpenGraphics + ((AV / 2) * 3)
    AvDN125 = DollyOpenGraphics - ((AV / 4) * 5)
    AvUP125 = DollyOpenGraphics + ((AV / 4) * 5)
    AvDN100 = DollyOpenGraphics - AV
    AvUP100 = DollyOpenGraphics + AV
    AvDN75 = DollyOpenGraphics - ((AV / 4) * 3)
    AvUP75 = DollyOpenGraphics + ((AV / 4) * 3)
    AvDN50 = DollyOpenGraphics - (AV / 2)
    AvUP50 = DollyOpenGraphics + (AV / 2)
    AvDN25 = DollyOpenGraphics - (AV / 4)
    AvUP25 = DollyOpenGraphics + (AV / 4)
    CLOSE = iClose(None, PERIOD_D1, 0)
    F = 0.0
    F = yesterday_high - yesterday_low
    FIBP300 = yesterday_low + (F * 4.0)
    FIBP250 = yesterday_low + (F * 3.5)
    FIBP200 = yesterday_low + (F * 3.0)
    FIBP150 = yesterday_low + (F * 2.5)
    FIBP100 = yesterday_low + (F * 2.0)
    FIBP764 = yesterday_low + (F * 1.764)
    FIBP618 = yesterday_low + (F * 1.618)
    FIBP50 = yesterday_low + (F * 1.5)
    FIBP382 = yesterday_low + (F * 1.382)
    FIBP236 = yesterday_low + (F * 1.236)
    FIB100 = yesterday_high
    FIB764 = yesterday_low + (F * 0.764)
    FIB618 = yesterday_low + (F * 0.618)
    FIB50 = yesterday_low + (F * 0.5)
    FIB382 = yesterday_low + (F * 0.382)
    FIB236 = yesterday_low + (F * 0.236)
    FIB0 = yesterday_low + (F * 0.0)
    FIBM236 = yesterday_low - (F * 0.236)
    FIBM382 = yesterday_low - (F * 0.382)
    FIBM50 = yesterday_low - (F * 0.5)
    FIBM618 = yesterday_low - (F * 0.618)
    FIBM764 = yesterday_low - (F * 0.764)
    FIBM100 = yesterday_low - (F * 1.0)
    FIBM150 = yesterday_low - (F * 1.5)
    FIBM200 = yesterday_low - (F * 2.0)
    FIBM250 = yesterday_low - (F * 2.5)
    FIBM300 = yesterday_low - (F * 3.0)
    B1 = DollyOpenGraphics + (BUY_Area * Point())
    S1 = DollyOpenGraphics - (SELL_Area * Point())
    B2 = DollyOpenGraphics + (BUY_Target_1 * Point())
    S2 = DollyOpenGraphics - (SELL_Target_1 * Point())
    B3 = DollyOpenGraphics + (BUY_Target_2 * Point())
    S3 = DollyOpenGraphics - (SELL_Target_2 * Point())
    ChartRedraw(0)
    if Alert_ON == True:
        if Ask > (B1 - (2 * Point())) and Ask < (B1 + (2 * Point())):
            Alert(Symbol(), ' M', Period(), ' : DOLLY : BUY AREA  @  ' + DoubleToString(B1, Digits()) + '')
        if Bid < (S1 + (2 * Point())) and Bid > (S1 - (2 * Point())):
            Alert(Symbol(), ' M', Period(), ' : DOLLY : SELL AREA  @  ' + DoubleToString(S1, Digits()) + '')
        if Ask > (B2 - (2 * Point())) and Ask < (B2 + (2 * Point())):
            Alert(Symbol(), ' M', Period(), ' : DOLLY : BUY TARGET #1  @  ' + DoubleToString(B2, Digits()) + '')
        if Bid < (S2 + (2 * Point())) and Bid > (S2 - (2 * Point())):
            Alert(Symbol(), ' M', Period(), ' : DOLLY : SELL TARGET #1  @  ' + DoubleToString(S2, Digits()) + '')
        if Ask > (B3 - (2 * Point())) and Ask < (B3 + (2 * Point())):
            Alert(Symbol(), ' M', Period(), ' : DOLLY : BUY TARGET #2  @  ' + DoubleToString(B3, Digits()) + '')
        if Bid < (S3 + (2 * Point())) and Bid > (S3 - (2 * Point())):
            Alert(Symbol(), ' M', Period(), ' : DOLLY : SELL TARGET #2  @  ' + DoubleToString(S3, Digits()) + '')
    Signal = ''
    Signal2 = ''
    Dolly_col = clrWhite
    Dolly_col2 = clrWhite
    if Show_DollyCOMMENTS == True:
        if Auto_Signals == True:
            if Using_OpenGraphics == True:
                Signal = 'Currently Signals Pending .................................'
                Dolly_col = clrCrimson
                if Ask > (B1 - (3 * Point())) and Ask < (B1 + (3 * Point())):
                    Signal = 'OPEN + [' + _str(BUY_Area) + '] @ ' + DoubleToString(B1, Digits()) + '' + ' - TP @ ' + DoubleToString(B1 + (20 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(B1 - (40 * Point()), Digits()) + ''
                    Dolly_col = 0xFAFA00
                if Ask > (B2 - (3 * Point())) and Ask < (B2 + (3 * Point())):
                    Signal = 'BUY Stop : OPEN + [' + _str(BUY_Target_1) + '] @ ' + DoubleToString(B2, Digits()) + '' + ' - TP @ ' + DoubleToString(B2 + (10 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(B2 - (20 * Point()), Digits()) + ''
                    Dolly_col = 0xFAFA00
                if Ask > (B3 - (3 * Point())) and Ask < (B3 + (3 * Point())):
                    Signal = 'BUY Stop : OPEN + [' + _str(BUY_Target_2) + '] @ ' + DoubleToString(B3, Digits()) + '' + ' - TP @ ' + DoubleToString(B3 + (10 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(B3 - (20 * Point()), Digits()) + ''
                    Dolly_col = 0xFAFA00
                if Ask > (AvUP100 - (3 * Point())) and Ask < (AvUP100 + (3 * Point())):
                    Signal = 'Caution approaching Daily Average Range @ ' + DoubleToString(AvUP100, Digits()) + ''
                    Dolly_col = _uint(YellowGreen)
                if Bid > (AvDN100 + (3 * Point())) and Bid < (AvDN100 - (3 * Point())):
                    Signal = 'Caution approaching Daily Average Range @ ' + DoubleToString(AvDN100, Digits()) + ''
                    Dolly_col = _uint(YellowGreen)
                if Bid < (S1 + (3 * Point())) and Bid > (S1 - (3 * Point())):
                    Signal = 'OPEN - [' + _str(SELL_Area) + '] @ ' + DoubleToString(S1, Digits()) + '' + ' - TP @ ' + DoubleToString(S1 - (20 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(S1 + (40 * Point()), Digits()) + ''
                    Dolly_col = 0x0096FA
                if Bid < (S2 + (3 * Point())) and Bid > (S2 - (3 * Point())):
                    Signal = 'SELL Stop : OPEN - [' + _str(SELL_Target_1) + '] @ ' + DoubleToString(S2, Digits()) + '' + ' - TP @ ' + DoubleToString(S2 - (10 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(S2 + (20 * Point()), Digits()) + ''
                    Dolly_col = 0x0096FA
                if Bid < (S3 + (3 * Point())) and Bid > (S3 - (3 * Point())):
                    Signal = 'SELL Stop : OPEN - [' + _str(SELL_Target_2) + '] @ ' + DoubleToString(S3, Digits()) + '' + ' - TP @ ' + DoubleToString(S3 - (10 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(S3 + (20 * Point()), Digits()) + ''
                    Dolly_col = 0x0096FA
                if Bid < (P + (3 * Point())) and Bid > (P - (3 * Point())):
                    Signal = 'Caution possible reversal  PIVOT @ ' + DoubleToString(P, Digits()) + ''
                    Dolly_col = _uint(White)
                if Bid < (OPEN + (2 * Point())) and Bid > (OPEN - (2 * Point())):
                    Signal = 'Caution possible reversal  OPEN @ ' + DoubleToString(OPEN, Digits()) + ''
                    Dolly_col = _uint(White)
                if Bid > S1 and Bid < B1:
                    Signal2 = 'Price Currently between BUY & SELL ZONES'
                    Dolly_col2 = 0x00E6FA
                if Bid <= S1 and Bid > S2:
                    Signal2 = 'Price Currently in SELL ZONE #1'
                    Dolly_col2 = 0x0032FA
                if Bid <= S2 and Bid > S3:
                    Signal2 = 'Price Currently in SELL ZONE #2'
                    Dolly_col2 = 0x005AFA
                if Bid >= B1 and Bid < B2:
                    Signal2 = 'Price Currently in BUY ZONE #1'
                    Dolly_col2 = 0xFA7800
                if Bid >= B2 and Bid < B3:
                    Signal2 = 'Price Currently in BUY ZONE #2'
                    Dolly_col2 = 0xFAB400
                if Bid >= B3 and Bid < AvUP100:
                    Signal2 = 'Price Currently Between BUY ZONE #2 & 100% D/AV'
                    Dolly_col2 = 0xFAFA78
                if Bid <= S3 and Bid > AvDN100:
                    Signal2 = 'Price Currently Between SELL ZONE #2 & 100% D/AV'
                    Dolly_col2 = 0x00FADC
            if Using_OpenGraphics == False:
                Signal = 'Currently Signals Pending .................................'
                Dolly_col = 0x00FAFA
                if Ask > (B1 - (3 * Point())) and Ask < (B1 + (3 * Point())):
                    Signal = 'PIVOT + [' + _str(BUY_Area) + '] @ ' + DoubleToString(B1, Digits()) + '' + ' - TP @ ' + DoubleToString(B1 + (20 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(B1 - (40 * Point()), Digits()) + ''
                    Dolly_col = 0xFAFA00
                if Ask > (B2 - (3 * Point())) and Ask < (B2 + (3 * Point())):
                    Signal = 'BUY Stop : PIVOT + [' + _str(BUY_Target_1) + '] @ ' + DoubleToString(B2, Digits()) + '' + ' - TP @ ' + DoubleToString(B2 + (10 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(B2 - (20 * Point()), Digits()) + ''
                    Dolly_col = 0xFAFA00
                if Ask > (B3 - (3 * Point())) and Ask < (B3 + (3 * Point())):
                    Signal = 'BUY Stop : PIVOT + [' + _str(BUY_Target_2) + '] @ ' + DoubleToString(B3, Digits()) + '' + ' - TP @ ' + DoubleToString(B3 + (10 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(B3 - (20 * Point()), Digits()) + ''
                    Dolly_col = 0xFAFA00
                if Ask > (AvUP100 - (3 * Point())) and Ask < (AvUP100 + (3 * Point())):
                    Signal = 'Caution approaching Daily Average Range @ ' + DoubleToString(AvUP100, Digits()) + ''
                    Dolly_col = _uint(YellowGreen)
                if Bid > (AvDN100 + (3 * Point())) and Bid < (AvDN100 - (3 * Point())):
                    Signal = 'Caution approaching Daily Average Range @ ' + DoubleToString(AvDN100, Digits()) + ''
                    Dolly_col = _uint(YellowGreen)
                if Bid < (S1 + (3 * Point())) and Bid > (S1 - (3 * Point())):
                    Signal = 'PIVOT - [' + _str(SELL_Area) + '] @ ' + DoubleToString(S1, Digits()) + '' + ' - TP @ ' + DoubleToString(S1 - (20 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(S1 + (40 * Point()), Digits()) + ''
                    Dolly_col = 0x0096FA
                if Bid < (S2 + (3 * Point())) and Bid > (S2 - (3 * Point())):
                    Signal = 'SELL Stop : PIVOT - [' + _str(SELL_Target_1) + '] @ ' + DoubleToString(S2, Digits()) + '' + ' - TP @ ' + DoubleToString(S2 - (10 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(S2 + (20 * Point()), Digits()) + ''
                    Dolly_col = 0x0096FA
                if Bid < (S3 + (3 * Point())) and Bid > (S3 - (3 * Point())):
                    Signal = 'SELL Stop : PIVOT - [' + _str(SELL_Target_2) + '] @ ' + DoubleToString(S3, Digits()) + '' + ' - TP @ ' + DoubleToString(S3 - (10 * Point()), Digits()) + '' + ' - SL @ ' + DoubleToString(S3 + (20 * Point()), Digits()) + ''
                    Dolly_col = 0x0096FA
                if Bid < (P + (3 * Point())) and Bid > (P - (3 * Point())):
                    Signal = 'Caution possible reversal  PIVOT @ ' + DoubleToString(P, Digits()) + ''
                    Dolly_col = _uint(White)
                if Bid < (OPEN + (2 * Point())) and Bid > (OPEN - (2 * Point())):
                    Signal = 'Caution possible reversal  OPEN @ ' + DoubleToString(OPEN, Digits()) + ''
                    Dolly_col = _uint(White)
                if Bid > S1 and Bid < B1:
                    Signal2 = 'Price Currently between BUY & SELL ZONES'
                    Dolly_col2 = 0x00E6FA
                if Bid <= S1 and Bid > S2:
                    Signal2 = 'Price Currently in SELL ZONE #1'
                    Dolly_col2 = 0x0032FA
                if Bid <= S2 and Bid > S3:
                    Signal2 = 'Price Currently in SELL ZONE #2'
                    Dolly_col2 = 0x005AFA
                if Bid >= B1 and Bid < B2:
                    Signal2 = 'Price Currently in BUY ZONE #1'
                    Dolly_col2 = 0xFA7800
                if Bid >= B2 and Bid < B3:
                    Signal2 = 'Price Currently in BUY ZONE #2'
                    Dolly_col2 = 0xFAB400
                if Bid >= B3 and Bid < AvUP100:
                    Signal2 = 'Price Currently Between BUY ZONE #2 & 100% D/AV'
                    Dolly_col2 = 0xFAFA78
                if Bid <= S3 and Bid > AvDN100:
                    Signal2 = 'Price Currently Between SELL ZONE #2 & 100% D/AV'
                    Dolly_col2 = 0x00FADC
            ObjectCreate(0, 'Signal', OBJ_LABEL, 0, 0, 0)
            ObjectSetString_(0, 'Signal', Signal, 11, 'Arial Bold', Dolly_col)
            ObjectSetInteger(0, 'Signal', OBJPROP_CORNER, 0)
            ObjectSetInteger(0, 'Signal', OBJPROP_XDISTANCE, 20)
            ObjectSetInteger(0, 'Signal', OBJPROP_YDISTANCE, 65)
            ObjectCreate(0, 'Signal2', OBJ_LABEL, 0, 0, 0)
            ObjectSetString_(0, 'Signal2', Signal2, 11, 'Arial Bold', Dolly_col2)
            ObjectSetInteger(0, 'Signal2', OBJPROP_CORNER, 0)
            ObjectSetInteger(0, 'Signal2', OBJPROP_XDISTANCE, 20)
            ObjectSetInteger(0, 'Signal2', OBJPROP_YDISTANCE, 85)
            ObjectCreate(0, 'Signal1', OBJ_LABEL, 0, 0, 0)
            ObjectSetString_(0, 'Signal1', 'Signal Auto Display', 9, 'Arial', _uint(Silver))
            ObjectSetInteger(0, 'Signal1', OBJPROP_CORNER, 4)
            ObjectSetInteger(0, 'Signal1', OBJPROP_XDISTANCE, 20)
            ObjectSetInteger(0, 'Signal1', OBJPROP_YDISTANCE, 47)
    CreateDollyGraphics('DollyBUY3', B3, B3, 0xD20000)
    CreateDollyGraphics('DollyBUY2', B2, B3, BUY_Color_2)
    CreateDollyGraphics('DollyBUY1', B1, B2, BUY_Color_1)
    CreateDollyGraphics('DollySELL1', S1, S2, SELL_Color_1)
    CreateDollyGraphics('DollySELL2', S2, S3, SELL_Color_2)
    CreateDollyGraphics('DollySELL3', S3, S3, 0x0000E6)
    if Show_DailyAverageGRAPHICS == True:
        CreateAvGraphics('AvBUY150', AvUP150, AvUP125, DAILY_Av_UP_Color_150)
        CreateAvGraphics('AvBUY125', AvUP125, AvUP100, DAILY_Av_UP_Color_125)
        CreateAvGraphics('AvBUY100', AvUP100, AvUP75, DAILY_Av_UP_Color_100)
        CreateAvGraphics('AvBUY75', AvUP75, B3, DAILY_Av_UP_Color_75)
        CreateAvGraphics('AvSELL75', AvDN75, S3, DAILY_Av_DN_Color_75)
        CreateAvGraphics('AvSELL100', AvDN100, AvDN75, DAILY_Av_DN_Color_100)
        CreateAvGraphics('AvSELL125', AvDN100, AvDN125, DAILY_Av_DN_Color_125)
        CreateAvGraphics('AvSELL150', AvDN125, AvDN150, DAILY_Av_DN_Color_150)
    CreatePivots1('P1', P, P, 2, 0, _uint(DimGray))
    if Show_PivotLines == True:
        CreatePivots('PP1', P, P, 2, 1, _uint(Gray))
        CreatePivots('RR3', r3, r3, 1, 0, _uint(Gray))
        CreatePivots('RR2', r2, r2, 1, 0, _uint(Gray))
        CreatePivots('RR1', r1, r1, 1, 0, _uint(Gray))
        CreatePivots('SS1', s1, s1, 1, 0, _uint(Gray))
        CreatePivots('SS2', s2, s2, 1, 0, _uint(Gray))
        CreatePivots('SS3', s3, s3, 1, 0, _uint(Gray))
    if Show_M_PivotLines == True:
        CreatePivots('MM5', m5, m5, 1, 2, _uint(Gray))
        CreatePivots('MM4', m4, m4, 1, 2, _uint(Gray))
        CreatePivots('MM3', m3, m3, 1, 2, _uint(Gray))
        CreatePivots('MM2', m2, m2, 1, 2, _uint(Gray))
        CreatePivots('MM1', m1, m1, 1, 2, _uint(Gray))
        CreatePivots('MM0', m0, m0, 1, 2, _uint(Gray))
    if Show_FibLines == True:
        CreateFibs('FibP100', FIBP100, FIBP100, 1, 0, _uint(Green))
        CreateFibs('FibP764', FIBP764, FIBP764, 1, 0, 0x003500)
        CreateFibs('FibP618', FIBP618, FIBP618, 1, 0, _uint(Green))
        CreateFibs('FibP50', FIBP50, FIBP50, 1, 0, 0x003500)
        CreateFibs('FibP382', FIBP382, FIBP382, 1, 0, _uint(Green))
        CreateFibs('FibP236', FIBP236, FIBP236, 1, 0, 0x003500)
        CreateFibs('Fib100', FIB100, FIB100, 1, 0, 0x00C800)
        CreateFibs('Fib764', FIB764, FIB764, 1, 0, 0x003500)
        CreateFibs('Fib618', FIB618, FIB618, 1, 0, _uint(Green))
        CreateFibs('Fib50', FIB50, FIB50, 1, 0, 0x003500)
        CreateFibs('Fib382', FIB382, FIB382, 1, 0, _uint(Green))
        CreateFibs('Fib236', FIB236, FIB236, 1, 0, 0x003500)
        CreateFibs('Fib0', FIB0, FIB0, 1, 0, 0x00C800)
        CreateFibs('FibM236', FIBM236, FIBM236, 1, 0, 0x003500)
        CreateFibs('FibM382', FIBM382, FIBM382, 1, 0, _uint(Green))
        CreateFibs('FibM50', FIBM50, FIBM50, 1, 0, 0x003500)
        CreateFibs('FibM618', FIBM618, FIBM618, 1, 0, _uint(Green))
        CreateFibs('FibM764', FIBM764, FIBM764, 1, 0, 0x003500)
        CreateFibs('FibM100', FIBM100, FIBM100, 1, 0, _uint(Green))
    if Show_EXTRAFibLines == True:
        CreateFibs('FibP300', FIBP300, FIBP300, 1, 0, _uint(Green))
        CreateFibs('FibP250', FIBP250, FIBP250, 1, 0, _uint(Green))
        CreateFibs('FibP200', FIBP200, FIBP200, 1, 0, _uint(Green))
        CreateFibs('FibP150', FIBP150, FIBP150, 1, 0, _uint(Green))
        CreateFibs('FibM150', FIBM150, FIBM150, 1, 0, _uint(Green))
        CreateFibs('FibM200', FIBM200, FIBM200, 1, 0, _uint(Green))
        CreateFibs('FibM250', FIBM250, FIBM250, 1, 0, _uint(Green))
        CreateFibs('FibM300', FIBM300, FIBM300, 1, 0, _uint(Green))
    if Show_Daily_HI_LOW == True:
        CreatePivots1('DHI', HI3, HI3, 2, 0, _uint(Turquoise))
        CreatePivots1('DLO', LOW3, LOW3, 2, 0, _uint(Turquoise))
        CreatePivots('DDHI', HI3, HI3, 2, 0, _uint(Turquoise))
        CreatePivots('DDLO', LOW3, LOW3, 2, 0, _uint(Turquoise))
    if Show_Daily_OPEN == True or Using_OpenGraphics == True:
        CreatePivots1('DO', OPEN, OPEN, 2, 0, _uint(YellowGreen))
    if ObjectFind(0, 'B1') != 0:
        ObjectCreate(0, 'B1', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), B1)
        ObjectSetString_(0, 'B1', '                        BUY AREA', 8, 'Arial', _uint(DodgerBlue))
        ObjectSetInteger(0, 'B1', OBJPROP_BACK, True)
    else:
        ObjectMove(0, 'B1', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), B1)
    if ObjectFind(0, 'B2') != 0:
        ObjectCreate(0, 'B2', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), B2)
        ObjectSetString_(0, 'B2', '                                   1st BUY TARGET ', 8, 'Arial', _uint(DodgerBlue))
        ObjectSetInteger(0, 'B2', OBJPROP_BACK, True)
    else:
        ObjectMove(0, 'B2', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), B2)
    if ObjectFind(0, 'B3') != 0:
        ObjectCreate(0, 'B3', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), B3)
        ObjectSetString_(0, 'B3', '                             2nd TARGET ', 8, 'Arial', _uint(DodgerBlue))
        ObjectSetInteger(0, 'B3', OBJPROP_BACK, True)
    else:
        ObjectMove(0, 'B3', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), B3)
    if ObjectFind(0, 'S1') != 0:
        ObjectCreate(0, 'S1', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), S1)
        ObjectSetString_(0, 'S1', '                         SELL AREA', 8, 'Arial', _uint(Orange))
        ObjectSetInteger(0, 'S1', OBJPROP_BACK, True)
    else:
        ObjectMove(0, 'S1', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), S1)
    if ObjectFind(0, 'S2') != 0:
        ObjectCreate(0, 'S2', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), S2)
        ObjectSetString_(0, 'S2', '                                   1st SELL TARGET ', 8, 'Arial', _uint(Orange))
        ObjectSetInteger(0, 'S2', OBJPROP_BACK, True)
    else:
        ObjectMove(0, 'S2', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), S2)
    if ObjectFind(0, 'S3') != 0:
        ObjectCreate(0, 'S3', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), S3)
        ObjectSetString_(0, 'S3', '                             2nd TARGET ', 8, 'Arial', _uint(Orange))
        ObjectSetInteger(0, 'S3', OBJPROP_BACK, True)
    else:
        ObjectMove(0, 'S3', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), S3)
    if ObjectFind(0, 'Pivot') != 0:
        ObjectCreate(0, 'Pivot', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), P)
        ObjectSetString_(0, 'Pivot', '                             PIVOT ' + DoubleToString(P, Digits()) + '', 8, 'Arial', _uint(Silver))
        ObjectSetInteger(0, 'Pivot', OBJPROP_BACK, True)
    else:
        ObjectMove(0, 'Pivot', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyText), P)
    if Show_DailyAverageGRAPHICS == True:
        if ObjectFind(0, 'TOP/AV150') != 0:
            ObjectCreate(0, 'TOP/AV150', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP150)
            ObjectSetString_(0, 'TOP/AV150', '                                    150% ', 8, 'Arial', _uint(DeepSkyBlue))
            ObjectSetInteger(0, 'TOP/AV150', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'TOP/AV150', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP150)
        if ObjectFind(0, 'LOW/AV150') != 0:
            ObjectCreate(0, 'LOW/AV150', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN150)
            ObjectSetString_(0, 'LOW/AV150', '                                    150% ', 8, 'Arial', _uint(Green))
            ObjectSetInteger(0, 'LOW/AV150', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'LOW/AV150', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN150)
        if ObjectFind(0, 'TOP/AV125') != 0:
            ObjectCreate(0, 'TOP/AV125', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP125)
            ObjectSetString_(0, 'TOP/AV125', '                                    125% ', 8, 'Arial', _uint(DeepSkyBlue))
            ObjectSetInteger(0, 'TOP/AV125', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'TOP/AV125', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP125)
        if ObjectFind(0, 'LOW/AV125') != 0:
            ObjectCreate(0, 'LOW/AV125', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN125)
            ObjectSetString_(0, 'LOW/AV125', '                                    125% ', 8, 'Arial', _uint(Green))
            ObjectSetInteger(0, 'LOW/AV125', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'LOW/AV125', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN125)
        if ObjectFind(0, 'TOP/AV100') != 0:
            ObjectCreate(0, 'TOP/AV100', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP100)
            ObjectSetString_(0, 'TOP/AV100', '                                   100%', 8, 'Arial', _uint(DeepSkyBlue))
            ObjectSetInteger(0, 'TOP/AV100', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'TOP/AV100', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP100)
        if ObjectFind(0, 'LOW/AV100') != 0:
            ObjectCreate(0, 'LOW/AV100', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN100)
            ObjectSetString_(0, 'LOW/AV100', '                                    100% ', 8, 'Arial', _uint(Green))
            ObjectSetInteger(0, 'LOW/AV100', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'LOW/AV100', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN100)
        if ObjectFind(0, 'TOP/AV75') != 0:
            ObjectCreate(0, 'TOP/AV75', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP75)
            ObjectSetString_(0, 'TOP/AV75', '                                      75% ', 8, 'Arial', _uint(DeepSkyBlue))
            ObjectSetInteger(0, 'TOP/AV75', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'TOP/AV75', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP75)
        if ObjectFind(0, 'LOW/AV75') != 0:
            ObjectCreate(0, 'LOW/AV75', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN75)
            ObjectSetString_(0, 'LOW/AV75', '                                     75%', 8, 'Arial', _uint(Green))
            ObjectSetInteger(0, 'LOW/AV75', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'LOW/AV75', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN75)
        if ObjectFind(0, 'LOW/AV50') != 0:
            ObjectCreate(0, 'LOW/AV50', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP50)
            ObjectSetString_(0, 'LOW/AV50', '                                       50% ', 8, 'Arial', _uint(DeepSkyBlue))
            ObjectSetInteger(0, 'LOW/AV50', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'LOW/AV50', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP50)
        if ObjectFind(0, 'TOP/AV50') != 0:
            ObjectCreate(0, 'TOP/AV50', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN50)
            ObjectSetString_(0, 'TOP/AV50', '                                      50% ', 8, 'Arial', _uint(Green))
            ObjectSetInteger(0, 'TOP/AV50', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'TOP/AV50', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN50)
        if ObjectFind(0, 'TOP/AV25') != 0:
            ObjectCreate(0, 'TOP/AV25', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP25)
            ObjectSetString_(0, 'TOP/AV25', '                                      25% ', 8, 'Arial', _uint(DeepSkyBlue))
            ObjectSetInteger(0, 'TOP/AV25', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'TOP/AV25', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvUP25)
        if ObjectFind(0, 'LOW/AV25') != 0:
            ObjectCreate(0, 'LOW/AV25', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN25)
            ObjectSetString_(0, 'LOW/AV25', '                                      25% ', 8, 'Arial', _uint(Green))
            ObjectSetInteger(0, 'LOW/AV25', OBJPROP_BACK, True)
        else:
            ObjectMove(0, 'LOW/AV25', 0, iTime(None, PERIOD_CURRENT, SHIFT_DailyAverageText), AvDN25)
    if Show_PivotLines == True:
        if ObjectFind(0, 'C/PIVOT') != 0:
            ObjectCreate(0, 'C/PIVOT', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), P)
            ObjectSetString_(0, 'C/PIVOT', 'P', 8, 'Arial', _uint(Silver))
        else:
            ObjectMove(0, 'C/PIVOT', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), P)
        if ObjectFind(0, 'R3') != 0:
            ObjectCreate(0, 'R3', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), r3)
            ObjectSetString_(0, 'R3', 'R3', 8, 'Arial', _uint(Silver))
        else:
            ObjectMove(0, 'R3', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), r3)
        if ObjectFind(0, 'R2') != 0:
            ObjectCreate(0, 'R2', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), r2)
            ObjectSetString_(0, 'R2', 'R2', 8, 'Arial', _uint(Silver))
        else:
            ObjectMove(0, 'R2', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), r2)
        if ObjectFind(0, 'R1') != 0:
            ObjectCreate(0, 'R1', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), r1)
            ObjectSetString_(0, 'R1', 'R1', 8, 'Arial', _uint(Silver))
        else:
            ObjectMove(0, 'R1', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), r1)
        if ObjectFind(0, 'PS1') != 0:
            ObjectCreate(0, 'PS1', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), s1)
            ObjectSetString_(0, 'PS1', 'S1', 8, 'Arial', _uint(Silver))
        else:
            ObjectMove(0, 'PS1', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), s1)
        if ObjectFind(0, 'PS2') != 0:
            ObjectCreate(0, 'PS2', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), s2)
            ObjectSetString_(0, 'PS2', 'S2', 8, 'Arial', _uint(Silver))
        else:
            ObjectMove(0, 'PS2', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), s2)
        if ObjectFind(0, 'PS3') != 0:
            ObjectCreate(0, 'PS3', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), s3)
            ObjectSetString_(0, 'PS3', 'S3', 8, 'Arial', _uint(Silver))
        else:
            ObjectMove(0, 'PS3', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), s3)
        if Show_M_PivotLines == True:
            if ObjectFind(0, 'M5') != 0:
                ObjectCreate(0, 'M5', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m5)
                ObjectSetString_(0, 'M5', 'M5', 8, 'Arial', _uint(Silver))
            else:
                ObjectMove(0, 'M5', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m5)
            if ObjectFind(0, 'M4') != 0:
                ObjectCreate(0, 'M4', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m4)
                ObjectSetString_(0, 'M4', 'M4', 8, 'Arial', _uint(Silver))
            else:
                ObjectMove(0, 'M4', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m4)
            if ObjectFind(0, 'M3') != 0:
                ObjectCreate(0, 'M3', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m3)
                ObjectSetString_(0, 'M3', 'M3', 8, 'Arial', _uint(Silver))
            else:
                ObjectMove(0, 'M3', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m3)
            if ObjectFind(0, 'M2') != 0:
                ObjectCreate(0, 'M2', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m2)
                ObjectSetString_(0, 'M2', 'M2', 8, 'Arial', _uint(Silver))
            else:
                ObjectMove(0, 'M2', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m2)
            if ObjectFind(0, 'M1') != 0:
                ObjectCreate(0, 'M1', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m1)
                ObjectSetString_(0, 'M1', 'M1', 8, 'Arial', _uint(Silver))
            else:
                ObjectMove(0, 'M1', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m1)
            if ObjectFind(0, 'M0') != 0:
                ObjectCreate(0, 'M0', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m0)
                ObjectSetString_(0, 'M0', 'M0', 8, 'Arial', _uint(Silver))
            else:
                ObjectMove(0, 'M0', 0, iTime(None, PERIOD_CURRENT, SHIFT_Pivot_PointText), m0)
    if Show_FibLines == True:
        if ObjectFind(0, 'FIB') != 0:
            ObjectCreate(0, 'FIB', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB100)
            ObjectSetString_(0, 'FIB', 'FIB 100% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB100)
        if ObjectFind(0, 'FIB2') != 0:
            ObjectCreate(0, 'FIB2', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB50)
            ObjectSetString_(0, 'FIB2', 'FIB 50% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB2', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB50)
        if ObjectFind(0, 'FIB3') != 0:
            ObjectCreate(0, 'FIB3', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB0)
            ObjectSetString_(0, 'FIB3', 'FIB 0.00% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB3', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB0)
        if ObjectFind(0, 'FIB4') != 0:
            ObjectCreate(0, 'FIB4', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB382)
            ObjectSetString_(0, 'FIB4', 'FIB 0.382% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB4', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB382)
        if ObjectFind(0, 'FIB5') != 0:
            ObjectCreate(0, 'FIB5', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB618)
            ObjectSetString_(0, 'FIB5', 'FIB 0.618% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB5', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB618)
        if ObjectFind(0, 'FIB6') != 0:
            ObjectCreate(0, 'FIB6', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP50)
            ObjectSetString_(0, 'FIB6', 'FIB +1.50% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB6', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP50)
        if ObjectFind(0, 'FIB7') != 0:
            ObjectCreate(0, 'FIB7', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP100)
            ObjectSetString_(0, 'FIB7', 'FIB +200% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB7', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP100)
        if ObjectFind(0, 'FIB8') != 0:
            ObjectCreate(0, 'FIB8', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM50)
            ObjectSetString_(0, 'FIB8', 'FIB -1.50% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB8', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM50)
        if ObjectFind(0, 'FIB9') != 0:
            ObjectCreate(0, 'FIB9', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM100)
            ObjectSetString_(0, 'FIB9', 'FIB -200% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB9', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM100)
        if ObjectFind(0, 'FIB10') != 0:
            ObjectCreate(0, 'FIB10', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP382)
            ObjectSetString_(0, 'FIB10', 'FIB +1.382% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB10', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP382)
        if ObjectFind(0, 'FIB11') != 0:
            ObjectCreate(0, 'FIB11', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM382)
            ObjectSetString_(0, 'FIB11', 'FIB -1.382% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB11', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM382)
        if ObjectFind(0, 'FIB12') != 0:
            ObjectCreate(0, 'FIB12', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP618)
            ObjectSetString_(0, 'FIB12', 'FIB +1.618% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB12', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP618)
        if ObjectFind(0, 'FIB13') != 0:
            ObjectCreate(0, 'FIB13', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM618)
            ObjectSetString_(0, 'FIB13', 'FIB -1.618% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB13', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM618)
        if ObjectFind(0, 'FIB14') != 0:
            ObjectCreate(0, 'FIB14', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB764)
            ObjectSetString_(0, 'FIB14', 'FIB 0.764% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB14', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB764)
        if ObjectFind(0, 'FIB15') != 0:
            ObjectCreate(0, 'FIB15', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB236)
            ObjectSetString_(0, 'FIB15', 'FIB 0.236% ', 8, 'Arial', _uint(Green))
        else:
            ObjectMove(0, 'FIB15', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIB236)
        if ObjectFind(0, 'FIB16') != 0:
            ObjectCreate(0, 'FIB16', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM236)
            ObjectSetString_(0, 'FIB16', 'FIB -1.236% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB16', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM236)
        if ObjectFind(0, 'FIB17') != 0:
            ObjectCreate(0, 'FIB17', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP236)
            ObjectSetString_(0, 'FIB17', 'FIB +1.236% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB17', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP236)
        if ObjectFind(0, 'FIB18') != 0:
            ObjectCreate(0, 'FIB18', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM764)
            ObjectSetString_(0, 'FIB18', 'FIB -1.764% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB18', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM764)
        if ObjectFind(0, 'FIB19') != 0:
            ObjectCreate(0, 'FIB19', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP764)
            ObjectSetString_(0, 'FIB19', 'FIB +1.764% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB19', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP764)
    if Show_EXTRAFibLines == True:
        if ObjectFind(0, 'FIB120') != 0:
            ObjectCreate(0, 'FIB20', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP150)
            ObjectSetString_(0, 'FIB20', 'FIB +250% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB20', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP150)
        if ObjectFind(0, 'FIB21') != 0:
            ObjectCreate(0, 'FIB21', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM150)
            ObjectSetString_(0, 'FIB21', 'FIB -250% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB21', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM150)
        if ObjectFind(0, 'FIB122') != 0:
            ObjectCreate(0, 'FIB22', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP200)
            ObjectSetString_(0, 'FIB22', 'FIB +300% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB22', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP200)
        if ObjectFind(0, 'FIB23') != 0:
            ObjectCreate(0, 'FIB23', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM200)
            ObjectSetString_(0, 'FIB23', 'FIB -300% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB23', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM200)
        if ObjectFind(0, 'FIB124') != 0:
            ObjectCreate(0, 'FIB24', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP250)
            ObjectSetString_(0, 'FIB24', 'FIB +350% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB24', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP250)
        if ObjectFind(0, 'FIB25') != 0:
            ObjectCreate(0, 'FIB25', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM250)
            ObjectSetString_(0, 'FIB25', 'FIB -350% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB25', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM250)
        if ObjectFind(0, 'FIB126') != 0:
            ObjectCreate(0, 'FIB26', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP300)
            ObjectSetString_(0, 'FIB26', 'FIB +400% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB26', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBP300)
        if ObjectFind(0, 'FIB27') != 0:
            ObjectCreate(0, 'FIB27', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM300)
            ObjectSetString_(0, 'FIB27', 'FIB -400% ', 8, 'Arial', 0x005D00)
        else:
            ObjectMove(0, 'FIB27', 0, iTime(None, PERIOD_CURRENT, SHIFT_FibText), FIBM300)
    if Show_Daily_HI_LOW == True:
        if ObjectFind(0, 'DHIGH') != 0:
            ObjectCreate(0, 'DHIGH', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_HI_LOW_TEXT), HI3)
            ObjectSetString_(0, 'DHIGH', 'Daily High ', 8, 'Arial', _uint(Turquoise))
        else:
            ObjectMove(0, 'DHIGH', 0, iTime(None, PERIOD_CURRENT, SHIFT_HI_LOW_TEXT), HI3)
        if ObjectFind(0, 'DLOW') != 0:
            ObjectCreate(0, 'DLOW', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_HI_LOW_TEXT), LOW3)
            ObjectSetString_(0, 'DLOW', 'Daily Low ', 8, 'Arial', _uint(Turquoise))
        else:
            ObjectMove(0, 'DLOW', 0, iTime(None, PERIOD_CURRENT, SHIFT_HI_LOW_TEXT), LOW3)
    if Show_Daily_OPEN == True or Using_OpenGraphics == True:
        if ObjectFind(0, 'Open') != 0:
            ObjectCreate(0, 'Open', OBJ_TEXT, 0, iTime(None, PERIOD_CURRENT, SHIFT_Daily_OPEN_TEXT), OPEN)
            ObjectSetString_(0, 'Open', '                            OPEN ' + DoubleToString(OPEN, Digits()) + '', 8, 'Arial Bold', _uint(YellowGreen))
        else:
            ObjectMove(0, 'Open', 0, iTime(None, PERIOD_CURRENT, SHIFT_Daily_OPEN_TEXT), OPEN)
    PRICE = ""
    OPEN1 = ""
    DAR = ""
    if Show_DollyCOMMENTS == True:
        NAME = ""
        BUYSTOP = ""
        BUYSTOP1 = ""
        STOP = ""
        STOP1 = ""
        PROFIT = ""
        PROFIT1 = ""
        SELL = ""
        SELL1 = ""
        STOP2 = ""
        STOP3 = ""
        PROFIT2 = ""
        PROFIT3 = ""
        BUYTARGT = ""
        PROFIT4 = ""
        SELLTARGT = ""
        PROFIT5 = ""
        TOTAL = ""
        TDR = ""
        LDR = ""
        TIME = ""
        TIME2 = ""
        CHANGE = ""
        TDR1 = ""
        LDR1 = ""
        STOP4 = ""
        STOP5 = ""
        ChangeVal = Bid - iOpen(Symbol(), PERIOD_D1, 0)
        NAME = 'Dolly Graphics #11 GMT Shift'
        BUYSTOP = DoubleToString(B1, Digits())
        BUYSTOP1 = DoubleToString(B2, Digits())
        STOP = DoubleToString(S1, Digits())
        STOP1 = DoubleToString(B1, Digits())
        PROFIT = DoubleToString(B2, Digits())
        PROFIT1 = DoubleToString(B3, Digits())
        SELL = DoubleToString(S1, Digits())
        SELL1 = DoubleToString(S2, Digits())
        STOP2 = DoubleToString(B1, Digits())
        STOP3 = DoubleToString(S1, Digits())
        PROFIT2 = DoubleToString(S2, Digits())
        PROFIT3 = DoubleToString(S3, Digits())
        BUYTARGT = DoubleToString(S2, Digits())
        PROFIT4 = DoubleToString(B1, Digits())
        STOP4 = DoubleToString(S3, Digits())
        SELLTARGT = DoubleToString(B2, Digits())
        PROFIT5 = DoubleToString(S1, Digits())
        STOP5 = DoubleToString(B3, Digits())
        OPEN1 = DoubleToString(OPEN, Digits())
        DAR = DoubleToString(_fdiv(AV, Point()), 0)
        TOTAL = DoubleToString(HI2 - LOW2, Digits())
        TDR = DoubleToString(P + AV, Digits())
        LDR = DoubleToString(P - AV, Digits())
        TDR1 = DoubleToString(P + (AV / 2), Digits())
        LDR1 = DoubleToString(P - (AV / 2), Digits())
        TIME = TimeToString(TimeLocal(), Digits() - 6)
        TIME2 = TimeToString(TimeCurrent(), Digits() - 6)
        PRICE = DoubleToString(PriceSeries(PRICE_CLOSE, 0), Digits())
        CHANGE = DoubleToString(ChangeVal, Digits())
        ObjectDelete(0, 'Dolly')
        Dolly('Dolly', 22, 12, 4)
        ObjectSetString_(0, 'Dolly', '' + NAME + '', 11, 'Arial', _uint(Red))
        ObjectDelete(0, 'Dolly1')
        Dolly1('Dolly1', 35, 12, 4)
        ObjectSetString_(0, 'Dolly1', ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', 8, 'Arial', _uint(Black))
        if Auto_Signals == False:
            ObjectDelete(0, 'Dolly2')
            Dolly2('Dolly2', 50, 12, 4)
            ObjectSetString_(0, 'Dolly2', 'BUY ZONE', 9, 'Arial', _uint(DeepSkyBlue))
            ObjectDelete(0, 'Dolly3')
            Dolly3('Dolly3', 60, 12, 4)
            ObjectSetString_(0, 'Dolly3', ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', 8, 'Arial', _uint(Black))
            ObjectDelete(0, 'Dolly4')
            Dolly4('Dolly4', 75, 12, 4)
            ObjectSetString_(0, 'Dolly4', 'BUY STOP-1  ' + Symbol() + '  @ ', 9, 'Arial', _uint(DodgerBlue))
            ObjectDelete(0, 'Dolly5')
            Dolly5('Dolly5', 75, 12, 4)
            ObjectSetString_(0, 'Dolly5', ' ' + BUYSTOP + '', 9, 'Arial', _uint(DarkOrange))
            ObjectDelete(0, 'Dolly6')
            Dolly6('Dolly6', 90, 12, 4)
            ObjectSetString_(0, 'Dolly6', 'TP               and SL @    ', 9, 'Arial', _uint(DodgerBlue))
            ObjectDelete(0, 'Dolly7')
            Dolly7('Dolly7', 90, 12, 4)
            ObjectSetString_(0, 'Dolly7', ' ' + BUYSTOP1 + '', 9, 'Arial', _uint(YellowGreen))
            ObjectDelete(0, 'Dolly8')
            Dolly8('Dolly8', 90, 12, 4)
            ObjectSetString_(0, 'Dolly8', ' ' + STOP + '', 9, 'Arial', _uint(CornflowerBlue))
            ObjectDelete(0, 'Dolly9')
            Dolly9('Dolly9', 110, 12, 4)
            ObjectSetString_(0, 'Dolly9', 'BUY STOP-2  ' + Symbol() + '  @ ', 9, 'Arial', _uint(LightBlue))
            ObjectDelete(0, 'Dolly10')
            Dolly10('Dolly10', 110, 12, 4)
            ObjectSetString_(0, 'Dolly10', ' ' + BUYSTOP1 + '', 9, 'Arial', _uint(DarkOrange))
            ObjectDelete(0, 'Dolly11')
            Dolly11('Dolly11', 125, 12, 4)
            ObjectSetString_(0, 'Dolly11', 'TP               and SL @    ', 9, 'Arial', _uint(LightBlue))
            ObjectDelete(0, 'Dolly12')
            Dolly12('Dolly12', 125, 12, 4)
            ObjectSetString_(0, 'Dolly12', ' ' + PROFIT1 + '', 9, 'Arial', _uint(YellowGreen))
            ObjectDelete(0, 'Dolly13')
            Dolly13('Dolly13', 125, 12, 4)
            ObjectSetString_(0, 'Dolly13', '' + STOP1 + '', 9, 'Arial', _uint(Red))
            ObjectDelete(0, 'Dolly14')
            Dolly14('Dolly14', 140, 12, 4)
            ObjectSetString_(0, 'Dolly14', ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', 8, 'Arial', _uint(Black))
            ObjectDelete(0, 'Dolly15')
            Dolly15('Dolly15', 155, 12, 4)
            ObjectSetString_(0, 'Dolly15', 'SELL ZONE', 9, 'Arial', _uint(Maroon))
            ObjectDelete(0, 'Dolly16')
            Dolly16('Dolly16', 165, 12, 4)
            ObjectSetString_(0, 'Dolly16', ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', 8, 'Arial', _uint(Black))
            ObjectDelete(0, 'Dolly17')
            Dolly17('Dolly17', 180, 12, 4)
            ObjectSetString_(0, 'Dolly17', 'SELL STOP-1  ' + Symbol() + '  to ', 9, 'Arial', _uint(OrangeRed))
            ObjectDelete(0, 'Dolly18')
            Dolly18('Dolly18', 180, 12, 4)
            ObjectSetString_(0, 'Dolly18', ' ' + SELL + '', 9, 'Arial', _uint(DarkOrange))
            ObjectDelete(0, 'Dolly19')
            Dolly19('Dolly19', 195, 12, 4)
            ObjectSetString_(0, 'Dolly19', 'TP               and SL @    ', 9, 'Arial', _uint(OrangeRed))
            ObjectDelete(0, 'Dolly20')
            Dolly20('Dolly20', 195, 12, 4)
            ObjectSetString_(0, 'Dolly20', ' ' + PROFIT2 + '', 9, 'Arial', _uint(YellowGreen))
            ObjectDelete(0, 'Dolly21')
            Dolly21('Dolly21', 195, 12, 4)
            ObjectSetString_(0, 'Dolly21', ' ' + STOP1 + ' ', 9, 'Arial', _uint(Yellow))
            ObjectDelete(0, 'Dolly22')
            Dolly22('Dolly22', 215, 12, 4)
            ObjectSetString_(0, 'Dolly22', 'SELL STOP-2  ' + Symbol() + '  to ', 9, 'Arial', _uint(OrangeRed))
            ObjectDelete(0, 'Dolly23')
            Dolly23('Dolly23', 215, 12, 4)
            ObjectSetString_(0, 'Dolly23', ' ' + SELL1 + '', 9, 'Arial', _uint(DarkOrange))
            ObjectDelete(0, 'Dolly24')
            Dolly24('Dolly24', 230, 12, 4)
            ObjectSetString_(0, 'Dolly24', 'TP               and SL @    ', 9, 'Arial', _uint(OrangeRed))
            ObjectDelete(0, 'Dolly25')
            Dolly25('Dolly25', 230, 12, 4)
            ObjectSetString_(0, 'Dolly25', ' ' + PROFIT3 + '', 9, 'Arial', _uint(YellowGreen))
            ObjectDelete(0, 'Dolly26')
            Dolly26('Dolly26', 230, 12, 4)
            ObjectSetString_(0, 'Dolly26', ' ' + STOP3 + ' ', 9, 'Arial', _uint(Yellow))
            ObjectDelete(0, 'Dolly27')
            Dolly27('Dolly27', 245, 12, 4)
            ObjectSetString_(0, 'Dolly27', ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', 8, 'Arial', _uint(Black))
            ObjectDelete(0, 'Dolly28')
            Dolly28('Dolly28', 260, 12, 4)
            ObjectSetString_(0, 'Dolly28', 'POTENTIAL REVERSAL LEVELS', 9, 'Arial', _uint(DarkSeaGreen))
            ObjectDelete(0, 'Dolly29')
            Dolly29('Dolly29', 270, 12, 4)
            ObjectSetString_(0, 'Dolly29', ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', 8, 'Arial', _uint(Black))
            ObjectDelete(0, 'Dolly30')
            Dolly30('Dolly30', 285, 12, 4)
            ObjectSetString_(0, 'Dolly30', 'BEARISH CORRECTION : ', 9, 'Arial', _uint(DeepSkyBlue))
            ObjectDelete(0, 'Dolly31')
            Dolly31('Dolly31', 300, 12, 4)
            ObjectSetString_(0, 'Dolly31', 'BUY STOP ' + Symbol() + '  @ ', 9, 'Arial', _uint(DodgerBlue))
            ObjectDelete(0, 'Dolly32')
            Dolly32('Dolly32', 300, 12, 4)
            ObjectSetString_(0, 'Dolly32', ' ' + BUYTARGT + '', 9, 'Arial', _uint(DarkOrange))
            ObjectDelete(0, 'Dolly33')
            Dolly33('Dolly33', 315, 12, 4)
            ObjectSetString_(0, 'Dolly33', 'TP               and SL @    ', 9, 'Arial', _uint(DodgerBlue))
            ObjectDelete(0, 'Dolly34')
            Dolly34('Dolly34', 315, 12, 4)
            ObjectSetString_(0, 'Dolly34', ' ' + PROFIT4 + '', 9, 'Arial', _uint(YellowGreen))
            ObjectDelete(0, 'Dolly35')
            Dolly35('Dolly35', 315, 12, 4)
            ObjectSetString_(0, 'Dolly35', ' ' + STOP4 + ' ', 9, 'Arial', _uint(Yellow))
            ObjectDelete(0, 'Dolly36')
            Dolly36('Dolly36', 335, 12, 4)
            ObjectSetString_(0, 'Dolly36', 'BULLISH CORRECTION : ', 9, 'Arial', _uint(Orange))
            ObjectDelete(0, 'Dolly37')
            Dolly37('Dolly37', 350, 12, 4)
            ObjectSetString_(0, 'Dolly37', 'SELL STOP ' + Symbol() + '  @ ', 9, 'Arial', _uint(OrangeRed))
            ObjectDelete(0, 'Dolly38')
            Dolly38('Dolly38', 350, 12, 4)
            ObjectSetString_(0, 'Dolly38', ' ' + SELLTARGT + '', 9, 'Arial', _uint(DarkOrange))
            ObjectDelete(0, 'Dolly39')
            Dolly39('Dolly39', 365, 12, 4)
            ObjectSetString_(0, 'Dolly39', 'TP               and SL @    ', 9, 'Arial', _uint(OrangeRed))
            ObjectDelete(0, 'Dolly40')
            Dolly40('Dolly40', 365, 12, 4)
            ObjectSetString_(0, 'Dolly40', ' ' + PROFIT5 + '', 9, 'Arial', _uint(YellowGreen))
            ObjectDelete(0, 'Dolly41')
            Dolly41('Dolly41', 365, 12, 4)
            ObjectSetString_(0, 'Dolly41', ' ' + STOP5 + ' ', 9, 'Arial', _uint(Yellow))
            ObjectDelete(0, 'Dolly42')
            Dolly42('Dolly42', 380, 12, 4)
            ObjectSetString_(0, 'Dolly42', ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', 8, 'Arial', _uint(Black))
            ObjectDelete(0, 'Dolly43')
            Dolly43('Dolly43', 395, 12, 4)
            ObjectSetString_(0, 'Dolly43', 'DAILY OPEN', 9, 'Arial', _uint(Orange))
            ObjectDelete(0, 'Dolly44')
            Dolly44('Dolly44', 395, 12, 4)
            ObjectSetString_(0, 'Dolly44', ' ' + OPEN1 + '', 9, 'Arial', _uint(YellowGreen))
            ObjectDelete(0, 'Dolly45')
            Dolly45('Dolly45', 410, 12, 4)
            ObjectSetString_(0, 'Dolly45', 'DAILY AVERAGE RANGE ', 9, 'Arial', _uint(DarkSeaGreen))
            ObjectDelete(0, 'Dolly46')
            Dolly46('Dolly46', 410, 12, 4)
            ObjectSetString_(0, 'Dolly46', ' ' + DAR + ' ', 9, 'Arial', _uint(DarkOrange))
            ObjectDelete(0, 'Dolly47')
            Dolly47('Dolly47', 420, 12, 4)
            ObjectSetString_(0, 'Dolly47', ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', 8, 'Arial', _uint(Black))
            ObjectDelete(0, 'Dolly48')
            Dolly48('Dolly48', 435, 12, 4)
            ObjectSetString_(0, 'Dolly48', 'Price', 10, 'Arial', _uint(Silver))
            ObjectDelete(0, 'Dolly49')
            Dolly49('Dolly49', 435, 12, 4)
            ObjectSetString_(0, 'Dolly49', ' ' + PRICE + ' ', 15, 'Arial', _uint(Silver))
        ObjectDelete(0, 'Dolly50')
        Dolly50('Dolly50', 10, 12, 4)
        ObjectSetString_(0, 'Dolly50', 'Change', 10, 'Arial', _uint(Silver))
        ObjectDelete(0, 'Dolly51')
        Dolly51('Dolly51', 18, 12, 4)
        if ChangeVal == 0:
            ObjectSetString_(0, 'Dolly51', '+' + CHANGE + ' ', 15, 'Arial', _uint(Gold))
        elif ChangeVal > 0:
            ObjectSetString_(0, 'Dolly51', '+' + CHANGE + ' ', 15, 'Arial', _uint(Lime))
        else:
            ObjectSetString_(0, 'Dolly51', ' ' + CHANGE + ' ', 15, 'Arial', _uint(Red))
    if Auto_Signals == True:
        if Show_DollyCOMMENTS == True:
            ObjectDelete(0, 'Dolly42')
            Dolly42('Dolly42', 98, 12, 4)
            ObjectSetString_(0, 'Dolly42', ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', 8, 'Arial', _uint(Black))
            ObjectDelete(0, 'Dolly43')
            Dolly43('Dolly43', 112, 12, 4)
            ObjectSetString_(0, 'Dolly43', 'DAILY OPEN', 9, 'Arial', _uint(Orange))
            ObjectDelete(0, 'Dolly44')
            Dolly44('Dolly44', 112, 12, 4)
            ObjectSetString_(0, 'Dolly44', ' ' + OPEN1 + '', 9, 'Arial', _uint(YellowGreen))
            ObjectDelete(0, 'Dolly45')
            Dolly45('Dolly45', 125, 12, 4)
            ObjectSetString_(0, 'Dolly45', 'DAILY AVERAGE RANGE ', 9, 'Arial', _uint(DarkSeaGreen))
            ObjectDelete(0, 'Dolly46')
            Dolly46('Dolly46', 125, 12, 4)
            ObjectSetString_(0, 'Dolly46', ' ' + DAR + ' ', 9, 'Arial', _uint(DarkOrange))
            ObjectDelete(0, 'Dolly47')
            Dolly47('Dolly47', 134, 12, 4)
            ObjectSetString_(0, 'Dolly47', ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', 8, 'Arial', _uint(Black))
            ObjectDelete(0, 'Dolly48')
            Dolly48('Dolly48', 148, 12, 4)
            ObjectSetString_(0, 'Dolly48', 'Price', 10, 'Arial', _uint(Silver))
            ObjectDelete(0, 'Dolly49')
            Dolly49('Dolly49', 148, 12, 4)
            ObjectSetString_(0, 'Dolly49', ' ' + PRICE + ' ', 15, 'Arial', _uint(Silver))

def ObjectSetString_(chart_ID, name, text, textsize, font, Color):
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, textsize)

def Dolly(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly1(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly2(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly3(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly4(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly5(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 170)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly6(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly7(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 35)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly8(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 140)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly9(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly10(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 170)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly11(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly12(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 35)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly13(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 140)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly14(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly15(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly16(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly17(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly18(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 170)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly19(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly20(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 35)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly21(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 140)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly22(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly23(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 170)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly24(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly25(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 35)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly26(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 140)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly27(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly28(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly29(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly30(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly31(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly32(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 170)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly33(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly34(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 35)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly35(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 140)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly36(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly37(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly38(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 170)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly39(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly40(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 35)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly41(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 140)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly42(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly43(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly44(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 100)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly45(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly46(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 160)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly47(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly48(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 20)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly49(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 50)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly50(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 850)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def Dolly51(Text, xOffset, yOffset, iCorner):
    ObjectCreate(0, Text, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, Text, OBJPROP_CORNER, iCorner)
    ObjectSetInteger(0, Text, OBJPROP_XDISTANCE, 885)
    ObjectSetInteger(0, Text, OBJPROP_YDISTANCE, xOffset)
    ObjectSetInteger(0, Text, OBJPROP_BACK, True)

def PriceSeries(applied_price, bar):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return iClose(None, PERIOD_CURRENT, bar)
    elif _sw1 == PRICE_OPEN:
        return iOpen(None, PERIOD_CURRENT, bar)
    elif _sw1 == PRICE_HIGH:
        return iHigh(None, PERIOD_CURRENT, bar)
    elif _sw1 == PRICE_LOW:
        return iLow(None, PERIOD_CURRENT, bar)
    elif _sw1 == PRICE_MEDIAN:
        return (iHigh(None, PERIOD_CURRENT, bar) + iLow(None, PERIOD_CURRENT, bar)) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (iClose(None, PERIOD_CURRENT, bar) + iHigh(None, PERIOD_CURRENT, bar) + iLow(None, PERIOD_CURRENT, bar)) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * iClose(None, PERIOD_CURRENT, bar)) + iHigh(None, PERIOD_CURRENT, bar) + iLow(None, PERIOD_CURRENT, bar)) / 4.0
    return iClose(None, PERIOD_CURRENT, bar)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DollyGraphicsV11GMTShift(_MQL5Indicator):
    name = 'Dolly_Graphics_v11-GMTShift'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'GMTshift': 0,
        'Using_OpenGraphics': True,
        'Dolly_GRAPHICS': True,
        'Alert_ON': False,
        'Auto_Signals': True,
        'Show_DollyCOMMENTS': True,
        'BUY_Target_2': 50,
        'BUY_Target_1': 40,
        'BUY_Area': 20,
        'SELL_Area': 20,
        'SELL_Target_1': 40,
        'SELL_Target_2': 50,
        'SHIFT_DailyText': 0,
        'Show_DailyAverageGRAPHICS': True,
        'Daily_AverageGRAPHICS': True,
        'SHIFT_DailyAverageText': 28,
        'Show_PivotLines': False,
        'Show_M_PivotLines': False,
        'SHIFT_Pivot_PointText': 0,
        'Pivot_Point_ExtendLINE': 0,
        'Show_FibLines': False,
        'Show_EXTRAFibLines': False,
        'SHIFT_FibText': 65,
        'FIB_ExtendDISPLAY': 1,
        'Show_Daily_HI_LOW': False,
        'SHIFT_HI_LOW_TEXT': 50,
        'Show_Daily_OPEN': False,
        'SHIFT_Daily_OPEN_TEXT': 0,
    }

