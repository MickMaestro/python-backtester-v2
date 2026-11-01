"""size_highs_and_lows — converted from MQL5: MQL5 Indicators/Size Highs And Lows/size_highs_and_lows.mq5

email: hello.tol64@gmail.com
Copyright: Copyright 2011, tol64.; Link: https://login.mql5.com/en/users/tol64; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, tol64.', 'link': 'https://login.mql5.com/en/users/tol64', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 3, 2: 3, 3: 1, 4: 1, 5: 3, 6: 3}, 'colors': {1: [55295], 2: [65280], 3: [55295], 4: [65280], 5: [1993170], 6: [5737262]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['email: hello.tol64@gmail.com'], 'name': 'size_highs_and_lows', 'source': 'MQL5 Indicators/Size Highs And Lows/size_highs_and_lows.mq5', 'folder': 'Size Highs And Lows', 'inputs': [{'mql': 'minHighPeriod', 'py': 'minHighPeriod', 'param': 'minHighPeriod', 'type': 'int', 'default': 14, 'label': 'Period Max High', 'sinput': False}, {'mql': 'minLowPeriod', 'py': 'minLowPeriod', 'param': 'minLowPeriod', 'type': 'int', 'default': 14, 'label': 'Period Max Low', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
minHighPeriod = _input('minHighPeriod', 14)  # Period Max High
minLowPeriod = _input('minLowPeriod', 14)  # Period Max Low
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
maxHighBuffer = Arr(0, 0.0)
maxLowBuffer = Arr(0, 0.0)
ColorHighBuffer = Arr(0, 0.0)
ColorLowBuffer = Arr(0, 0.0)
minH = 0
minL = 0

def OnInit():
    global minH, minL
    if minHighPeriod <= 0:
        minH = 14
        printf('Incorrect input parameter minHighPeriod = %d. Indicator will use value %d for calculations.', minHighPeriod, minH)
    else:
        minH = minHighPeriod
    if minLowPeriod <= 0:
        minL = 14
        printf('Incorrect input parameter minLowPeriod = %d. Indicator will use value %d for calculations.', minLowPeriod, minL)
    else:
        minL = minLowPeriod
    short_name = 'SIZE HIGHS / LOWS:'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    SetIndexBuffer(0, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, maxHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, maxLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ColorHighBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, ColorLowBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, minHighPeriod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, minLowPeriod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, minHighPeriod)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, minLowPeriod)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, minHighPeriod)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, minLowPeriod)
    PlotIndexSetInteger(0, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 4)
    PlotIndexSetInteger(1, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 4)
    PlotIndexSetInteger(2, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, 1)
    PlotIndexSetInteger(3, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(3, PLOT_LINE_WIDTH, 1)
    PlotIndexSetInteger(4, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(4, PLOT_LINE_WIDTH, 4)
    PlotIndexSetInteger(5, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(5, PLOT_LINE_WIDTH, 4)
    PlotIndexSetString(0, PLOT_LABEL, 'Size Highs')
    PlotIndexSetString(1, PLOT_LABEL, 'Size Lows')
    PlotIndexSetString(2, PLOT_LABEL, 'Max Size Highs')
    PlotIndexSetString(3, PLOT_LABEL, 'Max Size Lows')
    PlotIndexSetString(4, PLOT_LABEL, '')
    PlotIndexSetString(5, PLOT_LABEL, '')
    IndicatorSetInteger(INDICATOR_LEVELS, 12)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, clrSilver)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, vDgtMlt(Digits() * 2) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, vDgtMlt(Digits() * 4) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, vDgtMlt(Digits() * 6) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, vDgtMlt(Digits() * 8) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, vDgtMlt(Digits() * 10) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, vDgtMlt(Digits() * 12) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 6, (-vDgtMlt(Digits() * 2)) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 7, (-vDgtMlt(Digits() * 4)) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 8, (-vDgtMlt(Digits() * 6)) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 9, (-vDgtMlt(Digits() * 8)) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 10, (-vDgtMlt(Digits() * 10)) * Point())
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 11, (-vDgtMlt(Digits() * 12)) * Point())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if rates_total <= minHighPeriod:
        return 0
    if rates_total <= minLowPeriod:
        return 0
    if prev_calculated == 0:
        HighBuffer[0] = EMPTY_VALUE
        LowBuffer[0] = EMPTY_VALUE
        maxHighBuffer[0] = EMPTY_VALUE
        maxLowBuffer[0] = EMPTY_VALUE
        ColorHighBuffer[0] = EMPTY_VALUE
        ColorLowBuffer[0] = EMPTY_VALUE
        limit = 1
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        if Close[i] > Open[i]:
            HighBuffer[i] = ND_dgt(High[i], Digits()) - ND_dgt(Close[i], Digits())
            maxHighBuffer[i] = ND_dgt(Highest(HighBuffer, minHighPeriod, i), Digits())
            if Close[i] < Open[i]:
                ColorHighBuffer[i] = HighBuffer[i]
            elif Close[i] > Open[i]:
                ColorHighBuffer[i] = EMPTY_VALUE
            else:
                ColorHighBuffer[i] = EMPTY_VALUE
        elif Close[i] < Open[i]:
            HighBuffer[i] = ND_dgt(High[i], Digits()) - ND_dgt(Open[i], Digits())
            maxHighBuffer[i] = ND_dgt(Highest(HighBuffer, minHighPeriod, i), Digits())
            if Close[i] < Open[i]:
                ColorHighBuffer[i] = HighBuffer[i]
            elif Close[i] > Open[i]:
                ColorHighBuffer[i] = EMPTY_VALUE
            else:
                ColorHighBuffer[i] = EMPTY_VALUE
        else:
            HighBuffer[i] = 0.0
            maxHighBuffer[i] = maxHighBuffer[i - 1]
            ColorHighBuffer[i] = EMPTY_VALUE
        if Close[i] > Open[i]:
            LowBuffer[i] = ND_dgt(Low[i], Digits()) - ND_dgt(Open[i], Digits())
            maxLowBuffer[i] = ND_dgt(Lowest(LowBuffer, minLowPeriod, i), Digits())
            if Close[i] > Open[i]:
                ColorLowBuffer[i] = LowBuffer[i]
            elif Close[i] < Open[i]:
                ColorLowBuffer[i] = EMPTY_VALUE
            else:
                ColorLowBuffer[i] = EMPTY_VALUE
        elif Close[i] < Open[i]:
            LowBuffer[i] = ND_dgt(Low[i], Digits()) - ND_dgt(Close[i], Digits())
            maxLowBuffer[i] = ND_dgt(Lowest(LowBuffer, minLowPeriod, i), Digits())
            if Close[i] > Open[i]:
                ColorLowBuffer[i] = LowBuffer[i]
            elif Close[i] < Open[i]:
                ColorLowBuffer[i] = EMPTY_VALUE
            else:
                ColorLowBuffer[i] = EMPTY_VALUE
        else:
            LowBuffer[i] = 0.0
            maxLowBuffer[i] = maxLowBuffer[i - 1]
            ColorLowBuffer[i] = EMPTY_VALUE
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def Highest(array, range_, fromIndex):
    i = 0
    res = 0.0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res < array[i]:
            res = array[i]
        i -= 1
    return res

def Lowest(array, range_, fromIndex):
    i = 0
    res = 0.0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res > array[i]:
            res = array[i]
        i -= 1
    return res

def vDgtMlt(value):
    if Digits() == 3 or Digits() == 5:
        return (value := value * 10)
    else:
        return value

def DS_dgt(aValue, digit):
    return DoubleToString(aValue, digit)

def ND_dgt(aValue, digit):
    return NormalizeDouble(aValue, digit)

def DSNDdgt(aValue, digit):
    return DS_dgt(ND_dgt(aValue, digit), digit)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SizeHighsAndLows(_MQL5Indicator):
    name = 'size_highs_and_lows'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'minHighPeriod': 14,  # Period Max High
        'minLowPeriod': 14,  # Period Max Low
    }

