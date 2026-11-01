"""Candle_Fitness — converted from MQL5: MQL5 Indicators/Candle Fitness/Candle_Fitness.mq5

Copyright: Copyright 2024, Rajesh Kumar Nait; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Rajesh Kumar Nait', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': [], 'name': 'Candle_Fitness', 'source': 'MQL5 Indicators/Candle Fitness/Candle_Fitness.mq5', 'folder': 'Candle Fitness', 'inputs': [{'mql': 'clr_Bull', 'py': 'clr_Bull', 'param': None, 'type': 'color', 'default': 3434752, 'label': '', 'sinput': False}, {'mql': 'clr_Bear', 'py': 'clr_Bear', 'param': None, 'type': 'color', 'default': 2448369, 'label': '', 'sinput': False}, {'mql': 'threshold', 'py': 'threshold', 'param': 'threshold', 'type': 'double', 'default': 0.75, 'label': 'Threshold for body weight', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
clr_Bull = _input('clr_Bull', 0x346900)
clr_Bear = _input('clr_Bear', 0x255BF1)
threshold = _input('threshold', 0.75)  # Threshold for body weight
buf_open = Arr(0, 0.0)
buf_high = Arr(0, 0.0)
buf_low = Arr(0, 0.0)
buf_close = Arr(0, 0.0)
buf_color = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, buf_open, INDICATOR_DATA)
    SetIndexBuffer(1, buf_high, INDICATOR_DATA)
    SetIndexBuffer(2, buf_low, INDICATOR_DATA)
    SetIndexBuffer(3, buf_close, INDICATOR_DATA)
    colorbg = ChartBackColorGet(ChartID())
    SetIndexBuffer(4, buf_color, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, colorbg)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, clr_Bull)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, clr_Bear)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(prev_calculated, rates_total - 1 + 1):
        buf_open[i] = open[i]
        buf_high[i] = high[i]
        buf_low[i] = low[i]
        buf_close[i] = close[i]
        bodyWeight = MathAbs(close[i] - open[i])
        upperWick = high[i] - MathMax(open[i], close[i])
        lowerWick = MathMin(open[i], close[i]) - low[i]
        bodyWeightPercentage = _fdiv(bodyWeight, upperWick + lowerWick)
        isFit = bodyWeightPercentage >= threshold
        if not isFit:
            buf_color[i] = 0.0
        else:
            if close[i] > open[i]:
                buf_color[i] = 1.0
            if close[i] < open[i]:
                buf_color[i] = 2.0
    return rates_total

def ChartBackColorGet(chart_ID=0):
    result = Box(clrNONE)
    ResetLastError()
    if not ChartGetInteger(chart_ID, CHART_COLOR_BACKGROUND, 0, result):
        Print('ChartBackColorGet' + ', Error Code = ', GetLastError())
    return _uint(result.v)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleFitness(_MQL5Indicator):
    name = 'Candle_Fitness'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'threshold': 0.75,  # Threshold for body weight
    }

