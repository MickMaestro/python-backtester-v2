"""Trend trigger factor JMA — converted from MQL5: MQL5 Indicators/Trend Trigger Factor JMA/Trend trigger factor JMA.mq5

Trend trigger factor JMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [16760576, 6333684], 2: [11119017], 3: [11119017, 16748574, 17919]}, 'widths': {2: 0, 3: 2}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Trend trigger factor levels'}, 'levels': [], 'description': ['Trend trigger factor JMA'], 'name': 'Trend trigger factor JMA', 'source': 'MQL5 Indicators/Trend Trigger Factor JMA/Trend trigger factor JMA.mq5', 'folder': 'Trend Trigger Factor JMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 15, 'label': 'Period', 'sinput': False}, {'mql': 'inpJmaPeriod', 'py': 'inpJmaPeriod', 'param': 'inpJmaPeriod', 'type': 'int', 'default': 5, 'label': 'JMA smoothing period', 'sinput': False}, {'mql': 'inpLevels', 'py': 'inpLevels', 'param': 'inpLevels', 'type': 'double', 'default': 100.0, 'label': 'Levels at +- (nnn)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 15)  # Period
inpJmaPeriod = _input('inpJmaPeriod', 5)  # JMA smoothing period
inpLevels = _input('inpLevels', 100.0)  # Levels at +- (nnn)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
lev = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
m_wrk = Arr(0, 0.0, dims=(10,))
m_size = 0

def OnInit():
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, lev, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend trigger factor (JMA)(' + _str(inpPeriod) + ',' + _str(inpJmaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - inpPeriod + 1, 0)
        _starto = MathMax(i - inpPeriod - inpPeriod + 1, 0)
        HighestHighRecent = high[ArrayMaximum(high, _start, inpPeriod)]
        HighestHighOlder = high[ArrayMaximum(high, _starto, inpPeriod)]
        LowestLowRecent = low[ArrayMinimum(low, _start, inpPeriod)]
        LowestLowOlder = low[ArrayMinimum(low, _starto, inpPeriod)]
        BuyPower = HighestHighRecent - LowestLowOlder
        SellPower = HighestHighOlder - LowestLowRecent
        ttf = (_fdiv(100 * (BuyPower - SellPower), 0.5 * (BuyPower + SellPower)) if ((BuyPower + SellPower) != 0) else 0)
        val[i] = iSmooth(ttf, inpJmaPeriod, 0.0, i, rates_total)
        valc[i] = (1 if (val[i] > inpLevels) else 2 if (val[i] < (-inpLevels)) else 0)
        lev[i] = (inpLevels if (val[i] > 0) else (-inpLevels) if (val[i] < 0) else 0)
        fup[i] = val[i]
        fdn[i] = (MathMin(val[i], inpLevels) if (val[i] > 0) else MathMax(val[i], -inpLevels))
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


class TrendTriggerFactorJMA(_MQL5Indicator):
    name = 'Trend trigger factor JMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 15,  # Period
        'inpJmaPeriod': 5,  # JMA smoothing period
        'inpLevels': 100.0,  # Levels at +- (nnn)
    }

