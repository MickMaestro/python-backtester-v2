"""Random walk index - jma smoothed — converted from MQL5: MQL5 Indicators/Random Walk Index - JMA Smoothed/Random walk index - jma smoothed.mq5

Random walk index - JMA smoothed
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329330], 2: [9662683]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Random walk index up', 2: 'Random walk index down'}, 'levels': [], 'description': ['Random walk index - JMA smoothed'], 'name': 'Random walk index - jma smoothed', 'source': 'MQL5 Indicators/Random Walk Index - JMA Smoothed/Random walk index - jma smoothed.mq5', 'folder': 'Random Walk Index - JMA Smoothed', 'inputs': [{'mql': 'inpRwiLength', 'py': 'inpRwiLength', 'param': 'inpRwiLength', 'type': 'int', 'default': 25, 'label': 'Random walk index period', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 14, 'label': 'Smooth period', 'sinput': False}, {'mql': 'inpSmoothPhase', 'py': 'inpSmoothPhase', 'param': 'inpSmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Smooth phase', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRwiLength = _input('inpRwiLength', 25)  # Random walk index period
inpSmoothPeriod = _input('inpSmoothPeriod', 14)  # Smooth period
inpSmoothPhase = _input('inpSmoothPhase', 0.0)  # Smooth phase
rwiUp = Arr(0, 0.0)
rwiDn = Arr(0, 0.0)
ranges = Arr(0, 0.0)
m_wrk = Arr(0, 0.0, dims=(20,))
m_size = 0

def OnInit():
    SetIndexBuffer(0, rwiUp, INDICATOR_DATA)
    SetIndexBuffer(1, rwiDn, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, ' JMA smoothed Random walk index (' + _str(inpRwiLength) + ',' + _str(inpSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArraySize(ranges) != rates_total:
        ArrayResize(ranges, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        ranges[i] = ((MathMax(high[i - 1], close[i - 2]) - MathMin(low[i - 1], close[i - 2])) if (i > 2) else 0)
        trwiUp = 0.0
        trwiDo = 0.0
        atr = ranges[i]
        k = 1
        while k < inpRwiLength and (i - k) >= 0:
            atr += ranges[i - k]
            denominator = _fdiv(atr, k + 1.0) * MathSqrt(k + 1)
            if denominator != 0:
                trwiUp = MathMax(trwiUp, _fdiv(high[i] - low[i - k], denominator))
                trwiDo = MathMax(trwiDo, _fdiv(high[i - k] - low[i], denominator))
            k += 1
        rwiUp[i] = iSmooth(trwiUp, inpSmoothPeriod, inpSmoothPhase, i, rates_total, 0)
        rwiDn[i] = iSmooth(trwiDo, inpSmoothPeriod, inpSmoothPhase, i, rates_total, 1)
    return rates_total

def iSmooth(price, length, phase, r, bars, instanceNo=0):
    if ArrayRange(m_wrk, 0) != bars:
        ArrayResize(m_wrk, bars)
    if ArrayRange(m_wrk, 0) != bars:
        return price
    instanceNo *= 10
    if r == 0 or length <= 1:
        k = 0
        while k < 7:
            m_wrk[r][instanceNo + k] = price
            k += 1
        while k < 10:
            m_wrk[r][instanceNo + k] = 0.0
            k += 1
        return price
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = price - m_wrk[r - 1][instanceNo + 5]
    del2 = price - m_wrk[r - 1][instanceNo + 6]
    forBar = MathMin(r, 10)
    m_wrk[r][instanceNo + 7] = 0.0
    if MathAbs(del1) > MathAbs(del2):
        m_wrk[r][instanceNo + 7] = MathAbs(del1)
    if MathAbs(del1) < MathAbs(del2):
        m_wrk[r][instanceNo + 7] = MathAbs(del2)
    m_wrk[r][instanceNo + 8] = m_wrk[r - 1][instanceNo + 8] + ((m_wrk[r][instanceNo + 7] - m_wrk[r - forBar][instanceNo + 7]) * 0.1)
    m_wrk[r][instanceNo + 9] = m_wrk[r - 1][instanceNo + 9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (m_wrk[r][instanceNo + 8] - m_wrk[r - 1][instanceNo + 9]))
    dVolty = (_fdiv(m_wrk[r][instanceNo + 7], m_wrk[r][instanceNo + 9]) if (m_wrk[r][instanceNo + 9] > 0) else 0)
    if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
        dVolty = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty < 1:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    if del1 > 0:
        m_wrk[r][instanceNo + 5] = price
    else:
        m_wrk[r][instanceNo + 5] = price - (Kv * del1)
    if del2 < 0:
        m_wrk[r][instanceNo + 6] = price
    else:
        m_wrk[r][instanceNo + 6] = price - (Kv * del2)
    corr = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    m_wrk[r][instanceNo + 0] = price + (alpha * (m_wrk[r - 1][instanceNo + 0] - price))
    m_wrk[r][instanceNo + 1] = ((price - m_wrk[r][instanceNo + 0]) * (1 - beta)) + (beta * m_wrk[r - 1][instanceNo + 1])
    m_wrk[r][instanceNo + 2] = m_wrk[r][instanceNo + 0] + (corr * m_wrk[r][instanceNo + 1])
    m_wrk[r][instanceNo + 3] = ((m_wrk[r][instanceNo + 2] - m_wrk[r - 1][instanceNo + 4]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * m_wrk[r - 1][instanceNo + 3])
    m_wrk[r][instanceNo + 4] = m_wrk[r - 1][instanceNo + 4] + m_wrk[r][instanceNo + 3]
    return m_wrk[r][instanceNo + 4]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RandomWalkIndexJmaSmoothed(_MQL5Indicator):
    name = 'Random walk index - jma smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRwiLength': 25,  # Random walk index period
        'inpSmoothPeriod': 14,  # Smooth period
        'inpSmoothPhase': 0.0,  # Smooth phase
    }

