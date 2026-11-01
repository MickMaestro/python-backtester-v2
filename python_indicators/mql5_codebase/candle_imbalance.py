"""Candle_Imbalance — converted from MQL5: MQL5 Indicators/Candlestick Wick Imbalance/Candle_Imbalance.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16448255], 2: [16448255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '+CI', 2: '-CI'}, 'levels': [], 'description': [], 'name': 'Candle_Imbalance', 'source': 'MQL5 Indicators/Candlestick Wick Imbalance/Candle_Imbalance.mq5', 'folder': 'Candlestick Wick Imbalance', 'inputs': [{'mql': 'InpBullishCandle_ImbalanceCode', 'py': 'InpBullishCandle_ImbalanceCode', 'param': 'InpBullishCandle_ImbalanceCode', 'type': 'uchar', 'default': 167, 'label': 'Bullish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)', 'sinput': True}, {'mql': 'InpBullishCandle_ImbalanceShift', 'py': 'InpBullishCandle_ImbalanceShift', 'param': 'InpBullishCandle_ImbalanceShift', 'type': 'int', 'default': 0, 'label': 'Bullish Candle_Imbalance: vertical shift of arrows in pixels', 'sinput': False}, {'mql': 'InpBearishCandle_ImbalanceCode', 'py': 'InpBearishCandle_ImbalanceCode', 'param': 'InpBearishCandle_ImbalanceCode', 'type': 'uchar', 'default': 167, 'label': 'Bearish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)', 'sinput': True}, {'mql': 'InpBearishCandle_ImbalanceShift', 'py': 'InpBearishCandle_ImbalanceShift', 'param': 'InpBearishCandle_ImbalanceShift', 'type': 'int', 'default': 0, 'label': 'Bearish Candle Imbalance: vertical shift of arrows in pixels', 'sinput': False}, {'mql': 'multiply', 'py': 'multiply', 'param': 'multiply', 'type': 'double', 'default': 2.0, 'label': 'Multiplicator of Candle Wick', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBullishCandle_ImbalanceCode = _input('InpBullishCandle_ImbalanceCode', 167)  # Bullish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)
InpBullishCandle_ImbalanceShift = _input('InpBullishCandle_ImbalanceShift', 0)  # Bullish Candle_Imbalance: vertical shift of arrows in pixels
InpBearishCandle_ImbalanceCode = _input('InpBearishCandle_ImbalanceCode', 167)  # Bearish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)
InpBearishCandle_ImbalanceShift = _input('InpBearishCandle_ImbalanceShift', 0)  # Bearish Candle Imbalance: vertical shift of arrows in pixels
multiply = _input('multiply', 2.0)  # Multiplicator of Candle Wick
BullishCandle_ImbalanceBuffer = Arr(0, 0.0)
BearishCandle_ImbalanceBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BullishCandle_ImbalanceBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BearishCandle_ImbalanceBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, InpBullishCandle_ImbalanceCode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpBearishCandle_ImbalanceCode)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, InpBullishCandle_ImbalanceShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -InpBearishCandle_ImbalanceShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 1
        BullishCandle_ImbalanceBuffer[0] = 0.0
        BearishCandle_ImbalanceBuffer[0] = 0.0
    for i in range(limit, rates_total):
        BullishCandle_ImbalanceBuffer[i] = 0.0
        BearishCandle_ImbalanceBuffer[i] = 0.0
        if i > 0:
            if open[i] < close[i]:
                if (high[i] - close[i]) > ((open[i] - low[i]) * multiply):
                    BearishCandle_ImbalanceBuffer[i] = high[i]
                if ((high[i] - close[i]) * multiply) < (open[i] - low[i]):
                    BearishCandle_ImbalanceBuffer[i] = low[i]
            else:
                if (high[i] - open[i]) > ((close[i] - low[i]) * multiply):
                    BullishCandle_ImbalanceBuffer[i] = high[i]
                if ((high[i] - open[i]) * multiply) < (close[i] - low[i]):
                    BullishCandle_ImbalanceBuffer[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleImbalance(_MQL5Indicator):
    name = 'Candle_Imbalance'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBullishCandle_ImbalanceCode': 167,  # Bullish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)
        'InpBullishCandle_ImbalanceShift': 0,  # Bullish Candle_Imbalance: vertical shift of arrows in pixels
        'InpBearishCandle_ImbalanceCode': 167,  # Bearish Candle Imbalance: code for style DRAW_ARROW (font Wingdings)
        'InpBearishCandle_ImbalanceShift': 0,  # Bearish Candle Imbalance: vertical shift of arrows in pixels
        'multiply': 2.0,  # Multiplicator of Candle Wick
    }

