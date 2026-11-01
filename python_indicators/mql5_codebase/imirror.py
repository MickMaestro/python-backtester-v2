"""imirror — converted from MQL5: MQL5 Indicators/iMirror/imirror.mq5

Copyright: 2014, Timur Gatin; Link: https://login.mql5.com/ru/users/gt788; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2014, Timur Gatin', 'link': 'https://login.mql5.com/ru/users/gt788', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [3329330, 255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'iMirror'}, 'levels': [], 'description': [], 'name': 'imirror', 'source': 'MQL5 Indicators/iMirror/imirror.mq5', 'folder': 'iMirror', 'inputs': [{'mql': 'Up', 'py': 'Up', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'The color of the bullish candlestick', 'sinput': False}, {'mql': 'Down', 'py': 'Down', 'param': None, 'type': 'color', 'default': 255, 'label': 'The color of the bearish candlestick', 'sinput': False}, {'mql': 'Back', 'py': 'Back', 'param': None, 'type': 'color', 'default': 7346457, 'label': 'background color', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Up = _input('Up', clrLimeGreen)  # The color of the bullish candlestick
Down = _input('Down', clrRed)  # The color of the bearish candlestick
Back = _input('Back', clrMidnightBlue)  # background color
open = Arr(0, 0.0)
high = Arr(0, 0.0)
low = Arr(0, 0.0)
close = Arr(0, 0.0)
colors = Arr(0, 0.0)
chart = Arr(6, 0, dyn=False)  # an array for storing chart parameters

def OnInit():
    SetIndexBuffer(0, open, INDICATOR_DATA)
    SetIndexBuffer(1, high, INDICATOR_DATA)
    SetIndexBuffer(2, low, INDICATOR_DATA)
    SetIndexBuffer(3, close, INDICATOR_DATA)
    SetIndexBuffer(4, colors, INDICATOR_COLOR_INDEX)
    ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, 1)
    chart[0] = ChartGetInteger(0, CHART_FOREGROUND)
    chart[1] = ChartGetInteger(0, CHART_COLOR_CHART_UP)
    chart[2] = ChartGetInteger(0, CHART_COLOR_CHART_DOWN)
    chart[3] = ChartGetInteger(0, CHART_COLOR_CHART_LINE)
    chart[4] = ChartGetInteger(0, CHART_COLOR_CANDLE_BULL)
    chart[5] = ChartGetInteger(0, CHART_COLOR_CANDLE_BEAR)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, 0)
    ChartSetInteger(0, CHART_FOREGROUND, chart[0])
    ChartSetInteger(0, CHART_COLOR_CHART_UP, chart[1])
    ChartSetInteger(0, CHART_COLOR_CHART_DOWN, chart[2])
    ChartSetInteger(0, CHART_COLOR_CHART_LINE, chart[3])
    ChartSetInteger(0, CHART_COLOR_CANDLE_BULL, chart[4])
    ChartSetInteger(0, CHART_COLOR_CANDLE_BEAR, chart[5])
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, begin, price):
    EventChartCustom(0, 1387, 0, 0, None)
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global _s_OnChartEvent_click_flag, _s_OnChartEvent_flag, _s_OnChartEvent_minimax, _s_OnChartEvent_sdelay, _s_OnChartEvent_sleft, _s_OnChartEvent_sright
    if ((id_ != CHARTEVENT_CHART_CHANGE and id_ != (CHARTEVENT_CUSTOM + 1387)) and id_ != CHARTEVENT_CLICK) and id_ != CHARTEVENT_MOUSE_MOVE:
        return
    if id_ == CHARTEVENT_MOUSE_MOVE and (_s_OnChartEvent_click_flag or (GetTickCount() - _s_OnChartEvent_sdelay) < 50):
        return
    first = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR)) + 1
    window = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
    bars = Bars(Symbol(), Period())
    left = bars - first
    right = left + window
    if right > bars:
        return
    if (left != _s_OnChartEvent_sleft or right != _s_OnChartEvent_sright) or right == bars:
        start = first - window
        lleft = left
        if left == _s_OnChartEvent_sleft and right == _s_OnChartEvent_sright:
            window = 1
            lleft = right - 1
        if CopyHigh(Symbol(), Period(), start, window, _s_OnChartEvent_H) != window:
            return
        if CopyLow(Symbol(), Period(), start, window, _s_OnChartEvent_L) != window:
            return
        if CopyClose(Symbol(), Period(), start, window, _s_OnChartEvent_C) != window:
            return
        _s_OnChartEvent_sright = right
        _s_OnChartEvent_sleft = left
        if window > 1:
            if CopyOpen(Symbol(), Period(), start, window, _s_OnChartEvent_O) != window:
                return
            if CopyTime(Symbol(), Period(), start, window, _s_OnChartEvent_T) != window:
                return
            max_ = _s_OnChartEvent_H[ArrayMaximum(_s_OnChartEvent_H)]
            min_ = _s_OnChartEvent_L[ArrayMinimum(_s_OnChartEvent_L)]
            _s_OnChartEvent_minimax = max_ + min_
        for i in range(lleft, right):
            if window > 1:
                open[i] = _s_OnChartEvent_minimax - _s_OnChartEvent_O[i - lleft]
            high[i] = _s_OnChartEvent_minimax - _s_OnChartEvent_L[i - lleft]
            low[i] = _s_OnChartEvent_minimax - _s_OnChartEvent_H[i - lleft]
            close[i] = _s_OnChartEvent_minimax - _s_OnChartEvent_C[i - lleft]
            if open[i] < close[i]:
                colors[i] = 0.0
            else:
                colors[i] = 1.0
    if id_ == CHARTEVENT_MOUSE_MOVE or id_ == CHARTEVENT_CLICK:
        _s_OnChartEvent_sdelay = GetTickCount()
        x = _int(lparam)
        y = _int(dparam)
        sub = Box(0)
        p = Box(0.0)
        t = Box(0)
        dt = PeriodSeconds()
        ChartXYToTimePrice(0, x, y, sub, t, p)
        color_flag = False
        for i in range(left, right):
            if ((t.v > (_s_OnChartEvent_T[i - left] - dt) and t.v < (_s_OnChartEvent_T[i - left] + dt)) and p.v < high[i]) and p.v > low[i]:
                color_flag = True
                break
        if color_flag and id_ == CHARTEVENT_CLICK:
            if _s_OnChartEvent_click_flag:
                _s_OnChartEvent_click_flag = False
            else:
                _s_OnChartEvent_click_flag = True
        if (color_flag or _s_OnChartEvent_click_flag) and (not _s_OnChartEvent_flag):
            _s_OnChartEvent_flag = True
            PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, Up)
            PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Down)
            ChartSetInteger(0, CHART_FOREGROUND, 0)
            ChartSetInteger(0, CHART_COLOR_CHART_UP, Back)
            ChartSetInteger(0, CHART_COLOR_CHART_DOWN, Back)
            ChartSetInteger(0, CHART_COLOR_CHART_LINE, Back)
            ChartSetInteger(0, CHART_COLOR_CANDLE_BULL, Back)
            ChartSetInteger(0, CHART_COLOR_CANDLE_BEAR, Back)
        if ((not color_flag) and (not _s_OnChartEvent_click_flag)) and _s_OnChartEvent_flag:
            _s_OnChartEvent_flag = False
            PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, Back)
            PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Back)
            ChartSetInteger(0, CHART_FOREGROUND, 1)
            ChartSetInteger(0, CHART_COLOR_CHART_UP, Up)
            ChartSetInteger(0, CHART_COLOR_CHART_DOWN, Down)
            ChartSetInteger(0, CHART_COLOR_CHART_LINE, Up)
            ChartSetInteger(0, CHART_COLOR_CANDLE_BULL, Up)
            ChartSetInteger(0, CHART_COLOR_CANDLE_BEAR, Down)
    ChartRedraw()

# ---- static local variables
_s_OnChartEvent_click_flag = False
_s_OnChartEvent_sdelay = 0
_s_OnChartEvent_O = Arr(0, 0.0)
_s_OnChartEvent_H = Arr(0, 0.0)
_s_OnChartEvent_L = Arr(0, 0.0)
_s_OnChartEvent_C = Arr(0, 0.0)
_s_OnChartEvent_T = Arr(0, 0)
_s_OnChartEvent_sleft = 0
_s_OnChartEvent_sright = 0
_s_OnChartEvent_minimax = 0.0
_s_OnChartEvent_flag = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Imirror(_MQL5Indicator):
    name = 'imirror'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

