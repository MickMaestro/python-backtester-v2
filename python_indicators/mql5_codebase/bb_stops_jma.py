"""BB stops JMA — converted from MQL5: MQL5 Indicators/BB Stops JMA/BB stops JMA.mq5

BB stops Jurik
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 12}, 'colors': {1: [8421504], 2: [8421504], 3: [16748574], 4: [6333684], 5: [12632256, 16748574, 6333684]}, 'widths': {3: 3, 4: 3, 5: 2}, 'styles': {1: 2, 2: 2}, 'labels': {}, 'levels': [], 'description': ['BB stops Jurik'], 'name': 'BB stops JMA', 'source': 'MQL5 Indicators/BB Stops JMA/BB stops JMA.mq5', 'folder': 'BB Stops JMA', 'inputs': [{'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 20, 'label': 'Bollinger bands period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpRisk', 'py': 'inpRisk', 'param': 'inpRisk', 'type': 'double', 'default': 1.0, 'label': 'Risk', 'sinput': False}, {'mql': 'inpDeviationPeriod', 'py': 'inpDeviationPeriod', 'param': 'inpDeviationPeriod', 'type': 'int', 'default': 20, 'label': 'Deviations period', 'sinput': False}, {'mql': 'inpDeviation', 'py': 'inpDeviation', 'param': 'inpDeviation', 'type': 'double', 'default': 1.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'inpDeviationSample', 'py': 'inpDeviationSample', 'param': 'inpDeviationSample', 'type': 'bool', 'default': False, 'label': 'Deviation sample correction?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMaPeriod = _input('inpMaPeriod', 20)  # Bollinger bands period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpRisk = _input('inpRisk', 1.0)  # Risk
inpDeviationPeriod = _input('inpDeviationPeriod', 20)  # Deviations period
inpDeviation = _input('inpDeviation', 1.0)  # Deviation
inpDeviationSample = _input('inpDeviationSample', False)  # Deviation sample correction?
bba = Arr(0, 0.0)
bbc = Arr(0, 0.0)
bblu = Arr(0, 0.0)
bbld = Arr(0, 0.0)
amax = Arr(0, 0.0)
amin = Arr(0, 0.0)
bmax = Arr(0, 0.0)
bmin = Arr(0, 0.0)
trend = Arr(0, 0.0)
workDev = Arr(0, 0.0, dims=(1,))
m_wrk = Arr(0, 0.0, dims=(10,))
m_size = 0

def OnInit():
    SetIndexBuffer(0, bmax, INDICATOR_DATA)
    SetIndexBuffer(1, bmin, INDICATOR_DATA)
    SetIndexBuffer(2, bblu, INDICATOR_DATA)
    SetIndexBuffer(3, bbld, INDICATOR_DATA)
    SetIndexBuffer(4, bba, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    SetIndexBuffer(5, bbc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, amax, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, amin, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, trend, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickVolume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        dev = iDeviation(price, inpDeviationPeriod, inpDeviationSample, i, rates_total)
        ma = iSmooth(price, inpMaPeriod, 0.0, i, rates_total, 0)
        amax[i] = ma + (dev * inpDeviation)
        amin[i] = ma - (dev * inpDeviation)
        bmax[i] = amax[i] + (0.5 * (inpRisk - 1) * (amax[i] - amin[i]))
        bmin[i] = amin[i] - (0.5 * (inpRisk - 1) * (amax[i] - amin[i]))
        trend[i] = ((1 if (price > amax[i - 1]) else -1 if (price < amin[i - 1]) else trend[i - 1]) if (i > 0) else 0)
        if i > 0:
            if trend[i] == -1 and amax[i] > amax[i - 1]:
                amax[i] = amax[i - 1]
            if trend[i] == 1 and amin[i] < amin[i - 1]:
                amin[i] = amin[i - 1]
            if trend[i] == -1 and bmax[i] > bmax[i - 1]:
                bmax[i] = bmax[i - 1]
            if trend[i] == 1 and bmin[i] < bmin[i - 1]:
                bmin[i] = bmin[i - 1]
        bblu[i] = EMPTY_VALUE
        bbld[i] = EMPTY_VALUE
        if trend[i] == 1:
            bblu[i] = bmin[i]
            bbc[i] = 1.0
        if trend[i] == -1:
            bbld[i] = bmax[i]
            bbc[i] = 2.0
        bba[i] = (((bblu[i] if (trend[i] == 1) else bbld[i]) if (trend[i] != trend[i - 1]) else EMPTY_VALUE) if (i > 0) else EMPTY_VALUE)
        i += 1
    return i

def iDeviation(value, length, isSample, i, bars, instanceNo=0):
    if ArrayRange(workDev, 0) != bars:
        ArrayResize(workDev, bars)
    workDev[i][instanceNo] = value
    oldMean = value
    newMean = value
    squares = 0.0
    k = 0
    k = 1
    while k < length and (i - k) >= 0:
        newMean = _fdiv(workDev[i - k][instanceNo] - oldMean, k + 1) + oldMean
        squares += (workDev[i - k][instanceNo] - oldMean) * (workDev[i - k][instanceNo] - newMean)
        oldMean = newMean
        k += 1
    return MathSqrt(_fdiv(squares, MathMax(k - isSample, 1)))

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


class BBStopsJMA(_MQL5Indicator):
    name = 'BB stops JMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMaPeriod': 20,  # Bollinger bands period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpRisk': 1.0,  # Risk
        'inpDeviationPeriod': 20,  # Deviations period
        'inpDeviation': 1.0,  # Deviation
        'inpDeviationSample': False,  # Deviation sample correction?
    }

