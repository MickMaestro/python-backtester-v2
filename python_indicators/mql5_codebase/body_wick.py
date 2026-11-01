"""Body_Wick — converted from MQL5: MQL5 Indicators/Body Wick Comparison/Body_Wick.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16448255], 2: [16448255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '+BW', 2: '-BW'}, 'levels': [], 'description': [], 'name': 'Body_Wick', 'source': 'MQL5 Indicators/Body Wick Comparison/Body_Wick.mq5', 'folder': 'Body Wick Comparison', 'inputs': [{'mql': 'InpBullishBodyWickCode', 'py': 'InpBullishBodyWickCode', 'param': 'InpBullishBodyWickCode', 'type': 'uchar', 'default': 167, 'label': 'Bullish BodyWick: code for style DRAW_ARROW (font Wingdings)', 'sinput': True}, {'mql': 'InpBullishBodyWickShift', 'py': 'InpBullishBodyWickShift', 'param': 'InpBullishBodyWickShift', 'type': 'int', 'default': 0, 'label': 'Bullish BodyWick: vertical shift of arrows in pixels', 'sinput': False}, {'mql': 'InpBearishBodyWickCode', 'py': 'InpBearishBodyWickCode', 'param': 'InpBearishBodyWickCode', 'type': 'uchar', 'default': 167, 'label': 'Bearish BodyWick: code for style DRAW_ARROW (font Wingdings)', 'sinput': True}, {'mql': 'InpBearishBodyWickShift', 'py': 'InpBearishBodyWickShift', 'param': 'InpBearishBodyWickShift', 'type': 'int', 'default': 0, 'label': 'Bearish BodyWick: vertical shift of arrows in pixels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBullishBodyWickCode = _input('InpBullishBodyWickCode', 167)  # Bullish BodyWick: code for style DRAW_ARROW (font Wingdings)
InpBullishBodyWickShift = _input('InpBullishBodyWickShift', 0)  # Bullish BodyWick: vertical shift of arrows in pixels
InpBearishBodyWickCode = _input('InpBearishBodyWickCode', 167)  # Bearish BodyWick: code for style DRAW_ARROW (font Wingdings)
InpBearishBodyWickShift = _input('InpBearishBodyWickShift', 0)  # Bearish BodyWick: vertical shift of arrows in pixels
BullishBodyWickBuffer = Arr(0, 0.0)
BearishBodyWickBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BullishBodyWickBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BearishBodyWickBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, InpBullishBodyWickCode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpBearishBodyWickCode)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, InpBullishBodyWickShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -InpBearishBodyWickShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 1
        BullishBodyWickBuffer[0] = 0.0
        BearishBodyWickBuffer[0] = 0.0
    for i in range(limit, rates_total):
        BullishBodyWickBuffer[i] = 0.0
        BearishBodyWickBuffer[i] = 0.0
        if i > 0:
            if open[i] > close[i]:
                if (open[i] - close[i]) < (close[i] - low[i]) or (open[i] - close[i]) < (high[i] - open[i]):
                    BearishBodyWickBuffer[i] = high[i]
            else:
                if (close[i] - open[i]) < (open[i] - low[i]) or (close[i] - open[i]) < (high[i] - close[i]):
                    BullishBodyWickBuffer[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BodyWick(_MQL5Indicator):
    name = 'Body_Wick'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBullishBodyWickCode': 167,  # Bullish BodyWick: code for style DRAW_ARROW (font Wingdings)
        'InpBullishBodyWickShift': 0,  # Bullish BodyWick: vertical shift of arrows in pixels
        'InpBearishBodyWickCode': 167,  # Bearish BodyWick: code for style DRAW_ARROW (font Wingdings)
        'InpBearishBodyWickShift': 0,  # Bearish BodyWick: vertical shift of arrows in pixels
    }

