"""Six_Continuation — converted from MQL5: MQL5 Indicators/Six Soldiers/Six_Continuation.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16448255], 2: [16448255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '+SS', 2: '-SS'}, 'levels': [], 'description': [], 'name': 'Six_Continuation', 'source': 'MQL5 Indicators/Six Soldiers/Six_Continuation.mq5', 'folder': 'Six Soldiers', 'inputs': [{'mql': 'SelectMode', 'py': 'SelectMode', 'param': 'SelectMode', 'type': 'int', 'default': 0, 'label': 'Search Mode', 'sinput': False}, {'mql': 'InpSSBullishCode', 'py': 'InpSSBullishCode', 'param': 'InpSSBullishCode', 'type': 'uchar', 'default': 233, 'label': 'SSBullish: code for style DRAW_ARROW (font Wingdings)', 'sinput': False}, {'mql': 'InpSSBullishShift', 'py': 'InpSSBullishShift', 'param': 'InpSSBullishShift', 'type': 'int', 'default': 10, 'label': 'SSBullish: vertical shift of arrows in pixels', 'sinput': False}, {'mql': 'InpSSBearishCode', 'py': 'InpSSBearishCode', 'param': 'InpSSBearishCode', 'type': 'uchar', 'default': 234, 'label': 'SSBearish: code for style DRAW_ARROW (font Wingdings)', 'sinput': False}, {'mql': 'InpSSBearishShift', 'py': 'InpSSBearishShift', 'param': 'InpSSBearishShift', 'type': 'int', 'default': 10, 'label': 'SSBearish: vertical shift of arrows in pixels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum mode
Two = 0
Three = 1
_enum('mode', {0: 'Two', 1: 'Three'})

# ---- inputs and global variables
SelectMode = _input('SelectMode', Two)  # Search Mode
InpSSBullishCode = _input('InpSSBullishCode', 233)  # SSBullish: code for style DRAW_ARROW (font Wingdings)
InpSSBullishShift = _input('InpSSBullishShift', 10)  # SSBullish: vertical shift of arrows in pixels
InpSSBearishCode = _input('InpSSBearishCode', 234)  # SSBearish: code for style DRAW_ARROW (font Wingdings)
InpSSBearishShift = _input('InpSSBearishShift', 10)  # SSBearish: vertical shift of arrows in pixels
SSBullishBuffer = Arr(0, 0.0)
SSBearishBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 6
    SetIndexBuffer(0, SSBullishBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SSBearishBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_ARROW, InpSSBullishCode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpSSBearishCode)
    ArraySetAsSeries(SSBullishBuffer, True)
    ArraySetAsSeries(SSBearishBuffer, True)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, InpSSBullishShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -InpSSBearishShift)
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
        SSBullishBuffer[i] = 0.0
        SSBearishBuffer[i] = 0.0
        SSBearishBuffer[0] = 0.0
        if ((((open[i + 5] > close[i + 5] and open[i + 4] > close[i + 4]) and open[i + 3] > close[i + 3]) and open[i + 2] > close[i + 2]) and open[i + 1] > close[i + 1]) and open[i] > close[i]:
            SSBearishBuffer[i] = high[i]
        SSBullishBuffer[0] = 0.0
        if ((((open[i + 5] < close[i + 5] and open[i + 4] < close[i + 4]) and open[i + 3] < close[i + 3]) and open[i + 2] < close[i + 2]) and open[i + 1] < close[i + 1]) and open[i] < close[i]:
            SSBullishBuffer[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SixContinuation(_MQL5Indicator):
    name = 'Six_Continuation'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SelectMode': _Choice({0: 'Two Candle Breaks', 1: 'Three Candle Breaks'}, default=0),  # Search Mode
        'InpSSBullishCode': 233,  # SSBullish: code for style DRAW_ARROW (font Wingdings)
        'InpSSBullishShift': 10,  # SSBullish: vertical shift of arrows in pixels
        'InpSSBearishCode': 234,  # SSBearish: code for style DRAW_ARROW (font Wingdings)
        'InpSSBearishShift': 10,  # SSBearish: vertical shift of arrows in pixels
    }

