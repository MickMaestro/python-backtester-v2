"""Phase change index - JMA — converted from MQL5: MQL5 Indicators/Phase change index - JMA/Phase change index - JMA.mq5

Phase change index - JMA smoothed
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [14474460, 14474460], 2: [11119017, 6333684, 16760576]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Phase change trend zone', 2: 'Phase change index'}, 'levels': [], 'description': ['Phase change index - JMA smoothed'], 'name': 'Phase change index - JMA', 'source': 'MQL5 Indicators/Phase change index - JMA/Phase change index - JMA.mq5', 'folder': 'Phase change index - JMA', 'inputs': [{'mql': 'inpLength', 'py': 'inpLength', 'param': 'inpLength', 'type': 'int', 'default': 30, 'label': 'Phase change index period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'double', 'default': 5.0, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpSmoothType', 'py': 'inpSmoothType', 'param': 'inpSmoothType', 'type': 'int', 'default': 1, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'inpLevelHigh', 'py': 'inpLevelHigh', 'param': 'inpLevelHigh', 'type': 'double', 'default': 80.0, 'label': 'Level high', 'sinput': False}, {'mql': 'inpLevelLow', 'py': 'inpLevelLow', 'param': 'inpLevelLow', 'type': 'double', 'default': 20.0, 'label': 'Level low', 'sinput': False}, {'mql': 'inpInverted', 'py': 'inpInverted', 'param': 'inpInverted', 'type': 'int', 'default': 1, 'label': 'Display type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enInverted
inv_regular = 0
inv_inverted = 1
_enum('enInverted', {0: 'inv_regular', 1: 'inv_inverted'})

# enum enSmoothType
smt_pre = 0
smt_val = 1
smt_all = 2
_enum('enSmoothType', {0: 'smt_pre', 1: 'smt_val', 2: 'smt_all'})

# ---- inputs and global variables
inpLength = _input('inpLength', 30)  # Phase change index period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpSmooth = _input('inpSmooth', 5.0)  # Smoothing period
inpSmoothType = _input('inpSmoothType', smt_val)  # Smoothing type
inpLevelHigh = _input('inpLevelHigh', 80.0)  # Level high
inpLevelLow = _input('inpLevelLow', 20.0)  # Level low
inpInverted = _input('inpInverted', inv_inverted)  # Display type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levup = Arr(0, 0.0)
levdn = Arr(0, 0.0)
prices = Arr(0, 0.0)
state = Arr(0, 0.0)
_smtModes = Arr.of(['price', 'value', 'price and value'], fill="")
m_wrk = Arr(0, 0.0, dims=(20,))
m_size = 0

def OnInit():
    SetIndexBuffer(0, levup, INDICATOR_DATA)
    SetIndexBuffer(1, levdn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, state, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevelHigh)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpLevelLow)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Phase change index ' + _smtModes[inpSmoothType] + ' smoothed (' + _str(inpLength) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    _smoothP = (0 if (inpSmoothType == smt_val) else inpSmooth)
    _smoothV = (0 if (inpSmoothType == smt_pre) else inpSmooth)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = iSmooth(getPrice(inpPrice, open, close, high, low, i, rates_total), _smoothP, 0.0, i, rates_total, 0)
        momentum = ((prices[i] - prices[i - inpLength]) if (i >= inpLength) else 0)
        sumUpDi = 0.0
        sumDnDi = 0.0
        j = 1
        while (j < inpLength and (i - j) >= 0) and (i - inpLength) >= 0:
            gradient = prices[i - inpLength] + ((momentum * (inpLength - j)) / inpLength)
            deviation = prices[i - j] - gradient
            if deviation > 0:
                sumUpDi += deviation
            else:
                sumDnDi -= deviation
            j += 1
        val[i] = iSmooth((_fdiv(100.0 * sumUpDi, sumUpDi + sumDnDi) if ((sumUpDi + sumDnDi) != 0) else 0), _smoothV, 0.0, i, rates_total, 1)
        if inpInverted == inv_inverted:
            val[i] = 100 - val[i]
        levdn[i] = 50.0
        levup[i] = (100 if (val[i] > inpLevelHigh) else 0 if (val[i] < inpLevelLow) else 50)
        valc[i] = (2 if (val[i] > inpLevelHigh) else 1 if (val[i] < inpLevelLow) else 0)
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


class PhaseChangeIndexJMA(_MQL5Indicator):
    name = 'Phase change index - JMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpLength': 30,  # Phase change index period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSmooth': 5.0,  # Smoothing period
        'inpSmoothType': _Choice({0: 'Smooth prices only', 1: 'Smooth phase change index only', 2: 'Smooth both price and phase change index'}, default=1),  # Smoothing type
        'inpLevelHigh': 80.0,  # Level high
        'inpLevelLow': 20.0,  # Level low
        'inpInverted': _Choice({0: 'Display regular value', 1: 'Display inverted value'}, default=1),  # Display type
    }

