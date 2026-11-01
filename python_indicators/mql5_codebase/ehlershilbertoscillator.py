"""EhlersHilbertOscillator — converted from MQL5: MQL5 Indicators/The Hilbert Oscillator Indicator/EhlersHilbertOscillator.mq5

Telegram Channel: https://t.me/fxstill\\n
The Hilbert Oscillator:\\nJohn Ehlers, \\"Rocket Science For Traders\\", pg.90-91
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 8, 2: 1, 3: 1}, 'colors': {1: [32768, 255, 3329330], 2: [16748574], 3: [255]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'snr', 2: 'V3', 3: 'I3'}, 'levels': [], 'description': ['Telegram Channel: https://t.me/fxstill\\n', 'The Hilbert Oscillator:\\nJohn Ehlers, \\"Rocket Science For Traders\\", pg.90-91'], 'name': 'EhlersHilbertOscillator', 'source': 'MQL5 Indicators/The Hilbert Oscillator Indicator/EhlersHilbertOscillator.mq5', 'folder': 'The Hilbert Oscillator Indicator', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
zr = Arr(0, 0.0)
zc = Arr(0, 0.0)
v1 = Arr(0, 0.0)
i3 = Arr(0, 0.0)
q3 = Arr(0, 0.0)
MINBAR = 5
h = 0

def OnInit():
    global h
    h = iCustom(None, 0, 'EhlersHilbertTransform')
    if h == INVALID_HANDLE:
        Print('Error while creating "EhlersHilbertTransform"')
        return INIT_FAILED
    SetIndexBuffer(0, zr, INDICATOR_DATA)
    SetIndexBuffer(1, zc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, v1, INDICATOR_DATA)
    SetIndexBuffer(3, i3, INDICATOR_DATA)
    SetIndexBuffer(4, q3, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(zr, True)
    ArraySetAsSeries(zc, True)
    ArraySetAsSeries(v1, True)
    ArraySetAsSeries(i3, True)
    ArraySetAsSeries(q3, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersHilbertOscillator')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT__SUCCEEDED()

def GetValue(price, shift):
    SmoothPeriod = Arr(1, 0.0, dyn=False)
    if CopyBuffer(h, 13, shift, 1, SmoothPeriod) <= 0:
        return
    if SmoothPeriod[0] == 0.0:
        return
    sp2 = _int(MathCeil(SmoothPeriod[0] / 2))
    if (shift + sp2) >= ArraySize(q3):
        return
    if sp2 < 3:
        sp2 = 3
    Smooth = Arr(0, 0.0)
    ArrayResize(Smooth, sp2 + 1)
    ArrayInitialize(Smooth, 0)
    ArraySetAsSeries(Smooth, True)
    if CopyBuffer(h, 2, shift, sp2, Smooth) <= 0:
        return
    q3[shift] = 0.5 * (Smooth[0] - Smooth[2]) * ((0.1759 * SmoothPeriod[0]) + 0.4607)
    i3[shift] = q3[shift]
    i3[shift] = 0.0
    for i in range(0, sp2):
        i3[shift] = i3[shift] + q3[shift + i]
    i3[shift] = _fdiv(1.57 * i3[shift], sp2)
    sp4 = MathCeil(SmoothPeriod[0] / 4)
    v1[shift] = 0.0
    i = 0
    while i < sp4:
        v1[shift] = v1[shift] + q3[shift + i]
        i += 1
    v1[shift] = _fdiv(1.25 * v1[shift], sp4)
    if price[shift] < Smooth[0]:
        zc[shift] = 1.0
    elif price[shift] > Smooth[0]:
        zc[shift] = 2.0

def INIT__SUCCEEDED():
    PlaySound('ok.wav')
    cm = 'Subscribe! https://t.me/fxstill'
    Print(cm)
    Comment('\n' + cm)
    return INIT_SUCCEEDED

def ZerroIfEmpty(value):
    if value >= EMPTY_VALUE or value <= (-EMPTY_VALUE):
        return 0.0
    return value

def OnDeinit(reason):
    Comment('')
    if h != INVALID_HANDLE:
        IndicatorRelease(h)

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
        ArrayInitialize(zr, 0)
        ArrayInitialize(v1, EMPTY_VALUE)
        ArrayInitialize(i3, EMPTY_VALUE)
        ArrayInitialize(zc, 0)
        ArrayInitialize(q3, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersHilbertOscillator(_MQL5Indicator):
    name = 'EhlersHilbertOscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

