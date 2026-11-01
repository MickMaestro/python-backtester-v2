"""Stochastic MACD — converted from MQL5: MQL5 Indicators/Stochastic MACD/Stochastic MACD.mq5

Copyright: © mladen, 2020; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2020', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16760576], 2: [5275647]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'MACD', 2: 'Signal'}, 'levels': [], 'description': [], 'name': 'Stochastic MACD', 'source': 'MQL5 Indicators/Stochastic MACD/Stochastic MACD.mq5', 'folder': 'Stochastic MACD', 'inputs': [{'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 45, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpSignPeriod', 'py': 'inpSignPeriod', 'param': 'inpSignPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevelOb', 'py': 'inpLevelOb', 'param': 'inpLevelOb', 'type': 'double', 'default': 10.0, 'label': 'Ovberbought level', 'sinput': False}, {'mql': 'inpLevelOs', 'py': 'inpLevelOs', 'param': 'inpLevelOs', 'type': 'double', 'default': -10.0, 'label': 'Ovbersold level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpStoPeriod = _input('inpStoPeriod', 45)  # Stochastic period
inpFastPeriod = _input('inpFastPeriod', 12)  # Fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # Slow period
inpSignPeriod = _input('inpSignPeriod', 9)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLevelOb = _input('inpLevelOb', 10.0)  # Ovberbought level
inpLevelOs = _input('inpLevelOs', -10.0)  # Ovbersold level
val = Arr(0, 0.0)
vals = Arr(0, 0.0)
_minmaxPeriod = 0

class CEma(MqlObject):
    _q_fields = ('m_alpha', 'm_period', 'm_array', 'm_arraySize')
    def __init__(self):
        self.m_alpha = 0.0
        self.m_period = 0.0
        self.m_array = Arr(0, 0.0)
        self.m_arraySize = 0
        self.m_alpha = 1.0
        self.m_arraySize = -1
        self.m_period = 1.0
    def _q_dtor(self):
        pass
    def OnInit(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_alpha = _fdiv(2.0, 1.0 + self.m_period)
    def OnCalculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
        if i > 0:
            self.m_array[i] = self.m_array[i - 1] + (self.m_alpha * (value - self.m_array[i - 1]))
        else:
            self.m_array[i] = value
        return self.m_array[i]

def OnInit():
    global _minmaxPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, vals, INDICATOR_DATA)
    _minmaxPeriod = MathMax(inpStoPeriod - 1, 1)
    iFast.OnInit(inpFastPeriod)
    iSlow.OnInit(inpSlowPeriod)
    iSignal.OnInit(inpSignPeriod)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevelOb)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpLevelOs)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic MACD (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignPeriod) + ',' + _str(inpStoPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_max, _s_OnCalculate_prev_min, _s_OnCalculate_prev_time
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    for i in range(limit, rates_total):
        if _s_OnCalculate_prev_time != time[i]:
            _s_OnCalculate_prev_time = time[i]
            start = i - inpStoPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = high[ArrayMaximum(high, start, _minmaxPeriod)]
            _s_OnCalculate_prev_min = low[ArrayMinimum(low, start, _minmaxPeriod)]
        prc = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            prc = close[i]
        elif _sw1 == PRICE_OPEN:
            prc = open[i]
        elif _sw1 == PRICE_HIGH:
            prc = high[i]
        elif _sw1 == PRICE_LOW:
            prc = low[i]
        elif _sw1 == PRICE_MEDIAN:
            prc = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            prc = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            prc = (high[i] + low[i] + close[i] + close[i]) / 4.0
        fastEma = iFast.OnCalculate(prc, i, rates_total)
        slowEma = iSlow.OnCalculate(prc, i, rates_total)
        max_ = (high[i] if (high[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (low[i] if (low[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        fastStoch = (_fdiv(fastEma - min_, max_ - min_) if (max_ != min_) else 0)
        slowStoch = (_fdiv(slowEma - min_, max_ - min_) if (max_ != min_) else 0)
        val[i] = 100.0 * (fastStoch - slowStoch)
        vals[i] = iSignal.OnCalculate(val[i], i, rates_total)
    return rates_total

# ---- global variables initialised from expressions
iFast = _alloc(CEma)
iFast.__init__()
iSlow = _alloc(CEma)
iSlow.__init__()
iSignal = _alloc(CEma)
iSignal.__init__()

# ---- static local variables
_s_OnCalculate_prev_time = 0
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticMACD(_MQL5Indicator):
    name = 'Stochastic MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStoPeriod': 45,  # Stochastic period
        'inpFastPeriod': 12,  # Fast period
        'inpSlowPeriod': 26,  # Slow period
        'inpSignPeriod': 9,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLevelOb': 10.0,  # Ovberbought level
        'inpLevelOs': -10.0,  # Ovbersold level
    }

