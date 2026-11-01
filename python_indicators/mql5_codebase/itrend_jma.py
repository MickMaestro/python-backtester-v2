"""iTrend JMA — converted from MQL5: MQL5 Indicators/iTrend JMA/iTrend JMA.mq5

iTrendd JMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 8}, 'colors': {1: [3329330, 3329330], 2: [9639167, 9639167], 3: [11119017], 4: [11119017], 5: [11119017, 65280, 11823615]}, 'widths': {3: 2, 4: 2, 5: 2}, 'styles': {5: 0}, 'labels': {1: 'iTrend up', 2: 'iTrend down', 3: 'iTrend line up', 4: 'iTrend line down', 5: 'iTrend'}, 'levels': [], 'description': ['iTrendd JMA'], 'name': 'iTrend JMA', 'source': 'MQL5 Indicators/iTrend JMA/iTrend JMA.mq5', 'folder': 'iTrend JMA', 'inputs': [{'mql': 'ItPeriod', 'py': 'ItPeriod', 'param': 'ItPeriod', 'type': 'int', 'default': 20, 'label': 'iTrend period', 'sinput': False}, {'mql': 'ItPrice', 'py': 'ItPrice', 'param': 'ItPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'LevelBars', 'py': 'LevelBars', 'param': 'LevelBars', 'type': 'int', 'default': 300, 'label': 'Look back period for levels', 'sinput': False}, {'mql': 'LevelFactor', 'py': 'LevelFactor', 'param': 'LevelFactor', 'type': 'double', 'default': 0.283, 'label': 'Levels factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ItPeriod = _input('ItPeriod', 20)  # iTrend period
ItPrice = _input('ItPrice', PRICE_CLOSE)  # Price
LevelBars = _input('LevelBars', 300)  # Look back period for levels
LevelFactor = _input('LevelFactor', 0.283)  # Levels factor
itrend = Arr(0, 0.0)
itrendc = Arr(0, 0.0)
lup = Arr(0, 0.0)
ldn = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filluz = Arr(0, 0.0)
filld = Arr(0, 0.0)
filldz = Arr(0, 0.0)
m_wrk = Arr(0, 0.0, dims=(10,))
m_size = 0

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filluz, INDICATOR_DATA)
    SetIndexBuffer(2, filld, INDICATOR_DATA)
    SetIndexBuffer(3, filldz, INDICATOR_DATA)
    SetIndexBuffer(4, lup, INDICATOR_DATA)
    SetIndexBuffer(5, ldn, INDICATOR_DATA)
    SetIndexBuffer(6, itrend, INDICATOR_DATA)
    SetIndexBuffer(7, itrendc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'iTrend JMA (' + _str(ItPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        ma = getPrice(ItPrice, open, close, high, low, i, rates_total)
        mv = iSmooth(ma, ItPeriod, 0.0, i, rates_total, 0)
        fillu[i] = ma - mv
        lup[i] = fillu[i]
        filluz[i] = 0.0
        filld[i] = -(low[i] + high[i] - (2 * mv))
        ldn[i] = filld[i]
        filldz[i] = 0.0
        hi = MathMax(fillu[i], filld[i])
        k = 1
        while k < LevelBars and (i - k) >= 0:
            hi = MathMax(hi, MathMax(fillu[i - k], filld[i - k]))
            k += 1
        itrend[i] = hi * LevelFactor
        itrendc[i] = (1 if (fillu[i] > itrend[i]) else 2 if (filld[i] > itrend[i]) else itrendc[i - 1] if (i > 0) else 0)
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

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw1 = tprice
        if _sw1 == PRICE_CLOSE:
            return close[i]
        elif _sw1 == PRICE_OPEN:
            return open[i]
        elif _sw1 == PRICE_HIGH:
            return high[i]
        elif _sw1 == PRICE_LOW:
            return low[i]
        elif _sw1 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ITrendJMA(_MQL5Indicator):
    name = 'iTrend JMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ItPeriod': 20,  # iTrend period
        'ItPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'LevelBars': 300,  # Look back period for levels
        'LevelFactor': 0.283,  # Levels factor
    }

