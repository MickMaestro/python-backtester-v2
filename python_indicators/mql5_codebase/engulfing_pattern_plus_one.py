"""Engulfing Pattern Plus One — converted from MQL5: MQL5 Indicators/Engulfing Pattern Plus One/Engulfing Pattern Plus One.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16760576], 2: [17919]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'BUY', 2: 'SELL'}, 'levels': [], 'description': [], 'name': 'Engulfing Pattern Plus One', 'source': 'MQL5 Indicators/Engulfing Pattern Plus One/Engulfing Pattern Plus One.mq5', 'folder': 'Engulfing Pattern Plus One', 'inputs': [{'mql': 'Inp_BUY_ArrowCode', 'py': 'Inp_BUY_ArrowCode', 'param': 'Inp_BUY_ArrowCode', 'type': 'uchar', 'default': 116, 'label': "Arrow 'BUY': code (font Wingdings)", 'sinput': False}, {'mql': 'Inp_BUY_ArrowShift', 'py': 'Inp_BUY_ArrowShift', 'param': 'Inp_BUY_ArrowShift', 'type': 'int', 'default': 10, 'label': "Arrow 'BUY': vertical shift in pixel", 'sinput': False}, {'mql': 'Inp_SELL_ArrowCode', 'py': 'Inp_SELL_ArrowCode', 'param': 'Inp_SELL_ArrowCode', 'type': 'uchar', 'default': 116, 'label': "Arrow 'SELL': code (font Wingdings)", 'sinput': False}, {'mql': 'Inp_SELL_ArrowShift', 'py': 'Inp_SELL_ArrowShift', 'param': 'Inp_SELL_ArrowShift', 'type': 'int', 'default': 10, 'label': "Arrow 'SELL': vertical shift in pixel", 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_BUY_ArrowCode = _input('Inp_BUY_ArrowCode', 116)  # Arrow 'BUY': code (font Wingdings)
Inp_BUY_ArrowShift = _input('Inp_BUY_ArrowShift', 10)  # Arrow 'BUY': vertical shift in pixel
Inp_SELL_ArrowCode = _input('Inp_SELL_ArrowCode', 116)  # Arrow 'SELL': code (font Wingdings)
Inp_SELL_ArrowShift = _input('Inp_SELL_ArrowShift', 10)  # Arrow 'SELL': vertical shift in pixel
BUYBuffer = Arr(0, 0.0)
SELLBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BUYBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SELLBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, Inp_BUY_ArrowCode)
    PlotIndexSetInteger(1, PLOT_ARROW, Inp_SELL_ArrowCode)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, Inp_BUY_ArrowShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -Inp_SELL_ArrowShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 2
        for i in range(0, limit):
            BUYBuffer[i] = 0.0
            SELLBuffer[i] = 0.0
    for i in range(limit, rates_total):
        BUYBuffer[i] = 0.0
        SELLBuffer[i] = 0.0
        if high[i] >= high[i - 1] and high[i] >= high[i - 2]:
            if low[i] <= low[i - 1] and low[i] <= low[i - 2]:
                if open[i] < close[i]:
                    BUYBuffer[i] = low[i]
                else:
                    SELLBuffer[i] = high[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EngulfingPatternPlusOne(_MQL5Indicator):
    name = 'Engulfing Pattern Plus One'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_BUY_ArrowCode': 116,  # Arrow 'BUY': code (font Wingdings)
        'Inp_BUY_ArrowShift': 10,  # Arrow 'BUY': vertical shift in pixel
        'Inp_SELL_ArrowCode': 116,  # Arrow 'SELL': code (font Wingdings)
        'Inp_SELL_ArrowShift': 10,  # Arrow 'SELL': vertical shift in pixel
    }

