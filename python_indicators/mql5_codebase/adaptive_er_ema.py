"""Adaptive ER EMA — converted from MQL5: MQL5 Indicators/Adaptive efficiency ratio EMA/Adaptive ER EMA.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [6908265, 7451452, 9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Adaptive EMA'}, 'levels': [], 'description': [], 'name': 'Adaptive ER EMA', 'source': 'MQL5 Indicators/Adaptive efficiency ratio EMA/Adaptive ER EMA.mq5', 'folder': 'Adaptive efficiency ratio EMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
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
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    m_period = (inpPeriod if (inpPeriod > 1) else 1)
    m_fastEnd = MathMax(m_period / 2.0, 1)
    m_slowEnd = m_period * 5
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adaptive EMA (' + _str(m_period) + ')')
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
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        _s_OnCalculate_m_array[i].price = _price
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
        val[i] = ((val[i - 1] + (_fdiv(2.0, 1.0 + averagePeriod) * (_price - val[i - 1]))) if (i > 0) else _price)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return rates_total

# ---- static local variables
_s_OnCalculate_m_array = Arr(0, 0, factory=sEfrStruct)
_s_OnCalculate_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdaptiveEREMA(_MQL5Indicator):
    name = 'Adaptive ER EMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

