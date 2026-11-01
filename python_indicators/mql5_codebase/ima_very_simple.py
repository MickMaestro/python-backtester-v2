"""Ima Very Simple — converted from MQL5: MQL5 Indicators/Ima() very simply/Ima Very Simple.mq5

Ima() very simply.\\nA multi timeframe version is available for developers or profitable traders for free under conditions
Copyright: Copyright 2024, GwDs; Link: https://www.mql5.com/fr/users/william210; Version: 1.04

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, GwDs', 'link': 'https://www.mql5.com/fr/users/william210', 'version': '1.04', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Moving average'}, 'levels': [], 'description': ['Ima() very simply.\\nA multi timeframe version is available for developers or profitable traders for free under conditions'], 'name': 'Ima Very Simple', 'source': 'MQL5 Indicators/Ima() very simply/Ima Very Simple.mq5', 'folder': 'Ima() very simply', 'inputs': [{'mql': 'g_MAPeriod', 'py': 'g_MAPeriod', 'param': 'g_MAPeriod', 'type': 'uchar', 'default': 20, 'label': 'Averaging period', 'sinput': False}, {'mql': 'g_MAShift', 'py': 'g_MAShift', 'param': 'g_MAShift', 'type': 'uchar', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'g_MAMethod', 'py': 'g_MAMethod', 'param': 'g_MAMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'g_MAApplied', 'py': 'g_MAApplied', 'param': 'g_MAApplied', 'type': 'int', 'default': 1, 'label': 'Type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_MAPeriod = _input('g_MAPeriod', 20)  # Averaging period
g_MAShift = _input('g_MAShift', 0)  # Horizontal shift
g_MAMethod = _input('g_MAMethod', MODE_SMA)  # Smoothing type
g_MAApplied = _input('g_MAApplied', PRICE_CLOSE)  # Type of price
g_PtMA = INVALID_HANDLE  # Pointer of the iMA function
g_BufferMA = Arr(0, 0.0)  # Data buffer

def OnInit():
    global g_PtMA
    g_PtMA = iMA(Symbol(), Period(), g_MAPeriod, g_MAShift, g_MAMethod, g_MAApplied)
    if g_PtMA == INVALID_HANDLE:
        PrintFormat('%s: Error %d when creating iMA pointer', 'OnInit', GetLastError())
        return INIT_FAILED
    if not SetIndexBuffer(0, g_BufferMA, INDICATOR_DATA):
        PrintFormat('%s: Error %d SetIndexBuffer( g_BufferMA)', 'OnInit', GetLastError())
    if not PlotIndexSetInteger(0, PLOT_SHIFT, g_MAShift):
        PrintFormat('%s: Error %d PlotIndexSetInteger( g_indexiMA)', 'OnInit', GetLastError())
    if ArrayInitialize(g_BufferMA, EMPTY_VALUE) == -1:
        PrintFormat('%s: Error %d ArrayInitialize(g_BufferMA)', 'OnInit', GetLastError())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i_Diff = rates_total - prev_calculated + 1
    if CopyBuffer(g_PtMA, 0, -g_MAShift, i_Diff, g_BufferMA) < 0:
        PrintFormat('%s: Error %n in data recovery', 'OnCalculate', GetLastError())
        return 0
    return rates_total

def OnDeinit(reason):
    global g_PtMA
    Comment('')
    if g_PtMA != INVALID_HANDLE:
        Comment('')
        IndicatorRelease(g_PtMA)
        g_PtMA = INVALID_HANDLE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ImaVerySimple(_MQL5Indicator):
    name = 'Ima Very Simple'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_MAPeriod': 20,  # Averaging period
        'g_MAShift': 0,  # Horizontal shift
        'g_MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing type
        'g_MAApplied': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Type of price
    }

