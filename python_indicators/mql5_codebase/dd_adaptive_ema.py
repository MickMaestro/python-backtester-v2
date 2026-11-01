"""DD adaptive EMA — converted from MQL5: MQL5 Indicators/Dual differentiator adaptive EMA/DD adaptive EMA.mq5

Dual differentiator adaptive EMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 32768]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'EMA'}, 'levels': [], 'description': ['Dual differentiator adaptive EMA'], 'name': 'DD adaptive EMA', 'source': 'MQL5 Indicators/Dual differentiator adaptive EMA/DD adaptive EMA.mq5', 'folder': 'Dual differentiator adaptive EMA', 'inputs': [{'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}, {'mql': 'inpFilter', 'py': 'inpFilter', 'param': 'inpFilter', 'type': 'double', 'default': 5.0, 'label': 'Filter', 'sinput': False}, {'mql': 'inpMinimal', 'py': 'inpMinimal', 'param': 'inpMinimal', 'type': 'double', 'default': 0.0, 'label': 'Minimal test value', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
inpFilter = _input('inpFilter', 5.0)  # Filter
inpMinimal = _input('inpMinimal', 0.0)  # Minimal test value
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
_minimal = 0.0

class iDualDifferentiatorStruct(MqlObject):
    _q_fields = ('price', 'smooth', 'detrender', 'period', 'Q1', 'Q2', 'I1', 'I2', 'JI', 'JQ', 'res')
    def __init__(self, *args):
        self.price = 0.0
        self.smooth = 0.0
        self.detrender = 0.0
        self.period = 0.0
        self.Q1 = 0.0
        self.Q2 = 0.0
        self.I1 = 0.0
        self.I2 = 0.0
        self.JI = 0.0
        self.JQ = 0.0
        self.res = 0.0

def OnInit():
    global _minimal
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    _minimal = inpMinimal * Point()
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dual differentiator adaptive EMA (' + _str(inpFilter) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
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
        _phase = iDualDifferentiator(_price, inpFilter, _minimal, i, rates_total)
        val[i] = ((val[i - 1] + (_fdiv(2.0, 1.0 + _phase) * (_price - val[i - 1]))) if (i > 0) else _price)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return rates_total

def iDualDifferentiator(price, filter_, minValue, i, bars):
    global _s_iDualDifferentiator_m_arraySize
    if _s_iDualDifferentiator_m_arraySize < bars:
        _s_iDualDifferentiator_m_arraySize = ArrayResize(_s_iDualDifferentiator_m_array, bars + 500)
        if _s_iDualDifferentiator_m_arraySize < bars:
            return price
    _s_iDualDifferentiator_m_array[i].price = price
    if i < 6:
        _s_iDualDifferentiator_m_array[i].JQ = 0.0
        _s_iDualDifferentiator_m_array[i].JI = _s_iDualDifferentiator_m_array[i].JQ
        _s_iDualDifferentiator_m_array[i].I2 = _s_iDualDifferentiator_m_array[i].JI
        _s_iDualDifferentiator_m_array[i].I1 = _s_iDualDifferentiator_m_array[i].I2
        _s_iDualDifferentiator_m_array[i].Q2 = _s_iDualDifferentiator_m_array[i].I1
        _s_iDualDifferentiator_m_array[i].Q1 = _s_iDualDifferentiator_m_array[i].Q2
        _s_iDualDifferentiator_m_array[i].res = _s_iDualDifferentiator_m_array[i].Q1
        _s_iDualDifferentiator_m_array[i].period = _s_iDualDifferentiator_m_array[i].res
        _s_iDualDifferentiator_m_array[i].detrender = price
        _s_iDualDifferentiator_m_array[i].smooth = _s_iDualDifferentiator_m_array[i].detrender
        return 0.0
    _s_iDualDifferentiator_m_array[i].smooth = ((4.0 * _s_iDualDifferentiator_m_array[i].price) + (3.0 * _s_iDualDifferentiator_m_array[i - 1].price) + (2.0 * _s_iDualDifferentiator_m_array[i - 2].price) + _s_iDualDifferentiator_m_array[i - 3].price) / 10.0
    _s_iDualDifferentiator_m_array[i].detrender = ((0.0962 * _s_iDualDifferentiator_m_array[i].smooth) + (0.5769 * _s_iDualDifferentiator_m_array[i - 2].smooth) - (0.5769 * _s_iDualDifferentiator_m_array[i - 4].smooth) - (0.0962 * _s_iDualDifferentiator_m_array[i - 6].smooth)) * ((0.075 * _s_iDualDifferentiator_m_array[i - 1].period) + 0.54)
    _s_iDualDifferentiator_m_array[i].Q1 = ((0.0962 * _s_iDualDifferentiator_m_array[i].detrender) + (0.5769 * _s_iDualDifferentiator_m_array[i - 2].detrender) - (0.5769 * _s_iDualDifferentiator_m_array[i - 4].detrender) - (0.0962 * _s_iDualDifferentiator_m_array[i - 6].detrender)) * ((0.075 * _s_iDualDifferentiator_m_array[i - 1].period) + 0.54)
    _s_iDualDifferentiator_m_array[i].I1 = _s_iDualDifferentiator_m_array[i - 3].detrender
    _s_iDualDifferentiator_m_array[i].JI = ((0.0962 * _s_iDualDifferentiator_m_array[i].I1) + (0.5769 * _s_iDualDifferentiator_m_array[i - 2].I1) - (0.5769 * _s_iDualDifferentiator_m_array[i - 4].I1) - (0.0962 * _s_iDualDifferentiator_m_array[i - 6].I1)) * ((0.075 * _s_iDualDifferentiator_m_array[i - 1].period) + 0.54)
    _s_iDualDifferentiator_m_array[i].JQ = ((0.0962 * _s_iDualDifferentiator_m_array[i].Q1) + (0.5769 * _s_iDualDifferentiator_m_array[i - 2].Q1) - (0.5769 * _s_iDualDifferentiator_m_array[i - 4].Q1) - (0.0962 * _s_iDualDifferentiator_m_array[i - 6].Q1)) * ((0.075 * _s_iDualDifferentiator_m_array[i - 1].period) + 0.54)
    _s_iDualDifferentiator_m_array[i].I2 = (0.15 * (_s_iDualDifferentiator_m_array[i].I1 - _s_iDualDifferentiator_m_array[i].JQ)) + (0.85 * _s_iDualDifferentiator_m_array[i - 1].I2)
    _s_iDualDifferentiator_m_array[i].Q2 = (0.15 * (_s_iDualDifferentiator_m_array[i].Q1 + _s_iDualDifferentiator_m_array[i].JI)) + (0.85 * _s_iDualDifferentiator_m_array[i - 1].Q2)
    temp = (_s_iDualDifferentiator_m_array[i].Q2 * (_s_iDualDifferentiator_m_array[i].I2 - _s_iDualDifferentiator_m_array[i - 1].I2)) - (_s_iDualDifferentiator_m_array[i].I2 * (_s_iDualDifferentiator_m_array[i].Q2 - _s_iDualDifferentiator_m_array[i - 1].Q2))
    _s_iDualDifferentiator_m_array[i].period = _s_iDualDifferentiator_m_array[i - 1].period
    if temp > minValue:
        _s_iDualDifferentiator_m_array[i].period = _fdiv(6.2832 * ((_s_iDualDifferentiator_m_array[i].I2 * _s_iDualDifferentiator_m_array[i].I2) + (_s_iDualDifferentiator_m_array[i].Q2 * _s_iDualDifferentiator_m_array[i].Q2)), temp)
    _s_iDualDifferentiator_m_array[i].period = MathMin(_s_iDualDifferentiator_m_array[i].period, 1.5 * _s_iDualDifferentiator_m_array[i - 1].period)
    _s_iDualDifferentiator_m_array[i].period = MathMax(_s_iDualDifferentiator_m_array[i].period, 0.67 * _s_iDualDifferentiator_m_array[i - 1].period)
    _s_iDualDifferentiator_m_array[i].period = MathMin(MathMax(_s_iDualDifferentiator_m_array[i].period, 6), 50)
    _s_iDualDifferentiator_m_array[i].period = (0.15 * _s_iDualDifferentiator_m_array[i].period) + (0.85 * _s_iDualDifferentiator_m_array[i - 1].period)
    alpha = _fdiv(2.0, 1.0 + filter_)
    _s_iDualDifferentiator_m_array[i].res = _s_iDualDifferentiator_m_array[i - 1].res + (alpha * (_s_iDualDifferentiator_m_array[i].period - _s_iDualDifferentiator_m_array[i - 1].res))
    return _s_iDualDifferentiator_m_array[i].res

# ---- static local variables
_s_iDualDifferentiator_m_array = Arr(0, 0, factory=iDualDifferentiatorStruct)
_s_iDualDifferentiator_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DDAdaptiveEMA(_MQL5Indicator):
    name = 'DD adaptive EMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
        'inpFilter': 5.0,  # Filter
        'inpMinimal': 0.0,  # Minimal test value
    }

