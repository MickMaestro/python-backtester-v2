"""iRSI Very Simple — converted from MQL5: MQL5 Indicators/iRSI Very Simple/iRSI Very Simple.mq5

iRSI() very simply.\\nA multi timeframe version is available for developers or profitable traders for free under conditions
Copyright: Copyright 2023, GwDs; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.02', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Rsi'}, 'levels': [70.0, 30.0], 'description': ['iRSI() very simply.\\nA multi timeframe version is available for developers or profitable traders for free under conditions'], 'name': 'iRSI Very Simple', 'source': 'MQL5 Indicators/iRSI Very Simple/iRSI Very Simple.mq5', 'folder': 'iRSI Very Simple', 'inputs': [{'mql': 'g_RsiPeriod', 'py': 'g_RsiPeriod', 'param': 'g_RsiPeriod', 'type': 'uchar', 'default': 14, 'label': 'Rsi Period', 'sinput': False}, {'mql': 'g_applBar', 'py': 'g_applBar', 'param': 'g_applBar', 'type': 'int', 'default': 1, 'label': 'Applied to', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_RsiPeriod = _input('g_RsiPeriod', 14)  # Rsi Period
g_applBar = _input('g_applBar', PRICE_CLOSE)  # Applied to
g_PtRsi = INVALID_HANDLE  # Pointer of the iRsi function
g_BufferRsi = Arr(0, 0.0)  # Data buffer

def OnInit():
    global g_PtRsi
    g_PtRsi = iRSI(Symbol(), Period(), g_RsiPeriod, g_applBar)
    if g_PtRsi == INVALID_HANDLE:
        PrintFormat('%s. Error %d when creating Rsi pointer', 'OnInit', GetLastError())
        return INIT_FAILED
    if not SetIndexBuffer(0, g_BufferRsi, INDICATOR_DATA):
        PrintFormat('%s: Error retrieving data for Rsi', 'OnInit', GetLastError())
        return 0
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i_Diff = rates_total - prev_calculated + 1
    if CopyBuffer(g_PtRsi, 0, 0, i_Diff, g_BufferRsi) < 0:
        PrintFormat('%s; Error %d in data recovery', 'OnCalculate', GetLastError())
        return 0
    return rates_total

def OnDeinit(reason):
    global g_PtRsi
    Comment('')
    if g_PtRsi != INVALID_HANDLE:
        IndicatorRelease(g_PtRsi)
        g_PtRsi = INVALID_HANDLE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IRSIVerySimple(_MQL5Indicator):
    name = 'iRSI Very Simple'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_RsiPeriod': 14,  # Rsi Period
        'g_applBar': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied to
    }
    y_range = (0.0, 100.0)

