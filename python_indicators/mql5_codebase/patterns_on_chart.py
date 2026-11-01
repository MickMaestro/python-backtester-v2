"""patterns_on_chart — converted from MQL5: MQL5 Indicators/Japanese Candlestick Patterns/patterns_on_chart.mq5

Recognizes Japanese candlestick patterns.
Copyright: Ronnie Mansolillo; Link: https://login.mql5.com/en/users/rosiman; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Ronnie Mansolillo', 'link': 'https://login.mql5.com/en/users/rosiman', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [13749760], 2: [42495]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': ['Recognizes Japanese candlestick patterns.'], 'name': 'patterns_on_chart', 'source': 'MQL5 Indicators/Japanese Candlestick Patterns/patterns_on_chart.mq5', 'folder': 'Japanese Candlestick Patterns', 'inputs': [{'mql': 'UseExtraDigit', 'py': 'UseExtraDigit', 'param': 'UseExtraDigit', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Show_Alert', 'py': 'Show_Alert', 'param': 'Show_Alert', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Display_ShootStar_2', 'py': 'Display_ShootStar_2', 'param': 'Display_ShootStar_2', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_ShootStar_Alert_2', 'py': 'Show_ShootStar_Alert_2', 'param': 'Show_ShootStar_Alert_2', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Display_ShootStar_3', 'py': 'Display_ShootStar_3', 'param': 'Display_ShootStar_3', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_ShootStar_Alert_3', 'py': 'Show_ShootStar_Alert_3', 'param': 'Show_ShootStar_Alert_3', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Display_ShootStar_4', 'py': 'Display_ShootStar_4', 'param': 'Display_ShootStar_4', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_ShootStar_Alert_4', 'py': 'Show_ShootStar_Alert_4', 'param': 'Show_ShootStar_Alert_4', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Color_ShootStar', 'py': 'Color_ShootStar', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Display_Hammer_2', 'py': 'Display_Hammer_2', 'param': 'Display_Hammer_2', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_Hammer_Alert_2', 'py': 'Show_Hammer_Alert_2', 'param': 'Show_Hammer_Alert_2', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Display_Hammer_3', 'py': 'Display_Hammer_3', 'param': 'Display_Hammer_3', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_Hammer_Alert_3', 'py': 'Show_Hammer_Alert_3', 'param': 'Show_Hammer_Alert_3', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Display_Hammer_4', 'py': 'Display_Hammer_4', 'param': 'Display_Hammer_4', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_Hammer_Alert_4', 'py': 'Show_Hammer_Alert_4', 'param': 'Show_Hammer_Alert_4', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Color_Hammer', 'py': 'Color_Hammer', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Display_Doji', 'py': 'Display_Doji', 'param': 'Display_Doji', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_Doji_Alert', 'py': 'Show_Doji_Alert', 'param': 'Show_Doji_Alert', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Color_Doji', 'py': 'Color_Doji', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Display_Stars', 'py': 'Display_Stars', 'param': 'Display_Stars', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_Stars_Alert', 'py': 'Show_Stars_Alert', 'param': 'Show_Stars_Alert', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Star_Body_Length', 'py': 'Star_Body_Length', 'param': 'Star_Body_Length', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Color_Star', 'py': 'Color_Star', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Display_Dark_Cloud_Cover', 'py': 'Display_Dark_Cloud_Cover', 'param': 'Display_Dark_Cloud_Cover', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_DarkCC_Alert', 'py': 'Show_DarkCC_Alert', 'param': 'Show_DarkCC_Alert', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Color_DarkCC', 'py': 'Color_DarkCC', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Display_Piercing_Line', 'py': 'Display_Piercing_Line', 'param': 'Display_Piercing_Line', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_Piercing_Line_Alert', 'py': 'Show_Piercing_Line_Alert', 'param': 'Show_Piercing_Line_Alert', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Color_Piercing_Line', 'py': 'Color_Piercing_Line', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Display_Bearish_Engulfing', 'py': 'Display_Bearish_Engulfing', 'param': 'Display_Bearish_Engulfing', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_Bearish_Engulfing_Alert', 'py': 'Show_Bearish_Engulfing_Alert', 'param': 'Show_Bearish_Engulfing_Alert', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Color_Bearish_Engulfing', 'py': 'Color_Bearish_Engulfing', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Display_Bullish_Engulfing', 'py': 'Display_Bullish_Engulfing', 'param': 'Display_Bullish_Engulfing', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Show_Bullish_Engulfing_Alert', 'py': 'Show_Bullish_Engulfing_Alert', 'param': 'Show_Bullish_Engulfing_Alert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Color_Bullish_Engulfing', 'py': 'Color_Bullish_Engulfing', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Aqua = 0xFFFF00  # MQL4 colour name
Blue = 0xFF0000  # MQL4 colour name
Brown = 0x2A2AA5  # MQL4 colour name
DeepPink = 0x9314FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
SpringGreen = 0x7FFF00  # MQL4 colour name

# ---- inputs and global variables
UseExtraDigit = _input('UseExtraDigit', False)
Show_Alert = _input('Show_Alert', True)
Display_ShootStar_2 = _input('Display_ShootStar_2', True)
Show_ShootStar_Alert_2 = _input('Show_ShootStar_Alert_2', True)
Display_ShootStar_3 = _input('Display_ShootStar_3', True)
Show_ShootStar_Alert_3 = _input('Show_ShootStar_Alert_3', True)
Display_ShootStar_4 = _input('Display_ShootStar_4', True)
Show_ShootStar_Alert_4 = _input('Show_ShootStar_Alert_4', True)
Text_ShootStar = 10
Display_Hammer_2 = _input('Display_Hammer_2', True)
Show_Hammer_Alert_2 = _input('Show_Hammer_Alert_2', True)
Display_Hammer_3 = _input('Display_Hammer_3', True)
Show_Hammer_Alert_3 = _input('Show_Hammer_Alert_3', True)
Display_Hammer_4 = _input('Display_Hammer_4', True)
Show_Hammer_Alert_4 = _input('Show_Hammer_Alert_4', True)
Text_Hammer = 10
Display_Doji = _input('Display_Doji', True)
Show_Doji_Alert = _input('Show_Doji_Alert', True)
Text_Doji = 10
Display_Stars = _input('Display_Stars', True)
Show_Stars_Alert = _input('Show_Stars_Alert', True)
Star_Body_Length = _input('Star_Body_Length', 5)
Text_Star = 10
Display_Dark_Cloud_Cover = _input('Display_Dark_Cloud_Cover', True)
Show_DarkCC_Alert = _input('Show_DarkCC_Alert', True)
Text_DarkCC = 10
Display_Piercing_Line = _input('Display_Piercing_Line', True)
Show_Piercing_Line_Alert = _input('Show_Piercing_Line_Alert', True)
Text_Piercing_Line = 10
Display_Bearish_Engulfing = _input('Display_Bearish_Engulfing', True)
Show_Bearish_Engulfing_Alert = _input('Show_Bearish_Engulfing_Alert', True)
Text_Bearish_Engulfing = 8
Display_Bullish_Engulfing = _input('Display_Bullish_Engulfing', False)
Show_Bullish_Engulfing_Alert = _input('Show_Bullish_Engulfing_Alert', False)
Text_Bullish_Engulfing = 8
upArrow = Arr(0, 0.0)
downArrow = Arr(0, 0.0)
period = ""
Doji_Star_Ratio = 0.0
Doji_MinLength = 0.0
Star_MinLength = 0.0
Pointer_Offset = 0  # The offset value for the arrow to be located off the candle high or low point.
High_Offset = 0  # The offset value added to the high arrow pointer for correct plotting of the pattern label.
Offset_ShootStar = 0  # The offset value of the shooting star above or below the pointer arrow.
Offset_Hammer = 0  # The offset value of the hammer above or below the pointer arrow.
Offset_Doji = 0  # The offset value of the doji above or below the pointer arrow.
Offset_Star = 0  # The offset value of the star above or below the pointer arrow.
Offset_Piercing_Line = 0  # The offset value of the piercing line above or below the pointer arrow.
Offset_DarkCC = 0  # The offset value of the dark cloud cover above or below the pointer arrow.
Offset_Bullish_Engulfing = 0
Offset_Bearish_Engulfing = 0
IncOffset = 0  # The offset value that is added to a cummaltive offset value for each pass through the routine so any
Piercing_Line_Ratio = 0.0
Piercing_Candle_Length = 0
Engulfing_Length = 0
Candle_WickBody_Percent = 0.0
CandleLength = 0

def OnInit():
    global CandleLength, Candle_WickBody_Percent, Doji_Star_Ratio, Engulfing_Length, High_Offset, IncOffset, Offset_Bearish_Engulfing, Offset_Bullish_Engulfing, Offset_DarkCC, Offset_Doji, Offset_Hammer, Offset_Piercing_Line, Offset_ShootStar, Offset_Star, Piercing_Candle_Length, Piercing_Line_Ratio, Pointer_Offset, Text_Bearish_Engulfing, Text_Bullish_Engulfing, Text_DarkCC, Text_Hammer, Text_Piercing_Line, Text_ShootStar, Text_Star, period
    IndicatorSetString(INDICATOR_SHORTNAME, 'PRM')
    PlotIndexSetInteger(0, PLOT_ARROW, 71)
    PlotIndexSetInteger(1, PLOT_ARROW, 72)
    SetIndexBuffer(0, upArrow)
    SetIndexBuffer(1, downArrow)
    ArraySetAsSeries(upArrow, True)
    ArraySetAsSeries(downArrow, True)
    Comment('\n', '\n', 'Bearish', '\n', 'SS 2,3,4 - Shooting Star', '\n', 'E_Star   - Evening Star', '\n', 'E_Doji   - Evening Doji Star', '\n', 'DCC      - Dark Cloud Pattern', '\n', 'S_E      - Bearish Engulfing Pattern', '\n', '\n', 'Bullish', '\n', 'HMR 2,3,4 - Bullish Hammer', '\n', 'M_Star    - Morning Star', '\n', 'M_Doji    - Morning Doji Star', '\n', 'P_L       - Piercing Line Pattern', '\n', 'L_E       - Bullish Engulfing Pattern')
    _sw1 = Period()
    if _sw1 == PERIOD_M1:
        period = 'M1'
        Doji_Star_Ratio = 0.0
        Piercing_Line_Ratio = 0.5
        Piercing_Candle_Length = 10
        Engulfing_Length = 10
        Candle_WickBody_Percent = 0.9
        CandleLength = 12
        Pointer_Offset = 9
        High_Offset = 15
        Offset_Hammer = 5
        Offset_ShootStar = 5
        Offset_Doji = 5
        Offset_Star = 5
        Offset_Piercing_Line = 5
        Offset_DarkCC = 5
        Offset_Bearish_Engulfing = 5
        Offset_Bullish_Engulfing = 5
        Text_ShootStar = 8
        Text_Hammer = 8
        Text_Star = 8
        Text_DarkCC = 8
        Text_Piercing_Line = 8
        Text_Bearish_Engulfing = 8
        Text_Bullish_Engulfing = 8
        IncOffset = 16
    elif _sw1 == PERIOD_M5:
        period = 'M5'
        Doji_Star_Ratio = 0.0
        Piercing_Line_Ratio = 0.5
        Piercing_Candle_Length = 10
        Engulfing_Length = 10
        Candle_WickBody_Percent = 0.9
        CandleLength = 12
        Pointer_Offset = 9
        High_Offset = 15
        Offset_Hammer = 5
        Offset_ShootStar = 5
        Offset_Doji = 5
        Offset_Star = 5
        Offset_Piercing_Line = 5
        Offset_DarkCC = 5
        Offset_Bearish_Engulfing = 5
        Offset_Bullish_Engulfing = 5
        Text_ShootStar = 8
        Text_Hammer = 8
        Text_Star = 8
        Text_DarkCC = 8
        Text_Piercing_Line = 8
        Text_Bearish_Engulfing = 8
        Text_Bullish_Engulfing = 8
        IncOffset = 16
    elif _sw1 == PERIOD_M15:
        period = 'M15'
        Doji_Star_Ratio = 0.0
        Piercing_Line_Ratio = 0.5
        Piercing_Candle_Length = 10
        Engulfing_Length = 0
        Candle_WickBody_Percent = 0.9
        CandleLength = 12
        Pointer_Offset = 9
        High_Offset = 15
        Offset_Hammer = 5
        Offset_ShootStar = 5
        Offset_Doji = 5
        Offset_Star = 5
        Offset_Piercing_Line = 5
        Offset_DarkCC = 5
        Offset_Bearish_Engulfing = 5
        Offset_Bullish_Engulfing = 5
        Text_ShootStar = 8
        Text_Hammer = 8
        Text_Star = 8
        Text_DarkCC = 8
        Text_Piercing_Line = 8
        Text_Bearish_Engulfing = 8
        Text_Bullish_Engulfing = 8
        IncOffset = 16
    elif _sw1 == PERIOD_M30:
        period = 'M30'
        Doji_Star_Ratio = 0.0
        Piercing_Line_Ratio = 0.5
        Piercing_Candle_Length = 10
        Engulfing_Length = 15
        Candle_WickBody_Percent = 0.9
        CandleLength = 12
        Pointer_Offset = 9
        High_Offset = 15
        Offset_Hammer = 5
        Offset_ShootStar = 5
        Offset_Doji = 5
        Offset_Star = 5
        Offset_Piercing_Line = 5
        Offset_DarkCC = 5
        Offset_Bearish_Engulfing = 5
        Offset_Bullish_Engulfing = 5
        Text_ShootStar = 8
        Text_Hammer = 8
        Text_Star = 8
        Text_DarkCC = 8
        Text_Piercing_Line = 8
        Text_Bearish_Engulfing = 8
        Text_Bullish_Engulfing = 8
        IncOffset = 16
    elif _sw1 == PERIOD_H1:
        period = 'H1'
        Doji_Star_Ratio = 0.0
        Piercing_Line_Ratio = 0.5
        Piercing_Candle_Length = 10
        Engulfing_Length = 25
        Candle_WickBody_Percent = 0.9
        CandleLength = 12
        Pointer_Offset = 9
        High_Offset = 20
        Offset_Hammer = 8
        Offset_ShootStar = 8
        Offset_Doji = 8
        Offset_Star = 8
        Offset_Piercing_Line = 8
        Offset_DarkCC = 8
        Offset_Bearish_Engulfing = 8
        Offset_Bullish_Engulfing = 8
        Text_ShootStar = 8
        Text_Hammer = 8
        Text_Star = 8
        Text_DarkCC = 8
        Text_Piercing_Line = 8
        Text_Bearish_Engulfing = 8
        Text_Bullish_Engulfing = 8
        IncOffset = 18
    elif _sw1 == PERIOD_H4:
        period = 'H4'
        Doji_Star_Ratio = 0.0
        Piercing_Line_Ratio = 0.5
        Piercing_Candle_Length = 10
        Engulfing_Length = 20
        Candle_WickBody_Percent = 0.9
        CandleLength = 12
        Pointer_Offset = 20
        High_Offset = 40
        Offset_Hammer = 10
        Offset_ShootStar = 10
        Offset_Doji = 10
        Offset_Star = 10
        Offset_Piercing_Line = 10
        Offset_DarkCC = 10
        Offset_Bearish_Engulfing = 10
        Offset_Bullish_Engulfing = 10
        Text_ShootStar = 8
        Text_Hammer = 8
        Text_Star = 8
        Text_DarkCC = 8
        Text_Piercing_Line = 8
        Text_Bearish_Engulfing = 8
        Text_Bullish_Engulfing = 8
        IncOffset = 25
    elif _sw1 == PERIOD_D1:
        period = 'D1'
        Doji_Star_Ratio = 0.0
        Piercing_Line_Ratio = 0.5
        Piercing_Candle_Length = 10
        Engulfing_Length = 30
        Candle_WickBody_Percent = 0.9
        CandleLength = 12
        Pointer_Offset = 9
        High_Offset = 80
        Offset_Hammer = 15
        Offset_ShootStar = 15
        Offset_Doji = 15
        Offset_Star = 15
        Offset_Piercing_Line = 15
        Offset_DarkCC = 15
        Offset_Bearish_Engulfing = 15
        Offset_Bullish_Engulfing = 15
        Text_ShootStar = 8
        Text_Hammer = 8
        Text_Star = 8
        Text_DarkCC = 8
        Text_Piercing_Line = 8
        Text_Bearish_Engulfing = 8
        Text_Bullish_Engulfing = 8
        IncOffset = 60
    elif _sw1 == PERIOD_W1:
        period = 'W1'
        Doji_Star_Ratio = 0.0
        Piercing_Line_Ratio = 0.5
        Piercing_Candle_Length = 10
        Engulfing_Length = 40
        Candle_WickBody_Percent = 0.9
        CandleLength = 12
        Pointer_Offset = 9
        High_Offset = 35
        Offset_Hammer = 20
        Offset_ShootStar = 20
        Offset_Doji = 20
        Offset_Star = 20
        Offset_Piercing_Line = 20
        Offset_DarkCC = 20
        Offset_Bearish_Engulfing = 20
        Offset_Bullish_Engulfing = 20
        Text_ShootStar = 8
        Text_Hammer = 8
        Text_Star = 8
        Text_DarkCC = 8
        Text_Piercing_Line = 8
        Text_Bearish_Engulfing = 8
        Text_Bullish_Engulfing = 8
        IncOffset = 35
    elif _sw1 == PERIOD_MN1:
        period = 'MN'
        Doji_Star_Ratio = 0.0
        Piercing_Line_Ratio = 0.5
        Piercing_Candle_Length = 10
        Engulfing_Length = 50
        Candle_WickBody_Percent = 0.9
        CandleLength = 12
        Pointer_Offset = 9
        High_Offset = 45
        Offset_Hammer = 30
        Offset_ShootStar = 30
        Offset_Doji = 30
        Offset_Star = 30
        Offset_Piercing_Line = 30
        Offset_DarkCC = 30
        Offset_Bearish_Engulfing = 30
        Offset_Bullish_Engulfing = 30
        Text_ShootStar = 8
        Text_Hammer = 8
        Text_Star = 8
        Text_DarkCC = 8
        Text_Piercing_Line = 8
        Text_Bearish_Engulfing = 8
        Text_Bullish_Engulfing = 8
        IncOffset = 45
    if UseExtraDigit:
        Piercing_Candle_Length *= 10
        Engulfing_Length *= 10
        Candle_WickBody_Percent *= 10
        CandleLength *= 10
        Pointer_Offset *= 10
        High_Offset *= 10
        Offset_Hammer *= 10
        Offset_ShootStar *= 10
        Offset_Doji *= 10
        Offset_Star *= 10
        Offset_Piercing_Line *= 10
        Offset_DarkCC = 10
        Offset_Bearish_Engulfing *= 10
        Offset_Bullish_Engulfing *= 10
        IncOffset *= 10

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, OBJ_TEXT)
    Comment('')

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global _s_OnCalculate_prevtime
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Open, True)
    Range = 0.0
    AvgRange = 0.0
    counter = 0
    setalert = 0
    shift = 0
    shift1 = 0
    shift2 = 0
    shift3 = 0
    shift4 = 0
    pattern = ""
    setPattern = 0
    alert = 0
    O = 0.0
    O1 = 0.0
    O2 = 0.0
    C = 0.0
    C1 = 0.0
    C2 = 0.0
    C3 = 0.0
    L = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    H = 0.0
    H1 = 0.0
    H2 = 0.0
    H3 = 0.0
    CL = 0.0
    CL1 = 0.0
    CL2 = 0.0
    BL = 0.0
    BLa = 0.0
    BL90 = 0.0
    UW = 0.0
    LW = 0.0
    BodyHigh = 0.0
    BodyLow = 0.0
    BodyHigh = 0.0
    BodyLow = 0.0
    CumOffset = 0
    if _s_OnCalculate_prevtime == Time[0]:
        return rates_total
    _s_OnCalculate_prevtime = Time[0]
    shift = 0
    for shift in range(shift, rates_total - 9):
        CumOffset = 0
        setalert = 0
        counter = shift
        Range = 0.0
        AvgRange = 0.0
        counter = shift
        for counter in range(counter, shift + 9 + 1):
            AvgRange = AvgRange + MathAbs(High[counter] - Low[counter])
        else:
            counter = _range_end(counter, shift + 9 + 1, 1)
        Range = AvgRange / 10
        shift1 = shift + 1
        shift2 = shift + 2
        shift3 = shift + 3
        shift4 = shift + 4
        O = Open[shift1]
        O1 = Open[shift2]
        O2 = Open[shift3]
        H = High[shift1]
        H1 = High[shift2]
        H2 = High[shift3]
        H3 = High[shift4]
        L = Low[shift1]
        L1 = Low[shift2]
        L2 = Low[shift3]
        L3 = Low[shift4]
        C = Close[shift1]
        C1 = Close[shift2]
        C2 = Close[shift3]
        C3 = Close[shift4]
        if O > C:
            BodyHigh = O
            BodyLow = C
        else:
            BodyHigh = C
            BodyLow = O
        CL = High[shift1] - Low[shift1]
        CL1 = High[shift2] - Low[shift2]
        CL2 = High[shift3] - Low[shift3]
        BL = Open[shift1] - Close[shift1]
        UW = High[shift1] - BodyHigh
        LW = BodyLow - Low[shift1]
        BLa = MathAbs(BL)
        BL90 = BLa * Candle_WickBody_Percent
        if (H >= H1 and H > H2) and H > H3:
            if (((((UW / 2) > LW and UW > (2 * BL90)) and CL >= (CandleLength * Point())) and O != C) and (UW / 3) <= LW) and (UW / 4) <= LW:
                if Display_ShootStar_2:
                    MarkPattern(GetName('SS 2', Time[shift]), Time[shift1], High[shift1] + ((Pointer_Offset + Offset_ShootStar + High_Offset + CumOffset) * Point()), 'SS 2', Text_ShootStar, Color_ShootStar)
                    CumOffset = CumOffset + IncOffset
                    downArrow[shift1] = High[shift1] + (Pointer_Offset * Point())
                if Show_ShootStar_Alert_2:
                    if setalert == 0 and Show_Alert:
                        pattern = 'Shooting ShootStar 2'
                        setalert = 1
        if (H >= H1 and H > H2) and H > H3:
            if ((((UW / 3) > LW and UW > (2 * BL90)) and CL >= (CandleLength * Point())) and O != C) and (UW / 4) <= LW:
                if Display_ShootStar_3:
                    MarkPattern(GetName('SS 3', Time[shift]), Time[shift1], High[shift1] + ((Pointer_Offset + Offset_ShootStar + High_Offset + CumOffset) * Point()), 'SS 3', Text_ShootStar, Color_ShootStar)
                    CumOffset = CumOffset + IncOffset
                    downArrow[shift1] = High[shift1] + (Pointer_Offset * Point())
                if Show_ShootStar_Alert_3:
                    if setalert == 0 and Show_Alert:
                        pattern = 'Shooting ShootStar 3'
                        setalert = 1
        if (H >= H1 and H > H2) and H > H3:
            if (((UW / 4) > LW and UW > (2 * BL90)) and CL >= (CandleLength * Point())) and O != C:
                if Display_ShootStar_4:
                    MarkPattern(GetName('SS 4', Time[shift]), Time[shift1], High[shift1] + ((Pointer_Offset + Offset_ShootStar + High_Offset + CumOffset) * Point()), 'SS 4', Text_ShootStar, Color_ShootStar)
                    CumOffset = CumOffset + IncOffset
                    downArrow[shift1] = High[shift1] + (Pointer_Offset * Point())
                if Show_ShootStar_Alert_4:
                    if setalert == 0 and Show_Alert:
                        pattern = 'Shooting ShootStar 4'
                        setalert = 1
        if (H >= H1 and H1 > H2) and H1 > H3:
            if (((((BLa < (Star_Body_Length * Point()) and C2 > O2) and (not O) == C) and _fdiv(C2 - O2, H2 - L2) > Doji_Star_Ratio) and C1 > O1) and O > C) and CL >= (Star_MinLength * Point()):
                if Display_Stars:
                    MarkPattern(GetName('Star', Time[shift]), Time[shift1], High[shift1] + ((Pointer_Offset + Offset_Star + High_Offset + CumOffset) * Point()), 'E_Star', Text_Star, Color_Star)
                    CumOffset = CumOffset + IncOffset
                    downArrow[shift1] = High[shift1] + (Pointer_Offset * Point())
                if Show_Stars_Alert:
                    if setalert == 0 and Show_Alert:
                        pattern = 'Evening Star Pattern'
                        setalert = 1
        if (H >= H1 and H1 > H2) and H1 > H3:
            if ((O == C and (C2 > O2 and _fdiv(C2 - O2, H2 - L2) > Doji_Star_Ratio)) and C1 > O1) and CL >= (Doji_MinLength * Point()):
                if Display_Doji:
                    MarkPattern(GetName('Doji', Time[shift]), Time[shift1], High[shift1] + ((Pointer_Offset + Offset_Doji + High_Offset + CumOffset) * Point()), 'E_Doji', Text_Doji, Color_Doji)
                    CumOffset = CumOffset + IncOffset
                    downArrow[shift1] = High[shift1] + (Pointer_Offset * Point())
                if Show_Doji_Alert:
                    if setalert == 0 and Show_Alert:
                        pattern = 'Evening Doji Star Pattern'
                        setalert = 1
        if ((((C1 > O1 and ((C1 + O1) / 2) > C) and O > C) and C > O1) and _fdiv(O - C, H - L) > Piercing_Line_Ratio) and CL >= (Piercing_Candle_Length * Point()):
            if Display_Dark_Cloud_Cover:
                MarkPattern(GetName('DCC', Time[shift]), Time[shift1], High[shift1] + ((Pointer_Offset + Offset_DarkCC + High_Offset + CumOffset) * Point()), 'DCC', Text_DarkCC, Color_DarkCC)
                CumOffset = CumOffset + IncOffset
                downArrow[shift1] = High[shift1] + (Pointer_Offset * Point())
            if Show_DarkCC_Alert:
                if setalert == 0 and Show_Alert:
                    pattern = 'Dark Cloud Cover Pattern'
                    setalert = 1
        if ((((C1 > O1 and O > C) and O >= C1) and O1 >= C) and (O - C) > (C1 - O1)) and CL >= (Engulfing_Length * Point()):
            if Display_Bearish_Engulfing:
                MarkPattern(GetName('S_E', Time[shift]), Time[shift1], High[shift1] + ((Pointer_Offset + Offset_Bearish_Engulfing + High_Offset + CumOffset) * Point()), 'S_E', Text_Bearish_Engulfing, Color_Bearish_Engulfing)
                CumOffset = CumOffset + IncOffset
                downArrow[shift1] = High[shift1] + (Pointer_Offset * Point())
            if Show_Bearish_Engulfing_Alert:
                if setalert == 0 and Show_Alert:
                    pattern = 'Bearish Engulfing Pattern'
                    setalert = 1
        if (L <= L1 and L < L2) and L < L3:
            if (((((LW / 2) > UW and LW > BL90) and CL >= (CandleLength * Point())) and O != C) and (LW / 3) <= UW) and (LW / 4) <= UW:
                if Display_Hammer_2:
                    MarkPattern(GetName('HMR 2', Time[shift]), Time[shift1], Low[shift1] - ((Pointer_Offset + Offset_Hammer + CumOffset) * Point()), 'HMR 2', Text_Hammer, Color_Hammer)
                    CumOffset = CumOffset + IncOffset
                    upArrow[shift1] = Low[shift1] - (Pointer_Offset * Point())
                if Show_Hammer_Alert_2:
                    if setalert == 0 and Show_Alert:
                        pattern = 'Bullish Hammer 2'
                        setalert = 1
        if (L <= L1 and L < L2) and L < L3:
            if ((((LW / 3) > UW and LW > BL90) and CL >= (CandleLength * Point())) and O != C) and (LW / 4) <= UW:
                if Display_Hammer_3:
                    MarkPattern(GetName('HMR 3', Time[shift]), Time[shift1], Low[shift1] - ((Pointer_Offset + Offset_Hammer + CumOffset) * Point()), 'HMR 3', Text_Hammer, Color_Hammer)
                    CumOffset = CumOffset + IncOffset
                    upArrow[shift1] = Low[shift1] - (Pointer_Offset * Point())
                if Show_Hammer_Alert_3:
                    if setalert == 0 and Show_Alert:
                        pattern = 'Bullish Hammer 3'
                        setalert = 1
        if (L <= L1 and L < L2) and L < L3:
            if (((LW / 4) > UW and LW > BL90) and CL >= (CandleLength * Point())) and O != C:
                if Display_Hammer_4:
                    MarkPattern(GetName('HMR 4', Time[shift]), Time[shift1], Low[shift1] - ((Pointer_Offset + Offset_Hammer + CumOffset) * Point()), 'HMR 4', Text_Hammer, Color_Hammer)
                    CumOffset = CumOffset + IncOffset
                    upArrow[shift1] = Low[shift1] - (Pointer_Offset * Point())
                if Show_Hammer_Alert_4:
                    if setalert == 0 and Show_Alert:
                        pattern = 'Bullish Hammer 4'
                        setalert = 1
        if (L <= L1 and L1 < L2) and L1 < L3:
            if ((((BLa < (Star_Body_Length * Point()) and (not O) == C) and (O2 > C2 and _fdiv(O2 - C2, H2 - L2) > Doji_Star_Ratio)) and O1 > C1) and C > O) and CL >= (Star_MinLength * Point()):
                if Display_Stars:
                    MarkPattern(GetName('Star', Time[shift]), Time[shift1], Low[shift1] - ((Pointer_Offset + Offset_Star + CumOffset) * Point()), 'Star', Text_Star, Color_Hammer)
                    CumOffset = CumOffset + IncOffset
                    upArrow[shift1] = Low[shift1] - (Pointer_Offset * Point())
                if Show_Stars_Alert:
                    if setalert == 0 and Show_Alert:
                        pattern = 'Morning Star Pattern'
                        setalert = 1
        if (L <= L1 and L1 < L2) and L1 < L3:
            if ((O == C and (O2 > C2 and _fdiv(O2 - C2, H2 - L2) > Doji_Star_Ratio)) and O1 > C1) and CL >= (Doji_MinLength * Point()):
                if Display_Doji:
                    MarkPattern(GetName('Doji', Time[shift]), Time[shift1], Low[shift1] - ((Pointer_Offset + Offset_Doji + CumOffset) * Point()), 'Doji', Text_Doji, Color_Doji)
                    CumOffset = CumOffset + IncOffset
                    upArrow[shift1] = Low[shift1] - (Pointer_Offset * Point())
                if Show_Doji_Alert:
                    if shift == 0 and Show_Alert:
                        pattern = 'Morning Doji Pattern'
                        setalert = 1
        if (((C1 < O1 and ((O1 + C1) / 2) < C) and O < C) and _fdiv(C - O, H - L) > Piercing_Line_Ratio) and CL >= (Piercing_Candle_Length * Point()):
            if Display_Piercing_Line:
                MarkPattern(GetName('PrcLn', Time[shift]), Time[shift1], Low[shift1] - ((Pointer_Offset + Offset_Piercing_Line + CumOffset) * Point()), 'PrcLn', Text_Piercing_Line, Color_Piercing_Line)
                CumOffset = CumOffset + IncOffset
                upArrow[shift1] = Low[shift1] - (Pointer_Offset * Point())
            if Show_Piercing_Line_Alert:
                if shift == 0 and Show_Alert:
                    pattern = 'Piercing Line Pattern'
                    setalert = 1
        if ((((O1 > C1 and C > O) and C >= O1) and C1 >= O) and (C - O) > (O1 - C1)) and CL >= (Engulfing_Length * Point()):
            if Display_Bullish_Engulfing:
                MarkPattern(GetName('L_E', Time[shift]), Time[shift1], Low[shift1] - ((Pointer_Offset + Offset_Bullish_Engulfing + CumOffset) * Point()), 'L_E', Text_Bullish_Engulfing, Color_Bullish_Engulfing)
                CumOffset = CumOffset + IncOffset
                upArrow[shift1] = Low[shift1] - (Pointer_Offset * Point())
            if Show_Bullish_Engulfing_Alert:
                if shift == 0 and Show_Alert:
                    pattern = 'Bullish Engulfing Pattern'
                    setalert = 1
        if setalert == 1 and shift == 0:
            Alert(Symbol(), ' ', period, ' ', pattern)
            setalert = 0
        CumOffset = 0
    else:
        shift = _range_end(shift, rates_total - 9, 1)
    return rates_total

def GetName(aName, timeshift):
    return aName + DoubleToString(timeshift, 0)

def MarkPattern(name, time, price, shortname, fontsize, patterncolor):
    ObjectCreate(0, name, OBJ_TEXT, 0, time, price)
    ObjectSetString(0, name, OBJPROP_TEXT, shortname)
    ObjectSetString(0, name, OBJPROP_FONT, 'Times New Roman')
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, fontsize)
    ObjectSetInteger(0, name, OBJPROP_COLOR, patterncolor)

# ---- global variables initialised from expressions
Color_ShootStar = _input('Color_ShootStar', _uint(DeepPink))
Color_Hammer = _input('Color_Hammer', _uint(Blue))
Color_Doji = _input('Color_Doji', _uint(SpringGreen))
Color_Star = _input('Color_Star', _uint(Aqua))
Color_DarkCC = _input('Color_DarkCC', _uint(Brown))
Color_Piercing_Line = _input('Color_Piercing_Line', _uint(Blue))
Color_Bearish_Engulfing = _input('Color_Bearish_Engulfing', _uint(Red))
Color_Bullish_Engulfing = _input('Color_Bullish_Engulfing', _uint(Blue))

# ---- static local variables
_s_OnCalculate_prevtime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PatternsOnChart(_MQL5Indicator):
    name = 'patterns_on_chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'UseExtraDigit': False,
        'Show_Alert': True,
        'Display_ShootStar_2': True,
        'Show_ShootStar_Alert_2': True,
        'Display_ShootStar_3': True,
        'Show_ShootStar_Alert_3': True,
        'Display_ShootStar_4': True,
        'Show_ShootStar_Alert_4': True,
        'Display_Hammer_2': True,
        'Show_Hammer_Alert_2': True,
        'Display_Hammer_3': True,
        'Show_Hammer_Alert_3': True,
        'Display_Hammer_4': True,
        'Show_Hammer_Alert_4': True,
        'Display_Doji': True,
        'Show_Doji_Alert': True,
        'Display_Stars': True,
        'Show_Stars_Alert': True,
        'Star_Body_Length': 5,
        'Display_Dark_Cloud_Cover': True,
        'Show_DarkCC_Alert': True,
        'Display_Piercing_Line': True,
        'Show_Piercing_Line_Alert': True,
        'Display_Bearish_Engulfing': True,
        'Show_Bearish_Engulfing_Alert': True,
        'Display_Bullish_Engulfing': False,
        'Show_Bullish_Engulfing_Alert': False,
    }

