"""SAR_Oscillator2 — converted from MQL5: MQL5 Indicators/SAR_Oscillator2/SAR_Oscillator2.mq5

SAR Oscillator 2
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16760576, 15130800, 11920639, 42495, 14474460]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SAR Osc'}, 'levels': [], 'description': ['SAR Oscillator 2'], 'name': 'SAR_Oscillator2', 'source': 'MQL5 Indicators/SAR_Oscillator2/SAR_Oscillator2.mq5', 'folder': 'SAR_Oscillator2', 'inputs': [{'mql': 'InpStep', 'py': 'InpStep', 'param': 'InpStep', 'type': 'double', 'default': 0.02, 'label': 'SAR step', 'sinput': False}, {'mql': 'InpMax', 'py': 'InpMax', 'param': 'InpMax', 'type': 'double', 'default': 0.2, 'label': 'SAR maximum', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpStep = _input('InpStep', 0.02)  # SAR step
InpMax = _input('InpMax', 0.2)  # SAR maximum
BufferOscSAR = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSAR = Arr(0, 0.0)
step = 0.0
max_ = 0.0
handle_sar = 0

def OnInit():
    global handle_sar, max_, step
    step = (0.0001 if (InpStep < 0.0001) else InpStep)
    max_ = (0.0001 if (InpMax < 0.0001) else InpMax)
    SetIndexBuffer(0, BufferOscSAR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSAR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SAR Oscillator 2 ' + DoubleToString(step, 2) + ',' + DoubleToString(max_, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferOscSAR, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSAR, True)
    ResetLastError()
    handle_sar = iSAR(None, PERIOD_CURRENT, step, max_)
    if handle_sar == INVALID_HANDLE:
        Print('The iSAR(', DoubleToString(step, 2), ',' + DoubleToString(max_, 2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferOscSAR, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferSAR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_sar, 0, 0, count, BufferSAR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferOscSAR[i] = BufferSAR[i] - close[i]
        BufferColors[i] = ((1 if (BufferOscSAR[i] > BufferOscSAR[i + 1]) else 0 if (BufferOscSAR[i] < BufferOscSAR[i + 1]) else 4) if (BufferOscSAR[i] < 0) else (3 if (BufferOscSAR[i] > BufferOscSAR[i + 1]) else 2 if (BufferOscSAR[i] < BufferOscSAR[i + 1]) else 4) if (BufferOscSAR[i] > 0) else 4)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SAROscillator2(_MQL5Indicator):
    name = 'SAR_Oscillator2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStep': 0.02,  # SAR step
        'InpMax': 0.2,  # SAR maximum
    }

