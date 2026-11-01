"""Fractals chaos oscillator — converted from MQL5: MQL5 Indicators/Fractals Chaos Oscillator/Fractals chaos oscillator.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': -1.0, 'indicator_maximum': 1.0}, 'types': {1: 8}, 'colors': {1: [12632256, 3329330, 14053594]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Fractals chaos oscillator'}, 'levels': [], 'description': [], 'name': 'Fractals chaos oscillator', 'source': 'MQL5 Indicators/Fractals Chaos Oscillator/Fractals chaos oscillator.mq5', 'folder': 'Fractals Chaos Oscillator', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
_fractalHandle = 0

def OnInit():
    global _fractalHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    _fractalHandle = iFractals(Symbol(), 0)
    if _fractalHandle == INVALID_HANDLE:
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fractals chaos oscillator')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if BarsCalculated(_fractalHandle) < rates_total:
        return prev_calculated
    _fruVal = Arr(1, 0.0, dyn=False)
    _frdVal = Arr(1, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        valc[i] = 0.0
        _fruCopied = CopyBuffer(_fractalHandle, 0, _DT(time[i]), 1, _fruVal)
        _frdCopied = CopyBuffer(_fractalHandle, 1, _DT(time[i]), 1, _frdVal)
        if _fruCopied == 1 and _frdCopied == 1:
            valc[i] = (1 if (_fruVal[0] != EMPTY_VALUE) else 2 if (_frdVal[0] != EMPTY_VALUE) else 0)
        val[i] = (1 if (valc[i] == 1) else -1 if (valc[i] == 2) else 0)
        i += 1
    return MathMax(i - 3, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalsChaosOscillator(_MQL5Indicator):
    name = 'Fractals chaos oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }
    y_range = (-1.0, 1.0)

