"""MovingAverages.mqh Part II — converted from MQL5: MQL5 Indicators/MovingAverages.mqh Part II/MovingAverages.mqh Part II.mq5

MovingAverages.mqh very simply.\\nA multi timeframe version is available for developers or profitable traders for free under conditions
Copyright: Copyright 2024, GwDs; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2024, GwDs', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Moving average'}, 'levels': [], 'description': ['MovingAverages.mqh very simply.\\nA multi timeframe version is available for developers or profitable traders for free under conditions'], 'name': 'MovingAverages.mqh Part II', 'source': 'MQL5 Indicators/MovingAverages.mqh Part II/MovingAverages.mqh Part II.mq5', 'folder': 'MovingAverages.mqh Part II', 'inputs': [{'mql': 'g_MAPeriod', 'py': 'g_MAPeriod', 'param': 'g_MAPeriod', 'type': 'uchar', 'default': 20, 'label': 'Averaging period', 'sinput': False}, {'mql': 'g_MAShift', 'py': 'g_MAShift', 'param': 'g_MAShift', 'type': 'uchar', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'g_MAMethod', 'py': 'g_MAMethod', 'param': 'g_MAMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'g_MAApplied', 'py': 'g_MAApplied', 'param': 'g_MAApplied', 'type': 'int', 'default': 3, 'label': 'Type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum g_PriceType
PRICE_H = 0
PRICE_O = 1
PRICE_L = 2
PRICE_C = 3
_enum('g_PriceType', {0: 'PRICE_H', 1: 'PRICE_O', 2: 'PRICE_L', 3: 'PRICE_C'})

# enum ENUM_MA_METHOD_EXTENDED
ExtMODE_SMA = 0
ExtMODE_EMA = 1
ExtMODE_SMMA = 2
ExtMODE_LWMA_CLASSIC = 3
ExtMODE_LWMA_FAST = 4
_enum('ENUM_MA_METHOD_EXTENDED', {0: 'ExtMODE_SMA', 1: 'ExtMODE_EMA', 2: 'ExtMODE_SMMA', 3: 'ExtMODE_LWMA_CLASSIC', 4: 'ExtMODE_LWMA_FAST'})

# ---- inputs and global variables
g_weight_sum = 0
g_MAPeriod = _input('g_MAPeriod', 20)  # Averaging period
g_MAShift = _input('g_MAShift', 0)  # Horizontal shift
g_MAMethod = _input('g_MAMethod', ExtMODE_SMA)  # Smoothing type
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
    i_CalcResult = 0
    i_Start = 0
    if prev_calculated == 0:
        i_Start = g_MAPeriod - 1
        ArrayInitialize(g_BufferMA, EMPTY_VALUE)
    else:
        i_Start = prev_calculated
    if g_MAMethod == ExtMODE_SMA:
        _sw1 = g_MAApplied
        if _sw1 == PRICE_H:
            i_CalcResult = SimpleMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, high, g_BufferMA)
        elif _sw1 == PRICE_O:
            i_CalcResult = SimpleMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, open, g_BufferMA)
        elif _sw1 == PRICE_L:
            i_CalcResult = SimpleMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, low, g_BufferMA)
        else:
            i_CalcResult = SimpleMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, close, g_BufferMA)
        if i_CalcResult == 0:
            PrintFormat('%s: The function SimpleMAOnBuffer returned 0', 'OnCalculate')
    if g_MAMethod == ExtMODE_EMA:
        _sw2 = g_MAApplied
        if _sw2 == PRICE_O:
            i_CalcResult = ExponentialMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, open, g_BufferMA)
        elif _sw2 == PRICE_H:
            i_CalcResult = ExponentialMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, high, g_BufferMA)
        elif _sw2 == PRICE_L:
            i_CalcResult = ExponentialMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, low, g_BufferMA)
        else:
            i_CalcResult = ExponentialMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, close, g_BufferMA)
        if i_CalcResult == 0:
            PrintFormat('%s: The function ExponentialMAOnBuffer returned 0', 'OnCalculate')
    if g_MAMethod == ExtMODE_SMMA:
        _sw3 = g_MAApplied
        if _sw3 == PRICE_O:
            i_CalcResult = SmoothedMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, open, g_BufferMA)
        elif _sw3 == PRICE_H:
            i_CalcResult = SmoothedMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, high, g_BufferMA)
        elif _sw3 == PRICE_L:
            i_CalcResult = SmoothedMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, low, g_BufferMA)
        else:
            i_CalcResult = SmoothedMAOnBuffer(rates_total, prev_calculated, 0, g_MAPeriod, close, g_BufferMA)
        if i_CalcResult == 0:
            PrintFormat('%s: The function SmoothedMAOnBuffer returned 0', 'OnCalculate')
    if g_MAMethod == ExtMODE_LWMA_CLASSIC:
        _sw4 = g_MAApplied
        if _sw4 == PRICE_O:
            i_CalcResult = LinearWeightedMAOnBuffer_1(rates_total, prev_calculated, 0, g_MAPeriod, open, g_BufferMA)
        elif _sw4 == PRICE_H:
            i_CalcResult = LinearWeightedMAOnBuffer_1(rates_total, prev_calculated, 0, g_MAPeriod, high, g_BufferMA)
        elif _sw4 == PRICE_L:
            i_CalcResult = LinearWeightedMAOnBuffer_1(rates_total, prev_calculated, 0, g_MAPeriod, low, g_BufferMA)
        else:
            i_CalcResult = LinearWeightedMAOnBuffer_1(rates_total, prev_calculated, 0, g_MAPeriod, close, g_BufferMA)
        if i_CalcResult == 0:
            PrintFormat('%s: The function LinearWeightedMAOnBuffer returned 0', 'OnCalculate')
    if g_MAMethod == ExtMODE_LWMA_FAST:
        _sw5 = g_MAApplied
        if _sw5 == PRICE_O:
            i_CalcResult = LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, g_MAPeriod, open, g_BufferMA, _GlobRef(globals(), 'g_weight_sum'))
        elif _sw5 == PRICE_H:
            i_CalcResult = LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, g_MAPeriod, high, g_BufferMA, _GlobRef(globals(), 'g_weight_sum'))
        elif _sw5 == PRICE_L:
            i_CalcResult = LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, g_MAPeriod, low, g_BufferMA, _GlobRef(globals(), 'g_weight_sum'))
        else:
            i_CalcResult = LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, g_MAPeriod, close, g_BufferMA, _GlobRef(globals(), 'g_weight_sum'))
        if i_CalcResult == 0:
            PrintFormat('%s: The function LinearWeightedMAOnBuffer returned 0', 'OnCalculate')
    return rates_total

def OnDeinit(reason):
    global g_PtMA
    Comment('')
    if g_PtMA != INVALID_HANDLE:
        IndicatorRelease(g_PtMA)
        g_PtMA = INVALID_HANDLE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MovingAveragesMqhPartII(_MQL5Indicator):
    name = 'MovingAverages.mqh Part II'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_MAPeriod': 20,  # Averaging period
        'g_MAShift': 0,  # Horizontal shift
        'g_MAMethod': _Choice({0: 'Simple Moving Average', 1: 'Exponential Moving Average', 2: 'Smoothed Moving Average', 3: 'Linear Weighted Moving Average - Classic', 4: 'Linear Weighted Moving Average - Fast'}, default=0),  # Smoothing type
        'g_MAApplied': _Choice({0: 'High', 1: 'Open', 2: 'Low', 3: 'Close'}, default=3),  # Type of price
    }

