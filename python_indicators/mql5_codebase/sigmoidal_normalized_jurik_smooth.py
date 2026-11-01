"""Sigmoidal normalized Jurik smooth — converted from MQL5: MQL5 Indicators/Log Sigmoidal Normalized Jurik MA/Sigmoidal normalized Jurik smooth.mq5

Log sigmoidal normalized Jurik smooth
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 3329330, 3937500]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Normalized Jurik smooth'}, 'levels': [], 'description': ['Log sigmoidal normalized Jurik smooth'], 'name': 'Sigmoidal normalized Jurik smooth', 'source': 'MQL5 Indicators/Log Sigmoidal Normalized Jurik MA/Sigmoidal normalized Jurik smooth.mq5', 'folder': 'Log Sigmoidal Normalized Jurik MA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Jurik smooth period', 'sinput': False}, {'mql': 'inpPhase', 'py': 'inpPhase', 'param': 'inpPhase', 'type': 'double', 'default': 0.0, 'label': 'Phase', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpNormalizeLength', 'py': 'inpNormalizeLength', 'param': 'inpNormalizeLength', 'type': 'int', 'default': 30, 'label': 'Normalization length', 'sinput': False}, {'mql': 'inpNormalizeHyperbolic', 'py': 'inpNormalizeHyperbolic', 'param': 'inpNormalizeHyperbolic', 'type': 'bool', 'default': True, 'label': 'Hyperbolic normalization?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Jurik smooth period
inpPhase = _input('inpPhase', 0.0)  # Phase
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpNormalizeLength = _input('inpNormalizeLength', 30)  # Normalization length
inpNormalizeHyperbolic = _input('inpNormalizeHyperbolic', True)  # Hyperbolic normalization?
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
values = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
workDev = Arr(0, 0.0)

class CJurikSmooth(MqlObject):
    _q_fields = ('m_size', 'm_wrk')
    def __init__(self):
        self.m_size = 0
        self.m_wrk = Arr(0, 0.0, dims=(10,))
        self.m_size = 0
        return
    def _q_dtor(self):
        return
    def CalculateValue(self, price, length, phase, r, bars):
        if self.m_size != bars:
            ArrayResize(self.m_wrk, bars)
        if ArrayRange(self.m_wrk, 0) != bars:
            return price
        self.m_size = bars
        if r == 0 or length <= 1:
            k = 0
            while k < 7:
                self.m_wrk[r][k] = price
                k += 1
            while k < 10:
                self.m_wrk[r][k] = 0.0
                k += 1
            return price
        len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
        pow1 = MathMax(len1 - 2.0, 0.5)
        del1 = price - self.m_wrk[r - 1][5]
        del2 = price - self.m_wrk[r - 1][6]
        forBar = MathMin(r, 10)
        self.m_wrk[r][7] = 0.0
        if MathAbs(del1) > MathAbs(del2):
            self.m_wrk[r][7] = MathAbs(del1)
        if MathAbs(del1) < MathAbs(del2):
            self.m_wrk[r][7] = MathAbs(del2)
        self.m_wrk[r][8] = self.m_wrk[r - 1][8] + ((self.m_wrk[r][7] - self.m_wrk[r - forBar][7]) * 0.1)
        self.m_wrk[r][9] = self.m_wrk[r - 1][9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (self.m_wrk[r][8] - self.m_wrk[r - 1][9]))
        dVolty = (_fdiv(self.m_wrk[r][7], self.m_wrk[r][9]) if (self.m_wrk[r][9] > 0) else 0)
        if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
            dVolty = MathPow(len1, _fdiv(1.0, pow1))
        if dVolty < 1:
            dVolty = 1.0
        pow2 = MathPow(dVolty, pow1)
        len2 = MathSqrt(0.5 * (length - 1)) * len1
        Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
        if del1 > 0:
            self.m_wrk[r][5] = price
        else:
            self.m_wrk[r][5] = price - (Kv * del1)
        if del2 < 0:
            self.m_wrk[r][6] = price
        else:
            self.m_wrk[r][6] = price - (Kv * del2)
        corr = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
        beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
        alpha = MathPow(beta, pow2)
        self.m_wrk[r][0] = price + (alpha * (self.m_wrk[r - 1][0] - price))
        self.m_wrk[r][1] = ((price - self.m_wrk[r][0]) * (1 - beta)) + (beta * self.m_wrk[r - 1][1])
        self.m_wrk[r][2] = self.m_wrk[r][0] + (corr * self.m_wrk[r][1])
        self.m_wrk[r][3] = ((self.m_wrk[r][2] - self.m_wrk[r - 1][4]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * self.m_wrk[r - 1][3])
        self.m_wrk[r][4] = self.m_wrk[r - 1][4] + self.m_wrk[r][3]
        return self.m_wrk[r][4]

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, values, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Log sigmoidal normalized Jurik smooth (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        values[i] = iSmooth[0].CalculateValue(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, inpPhase, i, rates_total)
        mean = iSma(values[i], inpNormalizeLength, i, rates_total)
        deviation = iDeviation(values[i], inpNormalizeLength, i, rates_total)
        zeroMean = 0.0
        if deviation != 0:
            zeroMean = _fdiv(values[i] - mean, deviation)
        val[i] = (_fdiv(1.0 - MathExp(-zeroMean), 1.0 + MathExp(-zeroMean)) if inpNormalizeHyperbolic else _fdiv(1.0, 1.0 + MathExp(-zeroMean)))
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo + 0] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
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

# ---- global variables initialised from expressions
iSmooth = Arr(1, 0, dyn=False, factory=CJurikSmooth)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SigmoidalNormalizedJurikSmooth(_MQL5Indicator):
    name = 'Sigmoidal normalized Jurik smooth'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Jurik smooth period
        'inpPhase': 0.0,  # Phase
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpNormalizeLength': 30,  # Normalization length
        'inpNormalizeHyperbolic': True,  # Hyperbolic normalization?
    }

