"""GARCH_vol_threshold — converted from MQL5: MQL5 Indicators/GARCH Indicator - Industrial Level Volatility Estimator/GARCH_vol_threshold.mq5

Copyright: Copyright 2025, Serhad Yildirim

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, Serhad Yildirim', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [10526303], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'GARCH_Vol', 2: 'Threshold'}, 'levels': [], 'description': [], 'name': 'GARCH_vol_threshold', 'source': 'MQL5 Indicators/GARCH Indicator - Industrial Level Volatility Estimator/GARCH_vol_threshold.mq5', 'folder': 'GARCH Indicator - Industrial Level Volatility Estimator', 'inputs': [{'mql': 'InpGamma', 'py': 'InpGamma', 'param': 'InpGamma', 'type': 'double', 'default': 9.3493e-07, 'label': 'Gamma: constant term (unconditional variance)', 'sinput': False}, {'mql': 'InpAlpha1', 'py': 'InpAlpha1', 'param': 'InpAlpha1', 'type': 'double', 'default': 0.065834, 'label': 'Alpha: ARCH coefficient (reaction to last shock²)', 'sinput': False}, {'mql': 'beta1', 'py': 'beta1', 'param': 'beta1', 'type': 'double', 'default': 0.921607, 'label': 'Beta: GARCH coefficient (persistence of past variance)', 'sinput': False}, {'mql': 'InpWindowBars', 'py': 'InpWindowBars', 'param': 'InpWindowBars', 'type': 'int', 'default': 1000, 'label': 'Bar window: How many bars to include in rolling mean/std', 'sinput': False}, {'mql': 'InpK', 'py': 'InpK', 'param': 'InpK', 'type': 'double', 'default': 1.0, 'label': 'Threshold: meanVol + StdMultiplier * stdVol', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
VolBuf = Arr(0, 0.0)
ThreshBuf = Arr(0, 0.0)
winVol = Arr(0, 0.0)
bufPos = 0
bufFull = False
VolLookback = 0
historyDays = 0.0
sigma_prev = 0.0
meanVol = 0.0
M2Vol = 0.0
countVol = 0
InpGamma = _input('InpGamma', 9.3493e-07)  # Gamma: constant term (unconditional variance)
InpAlpha1 = _input('InpAlpha1', 0.065834)  # Alpha: ARCH coefficient (reaction to last shock²)
beta1 = _input('beta1', 0.921607)  # Beta: GARCH coefficient (persistence of past variance)
InpWindowBars = _input('InpWindowBars', 1000)  # Bar window: How many bars to include in rolling mean/std
InpK = _input('InpK', 1.0)  # Threshold: meanVol + StdMultiplier * stdVol

def OnInit():
    global M2Vol, VolLookback, bufFull, bufPos, countVol, historyDays, meanVol, sigma_prev
    historyDays = GetHistoryDays(Period())
    tfMinutes = float(PeriodSeconds(Period())) / 60.0
    VolLookback = _int(MathCeil(historyDays * _fdiv(1440.0, tfMinutes)))
    VolLookback = MathMin(VolLookback, Bars(Symbol(), Period()) - 3)
    VolLookback = MathMax(VolLookback, 10)
    if VolLookback < 2:
        Print('VolLookback too small: ', VolLookback)
        return INIT_PARAMETERS_INCORRECT
    if ((InpGamma <= 0 or InpAlpha1 < 0) or beta1 < 0) or (InpAlpha1 + beta1) >= 1.0:
        Print('Invalid GARCH params: require α₀>0, α₁≥0, β₁≥0, α₁+β₁<1')
        return INIT_PARAMETERS_INCORRECT
    ArrayResize(winVol, VolLookback)
    ArrayInitialize(winVol, 0.0)
    bufPos = 0
    bufFull = False
    countVol = 0
    meanVol = 0.0
    M2Vol = 0.0
    sigma_prev = MathSqrt(_fdiv(InpGamma, 1.0 - InpAlpha1 - beta1))
    SetIndexBuffer(0, VolBuf, INDICATOR_DATA)
    SetIndexBuffer(1, ThreshBuf, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArrayInitialize(VolBuf, EMPTY_VALUE)
    ArrayInitialize(ThreshBuf, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, VolLookback)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, VolLookback)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global M2Vol, bufFull, bufPos, countVol, meanVol, sigma_prev
    start = MathMax(3, VolLookback)
    begin = (prev_calculated if (prev_calculated > 0) else start)
    for i in range(begin, rates_total):
        Z_t1 = MathLog(_fdiv(close[i - 1], close[i - 2]))
        var_i = InpGamma + (InpAlpha1 * Z_t1 * Z_t1) + (beta1 * sigma_prev * sigma_prev)
        sigma_i = MathSqrt(var_i)
        VolBuf[i] = sigma_i
        sigma_prev = sigma_i
        if countVol < VolLookback:
            countVol += 1
            delta = sigma_i - meanVol
            meanVol += _fdiv(delta, countVol)
            M2Vol += delta * (sigma_i - meanVol)
            winVol[bufPos] = sigma_i
            if countVol == VolLookback:
                bufFull = True
        else:
            old = winVol[bufPos]
            deltaR = old - meanVol
            meanVol -= _fdiv(deltaR, VolLookback)
            M2Vol -= deltaR * (old - meanVol)
            deltaA = sigma_i - meanVol
            meanVol += _fdiv(deltaA, VolLookback)
            M2Vol += deltaA * (sigma_i - meanVol)
            winVol[bufPos] = sigma_i
        bufPos = _imod(bufPos + 1, VolLookback)
        if countVol >= 2:
            varV = _fdiv(M2Vol, countVol - 1)
            varV = MathMax(varV, 0.0)
            sdV = MathSqrt(varV)
            ThreshBuf[i] = meanVol + (InpK * sdV)
        else:
            ThreshBuf[i] = EMPTY_VALUE
    return rates_total

def GetHistoryDays(period):
    _sw1 = period
    if _sw1 in (PERIOD_M1, PERIOD_M5, PERIOD_M15):
        return 1.0
    elif _sw1 == PERIOD_M30:
        return 7.0
    elif _sw1 in (PERIOD_H1, PERIOD_H4):
        return 14.0
    elif _sw1 == PERIOD_D1:
        return 252.0
    elif _sw1 == PERIOD_W1:
        return 252.0 * 2
    elif _sw1 == PERIOD_MN1:
        return 252.0 * 5
    else:
        return 252.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GARCHVolThreshold(_MQL5Indicator):
    name = 'GARCH_vol_threshold'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpGamma': 9.3493e-07,  # Gamma: constant term (unconditional variance)
        'InpAlpha1': 0.065834,  # Alpha: ARCH coefficient (reaction to last shock²)
        'beta1': 0.921607,  # Beta: GARCH coefficient (persistence of past variance)
        'InpWindowBars': 1000,  # Bar window: How many bars to include in rolling mean/std
        'InpK': 1.0,  # Threshold: meanVol + StdMultiplier * stdVol
    }

