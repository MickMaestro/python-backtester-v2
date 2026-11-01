"""Vortex Oscillator — converted from MQL5: MQL5 Indicators/Vortex Oscillator/Vortex Oscillator.mq5

Copyright: Copyright 2009 under Creative Commons BY-SA License by Neil D. Rosenthal & Michael Moses; Link: http://creativecommons.org/licenses/by-sa/3.0/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2009 under Creative Commons BY-SA License by Neil D. Rosenthal & Michael Moses', 'link': 'http://creativecommons.org/licenses/by-sa/3.0/', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Vortex Oscillator'}, 'levels': [], 'description': [], 'name': 'Vortex Oscillator', 'source': 'MQL5 Indicators/Vortex Oscillator/Vortex Oscillator.mq5', 'folder': 'Vortex Oscillator', 'inputs': [{'mql': 'VI_Length', 'py': 'VI_Length', 'param': 'VI_Length', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
VI_Length = _input('VI_Length', 14)
VortexOsc = Arr(0, 0.0)  # The Vortex Oscialltor - the difference betweeen VI+ and VI-
PlusVI = Arr(0, 0.0)  # VI+ : + Vortex Indicator buffer
MinusVI = Arr(0, 0.0)  # VI- : - Vortex Indicator buffer
PlusVM = Arr(0, 0.0)  # VM+ : + Vortex Movement buffer
MinusVM = Arr(0, 0.0)  # VM- : - Vorext Movement buffer
SumPlusVM = Arr(0, 0.0)  # Sum of VI_Length PlusVM values
SumMinusVM = Arr(0, 0.0)  # Sum of VI_Length MinusVM values
SumTR = Arr(0, 0.0)  # True Range buffer
ExtTRBuffer = Arr(0, 0.0)  # ATR buffer
ExtATRBuffer = Arr(0, 0.0)  # ATR calculation buffer

def OnInit():
    SetIndexBuffer(0, VortexOsc, INDICATOR_DATA)
    SetIndexBuffer(1, PlusVI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, MinusVI, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, VI_Length)
    SetIndexBuffer(3, PlusVM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, MinusVM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, SumPlusVM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, SumMinusVM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, SumTR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, ExtTRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, ExtATRBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (VI_Length + 1):
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
        for i in range(limit, rates_total):
            PlusVI[i] = 0.0
            MinusVI[i] = 0.0
            PlusVM[i] = 0.0
            MinusVM[i] = 0.0
            SumPlusVM[i] = 0.0
            SumMinusVM[i] = 0.0
            SumTR[i] = 0.0
            ExtTRBuffer[i] = 0.0
            ExtATRBuffer[i] = 0.0
        limit = VI_Length
    for i in range(limit, rates_total):
        PlusVM[i] = MathAbs(high[i] - low[i - 1])
        MinusVM[i] = MathAbs(low[i] - high[i - 1])
        ExtTRBuffer[i] = MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])
        ExtATRBuffer[i] = ExtATRBuffer[i - 1] + ((ExtTRBuffer[i] - ExtTRBuffer[i - 1]) / 1.0)
        for j in range(0, VI_Length):
            SumPlusVM[i] += PlusVM[i - j]
            SumMinusVM[i] += MinusVM[i - j]
            SumTR[i] += ExtATRBuffer[i - j]
        PlusVI[i] = _fdiv(SumPlusVM[i], SumTR[i])
        MinusVI[i] = _fdiv(SumMinusVM[i], SumTR[i])
        VortexOsc[i] = PlusVI[i] - MinusVI[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VortexOscillator(_MQL5Indicator):
    name = 'Vortex Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'VI_Length': 14,
    }

