"""TrendFlex — converted from MQL5: MQL5 Indicators/TrendFlex/TrendFlex.mq5

Copyright: © mladen, 2020; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2020', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16748574, 5275647]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'TrendFlex'}, 'levels': [], 'description': [], 'name': 'TrendFlex', 'source': 'MQL5 Indicators/TrendFlex/TrendFlex.mq5', 'folder': 'TrendFlex', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 20, 'label': 'Fast trend-flex period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 50, 'label': 'Slow trend-flex period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 20)  # Fast trend-flex period
inpSlowPeriod = _input('inpSlowPeriod', 50)  # Slow trend-flex period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class CTrendFlex(MqlObject):
    _q_fields = ('m_c1', 'm_c2', 'm_c3', 'm_array', 'm_arraySize', 'm_period')
    def __init__(self):
        self.m_c1 = 0.0
        self.m_c2 = 0.0
        self.m_c3 = 0.0
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
        sum_ = (self.m_period * self.m_array[i].ssm) - self.m_array[i].sum
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
    iTfFast.OnInit(inpFastPeriod)
    iTfSlow.OnInit(inpSlowPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendFlex (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = MathMax(prev_calculated - 1, 0)
    for i in range(limit, rates_total):
        _price = (((close[i] + close[i - 1]) / 2) if (i > 0) else close[i])
        val[i] = iTfFast.OnCalculate(_price, i, rates_total) - iTfSlow.OnCalculate(_price, i, rates_total)
        valc[i] = ((0 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else 0) if (i > 0) else 0)
    return rates_total

# ---- global variables initialised from expressions
iTfSlow = _alloc(CTrendFlex)
iTfSlow.__init__()
iTfFast = _alloc(CTrendFlex)
iTfFast.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendFlex(_MQL5Indicator):
    name = 'TrendFlex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 20,  # Fast trend-flex period
        'inpSlowPeriod': 50,  # Slow trend-flex period
    }

