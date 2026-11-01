"""NoWick — converted from MQL5: MQL5 Indicators/Wickless Breakout/NoWick.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16448255], 2: [16448255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '+CI', 2: '-CI'}, 'levels': [], 'description': [], 'name': 'NoWick', 'source': 'MQL5 Indicators/Wickless Breakout/NoWick.mq5', 'folder': 'Wickless Breakout', 'inputs': [{'mql': 'InpBullishNoWickCode', 'py': 'InpBullishNoWickCode', 'param': 'InpBullishNoWickCode', 'type': 'uchar', 'default': 251, 'label': 'Bullish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)', 'sinput': True}, {'mql': 'InpBullishNoWickShift', 'py': 'InpBullishNoWickShift', 'param': 'InpBullishNoWickShift', 'type': 'int', 'default': 10, 'label': 'Bullish NoWick: vertical shift of arrows in pixels', 'sinput': False}, {'mql': 'InpBearishNoWickCode', 'py': 'InpBearishNoWickCode', 'param': 'InpBearishNoWickCode', 'type': 'uchar', 'default': 251, 'label': 'Bearish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)', 'sinput': True}, {'mql': 'InpBearishNoWickShift', 'py': 'InpBearishNoWickShift', 'param': 'InpBearishNoWickShift', 'type': 'int', 'default': 10, 'label': 'Bearish Candle Imbalance: vertical shift of arrows in pixels', 'sinput': False}, {'mql': 'multiply', 'py': 'multiply', 'param': 'multiply', 'type': 'double', 'default': 2.0, 'label': 'Multiplicator of Candle Wick', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBullishNoWickCode = _input('InpBullishNoWickCode', 251)  # Bullish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)
InpBullishNoWickShift = _input('InpBullishNoWickShift', 10)  # Bullish NoWick: vertical shift of arrows in pixels
InpBearishNoWickCode = _input('InpBearishNoWickCode', 251)  # Bearish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)
InpBearishNoWickShift = _input('InpBearishNoWickShift', 10)  # Bearish Candle Imbalance: vertical shift of arrows in pixels
multiply = _input('multiply', 2.0)  # Multiplicator of Candle Wick
BullishNoWickBuffer = Arr(0, 0.0)
BearishNoWickBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BullishNoWickBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BearishNoWickBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, InpBullishNoWickCode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpBearishNoWickCode)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, InpBullishNoWickShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -InpBearishNoWickShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 1
        BullishNoWickBuffer[0] = 0.0
        BearishNoWickBuffer[0] = 0.0
    for i in range(limit, rates_total):
        BullishNoWickBuffer[i] = 0.0
        BearishNoWickBuffer[i] = 0.0
        if i > 0:
            if open[i] < close[i]:
                if high[i] == close[i]:
                    BearishNoWickBuffer[i] = high[i]
                if low[i] == open[i]:
                    BullishNoWickBuffer[i] = low[i]
            else:
                if high[i] == open[i]:
                    BearishNoWickBuffer[i] = high[i]
                if low[i] == close[i]:
                    BullishNoWickBuffer[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NoWick(_MQL5Indicator):
    name = 'NoWick'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBullishNoWickCode': 251,  # Bullish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)
        'InpBullishNoWickShift': 10,  # Bullish NoWick: vertical shift of arrows in pixels
        'InpBearishNoWickCode': 251,  # Bearish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)
        'InpBearishNoWickShift': 10,  # Bearish Candle Imbalance: vertical shift of arrows in pixels
        'multiply': 2.0,  # Multiplicator of Candle Wick
    }

