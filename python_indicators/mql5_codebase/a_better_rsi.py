"""A BETTER RSI — converted from MQL5: MQL5 Indicators/A BETTER RSI/A BETTER RSI.mq5

Copyright: Copyright 2023, ZOE HIGHTOWER; Link: zoeinhightower@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2023, ZOE HIGHTOWER', 'link': 'zoeinhightower@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711935]}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'A BETTER RSI'}, 'levels': [4.0, -4.0, 1.0, -1.0, 0.0], 'description': [], 'name': 'A BETTER RSI', 'source': 'MQL5 Indicators/A BETTER RSI/A BETTER RSI.mq5', 'folder': 'A BETTER RSI', 'inputs': [{'mql': 'Signal_period', 'py': 'Signal_period', 'param': 'Signal_period', 'type': 'int', 'default': 22, 'label': 'Signal Period', 'sinput': False}, {'mql': 'ROC_period', 'py': 'ROC_period', 'param': 'ROC_period', 'type': 'int', 'default': 10, 'label': 'Rate of Change Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
Signal_period = _input('Signal_period', 22)  # Signal Period
ROC_period = _input('ROC_period', 10)  # Rate of Change Period
Deriv = Arr(0, 0.0)
RMS = Arr(0, 0.0)
Clip = Arr(0, 0.0)
Z3 = Arr(0, 0.0)
Signal = Arr(0, 0.0)
ROC = Arr(0, 0.0)
Z3MA = Arr(0, 0.0)
SignalMA = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ROC, INDICATOR_DATA)
    SetIndexBuffer(1, RMS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, Clip, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, Z3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, Signal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, Deriv, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, Z3MA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, SignalMA, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Z3MA, True)
    ArraySetAsSeries(SignalMA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    for i in range(3, rates_total):
        Deriv[i] = 0.0
        RMS[i] = 0.0
        Clip[i] = 0.0
        Z3[i] = 0.0
        Signal[i] = 0.0
        ROC[i] = 0.0
        Deriv[i] = price[i] - price[i - 2]
        RMS[i] = RMS[i] + (Deriv[i] * Deriv[i])
        if RMS[i] != 0:
            Clip[i] = _fdiv(2 * Deriv[i], MathSqrt(RMS[i] / 50))
        if Clip[i] > 1:
            Clip[i] = 1.0
        if Clip[i] < -1:
            Clip[i] = -1.0
        Z3[i] = Clip[i] + Clip[i - 1] + Clip[i - 2] + Clip[i - 3]
        Z3MA[i] = SimpleMA(i, ROC_period, Z3)
        Signal[i] = Z3MA[i]
        SignalMA[i] = SimpleMA(i, Signal_period, Signal)
        ROC[i] = Signal[i] - SignalMA[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ABETTERRSI(_MQL5Indicator):
    name = 'A BETTER RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Signal_period': 22,  # Signal Period
        'ROC_period': 10,  # Rate of Change Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

