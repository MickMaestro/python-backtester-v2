"""fractallevels — converted from MQL5: MQL5 Indicators/FractalLevels/fractallevels.mq5

Fractal Levels
Copyright: Copyright © 2008, lotos4u; Link: lotos4u@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, lotos4u', 'link': 'lotos4u@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [65280], 2: [255], 3: [16711680], 4: [16711935], 5: [65280], 6: [255]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4, 5: 4, 6: 4}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fractal resistance', 2: 'DOWNWARD fractal', 3: 'UPWARD fractal', 5: 'UPWARD breakout', 6: 'Пробой ВНИЗ'}, 'levels': [], 'description': ['Fractal Levels'], 'name': 'fractallevels', 'source': 'MQL5 Indicators/FractalLevels/fractallevels.mq5', 'folder': 'FractalLevels', 'inputs': [{'mql': 'LeftBars_', 'py': 'LeftBars_', 'param': 'LeftBars_', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'RightBars_', 'py': 'RightBars_', 'param': 'RightBars_', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LeftBars_ = _input('LeftBars_', 3)
RightBars_ = _input('RightBars_', 3)
LineUpBuffer = Arr(0, 0.0)
LineDownBuffer = Arr(0, 0.0)
ArrowUpBuffer = Arr(0, 0.0)
ArrowDownBuffer = Arr(0, 0.0)
ArrowBreakUpBuffer = Arr(0, 0.0)
ArrowBreakDownBuffer = Arr(0, 0.0)
min_rates_total = 0
LeftBars = 0
RightBars = 0

def OnInit():
    global LeftBars, RightBars, min_rates_total
    LeftBars = LeftBars_
    RightBars = RightBars_
    if LeftBars < 2:
        LeftBars = 2
    if RightBars < 2:
        RightBars = 2
    min_rates_total = _int(LeftBars + RightBars + 1)
    SetIndexBuffer(0, LineUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(LineUpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, LineDownBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(LineDownBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, ArrowUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 119)
    ArraySetAsSeries(ArrowUpBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, ArrowDownBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 119)
    ArraySetAsSeries(ArrowDownBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(4, ArrowBreakUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 108)
    ArraySetAsSeries(ArrowBreakUpBuffer, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(5, ArrowBreakDownBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_ARROW, 108)
    ArraySetAsSeries(ArrowBreakDownBuffer, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Fractal Levels'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def isFractalUp(index, lBars, rBars, High):
    start = index - rBars
    end = index + lBars + 1
    max_ = High[index]
    for i in range(start, end):
        if max_ < High[i] and i != index:
            if max_ < High[i]:
                return 0.0
            if MathAbs(i - index) > 1:
                return 0.0
    return max_

def isFractalDown(index, lBars, rBars, Low):
    start = index - rBars
    end = index + lBars + 1
    min_ = Low[index]
    for i in range(start, end):
        if min_ > Low[i] and i != index:
            if min_ > Low[i]:
                return 0.0
            if MathAbs(i - index) > 1:
                return 0.0
    return min_

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ArrowUpBuffer[bar] = 0.0
        ArrowDownBuffer[bar] = 0.0
        ArrowBreakUpBuffer[bar] = 0.0
        ArrowBreakDownBuffer[bar] = 0.0
        if bar < _int(RightBars):
            LineUpBuffer[bar] = LineUpBuffer[bar + 1]
            LineDownBuffer[bar] = LineDownBuffer[bar + 1]
            continue
        LineUpBuffer[bar] = isFractalUp(bar, LeftBars, RightBars, high)
        if not LineUpBuffer[bar]:
            LineUpBuffer[bar] = LineUpBuffer[bar + 1]
        else:
            ArrowUpBuffer[bar] = LineUpBuffer[bar]
        LineDownBuffer[bar] = isFractalDown(bar, LeftBars, RightBars, low)
        if not LineDownBuffer[bar]:
            LineDownBuffer[bar] = LineDownBuffer[bar + 1]
        else:
            ArrowDownBuffer[bar] = LineDownBuffer[bar]
        if close[bar] > LineUpBuffer[bar] and close[bar + 1] <= LineUpBuffer[bar + 1]:
            ArrowBreakUpBuffer[bar] = close[bar]
        if close[bar] < LineDownBuffer[bar] and close[bar + 1] >= LineDownBuffer[bar + 1]:
            ArrowBreakDownBuffer[bar] = close[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fractallevels(_MQL5Indicator):
    name = 'fractallevels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'LeftBars_': 3,
        'RightBars_': 3,
    }

