"""Triple Jurik smooth — converted from MQL5: MQL5 Indicators/Triple Jurik Smooth/Triple Jurik smooth.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 8, 2: 8, 3: 8}, 'colors': {1: [11119017, 9639167, 3329330], 2: [11119017, 9639167, 3329330], 3: [11119017, 9639167, 3329330]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Smooth high', 2: 'Smooth close', 3: 'Smooth low'}, 'levels': [], 'description': [], 'name': 'Triple Jurik smooth', 'source': 'MQL5 Indicators/Triple Jurik Smooth/Triple Jurik smooth.mq5', 'folder': 'Triple Jurik Smooth', 'inputs': [{'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'double', 'default': 27.0, 'label': 'Smooth period', 'sinput': False}, {'mql': 'inpSmoothPhase', 'py': 'inpSmoothPhase', 'param': 'inpSmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Smooth phase', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpSmoothPeriod = _input('inpSmoothPeriod', 27.0)  # Smooth period
inpSmoothPhase = _input('inpSmoothPhase', 0.0)  # Smooth phase
valu = Arr(0, 0.0)
valuc = Arr(0, 0.0)
valc = Arr(0, 0.0)
valcc = Arr(0, 0.0)
vald = Arr(0, 0.0)
valdc = Arr(0, 0.0)

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
    SetIndexBuffer(0, valu, INDICATOR_DATA)
    SetIndexBuffer(1, valuc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valc, INDICATOR_DATA)
    SetIndexBuffer(3, valcc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, vald, INDICATOR_DATA)
    SetIndexBuffer(5, valdc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Triple Jurik smooth (' + _str(inpSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        valu[i] = iSmooth[0].CalculateValue(high[i], inpSmoothPeriod, inpSmoothPhase, i, rates_total)
        valc[i] = iSmooth[1].CalculateValue(close[i], inpSmoothPeriod, inpSmoothPhase, i, rates_total)
        vald[i] = iSmooth[2].CalculateValue(low[i], inpSmoothPeriod, inpSmoothPhase, i, rates_total)
        valuc[i] = ((2 if (valu[i] > valu[i - 1]) else 1 if (valu[i] < valu[i - 1]) else valuc[i - 1]) if (i > 0) else 0)
        valcc[i] = ((2 if (valc[i] > valc[i - 1]) else 1 if (valc[i] < valc[i - 1]) else valcc[i - 1]) if (i > 0) else 0)
        valdc[i] = ((2 if (vald[i] > vald[i - 1]) else 1 if (vald[i] < vald[i - 1]) else valdc[i - 1]) if (i > 0) else 0)
    return rates_total

# ---- global variables initialised from expressions
iSmooth = Arr(3, 0, dyn=False, factory=CJurikSmooth)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TripleJurikSmooth(_MQL5Indicator):
    name = 'Triple Jurik smooth'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpSmoothPeriod': 27.0,  # Smooth period
        'inpSmoothPhase': 0.0,  # Smooth phase
    }

