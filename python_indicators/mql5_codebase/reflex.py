"""Reflex — converted from MQL5: MQL5 Indicators/Reflex/Reflex.mq5

Copyright: © mladen, 2020; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2020', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16748574, 5275647]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Reflex'}, 'levels': [], 'description': [], 'name': 'Reflex', 'source': 'MQL5 Indicators/Reflex/Reflex.mq5', 'folder': 'Reflex', 'inputs': [{'mql': 'inpReflexPeriod', 'py': 'inpReflexPeriod', 'param': 'inpReflexPeriod', 'type': 'int', 'default': 50, 'label': 'Reflex period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpReflexPeriod = _input('inpReflexPeriod', 50)  # Reflex period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class CReflex(MqlObject):
    _q_fields = ('m_c1', 'm_c2', 'm_c3', 'm_multi', 'm_array', 'm_arraySize', 'm_period')
    def __init__(self):
        self.m_c1 = 0.0
        self.m_c2 = 0.0
        self.m_c3 = 0.0
        self.m_multi = 0.0
        self.m_array = Arr(0, 0, factory=sWorkStruct)
        self.m_arraySize = 0
        self.m_period = 0
        self.m_c1 = 1.0
        self.m_c2 = 1.0
        self.m_c3 = 1.0
        self.m_arraySize = -1
    def _q_dtor(self):
        pass
    def OnInit(self, period):
        self.m_period = (period if (period > 1) else 1)
        a1 = MathExp(_fdiv(-1.414 * M_PI, self.m_period))
        b1 = 2.0 * a1 * MathCos(_fdiv(1.414 * M_PI, self.m_period))
        self.m_c2 = b1
        self.m_c3 = (-a1) * a1
        self.m_c1 = 1.0 - self.m_c2 - self.m_c3
        self.m_multi = 1.0
        for k in range(1, self.m_period):
            self.m_multi += k + 1
    def OnCalculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
        self.m_array[i].value = value
        if i > 1:
            self.m_array[i].ssm = ((self.m_c1 * (self.m_array[i].value + self.m_array[i - 1].value)) / 2.0) + (self.m_c2 * self.m_array[i - 1].ssm) + (self.m_c3 * self.m_array[i - 2].ssm)
        else:
            self.m_array[i].ssm = value
        if i > self.m_period:
            self.m_array[i].sum = self.m_array[i - 1].sum + self.m_array[i].ssm - self.m_array[i - self.m_period].ssm
        else:
            self.m_array[i].sum = self.m_array[i].ssm
            k = 1
            while k < self.m_period and (i - k) >= 0:
                self.m_array[i].sum += self.m_array[i - k].ssm
                k += 1
        slope = (_fdiv(self.m_array[i - self.m_period].ssm - self.m_array[i].ssm, self.m_period) if (i >= self.m_period) else 0)
        sum_ = (self.m_period * self.m_array[i].ssm) + (self.m_multi * slope) - self.m_array[i].sum
        sum_ = _fdiv(sum_, self.m_period)
        self.m_array[i].ms = (((0.04 * sum_ * sum_) + (0.96 * self.m_array[i - 1].ms)) if (i > 0) else 0)
        return (_fdiv(sum_, MathSqrt(self.m_array[i].ms)) if (self.m_array[i].ms != 0) else 0)

class sWorkStruct(MqlObject):
    _q_fields = ('value', 'ssm', 'sum', 'ms')
    def __init__(self, *args):
        self.value = 0.0
        self.ssm = 0.0
        self.sum = 0.0
        self.ms = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iReflex.OnInit(inpReflexPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Reflex (' + _str(inpReflexPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = MathMax(prev_calculated - 1, 0)
    for i in range(limit, rates_total):
        val[i] = iReflex.OnCalculate((((close[i] + close[i - 1]) / 2) if (i > 0) else close[i]), i, rates_total)
        valc[i] = ((0 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else 0) if (i > 0) else 0)
    return rates_total

# ---- global variables initialised from expressions
iReflex = _alloc(CReflex)
iReflex.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Reflex(_MQL5Indicator):
    name = 'Reflex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpReflexPeriod': 50,  # Reflex period
    }

