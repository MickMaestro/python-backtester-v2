"""Choppiness index - jma smoothed — converted from MQL5: MQL5 Indicators/Choppiness Index - JMA Smoothed/Choppiness index - jma smoothed.mq5

Choppiness index - JMA smoothed
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 3937500]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Choppiness index'}, 'levels': [], 'description': ['Choppiness index - JMA smoothed'], 'name': 'Choppiness index - jma smoothed', 'source': 'MQL5 Indicators/Choppiness Index - JMA Smoothed/Choppiness index - jma smoothed.mq5', 'folder': 'Choppiness Index - JMA Smoothed', 'inputs': [{'mql': 'inpChoPeriod', 'py': 'inpChoPeriod', 'param': 'inpChoPeriod', 'type': 'int', 'default': 14, 'label': 'Choppiness index period', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 14, 'label': 'Smooth period', 'sinput': False}, {'mql': 'inpSmoothPhase', 'py': 'inpSmoothPhase', 'param': 'inpSmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Smooth phase', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpChoPeriod = _input('inpChoPeriod', 14)  # Choppiness index period
inpSmoothPeriod = _input('inpSmoothPeriod', 14)  # Smooth period
inpSmoothPhase = _input('inpSmoothPhase', 0.0)  # Smooth phase
csi = Arr(0, 0.0)
csic = Arr(0, 0.0)
m_wrk = Arr(0, 0.0, dims=(10,))

def OnInit():
    SetIndexBuffer(0, csi, INDICATOR_DATA)
    SetIndexBuffer(1, csic, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Jma smoothed Choppiness index (' + _str(inpChoPeriod) + ',' + _str(inpSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _log = MathLog(inpChoPeriod) / 100.0
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        atrSum = 0.0
        maxHig = high[i]
        minLow = low[i]
        k = 0
        while k < inpChoPeriod and (i - k - 1) >= 0:
            atrSum += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
            maxHig = MathMax(maxHig, MathMax(high[i - k], close[i - k - 1]))
            minLow = MathMin(minLow, MathMin(low[i - k], close[i - k - 1]))
            k += 1
        _val = (_fdiv(atrSum, maxHig - minLow) if (maxHig != minLow) else 0)
        _csi = (_fdiv(MathLog(_val), _log) if (_val != 0) else 0)
        csi[i] = iSmooth(_csi, inpSmoothPeriod, inpSmoothPhase, i, rates_total, 0)
        csic[i] = ((0 if (csi[i] > csi[i - 1]) else 1 if (csi[i] < csi[i - 1]) else csic[i - 1]) if (i > 0) else 0)
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
    if r == (bars - 1):
        pass
    return m_wrk[r][instanceNo + 4]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChoppinessIndexJmaSmoothed(_MQL5Indicator):
    name = 'Choppiness index - jma smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpChoPeriod': 14,  # Choppiness index period
        'inpSmoothPeriod': 14,  # Smooth period
        'inpSmoothPhase': 0.0,  # Smooth phase
    }

