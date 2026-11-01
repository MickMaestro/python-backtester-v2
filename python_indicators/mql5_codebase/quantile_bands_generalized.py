"""Quantile_bands_-_generalized — converted from MQL5: MQL5 Indicators/Quantile bands - generalized/Quantile_bands_-_generalized.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 8}, 'colors': {1: [13628367], 2: [12052223], 3: [12632256, 3329330, 36095], 4: [12632256, 3329330, 36095], 5: [12632256, 3329330, 36095]}, 'widths': {5: 4}, 'styles': {}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Middle value'}, 'levels': [], 'description': [], 'name': 'Quantile_bands_-_generalized', 'source': 'MQL5 Indicators/Quantile bands - generalized/Quantile_bands_-_generalized.mq5', 'folder': 'Quantile bands - generalized', 'inputs': [{'mql': 'QPeriod', 'py': 'QPeriod', 'param': 'QPeriod', 'type': 'int', 'default': 32, 'label': 'Quantile period', 'sinput': False}, {'mql': 'HLPeriod', 'py': 'HLPeriod', 'param': 'HLPeriod', 'type': 'int', 'default': 1, 'label': 'Period for high/low finding', 'sinput': False}, {'mql': 'UpperBandPercent', 'py': 'UpperBandPercent', 'param': 'UpperBandPercent', 'type': 'double', 'default': 90.0, 'label': 'Upper band percent', 'sinput': False}, {'mql': 'MedianBandPercent', 'py': 'MedianBandPercent', 'param': 'MedianBandPercent', 'type': 'double', 'default': 50.0, 'label': 'Middle band percent', 'sinput': False}, {'mql': 'LowerBandPercent', 'py': 'LowerBandPercent', 'param': 'LowerBandPercent', 'type': 'double', 'default': 10.0, 'label': 'Lower band percent', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
QPeriod = _input('QPeriod', 32)  # Quantile period
HLPeriod = _input('HLPeriod', 1)  # Period for high/low finding
UpperBandPercent = _input('UpperBandPercent', 90.0)  # Upper band percent
MedianBandPercent = _input('MedianBandPercent', 50.0)  # Middle band percent
LowerBandPercent = _input('LowerBandPercent', 10.0)  # Lower band percent
bufferUp = Arr(0, 0.0)
bufferUpc = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferDnc = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
bufferMec = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
quantileValues = Arr(0, 0.0, dims=(3,))
quantileArray = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferUpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(7, bufferDnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, bufferMe, INDICATOR_DATA)
    SetIndexBuffer(9, bufferMec, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Quantile bands (' + _str(QPeriod) + ',' + _str(HLPeriod) + ')')
    return 0

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, begin, price):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        prices = Arr(3, 0.0, dyn=False)
        prices[0] = price[i]
        prices[1] = price[i]
        prices[2] = price[i]
        k = 0
        while k < HLPeriod and (i - k) >= 0:
            prices[0] = MathMax(prices[0], price[i - k])
            prices[1] = MathMin(prices[0], price[i - k])
            k += 1
        ArraySort(prices)
        bufferUp[i] = iQuantile(prices[2], QPeriod, UpperBandPercent, i, rates_total, 0)
        bufferMe[i] = iQuantile(prices[1], QPeriod, MedianBandPercent, i, rates_total, 2)
        bufferDn[i] = iQuantile(prices[0], QPeriod, LowerBandPercent, i, rates_total, 1)
        fupd[i] = bufferMe[i]
        fupu[i] = bufferUp[i]
        fdnu[i] = bufferMe[i]
        fdnd[i] = bufferDn[i]
        bufferUpc[i] = ((1 if (bufferUp[i] > bufferUp[i - 1]) else 2 if (bufferUp[i] < bufferUp[i - 1]) else bufferUpc[i - 1]) if (i > 0) else 0)
        bufferDnc[i] = ((1 if (bufferDn[i] > bufferDn[i - 1]) else 2 if (bufferDn[i] < bufferDn[i - 1]) else bufferDnc[i - 1]) if (i > 0) else 0)
        bufferMec[i] = (1 if (bufferUpc[i] == 1 and bufferDnc[i] == 1) else 2 if (bufferUpc[i] == 2 and bufferDnc[i] == 2) else 0)
    return rates_total

def iQuantile(value, period, qp, i, bars, instanceNo=0):
    if ArrayRange(quantileArray, 0) != period:
        ArrayResize(quantileArray, period)
    if ArrayRange(quantileValues, 0) != bars:
        ArrayResize(quantileValues, bars)
    quantileValues[i][instanceNo] = value
    k = 0
    while k < period and (i - k) >= 0:
        quantileArray[k] = quantileValues[i - k][instanceNo]
        k += 1
    ArraySort(quantileArray)
    index = ((period - 1) * MathMax(MathMin(qp, 100), 0)) / 100.0
    ind = _int(index)
    delta = index - ind
    if ind == NormalizeDouble(index, 5):
        return quantileArray[ind]
    return ((1.0 - delta) * quantileArray[ind]) + (delta * quantileArray[ind + 1])


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class QuantileBandsGeneralized(_MQL5Indicator):
    name = 'Quantile_bands_-_generalized'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'QPeriod': 32,  # Quantile period
        'HLPeriod': 1,  # Period for high/low finding
        'UpperBandPercent': 90.0,  # Upper band percent
        'MedianBandPercent': 50.0,  # Middle band percent
        'LowerBandPercent': 10.0,  # Lower band percent
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

