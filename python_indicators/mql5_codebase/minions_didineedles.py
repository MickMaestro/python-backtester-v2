"""Minions.DidiNeedles — converted from MQL5: MQL5 Indicators/Didi Needles - with MA Threshold Diff Filtering/Minions.DidiNeedles.mq5

Minions in the quest Didi Needles
 
(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
Copyright: www.MinionsLabs.com; Link: http://www.MinionsLabs.com; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.MinionsLabs.com', 'link': 'http://www.MinionsLabs.com', 'version': '1.1', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 1, 4: 1, 5: 1, 6: 0}, 'colors': {1: [16748574], 2: [255], 3: [255], 4: [65535], 5: [16711680]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2, 5: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Buy', 2: 'Sell', 3: 'Fast MA', 4: 'Medium MA', 5: 'Slow MA', 6: 'Diff Fast/Slow (%)'}, 'levels': [], 'description': ['Minions in the quest Didi Needles', ' ', '(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'], 'name': 'Minions.DidiNeedles', 'source': 'MQL5 Indicators/Didi Needles - with MA Threshold Diff Filtering/Minions.DidiNeedles.mq5', 'folder': 'Didi Needles - with MA Threshold Diff Filtering', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 3, 'label': 'Fast MA Period', 'sinput': False}, {'mql': 'inpMediumPeriod', 'py': 'inpMediumPeriod', 'param': 'inpMediumPeriod', 'type': 'int', 'default': 8, 'label': 'Medium MA Period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 20, 'label': 'Slow MA Period', 'sinput': False}, {'mql': 'inpMethod', 'py': 'inpMethod', 'param': 'inpMethod', 'type': 'int', 'default': 1, 'label': 'Smoothing Method', 'sinput': False}, {'mql': 'inpAppliedPrice', 'py': 'inpAppliedPrice', 'param': 'inpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'MA Price used', 'sinput': False}, {'mql': 'inpThreshold', 'py': 'inpThreshold', 'param': 'inpThreshold', 'type': 'double', 'default': 0.0, 'label': 'Threshold to Filter Entries', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 3)  # Fast MA Period
inpMediumPeriod = _input('inpMediumPeriod', 8)  # Medium MA Period
inpSlowPeriod = _input('inpSlowPeriod', 20)  # Slow MA Period
inpMethod = _input('inpMethod', MODE_EMA)  # Smoothing Method
inpAppliedPrice = _input('inpAppliedPrice', PRICE_CLOSE)  # MA Price used
inpThreshold = _input('inpThreshold', 0.0)  # Threshold to Filter Entries
bufferBuy_ID = 0  # put names on buffers!
bufferSell_ID = 1
bufferFast_ID = 2
bufferMedium_ID = 3
bufferSlow_ID = 4
bufferDiff_ID = 5
bufferBuy = Arr(0, 0.0)  # Data/Plot buffers
bufferSell = Arr(0, 0.0)
bufferFast = Arr(0, 0.0)
bufferMedium = Arr(0, 0.0)
bufferSlow = Arr(0, 0.0)
bufferDiff = Arr(0, 0.0)
hFast = 0  # MAs indicators handles
hMedium = 0
hSlow = 0
barsCalculated = 0  # we will keep the number of values in the Moving Average indicator

def OnInit():
    global hFast, hMedium, hSlow
    plotStart = 0
    SetIndexBuffer(bufferBuy_ID, bufferBuy, INDICATOR_DATA)
    SetIndexBuffer(bufferSell_ID, bufferSell, INDICATOR_DATA)
    SetIndexBuffer(bufferFast_ID, bufferFast, INDICATOR_DATA)
    SetIndexBuffer(bufferMedium_ID, bufferMedium, INDICATOR_DATA)
    SetIndexBuffer(bufferSlow_ID, bufferSlow, INDICATOR_DATA)
    SetIndexBuffer(bufferDiff_ID, bufferDiff, INDICATOR_DATA)
    PlotIndexSetInteger(bufferSell_ID, PLOT_ARROW, 234)
    PlotIndexSetInteger(bufferBuy_ID, PLOT_ARROW, 233)
    PlotIndexSetInteger(bufferSell_ID, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(bufferBuy_ID, PLOT_ARROW_SHIFT, 10)
    plotStart = MathMax(inpFastPeriod, MathMax(inpMediumPeriod, inpSlowPeriod))
    PlotIndexSetInteger(bufferFast_ID, PLOT_DRAW_BEGIN, plotStart)
    PlotIndexSetInteger(bufferMedium_ID, PLOT_DRAW_BEGIN, plotStart)
    PlotIndexSetInteger(bufferSlow_ID, PLOT_DRAW_BEGIN, plotStart)
    hFast = iMA(Symbol(), Period(), inpFastPeriod, 0, inpMethod, inpAppliedPrice)
    hMedium = iMA(Symbol(), Period(), inpMediumPeriod, 0, inpMethod, inpAppliedPrice)
    hSlow = iMA(Symbol(), Period(), inpSlowPeriod, 0, inpMethod, inpAppliedPrice)
    if (hFast == INVALID_HANDLE or hMedium == INVALID_HANDLE) or hSlow == INVALID_HANDLE:
        Print('Error starting MA indicators!')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global barsCalculated
    values_to_copy = 0
    i = 0
    calculated = BarsCalculated(hFast)
    if calculated <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != barsCalculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(hFast, 0, values_to_copy, bufferFast):
        return 0
    if not FillArrayFromBuffer(hMedium, 0, values_to_copy, bufferMedium):
        return 0
    if not FillArrayFromBuffer(hSlow, 0, values_to_copy, bufferSlow):
        return 0
    barsCalculated = calculated
    i = MathMax(1, values_to_copy - 1)
    for i in range(i, rates_total):
        bufferDiff[i] = MathAbs((_fdiv(bufferFast[i], bufferSlow[i]) - 1) * 100)
        if ((((bufferFast[i] > bufferFast[i - 1] and bufferMedium[i] > bufferMedium[i - 1]) and bufferSlow[i] > bufferSlow[i - 1]) and ((bufferFast[i] > bufferMedium[i] and bufferFast[i] > bufferSlow[i]) and bufferMedium[i] > bufferSlow[i])) and (((((bufferFast[i] >= open[i] and bufferFast[i] <= close[i]) and bufferMedium[i] >= open[i]) and bufferMedium[i] <= close[i]) and bufferSlow[i] >= open[i]) and bufferSlow[i] <= close[i])) and bufferDiff[i] >= inpThreshold:
            bufferBuy[i] = low[i]
            bufferSell[i] = EMPTY_VALUE
        elif ((((bufferFast[i] < bufferFast[i - 1] and bufferMedium[i] < bufferMedium[i - 1]) and bufferSlow[i] < bufferSlow[i - 1]) and ((bufferFast[i] < bufferMedium[i] and bufferFast[i] < bufferSlow[i]) and bufferMedium[i] < bufferSlow[i])) and (((((bufferFast[i] <= open[i] and bufferFast[i] >= close[i]) and bufferMedium[i] <= open[i]) and bufferMedium[i] >= close[i]) and bufferSlow[i] <= open[i]) and bufferSlow[i] >= close[i])) and bufferDiff[i] >= inpThreshold:
            bufferSell[i] = high[i]
            bufferBuy[i] = EMPTY_VALUE
        else:
            bufferSell[i] = EMPTY_VALUE
            bufferBuy[i] = bufferSell[i]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def FillArrayFromBuffer(indicatorHandle, indicatorInternalBuffer, itemsQty, bufferToCopyInto):
    ResetLastError()
    if CopyBuffer(indicatorHandle, indicatorInternalBuffer, 0, itemsQty, bufferToCopyInto) < 0:
        Print('Failed to copy data from the Indicator. Error Code:', GetLastError())
        return False
    return True

def OnDeinit(reason):
    IndicatorRelease(hFast)
    IndicatorRelease(hMedium)
    IndicatorRelease(hSlow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MinionsDidiNeedles(_MQL5Indicator):
    name = 'Minions.DidiNeedles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpFastPeriod': 3,  # Fast MA Period
        'inpMediumPeriod': 8,  # Medium MA Period
        'inpSlowPeriod': 20,  # Slow MA Period
        'inpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing Method
        'inpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Price used
        'inpThreshold': 0.0,  # Threshold to Filter Entries
    }

