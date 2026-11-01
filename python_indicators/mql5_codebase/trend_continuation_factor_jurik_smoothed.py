"""Trend continuation factor - Jurik smoothed — converted from MQL5: MQL5 Indicators/Trend Continuation Factor - Jurik smoothed/Trend continuation factor - Jurik smoothed.mq5

Trend continuation factor (Jurik smoothed)
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [15130800, 14150650], 2: [11119017, 6333684, 16760576]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Trend continuation factor zone', 2: 'Trend continuation factor'}, 'levels': [], 'description': ['Trend continuation factor (Jurik smoothed)'], 'name': 'Trend continuation factor - Jurik smoothed', 'source': 'MQL5 Indicators/Trend Continuation Factor - Jurik smoothed/Trend continuation factor - Jurik smoothed.mq5', 'folder': 'Trend Continuation Factor - Jurik smoothed', 'inputs': [{'mql': 'inpLength', 'py': 'inpLength', 'param': 'inpLength', 'type': 'int', 'default': 30, 'label': 'Trend continuation factor period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'double', 'default': 5.0, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpSmoothPhase', 'py': 'inpSmoothPhase', 'param': 'inpSmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Smoothing phase', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enInverted
inv_regular = 0
inv_inverted = 1
_enum('enInverted', {0: 'inv_regular', 1: 'inv_inverted'})

# ---- inputs and global variables
inpLength = _input('inpLength', 30)  # Trend continuation factor period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpSmooth = _input('inpSmooth', 5.0)  # Smoothing period
inpSmoothPhase = _input('inpSmoothPhase', 0.0)  # Smoothing phase
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levup = Arr(0, 0.0)
levdn = Arr(0, 0.0)
prices = Arr(0, 0.0)
values = Arr(0, 0.0, dims=(4,))

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
    SetIndexBuffer(0, levup, INDICATOR_DATA)
    SetIndexBuffer(1, levdn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend continuation factor (Jurik smoothed)(' + _str(inpLength) + ',' + _str(inpSmooth) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(values, 0) != rates_total:
        ArrayResize(values, rates_total)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        roc = ((prices[i] - prices[i - 1]) if (i > 0) else 0)
        values[i][0] = 0.0
        values[i][1] = 0.0
        values[i][2] = 0.0
        values[i][3] = 0.0
        if roc > 0:
            values[i][0] = roc
            values[i][2] = ((values[i][0] + values[i - 1][2]) if (i > 0) else values[i][0])
        if roc < 0:
            values[i][1] = -roc
            values[i][3] = ((values[i][1] + values[i - 1][3]) if (i > 0) else values[i][1])
        levUp = 0.0
        levDn = 0.0
        l = 0
        while l < inpLength and (i - l) >= 0:
            levUp += values[i - l][0] - values[i - l][3]
            levDn += values[i - l][1] - values[i - l][2]
            l += 1
        levup[i] = iSmooth[0].CalculateValue(levUp, inpSmooth, inpSmoothPhase, i, rates_total)
        levdn[i] = iSmooth[1].CalculateValue(levDn, inpSmooth, inpSmoothPhase, i, rates_total)
        val[i] = levup[i]
        valc[i] = (2 if (levup[i] > levdn[i]) else 1 if (levup[i] < levdn[i]) else 0)
        i += 1
    return i

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
iSmooth = Arr(2, 0, dyn=False, factory=CJurikSmooth)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendContinuationFactorJurikSmoothed(_MQL5Indicator):
    name = 'Trend continuation factor - Jurik smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpLength': 30,  # Trend continuation factor period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSmooth': 5.0,  # Smoothing period
        'inpSmoothPhase': 0.0,  # Smoothing phase
    }

