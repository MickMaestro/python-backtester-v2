"""Float — converted from MQL5: MQL5 Indicators/Float MT5/Float.mq5

Float - Trend strength, volume, Fibonacci and Dinapoli levels.
Link: https://t.me/ForexEaPremium; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'https://t.me/ForexEaPremium', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {2: 0}, 'labels': {1: 'Float Histogram', 2: 'Float Line'}, 'levels': [], 'description': ['Float - Trend strength, volume, Fibonacci and Dinapoli levels.'], 'name': 'Float', 'source': 'MQL5 Indicators/Float MT5/Float.mq5', 'folder': 'Float MT5', 'inputs': [{'mql': 'Float', 'py': 'Float', 'param': 'Float', 'type': 'int', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'ObjectPrefix', 'py': 'ObjectPrefix', 'param': None, 'type': 'string', 'default': 'FI-', 'label': '', 'sinput': False}, {'mql': 'DisableDinapoli', 'py': 'DisableDinapoli', 'param': 'DisableDinapoli', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'DisableFibonacci', 'py': 'DisableFibonacci', 'param': 'DisableFibonacci', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'DrawVerticalLinesAsBackground', 'py': 'DrawVerticalLinesAsBackground', 'param': 'DrawVerticalLinesAsBackground', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SwingBorderColor', 'py': 'SwingBorderColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'SwingBorderWidth', 'py': 'SwingBorderWidth', 'param': 'SwingBorderWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'SwingBorderStyle', 'py': 'SwingBorderStyle', 'param': 'SwingBorderStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SwingLinesColor', 'py': 'SwingLinesColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'SwingLinesWidth', 'py': 'SwingLinesWidth', 'param': 'SwingLinesWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'SwingLinesStyle', 'py': 'SwingLinesStyle', 'param': 'SwingLinesStyle', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'FiboColor', 'py': 'FiboColor', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'FiboWidth', 'py': 'FiboWidth', 'param': 'FiboWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FiboStyle', 'py': 'FiboStyle', 'param': 'FiboStyle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'DinapoliColor', 'py': 'DinapoliColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'DinapoliWidth', 'py': 'DinapoliWidth', 'param': 'DinapoliWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'DinapoliStyle', 'py': 'DinapoliStyle', 'param': 'DinapoliStyle', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Float = _input('Float', 200)
ObjectPrefix = _input('ObjectPrefix', 'FI-')
DisableDinapoli = _input('DisableDinapoli', False)
DisableFibonacci = _input('DisableFibonacci', False)
DrawVerticalLinesAsBackground = _input('DrawVerticalLinesAsBackground', False)
SwingBorderColor = _input('SwingBorderColor', clrBlue)
SwingBorderWidth = _input('SwingBorderWidth', 1)
SwingBorderStyle = _input('SwingBorderStyle', STYLE_SOLID)
SwingLinesColor = _input('SwingLinesColor', clrRed)
SwingLinesWidth = _input('SwingLinesWidth', 1)
SwingLinesStyle = _input('SwingLinesStyle', STYLE_DOT)
FiboColor = _input('FiboColor', clrGreen)
FiboWidth = _input('FiboWidth', 1)
FiboStyle = _input('FiboStyle', STYLE_DASH)
DinapoliColor = _input('DinapoliColor', clrRed)
DinapoliWidth = _input('DinapoliWidth', 1)
DinapoliStyle = _input('DinapoliStyle', STYLE_DOT)
prevbars = 0
Histogram = Arr(0, 0.0)
Line = Arr(0, 0.0)

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Float')
    SetIndexBuffer(0, Histogram, INDICATOR_DATA)
    SetIndexBuffer(1, Line, INDICATOR_DATA)
    ArraySetAsSeries(Histogram, True)
    ArraySetAsSeries(Line, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Float * 2)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Float * 2)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), ObjectPrefix)
    Comment('')

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, close, Volume, real_volume, spread):
    global prevbars
    if (rates_total - prevbars) < 1:
        return rates_total
    prevbars = rates_total
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Volume, True)
    ArraySetAsSeries(Time, True)
    first = True
    cumulativeV = 0
    FLOATV = 0.0
    high_bar = 0.0
    low_bar = 0.0
    bars_high = 0
    bars_low = 0
    shift = 0
    swing_time = 0
    cvstart = 0
    cvend = 0
    loopbegin1 = rates_total - Float
    shift = loopbegin1
    while shift >= 0:
        bars_high = iHighest(Symbol(), Period(), MODE_HIGH, Float, 1)
        bars_low = iLowest(Symbol(), Period(), MODE_LOW, Float, 1)
        high_bar = High[bars_high]
        low_bar = Low[bars_low]
        if bars_high < bars_low:
            cvstart = bars_low
            cvend = bars_high
        else:
            cvstart = bars_high
            cvend = bars_low
        if first and FLOATV == 0:
            shift = cvstart
            for shift in range(shift, cvend - 1, -1):
                FLOATV = FLOATV + Volume[shift]
                first = False
            else:
                shift = _range_end(shift, cvend - 1, -1)
        shift -= 1
    swing_time = MathAbs(bars_low - bars_high)
    shift = cvstart
    for shift in range(shift, 0 - 1, -1):
        cumulativeV += Volume[shift]
        if cumulativeV >= FLOATV:
            cumulativeV = 0
        Histogram[shift] = cumulativeV * 0.001
        Line[shift] = FLOATV * 0.001
    else:
        shift = _range_end(shift, 0 - 1, -1)
    Comment('\n', 'High was   ', bars_high, '  bars ago', '\n', 'Low was    ', bars_low, ' bars ago', '\n', '\n', 'Float time was    = ', swing_time, ' bars', '\n', 'Float volume left = ', FLOATV - cumulativeV, '\n', 'Float volume      = ', FLOATV)
    ObjectDelete(0, ObjectPrefix + 'Swingtop')
    ObjectCreate(0, ObjectPrefix + 'Swingtop', OBJ_TREND, 0, Time[cvstart], high_bar, Time[1], high_bar)
    ObjectSetInteger(0, ObjectPrefix + 'Swingtop', OBJPROP_STYLE, SwingBorderStyle)
    ObjectSetInteger(0, ObjectPrefix + 'Swingtop', OBJPROP_COLOR, SwingBorderColor)
    ObjectSetInteger(0, ObjectPrefix + 'Swingtop', OBJPROP_RAY_LEFT, 0)
    ObjectSetInteger(0, ObjectPrefix + 'Swingtop', OBJPROP_WIDTH, SwingBorderWidth)
    ObjectDelete(0, ObjectPrefix + 'Swingbottom')
    ObjectCreate(0, ObjectPrefix + 'Swingbottom', OBJ_TREND, 0, Time[cvstart], low_bar, Time[1], low_bar)
    ObjectSetInteger(0, ObjectPrefix + 'Swingbottom', OBJPROP_STYLE, SwingBorderStyle)
    ObjectSetInteger(0, ObjectPrefix + 'Swingbottom', OBJPROP_COLOR, SwingBorderColor)
    ObjectSetInteger(0, ObjectPrefix + 'Swingbottom', OBJPROP_RAY_LEFT, 0)
    ObjectSetInteger(0, ObjectPrefix + 'Swingbottom', OBJPROP_WIDTH, SwingBorderWidth)
    if (not DisableDinapoli) or (not DisableFibonacci):
        ObjectDelete(0, ObjectPrefix + 'Fib23')
        ObjectDelete(0, ObjectPrefix + 'Fib38')
        ObjectDelete(0, ObjectPrefix + 'Fib50')
        ObjectDelete(0, ObjectPrefix + 'Fib62')
        ObjectDelete(0, ObjectPrefix + 'Fib76')
        ObjectDelete(0, ObjectPrefix + 'Dinap0')
        ObjectDelete(0, ObjectPrefix + 'Dinap1')
        ObjectDelete(0, ObjectPrefix + 'Dinap2')
        ObjectDelete(0, ObjectPrefix + 'Dinap3')
        ObjectDelete(0, ObjectPrefix + 'Dinap4')
        ObjectDelete(0, ObjectPrefix + 'Dinap5')
        Fib23 = ((high_bar - low_bar) * 0.236) + low_bar
        Fib38 = ((high_bar - low_bar) * 0.382) + low_bar
        Fib50 = ((high_bar - low_bar) / 2) + low_bar
        Fib62 = ((high_bar - low_bar) * 0.618) + low_bar
        Fib76 = ((high_bar - low_bar) * 0.764) + low_bar
        if not DisableFibonacci:
            ObjectCreate(0, ObjectPrefix + 'Fib23', OBJ_TREND, 0, Time[cvstart], Fib23, Time[1], Fib23)
            ObjectSetInteger(0, ObjectPrefix + 'Fib23', OBJPROP_STYLE, FiboStyle)
            ObjectSetInteger(0, ObjectPrefix + 'Fib23', OBJPROP_COLOR, FiboColor)
            ObjectSetInteger(0, ObjectPrefix + 'Fib23', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Fib23', OBJPROP_WIDTH, FiboWidth)
            ObjectCreate(0, ObjectPrefix + 'Fib23t', OBJ_TEXT, 0, Time[1], Fib23)
            ObjectSetString(0, ObjectPrefix + 'Fib23t', OBJPROP_TEXT, '23.6')
            ObjectSetInteger(0, ObjectPrefix + 'Fib23t', OBJPROP_FONTSIZE, 8)
            ObjectSetString(0, ObjectPrefix + 'Fib23t', OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, ObjectPrefix + 'Fib23t', OBJPROP_COLOR, FiboColor)
            ObjectCreate(0, ObjectPrefix + 'Fib38', OBJ_TREND, 0, Time[cvstart], Fib38, Time[1], Fib38)
            ObjectSetInteger(0, ObjectPrefix + 'Fib38', OBJPROP_STYLE, FiboStyle)
            ObjectSetInteger(0, ObjectPrefix + 'Fib38', OBJPROP_COLOR, FiboColor)
            ObjectSetInteger(0, ObjectPrefix + 'Fib38', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Fib38', OBJPROP_WIDTH, FiboWidth)
            ObjectCreate(0, ObjectPrefix + 'Fib38t', OBJ_TEXT, 0, Time[1], Fib38)
            ObjectSetString(0, ObjectPrefix + 'Fib38t', OBJPROP_TEXT, '38.2')
            ObjectSetInteger(0, ObjectPrefix + 'Fib38t', OBJPROP_FONTSIZE, 8)
            ObjectSetString(0, ObjectPrefix + 'Fib38t', OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, ObjectPrefix + 'Fib38t', OBJPROP_COLOR, FiboColor)
            ObjectCreate(0, ObjectPrefix + 'Fib50', OBJ_TREND, 0, Time[cvstart], Fib50, Time[1], Fib50)
            ObjectSetInteger(0, ObjectPrefix + 'Fib50', OBJPROP_STYLE, STYLE_SOLID)
            ObjectSetInteger(0, ObjectPrefix + 'Fib50', OBJPROP_COLOR, FiboColor)
            ObjectSetInteger(0, ObjectPrefix + 'Fib50', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Fib50', OBJPROP_WIDTH, FiboWidth + 1)
            ObjectCreate(0, ObjectPrefix + 'Fib50t', OBJ_TEXT, 0, Time[1], Fib50)
            ObjectSetString(0, ObjectPrefix + 'Fib50t', OBJPROP_TEXT, '50.0')
            ObjectSetInteger(0, ObjectPrefix + 'Fib50t', OBJPROP_FONTSIZE, 8)
            ObjectSetString(0, ObjectPrefix + 'Fib50t', OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, ObjectPrefix + 'Fib50t', OBJPROP_COLOR, FiboColor)
            ObjectCreate(0, ObjectPrefix + 'Fib62', OBJ_TREND, 0, Time[cvstart], Fib62, Time[1], Fib62)
            ObjectSetInteger(0, ObjectPrefix + 'Fib62', OBJPROP_STYLE, FiboStyle)
            ObjectSetInteger(0, ObjectPrefix + 'Fib62', OBJPROP_COLOR, FiboColor)
            ObjectSetInteger(0, ObjectPrefix + 'Fib62', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Fib62', OBJPROP_WIDTH, FiboWidth)
            ObjectCreate(0, ObjectPrefix + 'Fib62t', OBJ_TEXT, 0, Time[1], Fib62)
            ObjectSetString(0, ObjectPrefix + 'Fib62t', OBJPROP_TEXT, '61.8')
            ObjectSetInteger(0, ObjectPrefix + 'Fib62t', OBJPROP_FONTSIZE, 8)
            ObjectSetString(0, ObjectPrefix + 'Fib62t', OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, ObjectPrefix + 'Fib62t', OBJPROP_COLOR, FiboColor)
            ObjectCreate(0, ObjectPrefix + 'Fib76', OBJ_TREND, 0, Time[cvstart], Fib76, Time[1], Fib76)
            ObjectSetInteger(0, ObjectPrefix + 'Fib76', OBJPROP_STYLE, FiboStyle)
            ObjectSetInteger(0, ObjectPrefix + 'Fib76', OBJPROP_COLOR, FiboColor)
            ObjectSetInteger(0, ObjectPrefix + 'Fib76', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Fib76', OBJPROP_WIDTH, FiboWidth)
            ObjectCreate(0, ObjectPrefix + 'Fib76t', OBJ_TEXT, 0, Time[1], Fib76)
            ObjectSetString(0, ObjectPrefix + 'Fib76t', OBJPROP_TEXT, '76.4')
            ObjectSetInteger(0, ObjectPrefix + 'Fib76t', OBJPROP_FONTSIZE, 8)
            ObjectSetString(0, ObjectPrefix + 'Fib76t', OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, ObjectPrefix + 'Fib76t', OBJPROP_COLOR, FiboColor)
        if not DisableDinapoli:
            Dinap0 = (low_bar + Fib23) / 2
            Dinap1 = (Fib23 + Fib38) / 2
            Dinap2 = (Fib38 + Fib50) / 2
            Dinap3 = (Fib50 + Fib62) / 2
            Dinap4 = (Fib62 + Fib76) / 2
            Dinap5 = (high_bar + Fib76) / 2
            ObjectCreate(0, ObjectPrefix + 'Dinap0', OBJ_TREND, 0, Time[cvstart], Dinap0, Time[1], Dinap0)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap0', OBJPROP_STYLE, DinapoliStyle)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap0', OBJPROP_COLOR, DinapoliColor)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap0', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap0', OBJPROP_WIDTH, DinapoliWidth)
            ObjectCreate(0, ObjectPrefix + 'Dinap1', OBJ_TREND, 0, Time[cvstart], Dinap1, Time[1], Dinap1)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap1', OBJPROP_STYLE, DinapoliStyle)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap1', OBJPROP_COLOR, DinapoliColor)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap1', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap1', OBJPROP_WIDTH, DinapoliWidth)
            ObjectCreate(0, ObjectPrefix + 'Dinap2', OBJ_TREND, 0, Time[cvstart], Dinap2, Time[1], Dinap2)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap2', OBJPROP_STYLE, DinapoliStyle)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap2', OBJPROP_COLOR, DinapoliColor)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap2', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap2', OBJPROP_WIDTH, DinapoliWidth)
            ObjectCreate(0, ObjectPrefix + 'Dinap3', OBJ_TREND, 0, Time[cvstart], Dinap3, Time[1], Dinap3)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap3', OBJPROP_STYLE, DinapoliStyle)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap3', OBJPROP_COLOR, DinapoliColor)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap3', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap3', OBJPROP_WIDTH, DinapoliWidth)
            ObjectCreate(0, ObjectPrefix + 'Dinap4', OBJ_TREND, 0, Time[cvstart], Dinap4, Time[1], Dinap4)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap4', OBJPROP_STYLE, DinapoliStyle)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap4', OBJPROP_COLOR, DinapoliColor)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap4', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap4', OBJPROP_WIDTH, DinapoliWidth)
            ObjectCreate(0, ObjectPrefix + 'Dinap5', OBJ_TREND, 0, Time[cvstart], Dinap5, Time[1], Dinap5)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap5', OBJPROP_STYLE, DinapoliStyle)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap5', OBJPROP_COLOR, clrRed)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap5', OBJPROP_RAY_LEFT, 0)
            ObjectSetInteger(0, ObjectPrefix + 'Dinap5', OBJPROP_WIDTH, 1)
    ObjectDelete(0, ObjectPrefix + 'CVSTART')
    ObjectCreate(0, ObjectPrefix + 'CVSTART', OBJ_TREND, 0, Time[cvstart], high_bar, Time[cvstart], low_bar * Point())
    ObjectSetInteger(0, ObjectPrefix + 'CVSTART', OBJPROP_STYLE, SwingBorderStyle)
    ObjectSetInteger(0, ObjectPrefix + 'CVSTART', OBJPROP_COLOR, SwingBorderColor)
    ObjectSetInteger(0, ObjectPrefix + 'CVSTART', OBJPROP_RAY_LEFT, 0)
    ObjectSetInteger(0, ObjectPrefix + 'CVSTART', OBJPROP_WIDTH, SwingBorderWidth)
    ObjectSetInteger(0, ObjectPrefix + 'CVSTART', OBJPROP_BACK, DrawVerticalLinesAsBackground)
    ObjectDelete(0, ObjectPrefix + 'CVEND')
    ObjectCreate(0, ObjectPrefix + 'CVEND', OBJ_TREND, 0, Time[cvend], high_bar, Time[cvend], low_bar * Point())
    ObjectSetInteger(0, ObjectPrefix + 'CVEND', OBJPROP_STYLE, SwingBorderStyle)
    ObjectSetInteger(0, ObjectPrefix + 'CVEND', OBJPROP_COLOR, SwingBorderColor)
    ObjectSetInteger(0, ObjectPrefix + 'CVEND', OBJPROP_RAY_LEFT, 0)
    ObjectSetInteger(0, ObjectPrefix + 'CVEND', OBJPROP_WIDTH, SwingBorderWidth)
    ObjectSetInteger(0, ObjectPrefix + 'CVEND', OBJPROP_BACK, DrawVerticalLinesAsBackground)
    ObjectDelete(0, ObjectPrefix + 'Swingend')
    if (cvend - swing_time) > 0:
        ObjectCreate(0, ObjectPrefix + 'Swingend', OBJ_TREND, 0, Time[cvend - swing_time + 5], high_bar, Time[cvend - swing_time + 5], low_bar)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend', OBJPROP_STYLE, SwingLinesStyle)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend', OBJPROP_COLOR, SwingLinesColor)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend', OBJPROP_RAY_LEFT, 0)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend', OBJPROP_WIDTH, SwingLinesWidth)
    ObjectDelete(0, ObjectPrefix + 'Swingend2')
    if (cvend - (swing_time * 2)) > 0:
        ObjectCreate(0, ObjectPrefix + 'Swingend2', OBJ_TREND, 0, Time[cvend - (swing_time * 2) + 5], high_bar, Time[cvend - (swing_time * 2) + 5], low_bar)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend2', OBJPROP_STYLE, SwingLinesStyle)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend2', OBJPROP_COLOR, SwingLinesColor)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend2', OBJPROP_RAY_LEFT, 0)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend2', OBJPROP_WIDTH, SwingLinesWidth)
    ObjectDelete(0, ObjectPrefix + 'Swingend3')
    if (cvend - (swing_time * 3)) > 0:
        ObjectCreate(0, ObjectPrefix + 'Swingend3', OBJ_TREND, 0, Time[cvend - (swing_time * 3) + 5], high_bar, Time[cvend - (swing_time * 3) + 5], low_bar)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend3', OBJPROP_STYLE, SwingLinesStyle)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend3', OBJPROP_COLOR, SwingLinesColor)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend3', OBJPROP_RAY_LEFT, 0)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend3', OBJPROP_WIDTH, SwingLinesWidth)
    ObjectDelete(0, ObjectPrefix + 'Swingend4')
    if (cvend - (swing_time * 4)) > 0:
        ObjectCreate(0, ObjectPrefix + 'Swingend4', OBJ_TREND, 0, Time[cvend - (swing_time * 4) + 5], high_bar, Time[cvend - (swing_time * 4) + 5], low_bar)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend4', OBJPROP_STYLE, SwingLinesStyle)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend4', OBJPROP_COLOR, SwingLinesColor)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend4', OBJPROP_RAY_LEFT, 0)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend4', OBJPROP_WIDTH, SwingLinesWidth)
    ObjectDelete(0, ObjectPrefix + 'Swingend5')
    if (cvend - (swing_time * 5)) > 0:
        ObjectCreate(0, ObjectPrefix + 'Swingend5', OBJ_TREND, 0, Time[cvend - (swing_time * 5) + 5], high_bar, Time[cvend - (swing_time * 5) + 5], low_bar)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend5', OBJPROP_STYLE, SwingLinesStyle)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend5', OBJPROP_COLOR, SwingLinesColor)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend5', OBJPROP_RAY_LEFT, 0)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend5', OBJPROP_WIDTH, SwingLinesWidth)
    ObjectDelete(0, ObjectPrefix + 'Swingend6')
    if (cvend - (swing_time * 6)) > 0:
        ObjectCreate(0, ObjectPrefix + 'Swingend6', OBJ_TREND, 0, Time[cvend - (swing_time * 6) + 5], high_bar, Time[cvend - (swing_time * 6) + 5], low_bar)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend6', OBJPROP_STYLE, SwingLinesStyle)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend6', OBJPROP_COLOR, SwingLinesColor)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend6', OBJPROP_RAY_LEFT, 0)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend6', OBJPROP_WIDTH, SwingLinesWidth)
    ObjectDelete(0, ObjectPrefix + 'Swingend7')
    if (cvend - (swing_time * 7)) > 0:
        ObjectCreate(0, ObjectPrefix + 'Swingend7', OBJ_TREND, 0, Time[cvend - (swing_time * 7) + 5], high_bar, Time[cvend - (swing_time * 7) + 5], low_bar)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend7', OBJPROP_STYLE, SwingLinesStyle)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend7', OBJPROP_COLOR, SwingLinesColor)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend7', OBJPROP_RAY_LEFT, 0)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend7', OBJPROP_WIDTH, SwingLinesWidth)
    ObjectDelete(0, ObjectPrefix + 'Swingend8')
    if (cvend - (swing_time * 8)) > 0:
        ObjectCreate(0, ObjectPrefix + 'Swingend8', OBJ_TREND, 0, Time[cvend - (swing_time * 8) + 5], high_bar, Time[cvend - (swing_time * 8) + 5], low_bar)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend8', OBJPROP_STYLE, SwingLinesStyle)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend8', OBJPROP_COLOR, SwingLinesColor)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend8', OBJPROP_RAY_LEFT, 0)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend8', OBJPROP_WIDTH, SwingLinesWidth)
    ObjectDelete(0, ObjectPrefix + 'Swingend9')
    if (cvend - (swing_time * 9)) > 0:
        ObjectCreate(0, ObjectPrefix + 'Swingend9', OBJ_TREND, 0, Time[cvend - (swing_time * 9) + 5], high_bar, Time[cvend - (swing_time * 9) + 5], low_bar)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend9', OBJPROP_STYLE, SwingLinesStyle)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend9', OBJPROP_COLOR, SwingLinesColor)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend9', OBJPROP_RAY_LEFT, 0)
        ObjectSetInteger(0, ObjectPrefix + 'Swingend9', OBJPROP_WIDTH, SwingLinesWidth)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FloatIndicator(_MQL5Indicator):
    name = 'Float'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Float': 200,
        'DisableDinapoli': False,
        'DisableFibonacci': False,
        'DrawVerticalLinesAsBackground': False,
        'SwingBorderWidth': 1,
        'SwingBorderStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'SwingLinesWidth': 1,
        'SwingLinesStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),
        'FiboWidth': 1,
        'FiboStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),
        'DinapoliWidth': 1,
        'DinapoliStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),
    }

