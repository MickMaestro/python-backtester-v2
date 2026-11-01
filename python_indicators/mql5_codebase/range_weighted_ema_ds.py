"""Range weighted EMA (ds) — converted from MQL5: MQL5 Indicators/Range weighted smoothed EMA/Range weighted EMA (ds).mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 17919, 7451452]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Range weighted smoothed EMA'}, 'levels': [], 'description': [], 'name': 'Range weighted EMA (ds)', 'source': 'MQL5 Indicators/Range weighted smoothed EMA/Range weighted EMA (ds).mq5', 'folder': 'Range weighted smoothed EMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ª_alpha = 0.0

class sRwEma(MqlObject):
    _q_fields = ('num', 'den', 'num2', 'den2', 'ema')
    def __init__(self, *args):
        self.num = 0.0
        self.den = 0.0
        self.num2 = 0.0
        self.den2 = 0.0
        self.ema = 0.0

def OnInit():
    global ª_alpha
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    ª_alpha = _fdiv(2.0, 1.0 + MathSqrt((inpPeriod if (inpPeriod > 1) else 1)))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range smoothed weighted EMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize
    if _s_OnCalculate_m_arraySize < rates_total:
        _res = ArrayResize(_s_OnCalculate_m_array, rates_total + 500)
        if _res <= rates_total:
            return prev_calculated
        _s_OnCalculate_m_arraySize = _res
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
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
        _weight = high[i] - low[i]
        if _weight == 0:
            _weight = Point()
        if i > 0:
            _s_OnCalculate_m_array[i].num = _s_OnCalculate_m_array[i - 1].num + (ª_alpha * ((_weight * _price) - _s_OnCalculate_m_array[i - 1].num))
            _s_OnCalculate_m_array[i].den = _s_OnCalculate_m_array[i - 1].den + (ª_alpha * (_weight - _s_OnCalculate_m_array[i - 1].den))
            _s_OnCalculate_m_array[i].num2 = _s_OnCalculate_m_array[i - 1].num2 + (ª_alpha * (_s_OnCalculate_m_array[i].num - _s_OnCalculate_m_array[i - 1].num2))
            _s_OnCalculate_m_array[i].den2 = _s_OnCalculate_m_array[i - 1].den2 + (ª_alpha * (_s_OnCalculate_m_array[i].den - _s_OnCalculate_m_array[i - 1].den2))
            _s_OnCalculate_m_array[i].ema = _s_OnCalculate_m_array[i - 1].ema + (ª_alpha * (_fdiv(_s_OnCalculate_m_array[i].num2, _s_OnCalculate_m_array[i].den2) - _s_OnCalculate_m_array[i - 1].ema))
        else:
            _s_OnCalculate_m_array[i].num2 = _weight * _price
            _s_OnCalculate_m_array[i].num = _s_OnCalculate_m_array[i].num2
            _s_OnCalculate_m_array[i].den2 = _weight
            _s_OnCalculate_m_array[i].den = _s_OnCalculate_m_array[i].den2
            _s_OnCalculate_m_array[i].ema = _price
        val[i] = _s_OnCalculate_m_array[i].ema
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_m_array = Arr(0, 0, factory=sRwEma)
_s_OnCalculate_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangeWeightedEMADs(_MQL5Indicator):
    name = 'Range weighted EMA (ds)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

