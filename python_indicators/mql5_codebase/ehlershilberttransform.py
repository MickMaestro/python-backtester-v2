"""EhlersHilbertTransform — converted from MQL5: MQL5 Indicators/The Hilbert Oscillator Indicator/EhlersHilbertTransform.mq5

Telegram Channel: https://t.me/fxstill\\n
The Hilbert Transform:\\nJohn Ehlers, \\"Rocket Science for Traders.\\", pg.51
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 14, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [42495], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': ['Telegram Channel: https://t.me/fxstill\\n', 'The Hilbert Transform:\\nJohn Ehlers, \\"Rocket Science for Traders.\\", pg.51'], 'name': 'EhlersHilbertTransform', 'source': 'MQL5 Indicators/The Hilbert Oscillator Indicator/EhlersHilbertTransform.mq5', 'folder': 'The Hilbert Oscillator Indicator', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InPhase = Arr(0, 0.0)
Quadrature = Arr(0, 0.0)
Smooth = Arr(0, 0.0)
Detrender = Arr(0, 0.0)
I1 = Arr(0, 0.0)
Q1 = Arr(0, 0.0)
jI = Arr(0, 0.0)
jQ = Arr(0, 0.0)
I2 = Arr(0, 0.0)
Q2 = Arr(0, 0.0)
Re = Arr(0, 0.0)
Im = Arr(0, 0.0)
Per = Arr(0, 0.0)
SmoothPeriod = Arr(0, 0.0)
MINBAR = 7

def OnInit():
    SetIndexBuffer(0, InPhase, INDICATOR_DATA)
    SetIndexBuffer(1, Quadrature, INDICATOR_DATA)
    SetIndexBuffer(2, Smooth, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, Detrender, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, I1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, Q1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, jI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, jQ, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, I2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, Q2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, Re, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, Im, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, Per, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, SmoothPeriod, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(InPhase, True)
    ArraySetAsSeries(Quadrature, True)
    ArraySetAsSeries(Smooth, True)
    ArraySetAsSeries(Detrender, True)
    ArraySetAsSeries(I1, True)
    ArraySetAsSeries(Q1, True)
    ArraySetAsSeries(jI, True)
    ArraySetAsSeries(jQ, True)
    ArraySetAsSeries(I2, True)
    ArraySetAsSeries(Q2, True)
    ArraySetAsSeries(Re, True)
    ArraySetAsSeries(Im, True)
    ArraySetAsSeries(Per, True)
    ArraySetAsSeries(SmoothPeriod, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersHilbertTransform')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < MINBAR:
        return 0
    ArraySetAsSeries(price, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        Hilbert(price, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(InPhase, EMPTY_VALUE)
        ArrayInitialize(Quadrature, EMPTY_VALUE)
        ArrayInitialize(Smooth, 0)
        ArrayInitialize(Detrender, 0)
        ArrayInitialize(I1, 0)
        ArrayInitialize(Q1, 0)
        ArrayInitialize(jI, 0)
        ArrayInitialize(jQ, 0)
        ArrayInitialize(I2, 0)
        ArrayInitialize(Q2, 0)
        ArrayInitialize(Re, 0)
        ArrayInitialize(Im, 0)
        ArrayInitialize(Per, 0)
        ArrayInitialize(SmoothPeriod, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            Hilbert(price, i)
        return rates_total
    Hilbert(price, 0)
    return rates_total

def Hilbert(price, i):
    Smooth[i] = ((4 * price[i]) + (3 * price[i + 1]) + (2 * price[i + 2]) + price[i + 3]) / 10
    Detrender[i] = ((0.0962 * Smooth[i]) + (0.5769 * Smooth[i + 2]) - (0.5769 * Smooth[i + 4]) - (0.0962 * Smooth[i + 6])) * ((0.075 * Per[i + 1]) + 0.54)
    Q1[i] = ((0.0962 * Detrender[i]) + (0.5769 * Detrender[i + 2]) - (0.5769 * Detrender[i + 4]) - (0.0962 * Detrender[i + 6])) * ((0.075 * Per[i + 1]) + 0.54)
    I1[i] = Detrender[i + 3]
    jI[i] = ((0.0962 * I1[i]) + (0.5769 * I1[i + 2]) - (0.5769 * I1[i + 4]) - (0.0962 * I1[i + 6])) * ((0.075 * Per[i + 1]) + 0.54)
    jQ[i] = ((0.0962 * Q1[i]) + (0.5769 * Q1[i + 2]) - (0.5769 * Q1[i + 4]) - (0.0962 * Q1[i + 6])) * ((0.075 * Per[i + 1]) + 0.54)
    I2[i] = I1[i] - jQ[i]
    Q2[i] = Q1[i] + jI[i]
    I2[i] = (0.2 * I2[i]) + (0.8 * I2[i + 1])
    Q2[i] = (0.2 * Q2[i]) + (0.8 * Q2[i + 1])
    Re[i] = (I2[i] * I2[i]) + (Q2[i] * Q2[i + 1])
    Im[i] = (I2[i] * Q2[i + 1]) - (Q2[i] * I2[i + 1])
    Re[i] = (0.2 * Re[i]) + (0.8 * Re[i + 1])
    Im[i] = (0.2 * Im[i]) + (0.8 * Im[i + 1])
    if Im[i] != 0 and Re[i] != 0:
        Per[i] = _fdiv(2 * M_PI, MathArctan(_fdiv(Im[i], Re[i])))
    else:
        Per[i] = 0.0
    if Per[i] > (1.5 * Per[i + 1]):
        Per[i] = 1.5 * Per[i + 1]
    if Per[i] < (0.67 * Per[i + 1]):
        Per[i] = 0.67 * Per[i + 1]
    if Per[i] < 6:
        Per[i] = 6.0
    if Per[i] > 50:
        Per[i] = 50.0
    Per[i] = (0.2 * Per[i]) + (0.8 * Per[i + 1])
    SmoothPeriod[i] = (0.33 * Per[i]) + (0.67 * SmoothPeriod[i + 1])
    InPhase[i] = I1[i]
    Quadrature[i] = Q1[i]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersHilbertTransform(_MQL5Indicator):
    name = 'EhlersHilbertTransform'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

