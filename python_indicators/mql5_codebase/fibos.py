"""fibos — converted from MQL5: MQL5 Indicators/Auto Fibonacci Indicator (Auto Fibos)/fibos.mq5

Copyright: Coders' Guru; Link: http://www.xpworx.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': "Coders' Guru", 'link': 'http://www.xpworx.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'fibos', 'source': 'MQL5 Indicators/Auto Fibonacci Indicator (Auto Fibos)/fibos.mq5', 'folder': 'Auto Fibonacci Indicator (Auto Fibos)', 'inputs': [{'mql': 'HighToLow', 'py': 'HighToLow', 'param': 'HighToLow', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Fibo_Level_1', 'py': 'Fibo_Level_1', 'param': 'Fibo_Level_1', 'type': 'double', 'default': 0.236, 'label': '', 'sinput': False}, {'mql': 'Fibo_Level_2', 'py': 'Fibo_Level_2', 'param': 'Fibo_Level_2', 'type': 'double', 'default': 0.382, 'label': '', 'sinput': False}, {'mql': 'Fibo_Level_3', 'py': 'Fibo_Level_3', 'param': 'Fibo_Level_3', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'Fibo_Level_4', 'py': 'Fibo_Level_4', 'param': 'Fibo_Level_4', 'type': 'double', 'default': 0.618, 'label': '', 'sinput': False}, {'mql': 'Fibo_Level_5', 'py': 'Fibo_Level_5', 'param': 'Fibo_Level_5', 'type': 'double', 'default': 0.764, 'label': '', 'sinput': False}, {'mql': 'Fibo_Level_6', 'py': 'Fibo_Level_6', 'param': 'Fibo_Level_6', 'type': 'double', 'default': 0.886, 'label': '', 'sinput': False}, {'mql': 'StartBar', 'py': 'StartBar', 'param': 'StartBar', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'BarsBack', 'py': 'BarsBack', 'param': 'BarsBack', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'Pause', 'py': 'Pause', 'param': 'Pause', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HighToLow = _input('HighToLow', True)
Fibo_Level_1 = _input('Fibo_Level_1', 0.236)
Fibo_Level_2 = _input('Fibo_Level_2', 0.382)
Fibo_Level_3 = _input('Fibo_Level_3', 0.5)
Fibo_Level_4 = _input('Fibo_Level_4', 0.618)
Fibo_Level_5 = _input('Fibo_Level_5', 0.764)
Fibo_Level_6 = _input('Fibo_Level_6', 0.886)
StartBar = _input('StartBar', 0)
BarsBack = _input('BarsBack', 20)
Pause = _input('Pause', False)
VerticalLinesColor = clrRed
FiboLinesColors = clrBlue
Fibo_Level_0 = 0.0
Fibo_Level_7 = 1.0
f_1 = Arr(0, 0.0)
f_2 = Arr(0, 0.0)
f_3 = Arr(0, 0.0)
f_4 = Arr(0, 0.0)
f_5 = Arr(0, 0.0)
f_6 = Arr(0, 0.0)
f_7 = Arr(0, 0.0)
f_8 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, f_1, INDICATOR_DATA)
    SetIndexBuffer(1, f_2, INDICATOR_DATA)
    SetIndexBuffer(2, f_3, INDICATOR_DATA)
    SetIndexBuffer(3, f_4, INDICATOR_DATA)
    SetIndexBuffer(4, f_5, INDICATOR_DATA)
    SetIndexBuffer(5, f_6, INDICATOR_DATA)
    SetIndexBuffer(6, f_7, INDICATOR_DATA)
    SetIndexBuffer(7, f_8, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Fibo_' + DoubleToString(Fibo_Level_0, 4))
    PlotIndexSetString(1, PLOT_LABEL, 'Fibo_' + DoubleToString(Fibo_Level_1, 4))
    PlotIndexSetString(2, PLOT_LABEL, 'Fibo_' + DoubleToString(Fibo_Level_2, 4))
    PlotIndexSetString(3, PLOT_LABEL, 'Fibo_' + DoubleToString(Fibo_Level_3, 4))
    PlotIndexSetString(4, PLOT_LABEL, 'Fibo_' + DoubleToString(Fibo_Level_4, 4))
    PlotIndexSetString(5, PLOT_LABEL, 'Fibo_' + DoubleToString(Fibo_Level_5, 4))
    PlotIndexSetString(6, PLOT_LABEL, 'Fibo_' + DoubleToString(Fibo_Level_6, 4))
    PlotIndexSetString(7, PLOT_LABEL, 'Fibo_' + DoubleToString(Fibo_Level_7, 4))
    ObjectsDeleteAll(0)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Pause == False:
        LowBar = 0
        HighBar = 0
        LowValue = 0.0
        HighValue = 0.0
        lowest_bar = iLowest_u("", 0, 1, BarsBack, StartBar)
        highest_bar = iHighest_u("", 0, 2, BarsBack, StartBar)
        higher_point = 0.0
        lower_point = 0.0
        HighValue = High(highest_bar)
        LowValue = Low(lowest_bar)
        if HighToLow:
            DrawVerticalLine('v_u_hl', highest_bar, VerticalLinesColor)
            DrawVerticalLine('v_l_hl', lowest_bar, VerticalLinesColor)
            if ObjectFind(0, 'trend_hl') < 0:
                ObjectCreate(0, 'trend_hl', OBJ_TREND, 0, Time(highest_bar), HighValue, Time(lowest_bar), LowValue)
            ObjectSetInteger(0, 'trend_hl', OBJPROP_TIME, 0, Time(highest_bar))
            ObjectSetInteger(0, 'trend_hl', OBJPROP_TIME, 1, Time(lowest_bar))
            ObjectSetDouble(0, 'trend_hl', OBJPROP_PRICE, 0, HighValue)
            ObjectSetDouble(0, 'trend_hl', OBJPROP_PRICE, 1, LowValue)
            ObjectSetInteger(0, 'trend_hl', OBJPROP_COLOR, VerticalLinesColor)
            ObjectSetInteger(0, 'trend_hl', OBJPROP_STYLE, STYLE_DOT)
            ObjectSetInteger(0, 'trend_hl', OBJPROP_RAY, False)
            if ObjectFind(0, 'Fibo_hl') < 0:
                ObjectCreate(0, 'Fibo_hl', OBJ_FIBO, 0, 0, HighValue, 0, LowValue)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_PRICE, 0, HighValue)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_PRICE, 1, LowValue)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_TIME, 0, Time(highest_bar))
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_TIME, 1, Time(lowest_bar))
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_COLOR, FiboLinesColors)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELCOLOR, 0, FiboLinesColors)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELCOLOR, 1, FiboLinesColors)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELCOLOR, 2, FiboLinesColors)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELCOLOR, 3, FiboLinesColors)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELCOLOR, 4, FiboLinesColors)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELCOLOR, 5, FiboLinesColors)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELCOLOR, 6, FiboLinesColors)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELCOLOR, 7, FiboLinesColors)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELS, 8)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 0, Fibo_Level_0)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 1, Fibo_Level_1)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 2, Fibo_Level_2)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 3, Fibo_Level_3)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 4, Fibo_Level_4)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 5, Fibo_Level_5)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 6, Fibo_Level_6)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 7, Fibo_Level_7)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_RAY_RIGHT, True)
            ChartRedraw()
            for i in range(prev_calculated, rates_total):
                f_8[i] = NormalizeDouble(LowValue + ((HighValue - LowValue) * Fibo_Level_7), Digits())
                f_7[i] = NormalizeDouble(LowValue + ((HighValue - LowValue) * Fibo_Level_6), Digits())
                f_6[i] = NormalizeDouble(LowValue + ((HighValue - LowValue) * Fibo_Level_5), Digits())
                f_5[i] = NormalizeDouble(LowValue + ((HighValue - LowValue) * Fibo_Level_4), Digits())
                f_4[i] = NormalizeDouble(LowValue + ((HighValue - LowValue) * Fibo_Level_3), Digits())
                f_3[i] = NormalizeDouble(LowValue + ((HighValue - LowValue) * Fibo_Level_2), Digits())
                f_2[i] = NormalizeDouble(LowValue + ((HighValue - LowValue) * Fibo_Level_1), Digits())
                f_1[i] = NormalizeDouble(LowValue + ((HighValue - LowValue) * Fibo_Level_0), Digits())
        else:
            DrawVerticalLine('v_u_hl', highest_bar, VerticalLinesColor)
            DrawVerticalLine('v_l_hl', lowest_bar, VerticalLinesColor)
            if ObjectFind(0, 'trend_hl') < 0:
                ObjectCreate(0, 'trend_hl', OBJ_TREND, 0, Time(lowest_bar), LowValue, Time(highest_bar), HighValue)
            ObjectSetInteger(0, 'trend_hl', OBJPROP_TIME, 0, Time(lowest_bar))
            ObjectSetInteger(0, 'trend_hl', OBJPROP_TIME, 1, Time(highest_bar))
            ObjectSetDouble(0, 'trend_hl', OBJPROP_PRICE, 0, LowValue)
            ObjectSetDouble(0, 'trend_hl', OBJPROP_PRICE, 1, HighValue)
            ObjectSetInteger(0, 'trend_hl', OBJPROP_STYLE, STYLE_DOT)
            ObjectSetInteger(0, 'trend_hl', OBJPROP_RAY, False)
            if ObjectFind(0, 'Fibo_hl') < 0:
                ObjectCreate(0, 'Fibo_hl', OBJ_FIBO, 0, 0, LowValue, 0, HighValue)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_PRICE, 0, LowValue)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_PRICE, 1, HighValue)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_TIME, 0, Time(lowest_bar))
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_TIME, 1, Time(highest_bar))
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELCOLOR, FiboLinesColors)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_LEVELS, 8)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 0, Fibo_Level_0)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 1, Fibo_Level_1)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 2, Fibo_Level_2)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 3, Fibo_Level_3)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 4, Fibo_Level_4)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 5, Fibo_Level_5)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 6, Fibo_Level_6)
            ObjectSetDouble(0, 'Fibo_hl', OBJPROP_LEVELVALUE, 7, Fibo_Level_7)
            ObjectSetInteger(0, 'Fibo_hl', OBJPROP_RAY_RIGHT, True)
            ChartRedraw()
            for i in range(prev_calculated, rates_total):
                f_8[i] = NormalizeDouble(LowValue, Digits())
                f_7[i] = NormalizeDouble(HighValue - ((HighValue - LowValue) * Fibo_Level_6), Digits())
                f_6[i] = NormalizeDouble(HighValue - ((HighValue - LowValue) * Fibo_Level_5), Digits())
                f_5[i] = NormalizeDouble(HighValue - ((HighValue - LowValue) * Fibo_Level_4), Digits())
                f_4[i] = NormalizeDouble(HighValue - ((HighValue - LowValue) * Fibo_Level_3), Digits())
                f_3[i] = NormalizeDouble(HighValue - ((HighValue - LowValue) * Fibo_Level_2), Digits())
                f_2[i] = NormalizeDouble(HighValue - ((HighValue - LowValue) * Fibo_Level_1), Digits())
                f_1[i] = NormalizeDouble(HighValue, Digits())
    return rates_total

def DrawVerticalLine(name, bar, clr):
    if ObjectFind(0, name) < 0:
        ObjectCreate(0, name, OBJ_VLINE, 0, Time(bar), 0)
        ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DASH)
        ObjectSetInteger(0, name, OBJPROP_WIDTH, 1)
        ChartRedraw()
    else:
        ObjectSetInteger(0, name, OBJPROP_TIME, Time(bar))
        ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DASH)
        ObjectSetInteger(0, name, OBJPROP_WIDTH, 1)
        ChartRedraw()

def OnDeinit(reason):
    ObjectsDeleteAll(0)

def iHighest_u(symbol, timeframe, type_=2, count=WHOLE_ARRAY, start=0):
    if start < 0:
        return -1
    if count == 0:
        count = Bars(symbol, ToTimeFrame(timeframe))
    if type_ == 2:
        Arr_ = Arr(0, 0.0)
        if CopyHigh(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMaximum(Arr_) - 1 + start
        else:
            return -1
    elif type_ == 1:
        Arr_ = Arr(0, 0.0)
        if CopyLow(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMaximum(Arr_) - 1 + start
        else:
            return -1
    elif type_ == 0:
        Arr_ = Arr(0, 0.0)
        if CopyOpen(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMaximum(Arr_) - 1 + start
        else:
            return -1
    elif type_ == 3:
        Arr_ = Arr(0, 0.0)
        if CopyClose(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMaximum(Arr_) - 1 + start
        else:
            return -1
    elif type_ == 4:
        Arr_ = Arr(0, 0)
        if CopyTickVolume(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMaximum(Arr_) - 1 + start
        else:
            return -1
    elif type_ == 5:
        Arr_ = Arr(0, 0)
        if CopyRealVolume(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMaximum(Arr_) - 1 + start
        else:
            return -1
    else:
        return -1

def iLowest_u(symbol, timeframe, type_=1, count=WHOLE_ARRAY, start=0):
    if start < 0:
        return -1
    if count == 0:
        count = Bars(symbol, ToTimeFrame(timeframe))
    if type_ == 1:
        Arr_ = Arr(0, 0.0)
        if CopyLow(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMinimum(Arr_) - 1 + start
        else:
            return -1
    elif type_ == 2:
        Arr_ = Arr(0, 0.0)
        if CopyHigh(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMinimum(Arr_) - 1 + start
        else:
            return -1
    if type_ == 0:
        Arr_ = Arr(0, 0.0)
        if CopyOpen(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMinimum(Arr_) - 1 + start
        else:
            return -1
    elif type_ == 3:
        Arr_ = Arr(0, 0.0)
        if CopyClose(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMinimum(Arr_) - 1 + start
        else:
            return -1
    elif type_ == 4:
        Arr_ = Arr(0, 0)
        if CopyTickVolume(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMinimum(Arr_) - 1 + start
        else:
            return -1
    elif type_ == 5:
        Arr_ = Arr(0, 0)
        if CopyRealVolume(symbol, ToTimeFrame(timeframe), start, count, Arr_) > 0:
            return count - ArrayMinimum(Arr_) - 1 + start
        else:
            return -1
    else:
        return -1

def iHigh_u(symbol, timeframe, shift):
    if shift < 0:
        return -1.0
    Arr_ = Arr(0, 0.0)
    if CopyHigh(symbol, ToTimeFrame(timeframe), shift, 1, Arr_) > 0:
        return Arr_[0]
    return -1.0

def iLow_u(symbol, timeframe, shift):
    if shift < 0:
        return -1.0
    Arr_ = Arr(0, 0.0)
    if CopyLow(symbol, ToTimeFrame(timeframe), shift, 1, Arr_) > 0:
        return Arr_[0]
    return -1.0

def iTime_u(symbol, timeframe, shift):
    if shift < 0:
        return -1
    Arr_ = Arr(0, 0)
    if CopyTime(symbol, ToTimeFrame(timeframe), shift, 1, Arr_) > 0:
        return Arr_[0]
    return -1

def High(bar=0):
    return iHigh_u(Symbol(), 0, bar)

def Low(bar=0):
    return iLow_u(Symbol(), 0, bar)

def Time(bar=0):
    return iTime_u(Symbol(), 0, bar)

def ToTimeFrame(timeframe):
    _sw1 = timeframe
    if _sw1 == 0:
        return PERIOD_CURRENT
    elif _sw1 == 1:
        return PERIOD_M1
    elif _sw1 == 5:
        return PERIOD_M5
    elif _sw1 == 15:
        return PERIOD_M15
    elif _sw1 == 30:
        return PERIOD_M30
    elif _sw1 == 60:
        return PERIOD_H1
    elif _sw1 == 240:
        return PERIOD_H4
    elif _sw1 == 1440:
        return PERIOD_D1
    elif _sw1 == 10080:
        return PERIOD_W1
    elif _sw1 == 43200:
        return PERIOD_MN1
    return PERIOD_CURRENT


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fibos(_MQL5Indicator):
    name = 'fibos'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'HighToLow': True,
        'Fibo_Level_1': 0.236,
        'Fibo_Level_2': 0.382,
        'Fibo_Level_3': 0.5,
        'Fibo_Level_4': 0.618,
        'Fibo_Level_5': 0.764,
        'Fibo_Level_6': 0.886,
        'StartBar': 0,
        'BarsBack': 20,
        'Pause': False,
    }

