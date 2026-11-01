"""Adaptive ATR — converted from MQL5: MQL5 Indicators/Adaptive ATR/Adaptive ATR.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Adaptive ATR'}, 'levels': [], 'description': [], 'name': 'Adaptive ATR', 'source': 'MQL5 Indicators/Adaptive ATR/Adaptive ATR.mq5', 'folder': 'Adaptive ATR', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # period
val = Arr(0, 0.0)
m_fastEnd = 0.0
m_slowEnd = 0.0
m_period = 0

class sEfrStruct(MqlObject):
    _q_fields = ('price', 'difference', 'noise')
    def __init__(self, *args):
        self.price = 0.0
        self.difference = 0.0
        self.noise = 0.0

def OnInit():
    global m_fastEnd, m_period, m_slowEnd
    SetIndexBuffer(0, val, INDICATOR_DATA)
    m_period = (inpPeriod if (inpPeriod > 1) else 1)
    m_fastEnd = MathMax(m_period / 2.0, 1)
    m_slowEnd = m_period * 5
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adaptive ATR (' + _str(m_period) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize
    if _s_OnCalculate_m_arraySize < rates_total:
        _s_OnCalculate_m_arraySize = ArrayResize(_s_OnCalculate_m_array, rates_total + 500)
        if _s_OnCalculate_m_arraySize < rates_total:
            return 0
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _s_OnCalculate_m_array[i].price = (high[i] + low[i]) / 2.0
        _s_OnCalculate_m_array[i].difference = ((_s_OnCalculate_m_array[i].price - _s_OnCalculate_m_array[i - 1].price) if (i > 0) else 0)
        if _s_OnCalculate_m_array[i].difference < 0:
            _s_OnCalculate_m_array[i].difference *= -1.0
        signal = 0.0
        if i > m_period:
            signal = _s_OnCalculate_m_array[i].price - _s_OnCalculate_m_array[i - m_period].price
            if signal < 0:
                signal *= -1.0
            _s_OnCalculate_m_array[i].noise = _s_OnCalculate_m_array[i - 1].noise + _s_OnCalculate_m_array[i].difference - _s_OnCalculate_m_array[i - m_period].difference
        else:
            _s_OnCalculate_m_array[i].noise = _s_OnCalculate_m_array[i].difference
            k = 1
            while k < m_period and i >= k:
                _s_OnCalculate_m_array[i].noise += _s_OnCalculate_m_array[i - k].difference
                k += 1
        efratio = (_fdiv(signal, _s_OnCalculate_m_array[i].noise) if (_s_OnCalculate_m_array[i].noise != 0) else 1)
        averagePeriod = (((_fdiv(signal, _s_OnCalculate_m_array[i].noise) * (m_slowEnd - m_fastEnd)) + m_fastEnd) if (_s_OnCalculate_m_array[i].noise != 0) else m_period)
        val[i] = ((val[i - 1] + (_fdiv(2.0, 1.0 + averagePeriod) * (high[i] - low[i] - val[i - 1]))) if (i > 0) else (high[i] - low[i]))
        i += 1
    return rates_total

# ---- static local variables
_s_OnCalculate_m_array = Arr(0, 0, factory=sEfrStruct)
_s_OnCalculate_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdaptiveATR(_MQL5Indicator):
    name = 'Adaptive ATR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # period
    }

