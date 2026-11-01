"""TrendStrength Jurik smothed rsi — converted from MQL5: MQL5 Indicators/Trend Strength - Jurik smoothed RSI/TrendStrength Jurik smothed rsi.mq5

TrendStrength Jurik smoothed (rsi)
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11119017], 2: [16748574], 3: [6333684]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'rsi', 2: 'trend up', 3: 'trend down'}, 'levels': [], 'description': ['TrendStrength Jurik smoothed (rsi)'], 'name': 'TrendStrength Jurik smothed rsi', 'source': 'MQL5 Indicators/Trend Strength - Jurik smoothed RSI/TrendStrength Jurik smothed rsi.mq5', 'folder': 'Trend Strength - Jurik smoothed RSI', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 32.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpStrength', 'py': 'inpStrength', 'param': 'inpStrength', 'type': 'double', 'default': 4.236, 'label': 'Strength', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'double', 'default': 32.0, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpSmoothPhase', 'py': 'inpSmoothPhase', 'param': 'inpSmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Smoothing hase', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32.0)  # Period
inpStrength = _input('inpStrength', 4.236)  # Strength
inpSmooth = _input('inpSmooth', 32.0)  # Smoothing period
inpSmoothPhase = _input('inpSmoothPhase', 0.0)  # Smoothing hase
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
rsi = Arr(0, 0.0)
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
smin = Arr(0, 0.0)
smax = Arr(0, 0.0)
trend = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(3,))

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
    SetIndexBuffer(0, rsi, INDICATOR_DATA)
    SetIndexBuffer(1, valu, INDICATOR_DATA)
    SetIndexBuffer(2, vald, INDICATOR_DATA)
    SetIndexBuffer(3, smin, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, smax, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, trend, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendStrength (Jurik smoothed rsi) (' + _str(inpPeriod) + ',' + _str(inpStrength) + ',' + _str(inpSmooth) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        rsi[i] = iSmooth[0].CalculateValue(iRsi(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i, rates_total), inpSmooth, inpSmoothPhase, i, rates_total)
        valu[i] = EMPTY_VALUE
        vald[i] = EMPTY_VALUE
        trend[i] = 0.0
        if i > 0:
            hrsi = rsi[i]
            lrsi = rsi[i]
            if rsi[i] > rsi[i - 1]:
                hrsi = rsi[i]
                lrsi = rsi[i - 1]
            if rsi[i] < rsi[i - 1]:
                hrsi = rsi[i - 1]
                lrsi = rsi[i]
            delta = hrsi - lrsi
            smin[i] = rsi[i] - (inpStrength * delta)
            smax[i] = rsi[i] + (inpStrength * delta)
            trend[i] = trend[i - 1]
            if rsi[i] > smax[i - 1]:
                trend[i] = 1.0
            if rsi[i] < smin[i - 1]:
                trend[i] = -1.0
            if trend[i] > 0:
                if smin[i] < smin[i - 1]:
                    smin[i] = smin[i - 1]
                valu[i] = smin[i]
            if trend[i] < 0:
                if smax[i] > smax[i - 1]:
                    smax[i] = smax[i - 1]
                vald[i] = smax[i]
    return rates_total

def iRsi(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 3
    workRsi[r][z + 0] = price
    alpha = _fdiv(1.0, MathMax(period, 1))
    if r < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (r - k - 1) >= 0:
            sum_ += MathAbs(workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0])
            k += 1
        workRsi[r][z + 1] = _fdiv(workRsi[r][z + 0] - workRsi[0][z + 0], MathMax(k, 1))
        workRsi[r][z + 2] = _fdiv(sum_, MathMax(k, 1))
    else:
        change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
        workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
        workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
    return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], DBL_MIN)) + 1)

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

# ---- global variables initialised from expressions
iSmooth = Arr(2, 0, dyn=False, factory=CJurikSmooth)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendStrengthJurikSmothedRsi(_MQL5Indicator):
    name = 'TrendStrength Jurik smothed rsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32.0,  # Period
        'inpStrength': 4.236,  # Strength
        'inpSmooth': 32.0,  # Smoothing period
        'inpSmoothPhase': 0.0,  # Smoothing hase
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

