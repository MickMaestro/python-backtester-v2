"""multilinemovingaverage — converted from MQL5: MQL5 Indicators/MultiLineMovingAverage/multilinemovingaverage.mq5

The indicator gives signals in case
Copyright: Copyright © 2011,  PozitiF; Link: Alex-W-@bk.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011,  PozitiF', 'link': 'Alex-W-@bk.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The indicator gives signals in case'], 'name': 'multilinemovingaverage', 'source': 'MQL5 Indicators/MultiLineMovingAverage/multilinemovingaverage.mq5', 'folder': 'MultiLineMovingAverage', 'inputs': [{'mql': 'level_name', 'py': 'level_name', 'param': None, 'type': 'string', 'default': 'MultiLineMovingAverage 1', 'label': 'Actuation level name', 'sinput': False}, {'mql': 'level_comment', 'py': 'level_comment', 'param': None, 'type': 'string', 'default': 'MultiLineMovingAverage', 'label': 'Actuation level comment', 'sinput': False}, {'mql': 'TxtPos', 'py': 'TxtPos', 'param': 'TxtPos', 'type': 'int', 'default': 1, 'label': 'Text position', 'sinput': False}, {'mql': 'TextSize', 'py': 'TextSize', 'param': 'TextSize', 'type': 'uint', 'default': 15, 'label': 'Text size', 'sinput': False}, {'mql': 'Up_levels_color', 'py': 'Up_levels_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Up MA level color', 'sinput': False}, {'mql': 'Fl_levels_color', 'py': 'Fl_levels_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Flat MA level color', 'sinput': False}, {'mql': 'Dn_levels_color', 'py': 'Dn_levels_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Down MA level color', 'sinput': False}, {'mql': 'CandleCount', 'py': 'CandleCount', 'param': 'CandleCount', 'type': 'uint', 'default': 10, 'label': 'Level length', 'sinput': False}, {'mql': 'display_MA1', 'py': 'display_MA1', 'param': 'display_MA1', 'type': 'bool', 'default': True, 'label': 'Show MA Level', 'sinput': False}, {'mql': 'Timeframe1', 'py': 'Timeframe1', 'param': 'Timeframe1', 'type': 'int', 'default': 5, 'label': 'Timeframe of MA', 'sinput': False}, {'mql': 'MA1_SMethod', 'py': 'MA1_SMethod', 'param': 'MA1_SMethod', 'type': 'int', 'default': 1, 'label': 'Smoothing MA method', 'sinput': False}, {'mql': 'MA1_Length', 'py': 'MA1_Length', 'param': 'MA1_Length', 'type': 'uint', 'default': 10, 'label': 'MA period', 'sinput': False}, {'mql': 'MA1_Signal_Bar', 'py': 'MA1_Signal_Bar', 'param': 'MA1_Signal_Bar', 'type': 'uint', 'default': 1, 'label': 'MA signal bar', 'sinput': False}, {'mql': 'AppliedPrice1', 'py': 'AppliedPrice1', 'param': 'AppliedPrice1', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'level1_style', 'py': 'level1_style', 'param': 'level1_style', 'type': 'int', 'default': 0, 'label': 'Actuation level style', 'sinput': False}, {'mql': 'level1_width', 'py': 'level1_width', 'param': 'level1_width', 'type': 'int', 'default': 2, 'label': 'Actuation level width', 'sinput': False}, {'mql': 'display_MA2', 'py': 'display_MA2', 'param': 'display_MA2', 'type': 'bool', 'default': True, 'label': 'Show MA Level', 'sinput': False}, {'mql': 'Timeframe2', 'py': 'Timeframe2', 'param': 'Timeframe2', 'type': 'int', 'default': 30, 'label': 'Timeframe of MA', 'sinput': False}, {'mql': 'MA2_SMethod', 'py': 'MA2_SMethod', 'param': 'MA2_SMethod', 'type': 'int', 'default': 1, 'label': 'Smoothing MA method', 'sinput': False}, {'mql': 'MA2_Length', 'py': 'MA2_Length', 'param': 'MA2_Length', 'type': 'uint', 'default': 10, 'label': 'MA period', 'sinput': False}, {'mql': 'MA2_Signal_Bar', 'py': 'MA2_Signal_Bar', 'param': 'MA2_Signal_Bar', 'type': 'uint', 'default': 1, 'label': 'MA signal bar', 'sinput': False}, {'mql': 'AppliedPrice2', 'py': 'AppliedPrice2', 'param': 'AppliedPrice2', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'level2_style', 'py': 'level2_style', 'param': 'level2_style', 'type': 'int', 'default': 0, 'label': 'Actuation level style', 'sinput': False}, {'mql': 'level2_width', 'py': 'level2_width', 'param': 'level2_width', 'type': 'int', 'default': 2, 'label': 'Actuation level width', 'sinput': False}, {'mql': 'display_MA3', 'py': 'display_MA3', 'param': 'display_MA3', 'type': 'bool', 'default': True, 'label': 'Show MA Level', 'sinput': False}, {'mql': 'Timeframe3', 'py': 'Timeframe3', 'param': 'Timeframe3', 'type': 'int', 'default': 16386, 'label': 'Timeframe of MA', 'sinput': False}, {'mql': 'MA3_SMethod', 'py': 'MA3_SMethod', 'param': 'MA3_SMethod', 'type': 'int', 'default': 1, 'label': 'Smoothing MA method', 'sinput': False}, {'mql': 'MA3_Length', 'py': 'MA3_Length', 'param': 'MA3_Length', 'type': 'uint', 'default': 10, 'label': 'MA period', 'sinput': False}, {'mql': 'MA3_Signal_Bar', 'py': 'MA3_Signal_Bar', 'param': 'MA3_Signal_Bar', 'type': 'uint', 'default': 1, 'label': 'MA signal bar', 'sinput': False}, {'mql': 'AppliedPrice3', 'py': 'AppliedPrice3', 'param': 'AppliedPrice3', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'level3_style', 'py': 'level3_style', 'param': 'level3_style', 'type': 'int', 'default': 0, 'label': 'Actuation level style', 'sinput': False}, {'mql': 'level3_width', 'py': 'level3_width', 'param': 'level3_width', 'type': 'int', 'default': 2, 'label': 'Actuation level width', 'sinput': False}, {'mql': 'display_MA4', 'py': 'display_MA4', 'param': 'display_MA4', 'type': 'bool', 'default': True, 'label': 'Show MA Level', 'sinput': False}, {'mql': 'Timeframe4', 'py': 'Timeframe4', 'param': 'Timeframe4', 'type': 'int', 'default': 16388, 'label': 'Timeframe of MA', 'sinput': False}, {'mql': 'MA4_SMethod', 'py': 'MA4_SMethod', 'param': 'MA4_SMethod', 'type': 'int', 'default': 1, 'label': 'Smoothing MA method', 'sinput': False}, {'mql': 'MA4_Length', 'py': 'MA4_Length', 'param': 'MA4_Length', 'type': 'uint', 'default': 10, 'label': 'MA period', 'sinput': False}, {'mql': 'MA4_Signal_Bar', 'py': 'MA4_Signal_Bar', 'param': 'MA4_Signal_Bar', 'type': 'uint', 'default': 1, 'label': 'MA signal bar', 'sinput': False}, {'mql': 'AppliedPrice4', 'py': 'AppliedPrice4', 'param': 'AppliedPrice4', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'level4_style', 'py': 'level4_style', 'param': 'level4_style', 'type': 'int', 'default': 0, 'label': 'Actuation level style', 'sinput': False}, {'mql': 'level4_width', 'py': 'level4_width', 'param': 'level4_width', 'type': 'int', 'default': 2, 'label': 'Actuation level width', 'sinput': False}, {'mql': 'display_MA5', 'py': 'display_MA5', 'param': 'display_MA5', 'type': 'bool', 'default': True, 'label': 'Show MA Level', 'sinput': False}, {'mql': 'Timeframe5', 'py': 'Timeframe5', 'param': 'Timeframe5', 'type': 'int', 'default': 16396, 'label': 'Timeframe of MA', 'sinput': False}, {'mql': 'MA5_SMethod', 'py': 'MA5_SMethod', 'param': 'MA5_SMethod', 'type': 'int', 'default': 1, 'label': 'Smoothing MA method', 'sinput': False}, {'mql': 'MA5_Length', 'py': 'MA5_Length', 'param': 'MA5_Length', 'type': 'uint', 'default': 10, 'label': 'MA period', 'sinput': False}, {'mql': 'MA5_Signal_Bar', 'py': 'MA5_Signal_Bar', 'param': 'MA5_Signal_Bar', 'type': 'uint', 'default': 1, 'label': 'MA signal bar', 'sinput': False}, {'mql': 'AppliedPrice5', 'py': 'AppliedPrice5', 'param': 'AppliedPrice5', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'level5_style', 'py': 'level5_style', 'param': 'level5_style', 'type': 'int', 'default': 0, 'label': 'Actuation level style', 'sinput': False}, {'mql': 'level5_width', 'py': 'level5_width', 'param': 'level5_width', 'type': 'int', 'default': 2, 'label': 'Actuation level width', 'sinput': False}, {'mql': 'display_MA6', 'py': 'display_MA6', 'param': 'display_MA6', 'type': 'bool', 'default': True, 'label': 'Show MA Level', 'sinput': False}, {'mql': 'Timeframe6', 'py': 'Timeframe6', 'param': 'Timeframe6', 'type': 'int', 'default': 16408, 'label': 'Timeframe of MA', 'sinput': False}, {'mql': 'MA6_SMethod', 'py': 'MA6_SMethod', 'param': 'MA6_SMethod', 'type': 'int', 'default': 1, 'label': 'Smoothing MA method', 'sinput': False}, {'mql': 'MA6_Length', 'py': 'MA6_Length', 'param': 'MA6_Length', 'type': 'uint', 'default': 10, 'label': 'MA period', 'sinput': False}, {'mql': 'MA6_Signal_Bar', 'py': 'MA6_Signal_Bar', 'param': 'MA6_Signal_Bar', 'type': 'uint', 'default': 1, 'label': 'MA signal bar', 'sinput': False}, {'mql': 'AppliedPrice6', 'py': 'AppliedPrice6', 'param': 'AppliedPrice6', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'level6_style', 'py': 'level6_style', 'param': 'level6_style', 'type': 'int', 'default': 0, 'label': 'Actuation level style', 'sinput': False}, {'mql': 'level6_width', 'py': 'level6_width', 'param': 'level6_width', 'type': 'int', 'default': 2, 'label': 'Actuation level width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Gray = 0x808080  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# enum ENUM_TEXT_POSITION
Left = 0
Right = 1
_enum('ENUM_TEXT_POSITION', {0: 'Left', 1: 'Right'})

# ---- inputs and global variables
level_name = _input('level_name', 'MultiLineMovingAverage 1')  # Actuation level name
level_comment = _input('level_comment', 'MultiLineMovingAverage')  # Actuation level comment
TxtPos = _input('TxtPos', Right)  # Text position
TextSize = _input('TextSize', 15)  # Text size
CandleCount = _input('CandleCount', 10)  # Level length
display_MA1 = _input('display_MA1', True)  # Show MA Level
Timeframe1 = _input('Timeframe1', PERIOD_M5)  # Timeframe of MA
MA1_SMethod = _input('MA1_SMethod', MODE_EMA)  # Smoothing MA method
MA1_Length = _input('MA1_Length', 10)  # MA period
MA1_Signal_Bar = _input('MA1_Signal_Bar', 1)  # MA signal bar
AppliedPrice1 = _input('AppliedPrice1', PRICE_CLOSE)  # Applied price
level1_style = _input('level1_style', STYLE_SOLID)  # Actuation level style
level1_width = _input('level1_width', w_2)  # Actuation level width
display_MA2 = _input('display_MA2', True)  # Show MA Level
Timeframe2 = _input('Timeframe2', PERIOD_M30)  # Timeframe of MA
MA2_SMethod = _input('MA2_SMethod', MODE_EMA)  # Smoothing MA method
MA2_Length = _input('MA2_Length', 10)  # MA period
MA2_Signal_Bar = _input('MA2_Signal_Bar', 1)  # MA signal bar
AppliedPrice2 = _input('AppliedPrice2', PRICE_CLOSE)  # Applied price
level2_style = _input('level2_style', STYLE_SOLID)  # Actuation level style
level2_width = _input('level2_width', w_2)  # Actuation level width
display_MA3 = _input('display_MA3', True)  # Show MA Level
Timeframe3 = _input('Timeframe3', PERIOD_H2)  # Timeframe of MA
MA3_SMethod = _input('MA3_SMethod', MODE_EMA)  # Smoothing MA method
MA3_Length = _input('MA3_Length', 10)  # MA period
MA3_Signal_Bar = _input('MA3_Signal_Bar', 1)  # MA signal bar
AppliedPrice3 = _input('AppliedPrice3', PRICE_CLOSE)  # Applied price
level3_style = _input('level3_style', STYLE_SOLID)  # Actuation level style
level3_width = _input('level3_width', w_2)  # Actuation level width
display_MA4 = _input('display_MA4', True)  # Show MA Level
Timeframe4 = _input('Timeframe4', PERIOD_H4)  # Timeframe of MA
MA4_SMethod = _input('MA4_SMethod', MODE_EMA)  # Smoothing MA method
MA4_Length = _input('MA4_Length', 10)  # MA period
MA4_Signal_Bar = _input('MA4_Signal_Bar', 1)  # MA signal bar
AppliedPrice4 = _input('AppliedPrice4', PRICE_CLOSE)  # Applied price
level4_style = _input('level4_style', STYLE_SOLID)  # Actuation level style
level4_width = _input('level4_width', w_2)  # Actuation level width
display_MA5 = _input('display_MA5', True)  # Show MA Level
Timeframe5 = _input('Timeframe5', PERIOD_H12)  # Timeframe of MA
MA5_SMethod = _input('MA5_SMethod', MODE_EMA)  # Smoothing MA method
MA5_Length = _input('MA5_Length', 10)  # MA period
MA5_Signal_Bar = _input('MA5_Signal_Bar', 1)  # MA signal bar
AppliedPrice5 = _input('AppliedPrice5', PRICE_CLOSE)  # Applied price
level5_style = _input('level5_style', STYLE_SOLID)  # Actuation level style
level5_width = _input('level5_width', w_2)  # Actuation level width
display_MA6 = _input('display_MA6', True)  # Show MA Level
Timeframe6 = _input('Timeframe6', PERIOD_D1)  # Timeframe of MA
MA6_SMethod = _input('MA6_SMethod', MODE_EMA)  # Smoothing MA method
MA6_Length = _input('MA6_Length', 10)  # MA period
MA6_Signal_Bar = _input('MA6_Signal_Bar', 1)  # MA signal bar
AppliedPrice6 = _input('AppliedPrice6', PRICE_CLOSE)  # Applied price
level6_style = _input('level6_style', STYLE_SOLID)  # Actuation level style
level6_width = _input('level6_width', w_2)  # Actuation level width
PerSec = 0
levellength = 0
text1_name = ""
text2_name = ""
text3_name = ""
text4_name = ""
text5_name = ""
text6_name = ""
level1_name = ""
level2_name = ""
level3_name = ""
level4_name = ""
level5_name = ""
level6_name = ""
MA1_Handle = 0
MA2_Handle = 0
MA3_Handle = 0
MA4_Handle = 0
MA5_Handle = 0
MA6_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def GetStringMAName(SMethod):
    _sw1 = SMethod
    if _sw1 == MODE_SMA:
        return 'SMA'
    elif _sw1 == MODE_EMA:
        return 'EMA'
    elif _sw1 == MODE_SMMA:
        return 'SMMA'
    elif _sw1 == MODE_LWMA:
        return 'LWMA'
    return 'SMA'

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, False)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)

def CreateText(chart_id, name, nwin, time, price, text, Color, Font, Size, point):
    ObjectCreate(chart_id, name, OBJ_TEXT, nwin, time, price)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ANCHOR, point)

def SetText(chart_id, name, nwin, time, price, text, Color, Font, Size, point):
    if ObjectFind(chart_id, name) == -1:
        CreateText(chart_id, name, nwin, time, price, text, Color, Font, Size, point)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time, price)

def OnInit():
    global MA1_Handle, MA2_Handle, MA3_Handle, MA4_Handle, MA5_Handle, MA6_Handle, PerSec, level1_name, level2_name, level3_name, level4_name, level5_name, level6_name, levellength, text1_name, text2_name, text3_name, text4_name, text5_name, text6_name
    if display_MA1:
        MA1_Handle = iMA(None, Timeframe1, MA1_Length, 0, MA1_SMethod, AppliedPrice1)
        if MA1_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the iMA 1 indicator')
            return INIT_FAILED
    if display_MA2:
        MA2_Handle = iMA(None, Timeframe2, MA2_Length, 0, MA2_SMethod, AppliedPrice2)
        if MA2_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the iMA 2 indicator')
            return INIT_FAILED
    if display_MA3:
        MA3_Handle = iMA(None, Timeframe3, MA3_Length, 0, MA3_SMethod, AppliedPrice3)
        if MA3_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the iMA 3 indicator')
            return INIT_FAILED
    if display_MA4:
        MA4_Handle = iMA(None, Timeframe4, MA4_Length, 0, MA4_SMethod, AppliedPrice4)
        if MA4_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the iMA 4 indicator')
            return INIT_FAILED
    if display_MA5:
        MA5_Handle = iMA(None, Timeframe5, MA5_Length, 0, MA5_SMethod, AppliedPrice5)
        if MA5_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the iMA 5 indicator')
            return INIT_FAILED
    if display_MA6:
        MA6_Handle = iMA(None, Timeframe6, MA6_Length, 0, MA6_SMethod, AppliedPrice6)
        if MA6_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the iMA 6 indicator')
            return INIT_FAILED
    level1_name = level_name + '_1'
    level2_name = level_name + '_2'
    level3_name = level_name + '_3'
    level4_name = level_name + '_4'
    level5_name = level_name + '_5'
    level6_name = level_name + '_6'
    text1_name = level1_name + '_Text'
    text2_name = level2_name + '_Text'
    text3_name = level3_name + '_Text'
    text4_name = level4_name + '_Text'
    text5_name = level5_name + '_Text'
    text6_name = level6_name + '_Text'
    levellength = PeriodSeconds() * CandleCount
    PerSec = PeriodSeconds()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, level1_name)
    ObjectDelete(0, text1_name)
    ObjectDelete(0, level2_name)
    ObjectDelete(0, text2_name)
    ObjectDelete(0, level3_name)
    ObjectDelete(0, text3_name)
    ObjectDelete(0, level4_name)
    ObjectDelete(0, text4_name)
    ObjectDelete(0, level5_name)
    ObjectDelete(0, text5_name)
    ObjectDelete(0, level6_name)
    ObjectDelete(0, text6_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total == prev_calculated:
        return rates_total
    if BarsCalculated(MA1_Handle) < Bars(Symbol(), Timeframe1):
        return prev_calculated
    if BarsCalculated(MA2_Handle) < Bars(Symbol(), Timeframe2):
        return prev_calculated
    if BarsCalculated(MA3_Handle) < Bars(Symbol(), Timeframe3):
        return prev_calculated
    if BarsCalculated(MA4_Handle) < Bars(Symbol(), Timeframe4):
        return prev_calculated
    if BarsCalculated(MA5_Handle) < Bars(Symbol(), Timeframe5):
        return prev_calculated
    if BarsCalculated(MA6_Handle) < Bars(Symbol(), Timeframe6):
        return prev_calculated
    LevelColor = 0
    text = Box('')
    Point_ = 0
    timeT = 0
    time1 = 0
    time2 = 0
    MA = Arr(2, 0.0, dyn=False)
    price = 0.0
    priceT = 0.0
    ArraySetAsSeries(time, True)
    _sw2 = TxtPos
    if _sw2 == Left:
        time1 = time[0] - levellength
        timeT = time1 - (2 * PerSec)
        time2 = time[0] + PerSec
        Point_ = ANCHOR_RIGHT
    elif _sw2 == Right:
        time1 = time[0] - levellength
        time2 = time[0] + PerSec
        timeT = time2 + (2 * PerSec)
        Point_ = ANCHOR_LEFT
    if display_MA1:
        if CopyBuffer(MA1_Handle, 0, MA1_Signal_Bar, 2, MA) <= 0:
            return 0
        price = MA[1]
        if (MA[1] - MA[0]) > 0:
            LevelColor = Up_levels_color
        elif (MA[1] - MA[0]) < 0:
            LevelColor = Dn_levels_color
        else:
            LevelColor = Fl_levels_color
        priceT = price
        text.v = ''
        StringConcatenate(text, GetStringTimeframe(Timeframe1), ' ', GetStringMAName(MA1_SMethod), MA1_Length)
        SetTline(0, level1_name, 0, time1, price, time2, price, LevelColor, level1_style, level1_width, level_comment)
        CreateText(0, text1_name, 0, timeT, priceT, text.v, LevelColor, 'Georgia', TextSize, Point_)
    if display_MA2:
        if CopyBuffer(MA2_Handle, 0, MA2_Signal_Bar, 2, MA) <= 0:
            return 0
        price = MA[1]
        if (MA[1] - MA[0]) > 0:
            LevelColor = Up_levels_color
        elif (MA[1] - MA[0]) < 0:
            LevelColor = Dn_levels_color
        else:
            LevelColor = Fl_levels_color
        priceT = price
        text.v = ''
        StringConcatenate(text, GetStringTimeframe(Timeframe2), ' ', GetStringMAName(MA2_SMethod), MA2_Length)
        SetTline(0, level2_name, 0, time1, price, time2, price, LevelColor, level2_style, level2_width, level_comment)
        CreateText(0, text2_name, 0, timeT, priceT, text.v, LevelColor, 'Georgia', TextSize, Point_)
    if display_MA3:
        if CopyBuffer(MA3_Handle, 0, MA3_Signal_Bar, 2, MA) <= 0:
            return 0
        price = MA[1]
        if (MA[1] - MA[0]) > 0:
            LevelColor = Up_levels_color
        elif (MA[1] - MA[0]) < 0:
            LevelColor = Dn_levels_color
        else:
            LevelColor = Fl_levels_color
        priceT = price
        text.v = ''
        StringConcatenate(text, GetStringTimeframe(Timeframe3), ' ', GetStringMAName(MA3_SMethod), MA3_Length)
        SetTline(0, level3_name, 0, time1, price, time2, price, LevelColor, level3_style, level3_width, level_comment)
        CreateText(0, text3_name, 0, timeT, priceT, text.v, LevelColor, 'Georgia', TextSize, Point_)
    if display_MA4:
        if CopyBuffer(MA4_Handle, 0, MA4_Signal_Bar, 2, MA) <= 0:
            return 0
        price = MA[1]
        if (MA[1] - MA[0]) > 0:
            LevelColor = Up_levels_color
        elif (MA[1] - MA[0]) < 0:
            LevelColor = Dn_levels_color
        else:
            LevelColor = Fl_levels_color
        priceT = price
        text.v = ''
        StringConcatenate(text, GetStringTimeframe(Timeframe4), ' ', GetStringMAName(MA4_SMethod), MA4_Length)
        SetTline(0, level4_name, 0, time1, price, time2, price, LevelColor, level4_style, level4_width, level_comment)
        CreateText(0, text4_name, 0, timeT, priceT, text.v, LevelColor, 'Georgia', TextSize, Point_)
    if display_MA5:
        if CopyBuffer(MA5_Handle, 0, MA5_Signal_Bar, 2, MA) <= 0:
            return 0
        price = MA[1]
        if (MA[1] - MA[0]) > 0:
            LevelColor = Up_levels_color
        elif (MA[1] - MA[0]) < 0:
            LevelColor = Dn_levels_color
        else:
            LevelColor = Fl_levels_color
        priceT = price
        text.v = ''
        StringConcatenate(text, GetStringTimeframe(Timeframe5), ' ', GetStringMAName(MA5_SMethod), MA5_Length)
        SetTline(0, level5_name, 0, time1, price, time2, price, LevelColor, level5_style, level5_width, level_comment)
        CreateText(0, text5_name, 0, timeT, priceT, text.v, LevelColor, 'Georgia', TextSize, Point_)
    if display_MA6:
        if CopyBuffer(MA6_Handle, 0, MA6_Signal_Bar, 2, MA) <= 0:
            return 0
        price = MA[1]
        if (MA[1] - MA[0]) > 0:
            LevelColor = Up_levels_color
        elif (MA[1] - MA[0]) < 0:
            LevelColor = Dn_levels_color
        else:
            LevelColor = Fl_levels_color
        priceT = price
        text.v = ''
        StringConcatenate(text, GetStringTimeframe(Timeframe6), ' ', GetStringMAName(MA6_SMethod), MA6_Length)
        SetTline(0, level6_name, 0, time1, price, time2, price, LevelColor, level6_style, level6_width, level_comment)
        CreateText(0, text6_name, 0, timeT, priceT, text.v, LevelColor, 'Georgia', TextSize, Point_)
    return rates_total

# ---- global variables initialised from expressions
Up_levels_color = _input('Up_levels_color', _uint(Lime))  # Up MA level color
Fl_levels_color = _input('Fl_levels_color', _uint(Gray))  # Flat MA level color
Dn_levels_color = _input('Dn_levels_color', _uint(Red))  # Down MA level color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Multilinemovingaverage(_MQL5Indicator):
    name = 'multilinemovingaverage'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TxtPos': _Choice({0: 'left', 1: 'Right'}, default=1),  # Text position
        'TextSize': 15,  # Text size
        'CandleCount': 10,  # Level length
        'display_MA1': True,  # Show MA Level
        'Timeframe1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=5),  # Timeframe of MA
        'MA1_SMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing MA method
        'MA1_Length': 10,  # MA period
        'MA1_Signal_Bar': 1,  # MA signal bar
        'AppliedPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'level1_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Actuation level style
        'level1_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Actuation level width
        'display_MA2': True,  # Show MA Level
        'Timeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # Timeframe of MA
        'MA2_SMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing MA method
        'MA2_Length': 10,  # MA period
        'MA2_Signal_Bar': 1,  # MA signal bar
        'AppliedPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'level2_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Actuation level style
        'level2_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Actuation level width
        'display_MA3': True,  # Show MA Level
        'Timeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16386),  # Timeframe of MA
        'MA3_SMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing MA method
        'MA3_Length': 10,  # MA period
        'MA3_Signal_Bar': 1,  # MA signal bar
        'AppliedPrice3': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'level3_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Actuation level style
        'level3_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Actuation level width
        'display_MA4': True,  # Show MA Level
        'Timeframe4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Timeframe of MA
        'MA4_SMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing MA method
        'MA4_Length': 10,  # MA period
        'MA4_Signal_Bar': 1,  # MA signal bar
        'AppliedPrice4': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'level4_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Actuation level style
        'level4_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Actuation level width
        'display_MA5': True,  # Show MA Level
        'Timeframe5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # Timeframe of MA
        'MA5_SMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing MA method
        'MA5_Length': 10,  # MA period
        'MA5_Signal_Bar': 1,  # MA signal bar
        'AppliedPrice5': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'level5_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Actuation level style
        'level5_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Actuation level width
        'display_MA6': True,  # Show MA Level
        'Timeframe6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Timeframe of MA
        'MA6_SMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing MA method
        'MA6_Length': 10,  # MA period
        'MA6_Signal_Bar': 1,  # MA signal bar
        'AppliedPrice6': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'level6_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Actuation level style
        'level6_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Actuation level width
    }

