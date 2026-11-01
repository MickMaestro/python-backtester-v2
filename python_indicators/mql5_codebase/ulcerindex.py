"""UlcerIndex — converted from MQL5: MQL5 Indicators/Ulcer Index/UlcerIndex.mq5

Copyright: Copyright 2018, Samuel Williams; Link: https://www.mql5.com/en/users/sambo3261; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, Samuel Williams', 'link': 'https://www.mql5.com/en/users/sambo3261', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [36095]}, 'widths': {1: 3}, 'styles': {1: 1}, 'labels': {1: 'UI'}, 'levels': [], 'description': [], 'name': 'UlcerIndex', 'source': 'MQL5 Indicators/Ulcer Index/UlcerIndex.mq5', 'folder': 'Ulcer Index', 'inputs': [{'mql': 'LookBackPeriod', 'py': 'LookBackPeriod', 'param': 'LookBackPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LookBackPeriod = _input('LookBackPeriod', 14)
UIBuffer = Arr(0, 0.0)
DrawDownBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, UIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DrawDownBuffer, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        DrawDownBuffer[i] = _fdiv(close[i] - close[ArrayMaximum(close, LookBackPeriod, i)], close[ArrayMaximum(close, LookBackPeriod, i)])
        squaredDD = 0.0
        squaredAvg = 0.0
        if i > LookBackPeriod:
            for x in range(i - LookBackPeriod, i):
                squaredDD = squaredDD + MathPow(DrawDownBuffer[x], 2)
        squaredAvg = squaredDD / LookBackPeriod
        UIBuffer[i] = MathSqrt(squaredAvg)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UlcerIndex(_MQL5Indicator):
    name = 'UlcerIndex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LookBackPeriod': 14,
    }

