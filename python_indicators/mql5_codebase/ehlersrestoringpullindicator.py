"""EhlersRestoringPullIndicator — converted from MQL5: MQL5 Indicators/The Restoring Pull Indicator/EhlersRestoringPullIndicator.mq5

The Restoring Pull Indicator:\\nJohn Ehlers, \\"Stocks & Commodities V.11:10 (395-400)\\"
Copyright: Copyright 2020, Andrei Novichkov.; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [32768, 255, 3329330], 2: [16748574]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'V1', 2: 'V2'}, 'levels': [], 'description': ['The Restoring Pull Indicator:\\nJohn Ehlers, \\"Stocks & Commodities V.11:10 (395-400)\\"'], 'name': 'EhlersRestoringPullIndicator', 'source': 'MQL5 Indicators/The Restoring Pull Indicator/EhlersRestoringPullIndicator.mq5', 'folder': 'The Restoring Pull Indicator', 'inputs': [{'mql': 'minperiod', 'py': 'minperiod', 'param': 'minperiod', 'type': 'int', 'default': 8, 'label': 'MinPeriod', 'sinput': False}, {'mql': 'maxperiod', 'py': 'maxperiod', 'param': 'maxperiod', 'type': 'int', 'default': 50, 'label': 'MaxPeriod', 'sinput': False}, {'mql': 'hpPeriod', 'py': 'hpPeriod', 'param': 'hpPeriod', 'type': 'int', 'default': 40, 'label': 'HpPeriod', 'sinput': False}, {'mql': 'medianPeriod', 'py': 'medianPeriod', 'param': 'medianPeriod', 'type': 'int', 'default': 10, 'label': 'MedianPeriod', 'sinput': False}, {'mql': 'decibelPeriod', 'py': 'decibelPeriod', 'param': 'decibelPeriod', 'type': 'int', 'default': 20, 'label': 'DecibelPeriod', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
minperiod = _input('minperiod', 8)  # MinPeriod
maxperiod = _input('maxperiod', 50)  # MaxPeriod
hpPeriod = _input('hpPeriod', 40)  # HpPeriod
medianPeriod = _input('medianPeriod', 10)  # MedianPeriod
decibelPeriod = _input('decibelPeriod', 20)  # DecibelPeriod
v1 = Arr(0, 0.0)
v2 = Arr(0, 0.0)
tc = Arr(0, 0.0)
smoothHp = Arr(0, 0.0)
hp = Arr(0, 0.0)
dc = Arr(0, 0.0)
Q = Arr(0, 0.0)
I = Arr(0, 0.0)
Real = Arr(0, 0.0)
Imag = Arr(0, 0.0)
Ampl = Arr(0, 0.0)
OldQ = Arr(0, 0.0)
OldI = Arr(0, 0.0)
OlderQ = Arr(0, 0.0)
OlderI = Arr(0, 0.0)
OldReal = Arr(0, 0.0)
OldImag = Arr(0, 0.0)
OlderReal = Arr(0, 0.0)
OlderImag = Arr(0, 0.0)
OldAmpl = Arr(0, 0.0)
DB = Arr(0, 0.0)
MINBAR = maxperiod + 1
a1 = 0.0
a2 = 0.0

def OnInit():
    global a1, a2
    SetIndexBuffer(0, v1, INDICATOR_DATA)
    SetIndexBuffer(1, tc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, v2, INDICATOR_DATA)
    SetIndexBuffer(3, smoothHp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, dc, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, hp, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(v1, True)
    ArraySetAsSeries(tc, True)
    ArraySetAsSeries(v2, True)
    ArraySetAsSeries(smoothHp, True)
    ArraySetAsSeries(dc, True)
    ArraySetAsSeries(hp, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersRestoringPullIndicator')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    a1 = _fdiv(1 - MathSin((2 * M_PI) / hpPeriod), MathCos((2 * M_PI) / hpPeriod))
    a2 = 0.5 * (1 + a1)
    InitArrays()
    return INIT_SUCCEEDED

def InitArrays():
    ArrayResize(Q, maxperiod + 1)
    ArraySetAsSeries(Q, True)
    ArrayInitialize(Q, 0)
    ArrayResize(I, maxperiod + 1)
    ArraySetAsSeries(I, True)
    ArrayInitialize(I, 0)
    ArrayResize(Real, maxperiod + 1)
    ArraySetAsSeries(Real, True)
    ArrayInitialize(Real, 0)
    ArrayResize(Imag, maxperiod + 1)
    ArraySetAsSeries(Imag, True)
    ArrayInitialize(Imag, 0)
    ArrayResize(Ampl, maxperiod + 1)
    ArraySetAsSeries(Ampl, True)
    ArrayInitialize(Ampl, 0)
    ArrayResize(OldQ, maxperiod + 1)
    ArraySetAsSeries(OldQ, True)
    ArrayInitialize(OldQ, 0)
    ArrayResize(OldI, maxperiod + 1)
    ArraySetAsSeries(OldI, True)
    ArrayInitialize(OldI, 0)
    ArrayResize(OlderQ, maxperiod + 1)
    ArraySetAsSeries(OlderQ, True)
    ArrayInitialize(OlderQ, 0)
    ArrayResize(OlderI, maxperiod + 1)
    ArraySetAsSeries(OlderI, True)
    ArrayInitialize(OlderI, 0)
    ArrayResize(OldReal, maxperiod + 1)
    ArraySetAsSeries(OldReal, True)
    ArrayInitialize(OldReal, 0)
    ArrayResize(OldImag, maxperiod + 1)
    ArraySetAsSeries(OldImag, True)
    ArrayInitialize(OldImag, 0)
    ArrayResize(OlderReal, maxperiod + 1)
    ArraySetAsSeries(OlderReal, True)
    ArrayInitialize(OlderReal, 0)
    ArrayResize(OlderImag, maxperiod + 1)
    ArraySetAsSeries(OlderImag, True)
    ArrayInitialize(OlderImag, 0)
    ArrayResize(OldAmpl, maxperiod + 1)
    ArraySetAsSeries(OldAmpl, True)
    ArrayInitialize(OldAmpl, 0)
    ArrayResize(DB, maxperiod + 1)
    ArraySetAsSeries(DB, True)
    ArrayInitialize(DB, 0)

def GetValue(h, l, v, shift):
    p0 = (h[shift] + l[shift]) / 2
    p1 = (h[shift + 1] + l[shift + 1]) / 2
    hp[shift] = (a2 * (p0 - p1)) + (a1 * hp[shift + 1])
    smoothHp[shift] = (hp[shift] + (2 * hp[shift + 1]) + (3 * hp[shift + 2]) + (3 * hp[shift + 3]) + (2 * hp[shift + 4]) + hp[shift + 5]) / 12
    delta = (-0.015 * shift) + 0.5
    if delta < 0.15:
        delta = 0.15
    num = 0.0
    denom = 0.0
    maxAmpl = 0.0
    s1 = smoothHp[shift] - smoothHp[shift + 1]
    beta = 0.0
    gamma = 0.0
    alpha = 0.0
    for n in range(minperiod, maxperiod + 1):
        beta = MathCos(_fdiv(2 * M_PI, n))
        gamma = _fdiv(1, MathCos(_fdiv(4 * M_PI * delta, n)))
        alpha = gamma - MathSqrt(MathPow(gamma, 2) - 1)
        Q[n] = (n / 6.283185) * s1
        I[n] = smoothHp[shift]
        Real[n] = (0.5 * (1 - alpha) * (I[n] - OlderI[n])) + (beta * (1 + alpha) * OldReal[n]) - (alpha * OlderReal[n])
        Imag[n] = (0.5 * (1 - alpha) * (Q[n] - OlderQ[n])) + (beta * (1 + alpha) * OldImag[n]) - (alpha * OlderImag[n])
        Ampl[n] = MathPow(Real[n], 2) + MathPow(Imag[n], 2)
    MaxAmpl = Ampl[medianPeriod]
    for n in range(minperiod, maxperiod + 1):
        OlderI[n] = OldI[n]
        OldI[n] = I[n]
        OlderQ[n] = OldQ[n]
        OldQ[n] = Q[n]
        OlderReal[n] = OldReal[n]
        OldReal[n] = Real[n]
        OlderImag[n] = OldImag[n]
        OldImag[n] = Imag[n]
        OldAmpl[n] = Ampl[n]
        if Ampl[n] > MaxAmpl:
            MaxAmpl = Ampl[n]
    for n in range(minperiod, maxperiod + 1):
        if MaxAmpl != 0:
            t = 1 - _fdiv(0.99 * Ampl[n], MaxAmpl)
            if t != 0:
                DB[n] = _fdiv((-medianPeriod) * MathLog(_fdiv(0.01, t)), MathLog(10))
        if DB[n] > decibelPeriod:
            DB[n] = decibelPeriod
        if DB[n] <= 3:
            num = num + (n * (decibelPeriod - DB[n]))
            denom = denom + (decibelPeriod - DB[n])
    if denom != 0:
        dc[shift] = _fdiv(num, denom)
    domCyc = MathMedian(dc, shift, medianPeriod)
    if domCyc < minperiod:
        domCyc = decibelPeriod
    beta = MathCos(_fdiv(2 * M_PI, domCyc))
    gamma = _fdiv(1, MathCos(_fdiv(4 * M_PI * delta, domCyc)))
    alpha = gamma - MathSqrt(MathPow(gamma, 2) - 1)
    v1[shift] = v[shift] * MathPow(_fdiv(2 * M_PI, domCyc), 2)
    v2[shift] = SimpleMA(shift, minperiod, v1)
    if v1[shift] < v2[shift]:
        tc[shift] = 2.0
    elif v1[shift] > v2[shift]:
        tc[shift] = 1.0

def SimpleMA(position, period, price):
    result = 0.0
    for i in range(0, period):
        result += price[position + i]
    result = _fdiv(result, period)
    return result

def MathMedian(array, start, count=WHOLE_ARRAY):
    size = ArraySize(array)
    if size < count:
        return EMPTY_VALUE
    sorted_values = Arr(0, 0.0)
    if ArrayCopy(sorted_values, array, 0, start, count) != count:
        return EMPTY_VALUE
    ArraySort(sorted_values)
    size = ArraySize(sorted_values)
    if _imod(size, 2) == 1:
        return sorted_values[_idiv(size, 2)]
    else:
        return 0.5 * (sorted_values[_idiv(size - 1, 2)] + sorted_values[_idiv(size + 1, 2)])

def ZerroIfEmpty(value):
    if value >= EMPTY_VALUE or value <= (-EMPTY_VALUE):
        return 0.0
    return value

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < MINBAR:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(volume, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        GetValue(high, low, tick_volume, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(v1, EMPTY_VALUE)
        ArrayInitialize(v2, EMPTY_VALUE)
        ArrayInitialize(smoothHp, 0)
        ArrayInitialize(tc, 0)
        ArrayInitialize(dc, 0)
        ArrayInitialize(hp, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(high, low, tick_volume, i)
        return rates_total
    GetValue(high, low, tick_volume, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersRestoringPullIndicator(_MQL5Indicator):
    name = 'EhlersRestoringPullIndicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'minperiod': 8,  # MinPeriod
        'maxperiod': 50,  # MaxPeriod
        'hpPeriod': 40,  # HpPeriod
        'medianPeriod': 10,  # MedianPeriod
        'decibelPeriod': 20,  # DecibelPeriod
    }

