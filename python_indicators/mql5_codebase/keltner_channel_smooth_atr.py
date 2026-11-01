"""Keltner channel - smooth ATR — converted from MQL5: MQL5 Indicators/Keltner channel - smooth ATR/Keltner channel - smooth ATR.mq5

Keltner channel - smooth ATR
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 1}, 'colors': {1: [13628367], 2: [13492732], 3: [3329330, 6333684], 4: [3329330, 6333684], 5: [11119017]}, 'widths': {3: 2, 4: 2, 5: 1}, 'styles': {}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Middle value'}, 'levels': [], 'description': ['Keltner channel - smooth ATR'], 'name': 'Keltner channel - smooth ATR', 'source': 'MQL5 Indicators/Keltner channel - smooth ATR/Keltner channel - smooth ATR.mq5', 'folder': 'Keltner channel - smooth ATR', 'inputs': [{'mql': 'inpPeriods', 'py': 'inpPeriods', 'param': 'inpPeriods', 'type': 'int', 'default': 20, 'label': 'Keltner channel period', 'sinput': False}, {'mql': 'inpMulti', 'py': 'inpMulti', 'param': 'inpMulti', 'type': 'double', 'default': 2.0, 'label': 'Channel multiplicator', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 0, 'label': 'Keltner channel median value average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpPeriods = _input('inpPeriods', 20)  # Keltner channel period
inpMulti = _input('inpMulti', 2.0)  # Channel multiplicator
inpMaMethod = _input('inpMaMethod', ma_sma)  # Keltner channel median value average method
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
bufferUp = Arr(0, 0.0)
bufferUpc = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferDnc = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
m_wrk = Arr(0, 0.0, dims=(10,))
m_size = 0
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferUpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(7, bufferDnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, bufferMe, INDICATOR_DATA)
    return 0

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        _tr = ((MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])) if (i > 0) else (high[i] - low[i]))
        atr = iSmooth(_tr, inpPeriods, 0.0, i, rates_total)
        bufferMe[i] = iCustomMa(inpMaMethod, price, inpPeriods, i, rates_total)
        bufferUp[i] = bufferMe[i] + (atr * inpMulti)
        bufferDn[i] = bufferMe[i] - (atr * inpMulti)
        fupd[i] = bufferMe[i]
        fupu[i] = bufferUp[i]
        fdnu[i] = bufferMe[i]
        fdnd[i] = bufferDn[i]
        if i > 0:
            bufferUpc[i] = bufferUpc[i - 1]
            bufferDnc[i] = bufferDnc[i - 1]
            if bufferUp[i] > bufferUp[i - 1]:
                bufferUpc[i] = 0.0
            if bufferUp[i] < bufferUp[i - 1]:
                bufferUpc[i] = 1.0
            if bufferDn[i] > bufferDn[i - 1]:
                bufferDnc[i] = 0.0
            if bufferDn[i] < bufferDn[i - 1]:
                bufferDnc[i] = 1.0
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

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

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

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period < 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw2 = tprice
    if _sw2 == PRICE_CLOSE:
        return close[i]
    elif _sw2 == PRICE_OPEN:
        return open[i]
    elif _sw2 == PRICE_HIGH:
        return high[i]
    elif _sw2 == PRICE_LOW:
        return low[i]
    elif _sw2 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KeltnerChannelSmoothATR(_MQL5Indicator):
    name = 'Keltner channel - smooth ATR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriods': 20,  # Keltner channel period
        'inpMulti': 2.0,  # Channel multiplicator
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Keltner channel median value average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

