"""simplezzcolorretracement — converted from MQL5: MQL5 Indicators/ZZ Color Retracement/simplezzcolorretracement.mq5

Copyright: Copyright 2016, Oschenker; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, Oschenker', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 9}, 'colors': {1: [16711680, 8421504, 255]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'MyZigZag'}, 'levels': [], 'description': [], 'name': 'simplezzcolorretracement', 'source': 'MQL5 Indicators/ZZ Color Retracement/simplezzcolorretracement.mq5', 'folder': 'ZZ Color Retracement', 'inputs': [{'mql': 'Retracement', 'py': 'Retracement', 'param': 'Retracement', 'type': 'int', 'default': 10, 'label': 'Typical retracement size', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 20, 'label': 'Moves averaging period', 'sinput': False}, {'mql': 'Bound', 'py': 'Bound', 'param': 'Bound', 'type': 'int', 'default': 61, 'label': 'Moves percentage difference', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Retracement = _input('Retracement', 10)  # Typical retracement size
MAPeriod = _input('MAPeriod', 20)  # Moves averaging period
Bound = _input('Bound', 61)  # Moves percentage difference
Goal = 0
LastPoint = 0
ZZPoints = Arr(0, 0.0)
ZZColor = Arr(0, 0.0)
LMoves = Arr(0, 0.0)
Scale = 0.0  # Typical retracement size
LLow = 0.0  # Last Low
LHigh = 0.0  # Last High
PLow = 0.0  # Prior Low
PHigh = 0.0  # Prior High
LMove = 0.0  # Last Move
SumMove = 0.0  # sum of N last moves (N = MAPeriod)
MAMoves = 0.0  # moving average of N last moves (N = MAPeriod)
DoubleBound = 0.0
com = ""

def OnInit():
    global DoubleBound, Scale
    SetIndexBuffer(0, ZZPoints, INDICATOR_DATA)
    SetIndexBuffer(1, ZZColor, INDICATOR_COLOR_INDEX)
    PlotIndexSetString(0, PLOT_LABEL, 'Color Trend ZigZag(' + _str(Scale) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    Scale = Retracement * Point()
    DoubleBound = Bound * 0.01
    return INIT_SUCCEEDED

def OnDeinit(reason):
    global Scale
    ObjectsDeleteAll(0, 'Level_', 0, OBJ_TREND)
    ChartSetString(0, CHART_COMMENT, '')
    Scale = 0.0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Goal, LHigh, LLow, LMove, LastPoint, MAMoves, PHigh, PLow, SumMove
    Start = 0
    MAIndex = 0
    if rates_total < 3:
        return 0
    ArrayResize(LMoves, MAPeriod, 0)
    if prev_calculated == 0:
        ArrayInitialize(ZZPoints, EMPTY_VALUE)
        ArrayInitialize(ZZColor, EMPTY_VALUE)
        ArrayInitialize(LMoves, 0.0)
        Start = 1
        if low[0] < high[1]:
            LLow = low[0]
            PLow = LLow
            LHigh = high[1]
            PHigh = LHigh
            Goal = 2
        else:
            LHigh = high[0]
            PHigh = LHigh
            LLow = low[1]
            PLow = LLow
            Goal = 1
        MAMoves = LHigh - LLow
        LMoves[0] = MAMoves
        LMoves[1] = 0.0
    else:
        Start = prev_calculated - 1
    for bar in range(Start, rates_total - 1):
        _sw1 = Goal
        if _sw1 == 1:
            if low[bar] <= LLow:
                LLow = low[bar]
                ZZPoints[LastPoint] = EMPTY_VALUE
                ZZColor[LastPoint] = EMPTY_VALUE
                LastPoint = bar
                ZZPoints[LastPoint] = LLow
                ZZColor[LastPoint] = ColorCheck(_fdiv(LHigh - LLow, MAMoves), DoubleBound)
                pass  # break
            if high[bar] > (LLow + Scale):
                MAIndex += 1
                if MAIndex == MAPeriod:
                    MAIndex = 0
                LMove = LHigh - LLow
                SumMove = SumMove + LMove - LMoves[MAIndex]
                LMoves[MAIndex] = LMove
                MAMoves = SumMove / MAPeriod
                PHigh = LHigh
                LHigh = high[bar]
                LastPoint = bar
                ZZPoints[LastPoint] = LHigh
                ZZColor[LastPoint] = ColorCheck(_fdiv(LHigh - LLow, MAMoves), DoubleBound)
                Goal = 2
        elif _sw1 == 2:
            if high[bar] >= LHigh:
                LHigh = high[bar]
                ZZPoints[LastPoint] = EMPTY_VALUE
                ZZColor[LastPoint] = EMPTY_VALUE
                LastPoint = bar
                ZZPoints[LastPoint] = LHigh
                ZZColor[LastPoint] = ColorCheck(_fdiv(LHigh - LLow, MAMoves), DoubleBound)
                pass  # break
            if low[bar] < (LHigh - Scale):
                MAIndex += 1
                if MAIndex == MAPeriod:
                    MAIndex = 0
                LMove = LHigh - LLow
                SumMove = SumMove + LMove - LMoves[MAIndex]
                LMoves[MAIndex] = LMove
                MAMoves = SumMove / MAPeriod
                PLow = LLow
                LLow = low[bar]
                LastPoint = bar
                ZZPoints[LastPoint] = LLow
                ZZColor[LastPoint] = ColorCheck(_fdiv(LHigh - LLow, MAMoves), DoubleBound)
                Goal = 1
    return rates_total

def ColorCheck(p_ratio, p_bound):
    color_check = 0
    if p_ratio > (1 + p_bound):
        color_check = 0
    else:
        if p_ratio < (1 - p_bound):
            color_check = 2
        else:
            color_check = 1
    return color_check


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Simplezzcolorretracement(_MQL5Indicator):
    name = 'simplezzcolorretracement'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Retracement': 10,  # Typical retracement size
        'MAPeriod': 20,  # Moves averaging period
        'Bound': 61,  # Moves percentage difference
    }

