"""ichimokuoscillator — converted from MQL5: MQL5 Indicators/Ichimoku Oscillator/ichimokuoscillator.mq5

Copyright: Copyright 2010, Alf; Link: http://forum.liteforex.org/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, Alf', 'link': 'http://forum.liteforex.org/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65535], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fist', 2: 'Second'}, 'levels': [], 'description': [], 'name': 'ichimokuoscillator', 'source': 'MQL5 Indicators/Ichimoku Oscillator/ichimokuoscillator.mq5', 'folder': 'Ichimoku Oscillator', 'inputs': [{'mql': 'Tankan_sen', 'py': 'Tankan_sen', 'param': 'Tankan_sen', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'Kijun_sen', 'py': 'Kijun_sen', 'param': 'Kijun_sen', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'Senkou_snap_B', 'py': 'Senkou_snap_B', 'param': 'Senkou_snap_B', 'type': 'int', 'default': 52, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Tankan_sen = _input('Tankan_sen', 9)
Kijun_sen = _input('Kijun_sen', 26)
Senkou_snap_B = _input('Senkou_snap_B', 52)
FistBuffer = Arr(0, 0.0)
SecondBuffer = Arr(0, 0.0)
b1 = Arr(0, 0.0)
b2 = Arr(0, 0.0)
b3 = Arr(0, 0.0)
b4 = Arr(0, 0.0)
ish = 0

def OnInit():
    global ish
    SetIndexBuffer(0, FistBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SecondBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, b1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, b2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, b3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, b4, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_SHIFT, Kijun_sen)
    ish = iIchimoku(Symbol(), 0, Tankan_sen, Kijun_sen, Senkou_snap_B)
    Print('i=', ish)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < Senkou_snap_B:
        return 0
    calculated = BarsCalculated(ish)
    if calculated < rates_total:
        Print('Not all data of ExtFastMaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if CopyBuffer(ish, 0, 0, to_copy, b1) <= 0:
        Print('ER1 ', to_copy)
        return 0
    if CopyBuffer(ish, 1, 0, to_copy, b2) <= 0:
        Print('ER2 ', to_copy)
        return 0
    if CopyBuffer(ish, 2, 0 - Kijun_sen, to_copy, b3) <= 0:
        Print('ER3 ', to_copy)
        return 0
    if CopyBuffer(ish, 3, 0 - Kijun_sen, to_copy, b4) <= 0:
        Print('ER4', to_copy)
        return 0
    for i in range(0, rates_total):
        FistBuffer[i] = b1[i] - b2[i]
        SecondBuffer[i] = b3[i] - b4[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ichimokuoscillator(_MQL5Indicator):
    name = 'ichimokuoscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Tankan_sen': 9,
        'Kijun_sen': 26,
        'Senkou_snap_B': 52,
    }

