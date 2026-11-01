"""RSX range expansion index - cb — converted from MQL5: MQL5 Indicators/RSX range expansion index - with confidence bands/RSX range expansion index - cb.mq5

RSX Range expansion index (REI)
With confidence bands
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [2263842], 2: [11119017], 3: [3937500], 4: [11119017, 3937500, 2263842]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Level up', 2: 'Middle level', 3: 'Level down', 4: 'REI'}, 'levels': [], 'description': ['RSX Range expansion index (REI)', 'With confidence bands'], 'name': 'RSX range expansion index - cb', 'source': 'MQL5 Indicators/RSX range expansion index - with confidence bands/RSX range expansion index - cb.mq5', 'folder': 'RSX range expansion index - with confidence bands', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 32.0, 'label': 'REI period', 'sinput': False}, {'mql': 'inpConfidenceLevel', 'py': 'inpConfidenceLevel', 'param': 'inpConfidenceLevel', 'type': 'double', 'default': 95.0, 'label': 'Confidence level', 'sinput': False}, {'mql': 'inpConfidenceBandsShift', 'py': 'inpConfidenceBandsShift', 'param': 'inpConfidenceBandsShift', 'type': 'int', 'default': 2, 'label': 'Confidence level shift', 'sinput': False}, {'mql': 'inpColorMode', 'py': 'inpColorMode', 'param': 'inpColorMode', 'type': 'int', 'default': 0, 'label': 'Change color mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorMode
col_onZero = 0
col_onOuter = 1
_enum('enColorMode', {0: 'col_onZero', 1: 'col_onOuter'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32.0)  # REI period
inpConfidenceLevel = _input('inpConfidenceLevel', 95.0)  # Confidence level
inpConfidenceBandsShift = _input('inpConfidenceBandsShift', 2)  # Confidence level shift
inpColorMode = _input('inpColorMode', col_onZero)  # Change color mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
flup = Arr(0, 0.0)
flmi = Arr(0, 0.0)
fldn = Arr(0, 0.0)
ConfidenceZ = 0.0
ConfidenceLevel = 0.0
ConfidenceBandsShift = 0
workRsi = Arr(5, 0.0, dyn=False, dims=(26,))
_cbc = Arr.of([2.515517, 0.802853, 0.010328], fill=0.0)
_cbd = Arr.of([1.432788, 0.189269, 0.001308], fill=0.0)

def OnInit():
    global ConfidenceBandsShift, ConfidenceLevel, ConfidenceZ
    SetIndexBuffer(0, flup, INDICATOR_DATA)
    SetIndexBuffer(1, flmi, INDICATOR_DATA)
    SetIndexBuffer(2, fldn, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    ConfidenceLevel = MathMax(MathMin(inpConfidenceLevel, 99.9999999999), 1e-10)
    ConfidenceBandsShift = MathMax(inpConfidenceBandsShift, 1)
    ConfidenceZ = NormalCDFInverse((ConfidenceLevel + ((100 - ConfidenceLevel) / 2.0)) / 100.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSX Range expansion index (' + _str(inpPeriod) + ' with ' + _str(inpConfidenceLevel) + ' confidence bands)')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        val[i] = iRsx(high[i], inpPeriod, i, 0) + iRsx(low[i], inpPeriod, i, 1) - 100
        va = (((val[i - ConfidenceBandsShift] + 100.0) / 200.0) if ((i - ConfidenceBandsShift) >= 0) else 0)
        me = ConfidenceZ * MathSqrt((va * (1.0 - va)) / inpPeriod) * 100.0
        flup[i] = ((val[i - ConfidenceBandsShift] + me) if ((i - ConfidenceBandsShift) >= 0) else val[i])
        fldn[i] = ((val[i - ConfidenceBandsShift] - me) if ((i - ConfidenceBandsShift) >= 0) else val[i])
        flmi[i] = (flup[i] + fldn[i]) / 2.0
        _sw1 = inpColorMode
        if _sw1 == col_onOuter:
            valc[i] = (2 if (val[i] > flup[i]) else 1 if (val[i] < fldn[i]) else 0)
        elif _sw1 == col_onZero:
            valc[i] = (2 if (val[i] > flmi[i]) else 1 if (val[i] < flmi[i]) else valc[i - 1] if (i > 0) else 0)
    return rates_total

def iRsx(price, period, i, instanceNo=0):
    _indP = _int(MathMod(i - 1, 5))
    _indC = _int(MathMod(i, 5))
    _inst = instanceNo * 13
    if i < period:
        for k in range(1, 13):
            workRsi[_indC][_inst + k] = 0.0
        return 50.0
    workRsi[_indC][_inst] = price
    Kg = _fdiv(3.0, 2.0 + period)
    Hg = 1.0 - Kg
    mom = workRsi[_indC][_inst] - workRsi[_indP][_inst]
    moa = MathAbs(mom)
    for k in range(0, 3):
        kk = _inst + (k * 2)
        workRsi[_indC][kk + 1] = (Kg * mom) + (Hg * workRsi[_indP][kk + 1])
        workRsi[_indC][kk + 2] = (Kg * workRsi[_indC][kk + 1]) + (Hg * workRsi[_indP][kk + 2])
        mom = (1.5 * workRsi[_indC][kk + 1]) - (0.5 * workRsi[_indC][kk + 2])
        workRsi[_indC][kk + 7] = (Kg * moa) + (Hg * workRsi[_indP][kk + 7])
        workRsi[_indC][kk + 8] = (Kg * workRsi[_indC][kk + 7]) + (Hg * workRsi[_indP][kk + 8])
        moa = (1.5 * workRsi[_indC][kk + 7]) - (0.5 * workRsi[_indC][kk + 8])
    return MathMax(MathMin((_fdiv(mom, MathMax(moa, DBL_MIN)) + 1.0) * 50.0, 100.0), 0.0)

def RationalApproximation(t):
    return t - _fdiv((((_cbc[2] * t) + _cbc[1]) * t) + _cbc[0], (((((_cbd[2] * t) + _cbd[1]) * t) + _cbd[0]) * t) + 1.0)

def NormalCDFInverse(p):
    if p <= 0.0 or p >= 1.0:
        return 0.0
    if p < 0.5:
        return -RationalApproximation(MathSqrt(-2.0 * MathLog(p)))
    else:
        return RationalApproximation(MathSqrt(-2.0 * MathLog(1.0 - p)))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSXRangeExpansionIndexCb(_MQL5Indicator):
    name = 'RSX range expansion index - cb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 32.0,  # REI period
        'inpConfidenceLevel': 95.0,  # Confidence level
        'inpConfidenceBandsShift': 2,  # Confidence level shift
        'inpColorMode': _Choice({0: 'Change color on middle line cross', 1: 'Change color on outer levels cross'}, default=0),  # Change color mode
    }

