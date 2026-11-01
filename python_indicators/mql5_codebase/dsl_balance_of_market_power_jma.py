"""Dsl - Balance of Market Power JMA — converted from MQL5: MQL5 Indicators/DSL Balance of market power JMA/Dsl - Balance of Market Power JMA.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 3329330, 42495]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'Balance of Market Power'}, 'levels': [], 'description': [], 'name': 'Dsl - Balance of Market Power JMA', 'source': 'MQL5 Indicators/DSL Balance of market power JMA/Dsl - Balance of Market Power JMA.mq5', 'folder': 'DSL Balance of market power JMA', 'inputs': [{'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 90, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpSigPeriod', 'py': 'inpSigPeriod', 'param': 'inpSigPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpSmoothPeriod = _input('inpSmoothPeriod', 90)  # Smoothing period
inpSigPeriod = _input('inpSigPeriod', 9)  # Signal period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
m_wrk = Arr(0, 0.0, dims=(20,))

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, '(dsl) Balance of Market Power JMA (' + _str(inpSmoothPeriod) + ',' + _str(inpSigPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alpha = _fdiv(2.0, 1.0 + inpSigPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        HighLowRange = high[i] - low[i]
        BullsRewardBasedOnOpen = (_fdiv(high[i] - open[i], HighLowRange) if (HighLowRange != 0) else 0)
        BearsRewardBasedOnOpen = (_fdiv(open[i] - low[i], HighLowRange) if (HighLowRange != 0) else 0)
        BullsRewardBasedOnClose = (_fdiv(close[i] - low[i], HighLowRange) if (HighLowRange != 0) else 0)
        BearsRewardBasedOnClose = (_fdiv(high[i] - close[i], HighLowRange) if (HighLowRange != 0) else 0)
        BullsRewardBasedOnOpenClose = ((_fdiv(close[i] - open[i], HighLowRange) if (close[i] > open[i]) else 0) if (HighLowRange != 0) else 0)
        BearsRewardBasedOnOpenClose = ((_fdiv(open[i] - close[i], HighLowRange) if (close[i] < open[i]) else 0) if (HighLowRange != 0) else 0)
        BullsRewardDaily = (BullsRewardBasedOnOpen + BullsRewardBasedOnClose + BullsRewardBasedOnOpenClose) / 3
        BearsRewardDaily = (BearsRewardBasedOnOpen + BearsRewardBasedOnClose + BearsRewardBasedOnOpenClose) / 3
        val[i] = iSmooth(BullsRewardDaily - BearsRewardDaily, inpSmoothPeriod, 0.0, i, rates_total)
        levelUp[i] = (((levelUp[i - 1] + (alpha * (val[i] - levelUp[i - 1]))) if (val[i] > 0) else levelUp[i - 1]) if (i > 0) else 0)
        levelDn[i] = (((levelDn[i - 1] + (alpha * (val[i] - levelDn[i - 1]))) if (val[i] < 0) else levelDn[i - 1]) if (i > 0) else 0)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
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


class DslBalanceOfMarketPowerJMA(_MQL5Indicator):
    name = 'Dsl - Balance of Market Power JMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpSmoothPeriod': 90,  # Smoothing period
        'inpSigPeriod': 9,  # Signal period
    }

