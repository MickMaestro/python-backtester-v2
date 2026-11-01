"""pine_sample_div — converted from MQL5: MQL5 Indicators/Sample pine script stochastic divergence/pine_sample_div.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [17919], 2: [3329330]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'regular_bearish_div', 2: 'regular_bullish_div'}, 'levels': [], 'description': [], 'name': 'pine_sample_div', 'source': 'MQL5 Indicators/Sample pine script stochastic divergence/pine_sample_div.mq5', 'folder': 'Sample pine script stochastic divergence', 'inputs': [{'mql': 'stoch_len', 'py': 'stoch_len', 'param': 'stoch_len', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
stoch_len = _input('stoch_len', 5)
regular_bearish_divBuffer = Arr(0, 0.0)
regular_bullish_divBuffer = Arr(0, 0.0)
stochBuffer = Arr(0, 0.0)
fractal_topBuffer = Arr(0, 0.0)
fractal_botBuffer = Arr(0, 0.0)
high_prevBuffer = Arr(0, 0.0)
high_priceBuffer = Arr(0, 0.0)
low_prevBuffer = Arr(0, 0.0)
low_priceBuffer = Arr(0, 0.0)
prefix = 'Div_'

def OnInit():
    SetIndexBuffer(0, regular_bearish_divBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, regular_bullish_divBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, stochBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, fractal_topBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, fractal_botBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, high_prevBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, high_priceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, low_prevBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, low_priceBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(0, PLOT_SHIFT, -2)
    PlotIndexSetInteger(1, PLOT_SHIFT, -2)
    ArraySetAsSeries(regular_bearish_divBuffer, True)
    ArraySetAsSeries(regular_bullish_divBuffer, True)
    ArraySetAsSeries(stochBuffer, True)
    ArraySetAsSeries(fractal_topBuffer, True)
    ArraySetAsSeries(fractal_botBuffer, True)
    ArraySetAsSeries(high_prevBuffer, True)
    ArraySetAsSeries(high_priceBuffer, True)
    ArraySetAsSeries(low_prevBuffer, True)
    ArraySetAsSeries(low_priceBuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    BARS = MathMax(rates_total - prev_calculated - stoch_len, 1)
    for i in range(BARS, 0 - 1, -1):
        stochBuffer[i] = pine_stoch(close, high, low, stoch_len, i)
        fractal_topBuffer[i] = (stochBuffer[i + 2] if (f_fractalize(stochBuffer, i) > 0) else EMPTY_VALUE)
        fractal_botBuffer[i] = (stochBuffer[i + 2] if (f_fractalize(stochBuffer, i) < 0) else EMPTY_VALUE)
        prev_top_index = Box(0)
        prev_bot_index = Box(0)
        high_prevBuffer[i] = pine_valuewhen(fractal_topBuffer, stochBuffer, 1, i, rates_total, prev_top_index)
        high_priceBuffer[i] = pine_valuewhen(fractal_topBuffer, high, 1, i, rates_total, prev_top_index)
        low_prevBuffer[i] = pine_valuewhen(fractal_botBuffer, stochBuffer, 1, i, rates_total, prev_bot_index)
        low_priceBuffer[i] = pine_valuewhen(fractal_botBuffer, low, 1, i, rates_total, prev_bot_index)
        regular_bearish_divBuffer[i] = (high[i + 2] if ((fractal_topBuffer[i] != EMPTY_VALUE and high[i + 2] > high_priceBuffer[i]) and stochBuffer[i + 2] < high_prevBuffer[i]) else EMPTY_VALUE)
        regular_bullish_divBuffer[i] = (low[i + 2] if ((fractal_botBuffer[i] != EMPTY_VALUE and low[i + 2] < low_priceBuffer[i]) and stochBuffer[i + 2] > low_prevBuffer[i]) else EMPTY_VALUE)
        if regular_bearish_divBuffer[i] != EMPTY_VALUE:
            PlotText(time[i + 2], high[i + 2], 'R', clrOrangeRed, ANCHOR_LOWER)
            PlotLine(time[prev_top_index.v + 2], time[i + 2], high[prev_top_index.v + 2], high[i + 2], clrOrangeRed)
        if regular_bullish_divBuffer[i] != EMPTY_VALUE:
            PlotText(time[i + 2], low[i + 2], 'R', clrLimeGreen, ANCHOR_UPPER)
            PlotLine(time[prev_bot_index.v + 2], time[i + 2], low[prev_bot_index.v + 2], low[i + 2], clrLimeGreen)
    return rates_total

def pine_stoch(source, high, low, length, index):
    return _fdiv(100 * (source[index] - pine_lowest(low, length, index)), pine_highest(high, length, index) - pine_lowest(low, length, index))

def pine_highest(_src, len_, i):
    return _src[ArrayMaximum(_src, i, len_)]

def pine_lowest(_src, len_, i):
    return _src[ArrayMinimum(_src, i, len_)]

def f_top_fractal(_src, index):
    return ((_src[index + 4] < _src[index + 2] and _src[index + 3] < _src[index + 2]) and _src[index + 2] > _src[index + 1]) and _src[index + 2] > _src[index + 0]

def f_bot_fractal(_src, index):
    return ((_src[index + 4] > _src[index + 2] and _src[index + 3] > _src[index + 2]) and _src[index + 2] < _src[index + 1]) and _src[index + 2] < _src[index + 0]

def f_fractalize(_src, index):
    f_bot_fractal__1 = f_bot_fractal(_src, index)
    return (1 if f_top_fractal(_src, index) else -1 if f_bot_fractal__1 else 0)

def pine_valuewhen(condition, source, occurence, index, rates_total, out_index):
    counter = -1
    out_index.v = -1
    for i in range(index, rates_total):
        if condition[i] != EMPTY_VALUE:
            counter += 1
        if counter == occurence:
            out_index.v = i
            return source[i + 2]
    return EMPTY_VALUE

def PlotText(time, price, text, col, anchor):
    name = prefix + TimeToString(time)
    ObjectCreate(0, name, OBJ_TEXT, 0, time, price)
    ObjectSetInteger(0, name, OBJPROP_COLOR, col)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 14)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, anchor)

def PlotLine(time1, time2, prev, price, col):
    name = prefix + '_LINE_' + TimeToString(time1)
    ObjectCreate(0, name, OBJ_TREND, 0, time1, prev, time2, price)
    ObjectSetInteger(0, name, OBJPROP_COLOR, col)
    ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, False)
    ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, False)

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PineSampleDiv(_MQL5Indicator):
    name = 'pine_sample_div'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'stoch_len': 5,
    }

