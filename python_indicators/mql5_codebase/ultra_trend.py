"""Ultra trend — converted from MQL5: MQL5 Indicators/Ultra Trend/Ultra trend.mq5

Ultra trend
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 8}, 'colors': {1: [9498256, 11788021], 2: [11119017, 3329330, 42495], 3: [11119017, 3329330, 42495]}, 'widths': {2: 3, 3: 1}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Ultra trend +', 3: 'Ultra trend -'}, 'levels': [], 'description': ['Ultra trend'], 'name': 'Ultra trend', 'source': 'MQL5 Indicators/Ultra Trend/Ultra trend.mq5', 'folder': 'Ultra Trend', 'inputs': [{'mql': 'inpUtrPeriod', 'py': 'inpUtrPeriod', 'param': 'inpUtrPeriod', 'type': 'int', 'default': 3, 'label': 'Start period', 'sinput': False}, {'mql': 'inpProgression', 'py': 'inpProgression', 'param': 'inpProgression', 'type': 'int', 'default': 5, 'label': 'Step', 'sinput': False}, {'mql': 'inpInstances', 'py': 'inpInstances', 'param': 'inpInstances', 'type': 'int', 'default': 30, 'label': 'Instances', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'int', 'default': 5, 'label': 'Ultra trend smoothing period', 'sinput': False}, {'mql': 'inpSmoothPhase', 'py': 'inpSmoothPhase', 'param': 'inpSmoothPhase', 'type': 'int', 'default': 100, 'label': 'Ultra trend smoothing phase', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpUtrPeriod = _input('inpUtrPeriod', 3)  # Start period
inpProgression = _input('inpProgression', 5)  # Step
inpInstances = _input('inpInstances', 30)  # Instances
inpSmooth = _input('inpSmooth', 5)  # Ultra trend smoothing period
inpSmoothPhase = _input('inpSmoothPhase', 100)  # Ultra trend smoothing phase
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
valp = Arr(0, 0.0)
valpc = Arr(0, 0.0)
valm = Arr(0, 0.0)
valmc = Arr(0, 0.0)

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
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, valp, INDICATOR_DATA)
    SetIndexBuffer(3, valpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, valm, INDICATOR_DATA)
    SetIndexBuffer(5, valmc, INDICATOR_COLOR_INDEX)
    ArrayResize(_iSmooth, inpInstances + 3)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ultra trend (' + _str(inpUtrPeriod) + ',' + _str(inpProgression) + ',' + _str(inpInstances) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    endLength = inpUtrPeriod + (inpProgression * inpInstances)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        valueUp = 0.0
        valueDn = 0.0
        k = inpUtrPeriod
        instance = 2
        while k <= endLength and i > 0:
            if _iSmooth[instance].CalculateValue(close[i - 1], k, inpSmoothPhase, i - 1, rates_total) < _iSmooth[instance].CalculateValue(close[i], k, inpSmoothPhase, i, rates_total):
                valueUp += 1
            else:
                valueDn += 1
            k += inpProgression
            instance += 1
        valp[i] = _iSmooth[0].CalculateValue(valueUp, inpSmooth, inpSmoothPhase, i, rates_total)
        valm[i] = _iSmooth[1].CalculateValue(valueDn, inpSmooth, inpSmoothPhase, i, rates_total)
        valpc[i] = (1 if (valp[i] > valm[i]) else 2)
        valmc[i] = valpc[i]
        fillu[i] = valp[i]
        filld[i] = valm[i]
        i += 1
    return i

# ---- global variables initialised from expressions
_iSmooth = Arr(0, 0, factory=CJurikSmooth)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UltraTrend(_MQL5Indicator):
    name = 'Ultra trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpUtrPeriod': 3,  # Start period
        'inpProgression': 5,  # Step
        'inpInstances': 30,  # Instances
        'inpSmooth': 5,  # Ultra trend smoothing period
        'inpSmoothPhase': 100,  # Ultra trend smoothing phase
    }

