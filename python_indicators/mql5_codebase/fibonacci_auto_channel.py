"""Fibonacci_auto_channel — converted from MQL5: MQL5 Indicators/Fibonacci Auto Channel/Fibonacci_auto_channel.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'www.forex-tsd.com', 'copyright': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 9}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'colors': {1: [14546909], 2: [14937853], 3: [3329330, 6333684], 4: [3329330, 6333684], 5: [11119017], 6: [11119017], 7: [11119017], 8: [11119017], 9: [11119017]}, 'widths': {3: 3, 4: 3, 5: 2}, 'styles': {6: 2, 7: 2, 8: 2, 9: 2}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Middle value', 6: 'value 0.236', 7: 'value 0.382', 8: 'value 0.618', 9: 'value 0.764'}, 'levels': [], 'description': [], 'name': 'Fibonacci_auto_channel', 'source': 'MQL5 Indicators/Fibonacci Auto Channel/Fibonacci_auto_channel.mq5', 'folder': 'Fibonacci Auto Channel', 'inputs': [{'mql': 'HighLowPeriod', 'py': 'HighLowPeriod', 'param': 'HighLowPeriod', 'type': 'int', 'default': 50, 'label': 'High/low period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HighLowPeriod = _input('HighLowPeriod', 50)  # High/low period
bufferUp = Arr(0, 0.0)
bufferUpc = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferDnc = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
lev1 = Arr(0, 0.0)
lev2 = Arr(0, 0.0)
lev3 = Arr(0, 0.0)
lev4 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferUpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(7, bufferDnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, bufferMe, INDICATOR_DATA)
    SetIndexBuffer(9, lev1, INDICATOR_DATA)
    SetIndexBuffer(10, lev2, INDICATOR_DATA)
    SetIndexBuffer(11, lev3, INDICATOR_DATA)
    SetIndexBuffer(12, lev4, INDICATOR_DATA)
    return 0

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        hh = high[i]
        ll = low[i]
        k = 1
        while k < HighLowPeriod and (i - k) >= 0:
            hh = MathMax(hh, high[i - k])
            ll = MathMin(ll, low[i - k])
            k += 1
        rng = hh - ll
        bufferUp[i] = hh
        bufferDn[i] = ll
        bufferMe[i] = (hh + ll) / 2
        lev1[i] = ll + (0.236 * rng)
        lev2[i] = ll + (0.382 * rng)
        lev3[i] = ll + (0.618 * rng)
        lev4[i] = ll + (0.764 * rng)
        fupd[i] = bufferMe[i]
        fupu[i] = bufferUp[i]
        fdnu[i] = bufferMe[i]
        fdnd[i] = bufferDn[i]
        if i > 0:
            bufferUpc[i] = bufferUpc[i - 1]
            bufferDnc[i] = bufferDnc[i - 1]
            if bufferUp[i] > bufferUp[i - 1]:
                bufferUpc[i] = 0.0
            if bufferUp[i] < bufferUp[i - 1]:
                bufferUpc[i] = 1.0
            if bufferDn[i] > bufferDn[i - 1]:
                bufferDnc[i] = 0.0
            if bufferDn[i] < bufferDn[i - 1]:
                bufferDnc[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FibonacciAutoChannel(_MQL5Indicator):
    name = 'Fibonacci_auto_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HighLowPeriod': 50,  # High/low period
    }

