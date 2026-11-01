"""Wick_50_Perc — converted from MQL5: MQL5 Indicators/Custom Hammer and Inverted Hammer/Wick_50_Perc.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': [], 'name': 'Wick_50_Perc', 'source': 'MQL5 Indicators/Custom Hammer and Inverted Hammer/Wick_50_Perc.mq5', 'folder': 'Custom Hammer and Inverted Hammer', 'inputs': [{'mql': 'clr_Green', 'py': 'clr_Green', 'param': None, 'type': 'color', 'default': 12707084, 'label': '', 'sinput': False}, {'mql': 'clr_Red', 'py': 'clr_Red', 'param': None, 'type': 'color', 'default': 3684607, 'label': '', 'sinput': False}, {'mql': 'multiply', 'py': 'multiply', 'param': 'multiply', 'type': 'double', 'default': 1.25, 'label': 'Multiplicator of Candle Body', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
clr_Green = _input('clr_Green', 0xC1E50C)
clr_Red = _input('clr_Red', 0x3838FF)
multiply = _input('multiply', 1.25)  # Multiplicator of Candle Body
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
    SetIndexBuffer(4, buf_color, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 2)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, clr_Green)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, clr_Red)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(prev_calculated, rates_total - 1 + 1):
        buf_open[i] = open[i]
        buf_high[i] = high[i]
        buf_low[i] = low[i]
        buf_close[i] = close[i]
        if open[i] < close[i] and (multiply * (close[i] - open[i])) < (high[i] - close[i]):
            buf_color[i] = 1.0
        elif open[i] > close[i] and (multiply * (open[i] - close[i])) < (close[i] - low[i]):
            buf_color[i] = 0.0
        else:
            buf_color[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wick50Perc(_MQL5Indicator):
    name = 'Wick_50_Perc'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'multiply': 1.25,  # Multiplicator of Candle Body
    }

