"""Marubozu — converted from MQL5: MQL5 Indicators/Marubozu/Marubozu.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [3329330], 2: [9639167]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '+M', 2: '-M'}, 'levels': [], 'description': [], 'name': 'Marubozu', 'source': 'MQL5 Indicators/Marubozu/Marubozu.mq5', 'folder': 'Marubozu', 'inputs': [{'mql': 'InpBullishMarubozuCode', 'py': 'InpBullishMarubozuCode', 'param': 'InpBullishMarubozuCode', 'type': 'uchar', 'default': 167, 'label': 'Bullish Marubozu: code for style DRAW_ARROW (font Wingdings)', 'sinput': True}, {'mql': 'InpBullishMarubozuShift', 'py': 'InpBullishMarubozuShift', 'param': 'InpBullishMarubozuShift', 'type': 'int', 'default': 10, 'label': 'Bullish Marubozu: vertical shift of arrows in pixels', 'sinput': True}, {'mql': 'InpBearishMarubozuCode', 'py': 'InpBearishMarubozuCode', 'param': 'InpBearishMarubozuCode', 'type': 'uchar', 'default': 167, 'label': 'Bearish Marubozu: code for style DRAW_ARROW (font Wingdings)', 'sinput': True}, {'mql': 'InpBearishMarubozuShift', 'py': 'InpBearishMarubozuShift', 'param': 'InpBearishMarubozuShift', 'type': 'int', 'default': 10, 'label': 'Bearish Marubozu: vertical shift of arrows in pixels', 'sinput': True}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBullishMarubozuCode = _input('InpBullishMarubozuCode', 167)  # Bullish Marubozu: code for style DRAW_ARROW (font Wingdings)
InpBullishMarubozuShift = _input('InpBullishMarubozuShift', 10)  # Bullish Marubozu: vertical shift of arrows in pixels
InpBearishMarubozuCode = _input('InpBearishMarubozuCode', 167)  # Bearish Marubozu: code for style DRAW_ARROW (font Wingdings)
InpBearishMarubozuShift = _input('InpBearishMarubozuShift', 10)  # Bearish Marubozu: vertical shift of arrows in pixels
BullishMarubozuBuffer = Arr(0, 0.0)
BearishMarubozuBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BullishMarubozuBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BearishMarubozuBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, InpBullishMarubozuCode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpBearishMarubozuCode)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, InpBullishMarubozuShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -InpBearishMarubozuShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 1
        BullishMarubozuBuffer[0] = 0.0
        BearishMarubozuBuffer[0] = 0.0
    for i in range(limit, rates_total):
        BullishMarubozuBuffer[i] = 0.0
        BearishMarubozuBuffer[i] = 0.0
        if i > 0:
            if open[i] == high[i] and close[i] == low[i]:
                BearishMarubozuBuffer[i] = high[i]
            if close[i] == high[i] and open[i] == low[i]:
                BullishMarubozuBuffer[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Marubozu(_MQL5Indicator):
    name = 'Marubozu'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBullishMarubozuCode': 167,  # Bullish Marubozu: code for style DRAW_ARROW (font Wingdings)
        'InpBullishMarubozuShift': 10,  # Bullish Marubozu: vertical shift of arrows in pixels
        'InpBearishMarubozuCode': 167,  # Bearish Marubozu: code for style DRAW_ARROW (font Wingdings)
        'InpBearishMarubozuShift': 10,  # Bearish Marubozu: vertical shift of arrows in pixels
    }

