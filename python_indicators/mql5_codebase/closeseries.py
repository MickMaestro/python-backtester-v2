"""closeseries — converted from MQL5: MQL5 Indicators/CloseSeries/closeseries.mq5

The indicator shows the series of internal, external and unidirectional closures.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [6908265], 2: [14822282], 3: [16748574]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'In Close', 2: 'Out Close', 3: 'Direct Close'}, 'levels': [0.0, 3.0, -3.0], 'description': ['The indicator shows the series of internal, external and unidirectional closures.'], 'name': 'closeseries', 'source': 'MQL5 Indicators/CloseSeries/closeseries.mq5', 'folder': 'CloseSeries', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InCloseBuffer = Arr(0, 0.0)
OutCloseBuffer = Arr(0, 0.0)
DirectCloseBuffer = Arr(0, 0.0)
minRequiredBars = 0

def OnInit():
    global minRequiredBars
    minRequiredBars = 1
    SetIndexBuffer(0, InCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, OutCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, DirectCloseBuffer, INDICATOR_DATA)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Close Series')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    startBar = 0
    if rates_total < minRequiredBars:
        Print('Not enough bars for the calculation.')
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        startBar = minRequiredBars
        for bar in range(0, minRequiredBars):
            InCloseBuffer[bar] = 0.0
            OutCloseBuffer[bar] = 0.0
            DirectCloseBuffer[bar] = 0.0
    else:
        startBar = prev_calculated - 1
    for bar in range(startBar, rates_total):
        prevBar = bar - 1
        if close[bar] <= high[prevBar] and close[bar] >= low[prevBar]:
            if InCloseBuffer[prevBar] > 0:
                InCloseBuffer[bar] = InCloseBuffer[prevBar] + 1
            else:
                InCloseBuffer[bar] = 1.0
        else:
            InCloseBuffer[bar] = 0.0
        if close[bar] > high[prevBar]:
            if OutCloseBuffer[prevBar] > 0:
                OutCloseBuffer[bar] = OutCloseBuffer[prevBar] + 1
            else:
                OutCloseBuffer[bar] = 1.0
        elif close[bar] < low[prevBar]:
            if OutCloseBuffer[prevBar] < 0:
                OutCloseBuffer[bar] = OutCloseBuffer[prevBar] - 1
            else:
                OutCloseBuffer[bar] = -1.0
        else:
            OutCloseBuffer[bar] = 0.0
        if close[bar] > open[bar]:
            if DirectCloseBuffer[prevBar] > 0:
                DirectCloseBuffer[bar] = DirectCloseBuffer[prevBar] + 1
            else:
                DirectCloseBuffer[bar] = 1.0
        elif close[bar] < open[bar]:
            if DirectCloseBuffer[prevBar] < 0:
                DirectCloseBuffer[bar] = DirectCloseBuffer[prevBar] - 1
            else:
                DirectCloseBuffer[bar] = -1.0
        else:
            DirectCloseBuffer[bar] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Closeseries(_MQL5Indicator):
    name = 'closeseries'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

