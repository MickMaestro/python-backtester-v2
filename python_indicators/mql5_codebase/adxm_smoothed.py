"""ADXm smoothed — converted from MQL5: MQL5 Indicators/ADXm smoothed/ADXm smoothed.mq5

ADXm smoothed
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [11119017], 2: [11119017, 16748574, 6333684]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'DI', 2: 'ADXm'}, 'levels': [], 'description': ['ADXm smoothed'], 'name': 'ADXm smoothed', 'source': 'MQL5 Indicators/ADXm smoothed/ADXm smoothed.mq5', 'folder': 'ADXm smoothed', 'inputs': [{'mql': 'inpAdxmPeriod', 'py': 'inpAdxmPeriod', 'param': 'inpAdxmPeriod', 'type': 'int', 'default': 14, 'label': 'ADXm period', 'sinput': False}, {'mql': 'inpAdxmSmooth', 'py': 'inpAdxmSmooth', 'param': 'inpAdxmSmooth', 'type': 'int', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpAdxmSmoothPhase', 'py': 'inpAdxmSmoothPhase', 'param': 'inpAdxmSmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Smoothing phase', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAdxmPeriod = _input('inpAdxmPeriod', 14)  # ADXm period
inpAdxmSmooth = _input('inpAdxmSmooth', 5)  # Smoothing period
inpAdxmSmoothPhase = _input('inpAdxmSmoothPhase', 0.0)  # Smoothing phase
adxm = Arr(0, 0.0)
adxmc = Arr(0, 0.0)
di = Arr(0, 0.0)
_adxmWork = Arr(0, 0.0, dims=(8,))
m_wrk = Arr(0, 0.0, dims=(10,))
m_size = 0

def OnInit():
    SetIndexBuffer(0, di, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, adxm, INDICATOR_DATA)
    SetIndexBuffer(2, adxmc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ADXm smoothed (' + _str(inpAdxmPeriod) + ',' + _str(inpAdxmSmooth) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _di = Box(0.0)
        adxm[i] = iSmooth(iAdxm(close[i], high[i], low[i], inpAdxmPeriod, _di, i, rates_total), inpAdxmSmooth, inpAdxmSmoothPhase, i, rates_total)
        di[i] = _di.v
        adxmc[i] = ((1 if (adxm[i] > adxm[i - 1]) else 2 if (adxm[i] < adxm[i - 1]) else adxmc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iAdxm(_close, _high, _low, _period, _di, i, bars, instanceNo=0):
    if ArrayRange(_adxmWork, 0) != bars:
        ArrayResize(_adxmWork, bars)
    instanceNo *= 8
    _adxmWork[i][instanceNo + 3] = _close
    _adxmWork[i][instanceNo + 4] = _high
    _adxmWork[i][instanceNo + 5] = _low
    hc = _adxmWork[i][instanceNo + 4]
    lc = _adxmWork[i][instanceNo + 5]
    cp = (_adxmWork[i - 1][instanceNo + 3] if (i > 0) else _adxmWork[i][instanceNo + 3])
    hp = (_adxmWork[i - 1][instanceNo + 4] if (i > 0) else _adxmWork[i][instanceNo + 4])
    lp = (_adxmWork[i - 1][instanceNo + 5] if (i > 0) else _adxmWork[i][instanceNo + 5])
    dh = MathMax(hc - hp, 0)
    dl = MathMax(lp - lc, 0)
    if dh == dl:
        dh = 0.0
        dl = 0.0
    elif dh < dl:
        dh = 0.0
    elif dl < dh:
        dl = 0.0
    tr = MathMax(hc, cp) - MathMin(lc, cp)
    dhk = (_fdiv(100.0 * dh, tr) if (tr != 0) else 0)
    dlk = (_fdiv(100.0 * dl, tr) if (tr != 0) else 0)
    alpha = _fdiv(2.0, _period + 1.0)
    _adxmWork[i][instanceNo + 0] = ((_adxmWork[i - 1][instanceNo + 0] + (alpha * (dhk - _adxmWork[i - 1][instanceNo + 0]))) if (i > 0) else dhk)
    _adxmWork[i][instanceNo + 1] = ((_adxmWork[i - 1][instanceNo + 1] + (alpha * (dlk - _adxmWork[i - 1][instanceNo + 1]))) if (i > 0) else dlk)
    _adxmWork[i][instanceNo + 6] = _adxmWork[i][instanceNo + 0] - _adxmWork[i][instanceNo + 1]
    div = MathAbs(_adxmWork[i][instanceNo + 0] + _adxmWork[i][instanceNo + 1])
    temp = (_fdiv(100 * _adxmWork[i][instanceNo + 6], div) if (div != 0.0) else 0)
    _adxmWork[i][instanceNo + 7] = ((_adxmWork[i - 1][instanceNo + 7] + (alpha * (temp - _adxmWork[i - 1][instanceNo + 7]))) if (i > 0) else 0)
    _di.v = _adxmWork[i][instanceNo + 6]
    return _adxmWork[i][instanceNo + 7]

def iSmooth(price, length, phase, r, bars):
    global m_size
    if m_size != bars:
        ArrayResize(m_wrk, bars)
    if ArrayRange(m_wrk, 0) != bars:
        return price
    m_size = bars
    if r == 0 or length <= 1:
        k = 0
        while k < 7:
            m_wrk[r][k] = price
            k += 1
        while k < 10:
            m_wrk[r][k] = 0.0
            k += 1
        return price
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = price - m_wrk[r - 1][5]
    del2 = price - m_wrk[r - 1][6]
    forBar = MathMin(r, 10)
    m_wrk[r][7] = 0.0
    if MathAbs(del1) > MathAbs(del2):
        m_wrk[r][7] = MathAbs(del1)
    if MathAbs(del1) < MathAbs(del2):
        m_wrk[r][7] = MathAbs(del2)
    m_wrk[r][8] = m_wrk[r - 1][8] + ((m_wrk[r][7] - m_wrk[r - forBar][7]) * 0.1)
    m_wrk[r][9] = m_wrk[r - 1][9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (m_wrk[r][8] - m_wrk[r - 1][9]))
    dVolty = (_fdiv(m_wrk[r][7], m_wrk[r][9]) if (m_wrk[r][9] > 0) else 0)
    if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
        dVolty = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty < 1:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    if del1 > 0:
        m_wrk[r][5] = price
    else:
        m_wrk[r][5] = price - (Kv * del1)
    if del2 < 0:
        m_wrk[r][6] = price
    else:
        m_wrk[r][6] = price - (Kv * del2)
    corr = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    m_wrk[r][0] = price + (alpha * (m_wrk[r - 1][0] - price))
    m_wrk[r][1] = ((price - m_wrk[r][0]) * (1 - beta)) + (beta * m_wrk[r - 1][1])
    m_wrk[r][2] = m_wrk[r][0] + (corr * m_wrk[r][1])
    m_wrk[r][3] = ((m_wrk[r][2] - m_wrk[r - 1][4]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * m_wrk[r - 1][3])
    m_wrk[r][4] = m_wrk[r - 1][4] + m_wrk[r][3]
    return m_wrk[r][4]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADXmSmoothed(_MQL5Indicator):
    name = 'ADXm smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpAdxmPeriod': 14,  # ADXm period
        'inpAdxmSmooth': 5,  # Smoothing period
        'inpAdxmSmoothPhase': 0.0,  # Smoothing phase
    }

