"""MovingAverages.mqh Part I — converted from MQL5: MQL5 Indicators/MovingAverages.mqh Part I/MovingAverages.mqh Part I.mq5

MovingAverages.mqh very simply.\\nA multi timeframe version is available for developers or profitable traders for free under conditions
Copyright: Copyright 2024, GwDs; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2024, GwDs', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Moving average'}, 'levels': [], 'description': ['MovingAverages.mqh very simply.\\nA multi timeframe version is available for developers or profitable traders for free under conditions'], 'name': 'MovingAverages.mqh Part I', 'source': 'MQL5 Indicators/MovingAverages.mqh Part I/MovingAverages.mqh Part I.mq5', 'folder': 'MovingAverages.mqh Part I', 'inputs': [{'mql': 'g_MAPeriod', 'py': 'g_MAPeriod', 'param': 'g_MAPeriod', 'type': 'uchar', 'default': 20, 'label': 'Averaging period', 'sinput': False}, {'mql': 'g_MAShift', 'py': 'g_MAShift', 'param': 'g_MAShift', 'type': 'uchar', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'g_MAMethod', 'py': 'g_MAMethod', 'param': 'g_MAMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'g_MAApplied', 'py': 'g_MAApplied', 'param': 'g_MAApplied', 'type': 'int', 'default': 3, 'label': 'Type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum g_PriceType
PRICE_H = 0
PRICE_O = 1
PRICE_L = 2
PRICE_C = 3
_enum('g_PriceType', {0: 'PRICE_H', 1: 'PRICE_O', 2: 'PRICE_L', 3: 'PRICE_C'})

# ---- inputs and global variables
g_MAPeriod = _input('g_MAPeriod', 20)  # Averaging period
g_MAShift = _input('g_MAShift', 0)  # Horizontal shift
g_MAMethod = _input('g_MAMethod', MODE_SMA)  # Smoothing type
g_MAApplied = _input('g_MAApplied', 3)  # Type of price
g_PtMA = INVALID_HANDLE  # Pointer of the iMA function
g_BufferMA = Arr(0, 0.0)  # Data buffer

def OnInit():
    if not SetIndexBuffer(0, g_BufferMA, INDICATOR_DATA):
        PrintFormat('%s: Error %d SetIndexBuffer( g_BufferMA)', 'OnInit', GetLastError())
    if not PlotIndexSetInteger(0, PLOT_SHIFT, g_MAShift):
        PrintFormat('%s: Error %d PlotIndexSetInteger( g_indexiMA)', 'OnInit', GetLastError())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    i_Diff = 0
    i_Price = Arr(0, 0.0)
    i_Start = 0
    if prev_calculated == 0:
        i_Start = g_MAPeriod - 1
        ArrayInitialize(g_BufferMA, EMPTY_VALUE)
    else:
        i_Start = prev_calculated - 1
    for i_2 in range(i_Start, rates_total):
        if g_MAMethod == MODE_SMA:
            _sw1 = g_MAApplied
            if _sw1 == PRICE_H:
                g_BufferMA[i_2] = SimpleMA(i_2, g_MAPeriod, high)
            elif _sw1 == PRICE_O:
                g_BufferMA[i_2] = SimpleMA(i_2, g_MAPeriod, open)
            elif _sw1 == PRICE_L:
                g_BufferMA[i_2] = SimpleMA(i_2, g_MAPeriod, low)
            else:
                g_BufferMA[i_2] = SimpleMA(i_2, g_MAPeriod, close)
        if g_MAMethod == MODE_EMA:
            _sw2 = g_MAApplied
            if _sw2 == PRICE_O:
                if i_2 == (g_MAPeriod - 1):
                    g_BufferMA[i_2] = CalculateFirstSMA(g_MAPeriod, open)
                else:
                    g_BufferMA[i_2] = ExponentialMA(i_2, g_MAPeriod, g_BufferMA[i_2 - 1], open)
            elif _sw2 == PRICE_H:
                if i_2 == (g_MAPeriod - 1):
                    g_BufferMA[i_2] = CalculateFirstSMA(g_MAPeriod, high)
                else:
                    g_BufferMA[i_2] = ExponentialMA(i_2, g_MAPeriod, g_BufferMA[i_2 - 1], high)
            elif _sw2 == PRICE_L:
                if i_2 == (g_MAPeriod - 1):
                    g_BufferMA[i_2] = CalculateFirstSMA(g_MAPeriod, low)
                else:
                    g_BufferMA[i_2] = ExponentialMA(i_2, g_MAPeriod, g_BufferMA[i_2 - 1], low)
            else:
                if i_2 == (g_MAPeriod - 1):
                    g_BufferMA[i_2] = CalculateFirstSMA(g_MAPeriod, close)
                else:
                    g_BufferMA[i_2] = ExponentialMA(i_2, g_MAPeriod, g_BufferMA[i_2 - 1], close)
        if g_MAMethod == MODE_SMMA:
            _sw3 = g_MAApplied
            if _sw3 == PRICE_O:
                if i_2 == (g_MAPeriod - 1):
                    g_BufferMA[i_2] = CalculateFirstSMA(g_MAPeriod, open)
                else:
                    g_BufferMA[i_2] = SmoothedMA(i_2, g_MAPeriod, g_BufferMA[i_2 - 1], open)
            elif _sw3 == PRICE_H:
                if i_2 == (g_MAPeriod - 1):
                    g_BufferMA[i_2] = CalculateFirstSMA(g_MAPeriod, high)
                else:
                    g_BufferMA[i_2] = SmoothedMA(i_2, g_MAPeriod, g_BufferMA[i_2 - 1], high)
            elif _sw3 == PRICE_L:
                if i_2 == (g_MAPeriod - 1):
                    g_BufferMA[i_2] = CalculateFirstSMA(g_MAPeriod, low)
                else:
                    g_BufferMA[i_2] = SmoothedMA(i_2, g_MAPeriod, g_BufferMA[i_2 - 1], low)
            else:
                if i_2 == (g_MAPeriod - 1):
                    g_BufferMA[i_2] = CalculateFirstSMA(g_MAPeriod, close)
                else:
                    g_BufferMA[i_2] = SmoothedMA(i_2, g_MAPeriod, g_BufferMA[i_2 - 1], close)
        if g_MAMethod == MODE_LWMA:
            _sw4 = g_MAApplied
            if _sw4 == PRICE_H:
                g_BufferMA[i_2] = LinearWeightedMA(i_2, g_MAPeriod, high)
            elif _sw4 == PRICE_O:
                g_BufferMA[i_2] = LinearWeightedMA(i_2, g_MAPeriod, open)
            elif _sw4 == PRICE_L:
                g_BufferMA[i_2] = LinearWeightedMA(i_2, g_MAPeriod, low)
            else:
                g_BufferMA[i_2] = LinearWeightedMA(i_2, g_MAPeriod, close)
    return rates_total

def CalculateFirstSMA(period, price):
    i_SMA = 0.0
    for j in range(0, period):
        i_SMA += price[j]
    return _fdiv(i_SMA, period)

def OnDeinit(reason):
    global g_PtMA
    Comment('')
    if g_PtMA != INVALID_HANDLE:
        IndicatorRelease(g_PtMA)
        g_PtMA = INVALID_HANDLE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MovingAveragesMqhPartI(_MQL5Indicator):
    name = 'MovingAverages.mqh Part I'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_MAPeriod': 20,  # Averaging period
        'g_MAShift': 0,  # Horizontal shift
        'g_MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing type
        'g_MAApplied': _Choice({0: 'High', 1: 'Open', 2: 'Low', 3: 'Close'}, default=3),  # Type of price
    }

