"""EhlersDecyclerOscillator — converted from MQL5: MQL5 Indicators/The Decycler Oscillator/EhlersDecyclerOscillator.mq5

The Decycler Oscillator:\\nJohn Ehlers, \\"Cycle Analytics For Traders\\", pg.43-44
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Dec'}, 'levels': [], 'description': ['The Decycler Oscillator:\\nJohn Ehlers, \\"Cycle Analytics For Traders\\", pg.43-44'], 'name': 'EhlersDecyclerOscillator', 'source': 'MQL5 Indicators/The Decycler Oscillator/EhlersDecyclerOscillator.mq5', 'folder': 'The Decycler Oscillator', 'inputs': [{'mql': 'l1', 'py': 'l1', 'param': 'l1', 'type': 'int', 'default': 10, 'label': 'Period 1', 'sinput': False}, {'mql': 'l2', 'py': 'l2', 'param': 'l2', 'type': 'int', 'default': 20, 'label': 'Period 2', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
l1 = _input('l1', 10)  # Period 1
l2 = _input('l2', 20)  # Period 2
dec = Arr(0, 0.0)
hp1 = Arr(0, 0.0)
hp2 = Arr(0, 0.0)
MINBAR = 5
a1 = 0.0
a1k = 0.0
a1l = 0.0
a2 = 0.0
a2k = 0.0
a2l = 0.0

def OnInit():
    global a1, a1k, a1l, a2, a2k, a2l
    SetIndexBuffer(0, dec, INDICATOR_DATA)
    SetIndexBuffer(1, hp1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, hp2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(dec, True)
    ArraySetAsSeries(hp1, True)
    ArraySetAsSeries(hp2, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersDecyclerOscillator')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    k = M_SQRT1_2 * 2 * M_PI
    t1 = _fdiv(MathCos(k / l1) + MathSin(k / l1) - 1, MathCos(k / l1))
    a1 = 1 - t1
    a1k = 1 - (t1 / 2)
    a1k *= a1k
    a1l = MathPow(a1, 2)
    a1 *= 2
    t2 = _fdiv(MathCos(k / l2) + MathSin(k / l2) - 1, MathCos(k / l2))
    a2 = 1 - t2
    a2k = 1 - (t2 / 2)
    a2k *= a2k
    a2l = MathPow(a2, 2)
    a2 *= 2
    return INIT_SUCCEEDED

def GetValue(price, shift):
    hp1[shift] = (a1k * (price[shift] - (2 * price[shift + 1]) + price[shift + 2])) + (a1 * hp1[shift + 1]) - (a1l * hp1[shift + 2])
    hp2[shift] = (a2k * (price[shift] - (2 * price[shift + 1]) + price[shift + 2])) + (a2 * hp2[shift + 1]) - (a2l * hp2[shift + 2])
    dec[shift] = hp2[shift] - hp1[shift]

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < MINBAR:
        return 0
    ArraySetAsSeries(price, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        GetValue(price, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(dec, EMPTY_VALUE)
        ArrayInitialize(hp1, 0)
        ArrayInitialize(hp2, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersDecyclerOscillator(_MQL5Indicator):
    name = 'EhlersDecyclerOscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'l1': 10,  # Period 1
        'l2': 20,  # Period 2
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

