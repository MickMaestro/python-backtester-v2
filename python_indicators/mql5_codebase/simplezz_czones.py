"""simplezz_czones — converted from MQL5: MQL5 Indicators/Simple ZZ Consolidation Zones/simplezz_czones.mq5

Copyright: Copyright 2016, (C) Oschenker; Link: https://www.mql5.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, (C) Oschenker', 'link': 'https://www.mql5.com', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'MyZigZag'}, 'levels': [], 'description': [], 'name': 'simplezz_czones', 'source': 'MQL5 Indicators/Simple ZZ Consolidation Zones/simplezz_czones.mq5', 'folder': 'Simple ZZ Consolidation Zones', 'inputs': [{'mql': 'TotalPoints', 'py': 'TotalPoints', 'param': 'TotalPoints', 'type': 'int', 'default': 15, 'label': 'Number of ZZ points analyzed', 'sinput': False}, {'mql': 'TouchNum', 'py': 'TouchNum', 'param': 'TouchNum', 'type': 'int', 'default': 3, 'label': 'Number of times the price touches the level', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'int', 'default': 10, 'label': 'High/low max. deviation around level', 'sinput': False}, {'mql': 'Retracement', 'py': 'Retracement', 'param': 'Retracement', 'type': 'int', 'default': 10, 'label': 'Typical retracement size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TotalPoints = _input('TotalPoints', 15)  # Number of ZZ points analyzed
TouchNum = _input('TouchNum', 3)  # Number of times the price touches the level
Deviation = _input('Deviation', 10)  # High/low max. deviation around level
Retracement = _input('Retracement', 10)  # Typical retracement size
Goal = 0
LastExtrBar = 0
ZZPoints = Arr(0, 0.0)
Scale = 0.0
LLow = 0.0
LHigh = 0.0
PLow = 0.0
PHigh = 0.0
Level = 0.0
com = ""

def OnInit():
    global Scale
    SetIndexBuffer(0, ZZPoints, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'SiZZ ConZones(' + _str(Scale) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    Scale = Retracement * Point()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    global Scale
    ObjectsDeleteAll(0, 'Level_', 0, OBJ_RECTANGLE)
    ChartSetString(0, CHART_COMMENT, '')
    Scale = 0.0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Goal, LHigh, LLow, LastExtrBar, Level, PHigh, PLow
    Start = 0
    if rates_total < 3:
        return 0
    if prev_calculated == 0:
        ArrayInitialize(ZZPoints, 0.0)
        Start = 2
        if low[0] < high[1]:
            LLow = low[0]
            PLow = LLow
            LHigh = high[1]
            PHigh = LHigh
            Goal = 1
        else:
            LHigh = high[0]
            PHigh = LHigh
            LLow = low[1]
            PLow = LLow
            Goal = 2
    else:
        Start = prev_calculated - 1
    for bar in range(Start, rates_total - 1):
        _sw1 = Goal
        if _sw1 == 1:
            if low[bar] <= LLow:
                LLow = low[bar]
                ZZPoints[LastExtrBar] = 0.0
                LastExtrBar = bar
                ZZPoints[LastExtrBar] = LLow
                pass  # break
            if high[bar] > (LLow + Scale):
                PHigh = LHigh
                LHigh = high[bar]
                Level = CZone(Goal, TotalPoints, TouchNum, LastExtrBar, Deviation, time)
                LastExtrBar = bar
                ZZPoints[LastExtrBar] = LHigh
                Goal = 2
        elif _sw1 == 2:
            if high[bar] >= LHigh:
                LHigh = high[bar]
                ZZPoints[LastExtrBar] = 0.0
                LastExtrBar = bar
                ZZPoints[LastExtrBar] = LHigh
                pass  # break
            if low[bar] < (LHigh - Scale):
                PLow = LLow
                LLow = low[bar]
                Level = CZone(Goal, TotalPoints, TouchNum, LastExtrBar, Deviation, time)
                LastExtrBar = bar
                ZZPoints[LastExtrBar] = LLow
                Goal = 1
    return rates_total

def CZone(par_Goal, par_TotalPoints, par_TouchNum, par_LastExtrBar, par_Deviation, time):
    points = 0
    touch_num = 0
    touch_bar = 0
    shift = 1
    high_low = 0
    level = 0.0
    width = Point() * par_Deviation
    level_color = 0
    while points <= par_TotalPoints and shift <= par_LastExtrBar:
        if ZZPoints[par_LastExtrBar - shift] != 0:
            _sw2 = high_low
            if _sw2 == 0:
                if fabs(ZZPoints[par_LastExtrBar] - ZZPoints[par_LastExtrBar - shift]) > width:
                    width = ZZPoints[par_LastExtrBar - shift]
                high_low = 1
            elif _sw2 == 1:
                if fabs(ZZPoints[par_LastExtrBar] - ZZPoints[par_LastExtrBar - shift]) < (Point() * par_Deviation):
                    touch_num += 1
                    touch_bar = par_LastExtrBar - shift
                    high_low = 0
            points += 1
        shift += 1
    level_color = clrGray
    if touch_num >= par_TouchNum:
        level = ZZPoints[LastExtrBar]
        if ObjectCreate(0, 'Level_' + IntegerToString(par_LastExtrBar, 4, 48), OBJ_RECTANGLE, 0, time[touch_bar], width, time[par_LastExtrBar], level):
            _sw3 = par_Goal
            if _sw3 == 1:
                level_color = clrBlue
            elif _sw3 == 2:
                level_color = clrRed
            ObjectSetInteger(0, 'Level_' + IntegerToString(par_LastExtrBar, 4, 48), OBJPROP_COLOR, level_color)
            ObjectSetInteger(0, 'Level_' + IntegerToString(par_LastExtrBar, 4, 48), OBJPROP_WIDTH, 3)
    return level


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimplezzCzones(_MQL5Indicator):
    name = 'simplezz_czones'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TotalPoints': 15,  # Number of ZZ points analyzed
        'TouchNum': 3,  # Number of times the price touches the level
        'Deviation': 10,  # High/low max. deviation around level
        'Retracement': 10,  # Typical retracement size
    }

