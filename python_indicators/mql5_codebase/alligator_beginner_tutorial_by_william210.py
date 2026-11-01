"""Alligator beginner tutorial by William210 — converted from MQL5: MQL5 Indicators/Alligator code for beginners by William210/Alligator beginner tutorial by William210.mq5

Search all my free or paid codes with William210
\\nAlligator beginner tutorial to learn
Questions about the code? ask me in MP
Contact me on https://www.mql5.com/fr/users/william210
Code request? https://www.mql5.com/en/forum/453288
Copyright: Copyright 2023, GwDs; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [65280]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Jaws', 2: 'Teeth', 3: 'Lips'}, 'levels': [], 'description': ['Search all my free or paid codes with William210', '\\nAlligator beginner tutorial to learn', 'Questions about the code? ask me in MP', 'Contact me on https://www.mql5.com/fr/users/william210', 'Code request? https://www.mql5.com/en/forum/453288'], 'name': 'Alligator beginner tutorial by William210', 'source': 'MQL5 Indicators/Alligator code for beginners by William210/Alligator beginner tutorial by William210.mq5', 'folder': 'Alligator code for beginners by William210', 'inputs': [{'mql': 'g_jaw_period', 'py': 'g_jaw_period', 'param': 'g_jaw_period', 'type': 'uchar', 'default': 13, 'label': 'Period of the Jaw line', 'sinput': False}, {'mql': 'g_jaw_shift', 'py': 'g_jaw_shift', 'param': 'g_jaw_shift', 'type': 'uchar', 'default': 8, 'label': 'Shift of the Jaw line', 'sinput': False}, {'mql': 'g_teeth_period', 'py': 'g_teeth_period', 'param': 'g_teeth_period', 'type': 'uchar', 'default': 8, 'label': 'Period of the Teeth line', 'sinput': False}, {'mql': 'g_teeth_shift', 'py': 'g_teeth_shift', 'param': 'g_teeth_shift', 'type': 'uchar', 'default': 5, 'label': 'Shift of the Teeth line', 'sinput': False}, {'mql': 'g_lips_period', 'py': 'g_lips_period', 'param': 'g_lips_period', 'type': 'uchar', 'default': 5, 'label': 'Period of the Lips line', 'sinput': False}, {'mql': 'g_lips_shift', 'py': 'g_lips_shift', 'param': 'g_lips_shift', 'type': 'uchar', 'default': 3, 'label': 'Shift of the Lips line', 'sinput': False}, {'mql': 'g_MA_method', 'py': 'g_MA_method', 'param': 'g_MA_method', 'type': 'int', 'default': 2, 'label': 'Method of averaging of the Alligator lines', 'sinput': False}, {'mql': 'g_applied_price', 'py': 'g_applied_price', 'param': 'g_applied_price', 'type': 'int', 'default': 5, 'label': 'Type of price used for calculation of Alligator', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_jaw_period = _input('g_jaw_period', 13)  # Period of the Jaw line
g_jaw_shift = _input('g_jaw_shift', 8)  # Shift of the Jaw line
g_teeth_period = _input('g_teeth_period', 8)  # Period of the Teeth line
g_teeth_shift = _input('g_teeth_shift', 5)  # Shift of the Teeth line
g_lips_period = _input('g_lips_period', 5)  # Period of the Lips line
g_lips_shift = _input('g_lips_shift', 3)  # Shift of the Lips line
g_MA_method = _input('g_MA_method', MODE_SMMA)  # Method of averaging of the Alligator lines
g_applied_price = _input('g_applied_price', PRICE_MEDIAN)  # Type of price used for calculation of Alligator
g_PtAlligator = INVALID_HANDLE  # Pointer of the iRsi function
g_JawsBuffer = Arr(0, 0.0)  # Data buffer jaws
g_TeethBuffer = Arr(0, 0.0)  # Data buffer teeth
g_LipsBuffer = Arr(0, 0.0)  # Data buffer lips

def OnInit():
    global g_PtAlligator
    g_PtAlligator = iAlligator(Symbol(), Period(), g_jaw_period, g_jaw_shift, g_teeth_period, g_teeth_shift, g_lips_period, g_lips_shift, g_MA_method, g_applied_price)
    if g_PtAlligator == INVALID_HANDLE:
        PrintFormat('%s: Error when creating Alligator pointer', 'OnInit')
        return INIT_FAILED
    SetIndexBuffer(0, g_JawsBuffer, INDICATOR_DATA)
    PrintFormat('%s: Error %d SetIndexBuffer( g_BuffADXMinus)', 'OnInit', GetLastError())
    SetIndexBuffer(1, g_TeethBuffer, INDICATOR_DATA)
    PrintFormat('%s: Error %d SetIndexBuffer( g_BuffADXMinus)', 'OnInit', GetLastError())
    SetIndexBuffer(2, g_LipsBuffer, INDICATOR_DATA)
    PrintFormat('%s: Error %d SetIndexBuffer( g_BuffADXMinus)', 'OnInit', GetLastError())
    PlotIndexSetInteger(0, PLOT_SHIFT, g_jaw_shift)
    PrintFormat('%s: Error %d PlotIndexSetInteger( g_indexiMA)', 'OnInit', GetLastError())
    PlotIndexSetInteger(1, PLOT_SHIFT, g_teeth_shift)
    PrintFormat('%s: Error %d PlotIndexSetInteger( g_indexiMA)', 'OnInit', GetLastError())
    PlotIndexSetInteger(2, PLOT_SHIFT, g_lips_shift)
    PrintFormat('%s: Error %d PlotIndexSetInteger( g_indexiMA)', 'OnInit', GetLastError())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i_Diff = 0
    if prev_calculated < rates_total:
        i_Diff = rates_total - prev_calculated
        if CopyBuffer(g_PtAlligator, 0, -g_jaw_shift, i_Diff, g_JawsBuffer) < 0:
            PrintFormat('%s: Data recovery error for jaws', 'OnCalculate')
            return 0
        if CopyBuffer(g_PtAlligator, 1, -g_teeth_shift, i_Diff, g_TeethBuffer) < 0:
            PrintFormat('%s: Data recovery error for teeth', 'OnCalculate')
            return 0
        if CopyBuffer(g_PtAlligator, 2, -g_lips_shift, i_Diff, g_LipsBuffer) < 0:
            PrintFormat('%s: Data recovery error for lips', 'OnCalculate')
            return 0
    return rates_total

def OnDeinit(reason):
    global g_PtAlligator
    Comment('')
    if g_PtAlligator != INVALID_HANDLE:
        IndicatorRelease(g_PtAlligator)
        g_PtAlligator = INVALID_HANDLE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AlligatorBeginnerTutorialByWilliam210(_MQL5Indicator):
    name = 'Alligator beginner tutorial by William210'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_jaw_period': 13,  # Period of the Jaw line
        'g_jaw_shift': 8,  # Shift of the Jaw line
        'g_teeth_period': 8,  # Period of the Teeth line
        'g_teeth_shift': 5,  # Shift of the Teeth line
        'g_lips_period': 5,  # Period of the Lips line
        'g_lips_shift': 3,  # Shift of the Lips line
        'g_MA_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method of averaging of the Alligator lines
        'g_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Type of price used for calculation of Alligator
    }

