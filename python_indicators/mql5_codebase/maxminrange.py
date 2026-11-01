"""maxminrange — converted from MQL5: MQL5 Indicators/MaxMinRange/maxminrange.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [16711935, 65280, 16748574], 2: [16711935, 255, 16748574]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MaxRange', 2: 'MinRange'}, 'levels': [0.0], 'description': [], 'name': 'maxminrange', 'source': 'MQL5 Indicators/MaxMinRange/maxminrange.mq5', 'folder': 'MaxMinRange', 'inputs': [{'mql': 'GreenLimit', 'py': 'GreenLimit', 'param': 'GreenLimit', 'type': 'uint', 'default': 75, 'label': 'limit for green bars in histogram', 'sinput': False}, {'mql': 'DarkGreenLimitOffset', 'py': 'DarkGreenLimitOffset', 'param': 'DarkGreenLimitOffset', 'type': 'uint', 'default': 30, 'label': 'Offsetlimit from GreenLimit for darkgreen bars in histogram', 'sinput': False}, {'mql': 'NumbOfBars', 'py': 'NumbOfBars', 'param': 'NumbOfBars', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
GreenLimit = _input('GreenLimit', 75)  # limit for green bars in histogram
DarkGreenLimitOffset = _input('DarkGreenLimitOffset', 30)  # Offsetlimit from GreenLimit for darkgreen bars in histogram
NumbOfBars = _input('NumbOfBars', 15)
min_rates_total = 0
MaxBuffer = Arr(0, 0.0)
ColorMaxBuffer = Arr(0, 0.0)
MinBuffer = Arr(0, 0.0)
ColorMinBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(NumbOfBars)
    SetIndexBuffer(0, MaxBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorMaxBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, MinBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, ColorMinBuffer, INDICATOR_COLOR_INDEX)
    short_name = 'MaxMinRange(' + _str(NumbOfBars) + ',' + _str(GreenLimit)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    nMax = 0.0
    nMin = 0.0
    nVal = 0.0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        nMax = -999999.0
        nMin = 999999.0
        MaxBuffer[bar] = 0.0
        MinBuffer[bar] = 0.0
        for kkk in range(0, _int(NumbOfBars)):
            nVal = high[bar] - low[bar - kkk]
            if nVal > nMax:
                nMax = nVal
            nVal = low[bar] - high[bar - kkk]
            if nVal < nMin:
                nMin = nVal
        if nMax > 0.0:
            MaxBuffer[bar] = _fdiv(nMax, Point())
            if (10000.0 * nMax) < GreenLimit:
                clr = 0
            elif (10000.0 * nMax) < (GreenLimit + DarkGreenLimitOffset):
                clr = 2
            else:
                clr = 1
            ColorMaxBuffer[bar] = clr
        if nMin < 0.0:
            MinBuffer[bar] = _fdiv(nMin, Point())
            if (10000.0 * nMin) > (-GreenLimit):
                clr = 0
            elif (10000.0 * nMin) > ((-GreenLimit) - DarkGreenLimitOffset):
                clr = 2
            else:
                clr = 1
            ColorMinBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Maxminrange(_MQL5Indicator):
    name = 'maxminrange'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'GreenLimit': 75,  # limit for green bars in histogram
        'DarkGreenLimitOffset': 30,  # Offsetlimit from GreenLimit for darkgreen bars in histogram
        'NumbOfBars': 15,
    }

