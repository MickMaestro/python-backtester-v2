"""RMA — converted from MQL5: MQL5 Indicators/RMA/RMA.mq5

RMA
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['RMA'], 'name': 'RMA', 'source': 'MQL5 Indicators/RMA/RMA.mq5', 'folder': 'RMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
_calcPeriod1 = 0
_calcPeriod2 = 0
_calcPeriod3 = 0

class sRmaStruct(MqlObject):
    _q_fields = ('price', 'summ1', 'summ2', 'summ3')
    def __init__(self, *args):
        self.price = 0.0
        self.summ1 = 0.0
        self.summ2 = 0.0
        self.summ3 = 0.0

def OnInit():
    global _calcPeriod1, _calcPeriod2, _calcPeriod3
    SetIndexBuffer(0, val)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    _calcPeriod1 = (inpPeriod if (inpPeriod > 1) else 1)
    _calcPeriod2 = 2 * _calcPeriod1
    _calcPeriod3 = 3 * _calcPeriod1
    IndicatorSetString(INDICATOR_SHORTNAME, 'RMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

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
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _s_OnCalculate_m_array[i].price = close[i]
        elif _sw1 == PRICE_OPEN:
            _s_OnCalculate_m_array[i].price = open[i]
        elif _sw1 == PRICE_HIGH:
            _s_OnCalculate_m_array[i].price = high[i]
        elif _sw1 == PRICE_LOW:
            _s_OnCalculate_m_array[i].price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _s_OnCalculate_m_array[i].price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _s_OnCalculate_m_array[i].price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _s_OnCalculate_m_array[i].price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _s_OnCalculate_m_array[i].price = 0.0
        if i > _calcPeriod1:
            _s_OnCalculate_m_array[i].summ1 = _s_OnCalculate_m_array[i - 1].summ1 + _s_OnCalculate_m_array[i].price - _s_OnCalculate_m_array[i - _calcPeriod1].price
        else:
            _s_OnCalculate_m_array[i].summ1 = _s_OnCalculate_m_array[i].price
            k = 1
            while k < _calcPeriod1 and i >= k:
                _s_OnCalculate_m_array[i].summ1 += _s_OnCalculate_m_array[i - k].price
                k += 1
        if i > _calcPeriod2:
            _s_OnCalculate_m_array[i].summ2 = _s_OnCalculate_m_array[i - 1].summ2 + _s_OnCalculate_m_array[i].price - _s_OnCalculate_m_array[i - _calcPeriod2].price
        else:
            _s_OnCalculate_m_array[i].summ2 = _s_OnCalculate_m_array[i].price
            k = 1
            while k < _calcPeriod2 and i >= k:
                _s_OnCalculate_m_array[i].summ2 += _s_OnCalculate_m_array[i - k].price
                k += 1
        if i > _calcPeriod3:
            _s_OnCalculate_m_array[i].summ3 = _s_OnCalculate_m_array[i - 1].summ3 + _s_OnCalculate_m_array[i].price - _s_OnCalculate_m_array[i - _calcPeriod3].price
        else:
            _s_OnCalculate_m_array[i].summ3 = _s_OnCalculate_m_array[i].price
            k = 1
            while k < _calcPeriod3 and i >= k:
                _s_OnCalculate_m_array[i].summ3 += _s_OnCalculate_m_array[i - k].price
                k += 1
        val[i] = _fdiv(_s_OnCalculate_m_array[i].summ3, float(_calcPeriod3)) - _fdiv(_s_OnCalculate_m_array[i].summ2, float(_calcPeriod2)) + _fdiv(_s_OnCalculate_m_array[i].summ1, float(_calcPeriod1))
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_m_array = Arr(0, 0, factory=sRmaStruct)
_s_OnCalculate_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RMA(_MQL5Indicator):
    name = 'RMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

