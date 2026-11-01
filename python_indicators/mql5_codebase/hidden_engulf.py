"""Hidden_Engulf — converted from MQL5: MQL5 Indicators/Hidden Engulfing/Hidden_Engulf.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16448255], 2: [16448255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '+HE', 2: '-HE'}, 'levels': [], 'description': [], 'name': 'Hidden_Engulf', 'source': 'MQL5 Indicators/Hidden Engulfing/Hidden_Engulf.mq5', 'folder': 'Hidden Engulfing', 'inputs': [{'mql': 'SelectMode', 'py': 'SelectMode', 'param': 'SelectMode', 'type': 'int', 'default': 0, 'label': 'Search Mode', 'sinput': False}, {'mql': 'InpHiddenBullishCode', 'py': 'InpHiddenBullishCode', 'param': 'InpHiddenBullishCode', 'type': 'uchar', 'default': 233, 'label': 'HiddenBullish: code for style DRAW_ARROW (font Wingdings)', 'sinput': False}, {'mql': 'InpHiddenBullishShift', 'py': 'InpHiddenBullishShift', 'param': 'InpHiddenBullishShift', 'type': 'int', 'default': 10, 'label': 'HiddenBullish: vertical shift of arrows in pixels', 'sinput': False}, {'mql': 'InpHiddenBearishCode', 'py': 'InpHiddenBearishCode', 'param': 'InpHiddenBearishCode', 'type': 'uchar', 'default': 234, 'label': 'HiddenBearish: code for style DRAW_ARROW (font Wingdings)', 'sinput': False}, {'mql': 'InpHiddenBearishShift', 'py': 'InpHiddenBearishShift', 'param': 'InpHiddenBearishShift', 'type': 'int', 'default': 10, 'label': 'HiddenBearish: vertical shift of arrows in pixels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum mode
Two = 0
Three = 1
_enum('mode', {0: 'Two', 1: 'Three'})

# ---- inputs and global variables
SelectMode = _input('SelectMode', Two)  # Search Mode
InpHiddenBullishCode = _input('InpHiddenBullishCode', 233)  # HiddenBullish: code for style DRAW_ARROW (font Wingdings)
InpHiddenBullishShift = _input('InpHiddenBullishShift', 10)  # HiddenBullish: vertical shift of arrows in pixels
InpHiddenBearishCode = _input('InpHiddenBearishCode', 234)  # HiddenBearish: code for style DRAW_ARROW (font Wingdings)
InpHiddenBearishShift = _input('InpHiddenBearishShift', 10)  # HiddenBearish: vertical shift of arrows in pixels
HiddenBullishBuffer = Arr(0, 0.0)
HiddenBearishBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 5
    SetIndexBuffer(0, HiddenBullishBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HiddenBearishBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, InpHiddenBullishCode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpHiddenBearishCode)
    ArraySetAsSeries(HiddenBullishBuffer, True)
    ArraySetAsSeries(HiddenBearishBuffer, True)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, InpHiddenBullishShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -InpHiddenBearishShift)
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
        HiddenBullishBuffer[i] = 0.0
        HiddenBearishBuffer[i] = 0.0
        if SelectMode == Two:
            HiddenBearishBuffer[0] = EMPTY_VALUE
            if (open[i + 2] < close[i + 2] and open[i + 1] > close[i + 1]) and open[i] > close[i]:
                if open[i + 1] <= close[i + 2] and close[i + 1] >= open[i + 2]:
                    if close[i] < open[i + 2]:
                        HiddenBearishBuffer[i] = high[i]
            HiddenBullishBuffer[0] = EMPTY_VALUE
            if (open[i + 2] > close[i + 2] and open[i + 1] < close[i + 1]) and open[i] < close[i]:
                if open[i + 1] >= close[i + 2] and close[i + 1] <= open[i + 2]:
                    if close[i] > open[i + 2]:
                        HiddenBullishBuffer[i] = low[i]
        if SelectMode == Three:
            HiddenBearishBuffer[0] = EMPTY_VALUE
            if ((open[i + 3] < close[i + 3] and open[i + 2] > close[i + 2]) and open[i + 1] > close[i + 1]) and open[i] > close[i]:
                if ((open[i + 2] <= close[i + 3] and close[i + 2] >= open[i + 3]) and open[i + 1] <= close[i + 1]) and close[i + 1] >= open[i + 1]:
                    if close[i] < open[i + 3]:
                        HiddenBearishBuffer[i] = high[i]
            HiddenBullishBuffer[0] = EMPTY_VALUE
            if ((open[i + 3] > close[i + 3] and open[i + 2] < close[i + 2]) and open[i + 1] < close[i + 1]) and open[i] < close[i]:
                if ((open[i + 2] >= close[i + 3] and close[i + 2] <= open[i + 3]) and open[i + 1] >= close[i + 3]) and close[i + 1] <= open[i + 3]:
                    if close[i] > open[i + 3]:
                        HiddenBullishBuffer[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HiddenEngulf(_MQL5Indicator):
    name = 'Hidden_Engulf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SelectMode': _Choice({0: 'Two Candle Breaks', 1: 'Three Candle Breaks'}, default=0),  # Search Mode
        'InpHiddenBullishCode': 233,  # HiddenBullish: code for style DRAW_ARROW (font Wingdings)
        'InpHiddenBullishShift': 10,  # HiddenBullish: vertical shift of arrows in pixels
        'InpHiddenBearishCode': 234,  # HiddenBearish: code for style DRAW_ARROW (font Wingdings)
        'InpHiddenBearishShift': 10,  # HiddenBearish: vertical shift of arrows in pixels
    }

