"""Trendline Zigzag — converted from MQL5: MQL5 Indicators/Trendline zigzag in qualitative channel/Trendline Zigzag.mq5

Continuous trendlines from channel pivot to current extreme
Copyright: phade; Link: https://www.mql5.com; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'phade', 'link': 'https://www.mql5.com', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 1, 4: 1, 5: 1, 6: 6}, 'colors': {1: [11119017], 2: [11119017], 3: [5197615], 4: [12632256], 5: [12632256], 6: [13882323]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {}, 'labels': {1: 'Pivot Point A', 2: 'Pivot Point B', 3: 'Middle', 4: 'High Shifts', 5: 'Low Shifts', 6: 'Trendline Zigzag'}, 'levels': [], 'description': ['Continuous trendlines from channel pivot to current extreme'], 'name': 'Trendline Zigzag', 'source': 'MQL5 Indicators/Trendline zigzag in qualitative channel/Trendline Zigzag.mq5', 'folder': 'Trendline zigzag in qualitative channel', 'inputs': [{'mql': 'iPeriods', 'py': 'iPeriods', 'param': 'iPeriods', 'type': 'int', 'default': 50, 'label': 'Channel Period', 'sinput': False}, {'mql': 'zigzag_depth', 'py': 'zigzag_depth', 'param': 'zigzag_depth', 'type': 'int', 'default': 30, 'label': 'Depth', 'sinput': False}, {'mql': 'min_swing_distance', 'py': 'min_swing_distance', 'param': 'min_swing_distance', 'type': 'int', 'default': 5, 'label': 'Swing Deviation', 'sinput': False}, {'mql': 'drawing_trendline', 'py': 'drawing_trendline', 'param': 'drawing_trendline', 'type': 'bool', 'default': True, 'label': 'Draw trend line', 'sinput': False}, {'mql': 'pivot_correction', 'py': 'pivot_correction', 'param': 'pivot_correction', 'type': 'bool', 'default': True, 'label': 'Correct invalid pivots', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriods = _input('iPeriods', 50)  # Channel Period
zigzag_depth = _input('zigzag_depth', 30)  # Depth
min_swing_distance = _input('min_swing_distance', 5)  # Swing Deviation
drawing_trendline = _input('drawing_trendline', True)  # Draw trend line
pivot_correction = _input('pivot_correction', True)  # Correct invalid pivots
high_shifts = Arr(0, 0.0)
low_shifts = Arr(0, 0.0)
arr_buf_up = Arr(0, 0.0)
arr_buf_down = Arr(0, 0.0)
middle_band = Arr(0, 0.0)
mid_trend_up = Arr(0, 0.0)
mid_trend_down = Arr(0, 0.0)
ZigzagStart = Arr(0, 0.0)
ZigzagEnd = Arr(0, 0.0)
state = 0

def OnInit():
    SetIndexBuffer(0, arr_buf_up, INDICATOR_DATA)
    SetIndexBuffer(1, arr_buf_down, INDICATOR_DATA)
    SetIndexBuffer(2, middle_band, INDICATOR_DATA)
    SetIndexBuffer(3, high_shifts, INDICATOR_DATA)
    SetIndexBuffer(4, low_shifts, INDICATOR_DATA)
    SetIndexBuffer(5, ZigzagStart, INDICATOR_DATA)
    SetIndexBuffer(6, ZigzagEnd, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 33)
    PlotIndexSetInteger(1, PLOT_ARROW, 33)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, 10)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -10)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_cur_highest, _s_OnCalculate_cur_lowest, _s_OnCalculate_lastDownIndex, _s_OnCalculate_lastSwingHigh, _s_OnCalculate_lastSwingLow, _s_OnCalculate_lastUpIndex, state
    depth = zigzag_depth
    start = ((iPeriods + 1) if (prev_calculated == 0) else (prev_calculated - (depth + 1)))
    for i in range(start, rates_total):
        highest = high[ArrayMaximum(high, i - iPeriods + 1, iPeriods)]
        lowest = low[ArrayMinimum(low, i - iPeriods + 1, iPeriods)]
        high_shifts[i] = highest
        low_shifts[i] = lowest
        middle_band[i] = (highest + lowest) / 2.0
    for i in range(rates_total - 1, start - 1, -1):
        arr_buf_up[i] = EMPTY_VALUE
        arr_buf_down[i] = EMPTY_VALUE
        ZigzagStart[i] = EMPTY_VALUE
        ZigzagEnd[i] = EMPTY_VALUE
    upwardsDir = False
    downwardsDir = False
    leg_search = True
    for i in range(rates_total - 1 - (depth + 1), start - 1, -1):
        if state != 1:
            if low_shifts[i - 1] > low_shifts[i] and low_shifts[i] == low_shifts[i + depth + 1]:
                _s_OnCalculate_lastUpIndex = i
                currentLow = low[_s_OnCalculate_lastUpIndex]
                upwardsDir = True
                leg_search = False
                state = 1
                if _s_OnCalculate_lastSwingLow < 0 or _fdiv(fabs(currentLow - _s_OnCalculate_lastSwingLow), Point()) > min_swing_distance:
                    arr_buf_up[i] = low_shifts[_s_OnCalculate_lastUpIndex]
                    ZigzagStart[i] = currentLow
                    _s_OnCalculate_lastSwingLow = currentLow
                else:
                    if _s_OnCalculate_lastUpIndex >= 0:
                        for j in range(i, _s_OnCalculate_lastUpIndex, -1):
                            arr_buf_up[j] = EMPTY_VALUE
                            ZigzagStart[j] = EMPTY_VALUE
        else:
            leg_search = True
        if state != 2:
            if high_shifts[i - 1] < high_shifts[i] and high_shifts[i] == high_shifts[i + depth + 1]:
                _s_OnCalculate_lastDownIndex = i
                currentHigh = high[_s_OnCalculate_lastDownIndex]
                downwardsDir = True
                leg_search = False
                state = 2
                if _s_OnCalculate_lastSwingHigh < 0 or _fdiv(fabs(currentHigh - _s_OnCalculate_lastSwingHigh), Point()) > min_swing_distance:
                    arr_buf_down[i] = high_shifts[_s_OnCalculate_lastDownIndex]
                    ZigzagEnd[i] = currentHigh
                    _s_OnCalculate_lastSwingHigh = currentHigh
                else:
                    if _s_OnCalculate_lastDownIndex >= 0:
                        for j in range(i, _s_OnCalculate_lastDownIndex, -1):
                            arr_buf_down[j] = EMPTY_VALUE
                            ZigzagEnd[j] = EMPTY_VALUE
        else:
            leg_search = True
    if pivot_correction:
        for i in range(start, rates_total):
            if state == 1:
                if _s_OnCalculate_lastSwingLow >= 0 and low[i] < _s_OnCalculate_lastSwingLow:
                    if _s_OnCalculate_lastUpIndex >= 0:
                        for j in range(_s_OnCalculate_lastUpIndex, i):
                            arr_buf_up[j] = EMPTY_VALUE
                            ZigzagStart[j] = EMPTY_VALUE
                        state = 2
            if state == 2:
                if _s_OnCalculate_lastSwingHigh >= 0 and high[i] > _s_OnCalculate_lastSwingHigh:
                    if _s_OnCalculate_lastDownIndex >= 0:
                        for j in range(_s_OnCalculate_lastDownIndex, i):
                            arr_buf_down[j] = EMPTY_VALUE
                            ZigzagEnd[j] = EMPTY_VALUE
                        state = 1
    if drawing_trendline:
        for i in range(start, rates_total):
            _s_OnCalculate_cur_highest = high[ArrayMaximum(high, i - 10, 10)]
            _s_OnCalculate_cur_lowest = low[ArrayMinimum(low, i - 10, 10)]
            if leg_search:
                if state == 1 and (not downwardsDir):
                    ZigzagEnd[i] = _s_OnCalculate_cur_lowest
                    ZigzagEnd[i - 1] = EMPTY_VALUE
                    arr_buf_down[i - 1] = EMPTY_VALUE
                if state == 2 and (not upwardsDir):
                    ZigzagStart[i] = _s_OnCalculate_cur_highest
                    ZigzagStart[i - 1] = EMPTY_VALUE
                    arr_buf_up[i - 1] = EMPTY_VALUE
    return rates_total

def OnDeinit(reason):
    Comment('')

# ---- static local variables
_s_OnCalculate_lastUpIndex = -1
_s_OnCalculate_lastDownIndex = -1
_s_OnCalculate_lastSwingLow = -1.0
_s_OnCalculate_lastSwingHigh = -1.0
_s_OnCalculate_cur_highest = 0.0
_s_OnCalculate_cur_lowest = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendlineZigzag(_MQL5Indicator):
    name = 'Trendline Zigzag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'iPeriods': 50,  # Channel Period
        'zigzag_depth': 30,  # Depth
        'min_swing_distance': 5,  # Swing Deviation
        'drawing_trendline': True,  # Draw trend line
        'pivot_correction': True,  # Correct invalid pivots
    }

