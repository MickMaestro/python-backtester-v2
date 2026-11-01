"""Variance (Welford) — converted from MQL5: MQL5 Indicators/Variance/Variance (Welford).mq5

Variance
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Variance'}, 'levels': [], 'description': ['Variance'], 'name': 'Variance (Welford)', 'source': 'MQL5 Indicators/Variance/Variance (Welford).mq5', 'folder': 'Variance', 'inputs': [{'mql': 'inpVarPeriod', 'py': 'inpVarPeriod', 'param': 'inpVarPeriod', 'type': 'int', 'default': 14, 'label': 'Variance period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVarPeriod = _input('inpVarPeriod', 14)  # Variance period
val = Arr(0, 0.0)

class CVariance(MqlObject):
    _q_fields = ('m_period', 'm_array', 'm_arraySize')
    def __init__(self):
        self.m_period = 0
        self.m_array = Arr(0, 0, factory=sVarStruct)
        self.m_arraySize = 0
        self.m_period = 1
        self.m_arraySize = -1
        return
    def _q_dtor(self):
        return
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].value = value
        _m = 0.0
        _s = 0.0
        _oldm = 0.0
        k = 0
        while k < self.m_period and i >= k:
            _oldm = _m
            _m = _m + _fdiv(self.m_array[i - k].value - _m, 1.0 + k)
            _s = _s + ((self.m_array[i - k].value - _m) * (self.m_array[i - k].value - _oldm))
            k += 1
        return _fdiv(_s, self.m_period - 1)

class sVarStruct(MqlObject):
    _q_fields = ('value',)
    def __init__(self, *args):
        self.value = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    iVariance.init(inpVarPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Variance (' + _str(inpVarPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        val[i] = iVariance.calculate(close[i], i, rates_total)
        i += 1
    return i

# ---- global variables initialised from expressions
iVariance = _alloc(CVariance)
iVariance.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VarianceWelford(_MQL5Indicator):
    name = 'Variance (Welford)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpVarPeriod': 14,  # Variance period
    }

