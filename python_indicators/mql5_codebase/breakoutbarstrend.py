"""breakoutbarstrend — converted from MQL5: MQL5 Indicators/Breakout Bars Trend/breakoutbarstrend.mq5

Indicator to determine the trend, based on the breakdown of bars and the distance from the extremums.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 0, 2: 17}, 'colors': {1: [4294967295], 2: [16711680, 14772545, 16760576, 255, 4678655, 42495]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Series Values', 2: 'Breakout Open;Breakout High;Breakout Low;Breakout Close'}, 'levels': [], 'description': ['Indicator to determine the trend, based on the breakdown of bars and the distance from the extremums.'], 'name': 'breakoutbarstrend', 'source': 'MQL5 Indicators/Breakout Bars Trend/breakoutbarstrend.mq5', 'folder': 'Breakout Bars Trend', 'inputs': [{'mql': 'InpDelta', 'py': 'InpDelta', 'param': 'InpDelta', 'type': 'int', 'default': 1000, 'label': 'Delta', 'sinput': False}, {'mql': 'InpShowLastValues', 'py': 'InpShowLastValues', 'param': 'InpShowLastValues', 'type': 'bool', 'default': True, 'label': 'Show the size of the series', 'sinput': False}, {'mql': 'InpSeriesQuantity', 'py': 'InpSeriesQuantity', 'param': 'InpSeriesQuantity', 'type': 'int', 'default': 5, 'label': 'Number of series', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpDelta = _input('InpDelta', 1000)  # Delta
InpShowLastValues = _input('InpShowLastValues', True)  # Show the size of the series
InpSeriesQuantity = _input('InpSeriesQuantity', 5)  # Number of series
SeriesBuffer = Arr(0, 0.0)
OpenBreakoutBuffer = Arr(0, 0.0)
HighBreakoutBuffer = Arr(0, 0.0)
LowBreakoutBuffer = Arr(0, 0.0)
CloseBreakoutBuffer = Arr(0, 0.0)
BreakoutColors = Arr(0, 0.0)
minRequiredBars = 0
delta = 0.0
maxPrice = 0.0
minPrice = 0.0
seriesData = Arr(0, 0)

def OnInit():
    global delta, minRequiredBars
    minRequiredBars = 2
    delta = InpDelta * Point()
    SetIndexBuffer(0, SeriesBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, OpenBreakoutBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, HighBreakoutBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, LowBreakoutBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, CloseBreakoutBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, BreakoutColors, INDICATOR_COLOR_INDEX)
    for i in range(0, 2):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'BreakoutBarsTrend (' + _str(InpDelta) + ')')
    if InpShowLastValues:
        ArrayResize(seriesData, InpSeriesQuantity)
        ArrayInitialize(seriesData, 0)
    return 0

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global maxPrice, minPrice
    startBar = 0
    if rates_total < minRequiredBars:
        Print('Not enough data for the calculation')
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        startBar = minRequiredBars
        for bar in range(0, minRequiredBars):
            SeriesBuffer[bar] = 0.0
            OpenBreakoutBuffer[bar] = 0.0
            HighBreakoutBuffer[bar] = 0.0
            LowBreakoutBuffer[bar] = 0.0
            CloseBreakoutBuffer[bar] = 0.0
    else:
        startBar = prev_calculated - 1
    for bar in range(startBar, rates_total):
        prevBar = bar - 1
        seriesValue = 0.0
        if prev_calculated != rates_total:
            if (SeriesBuffer[prevBar] * SeriesBuffer[prevBar - 1]) < 0:
                maxPrice = high[prevBar]
                minPrice = low[prevBar]
                if InpShowLastValues:
                    arrayShift(seriesData, _int(SeriesBuffer[prevBar - 1]))
            else:
                maxPrice = MathMax(maxPrice, high[prevBar])
                minPrice = MathMin(minPrice, low[prevBar])
        SeriesBuffer[bar] = SeriesBuffer[prevBar]
        seriesValue = SeriesBuffer[bar]
        OpenBreakoutBuffer[bar] = open[bar]
        HighBreakoutBuffer[bar] = high[bar]
        LowBreakoutBuffer[bar] = low[bar]
        CloseBreakoutBuffer[bar] = close[bar]
        if seriesValue > 0.0:
            if close[bar] > maxPrice:
                BreakoutColors[bar] = 0.0
                SeriesBuffer[bar] = SeriesBuffer[prevBar] + 1
            elif close[bar] < (MathMax(maxPrice, high[bar]) - delta) and close[bar] < low[prevBar]:
                SeriesBuffer[bar] = -1.0
                BreakoutColors[bar] = 3.0
                maxPrice = high[bar]
            else:
                if close[bar] >= open[bar]:
                    BreakoutColors[bar] = 1.0
                else:
                    BreakoutColors[bar] = 2.0
        elif seriesValue < 0.0:
            if close[bar] < minPrice:
                BreakoutColors[bar] = 3.0
                SeriesBuffer[bar] = SeriesBuffer[prevBar] - 1
            elif close[bar] > (MathMin(minPrice, low[bar]) + delta) and close[bar] > high[prevBar]:
                SeriesBuffer[bar] = 1.0
                BreakoutColors[bar] = 0.0
                minPrice = low[bar]
            else:
                if close[bar] >= open[bar]:
                    BreakoutColors[bar] = 5.0
                else:
                    BreakoutColors[bar] = 4.0
        elif seriesValue == 0.0:
            if close[bar] >= close[prevBar]:
                SeriesBuffer[bar] = 1.0
            else:
                SeriesBuffer[bar] = -1.0
            maxPrice = high[bar]
            minPrice = low[bar]
    if InpShowLastValues:
        comm = 'Series Values: '
        seriesData[InpSeriesQuantity - 1] = _int(SeriesBuffer[rates_total - 1])
        for i in range(0, InpSeriesQuantity):
            comm += _str(seriesData[i]) + ' '
        Comment(comm)
    return rates_total

def arrayShift(array, newValue):
    last = InpSeriesQuantity - 2
    for i in range(0, last):
        array[i] = array[i + 1]
    array[last] = newValue


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Breakoutbarstrend(_MQL5Indicator):
    name = 'breakoutbarstrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDelta': 1000,  # Delta
        'InpShowLastValues': True,  # Show the size of the series
        'InpSeriesQuantity': 5,  # Number of series
    }

