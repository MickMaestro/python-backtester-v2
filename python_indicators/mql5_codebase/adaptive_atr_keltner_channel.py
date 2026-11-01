"""Adaptive ATR Keltner channel — converted from MQL5: MQL5 Indicators/Adaptive ATR Keltner channel/Adaptive ATR Keltner channel.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [9662683], 2: [11119017], 3: [11119017]}, 'widths': {1: 2}, 'styles': {1: 0, 2: 2, 3: 2}, 'labels': {1: 'SMA', 2: 'Channel up', 3: 'Channel down'}, 'levels': [], 'description': [], 'name': 'Adaptive ATR Keltner channel', 'source': 'MQL5 Indicators/Adaptive ATR Keltner channel/Adaptive ATR Keltner channel.mq5', 'folder': 'Adaptive ATR Keltner channel', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpMultiplier', 'py': 'inpMultiplier', 'param': 'inpMultiplier', 'type': 'double', 'default': 1.0, 'label': 'Channel width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
inpMultiplier = _input('inpMultiplier', 1.0)  # Channel width
val = Arr(0, 0.0)
chanup = Arr(0, 0.0)
chandn = Arr(0, 0.0)
atr = Arr(0, 0.0)
m_fastEnd = 0.0
m_slowEnd = 0.0
m_period = 0
ª_smaHandle = 0

class sEfrStruct(MqlObject):
    _q_fields = ('price', 'difference', 'noise')
    def __init__(self, *args):
        self.price = 0.0
        self.difference = 0.0
        self.noise = 0.0

def OnInit():
    global m_fastEnd, m_period, m_slowEnd, ª_smaHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, chanup, INDICATOR_DATA)
    SetIndexBuffer(2, chandn, INDICATOR_DATA)
    SetIndexBuffer(3, atr, INDICATOR_CALCULATIONS)
    m_period = (inpPeriod if (inpPeriod > 1) else 1)
    m_fastEnd = MathMax(m_period / 2.0, 1)
    m_slowEnd = m_period * 5
    ª_smaHandle = iMA(Symbol(), 0, m_period, 0, MODE_SMA, inpPrice)
    if not _checkHandle(ª_smaHandle, 'SMA'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adaptive ATR Keltner channel(' + _str(m_period) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_smaHandle, 0, 0, _copyCount, val) != _copyCount:
        return prev_calculated
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
        if val[i] == EMPTY_VALUE:
            val[i] = _price
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
        atr[i] = ((atr[i - 1] + (_fdiv(2.0, 1.0 + averagePeriod) * (high[i] - low[i] - atr[i - 1]))) if (i > 0) else (high[i] - low[i]))
        chanup[i] = val[i] + (inpMultiplier * atr[i])
        chandn[i] = val[i] - (inpMultiplier * atr[i])
        i += 1
    return rates_total

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__handles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__handles[i])
        ArrayResize(_s__checkHandle__handles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s_OnCalculate_m_array = Arr(0, 0, factory=sEfrStruct)
_s_OnCalculate_m_arraySize = -1
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdaptiveATRKeltnerChannel(_MQL5Indicator):
    name = 'Adaptive ATR Keltner channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpMultiplier': 1.0,  # Channel width
    }

