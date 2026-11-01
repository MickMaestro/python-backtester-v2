"""Candlestick_Patterns_v2 — converted from MQL5: MQL5 Indicators/Candlestick patterns/Candlestick_Patterns_v2.mq5

Candlestick Patterns
Copyright: Copyright 2024-2025, globus2008

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024-2025, globus2008', 'window': 'chart', 'indicator_buffers': 20, 'indicator_plots': 20}, 'types': {1: 5, 2: 5, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}, 'colors': {1: [14772545], 2: [9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Bullish_patterns', 2: 'Bearish_patterns', 3: 'Value_bullish', 4: 'Value_bearish', 5: 'be_three_black_cows', 6: 'bu_three_white_soldiers', 7: 'bu_bullish_kicker', 8: 'be_bearish_kicker', 9: 'bu_bullish_engulfing', 10: 'be_bearish_engulfing', 11: 'bu_bullish_harami', 12: 'be_bearish_harami', 13: 'bu_three_line_strike', 14: 'be_three_line_strike', 15: 'bu_three_inside_up', 16: 'be_three_inside_down', 17: 'bu_three_outside_up', 18: 'be_three_outside_down', 19: 'bu_tweezer_bottom', 20: 'be_tweezer_top'}, 'levels': [], 'description': ['Candlestick Patterns'], 'name': 'Candlestick_Patterns_v2', 'source': 'MQL5 Indicators/Candlestick patterns/Candlestick_Patterns_v2.mq5', 'folder': 'Candlestick patterns', 'inputs': [{'mql': 'Minimal_Value', 'py': 'Minimal_Value', 'param': 'Minimal_Value', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'imp_3C_three_white_soldiers_black_cows', 'py': 'imp_3C_three_white_soldiers_black_cows', 'param': 'imp_3C_three_white_soldiers_black_cows', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'imp_2C_bullish_bearish_kicker', 'py': 'imp_2C_bullish_bearish_kicker', 'param': 'imp_2C_bullish_bearish_kicker', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'imp_2C_bullish_bearish_engulfing', 'py': 'imp_2C_bullish_bearish_engulfing', 'param': 'imp_2C_bullish_bearish_engulfing', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'imp_2C_bullish_bearish_harami', 'py': 'imp_2C_bullish_bearish_harami', 'param': 'imp_2C_bullish_bearish_harami', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'imp_4C_three_line_strike', 'py': 'imp_4C_three_line_strike', 'param': 'imp_4C_three_line_strike', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'imp_3C_three_inside', 'py': 'imp_3C_three_inside', 'param': 'imp_3C_three_inside', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'imp_3C_three_outside', 'py': 'imp_3C_three_outside', 'param': 'imp_3C_three_outside', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'imp_2C_tweezer', 'py': 'imp_2C_tweezer', 'param': 'imp_2C_tweezer', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PATTERN_IMPORTANCE
NONE = 0
LOW = 1
MODERATE = 2
HIGH = 3
_enum('ENUM_PATTERN_IMPORTANCE', {0: 'NONE', 1: 'LOW', 2: 'MODERATE', 3: 'HIGH'})

# ---- inputs and global variables
bullish_patterns = Arr(0, 0.0)
bearish_patterns = Arr(0, 0.0)
Value_bullish = Arr(0, 0.0)
Value_bearish = Arr(0, 0.0)
be_three_black_cows = Arr(0, 0.0)
bu_three_white_soldiers = Arr(0, 0.0)
bu_bullish_kicker = Arr(0, 0.0)
be_bearish_kicker = Arr(0, 0.0)
bu_bullish_engulfing = Arr(0, 0.0)
be_bearish_engulfing = Arr(0, 0.0)
bu_bullish_harami = Arr(0, 0.0)
be_bearish_harami = Arr(0, 0.0)
bu_three_line_strike = Arr(0, 0.0)
be_three_line_strike = Arr(0, 0.0)
bu_three_inside_up = Arr(0, 0.0)
be_three_inside_down = Arr(0, 0.0)
bu_three_outside_up = Arr(0, 0.0)
be_three_outside_down = Arr(0, 0.0)
bu_tweezer_bottom = Arr(0, 0.0)
be_tweezer_top = Arr(0, 0.0)
Minimal_Value = _input('Minimal_Value', 2)
imp_3C_three_white_soldiers_black_cows = _input('imp_3C_three_white_soldiers_black_cows', MODERATE)
imp_2C_bullish_bearish_kicker = _input('imp_2C_bullish_bearish_kicker', MODERATE)
imp_2C_bullish_bearish_engulfing = _input('imp_2C_bullish_bearish_engulfing', MODERATE)
imp_2C_bullish_bearish_harami = _input('imp_2C_bullish_bearish_harami', MODERATE)
imp_4C_three_line_strike = _input('imp_4C_three_line_strike', HIGH)
imp_3C_three_inside = _input('imp_3C_three_inside', MODERATE)
imp_3C_three_outside = _input('imp_3C_three_outside', MODERATE)
imp_2C_tweezer = _input('imp_2C_tweezer', MODERATE)

def OnInit():
    SetIndexBuffer(0, bullish_patterns, INDICATOR_DATA)
    SetIndexBuffer(1, bearish_patterns, INDICATOR_DATA)
    SetIndexBuffer(2, Value_bullish, INDICATOR_DATA)
    SetIndexBuffer(3, Value_bearish, INDICATOR_DATA)
    SetIndexBuffer(4, be_three_black_cows, INDICATOR_DATA)
    SetIndexBuffer(5, bu_three_white_soldiers, INDICATOR_DATA)
    SetIndexBuffer(6, bu_bullish_kicker, INDICATOR_DATA)
    SetIndexBuffer(7, be_bearish_kicker, INDICATOR_DATA)
    SetIndexBuffer(8, bu_bullish_engulfing, INDICATOR_DATA)
    SetIndexBuffer(9, be_bearish_engulfing, INDICATOR_DATA)
    SetIndexBuffer(10, bu_bullish_harami, INDICATOR_DATA)
    SetIndexBuffer(11, be_bearish_harami, INDICATOR_DATA)
    SetIndexBuffer(12, bu_three_line_strike, INDICATOR_DATA)
    SetIndexBuffer(13, be_three_line_strike, INDICATOR_DATA)
    SetIndexBuffer(14, bu_three_inside_up, INDICATOR_DATA)
    SetIndexBuffer(15, be_three_inside_down, INDICATOR_DATA)
    SetIndexBuffer(16, bu_three_outside_up, INDICATOR_DATA)
    SetIndexBuffer(17, be_three_outside_down, INDICATOR_DATA)
    SetIndexBuffer(18, bu_tweezer_bottom, INDICATOR_DATA)
    SetIndexBuffer(19, be_tweezer_top, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_ARROW, 161)
    PlotIndexSetInteger(1, PLOT_ARROW, 164)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Candlestick Patterns')
    PlotIndexSetString(0, PLOT_LABEL, 'Bullish_patterns')
    PlotIndexSetString(1, PLOT_LABEL, 'Bearish_patterns')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(9, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(10, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(11, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(12, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(13, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(14, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(15, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(16, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(17, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(18, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(19, PLOT_EMPTY_VALUE, 0.0)

def OnDeinit(reason):
    ArrayFree(bullish_patterns)
    ArrayFree(bearish_patterns)
    ArrayFree(Value_bullish)
    ArrayFree(Value_bearish)
    ArrayFree(be_three_black_cows)
    ArrayFree(bu_three_white_soldiers)
    ArrayFree(bu_bullish_kicker)
    ArrayFree(be_bearish_kicker)
    ArrayFree(bu_bullish_engulfing)
    ArrayFree(be_bearish_engulfing)
    ArrayFree(bu_bullish_harami)
    ArrayFree(be_bearish_harami)
    ArrayFree(bu_three_line_strike)
    ArrayFree(be_three_line_strike)
    ArrayFree(bu_three_inside_up)
    ArrayFree(be_three_inside_down)
    ArrayFree(bu_three_outside_up)
    ArrayFree(be_three_outside_down)
    ArrayFree(bu_tweezer_bottom)
    ArrayFree(be_tweezer_top)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 100:
        return 0
    start = 1
    if prev_calculated > 0:
        start = prev_calculated - 1
    start = MathMax(10, start)
    for i in range(start, rates_total):
        Value_bullish[i] = 0.0
        Value_bearish[i] = 0.0
        bullish_patterns[i] = 0.0
        bearish_patterns[i] = 0.0
        be_three_black_cows[i] = 0.0
        bu_three_white_soldiers[i] = 0.0
        bu_bullish_kicker[i] = 0.0
        be_bearish_kicker[i] = 0.0
        bu_bullish_engulfing[i] = 0.0
        be_bearish_engulfing[i] = 0.0
        bu_bullish_harami[i] = 0.0
        be_bearish_harami[i] = 0.0
        bu_three_line_strike[i] = 0.0
        be_three_line_strike[i] = 0.0
        bu_three_inside_up[i] = 0.0
        be_three_inside_down[i] = 0.0
        bu_three_outside_up[i] = 0.0
        be_three_outside_down[i] = 0.0
        bu_tweezer_bottom[i] = 0.0
        be_tweezer_top[i] = 0.0
        cal_be_three_black_cows(open, high, low, close, time, i)
        cal_bu_three_white_soldiers(open, high, low, close, time, i)
        cal_bu_bullish_kicker(open, high, low, close, time, i)
        cal_be_bearish_kicker(open, high, low, close, time, i)
        cal_bu_bullish_engulfing(open, high, low, close, time, i)
        cal_be_bearish_engulfing(open, high, low, close, time, i)
        cal_bu_bullish_harami(open, high, low, close, time, i)
        cal_be_bearish_harami(open, high, low, close, time, i)
        cal_bu_three_line_strike(open, high, low, close, time, i)
        cal_be_three_line_strike(open, high, low, close, time, i)
        cal_bu_three_inside_up(open, high, low, close, time, i)
        cal_be_three_inside_down(open, high, low, close, time, i)
        cal_bu_three_outside_up(open, high, low, close, time, i)
        cal_be_three_outside_down(open, high, low, close, time, i)
        cal_bu_tweezer_bottom(open, high, low, close, time, i)
        cal_be_tweezer_top(open, high, low, close, time, i)
        if i < 10:
            continue
        if be_three_black_cows[i] > 0:
            if imp_3C_three_white_soldiers_black_cows != NONE:
                bearish_patterns[i] = be_three_black_cows[i]
            Value_bearish[i] += importance_value(imp_3C_three_white_soldiers_black_cows)
        if bu_three_white_soldiers[i] > 0:
            if imp_3C_three_white_soldiers_black_cows != NONE:
                bullish_patterns[i] = bu_three_white_soldiers[i]
            Value_bullish[i] += importance_value(imp_3C_three_white_soldiers_black_cows)
        if bu_bullish_kicker[i] > 0:
            if imp_2C_bullish_bearish_kicker != NONE:
                bullish_patterns[i] = bu_bullish_kicker[i]
            Value_bullish[i] += importance_value(imp_2C_bullish_bearish_kicker)
        if be_bearish_kicker[i] > 0:
            if imp_2C_bullish_bearish_kicker != NONE:
                bearish_patterns[i] = be_bearish_kicker[i]
            Value_bearish[i] += importance_value(imp_2C_bullish_bearish_kicker)
        if bu_bullish_engulfing[i] > 0:
            if imp_2C_bullish_bearish_engulfing != NONE:
                bullish_patterns[i] = bu_bullish_engulfing[i]
            Value_bullish[i] += importance_value(imp_2C_bullish_bearish_engulfing)
        if be_bearish_engulfing[i] > 0:
            if imp_2C_bullish_bearish_engulfing != NONE:
                bearish_patterns[i] = be_bearish_engulfing[i]
            Value_bearish[i] += importance_value(imp_2C_bullish_bearish_engulfing)
        if bu_bullish_harami[i] > 0:
            if imp_2C_bullish_bearish_engulfing != NONE:
                bullish_patterns[i] = bu_bullish_harami[i]
            Value_bullish[i] += importance_value(imp_2C_bullish_bearish_harami)
        if be_bearish_harami[i] > 0:
            if imp_2C_bullish_bearish_engulfing != NONE:
                bearish_patterns[i] = be_bearish_harami[i]
            Value_bearish[i] += importance_value(imp_2C_bullish_bearish_harami)
        if bu_three_line_strike[i] > 0:
            if imp_4C_three_line_strike != NONE:
                bullish_patterns[i] = bu_three_line_strike[i]
            Value_bullish[i] += importance_value(imp_4C_three_line_strike)
        if be_three_line_strike[i] > 0:
            if imp_4C_three_line_strike != NONE:
                bearish_patterns[i] = be_three_line_strike[i]
            Value_bearish[i] += importance_value(imp_4C_three_line_strike)
        if bu_three_inside_up[i] > 0:
            if imp_3C_three_inside != NONE:
                bullish_patterns[i] = bu_three_inside_up[i]
            Value_bullish[i] += importance_value(imp_3C_three_inside)
        if be_three_inside_down[i] > 0:
            if imp_3C_three_inside != NONE:
                bearish_patterns[i] = be_three_inside_down[i]
            Value_bearish[i] += importance_value(imp_3C_three_inside)
        if bu_three_outside_up[i] > 0:
            if imp_3C_three_outside != NONE:
                bullish_patterns[i] = bu_three_outside_up[i]
            Value_bullish[i] += importance_value(imp_3C_three_outside)
        if be_three_outside_down[i] > 0:
            if imp_3C_three_inside != NONE:
                bearish_patterns[i] = be_three_outside_down[i]
            Value_bearish[i] += importance_value(imp_3C_three_outside)
        if bu_tweezer_bottom[i] > 0:
            if imp_2C_tweezer != NONE:
                bullish_patterns[i] = bu_tweezer_bottom[i]
            Value_bullish[i] += importance_value(imp_2C_tweezer)
        if be_tweezer_top[i] > 0:
            if imp_2C_tweezer != NONE:
                bearish_patterns[i] = be_tweezer_top[i]
            Value_bearish[i] += importance_value(imp_2C_tweezer)
        if (Value_bullish[i] - Value_bearish[i]) >= Minimal_Value:
            pass
        else:
            bullish_patterns[i] = 0.0
        if (Value_bearish[i] - Value_bullish[i]) >= Minimal_Value:
            pass
        else:
            bearish_patterns[i] = 0.0
        if Value_bullish[i] >= Minimal_Value and Value_bearish[i] >= Minimal_Value:
            pass
    return rates_total

def importance_value(importance):
    if importance == NONE:
        return 0
    if importance == LOW:
        return 1
    if importance == MODERATE:
        return 2
    if importance == HIGH:
        return 3
    return 0

def cal_be_three_black_cows(open, high, low, close, time, i):
    if ((((((((open[i - 3] > close[i - 3] and open[i - 2] > close[i - 2]) and open[i - 1] > close[i - 1]) and open[i - 4] < close[i - 4]) and high[i - 3] > high[i - 2]) and high[i - 2] > high[i - 1]) and close[i - 3] > close[i - 2]) and close[i - 2] > close[i - 1]) and MathAbs((open[i - 7] + close[i - 7]) / 2) < MathAbs((open[i - 4] + close[i - 4]) / 2)) and MathAbs((open[i - 10] + close[i - 10]) / 2) < MathAbs((open[i - 7] + close[i - 7]) / 2):
        be_three_black_cows[i] = open[i]

def cal_bu_three_white_soldiers(open, high, low, close, time, i):
    if ((((((((open[i - 3] < close[i - 3] and open[i - 2] < close[i - 2]) and open[i - 1] < close[i - 1]) and open[i - 4] > close[i - 4]) and low[i - 3] < low[i - 2]) and low[i - 2] < low[i - 1]) and close[i - 3] < close[i - 2]) and close[i - 2] < close[i - 1]) and MathAbs((open[i - 7] + close[i - 7]) / 2) > MathAbs((open[i - 4] + close[i - 4]) / 2)) and MathAbs((open[i - 10] + close[i - 10]) / 2) > MathAbs((open[i - 7] + close[i - 7]) / 2):
        bu_three_white_soldiers[i] = open[i]

def cal_bu_bullish_kicker(open, high, low, close, time, i):
    if (open[i - 2] > close[i - 2] and open[i - 1] < close[i - 1]) and high[i - 2] < low[i - 1]:
        bu_bullish_kicker[i] = open[i]

def cal_be_bearish_kicker(open, high, low, close, time, i):
    if (open[i - 2] < close[i - 2] and open[i - 1] > close[i - 1]) and low[i - 2] > high[i - 1]:
        be_bearish_kicker[i] = open[i]

def cal_bu_bullish_engulfing(open, high, low, close, time, i):
    if (((open[i - 2] > close[i - 2] and open[i - 1] < close[i - 1]) and (high[i - 2] - low[i - 2]) < (high[i - 1] - low[i - 1])) and open[i - 2] < close[i - 1]) and close[i - 2] > open[i - 1]:
        bu_bullish_engulfing[i] = open[i]

def cal_be_bearish_engulfing(open, high, low, close, time, i):
    if (((open[i - 2] < close[i - 2] and open[i - 1] > close[i - 1]) and (high[i - 2] - low[i - 2]) < (high[i - 1] - low[i - 1])) and open[i - 2] > close[i - 1]) and close[i - 2] < open[i - 1]:
        be_bearish_engulfing[i] = open[i]

def cal_bu_bullish_harami(open, high, low, close, time, i):
    if (((open[i - 2] > close[i - 2] and open[i - 1] < close[i - 1]) and (high[i - 2] - low[i - 2]) > (high[i - 1] - low[i - 1])) and open[i - 2] > close[i - 1]) and close[i - 2] < open[i - 1]:
        bu_bullish_harami[i] = open[i]

def cal_be_bearish_harami(open, high, low, close, time, i):
    if (((open[i - 2] < close[i - 2] and open[i - 1] > close[i - 1]) and (high[i - 2] - low[i - 2]) > (high[i - 1] - low[i - 1])) and open[i - 2] < close[i - 1]) and close[i - 2] > open[i - 1]:
        be_bearish_harami[i] = open[i]

def cal_bu_three_line_strike(open, high, low, close, time, i):
    if (((((((open[i - 4] < close[i - 4] and open[i - 3] < close[i - 3]) and open[i - 2] < close[i - 2]) and open[i - 1] > close[i - 1]) and low[i - 4] > close[i - 1]) and close[i - 4] < close[i - 3]) and close[i - 3] < close[i - 2]) and low[i - 4] < low[i - 3]) and low[i - 3] < low[i - 2]:
        bu_three_line_strike[i] = open[i]

def cal_be_three_line_strike(open, high, low, close, time, i):
    if (((((((open[i - 4] > close[i - 4] and open[i - 3] > close[i - 3]) and open[i - 2] > close[i - 2]) and open[i - 1] < close[i - 1]) and high[i - 4] < close[i - 1]) and close[i - 4] > close[i - 3]) and close[i - 3] > close[i - 2]) and high[i - 4] > high[i - 3]) and high[i - 3] > high[i - 2]:
        bu_three_line_strike[i] = open[i]

def cal_bu_three_inside_up(open, high, low, close, time, i):
    if ((((open[i - 3] > close[i - 3] and open[i - 2] < close[i - 2]) and open[i - 1] < close[i - 1]) and MathAbs((open[i - 3] + close[i - 3]) / 2) < close[i - 2]) and open[i - 3] < close[i - 1]) and close[i - 2] < open[i - 3]:
        bu_three_inside_up[i] = open[i]

def cal_be_three_inside_down(open, high, low, close, time, i):
    if ((((open[i - 3] < close[i - 3] and open[i - 2] > close[i - 2]) and open[i - 1] > close[i - 1]) and MathAbs((open[i - 3] + close[i - 3]) / 2) > close[i - 2]) and close[i - 3] > open[i - 1]) and close[i - 2] > open[i - 3]:
        be_three_inside_down[i] = open[i]

def cal_bu_three_outside_up(open, high, low, close, time, i):
    if (((((open[i - 3] > close[i - 3] and open[i - 2] < close[i - 2]) and open[i - 1] < close[i - 1]) and (high[i - 3] - low[i - 3]) < (high[i - 2] - low[i - 2])) and open[i - 3] < close[i - 2]) and close[i - 3] > open[i - 2]) and close[i - 2] < close[i - 1]:
        bu_three_outside_up[i] = open[i]

def cal_be_three_outside_down(open, high, low, close, time, i):
    if (((((open[i - 3] < close[i - 3] and open[i - 2] > close[i - 2]) and open[i - 1] > close[i - 1]) and (high[i - 3] - low[i - 3]) < (high[i - 2] - low[i - 2])) and open[i - 3] > close[i - 2]) and close[i - 3] < open[i - 2]) and close[i - 2] > close[i - 1]:
        be_three_outside_down[i] = open[i]

def cal_bu_tweezer_bottom(open, high, low, close, time, i):
    if ((open[i - 2] > close[i - 2] and open[i - 1] < close[i - 1]) and low[i - 2] == close[i - 2]) and low[i - 1] == open[i - 1]:
        bu_tweezer_bottom[i] = open[i]

def cal_be_tweezer_top(open, high, low, close, time, i):
    if ((open[i - 2] < close[i - 2] and open[i - 1] > close[i - 1]) and high[i - 2] == close[i - 2]) and high[i - 1] == open[i - 1]:
        be_tweezer_top[i] = open[i]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandlestickPatternsV2(_MQL5Indicator):
    name = 'Candlestick_Patterns_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Minimal_Value': 2,
        'imp_3C_three_white_soldiers_black_cows': _Choice({0: 'NONE', 1: 'LOW', 2: 'MODERATE', 3: 'HIGH'}, default=2),
        'imp_2C_bullish_bearish_kicker': _Choice({0: 'NONE', 1: 'LOW', 2: 'MODERATE', 3: 'HIGH'}, default=2),
        'imp_2C_bullish_bearish_engulfing': _Choice({0: 'NONE', 1: 'LOW', 2: 'MODERATE', 3: 'HIGH'}, default=2),
        'imp_2C_bullish_bearish_harami': _Choice({0: 'NONE', 1: 'LOW', 2: 'MODERATE', 3: 'HIGH'}, default=2),
        'imp_4C_three_line_strike': _Choice({0: 'NONE', 1: 'LOW', 2: 'MODERATE', 3: 'HIGH'}, default=3),
        'imp_3C_three_inside': _Choice({0: 'NONE', 1: 'LOW', 2: 'MODERATE', 3: 'HIGH'}, default=2),
        'imp_3C_three_outside': _Choice({0: 'NONE', 1: 'LOW', 2: 'MODERATE', 3: 'HIGH'}, default=2),
        'imp_2C_tweezer': _Choice({0: 'NONE', 1: 'LOW', 2: 'MODERATE', 3: 'HIGH'}, default=2),
    }

