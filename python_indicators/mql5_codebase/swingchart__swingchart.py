"""SwingChart — converted from MQL5: MQL5 Indicators/Swingchart/SwingChart.mq5

Gann swingchart and hybrid ZigZag implementation.
Copyright: Copyright 2016, Andre S. Enger.; Link: andre_enger@hotmail.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, Andre S. Enger.', 'link': 'andre_enger@hotmail.com', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 6, 2: 17}, 'colors': {1: [55295], 2: [255, 8421504, 16711680, 32768]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Zig Zag', 2: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Gann swingchart and hybrid ZigZag implementation.'], 'name': 'SwingChart', 'source': 'MQL5 Indicators/Swingchart/SwingChart.mq5', 'folder': 'Swingchart', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtPeaksBuffer = Arr(0, 0.0)
ExtTroughsBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
lastDirection = False
lastIndex = 0

def OnInit():
    SetIndexBuffer(0, ExtPeaksBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTroughsBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global lastDirection, lastIndex
    start = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        start = 0
        lastIndex = 0
    else:
        start = prev_calculated - 1
    start = MathMax(1, start)
    for bar in range(start, rates_total - 1):
        upDay = low[bar - 1] <= low[bar] and high[bar - 1] < high[bar]
        downDay = low[bar - 1] > low[bar] and high[bar - 1] >= high[bar]
        insideDay = low[bar - 1] <= low[bar] and high[bar - 1] >= high[bar]
        outsideDay = low[bar - 1] > low[bar] and high[bar - 1] < high[bar]
        goingUp = close[bar] > open[bar]
        ExtOpenBuffer[bar] = open[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        ExtCloseBuffer[bar] = close[bar]
        if downDay:
            ExtColorBuffer[bar] = 0.0
        elif insideDay:
            ExtColorBuffer[bar] = 1.0
        elif outsideDay:
            ExtColorBuffer[bar] = 2.0
        elif upDay:
            ExtColorBuffer[bar] = 3.0
        ExtPeaksBuffer[bar] = 0.0
        ExtTroughsBuffer[bar] = 0.0
        if lastDirection:
            if high[bar] > high[lastIndex]:
                ExtPeaksBuffer[lastIndex] = 0.0
                ExtPeaksBuffer[bar] = high[bar]
                if outsideDay:
                    ExtTroughsBuffer[bar] = low[bar]
                    if goingUp:
                        ExtPeaksBuffer[lastIndex] = high[lastIndex]
                        ResolveUncertainityBull(bar, lastIndex, False, open, high, low, close)
                    else:
                        lastDirection = False
                lastIndex = bar
            elif downDay:
                ResolveUncertainityBull(bar, lastIndex, False, open, high, low, close)
                ExtTroughsBuffer[bar] = low[bar]
                lastDirection = False
                lastIndex = bar
            elif outsideDay:
                ExtPeaksBuffer[bar] = high[bar]
                ExtTroughsBuffer[bar] = low[bar]
                if goingUp:
                    ResolveUncertainityBull(bar, lastIndex, False, open, high, low, close)
                elif not goingUp:
                    ResolveUncertainityBull(bar, lastIndex, True, open, high, low, close)
                    lastDirection = False
                lastIndex = bar
        else:
            if low[bar] < low[lastIndex]:
                ExtTroughsBuffer[lastIndex] = 0.0
                ExtTroughsBuffer[bar] = low[bar]
                if outsideDay:
                    ExtPeaksBuffer[bar] = high[bar]
                    if not goingUp:
                        ExtTroughsBuffer[lastIndex] = low[lastIndex]
                        ResolveUncertainityBear(bar, lastIndex, False, open, high, low, close)
                    else:
                        lastDirection = True
                lastIndex = bar
            elif upDay:
                ResolveUncertainityBear(bar, lastIndex, False, open, high, low, close)
                ExtPeaksBuffer[bar] = high[bar]
                lastDirection = True
                lastIndex = bar
            elif outsideDay:
                ExtPeaksBuffer[bar] = high[bar]
                ExtTroughsBuffer[bar] = low[bar]
                if not goingUp:
                    ResolveUncertainityBear(bar, lastIndex, False, open, high, low, close)
                else:
                    ResolveUncertainityBear(bar, lastIndex, True, open, high, low, close)
                    lastDirection = True
                lastIndex = bar
    ExtPeaksBuffer[rates_total - 1] = 0.0
    ExtTroughsBuffer[rates_total - 1] = 0.0
    return rates_total

def ResolveUncertainityBull(bar, index, tweaked, open, high, low, close):
    startSkip = (0 if (ExtTroughsBuffer[index] == 0) else 1)
    if open[index] < close[index] and startSkip == 0:
        startSkip += 1
    minimal = ArrayMinimum(low, index + startSkip, bar - index - startSkip + (0 if tweaked else 1))
    while minimal != -1 and minimal < bar:
        ExtTroughsBuffer[minimal] = low[minimal]
        maxSkip = (0 if (ExtPeaksBuffer[minimal] == 0) else 1)
        if open[minimal] > close[minimal] and maxSkip == 0:
            maxSkip += 1
        maximal = ArrayMaximum(high, minimal + maxSkip, bar - minimal - maxSkip + (1 if tweaked else 0))
        if maximal == -1 or (tweaked and maximal >= bar):
            break
        ExtPeaksBuffer[maximal] = high[maximal]
        minSkip = (0 if (ExtTroughsBuffer[maximal] == 0) else 1)
        if open[maximal] < close[maximal] and minSkip == 0:
            minSkip += 1
        minimal = ArrayMinimum(low, maximal + minSkip, bar - maximal - minSkip + (0 if tweaked else 1))

def ResolveUncertainityBear(bar, index, tweaked, open, high, low, close):
    startSkip = (0 if (ExtPeaksBuffer[index] == 0) else 1)
    if open[index] > close[index] and startSkip == 0:
        startSkip += 1
    maximal = ArrayMaximum(high, index + startSkip, bar - index - startSkip + (0 if tweaked else 1))
    while maximal != -1 and maximal < bar:
        ExtPeaksBuffer[maximal] = high[maximal]
        minSkip = (0 if (ExtTroughsBuffer[maximal] == 0) else 1)
        if open[maximal] < close[maximal] and minSkip == 0:
            minSkip += 1
        minimal = ArrayMinimum(low, maximal + minSkip, bar - maximal - minSkip + (1 if tweaked else 0))
        if minimal == -1 or (tweaked and minimal == bar):
            break
        ExtTroughsBuffer[minimal] = low[minimal]
        maxSkip = (0 if (ExtPeaksBuffer[minimal] == 0) else 1)
        if open[minimal] > close[minimal] and maxSkip == 0:
            maxSkip += 1
        maximal = ArrayMaximum(high, minimal + maxSkip, bar - minimal - maxSkip + (0 if tweaked else 1))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SwingChart(_MQL5Indicator):
    name = 'SwingChart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

