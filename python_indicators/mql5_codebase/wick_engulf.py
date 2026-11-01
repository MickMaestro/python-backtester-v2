"""Wick_Engulf — converted from MQL5: MQL5 Indicators/Wick Engulf/Wick_Engulf.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16448255], 2: [16448255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '+WE', 2: '-WE'}, 'levels': [], 'description': [], 'name': 'Wick_Engulf', 'source': 'MQL5 Indicators/Wick Engulf/Wick_Engulf.mq5', 'folder': 'Wick Engulf', 'inputs': [{'mql': 'InpBullishWECode', 'py': 'InpBullishWECode', 'param': 'InpBullishWECode', 'type': 'uchar', 'default': 233, 'label': 'BullishWE: code for style DRAW_ARROW (font Wingdings)', 'sinput': False}, {'mql': 'InpBullishWEShift', 'py': 'InpBullishWEShift', 'param': 'InpBullishWEShift', 'type': 'int', 'default': 10, 'label': 'BullishWE: vertical shift of arrows in pixels', 'sinput': False}, {'mql': 'InpBearishWECode', 'py': 'InpBearishWECode', 'param': 'InpBearishWECode', 'type': 'uchar', 'default': 234, 'label': 'BearishWE: code for style DRAW_ARROW (font Wingdings)', 'sinput': False}, {'mql': 'InpBearishWEShift', 'py': 'InpBearishWEShift', 'param': 'InpBearishWEShift', 'type': 'int', 'default': 10, 'label': 'BearishWE: vertical shift of arrows in pixels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBullishWECode = _input('InpBullishWECode', 233)  # BullishWE: code for style DRAW_ARROW (font Wingdings)
InpBullishWEShift = _input('InpBullishWEShift', 10)  # BullishWE: vertical shift of arrows in pixels
InpBearishWECode = _input('InpBearishWECode', 234)  # BearishWE: code for style DRAW_ARROW (font Wingdings)
InpBearishWEShift = _input('InpBearishWEShift', 10)  # BearishWE: vertical shift of arrows in pixels
BullishWEBuffer = Arr(0, 0.0)
BearishWEBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, BullishWEBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BearishWEBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, InpBullishWECode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpBearishWECode)
    ArraySetAsSeries(BullishWEBuffer, True)
    ArraySetAsSeries(BearishWEBuffer, True)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, InpBullishWEShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -InpBearishWEShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    for i in range(limit, 0 - 1, -1):
        BullishWEBuffer[i] = 0.0
        BearishWEBuffer[i] = 0.0
        BearishWEBuffer[0] = 0.0
        if (((open[i] < close[i] and open[i + 1] < close[i + 1]) and high[i + 1] > high[i]) and open[i] >= close[i + 1]) or (((open[i] < close[i] and open[i + 1] > close[i + 1]) and high[i + 1] > high[i]) and open[i] >= open[i + 1]):
            BearishWEBuffer[i] = high[i]
        BullishWEBuffer[0] = 0.0
        if (((open[i] > close[i] and open[i + 1] > close[i + 1]) and low[i + 1] < low[i]) and open[i] <= close[i + 1]) or (((open[i] > close[i] and open[i + 1] < close[i + 1]) and low[i + 1] < low[i]) and open[i] <= open[i + 1]):
            BullishWEBuffer[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WickEngulf(_MQL5Indicator):
    name = 'Wick_Engulf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBullishWECode': 233,  # BullishWE: code for style DRAW_ARROW (font Wingdings)
        'InpBullishWEShift': 10,  # BullishWE: vertical shift of arrows in pixels
        'InpBearishWECode': 234,  # BearishWE: code for style DRAW_ARROW (font Wingdings)
        'InpBearishWEShift': 10,  # BearishWE: vertical shift of arrows in pixels
    }

