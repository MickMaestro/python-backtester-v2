"""Trend direction and force - JMA smoothed — converted from MQL5: MQL5 Indicators/Trend direction and force - JMA smoothed/Trend direction and force - JMA smoothed.mq5

Trend direction and force - JMA smoothed
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 8}, 'colors': {1: [14474460], 2: [11119017, 6333684, 16760576]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'No trend zone', 2: 'Trend direction and force'}, 'levels': [], 'description': ['Trend direction and force - JMA smoothed'], 'name': 'Trend direction and force - JMA smoothed', 'source': 'MQL5 Indicators/Trend direction and force - JMA smoothed/Trend direction and force - JMA smoothed.mq5', 'folder': 'Trend direction and force - JMA smoothed', 'inputs': [{'mql': 'trendPeriod', 'py': 'trendPeriod', 'param': 'trendPeriod', 'type': 'int', 'default': 20, 'label': 'Trend period', 'sinput': False}, {'mql': 'smoothPeriod', 'py': 'smoothPeriod', 'param': 'smoothPeriod', 'type': 'int', 'default': 3, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'TriggerUp', 'py': 'TriggerUp', 'param': 'TriggerUp', 'type': 'double', 'default': 0.05, 'label': 'Trigger up level', 'sinput': False}, {'mql': 'TriggerDown', 'py': 'TriggerDown', 'param': 'TriggerDown', 'type': 'double', 'default': -0.05, 'label': 'Trigger down level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
trendPeriod = _input('trendPeriod', 20)  # Trend period
smoothPeriod = _input('smoothPeriod', 3)  # Smoothing period
TriggerUp = _input('TriggerUp', 0.05)  # Trigger up level
TriggerDown = _input('TriggerDown', -0.05)  # Trigger down level
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levup = Arr(0, 0.0)
levdn = Arr(0, 0.0)
workTrend = Arr(0, 0.0, dims=(3,))
m_wrk = Arr(0, 0.0, dims=(10,))
m_size = 0

def OnInit():
    SetIndexBuffer(0, levup, INDICATOR_DATA)
    SetIndexBuffer(1, levdn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend direction and force JMA smoothed (' + _str(trendPeriod) + ',' + _str(smoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(workTrend, 0) != rates_total:
        ArrayResize(workTrend, rates_total)
    _alpha = 2.0 / (1 + trendPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        workTrend[i][0] = ((workTrend[i - 1][0] + (_alpha * (close[i] - workTrend[i - 1][0]))) if (i > 0) else close[i])
        workTrend[i][1] = ((workTrend[i - 1][1] + (_alpha * (workTrend[i][0] - workTrend[i - 1][1]))) if (i > 0) else workTrend[i][0])
        impetmma = ((workTrend[i][0] - workTrend[i - 1][0]) if (i > 0) else 0)
        impetsmma = ((workTrend[i][1] - workTrend[i - 1][1]) if (i > 0) else 0)
        divma = _fdiv(MathAbs(workTrend[i][0] - workTrend[i][1]), Point())
        averimpet = _fdiv(impetmma + impetsmma, 2 * Point())
        workTrend[i][2] = divma * MathPow(averimpet, 3)
        absValue = 0.0
        k = 0
        while k < (trendPeriod * 3) and (i - k) >= 0:
            absValue = MathMax(absValue, MathAbs(workTrend[i - k][2]))
            k += 1
        val[i] = iSmooth((_fdiv(workTrend[i][2], absValue) if (absValue > 0) else 0), smoothPeriod, 0.0, i, rates_total)
        levup[i] = TriggerUp
        levdn[i] = TriggerDown
        valc[i] = (2 if (val[i] > levup[i]) else 1 if (val[i] < levdn[i]) else 0)
        i += 1
    return i

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


class TrendDirectionAndForceJMASmoothed(_MQL5Indicator):
    name = 'Trend direction and force - JMA smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'trendPeriod': 20,  # Trend period
        'smoothPeriod': 3,  # Smoothing period
        'TriggerUp': 0.05,  # Trigger up level
        'TriggerDown': -0.05,  # Trigger down level
    }

