"""Range oscillator + bands smoothed — converted from MQL5: MQL5 Indicators/Range Oscillator + Bands (Smoothed)/Range oscillator + bands smoothed.mq5

Range oscillator with bands (smoothed version)
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [16748574], 2: [11119017], 3: [6333684], 4: [11119017, 16748574, 6333684]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Band up', 2: 'Average range oscillator', 3: 'Band down', 4: 'Range oscillator'}, 'levels': [], 'description': ['Range oscillator with bands (smoothed version)'], 'name': 'Range oscillator + bands smoothed', 'source': 'MQL5 Indicators/Range Oscillator + Bands (Smoothed)/Range oscillator + bands smoothed.mq5', 'folder': 'Range Oscillator + Bands (Smoothed)', 'inputs': [{'mql': 'inpRngPeriod', 'py': 'inpRngPeriod', 'param': 'inpRngPeriod', 'type': 'int', 'default': 40, 'label': 'Range oscillator period', 'sinput': False}, {'mql': 'inpBandsPeriod', 'py': 'inpBandsPeriod', 'param': 'inpBandsPeriod', 'type': 'int', 'default': 20, 'label': 'Bands period', 'sinput': False}, {'mql': 'inpBandsDeviations', 'py': 'inpBandsDeviations', 'param': 'inpBandsDeviations', 'type': 'double', 'default': 2.0, 'label': 'Bands deviation', 'sinput': False}, {'mql': 'inpSmtPeriod', 'py': 'inpSmtPeriod', 'param': 'inpSmtPeriod', 'type': 'int', 'default': 14, 'label': 'Smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRngPeriod = _input('inpRngPeriod', 40)  # Range oscillator period
inpBandsPeriod = _input('inpBandsPeriod', 20)  # Bands period
inpBandsDeviations = _input('inpBandsDeviations', 2.0)  # Bands deviation
inpSmtPeriod = _input('inpSmtPeriod', 14)  # Smoothing period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
bandu = Arr(0, 0.0)
bandm = Arr(0, 0.0)
bandd = Arr(0, 0.0)
m_wrk = Arr(0, 0.0, dims=(10,))
m_size = 0
workSma = Arr(0, 0.0, dims=(1,))
workDev = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, bandu, INDICATOR_DATA)
    SetIndexBuffer(1, bandm, INDICATOR_DATA)
    SetIndexBuffer(2, bandd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range oscillator + bands (smoothed)(' + _str(inpRngPeriod) + ',' + _str(inpBandsPeriod) + ',' + _str(inpSmtPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _start = MathMax(i - inpRngPeriod + 1, 0)
        _max = high[ArrayMaximum(high, _start, inpRngPeriod)]
        _min = low[ArrayMinimum(low, _start, inpRngPeriod)]
        _med = (high[i] + low[i]) / 2
        val[i] = iSmooth((_fdiv(100 * (_med - _min), _max - _min) if (_max != _min) else 0), inpSmtPeriod, 0.0, i, rates_total, 0)
        bandm[i] = iSma(val[i], inpBandsPeriod, i, rates_total)
        _dev = iDeviation(val[i], inpBandsPeriod, i, rates_total)
        bandu[i] = bandm[i] + (inpBandsDeviations * _dev)
        bandd[i] = bandm[i] - (inpBandsDeviations * _dev)
        valc[i] = (1 if (val[i] > bandu[i]) else 2 if (val[i] < bandd[i]) else 0)
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

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iDeviation(value, length, i, bars, isSample=False):
    if ArraySize(workDev) != bars:
        ArrayResize(workDev, bars)
    workDev[i] = value
    sumx = 0.0
    sumxx = 0.0
    k = 0
    while k < length and (i - k) >= 0:
        pass
        sumx += workDev[i - k]
        sumxx += workDev[i - k] * workDev[i - k]
        k += 1
    return MathSqrt(_fdiv(sumxx - _fdiv(sumx * sumx, length), MathMax(length - isSample, 1)))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangeOscillatorBandsSmoothed(_MQL5Indicator):
    name = 'Range oscillator + bands smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRngPeriod': 40,  # Range oscillator period
        'inpBandsPeriod': 20,  # Bands period
        'inpBandsDeviations': 2.0,  # Bands deviation
        'inpSmtPeriod': 14,  # Smoothing period
    }

